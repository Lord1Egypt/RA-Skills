"""
问题重写技能 (Skill: Rewrite Question)
原始来源: app/ai_chat_agents/rewrite_question_agent.py

完整还原 handle_message 的核心逻辑，去除：
  - autogen @message_handler / @capture_agent_context
  - send_response / publish_message 等流式推送
  - agent_history_service / qa_record_service 等持久化调用

入参: RewriteInput
出参: RewriteOutput

独立运行:
    python rewrite_question.py --query "用户的问题"
    输出: rewrite_output.json
"""

import json
import logging
import re
import time
import asyncio
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

import httpx

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# 1. 入参 / 出参 数据类
# ─────────────────────────────────────────────

@dataclass
class HistoryRecord:
    """历史对话记录（对应原 AgentHistorySnapshot ORM 对象的关键字段）"""
    session_id: str
    query: str
    created_at: datetime
    response_data: Optional[Dict[str, Any]] = None   # 含 clarification_type / candidates 等


@dataclass
class QAPair:
    """QA 对（来自 Milvus）"""
    id: str
    question: str
    sql: str


@dataclass
class RewriteInput:
    """问题重写的最小化入参"""
    query: str                                  # 用户原始问题
    history: List[HistoryRecord] = field(default_factory=list)   # 历史对话（最近 3 条）
    qa_pairs: List[QAPair] = field(default_factory=list)         # 所有 QA 对（来自 Milvus）


@dataclass
class RewriteOutput:
    """问题重写的出参"""
    final_query: str            # 送往下一环节的最终问题（重写后 or 原问题）
    is_rewritten: bool          # 是否发生重写
    thought: str = ""           # LLM 推理过程（可用于调试）
    confidence: float = 0.0     # 重写置信度

    # QA 对匹配快速路径 —— 若命中则直接跳过意图识别 / 多路召回 / SQL 生成
    matched_sql: Optional[str] = None          # QA 对中更新时间后的 SQL
    is_qa_matched: bool = False                # 是否命中 QA 对


# ─────────────────────────────────────────────
# 2. 核心业务类
# ─────────────────────────────────────────────

