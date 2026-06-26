#!/usr/bin/env python3
"""旅行历史记录管理器

记录用户去过的城市，支持查询、添加、删除操作。
数据存储在本地 JSON 文件中，确保盲盒推荐不重复。

使用方法:
    python history_manager.py add --city 杭州 --date 2026-04-01
    python history_manager.py list-visited-cities --current-location 上海
    python history_manager.py remove --city 杭州
    python history_manager.py show-history
"""

import json
import os
import sys
import argparse
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path


class HistoryManager:
    """旅行历史记录管理器"""
    
    # 默认存储路径
    DEFAULT_STORAGE_PATH = Path.home() / ".qoderwork" / "travel-blind-box" / "history.json"
    
    def __init__(self, storage_path: Optional[Path] = None):
        """
        初始化历史记录管理器
        
        Args:
            storage_path: 数据存储路径，默认使用 ~/.qoderwork/travel-blind-box/history.json
        """
        self.storage_path = storage_path or self.DEFAULT_STORAGE_PATH
        self._ensure_storage_dir()
        self.data = self._load_data()
    
    def _ensure_storage_dir(self):
        """确保存储目录存在"""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_data(self) -> Dict:
        """加载历史数据"""
        if not self.storage_path.exists():
            return {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "visited_cities": []  # 列表项：{"city": "杭州", "date": "2026-04-01", "notes": ""}
            }
        
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 确保数据结构完整
                if "visited_cities" not in data:
                    data["visited_cities"] = []
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"警告：读取历史文件失败，将创建新文件 - {e}", file=sys.stderr)
            return {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "visited_cities": []
            }
    
    def _save_data(self):
        """保存数据到文件"""
        self.data["updated_at"] = datetime.now().isoformat()
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_visited_city(self, city: str, date: str, notes: str = "") -> bool:
        """
        添加去过的城市记录
        
        Args:
            city: 城市名称
            date: 出行日期（YYYY-MM-DD）
            notes: 备注信息（可选）
        
        Returns:
            bool: 添加成功返回 True
        """
        # 检查是否已存在
        for record in self.data["visited_cities"]:
            if record["city"].lower() == city.lower():
                print(f"提示：{city} 已在历史记录中，将更新日期", file=sys.stderr)
                record["date"] = date
                if notes:
                    record["notes"] = notes
                self._save_data()
                return True
        
        # 添加新记录
        self.data["visited_cities"].append({
            "city": city,
            "date": date,
            "notes": notes
        })
        self._save_data()
        print(f"✓ 已记录：{city}（{date}）")
        return True
    
    def get_visited_cities(self) -> List[str]:
        """
        获取所有去过的城市列表
        
        Returns:
            城市名称列表
        """
        return [record["city"] for record in self.data["visited_cities"]]
    
    def has_visited(self, city: str) -> bool:
        """
        检查是否去过某个城市
        
        Args:
            city: 城市名称
        
        Returns:
            bool: 去过返回 True
        """
        return any(record["city"].lower() == city.lower() 
                   for record in self.data["visited_cities"])
    
    def remove_city(self, city: str) -> bool:
        """
        删除某个城市的历史记录
        
        Args:
            city: 城市名称
        
        Returns:
            bool: 删除成功返回 True
        """
        original_count = len(self.data["visited_cities"])
        self.data["visited_cities"] = [
            record for record in self.data["visited_cities"]
            if record["city"].lower() != city.lower()
        ]
        
        if len(self.data["visited_cities"]) < original_count:
            self._save_data()
            print(f"✓ 已删除：{city}")
            return True
        else:
            print(f"提示：{city} 不在历史记录中", file=sys.stderr)
            return False
    
    def get_recent_cities(self, limit: int = 10) -> List[Dict]:
        """
        获取最近去过的城市（按日期排序）
        
        Args:
            limit: 返回数量限制
        
        Returns:
            城市记录列表（包含 city, date, notes）
        """
        sorted_cities = sorted(
            self.data["visited_cities"],
            key=lambda x: x.get("date", ""),
            reverse=True
        )
        return sorted_cities[:limit]
    
    def suggest_destinations(self, current_location: str, 
                             exclude_visited: bool = True) -> List[str]:
        """
        根据当前位置推荐适合的城市（排除去过的城市）
        
        Args:
            current_location: 当前所在城市
            exclude_visited: 是否排除去过的城市
        
        Returns:
            推荐城市列表
        """
        # 这里只是一个简单示例，实际应该调用 flyai skill 或数据库
        # 根据地理位置推荐周边城市
        
        # 简单的城市关联映射（实际应该更复杂）
        nearby_cities_map = {
            "上海": ["苏州", "杭州", "南京", "无锡", "宁波", "绍兴", "扬州", "乌镇"],
            "北京": ["天津", "承德", "秦皇岛", "张家口", "保定"],
            "广州": ["深圳", "珠海", "佛山", "东莞", "中山", "惠州"],
            "成都": ["重庆", "都江堰", "乐山", "峨眉山", "绵阳"],
            "武汉": ["宜昌", "襄阳", "十堰", "荆州"],
            "西安": ["咸阳", "宝鸡", "渭南", "汉中"],
            # ... 可以扩展更多
        }
        
        nearby = nearby_cities_map.get(current_location, [])
        
        if exclude_visited:
            visited = set(self.get_visited_cities())
            nearby = [city for city in nearby if city not in visited]
        
        return nearby
    
    def export_history(self, output_path: Path) -> bool:
        """
        导出历史记录到文件
        
        Args:
            output_path: 输出文件路径
        
        Returns:
            bool: 导出成功返回 True
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            print(f"✓ 已导出历史记录到：{output_path}")
            return True
        except IOError as e:
            print(f"错误：导出失败 - {e}", file=sys.stderr)
            return False
    
    def import_history(self, input_path: Path, merge: bool = True) -> bool:
        """
        从文件导入历史记录
        
        Args:
            input_path: 输入文件路径
            merge: 是否合并（True）或覆盖（False）
        
        Returns:
            bool: 导入成功返回 True
        """
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                imported_data = json.load(f)
            
            if merge:
                # 合并模式：添加不重复的记录
                existing_cities = set(self.get_visited_cities())
                new_records = [
                    record for record in imported_data.get("visited_cities", [])
                    if record["city"] not in existing_cities
                ]
                self.data["visited_cities"].extend(new_records)
                print(f"✓ 导入了 {len(new_records)} 条新记录")
            else:
                # 覆盖模式
                self.data = imported_data
                print("✓ 已覆盖历史记录")
            
            self._save_data()
            return True
        except (json.JSONDecodeError, IOError) as e:
            print(f"错误：导入失败 - {e}", file=sys.stderr)
            return False
    
    def show_statistics(self):
        """显示统计信息"""
        cities = self.get_visited_cities()
        print("\n📊 旅行统计")
        print("=" * 50)
        print(f"已去过城市数：{len(cities)}")
        
        if cities:
            print(f"最近去过：{', '.join(cities[-5:])}")
            
            # 按年份统计
            years = {}
            for record in self.data["visited_cities"]:
                year = record.get("date", "")[:4]
                if year.isdigit():
                    years[year] = years.get(year, 0) + 1
            
            if years:
                print("\n按年份:")
                for year in sorted(years.keys()):
                    print(f"  {year}年：{years[year]}个城市")
        
        print("=" * 50)


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="旅行历史记录管理器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s add --city 杭州 --date 2026-04-01
  %(prog)s list-visited-cities --current-location 上海
  %(prog)s remove --city 杭州
  %(prog)s show-history
  %(prog)s suggest --current-location 上海
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='添加去过的城市')
    add_parser.add_argument('--city', required=True, help='城市名称')
    add_parser.add_argument('--date', required=True, help='出行日期（YYYY-MM-DD）')
    add_parser.add_argument('--notes', default='', help='备注信息')
    
    # list-visited-cities 命令
    list_parser = subparsers.add_parser('list-visited-cities', help='列出去过的城市')
    list_parser.add_argument('--current-location', help='当前所在城市（用于过滤推荐）')
    list_parser.add_argument('--format', choices=['text', 'json'], default='text', 
                            help='输出格式')
    
    # remove 命令
    remove_parser = subparsers.add_parser('remove', help='删除某个城市记录')
    remove_parser.add_argument('--city', required=True, help='城市名称')
    
    # show-history 命令
    show_parser = subparsers.add_parser('show-history', help='显示完整历史记录')
    show_parser.add_argument('--stats', action='store_true', help='显示统计信息')
    
    # suggest 命令
    suggest_parser = subparsers.add_parser('suggest', help='推荐目的地')
    suggest_parser.add_argument('--current-location', required=True, help='当前所在城市')
    suggest_parser.add_argument('--count', type=int, default=5, help='推荐数量')
    
    args = parser.parse_args()
    
    # 创建管理器实例
    manager = HistoryManager()
    
    # 执行命令
    if args.command == 'add':
        manager.add_visited_city(args.city, args.date, args.notes)
    
    elif args.command == 'list-visited-cities':
        cities = manager.get_visited_cities()
        if args.format == 'json':
            print(json.dumps(cities, ensure_ascii=False))
        else:
            if cities:
                print("去过的城市:")
                for city in cities:
                    print(f"  - {city}")
            else:
                print("暂无历史记录")
    
    elif args.command == 'remove':
        manager.remove_city(args.city)
    
    elif args.command == 'show-history':
        if args.stats:
            manager.show_statistics()
        else:
            recent = manager.get_recent_cities(20)
            if recent:
                print("最近去过的城市:")
                for record in recent:
                    print(f"  {record['city']} ({record['date']}) - {record.get('notes', '')}")
            else:
                print("暂无历史记录")
    
    elif args.command == 'suggest':
        suggestions = manager.suggest_destinations(args.current_location, exclude_visited=True)
        if suggestions:
            print(f"从 {args.current_location} 出发，推荐以下未去过的城市:")
            for i, city in enumerate(suggestions[:args.count], 1):
                print(f"  {i}. {city}")
        else:
            print("暂无推荐或所有周边城市都已去过")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
