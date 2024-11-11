import pandas as pd
import requests

# Your OpenCage API key
opencage_api_key = 'your_api_key'

# Function to get GPS coordinates from OpenCage Geocoding API
def get_location_details_opencage(address):
    # Append ", India" to the address to force the geocoder to prioritize India
    address_with_country = f"{address}, India"
    url = f"https://api.opencagedata.com/geocode/v1/json?q={address}&key={opencage_api_key}"
    
    print(f"Querying OpenCage API with URL: {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        result = response.json()
        # Print the full response to inspect it
        print(f"Full response for address '{address}': {result}")
        if result['results']:
            latitude = result['results'][0]['geometry']['lat']
            longitude = result['results'][0]['geometry']['lng']
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

# Apply geocoding to each address using OpenCage
df['Latitude'] = None
df['Longitude'] = None

for index, row in df.iterrows():
    address = row['Full Address']
    latitude, longitude = get_location_details_opencage(address)
    df.at[index, 'Latitude'] = latitude
    df.at[index, 'Longitude'] = longitude
    
# Drop the 'Full Address' column and keep only GPS coordinates
output_file = 'addresses_with_gps_coordinates_opencage.xlsx'

# Save the results to an Excel file
df.to_excel(output_file, index=False)

print(f"Geocoding completed and saved to {output_file}")
