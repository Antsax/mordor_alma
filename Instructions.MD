# Instructions

Try to complete the following problems with python and it's frameworks. Preferred method is either a python script or a jupyter notebook.


You are given three JSON files containing:
- Regions in Middle Earth
- Cities in those regions
- Merchants in cities.

### How to return:
- Jupyter notebook or a python script with the data folder included.
- If you use any external packages make sure to include a requirements.txt file with the dependencies.

## Part 1: Quality of the data

Look into the data and see if it has some abnormal things. Some examples:
- Does the data need to be cleaned for unwanted characters, duplicates, whitespace etc.?
- Does a same store exist in multiple cities/regions?
- Are there are regions/cities/merchants that have no relations?


## Part 2: Insights

Look at the data and give some insights of it. Some examples:
- Which regions have the most cities?
- Which cities have the most merchants? 
- Does number of cities directly correlate with the number of merchants?
- Can you find any outliers?


## Part 3: Data mangling

Use python and pythons basic datastructures to present the data as a nested dictionary. Result should be in the format of:

*ALL IDENTIFYING FIELDS CAN BE INCLUDED (CITY_ID, MORDOR_ID)*

    { Region:
        { City: [Merchants....],
          City2: [Merchants....]
        },
      Region2:
        {....
        },
      Region3.....
    }

or something like

    { Region:
        {"MORDOR_ID": do43ijhi9fds,
         "Cities":  [{CITY_ID: 432842394,
                      "MERCHANTS": [Merchant_data....]},
                     {CITY_ID: dsad89734,
                      "MERCHANTS": [Merchant_data....]}
                    ],
        },
      Region2:
        {....
        },
      Region3.....
    }

## Part 4: Bonus points:

Give us some kind of visualisations from the data. Feel free to use pandas/seaborn/excel/pen and paper or any other tool youre familiar. Something simple is more than enough!