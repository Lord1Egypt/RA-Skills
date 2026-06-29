#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Problem Logger — 结构化问题日志管理工具
"""

import json
import os
import sys
import argparse
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import hashlib

# R-12 审计锚点（放在 import 之后）
DEFAULT_DATA_DIR_RAW = "skills/.standardization/triphasic-execution/data/"
_data_dir_abs = os.path.normpath(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "..", DEFAULT_DATA_DIR_RAW
))

# ============================================================================
# 路径配置 — 统一指向 skills/.standardization/triphasic-execution/
# ============================================================================
_SKILL_DIR = Path(__file__).resolve().parent.parent

def _find_standardization_dir() -> Path:
    p = _SKILL_DIR.resolve()
    for parent in [p] + list(p.parents):
        if parent.name == "skills" and parent.parent.name != "skills":
            return parent / ".standardization" / _SKILL_DIR.name
    return _SKILL_DIR.parent / ".standardization" / _SKILL_DIR.name

_DEFAULT_HOME = _find_standardization_dir()
_TRIPHASIC_HOME = Path(os.environ.get("TRIPHASIC_HOME", str(_DEFAULT_HOME)))


def get_home() -> Path:
    """获取 TRIPHASIC_HOME，确保目录存在"""
    home = _TRIPHASIC_HOME
    home.mkdir(parents=True, exist_ok=True)
    return home


def get_logs_dir() -> Path:
    """获取日志目录（规范：logs/）"""
    return get_home() / "logs"


def get_config_file() -> Path:
    """获取配置文件路径"""
    return get_home() / "config.json"


def get_problems_jsonl() -> Path:
    """获取 JSONL 问题日志路径"""
    return get_logs_dir() / "problems.jsonl"


def get_problems_md() -> Path:
    """获取 PROBLEMS.md 路径（规范：output/）"""
    return get_home() / "output" / "PROBLEMS.md"


def get_risks_md() -> Path:
    """获取 RISKS.md 路径（规范：output/）"""
    return get_home() / "output" / "RISKS.md"


def get_lessons_md() -> Path:
    """获取 LESSONS_REGISTER.md 路径（规范：output/）"""
    return get_home() / "output" / "LESSONS_REGISTER.md"


def get_risks_jsonl() -> Path:
    """获取 JSONL 风险日志路径"""
    return get_logs_dir() / "risks.jsonl"


def get_exec_pipe() -> Path:
    """获取 exec 输出管道文件路径"""
    return get_home() / ".exec_output_pipe.txt"


def load_config() -> dict:
    """加载用户配置，缺失字段用默认值填充"""
    default_path = Path(__file__).parent.parent / "assets" / "default_config.json"
    defaults = {}
    if default_path.exists():
        try:
            defaults = json.loads(default_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    user_path = get_config_file()
    if user_path.exists():
        try:
            user_cfg = json.loads(user_path.read_text(encoding="utf-8"))
            defaults.update(user_cfg)
        except Exception:
            pass

    return defaults


# ============================================================================
# Windows 编码兼容
# ============================================================================
if sys.platform == "win32":
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    except Exception:
        pass


# ============================================================================
# 工具函数
# ============================================================================
MAX_RECENT = 50


def get_problem_id(scene: str, symptom: str) -> str:
    """生成问题唯一 ID（用于去重）"""
    key = f"{scene}|{symptom}"
    return hashlib.md5(key.encode()).hexdigest()[:8].upper()


def load_problems() -> list[dict]:
    """加载所有问题记录"""
    log = get_problems_jsonl()
    if not log.exists():
        return []
    problems = []
    with open(log, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    problems.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return problems


def save_problem(problem: dict):
    """追加保存问题记录（JSONL，保证不丢失）"""
    get_logs_dir().mkdir(parents=True, exist_ok=True)
    with open(get_problems_jsonl(), "a", encoding="utf-8") as f:
        f.write(json.dumps(problem, ensure_ascii=False) + "\n")
        f.flush()


def search_problems(keyword: str) -> list[dict]:
    """搜索关键词相关的问题"""
    all_probs = load_problems()
    hits = []
    for p in all_probs:
        text = f"{p.get('scene', '')} {p.get('symptom', '')} {p.get('cause', '')} {p.get('solution', '')}".lower()
        if keyword.lower() in text:
            hits.append(p)
    return sorted(hits, key=lambda x: x.get("timestamp", ""), reverse=True)


def get_next_problem_number() -> int:
    """获取下一个问题编号"""
    all_probs = load_problems()
    if not all_probs:
        return 1
    numbers = []
    for p in all_probs:
        num_str = str(p.get("number", "P0"))
        try:
            numbers.append(int(num_str.lstrip("P")))
        except ValueError:
            continue
    return max(numbers) + 1 if numbers else 1


def get_next_risk_number() -> int:
    """获取下一个风险编号"""
    risks = load_risks()
    if not risks:
        return 1
    numbers = []
    for r in risks:
        num_str = str(r.get("number", "R0"))
        try:
            numbers.append(int(num_str.lstrip("R")))
        except ValueError:
            continue
    return max(numbers) + 1 if numbers else 1


def load_risks() -> list[dict]:
    """加载所有风险记录"""
    log = get_risks_jsonl()
    if not log.exists():
        return []
    risks = []
    with open(log, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    risks.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    return risks


def save_risk(risk: dict):
    """追加保存风险记录（JSONL，保证不丢失）"""
    get_logs_dir().mkdir(parents=True, exist_ok=True)
    with open(get_risks_jsonl(), "a", encoding="utf-8") as f:
        f.write(json.dumps(risk, ensure_ascii=False) + "\n")
        f.flush()


# ============================================================================
# 命令实现
# ============================================================================
def cmd_add(args):
    """添加问题记录"""
    problem = {
        "id": get_problem_id(args.scene, args.symptom),
        "number": f"P{get_next_problem_number():03d}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "scene": args.scene,
        "symptom": args.symptom,
        "cause": args.cause or "待分析",
        "solution": args.solution or "待解决",
        "status": "已解决" if args.solution else "未解决",
        "related_task": args.task or None,
    }

    # 去重检查
    all_probs = load_problems()
    duplicates = [p for p in all_probs if p.get("id") == problem["id"]]

    if duplicates:
        print(f"⚠️  检测到重复问题（ID: {problem['id']}）")
        print(f"   已有记录：{duplicates[-1]['number']} @ {duplicates[-1]['timestamp']}")
        print(f"   场景：{duplicates[-1]['scene']}")
        if args.force:
            print("   --force 已指定，追加新记录")
        else:
            print("   跳过重复记录。使用 --force 强制添加。")
            return 0

    save_problem(problem)

    # 同步更新 PROBLEMS.md
    problems_file = get_problems_md()
    problems_file.parent.mkdir(parents=True, exist_ok=True)

    entry = f"""### [{problem['number']}] {problem['symptom'][:60]}

