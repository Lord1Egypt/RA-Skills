"""
Weather Skill - Get Current Temperature
Powered by OpenClaw + SkillPay
SKILL_ID: 53e00e19-e973-4011-8707-ac7298decedb
"""
import json
import requests
import re
from urllib.parse import quote
import os

# SkillPay Configuration
SKILLPAY_API_KEY = os.environ.get("SKILLPAY_API_KEY", "sk_93c5ff38cc3e6112623d361fffcc5d1eb1b5844eac9c40043b57c0e08f91430e")
SKILLPAY_API_URL = os.environ.get("SKILLPAY_API_URL", "https://skillpay.me/api/v1/billing")
SKILL_ID = os.environ.get("SKILLPAY_SKILL_ID", "53e00e19-e973-4011-8707-ac7298decedb")
PRICE_USDT = "0.001"
SKILL_NAME = "Weather Query"

def charge_user(user_id: str) -> dict:
    """
    Charge user via SkillPay before providing the service.
    """
    if not SKILLPAY_API_KEY or not SKILL_ID:
        return {"success": True, "demo": True, "error": "SKILLPAY not configured"}

    try:
        payload = {
            "user_id": user_id,
            "skill_id": SKILL_ID,
            "amount": float(PRICE_USDT)
        }
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": SKILLPAY_API_KEY
        }
        response = requests.post(f"{SKILLPAY_API_URL}/charge", json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return {"success": True, "balance": data.get("balance")}
            else:
                return {"success": False, "balance": data.get("balance"), "payment_url": data.get("payment_url")}
        else:
            return {"success": False, "error": response.text}
    except Exception as e:
        return {"success": True, "error": str(e), "demo": True}

def get_weather(city: str) -> dict:
    try:
        city = city.strip()
        city = re.sub(r'[^\w\s]', '', city)
        url = f"https://wttr.in/{quote(city)}?format=j1"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data.get('current_condition', [{}])[0]
            return {
                "city": city,
                "temperature": f"{current.get('temp_C', 'N/A')}°C",
                "feels_like": f"{current.get('FeelsLikeC', 'N/A')}°C",
                "condition": current.get('weatherDesc', [{}])[0].get('value', 'N/A'),
                "humidity": f"{current.get('humidity', 'N/A')}%",
                "wind": f"{current.get('windspeedKmph', 'N/A')} km/h",
                "uv_index": current.get('UVIndex', 'N/A'),
                "visibility": f"{current.get('visibility', 'N/A')} km"
            }
        else:
            return {"error": f"Could not get weather for {city}"}
    except Exception as e:
        return {"error": str(e)}

def handle(input_text: str, user_id: str = "default") -> dict:
    city = extract_city(input_text)
    if not city:
        return {
            "error": "Please provide a city name",
            "usage": "Example: 'What's the weather in Tokyo?' or 'Temperature in Beijing'"
        }
    charge_result = charge_user(user_id)
    if not charge_result.get("success") and not charge_result.get("demo"):
        return {
            "payment_required": True,
            "amount": PRICE_USDT,
            "skill_id": SKILL_ID, "message": f"Please pay {PRICE_USDT} USDT to use this skill",
            "payment_url": charge_result.get("payment_url", "https://skillpay.me")
        }
    weather = get_weather(city)
    weather["payment_status"] = "free_demo" if charge_result.get("demo") else "paid"
    return weather

def extract_city(text: str) -> str:
    text = text.lower()
    patterns = [
        r'weather\s+in\s+(\w+)', r'temperature\s+in\s+(\w+)',
        r'weather\s+(\w+)', r'temperature\s+(\w+)',
        r'(\w+)\s+weather', r'(\w+)\s+temperature', r'in\s+(\w+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            city = match.group(1)
            if city not in ['the', 'a', 'an', 'what', 'how', 'is', 'it', 'today', 'now']:
                return city.capitalize()
    return text.strip()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        user_id = sys.argv[2] if len(sys.argv) > 2 else "cli"
    else:
        user_input = input("Enter your query: ")
        user_id = "cli"
    result = handle(user_input, user_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))
