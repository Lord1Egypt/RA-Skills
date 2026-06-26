#!/usr/bin/env python3
"""LLM 标题价值判断模块 - 在下载 PDF 前筛选低价值公告

通过 OpenAI 兼容 API 判断公告标题是否包含实质性内容。
作为正则模式（SKIP_CONTENT_PATTERNS）的补充，捕获遗漏的低价值公告。
"""

import json
import logging
import os
import re
import time
from typing import Optional

import requests

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_TIMEOUT = 30

_ENV_PATH = None


def _get_env_path() -> str:
    global _ENV_PATH
    if _ENV_PATH is None:
        _ENV_PATH = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"
        )
    return _ENV_PATH


def _load_env_key(key: str) -> Optional[str]:
    path = _get_env_path()
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                k, _, v = line.partition("=")
                if k.strip() == key:
                    val = v.strip().strip("\"'")
                    return val if val else None
    except (OSError, UnicodeDecodeError) as e:
        logger.debug("读取 .env 失败: %s", e)
    return None

# A股公告分类：大类 -> 小类列表
A_CATEGORY_MAP = {
    "招股类": ["申报稿", "申报反馈", "招股说明书", "发行定价", "发行结果", "上市公告书"],
    "财务报告类": ["业绩预告", "业绩快报", "季度报告", "半年报告", "年度报告", "补充更正"],
    "重大事项类": ["利润分配", "股份增减持", "资金投向", "资产重组", "收购兼并", "重大合同", "股权激励", "关联交易", "借贷担保", "委托理财", "违纪违规", "政策影响", "人事变动"],
    "交易提示类": ["停牌提示", "交易异动", "澄清公告", "风险提示", "特别处理", "终止上市", "恢复上市", "暂停上市"],
    "配股类": ["配股预案", "配股说明书", "配股获准", "配股发行", "配股上市"],
    "增发类": ["增发预案", "增发说明书", "增发获准", "增发发行", "增发上市"],
    "股权股本类": ["权益变动", "股本变动", "质押冻结", "质押式回购", "回购股权", "约定购回", "股权分置改革"],
    "一般公告类": ["董事会公告", "股东大会", "权证公告", "中介公告", "法律纠纷", "机构调研公告", "其他补充更正", "公司资料变更", "融资融券", "员工持股", "产销经营快报", "个股其他公告", "ESG报告", "函件"],
}

# 港股公告分类：大类 -> 小类列表
HK_CATEGORY_MAP = {
    "业绩快报": ["业绩预告", "季度业绩", "中期业绩", "末期业绩", "业绩发布会"],
    "财务报告": ["环境及管治报告", "季度报告", "中期报告", "年度报告"],
    "上市文件": ["预览资料", "发售以供认购", "招股说明书", "公开招股", "供股", "资本化发行", "介绍上市", "发售现有证券", "聆讯资料", "其它上市文件"],
    "股权股本": ["权益变动", "证券/股本", "交易披露", "翌日报表", "月报表"],
    "公告及通函": ["重大事项", "新上市", "会议/表决", "关联交易", "须公布的交易", "公司变动", "财务资料", "杂项"],
    "一般公告": ["交易安排", "创业板资料", "监管者公告", "委任代表表格", "宪章文件"],
    "债券及结构性产品": ["权证公告", "权证上市", "债务证券公告", "其它"],
}


def _get_category(market: str, subtype: str) -> str:
    """根据市场和小类，查询对应的大类"""
    category_map = HK_CATEGORY_MAP if market == "港股" else A_CATEGORY_MAP
    for category, subtypes in category_map.items():
        if subtype in subtypes:
            return category
    return "一般公告类" if market != "港股" else "一般公告"


