# -*- coding: utf-8 -*-
"""
飞书多维表数据标注 Skill：
- 从多维表中抽取待标注记录；
- 为每条记录自动标注以下机器字段：
  - 「类型（机器）」：产品 / 观点 / 无关 / 运营
  - 「一级分类(机器)」「二级分类(机器)」「三级分类(机器)」：依据 system_prompt_class 的三级分类体系
  - 「评价情感（机器）」：正向 / 中立 / 负向
  - 「是否提及竞品(机器)」：是 / 否
  - 「端(机器)」：手机 / 车载 / 音箱 / 电视 / 眼镜 / 平板 / 电脑 / 穿戴 / 其他 / 无法判断
  - 「品牌安全(AI)」：是 / 否（是否存在品牌安全风险）
  - 「内容安全(AI)」：是 / 否（是否存在内容安全风险）
- 优先在当前进程内调用第三方大模型网关（OpenAI 兼容协议：OPENAI_BASE_URL / OPENAI_API_KEY / OPENAI_MODEL）并发完成标注；
- 若未配置上述环境变量，则退回到 OpenClaw 模式：从 stdin 读取模型输出并写回多维表字段。
依赖：requests。
"""
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional, Tuple

import requests
from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------- 配置（环境变量 / skill 入参）----------
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")
BITABLE_URL = os.getenv("BITABLE_URL")
LIMIT = int(os.getenv("LIMIT", "100"))
# 为 OpenClaw 准备：仅输出每条记录的用户提示词（每行一条），由平台用 SYSTEM_PROMPT + 每行 user 调内置模型，再将模型输出通过 stdin 传回
OUTPUT_PROMPTS_ONLY = os.getenv("OUTPUT_PROMPTS_ONLY", "").strip().lower() in ("1", "true", "yes")
# 强制重新标注所有记录（忽略已有标注值），用于修复历史默认值污染
FORCE_RELABEL = os.getenv("FORCE_RELABEL", "").strip().lower() in ("1", "true", "yes")

# 在进程内调用第三方大模型网关（OpenAI 兼容协议），全部由环境变量配置：
#   OPENAI_API_KEY      网关访问密钥 (必填)
#   OPENAI_BASE_URL     模型网关地址 (必填)，例如：https://api.openai.com/v1 或自建网关地址
#   OPENAI_MODEL        具体模型名 (必填)，例如：gpt-4o, gpt-4o-mini, qwen-plus 等
#   LLM_CONCURRENCY     并发 worker 数（建议 2~6，避免打爆限流）
#   LLM_TIMEOUT         单次调用超时时间（秒）
#   LLM_MAX_RETRIES     超时/5xx/429 时的重试次数
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "").strip()
# 去掉默认值，三个都必须由用户配置
if OPENAI_BASE_URL:
    OPENAI_BASE_URL = OPENAI_BASE_URL.rstrip("/")
LLM_CONCURRENCY = int(os.getenv("LLM_CONCURRENCY", "4"))
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "20"))
LLM_MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", "2"))

SESSION: Optional[requests.Session] = None

BASE_DIR = os.path.dirname(__file__)


