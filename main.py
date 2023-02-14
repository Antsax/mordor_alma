import tools
import json
import pandas as pd

MORDOR_CITIES = "./Data/mordor_cities.json"
MORDOR_REGIONS = "./Data/mordor_regions.json"
MORDOR_STORES = "./Data/mordor_stores.json"

cities = tools.clean_data(pd.read_json(MORDOR_CITIES))
regions = tools.clean_data(pd.read_json(MORDOR_REGIONS))
stores = tools.clean_data(pd.read_json(MORDOR_STORES))

regions_with_cities_dict = tools.most_occurences(cities, 'MORDOR_ID')
cities_with_stores_dict = tools.most_occurences(stores, 'CITY_ID')

regions_with_cities = tools.replace_id_with_name(regions_with_cities_dict, regions, 'MORDOR_ID', 'MIDDLE_EARTH_REGION', 'NUM_OF_CITIES')
cities_with_stores = tools.replace_id_with_name(cities_with_stores_dict, cities, 'CITY_ID', 'CITY_NAME', 'NUM_OF_MERCHANTS')

tools.set_merchants(regions_with_cities, regions, cities_with_stores_dict, cities)
tools.set_regions(cities_with_stores, cities, regions)

print("The regions with the most cities are: \n%s\n" % regions_with_cities.head().to_string(index=False))
print("The cities with the most merchants are: \n%s\n" % cities_with_stores.head().to_string(index=False))
print("There are a total of %i cities in the regions of Middle Earth" % regions_with_cities['NUM_OF_CITIES'].sum())
print("and %i merchants across all of the cities\n" % cities_with_stores['NUM_OF_MERCHANTS'].sum())

print("There is an average of %.2f (median %.2f) cities per region" % (regions_with_cities['NUM_OF_CITIES'].mean(), regions_with_cities['NUM_OF_CITIES'].median()))
print("and an average of %.2f (median %.2f) merchants per city\n" % (cities_with_stores['NUM_OF_MERCHANTS'].mean(), cities_with_stores['NUM_OF_MERCHANTS'].median()))

nested_directory = tools.create_nested_directory(regions, cities, stores)
print("The nested dictionary is: \n%s" % json.dumps(nested_directory, indent=4, ensure_ascii=False))

tools.draw_graph(regions_with_cities)
