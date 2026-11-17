"""验证 apply_results 的写入逻辑，不碰真实 models.json。
用临时文件模拟几种场景：正常更新、幂等短路、全部不完整拒绝写入、不降级保护。
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.expanduser(
    "~/.workbuddy/skills/workbuddy-model-capability-flags"))
import probe_model as pm

SAMPLE = [
    {"id": "m1", "name": "M1", "vendor": "V", "url": "https://x/1", "apiKey": "k",
     "supportsImages": False, "supportsToolCall": True, "supportsReasoning": True,
     "reasoning": {"defaultEffort": "high",
                   "supportedEfforts": ["low", "medium", "high"]}},
    {"id": "m2", "name": "M2", "vendor": "V", "url": "https://x/2", "apiKey": "k",
     "supportsImages": True, "supportsToolCall": True, "supportsReasoning": True,
     "reasoning": {"defaultEffort": "high",
                   "supportedEfforts": ["low", "medium", "high"]}},
]

fails = []


def setup():
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    pm.MODELS_PATH = path
    with open(path, "w", encoding="utf-8") as f:
        json.dump(SAMPLE, f, ensure_ascii=False, indent=2)
    return path


def load(path):
    return json.load(open(path, encoding="utf-8"))


def case(name, cond):
    print("  %s  %s" % ("PASS" if cond else "FAIL", name))
    if not cond:
        fails.append(name)


# --- 场景1：正常更新能力位 + 收敛档位为客户端可见的 6 档 ---
print("\n场景1：探测结论写回（含 none/ultra 过滤）")
p = setup()
pm.apply_results(
    {"m1": {"supportsImages": True, "supportsToolCall": True,
            "supportsReasoning": True, "_partial": False,
            "efforts": ["none", "minimal", "low", "medium", "high", "xhigh",
                        "ultra", "max"],
            "usable": ["minimal", "low", "medium", "high", "xhigh", "max"]},
     "m2": {"supportsImages": False, "supportsToolCall": False,
            "supportsReasoning": False, "_partial": False,
            "efforts": [], "usable": []}},
    [{"id": "m1"}, {"id": "m2"}], None, False)
d = {m["id"]: m for m in load(p)}
case("m1 supportsImages 改为 true", d["m1"]["supportsImages"] is True)
case("m1 档位过滤掉 none/ultra 只留 6 档",
     d["m1"]["reasoning"]["supportedEfforts"]
     == ["minimal", "low", "medium", "high", "xhigh", "max"])
case("m1 defaultEffort 保留原值 high（high 仍在可用档位内）",
     d["m1"]["reasoning"]["defaultEffort"] == "high")
case("m2 不支持推理时清掉 reasoning 块", "reasoning" not in d["m2"])
case("字段顺序仍是 id..reasoning",
     list(d["m1"].keys())[:5] == ["id", "name", "vendor", "url", "apiKey"])

# --- 场景2：幂等短路，文件字节不变 ---
print("\n场景2：结论一致时不重写文件")
p = setup()
before_mtime = os.path.getmtime(p)
with open(p, encoding="utf-8") as f:
    before_text = f.read()
pm.apply_results(
    {"m1": {"supportsImages": False, "supportsToolCall": True,
            "supportsReasoning": True, "_partial": False,
            "efforts": ["low", "medium", "high"],
            "usable": ["low", "medium", "high"]}},
    [{"id": "m1"}], "high", False)
after_text = open(p, encoding="utf-8").read()
case("文件内容未变", before_text == after_text)

# --- 场景3：全部探测不完整 → 拒绝写入 ---
print("\n场景3：探测全部不完整时拒绝写入（防网络故障误降级）")
p = setup()
before_text = open(p, encoding="utf-8").read()
pm.apply_results(
    {"m1": {"supportsImages": False, "supportsToolCall": False,
            "supportsReasoning": False, "_partial": True,
            "efforts": [], "usable": []}},
    [{"id": "m1"}], None, False)
case("配置未被改动", open(p, encoding="utf-8").read() == before_text)

# --- 场景4：单个探测项不完整 → 不把已验证的 true 降级 ---
print("\n场景4：不完整探测不降级已验证的 true")
p = setup()
# m2 当前 supportsImages=true；让探测因异常给出 false 且 _partial=true
pm.apply_results(
    {"m2": {"supportsImages": False, "supportsToolCall": True,
            "supportsReasoning": True, "_partial": True,
            "efforts": ["low", "medium", "high"],
            "usable": ["low", "medium", "high"]}},
    [{"id": "m2"}], "high", False)
d = {m["id"]: m for m in load(p)}
case("m2 supportsImages 仍为 true（未被误降级）", d["m2"]["supportsImages"] is True)

# --- 场景5：--force 可绕过完整性门槛 ---
print("\n场景5：--force 绕过完整性门槛")
p = setup()
pm.apply_results(
    {"m1": {"supportsImages": False, "supportsToolCall": False,
            "supportsReasoning": False, "_partial": True,
            "efforts": [], "usable": []}},
    [{"id": "m1"}], None, True)
d = {m["id"]: m for m in load(p)}
case("m1 被强制写成 false", d["m1"]["supportsImages"] is False)

# --- 场景6：探测出模型不在配置里 → 跳过而非报错 ---
print("\n场景6：模型不在 models.json 中时跳过")
p = setup()
before_text = open(p, encoding="utf-8").read()
pm.apply_results(
    {"ghost": {"supportsImages": True, "supportsToolCall": True,
               "supportsReasoning": True, "_partial": False,
               "efforts": ["low"], "usable": ["low"]}},
    [{"id": "ghost"}], None, False)
case("配置未被改动", open(p, encoding="utf-8").read() == before_text)

# --- 场景7：备份文件真的生成了 ---
print("\n场景7：写前自动备份")
bak_dir = os.path.join(os.path.dirname(p), "backups")
bak_files = os.listdir(bak_dir) if os.path.isdir(bak_dir) else []
case("backups/ 目录已生成", os.path.isdir(bak_dir))
case("备份文件名含 bak-probe",
     any("bak-probe" in f for f in bak_files))

# --- 场景8：不覆盖已有的 defaultEffort ---
print("\n场景8：保留用户已有的 defaultEffort（不降级）")
p = setup()   # m1 的 defaultEffort 原本是 high
pm.apply_results(
    {"m1": {"supportsImages": False, "supportsToolCall": True,
            "supportsReasoning": True, "_partial": False,
            "efforts": ["minimal", "low", "medium", "high", "xhigh", "max"],
            "usable": ["minimal", "low", "medium", "high", "xhigh", "max"]}},
    [{"id": "m1"}], None, False)
d = {m["id"]: m for m in load(p)}
case("m1 defaultEffort 仍为 high（未被改成 medium）",
     d["m1"]["reasoning"]["defaultEffort"] == "high")

# --- 场景9：原 defaultEffort 已不在可用档位里 → 重新挑 ---
print("\n场景9：原 defaultEffort 已失效时重新挑")
p = setup()
pm.apply_results(
    {"m1": {"supportsImages": False, "supportsToolCall": True,
            "supportsReasoning": True, "_partial": False,
            "efforts": ["low", "medium"], "usable": ["low", "medium"]}},
    [{"id": "m1"}], None, False)
d = {m["id"]: m for m in load(p)}
case("high 已不可用 → 落到 medium",
     d["m1"]["reasoning"]["defaultEffort"] == "medium")

# --- 场景10：--default-effort 显式覆盖优先 ---
print("\n场景10：--default-effort 显式指定时优先")
p = setup()
pm.apply_results(
    {"m1": {"supportsImages": False, "supportsToolCall": True,
            "supportsReasoning": True, "_partial": False,
            "efforts": ["low", "medium", "high"], "usable": ["low", "medium", "high"]}},
    [{"id": "m1"}], "low", False)
d = {m["id"]: m for m in load(p)}
case("defaultEffort 被显式改为 low",
     d["m1"]["reasoning"]["defaultEffort"] == "low")

os.unlink(p)
for f in (os.listdir(bak_dir) if os.path.isdir(bak_dir) else []):
    os.unlink(os.path.join(bak_dir, f))
os.rmdir(bak_dir)

print("\n" + "=" * 50)
print("失败 %d 项" % len(fails))
for f in fails:
    print("  - %s" % f)
sys.exit(1 if fails else 0)
