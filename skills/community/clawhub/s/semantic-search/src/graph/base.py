from typing import List, Dict, Any, Optional, Literal
import pandas as pd
import asyncio
import os
import yaml
import openai
import instructor

from src.vector import FlightDataBase
from utils.tools import (
    batch_get_infos, 
    call_rerank_sdk, 
    call_qwen_rerank
)
from utils.logger import logger
from utils.config import CONFIG
from src.semantic.intent import global_intent
from src.semantic._types import SearchState


yaml_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompts.yaml")
with open(yaml_path, "r", encoding="utf-8") as f:
    PROMPTS = yaml.safe_load(f)


# Constants
STRUCT_TABLE_NAME = CONFIG["struct_table"]
STRUCT_TABLE_EMBED_FIELD = CONFIG["struct_table_embed_field"]
SUB_STRUCT_TABLE_NAME = CONFIG["sub_struct_table"]
SUB_STRUCT_TABLE_EMBED_FIELD = CONFIG["sub_struct_table_embed_field"]
TEXT_TABLE_NAME = CONFIG["text_table"]
TEXT_TABLE_EMBED_FIELD = CONFIG["text_table_embed_field"]
SUB_TEXT_TABLE_NAME = CONFIG["sub_text_table"]
SUB_TEXT_TABLE_EMBED_FIELD = CONFIG["sub_text_table_embed_field"]
OLD_STRUCT_TABLE_NAME = CONFIG["old_struct_table"]
OLD_STRUCT_TABLE_EMBED_FIELD = CONFIG["old_struct_table_embed_field"]
OLD_FILE_TABLE_NAME = CONFIG["old_text_table"]
OLD_FILE_TABLE_EMBED_FIELD = CONFIG["old_text_table_embed_field"]