class RewriteQuestionSkill:
    """
    问题重写技能

    完整还原 RewriteQuestionAgent.handle_message 逻辑：
      路径 A — QA 精确匹配  → LLM 更新 SQL 时间 → 直接输出 SQL（跳过后续 Agent）
      路径 B — 无历史记录   → 透传原问题到意图识别
      路径 C — 有历史记录   → LLM 重写 + 置信度过滤（≥0.9 才采纳）
    """

    # ── 与原文件完全一致的 SYSTEM_PROMPT（含 Few-Shot 示例）────────────
    SYSTEM_PROMPT = """# Role

                            你是一个专精于AI问数的"对话上下文重写专家"。你的目标是将用户在多轮对话中的【不完整追问】，重写为【语义完整、独立、可直接用于数据库查询】的自然语言问题，同时严格识别并保留【已具备独立性】的问题，避免过度改写。

                            # Core Logic (核心逻辑)

                            第一步：独立性判定 (Pre-Check)
                               在进行任何重写动作前，首先扫描 Current Query 是否已构成独立查询：

                               判定标准：若 Current Query 同时具备 [时间] + [指标] + [维度/实体]，且不含代词（它、这些、那项），则视为独立问题。

                               处理动作：标记 is_rewritten: false，直接输出原句，严禁继承历史条件。

                            第二步：BI数据继承法则 (仅当不独立时执行)
                               同类覆盖，异类继承：

                               维度切换：新问题仅提维度（如"上海呢？"），替换旧维度，继承旧指标与时间。

                               指标切换：新问题仅提指标（如"毛利呢？"），替换旧指标，继承旧维度与时间。

                               下钻逻辑：若出现"其中"、"里面的"，在原有过滤条件基础上增加新条件。

                              指代消解：将"它"、"该店"、"这些产品"还原为历史中具体的名称。

                              澄清指令处理：若历史末尾是系统给出的【选项列表】，用户回答"第一个"或"按月"，需将其融合为完整指令。

                            # Output Rules
                            1. **严禁过度继承：如果用户已经明确提到了"全国"或"所有门店"，不得将历史中的"华西区"强行塞入。
                            2. **严禁臆造**：绝对不要创造历史记录中不存在的年份或数据值。
                            3. **保持独立**：重写后的句子必须能让不知道上下文的人也能完全听懂。
                            4. **判断无关**：如果Current Query是"你好"、"谢谢"、"太慢了"等非查询类闲聊，标记 `is_rewritten: false`。

                            # Few-Shot Examples

                            ## Case 1: 维度横向切换
                            **History:**
                            - User: 查看2024年华东地区的GMV。
                            - AI: (Result Table...)

                            **Current Query:** 华南的呢？

                            **Output:**
                            ```json
                            {{
                                "thought": "用户提供了新维度值[华南]，属于[地区]维度。需替换原有的[华东]，并继承时间[2024年]和指标[GMV]。",
                                "is_rewritten": true,
                                "rewritten_query": "查看2024年华南地区的GMV",
                                "confidence": 1.0
                            }}
                            ```

                            ## Case 2: 指标切换
                            **History:**
                            - User: 帮我看下上个月棉柔巾销量排名前十的门店。
                            - AI: (Result Chart...)

                            **Current Query:** 也就是看看销售额。

                            **Output:**
                            ```json
                            {{
                                "thought": "用户想看新指标[销售额]，需替换原指标[销量]，继承时间[上个月]、品类[棉柔巾]、维度[门店]及排序逻辑[前十]。",
                                "is_rewritten": true,
                                "rewritten_query": "帮我看下上个月棉柔巾销售额排名前十的门店",
                                "confidence": 0.95
                            }}
                            ```

                            ## Case 3: 时间切换
                            **History:**
                            - User: 2024年全棉时代的订单成交额是多少？
                            - AI: (Result...)

                            **Current Query:** 2025年的呢？

                            **Output:**
                            ```json
                            {{
                                "thought": "用户切换了时间维度[2025年]，需替换[2024年]，继承品牌[全棉时代]和指标[订单成交额]。",
                                "is_rewritten": true,
                                "rewritten_query": "2025年全棉时代的订单成交额是多少",
                                "confidence": 1.0
                            }}
                            ```

                            ## Case 4: 下钻增加条件
                            **History:**
                            - User: 查看2024年所有渠道的销售额。
                            - AI: (Result Table...)

                            **Current Query:** 其中O2O的占比？

                            **Output:**
                            ```json
                            {{
                                "thought": "用户在原有条件基础上，增加了渠道过滤[O2O]，并切换指标为[占比]。",
                                "is_rewritten": true,
                                "rewritten_query": "查看2024年O2O渠道的销售额占比",
                                "confidence": 0.95
                            }}
                            ```

                            ## Case 5: 指代消解
                            **History:**
                            - User: 万象城店的上个月销售额是多少？
                            - AI: (Result...)

                            **Current Query:** 它的利润呢？

                            **Output:**
                            ```json
                            {{
                                "thought": "代词[它]指代[万象城店]，需消解指代并切换指标为[利润]，继承时间[上个月]。",
                                "is_rewritten": true,
                                "rewritten_query": "万象城店的上个月利润是多少",
                                "confidence": 0.95
                            }}
                            ```

                            ## Case 6: 澄清选项处理
                            **History:**
                            - User: 查询XX指标
                            - AI: 已返回以下候选列表供选择：
                              1. 订单成交额 (编码: order_amount)
                              2. 订单数量 (编码: order_count)

                            **Current Query:** 用第一个

                            **Output:**
                            ```json
                            {{
                                "thought": "用户选择了候选列表中的第一项[订单成交额]，需将选择融合到原问题中。",
                                "is_rewritten": true,
                                "rewritten_query": "查询订单成交额",
                                "confidence": 1.0
                            }}
                            ```

                            ## Case 7: 非查询类闲聊
                            **Current Query:** 谢谢

                            **Output:**
                            ```json
                            {{
                                "thought": "这是礼貌用语，不是数据查询请求。",
                                "is_rewritten": false,
                                "rewritten_query": "谢谢",
                                "confidence": 0.0
                            }}
                            ```

                            # Output Format

                            请仅返回 JSON 格式，不要包含 Markdown 标记：
                            ```json
                            {{
                                "thought": "简要说明你的分析思路（可选，用于调试）",
                                "is_rewritten": true/false,
                                "rewritten_query": "重写后的完整问题",
                                "confidence": 0.0-1.0
                            }}
                            # Input
                                ## 用户的问题是:{query}
                                ## 历史记录是:{history}
                            ```
                            """

    # ── QA 时间更新专用 Prompt（与原 _update_sql_time_with_llm 完全一致）──
    SQL_TIME_UPDATE_SYSTEM_PROMPT = """你是一个专业的 SQL 生成专家。你的任务是根据 QA 对中的模板 SQL，结合当前用户问题和当前时间，生成最终可执行的 SQL。

# 核心任务
1. 分析 QA 对中的问题和 SQL
2. 理解当前用户问题的意图
3. 更新 SQL 中的时间条件为基于当前日期的正确时间
4. 如果当前问题与 QA 对问题略有差异，做出必要的调整
5. 返回 JSON 格式的结果

# 时间语义转换规则（基准日期: current_date）

| 用户表述 | SQL 时间条件 | 示例（假设 current_date=2025-12-22） |
|---------|------------|----------------------------------|
| 今天 | `date = current_date` | `year_month_day = '2025-12-22'` |
| 昨天 | `date = current_date - 1` | `year_month_day = '2025-12-21'` |
| 本月至今 | `date BETWEEN '月初' AND current_date` | `year_month_day BETWEEN '2025-12-01' AND '2025-12-22'` |
| 本月 | `date BETWEEN '月初' AND '月末'` | `year_month_day BETWEEN '2025-12-01' AND '2025-12-31'` |
| 上月 | `date BETWEEN '上月初' AND '上月末'` | `year_month_day BETWEEN '2025-11-01' AND '2025-11-30'` |
| 本年至今 | `date BETWEEN '年初' AND current_date` | `year_month_day BETWEEN '2025-01-01' AND '2025-12-22'` |
| 本年 | `date BETWEEN '年初' AND '年末'` | `year_month_day BETWEEN '2025-01-01' AND '2025-12-31'` |
| 去年 | `date BETWEEN '去年初' AND '去年末'` | `year_month_day BETWEEN '2024-01-01' AND '2024-12-31'` |
| 近7天 | `date BETWEEN current_date - 6 AND current_date` | `year_month_day BETWEEN '2025-12-16' AND '2025-12-22'` |
| 近30天 | `date BETWEEN current_date - 29 AND current_date` | `year_month_day BETWEEN '2025-11-23' AND '2025-12-22'` |

# 特殊处理规则
1. **具体日期**: 如果用户指定了具体日期（如"12月21日"），直接使用该日期，但要补全年份
2. **日期范围**: 如果原 SQL 使用 BETWEEN，保持 BETWEEN 语法
3. **单日期**: 如果原 SQL 使用 =，保持 = 语法
4. **其他条件**: SQL 中的其他筛选条件（渠道、维度等）保持不变

请仅返回 JSON 格式，不要包含 Markdown 标记：
{
    "thought": "简要说明你的分析思路和做了哪些调整",
    "original_sql": "QA 对中的原始 SQL",
    "final_sql": "生成的最终 SQL",
    "time_updated": true/false,
    "other_adjustments": "如果有其他调整，说明调整内容；如果没有则为空字符串"
}"""

    def __init__(
            self,
            gemini_api_url: str,
            gemini_api_key: str,
            gemini_token: str,
            llm_timeout: float = 120.0,
    ):
        self.api_url    = gemini_api_url
        self.api_key    = gemini_api_key
        self.token      = gemini_token
        self.llm_timeout = llm_timeout

    # ──────────────────────────────────────────────────────────────────
    # 对外唯一入口
    # ──────────────────────────────────────────────────────────────────

    async def run(self, inp: RewriteInput) -> RewriteOutput:
        """
        执行问题重写逻辑（完整还原 handle_message 三条路径）

        路径 A: QA 精确匹配
        路径 B: 无历史记录，透传
        路径 C: 有历史记录，LLM 重写
        """
        current_query = inp.query

        # ── 路径 A: 检查 QA 对精确匹配 ──────────────────────────────
        if inp.qa_pairs:
            matched_qa = self._find_matching_qa(current_query, inp.qa_pairs)
            if matched_qa:
                logger.info(f"命中 QA 对: id={matched_qa.id}")
                current_date = datetime.now().strftime("%Y-%m-%d")
                updated_sql = await self._update_sql_time_with_llm(matched_qa, current_query, current_date)
                return RewriteOutput(
                    final_query=current_query,
                    is_rewritten=False,
                    matched_sql=updated_sql,
                    is_qa_matched=True,
                )

        # ── 路径 B: 无历史记录，直接透传 ─────────────────────────────
        if not inp.history:
            logger.info("无历史记录，跳过重写，透传原问题")
            return RewriteOutput(
                final_query=current_query,
                is_rewritten=False,
            )

        # ── 路径 C: 有历史记录，调用 LLM 重写 ────────────────────────
        rewritten_result = await self._rewrite_question(current_query, inp.history)

        new_query = current_query
        is_rewritten = False

        if rewritten_result.get("is_rewritten", False):
            possible_query = rewritten_result.get("rewritten_query", current_query)
            confidence = rewritten_result.get("confidence", 0.0)
            thought = rewritten_result.get("thought", "")

            logger.info(
                f"重写分析: 原文='{current_query}' -> 改写='{possible_query}' "
                f"(置信度: {confidence}, 思路: {thought})"
            )
            # 置信度 >= 0.9 才采纳重写结果（原代码逻辑）
            if confidence >= 0.9:
                new_query = possible_query
                is_rewritten = True
            else:
                logger.info(f"置信度低 ({confidence} < 0.9)，保持原问题")
        else:
            logger.info("LLM 判断无需重写，保持原问题")

        return RewriteOutput(
            final_query=new_query,
            is_rewritten=is_rewritten,
            thought=rewritten_result.get("thought", ""),
            confidence=rewritten_result.get("confidence", 0.0),
        )

    # ──────────────────────────────────────────────────────────────────
    # 私有方法（与原 Agent 方法 1:1 对应）
    # ──────────────────────────────────────────────────────────────────

    def _find_matching_qa(self, current_query: str, qa_pairs: List[QAPair]) -> Optional[QAPair]:
        """完全匹配 QA 对（原 _find_matching_qa）"""
        normalized = current_query.strip().replace('\r\n', '\n').replace('\r', '\n')
        for qa in qa_pairs:
            qa_q = qa.question.strip().replace('\r\n', '\n').replace('\r', '\n')
            if normalized == qa_q:
                logger.info(f"找到完全匹配的 QA 对: {qa.id}")
                return qa
        return None

    async def _update_sql_time_with_llm(
            self, qa_pair: QAPair, current_query: str, current_date: str
    ) -> str:
        """用 LLM 将 QA 对中的 SQL 时间条件更新为当前日期（原 _update_sql_time_with_llm）"""
        user_prompt = f"""请根据以下信息生成最终的 SQL：

# QA 对信息
**QA 对中的问题**: {qa_pair.question}
**QA 对中的 SQL**:
{qa_pair.sql}

# 当前查询信息
**当前用户问题**: {current_query}
**当前日期**: {current_date}

# 任务
1. 分析 QA 对的 SQL 模板
2. 识别 SQL 中的时间条件
3. 根据当前日期，更新时间条件为正确的值
4. 如果当前问题与 QA 对问题有差异，做出必要的调整
5. 返回 JSON 格式的结果

请返回 JSON 格式的结果（不要包含 Markdown 标记）："""

        full_prompt = f"{self.SQL_TIME_UPDATE_SYSTEM_PROMPT}\n\n{user_prompt}"
        try:
            content = await self._call_gemini_rest(full_prompt)
            content = self._clean_json(content)
            result = json.loads(content)
            return result.get("final_sql", qa_pair.sql)
        except Exception as e:
            logger.error(f"LLM 更新 SQL 时间失败: {e}")
            return qa_pair.sql

    async def _rewrite_question(
            self, current_query: str, history: List[HistoryRecord]
    ) -> Dict[str, Any]:
        """
        格式化历史记录并调用 LLM 重写问题（原 _rewrite_question）

        历史格式化规则（与原代码完全一致）:
          - 按 session_id 分组，每组只保留一条：优先有 clarification_type 的，否则取最新的
          - 若某条历史有 clarification_type，在 AI 回复行展示候选列表
        """
        # Step 1: 按 session_id 去重
        session_records: Dict[str, HistoryRecord] = {}
        for h in history:
            sid = h.session_id
            if sid not in session_records:
                session_records[sid] = h
            else:
                has_new_clr = bool(
                    h.response_data and
                    isinstance(h.response_data, dict) and
                    h.response_data.get("clarification_type")
                )
                has_old_clr = bool(
                    session_records[sid].response_data and
                    isinstance(session_records[sid].response_data, dict) and
                    session_records[sid].response_data.get("clarification_type")
                )
                if has_new_clr and not has_old_clr:
                    session_records[sid] = h
                elif not has_new_clr and not has_old_clr:
                    if h.created_at > session_records[sid].created_at:
                        session_records[sid] = h

        # Step 2: 按时间正序排列，格式化为文本
        sorted_history = sorted(session_records.values(), key=lambda x: x.created_at)
        history_items = []
        for h in sorted_history:
            history_items.append(f"User: {h.query}")
            if h.response_data and isinstance(h.response_data, dict):
                clarification_type = h.response_data.get("clarification_type")
                if clarification_type:
                    candidates = h.response_data.get("candidates", [])
                    candidates_text = ""
                    for c in candidates:
                        idx = c.get("index", "")
                        name = c.get("name") or c.get("indicator_name") or c.get("value", "")
                        code = c.get("code") or c.get("indicator_code") or c.get("metric_code", "")
                        if code:
                            candidates_text += f"  {idx}. {name} (编码: {code})\n"
                        else:
                            candidates_text += f"  {idx}. {name}\n"
                    if candidates_text:
                        history_items.append(f"AI: 已返回以下候选列表供选择：\n{candidates_text.strip()}")

        history_text = "\n".join(history_items) if history_items else "无历史记录"

        # Step 3: 拼装 Prompt 并调用 LLM
        final_message = self.SYSTEM_PROMPT.format(query=current_query, history=history_text)
        logger.info(f"重写提示词: {final_message[:200]}...")
        try:
            content = await self._call_gemini_rest(final_message)
            content = self._clean_json(content)
            return json.loads(content)
        except Exception as e:
            logger.error(f"LLM 重写调用或解析失败: {e}")
            return {"is_rewritten": False, "confidence": 0.0}

    async def _call_gemini_rest(self, prompt: str) -> str:
        """
        同步调用 Gemini REST API（与原 intent_recognition.call_gemini_rest_sync 逻辑完全一致）
        包装为 asyncio.to_thread 以支持 async 上下文
        """
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
                result   = resp.json()
                duration = time.time() - start
                content  = ""
                cands    = result.get("candidates", [])
                if cands:
                    parts = cands[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        content = parts[0]["text"]
                logger.info(f"Gemini REST 调用成功，耗时 {duration:.2f}s")
                return content

        return await asyncio.to_thread(_sync_call)

    @staticmethod
    def _clean_json(content: str) -> str:
        """去除 Markdown 代码块标记"""
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        return content.strip()


# ═══════════════════════════════════════════════════════════════════
# 3. 连接真实服务的辅助函数（独立运行时使用）
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
    """从环境变量读取 Gemini API 配置（与工作区 intent_recognition.py 一致）"""
    import os
    base_url  = os.getenv("GEMINI_API_URL", "http://47.77.199.56/api/v1beta").rstrip("/")
    model     = os.getenv("GEMINI_MODEL_NAME", "gemini-3-flash-preview")
    api_url   = f"{base_url}/models/{model}:generateContent"
    # GEMINI_TOKEN 也可放入 .env；不配置时使用工作区内置值
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
        "api_url": api_url,
        "api_key": os.getenv("GEMINI_API_KEY", ""),
        "token":   os.getenv("GEMINI_TOKEN", _default_token),
    }


