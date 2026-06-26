"""
Utility functions for the wine cellar skill.
Handles data loading, saving, and common operations.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def ensure_data_dir():
    """Ensure the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)

def load_json(filename: str) -> Dict[str, Any]:
    """Load JSON data from file."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_json(filename: str, data: Dict[str, Any]) -> None:
    """Save JSON data to file."""
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)

def generate_id() -> str:
    """Generate a unique ID."""
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")

def validate_wine_data(wine_data: Dict[str, Any]) -> List[str]:
    """Validate wine data and return list of errors."""
    errors = []
    required_fields = ['producer', 'name', 'varietal', 'vintage']
    
    for field in required_fields:
        if not wine_data.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate vintage is a reasonable year
    vintage = wine_data.get('vintage')
    if vintage:
        try:
            vintage_int = int(vintage)
            if vintage_int < 1800 or vintage_int > datetime.now().year + 5:
                errors.append("Vintage must be a reasonable year")
        except ValueError:
            errors.append("Vintage must be a valid year")
    
    # Validate quantity is non-negative integer
    quantity = wine_data.get('quantity')
    if quantity is not None:
        try:
            quantity_int = int(quantity)
            if quantity_int < 0:
                errors.append("Quantity must be non-negative")
        except ValueError:
            errors.append("Quantity must be a valid integer")
    
    return errors

def format_wine_summary(wine: Dict[str, Any]) -> str:
    """Format a wine dictionary into a readable summary."""
    parts = [
        f"{wine.get('producer', 'Unknown Producer')}",
        f"{wine.get('name', 'Unknown Wine')}",
        f"{wine.get('varietal', 'Unknown Varietal')}",
        f"{wine.get('vintage', 'NV')}"
    ]
    
    region = wine.get('region')
    if region:
        parts.append(f"from {region}")
    
    quantity = wine.get('quantity', 0)
    if quantity > 0:
        parts.append(f"({quantity} bottles)")
    
    return " ".join(parts)