#!/usr/bin/env python3
"""
网大登录工具模块
提供填充手机号、获取验证码、填充短信验证码并登录的功能
"""

import asyncio
import json
import os
import re
import sys
import urllib.request
from collections import Counter

import websockets
from dotenv import load_dotenv

load_dotenv(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"), override=True
)

msg_id = 1


def validate_phone(phone):
    """校验手机号格式，返回 (是否有效, 错误信息)"""
    if not phone:
        return False, "手机号不能为空"
    if not re.match(r"^1\d{10}$", phone):
        return False, "手机号格式错误：必须是11位数字且以1开头"
    return True, None


async def get_page_texts(ws, timeout=2):
    """获取页面上的所有文本内容"""
    expr = """
    (() => {
        const texts = [];
        const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        let node;
        while (node = walker.nextNode()) {
            const text = node.textContent.trim();
            if (text && text.length > 0) {
                texts.push(text);
            }
        }
        return texts;
    })()
    """
    result = await evaluate(ws, expr)
    return result or []


async def check_send_result(ws, wait_seconds=3):
    """
    检查验证码发送结果
    返回: (成功, 消息)
    成功: True/False/None(不确定)
    """
    # 错误提示关键词（按优先级排序）
    error_patterns = [
        (r"操作频繁", "操作过于频繁，请稍后再试"),
        (r"请.*后再试", "请等待后再试"),
        (r"(\d+)s.*后.*重试", "验证码发送过于频繁"),
        (r"(\d+)秒.*后.*重试", "验证码发送过于频繁"),
        (r"发送失败", "验证码发送失败"),
        (r"请输入正确的手机号", "手机号格式错误"),
        (r"手机号.*错误", "手机号格式错误"),
        (r"格式.*错误", "手机号格式错误"),
        (r"系统.*忙", "系统繁忙"),
        (r"网络.*错误", "网络错误"),
    ]

    success_patterns = [
        r"验证码.*已发送",
        r"验证码.*发送成功",
        r"短信.*已发送",
    ]

    # 频繁检查，捕获toast提示（每0.1秒检查一次，更频繁）
    check_count = int(wait_seconds / 0.1)
    last_btn_text = None
    for i in range(check_count):
        await asyncio.sleep(0.1)

        texts = await get_page_texts(ws)
        texts_str = " ".join(texts)

        # 先检查错误
        for pattern, msg in error_patterns:
            if re.search(pattern, texts_str):
                return False, msg

        # 再检查成功
        for pattern in success_patterns:
            if re.search(pattern, texts_str):
                return True, "验证码发送成功"

    # 如果没有检测到成功或错误toast，检查按钮状态变化
    # 获取当前按钮文本
    expr = """
    (() => {
        const buttons = Array.from(document.querySelectorAll('button, .el-button, a, span, div, [class*="code"], [class*="verify"]'));
        for (const btn of buttons) {
            const text = (btn.textContent || '').trim();
            if (text && (text.includes('验证码') || /^\\d+\\s*[s秒]/.test(text))) {
                return text;
            }
        }
        return null;
    })()
    """
    btn_text = await evaluate(ws, expr)

    # 如果按钮显示倒计时数字（如"120s"、"70秒"），可能是SMS或SIM的倒计时
    if btn_text and re.search(r"^(\d+)\s*[s秒]", btn_text):
        seconds = re.search(r"^(\d+)", btn_text).group(1)
        seconds_int = int(seconds)
        # SMS冷却期通常是60-120秒，SIM认证也是120秒
        # 检查页面上是否有"验证码已发送至"的提示来确认是SMS
        check_sms_expr = """
        (() => {
            const allText = document.body.innerText || '';
            return allText.includes('验证码已发送至') || allText.includes('验证码已发送');
        })()
        """
        is_sms_sent = await evaluate(ws, check_sms_expr)

        if is_sms_sent:
            return False, f"验证码发送过于频繁，请等待{seconds}秒后再试"
        else:
            # 可能是SIM认证的倒计时，不确定SMS状态
            return None, f"检测到倒计时{btn_text}，但未确认SMS发送状态"

    # 按钮仍显示"获取验证码"，说明可能点击没生效
    if btn_text and "获取验证码" in btn_text:
        return None, "按钮仍显示获取验证码，发送可能未生效"

    return None, "未检测到发送结果"


