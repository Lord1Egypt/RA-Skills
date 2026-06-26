#!/usr/bin/env python3
"""
自然语言解析模块
解析用户输入，提取出发城市、到达城市、日期、航班号等信息
"""

import re
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import dateparser

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NaturalLanguageParser:
    """自然语言解析类"""
    
    def __init__(self):
        """初始化"""
        # 城市名列表（常见国内城市）
        self.cities = [
            '北京', '上海', '广州', '深圳', '成都', '重庆', '杭州', '南京',
            '武汉', '西安', '长沙', '青岛', '厦门', '昆明', '大连', '沈阳',
            '天津', '郑州', '哈尔滨', '长春', '无锡', '苏州', '宁波', '温州',
            '合肥', '福州', '济南', '南宁', '海口', '贵阳', '兰州', '西宁',
            '银川', '乌鲁木齐', '拉萨'
        ]
        
        # 航班号正则模式（两位字母+3-4位数字）
        self.flight_no_pattern = r'([A-Z]{2}\d{3,4})'
        
        # 机场代码映射（城市名->三字码）
        self.city_to_airport = {
            '北京': 'PEK', '上海': 'SHA', '广州': 'CAN', '深圳': 'SZX',
            '成都': 'CTU', '重庆': 'CKG', '杭州': 'HGH', '南京': 'NKG',
            '武汉': 'WUH', '西安': 'XIY', '长沙': 'CSX', '青岛': 'TAO',
            '厦门': 'XMN', '昆明': 'KMG', '大连': 'DLC', '沈阳': 'SHE',
            '天津': 'TSN', '郑州': 'CGO', '哈尔滨': 'HRB', '长春': 'CGQ',
            '无锡': 'WUX', '苏州': 'SZV', '宁波': 'NGB', '温州': 'WNZ',
            '合肥': 'HFE', '福州': 'FOC', '济南': 'TNA', '南宁': 'NNG',
            '海口': 'HAK', '贵阳': 'KWE', '兰州': 'LHW', '西宁': 'XNN',
            '银川': 'INC', '乌鲁木齐': 'URC', '拉萨': 'LXA'
        }
    
    def parse(self, query: str) -> Dict:
        """
        解析自然语言查询
        
        Args:
            query: 自然语言查询字符串
            
        Returns:
            解析后的参数字典，包含以下字段：
            - from_city: 出发城市
            - to_city: 到达城市
            - date: 日期 (YYYY-MM-DD格式)
            - flight_no: 航班号（可选）
            - action: 操作类型（query/subscribe/monitor）
            - cabin: 舱位（默认economy）
            - parsed_successfully: 是否成功解析
        """
        # 初始化结果
        result = {
            'from_city': None,
            'to_city': None,
            'date': None,
            'flight_no': None,
            'action': 'query',  # query/subscribe/monitor
            'cabin': 'economy',
            'parsed_successfully': False,
            'original_query': query
        }
        
        # 1. 识别操作类型
        subscribe_keywords = ['订阅', '监控', '关注', '设置提醒', '提醒', '监控一下']
        for keyword in subscribe_keywords:
            if keyword in query:
                result['action'] = 'subscribe'
                break
        
        # 2. 提取航班号
        flight_match = re.search(self.flight_no_pattern, query.upper())
        if flight_match:
            result['flight_no'] = flight_match.group(1)
            logger.info(f"识别到航班号: {result['flight_no']}")
        
        # 3. 提取日期信息
        date_str = self._extract_date(query)
        if date_str:
            result['date'] = date_str
        else:
            # 默认3天后
            default_date = datetime.now() + timedelta(days=3)
            result['date'] = default_date.strftime('%Y-%m-%d')
        
        # 4. 提取城市对
        cities_found = []
        for city in self.cities:
            if city in query:
                cities_found.append(city)
        
        # 如果找到两个城市，尝试确定顺序
        if len(cities_found) >= 2:
            # 查找分隔符
            separators = ['到', '飞', '至', '→']
            for sep in separators:
                if sep in query:
                    parts = query.split(sep)
                    if len(parts) >= 2:
                        # 检查每个部分包含的城市
                        for city in cities_found:
                            if city in parts[0] and result['from_city'] is None:
                                result['from_city'] = city
                            elif city in parts[1] and result['to_city'] is None:
                                result['to_city'] = city
            
            # 如果还是没确定，取前两个作为出发和到达
            if result['from_city'] is None and result['to_city'] is None:
                result['from_city'] = cities_found[0]
                result['to_city'] = cities_found[1]
        
        # 5. 如果有航班号但没有城市，尝试根据航班号推断航空公司
        if result['flight_no'] and (not result['from_city'] or not result['to_city']):
            # 这里可以扩展：根据航班号前缀推断航空公司，但需要外部数据
            pass
        
        # 6. 判断是否成功解析
        if result['from_city'] and result['to_city']:
            result['parsed_successfully'] = True
        elif result['flight_no']:
            # 仅有航班号也算成功（后续需要根据航班号查询城市）
            result['parsed_successfully'] = True
        
        logger.info(f"解析结果: {result}")
        return result
    
    def _extract_date(self, query: str) -> Optional[str]:
        """
        从查询字符串中提取日期
        
        Args:
            query: 查询字符串
            
        Returns:
            日期字符串 (YYYY-MM-DD) 或 None
        """
        # 日期模式
        patterns = [
            (r'(今天)', 0),
            (r'(明天)', 1),
            (r'(后天)', 2),
            (r'(大后天)', 3),
            (r'(\d{1,2})月(\d{1,2})日', None),  # 3月16日
            (r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', None),  # 2026-03-16
            (r'(\d{1,2})[-/.](\d{1,2})', None),  # 3.16 或 3-16
        ]
        
        base_date = datetime.now()
        
        for pattern, day_offset in patterns:
            match = re.search(pattern, query)
            if match:
                try:
                    if day_offset is not None:
                        # 今天/明天/后天/大后天
                        target_date = base_date + timedelta(days=day_offset)
                        return target_date.strftime('%Y-%m-%d')
                    
                    elif '月' in pattern and '日' in pattern:
                        # 3月16日格式
                        month = int(match.group(1))
                        day = int(match.group(2))
                        year = base_date.year
                        # 如果月份小于当前月份，可能是明年
                        if month < base_date.month:
                            year += 1
                        target_date = datetime(year, month, day)
                        return target_date.strftime('%Y-%m-%d')
                    
                    elif len(match.groups()) == 3:
                        # YYYY-MM-DD格式
                        year = int(match.group(1))
                        month = int(match.group(2))
                        day = int(match.group(3))
                        target_date = datetime(year, month, day)
                        return target_date.strftime('%Y-%m-%d')
                    
                    elif len(match.groups()) == 2:
                        # MM-DD或M.D格式
                        month = int(match.group(1))
                        day = int(match.group(2))
                        year = base_date.year
                        # 如果月份小于当前月份，可能是明年
                        if month < base_date.month:
                            year += 1
                        target_date = datetime(year, month, day)
                        return target_date.strftime('%Y-%m-%d')
                        
                except (ValueError, IndexError) as e:
                    logger.warning(f"日期解析失败: {match.group()}, 错误: {e}")
                    continue
        
        # 尝试使用dateparser库
        try:
            parsed = dateparser.parse(query, languages=['zh'])
            if parsed:
                return parsed.strftime('%Y-%m-%d')
        except Exception as e:
            logger.warning(f"dateparser解析失败: {e}")
        
        return None
    
    def get_airport_code(self, city_name: str) -> str:
        """
        获取城市对应的机场代码
        
        Args:
            city_name: 城市名
            
        Returns:
            机场三字码，如果找不到返回原城市名
        """
        clean_city = city_name.replace('市', '').strip()
        return self.city_to_airport.get(clean_city, clean_city)


def test_parser():
    """测试解析器"""
    parser = NaturalLanguageParser()
    
    test_cases = [
        "帮我查一下3.16日北京到成都的机票价格",
        "监控一下CA1611航班的价格波动情况",
        "订阅上海到广州的机票价格，监控一周",
        "查询明天北京到深圳的机票",
        "3月20日杭州到西安的飞机票",
        "CA1830航班明天什么价格",
    ]
    
    for query in test_cases:
        print(f"\n查询: {query}")
        result = parser.parse(query)
        print(f"结果: {json.dumps(result, ensure_ascii=False, indent=2)}")


if __name__ == '__main__':
    test_parser()