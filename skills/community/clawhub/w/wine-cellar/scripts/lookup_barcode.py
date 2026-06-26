#!/usr/bin/env python3
"""
Barcode lookup for wine information.
Retrieves wine details from barcode using local database or external APIs.
"""

import sys
import os
import json
sys.path.append(os.path.dirname(__file__))

from utils import load_json, save_json, generate_id
from typing import Dict, List, Optional, Tuple

# Load the wine database reference
def load_wine_database() -> Dict[str, Any]:
    """Load wine database from references."""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'references', 'wine_database.json')
    try:
        with open(db_path, 'r') as f:
            data = json.load(f)
            # Convert list to dict keyed by barcode for easy lookup
            wines = data.get('wines', [])
            return {wine['barcode']: wine for wine in wines}
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load wine database: {e}")
        return {}

def load_barcode_cache() -> Dict[str, Any]:
    """Load cached barcode lookups for performance."""
    cache = load_json('barcode_cache.json')
    return cache.get('cache', {})

def save_barcode_cache(cache: Dict[str, Any]) -> None:
    """Save barcode cache."""
    save_json('barcode_cache.json', {'cache': cache})

def lookup_wine_by_barcode(barcode: str) -> Optional[Dict[str, Any]]:
    """
    Look up wine information by barcode.
    First checks cache, then local database, then could query external APIs.
    """
    # Normalize barcode
    barcode = barcode.strip().replace('-', '').replace(' ', '')
    
    # Check cache first
    cache = load_barcode_cache()
    if barcode in cache:
        print(f"Found {barcode} in cache")
        return cache[barcode]
    
    # Check local database
    wine_db = load_wine_database()
    if barcode in wine_db:
        wine_info = wine_db[barcode]
        # Cache the result
        cache[barcode] = wine_info
        save_barcode_cache(cache)
        return wine_info
    
    # TODO: Add external API lookup (Wine-Searcher, Vivino, etc.)
    # For now, return None if not found
    print(f"Barcode {barcode} not found in database")
    return None

def add_wine_from_barcode(barcode: str, quantity: int = 1, 
                         location: str = "", price_paid: float = 0.0) -> Dict[str, Any]:
    """
    Add a wine to inventory from barcode lookup.
    Returns the wine record that was added.
    """
    # Look up wine info
    wine_info = lookup_wine_by_barcode(barcode)
    
    if not wine_info:
        return {"error": f"Could not find wine information for barcode: {barcode}"}
    
    # Load inventory
    inventory = load_json('wine_inventory.json')
    wines = inventory.get('wines', [])
    
    # Create wine record
    from utils import generate_id
    wine_record = {
        "id": generate_id(),
        "producer": wine_info.get("producer", "Unknown"),
        "name": wine_info.get("name", "Unknown Wine"),
        "varietal": wine_info.get("varietal", "Unknown"),
        "vintage": wine_info.get("vintage", "NV"),
        "region": wine_info.get("region", ""),
        "appellation": wine_info.get("appellation", ""),
        "quantity": quantity,
        "location": location,
        "acquired_date": None,  # Could set to today
        "price_paid": price_paid,
        "current_value": wine_info.get("typical_price", 0.0) * quantity,
        "drinking_window": "",  # Could derive from vintage/varietal
        "tasting_notes": "",
        "rating": 0,
        "barcode": barcode,
        "source": "barcode_lookup",
        "notes": wine_info.get("description", "")
    }
    
    # Add to inventory
    wines.append(wine_record)
    inventory['wines'] = wines
    save_json('wine_inventory.json', inventory)
    
    return wine_record

def main():
    """Command line interface for testing."""
    if len(sys.argv) < 2:
        print("Usage: python lookup_barcode.py <barcode> [quantity] [location] [price]")
        print("Example: python lookup_barcode.py 085000014315 2 'Bin 5' 15.99")
        sys.exit(1)
    
    barcode = sys.argv[1]
    quantity = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    location = sys.argv[3] if len(sys.argv) > 3 else ""
    price_paid = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    
    print(f"Looking up barcode: {barcode}")
    wine_info = lookup_wine_by_barcode(barcode)
    
    if wine_info:
        print("\nWine Information:")
        print(f"  Producer: {wine_info.get('producer')}")
        print(f"  Name: {wine_info.get('name')}")
        print(f"  Varietal: {wine_info.get('varietal')}")
        print(f"  Vintage: {wine_info.get('vintage')}")
        print(f"  Region: {wine_info.get('region')}")
        print(f"  Appellation: {wine_info.get('appellation')}")
        print(f"  Description: {wine_info.get('description')}")
        print(f"  Typical Price: ${wine_info.get('typical_price', 0):.2f}")
        
        # Ask if user wants to add to inventory
        if len(sys.argv) > 2:  # If quantity/location/price provided, add it
            print(f"\nAdding {quantity} bottle(s) to inventory...")
            result = add_wine_from_barcode(barcode, quantity, location, price_paid)
            
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                print(f"Successfully added to inventory!")
                print(f"  ID: {result['id']}")
                print(f"  Location: {result['location']}")
                print(f"  Quantity: {result['quantity']}")
    else:
        print(f"No information found for barcode {barcode}")
        print("You may need to add this wine manually or check the barcode.")

if __name__ == "__main__":
    main()