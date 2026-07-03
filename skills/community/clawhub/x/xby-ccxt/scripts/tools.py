from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def add_meal(
    description: str,
    mealType: str
) -> Dict[str, Any]:
    """
    Log a meal with food items and calories
    
    Args:
        description: Natural language description of the meal (e.g., 'chicken salad and a glass of milk')
        mealType: Type of meal
    
    Returns:
        
    """
    arguments = {
        "description": description,
        "mealType": mealType
    }
    
    return call_api("1777316659909635", "add_meal", arguments)

def get_daily_summary(
    date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get today's calorie intake summary
    
    Args:
        date: Date in YYYY-MM-DD format (defaults to today)
    
    Returns:
        
    """
    arguments = {
        "date": date
    }
    
    return call_api("1777316659909635", "get_daily_summary", arguments)

def get_weekly_report(
    startDate: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get weekly calorie consumption report
    
    Args:
        startDate: Start date in YYYY-MM-DD format (defaults to 7 days ago)
    
    Returns:
        
    """
    arguments = {
        "startDate": startDate
    }
    
    return call_api("1777316659909635", "get_weekly_report", arguments)

def search_food(
    foodName: str
) -> Dict[str, Any]:
    """
    Search for calorie information of a specific food
    
    Args:
        foodName: Name of the food to search
    
    Returns:
        
    """
    arguments = {
        "foodName": foodName
    }
    
    return call_api("1777316659909635", "search_food", arguments)

