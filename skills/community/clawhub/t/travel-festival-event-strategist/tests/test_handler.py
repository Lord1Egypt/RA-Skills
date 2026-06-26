"""
Tests for Festival and Event Travel Strategist
"""

import os
import sys
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from handler import handle

def test_returns_json():
    result = handle("test")
    parsed = json.loads(result)
    assert isinstance(parsed, dict)
    assert parsed["skill"] == "travel-festival-event-strategist"
    print("✓ JSON test passed for travel-festival-event-strategist")

def test_has_disclaimer():
    result = handle("test")
    assert "disclaimer" in result.lower()
    print("✓ Disclaimer test passed for travel-festival-event-strategist")

if __name__ == "__main__":
    test_returns_json()
    test_has_disclaimer()
    print("All tests passed for travel-festival-event-strategist")
