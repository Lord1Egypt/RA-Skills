#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能包结构自检器 —— 上传前验证目录是否符合主流平台（WorkBuddy / 扣子Coze·豆包 / Claude 等）规范

检查项：
  1. SKILL.md 存在于包根目录
  2. frontmatter 含必需的 name / description
  3. name 合规：<=64 字符、仅小写字母数字连字符、不含 anthropic/claude 保留字
  4. description 合规：非空、<=1024 字符、不含 XML 标签
  5. SKILL.md 正文 <=500 行（渐进式披露的性能建议）
  6. 标准目录齐备：scripts/ references/ assets/
  7. SKILL.md / README.md 中引用的相对文件路径真实存在
  8. 无编译缓存、临时文件、空目录
  9. scripts/*.py 语法可编译
 10. （可选 --zip）压缩包根目录直接就是 SKILL.md，没有多套一层文件夹

用法:
  python scripts/validate_pack.py                      # 检查本包
  python scripts/validate_pack.py --path ./my-skill    # 检查指定目录
  python scripts/validate_pack.py --zip ./skill.zip    # 额外检查压缩包结构
"""
import argparse
import os
import py_compile
import re
import sys
import tempfile
import zipfile

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

NAME_MAX = 64
DESC_MAX = 1024
BODY_MAX_LINES = 500
RESERVED = ("anthropic", "claude")

PASS, WARN, FAIL = "PASS", "WARN", "FAIL"
results = []


def add(status, item, detail=""):
    results.append((status, item, detail))


def read_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f


def parse_frontmatter(text):
    """返回 (frontmatter_dict, body)；无 frontmatter 则返回 (None, text)"""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm_text = text[3:end].strip("\n")
    body = text[end + 4:]
    fm = {}
    key = None
    for line in fm_text.split("\n"):
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$", line)
        if m:
            key = m.group(1)
            fm[key] = m.group(2).strip()
        elif key:  # 多行值（YAML 折叠），简单拼接
            fm[key] += " " + line.strip()
    return fm, body


def check_bad_files(root):
    bad = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ("__pycache__", ".git", ".workbuddy")]
        rel = os.path.relpath(dirpath, root).replace("\\", "/")
        if "__pycache__" in dirpath or ".git" in dirpath:
            bad.append(rel)
            continue
        for fn in filenames:
            if fn.endswith((".pyc", ".pyo", ".tmp", ".bak")) or fn in (".DS_Store", "Thumbs.db"):
                bad.append(f"{rel}/{fn}" if rel != "." else fn)
        if not dirnames and not filenames and rel != ".":
            bad.append(f"{rel} (空目录)")
    return bad


def check_refs(root, md_files):
    """检查 markdown 中引用的相对文件是否真实存在"""
    missing = []
    pattern = re.compile(r"\]\((?!https?://|#|mailto:)([^)\s]+)\)")
    for md in md_files:
        if not os.path.exists(md):
            continue
        with open(md, "r", encoding="utf-8") as f:
            text = f.read()
        for m in pattern.finditer(text):
            target = m.group(1).strip().strip("`").split("#")[0]
            if not target or target.startswith("{"):
                continue
            full = os.path.join(root, target.replace("/", os.sep))
            if not os.path.exists(full):
                missing.append(f"{os.path.basename(md)} → {target}")
    return missing


def check_scripts(root):
    """语法编译检查"""
    errs = []
    sdir = os.path.join(root, "scripts")
    if not os.path.isdir(sdir):
        return errs
    for fn in sorted(os.listdir(sdir)):
        if not fn.endswith(".py"):
            continue
        try:
            py_compile.compile(os.path.join(sdir, fn), doraise=True, cfile=tempfile.mktemp())
        except Exception as e:
            errs.append(f"{fn}: {e}")
    return errs


def check_zip(zip_path):
    """压缩包根目录必须直接包含 SKILL.md，不能多套一层"""
    if not os.path.exists(zip_path):
        add(FAIL, "压缩包检查", f"文件不存在: {zip_path}")
        return
    try:
        with zipfile.ZipFile(zip_path) as z:
            names = z.namelist()
    except Exception as e:
        add(FAIL, "压缩包检查", f"无法读取: {e}")
        return

    if not names:
        add(FAIL, "压缩包检查", "空压缩包")
        return

    has_root = any(n.strip("/").lower() == "skill.md" for n in names)
    if has_root:
        add(PASS, "压缩包根目录直含 SKILL.md", f"共 {len(names)} 个条目")
    else:
        tops = {n.split("/")[0] for n in names if "/" in n}
        add(FAIL, "压缩包根目录直含 SKILL.md",
            f"检测到外层文件夹 {tops} —— 请压缩文件夹内部内容，不要连文件夹一起压")

    norm = {n.lower() for n in names}
    if any("__pycache__" in n for n in norm):
        add(WARN, "压缩包无编译缓存", "存在 __pycache__，建议清理后重新打包")


def main():
    ap = argparse.ArgumentParser(description="技能包结构自检")
    ap.add_argument("--path", help="技能包根目录，默认为本脚本所在包")
    ap.add_argument("--zip", help="额外检查打包好的 zip")
    args = ap.parse_args()

    root = os.path.abspath(args.path) if args.path else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"[信息] 检查目录: {root}\n")

    # 1. SKILL.md
    skill_md = os.path.join(root, "SKILL.md")
    if not os.path.exists(skill_md):
        add(FAIL, "SKILL.md 存在于根目录", "缺失，这是各平台识别技能的必需入口")
        report(root)
        return 1
    add(PASS, "SKILL.md 存在于根目录", skill_md)

    with open(skill_md, "r", encoding="utf-8") as f:
        text = f.read()
    fm, body = parse_frontmatter(text)

    # 2. frontmatter
    if fm is None:
        add(FAIL, "YAML frontmatter", "未检测到 --- 包裹的 frontmatter")
        report(root)
        return 1
    add(PASS, "YAML frontmatter 存在", "字段: " + ", ".join(fm.keys()))

    # 3. name
    name = fm.get("name", "")
    if not name:
        add(FAIL, "frontmatter.name", "缺失（必需）")
    else:
        ok = True
        if len(name) > NAME_MAX:
            add(FAIL, "frontmatter.name 长度", f"{len(name)} 字符，超过 {NAME_MAX}")
            ok = False
        if not re.fullmatch(r"[a-z0-9\-]+", name):
            add(FAIL, "frontmatter.name 字符集", "只允许小写字母、数字、连字符")
            ok = False
        if any(r in name.lower() for r in RESERVED):
            add(FAIL, "frontmatter.name 保留字", "不得包含 anthropic / claude")
            ok = False
        if ok:
            add(PASS, "frontmatter.name 合规", f"{name}（{len(name)}/{NAME_MAX} 字符）")

    # 4. description
    desc = fm.get("description", "")
    if not desc:
        add(FAIL, "frontmatter.description", "缺失（必需，决定技能何时被触发）")
    else:
        ok = True
        if len(desc) > DESC_MAX:
            add(FAIL, "frontmatter.description 长度", f"{len(desc)} 字符，超过 {DESC_MAX}")
            ok = False
        if "<" in desc and ">" in desc:
            add(FAIL, "frontmatter.description XML", "不得包含 XML 标签")
            ok = False
        if ok:
            add(PASS, "frontmatter.description 合规", f"{len(desc)}/{DESC_MAX} 字符")

    # 5. 正文行数
    lines = len(body.strip().split("\n"))
    if lines > BODY_MAX_LINES:
        add(WARN, "SKILL.md 正文行数", f"{lines} 行，超过建议的 {BODY_MAX_LINES}，建议拆分到 references/")
    else:
        add(PASS, "SKILL.md 正文行数", f"{lines}/{BODY_MAX_LINES} 行")

    # 6. 标准目录
    for d, required in (("scripts", True), ("references", True), ("assets", False)):
        p = os.path.join(root, d)
        if os.path.isdir(p):
            n = sum(len(fs) for _, _, fs in os.walk(p))
            n_dirs = sum(len(ds) for _, ds, _ in os.walk(p))
            desc = f"{n} 个文件"
            if n_dirs:
                desc += f"（含 {n_dirs} 个子目录）"
            add(PASS if n else WARN, f"{d}/ 目录", desc if n else "存在但为空")
        elif required:
            add(WARN, f"{d}/ 目录", "建议提供（规范中的可选目录）")
        else:
            add(WARN, f"{d}/ 目录", "未提供（规范中的可选目录）")

    # 7. 引用完整性
    md_files = [os.path.join(root, f) for f in ("SKILL.md", "README.md")]
    missing = check_refs(root, md_files)
    if missing:
        add(FAIL, "文档内引用文件存在性", "缺失: " + "; ".join(missing[:5]))
    else:
        add(PASS, "文档内引用文件存在性", "全部命中")

    # 8. 垃圾文件
    bad = check_bad_files(root)
    if bad:
        add(FAIL, "无缓存/临时文件", "; ".join(bad[:5]))
    else:
        add(PASS, "无缓存/临时文件", "干净")

    # 9. 脚本语法
    errs = check_scripts(root)
    if errs:
        add(FAIL, "scripts/*.py 语法", "; ".join(errs))
    else:
        add(PASS, "scripts/*.py 语法", "全部可编译")

    # 10. zip
    if args.zip:
        check_zip(args.zip)

    return report(root)


def report(root):
    print("=" * 72)
    print(f"{'状态':<6} {'检查项':<28} 详情")
    print("=" * 72)
    for status, item, detail in results:
        print(f"{status:<6} {item:<28} {detail}")
    print("=" * 72)
    n_fail = sum(1 for r in results if r[0] == FAIL)
    n_warn = sum(1 for r in results if r[0] == WARN)
    n_pass = sum(1 for r in results if r[0] == PASS)
    print(f"通过 {n_pass} ｜ 警告 {n_warn} ｜ 失败 {n_fail}")

    if n_fail:
        print("\n[结论] ❌ 存在不合规项，请先修复再上传")
        return 1
    if n_warn:
        print("\n[结论] ⚠️  结构合规，但有可优化项（不影响上传）")
        return 0
    print("\n[结论] ✅ 结构完全合规，可打包上传")
    return 0


if __name__ == "__main__":
    sys.exit(main())
