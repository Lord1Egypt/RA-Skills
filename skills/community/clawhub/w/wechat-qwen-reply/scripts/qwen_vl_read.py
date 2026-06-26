import base64
import json
import subprocess
import sys
from pathlib import Path
import urllib.request

# ensure UTF-8 output
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="ignore")
    sys.stderr.reconfigure(encoding="utf-8", errors="ignore")
except Exception:
    pass


def run_ps(args):
    cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File"] + args
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip() or res.stdout.strip())
    return res.stdout.strip()

BASE = Path(r"C:\Users\chenxun\.nanobot\workspace")
API_KEY_PATH = BASE / ".secrets" / "dashscope_api_key.txt"
if not API_KEY_PATH.exists():
    raise SystemExit(f"Missing API key: {API_KEY_PATH}")
api_key = API_KEY_PATH.read_text(encoding="utf-8").strip().lstrip("\ufeff")
if not api_key:
    raise SystemExit("Empty API key")

# parse args
args = sys.argv[1:]
# default to fast mode unless --slow is specified
fast_mode = "--slow" not in args
debug_mode = "--debug" in args

# extract contact (first non-flag arg)
contact = "华工学术嫡长子"
for a in args:
    if not a.startswith("--"):
        contact = a
        break

# optional overrides
offset_x = None
offset_y = None
for a in args:
    if a.startswith("--offsetx="):
        offset_x = a.split("=", 1)[1]
    if a.startswith("--offsety="):
        offset_y = a.split("=", 1)[1]

# 1) capture cropped chat image
ps_script = "wechat_capture_fast.ps1" if fast_mode else "wechat_capture_crop.ps1"
ps_args = [str(BASE / ps_script), "-Contact", contact]
if offset_x is not None:
    ps_args += ["-ScreenOffsetX", offset_x]
if offset_y is not None:
    ps_args += ["-ScreenOffsetY", offset_y]

crop_path = run_ps(ps_args)
if not crop_path or not Path(crop_path).exists():
    raise SystemExit(f"Crop image not found: {crop_path}")

# save last crop for debug
last_crop = BASE / "qwen_last_crop.png"
Path(crop_path).replace(last_crop)
if debug_mode:
    print(f"[CROP] {last_crop}")

# 2) call Qwen-VL to read chat text
img_bytes = Path(last_crop).read_bytes()
img_b64 = base64.b64encode(img_bytes).decode("utf-8")

payload_vision = {
    "model": "qwen-vl-plus",
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "请读取图片中的微信聊天记录，尽量还原原文。请按聊天窗口从上到下的顺序输出（旧→新），不要打乱顺序。请依据气泡颜色和位置判断发送方：绿色气泡=我（用“我：内容”），白色气泡=对方（尽量识别昵称，用“昵称：内容”，不确定就用“对方：内容”）。若颜色不清晰，再参考右侧=我、左侧=对方。群聊请尽量标注具体昵称。文件卡片/红包卡片请标注发送方并注明“【文件卡片】/【红包卡片】”，系统提示不要当作聊天内容输出。只输出聊天文本，不要解释。",
                },
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
            ],
        }
    ],
}

req = urllib.request.Request(
    "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
    data=json.dumps(payload_vision).encode("utf-8"),
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    method="POST",
)

with urllib.request.urlopen(req, timeout=60) as resp:
    data = json.loads(resp.read().decode("utf-8"))

chat_text = data["choices"][0]["message"]["content"]

if not chat_text:
    raise SystemExit("Chat text invalid. Abort.")

# save outputs
(BASE / "qwen_chat_last.txt").write_text(chat_text, encoding="utf-8")

print(chat_text)