async def call(ws, method, params=None):
    """发送CDP命令并等待响应"""
    global msg_id
    req_id = msg_id
    msg_id += 1
    req = {"id": req_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(req))
    while True:
        try:
            resp_str = await asyncio.wait_for(ws.recv(), 5)
            resp = json.loads(resp_str)
            if resp.get("id") == req_id:
                return resp.get("result", {})
        except asyncio.TimeoutError:
            return None


async def evaluate(ws, expression):
    """在页面执行JavaScript表达式"""
    res = await call(
        ws, "Runtime.evaluate", {"expression": expression, "returnByValue": True}
    )
    if res and "result" in res:
        return res["result"].get("value")
    return None


async def find_leaf_text_center(ws, text):
    """查找包含指定文本的叶子元素中心坐标"""
    expr = f"""
    (() => {{
        let els = Array.from(document.body.querySelectorAll('*'));
        let el = els.find(e => e.offsetHeight > 0 && e.innerText && e.innerText.trim() === '{text}' && e.children.length === 0);
        if (!el) el = els.find(e => e.offsetHeight > 0 && e.innerText && e.innerText.includes('{text}') && e.children.length === 0);
        if (!el) return null;
        let r = el.getBoundingClientRect();
        return {{x: r.x, y: r.y, w: r.width, h: r.height}};
    }})()
    """
    rect = await evaluate(ws, expr)
    if rect:
        return rect["x"] + rect["w"] / 2, rect["y"] + rect["h"] / 2
    return None


async def find_css_center(ws, selector):
    """查找CSS选择器匹配的元素中心坐标"""
    expr = f"""
    (() => {{
        let el = document.querySelector("{selector}");
        if (!el) return null;
        let r = el.getBoundingClientRect();
        return {{x: r.x, y: r.y, w: r.width, h: r.height}};
    }})()
    """
    rect = await evaluate(ws, expr)
    if rect:
        return rect["x"] + rect["w"] / 2, rect["y"] + rect["h"] / 2
    return None


async def mouse_click(ws, x, y):
    """模拟鼠标点击"""
    await call(
        ws,
        "Input.dispatchMouseEvent",
        {"type": "mousePressed", "x": x, "y": y, "button": "left", "clickCount": 1},
    )
    await asyncio.sleep(0.05)
    await call(
        ws,
        "Input.dispatchMouseEvent",
        {"type": "mouseReleased", "x": x, "y": y, "button": "left", "clickCount": 1},
    )


async def type_text(ws, text):
    """模拟输入文本"""
    for char in text:
        await call(ws, "Input.dispatchKeyEvent", {"type": "char", "text": char})
        await asyncio.sleep(0.05)


async def clear_input(ws):
    """清空输入框（发送退格键）"""
    for _ in range(12):
        await call(
            ws,
            "Input.dispatchKeyEvent",
            {"type": "rawKeyDown", "windowsVirtualKeyCode": 8},
        )
        await call(
            ws, "Input.dispatchKeyEvent", {"type": "keyUp", "windowsVirtualKeyCode": 8}
        )


async def check_all_checkboxes(ws):
    """勾选页面上所有复选框"""
    await evaluate(
        ws,
        """
        Array.from(document.querySelectorAll('input[type="checkbox"]')).forEach(cb => {
            if(!cb.checked){
                cb.click();
                cb.checked=true;
                cb.dispatchEvent(new Event('change', {bubbles: true}));
            }
        })
    """,
    )


