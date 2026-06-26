"""
Semantic Search Skill 主入口

提供 OpenClaw Skill 接口，调用项目中的核心检索逻辑
自动使用项目现有配置
"""

from typing import Dict, Any, List, Optional, Union, Literal
from pydantic import BaseModel, Field
import asyncio
import sys
from pathlib import Path

# 尝试导入项目配置
try:
    # 如果在项目中使用，导入项目配置
    current_dir = Path(__file__).parent
    project_root = current_dir.parent.parent / "semantic_search"
    if project_root.exists():
        sys.path.insert(0, str(project_root))
    from utils.config import CONFIG as PROJECT_CONFIG
except (ImportError, ModuleNotFoundError):
    # 如果不在项目环境中，使用环境变量或默认配置
    import os
    PROJECT_CONFIG = {
        "flight_db": {
            "host": os.getenv("FLIGHT_DB_HOST", "localhost"),
            "port": int(os.getenv("FLIGHT_DB_PORT", "31337")),
            "user": os.getenv("FLIGHT_DB_USER", "admin"),
            "password": os.getenv("FLIGHT_DB_PASSWORD", ""),
            "insecure": os.getenv("FLIGHT_DB_INSECURE", "true").lower() == "true"
        },
        "llm": {
            "provider": os.getenv("LLM_PROVIDER", "qwen"),
            "model": os.getenv("LLM_MODEL", "qwen-max"),
            "api_key": os.getenv("LLM_API_KEY", ""),
            "base_url": os.getenv("LLM_BASE_URL", "")
        },
        "embedding": {
            "model": os.getenv("EMBEDDING_MODEL", "BGE-M3"),
            "dimension": int(os.getenv("EMBEDDING_DIMENSION", "1024")),
            "api_key": os.getenv("EMBEDDING_API_KEY", ""),
            "base_url": os.getenv("EMBEDDING_BASE_URL", "")
        }
    }

from . import SemanticSearch, DataGen


# ==================== 请求/响应模型 ====================

class TableSearchRequest(BaseModel):
    query: str
    resource_ids: Optional[List[int]] = []
    limit: int = Field(default=10, description="返回表的数量限制", ge=1)
    enable_query_enhancement: bool = Field(default=True)
    enable_rewrite: bool = Field(default=False)
    enable_hyde: bool = Field(default=False)
    enable_keywords: bool = Field(default=True)


class FieldSearchRequest(BaseModel):
    query: str
    resource_id: Union[int, List[int]]
    limit: int = Field(default=1, description="返回字段的数量限制", ge=1)


class DataGenRequest(BaseModel):
    query: str
    resource_id: Union[int, List[int]]
    return_all: bool = Field(default=False)
    max_attempts: int = Field(default=2)
    confidence_threshold: float = Field(default=0.8)


class FileSearchRequest(BaseModel):
    query: str
    search_type: Literal["text", "table"]
    limit: int = Field(default=10, ge=1, le=10000)


# ==================== Skill 主类 ====================

