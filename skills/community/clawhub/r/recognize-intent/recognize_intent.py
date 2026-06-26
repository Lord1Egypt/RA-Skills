"""
意图识别技能 (Skill: Recognize Intent)
原始来源:
  - app/ai_chat_agents/recognize_intent.py  (handle_message 路由)
  - app/crud/intent_recognition.py          (classify / composite_metric_data / extract_indicator /
                                             extract_metric / _process_single_candidate_metric_list)
  - app/core/sys_prompt.py                  (system_prompt_intent / system_prompt_extract_metric)

完整实现三条路由的内部逻辑，去除所有 app.* 本地依赖。
外部数据服务通过 Protocol 接口注入；LLM 调用使用 Gemini REST（与原代码一致）。
"""

import json
import logging
import re
import time
import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

import httpx

logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# 0.  意图类型常量
# ═══════════════════════════════════════════════════════════════════

class IntentType:
    WELCOME           = "welcome"
    HANDLE_DATA_QUERY = "handle_data_query"
    HANDLE_METADATA   = "handle_metadata_query"
    ATTRIBUTION       = "attribution_analysis"
    OTHER             = "other"


# ═══════════════════════════════════════════════════════════════════
# 1.  可注入的外部服务接口（Protocol）
# ═══════════════════════════════════════════════════════════════════

@runtime_checkable
class IndicatorSearcher(Protocol):
    """
    指标别名向量搜索服务（对应 indicator_alias_service.search_by_text）
    返回: [{"indicator_code": str, "indicator_name": str,
            "indicator_alias": str, "similarity_score": float}]
    """
    def search_by_text(self, indicator_name: str, top_k: int = 3) -> List[Dict[str, Any]]:
        ...

    def search_all_alias(self) -> str:
        """返回系统所有指标名称拼接字符串（用于 extract_indicator prompt）"""
        ...


@runtime_checkable
class MetricConfigLoader(Protocol):
    """
    指标维度配置加载服务（对应 indicator_metric_service.search_by_text）
    返回: [{"indicator_metadata": str, "aggregation": str, "metric_info": str, ...}]
    """
    def search_by_text(self, indicator_code: str) -> List[Dict[str, Any]]:
        ...


@runtime_checkable
class DictValueReplacer(Protocol):
    """
    字典值替换服务（对应 replace_dict_values）
    将 metric_data 中的中文值替换为标准编码值。
    """
    def replace(self, metric_info: str, metric_data: List[Dict], user_input: str) -> List[Dict]:
        ...


@runtime_checkable
class SemanticConceptExtractor(Protocol):
    """
    L1 语义概念抽取 + 向量召回（对应 semantic_logic_service）
    """
    def extract_and_recall_async(self, user_input: str, current_date: str) -> Any:
        """返回 Future，.result(timeout) 获取 {"l1_concepts": {...}, "l1_vector_candidates": {...}}"""
        ...

    def merge_candidates(
            self,
            l2_metrics: List[Dict],
            l1_concepts: List[Dict],
            user_input: str,
    ) -> Dict[str, Any]:
        """
        返回: {"candidates": [...], "l1_vector_candidates": {...}}
        candidates[i] = {"candidate_id": "SQL-F"|"SQL-1"..., "metric_list": [...]}
        """
        ...


# ═══════════════════════════════════════════════════════════════════
# 2.  入参 / 出参数据类
# ═══════════════════════════════════════════════════════════════════

@dataclass
class IntentInput:
    query: str
    memory_id: str = ""


@dataclass
class IntentOutput:
    intent: str
    indicator_metric: List[Dict[str, Any]] = field(default_factory=list)
    l1_concepts: Dict[str, Any] = field(default_factory=dict)
    vector_candidates: Dict[str, Any] = field(default_factory=dict)
    candidates: Dict[str, Any] = field(default_factory=dict)
    # 归因分析专用（嵌套分析组）
    indicator_metric_groups: List[List[Dict[str, Any]]] = field(default_factory=list)
    mode: str = ""
    success: bool = True
    message: str = ""
    # 澄清类响应（缺少必填字段时）
    result_data: Optional[Dict[str, Any]] = None


# ═══════════════════════════════════════════════════════════════════
# 3.  Gemini REST 工具函数（与原 call_gemini_rest_sync 完全一致）
# ═══════════════════════════════════════════════════════════════════

def _call_gemini_rest_sync(
        prompt: str,
        api_url: str,
        api_key: str,
        token: str,
        timeout: float = 120.0,
) -> str:
    """同步调用 Gemini REST API（原 intent_recognition.call_gemini_rest_sync）"""
    headers = {
        "x-goog-api-key": api_key,
        "token":           token,
        "Content-Type":    "application/json",
        "Accept":          "*/*",
    }
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"thinkingConfig": {"thinkingLevel": "low"}},
    }
    start = time.time()
    try:
        with httpx.Client(timeout=timeout) as client:
            resp = client.post(api_url, json=payload, headers=headers)
            resp.raise_for_status()
            result = resp.json()
            duration = time.time() - start
            content = ""
            candidates = result.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    content = parts[0]["text"]
            logger.info(f"Gemini REST 调用成功，耗时 {duration:.2f}s")
            return content
    except Exception as e:
        logger.error(f"Gemini REST 调用失败: {e}")
        raise


# ═══════════════════════════════════════════════════════════════════
# 4.  System Prompts（从 app/core/sys_prompt.py 内联）
# ═══════════════════════════════════════════════════════════════════

# 意图分类 Prompt（原 sys_prompt.system_prompt_intent）
_INTENT_SYSTEM_PROMPT = """
    你是全棉时代的AI问数系统意图识别专家，你叫小棉，负责识别用户提问问题的意图。
    
    用户意图包含以下几类：
    welcome: 欢迎问候阶段
    - 判断依据：用户输入包含问候语、致谢、道别、或开放性的起始性问句
    - 语义特征：句子长度<6词，无产品相关名词
    - 例如：你好、哈喽、在吗、谢谢、再见、你叫什么名字
                
    handle_metadata_query: 查询某个指标的概念
    - 判断依据：当用户在询问某个指标的定义、含义、是什么意思，元数据、或计算逻辑时
    - 语义特征：问题中包含定义、含义是什么、是什么意思、计算逻辑、公式、元数据、口径、口径变化等关键词
    - 例如：GMV是什么、毛利率计算逻辑是什么、UV和PV的区别、这个指标的口径变了吗
    
    handle_data_query: 查询某个指标具体的数据
    - 判断依据：问题明确要求获取特定时间范围、维度、或条件下的具体数值，注意一定是要获取某些值，而不是咨询原因
    - 语义特征：包含指标名（GMV、销售额）、数值询问词（是多少、查一下、看下）
    - 例如：11月的GMV是多少、查询上周的销售额、北京地区上个月的退货率
    
    attribution_analysis: 归因分析
    - 判断依据：用户在询问数据背后的原因、影响因素、或变化归属，要求系统进行追溯性分析
    - 语义特征：包含为什么、为啥、下降了/上涨了的原因、归因、影响因素等关键词
    - 例如：为什么今天的GMV下降了？、请对上个月用户流失率上升进行归因分析
    
    other: 其他
    - 判断依据：不属于上述任何一种意图的提问
    - 例如：你们系统怎么用、这个功能有什么用
    
    你需要根据本次咨询的用户问题以及用户历史的问题来综合推测用户本次的意图，请仅返回以上意图名称之一，无需任何解释
"""

# 指标提取 Prompt（原 sys_prompt.system_prompt_extract_indicator）
_EXTRACT_INDICATOR_PROMPT = """
        # 角色
        您是稳健医疗的 "AI问数核心指标提取专家"。您的唯一任务是从用户问题中提取**唯一的一个**最核心的查询指标。
        
        # 提取规则
        ## 1. 单一输出原则
        * 无论问题中提及多少个业务名词，只能返回一个指标名称。
        * 优先级: 基础量值 > 比率/衍生值
        ## 2. 负向清洗
        * 排除："同比"、"环比"、"增长率"、"趋势"、"情况"、"占比"、"分布"
        * 排除维度：时间、地点、渠道名称
        ## 3. 输出格式
        * 仅输出指标名称字符串，不要JSON，不要标点，不要解释。
        * 未发现指标返回：未发现指标

        # Few-Shot Examples
        User: "华东区各个小区的订单成交额、预算达成率，以及同比情况"
        Output: 订单成交额

        User: "查询北站店近三个月非会员成交额"
        Output: 非会员成交额

        User: "你好"
        Output: 未发现指标
"""