async def get_websocket(debug_port):
    """获取网大页面的WebSocket连接"""
    with urllib.request.urlopen(f"http://localhost:{debug_port}/json") as response:
        pages = json.loads(response.read().decode())
    target = next((p for p in pages if "wangda" in p.get("url", "")), None)
    if not target:
        raise RuntimeError("未找到网大页面")
    return await websockets.connect(target["webSocketDebuggerUrl"], max_size=None)


def get_current_url_sync(debug_port):
    """同步获取当前页面URL"""
    try:
        with urllib.request.urlopen(f"http://localhost:{debug_port}/json") as response:
            pages = json.loads(response.read().decode())
        target = next((p for p in pages if "wangda" in p.get("url", "")), None)
        if target:
            return target.get("url")
        return None
    except Exception:
        return None


# ========== 员工姓名提取相关函数（从chrome_tools_old.py移植）==========


def _attributes_to_dict(attributes):
    attrs = attributes or []
    return {
        str(attrs[i]).lower(): str(attrs[i + 1]) for i in range(0, len(attrs) - 1, 2)
    }


def _normalize_text(text):
    return re.sub(r"\s+", " ", text or "").strip()


def _walk_dom_nodes(node, ancestors=None):
    ancestors = ancestors or []
    yield node, ancestors
    for child in node.get("children") or []:
        yield from _walk_dom_nodes(child, ancestors + [node])


def _looks_like_person_name(text):
    cleaned = text.replace("·", "").replace("•", "")
    if not 2 <= len(cleaned) <= 4:
        return False
    if re.search(r"\d|https?://|[A-Za-z]", text):
        return False
    return bool(re.fullmatch(r"[\u4e00-\u9fff]{2,4}", cleaned))


def _collect_text_candidates(root):
    candidates = []
    for node, ancestors in _walk_dom_nodes(root):
        if node.get("nodeType") != 3:
            continue

        text = _normalize_text(node.get("nodeValue"))
        if not text:
            continue

        context_parts = []
        for ancestor in ancestors[-6:]:
            attrs = _attributes_to_dict(ancestor.get("attributes"))
            context_parts.extend(
                [
                    ancestor.get("nodeName", ""),
                    ancestor.get("localName", ""),
                    attrs.get("class", ""),
                    attrs.get("id", ""),
                    attrs.get("name", ""),
                    attrs.get("data-name", ""),
                ]
            )

        candidates.append(
            {
                "text": text,
                "context": " ".join(filter(None, context_parts)).lower(),
            }
        )
    return candidates


def _score_name_candidate(text, context, frequency):
    score = 0

    if _looks_like_person_name(text):
        score += 8

    score += min(frequency * 3, 9)

    for token, weight in [
        ("user", 5),
        ("profile", 4),
        ("center/index", 4),
        ("base-info", 3),
        ("user-info", 3),
        ("user-title", 3),
        ("common-title", 3),
        ("h2", 2),
        ("text-overflow", 1),
        ("inline-block", 1),
    ]:
        if token in context:
            score += weight

    for token, weight in [
        ("item-name", 4),
        ("menu", 3),
        ("subject", 3),
        ("study", 3),
        ("notice", 2),
        ("interest", 2),
        ("tab", 2),
    ]:
        if token in context:
            score -= weight

    if any(keyword in text for keyword in ["平台", "学习", "课程", "首页", "专题"]):
        score -= 5
    if " " in text:
        score -= 2

    return score


def _extract_employee_name(document):
    root = document.get("result", {}).get("root") or document.get("root")
    if not root:
        return None

    candidates = _collect_text_candidates(root)
    if not candidates:
        return None

    name_like_counts = Counter(
        candidate["text"]
        for candidate in candidates
        if _looks_like_person_name(candidate["text"])
    )

    prioritized = []
    for candidate in candidates:
        text = candidate["text"]
        context = candidate["context"]
        frequency = name_like_counts[text]
        if frequency == 0:
            continue
        prioritized.append(
            (
                _score_name_candidate(text, context, frequency),
                frequency,
                -len(text),
                text,
            )
        )

    if not prioritized:
        return None

    best_score, _, _, best_text = max(prioritized)
    if best_score < 8:
        return None

    return best_text


