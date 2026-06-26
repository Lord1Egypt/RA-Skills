# -*- coding: utf-8 -*-
"""
Market Data Skill 集成模块
使用已有的 market-data skill 获取行情数据
"""

import json
import logging
import subprocess
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)


class MarketDataFetcher:
    """
    集成 market-data skill 的数据获取器
    """
    
    def __init__(self, skill_path: Optional[str] = None):
        if skill_path is None:
            # 默认相对路径
            skill_path = Path(__file__).parent.parent.parent / "market-data"
        else:
            skill_path = Path(skill_path)
        
        self.skill_path = skill_path
        self.script_path = skill_path / "scripts" / "quote_cn_pro.py"
        
    def is_available(self) -> bool:
        """检查 market-data skill 是否可用"""
        return self.script_path.exists()
    
    def get_kline_data(self, code: str, count: int = 60, period: str = "day") -> Optional[pd.DataFrame]:
        """
        获取 K 线数据
        
        Args:
            code: 股票代码
            count: 数据条数
            period: 周期 (day/week/month/5min)
            
        Returns:
            DataFrame 包含 OHLCV 数据
        """
        if not self.is_available():
            logger.warning(f"market-data skill 不可用: {self.script_path}")
            return None
        
        try:
            cmd = [
                "python3", str(self.script_path),
                code,
                "--kline",
                "--count", str(count),
                "--period", period
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.skill_path)
            )
            
            if result.returncode != 0:
                logger.warning(f"获取 K 线数据失败: {result.stderr}")
                return None
            
            # 解析输出
            return self._parse_kline_output(result.stdout)
            
        except Exception as e:
            logger.error(f"调用 market-data skill 失败: {e}")
            return None
    
    def _parse_kline_output(self, output: str) -> Optional[pd.DataFrame]:
        """解析 K 线输出"""
        lines = output.strip().split('\n')
        data = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('📈') or line.startswith('📡') or line.startswith('='):
                continue
            
            # 尝试解析 K 线数据行
            # 格式: 日期 开盘 收盘 最高 最低 成交量 成交额 ...
            parts = line.split()
            if len(parts) >= 6:
                try:
                    data.append({
                        'date': parts[0],
                        'open': float(parts[1]),
                        'close': float(parts[2]),
                        'high': float(parts[3]),
                        'low': float(parts[4]),
                        'volume': float(parts[5]),
                    })
                except (ValueError, IndexError):
                    continue
        
        if data:
            df = pd.DataFrame(data)
            df['date'] = pd.to_datetime(df['date'])
            return df
        
        return None
    
    def get_daily_summary(self, code: str) -> Optional[Dict[str, Any]]:
        """
        获取日线总结
        
        Returns:
            包含价格、均线等数据的字典
        """
        if not self.is_available():
            return None
        
        try:
            cmd = [
                "python3", str(self.script_path),
                code,
                "--daily"
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=str(self.skill_path)
            )
            
            if result.returncode != 0:
                return None
            
            return self._parse_daily_output(result.stdout)
            
        except Exception as e:
            logger.error(f"获取日线数据失败: {e}")
            return None
    
    def _parse_daily_output(self, output: str) -> Dict[str, Any]:
        """解析日线输出"""
        result = {}
        lines = output.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # 提取当前价格
            if '当前价格:' in line:
                try:
                    result['price'] = float(line.split(':')[1].split()[0])
                except:
                    pass
            
            # 提取涨跌幅
            elif '涨跌:' in line:
                try:
                    parts = line.split(':')[1].strip()
                    if '+' in parts:
                        result['change_pct'] = float(parts.split('%')[0].replace('+', ''))
                    elif '-' in parts:
                        result['change_pct'] = -float(parts.split('%')[0].replace('-', ''))
                except:
                    pass
            
            # 提取均线
            elif 'MA5:' in line:
                try:
                    result['ma5'] = float(line.split(':')[1].strip())
                except:
                    pass
            elif 'MA10:' in line:
                try:
                    result['ma10'] = float(line.split(':')[1].strip())
                except:
                    pass
            elif 'MA20:' in line:
                try:
                    result['ma20'] = float(line.split(':')[1].strip())
                except:
                    pass
        
        return result


def create_data_fetcher(config: Optional[Dict] = None) -> Any:
    """
    工厂函数：创建合适的数据获取器
    
    优先使用 market-data skill，如果不可用则回退到 akshare
    """
    if config is None:
        config = {}
    
    use_market_data = config.get('data', {}).get('use_market_data_skill', True)
    
    if use_market_data:
        skill_path = config.get('data', {}).get('market_data_skill_path', '../market-data')
        fetcher = MarketDataFetcher(skill_path)
        
        if fetcher.is_available():
            logger.info("使用 market-data skill 获取数据")
            return fetcher
        else:
            logger.warning(f"market-data skill 不可用，回退到 akshare")
    
    # 回退到 akshare
    from scripts.data_fetcher import get_daily_data, get_realtime_quote
    return None  # 使用 None 表示使用默认的 akshare 方式