# 维度槽位提取 Prompt 模板（原 sys_prompt.system_prompt_extract_metric）
_EXTRACT_METRIC_PROMPT_TEMPLATE = """
        # Role
你是一个专精于商业智能（BI）系统的**语义槽位提取引擎**。你的核心任务是精准识别用户自然语言中的查询条件，将其映射为标准的结构化 JSON 数据。

# Context
- **当前系统时间**: {formatted_time}
- **任务目标**: 从用户问题中提取筛选维度（Dimensions），并根据提供的字典进行标准化。
- **处理模式**: **合并模式**。输入的用户问题可能包含多个句子，你需要分析所有句子，合并为一个统一的查询条件集合。

# Input Data
1. **用户问题**: {summary_resp}
2. **指标维度字典**: {metric_info}

---

# ⛔ Critical Constraints
1. **禁止批处理输出**：无论 Input Data 是多少个句子，**最终只能输出一个 JSON 对象**。
2. **绝对禁止提取"全棉"/"全棉时代"** 作为业务筛选维度。
3. **严禁返回数组**：JSON 中的 `value` 字段必须是字符串，多个值用英文逗号分隔。

---

# ⚙️ Extraction Rules

## 1. 时间维度处理
**原则**：将自然语言时间转换为 `yyyy-MM-dd to yyyy-MM-dd` 格式。
**基准时间**：{formatted_time}（所有时间计算基于此）

## 2. 实体归一化
| 关键词 | 目标维度(metric_name) | 编码(metric_code) | 标准Value |
|:---|:---|:---|:---|
| 门店 | 渠道名称 | chanl_name | 全棉门店事业部-连锁店,全棉门店事业部-新零售 |
| 电商 | 渠道名称 | chanl_name | 电商事业部 |
| 直播 | 渠道名称 | chanl_name | 稳健直播中心事业部 |
| 天猫/淘宝 | 二级渠道名称 | lv2_chanl_name | 淘系 |
| 京东 | 二级渠道名称 | lv2_chanl_name | 京东 |
| 拼多多/抖音/快手 | 大店名称 | big_shop_name | 对应名称 |

## 3. 隐式推断与去重
- 包含"哪个"、"排名"、"Top"等词时，必须将比较对象提取为维度（value为空字符串表示 Group By）

---

# Output Schema
严格输出以下 JSON，不包含 markdown 标记：

{{
    "metric_list": [
        {{
            "metric_name": "维度名称",
            "metric_code": "维度编码",
            "value": "归一化后的值",
            "logic_dsl": ""
        }}
    ]
}}
"""


# ═══════════════════════════════════════════════════════════════════
# 5.  核心业务类
# ═══════════════════════════════════════════════════════════════════