def load_prompt(filename: str, default: str) -> str:
    """
    尝试从同目录下的外部文件加载完整提示词，若失败则回退到内置精简版。
    这样既保留 system_prompt_* 中的详细规则，又避免在代码文件中内联超长文本。
    """
    path = os.path.join(BASE_DIR, filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return content or default
    except Exception:
        return default

# 「类型（机器）」合法取值（与 system_prompt_type 及多维表单选一致）
LABEL_OPTIONS = ["产品", "观点", "无关", "运营"]

# 「评价情感（机器）」合法取值（与 system_prompt_emotion 一致）
EMOTION_LABEL_OPTIONS = ["正向", "中立", "负向"]

# 「是否提及竞品(机器)」合法取值
COMPETITOR_FLAG_OPTIONS = ["是", "否"]

# 「端(机器)」合法取值（与 system_prompt 中端标签枚举一致）
DEVICE_LABEL_OPTIONS = ["手机", "车载", "音箱", "电视", "眼镜", "平板", "电脑", "穿戴", "其他", "无法判断"]

# 「品牌安全(AI)」合法取值（是/否）
BRAND_SAFETY_OPTIONS = ["是", "否"]

# 「内容安全(AI)」合法取值（是/否）
CONTENT_SAFETY_OPTIONS = ["是", "否"]

# ---------- 提示词模版：类型（机器）（运行时优先从 system_prompt_type 加载完整规则）----------
SYSTEM_PROMPT = load_prompt(
    "system_prompt_type.md",
    "你是小米小爱舆情标注专家，需要将每条内容归类为「产品」「观点」「无关」「运营」四类之一。"
)

USER_PROMPT_TEMPLATE = """请根据以下信息，将本条内容归类为「产品、观点、无关、运营」四类之一。

作者：{作者}
来源渠道：{来源渠道}
粉丝量：{粉丝量}
命中关键词：{命中关键词}

标题：
{标题}

正文：
{正文}

抽帧识别内容：
{抽帧识别内容}"""

# ---------- 提示词模版：是否提及竞品(机器)（运行时优先从 system_prompt_jinpin 加载完整规则）----------
SYSTEM_PROMPT_COMPETITOR = load_prompt(
    "system_prompt_jinpin.md",
    "你为小米服务，负责判断舆情内容中是否提及竞品（如华为小艺、Siri、ChatGPT 等）。"
)

USER_PROMPT_COMPETITOR_TEMPLATE = """请根据以下用户舆情内容，判断是否提及竞品。

标题：
{标题}

正文：
{正文}

抽帧识别内容：
{抽帧识别内容}"""

# ---------- 提示词模版：评价情感（机器）（运行时优先从 system_prompt_emotion 加载完整规则）----------
SYSTEM_PROMPT_EMOTION = load_prompt(
    "system_prompt_emotion.md",
    "你需要根据舆情内容判断整体情感倾向，只能输出「正向」「中立」「负向」之一。"
)

USER_PROMPT_EMOTION_TEMPLATE = """请根据以下用户舆情内容，判断情感分类（正向、中立、负向）。

标题：
{标题}

正文：
{正文}

抽帧识别内容：
{抽帧识别内容}"""

# ---------- 提示词模版：端(机器)（精简版，详细规则见 system_prompt）----------
SYSTEM_PROMPT_DEVICE = load_prompt(
    "system_prompt_device.md",
    "只能输入以下枚举选项的其中一个：手机、车载、音箱、电视、眼镜、平板、电脑、穿戴、其他、无法判断。"
)

USER_PROMPT_DEVICE_TEMPLATE = """请根据以下用户舆情内容，判断小爱同学的主要使用端（手机/车载/音箱/电视/眼镜/平板/电脑/穿戴/其他/无法判断）。

标题：
{标题}

正文：
{正文}

抽帧识别内容：
{抽帧识别内容}"""

# ---------- 提示词模版：品牌安全(AI)（运行时优先从 system_prompt_pinpai 加载完整规则）----------
SYSTEM_PROMPT_BRAND_SAFETY = load_prompt(
    "system_prompt_pinpai.md",
    "你是一名小米品牌安全风险分析师，需要判断一条舆情内容是否涉及小米/小爱相关的品牌安全风险。"
)

USER_PROMPT_BRAND_SAFETY_TEMPLATE = """请根据以下用户舆情内容，判断是否存在小米品牌/小爱相关的品牌安全风险（输出“是”或“否”）。

标题：
{标题}

正文：
{正文}

抽帧识别内容：
{抽帧识别内容}"""

# ---------- 提示词模版：内容安全(AI)（运行时优先从 system_prompt_content 加载完整规则）----------
SYSTEM_PROMPT_CONTENT_SAFETY = load_prompt(
    "system_prompt_content.md",
    "你是一名舆情内容安全风险研判专家，需要判断一条舆情内容是否存在内容安全风险，只能输出“是”或“否”。"
)

USER_PROMPT_CONTENT_SAFETY_TEMPLATE = """请根据以下用户舆情内容，判断是否存在内容安全风险（输出“是”或“否”）。

标题：
{标题}

正文：
{正文}

抽帧识别内容：
{抽帧识别内容}"""


def get_session() -> requests.Session:
    global SESSION
    if SESSION is None:
        SESSION = requests.Session()
    return SESSION


def parse_bitable_url(url: str) -> Tuple[str, str]:
    parsed = urlparse(url)
    app_token = ""
    parts = [p for p in parsed.path.split("/") if p]
    for i, p in enumerate(parts):
        if p == "base" and i + 1 < len(parts):
            app_token = parts[i + 1]
            break
    qs = parse_qs(parsed.query)
    table_id = qs.get("table", [None])[0]
    if not app_token or not table_id:
        raise RuntimeError(f"BITABLE_URL 解析失败: {url}")
    return app_token, table_id


def get_tenant_access_token() -> str:
    if not APP_ID or not APP_SECRET:
        raise RuntimeError("请设置环境变量 APP_ID 和 APP_SECRET")
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": APP_ID, "app_secret": APP_SECRET}
    resp = get_session().post(url, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"获取飞书 token 失败: {data}")
    return data["tenant_access_token"]


def _safe_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value).strip()


