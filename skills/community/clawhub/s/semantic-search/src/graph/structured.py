from typing import List, Dict, Optional
import pandas as pd
import asyncio
from langgraph.graph import StateGraph, END
from src.semantic._types import SearchState
from src.semantic.graph.base import BaseGraph, STRUCT_TABLE_NAME
from src.semantic.intent import global_intent
from utils.logger import logger


class StructuredGraph(BaseGraph):
    """
    结构化搜索子图。
    """
    BASE_FILE_TYPES = ["XLS", "XLSX", "CSV", "SHP", "MDB", "GDB", "JSON", "basic_view", "derived"]
    BASE_FILTER = "is_process is False"


    def __init__(self, vector_db, llm):
        super().__init__(vector_db, llm)
        self.graph = self._create_graph()


    async def analyze_intent(self, state: SearchState):
        """
        根据查询分析结构化搜索意图。
        """
        query = state["query"]
        logger.info(f"[StructuredGraph] Analyze Intent: {query}")
        intent = await global_intent.structured_intent(query)
        logger.info(f"Intent: {intent}")
        return {"intent": intent}


    def _get_file_types(self, state: SearchState) -> List[str]:
        """获取文件类型列表"""
        if state["intent"] and state["intent"].file_type:
            return [state["intent"].file_type.upper()]
        return self.BASE_FILE_TYPES


    def _safe_sql_string(self, value: str) -> str:
        """转义SQL字符串"""
        return str(value).replace("'", "''")


    async def _build_coverage_filters(self, intent) -> Optional[str]:
        """构建coverage过滤条件"""
        coverage = intent.coverage or []
        if not coverage:
            return None

        coverage_filters = [self.BASE_FILTER]
        for term in coverage:
            safe_term = self._safe_sql_string(term)
            coverage_filters.append(f"json_as_text(base_info, 'coverage') LIKE '%{safe_term}%'")

        return " AND ".join(coverage_filters)


    async def _build_kg_info_filters(self, intent) -> Optional[str]:
        """构建kg_info过滤条件"""
        if not intent or not intent.kg_info:
            return self.BASE_FILTER

        kg_filters = [self.BASE_FILTER]
        kg_conditions = []

        for key, value in intent.kg_info.items():
            if not value:
                continue

            values = value if isinstance(value, list) else [value]
            like_parts = []

            for v in values:
                if not v:
                    continue
                safe_v = self._safe_sql_string(v)
                safe_key = self._safe_sql_string(key)
                like_parts.append(f"json_as_text(kg_info, '{safe_key}') LIKE '%{safe_v}%'")

            if like_parts:
                safe_key = self._safe_sql_string(key)
                kg_conditions.append(
                    f"(json_contains(kg_info, '{safe_key}') AND ({' OR '.join(like_parts)}))"
                )

        if kg_conditions:
            kg_filters.extend(kg_conditions)

        return " AND ".join(kg_filters)


    async def _execute_bm25_search(
        self,
        query: str,
        text_fields: List[str],
        top_k: int,
        table_name: str,
        file_types: List[str],
        _filter: Optional[str] = None,
        return_field: Optional[str] = None
    ) -> pd.DataFrame:
        """执行BM25搜索的公共方法"""
        return await self.vector_db.bm25_search_multi_fields(
            query=query,
            text_fields=text_fields,
            top_k=top_k,
            _filter=_filter or self.BASE_FILTER,
            table_name=table_name,
            file_type=file_types,
            return_field=return_field,
        )


    async def _search_with_source(
        self,
        result: pd.DataFrame,
        source_name: str
    ) -> Dict[str, List[pd.DataFrame]]:
        """处理搜索结果并添加source标记"""
        if isinstance(result, pd.DataFrame) and not result.empty:
            result = result.copy()
            result["source"] = source_name
            return {"search_results": [result]}
        return {"search_results": []}


    async def search_by_coverage(self, state: SearchState):
        """Coverage search node"""
        try:
            file_types = self._get_file_types(state)
            _filter = await self._build_coverage_filters(state["intent"])

            result = await self._execute_bm25_search(
                query=state["query"],
                text_fields=["resource_abstract"],
                top_k=state.get("top_k", 50),
                table_name=STRUCT_TABLE_NAME,
                file_types=file_types,
                _filter=_filter,
                return_field="base_info"
            )

            return await self._search_with_source(result, "coverage")
        except Exception as e:
            logger.error(f"[StructuredGraph] Coverage search failed: {e}")
            return {"search_results": []}


    async def search_by_kg_info(self, state: SearchState):
        """KG Info search node"""
        try:
            file_types = self._get_file_types(state)
            _filter = await self._build_kg_info_filters(state["intent"])

            result = await self._execute_bm25_search(
                query=state["query"],
                text_fields=["resource_abstract"],
                top_k=state.get("top_k", 50),
                table_name=STRUCT_TABLE_NAME,
                file_types=file_types,
                _filter=_filter,
                return_field="kg_info"
            )

            return await self._search_with_source(result, "kg_info")
        except Exception as e:
            logger.error(f"[StructuredGraph] KG info search failed: {e}")
            return {"search_results": []}


    async def search_by_file_name(self, state: SearchState):
        """File name search node"""
        try:
            intent = state["intent"]
            if not intent or not intent.file_name:
                return {"search_results": []}

            file_types = self._get_file_types(state)

            result = await self._execute_bm25_search(
                query=intent.file_name,
                text_fields=["file_name"],
                top_k=state.get("top_k", 50),
                table_name=STRUCT_TABLE_NAME,
                file_types=file_types,
                return_field="file_name"
            )

            return await self._search_with_source(result, "file_name")
        except Exception as e:
            logger.error(f"[StructuredGraph] File name search failed: {e}")
            return {"search_results": []}


    async def search_abstract(self, state: SearchState):
        """Abstract search node"""
        try:
            file_types = self._get_file_types(state)

            result = await self._execute_bm25_search(
                query=state["query"],
                text_fields=["resource_abstract"],
                top_k=state.get("top_k", 50),
                table_name=STRUCT_TABLE_NAME,
                file_types=file_types
            )

            return await self._search_with_source(result, "resource_abstract")
        except Exception as e:
            logger.error(f"[StructuredGraph] Abstract search failed: {e}")
            return {"search_results": []}


    async def _parallel_search_all(self, state: SearchState):
        """并行执行所有相关的搜索任务"""
        intent = state["intent"]
        search_tasks = []
        task_names = []

        # 根据意图决定执行哪些搜索任务
        if intent.coverage:
            search_tasks.append(self.search_by_coverage(state))
            task_names.append("coverage")

        if intent.kg_info:
            search_tasks.append(self.search_by_kg_info(state))
            task_names.append("kg_info")

        if intent.file_name:
            search_tasks.append(self.search_by_file_name(state))
            task_names.append("file_name")

        # 总是执行 abstract 搜索
        search_tasks.append(self.search_abstract(state))
        task_names.append("abstract")

        # 并行执行所有搜索任务
        results = await asyncio.gather(*search_tasks, return_exceptions=True)

        # 合并所有搜索结果
        all_results = []
        for result in results:
            if isinstance(result, dict) and result.get("search_results"):
                all_results.extend(result["search_results"])
            elif isinstance(result, Exception):
                logger.error(f"[StructuredGraph] Search task failed: {result}")

        return {"search_results": all_results}


    def _create_graph(self):
        """
        创建结构化搜索子图。
        """
        workflow = StateGraph(SearchState)
        workflow.add_node("analyze_intent", self.analyze_intent)
        workflow.add_node("parallel_search", self._parallel_search_all)

        # 将 analyze_intent 设置为入口点
        workflow.set_entry_point("analyze_intent")

        # analyze_intent -> parallel_search -> END
        workflow.add_edge("analyze_intent", "parallel_search")
        workflow.add_edge("parallel_search", END)

        return workflow.compile()