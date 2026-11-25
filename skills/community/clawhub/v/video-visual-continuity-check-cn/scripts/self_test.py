#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
fallback_source = (ROOT / "scripts/render_promo_fallback.py").read_text(encoding="utf-8")
if "AssetsV2" in fallback_source:
    raise SystemExit("public promo fallback must not contain a machine-specific font path")
NO_BYTECODE_ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
required = ["SKILL.md", "manifest.yaml", "agents/openai.yaml", "icon-512.png", "fixtures/success-input.json", "fixtures/success-output.json", "fixtures/forward-success.json", "fixtures/failure-input.json", "fixtures/failure-output.json"]
absent = [f for f in required if not (ROOT / f).is_file()]
if absent:
    raise SystemExit("missing: " + ", ".join(absent))
for name in ("SKILL.md", "manifest.yaml"):
    text = (ROOT / name).read_text(encoding="utf-8")
    if "video-visual-continuity-check-cn" not in text:
        raise SystemExit(f"slug absent from {name}")
png = (ROOT / "icon-512.png").read_bytes()
if png[:8] != b"\x89PNG\r\n\x1a\n":
    raise SystemExit("icon is not PNG")
if struct.unpack(">II", png[16:24]) != (512, 512):
    raise SystemExit("icon must be 512x512")
