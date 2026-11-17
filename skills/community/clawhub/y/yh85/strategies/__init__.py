"""
策略基类
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional, Dict, List
import pandas as pd


@dataclass
class Signal:
    """交易信号"""
    timestamp: pd.Timestamp
    side: str           # "long" / "short"
    entry_price: float
    stop_loss: float
    take_profit: float
    strategy: str
    leverage: int = 10
    size_ratio: float = 1.0  # 仓位比例
    meta: Dict = field(default_factory=dict)

    def __repr__(self):
        return f"[{self.strategy}] {self.side.upper()} @ {self.entry_price:.4f} SL:{self.stop_loss:.4f} TP:{self.take_profit:.4f}"


class BaseStrategy(ABC):
    """所有策略的基类"""

    def __init__(self, name: str, leverage: int = 10):
        self.name = name
        self.leverage = leverage
        self.signals: List[Signal] = []

    @abstractmethod
    def prepare(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        预处理数据：计算所需指标，返回增强后的 DataFrame
        """
        pass

    @abstractmethod
    def generate_signals(self, df: pd.DataFrame) -> List[Signal]:
        """
        生成交易信号列表
        """
        pass

    def run(self, df: pd.DataFrame) -> list:
        """完整运行：准备数据 → 生成信号"""
        df = self.prepare(df)
        return self.generate_signals(df)
