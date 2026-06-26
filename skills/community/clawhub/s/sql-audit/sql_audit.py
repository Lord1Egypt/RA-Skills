"""
SQL 审核技能 (Skill: SQL Audit)
原始来源: app/ai_chat_agents/sql_audit_agent.py  (SqlAuditService + SqlAuditAgent.handle_message)

完整还原 handle_message 的核心审核/执行/兜底逻辑，去除：
  - autogen @message_handler / TopicId / publish_message / send_response
  - qa_record_service / agent_history_service 等持久化调用
  - _send_to_visualization_recommender（由调用方自行处理结果）
  - AssistantAgent (autogen) → 改为 llm_caller 注入

入参: SQLAuditInput
出参: SQLAuditOutput
"""

import copy
import json
import logging
import re
import time
import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, runtime_checkable

import httpx

logger = logging.getLogger(__name__)

MAX_RETRIES = 3


# ═══════════════════════════════════════════════════════════════════
# 0.  可注入的外部服务接口（Protocol）
#
#     DatabaseRunner — 执行 SQL 并返回结果集。
#       原始实现: SqlAuditService._sql_execution_tool 内部调用
#                 self.db_access.run_sql(cleaned_sql)（同步）
#                 返回 DataFrame，取前50条转为 List[Dict]。
#       这是真实的数据库连接，无法内嵌实现，必须注入。
# ═══════════════════════════════════════════════════════════════════

@runtime_checkable
class DatabaseRunner(Protocol):
    """
    SQL 执行服务接口（对应原 SqlAuditService.db_access.run_sql）
    调用方需实现此接口以连接真实数据库（StarRocks / MySQL / 等）
    """
    def run_sql(self, sql: str) -> Optional[List[Dict[str, Any]]]:
        """
        执行 SQL，返回 List[Dict]（每行一个 dict）；
        无数据返回 [] 或 None；执行失败抛出异常。
        """
        ...


# ─────────────────────────────────────────────
# 1. 数据类：入参 / 出参
# ─────────────────────────────────────────────

@dataclass
class SQLAuditInput:
    """SQL 审核的最小化入参（对应原 AiChatSqlMessage）"""
    query: str
    sql: Optional[str]                                      # 单 SQL（与 sql_candidates 二选一）
    sql_candidates: Optional[List[Dict[str, Any]]]          # 多候选（含 sql / context / index）
    indicator_metric: Any                                   # List[Dict] 或 List[List[Dict]]
    vector_candidates: Dict[str, Any] = field(default_factory=dict)
    retry_count: int = 0
    connection_id: int = 0
    memory_id: str = ""


@dataclass
class SQLAuditOutput:
    """SQL 审核的出参"""
    success: bool
    sql: Optional[str]
    data: List[Dict[str, Any]] = field(default_factory=list)
    row_count: int = 0
    error_msg: str = ""
    # 当 row_count==0 且可生成兜底时，更新后的 indicator_metrics（用于下一轮 SQL 生成）
    new_indicator_metrics: Optional[List[Any]] = None
    # 需要重试时为 True（调用方根据此字段决定是否重新调用 SQL 生成器）
    need_retry: bool = False
    retry_count: int = 0


# ─────────────────────────────────────────────
# 2. 核心业务类
# ─────────────────────────────────────────────

