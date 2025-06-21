import re
import numpy as np
import pandas as pd


building_condition_map = {
    'Good': 3, 
    'As new': 1, 
    'To be done up': 5, 
    'Just renovated': 2, 
    'To renovate': 4,
    'To restore': 6, 
}

yes_no_nan_mapping = {
    'Yes': 1,
    'No': 0,  
}

connected_mapping = {
    'Connected': 1,
    'Not connected': 0
}

energy_class_mapping = {
    'B': 4, 
    'C': 5, 
    'E': 7, 
    'F': 8, 
    'A': 3, 
    'D': 6, 
    'A+': 2, 
    'A++': 1
    }

kitchen_type_map = {
    'Installed': 3, 
    'Hyper equipped': 1, 
    'USA installed': 4, 
    'Semi equipped': 5,
    'Not installed': 6, 
    'USA hyper equipped': 2
}

heating_type_map = {
    'Fuel oil': 2, 
    'Gas': 1, 
    'Electric': 3, 
    'Pellet': 4, 
    'Wood': 5, 
    'Carbon': 6
}

planning_permission_map = {
    'Yes' : 1, 
    np.nan: 0
}

flood_map = {
    'zone' : 1, 
    np.nan: 0
}

gscore_map = {
    'A' : 1, 
    'B': 2, 
    'C': 3, 
    'D': 4
}

designated_land_map = {
    'Living area (residential, urban or rural)' : 1, 
    'Another type of area': 2, 
    'Extended residential area': 3, 
    'Residential recreation area': 4,
    'Residential area with cultural historical aesthetic value': 5, 
    'Area of landscape interest': 6,
    'Farming area': 7, 
    'Green area': 8, 
    'Residential park': 9, 
    'Industrial area': 10, 
    'Park area': 11, 
    'Leisure area': 12, 
    'Forest area': 13,
    'Natural area': 14
}

## Clean raw data ## 
def clean_data_column(data_list: list):
    """ Expand and clean data column """
    results = {}
    for i in data_list:
        # Dealing with lists that contains one item
        if len(i) == 1:
            words = i[0].split()
            if len(words) > 1:
                key = ' '.join(words[:-1])
                value = words[-1]
        # Dealing with lists that contains 2 items
        elif len(i) == 2:
            keys = i[0].split()
            key = ' '.join(keys)
            value = ''.join(i[1:])
        # Dealing with lists that contains 3 items
        elif len(i) == 3:
            key = i[0]
            value = ' '.join(i[1:])
        # Dealing with lists that contains 4 items
        elif len(i) == 4:
            key = i[0]
            value = ' '.join(i[1:])
        else:
            key = 'None'
            value = 'None'
            
        results[key] = value
    return results


def calculate_price(text_string:str):
    price_pattern = re.findall(r'\d+', text_string)
    numbers = [float(p) for p in price_pattern]
    return np.mean(numbers)


## Transform categorical to numerical values ## 
def extract_digits(text_string:str):
    pattern = re.findall(r'\d+', text_string)
    return pattern[0]

def transform_categorical_to_numerical(df:pd.DataFrame) -> pd.DataFrame:

    # Change all 'Not specified' values to NaN
    df.replace('Not specified', np.nan, inplace=True)

    # Price
    df['price'] = df['price'].apply(calculate_price)
    df['price'] = df['price'].astype(float)

    # Construction Year
    df['construction year'] = df['construction year'].apply(lambda x: int(x) if pd.notnull(x) else pd.NA)
    df['construction year'] = df['construction year'].astype('category')

    # Asbestos certificate
    df['asbestos certificate'] = df['asbestos certificate'].map(yes_no_nan_mapping)
    df['asbestos certificate'] = df['asbestos certificate'].astype('category')

    # Shared building
    df['shared building'] = df['shared building'].map(yes_no_nan_mapping)
    df['shared building'] = df['shared building'].astype('category')

    # Bedrooms
    df['bedrooms'] = df['bedrooms'].astype('category')

    # Bathrooms
    df['bathrooms'] = df['bathrooms'].astype(float)

    # Toilets
    df['toilets'] = df['toilets'].astype(float)

    # Building condition
    df['building condition'] = df['building condition'].map(building_condition_map)
    df['building condition'] = df['building condition'].astype('category')

    # Living area
    df['living area'] = df['living area'].apply(lambda x: extract_digits(x) if isinstance(x, str) else np.nan)
    df['living area'] = df['living area'].astype(float)

    # Possible priority purchase right
    df['possible priority purchase right'] = df['possible priority purchase right'].map(yes_no_nan_mapping)
    df['possible priority purchase right'] = df['possible priority purchase right'].astype('category')

    # Double glazing
    df['double glazing'] = df['double glazing'].map(yes_no_nan_mapping)
    df['double glazing'] = df['double glazing'].astype('category')

    # Inspection report of the electrical installation
    df['inspection report of the electrical installation'] = df['inspection report of the electrical installation'].map(yes_no_nan_mapping)
    df['inspection report of the electrical installation'] = df['inspection report of the electrical installation'].astype('category')

    # Subdivision permit
    df['subdivision permit'] = df['subdivision permit'].map(yes_no_nan_mapping)
    df['subdivision permit'] =  df['subdivision permit'].astype('category')

    # Proceedings for breach of planning regulations
    df['proceedings for breach of planning regulations'] = df['proceedings for breach of planning regulations'].map(yes_no_nan_mapping)
    df['proceedings for breach of planning regulations'] = df['proceedings for breach of planning regulations'].astype('category')
    
    # Sewer network connection
    df['sewer network connection'] = df['sewer network connection'].map(connected_mapping)
    df['sewer network connection'] = df['sewer network connection'].astype('category')

    # Energy class
    df['energy class'] = df['energy class'].map(energy_class_mapping)
    df['energy class'] =  df['energy class'].astype('category')

    # Primary energy consumption
    df['primary energy consumption'] = df['primary energy consumption'].apply(lambda x: extract_digits(x) if isinstance(x, str) else np.nan)
    df['primary energy consumption'] = df['primary energy consumption'].astype(float)   

    # Planning permission obtained
    df['planning permission obtained'] = df['planning permission obtained'].astype('category')

    # Non-flood zone
    df['non-flood zone'] = df['non-flood zone'].map(flood_map)
    df['non-flood zone'] = df['non-flood zone'].astype('category')

    # G-score
    df['g-score'] = df['g-score'].map(gscore_map)
    df['g-score'] = df['g-score'].astype('category')

    # Surface of the plot
    df['surface of the plot'] = df['surface of the plot'].apply(lambda x: extract_digits(x) if isinstance(x, str) else np.nan)
    df['surface of the plot'] = df['surface of the plot'].astype(float)

    # Designated land use
    df['designated land use'] = df['designated land use'].map(designated_land_map)
    df['designated land use'] = df['designated land use'].astype('category')

  
    # Planning permission obtained
    df['planning permission obtained'] = df['planning permission obtained'].map(planning_permission_map) 
    df['planning permission obtained'] = df['planning permission obtained'].astype('category')

    return df 