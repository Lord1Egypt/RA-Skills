import sys
import os
from seesaw import SeesawClient

def main():
    client = SeesawClient()
    positions = client.get_positions()
    if not positions:
        print("No positions found.")
        return

    print(f"Found {len(positions)} positions.")
    for pos in positions:
        market_id = pos.get('prediction_id')
        market = client.get_market(market_id)
        if market and market.get('status') == 'resolved':
            print(f"Market {market_id} is resolved! Attempting to claim...")
            try:
                res = client.claim_settlement(market_id)
                print(f"Claim result: {res}")
            except Exception as e:
                print(f"Failed to claim for {market_id}: {e}")
        else:
            status = market.get('status') if market else 'unknown'
            # print(f"Market {market_id} is {status}.")

if __name__ == "__main__":
    main()
