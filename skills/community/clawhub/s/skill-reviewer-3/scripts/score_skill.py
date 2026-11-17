#!/usr/bin/env python3
"""skill-reviewer 硬指标自动判定脚本

只读扫描一个 Skill 目录，产出机器可判定的结构类硬指标结果。
不执行被审目录中的任何脚本，不联网，不启动子进程，不读取凭据。

用法:
    python score_skill.py <skill目录路径> [--json]

输出:
    --json  时输出 JSON 到 stdout，否则输出人类可读文本。
    退出码: 0 = 扫描完成; 2 = 参数错误或目录不存在。
"""
import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def read_skill_md(skill_dir: Path):
    """读取 SKILL.md，返回 (文本, frontmatter字典, 正文)。"""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return None, None, None
    text = skill_md.read_text(encoding="utf-8", errors="replace")
    fm = {}
    body = text
    m = re.match(r"\A---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if m:
        body = text[m.end():]
        for line in m.group(1).splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"').strip("'")
    return text, fm, body


def scan_scripts(skill_dir: Path):
    """只读扫描 scripts 目录，产出能力清单。不执行任何脚本。"""
    scripts_dir = skill_dir / "scripts"
    capabilities = []
    if not scripts_dir.is_dir():
        return capabilities
    danger_tokens = {
        "network": ["requests", "urllib", "http", "socket", "aiohttp", "httpx"],
        "subprocess": ["subprocess", "os.system", "popen", "shell"],
        "dynamic": ["eval(", "exec(", "__import__", "pickle.load", "marshal", "compile("],
        "credential": ["os.environ", "getenv", "api_key", "token", "password", "secret"],
        "file_write": [".write(", "open(", "shutil", "os.remove", "os.unlink", "rmtree"],
    }
    for py in sorted(scripts_dir.rglob("*.py")):
        try:
            content = py.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        found = []
        for cat, tokens in danger_tokens.items():
            if any(t in content for t in tokens):
                found.append(cat)
        capabilities.append({"file": str(py.relative_to(skill_dir)), "flags": found})
    return capabilities


def hard_checks(skill_dir: Path):
    """执行全部硬指标检查，返回结果字典。"""
    results = {}
    name = skill_dir.name
    results["dir_name"] = name
    results["name_valid"] = bool(NAME_RE.match(name))

    text, fm, body = read_skill_md(skill_dir)

    if text is None:
        results["skill_md_exists"] = False
        results["checks"] = []
        return results

    results["skill_md_exists"] = True

    checks = []

    def add(key, passed, detail=""):
        checks.append({"key": key, "passed": passed, "detail": detail})

    # name 与目录同名
    fm_name = fm.get("name", "")
    add("name_matches_dir", fm_name == name,
        f"frontmatter.name='{fm_name}' vs 目录名='{name}'")

    # description 长度 20-1024
    desc = fm.get("description", "")
    add("description_length", 20 <= len(desc) <= 1024,
        f"description 长度={len(desc)}")

    # description 四要素启发式检查（做什么/何时用/触发短语）
    desc_lower = desc.lower()
    has_action = any(w in desc for w in ["制作", "审查", "优化", "生成", "build", "review", "create", "make", "优化"])
    has_when = any(w in desc for w in ["当", "时", "when", "use when", "触发"])
    add("description_elements", has_action and has_when,
        f"含'做什么'={'是' if has_action else '否'}，含'何时用'={'是' if has_when else '否'}")

    # version 和 agent_created
    has_version = "version" in fm
    agent_created = fm.get("agent_created", "").lower() == "true"
    add("has_version", has_version, f"version={'有' if has_version else '无'}")
    add("agent_created", agent_created, f"agent_created={'true' if agent_created else '缺失'}")

    # 正文行数 <= 500
    line_count = len(body.splitlines())
    add("body_under_500_lines", line_count <= 500, f"正文行数={line_count}")

    # TODO / 占位符检测
    todo_pattern = re.compile(r"\b(TODO|FIXME|XXX|TBD|待办|占位|placeholder|示例脚本|example\.py)\b", re.IGNORECASE)
    todos = todo_pattern.findall(body)
    add("no_todo", len(todos) == 0, f"检测到占位符: {', '.join(sorted(set(todos))) if todos else '无'}")

    # 加载式引用完整性：正文中 @reference/文件名 或 references/ 引用需真实存在
    ref_mentions = re.findall(r"`?(references/[\w\-./]+\.md)`?", body)
    missing_refs = []
    for ref in ref_mentions:
        p = skill_dir / ref.strip("`")
        if not p.is_file():
            missing_refs.append(ref)
    add("references_valid", len(missing_refs) == 0,
        f"缺失引用: {missing_refs if missing_refs else '无'}")

    # 脚本能力预检
    capabilities = scan_scripts(skill_dir)
    risky = [c for c in capabilities if c["flags"]]
    add("scripts_clean", len(risky) == 0,
        f"脚本数={len(capabilities)}，有风险标记的脚本={len(risky)}")
    results["script_capabilities"] = capabilities

    results["checks"] = checks
    results["frontmatter_keys"] = sorted(fm.keys())
    return results


def render_text(r):
    if not r.get("skill_md_exists"):
        print(f"目录: {r.get('dir_name')}")
        print("[FAIL] 未找到 SKILL.md")
        return
    print(f"目录: {r['dir_name']}")
    print(f"frontmatter 字段: {', '.join(r.get('frontmatter_keys', []))}")
    print("-" * 50)
    for c in r["checks"]:
        mark = "[PASS]" if c["passed"] else "[FAIL]"
        print(f"{mark} {c['key']}: {c['detail']}")
    print("-" * 50)
    caps = r.get("script_capabilities", [])
    if caps:
        print("脚本能力预检:")
        for c in caps:
            flags = ", ".join(c["flags"]) if c["flags"] else "无风险标记"
            print(f"  {c['file']}: {flags}")


def main():
    if len(sys.argv) < 2:
        print("用法: python score_skill.py <skill目录> [--json]", file=sys.stderr)
        sys.exit(2)
    target = Path(sys.argv[1])
    if not target.is_dir():
        print(f"错误: 目录不存在 {target}", file=sys.stderr)
        sys.exit(2)
    result = hard_checks(target)
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        render_text(result)
    sys.exit(0)


if __name__ == "__main__":
    main()