# ========== 主功能函数 ==========


async def find_verification_code_button(ws):
    """
    查找验证码按钮，区分正常状态和倒计时状态

    Returns:
        (类型, 坐标或文本)
        类型: 'ready'(可点击), 'countdown'(倒计时中), 'not_found'(未找到)
    """
    # 先获取所有可能的按钮文本，查找倒计时（纯数字+s，如"70s"）
    expr = """
    (() => {
        // 获取所有按钮和可点击元素的文本
        const elements = Array.from(document.querySelectorAll('button, .el-button, [class*="code"], [class*="verify"], a, span, div'));
        const texts = [];
        for (const el of elements) {
            const text = (el.textContent || el.innerText || '').trim();
            if (text && text.length > 0 && text.length < 50) {
                texts.push(text);
            }
        }
        return texts;
    })()
    """

    all_texts = await evaluate(ws, expr)
    if not all_texts:
        all_texts = []

    # 倒计时模式：纯数字+s（如"70s"）或数字+秒
    for text in all_texts:
        # 匹配 "70s"、"70s后重试"、"70秒"、"70秒后重试"
        if re.search(r"^\d+\s*[s秒]", text, re.IGNORECASE):
            match = re.search(r"(\d+)", text)
            seconds = match.group(1) if match else "若干"
            return "countdown", f"请等待{seconds}秒后再试"

    # 查找"获取验证码"按钮
    coords = await find_leaf_text_center(ws, "获取验证码")
    if coords:
        return "ready", coords

    # 如果没找到，尝试查找包含"获取验证码"的元素
    expr2 = """
    (() => {
        const allElements = Array.from(document.body.querySelectorAll('*'));
        for (const el of allElements) {
            const text = (el.textContent || '').trim();
            if (text.includes('获取验证码')) {
                const r = el.getBoundingClientRect();
                if (r.width > 0 && r.height > 0) {
                    return {x: r.x, y: r.y, w: r.width, h: r.height};
                }
            }
        }
        return null;
    })()
    """
    rect = await evaluate(ws, expr2)
    if rect:
        return "ready", (rect["x"] + rect["w"] / 2, rect["y"] + rect["h"] / 2)

    return "not_found", None


