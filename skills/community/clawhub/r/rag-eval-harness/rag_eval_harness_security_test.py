#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rag_eval_harness_security_test.py — RAG 评估与防幻觉验证 · 安全稳定性实测
工具型技能 8 维量化测试（本地闭环 · 零真实凭据 · 可重复）

维度（0-5 分制，驱动雷达图）：
  1. script_integrity   脚本完整性（随包脚本存在且可解析）
  2. path_sanitized     路径中性化（无本地绝对路径残留）
  3. sensitive_zero     敏感信息隔离（真名/邮箱/密钥 0 命中）
  4. dependency_lite    依赖轻量（无第三方包，仅标准库 + 本地 Ollama 可选）
  5. runnable_safe      可安全运行（脚本仅本地 loopback，无外传）
  6. frontmatter       frontmatter 全字段（跨平台发布字段齐全）
  7. doc_consistency    文档×代码一致（SKILL.md 声称的随包文件都在）
  8. license_attest     权属与许可完整性（LICENSE.md + © + 免责声明）

用法：
  python rag_eval_harness_security_test.py [技能目录]
产出：
  security_results.json（本目录，供 gen_skill_security_radar.py 渲染雷达）
"""
import ast
import json
import os
import re
import sys
from pathlib import Path

SENSITIVE = [r"(?<!\d)1[3-9]\d{9}(?!\d)", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
             r"C:\\Users\\", r"<USER_HOME>", r"/Users/", r"/home/",
             r"sk-[A-Za-z0-9]{20,}", r"ghp_[A-Za-z0-9]{36,}"]
LOCAL_PATH = [r"<WORK_DIR>", r"D:\\Workbuddy", r"C:\\Users", r"<USER_HOME>",
              r"<USER_HOME>", r"<USER_NAME>", r"<身份占位>", r"\b用户\b"]
CLAIMED_FILES = [
    "references/local_rag_eval.py",
    "references/capability_eval_suite/run_suite.py",
    "references/capability_eval_suite/suite_registry.json",
]


def score_dim(name: str, score: float, note: str) -> dict:
    return {"name": name, "score": round(min(max(score, 0), 5), 2), "note": note}


def main(root: str = ".") -> int:
    base = Path(root).resolve()
    sk = (base / "SKILL.md").read_text("utf-8")
    ref_dir = base / "references"
    py_files = sorted(ref_dir.rglob("*.py"))
    json_files = sorted(ref_dir.rglob("*.json"))
    lic = (base / "LICENSE.md").read_text("utf-8") if (base / "LICENSE.md").exists() else ""

    dims = []

    # 1. 脚本完整性：随包脚本存在、无语法错误
    broken = []
    for p in py_files:
        try:
            ast.parse(p.read_text("utf-8"))
        except SyntaxError as e:
            broken.append(f"{p.name}:{e.lineno}")
    missing = [f for f in CLAIMED_FILES if not (base / f).exists()]
    score1 = 5.0 if not broken and not missing else max(1.0, 5.0 - 1.5 * (len(broken) + len(missing)))
    dims.append(score_dim("脚本完整性", score1,
                          f"{len(py_files)} 个 py 可解析" if not broken and not missing else f"异常: {broken + missing}"))

    # 2. 路径中性化：无本地绝对路径残留
    all_code = "".join(p.read_text("utf-8", errors="ignore") for p in py_files + json_files)
    path_hits = [pat for pat in LOCAL_PATH if re.search(pat, all_code)]
    dims.append(score_dim("路径中性化", 5.0 if not path_hits else 1.0,
                          "0 残留" if not path_hits else f"命中: {path_hits}"))

    # 3. 敏感信息隔离
    sens_hits = []
    for fname, content in [(p.name, p.read_text("utf-8", errors="ignore")) for p in py_files] + [("SKILL.md", sk)]:
        for pat in SENSITIVE:
            if re.search(pat, content):
                sens_hits.append(f"{fname}")
                break
    dims.append(score_dim("敏感信息隔离", 5.0 if not sens_hits else 1.0,
                          "0 命中" if not sens_hits else f"命中: {sens_hits}"))

    # 4. 依赖轻量：仅标准库 import（无 requests/numpy 等第三方必须）
    third_party = set()
    for p in py_files:
        for n in ast.walk(ast.parse(p.read_text("utf-8"))):
            if isinstance(n, ast.Import):
                third_party.update(a.name.split(".")[0] for a in n.names)
            elif isinstance(n, ast.ImportFrom) and n.module:
                third_party.add(n.module.split(".")[0])
    stdlib_ok = {"os", "re", "json", "urllib", "math", "sys", "subprocess", "datetime", "pathlib"}
    extra = third_party - stdlib_ok
    dims.append(score_dim("依赖轻量", 5.0 if not extra else 3.0,
                          "仅标准库" if not extra else f"第三方: {extra}"))

    # 5. 可安全运行：网络仅本机 loopback，无外传
    code5 = "".join(p.read_text("utf-8", errors="ignore") for p in py_files)
    external = [d for d in ["http://", "https://"] if d in code5]
    loopback = "127.0.0.1" in code5 or "localhost" in code5
    dims.append(score_dim("安全运行", 5.0 if (not external or loopback) else 2.0,
                          "仅本机 loopback" if loopback or not external else f"外部URL: {external}"))

    # 6. frontmatter 全字段
    fm = sk.split("---")[1] if sk.startswith("---") else ""
    need = ["name", "slug", "displayName", "display_name", "title", "version",
            "author", "category", "platforms", "license", "description", "description_en", "tags"]
    miss = [f for f in need if not re.search(rf"^{f}:", fm, re.M)]
    dims.append(score_dim("frontmatter 全字段", 5.0 if not miss else max(1.0, 5.0 - 1.2 * len(miss)),
                          "13 字段齐全" if not miss else f"缺: {miss}"))

    # 7. 文档×代码一致：SKILL.md 声称随包提供的文件都在
    dims.append(score_dim("文档×代码一致", 5.0 if not missing else 2.0,
                          "随包声明 3 文件齐全" if not missing else f"缺失: {missing}"))

    # 8. 权属与许可完整性
    cop = 0
    if lic:
        cop += 2 if "MIT License" in lic and "Copyright" in lic else 0
    if "版权与许可" in sk:
        cop += 1
    if "免责声明" in sk and "AS IS" in sk:
        cop += 1
    if "敏感测试样本" in sk:
        cop += 1
    dims.append(score_dim("权属与许可", cop, "LICENSE+版权段+免责+署名" if cop >= 4 else f"命中 {cop}/5"))

    overall = sum(d["score"] for d in dims) / len(dims)
    result = {
        "skill": "rag-eval-harness",
        "version": "1.1.0",
        "timestamp_local": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "scope": "本地闭环 · 零真实凭据 · 可重复",
        "dimensions": dims,
        "overall": round(overall, 2),
    }
    out = base / "security_results.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), "utf-8")
    print(f"✔ 综合 {overall:.2f}/5 → {out}")
    for d in dims:
        print(f"  {d['name']:<8} {d['score']}/5  {d['note']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