def _fetch_all_qa_pairs() -> List[QAPair]:
    """
    从 Milvus 获取所有 QA 对（与原 _get_all_qa_pairs 逻辑一致）

    使用 .env 中的 Milvus 配置连接：
      MILVUS_HOST / MILVUS_PORT / MILVUS_USER / MILVUS_PASSWORD
      MILVUS_DB_NAME / MILVUS_COLLECTION
    """
    import os
    try:
        from pymilvus import MilvusClient as PyMilvusClient

        host       = os.getenv("MILVUS_HOST", "localhost")
        port       = int(os.getenv("MILVUS_PORT", "19530"))
        user       = os.getenv("MILVUS_USER", "")
        password   = os.getenv("MILVUS_PASSWORD", "")
        db_name    = os.getenv("MILVUS_DB_NAME", "default")
        collection = os.getenv("MILVUS_COLLECTION", "dev_vanna_sql")

        uri = f"http://{host}:{port}"
        kwargs = {"uri": uri}
        if user and password:
            kwargs.update({"user": user, "password": password, "db_name": db_name})

        client  = PyMilvusClient(**kwargs)
        results = client.query(
            collection_name=collection,
            filter="id != ''",
            output_fields=["id", "text", "sql"],
            limit=5000,
        )

        qa_pairs = [
            QAPair(id=str(r.get("id", "")), question=r.get("text", ""), sql=r.get("sql", ""))
            for r in results
            if r.get("text") and r.get("sql")
        ]
        print(f"[Milvus] 获取 QA 对 {len(qa_pairs)} 条  (collection={collection})")
        return qa_pairs

    except ImportError:
        print("[Milvus] pymilvus 未安装，跳过 QA 对召回")
        return []
    except Exception as e:
        print(f"[Milvus] 获取 QA 对失败: {e}，继续运行（无 QA 对）")
        return []


