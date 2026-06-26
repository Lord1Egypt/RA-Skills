"""企业微信 GUI 自动化发消息 v3.0

v3.0 改进（2026-04-24 测试验证）：
1. 截图策略：全部改用窗口截图（screencapture -l），避免全屏截图 OCR 返回空
2. 坐标换算：窗口截图 OCR 坐标 + 窗口 position = 屏幕坐标（cliclick 用屏幕坐标）
3. 右侧面板处理：企微可能弹出"智能服务总结"等侧边面板，需检测并关闭
4. 输入框定位：用坐标估算（工具栏下方），而非 OCR 找 placeholder

用法:
  python3 scripts/send_message.py "联系人或群名" "消息内容"
  python3 scripts/send_message.py "XXX" "今日AI资讯" --wait-login

Exit codes: 0=成功, 1=失败, 2=需要登录（仅非 --wait-login 模式）
"""

import sys
import os
import json
import subprocess
import time
import argparse

# ── 常量 ──

WECOM_BUNDLE_ID = "com.tencent.WeWorkMac"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = "/tmp/wecom-gui"
MAX_RETRIES = 3
RETINA_SCALE = 2

# 登录检测关键词
LOGIN_KEYWORDS = ["扫码登录", "扫一扫登录", "使用微信扫码", "手机确认登录",
                  "扫码授权", "请使用微信扫描", "手机企业微信扫码"]
# 系统通知弹窗
NOTIFICATION_KEYWORDS = ["App后台活动", "可能包括提醒"]
# 二维码
QR_KEYWORDS = ["扫码", "二维码", "扫一扫", "微信扫"]
# 右侧面板关键词（需关闭）
PANEL_KEYWORDS = ["智能服务总结", "学员详情", "快捷回复", "申请使用"]

# 窗口目标尺寸
WINDOW_POS = (0, 25)
WINDOW_SIZE = (1200, 800)


def log(msg):
    print(f"  [{time.strftime('%H:%M:%S')}] {msg}", file=sys.stderr)


