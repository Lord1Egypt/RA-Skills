"""
提取器基类 - 定义统一的提取接口
所有提取器继承此基类，实现 extract() 方法
"""

import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path


class BaseExtractor(ABC):
    """提取器抽象基类"""

    @abstractmethod
    def extract(self, file_path: str) -> List[Dict[str, Any]]:
        """
        从文件中提取知识实体。

        Args:
            file_path: 源文件路径

        Returns:
            提取结果列表，每项包含：
            {
                "entity_type": str,
                "entity": Dict[str, Any],
                "provenance": {
                    "source_type": str,
                    "source_path": str,
                    "extracted_at": str (ISO 8601),
                    "confidence": float
                },
                "tags": List[str]
            }
        """
        pass

    def _make_provenance(self, file_path: str, confidence: float = 0.8,
                         source_type: str = "unknown") -> Dict[str, Any]:
        """构造标准 provenance 字段"""
        return {
            "source_type": source_type,
            "source_path": str(file_path),
            "extracted_at": datetime.now().isoformat(),
            "confidence": confidence
        }

    def _file_exists(self, file_path: str) -> bool:
        """检查文件是否存在"""
        return os.path.isfile(file_path)

    def _read_text(self, file_path: str, encoding: str = "utf-8") -> str:
        """读取文本文件"""
        with open(file_path, "r", encoding=encoding, errors="replace") as f:
            return f.read()


if __name__ == "__main__":
    # 测试基类不可直接实例化
    try:
        b = BaseExtractor()
        print("ERROR: should not instantiate abstract class")
    except TypeError as e:
        print(f"OK: BaseExtractor is abstract: {e}")
