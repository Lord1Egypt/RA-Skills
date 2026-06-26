"""
统一的语义检索模块

整合了文件、字段、表格检索功能，并包含完整的图编排逻辑
"""
from typing import Dict, List, Any, Tuple, Union, Literal
import pandas as pd
from langgraph.graph import StateGraph, END
from utils.logger import logger
from src.semantic._types import SearchState
from src.semantic.graph.base import BaseGraph
from src.semantic.graph.structured import StructuredGraph
from src.semantic.graph.field import FieldGraph
from src.semantic.graph.unstructured import UnstructuredGraph


class SemanticSearch(BaseGraph):
    """
    统一的语义检索类，整合了文件、字段、表格检索功能

    整合了 SearchGraph 的图编排能力，提供完整的语义检索解决方案
    """

    def __init__(self):
        """初始化语义检索"""
        super().__init__()

        # 初始化子图
        self.structured_graph = StructuredGraph(self.vector_db, self.llm).graph
        self.field_graph = FieldGraph(self.vector_db, self.llm).graph
        self.unstructured_graph = UnstructuredGraph(self.vector_db, self.llm).graph

        # 编译主图
        self.app = self._create_graph()

    # ==================== 路由逻辑 ====================

    def check_root_entry_point(self, state: SearchState) -> Literal["field_search", "content_search"]:
        """确定根入口点（字段搜索或内容搜索）"""
        if state["search_type"] == "field":
            return "field_search"
        return "content_search"

    def check_content_entry_point(self, state: SearchState) -> Literal["single_id", "multi_ids", "structured_search", "unstructured_search"]:
        """根据过滤器确定内容搜索入口点"""
        _filter = state.get("filter", [])
        search_type = state.get("search_type", "structured")

        # 优先根据 search_type 判断
        if search_type == "unstructured":
            return "unstructured_search"
        elif search_type == "structured":
            # 结构化搜索根据 filter 判断
            if _filter and len(_filter) == 1:
                return "single_id"
            elif _filter and len(_filter) > 1:
                return "multi_ids"
            return "structured_search"

        # 默认行为（向后兼容）
        if _filter and len(_filter) == 1:
            return "single_id"
        elif _filter and len(_filter) > 1:
            return "multi_ids"
        return "structured_search"

    # ==================== 图构建 ====================

    def _create_content_graph(self):
        """创建内容搜索子图"""
        workflow = StateGraph(SearchState)

        # 添加节点
        workflow.add_node("fetch_single_by_id", self.fetch_single_by_id)
        workflow.add_node("fetch_multi_ids_and_rank", self.fetch_multi_ids_and_rank)
        workflow.add_node("structured_search_graph", self.structured_graph)
        workflow.add_node("unstructured_search_graph", self.unstructured_graph)
        workflow.add_node("merge_results", self.merge_results)
        workflow.add_node("rerank_results", self.rerank_results)
        workflow.add_node("fetch_details", self.fetch_details)

        # 入口点
        workflow.set_conditional_entry_point(
            self.check_content_entry_point,
            {
                "single_id": "fetch_single_by_id",
                "multi_ids": "fetch_multi_ids_and_rank",
                "structured_search": "structured_search_graph",
                "unstructured_search": "unstructured_search_graph"
            }
        )

        # 边连接
        workflow.add_edge("fetch_single_by_id", END)
        workflow.add_edge("fetch_multi_ids_and_rank", "rerank_results")
        workflow.add_edge("structured_search_graph", "merge_results")
        workflow.add_edge("unstructured_search_graph", "merge_results")
        workflow.add_edge("merge_results", "rerank_results")
        workflow.add_edge("rerank_results", "fetch_details")
        workflow.add_edge("fetch_details", END)

        return workflow.compile()

    def _create_graph(self):
        """创建主搜索图"""
        workflow = StateGraph(SearchState)

        # 添加子图节点
        workflow.add_node("field_search_graph", self.field_graph)
        workflow.add_node("content_search_graph", self._create_content_graph())

        # 入口点
        workflow.set_conditional_entry_point(
            self.check_root_entry_point,
            {
                "field_search": "field_search_graph",
                "content_search": "content_search_graph"
            }
        )

        workflow.add_edge("field_search_graph", END)
        workflow.add_edge("content_search_graph", END)

        return workflow.compile(name="semantic_search_agent")

    # ==================== 核心搜索方法 ====================

    async def search(
        self,
        query: str,
        search_type: Literal["structured", "unstructured", "field"] = "structured",
        _filter: List[int] = None,
        top_k: int = 50,
        timeout: float = 60,
        **kwargs
    ) -> Any:
        """
        核心搜索方法 - 执行搜索图

        Args:
            query: 搜索查询
            search_type: 搜索类型 ("structured", "unstructured", "field")
            _filter: 过滤的资源ID列表
            top_k: 返回结果数量
            timeout: 超时时间（秒）
            **kwargs: 字段搜索的额外参数（resource_id, resource_name）

        Returns:
            搜索结果（内容搜索为字典列表，字段搜索为元组）
        """
        if _filter is None:
            _filter = []

        state = {
            "query": query,
            "filter": _filter,
            "top_k": top_k,
            "timeout": timeout,
            "search_type": search_type,
            "resource_id": kwargs.get("resource_id"),
            "resource_name": kwargs.get("resource_name", ""),
            "search_results": [],
            "candidate_tables": pd.DataFrame(),
            "final_result": [],
            "field_result": None
        }

        try:
            result = await self.app.ainvoke(state)
            if search_type == "field":
                return result.get("field_result")
            return result.get("final_result", [])
        except Exception as e:
            logger.error(f"[SemanticSearch] Graph execution failed: {e}")
            raise e

    # ==================== 文件检索 ====================

    async def query2file(
        self,
        query: str,
        _filter: List[int] = None,
        table_name: str = None,
        top_k: int = 50,
        search_type: str = "unstructured",
        timeout: float = 60,
        enable_query_enhancement: bool = False,
        enable_rewrite: bool = True,
        enable_hyde: bool = False,
        enable_keywords: bool = False
    ) -> List[Dict[str, Any]]:
        """
        文件检索接口

        Args:
            query: 查询文本
            _filter: 资源ID过滤列表
            table_name: 表名（可选）
            top_k: 返回结果数量
            search_type: 搜索类型 (unstructured/structured)
            timeout: 超时时间（秒）
            enable_query_enhancement: 是否启用查询增强（未使用，保留兼容性）
            enable_rewrite: 是否启用查询重写
            enable_hyde: 是否启用HyDE（未使用，保留兼容性）
            enable_keywords: 是否启用关键词（未使用，保留兼容性）

        Returns:
            检索结果列表
        """
        return await self.search(
            query=query,
            search_type=search_type,
            _filter=_filter,
            top_k=top_k,
            timeout=timeout
        )

    # ==================== 字段检索 ====================

    async def query2field(
        self,
        query: str,
        resource_id: int = None,
        resource_name: str = "",
        table_structure: str = None,
        timeout: float = 180,
        top_k: int = 10
    ) -> Tuple[int, str, List]:
        """
        字段检索接口

        Args:
            query: 查询文本
            resource_id: 资源ID
            resource_name: 资源名称
            table_structure: 表结构（未使用，保留兼容性）
            timeout: 超时时间（秒）
            top_k: 返回结果数量

        Returns:
            (resource_id, resource_name, fields) 元组
        """
        result = await self.search(
            query=query,
            search_type="field",
            resource_id=resource_id,
            resource_name=resource_name,
            timeout=timeout,
            top_k=top_k
        )

        if result:
            return result

        # 失败时返回空结果
        return resource_id, resource_name, []

    # ==================== 表格检索 ====================

    async def query2table(
        self,
        query: str,
        _filter: List[int] = None,
        table_name: str = None,
        top_k: int = 50,
        timeout: float = 60,
        enable_query_enhancement: bool = False,
        enable_rewrite: bool = False,
        enable_hyde: bool = False,
        enable_keywords: bool = False
    ) -> List[Dict[str, Any]]:
        """
        表格检索接口

        Args:
            query: 查询文本
            _filter: 资源ID过滤列表
            table_name: 表名（可选）
            top_k: 返回结果数量
            timeout: 超时时间（秒）
            enable_query_enhancement: 是否启用查询增强（未使用，保留兼容性）
            enable_rewrite: 是否启用查询重写
            enable_hyde: 是否启用HyDE（未使用，保留兼容性）
            enable_keywords: 是否启用关键词（未使用，保留兼容性）

        Returns:
            检索结果列表
        """
        return await self.search(
            query=query,
            search_type="structured",
            _filter=_filter,
            top_k=top_k,
            timeout=timeout
        )


# ==================== 向后兼容的别名类 ====================

class FileSearch(SemanticSearch):
    """文件检索类（向后兼容）"""

    def __init__(self):
        super().__init__()


class FieldSearch(SemanticSearch):
    """字段检索类（向后兼容）"""

    def __init__(self):
        super().__init__()


class TableSearch(SemanticSearch):
    """表格检索类（向后兼容）"""

    def __init__(self):
        super().__init__()
