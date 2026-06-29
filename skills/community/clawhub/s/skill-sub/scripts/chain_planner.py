#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chain_planner.py - Chain Planner v1.29.1
链规划流水线：统一"搜索步骤→校验衔接→创建链"全流程。

三种模式：
  1. plan（交互规划）: 给定意图，搜索步骤 → LLM 选 → validate → 确认创建
  2. script（全自动）: 给定步骤ID列表，validate → 自动创建
  3. suggest（增强推荐）: 搜步骤 + 自动 validate 衔接

依赖：skill_extractor, step_indexer, step_link_validator, chain_manager
零外部依赖，仅 Python 标准库。
"""

import argparse
import json
import os
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))


def _import_extras():
    """延迟导入依赖模块"""
    from step_indexer import cmd_search as step_search
    from step_link_validator import validate_link
    from chain_manager import PathManager, ChainManager, _save_blueprint_snapshot
    from skill_extractor import find_skill_dir, extract_step_semantics
    return step_search, validate_link, PathManager, ChainManager, _save_blueprint_snapshot, find_skill_dir, extract_step_semantics


# ============================================================
# 模式 1: plan - 交互规划
# ============================================================

def cmd_plan(args):
    """交互规划模式：意图 → 搜索 → 选步骤 → validate → 创建"""
    step_search, validate_link, PathManager, ChainManager, _, find_skill_dir, extract_step_semantics = _import_extras()

    intent = args.intent
    print(f"🧩 链规划: {intent}")
    print(f"{'='*55}")

    # 1. 搜索候选步骤
    print(f"\n🔍 第1步: 搜索匹配步骤...")
    candidates = _search_steps(intent, step_search, args.min_score)
    if not candidates:
        print(f"❌ 未找到匹配的步骤，请调整意图或降低 --min-score")
        return 1

    print(f"   找到 {len(candidates)} 个候选步骤（显示前 {min(args.topk, len(candidates))} 个）：")
    for i, c in enumerate(candidates[:args.topk], 1):
        print(f"   {i}. [{c['score']}] {c['step_id']}: {c['step_name'][:40]}")
        if c.get("consumes"):
            print(f"      输入: {'; '.join(c['consumes'][:2])}")
        if c.get("produces"):
            print(f"      输出: {'; '.join(c['produces'][:2])}")

    # 2. LLM 选取步骤（输出给 AI，由 AI 返回 step_id 列表）
    print(f"\n🤖 第2步: LLM 选取步骤")
    print(f"   请从以上候选中选择步骤ID，按执行顺序排列（逗号分隔）")
    print(f"   或直接提供 --steps 参数跳过此步")
    if not args.steps:
        print(f"\n   💡 示例用法：")
        print(f"   chain_planner.py plan \\")
        print(f"     --intent \"{intent}\" \\")
        print(f"     --steps \"skill-A.步1,skill-B.步3,skill-A.步5\"")
        return 0

    # 3. 校验步骤可用性
    print(f"\n✅ 第3步: 校验步骤可用性...")
    selected = args.steps.split(",")
    validated = []
    for step_id in selected:
        step_id = step_id.strip()
        skill_name = step_id.split(".")[0]
        skill_dir = find_skill_dir(skill_name)
        if not skill_dir:
            print(f"   ❌ 技能 '{skill_name}' 不存在（{step_id}）")
            continue
        steps_info = extract_step_semantics(skill_dir)
        matched = False
        for si in steps_info:
            if si.get("step_id") == step_id or step_id.endswith(si.get("step_name", "")):
                validated.append(si)
                matched = True
                print(f"   ✅ {step_id}")
                break
        if not matched:
            # 模糊匹配
            for si in steps_info:
                rel = step_id.split(".", 1)[-1]
                if rel in si.get("step_id", ""):
                    validated.append(si)
                    print(f"   ✅ {step_id} → {si['step_id']}")
                    matched = True
                    break
        if not matched:
            print(f"   ⚠️  {step_id}: 未精确匹配到步骤，仍会保留（基于 action 描述）")
            validated.append({"step_id": step_id, "step_name": step_id, "interface": {"consumes": [], "produces": []}})

    if not validated:
        print(f"❌ 没有可用的步骤，终止")
        return 1

    # 4. 衔接校验
    print(f"\n🔗 第4步: 步骤衔接校验...")
    gaps_found = 0
    for i in range(len(validated) - 1):
        step_a = validated[i]
        step_b = validated[i + 1]
        iface_a = step_a.get("interface", {})
        iface_b = step_b.get("interface", {})
        result = validate_link(iface_a, iface_b,
                               step_a.get("step_name", f"步骤{i+1}"),
                               step_b.get("step_name", f"步骤{i+2}"))
        a_name = step_a.get("step_name", "?")[:25]
        b_name = step_b.get("step_name", "?")[:25]
        if result["passed"]:
            print(f"   ✅ {a_name} → {b_name} (分数: {result['score']})")
        else:
            gaps_found += 1
            print(f"   ⛔ {a_name} → {b_name}")
            print(f"      缺口: {result['gap_type']} (分数: {result['score']})")
            if result.get("adhesion_suggestion"):
                sug = result["adhesion_suggestion"]
                print(f"      建议: {sug['reason'][:80]}")
                print(f"      方案: {len(sug['solutions'])} 个")

    if gaps_found > 0:
        print(f"\n⚠️  检测到 {gaps_found} 个衔接缺口，建议检查后手动补充粘连点步骤")
        if not args.force:
            print(f"   使用 --force 强制创建（会生成无粘连点的链）")
            return 1

    # 5. 构建步骤 JSON
    steps_json = []
    for i, v in enumerate(validated, 1):
        step = {
            "index": i,
            "type": "skill",
            "step_name": v.get("step_name", f"步骤{i}"),
            "skill_name": v.get("step_id", "").split(".")[0] if v.get("step_id") else "",
            "action": v.get("description", v.get("step_name", ""))[:200],
            "depends_on": [i - 1] if i > 1 else [],
        }
        # 如果有 call_address 中的指令，记录
        ca = v.get("call_address", {})
        if ca.get("instructions"):
            step["skill_instruction"] = ca["instructions"][0]
        steps_json.append(step)

    # 6. 创建链
    print(f"\n🚀 第5步: 创建调用链...")
    chain_name = args.name or _auto_name(intent)
    cm = ChainManager()
    success, msg = cm.create_chain(
        name=chain_name,
        description=intent,
        purpose=args.purpose or intent,
        tags=args.tags.split(",") if args.tags else [],
        steps=steps_json,
        user_specified=args.user
    )
    if success:
        print(f"   ✅ {msg}")
        print(f"   链目录: {cm.path_manager.chains_dir / chain_name}")
        print(f"   ├── chain.json")
        print(f"   └── blueprints.json")
        return 0
    else:
        print(f"   ❌ {msg}")
        return 1


# ============================================================
# 模式 2: script - 全自动
# ============================================================

def cmd_script(args):
    """全自动模式：给定步骤ID列表，直接生成链"""
    # 转为 plan --steps 模式执行
    args.intent = args.name or "自动链"
    args.min_score = 0.0
    args.topk = 10
    args.force = True
    args.user = True
    if not args.tags:
        args.tags = "auto-generated"
    return cmd_plan(args)


# ============================================================
# 模式 3: suggest - 增强推荐
# ============================================================

def cmd_suggest(args):
    """增强推荐：搜索步骤 + 自动 validate 衔接"""
    step_search, validate_link, _, _, _, find_skill_dir, extract_step_semantics = _import_extras()

    intent = args.intent
    print(f"🔍 增强推荐: {intent}")
    print(f"{'='*55}")

    candidates = _search_steps(intent, step_search, args.min_score)
    if not candidates:
        print(f"❌ 未找到匹配步骤")
        return 1

    print(f"\n📋 候选步骤 ({len(candidates)} 个):")
    print(f"{'':-<100}")
    print(f"{'排名':<4} {'步骤ID':<35} {'分数':<6} {'步骤名':<30} {'I/O'}")
    print(f"{'':-<100}")

    for i, c in enumerate(candidates[:args.topk], 1):
        step_id = c["step_id"][:34]
        name = c["step_name"][:28]
        io = ""
        if c.get("produces"):
            io += "📤"
        if c.get("consumes"):
            io += "📥"
        print(f"{i:<4} {step_id:<35} {c['score']:<6} {name:<30} {io}")

    # 对推荐结果做自动衔接分析：看任意两个步骤之间能否串联
    print(f"\n🔗 自动衔接分析（前 {min(5, len(candidates))} 个候选):")
    chain_candidates = candidates[:5]
    for i in range(len(chain_candidates) - 1):
        a = chain_candidates[i]
        b = chain_candidates[i + 1]
        # 构建简易 interface
        iface_a = {"consumes": [{"type": "text", "desc": d} for d in a.get("consumes", [])],
                   "produces": [{"type": "text", "desc": d} for d in a.get("produces", [])]}
        iface_b = {"consumes": [{"type": "text", "desc": d} for d in b.get("consumes", [])],
                   "produces": [{"type": "text", "desc": d} for d in b.get("produces", [])]}
        result = validate_link(iface_a, iface_b, a["step_name"], b["step_name"])
        status = "✅" if result["passed"] else "⛔"
        print(f"  {status} {a['step_id'][:25]} → {b['step_id'][:25]} ({result['gap_type']}, {result['score']})")

    if args.json:
        result = {
            "intent": intent,
            "total": len(candidates),
            "candidates": candidates[:args.topk],
        }
        print(f"\n{json.dumps(result, ensure_ascii=False, indent=2)}")

    return 0


# ============================================================
# 共享函数
# ============================================================

def _search_steps(intent, step_search_fn, min_score):
    """包装 step_indexer search 返回结构化结果"""
    class FakeArgs:
        def __init__(self, intent, min_score):
            self.intent = intent
            self.min_score = min_score
            self.skill = ""
            self.json = True
            self.limit = 100

    # 捕获 JSON 输出
    old_stdout = sys.stdout
    sys.stdout = _CaptureStdout()
    try:
        step_search_fn(FakeArgs(intent, min_score))
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout

    # 解析 JSON
    try:
        data = json.loads(output)
        return data.get("results", [])
    except (json.JSONDecodeError, TypeError):
        return []


def _auto_name(intent):
    """从意图自动生成链名"""
    # 取意图的前 20 个字符作为名称
    name = intent.strip()[:20]
    # 移除特殊字符
    import re
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    return name.strip() or "未命名链"


class _CaptureStdout:
    """捕获标准输出"""
    def __init__(self):
        self._buffer = []
    def write(self, s):
        self._buffer.append(s)
    def getvalue(self):
        return "".join(self._buffer)
    def flush(self):
        pass


# ============================================================
# CLI 入口
# ============================================================

def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(
        description="Chain Planner v1.29.1 - 链规划流水线",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # plan: 交互规划
  python chain_planner.py plan --intent "代码审查并修复" --steps "skill-standardization.R-01,triphasic-execution.execute,skill-standardization.R-25" --name "审查修复链"

  # script: 全自动
  python chain_planner.py script --steps "skill-standardization.R-01,git-sync.push" --name "快速链"

  # suggest: 增强推荐
  python chain_planner.py suggest --intent "代码审查 分析 报告"
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # plan
    p_plan = subparsers.add_parser("plan", help="交互规划链")
    p_plan.add_argument("--intent", required=True, help="用户意图描述")
    p_plan.add_argument("--steps", default="", help="选定的步骤ID（逗号分隔）")
    p_plan.add_argument("--name", default="", help="链名称（可选，默认从意图生成）")
    p_plan.add_argument("--purpose", default="", help="链目的")
    p_plan.add_argument("--tags", default="", help="标签（逗号分隔）")
    p_plan.add_argument("--min-score", type=float, default=0.15, help="最低匹配分数")
    p_plan.add_argument("--topk", type=int, default=10, help="显示候选数")
    p_plan.add_argument("--force", action="store_true", help="强制创建（忽略衔接缺口）")
    p_plan.add_argument("--user", action="store_true", help="标记为用户指定链（自愈时跳过）")

    # script
    p_script = subparsers.add_parser("script", help="全自动生成链")
    p_script.add_argument("--steps", required=True, help="步骤ID列表（逗号分隔）")
    p_script.add_argument("--name", required=True, help="链名称")
    p_script.add_argument("--purpose", default="", help="链目的")
    p_script.add_argument("--tags", default="auto-generated", help="标签")

    # suggest
    p_suggest = subparsers.add_parser("suggest", help="增强步骤推荐")
    p_suggest.add_argument("--intent", required=True, help="用户意图")
    p_suggest.add_argument("--min-score", type=float, default=0.15, help="最低匹配分数")
    p_suggest.add_argument("--topk", type=int, default=10, help="显示候选数")
    p_suggest.add_argument("--json", action="store_true", help="JSON 格式输出")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "plan": cmd_plan,
        "script": cmd_script,
        "suggest": cmd_suggest,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        return cmd_func(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
