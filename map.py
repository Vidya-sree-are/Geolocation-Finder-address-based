import requests

def get_mapmyindia_token(client_id, client_secret):
    url = "https://outpost.mapmyindia.com/api/security/oauth/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
    else:
        print("Failed to get access token:", response.status_code)
        return None

client_id = '96dHZVzsAuuL1o46Qv2yxIrLRs5PSk7N8OMNkJj0bNSTsIH6AFFLvqFJeut-iJxSTQg2_yIubo0PB4azzuf7jA=='  # Replace with your MapMyIndia client_id
client_secret = 'lrFxI-iSEg_IMxmq3N40NFgWQ9PJgUxiLn3a7VjDIukZwbxaGEyGXuC56wBN-lo3uzX5TUJN7xralHchiL6lL5vyO2iVRuEl'  # Replace with your MapMyIndia client_secret
access_token = get_mapmyindia_token(client_id, client_secret)

if access_token:
    print("Access Token:", access_token)

def geocode_address(address, access_token):
    base_url = "https://apis.mapmyindia.com/advancedmaps/v1/{access_token}/geo_code"
    params = {
        'addr': address
    }
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    response = requests.get(base_url.format(access_token=access_token), params=params, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Geocoding failed:", response.status_code)
        return None

# Replace with the address you want to geocode
address = "Connaught Place, New Delhi"
geocoded_data = geocode_address(address, access_token)

if geocoded_data:
    print(geocoded_data)
