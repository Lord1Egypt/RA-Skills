# -*- coding: utf-8 -*-
"""
从飞书多维表中按用户规则筛选记录，将格式化后的内容推送到指定的群机器人 Webhook。

状态字段约定：
- 使用多维表字段「是否推送」作为单一状态字段：
  - 空：尚未判断
  - 不推送：已判断，不符合推送条件
  - 待推送：本次命中推送条件，准备推送
  - 已推送：已成功推送

本 Skill 每次仅扫描「是否推送」为空的记录，避免重复推送。
"""
import json
import os
import sys
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse, parse_qs

import requests

PUSH_FLAG_FIELD = "是否推送"
PUSH_FLAG_VALUE_NO = "不推送"
PUSH_FLAG_VALUE_PENDING = "待推送"
PUSH_FLAG_VALUE_DONE = "已推送"


def _env(key: str, default: str = "") -> str:
    return os.getenv(f"INPUT_{key.upper()}", os.getenv(key, default)).strip()


def _env_int(key: str, default: int) -> int:
    try:
        return int(_env(key, str(default)))
    except ValueError:
        return default


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


def get_session() -> requests.Session:
    return requests.Session()


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": app_id, "app_secret": app_secret}
    resp = get_session().post(url, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"获取飞书 token 失败: {data}")
    return data["tenant_access_token"]


def fetch_records(bitable_url: str, token: str, limit: int) -> List[Dict[str, Any]]:
    app_token, table_id = parse_bitable_url(bitable_url)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {"Authorization": f"Bearer {token}"}
    params: Dict[str, Any] = {"page_size": min(500, limit)}
    result: List[Dict[str, Any]] = []

    while len(result) < limit:
        resp = get_session().get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取记录失败: {data}")
        obj = data.get("data") or {}
        items = obj.get("items") or []
        result.extend(items)
        if len(result) >= limit:
            break
        if not obj.get("has_more") or not obj.get("page_token"):
            break
        params["page_token"] = obj["page_token"]

    return result[:limit]


def eval_rule(rule_expression: str, fields: Dict[str, Any]) -> bool:
    """
    使用受限 eval 计算用户规则表达式。
    - rule_expression 是一个 Python 表达式，需返回 True/False
    - 可用变量：fields（dict），建议使用 fields.get('字段名', '')
    """
    safe_globals = {"__builtins__": {}}
    safe_locals = {"fields": fields}
    try:
        return bool(eval(rule_expression, safe_globals, safe_locals))
    except Exception:
        return False


def render_message(template: str, fields: Dict[str, Any]) -> str:
    """按模板渲染纯文本（可嵌入到卡片某一块中）。"""
    class DefaultDict(dict):
        def __missing__(self, key):
            return ""

    flat_fields = DefaultDict()
    for k, v in fields.items():
        if isinstance(v, list):
            flat_fields[k] = ", ".join(str(x) for x in v)
        else:
            flat_fields[k] = str(v)
    try:
        return template.format_map(flat_fields)
    except Exception:
        return template


def send_to_webhook(webhook_url: str, fields: Dict[str, Any], message_template: str) -> None:
    """以飞书交互卡片（interactive card）的形式推送一条消息。"""
    title = str(fields.get("标题", "")) if fields.get("标题") is not None else ""
    emotion = str(fields.get("评价情感（机器）", "")) if fields.get("评价情感（机器）") is not None else ""
    content_type = str(fields.get("类型（机器）", "")) if fields.get("类型（机器）") is not None else ""
    brand_safety = str(fields.get("品牌安全(AI)", "")) if fields.get("品牌安全(AI)") is not None else ""
    content_safety = str(fields.get("内容安全(AI)", "")) if fields.get("内容安全(AI)") is not None else ""
    body = str(fields.get("正文", "")) if fields.get("正文") is not None else ""
    url = str(fields.get("原文 URL", "")) if fields.get("原文 URL") is not None else ""

    # 可选：在卡片中增加一块“自定义描述”，由 message_template 渲染
    extra_text = render_message(message_template, fields) if message_template else ""

    # 根据情感/安全状态选择卡片颜色
    if brand_safety == "是" or content_safety == "是":
        template_color = "red"
    elif emotion == "负向":
        template_color = "orange"
    elif emotion == "正向":
        template_color = "turquoise"
    else:
        template_color = "blue"

    card_title = f"舆情预警：{title[:40]}" if title else "舆情预警"

    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": True,
                "enable_forward": True,
            },
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": card_title,
                },
                "template": template_color,
            },
            "elements": [
                {
                    "tag": "div",
                    "fields": [
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**情感**：{emotion or '-'}",
                            },
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**类型**：{content_type or '-'}",
                            },
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**品牌安全**：{brand_safety or '-'}",
                            },
                        },
                        {
                            "is_short": True,
                            "text": {
                                "tag": "lark_md",
                                "content": f"**内容安全**：{content_safety or '-'}",
                            },
                        },
                    ],
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**标题：**{title or '-'}",
                    },
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content": f"**正文摘录：**{(body or '-')[:200]}",
                    },
                },
            ],
        },
    }

    # 若用户提供了 message_template，在卡片末尾追加一块“附加信息”
    if extra_text.strip():
        payload["card"]["elements"].append(
            {
                "tag": "hr",
            }
        )
        payload["card"]["elements"].append(
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": extra_text,
                },
            }
        )

    # 加上“查看原文”按钮（若有链接）
    if url:
        payload["card"]["elements"].append(
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": "查看原文",
                        },
                        "url": url,
                        "type": "primary",
                    }
                ],
            }
        )

    resp = get_session().post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=10,
    )
    resp.raise_for_status()