class RecognizeIntentSkill:
    """
    意图识别技能

    完整实现三条路由（与原 handle_message + crud/intent_recognition.py 逻辑一致）：
      1. classify          → Gemini REST 调用 + 意图枚举映射
      2. _handle_data_query → extract_indicator + extract_metric + _process_metrics
      3. _handle_attribution → split_user_question + per-question composite_metric_data

    注入依赖（仅外部数据服务）：
      indicator_searcher       : 指标向量搜索
      metric_config_loader     : 指标维度配置加载
      dict_value_replacer      : 字典值替换（中文→编码）
      semantic_extractor       : L1语义概念抽取 + 向量候选（可为 None）
      split_question_fn        : 问题拆解函数（归因路径专用，同步，可为 None）
    """

    def __init__(
            self,
            gemini_api_url: str,
            gemini_api_key: str,
            gemini_token: str,
            indicator_searcher: IndicatorSearcher,
            metric_config_loader: MetricConfigLoader,
            dict_value_replacer: Optional[DictValueReplacer] = None,
            semantic_extractor: Optional[SemanticConceptExtractor] = None,
            split_question_fn: Optional[Any] = None,    # (query, memory_id) -> {"status", "questionList", "mode"}
            llm_timeout: float = 120.0,
    ):
        self.api_url     = gemini_api_url
        self.api_key     = gemini_api_key
        self.token       = gemini_token
        self.timeout     = llm_timeout

        self.indicator_searcher    = indicator_searcher
        self.metric_config_loader  = metric_config_loader
        self.dict_replacer         = dict_value_replacer
        self.semantic_extractor    = semantic_extractor
        self.split_question_fn     = split_question_fn

    # ──────────────────────────────────────────────────────────────────
    # 对外唯一入口
    # ──────────────────────────────────────────────────────────────────

    async def run(self, inp: IntentInput) -> IntentOutput:
        """
        意图识别主流程（原 handle_message 路由逻辑）
        """
        intent = await self._classify(inp.query, inp.memory_id)
        logger.info(f"意图分类: query='{inp.query}' → intent='{intent}'")

        if intent == IntentType.HANDLE_DATA_QUERY:
            return await self._handle_data_query(inp.query, inp.memory_id)

        elif intent == IntentType.HANDLE_METADATA:
            return IntentOutput(intent=IntentType.HANDLE_METADATA, success=True)

        elif intent == IntentType.ATTRIBUTION:
            try:
                return await self._handle_attribution(inp.query, inp.memory_id)
            except Exception as e:
                logger.error(f"归因分析失败，降级数据查询: {e}")
                return await self._handle_data_query(inp.query, inp.memory_id)

        else:
            return IntentOutput(intent=IntentType.OTHER, success=True)

    # ──────────────────────────────────────────────────────────────────
    # 步骤1: 意图分类（原 classify）
    # ──────────────────────────────────────────────────────────────────

    async def _classify(self, query: str, memory_id: str) -> str:
        """
        调用 Gemini REST 进行意图分类（原 intent_recognition.classify）

        原始实现使用 LangChain agent.invoke（底层仍是 LLM 调用），
        此处直接使用 Gemini REST，System Prompt 完全一致。
        返回: IntentType 常量字符串
        """
        prompt = f"{_INTENT_SYSTEM_PROMPT}\n\n用户问题：{query}"
        try:
            content = await asyncio.to_thread(
                _call_gemini_rest_sync,
                prompt, self.api_url, self.api_key, self.token, self.timeout,
            )
            result = content.strip().lower()
            # 映射到标准 IntentType 字符串
            for intent in [
                IntentType.HANDLE_DATA_QUERY,
                IntentType.HANDLE_METADATA,
                IntentType.ATTRIBUTION,
                IntentType.WELCOME,
            ]:
                if intent in result:
                    return intent
            return IntentType.OTHER
        except Exception as e:
            logger.error(f"意图分类失败: {e}")
            return IntentType.OTHER

    # ──────────────────────────────────────────────────────────────────
    # 步骤2a: 数据查询路由（原 handle_query_data / composite_metric_data）
    # ──────────────────────────────────────────────────────────────────

    async def _handle_data_query(self, query: str, memory_id: str) -> IntentOutput:
        """
        完整还原 composite_metric_data 流程:
          extract_indicator → extract_metric → _process_single_candidate_metric_list
        """
        # ① 提取指标
        indicator_result = await self._extract_indicator(query, memory_id)
        if not indicator_result["success"]:
            return IntentOutput(
                intent=IntentType.HANDLE_DATA_QUERY,
                success=False,
                message=indicator_result.get("message", "指标提取失败"),
                result_data=indicator_result.get("result_data"),
            )

        metric_info_config = indicator_result["metric_info"]   # str（JSON）

        # ② 槽位提取（L2 Gemini REST + L1 语义召回合并）
        metric_extraction = await self._extract_metric(query, memory_id, metric_info_config)
        metric_list        = metric_extraction.get("metric_list", [])
        l1_concepts        = metric_extraction.get("l1_concepts", {})
        vector_candidates  = metric_extraction.get("vector_candidates", {})

        if not metric_list and not l1_concepts:
            return IntentOutput(
                intent=IntentType.HANDLE_DATA_QUERY,
                success=False,
                message="维度提取失败，请尝试重新描述问题",
            )

        # ③ 处理候选维度（校验、字典替换、业务规则）
        process_result = await self._process_metrics(
            metric_list, metric_info_config, query, memory_id
        )
        if not process_result["success"]:
            return IntentOutput(
                intent=IntentType.HANDLE_DATA_QUERY,
                success=False,
                message=process_result.get("message", "维度处理失败"),
                result_data=process_result.get("result_data"),
            )

        # ④ 构建输出
        indicator_metric = [{
            "indicator_name":     indicator_result["indicator_name"],
            "indicator_code":     indicator_result["indicator_code"],
            "indicator_metadata": indicator_result["indicator_metadata"],
            "aggregation":        indicator_result.get("aggregation", ""),
            "metric_info":        process_result["metric_data"],
        }]

        return IntentOutput(
            intent=IntentType.HANDLE_DATA_QUERY,
            success=True,
            indicator_metric=indicator_metric,
            l1_concepts=l1_concepts,
            vector_candidates=vector_candidates,
        )

    async def _extract_indicator(self, query: str, memory_id: str) -> Dict[str, Any]:
        """
        提取指标名并搜索指标配置（原 extract_indicator）

        流程:
          1. 获取系统所有指标名称（注入）
          2. 调用 LLM 提取指标名
          3. 向量搜索最相似指标（相似度 > 0.5 直接命中）
          4. 加载 metric_info 配置
        """
        # Step 1: 获取所有指标名称拼接串
        all_alias = ""
        try:
            all_alias = self.indicator_searcher.search_all_alias()
        except Exception as e:
            logger.warning(f"获取所有指标名失败: {e}")

        # Step 2: LLM 提取指标名
        prompt_input = f"用户问题：{query}"
        if all_alias:
            prompt_input += f"\n当前系统只存在以下指标: {all_alias}"

        full_prompt = f"{_EXTRACT_INDICATOR_PROMPT}\n\n{prompt_input}"
        try:
            content = await asyncio.to_thread(
                _call_gemini_rest_sync,
                full_prompt, self.api_url, self.api_key, self.token, self.timeout,
            )
            indicator_name = content.strip()
        except Exception as e:
            logger.error(f"LLM 提取指标名失败: {e}")
            return {"success": False, "message": f"指标提取 LLM 调用失败: {e}"}

        # 指标名标准化映射（原代码 indicator_alias_map）
        ALIAS_MAP = {
            "年累订单成交额": "订单成交额", "月累订单成交额": "订单成交额",
            "销售业绩": "订单成交额", "直播业绩": "订单成交额",
            "业绩达成率": "订单成交额", "抖音业绩": "订单成交额",
        }
        indicator_name = ALIAS_MAP.get(indicator_name, indicator_name)

        if not indicator_name or indicator_name == "未发现指标" or not indicator_name.strip():
            return {"success": False, "message": "未能从输入中提取到指标名称"}

        # Step 3: 向量搜索
        try:
            indicator_list = await asyncio.to_thread(
                self.indicator_searcher.search_by_text, indicator_name, 3
            )
        except Exception as e:
            logger.error(f"指标向量搜索失败: {e}")
            return {"success": False, "message": f"指标搜索失败: {e}"}

        if not indicator_list:
            return {
                "success": False,
                "message": f"未找到与'{indicator_name}'相关的指标，请确认问题中的指标名称",
            }

        best_match = indicator_list[0]
        similarity  = best_match.get("similarity_score", 0.0)
        logger.info(f"指标搜索: '{indicator_name}' → '{best_match.get('indicator_name')}' (相似度 {similarity:.2f})")

        # 相似度 <= 0.5 返回候选列表
        if similarity <= 0.5:
            candidates = [
                {
                    "indicator_code":  item.get("indicator_code"),
                    "indicator_name":  item.get("indicator_name"),
                    "similarity_score": item.get("similarity_score", 0.0),
                }
                for item in indicator_list
            ]
            candidate_str = "\n".join([f"- {c['indicator_name']}({c['indicator_code']})" for c in candidates])
            return {
                "success": False,
                "candidates": candidates,
                "message": f"未找到匹配的指标，您可能想问的是：\n{candidate_str}\n\n请重新输入您想咨询的问题",
            }

        # Step 4: 加载 metric_info 配置
        indicator_code = best_match.get("indicator_code")
        try:
            metric_list = await asyncio.to_thread(
                self.metric_config_loader.search_by_text, indicator_code
            )
        except Exception as e:
            logger.error(f"加载指标配置失败: {e}")
            return {"success": False, "message": f"指标配置加载失败: {e}"}

        if not metric_list:
            return {"success": False, "message": "该指标未配置维度数据，请联系开发处理"}

        indicator_resp = metric_list[0]
        return {
            "success":            True,
            "indicator_code":     indicator_code,
            "indicator_name":     best_match.get("indicator_name"),
            "indicator_metadata": indicator_resp.get("indicator_metadata", ""),
            "aggregation":        indicator_resp.get("aggregation", ""),
            "metric_info":        indicator_resp.get("metric_info", "[]"),
        }

    async def _extract_metric(
            self, query: str, memory_id: str, metric_info: str
    ) -> Dict[str, Any]:
        """
        L2 槽位提取 + L1 语义召回合并（原 extract_metric）

        流程:
          1. 精简 metric_info 字段（只保留 metric_name/code/desc）
          2. 构建 Prompt，调用 Gemini REST（L2 槽位识别，最多重试5次）
          3. 并行触发 L1 语义概念抽取（若有 semantic_extractor）
          4. 合并 L1/L2 候选，取融合方案 SQL-F
        """
        formatted_time = datetime.now().strftime("%Y-%m-%d")

        # Step 1: 精简 metric_info
        try:
            raw = json.loads(metric_info) if isinstance(metric_info, str) else metric_info
            simplified = [
                {
                    "metric_name": item.get("metric_name", ""),
                    "metric_code": item.get("metric_code", ""),
                    "metric_desc": item.get("metric_desc", ""),
                }
                for item in (raw if isinstance(raw, list) else [])
                if isinstance(item, dict)
            ]
            metric_info_str = json.dumps(simplified, ensure_ascii=False)
        except Exception:
            metric_info_str = metric_info

        # Step 2: 构建 Prompt
        prompt = _EXTRACT_METRIC_PROMPT_TEMPLATE.format(
            formatted_time=formatted_time,
            summary_resp=query,
            metric_info=metric_info_str,
        )
        logger.info(f"L2 槽位提取 Prompt (前200字): {prompt[:200]}...")

        # Step 3: 触发 L1 语义概念抽取（异步，不阻塞 L2）
        l1_future = None
        if self.semantic_extractor:
            try:
                l1_future = self.semantic_extractor.extract_and_recall_async(
                    query, current_date=formatted_time
                )
            except Exception as e:
                logger.warning(f"L1 语义抽取启动失败: {e}")

        # Step 4: L2 Gemini REST 调用（失败最多重试 5 次）
        llm_extracted_metrics = []
        MAX_L2_RETRY = 5
        for attempt in range(MAX_L2_RETRY):
            try:
                content = await asyncio.to_thread(
                    _call_gemini_rest_sync,
                    prompt, self.api_url, self.api_key, self.token, self.timeout,
                )
                llm_extracted_metrics = self._parse_llm_metric_response(content, query)
                if llm_extracted_metrics:
                    break
                # 检查是否返回了合法 JSON（若是则停止重试）
                if self._is_valid_json(content):
                    break
                logger.warning(f"L2 槽位第 {attempt+1} 次重试（非 JSON 响应）")
            except Exception as e:
                logger.error(f"L2 槽位第 {attempt+1} 次调用失败: {e}")

        # Step 5: 等待 L1 结果
        l1_concepts: Dict[str, Any] = {}
        l1_vector_candidates: Dict[str, Any] = {}
        if l1_future:
            try:
                l1_result = l1_future.result(timeout=30)
                l1_concepts = l1_result.get("l1_concepts", {})
            except Exception as e:
                logger.warning(f"等待 L1 结果失败: {e}")

        # Step 6: L1/L2 候选合并（若有 semantic_extractor）
        metric_list = []
        if self.semantic_extractor and (llm_extracted_metrics or l1_concepts):
            try:
                l1_concepts_list = l1_concepts.get("concepts", []) if isinstance(l1_concepts, dict) else []
                merge_result = await asyncio.to_thread(
                    self.semantic_extractor.merge_candidates,
                    llm_extracted_metrics,
                    l1_concepts_list,
                    query,
                )
                candidates        = merge_result.get("candidates", [])
                l1_vector_candidates = merge_result.get("l1_vector_candidates", {})
                # 优先取 SQL-F 融合方案
                f_candidate = next((c for c in candidates if c.get("candidate_id") == "SQL-F"), None)
                metric_list = f_candidate["metric_list"] if f_candidate else (
                    candidates[0]["metric_list"] if candidates else llm_extracted_metrics
                )
            except Exception as e:
                logger.error(f"L1/L2 候选合并失败，降级使用 L2: {e}")
                metric_list = llm_extracted_metrics
        else:
            metric_list = llm_extracted_metrics

        return {
            "metric_list":       metric_list,
            "l1_concepts":       l1_concepts,
            "vector_candidates": l1_vector_candidates,
        }

    async def _process_metrics(
            self, metric_data: List[Dict], metric_info: str, query: str, memory_id: str
    ) -> Dict[str, Any]:
        """
        处理维度候选列表（原 _process_single_candidate_metric_list）

        流程:
          1. 校验必填字段
          2. 字典值替换（中文→编码）
          3. 业务规则（xq_name、视频号渠道、二级渠道等）
          4. 过滤不在系统配置中的维度
        """
        # Step 1: 校验必填字段（原 validate_required_metrics）
        validation = self._validate_required_metrics(metric_info, metric_data)
        if not validation["success"]:
            missing_fields = validation.get("missing_fields", [])
            return {
                "success": False,
                "message": validation["message"],
                "result_data": {
                    "clarification_type": "lack_condition_candidates",
                    "original_query": query,
                    "missing_fields": missing_fields,
                    "candidates": [],
                    "message": validation["message"],
                },
            }

        # Step 2: 字典值替换（原 replace_dict_values）
        if self.dict_replacer:
            try:
                metric_data = await asyncio.to_thread(
                    self.dict_replacer.replace, metric_info, metric_data, query
                )
            except Exception as e:
                logger.warning(f"字典值替换失败（继续流程）: {e}")

        # Step 3: 业务规则（原 _process_single_candidate_metric_list 中的规则块）
        metric_data = self._apply_business_rules(metric_data)

        # Step 4: 过滤不在系统配置中的维度
        metric_data = self._filter_invalid_metrics(metric_data, metric_info)

        return {"success": True, "metric_data": metric_data}

    # ──────────────────────────────────────────────────────────────────
    # 步骤2b: 归因分析路由（原 handle_insight_analysis / handle_attribution_analysis）
    # ──────────────────────────────────────────────────────────────────

    async def _handle_attribution(self, query: str, memory_id: str) -> IntentOutput:
        """
        归因分析路由（原 intent_recognition.handle_attribution_analysis）

        需要 split_question_fn 注入（原 split_user_question）。
        若未注入，直接调用单问题 composite_metric_data。
        """
        if not self.split_question_fn:
            # 降级：当成单问题数据查询处理
            result = await self._handle_data_query(query, memory_id)
            result.intent = IntentType.ATTRIBUTION
            return result

        # Step 1: 拆解问题（同步，注入函数）
        try:
            question_resp = await asyncio.to_thread(self.split_question_fn, query, memory_id)
        except Exception as e:
            raise RuntimeError(f"问题拆解失败: {e}") from e

        if question_resp.get("status") == "failed":
            error_msg = question_resp.get("message") or question_resp.get("reason", "问题拆解失败")
            return IntentOutput(intent=IntentType.ATTRIBUTION, success=False, message=error_msg)

        question_list = question_resp.get("questionList", [])
        mode          = question_resp.get("mode", "")

        # 兼容旧格式：扁平数组 → 包装为单组
        if question_list and isinstance(question_list[0], str):
            question_list = [question_list]

        # Step 2: 对每组问题串行调用 composite_metric_data
        indicator_metric_groups: List[List[Dict]] = []
        for group_idx, question_group in enumerate(question_list):
            group_metrics: List[Dict] = []
            for sub_query in question_group:
                sub_result = await self._handle_data_query(sub_query, memory_id)
                if not sub_result.success:
                    return IntentOutput(
                        intent=IntentType.ATTRIBUTION,
                        success=False,
                        message=sub_result.message,
                    )
                # 取第一个 indicator_metric 条目
                if sub_result.indicator_metric:
                    group_metrics.append(sub_result.indicator_metric[0])
            indicator_metric_groups.append(group_metrics)
            logger.info(f"归因分析组 {group_idx+1}: {len(question_group)} 个问题 → {len(group_metrics)} 个指标")

        return IntentOutput(
            intent=IntentType.ATTRIBUTION,
            success=True,
            indicator_metric_groups=indicator_metric_groups,
            mode=mode,
        )

    # ──────────────────────────────────────────────────────────────────
    # 工具函数（原代码中的辅助函数，无外部依赖可直接实现）
    # ──────────────────────────────────────────────────────────────────

    @staticmethod
    def _parse_llm_metric_response(content: Any, user_input: str) -> List[Dict]:
        """
        解析 LLM 返回的维度提取结果（原 parse_llm_metric_response）
        支持: JSON 对象 / JSON 数组 / Markdown 代码块 / 多段 JSON 拼接
        """
        extracted: List[Dict] = []
        try:
            if isinstance(content, str):
                clean = re.sub(r"```json\s*", "", content, flags=re.IGNORECASE)
                clean = re.sub(r"```\s*", "", clean).strip()
                try:
                    parsed = json.loads(clean)
                except json.JSONDecodeError:
                    # 尝试提取所有独立 JSON 对象
                    obj_matches = re.findall(r"\{.*?\}", clean, re.DOTALL)
                    parsed_list = []
                    for obj_str in obj_matches:
                        try:
                            parsed_list.append(json.loads(obj_str))
                        except json.JSONDecodeError:
                            continue
                    if parsed_list:
                        parsed = parsed_list
                    else:
                        arr_match = re.search(r"\[.*\]", clean, re.DOTALL)
                        parsed = json.loads(arr_match.group(0)) if arr_match else {}

                if isinstance(parsed, list):
                    for item in parsed:
                        if isinstance(item, dict) and "metric_list" in item:
                            extracted.extend(item.get("metric_list", []))
                elif isinstance(parsed, dict):
                    extracted.extend(parsed.get("metric_list", []))
            elif isinstance(content, dict):
                extracted.extend(content.get("metric_list", []))
            elif isinstance(content, list):
                extracted.extend(content)
        except Exception as e:
            logger.error(f"解析 LLM 维度结果失败: {e}, query={user_input}")
        return extracted

    @staticmethod
    def _is_valid_json(content: str) -> bool:
        """判断字符串是否为合法 JSON"""
        if not isinstance(content, str):
            return True
        try:
            clean = re.sub(r"```json\s*", "", content, flags=re.IGNORECASE)
            clean = re.sub(r"```\s*", "", clean).strip()
            json.loads(clean)
            return True
        except (json.JSONDecodeError, ValueError):
            return False

    @staticmethod
    def _validate_required_metrics(metric_info: str, metric_data: List[Dict]) -> Dict[str, Any]:
        """
        校验必填字段（原 validate_required_metrics）
        必填字段配置在 metric_info JSON 中 need=="true"
        """
        try:
            if not metric_info:
                return {"success": True, "missing_fields": [], "message": ""}

            config_list  = json.loads(metric_info) if isinstance(metric_info, str) else metric_info
            required     = [m for m in config_list if isinstance(m, dict) and m.get("need") == "true"]
            if not required:
                return {"success": True, "missing_fields": [], "message": ""}

            data_dict = {
                item.get("metric_code"): item
                for item in (metric_data if isinstance(metric_data, list) else [])
                if isinstance(item, dict) and item.get("metric_code")
            }

            missing = []
            for req in required:
                code = req.get("metric_code")
                name = req.get("metric_name", code)
                if code not in data_dict:
                    missing.append(name)
                else:
                    val = data_dict[code].get("value", "")
                    if not val or (isinstance(val, str) and not val.strip()):
                        missing.append(name)

            if missing:
                return {
                    "success": False,
                    "missing_fields": missing,
                    "message": f"缺少必填字段：{'、'.join(missing)}，请补充后再试",
                }
            return {"success": True, "missing_fields": [], "message": ""}

        except Exception as e:
            logger.error(f"校验必填字段失败: {e}")
            return {"success": False, "missing_fields": [], "message": f"校验错误: {e}"}

    @staticmethod
    def _apply_business_rules(metric_data: List[Dict]) -> List[Dict]:
        """
        应用业务规则（原 _process_single_candidate_metric_list 中的规则块）

        规则1: xq_name（小区名称）— 只有渠道是门店事业部时才有值
        规则2: 视频号 + 自播/达播 → 拆分 operat_model
        规则3: budget_amt_1d 强制清空 value
        """
        metric_map = {m["metric_code"]: m for m in metric_data if isinstance(m, dict)}

        # 规则1: xq_name
        if "xq_name" in metric_map:
            chanl = metric_map.get("chanl_name")
            if not chanl or chanl.get("value") not in ("全棉门店事业部", "全棉海外事业部"):
                metric_map["xq_name"]["value"] = ""

        # 规则2: 视频号渠道拆分
        lv2 = metric_map.get("lv2_chanl_name")
        if lv2 and "视频号" in (lv2.get("value") or ""):
            val      = lv2["value"]
            has_self = "自播" in val
            has_kol  = "达播" in val
            val = val.replace("自播", "").replace("达播", "")
            val = re.sub(r",+", ",", val).strip(",")
            lv2["value"] = val

            operat_value = "自播,达播" if (has_self and has_kol) else ("自播" if has_self else "达播")
            metric_map["operat_model"] = {
                "dict_type":  "operat_model",
                "join":       "",
                "metric_code": "chanl_code",
                "metric_desc": "运营方式：自播/达播",
                "value":       operat_value,
                "metric_name": "运营方式",
                "table_name":  "ads_wj.ads_bi_ord_sale_pt_d_1df_2mi",
            }

        # 规则3: budget_amt_1d
        if "budget_amt_1d" in metric_map:
            metric_map["budget_amt_1d"]["value"] = ""

        return list(metric_map.values())

    @staticmethod
    def _filter_invalid_metrics(metric_data: List[Dict], metric_info: str) -> List[Dict]:
        """
        过滤不在系统配置中的维度（原代码最后过滤逻辑）
        保留: metric_code 在 metric_info 配置中，或者有 logic_dsl
        """
        try:
            config_list = json.loads(metric_info) if isinstance(metric_info, str) else metric_info
            valid_codes = {
                item.get("metric_code")
                for item in (config_list if isinstance(config_list, list) else [])
                if isinstance(item, dict) and item.get("metric_code")
            }
        except Exception:
            return metric_data

        return [
            m for m in metric_data
            if isinstance(m, dict)
               and m.get("metric_code")
               and (m.get("metric_code") in valid_codes or m.get("logic_dsl"))
        ]


