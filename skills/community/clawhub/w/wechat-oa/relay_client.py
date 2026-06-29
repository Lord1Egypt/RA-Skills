#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
wechat-oa relay client
中转模式客户端：将文章推送到公网服务器，由服务器转发至微信公众号平台
支持 AI 收（Alipay Aipay）支付流程
"""

import sys
import os
import json
import re
import base64
import requests
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"


def _fix_garbled(obj):
    """
    修复双重编码乱码（UTF-8 字节被误当作 Latin-1 解码）
    
    问题示例：
    - 原文 "女" → UTF-8 字节 E5 A5 B3
    - 服务器误当作 Latin-1 解码 → "å¥³"（乱码）
    - 需要修复：把 "å¥³" 还原回 "女"
    
    Args:
        obj: 任意对象（str, dict, list 等）
    
    Returns:
        修复后的对象
    """
    if isinstance(obj, str):
        result = obj
        # Step 1: 修复 Latin-1 双重编码乱码
        # 原文 "女" → UTF-8 字节 E5 A5 B3 → 误当作 Latin-1 解码 → "å¥³"
        try:
            result = result.encode('latin-1').decode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            pass
        # Step 2: 修复 \\uXXXX 双转义 Unicode（JSON 序列化时反斜杠被再次转义）
        # 服务端返回 \u5b69（字面反斜杠+u），需要还原为实际字符
        result = re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), result)
        return result
    elif isinstance(obj, dict):
        return {k: _fix_garbled(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_fix_garbled(item) for item in obj]
    else:
        return obj


def _truncate_digest(digest: str, max_units: int = 120) -> str:
    """
    截断 digest 以满足微信公众号 API 限制。

    微信规则：
      - 中文字符（汉字、中文标点、Emoji、全角符号）= 1 单位
      - 英文/数字/半角标点/空格 = 0.5 单位
      - 总校验公式：中文字符数 + (英文字符数 ÷ 2) ≤ 120
    """
    if not digest:
        return ""
    result = []
    used = 0.0
    for ch in digest:
        code = ord(ch)
        if (
            0x4E00 <= code <= 0x9FFF
            or 0x3400 <= code <= 0x4DBF
            or 0x20000 <= code <= 0x2A6DF
            or 0x2A700 <= code <= 0x2B73F
            or 0x2B740 <= code <= 0x2B81F
            or 0x2B820 <= code <= 0x2CEAF
            or 0xF900 <= code <= 0xFAFF
            or 0xFF00 <= code <= 0xFFEF
            or 0x3000 <= code <= 0x303F
            or 0x1F300 <= code <= 0x1FAFF
        ):
            cost = 1.0
        else:
            cost = 0.5
        if used + cost > max_units + 1e-9:
            break
        result.append(ch)
        used += cost
    return "".join(result)


def load_config():
    """从 config.json 加载配置"""
    default_config = {
        "APP_ID": "",
        "APP_SECRET": "",
        "author": "Woody",
        "PUSH_MODE": "direct",
        "WECHAT_OA_SERVER": "http://120.79.2.44",
        "WECHAT_OA_SERVER_KEY": "",
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            return {**default_config, **user_config}
        except Exception:
            return default_config
    return default_config


def _get_cfg_params(api_key: str, relay_server: str) -> tuple:
    """统一读取配置参数"""
    cfg = load_config()
    if not api_key:
        api_key = cfg.get("WECHAT_OA_SERVER_KEY", "")
    if not relay_server:
        relay_server = cfg.get("WECHAT_OA_SERVER", "http://120.79.2.44")
    return api_key, relay_server.rstrip('/'), cfg


def _post(url: str, payload: dict, api_key: str, timeout: int = 30) -> dict:
    """POST 请求封装，统一错误处理"""
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }
    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), timeout=timeout)
        # 捕获标准 HTTP 402（AI 付协议）
        if resp.status_code == 402:
            return {
                "status_code": 402,
                "payment_needed": resp.headers.get("Payment-Needed", ""),
                "body": resp.text,
            }
        resp.raise_for_status()
        return _fix_garbled(resp.json())
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"网络请求失败: {e}"}
    except json.JSONDecodeError:
        return {"success": False, "error": f"服务器返回非 JSON 数据: {resp.text[:200]}"}


def _put(url: str, payload: dict, api_key: str, timeout: int = 30) -> dict:
    """PUT 请求封装，统一错误处理"""
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
    }
    try:
        resp = requests.put(url, headers=headers, data=json.dumps(payload, ensure_ascii=False).encode('utf-8'), timeout=timeout)
        resp.raise_for_status()
        return _fix_garbled(resp.json())
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"网络请求失败: {e}"}
    except json.JSONDecodeError:
        return {"success": False, "error": f"服务器返回非 JSON 数据: {resp.text[:200]}"}


def _get(url: str, params: dict, api_key: str, timeout: int = 15) -> dict:
    """GET 请求封装，统一错误处理"""
    headers = {"X-API-Key": api_key}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=timeout)
        resp.raise_for_status()
        return _fix_garbled(resp.json())
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"网络请求失败: {e}"}
    except json.JSONDecodeError:
        return {"success": False, "error": f"服务器返回非 JSON 数据"}


# ════════════════════════════════════════════════════════════════════════════
# AI 收流程：info → order → execute
# ════════════════════════════════════════════════════════════════════════════

def get_push_info(api_key: str = "", relay_server: str = "") -> dict:
    """
    获取推送服务信息（是否收费、价格等）
    
    Returns:
        dict: {
            "service_name": "公众号文章推送",
            "description": "...",
            "price": {"amount": 0.01, "currency": "CNY", "unit": "per_request"},
            "charge_enabled": False,
            ...
        }
    """
    api_key, relay_server, _ = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    url = f"{relay_server}/api/push/article/info"
    return _get(url, {}, api_key)


def create_push_order(title: str = "", content: str = "", author: str = "", digest: str = "",
                      thumb_path: str = None, api_key: str = "", relay_server: str = "") -> dict:
    """
    创建推送订单，获取 Payment-Needed（收费模式）
    
    Args:
        title: 文章标题
        content: 文章正文 HTML
        author: 作者
        digest: 摘要
        thumb_path: 封面图本地路径（可选）
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址
    
    Returns:
        dict: {
            "success": True,
            "order_id": "PA_...",
            "status": "order_created",
            "amount": 0.01,
            "currency": "CNY",
            "payment_needed": "base64url_encoded_json...",  # Payment-Needed
            "payment_method": "alipay_aipay",
            ...
        }
    """
    api_key, relay_server, cfg = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    digest = _truncate_digest(digest)

    # 构建请求体（包含服务端必填字段）
    payload = {
        "appid": cfg.get("APP_ID", ""),
        "appsecret": cfg.get("APP_SECRET", ""),
        "title": title,
        "content": content,
        "author": author or cfg.get("author", "Woody"),
        "digest": digest,
    }

    # 封面图：读取并 base64 编码
    if thumb_path and os.path.exists(thumb_path):
        try:
            with open(thumb_path, 'rb') as f:
                img_data = f.read()
            payload["thumb_image"] = base64.b64encode(img_data).decode('utf-8')
            payload["thumb_filename"] = os.path.basename(thumb_path)
        except Exception as e:
            print(f"[WARN] 封面图读取失败，将继续无封面创建订单: {e}")

    url = f"{relay_server}/api/push/article/order"
    result = _post(url, payload, api_key)
    
    # 统一包装返回格式：服务端成功返回时添加 success 标记
    if "error" in result and not result.get("success"):
        return result  # 保持错误格式
    if "order_id" in result:
        result["success"] = True
    return result


def execute_push_article(title: str, content: str, order_id: str,
                         payment_proof: str = "", mock_pay: bool = False,
                         author: str = "", digest: str = "",
                         thumb_path: str = None, api_key: str = "",
                         relay_server: str = "") -> dict:
    """
    执行推送文章到公众号草稿箱（带订单验证）
    
    Args:
        title: 文章标题
        content: 文章正文 HTML
        order_id: 订单号（由 create_push_order 创建）
        payment_proof: 支付凭证（收费模式必填，mock_pay 可跳过）
        mock_pay: 是否模拟支付（调试模式，跳过真实支付验证）
        author: 作者
        digest: 摘要
        thumb_path: 封面图本地路径（可选，会 base64 编码后发送）
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址
    
    Returns:
        dict: {"success": True/False, "media_id": "...", "message": "..."}
    """
    api_key, relay_server, cfg = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    digest = _truncate_digest(digest)

    # 构建请求体
    payload = {
        "appid": cfg.get("APP_ID", ""),
        "appsecret": cfg.get("APP_SECRET", ""),
        "title": title,
        "content": content,
        "author": author or cfg.get("author", "Woody"),
        "digest": digest,
        "order_id": order_id,
        "payment_proof": payment_proof,
        "mock_pay": mock_pay,
    }

    # 封面图：读取并 base64 编码
    if thumb_path and os.path.exists(thumb_path):
        try:
            with open(thumb_path, 'rb') as f:
                img_data = f.read()
            payload["thumb_image"] = base64.b64encode(img_data).decode('utf-8')
            payload["thumb_filename"] = os.path.basename(thumb_path)
        except Exception as e:
            print(f"[WARN] 封面图读取失败，将继续无封面推送: {e}")

    url = f"{relay_server}/api/push/article"
    result = _post(url, payload, api_key)

    if result.get("success"):
        return {"success": True, "media_id": result.get("media_id", ""), "message": result.get("message", "")}
    else:
        return {"success": False, "error": result.get("error", "未知错误")}


# ════════════════════════════════════════════════════════════════════════════
# 兼容旧版：一站式推送（自动判断免费/收费模式）
# ════════════════════════════════════════════════════════════════════════════

def _extract_trade_no(output: str) -> str:
    """从 alipay-bot 输出中提取 trade_no"""
    import re
    match = re.search(r'交易号\s*[:：]\s*(\d{32})', output)
    if match:
        return match.group(1)
    match = re.search(r'tradeNo["\']?\s*[:=]\s*["\']?(\d{32})', output)
    if match:
        return match.group(1)
    return ""


def _inline_css(html):
    """
    简单的 CSS 内联转换（无外部依赖）。
    从 HTML 的 <style> 标签提取 CSS 规则，将样式内联到对应元素的 style 属性中。
    支持：标签选择器、class 选择器、tag.class 组合。
    """
    css_map = {}

    def parse_rules(css_text):
        for block in css_text.split('}'):
            block = block.strip()
            if not block or '{' not in block:
                continue
            selector, _, props = block.partition('{')
            selector = selector.strip()
            props = props.strip().rstrip(';')
            if not selector or not props:
                continue
            # 跳过伪类、属性选择器、ID 选择器
            first = selector.split()[0]
            if ':' in first or '[' in first or '#' in selector:
                continue
            css_map[selector] = props

    html = re.sub(
        r'<style[^>]*>(.*?)</style>',
        lambda m: (parse_rules(m.group(1)), '')[1],
        html,
        flags=re.DOTALL
    )

    if not css_map:
        return html

    def tag_replacer(m):
        raw = m.group(0)
        if raw.startswith('</'):
            return raw
        tag_m = re.match(r'</?([a-zA-Z][a-zA-Z0-9-]*)', raw)
        if not tag_m:
            return raw
        tag = tag_m.group(1).lower()
        after = raw[tag_m.end():]
        # 找到第一个不在引号内的 >
        i, in_quote, quote_char = 0, False, None
        while i < len(after):
            c = after[i]
            if not in_quote and c in ('"', "'"):
                in_quote, quote_char = True, c
            elif in_quote and c == quote_char:
                in_quote, quote_char = False, None
            elif not in_quote and c == '>':
                break
            i += 1
        attrs_str = after[:i]
        trailing_slash = ''
        if attrs_str.rstrip().endswith('/'):
            trailing_slash = '/'
            attrs_str = attrs_str.rstrip()[:-1]

        cls_match = re.search(r'class=["\']([^"\']+)["\']', attrs_str)
        cls = cls_match.group(1).split()[0] if cls_match else ""

        applied = []
        key = f"{tag}.{cls}" if cls else None
        if key and key in css_map:
            applied.append(css_map[key])
        if cls and f".{cls}" in css_map:
            applied.append(css_map[f".{cls}"])
        if tag in css_map:
            applied.append(css_map[tag])

        existing = re.search(r'style=["\']([^"\']*)["\']', attrs_str)
        if existing:
            applied.insert(0, existing.group(1))

        new_style = "; ".join(applied).rstrip("; ")
        if new_style:
            attrs_str = re.sub(r'\s*style=["\'][^"\']*["\']', '', attrs_str)
            attrs_str = attrs_str + f' style="{new_style}"'

        return f"<{tag}{attrs_str}{trailing_slash}>"

    return re.sub(r'</?[a-zA-Z][a-zA-Z0-9-]*(?:\s+[^>]*)?/?>', tag_replacer, html)


def push_article(title: str, content: str, author: str = "", digest: str = "",
                 thumb_path: str = None, api_key: str = "", relay_server: str = "") -> dict:
    """
    一站式推送文章到公众号草稿箱（通过中转服务器）
    
    兼容模式：自动检测是否收费
    - 免费模式：直接推送
    - 收费模式：返回标准 HTTP 402 的 Payment-Needed，调用 alipay-bot 支付
    
    Args:
        title: 文章标题
        content: 文章正文 HTML
        author: 作者
        digest: 摘要（建议 AI 生成 1-2 句概括；留空则服务端自动提取第一段正文）
        thumb_path: 封面图本地路径（可选，会 base64 编码后发送）
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址（如 http://120.79.2.44）
    
    Returns:
        dict: 免费模式: {"success": True, "media_id": "..."}
              收费模式: {"success": False, "charge_required": True, "trade_no": "...", "alipay_bot_output": "..."}
              失败: {"success": False, "error": "..."}
    """
    import subprocess
    import time

    api_key, relay_server, cfg = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    digest = _truncate_digest(digest)

    # CSS 内联：把 <style> 标签的样式内联到元素的 style 属性中
    # 这样微信 API 过滤掉 <style> 标签后，内联样式仍然生效
    content = _inline_css(content)

    # 构建请求体
    payload = {
        "appid": cfg.get("APP_ID", ""),
        "appsecret": cfg.get("APP_SECRET", ""),
        "title": title,
        "content": content,
        "author": author or cfg.get("author", "Woody"),
        "digest": digest or "",  # 空字符串让服务端 fallback 提取
    }

    # 封面图：读取并 base64 编码
    if thumb_path and os.path.exists(thumb_path):
        try:
            with open(thumb_path, 'rb') as f:
                img_data = f.read()
            payload["thumb_image"] = base64.b64encode(img_data).decode('utf-8')
            payload["thumb_filename"] = os.path.basename(thumb_path)
        except Exception as e:
            print(f"[WARN] 封面图读取失败，将继续无封面推送: {e}")

    url = f"{relay_server}/api/push/article"
    result = _post(url, payload, api_key)

    # 标准 HTTP 402：需要支付
    if result.get("status_code") == 402:
        payment_needed = result.get("payment_needed", "")
        if not payment_needed:
            return {"success": False, "error": "服务端返回 402 但未提供 Payment-Needed"}

        # 保存 Payment-Needed 到文件
        file_name = f"402_needed_{int(time.time())}.txt"
        file_path = f"/tmp/{file_name}"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(payment_needed)
        except Exception as e:
            return {"success": False, "error": f"保存 Payment-Needed 失败: {e}"}

        # 调用 alipay-bot 发起支付
        try:
            proc = subprocess.run(
                ["alipay-bot", "--", "402-buyer-pay", "-f", file_path],
                capture_output=True, text=True, timeout=60
            )
            output = proc.stdout + proc.stderr
            if proc.returncode != 0 and not output:
                output = proc.stderr or "alipay-bot 执行失败"
        except Exception as e:
            return {"success": False, "error": f"调用 alipay-bot 失败: {e}"}

        # 提取 trade_no
        trade_no = _extract_trade_no(output)

        return {
            "success": False,
            "charge_required": True,
            "trade_no": trade_no,
            "payment_needed_file": file_path,
            "payload": payload,
            "alipay_bot_output": output,
            "message": "请扫码完成支付，支付完成后告诉我'已支付'，我将继续推送",
        }

    # 正常返回
    if result.get("success"):
        return {"success": True, "media_id": result.get("media_id", ""), "message": result.get("message", "")}
    else:
        return {"success": False, "error": result.get("error", "未知错误")}


def finish_push(trade_no: str, payload: dict, api_key: str = "", relay_server: str = "") -> dict:
    """
    支付完成后，查询支付状态并自动重试推送
    
    Args:
        trade_no: 交易号（从 alipay-bot 输出中提取）
        payload: 文章推送的请求体（从 push_article 返回的 payload 中传入）
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址
    
    Returns:
        dict: {"success": True/False, "media_id": "...", "message": "..."}
    """
    import subprocess

    api_key, relay_server, _ = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}
    if not trade_no:
        return {"success": False, "error": "trade_no 不能为空"}

    resource_url = f"{relay_server}/api/push/article"
    data = json.dumps(payload)

    # 调用 alipay-bot 查询支付状态并自动重试（携带 Payment-Proof）
    try:
        proc = subprocess.run(
            [
                "alipay-bot", "402-query-payment-status",
                "-t", trade_no,
                "-r", resource_url,
                "-m", "POST",
                "-d", data,
                "-H", f"X-API-Key:{api_key}",
            ],
            capture_output=True, text=True, timeout=60
        )
        output = proc.stdout + proc.stderr
    except Exception as e:
        return {"success": False, "error": f"调用 alipay-bot 查询失败: {e}"}

    # 解析 alipay-bot 输出
    try:
        result = json.loads(output)
    except json.JSONDecodeError:
        # 可能不是 JSON，尝试从文本中提取
        return {
            "success": False,
            "error": f"alipay-bot 返回非 JSON 数据: {output[:500]}",
        }

    if not result.get("success"):
        return {
            "success": False,
            "error": result.get("errorMsg", "支付查询失败"),
        }

    # 提取资源响应
    resource_resp = result.get("resourceResponse", {})
    if resource_resp.get("status") == 200:
        body = resource_resp.get("body", {})
        if body.get("success") or body.get("media_id"):
            return {
                "success": True,
                "media_id": body.get("media_id", ""),
                "message": body.get("message", "推送成功"),
            }
        return {"success": False, "error": body.get("error", "推送失败")}
    else:
        return {
            "success": False,
            "error": f"资源请求失败: HTTP {resource_resp.get('status', '未知')}",
        }


# ════════════════════════════════════════════════════════════════════════════
# 列出草稿箱（通过中转服务器）
# ════════════════════════════════════════════════════════════════════════════

def list_drafts(count: int = 10, offset: int = 0, api_key: str = "", relay_server: str = "") -> dict:
    """
    列出公众号草稿箱（通过中转服务器）
    
    Args:
        count: 拉取数量（最大 20）
        offset: 偏移量
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址
    
    Returns:
        dict: {"success": True/False, "drafts": [...], "total": N}
    """
    api_key, relay_server, cfg = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    params = {
        "appid": cfg.get("APP_ID", ""),
        "appsecret": cfg.get("APP_SECRET", ""),
        "count": min(count, 20),
        "offset": offset,
    }

    url = f"{relay_server}/api/push/drafts"
    return _get(url, params, api_key)


# ════════════════════════════════════════════════════════════════════════════
# 更新草稿（通过中转服务器）
# ════════════════════════════════════════════════════════════════════════════

def update_draft(media_id: str, title: str, content: str, author: str = "", digest: str = "",
                    thumb_path: str = None, thumb_media_id: str = "",
                    api_key: str = "", relay_server: str = "") -> dict:
    """
    更新已有草稿（通过中转服务器）

    Args:
        media_id: 草稿 media_id
        title: 文章标题
        content: 文章正文 HTML（应已内联 CSS）
        author: 作者
        digest: 摘要
        thumb_path: 封面图本地路径（有则上传，无则用 thumb_media_id）
        thumb_media_id: 已有 thumb_media_id（直接使用，不上传新封面）
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址

    Returns:
        dict: {"success": True/False, "message": "..."}
    """
    api_key, relay_server, cfg = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    digest = _truncate_digest(digest)

    # CSS 内联：把 <style> 标签的样式内联到元素的 style 属性中
    content = _inline_css(content)

    # 构建请求体
    payload = {
        "appid": cfg.get("APP_ID", ""),
        "appsecret": cfg.get("APP_SECRET", ""),
        "title": title,
        "content": content,
        "author": author or cfg.get("author", "Woody"),
        "digest": digest,
    }

    # 封面图：优先用 thumb_path 上传新封面，其次用已有的 thumb_media_id
    if thumb_path and os.path.exists(thumb_path):
        try:
            with open(thumb_path, 'rb') as f:
                img_data = f.read()
            payload["thumb_image"] = base64.b64encode(img_data).decode('utf-8')
            payload["thumb_filename"] = os.path.basename(thumb_path)
        except Exception as e:
            print(f"[WARN] 封面图读取失败: {e}")
    elif thumb_media_id:
        payload["thumb_media_id"] = thumb_media_id

    url = f"{relay_server}/api/push/article/{media_id}"
    result = _put(url, payload, api_key, timeout=30)

    if result.get("success"):
        return {"success": True, "message": result.get("message", "更新成功")}
    else:
        return {"success": False, "error": result.get("error", "未知错误")}


# ════════════════════════════════════════════════════════════════════════════
# 删除草稿（通过中转服务器）
# ════════════════════════════════════════════════════════════════════════════

def delete_draft(media_id: str, api_key: str = "", relay_server: str = "") -> dict:
    """
    删除草稿（通过中转服务器）

    Args:
        media_id: 草稿 media_id
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址

    Returns:
        dict: {"success": True/False, "message": "..."}
    """
    api_key, relay_server, cfg = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    params = {
        "appid": cfg.get("APP_ID", ""),
        "appsecret": cfg.get("APP_SECRET", ""),
    }

    headers = {"X-API-Key": api_key}
    url = f"{relay_server}/api/push/article/{media_id}"

    try:
        resp = requests.delete(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        if result.get("success"):
            return {"success": True, "message": result.get("message", "删除成功")}
        else:
            return {"success": False, "error": result.get("error", "未知错误")}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"网络请求失败: {e}"}
    except json.JSONDecodeError:
        return {"success": False, "error": f"服务器返回非 JSON 数据: {resp.text[:200]}"}


# ════════════════════════════════════════════════════════════════════════════
# 搜索草稿（通过中转服务器）
# ════════════════════════════════════════════════════════════════════════════

def search_drafts(keyword: str, count: int = 20, offset: int = 0,
                 api_key: str = "", relay_server: str = "") -> dict:
    """
    按标题关键词搜索草稿（通过中转服务器）

    Args:
        keyword: 搜索关键词
        count: 拉取数量
        offset: 偏移量
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址

    Returns:
        dict: {"success": True/False, "drafts": [...], "total": N}
    """
    api_key, relay_server, cfg = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    params = {
        "appid": cfg.get("APP_ID", ""),
        "appsecret": cfg.get("APP_SECRET", ""),
        "keyword": keyword,
        "count": min(count, 20),
        "offset": offset,
    }

    url = f"{relay_server}/api/push/drafts"
    return _get(url, params, api_key, timeout=15)


# ════════════════════════════════════════════════════════════════════════════
# 上传素材（通过中转服务器）
# ════════════════════════════════════════════════════════════════════════════

def upload_material(file_path: str, material_type: str = "image",
                   api_key: str = "", relay_server: str = "") -> dict:
    """
    上传永久素材（通过中转服务器）

    Args:
        file_path: 文件路径
        material_type: 素材类型（image/voice/video）
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址

    Returns:
        dict: {"success": True/False, "media_id": "...", "url": "..."}
    """
    api_key, relay_server, cfg = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    if not os.path.exists(file_path):
        return {"success": False, "error": f"文件不存在: {file_path}"}

    # 读取文件并 base64 编码
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
    except Exception as e:
        return {"success": False, "error": f"读取文件失败: {e}"}

    payload = {
        "appid": cfg.get("APP_ID", ""),
        "appsecret": cfg.get("APP_SECRET", ""),
        "material_type": material_type,
        "filename": os.path.basename(file_path),
        "file_data": base64.b64encode(file_data).decode('utf-8'),
    }

    url = f"{relay_server}/api/material/upload"
    result = _post(url, payload, api_key, timeout=60)

    if result.get("success"):
        return {
            "success": True,
            "media_id": result.get("media_id", ""),
            "url": result.get("url", ""),
        }
    else:
        return {"success": False, "error": result.get("error", "未知错误")}


# ════════════════════════════════════════════════════════════════════════════
# 获取素材总数（通过中转服务器）
# ════════════════════════════════════════════════════════════════════════════

def get_material_count(api_key: str = "", relay_server: str = "") -> dict:
    """
    获取各类永久素材总数（通过中转服务器）

    Args:
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址

    Returns:
        dict: {"success": True/False, "voice_count": N, "video_count": N, ...}
    """
    api_key, relay_server, cfg = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    params = {
        "appid": cfg.get("APP_ID", ""),
        "appsecret": cfg.get("APP_SECRET", ""),
    }

    url = f"{relay_server}/api/material/count"
    return _get(url, params, api_key, timeout=15)


# ════════════════════════════════════════════════════════════════════════════
# 获取素材列表（通过中转服务器）
# ════════════════════════════════════════════════════════════════════════════

def list_materials(material_type: str = "image", count: int = 20, offset: int = 0,
                  keyword: str = None, api_key: str = "", relay_server: str = "") -> dict:
    """
    批量获取永久素材列表（通过中转服务器）

    Args:
        material_type: 素材类型（image/video/voice/news）
        count: 每页数量
        offset: 偏移量
        keyword: 关键词过滤（可选，客户端侧过滤）
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址

    Returns:
        dict: {"success": True/False, "items": [...], "total": N}
    """
    api_key, relay_server, cfg = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    params = {
        "appid": cfg.get("APP_ID", ""),
        "appsecret": cfg.get("APP_SECRET", ""),
        "material_type": material_type,
        "count": min(count, 20),
        "offset": offset,
    }
    # 注意：服务器端的 list_materials() 不支持 keyword 参数
    # 如果需要关键词过滤，在客户端侧进行

    url = f"{relay_server}/api/materials"
    result = _get(url, params, api_key, timeout=15)
    
    # 客户端侧关键词过滤
    if keyword and result.get("success") and result.get("items"):
        filtered_items = []
        for item in result["items"]:
            if material_type == "news":
                for news_item in item.get("content", {}).get("news_item", []):
                    if keyword.lower() in news_item.get("title", "").lower():
                        filtered_items.append(item)
                        break
            else:
                if keyword.lower() in item.get("media_id", "").lower() or \
                   keyword.lower() in item.get("name", "").lower():
                    filtered_items.append(item)
        result["items"] = filtered_items
        result["total"] = len(filtered_items)
    
    return result


# ════════════════════════════════════════════════════════════════════════════
# 删除素材（通过中转服务器）
# ════════════════════════════════════════════════════════════════════════════

def delete_material(media_id: str, api_key: str = "", relay_server: str = "") -> dict:
    """
    删除永久素材（通过中转服务器）

    Args:
        media_id: 素材 media_id
        api_key: WECHAT_OA_SERVER_KEY
        relay_server: 中转服务器地址

    Returns:
        dict: {"success": True/False, "message": "..."}
    """
    api_key, relay_server, cfg = _get_cfg_params(api_key, relay_server)
    if not api_key:
        return {"success": False, "error": "未配置 WECHAT_OA_SERVER_KEY"}

    params = {
        "appid": cfg.get("APP_ID", ""),
        "appsecret": cfg.get("APP_SECRET", ""),
    }

    headers = {"X-API-Key": api_key}
    url = f"{relay_server}/api/material/{media_id}"

    try:
        resp = requests.delete(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        result = resp.json()
        if result.get("success"):
            return {"success": True, "message": result.get("message", "删除成功")}
        else:
            return {"success": False, "error": result.get("error", "未知错误")}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": f"网络请求失败: {e}"}
    except json.JSONDecodeError:
        return {"success": False, "error": f"服务器返回非 JSON 数据: {resp.text[:200]}"}


# ════════════════════════════════════════════════════════════════════════════
# CLI 入口（供命令行直接调用测试）
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="wechat-oa relay client")
    subparsers = parser.add_subparsers(dest="command")

    # push 子命令（兼容旧版）
    push_parser = subparsers.add_parser("push", help="推送文章到公众号草稿箱")
    push_parser.add_argument("html_path", help="HTML 文件路径")
    push_parser.add_argument("--title", default="", help="文章标题")
    push_parser.add_argument("--author", default="", help="作者")
    push_parser.add_argument("--digest", default="", help="摘要")
    push_parser.add_argument("--thumb", default="", help="封面图路径")
    push_parser.add_argument("--mock-pay", action="store_true", help="模拟支付（调试模式）")

    # info 子命令
    info_parser = subparsers.add_parser("info", help="查看推送服务信息")

    # order 子命令
    order_parser = subparsers.add_parser("order", help="创建推送订单")
    order_parser.add_argument("html_path", help="HTML 文件路径")
    order_parser.add_argument("--title", default="", help="文章标题")
    order_parser.add_argument("--author", default="", help="作者")
    order_parser.add_argument("--digest", default="", help="摘要")
    order_parser.add_argument("--thumb", default="", help="封面图路径")

    # execute 子命令
    execute_parser = subparsers.add_parser("execute", help="执行推送（需先创建订单）")
    execute_parser.add_argument("html_path", help="HTML 文件路径")
    execute_parser.add_argument("--order-id", required=True, help="订单号")
    execute_parser.add_argument("--payment-proof", default="", help="支付凭证")
    execute_parser.add_argument("--mock-pay", action="store_true", help="模拟支付（调试模式）")
    execute_parser.add_argument("--title", default="", help="文章标题")
    execute_parser.add_argument("--author", default="", help="作者")
    execute_parser.add_argument("--digest", default="", help="摘要")
    execute_parser.add_argument("--thumb", default="", help="封面图路径")

    # list 子命令
    list_parser = subparsers.add_parser("list", help="列出草稿箱")
    list_parser.add_argument("--count", type=int, default=10, help="拉取数量")
    list_parser.add_argument("--offset", type=int, default=0, help="偏移量")

    args = parser.parse_args()

    if args.command == "push":
        if not os.path.exists(args.html_path):
            print(f"[ERROR] 文件不存在: {args.html_path}")
            sys.exit(1)
        with open(args.html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        title = args.title or os.path.basename(args.html_path).replace('.html', '')
        result = push_article(title, content, args.author, args.digest, args.thumb or None)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if result.get("charge_required"):
            print(f"\n[提示] 收费模式：请完成支付后，告诉我'已支付'，我将继续推送")
            print(f"  trade_no: {result.get('trade_no', 'N/A')}")

    elif args.command == "info":
        result = get_push_info()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "order":
        if not os.path.exists(args.html_path):
            print(f"[ERROR] 文件不存在: {args.html_path}")
            sys.exit(1)
        with open(args.html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        title = args.title or os.path.basename(args.html_path).replace('.html', '')
        result = create_push_order(
            title=title, content=content, author=args.author, digest=args.digest,
            thumb_path=args.thumb or None,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "execute":
        if not os.path.exists(args.html_path):
            print(f"[ERROR] 文件不存在: {args.html_path}")
            sys.exit(1)
        with open(args.html_path, 'r', encoding='utf-8') as f:
            content = f.read()
        title = args.title or os.path.basename(args.html_path).replace('.html', '')
        result = execute_push_article(
            title=title, content=content, order_id=args.order_id,
            payment_proof=args.payment_proof, mock_pay=args.mock_pay,
            author=args.author, digest=args.digest, thumb_path=args.thumb or None,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "list":
        result = list_drafts(args.count, args.offset)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        parser.print_help()
