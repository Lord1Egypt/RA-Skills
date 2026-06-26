import requests
import json
import os

BACKEND_URL = os.environ.get('BACKEND_URL', 'https://javatoarktsapi.uctoo.com')

print("Testing UCTOO API Client")
print("========================")
print(f"Backend URL: {BACKEND_URL}")
print()

# Test 1: Login
print("Test 1: Login with demo / 123456")
print("-" * 50)

login_url = f"{BACKEND_URL}/api/uctoo/auth/login"
login_data = {"username": "demo", "password": "123456"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(login_url, json=login_data, headers=headers, timeout=60)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 200 and 'data' in result:
            access_token = result['data'].get('access_token')
            if access_token:
                print(f"\n✅ Login successful! Access token obtained.")
                print(f"Token: {access_token[:50]}...")
            else:
                print("\n⚠️  Login response but no access token found")
        else:
            print(f"\n⚠️  Login failed: {result.get('message', 'Unknown error')}")
    else:
        print(f"\n❌ HTTP Error: {response.status_code}")
        
except Exception as e:
    print(f"\n❌ Exception: {str(e)}")

print()
print("=" * 50)
print("Test completed!")
