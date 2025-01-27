import json
import pandas as pd

def generate_geojson(input_csv, output_js, variable_name):
    """
    Generate GeoJSON from a CSV file and save it as a JavaScript file.
    
    Args:
    - input_csv (str): Path to the input CSV file.
    - output_js (str): Path to the output JavaScript file.
    - variable_name (str): JavaScript variable name to store the GeoJSON data.
    """
    # Load the CSV file into a DataFrame
    try:
        df = pd.read_csv(input_csv)
    except Exception as e:
        print(f"Error loading {input_csv}: {e}")
        return

    # Ensure necessary columns exist
    required_columns = ['longitude', 'latitude', 'birthplace', 'movie']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: Missing columns in {input_csv}: {missing_columns}")
        return

    # Fill missing values
    df.fillna({'birthplace': 'Unknown', 'movie': 'Unknown'}, inplace=True)

    # Create GeoJSON structure
    geo_data = {
        "type": "FeatureCollection",
        "features": []
    }

    # Iterate through the DataFrame and populate GeoJSON features
    for _, row in df.iterrows():
        try:
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [row["longitude"], row["latitude"]]  # Ensure [lng, lat] format
                },
                "properties": {
                    "birthplace": row['birthplace'],
                    "movie": row['movie']
                }
            }
            geo_data["features"].append(feature)
        except KeyError as e:
            print(f"Skipping row due to missing data: {e}")

    # Write GeoJSON to a JavaScript file
    try:
        with open(output_js, 'w') as geojson_file:
            geojson_file.write(f"const {variable_name} = ")
            json.dump(geo_data, geojson_file, indent=2)
        print(f"GeoJSON data saved to {output_js}")
    except Exception as e:
        print(f"Error writing {output_js}: {e}")


# Generate GeoJSON for the first dataset
generate_geojson('final_movies_with_coordinates.csv', 'geo-dataAGAIN.js', 'infoData')

# Generate GeoJSON for the second dataset
generate_geojson('BFI_final_movies_with_coordinates.csv', 'bfi-geo-data.js', 'bfiInfoData')