class BaseGraph:
    """
    基础搜索图类，包含通用节点和资源初始化。
    """
    def __init__(self, vector_db=None, llm=None):
        
        self.vector_db = vector_db or FlightDataBase()
        self.llm = llm or instructor.from_openai(
            openai.OpenAI(
                api_key=CONFIG["llm"]["api_key"],
                base_url=CONFIG["llm"]["base_url"]
            ),
            mode=instructor.Mode.JSON
        )

    def _extract_content_by_source(self, source: str, content_raw: str) -> Optional[str]:
        """根据来源类型提取内容"""
        import json

        if pd.isna(content_raw) or content_raw == "":
            return None

        if source == 'resource_abstract':
            return f"资源摘要：{content_raw}"

        elif source == 'coverage':
            try:
                data = json.loads(content_raw)
                if isinstance(data, dict) and 'coverage' in data and data['coverage']:
                    return f"覆盖范围：{data['coverage']}"
            except (json.JSONDecodeError, TypeError):
                pass

        elif source == 'kg_info':
            try:
                data = json.loads(content_raw)
                if isinstance(data, dict) and '业务分类' in data and data['业务分类']:
                    cats = data['业务分类']
                    val = ",".join(cats) if isinstance(cats, list) else str(cats)
                    return f"业务分类：{val}"
            except (json.JSONDecodeError, TypeError):
                pass

        elif source == 'file_name':
            return f"文件名：{content_raw}"

        return None

    def _aggregate_group(self, group):
        """聚合同一 resource_id 的多个来源结果"""
        # 取第一行的基础信息
        result = group.iloc[0].copy()

        # 收集所有来源的匹配信息用于 Rerank
        match_contents = []
        seen_content = set()

        for _, row in group.iterrows():
            source = row.get('source', '')
            content_raw = row.get('content', '')

            content_str = self._extract_content_by_source(source, content_raw)

            if content_str and content_str not in seen_content:
                match_contents.append(content_str)
                seen_content.add(content_str)

        # 更新 content 列，用于 Rerank
        result['content'] = "；".join(match_contents)

        # 合并 source 列以便调试
        result['source'] = ",".join(group['source'].unique())

        return result

    async def merge_results(self, state: SearchState):
        """
        合并来自不同来源的搜索结果，并为重排序生成内容。
        """
        results = state.get("search_results", [])

        if not results:
            return {"candidate_tables": pd.DataFrame()}

        # 1. 合并所有结果
        all_dfs = [df for df in results if isinstance(df, pd.DataFrame) and not df.empty]

        if not all_dfs:
            return {"candidate_tables": pd.DataFrame()}

        merged = pd.concat(all_dfs, ignore_index=True)

        if merged.empty or 'resource_id' not in merged.columns:
            return {"candidate_tables": pd.DataFrame()}

        # 2. 按 resource_id 分组聚合
        final_candidates = merged.groupby(
            'resource_id', as_index=False, sort=False
        ).apply(self._aggregate_group).reset_index(drop=True)

        return {"candidate_tables": final_candidates}


    def _extract_documents(self, original_data: pd.DataFrame) -> List[str]:
        """从原始数据中提取文档内容"""
        documents = []
        for _, row in original_data.iterrows():
            content_parts = []
            if 'content' in row and pd.notna(row['content']):
                content_parts.append(str(row['content']))
            documents.append(" ".join(content_parts) if content_parts else "")
        return documents

    def _build_rerank_data(
        self,
        original_data: pd.DataFrame,
        documents: List[str],
        rerank_results: List[Dict]
    ) -> pd.DataFrame:
        """构建重排序后的数据框"""
        rerank_data = []
        for result in rerank_results:
            index = result.get('index', 0)
            score = result.get('relevance_score', 0.0)
            if index < len(original_data):
                original_row = original_data.iloc[index]
                rerank_data.append({
                    'resource_id': original_row.get('resource_id'),
                    'content': documents[index],
                    'score': score,
                    **{col: original_row.get(col) for col in original_data.columns if col not in ['resource_id']}
                })
        return pd.DataFrame(rerank_data)

    async def rerank_results(self, state: SearchState):
        """
        使用重排序模型对候选结果进行重排序。
        """
        original_data = state.get("candidate_tables", pd.DataFrame())
        query = state["query"]
        top_k = state.get("top_k", 10)

        if original_data.empty:
            return {"candidate_tables": original_data}

        documents = self._extract_documents(original_data)

        # 尝试使用 Qwen rerank
        try:
            rerank_results = call_qwen_rerank(query, documents, top_k=top_k, mode="file")
            rerank_data = self._build_rerank_data(original_data, documents, rerank_results)
            return {"candidate_tables": rerank_data}

        except Exception as e:
            logger.warning(f"[SearchGraph] Qwen rerank failed: {e}, trying BGE")

            # 降级到 BGE rerank
            try:
                bge_res = call_rerank_sdk(query=query, df=original_data, text_field="content")
                return {"candidate_tables": bge_res}

            except Exception as inner_e:
                logger.error(f"[SearchGraph] BGE rerank failed: {inner_e}")
                return {"candidate_tables": original_data.head(top_k)}


    async def fetch_details(self, state: SearchState):
        """
        获取搜索结果的详细信息。
        """
        candidates = state.get("candidate_tables", pd.DataFrame())
        top_k = state.get("top_k", 10)
        
        if candidates.empty:
            return {"final_result": []}
            
        if len(candidates) > top_k:
            candidates = candidates.head(top_k)
            
        try:
            recs = candidates.to_dict(orient="records")
            final = await batch_get_infos(recs)
            return {"final_result": final}
        except Exception as e:
            logger.error(f"[SearchGraph] Fetch details failed: {e}")
            return {"final_result": []}


    async def fetch_single_by_id(self, state: SearchState):
        """
        根据 ID 获取单个结果。
        """
        res = await batch_get_infos([{"resource_id": state["filter"][0]}])
        return {"final_result": res}


    async def fetch_multi_ids_and_rank(self, state: SearchState):
        """
        根据多个 ID 获取结果并进行排序。
        """
        _filter = state.get("filter", [])
        vector_db = self.vector_db
        search_type = state["search_type"]
        
        if search_type == "structured":
            table_name = STRUCT_TABLE_NAME
            fields = CONFIG["struct_table_embed_field"]
            sql = f"SELECT resource_id, {','.join(map(str, fields))} FROM {table_name} WHERE resource_id IN ({','.join(map(str, _filter))})"
        else:
            fields = CONFIG["sub_text_table_embed_field"]
            sub_table = SUB_TEXT_TABLE_NAME
            sql = f"SELECT resource_id, {','.join(map(str, fields))} FROM {sub_table} WHERE resource_id IN ({','.join(map(str, _filter))})"
            
        df = pd.DataFrame(await vector_db.query(sql))
        
        if df.empty:
            return {"candidate_tables": pd.DataFrame()}
            
        df_unique = df.drop_duplicates(subset=['resource_id'], keep='first')
        return {"candidate_tables": df_unique}