- **记录时间**: {problem['timestamp']}
- **场景**: {problem['scene']}
- **现象**: {problem['symptom']}
- **原因**: {problem['cause']}
- **解决方案**: {problem['solution']}
- **状态**: {problem['status']}
- **关联任务**: {problem.get('related_task', 'N/A')}

---
"""
    with open(problems_file, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"✅ 问题已记录：{problem['number']} @ {problem['timestamp']}")
    print(f"   场景：{problem['scene']}")
    print(f"   现象：{problem['symptom']}")
    if problem["cause"] != "待分析":
        print(f"   原因：{problem['cause']}")
    if problem["solution"] != "待解决":
        print(f"   解决：{problem['solution']}")
    return 0


def cmd_add_risk(args):
    """添加风险记录"""
    risk = {
        "id": f"R{get_next_risk_number():03d}",
        "number": f"R{get_next_risk_number():03d}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "description": args.description,
        "impact": args.impact or "待评估",
        "mitigation": args.mitigation or "待制定",
        "status": "已缓解" if args.mitigation else "监控中",
        "related_task": args.task or None,
    }

    save_risk(risk)

    # 更新 RISKS.md
    risks_file = get_risks_md()
    risks_file.parent.mkdir(parents=True, exist_ok=True)

    entry = f"""### [{risk['number']}] {risk['description'][:60]}

- **识别时间**: {risk['timestamp']}
- **影响评估**: {risk['impact']}
- **缓解措施**: {risk['mitigation']}
- **状态**: {risk['status']}
- **关联任务**: {risk.get('related_task', 'N/A')}

