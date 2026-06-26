"""
围棋分享棋谱下载器 - 源基类定义
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List
import re
import os
from datetime import datetime

@dataclass
class FetchResult:
    """下载结果"""
    success: bool
    source: str                    # 来源标识
    url: str                       # 原始URL
    sgf_content: Optional[str]     # SGF内容
    output_path: Optional[str]     # 保存路径
    metadata: dict                 # 元数据
    error: Optional[str] = None    # 错误信息
    timing: dict = None            # 性能统计
    
    def __post_init__(self):
        if self.timing is None:
            self.timing = {}
        if self.metadata is None:
            self.metadata = {}


class BaseSourceFetcher(ABC):
    """棋谱下载源基类"""
    
    name = "base"           # 英文标识
    display_name = "基础源"  # 中文显示名
    
    # URL匹配模式（正则列表）
    url_patterns = []
    
    # 支持的URL示例
    url_examples = []
    
    @classmethod
    def can_handle(cls, url: str) -> bool:
        """判断是否支持该URL"""
        for pattern in cls.url_patterns:
            if re.search(pattern, url):
                return True
        return False
    
    @classmethod
    def extract_id(cls, url: str) -> Optional[str]:
        """从URL提取对局ID"""
        for pattern in cls.url_patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @abstractmethod
    def fetch(self, url: str, output_path: str = None) -> FetchResult:
        """下载棋谱"""
        pass
    
    def get_default_output_path(self, game_id: str) -> str:
        """获取默认输出路径"""
        tmp_dir = f"/tmp/weiqi_fetch/{datetime.now().strftime('%Y%m%d_%H%M%S')}/{self.name}"
        os.makedirs(tmp_dir, exist_ok=True)
        return f"{tmp_dir}/{self.name}_{game_id}.sgf"
    
    @staticmethod
    def coord_to_sgf(x: int, y: int, board_size: int = 19) -> str:
        """坐标转SGF格式"""
        # OGS/野狐: (0,0)=左上, x向右, y向下
        # SGF: a,b,c... 从左下角开始
        sgf_x = chr(ord('a') + x)
        sgf_y = chr(ord('a') + (board_size - 1 - y))
        return sgf_x + sgf_y
    
    @staticmethod
    def format_ogs_rank(rating: float) -> str:
        """OGS rating转段位"""
        if not rating:
            return ""
        rank = int(rating)
        if rank >= 30:
            return f"{rank - 29}d"
        else:
            return f"{30 - rank}k"
    
    @staticmethod
    def get_handicap_stones(handicap: int, board_size: int = 19) -> List[tuple]:
        """获取标准让子坐标 (0-based)"""
        if board_size != 19:
            t = 2 if board_size < 13 else 3
            stars = [
                (t, t), (board_size - t - 1, t),
                (t, board_size - t - 1), (board_size - t - 1, board_size - t - 1),
                (board_size // 2, t), (t, board_size // 2),
                (board_size // 2, board_size - t - 1), (board_size - t - 1, board_size // 2),
                (board_size // 2, board_size // 2)
            ]
            return stars[:handicap]
        
        # 19路标准星位 (0-based)
        stars = [
            (15, 3), (3, 15),   # 右上, 左下
            (15, 15), (3, 3),   # 右下, 左上
            (3, 9), (15, 9),    # 左边, 右边
            (9, 3), (9, 15),    # 上边, 下边
            (9, 9)              # 天元
        ]
        return stars[:handicap]


# 源注册表
_fetchers = {}

def register_fetcher(fetcher_class):
    """注册下载器"""
    _fetchers[fetcher_class.name] = fetcher_class
    return fetcher_class

def get_fetcher_for_url(url: str) -> Optional[BaseSourceFetcher]:
    """根据URL获取对应的下载器"""
    for name, fetcher_class in _fetchers.items():
        if fetcher_class.can_handle(url):
            return fetcher_class()
    return None

def get_fetcher_by_name(name: str) -> Optional[BaseSourceFetcher]:
    """根据名称获取下载器"""
    fetcher_class = _fetchers.get(name)
    if fetcher_class:
        return fetcher_class()
    return None

def list_fetchers():
    """列出所有可用的下载器"""
    return [(name, cls.display_name, cls.url_examples) for name, cls in _fetchers.items()]