SYSTEM_PROMPT = """你是上市公司公告分类专家。请按以下两步操作：

**第一步：分类** — 根据公告标题，判断它属于哪个 category（大类）和 type（小类）。

**第二步：判断价值** — 根据分类结果，判断是否需要下载 PDF 全文。

分类体系（参考万得金融终端）：

【中国大陆A股公告类型】
招股类：申报稿、申报反馈、招股说明书、发行定价、发行结果、上市公告书
财务报告类：业绩预告、业绩快报、季度报告、半年报告、年度报告、补充更正
重大事项类：利润分配、股份增减持、资金投向、资产重组、收购兼并、重大合同、股权激励、关联交易、借贷担保、委托理财、违纪违规、政策影响、人事变动
交易提示类：停牌提示、交易异动、澄清公告、风险提示、特别处理、终止上市、恢复上市、暂停上市
配股类：配股预案、配股说明书、配股获准、配股发行、配股上市
增发类：增发预案、增发说明书、增发获准、增发发行、增发上市
股权股本类：权益变动、股本变动、质押冻结、质押式回购、回购股权、约定购回、股权分置改革
一般公告类：董事会公告、股东大会、权证公告、中介公告、法律纠纷、机构调研公告、其他补充更正、公司资料变更、融资融券、员工持股、产销经营快报、个股其他公告、ESG报告、函件

【中国香港股票公告类型】
业绩快报：业绩预告、季度业绩、中期业绩、末期业绩、业绩发布会
财务报告：环境及管治报告、季度报告、中期报告、年度报告
上市文件：预览资料、发售以供认购、招股说明书、公开招股、供股、资本化发行、介绍上市、发售现有证券、聆讯资料、其它上市文件
股权股本：权益变动、证券/股本、交易披露、翌日报表、月报表
公告及通函：重大事项、新上市、会议/表决、关联交易、须公布的交易、公司变动、财务资料、杂项
一般公告：交易安排、创业板资料、监管者公告、委任代表表格、宪章文件
债券及结构性产品：权证公告、权证上市、债务证券公告、其它

**价值判断规则**（基于分类结果）：

高价值 type（几乎总是需要下载）：
- 财务报告类全部（业绩预告、业绩快报、季度报告、半年报告、年度报告）
- 交易提示类全部（停牌提示、交易异动、澄清公告、风险提示、特别处理、终止上市等）
- 重大事项类：资产重组、收购兼并、股权激励、关联交易、违纪违规
- 股权股本类：回购股权、权益变动
- 一般公告类：法律纠纷、产销经营快报、机构调研公告
- 港股：翌日报表、须公布的交易

低价值 type（几乎总是不需要下载）：
- 中介公告（法律意见书、保荐机构核查意见、律师核查意见）
- 股东大会通知（纯程序性通知，无实质内容）
- 薪酬管理制度、董事会议事规则、公司章程修正案
- 各类管理制度（离职管理制度、绩效考核制度、信息披露制度等）
- 回购注销股权激励限制性股票（量小无影响，保留普通回购注销）
- 业绩说明会、业绩发布会（纯形式，无实质内容）
- 限制性股票/股票期权预留授予完成登记（常规程序性公告）
- 债券付息公告、发行结果公告

需要结合标题判断的 type：
- 董事会公告：如果标题提到具体议案（收购、回购等）→ 有价值；纯程序性 → 无价值
- 借贷担保：所有担保公告（含为子公司担保、合计担保等）→ 无价值
- 利润分配：高送转 → 有价值；常规分红实施 → 无价值

重要约束：type 字段必须从上方分类列表中精确选择，不能自行简化或改写。

用JSON格式回答：
{"category": "交易提示类", "type": "风险提示", "judge": true}
{"category": "一般公告类", "type": "中介公告", "judge": false}
{"category": "重大事项类", "type": "资产重组", "judge": true}"""


