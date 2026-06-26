#!/usr/bin/env python3
"""
智能地点处理模块
支持城市名、经纬度、locationId自动识别
"""

import re
import os
import json
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass

@dataclass
class LocationResult:
    """地点处理结果"""
    location_id: str  # 和风天气locationId
    name: str         # 地点名称
    adm2: str         # 市级名称
    adm1: str         # 省级名称
    country: str      # 国家
    lat: Optional[float] = None  # 纬度
    lon: Optional[float] = None  # 经度
    source: str = "unknown"      # 来源：city_name, coordinates, location_id, default


class LocationHandler:
    """智能地点处理器"""
    
    def __init__(self, api_client=None):
        self.api_client = api_client
        self.city_map = self._init_city_map()
        self.default_location = os.getenv("QWEATHER_DEFAULT_LOCATION", "beijing")
        
    def _init_city_map(self) -> Dict[str, Dict]:
        """初始化城市映射表"""
        return {
            # 直辖市
            "北京": {"id": "101010100", "en": "beijing", "adm1": "北京", "adm2": "北京"},
            "上海": {"id": "101020100", "en": "shanghai", "adm1": "上海", "adm2": "上海"},
            "天津": {"id": "101030100", "en": "tianjin", "adm1": "天津", "adm2": "天津"},
            "重庆": {"id": "101040100", "en": "chongqing", "adm1": "重庆", "adm2": "重庆"},
            
            # 省会城市
            "广州": {"id": "101280101", "en": "guangzhou", "adm1": "广东", "adm2": "广州"},
            "深圳": {"id": "101280601", "en": "shenzhen", "adm1": "广东", "adm2": "深圳"},
            "杭州": {"id": "101210101", "en": "hangzhou", "adm1": "浙江", "adm2": "杭州"},
            "成都": {"id": "101270101", "en": "chengdu", "adm1": "四川", "adm2": "成都"},
            "武汉": {"id": "101200101", "en": "wuhan", "adm1": "湖北", "adm2": "武汉"},
            "南京": {"id": "101190101", "en": "nanjing", "adm1": "江苏", "adm2": "南京"},
            "西安": {"id": "101110101", "en": "xian", "adm1": "陕西", "adm2": "西安"},
            
            # 英文缩写
            "bj": {"id": "101010100", "en": "beijing", "adm1": "北京", "adm2": "北京"},
            "sh": {"id": "101020100", "en": "shanghai", "adm1": "上海", "adm2": "上海"},
            "gz": {"id": "101280101", "en": "guangzhou", "adm1": "广东", "adm2": "广州"},
            "sz": {"id": "101280601", "en": "shenzhen", "adm1": "广东", "adm2": "深圳"},
            "hz": {"id": "101210101", "en": "hangzhou", "adm1": "浙江", "adm2": "杭州"},
            "cd": {"id": "101270101", "en": "chengdu", "adm1": "四川", "adm2": "成都"},
        }
    
    def parse_input(self, input_str: str) -> LocationResult:
        """
        解析用户输入的地点
        支持：城市名、经纬度、locationId
        """
        if not input_str or input_str.strip() == "":
            return self._get_default_location()
        
        input_str = input_str.strip()
        
        # 1. 检查是否是locationId（纯数字）
        if re.match(r'^\d{9}$', input_str):
            return self._handle_location_id(input_str)
        
        # 2. 检查是否是经纬度
        coord_match = self._parse_coordinates(input_str)
        if coord_match:
            return self._handle_coordinates(coord_match)
        
        # 3. 检查是否是已知城市
        city_result = self._handle_city_name(input_str)
        if city_result:
            return city_result
        
        # 4. 尝试通过API搜索
        if self.api_client:
            api_result = self._search_via_api(input_str)
            if api_result:
                return api_result
        
        # 5. 返回默认地点
        return self._get_default_location()
    
    def _get_default_location(self) -> LocationResult:
        """获取默认地点"""
        default_city = self.default_location
        
        if default_city in self.city_map:
            city_info = self.city_map[default_city]
            return LocationResult(
                location_id=city_info["id"],
                name=city_info["en"],
                adm2=city_info["adm2"],
                adm1=city_info["adm1"],
                country="中国",
                source="default"
            )
        
        # 如果默认地点不在映射表中，使用北京
        beijing_info = self.city_map["北京"]
        return LocationResult(
            location_id=beijing_info["id"],
            name=beijing_info["en"],
            adm2=beijing_info["adm2"],
            adm1=beijing_info["adm1"],
            country="中国",
            source="default_fallback"
        )
    
    def _handle_location_id(self, location_id: str) -> LocationResult:
        """处理locationId"""
        # 首先检查映射表中是否有这个ID
        for city_name, city_info in self.city_map.items():
            if city_info["id"] == location_id:
                return LocationResult(
                    location_id=location_id,
                    name=city_info["en"],
                    adm2=city_info["adm2"],
                    adm1=city_info["adm1"],
                    country="中国",
                    source="location_id"
                )
        
        # 如果不在映射表中，返回基础信息
        return LocationResult(
            location_id=location_id,
            name=f"Location_{location_id}",
            adm2="未知",
            adm1="未知",
            country="中国",
            source="location_id_unknown"
        )
    
    def _parse_coordinates(self, input_str: str) -> Optional[Tuple[float, float]]:
        """解析经纬度字符串"""
        patterns = [
            # 格式: 39.9042,116.4074
            r'^(-?\d+\.?\d*)\s*,\s*(-?\d+\.?\d*)$',
            # 格式: 39°54'15.1"N 116°24'26.0"E
            r'^(\d+)°(\d+)\'(\d+\.?\d*)"([NS])\s+(\d+)°(\d+)\'(\d+\.?\d*)"([EW])$',
            # 格式: 39.9042°N, 116.4074°E
            r'^(\d+\.?\d*)°([NS])\s*,\s*(\d+\.?\d*)°([EW])$',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, input_str)
            if match:
                if ',' in input_str and '°' not in input_str:
                    # 简单的小数格式
                    lat = float(match.group(1))
                    lon = float(match.group(2))
                    return (lat, lon)
                elif '°' in input_str and "'" in input_str:
                    # 度分秒格式
                    lat_deg = float(match.group(1))
                    lat_min = float(match.group(2))
                    lat_sec = float(match.group(3))
                    lat_dir = match.group(4)
                    
                    lon_deg = float(match.group(5))
                    lon_min = float(match.group(6))
                    lon_sec = float(match.group(7))
                    lon_dir = match.group(8)
                    
                    lat = lat_deg + lat_min/60 + lat_sec/3600
                    lon = lon_deg + lon_min/60 + lon_sec/3600
                    
                    if lat_dir == 'S':
                        lat = -lat
                    if lon_dir == 'W':
                        lon = -lon
                    
                    return (lat, lon)
                elif '°' in input_str:
                    # 带方向的度数格式
                    lat = float(match.group(1))
                    lat_dir = match.group(2)
                    lon = float(match.group(3))
                    lon_dir = match.group(4)
                    
                    if lat_dir == 'S':
                        lat = -lat
                    if lon_dir == 'W':
                        lon = -lon
                    
                    return (lat, lon)
        
        return None
    
    def _handle_coordinates(self, coords: Tuple[float, float]) -> LocationResult:
        """处理经纬度"""
        lat, lon = coords
        
        # 尝试通过API获取地点信息
        if self.api_client:
            try:
                # 这里需要实现通过经纬度获取城市信息的API调用
                # 暂时返回基础信息
                pass
            except:
                pass
        
        return LocationResult(
            location_id=self._generate_location_id_from_coords(lat, lon),
            name=f"{lat:.4f},{lon:.4f}",
            adm2="坐标位置",
            adm1="",
            country="",
            lat=lat,
            lon=lon,
            source="coordinates"
        )
    
    def _generate_location_id_from_coords(self, lat: float, lon: float) -> str:
        """从经纬度生成临时的locationId"""
        # 简单实现：将经纬度转换为9位数字
        lat_int = int(abs(lat) * 10000)
        lon_int = int(abs(lon) * 10000)
        return f"{lat_int:05d}{lon_int:04d}"
    
    def _handle_city_name(self, city_name: str) -> Optional[LocationResult]:
        """处理城市名"""
        # 检查中文城市名
        if city_name in self.city_map:
            city_info = self.city_map[city_name]
            return LocationResult(
                location_id=city_info["id"],
                name=city_info["en"],
                adm2=city_info["adm2"],
                adm1=city_info["adm1"],
                country="中国",
                source="city_name"
            )
        
        # 检查英文城市名
        for chinese_name, city_info in self.city_map.items():
            if city_info["en"].lower() == city_name.lower():
                return LocationResult(
                    location_id=city_info["id"],
                    name=city_info["en"],
                    adm2=city_info["adm2"],
                    adm1=city_info["adm1"],
                    country="中国",
                    source="city_name_en"
                )
        
        return None
    
    def _search_via_api(self, query: str) -> Optional[LocationResult]:
        """通过API搜索地点"""
        # 这里需要实现和风天气的城市搜索API
        # 暂时返回None
        return None
    
    def format_location(self, location: LocationResult) -> str:
        """格式化地点信息"""
        if location.source == "coordinates":
            return f"坐标位置 ({location.lat:.4f}, {location.lon:.4f})"
        elif location.source == "location_id_unknown":
            return f"地点ID: {location.location_id}"
        else:
            return f"{location.adm2}{location.adm1 and f'({location.adm1})' or ''}"
    
    def get_location_for_display(self, location: LocationResult) -> str:
        """获取用于显示的地点名称"""
        if location.adm2 and location.adm2 != "未知":
            return location.adm2
        elif location.name:
            return location.name
        else:
            return f"ID: {location.location_id}"


# 使用示例
if __name__ == "__main__":
    handler = LocationHandler()
    
    test_cases = [
        "北京",
        "shanghai",
        "101010100",
        "39.9042,116.4074",
        "",
        "未知城市"
    ]
    
    for test in test_cases:
        result = handler.parse_input(test)
        safe_print(f"输入: '{test}'")
        safe_print(f"  结果: {handler.format_location(result)}")
        safe_print(f"  ID: {result.location_id}")
        safe_print(f"  来源: {result.source}")
        safe_print()