#!/usr/bin/env python3
"""
操盘手习惯分析器 - 用于分析和学习特定股票的操盘手行为模式
"""

import json
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from pathlib import Path


class TraderAnalyzer:
    """
    操盘手习惯分析器
    通过长期监控单支股票，学习操盘手的行为模式和习惯
    """
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(__file__), "..", "data", "trader_patterns.db")
        
        # 确保数据目录存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建操盘手行为模式表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trader_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code TEXT NOT NULL,
                pattern_type TEXT NOT NULL,  -- 'timing', 'volume', 'price_action', 'support_resistance'
                pattern_key TEXT NOT NULL,   -- 具体的模式标识
                frequency INTEGER DEFAULT 1, -- 模式出现频率
                strength REAL DEFAULT 0.0,   -- 模式强度 (0-1)
                last_seen TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建交易行为记录表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trading_behaviors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code TEXT NOT NULL,
                date DATE NOT NULL,
                time_period TEXT NOT NULL,   -- 'morning', 'noon', 'afternoon'
                volume_behavior TEXT,        -- 'surge', 'normal', 'shrink'
                price_behavior TEXT,         -- 'breakout', 'reversal', 'consolidation'
                trend_direction TEXT,        -- 'up', 'down', 'sideways'
                strength_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建支撑阻力位表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS support_resistance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code TEXT NOT NULL,
                level_type TEXT NOT NULL,    -- 'support', 'resistance'
                price_level REAL NOT NULL,
                frequency INTEGER DEFAULT 1, -- 该价位被测试次数
                success_rate REAL DEFAULT 0.0, -- 该价位的有效性
                last_tested TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def record_trading_behavior(self, stock_code: str, date: str, time_period: str, 
                              volume_behavior: str, price_behavior: str, trend_direction: str,
                              strength_score: float = 0.5):
        """记录特定日期的交易行为"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO trading_behaviors 
            (stock_code, date, time_period, volume_behavior, price_behavior, trend_direction, strength_score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (stock_code, date, time_period, volume_behavior, price_behavior, trend_direction, strength_score))
        
        conn.commit()
        conn.close()
    
    def update_pattern_frequency(self, stock_code: str, pattern_type: str, pattern_key: str):
        """更新模式频率统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否已存在该模式
        cursor.execute("""
            SELECT frequency, strength FROM trader_patterns 
            WHERE stock_code = ? AND pattern_type = ? AND pattern_key = ?
        """, (stock_code, pattern_type, pattern_key))
        
        result = cursor.fetchone()
        if result:
            freq, strength = result
            new_freq = freq + 1
            # 简单的强度计算：随着频率增加，强度逐渐提高，但有上限
            new_strength = min(1.0, strength + 0.1)
            cursor.execute("""
                UPDATE trader_patterns 
                SET frequency = ?, strength = ?, last_seen = CURRENT_TIMESTAMP
                WHERE stock_code = ? AND pattern_type = ? AND pattern_key = ?
            """, (new_freq, new_strength, stock_code, pattern_type, pattern_key))
        else:
            cursor.execute("""
                INSERT INTO trader_patterns 
                (stock_code, pattern_type, pattern_key, frequency, strength, last_seen)
                VALUES (?, ?, ?, 1, 0.1, CURRENT_TIMESTAMP)
            """, (stock_code, pattern_type, pattern_key))
        
        conn.commit()
        conn.close()
    
    def analyze_time_patterns(self, stock_code: str) -> Dict:
        """分析操盘手的时间模式"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 分析不同时间段的活跃程度
        cursor.execute("""
            SELECT time_period, COUNT(*) as count
            FROM trading_behaviors 
            WHERE stock_code = ?
            GROUP BY time_period
            ORDER BY count DESC
        """, (stock_code,))
        
        time_patterns = {}
        for period, count in cursor.fetchall():
            time_patterns[period] = count
        
        conn.close()
        
        return time_patterns
    
    def analyze_volume_patterns(self, stock_code: str) -> Dict:
        """分析操盘手的成交量模式"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT volume_behavior, COUNT(*) as count
            FROM trading_behaviors 
            WHERE stock_code = ?
            GROUP BY volume_behavior
            ORDER BY count DESC
        """, (stock_code,))
        
        volume_patterns = {}
        for behavior, count in cursor.fetchall():
            volume_patterns[behavior] = count
        
        conn.close()
        
        return volume_patterns
    
    def analyze_price_patterns(self, stock_code: str) -> Dict:
        """分析操盘手的价格行为模式"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT price_behavior, COUNT(*) as count
            FROM trading_behaviors 
            WHERE stock_code = ?
            GROUP BY price_behavior
            ORDER BY count DESC
        """, (stock_code,))
        
        price_patterns = {}
        for behavior, count in cursor.fetchall():
            price_patterns[behavior] = count
        
        conn.close()
        
        return price_patterns
    
    def identify_support_resistance(self, stock_code: str, price: float) -> Tuple[str, float]:
        """
        识别价格是否接近支撑或阻力位
        返回: ('support'|'resistance'|None, strength)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 查找附近的支撑阻力位 (在价格的2%范围内)
        tolerance = price * 0.02
        
        cursor.execute("""
            SELECT level_type, price_level, success_rate, frequency
            FROM support_resistance
            WHERE stock_code = ? AND ABS(price_level - ?) <= ?
            ORDER BY ABS(price_level - ?) ASC
        """, (stock_code, price, tolerance, price))
        
        results = cursor.fetchall()
        conn.close()
        
        if results:
            level_type, level_price, success_rate, frequency = results[0]
            # 计算接近度强度 (越接近强度越高)
            proximity = 1.0 - abs(price - level_price) / tolerance
            combined_strength = min(1.0, (success_rate * 0.6 + proximity * 0.4))
            return level_type, combined_strength
        
        return None, 0.0
    
    def record_support_resistance(self, stock_code: str, price_level: float, level_type: str):
        """记录新的支撑或阻力位"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 检查是否已存在该价位
        cursor.execute("""
            SELECT frequency, success_rate FROM support_resistance
            WHERE stock_code = ? AND price_level = ? AND level_type = ?
        """, (stock_code, price_level, level_type))
        
        result = cursor.fetchone()
        if result:
            freq, success_rate = result
            new_freq = freq + 1
            # 简单的成功率更新逻辑
            new_success_rate = min(1.0, success_rate + 0.05)
            cursor.execute("""
                UPDATE support_resistance
                SET frequency = ?, success_rate = ?, last_tested = CURRENT_TIMESTAMP
                WHERE stock_code = ? AND price_level = ? AND level_type = ?
            """, (new_freq, new_success_rate, stock_code, price_level, level_type))
        else:
            cursor.execute("""
                INSERT INTO support_resistance
                (stock_code, level_type, price_level, frequency, success_rate, last_tested)
                VALUES (?, ?, ?, 1, 0.5, CURRENT_TIMESTAMP)
            """, (stock_code, level_type, price_level))
        
        conn.commit()
        conn.close()
    
    def generate_trader_profile(self, stock_code: str) -> Dict:
        """生成操盘手行为档案"""
        time_patterns = self.analyze_time_patterns(stock_code)
        volume_patterns = self.analyze_volume_patterns(stock_code)
        price_patterns = self.analyze_price_patterns(stock_code)
        
        # 获取高频模式
        common_time = max(time_patterns.items(), key=lambda x: x[1])[0] if time_patterns else "unknown"
        common_volume = max(volume_patterns.items(), key=lambda x: x[1])[0] if volume_patterns else "normal"
        common_price = max(price_patterns.items(), key=lambda x: x[1])[0] if price_patterns else "consolidation"
        
        return {
            "stock_code": stock_code,
            "time_preference": common_time,
            "volume_behavior": common_volume,
            "price_behavior": common_price,
            "time_patterns": time_patterns,
            "volume_patterns": volume_patterns,
            "price_patterns": price_patterns,
            "profile_generated_at": datetime.now().isoformat()
        }
    
    def detect_trader_habit(self, stock_code: str, current_data: Dict) -> List[str]:
        """检测当前数据是否符合操盘手习惯"""
        habits = []
        
        # 分析时间习惯
        time_patterns = self.analyze_time_patterns(stock_code)
        if time_patterns:
            # 获取最活跃的时间段
            most_active_time = max(time_patterns.items(), key=lambda x: x[1])[0]
            current_hour = datetime.now().hour
            
            # 判断当前时间是否符合活跃时段
            time_match = False
            if most_active_time == "morning" and 9 <= current_hour <= 11:
                time_match = True
            elif most_active_time == "noon" and 11 <= current_hour <= 13:
                time_match = True
            elif most_active_time == "afternoon" and 13 <= current_hour <= 15:
                time_match = True
            
            if time_match:
                habits.append(f"⏰ 符合操盘手活跃时段 ({most_active_time})")
        
        # 分析成交量习惯
        volume_patterns = self.analyze_volume_patterns(stock_code)
        if volume_patterns:
            most_common_volume = max(volume_patterns.items(), key=lambda x: x[1])[0]
            # 这里需要根据当前成交量判断是否匹配
            habits.append(f"📊 符合操盘手成交量习惯 ({most_common_volume})")
        
        # 分析价格行为习惯
        price_patterns = self.analyze_price_patterns(stock_code)
        if price_patterns:
            most_common_price = max(price_patterns.items(), key=lambda x: x[1])[0]
            habits.append(f"📈 符合操盘手价格行为习惯 ({most_common_price})")
        
        return habits
    
    def detect_abnormal_behavior(self, stock_code: str, current_data: Dict) -> List[str]:
        """检测操盘手异常行为"""
        abnormalities = []
        
        # 检查成交量异常（放量3倍以上）
        current_volume = current_data.get('volume', 0)
        if current_volume > 0:
            # 获取5日均量
            from monitor import StockAlert
            monitor = StockAlert()
            ma5_volume = monitor.fetch_volume_ma5(stock_code, 1 if stock_code.startswith('6') else 0)
            if ma5_volume > 0:
                volume_ratio = current_volume / ma5_volume
                if volume_ratio >= 3.0:  # 放量3倍以上视为异常
                    abnormalities.append(f"📊 操盘手异常放量 {volume_ratio:.1f}倍 (5日均量)")
        
        # 检查非活跃时段异动
        time_patterns = self.analyze_time_patterns(stock_code)
        if time_patterns:
            most_active_time = max(time_patterns.items(), key=lambda x: x[1])[0]
            current_hour = datetime.now().hour
            
            # 判断当前是否在非活跃时段
            non_active = True
            if most_active_time == "morning" and 9 <= current_hour <= 11:
                non_active = False
            elif most_active_time == "noon" and 11 <= current_hour <= 13:
                non_active = False
            elif most_active_time == "afternoon" and 13 <= current_hour <= 15:
                non_active = False
            
            if non_active:
                # 但在当前时段有明显价格变动
                change_pct = abs((current_data.get('price', 0) - current_data.get('prev_close', 1)) / current_data.get('prev_close', 1) * 100)
                if change_pct >= 2.0:  # 价格变动超过2%
                    abnormalities.append(f"⏰ 非活跃时段异动 {change_pct:.1f}%")
        
        return abnormalities
    
    def learn_from_price_action(self, stock_code: str, current_data: Dict):
        """从当前价格行为中学习"""
        price = current_data.get('price', 0)
        prev_close = current_data.get('prev_close', 0)
        volume = current_data.get('volume', 0)
        
        if prev_close > 0:
            change_pct = (price - prev_close) / prev_close * 100
            
            # 分析价格行为
            if abs(change_pct) > 3:
                behavior_type = "breakout" if change_pct > 0 else "reversal"
                self.update_pattern_frequency(stock_code, "price_action", behavior_type)
            else:
                self.update_pattern_frequency(stock_code, "price_action", "consolidation")
        
        # 分析成交量行为
        if volume > 0:
            # 需要对比历史均量才能判断
            volume_behavior = "normal"  # 简化处理
            self.update_pattern_frequency(stock_code, "volume_behavior", volume_behavior)
        
        # 记录当前交易行为
        current_date = datetime.now().strftime('%Y-%m-%d')
        current_hour = datetime.now().hour
        
        # 确定时间段
        if 9 <= current_hour <= 11:
            time_period = "morning"
        elif 11 < current_hour <= 13:
            time_period = "noon"
        elif 13 <= current_hour <= 15:
            time_period = "afternoon"
        else:
            time_period = "after_hours"
        
        self.record_trading_behavior(
            stock_code=stock_code,
            date=current_date,
            time_period=time_period,
            volume_behavior="normal",
            price_behavior="consolidation",
            trend_direction="sideways",
            strength_score=0.5
        )


    def detect_abnormal_behavior(self, stock_code: str, current_data: Dict) -> List[str]:
        """
        检测操盘手异常行为（只在真正异常时预警）
        返回异常行为列表，空列表表示无异常
        """
        abnormalities = []
        
        price = current_data.get('price', 0)
        prev_close = current_data.get('prev_close', 0)
        volume = current_data.get('volume', 0)
        current_hour = datetime.now().hour
        
        if prev_close > 0:
            change_pct = (price - prev_close) / prev_close * 100
        
        # 1. 成交量异常检测（放量>3 倍）
        if volume > 0:
            ma5_volume = self._get_ma5_volume(stock_code)
            if ma5_volume > 0:
                volume_ratio = volume / ma5_volume
                if volume_ratio >= 3.0:
                    abnormalities.append(f"📊 成交量异常：放量{volume_ratio:.1f}倍（5 日均量）")
                elif volume_ratio <= 0.3:
                    abnormalities.append(f"📉 成交量异常：缩量{volume_ratio:.1f}倍（5 日均量）")
        
        # 2. 非活跃时段突然行动
        time_patterns = self.analyze_time_patterns(stock_code)
        if time_patterns:
            most_active_time = max(time_patterns.items(), key=lambda x: x[1])[0] if time_patterns else "unknown"
            
            # 判断当前是否是非活跃时段
            is_inactive = False
            if most_active_time == "morning" and not (9 <= current_hour <= 11):
                is_inactive = True
            elif most_active_time == "afternoon" and not (13 <= current_hour <= 15):
                is_inactive = True
            
            # 非活跃时段 + 放量 = 异常
            if is_inactive and volume > 0:
                ma5_volume = self._get_ma5_volume(stock_code)
                if ma5_volume > 0 and volume / ma5_volume >= 2.0:
                    abnormalities.append(f"⚡ 非活跃时段异动：{current_hour}点放量（习惯时段：{most_active_time}）")
        
        # 3. 价格突破关键位（支撑/阻力）
        level_type, strength = self.identify_support_resistance(stock_code, price)
        if level_type and strength >= 0.8:
            level_text = "突破" if level_type == "resistance" else "跌破"
            abnormalities.append(f"🎯 {level_text}关键位（强度{strength:.0%}）")
        
        # 4. 价格行为与历史模式明显不同
        price_patterns = self.analyze_price_patterns(stock_code)
        if price_patterns:
            most_common = max(price_patterns.items(), key=lambda x: x[1])[0] if price_patterns else "consolidation"
            current_behavior = "breakout" if abs(change_pct) > 3 else "consolidation"
            
            if most_common == "consolidation" and current_behavior == "breakout":
                abnormalities.append(f"📈 打破盘整：涨跌幅{change_pct:+.1f}%（习惯：盘整）")
        
        return abnormalities


    def _get_ma5_volume(self, stock_code: str) -> float:
        """获取 5 日平均成交量（简化版，实际应从数据库读取）"""
        # TODO: 从数据库读取历史成交量
        return 0


def integrate_with_monitor(monitor_class):
    """将操盘手分析功能集成到监控类中"""
    original_init = monitor_class.__init__
    original_check_alerts = monitor_class.check_alerts
    
    def new_init(self):
        original_init(self)
        self.trader_analyzer = TraderAnalyzer()
    
    def new_check_alerts(self, stock_config, data):
        # 先执行原有的检查
        alerts, level = original_check_alerts(self, stock_config, data)
        
        # 添加操盘手习惯分析
        try:
            stock_code = stock_config['code']
            
            # 学习当前价格行为
            self.trader_analyzer.learn_from_price_action(stock_code, data)
            
            # 检测是否符合操盘手习惯
            habits = self.trader_analyzer.detect_trader_habit(stock_code, data)
            
            # 如果符合操盘手习惯，可以增强某些预警的重要性
            if habits:
                for habit in habits:
                    # 添加到预警中
                    alerts.append(('trader_habit', habit))
        except Exception as e:
            print(f"操盘手分析出错: {e}")
        
        return alerts, level
    
    monitor_class.__init__ = new_init
    monitor_class.check_alerts = new_check_alerts
    
    return monitor_class


if __name__ == '__main__':
    # 测试操盘手分析器
    analyzer = TraderAnalyzer()
    
    print("=== 操盘手分析器测试 ===")
    
    # 测试记录交易行为
    analyzer.record_trading_behavior(
        stock_code="600362",
        date="2026-03-27",
        time_period="morning",
        volume_behavior="surge",
        price_behavior="breakout",
        trend_direction="up",
        strength_score=0.8
    )
    
    # 测试更新模式频率
    analyzer.update_pattern_frequency("600362", "time", "morning_active")
    analyzer.update_pattern_frequency("600362", "volume", "high_volume_morning")
    
    # 测试生成操盘手档案
    profile = analyzer.generate_trader_profile("600362")
    print(f"操盘手档案: {profile}")
    
    # 测试支撑阻力位功能
    analyzer.record_support_resistance("600362", 55.0, "support")
    analyzer.record_support_resistance("600362", 60.0, "resistance")
    
    level_type, strength = analyzer.identify_support_resistance("600362", 55.2)
    print(f"支撑阻力位检测: {level_type}, 强度: {strength}")
