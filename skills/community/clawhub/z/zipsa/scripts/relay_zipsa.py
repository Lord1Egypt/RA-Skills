#!/usr/bin/env python3
import requests
import sys
import json

# Minimal Zipsa relay script for testing
def call_zipsa(query, session_id="test-session", base_url="http://localhost:8000"):
    try:
        response = requests.post(
            f"{base_url}/relay",
            json={
                "user_query": query,
                "session_id": session_id
            },
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 relay_zipsa.py 'your query'")
        sys.exit(1)
    
    query = sys.argv[1]
    result = call_zipsa(query)
    print(json.dumps(result, indent=2))
