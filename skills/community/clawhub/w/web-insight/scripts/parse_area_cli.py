#!/usr/bin/env python3
"""
地域解析 CLI 工具
整合了 area_code.py 和 parse_area.py 功能
传入地域名称，返回对应的国标区域编码

用法:
    python3 parse_area_cli.py --area "北京"
    python3 parse_area_cli.py --area "江苏,南京,上海" --batch
    python3 parse_area_cli.py --search "海淀"
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class AreaCodeResult:
    """地域编码查询结果"""
    province: str
    province_code: str
    city: str
    city_code: str
    county: str
    county_code: str
    
    def get_code(self) -> str:
        """获取最精确的编码（优先县级 > 市级 > 省级）"""
        if self.county_code and self.county_code != self.city_code:
            return self.county_code
        if self.city_code and self.city_code != self.province_code:
            return self.city_code
        return self.province_code
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "province": self.province,
            "province_code": self.province_code,
            "city": self.city,
            "city_code": self.city_code,
            "county": self.county,
            "county_code": self.county_code,
        }


# 全局地域编码索引（延迟加载）
_AREA_CODE_INDEX: Optional[Dict[str, AreaCodeResult]] = None
_AREA_CODE_BY_CODE: Optional[Dict[str, AreaCodeResult]] = None


def _load_area_codes() -> None:
    """从JSON文件加载地域编码数据"""
    global _AREA_CODE_INDEX, _AREA_CODE_BY_CODE
    
    if _AREA_CODE_INDEX is not None:
        return
    
    _AREA_CODE_INDEX = {}
    _AREA_CODE_BY_CODE = {}
    
    # 查找 area_codes.json 文件
    json_path = Path(__file__).parent.parent / "assets/area_codes.json"
    
    if not json_path.exists():
        logger.warning("area_codes.json not found at %s", json_path)
        return
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 解析嵌套结构
        for province in data.get("data", []):
            province_name = province.get("name", "")
            province_code = province.get("code", "")
            
            # 添加省级
            result = AreaCodeResult(
                province=province_name,
                province_code=province_code,
                city="",
                city_code="",
                county="",
                county_code=""
            )
            _add_to_index(province_name, result)
            _AREA_CODE_BY_CODE[province_code] = result
            
            # 处理市级（直辖市的children直接是区县）
            for city in province.get("children", []):
                city_name = city.get("name", "")
                city_code = city.get("code", "")
                city_children = city.get("children", [])
                
                if city_children:
                    # 有children，说明是市级
                    city_result = AreaCodeResult(
                        province=province_name,
                        province_code=province_code,
                        city=city_name,
                        city_code=city_code,
                        county="",
                        county_code=""
                    )
                    _add_to_index(city_name, city_result)
                    _AREA_CODE_BY_CODE[city_code] = city_result
                    
                    # 处理县/区级
                    for county in city_children:
                        county_name = county.get("name", "")
                        county_code = county.get("code", "")
                        
                        county_result = AreaCodeResult(
                            province=province_name,
                            province_code=province_code,
                            city=city_name,
                            city_code=city_code,
                            county=county_name,
                            county_code=county_code
                        )
                        _add_to_index(county_name, county_result)
                        _AREA_CODE_BY_CODE[county_code] = county_result
                else:
                    # 无children，直辖市的区县
                    county_result = AreaCodeResult(
                        province=province_name,
                        province_code=province_code,
                        city=province_name,
                        city_code=province_code,
                        county=city_name,
                        county_code=city_code
                    )
                    _add_to_index(city_name, county_result)
                    _AREA_CODE_BY_CODE[city_code] = county_result
        
        logger.info("Loaded %d area codes", len(_AREA_CODE_INDEX))
        
    except Exception as e:
        logger.error("Failed to load area_codes.json: %s", e)


def _add_to_index(name: str, result: AreaCodeResult) -> None:
    """添加到索引，支持多种名称变体"""
    if not name:
        return
    
    # 原始名称
    _AREA_CODE_INDEX[name] = result
    
    # 去掉后缀的简称
    for suffix in ["省", "市", "区", "县", "自治区", "自治州", "自治县", "特别行政区"]:
        if name.endswith(suffix) and len(name) > len(suffix):
            short_name = name[:-len(suffix)]
            if short_name and short_name not in _AREA_CODE_INDEX:
                _AREA_CODE_INDEX[short_name] = result


def search_area_code(name: str) -> Dict[str, Any]:
    """
    搜索地域编码
    
    Args:
        name: 地域名称（如"海淀"、"北京海淀区"、"上海"等）
        
    Returns:
        {
            "query": "搜索词",
            "count": 匹配数量,
            "results": [匹配结果列表]
        }
    """
    # 确保数据已加载
    _load_area_codes()
    
    results: List[AreaCodeResult] = []
    
    # 清理输入
    name = name.strip()
    if not name:
        return {"query": name, "count": 0, "results": []}
    
    # 1. 直接匹配
    if name in _AREA_CODE_INDEX:
        results.append(_AREA_CODE_INDEX[name])
    
    # 2. 组合地名解析（如"北京海淀"、"上海徐汇"）- 找最精确的匹配（优先县级）
    if not results:
        best_match = None
        best_priority = -1  # 县级=3, 市级=2, 省级=1
        for key, value in _AREA_CODE_INDEX.items():
            if key in name:
                # 计算优先级：县级 > 市级 > 省级
                if value.county_code:
                    priority = 3
                elif value.city_code:
                    priority = 2
                else:
                    priority = 1
                
                if priority > best_priority:
                    best_match = value
                    best_priority = priority
        if best_match:
            results.append(best_match)
    
    # 3. 模糊匹配（如果组合匹配也失败）
    if not results:
        for key, value in _AREA_CODE_INDEX.items():
            if name in key or key in name:
                results.append(value)
                break
    
    return {
        "query": name,
        "count": len(results),
        "results": [r.to_dict() for r in results]
    }


def get_area_codes(area_names: List[str]) -> List[str]:
    """
    批量获取地域编码
    
    Args:
        area_names: 地域名称列表
        
    Returns:
        地域编码列表（去重）
    """
    codes = set()
    for name in area_names:
        result = search_area_code(name)
        for r in result["results"]:
            # 优先使用最精确的编码
            if r.get("county_code"):
                codes.add(r["county_code"])
            elif r.get("city_code"):
                codes.add(r["city_code"])
            elif r.get("province_code"):
                codes.add(r["province_code"])
    
    return list(codes)


def parse_area_codes(area_names: List[str]) -> List[str]:
    """
    将地域名称列表转换为国标区域编码列表
    
    Args:
        area_names: 地域名称列表，如 ["北京", "上海", "江苏"]
        
    Returns:
        地域编码列表，如 ["110000", "310000", "320000"]
    """
    if not area_names:
        return []
    
    return get_area_codes(area_names)


def parse_single_area(area_name: str) -> dict:
    """
    查询单个地域的详细信息
    
    Args:
        area_name: 地域名称，如 "北京"、"海淀"、"江苏"
        
    Returns:
        地域详细信息字典
    """
    return search_area_code(area_name)


def get_area_display_name(area_names: List[str]) -> str:
    """获取地域的展示名称"""
    if not area_names:
        return "全国"
    return "、".join(area_names)


def main():
    parser = argparse.ArgumentParser(
        description='地域名称与国标区域编码转换工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --area "北京"                      # 查询单个地域编码
  %(prog)s --area "江苏,南京,上海" --batch     # 批量查询地域编码
  %(prog)s --search "海淀"                    # 搜索地域详细信息
  %(prog)s --list                             # 列出常见地域编码
        """
    )
    
    parser.add_argument('--area', '-a', help='地域名称，多个用逗号分隔（如：北京,上海,江苏）')
    parser.add_argument('--batch', '-b', action='store_true', help='批量模式（与--area配合）')
    parser.add_argument('--search', '-s', help='搜索地域详细信息')
    parser.add_argument('--list', '-l', action='store_true', help='列出常见省市编码')
    
    args = parser.parse_args()
    
    # 列出常见地域编码
    if args.list:
        common_areas = {
            "北京": "110000", "天津": "120000", "河北": "130000", "山西": "140000",
            "内蒙古": "150000", "辽宁": "210000", "吉林": "220000", "黑龙江": "230000",
            "上海": "310000", "江苏": "320000", "浙江": "330000", "安徽": "340000",
            "福建": "350000", "江西": "360000", "山东": "370000", "河南": "410000",
            "湖北": "420000", "湖南": "430000", "广东": "440000", "广西": "450000",
            "海南": "460000", "重庆": "500000", "四川": "510000", "贵州": "520000",
            "云南": "530000", "西藏": "540000", "陕西": "610000", "甘肃": "620000",
            "青海": "630000", "宁夏": "640000", "新疆": "650000",
        }
        print("常见省市国标区域编码：")
        print("-" * 40)
        for name, code in common_areas.items():
            print(f"  {name:8s} -> {code}")
        return
    
    # 搜索模式
    if args.search:
        result = parse_single_area(args.search)
        print(f"查询: {result['query']}")
        print(f"匹配数: {result['count']}")
        if result['results']:
            print("结果:")
            for r in result['results']:
                print(f"  省份: {r['province']} ({r['province_code']})")
                if r['city']:
                    print(f"  城市: {r['city']} ({r['city_code']})")
                if r['county']:
                    print(f"  区县: {r['county']} ({r['county_code']})")
        else:
            print("未找到匹配结果")
        return
    
    # 批量查询模式
    if args.area:
        if args.batch:
            # 批量解析
            areas = [a.strip() for a in args.area.split(',') if a.strip()]
            codes = parse_area_codes(areas)
            print(f"地域: {get_area_display_name(areas)}")
            print(f"编码: {codes}")
        else:
            # 单个查询详细信息
            result = parse_single_area(args.area)
            print(f"查询: {result['query']}")
            print(f"匹配数: {result['count']}")
            if result['results']:
                r = result['results'][0]
                print(f"编码: {r['province_code'] or r['city_code'] or r['county_code']}")
                print(f"省份: {r['province']}")
                if r['city']:
                    print(f"城市: {r['city']}")
                if r['county']:
                    print(f"区县: {r['county']}")
            else:
                print("未找到匹配结果")
        return
    
    # 无参数时显示帮助
    parser.print_help()


if __name__ == "__main__":
    main()