async def fill_phone(phone):
    """
    填充手机号并获取验证码

    Args:
        phone: 手机号

    Returns:
        发送验证码成功或失败

    Raises:
        Exception: 手机号格式错误、发送失败等情况
    """
    # 1. 校验手机号格式
    is_valid, error_msg = validate_phone(phone)
    if not is_valid:
        print(f"Error: {error_msg}")
        raise ValueError(error_msg)

    port = os.environ.get("_WANGDA_DEBUG_PORT")
    if not port:
        print("Error: _WANGDA_DEBUG_PORT环境变量未设置")
        raise Exception("未设置_WANGDA_DEBUG_PORT环境变量")

    try:
        async with await get_websocket(port) as ws:
            await call(ws, "DOM.enable")

            await asyncio.sleep(1)

            # 2. 点击短信验证登录标签
            coords = await find_leaf_text_center(ws, "短信验证登录")
            if coords:
                await mouse_click(ws, coords[0], coords[1])
                await asyncio.sleep(1)

            # 3. 点击并输入手机号
            coords = await find_css_center(
                ws, "input[maxlength='11'], input[placeholder*='手机']"
            )
            if not coords:
                coords = await find_css_center(ws, "input[type='text']")
            if coords:
                await mouse_click(ws, coords[0], coords[1])
                await asyncio.sleep(0.1)
                await clear_input(ws)
                await type_text(ws, phone)
                await asyncio.sleep(0.5)
            else:
                raise Exception("未找到手机号输入框")

            # 4. 勾选所有复选框
            await check_all_checkboxes(ws)
            await asyncio.sleep(0.5)

            # 5. 查找并点击获取验证码按钮
            # 先检查是否已经发送过验证码（通过查找成功提示文本）
            check_sent_expr = r"""
            (() => {
                const allText = document.body.innerText || '';
                // 严格匹配SMS发送成功的提示（包含"已发送至"）
                const hasSentMessage = allText.includes('验证码已发送至');

                if (hasSentMessage) {
                    // 查找倒计时数字
                    const matches = allText.match(/(\d+)\s*[s秒]/g);
                    if (matches) {
                        // 提取所有数字
                        const numbers = matches.map(m => parseInt(m.match(/(\d+)/)[1]));
                        // 找最小的那个（应该是SMS的倒计时，SIM认证通常是120秒固定）
                        if (numbers.length > 0) {
                            const minSeconds = Math.min(...numbers);
                            return {type: 'already_sent', seconds: minSeconds};
                        }
                    }
                    return {type: 'already_sent', seconds: null};
                }
                return {type: 'not_sent'};
            })()
            """
            sent_status = await evaluate(ws, check_sent_expr)

            # 调试：打印检测状态
            print(f"Debug: sent_status = {sent_status}", file=sys.stderr)

            # 检查是否已经发送过验证码
            if sent_status and sent_status.get("type") == "already_sent":
                seconds = sent_status.get("seconds")
                if seconds is not None and seconds > 0:
                    # 倒计时还在进行中，确实需要等待
                    raise Exception(f"验证码发送过于频繁，请等待{seconds}秒后再试")
                else:
                    # 倒计时已结束（seconds为None或0），页面残留旧文本
                    # 需要刷新页面后重新操作
                    print("Debug: 倒计时已结束，刷新页面后重新发送", file=sys.stderr)
                    await evaluate(ws, "location.reload()")
                    await asyncio.sleep(3)  # 等待页面重新加载

                    # 重新执行：点击短信验证登录标签
                    coords = await find_leaf_text_center(ws, "短信验证登录")
                    if coords:
                        await mouse_click(ws, coords[0], coords[1])
                        await asyncio.sleep(1)

                    # 重新执行：点击并输入手机号
                    coords = await find_css_center(
                        ws, "input[maxlength='11'], input[placeholder*='手机']"
                    )
                    if not coords:
                        coords = await find_css_center(ws, "input[type='text']")
                    if coords:
                        await mouse_click(ws, coords[0], coords[1])
                        await asyncio.sleep(0.1)
                        await clear_input(ws)
                        await type_text(ws, phone)
                        await asyncio.sleep(0.5)
                    else:
                        raise Exception("刷新后未找到手机号输入框")

                    # 重新执行：勾选复选框
                    await check_all_checkboxes(ws)
                    await asyncio.sleep(0.5)

            # 检查按钮状态（在输入手机号之后，点击之前）
            expr = """
            (() => {
                const buttons = Array.from(document.querySelectorAll('button, .el-button, a, span, div, [class*="btn"], [class*="button"]'));
                for (const btn of buttons) {
                    const text = (btn.textContent || btn.innerText || '').trim();
                    // 匹配倒计时格式：数字+s/秒（如"39s"、"120秒"），后面可能有"后重试"等
                    const countdownMatch = text.match(/^(\\d+)\\s*([s秒])(?:后?重?试?)?$/);
                    if (countdownMatch) {
                        return {type: 'countdown', seconds: countdownMatch[1], text: text};
                    }
                    if (text.includes('获取验证码')) {
                        return {type: 'ready', text: text};
                    }
                }
                return {type: 'unknown', text: ''};
            })()
            """
            btn_status = await evaluate(ws, expr)

            # 检查是否检测到倒计时
            if btn_status and btn_status.get("type") == "countdown":
                seconds = btn_status.get("seconds", "0")
                raise Exception(f"验证码发送过于频繁，请等待{seconds}秒后再试")

            # 检查是否是正常状态
            if btn_status and btn_status.get("type") == "ready":
                # 按钮是正常状态，尝试点击
                coords = await find_leaf_text_center(ws, "获取验证码")
                if not coords:
                    # 备用：通过JavaScript点击
                    click_expr = """
                    (() => {
                        const buttons = Array.from(document.querySelectorAll('button, .el-button, a, span'));
                        for (const btn of buttons) {
                            const text = (btn.textContent || '').trim();
                            if (text.includes('获取验证码')) {
                                btn.click();
                                return true;
                            }
                        }
                        return false;
                    })()
                    """
                    clicked = await evaluate(ws, click_expr)
                    if not clicked:
                        raise Exception("未找到获取验证码按钮")
                else:
                    await mouse_click(ws, coords[0], coords[1])
            else:
                # 未知状态，尝试查找倒计时（可能检测漏了）
                check_expr = """
                (() => {
                    const allText = document.body.innerText || '';
                    const match = allText.match(/(\\d+)\\s*[s秒]\\s*后?重?试?/);
                    return match ? match[1] : null;
                })()
                """
                seconds = await evaluate(ws, check_expr)
                if seconds:
                    raise Exception(f"验证码发送过于频繁，请等待{seconds}秒后再试")
                raise Exception("未找到获取验证码按钮")

            # 6. 立即开始检测发送结果
            success, msg = await check_send_result(ws, wait_seconds=3)

            if success is True:
                print(f"发送验证码成功: {msg}")
                return True
            elif success is False:
                raise Exception(msg)
            else:
                # 无法确定结果，根据提示信息判断
                if "倒计时" in msg:
                    # 有倒计时，可能是发送成功了（toast没检测到）
                    print(f"警告: {msg}")
                    print("按钮已变成倒计时，可能发送成功，请检查手机短信")
                    return True
                else:
                    # 真的不确定，抛出异常
                    raise Exception(f"无法确定发送结果: {msg}")

    except Exception as e:
        raise e


