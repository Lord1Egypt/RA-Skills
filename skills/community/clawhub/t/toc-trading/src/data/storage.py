"""
TOC Trading System - 存储抽象层
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

class Storage:
    """JSON 文件存储"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_path(self, filename: str) -> Path:
        return self.data_dir / filename
    
    def load(self, filename: str, default: Any = None) -> Any:
        """加载 JSON 文件"""
        path = self._get_path(filename)
        if not path.exists():
            return default
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return default
    
    def save(self, filename: str, data: Any) -> bool:
        """保存 JSON 文件"""
        path = self._get_path(filename)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except IOError as e:
            print(f"保存失败 {filename}: {e}")
            return False
    
    def get_stocks(self) -> List[Dict]:
        """获取股票池"""
        data = self.load('stock_pool.json', {"stocks": []})
        return data.get('stocks', [])
    
    def save_stocks(self, stocks: List[Dict]) -> bool:
        """保存股票池"""
        data = {
            "version": "1.0",
            "last_update": datetime.now().isoformat(),
            "stocks": stocks
        }
        return self.save('stock_pool.json', data)
    
    def get_positions(self) -> List[Dict]:
        """获取持仓"""
        data = self.load('positions.json', {"positions": []})
        return data.get('positions', [])
    
    def save_positions(self, positions: List[Dict]) -> bool:
        """保存持仓"""
        data = {
            "version": "1.0",
            "last_update": datetime.now().isoformat(),
            "positions": positions
        }
        return self.save('positions.json', data)
    
    def get_trades(self) -> List[Dict]:
        """获取交易记录"""
        data = self.load('trades.json', {"trades": []})
        return data.get('trades', [])
    
    def save_trades(self, trades: List[Dict]) -> bool:
        """保存交易记录"""
        data = {
            "version": "1.0",
            "trades": trades
        }
        return self.save('trades.json', data)
    
    def add_trade(self, trade: Dict) -> bool:
        """添加交易记录"""
        trades = self.get_trades()
        trades.append(trade)
        return self.save_trades(trades)
    
    def get_recommendations(self) -> Dict:
        """获取推荐记录"""
        return self.load('recommendations.json', {
            "daily_stocks": [],
            "historical_recommendations": []
        })
    
    def save_recommendations(self, data: Dict) -> bool:
        """保存推荐记录"""
        return self.save('recommendations.json', data)
    
    def get_config(self) -> Dict:
        """获取配置"""
        return self.load('config.json', {
            "notification": {
                "enabled": True,
                "morning_time": "09:30",
                "noon_time": "13:00",
                "evening_time": "15:30"
            },
            "recommendation": {
                "daily_stock_enabled": True,
                "daily_stock_time": "09:00",
                "signal_filters": {
                    "min_change_pct": 3,
                    "min_volume_ratio": 1.5,
                    "min_moneyflow": 100000000
                }
            }
        })
    
    def save_config(self, config: Dict) -> bool:
        """保存配置"""
        return self.save('config.json', config)
    
    # ==================== 挑战相关 ====================
    
    def load_challenge(self) -> Dict:
        """加载挑战数据"""
        return self.load('challenge.json', {
            'version': '1.0',
            'active': False,
            'period': '',
            'initial_capital': 50000,
            'current_capital': 50000,
            'trades_count': 0,
            'win_count': 0,
            'loss_count': 0,
            'win_rate': 0,
            'daily_trades': [],
            'equity_curve': []
        })
    
    def save_challenge(self, data: Dict) -> bool:
        """保存挑战数据"""
        return self.save('challenge.json', data)