#!/usr/bin/env python3
"""
Count-Min Sketch 实现
用于估算元素频率的概略数据结构
"""

import hashlib
import pickle
import struct
from pathlib import Path
from typing import List, Union


class CountMinSketch:
    """Count-Min Sketch 实现
    
    使用多个哈希函数来估算元素出现的频率。
    对于每个元素，取所有哈希位置上的最小值作为估计值。
    """
    
    def __init__(self, width: int = 200000, depth: int = 5):
        """
        Args:
            width: 哈希表的宽度（列数），决定空间大小
            depth: 哈希函数的数量（行数），决定准确性
        """
        self.width = width
        self.depth = depth
        # 使用一维列表存储计数器，size = width * depth
        self.table = [0] * (width * depth)
        self._size = 0  # 记录插入的元素数量
    
    def _hash(self, item: str, seed: int) -> int:
        """生成哈希值
        
        使用 MD5 + seed 来生成不同的哈希函数
        """
        # 将 seed 和 item 组合后哈希
        data = f"{seed}:{item}".encode('utf-8')
        hash_val = hashlib.md5(data).digest()
        # 取前4字节作为整数
        return struct.unpack('I', hash_val[:4])[0] % self.width
    
    def update(self, item: str, count: int = 1):
        """更新元素的计数
        
        Args:
            item: 要计数的元素（字符串）
            count: 增加的数量，默认为1
        """
        for i in range(self.depth):
            idx = i * self.width + self._hash(item, i)
            self.table[idx] += count
        self._size += count
    
    def estimate(self, item: str) -> int:
        """估算元素的出现次数
        
        Args:
            item: 要查询的元素
            
        Returns:
            估算的计数（可能偏高，但不会偏低）
        """
        min_count = float('inf')
        for i in range(self.depth):
            idx = i * self.width + self._hash(item, i)
            min_count = min(min_count, self.table[idx])
        return int(min_count)
    
    def __len__(self):
        """返回插入的元素总数"""
        return self._size
    
    def __repr__(self):
        return f"CountMinSketch(width={self.width}, depth={self.depth}, size={self._size})"
    
    def save_to_file(self, path: Union[str, Path]):
        """将CMS保存到文件
        
        使用pickle序列化整个对象，包括width、depth、table和size
        
        Args:
            path: 保存路径
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'wb') as f:
            pickle.dump({
                'width': self.width,
                'depth': self.depth,
                'table': self.table,
                'size': self._size
            }, f)
    
    @classmethod
    def load_from_file(cls, path: Union[str, Path]) -> 'CountMinSketch':
        """从文件加载CMS
        
        Args:
            path: 文件路径
            
        Returns:
            加载后的CountMinSketch实例
        """
        path = Path(path)
        
        with open(path, 'rb') as f:
            data = pickle.load(f)
        
        cms = cls.__new__(cls)
        cms.width = data['width']
        cms.depth = data['depth']
        cms.table = data['table']
        cms._size = data['size']
        
        return cms
