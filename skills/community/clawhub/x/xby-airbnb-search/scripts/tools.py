from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def airbnb_search(
    location: str,
    placeId: Optional[str] = None,
    checkin: Optional[str] = None,
    checkout: Optional[str] = None,
    adults: Optional[float] = None,
    children: Optional[float] = None,
    infants: Optional[float] = None,
    pets: Optional[float] = None,
    minPrice: Optional[float] = None,
    maxPrice: Optional[float] = None,
    cursor: Optional[str] = None,
    ignoreRobotsText: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Search for Airbnb listings with various filters and pagination. Provide direct links to the user
    
    Args:
        location: Location to search for (city, state, etc.)
        placeId: Google Maps Place ID (overrides the location parameter)
        checkin: Check-in date (YYYY-MM-DD)
        checkout: Check-out date (YYYY-MM-DD)
        adults: Number of adults
        children: Number of children
        infants: Number of infants
        pets: Number of pets
        minPrice: Minimum price for the stay
        maxPrice: Maximum price for the stay
        cursor: Base64-encoded string used for Pagination
        ignoreRobotsText: Ignore robots.txt rules for this request
    
    Returns:
        
    """
    arguments = {
        "location": location,
        "placeId": placeId,
        "checkin": checkin,
        "checkout": checkout,
        "adults": adults,
        "children": children,
        "infants": infants,
        "pets": pets,
        "minPrice": minPrice,
        "maxPrice": maxPrice,
        "cursor": cursor,
        "ignoreRobotsText": ignoreRobotsText
    }
    
    return call_api("1777316659557379", "airbnb_search", arguments)

def airbnb_listing_details(
    id: str,
    checkin: Optional[str] = None,
    checkout: Optional[str] = None,
    adults: Optional[float] = None,
    children: Optional[float] = None,
    infants: Optional[float] = None,
    pets: Optional[float] = None,
    ignoreRobotsText: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Get detailed information about a specific Airbnb listing. Provide direct links to the user
    
    Args:
        id: The Airbnb listing ID
        checkin: Check-in date (YYYY-MM-DD)
        checkout: Check-out date (YYYY-MM-DD)
        adults: Number of adults
        children: Number of children
        infants: Number of infants
        pets: Number of pets
        ignoreRobotsText: Ignore robots.txt rules for this request
    
    Returns:
        
    """
    arguments = {
        "id": id,
        "checkin": checkin,
        "checkout": checkout,
        "adults": adults,
        "children": children,
        "infants": infants,
        "pets": pets,
        "ignoreRobotsText": ignoreRobotsText
    }
    
    return call_api("1777316659557379", "airbnb_listing_details", arguments)

