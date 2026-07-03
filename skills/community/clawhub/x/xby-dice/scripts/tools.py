from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def roll_dice(
    notation: str
) -> Dict[str, Any]:
    """
    Roll dice using standard notation (e.g., '2d6+3', '1d20-2')
    
    Args:
        notation: Dice notation (e.g., '2d6+3', '1d20-2')
    
    Returns:
        
    """
    arguments = {
        "notation": notation
    }
    
    return call_api("1777419066876931", "roll_dice", arguments)