def build_user_prompt(fields: Dict[str, Any]) -> str:
    """用多维表字段填充「类型（机器）」用户提示词。"""
    mapping = {
        "作者": _safe_text(fields.get("作者")),
        "来源渠道": _safe_text(fields.get("来源渠道")),
        "粉丝量": _safe_text(fields.get("粉丝量")),
        "命中关键词": _safe_text(fields.get("命中关键词")),
        "标题": _safe_text(fields.get("标题")),
        "正文": _safe_text(fields.get("正文")),
        "抽帧识别内容": _safe_text(fields.get("抽帧识别内容")),
    }
    return USER_PROMPT_TEMPLATE.format(**mapping)


def build_emotion_user_prompt(fields: Dict[str, Any]) -> str:
    """用多维表字段填充「评价情感（机器）」用户提示词。"""
    mapping = {
        "标题": _safe_text(fields.get("标题")),
        "正文": _safe_text(fields.get("正文")),
        "抽帧识别内容": _safe_text(fields.get("抽帧识别内容")),
    }
    return USER_PROMPT_EMOTION_TEMPLATE.format(**mapping)


def build_competitor_user_prompt(fields: Dict[str, Any]) -> str:
    """用多维表字段填充「是否提及竞品(机器）」用户提示词。"""
    mapping = {
        "标题": _safe_text(fields.get("标题")),
        "正文": _safe_text(fields.get("正文")),
        "抽帧识别内容": _safe_text(fields.get("抽帧识别内容")),
    }
    return USER_PROMPT_COMPETITOR_TEMPLATE.format(**mapping)


def build_device_user_prompt(fields: Dict[str, Any]) -> str:
    """用多维表字段填充「端(机器)」用户提示词。"""
    mapping = {
        "标题": _safe_text(fields.get("标题")),
        "正文": _safe_text(fields.get("正文")),
        "抽帧识别内容": _safe_text(fields.get("抽帧识别内容")),
    }
    return USER_PROMPT_DEVICE_TEMPLATE.format(**mapping)


def build_brand_safety_user_prompt(fields: Dict[str, Any]) -> str:
    """用多维表字段填充「品牌安全(AI)」用户提示词。"""
    mapping = {
        "标题": _safe_text(fields.get("标题")),
        "正文": _safe_text(fields.get("正文")),
        "抽帧识别内容": _safe_text(fields.get("抽帧识别内容")),
    }
    return USER_PROMPT_BRAND_SAFETY_TEMPLATE.format(**mapping)


def build_content_safety_user_prompt(fields: Dict[str, Any]) -> str:
    """用多维表字段填充「内容安全(AI)」用户提示词。"""
    mapping = {
        "标题": _safe_text(fields.get("标题")),
        "正文": _safe_text(fields.get("正文")),
        "抽帧识别内容": _safe_text(fields.get("抽帧识别内容")),
    }
    return USER_PROMPT_CONTENT_SAFETY_TEMPLATE.format(**mapping)


