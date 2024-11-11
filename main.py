import pandas as pd
import requests

# Your Azure Maps API key
azure_maps_api_key = 'your_azure_key'

# Function to get GPS coordinates from Azure Maps Geocoding API
def get_location_details_azure_maps(address):
    # Append ", India" to the address to force the geocoder to prioritize India
    address_with_country = f"{address}, India"
    url = f"https://atlas.microsoft.com/search/address/json?api-version=1.0&subscription-key={azure_maps_api_key}&query={address_with_country}"
    
    print(f"Querying Azure Maps API with URL: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        # Print the full response to inspect it
        print(f"Full response for address '{address}': {result}")
        if result['results']:
            latitude = result['results'][0]['position']['lat']
            longitude = result['results'][0]['position']['lon']
            return latitude, longitude
        else:
            print(f"No coordinates found for address: {address}")
            return None, None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None, None

# Read the addresses from your Excel file
input_file = 'addresses.xlsx'
df = pd.read_excel(input_file)

# Assuming the 'Address' column contains the full address
df['Full Address'] = df['Address']

# Apply geocoding to each address using Azure Maps
df['Latitude'] = None
df['Longitude'] = None

for index, row in df.iterrows():
    address = row['Full Address']
    latitude, longitude = get_location_details_azure_maps(address)
    df.at[index, 'Latitude'] = latitude
    df.at[index, 'Longitude'] = longitude
    
# Drop the 'Full Address' column and keep only GPS coordinates
output_file = 'addresses_with_gps_coordinates_azure_maps.xlsx'

# Save the results to an Excel file
df.to_excel(output_file, index=False)

print(f"Geocoding completed and saved to {output_file}")
