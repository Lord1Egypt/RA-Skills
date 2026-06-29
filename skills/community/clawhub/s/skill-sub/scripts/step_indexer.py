#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
step_indexer.py - Step Blueprint Indexer v1.29.0
步骤蓝图索引器：扫描已安装技能，构建步骤级蓝图索引，
支持搜索、状态查询、增量更新。

零外部依赖，仅使用 Python 标准库。
跨平台支持 Windows/Linux/macOS。

数据目录：
  ~/.workbuddy/skills/.standardization/skill-sub/step_index/
  ├── _blueprint.json          ← 元索引（版本/构建时间/技能数/步骤数）
  ├── skill-name.json          ← 每个技能一个步骤蓝图文件
  └── ...
"""

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-sub/data/"
SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR.parent / ".standardization" / "skill-sub" / "data"


# ============================================================

# 导入同目录的 skill_extractor
SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL_DIR / "scripts"))

try:
    from skill_extractor import (
        get_skills_dir, find_skill_dir, read_skill_md,
        extract_frontmatter, extract_description, extract_core_commands,
        extract_trigger_keywords, extract_step_semantics,
    )
except ImportError:
    # 直接导入
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "skill_extractor",
        str(SKILL_DIR / "scripts" / "skill_extractor.py")
    )
    skill_extractor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(skill_extractor)
    get_skills_dir = skill_extractor.get_skills_dir
    find_skill_dir = skill_extractor.find_skill_dir
    read_skill_md = skill_extractor.read_skill_md
    extract_frontmatter = skill_extractor.extract_frontmatter
    extract_description = skill_extractor.extract_description
    extract_core_commands = skill_extractor.extract_core_commands
    extract_trigger_keywords = skill_extractor.extract_trigger_keywords
    extract_step_semantics = skill_extractor.extract_step_semantics

# ============================================================
# 路径配置
# ============================================================

def get_index_dir():
    """获取步骤索引目录"""
    env_home = os.environ.get("SKILL_SUB_HOME") or os.environ.get("SKILL_CHAIN_HOME")
    if env_home:
        base = Path(env_home)
    else:
        base = Path.home() / ".workbuddy" / "skills" / ".standardization" / "skill-sub"
    idx_dir = base / "step_index"
    idx_dir.mkdir(parents=True, exist_ok=True)
    return idx_dir

INDEX_DIR = get_index_dir()
META_INDEX = INDEX_DIR / "_blueprint.json"

# ============================================================
# v1.29.1: 同义词字典 + 中文 n-gram 匹配
# ============================================================

_SYNONYM_MAP = {
    # 代码相关
    "代码": "code",
    "审查": "review audit 审",
    "审计": "audit 审",
    "审": "review audit",
    "扫描": "scan",
    "检测": "detect check",
    "验证": "verify validate",
    "校验": "validate verify check",
    "测试": "test",
    "构建": "build compile",
    "编译": "compile build",
    "部署": "deploy release",
    "发布": "publish release deploy",
    "上线": "deploy release",
    "推送": "push sync",
    "同步": "sync push",
    "打包": "pack zip",
    "分析": "analyze analysis",
    "处理": "process handle",
    "计算": "calculate compute",
    "统计": "stats statistics",
    "报告": "report",
    "数据": "data",
    "配置": "config",
    "参数": "param parameter",
    "结果": "result output",
    "输出": "output result",
    "输入": "input",
    "生成": "generate create",
    "创建": "create generate new",
    "导出": "export",
    "导入": "import",
    "保存": "save write",
    "读取": "read load",
    "加载": "load read",
    "文档": "doc document",
    "文件": "file",
    "目录": "dir directory folder",
    "路径": "path",
    "模板": "template",
    "格式": "format",
    "规划": "plan planing",
    "执行": "execute run",
    "运行": "run execute",
    "管理": "manage admin",
    "监控": "monitor watch",
    "搜索": "search query find",
    "查询": "query search",
    "通知": "notify alert",
    "告警": "alert notify",
    "网络": "network",
    "请求": "request",
    "响应": "response",
    "接口": "api interface",
    "API": "接口",
}


def _expand_synonyms(text):
    """展开同义词：将中文词替换为中文+英文同义词变体"""
    lower_text = text.lower()
    expanded = set()
    expanded.add(lower_text)
    for word, synonyms in _SYNONYM_MAP.items():
        if word.lower() in lower_text:
            for syn in synonyms.split():
                if syn:
                    expanded.add(lower_text.replace(word.lower(), syn))
                    expanded.add(syn)
    return " ".join(sorted(expanded))


def _ngram_match_score(intent_words, search_text):
    """中文 bi-gram 字符重叠 + 同义词展开的双重匹配分数"""
    expanded_intent = _expand_synonyms(" ".join(intent_words))
    expanded_search = _expand_synonyms(search_text)
    word_matches = sum(1 for w in intent_words if w in search_text)
    word_score = word_matches / max(len(intent_words), 1)
    syn_intent_words = expanded_intent.split()
    syn_matches = sum(1 for w in syn_intent_words if w in expanded_search)
    syn_score = syn_matches / max(len(syn_intent_words), 1)
    intent_chars = set("".join(intent_words))
    search_chars = set(search_text.replace(" ", ""))
    if intent_chars and search_chars:
        ngram_overlap = len(intent_chars & search_chars) / len(intent_chars | search_chars)
    else:
        ngram_overlap = 0.0
    final_score = word_score * 0.40 + syn_score * 0.40 + ngram_overlap * 0.20
    return min(final_score, 1.0)

# ============================================================
# 核心函数
# ============================================================

def _md5_of_file(path):
    """计算文件 MD5（用于增量扫描）"""
    if not path.exists():
        return ""
    data = path.read_bytes()
    return hashlib.md5(data).hexdigest()


def _build_blueprint(skill_dir):
    """为单个技能构建步骤蓝图 JSON"""
    skill_path = Path(skill_dir)
    skill_name = skill_path.name

    # 读取元信息
    meta = {}
    meta_file = skill_path / "_meta.json"
    if meta_file.exists():
        with open(meta_file, "r", encoding="utf-8") as f:
            meta = json.load(f)

    md5 = _md5_of_file(skill_path / "SKILL.md")

    # 提取步骤语义
    steps = extract_step_semantics(skill_path)

    # 第一步骤总数（含 fallback）
    total_steps = len(steps)
    usable_steps = len([s for s in steps if not s.get("_fallback")])

    blueprint = {
        "skill_name": skill_name,
        "version": meta.get("version", ""),
        "description": extract_description(read_skill_md(skill_path) or ""),
        "triggers": extract_trigger_keywords(read_skill_md(skill_path) or ""),
        "skill_md5": md5,
        "scanned_at": datetime.now().isoformat(),
        "total_steps": total_steps,
        "usable_steps": usable_steps,
        "steps": steps,
    }
    return blueprint


def cmd_scan(args):
    """扫描全部/指定技能，生成步骤蓝图索引"""
    skills_dir = get_skills_dir()
    if not skills_dir.exists():
        print(f"❌ 技能目录不存在: {skills_dir}")
        return 1

    # 加载元索引
    meta = _load_meta_index()
    if not meta:
        meta = {
            "version": "1.29.0",
            "built_at": "",
            "total_skills": 0,
            "total_steps": 0,
            "skills": {}
        }

    target_skill = args.skill
    changed_count = 0
    new_count = 0
    total_skills = 0
    total_steps = 0

    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        skill_md = entry / "SKILL.md"
        if not skill_md.exists():
            continue

        total_skills += 1
        skill_name = entry.name

        # 增量扫描：检查 MD5
        if not args.force and skill_name in meta.get("skills", {}):
            cached_md5 = meta["skills"].get(skill_name, {}).get("md5", "")
            if cached_md5 == _md5_of_file(skill_md):
                # 未变化，从缓存读取步骤数
                steps = meta["skills"][skill_name].get("steps", 0)
                total_steps += steps
                continue

        # 构建蓝图
        blueprint = _build_blueprint(entry)
        if not blueprint["steps"]:
            continue

        # 保存到 step_index/
        bp_file = INDEX_DIR / f"{skill_name}.json"
        with open(bp_file, "w", encoding="utf-8") as f:
            json.dump(blueprint, f, ensure_ascii=False, indent=2)

        # 更新元索引
        steps_count = blueprint["total_steps"]
        meta["skills"][skill_name] = {
            "md5": blueprint["skill_md5"],
            "version": blueprint.get("version", ""),
            "steps": steps_count,
            "usable_steps": blueprint.get("usable_steps", 0),
            "built_at": blueprint["scanned_at"],
        }
        total_steps += steps_count

        if skill_name in meta.get("skills", {}):
            changed_count += 1
        else:
            new_count += 1

        if args.verbose:
            print(f"  {'✅' if changed_count else '🆕'} {skill_name}: {steps_count} 步")

    # 保存元索引
    meta["version"] = "1.29.0"
    meta["built_at"] = datetime.now().isoformat()
    meta["total_skills"] = total_skills
    meta["total_steps"] = total_steps
    _save_meta_index(meta)

    print(f"✅ 步骤索引扫描完成")
    print(f"  技能总数: {total_skills}")
    print(f"  步骤总数: {total_steps}")
    if new_count:
        print(f"  新增技能: {new_count}")
    if changed_count:
        print(f"  更新技能: {changed_count}")
    if args.force:
        print(f"  模式: 全量重建")
    else:
        print(f"  模式: 增量扫描")

    return 0


def cmd_search(args):
    """在步骤蓝图中搜索匹配的步骤"""
    intent = args.intent.lower().strip()
    if not intent:
        print("❌ 请提供搜索意图")
        return 1

    intent_words = [w for w in intent.split() if len(w) > 1]
    if not intent_words:
        print("❌ 搜索词太短")
        return 1

    # 加载元索引
    meta = _load_meta_index()
    if not meta or not meta.get("skills"):
        print("❌ 步骤索引为空，请先运行 scan")
        return 1

    # 全量搜索 vs 指定技能搜索
    search_skills = args.skill.split(",") if args.skill else list(meta["skills"].keys())

    results = []
    for skill_name in search_skills:
        bp_file = INDEX_DIR / f"{skill_name}.json"
        if not bp_file.exists():
            if args.verbose:
                print(f"  ⚠️ 跳过 {skill_name}（无蓝图文件）")
            continue

        with open(bp_file, "r", encoding="utf-8") as f:
            blueprint = json.load(f)

        for step in blueprint.get("steps", []):
            step_text = (
                step.get("step_name", "") + " " +
                step.get("description", "") + " " +
                " ".join(i.get("desc", "") for i in step.get("interface", {}).get("consumes", [])) + " " +
                " ".join(i.get("desc", "") for i in step.get("interface", {}).get("produces", [])) + " " +
                step.get("usage_hint", "")
            ).lower()

            score = _ngram_match_score(intent_words, step_text)

            if score >= args.min_score:
                results.append({
                    "step_id": step.get("step_id", ""),
                    "skill_name": skill_name,
                    "step_name": step.get("step_name", ""),
                    "score": round(score, 2),
                    "consumes": [i.get("desc", "") for i in step.get("interface", {}).get("consumes", [])],
                    "produces": [i.get("desc", "") for i in step.get("interface", {}).get("produces", [])],
                    "call_address": step.get("call_address", {}),
                    "usage_hint": step.get("usage_hint", ""),
                })

    # 按分数降序排序
    results.sort(key=lambda r: r["score"], reverse=True)

    # 缺口检测（v1.29.1: 使用同义词展开）
    matched_words = set()
    for r in results:
        text = f"{r['step_name']} {' '.join(r['consumes'])} {' '.join(r['produces'])}".lower()
        text_expanded = _expand_synonyms(text)
        for w in intent_words:
            if w in text:
                matched_words.add(w)
            # 同义词匹配也算匹配到
            w_expanded = _expand_synonyms(w)
            for ew in w_expanded.split():
                if ew and ew in text_expanded:
                    matched_words.add(w)
                    break
    unmatched = [w for w in intent_words if w not in matched_words and len(w) > 1]

    if args.json:
        output = {
            "intent": intent,
            "total_results": len(results),
            "results": results,
            "gaps": unmatched,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"🔍 搜索: {intent}")
        print(f"  匹配步骤: {len(results)} 个")
        print()

        if results:
            print(f"{'':-<90}")
            print(f"{'排名':<5} {'步骤ID':<35} {'分数':<6} {'步骤名'}")
            print(f"{'':-<90}")
            for i, r in enumerate(results[:args.limit], 1):
                step_id = r["step_id"][:34]
                display_name = r["step_name"][:40]
                print(f"{i:<5} {step_id:<35} {r['score']:<6} {display_name}")

                if r["consumes"]:
                    print(f"     {'输入':>4}: {', '.join(r['consumes'][:3])}")
                if r["produces"]:
                    print(f"     {'输出':>4}: {', '.join(r['produces'][:3])}")
                if r["call_address"].get("instructions"):
                    print(f"     {'指令':>4}: {', '.join(r['call_address']['instructions'][:2])}")
                if r["usage_hint"]:
                    hint = r["usage_hint"][:60]
                    print(f"     {'提示':>4}: {hint}")
                print()

        if unmatched:
            print(f"检测到缺口（{len(unmatched)} 个）：")
            for w in unmatched:
                print(f"  - 「{w}」未被任何步骤的 interface 匹配")
        else:
            print("未检测到明显缺口")

    return 0


def cmd_info(args):
    """查看单个步骤详情"""
    step_id = args.step
    if "." not in step_id:
        print("❌ 步骤ID格式应为: skill_name.step_name")
        return 1

    skill_name = step_id.split(".")[0]
    step_rel = step_id[len(skill_name) + 1:]

    bp_file = INDEX_DIR / f"{skill_name}.json"
    if not bp_file.exists():
        print(f"❌ 技能 '{skill_name}' 的蓝图不存在，请先运行 scan")
        return 1

    with open(bp_file, "r", encoding="utf-8") as f:
        blueprint = json.load(f)

    # 查找匹配的步骤
    for step in blueprint.get("steps", []):
        if step.get("step_id") == step_id:
            _print_step_detail(step, blueprint)
            return 0

    # 模糊匹配
    for step in blueprint.get("steps", []):
        if step_rel.lower() in step.get("step_id", "").lower():
            _print_step_detail(step, blueprint)
            return 0

    print(f"❌ 步骤 '{step_id}' 未找到")
    return 1


def _print_step_detail(step, blueprint):
    """打印步骤详情"""
    print(f"📌 步骤: {step.get('step_name', '?')}")
    print(f"{'='*60}")
    print(f"  ID: {step.get('step_id', '?')}")
    print(f"  技能: {step.get('skill_name', '?')} v{blueprint.get('version', '?')}")
    print(f"  区域: {step.get('section', '?')}")
    print(f"  描述: {step.get('description', '')[:200]}")

    ca = step.get("call_address", {})
    if ca.get("instructions"):
        print(f"\n  📞 调用地址:")
        print(f"    指令: {', '.join(ca['instructions'])}")
        if ca.get("cli"):
            print(f"    CLI: {ca['cli']}")
        if ca.get("cli_alternatives"):
            for alt in ca["cli_alternatives"]:
                print(f"         {alt}")

    if step.get("usage_hint"):
        print(f"\n  💡 使用提示: {step['usage_hint'][:150]}")

    iface = step.get("interface", {})
    if iface.get("consumes"):
        print(f"\n  📥 输入:")
        for c in iface["consumes"]:
            print(f"    - [{c.get('type', '?')}] {c.get('desc', '')}")
    if iface.get("produces"):
        print(f"\n  📤 输出:")
        for p in iface["produces"]:
            print(f"    - [{p.get('type', '?')}] {p.get('desc', '')}")

    if step.get("_fallback"):
        print(f"\n  ⚠️ 该步骤为基于编号列表的 fallback 提取（非 ### 指令级提取）")


def cmd_status(args):
    """查看索引覆盖情况"""
    meta = _load_meta_index()
    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    if not meta or not meta.get("skills"):
        print("📋 步骤索引状态")
        print(f"{'='*40}")
        print("  索引为空，请先运行 scan")
        return 0

    skills = meta["skills"]
    built_at = meta.get("built_at", "?")

    print(f"📋 步骤索引状态")
    print(f"{'='*50}")
    print(f"  索引版本: v{meta.get('version', '?')}")
    print(f"  构建时间: {built_at}")
    print(f"  技能总数: {meta.get('total_skills', 0)}")
    print(f"  步骤总数: {meta.get('total_steps', 0)}")
    print(f"  有蓝图的技能: {len(skills)}")
    print()

    print(f"{'':-<70}")
    print(f"{'技能名称':<25} {'版本':<10} {'步骤':<6} {'可用':<6} {'构建时间'}")
    print(f"{'':-<70}")

    for sname in sorted(skills.keys()):
        info = skills[sname]
        ver = info.get("version", "?")[:9]
        steps = info.get("steps", 0)
        usable = info.get("usable_steps", 0)
        time_str = info.get("built_at", "?")[:16]
        print(f"{sname:<25} {ver:<10} {steps:<6} {usable:<6} {time_str}")

    print()

    # 检查 files
    bp_count = len(list(INDEX_DIR.glob("*.json"))) - 1  # 减去 _blueprint.json
    if bp_count != len(skills):
        print(f"⚠️  文件数 ({bp_count}) 与索引数 ({len(skills)}) 不一致，建议 rebuild")

    return 0


def cmd_rebuild(args):
    """全量重建索引"""
    # 清空现有索引（保留 _blueprint.json）
    for f in INDEX_DIR.glob("*.json"):
        if f.name != "_blueprint.json":
            f.unlink()

    # 清空元索引
    _save_meta_index({})

    print("🔄 全量重建索引...")
    return cmd_scan(args)


# ============================================================
# 辅助函数
# ============================================================

def _load_meta_index():
    """加载元索引"""
    if not META_INDEX.exists():
        return {}
    try:
        with open(META_INDEX, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def _save_meta_index(meta):
    """保存元索引"""
    META_INDEX.parent.mkdir(parents=True, exist_ok=True)
    with open(META_INDEX, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


# ============================================================
# CLI 入口
# ============================================================

def main():
    # 修复 Windows 控制台编码问题
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(
        description="Step Indexer v1.29.0 - 步骤蓝图索引工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python step_indexer.py scan
  python step_indexer.py scan --skill "triphasic-execution"
  python step_indexer.py scan --force
  python step_indexer.py search --intent "代码审查并生成报告"
  python step_indexer.py search --intent "分析" --skill "skill-standardization"
  python step_indexer.py info --step "skill-standardization.R-01"
  python step_indexer.py status
  python step_indexer.py rebuild
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # scan
    p_scan = subparsers.add_parser("scan", help="扫描技能生成步骤蓝图")
    p_scan.add_argument("--skill", default="", help="指定技能名称（可选，不指定则扫全部）")
    p_scan.add_argument("--force", action="store_true", help="强制全量扫描（跳过增量缓存）")
    p_scan.add_argument("--verbose", "-v", action="store_true", help="详细输出")

    # search
    p_search = subparsers.add_parser("search", help="在步骤蓝图中搜索")
    p_search.add_argument("--intent", required=True, help="搜索意图（自然语言）")
    p_search.add_argument("--skill", default="", help="限定技能名称（逗号分隔多个）")
    p_search.add_argument("--min-score", type=float, default=0.1, help="最低匹配分数（默认0.1）")
    p_search.add_argument("--json", action="store_true", help="JSON 格式输出")
    p_search.add_argument("--limit", type=int, default=20, help="最大结果数（默认20）")

    # info
    p_info = subparsers.add_parser("info", help="查看步骤详情")
    p_info.add_argument("--step", required=True, help="步骤ID（如 skill-standardization.R-01）")

    # status
    subparsers.add_parser("status", help="查看索引覆盖情况")

    # rebuild
    subparsers.add_parser("rebuild", help="全量重建步骤索引")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    commands = {
        "scan": cmd_scan,
        "search": cmd_search,
        "info": cmd_info,
        "status": cmd_status,
        "rebuild": cmd_rebuild,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        return cmd_func(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