def call_llm(system: str, user: str) -> str:
    """
    可选：当 OPENAI_API_KEY 已设置时，在进程内调用第三方大模型网关（OpenAI 兼容协议），返回模型回复全文。
    未设置时返回空字符串，交由 stdin 模式处理。
    """
    if not OPENAI_API_KEY or not OPENAI_MODEL:
        return ""

    url = f"{OPENAI_BASE_URL}/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }
    payload = {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.1,
        "max_tokens": 256,
    }

    # 简单重试 + 指数退避，减少瞬时超时/限流的影响
    last_err: Optional[Exception] = None
    for attempt in range(LLM_MAX_RETRIES + 1):
        try:
            resp = get_session().post(
                url,
                headers=headers,
                json=payload,
                timeout=LLM_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            choice = (data.get("choices") or [None])[0]
            if not choice:
                return ""
            message = choice.get("message") or {}
            content = message.get("content")
            if isinstance(content, str):
                return content
            return str(content or "")
        except requests.exceptions.Timeout as e:
            last_err = e
        except requests.exceptions.HTTPError as e:
            last_err = e
            status = e.response.status_code if e.response is not None else None
            # 打印 4xx 错误详情，帮助诊断
            if status is not None and status < 500:
                try:
                    err_body = e.response.text[:300]
                except Exception:
                    err_body = "(无法读取响应体)"
                print(f"    [LLM {status}错误] {err_body}", flush=True)
            # 429 / 5xx 可重试，4xx 直接放弃
            if status is not None and status < 500 and status != 429:
                break
        except requests.exceptions.RequestException as e:
            last_err = e

        # 需要重试且不是最后一次时，做一个简单退避
        if attempt < LLM_MAX_RETRIES:
            backoff = 1.0 * (2 ** attempt)
            time.sleep(backoff)

    # 重试全部失败，返回空字符串，后续解析层会走默认兜底标签
    if last_err:
        raise last_err
    return ""


def parse_label_from_response(text: str) -> str:
    """
    从模型回复中解析「类型（机器）」。
    输出约定：仅包含「产品、观点、无关、运营」其一，无其他说明。
    """
    text = (text or "").strip()
    # 1) 匹配 "类型（机器）：XXX" 或 直接标签
    for sep in ["类型（机器）：", "类型(机器)：", "类型（机器）:", "类型(机器):"]:
        if sep in text:
            part = text.split(sep, 1)[-1].strip()
            part = part.split("\n")[0].split("。")[0].strip()
            for opt in LABEL_OPTIONS:
                if opt == part or opt in part:
                    return opt
            if part:
                return part

    # 2) 在整段回复中查找第一个出现的合法标签（产品/观点/无关/运营）
    for opt in LABEL_OPTIONS:
        if opt in text:
            return opt

    return "无关"


def parse_emotion_from_response(text: str) -> str:
    """从模型回复中解析「评价情感（机器）」：正向、中立、负向。"""
    text = (text or "").strip()
    for opt in EMOTION_LABEL_OPTIONS:
        if opt in text:
            return opt
    return "中立"


def parse_competitor_flag_from_response(text: str) -> str:
    """
    从模型回复中解析「是否提及竞品(机器)」：
    - 若模型严格按 system_prompt_competitor 的约定，输出为若干竞品名或“否”。
    - 这里直接做一个简化规则：回复为“否”或空，视为「否」，其他情况视为「是」。
    """
    t = (text or "").strip()
    if not t or t == "否":
        return "否"
    return "是"


def parse_device_label_from_response(text: str) -> str:
    """
    从模型回复中解析「端(机器)」：
    - 端标签必须是 DEVICE_LABEL_OPTIONS 中的一种（手机、车载、音箱、电视、眼镜、平板、电脑、穿戴、其他、无法判断）
    - 如果模型输出不在枚举内，则统一标注为“无法判断”
    """
    t = (text or "").strip()
    if t in DEVICE_LABEL_OPTIONS:
        return t
    # 尝试在文本中查找第一个出现的合法端标签
    for opt in DEVICE_LABEL_OPTIONS:
        if opt in t:
            return opt
    return "无法判断"


def parse_brand_safety_from_response(text: str) -> str:
    """
    从模型回复中解析「品牌安全(AI)」：
    - 严格按 system_prompt_pinpai，只允许“是”或“否”
    - 解析规则：非空且明确为“是”时标为“是”，否则一律视为“否”
    """
    t = (text or "").strip()
    if t == "是":
        return "是"
    return "否"


def parse_content_safety_from_response(text: str) -> str:
    """
    从模型回复中解析「内容安全(AI)」：
    - 严格按 system_prompt_content，只允许“是”或“否”
    - 非空且明确为“是”时标为“是”，否则一律视为“否”
    """
    t = (text or "").strip()
    if t == "是":
        return "是"
    return "否"


def ensure_annotation_fields(token: str, existing_field_names: List[str]) -> None:
    """确保多维表中存在「类型（机器）」「评价情感（机器）」「是否提及竞品(机器)」「端(机器)」「品牌安全(AI)」「内容安全(AI)」字段。"""
    if not BITABLE_URL:
        raise RuntimeError("BITABLE_URL 未配置")
    app_token, table_id = parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    existing = set(existing_field_names)
    for field_name in ("类型（机器）", "评价情感（机器）", "是否提及竞品(机器)", "端(机器)", "品牌安全(AI)", "内容安全(AI)"):
        if field_name in existing:
            continue
        payload = {"field_name": field_name, "type": 1}
        resp = get_session().post(url, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"创建字段「{field_name}」失败: {data}")


def get_feishu_field_names(token: str) -> List[str]:
    if not BITABLE_URL:
        raise RuntimeError("BITABLE_URL 未配置")
    app_token, table_id = parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields"
    headers = {"Authorization": f"Bearer {token}"}
    params: Dict[str, Any] = {}
    names: List[str] = []

    while True:
        resp = get_session().get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取字段列表失败: {data}")
        items = (data.get("data") or {}).get("items") or []
        for item in items:
            n = item.get("field_name")
            if isinstance(n, str):
                names.append(n)
        page_token = (data.get("data") or {}).get("page_token")
        has_more = (data.get("data") or {}).get("has_more")
        if not has_more or not page_token:
            break
        params["page_token"] = page_token

    return names


def fetch_records_missing_label(token: str, limit: int) -> List[Dict[str, Any]]:
    """拉取「类型（机器）」「评价情感（机器）」「是否提及竞品(机器)」「端(机器)」「品牌安全(AI)」「内容安全(AI)」为空、需要标注的记录。"""
    if not BITABLE_URL:
        raise RuntimeError("BITABLE_URL 未配置")
    app_token, table_id = parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {"Authorization": f"Bearer {token}"}
    params: Dict[str, Any] = {"page_size": min(500, limit * 2)}
    result: List[Dict[str, Any]] = []

    while len(result) < limit:
        resp = get_session().get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取记录失败: {data}")
        obj = data.get("data") or {}
        items = obj.get("items") or []
        for rec in items:
            fields = rec.get("fields") or {}
            if FORCE_RELABEL:
                need_label = True
            else:
                need_type = not _safe_text(fields.get("类型（机器）"))
                need_emotion = not _safe_text(fields.get("评价情感（机器）"))
                need_competitor = not _safe_text(fields.get("是否提及竞品(机器)"))
                need_device = not _safe_text(fields.get("端(机器)"))
                need_brand_safety = not _safe_text(fields.get("品牌安全(AI)"))
                need_content_safety = not _safe_text(fields.get("内容安全(AI)"))
                need_label = need_type or need_emotion or need_competitor or need_device or need_brand_safety or need_content_safety
            if need_label:
                result.append(rec)
                if len(result) >= limit:
                    return result
        if not obj.get("has_more") or not obj.get("page_token"):
            break
        params["page_token"] = obj["page_token"]

    return result


def batch_update_records(token: str, updates: List[Dict[str, Any]]) -> None:
    """批量更新记录，每项为 {"record_id": xxx, "fields": {"类型（机器）": "...", "评价情感（机器）": "...", "是否提及竞品(机器)": "是/否", "端(机器)": "<端标签>", "品牌安全(AI)": "是/否", "内容安全(AI)": "是/否"}}"""
    if not updates:
        return
    if not BITABLE_URL:
        raise RuntimeError("BITABLE_URL 未配置")
    app_token, table_id = parse_bitable_url(BITABLE_URL)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {"records": updates}
    resp = get_session().post(
        url,
        headers=headers,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"批量更新失败: {data}")


def run_once() -> int:
    if not BITABLE_URL:
        raise RuntimeError("请设置环境变量 BITABLE_URL（飞书多维表链接）")

    token = get_tenant_access_token()
    field_names = get_feishu_field_names(token)
    ensure_annotation_fields(token, field_names)

    records = fetch_records_missing_label(token, LIMIT)
    if not records:
        if FORCE_RELABEL:
            print("没有可标注的记录（表为空）。")
        else:
            print("没有需要标注的记录（「类型（机器）」与「评价情感（机器）」均已填写）。如需强制重新标注，请设置 FORCE_RELABEL=1。")
        return 0

    # 仅输出提示词模式：每条记录输出 2 行——第 1 行类型提示词，第 2 行情感提示词；OpenClaw 用对应 SYSTEM_PROMPT 调模型后，stdin 按同样顺序传入 2*N 行结果
    if OUTPUT_PROMPTS_ONLY:
        for rec in records:
            fields = rec.get("fields") or {}
            print(build_user_prompt(fields))
            print(build_emotion_user_prompt(fields))
        return 0

    # 检查必填的OpenAI配置
    missing = []
    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")
    if not OPENAI_BASE_URL:
        missing.append("OPENAI_BASE_URL")
    if not OPENAI_MODEL:
        missing.append("OPENAI_MODEL")
    if missing:
        raise RuntimeError(f"标注skill需要配置OpenAI，缺失必填环境变量: {', '.join(missing)}。请在run_yuqing_pipeline.sh中添加配置后重试。")

    # 获取每条记录的类型/情感/竞品/端/品牌安全/内容安全标签：
    # 现在三个参数都必须配置，直接启用内部调用
    use_internal_llm = True

    results_raw: List[Tuple[str, str, str, str, str, str]] = [("", "", "", "", "", "") for _ in records]

    if use_internal_llm:
        def _task(idx_and_rec: Tuple[int, Dict[str, Any]]) -> Tuple[int, str, str, str, str, str, str]:
            idx, rec = idx_and_rec
            fields = rec.get("fields") or {}
            user_prompt = build_user_prompt(fields)
            emotion_prompt = build_emotion_user_prompt(fields)
            competitor_prompt = build_competitor_user_prompt(fields)
            device_prompt = build_device_user_prompt(fields)
            brand_safety_prompt = build_brand_safety_user_prompt(fields)
            content_safety_prompt = build_content_safety_user_prompt(fields)
            try:
                type_raw = call_llm(SYSTEM_PROMPT, user_prompt)
                emotion_raw = call_llm(SYSTEM_PROMPT_EMOTION, emotion_prompt)
                competitor_raw = call_llm(SYSTEM_PROMPT_COMPETITOR, competitor_prompt)
                device_raw = call_llm(SYSTEM_PROMPT_DEVICE, device_prompt)
                brand_safety_raw = call_llm(SYSTEM_PROMPT_BRAND_SAFETY, brand_safety_prompt)
                content_safety_raw = call_llm(SYSTEM_PROMPT_CONTENT_SAFETY, content_safety_prompt)
            except Exception as e:
                record_id = rec.get("record_id")
                print(f"  [{idx+1}] record_id={record_id} 调用模型失败: {e}")
                type_raw, emotion_raw, competitor_raw, device_raw, brand_safety_raw, content_safety_raw = "", "", "", "", "", ""
            return idx, type_raw, emotion_raw, competitor_raw, device_raw, brand_safety_raw, content_safety_raw

        with ThreadPoolExecutor(max_workers=max(1, LLM_CONCURRENCY)) as executor:
            futures = [
                executor.submit(_task, (idx, rec))
                for idx, rec in enumerate(records)
            ]
            completed = 0
            total = len(futures)
            for fut in as_completed(futures):
                completed += 1
                idx, type_raw, emotion_raw, competitor_raw, device_raw, brand_safety_raw, content_safety_raw = fut.result()
                results_raw[idx] = (type_raw, emotion_raw, competitor_raw, device_raw, brand_safety_raw, content_safety_raw)
                # 每 10 条报告一次进度（方便用户跟踪）
                if completed % 10 == 0:
                    print(f"\n✅ 进度：已完成 {completed}/{total} 条标注\n", flush=True)
    else:
        stdin_lines = [ln.strip() for ln in sys.stdin] if not sys.stdin.isatty() else []
        for i in range(len(records)):
            base = 6 * i
            type_raw = stdin_lines[base] if base < len(stdin_lines) else ""
            emotion_raw = stdin_lines[base + 1] if base + 1 < len(stdin_lines) else ""
            competitor_raw = stdin_lines[base + 2] if base + 2 < len(stdin_lines) else ""
            device_raw = stdin_lines[base + 3] if base + 3 < len(stdin_lines) else ""
            brand_safety_raw = stdin_lines[base + 4] if base + 4 < len(stdin_lines) else ""
            content_safety_raw = stdin_lines[base + 5] if base + 5 < len(stdin_lines) else ""
            results_raw[i] = (type_raw, emotion_raw, competitor_raw, device_raw, brand_safety_raw, content_safety_raw)

    updates: List[Dict[str, Any]] = []
    for i, rec in enumerate(records):
        record_id = rec.get("record_id")
        if not record_id:
            continue
        type_raw, emotion_raw, competitor_raw, device_raw, brand_safety_raw, content_safety_raw = results_raw[i]
        label = parse_label_from_response(type_raw)
        if label not in LABEL_OPTIONS:
            label = "无关"
        emotion = parse_emotion_from_response(emotion_raw)
        if emotion not in EMOTION_LABEL_OPTIONS:
            emotion = "中立"
        competitor_flag = parse_competitor_flag_from_response(competitor_raw)
        if competitor_flag not in COMPETITOR_FLAG_OPTIONS:
            competitor_flag = "否"
        device_label = parse_device_label_from_response(device_raw)
        if device_label not in DEVICE_LABEL_OPTIONS:
            device_label = "无法判断"
        brand_safety = parse_brand_safety_from_response(brand_safety_raw)
        if brand_safety not in BRAND_SAFETY_OPTIONS:
            brand_safety = "否"
        content_safety = parse_content_safety_from_response(content_safety_raw)
        if content_safety not in CONTENT_SAFETY_OPTIONS:
            content_safety = "否"
        updates.append({
            "record_id": record_id,
            "fields": {
                "类型（机器）": label,
                "评价情感（机器）": emotion,
                "是否提及竞品(机器)": competitor_flag,
                "端(机器)": device_label,
                "品牌安全(AI)": brand_safety,
                "内容安全(AI)": content_safety,
            },
        })
        print(
            f"  [{i+1}/{len(records)}] record_id={record_id} -> "
            f"类型（机器）={label} | 评价情感（机器）={emotion} | "
            f"是否提及竞品(机器)={competitor_flag} | 端(机器)={device_label} | 品牌安全(AI)={brand_safety}"
        )

    batch_update_records(token, updates)
    print(f"已写回 {len(updates)} 条记录的「类型（机器）」与「评价情感（机器）」")
    return len(updates)


def main() -> None:
    try:
        n = run_once()
        print(json.dumps({"updated_count": n}, ensure_ascii=False))
    except Exception as e:
        print(f"执行失败: {e}")
        raise


if __name__ == "__main__":
    main()
