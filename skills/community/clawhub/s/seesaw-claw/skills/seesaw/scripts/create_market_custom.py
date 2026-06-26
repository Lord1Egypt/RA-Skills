import sys
import os
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from seesaw import SeesawClient

def main():
    client = SeesawClient()
    
    title = "Will NASA's Artemis II mission launch by April 1, 2026?"
    description = "NASA continues targeting an April 1, 2026 launch date from Kennedy Space Center for Artemis II, the massive SLS moon rocket that will bring astronauts back to the vicinity of the moon for the first time in over 50 years. This market resolves to 'Yes' if the launch occurs on or before April 1, 2026 (UTC). Otherwise, it resolves to 'No'."
    options = ["Yes", "No"]
    initial_probabilities = [60, 40]
    end_time = "2026-04-02T00:00:00Z"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Artemis_II_Crew_Portrait.jpg/800px-Artemis_II_Crew_Portrait.jpg"

    try:
        resp = client.create_market(
            title=title,
            options=options,
            end_time=end_time,
            description=description,
            initial_probabilities=initial_probabilities,
            image_urls=[image_url]
        )
        print("Market Created:", resp)
        
        market_id = resp.get('id')
        if market_id:
            with open('/tmp/new_market.txt', 'w') as f:
                f.write(market_id)
                
    except Exception as e:
        print("Failed:", e)

if __name__ == "__main__":
    main()
