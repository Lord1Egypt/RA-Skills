from typing import List, Dict, Any, Optional, Literal, TypedDict, Annotated
import operator
from pydantic import BaseModel, Field
import pandas as pd

# ! 结构化文件的意图识别模型定义
class StructIntent(BaseModel):
    update_query: Optional[str] = Field(
        default=None,
        description="Normalized query rewritten from user input, optimized for resource_abstract BM25 retrieval"
    )

    file_type: Optional[
        Literal["mdb", "xlsx", "xls", "gdb", "csv", "shp", "json", "basic_view", "derived"]
    ] = Field(
        default=None,
        description="File type filter, only set if explicitly mentioned by user"
    )

    file_name: Optional[str] = Field(
        default=None,
        description="Exact file name filter, only if user explicitly specifies"
    )

    kg_info: Optional[
        Dict[
            Literal["业务分类", "数据分类", "业务场景", "知识点"],
            List[str]
        ]
    ] = Field(
        default=None,
        description="Knowledge graph tags, MUST be null unless explicitly mentioned"
    )

    data_context: Optional[Dict[str, Any]] = Field(
        default=None,
        description="High-level data context, MUST be null unless explicitly mentioned"
    )

    coverage: Optional[List[str]] = Field(
        default=None,
        description="Explicit geographic coverage, MUST be null unless explicitly mentioned"
    )

    reason: Optional[str] = Field(
        default=None,
        description="Brief explanation of intent understanding (optional, can be omitted)"
    )



# ! 旧表结构化文件的意图识别模型定义
class OldStructIntent(BaseModel):
    file_type: Optional[Literal["mdb", "xlsx", "xls", "gdb", "csv", "shp", "json", "basic_view", "derive"]] = Field(
        default="", description="File type to filter"
        )
    bm25_fields: List[Literal["file_name","resource_abstract"]] = Field(
        default_factory=list, description="BM25 text search fields"
        )
    reason: Optional[str] = Field(default="", description="Routing selection reason")


# ! 非结构化文件的意图识别模型定义
class TextIntent(BaseModel):
    tables: List[Literal["main", "sub"]] = Field(
        default_factory=list, description="Tables to query: main or sub"
        )
    file_type: Optional[Literal["PDF", "TXT", "DOC", "DOCX", "PNG", "JPG"]] = Field(
        default="", description="File type to filter"
        )
    
    # 主表检索字段
    main_vector_fields: List[Literal["summary_embedding", "chunk_embedding", "question1_embedding", "question2_embedding", "question3_embedding"]] = Field(
        default_factory=list, description="Vector search fields for main table"
        )
    main_bm25_fields: List[Literal["summary", "chunk", "question1", "question2", "question3"]] = Field(
        default_factory=list, description="BM25 text search fields for main table"
        )
        
    # 子表检索字段
    sub_vector_fields: List[Literal["file_name_embedding", "resource_abstract_embedding"]] = Field(
        default_factory=list, description="Vector search fields for sub table"
        )
    sub_bm25_fields: List[Literal["file_name", "resource_abstract"]] = Field(
        default_factory=list, description="BM25 text search fields for sub table"
        )

    kg_info: Dict[Literal["业务分类", "数据分类", "业务场景", "知识点"], Any] = Field(
        default_factory=dict,
        description="Knowledge graph information"
    )
    file_name: Optional[str] = Field(default="", description="File name to filter")
    data_context: Dict[str, Any] = Field(default_factory=dict, description="Data context information")
    reason: Optional[str] = Field(default="", description="Routing selection reason")
    
# ! 旧库表 非结构化文件的意图识别模型定义
class OldTextIntent(BaseModel):
    """旧库表非结构化文件意图分类模型"""
    
    file_type: Optional[Literal["PDF", "TXT", "DOC", "DOCX", "PNG", "JPG"]] = Field(
        default="", description="File type to filter"
        )
    vector_fields: List[Literal["summary_embedding", "chunk_embedding", "question1_embedding", "question2_embedding", "question3_embedding"]] = Field(
        default_factory=list, description="Vector search fields for main table"
        )
    bm25_fields: List[Literal["summary", "chunk", "question1", "question2", "question3"]] = Field(
        default_factory=list, description="BM25 text search fields for main table"
        )
    reason: Optional[str] = Field(default="", description="Routing selection reason")
    
    
# Define Models for Field Search
class FieldScoresResult(BaseModel):
    """字段打分结果响应模型"""
    fields: List[str] = Field(default_factory=list, description="字段名称列表，按重要性排序")
    scores: List[int] = Field(default_factory=list, description="字段对应的打分列表，按顺序与 fields 对应")
    
    
# ! Text2SQL Agent 状态定义
class AgentState(TypedDict):
    """Text2SQL Agent 状态定义"""
    
    query: str 
    resource_id: Optional[int]  
    table_info: Optional[Any] 
    table_name: Optional[str]  
    table_data: Optional[Any]  
    retrieved_context: Optional[str]  
    sql_query: Optional[str]  
    execution_result: Optional[Any]  
    error_message: Optional[str]
    reflection: Optional[str]  # Reflection feedback
    attempt_count: int = 0  
    max_attempts: int = 3  
    

# ! 搜索状态定义
class SearchState(TypedDict):
    """
    搜索状态定义
    """
    query: str
    filter: List[int]
    top_k: int
    timeout: float
    search_type: Literal["structured", "unstructured", "field"]
    
    # 字段搜索专用
    resource_id: Optional[int]
    resource_name: Optional[str]
    
    # 内部状态
    intent: Any
    search_results: Annotated[List[pd.DataFrame], operator.add]
    candidate_tables: pd.DataFrame
    final_result: List[Dict[str, Any]] # 用于表格/文件搜索
    field_result: Any #  用于字段搜索 (资源ID, 资源名称, 字段列表)