# ═══════════════════════════════════════════════════════════════════
# 6.  真实服务实现（独立运行时使用）
# ═══════════════════════════════════════════════════════════════════

def _load_dotenv() -> None:
    """从当前目录或各层父目录查找并加载 .env 文件"""
    from pathlib import Path
    try:
        from dotenv import load_dotenv
        search_path = Path(__file__).resolve().parent
        for _ in range(8):
            for name in (".env", ".env.dev", ".env.local"):
                env_file = search_path / name
                if env_file.exists():
                    load_dotenv(env_file, override=False)
                    print(f"[配置] 已加载: {env_file}")
                    return
            search_path = search_path.parent
        print("[配置] 未找到 .env，使用系统环境变量")
    except ImportError:
        print("[警告] python-dotenv 未安装，pip install python-dotenv")


def _get_gemini_config() -> Dict[str, str]:
    """从环境变量读取 Gemini API 配置"""
    import os
    base_url = os.getenv("GEMINI_API_URL", "http://47.77.199.56/api/v1beta").rstrip("/")
    model    = os.getenv("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
    _default_token = (
        "BI-eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJ1c2VySWRcIjpcImFkbWluXCIsXCJ1c2VyTG9na"
        "W5OYW1lXCI6bnVsbCxcInBob25lXCI6bnVsbCxcInN0YXR1c1wiOm51bGwsXCJpc1N5c3RlbVVzZX"
        "JcIjpudWxsLFwidmFsaWRUaW1lXCI6bnVsbCxcInRlbmFudElkXCI6bnVsbCxcImVuYWJsZWRcIjp"
        "0cnVlLFwiY3JlZGVudGlhbHNOb25FeHBpcmVkXCI6dHJ1ZSxcImFjY291bnROb25Mb2NrZWRcIjp0"
        "cnVlLFwiYWNjb3VudE5vbkV4cGlyZWRcIjp0cnVlLFwidXNlcm5hbWVcIjpcImFkbWluXCIsXCJhd"
        "XRob3JpdGllc1wiOm51bGx9IiwibmJmIjoxNzA4MTM5OTE5LCJpYXQiOjE3MDgxMzk5MTksImV4cC"
        "I6MTcxMDczMTkxOX0.taP4LXkfO570-eFawyzYlC4RhK9oLJ-YL9r2VfIj8pY"
    )
    return {
        "api_url": f"{base_url}/models/{model}:generateContent",
        "api_key": os.getenv("GEMINI_API_KEY", ""),
        "token":   os.getenv("GEMINI_TOKEN", _default_token),
    }


class _RealIndicatorSearcher:
    """
    真实指标别名向量搜索服务
    - search_by_text  → 连接 Milvus indicator_alias Collection，向量相似度搜索
    - search_all_alias → 查询所有指标名称，拼接为字符串
    使用 .env 中的 MILVUS_* / EMBEDDING_* 配置
    """

    def __init__(self) -> None:
        import os
        from pymilvus import MilvusClient as PyMilvusClient
        from openai import OpenAI
        from pydantic import SecretStr

        host       = os.getenv("MILVUS_HOST", "localhost")
        port       = int(os.getenv("MILVUS_PORT", "19530"))
        user       = os.getenv("MILVUS_USER", "")
        password   = os.getenv("MILVUS_PASSWORD", "")
        db_name    = os.getenv("MILVUS_DB_NAME", "default")
        self._collection = os.getenv("INDICATOR_ALIAS_COLLECTION_NAME", "indicator_alias")

        uri = f"http://{host}:{port}"
        kwargs: Dict[str, Any] = {"uri": uri}
        if user and password:
            kwargs.update({"user": user, "password": password, "db_name": db_name})
        self._milvus = PyMilvusClient(**kwargs)

        self._embed_client = OpenAI(
            api_key=os.getenv("EMBEDDING_API_KEY", ""),
            base_url=os.getenv("EMBEDDING_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        )
        self._embed_model  = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")

    def _vectorize(self, text: str) -> List[float]:
        resp = self._embed_client.embeddings.create(
            model=self._embed_model,
            input=[text],
            dimensions=1024,
            encoding_format="float",
        )
        return resp.data[0].embedding

    def search_by_text(self, indicator_name: str, top_k: int = 3) -> List[Dict[str, Any]]:
        try:
            vec = self._vectorize(indicator_name)
            results = self._milvus.search(
                collection_name=self._collection,
                data=[vec],
                anns_field="indicator_vector",
                search_params={"metric_type": "COSINE", "params": {"nprobe": 10}},
                limit=top_k,
                output_fields=["id", "indicator_name", "indicator_alias", "indicator_code"],
            )
            formatted = []
            for hits in results:
                for hit in hits:
                    entity = hit.get("entity", {})
                    formatted.append({
                        "indicator_code":   entity.get("indicator_code", ""),
                        "indicator_name":   entity.get("indicator_name", ""),
                        "indicator_alias":  entity.get("indicator_alias", ""),
                        "similarity_score": hit.get("distance", 0.0),
                    })
            return formatted
        except Exception as e:
            logger.error(f"指标别名向量搜索失败: {e}")
            return []

    def search_all_alias(self) -> str:
        """查询所有指标名称，拼接为逗号分隔的字符串（供 extract_indicator prompt 使用）"""
        try:
            results = self._milvus.query(
                collection_name=self._collection,
                filter="id != ''",
                output_fields=["indicator_name"],
                limit=2000,
            )
            names = list({r.get("indicator_name", "") for r in results if r.get("indicator_name")})
            return "、".join(names)
        except Exception as e:
            logger.warning(f"获取所有指标名失败: {e}")
            return ""


class _RealMetricConfigLoader:
    """
    真实指标维度配置加载服务
    - search_by_text(indicator_code) → 连接 MySQL indicator_metric 表
    使用 .env 中的 INTENT_MYSQL_* 配置
    """

    def __init__(self) -> None:
        import os
        import pymysql

        self._host     = os.getenv("INTENT_MYSQL_HOST", os.getenv("MYSQL_SERVER", "localhost"))
        self._port     = int(os.getenv("INTENT_MYSQL_PORT", os.getenv("MYSQL_PORT", "3306")))
        self._user     = os.getenv("INTENT_MYSQL_USER", os.getenv("MYSQL_USER", "root"))
        self._password = os.getenv("INTENT_MYSQL_PASSWORD", os.getenv("MYSQL_PASSWORD", ""))
        self._database = os.getenv("INTENT_MYSQL_DATABASE", os.getenv("MYSQL_DB", "winner_ai"))

    def _get_conn(self):
        import pymysql
        return pymysql.connect(
            host=self._host, port=self._port,
            user=self._user, password=self._password,
            database=self._database, charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def search_by_text(self, indicator_code: str) -> List[Dict[str, Any]]:
        try:
            conn   = self._get_conn()
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, indicator_name, indicator_code, indicator_metadata,
                          aggregation, metric_info, create_time, update_time
                   FROM indicator_metric
                   WHERE indicator_code = %s
                   LIMIT 1""",
                (indicator_code,),
            )
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            return list(rows)
        except Exception as e:
            logger.error(f"加载指标配置失败: {e}")
            return []


class _RealDictValueReplacer:
    """
    真实字典值替换服务（对应 replace_dict_values）

    核心逻辑：
      1. 解析 metric_info 配置，找出含有 dict_type 的字段
      2. 对 metric_data 中对应字段的中文 value 进行向量搜索
      3. 命中 sys_dict Milvus Collection 后，将 value 替换为标准 name
      4. 保留 original_value 字段记录替换前的原始值

    注意：业务特殊规则（strat_catg_tag / lunar_yoy_tag / chanl_name 等）在原始代码中
    有额外分支处理，此处实现通用路径，特殊 dict_type 如需精确匹配请在工程侧配置同名
    Milvus 过滤记录。

    使用 .env 中的 MILVUS_* / EMBEDDING_* 配置，Collection 名由 SYS_DICT_COLLECTION_NAME 决定。
    """

    def __init__(self) -> None:
        import os
        from pymilvus import MilvusClient as PyMilvusClient
        from openai import OpenAI

        host     = os.getenv("MILVUS_HOST", "localhost")
        port     = int(os.getenv("MILVUS_PORT", "19530"))
        user     = os.getenv("MILVUS_USER", "")
        password = os.getenv("MILVUS_PASSWORD", "")
        db_name  = os.getenv("MILVUS_DB_NAME", "default")
        self._collection = os.getenv("SYS_DICT_COLLECTION_NAME", "sys_dict")

        uri = f"http://{host}:{port}"
        kwargs: Dict[str, Any] = {"uri": uri}
        if user and password:
            kwargs.update({"user": user, "password": password, "db_name": db_name})
        self._milvus = PyMilvusClient(**kwargs)

        self._embed_client = OpenAI(
            api_key=os.getenv("EMBEDDING_API_KEY", ""),
            base_url=os.getenv("EMBEDDING_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        )
        self._embed_model = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")
        self._min_score   = float(os.getenv("DICT_REPLACE_MIN_SCORE", "0.50"))

    def _vectorize(self, text: str) -> List[float]:
        resp = self._embed_client.embeddings.create(
            model=self._embed_model,
            input=[text],
            dimensions=1024,
            encoding_format="float",
        )
        return resp.data[0].embedding

    def _contains_chinese(self, s: str) -> bool:
        return bool(re.search(r"[\u4e00-\u9fff]", s))

    def _search_dict(self, value: str, dict_type: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """在 sys_dict Collection 中按 dict_type 过滤，向量搜索最相似的字典项"""
        try:
            vec = self._vectorize(value)
            results = self._milvus.search(
                collection_name=self._collection,
                data=[vec],
                anns_field="name_vector",
                search_params={"metric_type": "COSINE", "params": {"nprobe": 10}},
                limit=top_k,
                filter=f'type == "{dict_type}"',
                output_fields=["id", "name", "code", "type"],
            )
            hits = []
            for batch in results:
                for hit in batch:
                    entity = hit.get("entity", {})
                    hits.append({
                        "name":             entity.get("name", ""),
                        "code":             entity.get("code", ""),
                        "type":             entity.get("type", ""),
                        "similarity_score": hit.get("distance", 0.0),
                    })
            return hits
        except Exception as e:
            logger.warning(f"sys_dict 向量搜索失败 (type={dict_type}): {e}")
            return []

    def replace(self, metric_info: str, metric_data: List[Dict], user_input: str) -> List[Dict]:
        """
        将 metric_data 中含有中文 value 的字段替换为 sys_dict 中的标准 name。

        参数:
            metric_info  : JSON 字符串或列表，格式 [{"metric_code": "xxx", "dict_type": "yyy", ...}, ...]
            metric_data  : 维度数据列表，格式 [{"metric_code": "xxx", "value": "中文值", ...}, ...]
            user_input   : 用户原始输入（仅用于日志记录）

        返回:
            处理后的 metric_data（in-place 修改 + 返回同引用）
        """
        if not metric_info or not metric_data:
            return metric_data

        try:
            config_list = json.loads(metric_info) if isinstance(metric_info, str) else metric_info
        except json.JSONDecodeError:
            logger.warning("metric_info JSON 解析失败，跳过字典替换")
            return metric_data

        # 用 metric_code 快速索引 metric_data
        data_index: Dict[str, Dict] = {
            item.get("metric_code", ""): item
            for item in metric_data
            if isinstance(item, dict) and item.get("metric_code")
        }

        for cfg_item in config_list:
            dict_type   = cfg_item.get("dict_type")
            metric_code = cfg_item.get("metric_code")

            if not dict_type or not metric_code:
                continue
            metric_obj = data_index.get(metric_code)
            if not metric_obj:
                continue

            # 若已有 logic_dsl（来自 QA 语料库命中），保留原值
            if metric_obj.get("logic_dsl"):
                continue

            # 同步额外元数据字段
            for key in ("table_name", "join", "metric_desc"):
                if cfg_item.get(key):
                    metric_obj[key] = cfg_item[key]

            value = metric_obj.get("value")
            if not value or not isinstance(value, str):
                continue
            if not self._contains_chinese(value):
                continue

            # 向量搜索替换
            hits = self._search_dict(value, dict_type, top_k=5)
            if hits:
                best = hits[0]
                if best["similarity_score"] >= self._min_score and best["name"]:
                    logger.info(
                        f"[DictReplace] user='{user_input}' code={metric_code} "
                        f"'{value}' → '{best['name']}' (score={best['similarity_score']:.3f})"
                    )
                    metric_obj["original_value"] = value
                    metric_obj["value"]          = best["name"]

        return metric_data


class _RealSemanticConceptExtractor:
    """
    真实 L1 语义概念抽取 + semantic_logic_dict 向量增强服务
    （对应 SemanticLogicService + merge_candidates_for_sql_generation）

    两个功能：
      1. extract_and_recall_async  — 用线程池异步调用 Gemini，
           以 system_prompt_semantic_logic_enrich 为系统提示词，
           抽取用户问题中的时间语义 / 业务概念 / 分析意图；
           返回 Future，.result(timeout) 得到 {"l1_concepts": {...}}。

      2. merge_candidates          — 将 L2 槽位（LLM 提取）和 L1 概念（语义抽取）
           通过 semantic_logic_dict Milvus Collection 向量增强合并：
           · L1 concepts → 搜索 semantic_logic_dict → 命中则打上 logic_dsl / table_name
           · L2 metrics  → 搜索 semantic_logic_dict → 命中则补充字段
           · 去重合并 → 生成候选 SQL-R（最终使用）
           返回 {"candidates": [...], "l1_vector_candidates": {...}}。

    使用 .env 中的 MILVUS_* / EMBEDDING_* / GEMINI_* 配置。
    semantic_logic_dict Collection 名由 SEMANTIC_LOGIC_COLLECTION 配置（默认 semantic_logic_dict）。
    """

    # ── L1 语义概念抽取 System Prompt（对应 sys_prompt.system_prompt_semantic_logic_enrich）──
    _L1_SYSTEM_PROMPT = """
🔹 Role

你是一个商业分析系统中的「语义概念抽取引擎」（Semantic Concept Extractor）。
你的职责是从用户的自然语言问题中，识别其提到的业务概念与分析意图，而不是将其映射为数据库字段。

🔹 Task Objective

从用户问题中抽取以下信息：

1. 时间语义（Time Semantics）
2. 业务概念（Business Concepts）
3. 分析意图（Analytical Intent）
4. 对比 / 分组 / 占比等分析结构信号

⚠️ 重要：
你只输出"用户表达了什么概念"，
不要判断这些概念属于哪个数据库维度或字段。

🔹 Output Schema（严格遵守）
{
  "time_semantics": {
    "original_text": "",
    "normalized_range": "",
    "confidence": 0.0
  },
  "concepts": [
    {
      "text": "",
      "type": "",
      "confidence": 0.0
    }
  ],
  "analysis_intent": [],
  "structure_signals": {
    "compare": false,
    "group_by": [],
    "proportion": false,
    "top_n": false
  }
}

🔹 Extraction Guidelines（核心规则）

1️⃣ 时间语义（Time Semantics）
- 识别用户提到的时间表达（如：本月、上月、今年、最近7天）
- 统一转换为时间区间字符串（如 yyyy-MM-dd to yyyy-MM-dd）
- 当前系统时间：{current_date}
- 若用户未提及时间：normalized_range 设为空字符串，confidence 设为 0.0

2️⃣ 业务概念（Concept Extraction）
你需要抽取用户提到的所有有业务含义的名词或名词短语，包括但不限于：
- 商品 / 系列 / 活动 / 标签 / 主题
- 品类（如棉柔巾、卫生巾）
- 渠道 / 场景（如门店、电商、直播）
- 人群 / 对象（会员、新会员、婴儿）
- 模糊营销语言（如"爆款"、"新年限定"）

每个概念必须包含：
- text：用户原始表达
- type：概念类型（自由文本，如：品类 / 营销概念 / 渠道 / 人群 / 未知）
- confidence：你对"这是一个有效业务概念"的置信度（0~1）

⚠️ 不要合并不同概念
⚠️ 绝对禁止提取公司名："全棉"、"全棉时代"、"Purcotton" 严禁作为概念出现

3️⃣ 分析意图（Analysis Intent）
识别用户"想怎么算"，常见 intent：
query_value / compare / proportion / trend / rank

4️⃣ 结构信号（Structure Signals）
从语义中识别 SQL 结构倾向（不等于字段）：
是否对比、是否分组、是否占比、是否 TopN

🔹 Explicit Prohibitions
🚫 不要输出任何数据库字段名
🚫 不要输出 metric_code / metric_name
🚫 不要输出 SQL 相关内容
🚫 不要使用 BI 字典进行归一化

🔹 Output Example
输入：本月新年限定和好运系列的棉柔巾分别卖了多少，占比棉柔巾全品类多少
输出：
{
  "time_semantics": {"original_text": "本月", "normalized_range": "2025-12-01 to 2025-12-31", "confidence": 0.95},
  "concepts": [
    {"text": "新年限定", "type": "营销/商品概念", "confidence": 0.78},
    {"text": "好运系列", "type": "商品概念", "confidence": 0.66},
    {"text": "棉柔巾", "type": "品类", "confidence": 0.97}
  ],
  "analysis_intent": ["query_value", "compare", "proportion"],
  "structure_signals": {"compare": true, "group_by": ["新年限定", "好运系列"], "proportion": true, "top_n": false}
}
"""

    def __init__(
            self,
            gemini_api_url: str,
            gemini_api_key: str,
            gemini_token: str,
    ) -> None:
        import os
        from concurrent.futures import ThreadPoolExecutor
        from pymilvus import MilvusClient as PyMilvusClient
        from openai import OpenAI

        self._gemini_url   = gemini_api_url
        self._gemini_key   = gemini_api_key
        self._gemini_token = gemini_token
        self._timeout      = float(os.getenv("GEMINI_TIMEOUT", "60"))

        # ── Milvus semantic_logic_dict 连接 ──
        host       = os.getenv("MILVUS_HOST", "localhost")
        port       = int(os.getenv("MILVUS_PORT", "19530"))
        user       = os.getenv("MILVUS_USER", "")
        password   = os.getenv("MILVUS_PASSWORD", "")
        db_name    = os.getenv("MILVUS_DB_NAME", "default")
        self._sl_collection = os.getenv("SEMANTIC_LOGIC_COLLECTION", "semantic_logic_dict")
        self._min_logic_score = float(os.getenv("SEMANTIC_LOGIC_MIN_SCORE", "0.80"))

        uri = f"http://{host}:{port}"
        milvus_kwargs: Dict[str, Any] = {"uri": uri}
        if user and password:
            milvus_kwargs.update({"user": user, "password": password, "db_name": db_name})
        self._milvus = PyMilvusClient(**milvus_kwargs)

        # ── Embedding 客户端（DashScope text-embedding-v4）──
        self._embed_client = OpenAI(
            api_key=os.getenv("EMBEDDING_API_KEY", ""),
            base_url=os.getenv("EMBEDDING_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"),
        )
        self._embed_model = os.getenv("EMBEDDING_MODEL", "text-embedding-v4")

        # ── 线程池（L1 抽取与 L2 并行）──
        self._executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="SemanticL1")

    # ──────────────────────────────────────────────────────────────────
    # 内部工具方法
    # ──────────────────────────────────────────────────────────────────

    def _vectorize(self, text: str) -> List[float]:
        """调用 DashScope embedding API 将文本转为 1024 维向量"""
        resp = self._embed_client.embeddings.create(
            model=self._embed_model,
            input=[text],
            dimensions=1024,
            encoding_format="float",
        )
        return resp.data[0].embedding

    def _call_gemini_with_system_prompt(
            self, user_text: str, system_prompt: str
    ) -> Dict[str, Any]:
        """
        以 system_instruction 方式调用 Gemini（对应 SemanticLogicService._call_llm_api）。
        返回解析后的 JSON 字典；失败时返回 {}。
        """
        import httpx

        # 将当前日期占位符替换（如有）
        headers = {
            "x-goog-api-key": self._gemini_key,
            "token":          self._gemini_token,
            "Content-Type":   "application/json",
            "Accept":         "*/*",
        }
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": user_text}]}
            ],
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            },
            "generationConfig": {
                "thinkingConfig": {"thinkingLevel": "low"}
            },
        }
        try:
            with httpx.Client(timeout=self._timeout) as client:
                resp = client.post(self._gemini_url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()

            # 提取文本内容
            content = ""
            for cand in data.get("candidates", []):
                parts = cand.get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    content = parts[0]["text"]
                    break

            # 清理 Markdown 代码块后解析 JSON
            content_clean = re.sub(r"```json\s*", "", content, flags=re.IGNORECASE)
            content_clean = re.sub(r"```\s*", "", content_clean).strip()
            json_m = re.search(r"\{.*\}", content_clean, re.DOTALL)
            if json_m:
                content_clean = json_m.group(0)
            return json.loads(content_clean)

        except Exception as e:
            logger.error(f"[SemanticConceptExtractor] Gemini 调用失败: {e}")
            return {}

    def _search_semantic_logic(self, value: str) -> List[Dict[str, Any]]:
        """
        在 semantic_logic_dict Collection 中向量搜索（对应 search_by_metric_name）。
        返回: [{"metric_name", "logic_dsl", "metric_desc", "table_name", "similarity_score"}]
        相似度低于 SEMANTIC_LOGIC_MIN_SCORE（默认 0.80）的结果被过滤。
        """
        if not value or not value.strip():
            return []
        try:
            vec = self._vectorize(value)
            results = self._milvus.search(
                collection_name=self._sl_collection,
                data=[vec],
                anns_field="metric_vector",
                search_params={"metric_type": "COSINE", "params": {"nprobe": 512}},
                limit=1,
                output_fields=["id", "metric_name", "logic_dsl", "metric_desc", "table_name"],
            )
            hits = []
            for batch in results:
                for hit in batch:
                    score = hit.get("distance", 0.0)
                    if score < self._min_logic_score:
                        continue
                    entity = hit.get("entity", {})
                    hits.append({
                        "metric_name":      entity.get("metric_name", ""),
                        "logic_dsl":        entity.get("logic_dsl", ""),
                        "metric_desc":      entity.get("metric_desc", ""),
                        "table_name":       entity.get("table_name", ""),
                        "similarity_score": score,
                    })
            return hits
        except Exception as e:
            logger.warning(f"[SemanticConceptExtractor] semantic_logic_dict 搜索失败 (value={value}): {e}")
            return []

    @staticmethod
    def _is_similar_value(v1: str, v2: str) -> bool:
        """
        简单相似判断：完全相同 or 一方包含另一方（用于 L1/L2 合并去重）。
        对应 intent_recognition.is_similar_value 的核心逻辑。
        """
        if not v1 or not v2:
            return False
        v1n, v2n = v1.strip(), v2.strip()
        return v1n == v2n or v1n in v2n or v2n in v1n

    def _enrich_metric(
            self,
            metric: Dict[str, Any],
            require_match: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """
        用 semantic_logic_dict 向量搜索增强单条维度记录（对应 enrich_metric_by_semantic_search）。

        - 若 require_match=True  且 搜索无命中 → 返回 None（用于 L1 概念，不确定时放弃）
        - 若 require_match=False 且 搜索无命中 → 返回原始 metric（用于 L2 规则提取结果）
        - 命中时补充 logic_dsl / table_name / metric_desc
        """
        value = metric.get("value", "")
        if not value:
            return None if require_match else metric

        hits = self._search_semantic_logic(value)
        if not hits:
            return None if require_match else metric

        best = hits[0]
        enriched = metric.copy()
        if best.get("logic_dsl"):
            enriched["logic_dsl"] = best["logic_dsl"]
        if best.get("table_name"):
            enriched["table_name"] = best["table_name"]
        if best.get("metric_desc"):
            enriched["metric_desc"] = best["metric_desc"]
        logger.info(
            f"[SemanticEnrich] value='{value}' → logic_dsl='{best.get('logic_dsl', '')[:60]}' "
            f"(score={best['similarity_score']:.3f})"
        )
        return enriched

    # ──────────────────────────────────────────────────────────────────
    # Protocol 接口实现
    # ──────────────────────────────────────────────────────────────────

    def extract_and_recall_async(self, user_input: str, current_date: str) -> Any:
        """
        异步执行 L1 语义概念抽取（对应 extract_semantic_concepts_with_vector_recall_async）。

        在独立线程中调用 Gemini，以 system_prompt_semantic_logic_enrich 为系统提示词，
        将 current_date 替换入提示词中的 {current_date} 占位符。

        返回 concurrent.futures.Future，通过 .result(timeout=30) 获取：
            {"l1_concepts": {
                "time_semantics": {...},
                "concepts": [...],
                "analysis_intent": [...],
                "structure_signals": {...}
            }}
        """
        system_prompt = self._L1_SYSTEM_PROMPT.replace("{current_date}", current_date or "")

        def _extract() -> Dict[str, Any]:
            logger.info(f"[L1 抽取] 开始异步抽取语义概念, user_input='{user_input[:50]}'")
            result = self._call_gemini_with_system_prompt(user_input, system_prompt)
            if not result:
                logger.warning("[L1 抽取] Gemini 返回空结果")
                return {"l1_concepts": {}}
            logger.info(f"[L1 抽取] 完成, concepts={len(result.get('concepts', []))}")
            return {"l1_concepts": result}

        return self._executor.submit(_extract)

    def merge_candidates(
            self,
            l2_metrics: List[Dict],
            l1_concepts: List[Dict],
            user_input: str,
    ) -> Dict[str, Any]:
        """
        L1/L2 候选融合 + semantic_logic_dict 向量增强
        （对应 merge_candidates_for_sql_generation + merge_and_enrich_metrics）。

        流程：
          1. 处理 L1 concepts（require_match=True）：
             - 将每个 concept.text 作为 value，concept.type 作为 metric_name
             - 向量搜索 semantic_logic_dict，命中则加入 final_metrics 并打标 logic_dsl
             - 去重（与已处理 value 相似的跳过）
          2. 处理 L2 metrics（require_match=False）：
             - 跳过与 L1 重复的 value
             - 向量搜索 semantic_logic_dict，命中则补充字段，未命中则保留原始
          3. 生成候选 SQL-R（使用最终合并后的 metrics）

        返回：
            {
                "candidates": [
                    {
                        "candidate_id": "SQL-R",
                        "candidate_desc": "L1/L2 合并增强候选",
                        "metric_list": [...]
                    }
                ],
                "l1_vector_candidates": {concept_text: [hit, ...], ...}
            }
        """
        logger.info(
            f"[候选融合] L2 metrics={len(l2_metrics)}, L1 concepts={len(l1_concepts)}, "
            f"user='{user_input[:40]}'"
        )

        final_metrics: List[Dict[str, Any]] = []
        processed_values: List[str] = []
        l1_vector_candidates: Dict[str, Any] = {}

        # ── Step 1: 优先处理 L1 concepts（高优先级，require_match=True）──
        for concept in l1_concepts:
            concept_text = concept.get("text", "").strip()
            if not concept_text:
                continue

            # 去重
            if any(self._is_similar_value(concept_text, v) for v in processed_values):
                logger.debug(f"[候选融合] L1 跳过重复 concept: '{concept_text}'")
                continue

            # 构造 metric 格式（用于 _enrich_metric）
            pseudo_metric: Dict[str, Any] = {
                "metric_name": concept.get("type", ""),
                "metric_code": "",
                "value":       concept_text,
                "confidence":  concept.get("confidence", 0.0),
            }
            enriched = self._enrich_metric(pseudo_metric, require_match=True)
            if enriched is None:
                logger.debug(f"[候选融合] L1 concept '{concept_text}' 在 semantic_logic_dict 中无命中，跳过")
                continue

            final_metrics.append(enriched)
            processed_values.append(concept_text)

            # 记录向量候选（供调试 / 上层使用）
            hits = self._search_semantic_logic(concept_text)
            if hits:
                l1_vector_candidates[concept_text] = [
                    {
                        "metric_name":   h["metric_name"],
                        "logic_dsl":     h.get("logic_dsl", ""),
                        "vector_score":  h["similarity_score"],
                    }
                    for h in hits
                ]

        # ── Step 2: 处理 L2 metrics（require_match=False，与 L1 去重）──
        for metric in l2_metrics:
            value = metric.get("value", "").strip()

            # 跳过与 L1 已处理 value 重复的项
            if value and any(self._is_similar_value(value, v) for v in processed_values):
                logger.debug(f"[候选融合] L2 跳过重复 value: '{value}'（已由 L1 覆盖）")
                continue

            enriched = self._enrich_metric(metric, require_match=False)
            if enriched is not None:
                final_metrics.append(enriched)
                if value:
                    processed_values.append(value)

        # ── Step 3: 若 L1/L2 合并结果为空，降级使用原始 L2 ──
        if not final_metrics and l2_metrics:
            logger.warning("[候选融合] 合并结果为空，降级使用原始 L2 metrics")
            final_metrics = list(l2_metrics)

        candidate_r = {
            "candidate_id":   "SQL-R",
            "candidate_desc": "L1/L2 合并增强候选（semantic_logic_dict 向量增强）",
            "metric_list":    final_metrics,
        }
        logger.info(f"[候选融合] 最终 metric 数量: {len(final_metrics)}")

        return {
            "candidates":          [candidate_r],
            "l1_vector_candidates": l1_vector_candidates,
        }


# ═══════════════════════════════════════════════════════════════════
# 7.  流水线工作目录 & main 入口（可独立运行）
# ═══════════════════════════════════════════════════════════════════

def _get_workflow_dir() -> "Path":  # type: ignore[name-defined]
    """
    返回技能流水线共享工作目录：<skills根>/.workflow/
    目录不存在时自动创建。

    目录结构：
        skills/
          .workflow/              ← 所有 *_output.json 存放于此
          rewrite-question/
          recognize-intent/       ← 本文件所在位置
          mult-call/
          sql-generator/
          sql-audit/

    约定：
        rewrite_question.py  写入  rewrite_output.json
        recognize_intent.py  读取  rewrite_output.json，写入  intent_output.json
        multi_call.py        读取  intent_output.json，写入  multicall_output.json
        sql_generator.py     读取  multicall_output.json，写入 sql_output.json
        sql_audit.py         读取  sql_output.json，写入   audit_output.json

    多次运行：
        每次写入前自动将旧文件备份为 <name>.bak.json（只保留一份）。
        使用 --clean 参数可强制删除当前步骤及后续所有 *_output.json，
        避免流水线混入过期数据。
    """
    from pathlib import Path
    skills_root = Path(__file__).resolve().parent.parent   # skills/
    wf_dir = skills_root / ".workflow"
    wf_dir.mkdir(parents=True, exist_ok=True)
    return wf_dir


def _backup_if_exists(path: "Path") -> None:  # type: ignore[name-defined]
    """将 path 文件备份为 .bak.json，覆盖旧备份"""
    from pathlib import Path
    p = Path(path)
    if p.exists():
        bak = p.with_suffix("").with_suffix("") if p.suffix == ".json" else p
        bak = p.parent / (p.stem + ".bak.json")
        p.replace(bak)
        logger.debug(f"已备份: {p.name} → {bak.name}")


async def main() -> None:
    """
    独立运行入口

    读取上一步 rewrite_output.json 中的 final_query，执行意图识别。

    用法（从任意目录均可运行，输入/输出统一放在 skills/.workflow/ 下）:
        python recognize_intent.py
        python recognize_intent.py --input /path/to/rewrite_output.json
        python recognize_intent.py --output /path/to/intent_output.json
        python recognize_intent.py --clean          # 清除本步及后续输出文件再运行

    输出文件 (intent_output.json) 供下一步 multi_call.py 读取。
    """
    import argparse, os
    from pathlib import Path

    wf = _get_workflow_dir()
    default_input  = str(wf / "rewrite_output.json")
    default_output = str(wf / "intent_output.json")

    parser = argparse.ArgumentParser(description="意图识别技能 — 独立运行")
    parser.add_argument("--input",  default=default_input,  help=f"上一步输出文件 (默认: {default_input})")
    parser.add_argument("--output", default=default_output, help=f"本步输出文件 (默认: {default_output})")
    parser.add_argument("--clean",  action="store_true",    help="运行前删除本步及后续输出文件（防止旧数据污染）")
    args = parser.parse_args()

    # ── 可选：清理本步及后续输出（多次调试时避免混入旧数据）──
    if args.clean:
        for name in ("intent_output.json", "multicall_output.json",
                     "sql_output.json", "audit_output.json"):
            stale = wf / name
            if stale.exists():
                stale.unlink()
                print(f"[清理] 已删除: {stale}")

    # 1. 加载环境变量
    _load_dotenv()

    # 2. 读取上一步输出，获取 final_query
    if not os.path.exists(args.input):
        print(f"[错误] 找不到输入文件 {args.input}")
        print(f"       请先运行 rewrite_question.py，输出会保存到 {default_input}")
        return

    with open(args.input, encoding="utf-8") as f:
        prev = json.load(f)

    query = prev.get("final_query") or prev.get("original_query", "")

    # ── QA 快捷路径：上一步已命中 QA 对，直接透传 SQL ──
    if prev.get("is_qa_matched") and prev.get("matched_sql"):
        print("[跳过] 上一步已命中 QA 对，直接透传 SQL，跳过意图识别")
        result = {
            "intent":           "handle_data_query",
            "success":          True,
            "is_qa_shortcut":   True,
            "matched_sql":      prev["matched_sql"],
            "final_query":      query,
            "indicator_metric": [],
        }
        _backup_if_exists(args.output)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[输出] 已保存到: {args.output}")
        return

    if not query:
        print("[错误] 输入文件中缺少 final_query 字段")
        return

    # 3. 获取 Gemini 配置
    cfg = _get_gemini_config()
    if not cfg["api_key"]:
        print("[错误] GEMINI_API_KEY 未配置，请检查 .env 文件")
        return

    # 4. 构建真实服务（依赖 .env 中的配置）
    try:
        indicator_searcher   = _RealIndicatorSearcher()
        metric_config_loader = _RealMetricConfigLoader()
    except Exception as e:
        print(f"[错误] 核心服务初始化失败: {e}")
        return

    # dict_value_replacer：连接 Milvus sys_dict，失败时降级为 None（跳过值替换，不影响主流程）
    dict_value_replacer = None
    try:
        dict_value_replacer = _RealDictValueReplacer()
        print("[服务] 字典值替换服务 (sys_dict) 初始化成功")
    except Exception as e:
        print(f"[警告] 字典值替换服务初始化失败，跳过值替换: {e}")

    # semantic_extractor：连接 Milvus semantic_logic_dict + Gemini L1 抽取
    #   - 命中时为维度补充 logic_dsl / table_name，提升 SQL 生成准确率
    #   - 失败时降级为 None（L2 槽位结果直接使用，不影响主流程）
    semantic_extractor = None
    try:
        semantic_extractor = _RealSemanticConceptExtractor(
            gemini_api_url=cfg["api_url"],
            gemini_api_key=cfg["api_key"],
            gemini_token=cfg["token"],
        )
        print("[服务] L1 语义概念抽取服务 (semantic_logic_dict) 初始化成功")
    except Exception as e:
        print(f"[警告] L1 语义概念抽取服务初始化失败，将跳过 L1/L2 融合: {e}")

    # 5. 执行意图识别
    skill = RecognizeIntentSkill(
        gemini_api_url=cfg["api_url"],
        gemini_api_key=cfg["api_key"],
        gemini_token=cfg["token"],
        indicator_searcher=indicator_searcher,
        metric_config_loader=metric_config_loader,
        dict_value_replacer=dict_value_replacer,    # None 时跳过字典替换
        semantic_extractor=semantic_extractor,      # None 时跳过 L1/L2 候选融合
    )

    print(f"\n[运行] 意图识别: '{query}'")
    output = await skill.run(IntentInput(query=query))

    # 6. 整理并保存输出
    result: Dict[str, Any] = {
        "intent":                  output.intent,
        "success":                 output.success,
        "message":                 output.message,
        "final_query":             query,
        "is_qa_shortcut":          False,
        "matched_sql":             None,
        "indicator_metric":        output.indicator_metric,
        "l1_concepts":             output.l1_concepts,
        "vector_candidates":       output.vector_candidates,
        "indicator_metric_groups": output.indicator_metric_groups,
        "mode":                    output.mode,
        "result_data":             output.result_data,
    }

    _backup_if_exists(args.output)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 7. 打印摘要
    print(f"\n{'='*60}")
    print(f"问题    : {query}")
    print(f"意图    : {output.intent}")
    print(f"成功    : {output.success}")
    if not output.success:
        print(f"消息    : {output.message}")
    elif output.indicator_metric:
        im = output.indicator_metric[0]
        print(f"指标    : {im.get('indicator_name')} ({im.get('indicator_code')})")
        print(f"维度数  : {len(im.get('metric_info', []))}")
    print(f"{'='*60}")
    print(f"[输出] 已保存到: {args.output}")
    print(f"[下一步] python ../mult-call/multi_call.py   (读取 {args.output})")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    asyncio.run(main())