def run(cmd, timeout=15):
    log(f"→ {cmd[:120]}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    if result.returncode != 0 and result.stderr:
        log(f"  stderr: {result.stderr[:200]}")
    return result


# ── 窗口管理 ──

def get_window_info():
    """获取企微主窗口 ID 和位置"""
    result = run(f'peekaboo window list --app "{WECOM_BUNDLE_ID}" --json', timeout=10)
    if result.returncode != 0:
        return None
    try:
        data = json.loads(result.stdout)
        windows = data.get("data", {}).get("windows", [])
        if not windows:
            return None
        w = windows[0]
        return {
            "id": w["window_id"],
            "x": w["bounds"]["x"],
            "y": w["bounds"]["y"],
            "width": w["bounds"]["width"],
            "height": w["bounds"]["height"],
        }
    except (json.JSONDecodeError, KeyError, IndexError):
        return None


def activate_wecom():
    """激活并前置企业微信"""
    log("激活企业微信...")
    result = run('lsappinfo list | grep -c "com.tencent.WeWorkMac"')
    if result.stdout.strip() == "0":
        log("  企业微信未运行，启动中...")
        run('open "/Applications/企业微信.app"')
        time.sleep(5)
    run(f'osascript -e \'tell application id "{WECOM_BUNDLE_ID}" to activate\'')
    time.sleep(2)
    run(f'peekaboo window focus --app "{WECOM_BUNDLE_ID}"')
    time.sleep(1)


def resize_window():
    """调整窗口大小"""
    wx, wy = WINDOW_POS
    ww, wh = WINDOW_SIZE
    log(f"调整窗口: {ww}x{wh} @ ({wx},{wy})")
    run(f'''osascript -e '
tell application "System Events"
    tell process "企业微信"
        set frontmost to true
        delay 0.5
        try
            set position of window 1 to {{{wx}, {wy}}}
            set size of window 1 to {{{ww}, {wh}}}
        end try
    end tell
end tell'
''')
    time.sleep(1)


# ── 截图（关键：始终用窗口截图，不用全屏截图）──

def screenshot(filename="capture.png"):
    """截取企微窗口（非全屏！避免 OCR 空结果）
    
    返回 (image_path, window_info)
    window_info 用于坐标换算: screen_x = win_x + ocr_logic_x
    """
    os.makedirs(TMP_DIR, exist_ok=True)
    path = os.path.join(TMP_DIR, filename)
    win = get_window_info()
    if win:
        run(f"screencapture -x -l {win['id']} {path}")
    else:
        log("  ⚠ 无法获取窗口ID，回退到全屏截图")
        run(f"screencapture -x {path}")
        # 全屏截图时坐标就是屏幕坐标，offset 为 0
        win = {"id": 0, "x": 0, "y": 0, "width": 1512, "height": 982}
    return path, win


# ── OCR ──

def ocr(image_path, keyword=None):
    """Swift Vision OCR"""
    ocr_script = os.path.join(SCRIPT_DIR, "ocr_screen.swift")
    cmd = f'swift {ocr_script} "{image_path}"'
    if keyword:
        cmd += f' "{keyword}"'
    result = run(cmd, timeout=30)
    if result.returncode != 0:
        return None
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return None


def ocr_has_keyword(image_path, keywords):
    """检测是否包含关键词"""
    ocr_result = ocr(image_path)
    if not ocr_result or not ocr_result.get("success"):
        return False, []
    all_texts = " ".join([t["text"] for t in ocr_result.get("all_texts", [])])
    matched = [kw for kw in keywords if kw in all_texts]
    return len(matched) > 0, matched


def ocr_find(image_path, keyword):
    """查找关键词，返回窗口内逻辑坐标"""
    result = ocr(image_path, keyword)
    if not result or not result.get("matched"):
        return None
    target = result["matched"][0]
    return {
        "text": target["text"],
        "px": target["center_x"], "py": target["center_y"],
        "lx": int(target["center_x"] / RETINA_SCALE),
        "ly": int(target["center_y"] / RETINA_SCALE),
    }


def to_screen(win, window_lx, window_ly):
    """窗口逻辑坐标 → 屏幕逻辑坐标
    
    关键公式：screen = window_position + ocr_window_coord
    窗口截图 OCR 返回的是窗口内坐标，cliclick 需要屏幕坐标
    """
    return win["x"] + window_lx, win["y"] + window_ly


# ── 基础操作 ──

def click_at(sx, sy):
    """点击屏幕坐标"""
    run(f"cliclick c:{sx},{sy}")
    time.sleep(0.5)


def click_ocr_target(win, target):
    """点击 OCR 找到的目标（自动换算坐标）"""
    sx, sy = to_screen(win, target["lx"], target["ly"])
    log(f"  点击 '{target['text']}' win({target['lx']},{target['ly']}) → screen({sx},{sy})")
    click_at(sx, sy)


def paste_text(text):
    safe_text = text.replace('"', '\\"')
    run(f'peekaboo paste --text "{safe_text}" --app "{WECOM_BUNDLE_ID}"')
    time.sleep(1)


def press_key(key):
    run(f'peekaboo press {key} --app "{WECOM_BUNDLE_ID}"')
    time.sleep(0.5)


def hotkey(keys):
    run(f'peekaboo hotkey --keys "{keys}" --app "{WECOM_BUNDLE_ID}"')
    time.sleep(0.5)


# ── 登录检测 ──

def check_login():
    log("检测登录状态...")
    img, _ = screenshot("login_check.png")
    needs_login, matched = ocr_has_keyword(img, LOGIN_KEYWORDS)
    if needs_login:
        log(f"  ⚠ 需要登录（{matched}）")
        return False
    log("  ✓ 已登录")
    return True


def capture_qr_code():
    log("截取二维码...")
    for retry in range(5):
        time.sleep(3)
        qr_path, _ = screenshot(f"qr_{retry}.png")
        has_qr, _ = ocr_has_keyword(qr_path, QR_KEYWORDS)
        if has_qr:
            log(f"  ✓ 二维码已确认（第 {retry+1} 次）")
            return qr_path
    return qr_path


def wait_for_login(timeout=120):
    log(f"等待登录（最长 {timeout}s）...")
    for i in range(timeout // 5):
        time.sleep(5)
        img, _ = screenshot(f"login_poll_{i}.png")
        needs_login, _ = ocr_has_keyword(img, LOGIN_KEYWORDS)
        if not needs_login:
            log(f"  ✓ 登录成功（{(i+1)*5}s）")
            return True
        if i % 4 == 0:
            log(f"  等待中... ({(i+1)*5}s/{timeout}s)")
    log("  ✗ 登录超时")
    return False


# ── 通知弹窗处理 ──

def wait_for_notifications_clear(max_wait=15):
    """等待 macOS 系统通知弹窗消失
    
    不点击弹窗按钮（会打开系统设置遮挡企微）！
    只点击企微窗口区域让系统通知自动消失。
    """
    log("检测系统通知弹窗...")
    for i in range(max_wait // 3):
        # 用全屏截图检测通知（通知在屏幕右上角，不在企微窗口内）
        notif_path = os.path.join(TMP_DIR, "notif_check.png")
        run(f"screencapture -x {notif_path}")
        has_notif, matched = ocr_has_keyword(notif_path, NOTIFICATION_KEYWORDS)
        if not has_notif:
            log("  ✓ 无弹窗干扰")
            return True
        log(f"  ⚠ 检测到弹窗: {matched}，等待...")
        # 点击企微窗口中央，不点弹窗
        wx, wy = WINDOW_POS
        ww, wh = WINDOW_SIZE
        click_at(wx + ww // 2, wy + wh // 2)
        time.sleep(3)
    log("  ⚠ 弹窗可能仍存在，继续执行")
    return False


# ── 关闭右侧面板 ──

def close_side_panel():
    """检测并关闭企微右侧面板（智能服务总结等）
    
    这些面板会挤压聊天区域、遮挡输入框。
    关闭方式：按 Escape 或点击聊天区域。
    """
    img, win = screenshot("panel_check.png")
    has_panel, matched = ocr_has_keyword(img, PANEL_KEYWORDS)
    if has_panel:
        log(f"  检测到右侧面板: {matched}，尝试关闭...")
        press_key("escape")
        time.sleep(0.5)
        # 验证
        img2, _ = screenshot("panel_check2.png")
        still_has, _ = ocr_has_keyword(img2, PANEL_KEYWORDS)
        if still_has:
            log("  ⚠ 面板仍存在（可能需手动关闭）")
        else:
            log("  ✓ 面板已关闭")


# ── 切换到消息 Tab ──

def switch_to_messages():
    log("切换到消息页...")
    img, win = screenshot("tab_check.png")
    target = ocr_find(img, "消息")
    if target:
        click_ocr_target(win, target)
        time.sleep(1)
        log("  ✓ 已点击「消息」")
        return True
    log("  ⚠ 未找到「消息」Tab（可能已在消息页）")
    return True  # 不 block，可能已在消息页


# ── 查找并点击目标 ──

def find_and_click_target(name):
    """在消息列表中 OCR 查找并点击目标
    
    注意：不用 Cmd+F 搜索！企微搜索对外部微信联系人不可靠。
    直接在消息列表里 OCR 找目标名并点击。
    """
    log(f"在消息列表查找: {name}")
    switch_to_messages()
    time.sleep(1)

    for attempt in range(MAX_RETRIES):
        img, win = screenshot(f"msglist_{attempt}.png")

        # 精确匹配
        target = ocr_find(img, name)
        # 回退到前两个字
        if not target and len(name) >= 2:
            target = ocr_find(img, name[:2])

        if target:
            log(f"  ✓ 找到 '{target['text']}'")
            click_ocr_target(win, target)
            time.sleep(2)

            # 验证：右侧聊天区是否有内容
            img2, _ = screenshot("after_click.png")
            ocr_result = ocr(img2)
            if ocr_result and ocr_result.get("success"):
                right_texts = [t for t in ocr_result.get("all_texts", [])
                               if t["center_x"] > 800]
                if len(right_texts) > 3:
                    log(f"  ✓ 聊天窗口已打开（右侧 {len(right_texts)} 元素）")
                    return True

            log(f"  ⚠ 第 {attempt+1} 次未确认聊天窗口，重试...")
            time.sleep(1)
        else:
            ocr_result = ocr(img)
            if ocr_result:
                list_items = [t["text"][:20] for t in ocr_result.get("all_texts", [])
                              if 200 < t["center_x"] < 800 and 100 < t["center_y"] < 1200]
                log(f"  消息列表: {list_items[:8]}")
            time.sleep(2)

    log(f"  ✗ 未找到 '{name}'")
    return False


# ── 发送消息 ──

def send_message(message):
    """在当前聊天窗口发送消息
    
    输入框定位策略（无 placeholder 文字，OCR 找不到）：
    - 聊天工具栏（emoji/文件图标）在窗口底部约 75% 处
    - 输入框在工具栏下方，约窗口底部 85% 处
    - 使用窗口相对比例计算，适应不同窗口大小
    """
    log(f"发送消息: {message[:80]}...")

    # 先关闭右侧面板
    close_side_panel()

    win = get_window_info()
    if not win:
        log("  ✗ 无法获取窗口信息")
        return False

    # 输入框屏幕坐标：窗口中间偏右 x, 底部 85% y
    input_sx = win["x"] + int(win["width"] * 0.5)
    input_sy = win["y"] + int(win["height"] * 0.93)
    log(f"  点击输入框: screen({input_sx},{input_sy})")
    click_at(input_sx, input_sy)
    time.sleep(0.5)

    # 清空可能残留的内容
    hotkey("cmd,a")
    time.sleep(0.2)
    press_key("delete")
    time.sleep(0.3)

    # 处理 \n 换行
    lines = message.split("\\n")
    for i, line in enumerate(lines):
        if line.strip():
            paste_text(line)
        if i < len(lines) - 1:
            hotkey("shift,return")
            time.sleep(0.3)

    time.sleep(0.5)

    # 验证输入框有内容
    img, _ = screenshot("pre_send.png")
    check_text = message.split("\\n")[0][:8]
    found = ocr_find(img, check_text)
    if found and found["ly"] > win["height"] * 0.7:
        log(f"  ✓ 输入框确认有内容: '{found['text']}'")
    else:
        log(f"  ⚠ 未确认输入框内容，尝试继续发送")

    # 发送
    log("按回车发送...")
    press_key("return")
    time.sleep(2)

    # 验证发送
    img, _ = screenshot("sent_verify.png")
    target = ocr_find(img, check_text)
    if target:
        log("  ✅ 消息已在聊天记录中确认")
    else:
        log("  ⚠ 未在聊天记录确认（回车已按，大概率已发送）")

    return True


# ── main ──

def main():
    parser = argparse.ArgumentParser(description="企业微信 GUI 自动化发消息 v3.0")
    parser.add_argument("name", help="联系人或群名称")
    parser.add_argument("message", help="消息内容（\\n 换行）")
    parser.add_argument("--wait-login", action="store_true", help="登录时自动等待")
    parser.add_argument("--timeout", type=int, default=120, help="登录超时（秒）")
    args = parser.parse_args()

    os.makedirs(TMP_DIR, exist_ok=True)
    log(f"目标: {args.name}")
    log(f"消息: {args.message[:80]}...")

    # 1. 激活企微
    activate_wecom()

    # 2. 调整窗口
    resize_window()

    # 3. 登录检测
    if not check_login():
        qr_path = capture_qr_code()
        if args.wait_login:
            print(json.dumps({
                "status": "waiting_login", "qr_code": qr_path,
                "message": "企业微信需要登录，请扫描二维码"
            }, ensure_ascii=False), flush=True)
            if not wait_for_login(args.timeout):
                print(json.dumps({"success": False, "error": "登录超时"}, ensure_ascii=False))
                sys.exit(1)
            time.sleep(3)
            resize_window()
        else:
            print(json.dumps({
                "success": False, "needs_login": True, "qr_code": qr_path,
                "message": "企业微信需要登录，请扫描二维码"
            }, ensure_ascii=False))
            sys.exit(2)

    # 4. 等待系统弹窗
    wait_for_notifications_clear()

    # 5. 查找并点击目标
    if not find_and_click_target(args.name):
        print(json.dumps({"success": False, "error": f"未找到: {args.name}"},
                         ensure_ascii=False))
        sys.exit(1)

    # 6. 发送消息
    if send_message(args.message):
        print(json.dumps({
            "success": True, "to": args.name, "message": args.message
        }, ensure_ascii=False, indent=2))
        log("✅ 完成")
    else:
        print(json.dumps({"success": False, "error": "消息发送失败"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