def mark_records(
    bitable_url: str,
    token: str,
    record_ids: List[str],
    value: str,
) -> None:
    """将记录在多维表中按「是否推送」字段打标。"""
    if not record_ids:
        return
    app_token, table_id = parse_bitable_url(bitable_url)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    records = [
        {"record_id": rid, "fields": {PUSH_FLAG_FIELD: value}}
        for rid in record_ids
    ]
    payload = {"records": records}
    resp = get_session().post(
        url,
        headers=headers,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"标记记录失败: {data}")


def main() -> None:
    bitable_url = _env("bitable_url")
    app_id = _env("app_id")
    app_secret = _env("app_secret")
    webhook_url = _env("webhook_url")
    rule_expression = _env("rule_expression")
    message_template = _env("message_template")
    limit = _env_int("limit", 50)

    if not all([bitable_url, app_id, app_secret, webhook_url, rule_expression, message_template]):
        print(
            "missing_required=bitable_url,app_id,app_secret,webhook_url,rule_expression,message_template",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        token = get_tenant_access_token(app_id, app_secret)
        records = fetch_records(bitable_url, token, limit)

        no_push_ids: List[str] = []
        to_push_ids: List[str] = []
        success_ids: List[str] = []
        pushed = 0

        # 为后续快速根据 record_id 拿到 fields 构建映射
        fields_map: Dict[str, Dict[str, Any]] = {}
        for rec in records:
            rid = rec.get("record_id")
            if not rid:
                continue
            fields_map[rid] = rec.get("fields") or {}

        # 1) 只扫描「是否推送」为空的记录，根据规则划分为 不推送 / 待推送
        for rid, fields in fields_map.items():
            flag_val = fields.get(PUSH_FLAG_FIELD)
            if isinstance(flag_val, list):
                flag_text = ",".join(str(x) for x in flag_val)
            else:
                flag_text = str(flag_val) if flag_val is not None else ""
            if flag_text:  # 已经有状态的记录（不推送/待推送/已推送）全部跳过
                continue

            if not eval_rule(rule_expression, fields):
                no_push_ids.append(rid)
                continue

            to_push_ids.append(rid)

        # 2) 先把待推送记录标记为「待推送」
        if to_push_ids:
            mark_records(bitable_url, token, to_push_ids, PUSH_FLAG_VALUE_PENDING)

        # 3) 对待推送记录逐条发送
        for rid in to_push_ids:
            fields = fields_map.get(rid, {})
            send_to_webhook(webhook_url, fields, message_template)
            pushed += 1
            success_ids.append(rid)

        # 4) 标记状态：不推送 / 已推送
        if no_push_ids:
            mark_records(bitable_url, token, no_push_ids, PUSH_FLAG_VALUE_NO)
        if success_ids:
            mark_records(bitable_url, token, success_ids, PUSH_FLAG_VALUE_DONE)

        print(f"pushed_count={pushed}")
    except Exception as e:
        print(f"push_error={e}", file=sys.stderr)
        print("pushed_count=0")
        sys.exit(1)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
从飞书多维表中按用户规则筛选记录，将格式化后的内容推送到指定的群机器人 Webhook。

使用方式：
- 由 OpenClaw 注入 INPUT_* 环境变量（见 SKILL.md 中 inputs）
- 支持两种使用场景：
  1）只关注最近一批增量记录（建议在同步+标注后立刻调用，配合视图过滤）
  2）在多维表视图中提前用筛选条件限制候选记录，再由 rule_expression 做精细过滤
"""
import json
import os
import sys
from typing import Any, Dict, List, Tuple
from urllib.parse import urlparse, parse_qs

import requests


def _env(key: str, default: str = "") -> str:
    return os.getenv(f"INPUT_{key.upper()}", os.getenv(key, default)).strip()


def _env_int(key: str, default: int) -> int:
    try:
        return int(_env(key, str(default)))
    except ValueError:
        return default


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


def get_session() -> requests.Session:
    session = requests.Session()
    return session


def get_tenant_access_token(app_id: str, app_secret: str) -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    payload = {"app_id": app_id, "app_secret": app_secret}
    resp = get_session().post(url, json=payload, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"获取飞书 token 失败: {data}")
    return data["tenant_access_token"]


def fetch_records(bitable_url: str, token: str, limit: int) -> List[Dict[str, Any]]:
    app_token, table_id = parse_bitable_url(bitable_url)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    headers = {"Authorization": f"Bearer {token}"}
    params: Dict[str, Any] = {"page_size": min(500, limit)}
    result: List[Dict[str, Any]] = []

    while len(result) < limit:
        resp = get_session().get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if data.get("code") != 0:
            raise RuntimeError(f"获取记录失败: {data}")
        obj = data.get("data") or {}
        items = obj.get("items") or []
        result.extend(items)
        if len(result) >= limit:
            break
        if not obj.get("has_more") or not obj.get("page_token"):
            break
        params["page_token"] = obj["page_token"]

    return result[:limit]


def eval_rule(rule_expression: str, fields: Dict[str, Any]) -> bool:
    """
    使用受限 eval 计算用户规则表达式。
    - rule_expression 是一个 Python 表达式，需返回 True/False
    - 可用变量：fields（dict），建议使用 fields.get('字段名', '')
    """
    safe_globals = {"__builtins__": {}}
    safe_locals = {"fields": fields}
    try:
        return bool(eval(rule_expression, safe_globals, safe_locals))
    except Exception:
        return False


def render_message(template: str, fields: Dict[str, Any]) -> str:
    class DefaultDict(dict):
        def __missing__(self, key):
            return ""

    flat_fields = DefaultDict()
    for k, v in fields.items():
        if isinstance(v, list):
            flat_fields[k] = ", ".join(str(x) for x in v)
        else:
            flat_fields[k] = str(v)
    try:
        return template.format_map(flat_fields)
    except Exception:
        return template


def send_to_webhook(webhook_url: str, text: str) -> None:
    payload = {
        "msg_type": "text",
        "content": {"text": text},
    }
    resp = get_session().post(
        webhook_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=10,
    )
    resp.raise_for_status()


def mark_pushed_records(
    bitable_url: str,
    token: str,
    record_ids: List[str],
    push_flag_field: str,
    push_flag_value: str,
) -> None:
    """将已推送的记录在多维表中打标，避免下次重复推送。"""
    if not record_ids:
        return
    app_token, table_id = parse_bitable_url(bitable_url)
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/batch_update"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    records = [
        {"record_id": rid, "fields": {push_flag_field: push_flag_value}}
        for rid in record_ids
    ]
    payload = {"records": records}
    resp = get_session().post(
        url,
        headers=headers,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if data.get("code") != 0:
        raise RuntimeError(f"标记已推送记录失败: {data}")


def main() -> None:
    bitable_url = _env("bitable_url")
    app_id = _env("app_id")
    app_secret = _env("app_secret")
    webhook_url = _env("webhook_url")
    rule_expression = _env("rule_expression")
    message_template = _env("message_template")
    limit = _env_int("limit", 50)
    push_flag_field = _env("push_flag_field")
    push_flag_value = _env("push_flag_value", "已推送")

    if not all([bitable_url, app_id, app_secret, webhook_url, rule_expression, message_template]):
        print(
            "missing_required=bitable_url,app_id,app_secret,webhook_url,rule_expression,message_template",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        token = get_tenant_access_token(app_id, app_secret)
        records = fetch_records(bitable_url, token, limit)
        pushed = 0
        marked_ids: List[str] = []
        for rec in records:
            record_id = rec.get("record_id")
            fields = rec.get("fields") or {}
            # 若配置了 push_flag_field，且已标记为 push_flag_value，则跳过（避免重复推送）
            if push_flag_field:
                val = fields.get(push_flag_field)
                # 字段可能是单值或列表，这里统一转成字符串比较
                if isinstance(val, list):
                    flag_text = ",".join(str(x) for x in val)
                else:
                    flag_text = str(val) if val is not None else ""
                if flag_text == push_flag_value:
                    continue

            if not eval_rule(rule_expression, fields):
                continue
            text = render_message(message_template, fields)
            if not text.strip():
                continue
            send_to_webhook(webhook_url, text)
            pushed += 1
            if push_flag_field and record_id:
                marked_ids.append(record_id)

        # 推送完成后，对本次推送成功的记录打标记（若配置了 push_flag_field）
        if push_flag_field and marked_ids:
            mark_pushed_records(bitable_url, token, marked_ids, push_flag_field, push_flag_value)

        print(f"pushed_count={pushed}")
    except Exception as e:
        print(f"push_error={e}", file=sys.stderr)
        print("pushed_count=0")
        sys.exit(1)


if __name__ == "__main__":
    main()