promo = (ROOT / "assets/promo-1600x900.png").read_bytes()
if promo[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", promo[16:24]) != (1600, 900):
    raise SystemExit("promo must be a 1600x900 PNG")
run = subprocess.run([sys.executable, str(ROOT / "scripts/check_continuity.py"), str(ROOT / "fixtures/success-input.json")], capture_output=True, text=True, check=True, env=NO_BYTECODE_ENV)
result = json.loads(run.stdout)
if result["status"] != "ok" or not any("人物参考要求" in item["evidence"] for item in result["issues"]):
    raise SystemExit("success fixture did not detect a contradiction with the character reference")
if result != json.loads((ROOT / "fixtures/success-output.json").read_text(encoding="utf-8")):
    raise SystemExit("success fixture output is not a real checker result")
if result != json.loads((ROOT / "fixtures/forward-success.json").read_text(encoding="utf-8")):
    raise SystemExit("forward success fixture must match the current checker output")
run = subprocess.run([sys.executable, str(ROOT / "scripts/check_continuity.py"), str(ROOT / "fixtures/failure-input.json")], capture_output=True, text=True, check=True, env=NO_BYTECODE_ENV)
failure = json.loads(run.stdout)
if failure["status"] != "needs_material" or not any(".id" in item for item in failure["missing"]):
    raise SystemExit("failure fixture did not request missing material")
if failure != json.loads((ROOT / "fixtures/failure-output.json").read_text(encoding="utf-8")):
    raise SystemExit("failure fixture output is not a real checker result")
named_gap = {
    "references": {"character": {"林岚": "深蓝外套"}, "scene": "书店"},
    "shots": [{"id": "01", "character": "林岚和陈默同框", "space": "书店"}]
}
result = json.loads(subprocess.run(
    [sys.executable, "-c", "import json,sys; from scripts.check_continuity import check; print(json.dumps(check(json.load(sys.stdin))))"],
    input=json.dumps(named_gap), capture_output=True, text=True, cwd=ROOT, check=True, env=NO_BYTECODE_ENV).stdout)
if result["status"] != "needs_material" or "references.character（陈默，shots[1]涉及人物）" not in result["missing"]:
    raise SystemExit("named co-presence did not request 陈默's missing character reference")
for prop in ("相机停在桌上", "杯子拿在左手"):
    result = json.loads(subprocess.run(
        [sys.executable, "-c", "import json,sys; from scripts.check_continuity import check; print(json.dumps(check(json.load(sys.stdin)), ensure_ascii=False))"],
        input=json.dumps({"shots": [{"id": "01", "prop": prop}]}, ensure_ascii=False),
        capture_output=True, text=True, cwd=ROOT, check=True, env=NO_BYTECODE_ENV).stdout)
    if result["status"] != "ok" or any("references.character" in item for item in result["missing"]):
        raise SystemExit(f"prop-only shot incorrectly required a character reference: {prop}")
explained = {
    "references": {"character": "林岚：深蓝外套", "scene": "书店门口，暖光从左侧"},
    "shots": [
        {"id": "01", "character": "林岚穿深蓝外套", "prop": "手拿纸袋", "lighting": "暖光从左侧", "space": "书店门口"},
        {"id": "02", "character": "林岚穿深蓝外套", "prop": "放下纸袋后双手空着", "lighting": "开灯后冷光从右侧", "space": "走到咖啡店"}
    ]
}
result = json.loads(subprocess.run(
    [sys.executable, "-c", "import json,sys; from pathlib import Path; from scripts.check_continuity import check; print(json.dumps(check(json.load(sys.stdin))))"],
    input=json.dumps(explained), capture_output=True, text=True, cwd=ROOT, check=True, env=NO_BYTECODE_ENV).stdout)
if result["issues"]:
    raise SystemExit("explicit action, movement, and lighting explanations were incorrectly reported")
regression = {
    "references": {
        "character": {"林岚": "长发，戴黑框眼镜"},
        "scene": "办公室，明亮暖光，办公桌左侧",
    },
    "shots": [
        {"id": "01", "description": "林岚长发、戴黑框眼镜，右手拿黄色纸袋，明亮暖光，办公桌左侧"},
        {"id": "02", "description": "林岚短发、未戴眼镜，黄色纸袋在桌上，昏暗暖光，办公桌右侧"},
    ],
}
result = json.loads(subprocess.run(
    [sys.executable, "-c", "import json,sys; from scripts.check_continuity import check; print(json.dumps(check(json.load(sys.stdin))))"],
    input=json.dumps(regression), capture_output=True, text=True, cwd=ROOT, check=True, env=NO_BYTECODE_ENV).stdout)
required_aspects = {"头发", "眼镜", "纸袋位置", "光线明暗", "办公桌位置"}
if result["status"] != "ok" or not required_aspects <= {item["aspect"] for item in result["issues"]}:
    raise SystemExit("explicit character, prop, lighting, and space changes were not all reported")
baseline = {
    "references": {"character": {"林岚": "深蓝外套"}, "scene": "室内暖光"},
    "shots": [
        {"id": "01", "character": "林岚穿白色外套", "transition": {"character": "林岚把深蓝外套换成白色外套"}},
        {"id": "02", "character": "林岚低头"},
        {"id": "03", "character": "林岚穿红色外套"},
    ],
}
result = json.loads(subprocess.run(
    [sys.executable, "-c", "import json,sys; from scripts.check_continuity import check; print(json.dumps(check(json.load(sys.stdin))))"],
    input=json.dumps(baseline), capture_output=True, text=True, cwd=ROOT, check=True, env=NO_BYTECODE_ENV).stdout)
if not any(item["category"] == "角色" and item["shots"] == ["01", "03"] and item["aspect"] == "外套" for item in result["issues"]):
    raise SystemExit("a documented new baseline hid a later wardrobe contradiction")
intra_shot = {
    "references": {"character": {"林岚": "深蓝外套"}, "scene": "室内暖光"},
    "shots": [{"id": "01", "character": "林岚穿深蓝外套", "lighting": "暖光从左侧",
               "description": "林岚穿白色外套，暖光从右侧"}],
}
result = json.loads(subprocess.run(
    [sys.executable, "-c", "import json,sys; from scripts.check_continuity import check; print(json.dumps(check(json.load(sys.stdin)), ensure_ascii=False))"],
    input=json.dumps(intra_shot, ensure_ascii=False), capture_output=True, text=True, cwd=ROOT, check=True, env=NO_BYTECODE_ENV).stdout)
if not {"外套", "来光方向"} <= {item["aspect"] for item in result["issues"]}:
    raise SystemExit("intra-shot field conflicts were not both reported")
prop_scope = {
    "references": {"character": {"林岚": "深蓝外套"}},
    "shots": [
        {"id": "01", "character": "林岚穿深蓝外套", "prop": "右手拿手机，左手拿纸袋"},
        {"id": "02", "character": "林岚穿深蓝外套", "prop": "放下纸袋，手机在桌上"},
    ],
}
result = json.loads(subprocess.run(
    [sys.executable, "-c", "import json,sys; from scripts.check_continuity import check; print(json.dumps(check(json.load(sys.stdin)), ensure_ascii=False))"],
    input=json.dumps(prop_scope, ensure_ascii=False), capture_output=True, text=True, cwd=ROOT, check=True, env=NO_BYTECODE_ENV).stdout)
if not any(item["category"] == "道具" and item["aspect"] == "手机位置" for item in result["issues"]):
    raise SystemExit("a paper-bag transition incorrectly explained the phone position")
forward_prop_gap = {
    "shots": [
        {"id": "01", "prop": "双手空着"},
        {"id": "02", "prop": "右手拿黄色纸袋"},
    ],
}
result = json.loads(subprocess.run(
    [sys.executable, "-c", "import json,sys; from scripts.check_continuity import check; print(json.dumps(check(json.load(sys.stdin)), ensure_ascii=False))"],
    input=json.dumps(forward_prop_gap, ensure_ascii=False), capture_output=True, text=True, cwd=ROOT, check=True, env=NO_BYTECODE_ENV).stdout)
if not any(item["category"] == "道具" and item["aspect"] == "纸袋" for item in result["issues"]):
    raise SystemExit("an empty-handed prop-only shot allowed a paper bag to appear without a transition")
severity_regression = {
    "references": {"character": {"林岚": "深蓝外套"}, "scene": "办公室，明亮暖光从左侧"},
    "shots": [
        {"id": "01", "character": "林岚穿深蓝外套", "prop": "右手拿手机", "lighting": "明亮暖光从左侧", "space": "办公室"},
        {"id": "02", "character": "林岚穿白色外套", "prop": "手机在桌上", "lighting": "昏暗暖光从左侧", "space": "办公室"},
    ],
}
result = json.loads(subprocess.run(
    [sys.executable, "-c", "import json,sys; from scripts.check_continuity import check; print(json.dumps(check(json.load(sys.stdin)), ensure_ascii=False))"],
    input=json.dumps(severity_regression, ensure_ascii=False), capture_output=True, text=True, cwd=ROOT, check=True, env=NO_BYTECODE_ENV).stdout)
severity_by_aspect = {item["aspect"]: item["severity"] for item in result["issues"]}
if (severity_by_aspect.get("外套"), severity_by_aspect.get("手机位置"), severity_by_aspect.get("光线明暗")) != ("high", "medium", "low"):
    raise SystemExit("severity classification did not distinguish high, medium, and low visual impact")
rank = {"high": 0, "medium": 1, "low": 2}
if [rank[item["severity"]] for item in result["issues"]] != sorted(rank[item["severity"]] for item in result["issues"]):
    raise SystemExit("issues were not sorted by severity")
subprocess.run([sys.executable, str(ROOT / "scripts/test_behavior.py")], check=True, env=NO_BYTECODE_ENV)
print("self-test passed: structure, fixtures, identity/scene safety, intra-shot conflicts, item-scoped prop transitions, and carried-baseline regressions")