---
"""
    with open(risks_file, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"✅ 风险已记录：{risk['number']} @ {risk['timestamp']}")
    print(f"   描述：{risk['description'][:60]}...")
    print(f"   影响：{risk['impact']}")
    print(f"   缓解：{risk['mitigation']}")
    return 0


def cmd_list(args):
    """列出问题记录"""
    n = args.recent or MAX_RECENT
    all_probs = load_problems()
    recent = sorted(all_probs, key=lambda x: x.get("timestamp", ""), reverse=True)[:n]

    if not recent:
        print("📭 暂无问题记录")
        return 0

    print(f"📋 最近 {len(recent)} 条问题记录:\n")
    for p in recent:
        status_icon = "✅" if p["status"] == "已解决" else "❌"
        print(f"{status_icon} [{p['number']}] {p['timestamp']} | {p['scene'][:40]}")
        symptom = p['symptom']
        print(f"    现象：{symptom[:60]}..." if len(symptom) > 60 else f"    现象：{symptom}")
        if p["cause"] != "待分析":
            cause = p["cause"]
            print(f"    原因：{cause[:50]}..." if len(cause) > 50 else f"    原因：{cause}")
        if p["solution"] != "待解决":
            sol = p["solution"]
            print(f"    解决：{sol[:50]}..." if len(sol) > 50 else f"    解决：{sol}")
        print()
    return 0


def cmd_search(args):
    """搜索问题"""
    hits = search_problems(args.keyword)

    if not hits:
        print(f"🔍 未找到与「{args.keyword}」相关的问题")
        return 0

    print(f"🔍 找到 {len(hits)} 条匹配记录:\n")
    for p in hits:
        status_icon = "✅" if p["status"] == "已解决" else "❌"
        print(f"{status_icon} [{p['number']}] {p['timestamp']} | {p['scene']}")
        print(f"    现象：{p['symptom']}")
        if p["cause"] != "待分析":
            print(f"    原因：{p['cause']}")
        if p["solution"] != "待解决":
            print(f"    解决：{p['solution']}")
        print()
    return 0


def cmd_update(args):
    """更新问题（补充原因/解决路径）"""
    all_probs = load_problems()
    matching = [p for p in all_probs if p.get("id") == args.id or p.get("number") == f"P{args.id}"]
    if not matching:
        print(f"❌ 未找到问题 ID={args.id}")
        return 1

    target = matching[-1]
    updated = False

    if args.cause and target["cause"] == "待分析":
        target["cause"] = args.cause
        print(f"✅ 已补充原因：{args.cause}")
        updated = True

    if args.solution and target["solution"] == "待解决":
        target["solution"] = args.solution
        target["status"] = "已解决"
        print(f"✅ 已补充解决方案：{args.solution}")
        updated = True

    if not updated:
        print("⚠️  未进行更新（原因和解决路径均已存在）")
        return 0

    save_problem(target)
    print(f"\n📝 问题 {target['number']} 已更新 @ {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    return 0


def cmd_merge_to_lessons(args):
    """合并问题清单和风险手册到经验教训登记册"""
    print("🔨 正在生成经验教训登记册...")

    all_probs = load_problems()
    resolved = [p for p in all_probs if p["status"] == "已解决"]
    unresolved = [p for p in all_probs if p["status"] == "未解决"]

    risks_content = ""
    risks_file = get_risks_md()
    if risks_file.exists():
        risks_content = risks_file.read_text(encoding="utf-8")

    home = get_home()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    header = f"""# 📚 经验教训登记册 (Lessons Learned Register)

> **生成时间**: {now}
> **来源**: 问题清单 ({get_problems_jsonl().name}) + 风险手册 ({get_risks_md().name})
> **目的**: 固化过程资产，避免重复踩坑

---

"""

    # Part 1: 已解决
    part1 = "## ✅ 已解决的教训 (Resolved)\n\n"
    if resolved:
        for p in sorted(resolved, key=lambda x: x["timestamp"]):
            part1 += f"""### [{p['number']}] {p['scene']}

- **发生时间**: {p['timestamp']}
- **现象**: {p['symptom']}
- **根因**: {p['cause']}
- **解决方案**: {p['solution']}
- **关联任务**: {p.get('related_task', 'N/A')}

---

"""
    else:
        part1 += "*暂无已解决的问题记录*\n\n---\n\n"

    # Part 2: 未解决
    part2 = "## ⚠️ 待解决的教训 (Unresolved)\n\n"
    if unresolved:
        for p in sorted(unresolved, key=lambda x: x["timestamp"]):
            part2 += f"""### [{p['number']}] {p['scene']}

- **发生时间**: {p['timestamp']}
- **现象**: {p['symptom']}
- **关联任务**: {p.get('related_task', 'N/A')}

---

"""
    else:
        part2 += "*暂无未解决的问题记录*\n\n---\n\n"

    # Part 3: 风险手册
    part3 = "## 📕 已知风险 (Known Risks)\n\n"
    if risks_file.exists() and risks_content.strip():
        risk_lines = [l for l in risks_content.split("\n") if l.strip() and not l.startswith("# ")]
        part3 += "\n".join(risk_lines) + "\n\n---\n\n"
    else:
        part3 += "*暂无风险记录*\n\n---\n\n"

    # Part 4: 使用指南
    script_path = Path(__file__).resolve()
    part4 = f"""## 📖 使用指南

### 执行前检索
```bash
python "{script_path}" search "关键词"
```

### 增量更新
新问题记录后，运行 `merge-to-lessons` 命令合并到本文件。

---