class LLMJudge:
    """LLM 标题价值判断器"""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        model: str = DEFAULT_MODEL,
        enabled: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = 2,
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.enabled = enabled
        self.timeout = timeout
        self.retries = retries

        self._chat_url = f"{self.base_url}/chat/completions"
        self._headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # 统计信息
        self.stats = {"total": 0, "valuable": 0, "skip": 0, "error": 0}

    def judge(self, title: str, stock_name: str = "", market: str = "A股") -> dict:
        """判断公告标题是否有价值，并返回类型分类

        Args:
            title: 公告标题
            stock_name: 股票名称（可选）
            market: 市场类型，"A股" 或 "港股"（可选，默认 A 股）

        Returns:
            {"valuable": True/False, "category": "股权股本类", "type": "回购"} 等
        """
        if not self.enabled:
            return {"valuable": True, "category": "一般公告类", "type": "个股其他公告"}

        self.stats["total"] += 1

        user_msg = f"标题：{title}"
        if stock_name:
            user_msg += f"\n股票：{stock_name}"
        user_msg += f"\n市场：{market}"

        for attempt in range(self.retries + 1):
            try:
                resp = requests.post(
                    self._chat_url,
                    headers=self._headers,
                    json={
                        "model": self.model,
                        "response_format": {"type": "json_object"},
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_msg},
                        ],
                        "temperature": 0.1,
                        "max_tokens": 1024,
                    },
                    timeout=self.timeout,
                )
                resp.raise_for_status()
                data = resp.json()
                message = data.get("choices", [{}])[0].get("message", {})
                content = (message.get("content") or "").strip()
                reasoning = (message.get("reasoning_content") or "").strip()

                # 优先解析 JSON content
                if content:
                    try:
                        parsed = json.loads(content)
                        subtype = parsed.get("type", "个股其他公告")
                        category = parsed.get("category", "")
                        if not category:
                            category = _get_category(market, subtype)
                        result = {
                            "valuable": parsed.get("judge", True),
                            "category": category,
                            "type": subtype,
                        }
                    except (json.JSONDecodeError, KeyError):
                        result = {"valuable": True, "category": "一般公告类", "type": "个股其他公告"}
                else:
                    # reasoning 模型可能 content 为空，从 reasoning 末尾提取结论
                    combined = reasoning.lower()
                    is_valuable = True  # fail-open
                    try:
                        json_match = re.search(r'\{[^}]*"judge"\s*:\s*(true|false)[^}]*\}', combined)
                        if json_match:
                            is_valuable = json_match.group(1) == "true"
                        elif re.search(r'judge\s*[:=]\s*(true|false)', combined):
                            m = re.search(r'judge\s*[:=]\s*(true|false)', combined)
                            is_valuable = m.group(1) == "true"
                        else:
                            tail = combined[-100:]
                            if re.search(r'(无价值|没有价值|不值得|跳过|skip)', tail):
                                is_valuable = False
                    except (IndexError, TypeError, AttributeError):
                        pass
                    result = {"valuable": is_valuable, "category": "一般公告类", "type": "个股其他公告"}

                if result["valuable"]:
                    self.stats["valuable"] += 1
                    logger.debug("LLM判断: 有价值 [%s] %s", stock_name, title[:40])
                else:
                    self.stats["skip"] += 1
                    logger.info("LLM跳过: 无价值 [%s] %s", stock_name, title[:60])

                return result

            except (requests.RequestException, json.JSONDecodeError) as e:
                logger.warning(
                    "LLM 调用失败 (attempt %d/%d): %s", attempt + 1, self.retries + 1, e
                )
                if attempt < self.retries:
                    time.sleep((attempt + 1) * 2)
                continue

        self.stats["error"] += 1
        logger.warning("LLM 调用全部失败，默认视为有价值: [%s] %s", stock_name, title[:40])
        return {"valuable": True, "category": "一般公告类", "type": "个股其他公告"}

    def report(self) -> str:
        """返回 LLM 判断统计信息"""
        total = self.stats["total"]
        if total == 0:
            return "LLM 未进行任何判断"
        skip_pct = self.stats["skip"] / total * 100
        return (
            f"LLM 判断: 共 {total} 条, "
            f"有价值 {self.stats['valuable']} 条, "
            f"跳过 {self.stats['skip']} 条 ({skip_pct:.1f}%), "
            f"失败 {self.stats['error']} 条"
        )

    @classmethod
    def from_config(cls, config: dict) -> "LLMJudge":
        """从配置字典 + .env 文件创建 LLMJudge 实例

        api_key 优先从 .env 文件读取（LLM_API_KEY 变量），
        config.json 中不再存储敏感信息。
        """
        llm_cfg = config.get("llm", {})
        if not llm_cfg.get("enabled", False):
            return cls(api_key="", enabled=False)

        api_key = _load_env_key("LLM_API_KEY")
        if not api_key:
            logger.warning(
                "LLM 已启用但 .env 中未配置 LLM_API_KEY，已自动禁用"
            )
            return cls(api_key="", enabled=False)

        return cls(
            api_key=api_key,
            base_url=llm_cfg.get("base_url", "https://api.openai.com/v1"),
            model=llm_cfg.get("model", DEFAULT_MODEL),
            enabled=True,
            timeout=llm_cfg.get("timeout", DEFAULT_TIMEOUT),
            retries=llm_cfg.get("retries", 2),
        )
