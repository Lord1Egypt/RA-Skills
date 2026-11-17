"""DeepSeek 读图判定稳定性：同一张测试图连跑 6 次，看判定是否稳定。
怀疑点：模型偶尔会把答案写进 reasoning_content，或用别的措辞导致我的判定误报不支持。

用法（key 走环境变量，不要写死）：
    setx DEEPSEEK_API_KEY "sk-..."
    python test_vision_stability.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.expanduser(
    "~/.workbuddy/skills/workbuddy-model-capability-flags"))
import probe_model as pm

MODEL = os.environ.get("PROBE_MODEL", "deepseek-v4-flash")
URL = os.environ.get("PROBE_URL", "https://api.deepseek.com/chat/completions")
# ⚠ key 只能从环境变量读。此前这个文件里硬编码过一枚真实 key，
# skill 一旦发布就等于公开泄露 —— 已改为必须显式提供。
KEY = os.environ.get("DEEPSEEK_API_KEY") or os.environ.get("PROBE_KEY")
if not KEY:
    sys.exit("缺少 key：请先 setx DEEPSEEK_API_KEY \"sk-...\"（不要把 key 写进本文件）")

ROUNDS = int(os.environ.get("PROBE_ROUNDS", "6"))

b64 = pm.load_image_b64(None)
ok_count = 0
for i in range(ROUNDS):
    ok, detail, reasoning = pm.probe_vision(MODEL, URL, KEY, b64)
    ok_count += 1 if ok else 0
    print("第%d次  判定=%-6s  %s" % (i + 1, "支持" if ok else "不支持", detail[:150]))
    if reasoning:
        print("        reasoning: %s" % reasoning[:150].replace("\n", " "))
    time.sleep(4)
print("\n支持 %d/%d 次" % (ok_count, ROUNDS))