class SQLAuditSkill:
    """
    SQL 审核技能

    完整还原 SqlAuditAgent.handle_message 逻辑：

      Step 1: 处理多候选 sql_candidates
              - 逐个执行，取第一个 row_count > 0 的候选
              - 若全都无数据，取第一个候选

      Step 2: 单 SQL 直接执行

      Step 3: row_count == 0 时触发兜底（Level 2 候选生成）
              - 从 vector_candidates 取前 4 个向量候选
              - LLM 生成 2 个简化候选（去维度 / 扩时间范围）
              - 将 new_indicator_metrics 返回给调用方，触发重试 SQL 生成

      Step 4: exec_flag=True  → 返回成功结果
              exec_flag=False → retry_count < MAX_RETRIES → 返回需重试标志
                              → retry_count >= MAX_RETRIES → 返回最终失败

    外部依赖：
      db_service:    DatabaseRunner 接口实现（必须注入，真实数据库连接）
      LLM 调用:     Gemini REST（直接内嵌，参数通过构造器传入）
    """

    def __init__(
            self,
            db_service: DatabaseRunner,
            gemini_api_url: str = "",
            gemini_api_key: str = "",
            gemini_token: str = "",
            llm_timeout: float = 120.0,
    ):
        """
        Args:
            db_service:      DatabaseRunner 实现，用于执行 SQL（必须注入）。
            gemini_api_url:  Gemini REST API 地址（用于生成简化候选）。
            gemini_api_key:  x-goog-api-key。
            gemini_token:    自定义鉴权 token。
            llm_timeout:     HTTP 超时秒数。
        """
        self.db_service  = db_service
        self.api_url     = gemini_api_url
        self.api_key     = gemini_api_key
        self.token       = gemini_token
        self.llm_timeout = llm_timeout

    # ──────────────────────────────────────────────────────────────────
    # 对外唯一入口
    # ──────────────────────────────────────────────────────────────────

    async def run(self, inp: SQLAuditInput) -> SQLAuditOutput:
        """
        执行 SQL 审核（完整还原 handle_message 的三步核心逻辑）
        """
        query          = inp.query
        sql            = inp.sql
        sql_candidates = inp.sql_candidates
        retry_count    = inp.retry_count
        indicator_metric = inp.indicator_metric

        context_update: Dict[str, Any] = {}   # 记录 context 变更（for 兜底候选更新）

        # ── Step 1: 多候选处理（原 if sql_candidates 分支）─────────────
        if sql_candidates:
            logger.info(f"处理 {len(sql_candidates)} 个 SQL 候选方案")
            execution_result, winning = self._pick_best_candidate(sql_candidates)
            if winning:
                sql            = winning.get("sql")
                context_update = winning.get("context", {})
                # 更新 indicator_metric（使用获奖候选的 context）
                if context_update and isinstance(context_update, dict):
                    indicator_metric = context_update.get("indicator_metric", indicator_metric)
            else:
                sql            = sql_candidates[0].get("sql")
                context_update = sql_candidates[0].get("context", {})
                execution_result = self._sql_execution_tool(sql)

        else:
            # ── Step 2: 单 SQL 执行（原 else 分支）────────────────────
            execution_result = self._sql_execution_tool(sql)

        exec_flag = execution_result.get("success", False)
        data      = execution_result.get("data", [])
        row_count = execution_result.get("row_count", 0)
        error_msg = execution_result.get("error", "")

        # ── Step 3: row_count==0 时触发兜底（原 if row_count == 0 分支）
        new_indicator_metrics: Optional[List[Any]] = None
        if row_count == 0:
            max_retries_here = 1   # 兜底只允许再重试一次（原代码逻辑）
            exec_flag = False

            is_multi_version = self._is_multi_version(indicator_metric)

            if is_multi_version:
                error_msg = "抱歉，经过所有候选组合尝试，仍未能查询到相关数据。请尝试调整查询条件。"
            else:
                new_candidates = await self._build_fallback_candidates(
                    query=query,
                    indicator_metric=indicator_metric,
                    vector_candidates=inp.vector_candidates,
                )
                if new_candidates:
                    new_indicator_metrics = new_candidates
                    error_msg = f"查询无结果，已自动准备 {len(new_candidates)} 个推荐方案进行匹配..."
                else:
                    error_msg = "查询无结果，且无法提供推荐方案。"
        else:
            max_retries_here = MAX_RETRIES

        # ── Step 4: 路由结果──────────────────────────────────────────
        if exec_flag:
            return SQLAuditOutput(
                success=True,
                sql=sql,
                data=data,
                row_count=row_count,
            )

        # 需要重试
        if retry_count < max_retries_here:
            return SQLAuditOutput(
                success=False,
                sql=sql,
                error_msg=error_msg,
                need_retry=True,
                retry_count=retry_count + 1,
                new_indicator_metrics=new_indicator_metrics,
            )

        # 超过最大重试次数
        return SQLAuditOutput(
            success=False,
            sql=sql,
            data=data or [],
            error_msg=error_msg,
            need_retry=False,
            retry_count=retry_count,
        )

    # ──────────────────────────────────────────────────────────────────
    # 私有方法（与原 SqlAuditService / SqlAuditAgent 方法 1:1 对应）
    # ──────────────────────────────────────────────────────────────────

    def _pick_best_candidate(
            self, sql_candidates: List[Dict[str, Any]]
    ) -> Tuple[Dict[str, Any], Optional[Dict[str, Any]]]:
        """
        逐个执行候选 SQL，返回第一个 row_count > 0 的结果（原多候选循环逻辑）

        Returns: (execution_result, winning_candidate)
        """
        for candidate in sql_candidates:
            cand_sql = candidate.get("sql")
            result   = self._sql_execution_tool(cand_sql)
            if result.get("success") and result.get("row_count", 0) > 0:
                return result, candidate
        return self._sql_execution_tool(sql_candidates[0].get("sql")), None

    def _sql_execution_tool(self, sql: Optional[str]) -> Dict[str, Any]:
        """
        执行 SQL 并返回标准化结果字典（原 _sql_execution_tool）

        原始实现通过 self.db_access.run_sql(cleaned_sql)（同步）获取 DataFrame，
        取前50条，转 List[Dict]，并可选地按第一个数值字段倒序排序。
        此处通过 DatabaseRunner 接口调用。

        返回格式: {success, data, row_count, message} 或 {success, error}
        """
        if not sql:
            return {"success": False, "error": "SQL 为空"}

        cleaned_sql = self._clean_sql(sql)
        try:
            rows = self.db_service.run_sql(cleaned_sql)

            if not rows:
                return {
                    "success": True,
                    "data": [],
                    "row_count": 0,
                    "message": "查询执行成功，但没有返回任何结果",
                }

            data = rows[:50]   # 取前 50 条（原代码逻辑）

            # 若 SQL 不含全局 ORDER BY，则按第一个数值字段倒序排序
            sql_upper = cleaned_sql.strip().rstrip(";").upper()
            if not self.is_globally_sorted(sql_upper):
                data = self._sort_by_first_numeric(data)

            return {
                "success": True,
                "data": data,
                "row_count": len(data),
                "message": f"查询执行成功，返回 {len(data)} 条结果",
            }

        except Exception as e:
            return {"success": False, "error": f"SQL执行错误: {str(e)}"}

    def is_globally_sorted(self, sql: str) -> bool:
        """
        判断 SQL 中最后一个 ORDER BY 是否在最外层（非子查询内）（原 is_globally_sorted）
        """
        clean_sql = sql.strip().rstrip(";").upper()
        last_order_pos = clean_sql.rfind("ORDER BY")
        if last_order_pos == -1:
            return False

        suffix  = clean_sql[last_order_pos:]
        balance = 0
        for char in suffix:
            if char == "(":
                balance += 1
            elif char == ")":
                balance -= 1
            if balance < 0:
                return False
        return True

    @staticmethod
    def _sort_by_first_numeric(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """按第一个数值字段倒序排序（原代码逻辑）"""
        if not data:
            return data
        first_numeric = next(
            (k for k, v in data[0].items() if isinstance(v, (int, float)) and v is not None),
            None,
        )
        if not first_numeric:
            return data
        try:
            return sorted(
                data,
                key=lambda x: float(x.get(first_numeric, float("-inf")) or float("-inf")),
                reverse=True,
            )
        except (TypeError, ValueError):
            return data

    @staticmethod
    def _is_multi_version(indicator_metric: Any) -> bool:
        """判断是否已经是多候选版本（原 is_multi_version 判断逻辑）"""
        if not isinstance(indicator_metric, list) or len(indicator_metric) == 0:
            return False
        return len(indicator_metric) > 1 or isinstance(indicator_metric[0], list)

    async def _build_fallback_candidates(
            self,
            query: str,
            indicator_metric: Any,
            vector_candidates: Dict[str, Any],
    ) -> List[List[Dict[str, Any]]]:
        """
        构建兜底候选列表（原 row_count==0 分支逻辑）：

        1. 从 vector_candidates 取前 4 个向量候选
        2. 通过 LLM 简化生成 2 个候选（去维度 / 扩时间范围）

        Returns: List[List[Dict]]，每项为一个完整的 indicator_metric 变体
        """
        initial_variant = indicator_metric if isinstance(indicator_metric, list) else [indicator_metric]
        new_list: List[List[Dict[str, Any]]] = []

        # ① 向量候选（最多 4 个）
        if vector_candidates:
            try:
                first_concept    = next(iter(vector_candidates))
                candidates_data  = vector_candidates[first_concept]
                for i in range(min(4, len(candidates_data))):
                    cand         = candidates_data[i]
                    cand_value   = cand.get("value")
                    logic_dsl    = cand.get("logic_dsl")
                    metric_desc  = cand.get("metric_desc")

                    im_copy = copy.deepcopy(initial_variant)
                    for im_dict in im_copy:
                        for mi in im_dict.get("metric_info", []):
                            if mi.get("metric_code") == first_concept or \
                                    mi.get("metric_name") == first_concept:
                                mi["value"] = cand_value
                                if metric_desc:
                                    mi["metric_desc"] = metric_desc
                                if logic_dsl:
                                    mi["logic_dsl"] = logic_dsl
                    new_list.append(im_copy)
            except Exception as e:
                logger.error(f"构建向量候选失败: {e}")

        # ② Gemini REST 简化候选（最多 2 个）
        if self.api_url and self.api_key:
            try:
                simplified = await self._simplify_indicator_metric_via_llm(
                    query, initial_variant, count=2
                )
                new_list.extend(simplified)
            except Exception as e:
                logger.error(f"构建 LLM 简化候选失败: {e}")

        return new_list

    async def _simplify_indicator_metric_via_llm(
            self,
            query: str,
            indicator_metric: List[Dict[str, Any]],
            count: int = 2,
    ) -> List[List[Dict[str, Any]]]:
        """
        通过 LLM 生成简化候选（原 _simplify_indicator_metric_via_llm）

        策略：
          版本1 — 删除一个非核心维度（metric_info 减少 1 个）
          版本2 — 扩大时间范围（若有 year_month_day 字段）或再删除一个不同维度
        """
        original_metric_info_count = 0
        time_metric_info = None
        if indicator_metric and len(indicator_metric) > 0:
            metric_info = indicator_metric[0].get("metric_info", [])
            original_metric_info_count = len(metric_info)
            for mi in metric_info:
                if mi.get("metric_code") == "year_month_day":
                    time_metric_info = mi
                    break

        indicator_json = json.dumps(indicator_metric, ensure_ascii=False, indent=2)
        time_note = ""
        if time_metric_info:
            original_time = time_metric_info.get("value", "")
            time_note = f"""
**重要：第二个版本的特殊处理**
- 原始时间范围：{original_time}
- 版本2 应扩大时间范围，维度数量保持 {original_metric_info_count}（不删除维度）
"""

        prompt = f"""你是一个数据分析专家。当前查询维度配置导致数据库返回结果为空。
生成 **{count} 个不同的简化版本**，扩大查询范围。

【用户问题】
{query}

【原始配置】
{indicator_json}

【关键要求】
1. 原始 metric_info 有 {original_metric_info_count} 个维度
2. 版本1：删除一个非核心维度，维度数量变为 {original_metric_info_count - 1}
3. 版本2：{'扩大时间范围（维度数量保持）' if time_metric_info else '删除一个不同的非核心维度'}
{time_note}
【执行要求】
- 保持 JSON 结构完全一致
- 返回包含 {count} 个 indicator_metric 数组的 JSON 数组
- 格式: [indicator_metric1, indicator_metric2]
- 严禁任何解释或 Markdown 标记，只输出纯 JSON
"""
        try:
            raw = await self._call_gemini_rest(prompt)
            json_str = self._extract_json_block(raw)
            if not json_str:
                return self._generate_fallback_versions(indicator_metric, count, time_metric_info, original_metric_info_count)

            parsed = json.loads(json_str)
            return self._validate_simplified_versions(parsed, count, indicator_metric, original_metric_info_count, time_metric_info)

        except Exception as e:
            logger.error(f"LLM 简化候选失败: {e}")
            return self._generate_fallback_versions(indicator_metric, count, time_metric_info, original_metric_info_count)

    def _validate_simplified_versions(
            self,
            parsed: Any,
            count: int,
            original: List[Dict],
            original_count: int,
            time_metric_info: Optional[Dict],
    ) -> List[List[Dict[str, Any]]]:
        """验证并规范化 LLM 返回的简化候选（原验证逻辑）"""
        results: List[List[Dict]] = []
        if not isinstance(parsed, list):
            return self._generate_fallback_versions(original, count, time_metric_info, original_count)

        def get_inner(item):
            if isinstance(item, dict):
                return [item]
            if isinstance(item, list) and item:
                if isinstance(item[0], dict):
                    return item
                if isinstance(item[0], list):
                    return get_inner(item[0])
            return item if isinstance(item, list) else []

        for idx, item in enumerate(parsed[:count]):
            inner = get_inner(item)
            if not inner or not isinstance(inner[0], dict):
                continue
            first_im   = inner[0]
            mi_list    = first_im.get("metric_info", [])
            mi_count   = len(mi_list)

            if idx == 0:  # 版本1：必须删除一个维度
                if mi_count < original_count:
                    results.append(inner)
                else:
                    # LLM 未删减，手动删除最后一个
                    fallback = copy.deepcopy(inner)
                    if fallback[0].get("metric_info"):
                        fallback[0]["metric_info"].pop()
                    results.append(fallback)
            else:        # 版本2：扩时间 or 删维度
                if time_metric_info:
                    # 验证时间字段是否扩大（不严格检验，信任 LLM）
                    results.append(inner)
                else:
                    if mi_count < original_count:
                        results.append(inner)
                    else:
                        fallback = copy.deepcopy(inner)
                        # 删除与版本1不同的字段（若可确定）
                        if len(fallback[0].get("metric_info", [])) > 0:
                            fallback[0]["metric_info"].pop(0)
                        results.append(fallback)

        if not results:
            return self._generate_fallback_versions(original, count, time_metric_info, original_count)
        return results

    @staticmethod
    def _generate_fallback_versions(
            indicator_metric: List[Dict],
            count: int,
            time_metric_info: Optional[Dict],
            original_count: int,
    ) -> List[List[Dict]]:
        """
        当 LLM 失败时的纯代码兜底版本生成（原 _generate_fallback_versions）

        版本1: 删除最后一个 metric_info 项
        版本2: 若有时间字段则扩时间范围（+3年），否则删除倒数第二个
        """
        results: List[List[Dict]] = []
        if not indicator_metric:
            return results

        # 版本1: 删除最后一个维度
        v1 = copy.deepcopy(indicator_metric)
        if v1[0].get("metric_info"):
            v1[0]["metric_info"].pop()
        results.append(v1)

        if count >= 2:
            v2 = copy.deepcopy(indicator_metric)
            if time_metric_info:
                # 扩大时间范围
                for im in v2:
                    for mi in im.get("metric_info", []):
                        if mi.get("metric_code") == "year_month_day":
                            val = mi.get("value", "")
                            if " to " in val:
                                parts = val.split(" to ")
                                try:
                                    from datetime import datetime, timedelta
                                    start = datetime.strptime(parts[0].strip(), "%Y-%m-%d")
                                    end   = datetime.strptime(parts[1].strip(), "%Y-%m-%d")
                                    new_start = start.replace(year=start.year - 3)
                                    mi["value"] = f"{new_start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}"
                                except Exception:
                                    pass
            else:
                if len(v2[0].get("metric_info", [])) > 1:
                    v2[0]["metric_info"].pop(0)
            results.append(v2)

        return results

    @staticmethod
    def _extract_json_block(text: str) -> Optional[str]:
        """从 LLM 输出中提取 JSON 字符串（原 _extract_json_block）"""
        if not text:
            return None
        # 优先提取 ```json ... ``` 代码块
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if match:
            return match.group(1).strip()
        # 其次提取 [ ... ] 或 { ... }
        for pattern in [r"\[[\s\S]*\]", r"\{[\s\S]*\}"]:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        return None

    async def _call_gemini_rest(self, prompt: str) -> str:
        """
        调用 Gemini REST API（同步包装为异步，与原 call_gemini_rest_sync 逻辑一致）
        用于 _simplify_indicator_metric_via_llm 中的 LLM 简化候选生成。
        """
        if not self.api_url or not self.api_key:
            raise RuntimeError("Gemini REST 参数未配置（api_url / api_key 为空）")

        headers = {
            "x-goog-api-key": self.api_key,
            "token":           self.token,
            "Content-Type":    "application/json",
            "Accept":          "*/*",
        }
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"thinkingConfig": {"thinkingLevel": "low"}},
        }

        def _sync_call() -> str:
            start = time.time()
            with httpx.Client(timeout=self.llm_timeout) as client:
                resp = client.post(self.api_url, json=payload, headers=headers)
                resp.raise_for_status()
                result = resp.json()
                duration = time.time() - start
                content = ""
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        content = parts[0]["text"]
                logger.info(f"Gemini REST（审核兜底）调用成功，耗时 {duration:.2f}s")
                return content

        return await asyncio.to_thread(_sync_call)

    @staticmethod
    def _clean_sql(sql: str) -> str:
        return sql.replace("```sql", "").replace("```", "").strip()


