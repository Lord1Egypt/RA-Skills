from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def GetChartImgLink(
    json: Optional[null] = None
) -> Dict[str, Any]:
    """
    To draw chart and get chart image link by parameters, and parameter grammar follows Quick Chart API (quickchart.io).
    
    Args:
        json: quick chart api's (quickchart.io) parameters and format is JSON object. The object does not include any functions, only values.
    
    Returns:
        
    """
    arguments = {
        "json": json
    }
    
    return call_api("1777316659546115", "GetChartImgLink", arguments)

