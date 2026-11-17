#!/usr/bin/env python3
"""check_sync.py — skill 三处版本一致性自检（只读，不改任何文件）。

比对三处状态：
  1. 本地 repos   ——  repos/text-to-infographic/
  2. 本地打包 zip ——  工作区根目录 text-to-infographic.zip
  3. 线上 ClawHub ——  clawhub skill verify bonniegeng-max/text-to-infographic

判据（与 Bonnie 确认的规则一致）：
  主判据 = 版本号（_meta.json / SKILL.md frontmatter / clawhub verify）
  危险信号 = 版本号相同但关键脚本 sha256 不一致（静默分叉，需人工 diff）
  日期只作旁证，不参与判断

用法:
    python3 check_sync.py            # 三处全查
    python3 check_sync.py --offline  # 跳过线上查询（离线可用）
"""
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

WS = Path(__file__).resolve().parents[3]          # 工作区根
REPO = Path(__file__).resolve().parents[1]        # repos/text-to-infographic
ZIP = WS / "text-to-infographic.zip"
SKILL = "bonniegeng-max/text-to-infographic"

# 需要比对指纹的关键文件（相对 SKILL 根目录）
FINGERPRINT_FILES = [
    "scripts/render_infographic_html.py",
    "scripts/validate_infographic_plan.py",
    "scripts/build_plan_from_text.py",
    "scripts/export_png.py",
]


def sha256(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def read_repo():
    """本地 repos 状态。"""
    meta = json.loads((REPO / "_meta.json").read_text())
    fm = re.search(r"^version:\s*([\w.\-]+)",
                   (REPO / "SKILL.md").read_text(), re.M)
    hashes = {f: sha256((REPO / f).read_bytes()) for f in FINGERPRINT_FILES
              if (REPO / f).exists()}
    return {"where": "本地 repos", "version": meta.get("version"),
            "fm_version": fm.group(1) if fm else None, "hashes": hashes}


def read_zip():
    """本地打包 zip 状态。"""
    if not ZIP.exists():
        return {"where": "本地 zip", "version": None, "fm_version": None,
                "hashes": {}, "note": "zip 不存在"}
    with zipfile.ZipFile(ZIP) as z:
        names = set(z.namelist())
        base = ""  # zip 根即 SKILL 根
        meta = json.loads(z.read(base + "_meta.json"))
        fm = re.search(r"^version:\s*([\w.\-]+)",
                       z.read(base + "SKILL.md").decode(), re.M)
        hashes = {}
        for f in FINGERPRINT_FILES:
            if base + f in names:
                hashes[f] = sha256(z.read(base + f))
        return {"where": "本地 zip", "version": meta.get("version"),
                "fm_version": fm.group(1) if fm else None, "hashes": hashes}


def read_online():
    """线上 ClawHub 状态（依赖 clawhub CLI + 网络）。"""
    try:
        r = subprocess.run(["clawhub", "skill", "verify", SKILL],
                           capture_output=True, text=True, timeout=30)
        d = json.loads(r.stdout)
        created = d.get("createdAt")
        import datetime
        when = datetime.datetime.fromtimestamp(
            created / 1000).strftime("%m-%d %H:%M") if created else "?"
        return {"where": "线上 ClawHub", "version": d.get("version"),
                "decision": d.get("decision"), "published": when}
    except Exception as e:
        return {"where": "线上 ClawHub", "version": None,
                "note": f"查询失败({type(e).__name__}: {e})"}


def vtuple(v):
    if not v:
        return ()
    return tuple(int(x) if x.isdigit() else x
                 for x in re.split(r"[.\-]", str(v)))


def main():
    offline = "--offline" in sys.argv
    repo = read_repo()
    zip_ = read_zip()
    online = None if offline else read_online()

    print("=== 三处状态 ===")
    for s in [s for s in (repo, zip_, online) if s]:
        line = f"  {s['where']:<12} version: {s.get('version') or '?'}"
        if s.get("published"):
            line += f"  (发布于 {s['published']})"
        if s.get("note"):
            line += f"  ⚠ {s['note']}"
        print(line)
    if repo.get("fm_version") != repo.get("version"):
        print(f"  ⚠ 本地 repos frontmatter({repo['fm_version']})"
              f" 与 _meta({repo['version']}) 不一致")

    print("\n=== 指纹（关键脚本 sha256 前 12 位）===")
    for f in FINGERPRINT_FILES:
        a, b = repo["hashes"].get(f, "?")[:12], zip_["hashes"].get(f, "?")[:12]
        mark = "一致" if a == b else "❌ 不一致"
        print(f"  {f.split('/')[-1]:<32} repo:{a}  zip:{b}  {mark}")

    print("\n=== 判断 ===")
    rv, zv = repo.get("version"), zip_.get("version")
    ov = online.get("version") if online else None

    if rv and zv and rv != zv:
        newer = "repos" if vtuple(rv) > vtuple(zv) else "zip"
        print(f"  ❌ repos({rv}) 与 zip({zv}) 不一致 → 打包过期或超前，"
              f"重打包或回滚，不要在这种状态下开发")
    else:
        # 指纹检查：版本相同但内容不同 = 静默分叉
        drift = [f for f in FINGERPRINT_FILES
                 if repo["hashes"].get(f) and zip_["hashes"].get(f)
                 and repo["hashes"][f] != zip_["hashes"][f]]
        if drift:
            print(f"  ❌ 静默分叉：版本同为 {rv} 但 {len(drift)} 个脚本指纹不同"
                  f"（{', '.join(d.split('/')[-1] for d in drift)}）→ 停，人工 diff")
        else:
            print(f"  ✅ repos 与 zip 一致（{rv}）")

    if online and ov:
        if vtuple(rv) > vtuple(ov):
            print(f"  🟡 本地 {rv} > 线上 {ov} → 待发布（等你说「发」，不自动 publish）")
        elif vtuple(rv) < vtuple(ov):
            print(f"  🔴 线上 {ov} > 本地 {rv} → 线上有新版本，必须先合回来再开发"
                  f"（clawhub install + diff，别直接覆盖）")
        else:
            print(f"  ✅ 本地与线上同为 {ov} → 已同步")
    elif offline:
        print("  （--offline 模式，跳过线上判断）")

    print("\n规则提醒：任何 publish/push 等 Bonnie 明确说「发/推」。")


if __name__ == "__main__":
    main()
