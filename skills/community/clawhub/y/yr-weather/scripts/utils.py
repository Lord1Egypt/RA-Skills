#!/usr/bin/env python3
"""
Utility functions for Yr.no Weather skill.
"""

def get_emoji(symbol_code: str) -> str:
    """
    Convert MET symbol code to emoji.
    """
    emojis = {
        "clearsky": "☀️",
        "fair": "🌤️",
        "partlycloudy": "⛅",
        "cloudy": "☁️",
        "rain": "🌧️",
        "lightrain": "🌦️",
        "heavyrain": "⛈️",
        "rainshowers": "🌦️",
        "sleet": "🌨️",
        "snow": "❄️",
        "lightsnow": "🌨️",
        "heavysnow": "❄️",
        "snowshowers": "🌨️",
        "fog": "🌫️",
    }
    base_symbol = symbol_code.split("_")[0]
    return emojis.get(base_symbol, "🌡️")

def format_symbol(symbol_code: str) -> str:
    """
    Format symbol code for display.
    """
    return symbol_code.replace("_", " ").title()
