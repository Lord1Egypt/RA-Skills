import asyncio
from typing import Optional, List
from langgraph.graph import StateGraph, END, START
from utils.tools import get_labeled_table_info, get_table_info
from utils.logger import logger
from utils.config import CONFIG
from src.semantic._types import SearchState, FieldScoresResult
from src.semantic.graph.base import BaseGraph, PROMPTS


class FieldGraph(BaseGraph):
    """
    字段搜索子图。
    """
    def __init__(self, vector_db, llm):
        super().__init__(vector_db, llm)
        self.graph = self._create_graph()

    async def _get_table_info_with_fallback(
        self,
        resource_id: str,
        timeout: float
    ) -> Optional[str]:
        """获取表信息，优先使用 labeled table info，失败时回退到普通 table info"""
        # 优先尝试获取 labeled table info
        try:
            labeled_table_info = await asyncio.wait_for(
                get_labeled_table_info(resource_id),
                timeout=timeout
            )
            if labeled_table_info:
                return labeled_table_info
        except Exception as e:
            logger.debug(f"[FieldGraph] Labeled table info failed: {e}")

        # 回退到普通 table info
        try:
            table_info = await asyncio.wait_for(
                get_table_info(resource_id),
                timeout=timeout
            )
            return table_info
        except asyncio.TimeoutError:
            logger.warning(f"[FieldGraph] Table info timeout for resource {resource_id}")
        except Exception as e:
            logger.warning(f"[FieldGraph] Table info failed for resource {resource_id}: {e}")

        return None

    async def _call_llm_field_search(
        self,
        table_info: str,
        query: str
    ) -> List:
        """调用 LLM 进行字段搜索"""
        prompt = PROMPTS["FIELD_SEARCH_PROMPT"]
        prompt_filled = prompt % (table_info, query)

        field_info = await asyncio.to_thread(
            self.llm.create,
            response_model=FieldScoresResult,
            messages=[{"role": "user", "content": prompt_filled}],
            model=CONFIG["llm"]["model"]
        )

        logger.info(f"[FieldGraph] Field Search LLM Response: {field_info}")
        return field_info.fields

    async def execute_field_search(self, state: SearchState):
        """
        字段搜索逻辑。
        """
        query = state["query"]
        resource_id = state["resource_id"]
        resource_name = state["resource_name"]
        timeout = state["timeout"]

        # 获取表信息
        table_info = await self._get_table_info_with_fallback(resource_id, timeout)

        if not table_info:
            logger.warning(f"[FieldGraph] No table info available for resource {resource_id}")
            return {"field_result": (resource_id, resource_name, [])}

        logger.info(f"[FieldGraph] Table Info: {table_info}")

        # 调用 LLM 进行字段搜索
        try:
            result = await self._call_llm_field_search(table_info, query)
            return {"field_result": (resource_id, resource_name, result)}
        except Exception as e:
            logger.error(f"[FieldGraph] LLM call failed: {e}")
            return {"field_result": (resource_id, resource_name, [])}

    def _create_graph(self):
        """
        创建字段搜索子图。
        """
        workflow = StateGraph(SearchState)
        workflow.add_node("execute_field_search", self.execute_field_search)
        workflow.add_edge(START, "execute_field_search")
        workflow.add_edge("execute_field_search", END)
        return workflow.compile()