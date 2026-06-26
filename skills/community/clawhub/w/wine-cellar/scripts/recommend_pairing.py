#!/usr/bin/env python3
"""
Wine pairing recommendation engine.
Suggests wines from inventory based on dish characteristics.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils import load_json, generate_id
from typing import Dict, List, Tuple

# Basic pairing principles (could be moved to references)
PAIRING_RULES = {
    # Protein-based rules
    'red_meat': {
        'preferred_varietals': ['Cabernet Sauvignon', 'Merlot', 'Syrah', 'Malbec', 'Pinot Noir', 'Tempranillo', 'Rioja'],
        'preferred_regions': ['Bordeaux', 'Napa Valley', 'Tuscany', 'Rioja'],
        'min_body': 'medium',
        'notes': 'Red meats pair well with tannic red wines'
    },
    'white_meat': {
        'preferred_varietals': ['Chardonnay', 'Pinot Grigio', 'Sauvignon Blanc', 'Viognier'],
        'preferred_regions': ['Burgundy', 'Loire Valley', 'California', 'Alsace'],
        'min_body': 'light',
        'notes': 'White meats work with lighter whites and some light reds'
    },
    'fish': {
        'preferred_varietals': ['Sauvignon Blanc', 'Pinot Grigio', 'Chardonnay', 'Albariño'],
        'preferred_regions': ['Loire Valley', 'New Zealand', 'Alsace', 'Spain'],
        'min_body': 'light',
        'notes': 'Fish pairs best with crisp, acidic whites'
    },
    'seafood': {
        'preferred_varietals': ['Chardonnay', 'Viognier', 'Rosé', 'Pinot Grigio'],
        'preferred_regions': ['Burgundy', 'Rhone', 'Provence', 'California'],
        'min_body': 'medium-light',
        'notes': 'Seafood versatility allows for richer whites and rosés'
    },
    'pasta_red_sauce': {
        'preferred_varietals': ['Chianti', 'Sangiovese', 'Montepulciano', 'Barbera'],
        'preferred_regions': ['Tuscany', 'Piedmont'],
        'min_body': 'medium',
        'notes': 'Tomato-based sauces need acidity to cut through'
    },
    'pasta_cream': {
        'preferred_varietals': ['Chardonnay', 'Pinot Bianco', 'Soave'],
        'preferred_regions': ['Burgundy', 'Italy', 'Oregon'],
        'min_body': 'medium',
        'notes': 'Creamy sauces pair with richer whites'
    },
    'pasta_pesto': {
        'preferred_varietals': ['Vermentino', 'Sauvignon Blanc', 'Pinot Grigio'],
        'preferred_regions': ['Liguria', 'Sardinia', 'New Zealand'],
        'min_body': 'light',
        'notes': 'Herbaceous dishes need aromatic whites'
    },
    'mushroom': {
        'preferred_varietals': ['Pinot Noir', 'Nebbiolo', 'Barolo', 'Barbaresco'],
        'preferred_regions': ['Burgundy', 'Piedmont'],
        'min_body': 'medium-light',
        'notes': 'Earthy flavors match with earthy, lighter reds'
    },
    'cheese': {
        'preferred_varietals': ['Port', 'Sherry', 'Riesling', 'Gewürztraminer'],
        'preferred_regions': ['Portugal', 'Spain', 'Germany', 'Alsace'],
        'min_body': 'varied',
        'notes': 'Cheese pairing depends on cheese type'
    },
    'chocolate_dessert': {
        'preferred_varietals': ['Port', 'Banyuls', 'Malbec', 'Zinfandel'],
        'preferred_regions': ['Portugal', 'France', 'Argentina', 'California'],
        'min_body': 'full',
        'notes': 'Chocolate needs sweet, fortified wines'
    },
    'fruit_dessert': {
        'preferred_varietals': ['Moscato', 'Riesling', 'Gewürztraminer', 'Chenin Blanc'],
        'preferred_regions': ['Germany', 'Alsace', 'Loire Valley', 'South Africa'],
        'min_body': 'light',
        'notes': 'Fruit desserts pair with off-dry to sweet whites'
    },
    'spicy': {
        'preferred_varietals': ['Riesling', 'Gewürztraminer', 'RosÃ©', 'Beaujolais'],
        'preferred_regions': ['Germany', 'Alsace', 'Provence', 'Beaujolais'],
        'min_body': 'light-medium',
        'notes': 'Spicy food benefits from slight sweetness and low alcohol'
    }
}

# Body weight mapping for scoring
BODY_WEIGHTS = {
    'light': 1,
    'medium-light': 2,
    'medium': 3,
    'medium-full': 4,
    'full': 5
}

def get_dish_type(dish: str) -> str:
    """
    Determine dish type from dish description.
    Simple keyword matching - could be enhanced with NLP.
    """
    dish_lower = dish.lower()
    
    # Red meat indicators
    if any(word in dish_lower for word in ['beef', 'steak', 'burger', 'lamb', 'venison', 'duck', 'goose', 'meatloaf', 'meatball']):
        return 'red_meat'
    
    # White meat indicators
    if any(word in dish_lower for word in ['chicken', 'turkey', 'pork', 'veal']):
        return 'white_meat'
    
    # Fish indicators
    if any(word in dish_lower for word in ['salmon', 'tuna', 'cod', 'halibut', 'sea bass', 'tilapia', 'fish', 'sushi', 'sashimi']):
        return 'fish'
    
    # Seafood indicators
    if any(word in dish_lower for word in ['shrimp', 'lobster', 'crab', 'clam', 'mussel', 'oyster', 'scallop', 'seafood']):
        return 'seafood'
    
    # Pasta indicators
    if 'pasta' in dish_lower or 'spaghetti' in dish_lower or 'linguine' in dish_lower or 'ravioli' in dish_lower or 'gnocchi' in dish_lower:
        if any(word in dish_lower for word in ['tomato', 'marinara', 'arrabbiata', 'bolognese']):
            return 'pasta_red_sauce'
        elif any(word in dish_lower for word in ['cream', 'alfredo', 'carbonara']):
            return 'pasta_cream'
        elif any(word in dish_lower for word in ['pesto', 'basil', 'herb']):
            return 'pasta_pesto'
        else:
            # Default pasta
            return 'pasta_red_sauce'  # Most common
    
    # Mushroom indicators
    if any(word in dish_lower for word in ['mushroom', 'porcini', 'shiitake', 'truffle']):
        return 'mushroom'
    
    # Cheese indicators
    if any(word in dish_lower for word in ['cheese', 'fondue', 'raclette', 'queso']):
        return 'cheese'
    
    # Dessert indicators
    if any(word in dish_lower for word in ['dessert', 'cake', 'pie', 'tart', 'pastry']):
        if any(word in dish_lower for word in ['chocolate', 'cocoa', 'brownie']):
            return 'chocolate_dessert'
        elif any(word in dish_lower for word in ['fruit', 'berry', 'apple', 'pear', 'peach']):
            return 'fruit_dessert'
        else:
            return 'fruit_dessert'  # Default dessert
    
    # Spicy indicators
    if any(word in dish_lower for word in ['spicy', 'chili', 'pepper', 'curry', 'szechuan', 'thai', 'mexican', 'indian', 'hot']):
        return 'spicy'
    
    # Default fallback
    return 'white_meat'  # Safe default

def score_wine_for_dish(wine: Dict[str, Any], dish_type: str) -> Tuple[float, List[str]]:
    """
    Score how well a wine pairs with a given dish type.
    Returns (score, reasons) where score is 0-100.
    """
    if dish_type not in PAIRING_RULES:
        return 50.0, ["No specific pairing rules for this dish type"]
    
    rules = PAIRING_RULES[dish_type]
    score = 0.0
    max_score = 100.0
    reasons = []
    
    # Check varietal match (40 points)
    varietal = wine.get('varietal', '')
    preferred_varietals = rules.get('preferred_varietals', [])
    varietal_match = False
    for pref in preferred_varietals:
        if pref.lower() in varietal.lower() or varietal.lower() in pref.lower():
            varietal_match = True
            break
    
    if varietal_match:
        score += 40
        reasons.append(f"Varietal '{varietal}' matches preferred types")
    else:
        reasons.append(f"Varietal '{varietal}' not in preferred list: {', '.join(preferred_varietals[:3])}")
    
    # Check region match (30 points)
    region = wine.get('region', '')
    preferred_regions = rules.get('preferred_regions', [])
    region_match = False
    for pref in preferred_regions:
        if pref.lower() in region.lower() or region.lower() in pref.lower():
            region_match = True
            break
    
    if region_match:
        score += 30
        reasons.append(f"Region '{region}' matches preferred regions")
    else:
        reasons.append(f"Region '{region}' not in preferred list: {', '.join(preferred_regions[:3])}")
    
    # Check body weight (20 points) - simplified
    # We'll assume most wines are medium body unless specified
    # In a real implementation, we'd have body weight in wine data
    score += 20  # Default medium body assumption
    reasons.append("Assumed medium body (adjust with actual body data)")
    
    # Check vintage/age suitability (10 points) - simplified
    vintage = wine.get('vintage')
    if vintage:
        try:
            vintage_int = int(vintage)
            # Very basic: younger wines for lighter dishes, older for richer
            # This is overly simplistic but demonstrates concept
            score += 5
            reasons.append(f"Vintage {vintage} considered")
        except ValueError:
            pass
    else:
        reasons.append("No vintage information")
    
    return min(score, max_score), reasons

def recommend_wine(dish: str, limit: int = 3) -> List[Dict[str, Any]]:
    """
    Recommend wines from inventory for a given dish.
    Returns list of wine dictionaries sorted by score.
    """
    # Load inventory
    inventory = load_json('wine_inventory.json')
    wines = inventory.get('wines', [])
    
    if not wines:
        return [{"error": "No wines in inventory"}]
    
    # Determine dish type
    dish_type = get_dish_type(dish)
    
    # Score each wine
    scored_wines = []
    for wine in wines:
        score, reasons = score_wine_for_dish(wine, dish_type)
        wine_copy = wine.copy()
        wine_copy['pairing_score'] = score
        wine_copy['pairing_reasons'] = reasons
        scored_wines.append(wine_copy)
    
    # Sort by score descending
    scored_wines.sort(key=lambda x: x['pairing_score'], reverse=True)
    
    # Return top recommendations
    return scored_wines[:limit]

def main():
    """Command line interface for testing."""
    if len(sys.argv) < 2:
        print("Usage: python recommend_pairing.py '<dish description>'")
        print("Example: python recommend_pairing.py 'grilled steak with mushrooms'")
        sys.exit(1)
    
    dish = sys.argv[1]
    recommendations = recommend_wine(dish)
    
    print(f"\nWine recommendations for: {dish}")
    print("=" * 50)
    
    if recommendations and 'error' in recommendations[0]:
        print(recommendations[0]['error'])
        return
    
    for i, wine in enumerate(recommendations, 1):
        print(f"\n{i}. {wine.get('producer', 'Unknown')} {wine.get('name', 'Wine')}")
        print(f"   {wine.get('varietal', '')} {wine.get('vintage', 'NV')}")
        if wine.get('region'):
            print(f"   from {wine.get('region')}")
        print(f"   Score: {wine.get('pairing_score', 0):.1f}/100")
        print(f"   Why: {', '.join(wine.get('pairing_reasons', []))}")
        print(f"   Bottles available: {wine.get('quantity', 0)}")

if __name__ == "__main__":
    main()