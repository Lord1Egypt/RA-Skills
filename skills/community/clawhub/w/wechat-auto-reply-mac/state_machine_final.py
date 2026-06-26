#!/usr/bin/env python3
import subprocess
import time
from Foundation import NSURL
from Vision import VNRecognizeTextRequest, VNImageRequestHandler

CONTACT = "文件传输助手"
MESSAGE = "状态机终测：如果你看到这条，说明聊天态确认、浮层退出、输入框预填和发送都已打通。"


def osa(script: str) -> str:
    return subprocess.check_output(["osascript", "-e", script]).decode().strip()


def click(x: int, y: int, double: bool = False):
    kind = "dc" if double else "c"
    subprocess.run(["/usr/local/bin/cliclick", f"{kind}:{x},{y}"], check=True)


def key_enter():
    osa('tell application "WeChat" to activate')
    time.sleep(0.2)
    osa('tell application "System Events" to key code 36')


def paste_text(text: str):
    osa(f'set the clipboard to "{text}"')
    osa('tell application "System Events" to keystroke "v" using command down')


def get_wechat_bounds():
    out = osa('''tell application "WeChat" to activate
    delay 0.3
    tell application "System Events"
      tell process "WeChat"
        set frontmost to true
        set p to position of window 1
        set s to size of window 1
        return (item 1 of p as text) & "," & (item 2 of p as text) & "," & (item 1 of s as text) & "," & (item 2 of s as text)
      end tell
    end tell''')
    return tuple(map(int, out.split(',')))


def vision_texts(path: str):
    url = NSURL.fileURLWithPath_(path)
    req = VNRecognizeTextRequest.alloc().init()
    req.setRecognitionLanguages_(['zh-Hans', 'en-US'])
    req.setUsesLanguageCorrection_(True)
    handler = VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    handler.performRequests_error_([req], None)
    results = req.results() or []
    texts = []
    for obs in results:
        cands = obs.topCandidates_(1)
        if cands:
            texts.append(str(cands[0].string()).strip())
    return texts


def switch_contact(contact: str):
    osa(f'''tell application "WeChat" to activate
set the clipboard to "{contact}"
delay 0.3
tell application "System Events"
  tell process "WeChat"
    set frontmost to true
    keystroke "f" using command down
    delay 0.5
    keystroke "a" using command down
    delay 0.2
    keystroke "v" using command down
    delay 1
  end tell
end tell''')
    X, Y, W, H = get_wechat_bounds()
    RX, RY, RW, RH = X, Y + 60, 520, 520
    img = "/tmp/wechat-state-search.png"
    subprocess.run(["/usr/sbin/screencapture", f"-R{RX},{RY},{RW},{RH}", img], check=True)
    url = NSURL.fileURLWithPath_(img)
    req = VNRecognizeTextRequest.alloc().init()
    req.setRecognitionLanguages_(['zh-Hans', 'en-US'])
    req.setUsesLanguageCorrection_(True)
    handler = VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    handler.performRequests_error_([req], None)
    results = req.results() or []
    hits = []
    for obs in results:
        cands = obs.topCandidates_(1)
        if not cands:
            continue
        text = str(cands[0].string()).strip()
        if contact not in text:
            continue
        if any(bad in text for bad in ['怎么', '聊天记录', '打开', '恢复', '关闭', 'Q ']):
            continue
        box = obs.boundingBox()
        bx, by, bw, bh = box.origin.x, box.origin.y, box.size.width, box.size.height
        cx = RX + int((bx + bw/2) * RW)
        cy = RY + int((1 - (by + bh/2)) * RH)
        score = 100 if text == contact else 0
        score += max(0, 20 - len(text))
        hits.append((score, text, cx, cy))
    if not hits:
        print('FAIL_SWITCH:NO_HIT')
        return False
    hits.sort(reverse=True)
    _, text, cx, cy = hits[0]
    # 不点文字本身，改点同一行右侧更像“进入聊天”的区域
    click_x = min(X + W - 110, cx + 210)
    click_y = cy
    print(f'SWITCH_CONTACT: row {text} @ {cx},{cy}; click enter-chat area @ {click_x},{click_y}')
    click(click_x, click_y)
    time.sleep(1.0)
    # 退出可能残留的搜索聊天记录浮层
    osa('tell application "System Events" to key code 53')
    time.sleep(0.8)
    return True


def screenshot_region(path: str, rx: int, ry: int, rw: int, rh: int):
    subprocess.run(["/usr/sbin/screencapture", f"-R{rx},{ry},{rw},{rh}", path], check=True)


def confirm_clean_chat_state():
    X, Y, W, H = get_wechat_bounds()
    # 聊天标题附近区域，确认出现 文件传输助手
    img = '/tmp/wechat-title-check.png'
    screenshot_region(img, X + 360, Y + 0, W - 360, 120)
    texts = vision_texts(img)
    joined = ' | '.join(texts)
    print('TITLE_OCR:', joined)
    return CONTACT in joined


def confirm_no_search_overlay():
    X, Y, W, H = get_wechat_bounds()
    img = '/tmp/wechat-overlay-check.png'
    screenshot_region(img, X + 0, Y + 0, 420, 180)
    texts = vision_texts(img)
    joined = ' | '.join(texts)
    print('OVERLAY_OCR:', joined)
    # 不出现“搜索聊天记录”则视为浮层已清掉
    return '搜索聊天记录' not in joined


def confirm_input_has_message(expected: str) -> bool:
    X, Y, W, H = get_wechat_bounds()
    RX = X + int(W * 0.48)
    RY = Y + int(H * 0.80)
    RW = int(W * 0.48)
    RH = int(H * 0.17)
    img = '/tmp/wechat-input-check-final.png'
    screenshot_region(img, RX, RY, RW, RH)
    texts = vision_texts(img)
    joined = ' | '.join(texts)
    print('INPUT_OCR:', joined)
    return expected[:8] in joined or expected[:6] in joined


def main():
    if not switch_contact(CONTACT):
        return 2
    if not confirm_clean_chat_state():
        print('FAIL_STATE: not in target chat')
        return 3
    if not confirm_no_search_overlay():
        print('FAIL_STATE: overlay still present')
        return 4

    # 在干净聊天态里，用已验证点位预填
    click(1043, 878, double=True)
    time.sleep(0.5)
    paste_text(MESSAGE)
    time.sleep(0.8)

    if not confirm_input_has_message(MESSAGE):
        print('FAIL_STATE: message not in input')
        return 5

    key_enter()
    print('SEND_OK')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
