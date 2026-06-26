from pathlib import Path
from typing import Dict, Type
from core.importer.base import BaseImporter
from core.importer.unified_json import UnifiedJsonImporter


class ImporterFactory:
    """
    导入器工厂，统一使用 UnifiedJsonImporter
    支持自动识别 QQ / WhatsApp 等 JSON 格式
    """
    
    _importers: Dict[str, Type[BaseImporter]] = {
        "json": UnifiedJsonImporter,
    }
    
    @classmethod
    def get_importer(cls, file_type: str) -> BaseImporter:
        """
        获取指定文件类型的导入器
        
        Args:
            file_type: 文件扩展名（不含点号）
            
        Returns:
            对应的导入器实例
            
        Raises:
            ValueError: 不支持的文件类型
        """
        if not file_type:
            file_type = "json"
        
        importer_class = cls._importers.get(file_type.lower())
        
        if importer_class is None:
            raise ValueError(f"Unsupported file type: {file_type}")
            
        return importer_class()
    
    @classmethod
    def register_importer(cls, file_type: str, importer_class: Type[BaseImporter]):
        """注册新的导入器"""
        cls._importers[file_type.lower()] = importer_class
    
    @classmethod
    def get_supported_types(cls) -> list:
        """获取所有支持的文件类型"""
        return list(cls._importers.keys())
