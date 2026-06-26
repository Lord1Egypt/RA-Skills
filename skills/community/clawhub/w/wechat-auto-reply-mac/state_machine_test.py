#!/usr/bin/env python3
import subprocess
import time
from Foundation import NSURL
from Vision import VNRecognizeTextRequest, VNImageRequestHandler

CONTACT = "文件传输助手"
MESSAGE = "状态机测试：如果你看到这条，说明候选点轮询 + OCR 确认 + 自动发送成功。"
VENV_PY = "/Users/chuck/.venvs/pyobjc/bin/python"


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
    script = f'''tell application "WeChat" to activate
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
end tell'''
    osa(script)
    X, Y, W, H = get_wechat_bounds()
    RX, RY, RW, RH = X, Y + 60, 520, 520
    img = "/tmp/wechat-search-state-machine.png"
    subprocess.run(["/usr/sbin/screencapture", f"-R{RX},{RY},{RW},{RH}", img], check=True)
    # 从 OCR 里找纯命中，点击其文本行
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
        print("SWITCH_CONTACT: no contact hit")
        return False
    hits.sort(reverse=True)
    _, text, cx, cy = hits[0]
    print(f"SWITCH_CONTACT: click {text} @ {cx},{cy}")
    click(cx, cy)
    time.sleep(0.8)
    # 关键：退出搜索上下文，避免后续粘贴仍然落到搜索聊天记录框
    osa('tell application "System Events" to key code 53')
    time.sleep(0.4)
    return True


def confirm_input_has_message(expected: str) -> bool:
    X, Y, W, H = get_wechat_bounds()
    RX = X + int(W * 0.48)
    RY = Y + int(H * 0.80)
    RW = int(W * 0.48)
    RH = int(H * 0.17)
    img = "/tmp/wechat-input-check.png"
    subprocess.run(["/usr/sbin/screencapture", f"-R{RX},{RY},{RW},{RH}", img], check=True)
    texts = vision_texts(img)
    joined = " | ".join(texts)
    print("INPUT_OCR:", joined)
    # 用前 8 个字做宽松匹配
    return expected[:8] in joined or expected[:6] in joined


def main():
    if not switch_contact(CONTACT):
        print("FAIL: switch contact")
        return 2

    X, Y, W, H = get_wechat_bounds()
    candidates = [
        (X + int(W * 0.60), Y + int(H * 0.88)),
        (X + int(W * 0.68), Y + int(H * 0.90)),
        (X + int(W * 0.72), Y + int(H * 0.90)),
        (X + int(W * 0.80), Y + int(H * 0.88)),
    ]

    for idx, (cx, cy) in enumerate(candidates, 1):
        print(f"TRY_POINT_{idx}: {cx},{cy}")
        click(cx, cy, double=True)
        time.sleep(0.5)
        osa('tell application "System Events" to keystroke "a" using command down')
        time.sleep(0.2)
        paste_text(MESSAGE)
        time.sleep(0.8)
        if confirm_input_has_message(MESSAGE):
            print(f"POINT_OK: {cx},{cy}")
            key_enter()
            print("SEND_OK")
            return 0
    print("FAIL: no input point worked")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