# ═══════════════════════════════════════════════════════════════════
# 4. 流水线工作目录 & main 入口（可独立运行）
# ═══════════════════════════════════════════════════════════════════

def _get_workflow_dir() -> "Path":  # type: ignore[name-defined]
    """
    返回技能流水线共享工作目录：<skills根>/.workflow/
    目录不存在时自动创建。

    目录结构：
        skills/
          .workflow/              ← 所有 *_output.json 统一存放于此
          rewrite-question/       ← 本文件所在位置
          recognize-intent/
          mult-call/
          sql-generator/
          sql-audit/

    文件命名约定（依次衔接）：
        rewrite_question.py  → rewrite_output.json
        recognize_intent.py  → intent_output.json    (读取 rewrite_output.json)
        multi_call.py        → multicall_output.json (读取 intent_output.json)
        sql_generator.py     → sql_output.json       (读取 multicall_output.json)
        sql_audit.py         → audit_output.json     (读取 sql_output.json)

    多次运行说明：
        每次写入前自动将旧文件备份为 <name>.bak.json（只保留一份）。
        使用 --clean 参数可强制删除本步及后续所有 *_output.json，
        避免重复调试时混入过期数据。
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

    用法（从任意目录均可运行，输出统一写入 skills/.workflow/）:
        python rewrite_question.py --query "今天汉河店的成交额"
        python rewrite_question.py --query "上个月呢"             # 无历史时直接透传
        python rewrite_question.py --query "..." --clean         # 清理本步及后续输出再运行

    输出文件 rewrite_output.json 保存在 skills/.workflow/，
    供下一步 recognize_intent.py 读取。
    """
    import argparse, os
    from pathlib import Path

    wf = _get_workflow_dir()
    default_output = str(wf / "rewrite_output.json")

    parser = argparse.ArgumentParser(description="问题重写技能 — 独立运行")
    parser.add_argument("--query",  required=True,           help="用户原始问题")
    parser.add_argument("--output", default=default_output,  help=f"输出 JSON 文件路径 (默认: {default_output})")
    parser.add_argument("--clean",  action="store_true",     help="运行前删除本步及后续所有输出文件（防止旧数据污染）")
    args = parser.parse_args()

    # ── 可选：清理当前步骤和所有后续步骤的输出（多次调试时使用）──
    if args.clean:
        for name in ("rewrite_output.json", "intent_output.json", "multicall_output.json",
                     "sql_output.json", "audit_output.json"):
            stale = wf / name
            if stale.exists():
                stale.unlink()
                print(f"[清理] 已删除: {stale}")

    # 1. 加载环境变量
    _load_dotenv()

    # 2. 获取 Gemini 配置
    cfg = _get_gemini_config()
    if not cfg["api_key"]:
        print("[错误] GEMINI_API_KEY 未配置，请在 .env 中添加")
        return

    # 3. 从 Milvus 获取所有 QA 对
    qa_pairs = _fetch_all_qa_pairs()

    # 4. 构建输入（独立运行时无历史记录）
    inp = RewriteInput(
        query=args.query,
        history=[],       # 无历史记录时走路径 B（直接透传）或路径 A（命中 QA 对）
        qa_pairs=qa_pairs,
    )

    # 5. 执行技能
    skill = RewriteQuestionSkill(
        gemini_api_url=cfg["api_url"],
        gemini_api_key=cfg["api_key"],
        gemini_token=cfg["token"],
    )

    print(f"\n[运行] 问题重写: '{args.query}'")
    output = await skill.run(inp)

    # 6. 整理并保存输出（自动备份旧文件）
    result = {
        "original_query": args.query,
        "final_query":    output.final_query,
        "is_rewritten":   output.is_rewritten,
        "confidence":     output.confidence,
        "thought":        output.thought,
        "is_qa_matched":  output.is_qa_matched,
        "matched_sql":    output.matched_sql,
    }

    _backup_if_exists(args.output)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # 7. 打印摘要
    print(f"\n{'='*60}")
    print(f"原始问题 : {args.query}")
    print(f"最终问题 : {output.final_query}")
    if output.is_rewritten:
        print(f"已重写   : 是 (置信度 {output.confidence:.2f})")
    if output.is_qa_matched:
        print(f"命中QA对 : 是")
        print(f"生成SQL  :\n{output.matched_sql}")
    print(f"{'='*60}")
    print(f"[输出] 已保存到: {args.output}")
    print(f"[下一步] python ../recognize-intent/recognize_intent.py  (读取 {args.output})")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    asyncio.run(main())
