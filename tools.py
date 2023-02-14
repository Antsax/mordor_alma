import numpy as np
import pandas as pd
import plotly.express as plx

def clean_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    column_names = [column for column in dataframe]
    for column in column_names:
        dataframe[column] = dataframe[column].str.strip()

    dataframe = dataframe.drop_duplicates()

    dataframe = dataframe.replace('', np.nan)
    dataframe = dataframe.dropna()

    return dataframe


def most_occurences(dataframe: pd.DataFrame, id: str) -> dict:
    occurences = {}
    for item in dataframe[id]:
        if item not in occurences:
            occurences[item] = 1
        else:
            occurences[item] += 1
    occurences = dict(sorted(occurences.items(), key=lambda item: item[1]))
    return occurences


def replace_id_with_name(dictionary: dict, comparable_dataframe: pd.DataFrame, df_id: str, desired_field: str, column_name: str) -> pd.DataFrame:
    occurences = {}
    for key in dictionary.keys():
        name = list(comparable_dataframe.loc[comparable_dataframe[df_id] == key, desired_field])
        if name != []:
            name = name[0]
            if name not in occurences:
                occurences[name] = dictionary[key]
            else:
                occurences[name] += dictionary[key]
    occurences = dict(sorted(occurences.items(), key=lambda item: item[1], reverse=True))
    occurences_dataframe = pd.DataFrame(occurences.items(), columns=[desired_field, column_name])
    return occurences_dataframe


def set_merchants(regions_with_cities: pd.DataFrame, all_regions: pd.DataFrame, cities_dict: dict, all_cities: pd.DataFrame):
    num_of_merchants = {}
    for region in regions_with_cities['MIDDLE_EARTH_REGION']:
        num_of_merchants[region] = 0
        region_ids = list(all_regions.loc[all_regions['MIDDLE_EARTH_REGION'] == region, 'MORDOR_ID'])
        for _, city in all_cities.iterrows():
            if city['MORDOR_ID'] in region_ids:
                amount_of_stores_in_city = cities_dict.get(city['CITY_ID'])
                if amount_of_stores_in_city is not None:
                    num_of_merchants[region] += amount_of_stores_in_city
    regions_with_cities['NUM_OF_MERCHANTS'] = regions_with_cities['MIDDLE_EARTH_REGION'].map(num_of_merchants)


def set_regions(cities_with_stores: pd.DataFrame, all_cities: pd.DataFrame, all_regions: pd.DataFrame):
    name_of_regions = {}
    for city_name in cities_with_stores['CITY_NAME']:
        mordor_id = all_cities.loc[all_cities['CITY_NAME'] == city_name, 'MORDOR_ID'].iloc[0]
        name_of_regions[city_name] = all_regions.loc[all_regions['MORDOR_ID'] == mordor_id, 'MIDDLE_EARTH_REGION'].iloc[0]
    cities_with_stores['MIDDLE_EARTH_REGION'] = cities_with_stores['CITY_NAME'].map(name_of_regions)


def create_nested_directory(regions: pd.DataFrame, cities: pd.DataFrame, stores: pd.DataFrame):
    nested_directory = {}
    for region in regions['MIDDLE_EARTH_REGION']:
        nested_directory[region] = {}
    
    for _, city in cities.iterrows():
        mordor_region = check_region_name(regions, city['MORDOR_ID'])
        if mordor_region is None:
            continue
        nested_directory[mordor_region][city['CITY_NAME']] = []
        
    for _, merchant in stores.iterrows():
        if cities['CITY_ID'].eq(merchant['CITY_ID']).any():
            city_id = cities.loc[cities['CITY_ID'] == merchant['CITY_ID'], 'MORDOR_ID'].iloc[0]
            mordor_region = check_region_name(regions, city_id)
            if mordor_region is None:
                continue
            city_name = cities.loc[cities['CITY_ID'] == merchant['CITY_ID'], 'CITY_NAME'].iloc[0]
            nested_directory[mordor_region][city_name].append(merchant['MERCHANT_NAME'])

    return nested_directory


def check_region_name(regions: pd.DataFrame, city_id: str):
    if regions['MORDOR_ID'].eq(city_id).any():
        mordor_region = regions.loc[regions['MORDOR_ID'] == city_id, 'MIDDLE_EARTH_REGION'].iloc[0]
        return mordor_region
    return None


def draw_graph(dataframe: pd.DataFrame):
    fig = plx.scatter(dataframe, x='NUM_OF_CITIES', y='NUM_OF_MERCHANTS', trendline='ols', text='MIDDLE_EARTH_REGION')
    fig.update_traces(textposition='top center')
    fig.write_image("mordor_scatterplot.png")
    fig.show()
    
