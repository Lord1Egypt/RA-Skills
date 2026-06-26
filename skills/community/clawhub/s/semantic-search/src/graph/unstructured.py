from typing import List, Dict, Optional
import pandas as pd
import asyncio
from langgraph.graph import StateGraph, END
from src.semantic._types import SearchState
from src.semantic.graph.base import BaseGraph, TEXT_TABLE_NAME, SUB_TEXT_TABLE_NAME
from src.semantic.intent import global_intent
from utils.logger import logger


class UnstructuredGraph(BaseGraph):
    """
    非结构化搜索子图。
    """
    BASE_FILE_TYPES = ["PDF", "TXT", "DOC", "DOCX", "PNG", "JPG"]
    BASE_FILTER = None  # 非结构化表没有 is_process 字段

    def __init__(self, vector_db, llm):
        super().__init__(vector_db, llm)
        self.graph = self._create_graph()

    async def analyze_intent(self, state: SearchState):
        """
        根据查询分析非结构化搜索意图。
        """
        query = state["query"]
        logger.info(f"[UnstructuredGraph] Analyze Intent: {query}")
        intent = await global_intent.file_intent(query)
        return {"intent": intent}

    def _get_file_types(self, state: SearchState) -> List[str]:
        """获取文件类型列表"""
        intent = state["intent"]
        if intent and intent.file_type:
            return [intent.file_type]
        return self.BASE_FILE_TYPES

    async def _build_main_table_filters(self, intent) -> Optional[str]:
        """构建主表过滤条件"""
        if not intent or not intent.kg_info:
            return self.BASE_FILTER

        kg_conditions = []

        for key, value in intent.kg_info.items():
            if not value:
                continue

            values = value if isinstance(value, list) else [value]
            like_parts = []

            for v in values:
                if not v:
                    continue
                safe_v = str(v).replace("'", "''")
                safe_key = str(key).replace("'", "''")
                like_parts.append(f"json_as_text(kg_info, '{safe_key}') LIKE '%{safe_v}%'")

            if like_parts:
                safe_key = str(key).replace("'", "''")
                kg_conditions.append(
                    f"(json_contains(kg_info, '{safe_key}') AND ({' OR '.join(like_parts)}))"
                )

        # 如果只有 kg_conditions，直接返回
        if kg_conditions:
            return " AND ".join(kg_conditions)

        # 否则返回 BASE_FILTER（可能是 None）
        return self.BASE_FILTER

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

    async def search_main_table_summary(self, state: SearchState):
        """主表 summary 搜索"""
        try:
            intent = state["intent"]
            if not intent or "summary" not in intent.main_bm25_fields:
                return {"search_results": []}

            file_types = self._get_file_types(state)
            _filter = await self._build_main_table_filters(intent)

            result = await self._execute_bm25_search(
                query=state["query"],
                text_fields=["summary"],
                top_k=state.get("top_k", 50),
                table_name=TEXT_TABLE_NAME,
                file_types=file_types,
                _filter=_filter,
                return_field="summary"
            )

            return await self._search_with_source(result, "main_summary")
        except Exception as e:
            logger.error(f"[UnstructuredGraph] Main table summary search failed: {e}")
            return {"search_results": []}

    async def search_main_table_chunk(self, state: SearchState):
        """主表 chunk 搜索"""
        try:
            intent = state["intent"]
            if not intent or "chunk" not in intent.main_bm25_fields:
                return {"search_results": []}

            file_types = self._get_file_types(state)
            _filter = await self._build_main_table_filters(intent)

            result = await self._execute_bm25_search(
                query=state["query"],
                text_fields=["chunk"],
                top_k=state.get("top_k", 50),
                table_name=TEXT_TABLE_NAME,
                file_types=file_types,
                _filter=_filter,
                return_field="chunk"
            )

            return await self._search_with_source(result, "main_chunk")
        except Exception as e:
            logger.error(f"[UnstructuredGraph] Main table chunk search failed: {e}")
            return {"search_results": []}

    async def search_main_table_questions(self, state: SearchState):
        """主表 questions 搜索"""
        try:
            intent = state["intent"]
            question_fields = ["question1", "question2", "question3"]
            available_fields = [f for f in question_fields if f in intent.main_bm25_fields]

            if not available_fields:
                return {"search_results": []}

            file_types = self._get_file_types(state)
            _filter = await self._build_main_table_filters(intent)

            result = await self._execute_bm25_search(
                query=state["query"],
                text_fields=available_fields,
                top_k=state.get("top_k", 50),
                table_name=TEXT_TABLE_NAME,
                file_types=file_types,
                _filter=_filter,
                return_field=None
            )

            return await self._search_with_source(result, "main_questions")
        except Exception as e:
            logger.error(f"[UnstructuredGraph] Main table questions search failed: {e}")
            return {"search_results": []}

    async def search_sub_table(self, state: SearchState):
        """子表搜索"""
        try:
            intent = state["intent"]
            if not intent or "sub" not in intent.tables:
                return {"search_results": []}

            file_types = self._get_file_types(state)

            # 收集所有子表的搜索字段
            text_fields = []
            if "file_name" in intent.sub_bm25_fields:
                text_fields.append("file_name")
            if "resource_abstract" in intent.sub_bm25_fields:
                text_fields.append("resource_abstract")

            if not text_fields:
                return {"search_results": []}

            result = await self._execute_bm25_search(
                query=state["query"],
                text_fields=text_fields,
                top_k=state.get("top_k", 50),
                table_name=SUB_TEXT_TABLE_NAME,
                file_types=file_types,
                _filter=None,  # 子表不需要额外过滤
                return_field=None
            )

            return await self._search_with_source(result, "sub_table")
        except Exception as e:
            logger.error(f"[UnstructuredGraph] Sub table search failed: {e}")
            return {"search_results": []}

    async def _parallel_search_all(self, state: SearchState):
        """并行执行所有相关的搜索任务"""
        intent = state["intent"]
        search_tasks = []

        # 根据意图决定执行哪些搜索任务
        if intent and "main" in intent.tables:
            if "summary" in intent.main_bm25_fields:
                search_tasks.append(self.search_main_table_summary(state))

            if "chunk" in intent.main_bm25_fields:
                search_tasks.append(self.search_main_table_chunk(state))

            if any(f in intent.main_bm25_fields for f in ["question1", "question2", "question3"]):
                search_tasks.append(self.search_main_table_questions(state))

        if intent and "sub" in intent.tables:
            if intent.sub_bm25_fields:
                search_tasks.append(self.search_sub_table(state))

        # 如果没有搜索任务，返回空结果
        if not search_tasks:
            logger.warning("[UnstructuredGraph] No search tasks to execute")
            return {"search_results": []}

        # 并行执行所有搜索任务
        results = await asyncio.gather(*search_tasks, return_exceptions=True)

        # 合并所有搜索结果
        all_results = []
        for result in results:
            if isinstance(result, dict) and result.get("search_results"):
                all_results.extend(result["search_results"])
            elif isinstance(result, Exception):
                logger.error(f"[UnstructuredGraph] Search task failed: {result}")

        return {"search_results": all_results}

    def _create_graph(self):
        """
        创建非结构化搜索子图。
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