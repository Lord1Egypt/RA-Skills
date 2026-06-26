#!/usr/bin/env python3
"""Evaluate property systematically."""
import json
import os
import uuid
import argparse
from datetime import datetime

REALESTATE_DIR = os.path.expanduser("~/.openclaw/workspace/memory/realestate")

def ensure_dir():
    os.makedirs(REALESTATE_DIR, exist_ok=True)

def main():
    parser = argparse.ArgumentParser(description='Evaluate property')
    parser.add_argument('--address', required=True, help='Property address')
    parser.add_argument('--price', type=float, required=True, help='List price')
    parser.add_argument('--type', default='single-family', help='Property type')
    parser.add_argument('--year', type=int, help='Year built')
    
    args = parser.parse_args()
    
    prop_id = f"PROP-{str(uuid.uuid4())[:6].upper()}"
    
    print(f"\n🏠 PROPERTY EVALUATION: {args.address}")
    print("=" * 60)
    print(f"Price: ${args.price:,.0f}")
    print(f"Type: {args.type}")
    if args.year:
        print(f"Year Built: {args.year}")
    print()
    
    print("EVALUATION CHECKLIST:")
    print("-" * 40)
    
    print("\nBEFORE VIEWING:")
    print("☐ Research sale history")
    print("☐ Check days on market")
    print("☐ Review comparable sales")
    print("☐ Check property tax records")
    print("☐ Research neighborhood trends")
    
    print("\nDURING VIEWING:")
    print("☐ Roof condition and age")
    print("☐ HVAC system age")
    print("☐ Plumbing updates")
    print("☐ Electrical panel")
    print("☐ Windows and doors")
    print("☐ Foundation cracks or settling")
    print("☐ Water stains or moisture")
    print("☐ Natural light at different times")
    print("☐ Noise levels (traffic, neighbors)")
    print("☐ Cell signal and internet options")
    
    print("\nNEIGHBORHOOD:")
    print("☐ Condition of neighboring properties")
    print("☐ Proximity to amenities")
    print("☐ School ratings (if relevant)")
    print("☐ Crime statistics")
    print("☐ Future development plans")
    
    print("\nFINANCIAL:")
    print("☐ HOA fees and restrictions")
    print("☐ Utility costs (ask for averages)")
    print("☐ Property tax trend")
    print("☐ Insurance costs")
    print("☐ Immediate repair needs")
    
    # Save evaluation
    prop = {
        "id": prop_id,
        "address": args.address,
        "price": args.price,
        "type": args.type,
        "year_built": args.year,
        "evaluated_at": datetime.now().isoformat(),
        "status": "evaluating"
    }
    
    props_file = os.path.join(REALESTATE_DIR, "properties.json")
    data = {"properties": []}
    if os.path.exists(props_file):
        with open(props_file, 'r') as f:
            data = json.load(f)
    
    data['properties'].append(prop)
    
    ensure_dir()
    with open(props_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"\n✓ Property logged: {prop_id}")

if __name__ == '__main__':
    main()
