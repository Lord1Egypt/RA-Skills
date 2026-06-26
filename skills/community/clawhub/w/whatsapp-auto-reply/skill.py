import os
import requests

API_KEY = os.getenv("WHATSAPP_API_KEY")

def run(input_data):
    phone = input_data["phone_number"]
    message = input_data["message"]

    response = requests.post(
        "https://api.whatsapp-service/send",
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "phone": phone,
            "message": message
        }
    )

    return {
        "status": "success",
        "api_response": response.json()
    }