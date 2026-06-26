#!/usr/bin/env python3
"""
Tool for saving local pet profiles.
Securely stores the pet information collected by the AI agent locally.
"""
import os
import json
import argparse

PROFILE_DIR = os.path.expanduser("~/.openclaw/profiles")
PROFILE_PATH = os.path.join(PROFILE_DIR, "zuozuo_pet_profile.json")

def save_profile(category, breed, age, weight, heath_status, region):
    if not os.path.exists(PROFILE_DIR):
        os.makedirs(PROFILE_DIR, exist_ok=True)
    
    # Try to load existing data for merging or overwriting
    data = {}
    if os.path.exists(PROFILE_PATH):
        try:
            with open(PROFILE_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            pass # Rebuild from scratch if parsing fails
    
    # Update pet information
    data = {
        "pet_category": category,
        "pet_breed": breed,
        "pet_age": age,
        "pet_weight": weight,
        "health_status": heath_status,
        "user_region": region,
        "last_updated": "current_timestamp_placeholder" # Optional timestamp
    }
    
    try:
        with open(PROFILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return {"status": "success", "message": "Pet profile saved to local storage successfully", "data": data}
    except Exception as e:
        return {"status": "error", "message": f"Failed to save profile: {str(e)}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Save local profile for zuozuo pet assistant")
    parser.add_argument("--category", required=True, help="Pet category (e.g., cat/dog)")
    parser.add_argument("--breed", required=True, help="Pet breed")
    parser.add_argument("--age", required=True, help="Pet age")
    parser.add_argument("--weight", required=True, help="Pet weight")
    parser.add_argument("--health", required=True, help="Health status description")
    parser.add_argument("--region", required=True, help="User's region")
    
    args = parser.parse_args()
    result = save_profile(args.category, args.breed, args.age, args.weight, args.health, args.region)
    print(json.dumps(result, ensure_ascii=False, indent=2))