async def check_login_result(ws, port, wait_seconds=3):
    """
    检查登录结果

    Returns:
        (是否成功, 消息)
    """
    await asyncio.sleep(wait_seconds)

    # 1. 检查当前URL是否还在登录页面
    current_url = get_current_url_sync(port)
    if current_url and "login" not in current_url:
        # URL不包含login，说明已经跳转，登录成功
        return True, "登录成功"

    # 2. 获取页面文本，查找错误提示
    texts = await get_page_texts(ws)
    texts_str = " ".join(texts)

    # 登录失败的错误提示
    error_patterns = [
        (r"验证码.*错误", "验证码错误"),
        (r"验证码.*失效", "验证码已失效，请重新获取"),
        (r"验证码.*过期", "验证码已过期，请重新获取"),
        (r"验证码.*不正确", "验证码不正确"),
        (r"验证码.*无效", "验证码无效"),
        (r"登录.*失败", "登录失败"),
        (r"账号.*不存在", "账号不存在"),
        (r"用户.*不存在", "用户不存在"),
        (r"手机号.*错误", "手机号错误"),
        (r"手机号.*格式", "手机号格式错误"),
        (r"请先.*验证码", "请先获取验证码"),
        (r"请.*验证码", "请输入验证码"),
    ]

    for pattern, msg in error_patterns:
        if re.search(pattern, texts_str):
            return False, msg

    # 3. 检查是否还在登录页面（URL包含login）
    if current_url and "login" in current_url:
        # 还在登录页面，但没看到明确错误，可能是登录中或未知错误
        return False, "登录失败，请检查验证码是否正确"

    return None, "无法确定登录结果"


