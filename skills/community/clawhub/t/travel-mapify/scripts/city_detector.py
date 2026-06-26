#!/usr/bin/env python3
"""
Automatic city detection from location names.
Detects the most likely city from a list of POI names.
"""

import re
from typing import List, Optional

def detect_city_from_locations(locations: List[str]) -> Optional[str]:
    """
    Detect the most likely city from a list of location names.
    
    Args:
        locations: List of location/POI names
        
    Returns:
        Detected city name or None if no clear city detected
    """
    if not locations:
        return None
    
    # Common Chinese cities and their alternative names
    city_patterns = {
        '北京': ['北京', 'Beijing', '京'],
        '上海': ['上海', 'Shanghai', '沪'],
        '广州': ['广州', 'Guangzhou', '穗'],
        '深圳': ['深圳', 'Shenzhen', '鹏城'],
        '杭州': ['杭州', 'Hangzhou', '杭'],
        '成都': ['成都', 'Chengdu', '蓉'],
        '重庆': ['重庆', 'Chongqing', '渝'],
        '西安': ['西安', 'Xi\'an', '长安'],
        '三亚': ['三亚', 'Sanya', '崖州'],
        '厦门': ['厦门', 'Xiamen', '鹭岛'],
        '青岛': ['青岛', 'Qingdao', '岛城'],
        '大连': ['大连', 'Dalian', '滨城'],
        '苏州': ['苏州', 'Suzhou', '姑苏'],
        '南京': ['南京', 'Nanjing', '金陵'],
        '武汉': ['武汉', 'Wuhan', '江城'],
        '长沙': ['长沙', 'Changsha', '星城'],
        '郑州': ['郑州', 'Zhengzhou', '绿城'],
        '天津': ['天津', 'Tianjin', '津'],
        '宁波': ['宁波', 'Ningbo', '甬城']
    }
    
    # Count city mentions in all locations
    city_counts = {}
    all_text = ' '.join(locations).lower()
    
    for city, patterns in city_patterns.items():
        count = 0
        for pattern in patterns:
            # Case-insensitive matching
            if pattern.lower() in all_text:
                count += 1
        if count > 0:
            city_counts[city] = count
    
    # Return the city with highest count, or None if no city found
    if city_counts:
        return max(city_counts, key=city_counts.get)
    
    return None

def get_default_city_for_locations(locations: List[str], fallback_city: str = '上海') -> str:
    """
    Get the appropriate city for geocoding based on locations.
    
    Args:
        locations: List of location names
        fallback_city: Default city to use if no city detected
        
    Returns:
        City name to use for geocoding
    """
    detected_city = detect_city_from_locations(locations)
    return detected_city if detected_city else fallback_city

# Test function
def main():
    test_cases = [
        ["北京军事博物馆", "北京科技大学"],
        ["上海迪士尼乐园", "豫园"],
        ["三亚美高梅", "鹿回头"],
        ["解放碑", "洪崖洞"],
        ["Unknown Location", "Another Place"]
    ]
    
    for locations in test_cases:
        detected = detect_city_from_locations(locations)
        final_city = get_default_city_for_locations(locations)
        print(f"Locations: {locations}")
        print(f"Detected city: {detected}")
        print(f"Final city: {final_city}")
        print("-" * 50)

if __name__ == '__main__':
    main()