# ═══════════════════════════════════════════════════════════════════
# 3.  真实服务实现（独立运行时使用）
# ═══════════════════════════════════════════════════════════════════

def _load_dotenv() -> None:
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
        print("[警告] pip install python-dotenv")


def _get_gemini_config() -> Dict[str, str]:
    import os
    base_url = os.environ.get("GEMINI_API_URL", "http://47.77.199.56/api/v1beta").rstrip("/")
    model    = os.environ.get("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
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
        "api_key": os.environ.get("GEMINI_API_KEY", ""),
        "token":   os.environ.get("GEMINI_TOKEN", _default_token),
    }


class _StarRocksRunner:
    """
    真实 StarRocks (Doris) SQL 执行服务
    - 使用 pymysql 连接（StarRocks 兼容 MySQL 协议）
    - 返回 List[Dict]（每行一个字典）
    使用 .env 中的 DB_HOST / DB_PORT / DB_USER / DB_PASSWORD / DB_NAME 配置
    """

    def __init__(self) -> None:
        import os
        self._host     = os.environ.get("DB_HOST", "localhost")
        self._port     = int(os.environ.get("DB_PORT", "9030"))
        self._user     = os.environ.get("DB_USER", "root")
        self._password = os.environ.get("DB_PASSWORD", "")
        self._database = os.environ.get("DB_NAME", "")

    def _get_conn(self):
        import pymysql
        return pymysql.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=30,
            read_timeout=120,
        )

    def run_sql(self, sql: str) -> Optional[List[Dict[str, Any]]]:
        """执行 SQL 并返回 List[Dict]；执行失败则抛出异常"""
        conn   = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return list(rows) if rows else []
        finally:
            cursor.close()
            conn.close()


