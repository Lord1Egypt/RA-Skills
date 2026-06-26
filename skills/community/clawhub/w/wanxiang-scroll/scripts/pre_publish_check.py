"""
万象绘卷预发布审核检查脚本
发布前运行此脚本，确保技能包通过ClawHub审核
"""

import os
import sys
import re
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CHECKS_PASSED = 0
CHECKS_FAILED = 0
WARNINGS = 0


def check(cond, msg, level="fail"):
    global CHECKS_PASSED, CHECKS_FAILED, WARNINGS
    if cond:
        CHECKS_PASSED += 1
        print(f"  [PASS] {msg}")
    elif level == "fail":
        CHECKS_FAILED += 1
        print(f"  [FAIL] {msg}")
    else:
        WARNINGS += 1
        print(f"  [WARN] {msg}")


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


def read_bytes(path):
    try:
        with open(path, "rb") as f:
            return f.read()
    except Exception:
        return b""


def walk_md_files():
    result = []
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.endswith(".md"):
                result.append(os.path.join(root, f))
    return result


def check_unicode_control():
    print("\n=== 1. Unicode控制字符检查 ===")
    suspicious_ranges = [
        (0x200B, 0x200F, "零宽/方向控制"),
        (0x202A, 0x202E, "Bidi控制"),
        (0x2060, 0x206F, "不可见/格式字符"),
    ]
    found_any = False
    for path in walk_md_files():
        content = read_file(path)
        for i, c in enumerate(content):
            code = ord(c)
            for lo, hi, desc in suspicious_ranges:
                if lo <= code <= hi:
                    rel = os.path.relpath(path, BASE_DIR)
                    print(f"  [FAIL] {rel}: Position {i} U+{code:04X} ({desc})")
                    CHECKS_FAILED += 1
                    found_any = True
                    break
    if not found_any:
        CHECKS_PASSED += 1
        print("  [PASS] 无Unicode控制字符")

    bom_count = 0
    for path in walk_md_files():
        data = read_bytes(path)
        if len(data) >= 3 and data[0] == 0xEF and data[1] == 0xBB and data[2] == 0xBF:
            bom_count += 1
            rel = os.path.relpath(path, BASE_DIR)
            print(f"  [FAIL] {rel}: 含BOM标记")
            CHECKS_FAILED += 1
    if bom_count == 0:
        CHECKS_PASSED += 1
        print("  [PASS] 无BOM标记")


def check_skill_md():
    print("\n=== 2. SKILL.md格式检查 ===")
    skill_path = os.path.join(BASE_DIR, "SKILL.md")
    content = read_file(skill_path)

    check(content.startswith("---\n"), "SKILL.md以YAML frontmatter开头")
    check("name: wanxiang-scroll" in content, "frontmatter含name字段")
    check("description:" in content, "frontmatter含description字段")
    check("version:" in content, "frontmatter含version字段")

    bad_words = ["文笔润色", "去痕迹", "AI痕迹识别与修复", "降AI"]
    for w in bad_words:
        check(w not in content, f"不含敏感词'{w}'")

    good_words = ["文笔润色", "文学润色", "游戏资料包"]
    for w in good_words:
        check(w in content, f"含正面描述词'{w}'")

    check("SECURITY_AUDIT.md" not in content, "不引用不存在的SECURITY_AUDIT.md")

    version_match = re.search(r"version:\s*(\S+)", content)
    if version_match:
        version = version_match.group(1)
        version_path = os.path.join(BASE_DIR, "VERSION")
        version_file = read_file(version_path).strip()
        check(version == version_file, f"SKILL.md版本({version})与VERSION文件({version_file})一致")


def check_sensitive_content():
    print("\n=== 3. 敏感内容检查 ===")
    sensitive_patterns = [
        (r"subprocess\.check_call", "自动安装依赖(subprocess.check_call)"),
        (r"os\.system\s*\(", "系统命令执行(os.system)"),
        (r"eval\s*\(", "动态代码执行(eval)"),
        (r"exec\s*\(", "动态代码执行(exec)"),
    ]
    scripts_dir = os.path.join(BASE_DIR, "scripts")
    if os.path.isdir(scripts_dir):
        for f in os.listdir(scripts_dir):
            if f.endswith(".py"):
                path = os.path.join(scripts_dir, f)
                content = read_file(path)
                for pattern, desc in sensitive_patterns:
                    check(pattern not in content, f"{f}: 不含{desc}")


def check_auto_execution():
    print("\n=== 4. 自动执行检查 ===")
    scripts_dir = os.path.join(BASE_DIR, "scripts")
    if os.path.isdir(scripts_dir):
        for f in os.listdir(scripts_dir):
            if f.endswith(".py"):
                path = os.path.join(scripts_dir, f)
                content = read_file(path)
                has_main_guard = 'if __name__ == "__main__"' in content
                check(has_main_guard, f"{f}: 使用__main__守卫(不会自动执行)")

    skill_path = os.path.join(BASE_DIR, "SKILL.md")
    content = read_file(skill_path)
    check("手动跑" in content or "手动执行" in content, "SKILL.md说明脚本需手动运行")


def check_file_integrity():
    print("\n=== 5. 文件完整性检查 ===")
    required_files = [
        "SKILL.md",
        "VERSION",
        "requirements.txt",
    ]
    for f in required_files:
        path = os.path.join(BASE_DIR, f)
        check(os.path.isfile(path), f"必需文件存在: {f}")

    required_dirs = [
        "references",
        "scripts",
        "saves",
    ]
    for d in required_dirs:
        path = os.path.join(BASE_DIR, d)
        check(os.path.isdir(path), f"必需目录存在: {d}")

    skill_path = os.path.join(BASE_DIR, "SKILL.md")
    content = read_file(skill_path)
    dir_refs = re.findall(r"(\S+/)\s+#", content)
    for d in dir_refs:
        clean = d.strip("/")
        path = os.path.join(BASE_DIR, "references", clean)
        if clean.startswith("ch") or clean == "原始草稿":
            check(os.path.isdir(path), f"SKILL.md引用的目录存在: {clean}")


def check_clawhub_meta():
    print("\n=== 6. ClawHub元数据检查 ===")
    lock_path = os.path.join(BASE_DIR, ".clawhub", "lock.json")
    if os.path.isfile(lock_path):
        data = json.loads(read_file(lock_path))
        skill_ver = data.get("skills", {}).get("wanxiang-scroll", {}).get("version", "")
        version_path = os.path.join(BASE_DIR, "VERSION")
        version_file = read_file(version_path).strip()
        check(skill_ver == version_file, f"lock.json版本({skill_ver})与VERSION({version_file})一致")
    else:
        print("  [WARN] .clawhub/lock.json不存在(首次发布)")
        WARNINGS += 1

    ignore_path = os.path.join(BASE_DIR, ".clawhubignore")
    check(os.path.isfile(ignore_path), ".clawhubignore存在")


def main():
    print("=" * 50)
    print("万象绘卷 预发布审核检查")
    print("=" * 50)

    check_unicode_control()
    check_skill_md()
    check_sensitive_content()
    check_auto_execution()
    check_file_integrity()
    check_clawhub_meta()

    print("\n" + "=" * 50)
    print(f"审核结果: {CHECKS_PASSED} 通过, {CHECKS_FAILED} 失败, {WARNINGS} 警告")
    print("=" * 50)

    if CHECKS_FAILED > 0:
        print("\n存在失败项，请修复后再发布！")
        sys.exit(1)
    else:
        print("\n全部通过，可以发布！")
        sys.exit(0)


if __name__ == "__main__":
    main()
