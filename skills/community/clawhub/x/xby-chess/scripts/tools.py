from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def visualize_fen(
    fen_string: str
) -> Dict[str, Any]:
    """
    Convert FEN notation to ASCII chess board visualization
    
    Args:
        fen_string: FEN (Forsyth-Edwards Notation) string representing chess position
    
    Returns:
        
    """
    arguments = {
        "fen_string": fen_string
    }
    
    return call_api("1777316659713027", "visualize_fen", arguments)