class SemanticSearchSkill:
    """
    Semantic Search OpenClaw Skill
    
    提供统一的语义检索接口，支持：
    - 表格检索 (table_search)
    - 字段检索 (field_search)
    - Text-to-SQL 数据生成 (data_gen)
    - 文件检索 (file_search)
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        初始化技能
        
        Args:
            config: 配置字典，包含数据库连接等信息
                   如果为 None，自动使用项目现有配置
        """
        # 优先使用传入的配置，否则使用项目配置
        self.config = config or PROJECT_CONFIG
        self._search_instance = None
        self._data_gen_instance = None
    
    @property
    def search(self) -> SemanticSearch:
        """懒加载 SemanticSearch 实例"""
        if self._search_instance is None:
            self._search_instance = SemanticSearch()
        return self._search_instance
    
    @property
    def data_gen(self) -> DataGen:
        """懒加载 DataGen 实例"""
        if self._data_gen_instance is None:
            self._data_gen_instance = DataGen()
        return self._data_gen_instance
    
    async def invoke(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用技能方法
        
        Args:
            action: 操作类型 (table_search, field_search, data_gen, file_search)
            params: 操作参数
        
        Returns:
            操作结果
        """
        
        if action == "table_search":
            return await self.table_search(TableSearchRequest(**params))
        
        elif action == "field_search":
            return await self.field_search(FieldSearchRequest(**params))
        
        elif action == "data_gen":
            return await self.data_generate(DataGenRequest(**params))
        
        elif action == "file_search":
            return await self.file_search(FileSearchRequest(**params))
        
        else:
            raise ValueError(f"Unknown action: {action}")
    
    async def table_search(self, request: TableSearchRequest) -> Dict[str, Any]:
        """
        表格语义检索
        
        Args:
            request: 请求参数
        
        Returns:
            匹配的表列表
        """
        try:
            result = await self.search.query2table(
                query=request.query,
                _filter=request.resource_ids,
                limit=request.limit,
                enable_query_enhancement=request.enable_query_enhancement,
                enable_rewrite=request.enable_rewrite,
                enable_hyde=request.enable_hyde,
                enable_keywords=request.enable_keywords
            )
            
            return {
                "code": 200,
                "msg": "success",
                "data": result
            }
        
        except Exception as e:
            return {
                "code": 500,
                "msg": f"表格检索失败：{str(e)}",
                "data": []
            }
    
    async def field_search(self, request: FieldSearchRequest) -> Dict[str, Any]:
        """
        字段语义检索
        
        Args:
            request: 请求参数
        
        Returns:
            字段名列表
        """
        try:
            resource_id = request.resource_id
            if isinstance(resource_id, list):
                resource_id = resource_id[0]
            
            _, _, fields = await self.search.query2field(
                query=request.query,
                resource_id=resource_id,
                limit=request.limit
            )
            
            result = fields[:request.limit] if len(fields) > request.limit else fields
            
            return {
                "code": 200,
                "msg": "success",
                "data": result
            }
        
        except Exception as e:
            return {
                "code": 500,
                "msg": f"字段检索失败：{str(e)}",
                "data": []
            }
    
    async def data_generate(self, request: DataGenRequest) -> Dict[str, Any]:
        """
        Text-to-SQL 数据生成
        
        Args:
            request: 请求参数
        
        Returns:
            数据结果和生成的 SQL
        """
        try:
            resource_id = request.resource_id
            if isinstance(resource_id, list):
                resource_id = resource_id[0]
            
            result, sql = await self.data_gen.query2sql(
                query=request.query,
                resource_id=resource_id,
                max_attempts=request.max_attempts,
                confidence_threshold=request.confidence_threshold
            )
            
            return {
                "code": 200,
                "msg": "success",
                "data": {
                    "result": result,
                    "sql": sql
                }
            }
        
        except Exception as e:
            return {
                "code": 500,
                "msg": f"数据生成失败：{str(e)}",
                "data": {
                    "result": None,
                    "sql": ""
                }
            }
    
    async def file_search(self, request: FileSearchRequest) -> Dict[str, Any]:
        """
        文件语义检索
        
        Args:
            request: 请求参数
        
        Returns:
            文件列表
        """
        try:
            files = await self.search.query2file(
                query=request.query,
                top_k=request.limit,
                search_type=request.search_type
            )
            
            if isinstance(files, str):
                return {
                    "code": 500,
                    "msg": f"文件搜索失败：{files}",
                    "data": []
                }
            
            limited_files = files[:request.limit] if isinstance(files, list) else []
            
            return {
                "code": 200,
                "msg": "success",
                "data": limited_files
            }
        
        except Exception as e:
            return {
                "code": 500,
                "msg": f"文件搜索失败：{str(e)}",
                "data": []
            }


# ==================== 导出 ====================

__all__ = ['SemanticSearchSkill']
