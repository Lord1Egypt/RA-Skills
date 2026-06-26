"""文件扫描器 - 扫描目录，识别文件类型"""
import os
from pathlib import Path
from typing import List, Optional

try:
    from .config import SUPPORTED_EXTENSIONS
    from .models import TicketType
except ImportError:
    from config import SUPPORTED_EXTENSIONS
    from models import TicketType


class FileInfo:
    """文件信息"""
    def __init__(self, path: str, name: str, ext: str):
        self.path = path
        self.name = name
        self.ext = ext.lower()
        self._pretype: Optional[TicketType] = None

    @property
    def pretype(self) -> TicketType:
        """预判票据类型"""
        if self._pretype is None:
            self._pretype = self._detect_type()
        return self._pretype

    def _detect_type(self) -> TicketType:
        """根据文件名/扩展名预判票据类型"""
        name_lower = self.name.lower()

        # 检查扩展名
        if self.ext not in SUPPORTED_EXTENSIONS:
            return TicketType.UNKNOWN

        # 检查关键词
        if "火车票" in self.name or "中国铁路" in self.name:
            return TicketType.TRAIN
        elif "行程单" in self.name:
            return TicketType.TRIP
        elif "发票" in self.name:
            # 可能是滴滴或酒店
            if "滴滴" in self.name or "出租" in self.name:
                return TicketType.DIDI
            elif "酒店" in self.name:
                return TicketType.HOTEL
            return TicketType.DIDI
        elif "酒店" in self.name:
            return TicketType.HOTEL
        elif "机票" in self.name or "航空" in self.name:
            return TicketType.FLIGHT

        return TicketType.UNKNOWN


class FileScanner:
    """文件扫描器"""

    def __init__(self, directory: str):
        self.directory = Path(directory)
        self.files: List[FileInfo] = []

    def scan(self) -> List[FileInfo]:
        """扫描目录，返回文件列表"""
        if not self.directory.exists():
            raise FileNotFoundError(f"目录不存在: {self.directory}")

        if not self.directory.is_dir():
            raise NotADirectoryError(f"不是目录: {self.directory}")

        self.files = []

        for item in self.directory.iterdir():
            if item.is_file():
                ext = item.suffix
                if ext.lower() in SUPPORTED_EXTENSIONS:
                    file_info = FileInfo(
                        path=str(item),
                        name=item.name,
                        ext=ext
                    )
                    self.files.append(file_info)

        return self.files

    def get_files_by_type(self, ticket_type: TicketType) -> List[FileInfo]:
        """获取指定类型的文件"""
        return [f for f in self.files if f.pretype == ticket_type]

    def get_summary(self) -> dict:
        """获取扫描摘要"""
        summary = {}
        for f in self.files:
            type_name = f.pretype.value
            summary[type_name] = summary.get(type_name, 0) + 1
        return summary