# ═══════════════════════════════════════════════════════════════════
# 4.  流水线工作目录 & main 入口（可独立运行）
# ═══════════════════════════════════════════════════════════════════

def _get_workflow_dir() -> "Path":  # type: ignore[name-defined]
    """
    返回技能流水线共享工作目录：<skills根>/.workflow/
    目录不存在时自动创建。

    所有 *_output.json 统一存放于此目录，各技能通过约定的文件名衔接：
        rewrite_output.json → intent_output.json → multicall_output.json
        → sql_output.json → audit_output.json
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
        bak = p.parent / (p.stem + ".bak.json")
        p.replace(bak)


async def main() -> None:
    """
    独立运行入口

    读取上一步 sql_output.json，执行 SQL 审核（真实 StarRocks 执行）。
    这是整个链路的最后一步，输出最终查询结果。

    用法（从任意目录均可运行，输入/输出统一在 skills/.workflow/）:
        python sql_audit.py
        python sql_audit.py --input /path/to/sql_output.json
        python sql_audit.py --clean    # 仅清理 audit_output.json（本步为最后一步）
    """
    import argparse, os, json as _json
    from pathlib import Path

    wf = _get_workflow_dir()
    default_input  = str(wf / "sql_output.json")
    default_output = str(wf / "audit_output.json")

    parser = argparse.ArgumentParser(description="SQL 审核技能 — 独立运行")
    parser.add_argument("--input",  default=default_input,  help=f"上一步输出文件 (默认: {default_input})")
    parser.add_argument("--output", default=default_output, help=f"本步输出文件 (默认: {default_output})")
    parser.add_argument("--clean",  action="store_true",    help="运行前删除 audit_output.json")
    args = parser.parse_args()

    if args.clean:
        stale = wf / "audit_output.json"
        if stale.exists():
            stale.unlink()
            print(f"[清理] 已删除: {stale}")

    # 1. 加载环境变量
    _load_dotenv()

    # 2. 读取上一步输出
    if not os.path.exists(args.input):
        print(f"[错误] 找不到输入文件 {args.input}，请先运行 sql_generator.py")
        return

    with open(args.input, encoding="utf-8") as f:
        prev = _json.load(f)

    # 3. 初始化 StarRocks 连接
    try:
        db_service = _StarRocksRunner()
        # 做一次轻量级连接测试
        db_service.run_sql("SELECT 1")
        print(f"[StarRocks] 连接成功: {db_service._host}:{db_service._port}/{db_service._database}")
    except Exception as e:
        print(f"[错误] StarRocks 连接失败: {e}")
        return

    # 4. 获取 Gemini 配置（兜底简化候选需要）
    cfg = _get_gemini_config()

    # 5. 构建 SQLAuditInput
    inp = SQLAuditInput(
        query=prev.get("user_message", ""),
        sql=prev.get("sql"),
        sql_candidates=prev.get("sql_candidates"),
        indicator_metric=prev.get("indicator_metric", []),
        vector_candidates=prev.get("vector_candidates", {}),
        retry_count=prev.get("retry_count", 0),
        memory_id=prev.get("memory_id", ""),
        connection_id=prev.get("connection_id", 0),
    )

    # 6. 执行 SQL 审核（含重试循环，最多 MAX_RETRIES 次）
    skill = SQLAuditSkill(
        db_service=db_service,
        gemini_api_url=cfg["api_url"],
        gemini_api_key=cfg["api_key"],
        gemini_token=cfg["token"],
    )

    print(f"\n[运行] SQL 审核: '{inp.query}'")
    output = await skill.run(inp)

    # 若需要重试但本文件只做单次运行，记录并输出错误信息
    if output.need_retry:
        print(f"[提示] 数据为空，建议重新运行 sql_generator.py 使用简化候选")

    # 7. 整理并保存输出
    result: Dict[str, Any] = {
        "success":     output.success,
        "sql":         output.sql,
        "data":        output.data,
        "row_count":   output.row_count,
        "error_msg":   output.error_msg,
        "need_retry":  output.need_retry,
        "retry_count": output.retry_count,
        "query":       inp.query,
        # new_indicator_metrics 供调用方重试时使用
        "new_indicator_metrics": output.new_indicator_metrics,
    }

    _backup_if_exists(args.output)
    with open(args.output, "w", encoding="utf-8") as f:
        _json.dump(result, f, ensure_ascii=False, indent=2, default=str)

    # 8. 打印摘要
    print(f"\n{'='*60}")
    print(f"问题     : {inp.query}")
    print(f"执行SQL  :\n{output.sql}")
    print(f"{'─'*60}")
    if output.success and output.row_count > 0:
        print(f"结果行数 : {output.row_count}")
        # 打印前 3 行
        for i, row in enumerate(output.data[:3]):
            print(f"  行{i+1}: {row}")
        if output.row_count > 3:
            print(f"  ... 共 {output.row_count} 行")
    elif output.success and output.row_count == 0:
        print(f"结果     : 查询成功，但无数据返回")
        if output.need_retry:
            print(f"提示     : 已准备 {len(output.new_indicator_metrics or [])} 个简化候选方案")
    else:
        print(f"错误     : {output.error_msg}")
    print(f"{'='*60}")
    print(f"[输出] 已保存到: {args.output}")
    print(f"\n✅ 全链路执行完成！")
    print(f"   完整流程: rewrite_question → recognize_intent → multi_call → sql_generator → sql_audit")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    asyncio.run(main())