async def fill_sms_code(code):
    """
    填充短信验证码并登录

    Args:
        code: 短信验证码

    Returns:
        登录成功或失败

    Raises:
        Exception: 登录失败或操作出错
    """
    # 校验验证码格式：必须是6位数字
    if not code or not re.match(r"^\d{6}$", code):
        raise Exception("验证码格式错误：必须是6位数字")

    port = os.environ.get("_WANGDA_DEBUG_PORT")
    if not port:
        raise Exception("_WANGDA_DEBUG_PORT环境变量未设置")

    async with await get_websocket(port) as ws:
        await call(ws, "DOM.enable")

        # 1. 点击验证码输入框并输入
        coords = await find_css_center(ws, "input[placeholder*='短信验证码']")
        if not coords:
            coords = await find_css_center(ws, "input[placeholder*='验证码']")

        if coords:
            await mouse_click(ws, coords[0], coords[1])
            await asyncio.sleep(0.1)
            # 清空已有内容
            for _ in range(6):
                await call(
                    ws,
                    "Input.dispatchKeyEvent",
                    {"type": "rawKeyDown", "windowsVirtualKeyCode": 8},
                )
                await call(
                    ws,
                    "Input.dispatchKeyEvent",
                    {"type": "keyUp", "windowsVirtualKeyCode": 8},
                )
            await type_text(ws, code)
            await asyncio.sleep(0.5)
        else:
            raise Exception("未找到验证码输入框")

        # 2. 确保所有复选框已勾选
        await check_all_checkboxes(ws)
        await asyncio.sleep(0.5)

        # 3. 点击登录按钮
        coords = await find_leaf_text_center(ws, "登录")
        if not coords:
            raise Exception("未找到登录按钮")

        await mouse_click(ws, coords[0], coords[1])

        # 4. 等待并校验登录结果
        success, msg = await check_login_result(ws, port, wait_seconds=3)

        if success is True:
            print(msg)
            return True
        else:
            raise Exception(msg)


async def get_employee_name():
    """
    登录成功后,获取登录的员工信息

    Returns:
        员工姓名
    """
    port = os.environ.get("_WANGDA_DEBUG_PORT")
    if not port:
        print("Error: _WANGDA_DEBUG_PORT环境变量未设置")
        sys.exit(1)

    # 1. 获取当前页面URL
    current_url = get_current_url_sync(port)
    if not current_url:
        print("Error: 无法获取当前页面URL")
        sys.exit(1)

    profile_url = "https://wangda.chinamobile.com/#/center/index"

    try:
        async with await get_websocket(port) as ws:
            await call(ws, "DOM.enable")

            # 2. 跳转到个人中心页面（如果不是已经在该页面）
            if current_url != profile_url:
                await call(ws, "Page.navigate", {"url": profile_url})
                await asyncio.sleep(3)

            # 3. 获取页面DOM
            doc_result = await call(ws, "DOM.getDocument", {"depth": -1})
            if not doc_result:
                print("Error: 无法获取页面DOM")
                raise Exception("无法获取页面DOM")

            # 4. 提取员工姓名
            employee_name = _extract_employee_name(doc_result)
            if not employee_name:
                print("Error: 无法从页面中提取员工姓名")
                raise Exception("无法从页面中提取员工姓名")

            print(employee_name)

            # 5. 恢复原来的页面
            if current_url != profile_url:
                await call(ws, "Page.navigate", {"url": current_url})

            return employee_name

    except Exception as e:
        print(f"Error: {e}")
        raise e


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="网大登录工具")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    fill_phone_cmd = subparsers.add_parser(
        "fill-phone", help="填充手机号至登录页面,并发送验证码"
    )
    fill_phone_cmd.add_argument("phone_number", type=str, help="手机号")

    fill_sms_cmd = subparsers.add_parser(
        "fill-sms-code", help="填充验证码至登录页面,并尝试登录"
    )
    fill_sms_cmd.add_argument("code", type=str, help="短信验证码")

    subparsers.add_parser("get-employee-name", help="登录成功后,获取登录的员工信息")

    args = parser.parse_args()

    if args.command == "fill-phone":
        try:
            asyncio.run(fill_phone(args.phone_number))
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    elif args.command == "fill-sms-code":
        try:
            asyncio.run(fill_sms_code(args.code))
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    elif args.command == "get-employee-name":
        try:
            asyncio.run(get_employee_name())
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        parser.print_help()