*本文件由 problem_logger.py 自动生成，手动修改可能被覆盖。*
"""

    full_content = header + part1 + part2 + part3 + part4
    get_lessons_md().write_text(full_content, encoding="utf-8")

    print(f"✅ 经验教训登记册已生成：{get_lessons_md()}")
    print(f"   - 已解决的问题：{len(resolved)} 条")
    print(f"   - 未解决的问题：{len(unresolved)} 条")
    if risks_file.exists() and risks_content.strip():
        print(f"   - 风险记录：从 RISKS.md 合并")
    return 0


def cmd_init(args):
    """初始化 TRIPHASIC_HOME 目录结构"""
    home = get_home()
    logs = get_logs_dir()

    print(f"📦 初始化 Triphasic Execution 数据目录...")
    print(f"   TRIPHASIC_HOME: {home}")

    # 复制默认配置（如果不存在）
    config = get_config_file()
    if not config.exists():
        default = Path(__file__).parent.parent / "assets" / "default_config.json"
        if default.exists():
            shutil.copy2(default, config)
            print(f"   ✅ 默认配置已写入：{config}")

    # 创建日志目录
    logs.mkdir(parents=True, exist_ok=True)
    print(f"   ✅ 日志目录：{logs}")

    # 检查其他文件
    for name, path in [("问题清单", get_problems_md()), ("风险手册", get_risks_md()),
                       ("经验教训登记册", get_lessons_md())]:
        if not path.exists():
            path.write_text(f"# {name}\n\n*暂无记录*\n", encoding="utf-8")
            print(f"   ✅ {name}：{path}")
        else:
            print(f"   ⏭️  {name}：已存在")

    print(f"\n🎉 初始化完成！TRIPHASIC_HOME={home}")
    return 0


# ============================================================================
# CLI 入口
# ============================================================================
def main():
    parser = argparse.ArgumentParser(
        description="Problem Logger — 结构化问题日志管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 初始化数据目录
  python problem_logger.py init

  # 添加新问题
  python problem_logger.py add --scene "API测试" --symptom "HTTP 503" --cause "服务端限流" --solution "增加重试机制"

  # 列出最近问题
  python problem_logger.py list --recent 10

  # 搜索关键词
  python problem_logger.py search "503"

  # 补充原因/解决路径
  python problem_logger.py update --id P001 --cause "xxx" --solution "yyy"

  # 合并到经验教训登记册
  python problem_logger.py merge-to-lessons

环境变量:
  TRIPHASIC_HOME  数据目录（默认 ~/.workbuddy/triphasic/）
        """,
    )

    parser.add_argument("--home", type=str, default=None, help="覆盖 TRIPHASIC_HOME")

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # init
    subparsers.add_parser("init", help="初始化数据目录")

    # add
    p_add = subparsers.add_parser("add", help="添加问题记录")
    p_add.add_argument("--scene", required=True, help="场景描述")
    p_add.add_argument("--symptom", required=True, help="现象描述")
    p_add.add_argument("--cause", default=None, help="原因分析")
    p_add.add_argument("--solution", default=None, help="解决方案")
    p_add.add_argument("--task", default=None, help="关联任务")
    p_add.add_argument("--force", action="store_true", help="强制添加重复记录")

    # add-risk
    p_risk = subparsers.add_parser("add-risk", help="添加风险记录")
    p_risk.add_argument("--description", required=True, help="风险描述")
    p_risk.add_argument("--impact", default=None, help="影响评估")
    p_risk.add_argument("--mitigation", default=None, help="缓解措施")
    p_risk.add_argument("--task", default=None, help="关联任务")

    # list
    p_list = subparsers.add_parser("list", help="列出问题记录")
    p_list.add_argument("--recent", type=int, default=MAX_RECENT, help=f"最近 N 条（默认{MAX_RECENT}）")

    # search
    p_search = subparsers.add_parser("search", help="搜索问题")
    p_search.add_argument("keyword", help="关键词")

    # update
    p_update = subparsers.add_parser("update", help="更新问题（补充原因/解决）")
    p_update.add_argument("--id", required=True, help="问题 ID 或编号")
    p_update.add_argument("--cause", default=None, help="补充原因分析")
    p_update.add_argument("--solution", default=None, help="补充解决方案")

    # merge-to-lessons
    subparsers.add_parser("merge-to-lessons", help="合并到经验教训登记册")

    args = parser.parse_args()

    # --home 覆盖
    if args.home:
        global _TRIPHASIC_HOME
        _TRIPHASIC_HOME = Path(args.home).expanduser().resolve()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "init":
        return cmd_init(args)
    elif args.command == "add":
        return cmd_add(args)
    elif args.command == "add-risk":
        return cmd_add_risk(args)
    elif args.command == "list":
        return cmd_list(args)
    elif args.command == "search":
        return cmd_search(args)
    elif args.command == "update":
        return cmd_update(args)
    elif args.command == "merge-to-lessons":
        return cmd_merge_to_lessons(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
