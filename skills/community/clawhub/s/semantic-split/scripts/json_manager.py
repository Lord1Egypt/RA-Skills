#!/usr/bin/env python3
"""
semantic-split JSON Manager v1.0

统一管理能力级/规则级 json 的 CLI 工具。
零外部依赖，仅使用 Python 标准库。
产出物遵循铁律4：数据统一存放于 ~/standardization/semantic-split/data/。

用法:
  python json_manager.py <subcommand> [options]

Subcommands:
  scan       扫描 json 库，按关键词匹配返回结果
  categorize 归类统计所有能力级 json，判断是否达到规则级阈值
  generalize 将具体内容通用化为占位符（字段替换）
  rule-gen   根据多个同类能力级 json 生成规则级 json 框架
  list       列出所有 json 文件（支持过滤）
  create     创建新的能力级/规则级 json 文件
  validate   验证 json 文件格式正确性
  info       显示 json 文件详情
"""

import json
import os
import sys
import argparse
from pathlib import Path
from collections import Counter
from datetime import datetime, date
from copy import deepcopy

# ============================================================
# 路径常量（铁律4：产出物存至 skills/.standardization/semantic-split/data/）
# ============================================================

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR.parent / ".standardization" / "semantic-split" / "data"
CAP_DIR = DATA_DIR / "capabilities"
RULE_DIR = DATA_DIR / "rules"

# ============================================================
# 工具函数
# ============================================================


def _load_json(filepath: Path) -> dict:
    """加载 json 文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(filepath: Path, data: dict, indent: int = 2):
    """保存 json 文件"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)


def _iter_capabilities() -> list[tuple[Path, dict]]:
    """遍历所有能力级 json"""
    results = []
    if CAP_DIR.exists():
        for f in sorted(CAP_DIR.glob("*.json")):
            try:
                results.append((f, _load_json(f)))
            except (json.JSONDecodeError, Exception) as e:
                print(f"[WARN] 跳过损坏文件: {f.name} ({e})", file=sys.stderr)
    return results


def _iter_rules() -> list[tuple[Path, dict]]:
    """遍历所有规则级 json"""
    results = []
    if RULE_DIR.exists():
        for f in sorted(RULE_DIR.glob("*.json")):
            try:
                results.append((f, _load_json(f)))
            except (json.JSONDecodeError, Exception) as e:
                print(f"[WARN] 跳过损坏文件: {f.name} ({e})", file=sys.stderr)
    return results


def _match_score(keywords: list[str], json_data: dict) -> float:
    """
    计算关键词与 json 的匹配分数 (0.0 ~ 1.0)

    匹配维度：
    - tags 完全匹配：每个命中的 tag +0.15
    - name 包含关键词：每个命中 +0.2
    - description 包含关键词：每个命中 +0.1
    - steps.name/action 包含关键词：每个命中 +0.05
    """
    if not keywords:
        return 0.0

    score = 0.0
    kw_lower = [k.lower() for k in keywords]

    # tags 匹配
    tags = [t.lower() for t in json_data.get("tags", [])]
    for kw in kw_lower:
        for tag in tags:
            if kw in tag or tag in kw:
                score += 0.15
                break

    # name 匹配
    name = json_data.get("name", "").lower()
    for kw in kw_lower:
        if kw in name:
            score += 0.2

    # description 匹配
    desc = json_data.get("description", "").lower()
    for kw in kw_lower:
        if kw in desc:
            score += 0.1

    # steps 匹配
    for step in json_data.get("steps", []):
        step_text = f"{step.get('name', '')} {step.get('action', '')}".lower()
        for kw in kw_lower:
            if kw in step_text:
                score += 0.05
                break  # 每个步骤最多匹配一次

    return min(score, 1.0)


# ============================================================
# Subcommand: scan
# ============================================================


def cmd_scan(args):
    """
    扫描 json 库，按关键词匹配返回结果。

    搜索顺序：规则级 → 能力级（与决策树一致）
    """
    keywords = args.keywords
    threshold = args.threshold
    top_n = args.top
    json_type = args.type  # "all", "rule", "capability"

    if not keywords:
        print("[ERROR] 请提供至少一个关键词: --keywords kw1 kw2 ...")
        sys.exit(1)

    results = []

    # 扫描规则级
    if json_type in ("all", "rule"):
        for path, data in _iter_rules():
            s = _match_score(keywords, data)
            if s >= threshold:
                results.append((s, "rule", path, data))

    # 扫描能力级
    if json_type in ("all", "capability"):
        for path, data in _iter_capabilities():
            s = _match_score(keywords, data)
            if s >= threshold:
                results.append((s, "capability", path, data))

    # 按分数排序
    results.sort(key=lambda x: x[0], reverse=True)

    # 取 top N
    results = results[:top_n] if top_n > 0 else results

    # 输出
    if not results:
        print(json.dumps({
            "matched": False,
            "message": "未找到匹配的 json",
            "keywords": keywords,
            "threshold": threshold
        }, ensure_ascii=False, indent=2))
        return

    output = {
        "matched": True,
        "keywords": keywords,
        "total": len(results),
        "results": []
    }

    for score, jtype, path, data in results:
        entry = {
            "score": round(score, 3),
            "type": jtype,
            "id": data.get("id", path.stem),
            "name": data.get("name", ""),
            "file": str(path.relative_to(SKILL_DIR)),
            "steps_count": len(data.get("steps", [])) if jtype == "capability" else len(data.get("condensed_steps", []))
        }
        if jtype == "capability":
            entry["tags"] = data.get("tags", [])
            entry["generic_params"] = data.get("generic_params", [])
        elif jtype == "rule":
            entry["tags"] = data.get("tags", [])
            entry["capability_refs"] = [r.get("id", "") for r in data.get("capability_refs", [])]
        output["results"].append(entry)

    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============================================================
# Subcommand: categorize
# ============================================================


def cmd_categorize(args):
    """
    归类统计所有能力级 json，按 tags 分组。
    判断哪些分组已达到规则级凝练阈值（≥5份）。
    """
    threshold = args.threshold

    # 收集所有能力级 json 的 tags
    tag_items = {}  # tag -> [(path, data), ...]
    all_caps = _iter_capabilities()

    for path, data in all_caps:
        for tag in data.get("tags", []):
            if tag not in tag_items:
                tag_items[tag] = []
            tag_items[tag].append((path, data))

    # 输出
    output = {
        "total_capabilities": len(all_caps),
        "threshold": threshold,
        "categories": {},
        "ready_for_rule": []
    }

    for tag in sorted(tag_items.keys()):
        items = tag_items[tag]
        ids = [d.get("id", p.stem) for p, d in items]
        count = len(items)
        ready = count >= threshold

        cat_entry = {
            "tag": tag,
            "count": count,
            "ready_for_rule": ready,
            "capability_ids": ids
        }
        output["categories"][tag] = cat_entry

        if ready:
            output["ready_for_rule"].append({
                "tag": tag,
                "count": count,
                "capability_ids": ids
            })

    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============================================================
# Subcommand: generalize
# ============================================================


def cmd_generalize(args):
    """
    将具体内容通用化为占位符（字段替换）。

    支持两种模式：
    1. --params 模式：直接指定替换映射（推荐 AI 调用时使用）
    2. --auto 模式：自动检测中括号内容作为占位符（不替换，仅提取）

    输入：一个能力级 json 文件路径
    输出：通用化后的 json（写入新文件或 stdout）
    """
    input_file = Path(args.input)
    params = args.params  # ["钛合金马扎=[产品名称]", "明天=[截止时间]"]
    auto = args.auto
    output_file = args.output

    if not input_file.exists():
        print(f"[ERROR] 文件不存在: {input_file}", file=sys.stderr)
        sys.exit(1)

    data = _load_json(input_file)
    generic_params = list(data.get("generic_params", []))

    if params:
        # 构建替换映射
        replace_map = {}
        new_generic_params = []
        for p in params:
            if "=" not in p:
                print(f"[WARN] 忽略格式错误的参数: {p} (需要 key=value)", file=sys.stderr)
                continue
            original, placeholder = p.split("=", 1)
            replace_map[original] = placeholder
            if placeholder not in generic_params:
                new_generic_params.append(placeholder)
                generic_params.append(placeholder)

        # 执行替换（遍历所有字符串字段）
        data = _replace_in_dict(data, replace_map)

    if auto:
        # 自动模式：仅收集步骤 action 中已有的中括号占位符，不额外提取
        for step in data.get("steps", []):
            import re
            found = re.findall(r'\[([^\]]+)\]', step.get("action", ""))
            for p in found:
                placeholder = f"[{p}]"
                if placeholder not in generic_params:
                    generic_params.append(placeholder)
        data["generic_params"] = generic_params
    else:
        data["generic_params"] = generic_params

    # 更新元数据
    if auto or params:
        data["_generalized"] = True
        data["_generalized_at"] = str(date.today())

    # 输出
    if output_file:
        out_path = Path(output_file)
        _save_json(out_path, data)
        print(json.dumps({
            "status": "ok",
            "output_file": str(out_path.relative_to(SKILL_DIR)),
            "generic_params": data.get("generic_params", [])
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def _replace_in_dict(obj, replace_map: dict):
    """递归替换字典中所有字符串字段的值"""
    if isinstance(obj, str):
        for original, placeholder in replace_map.items():
            obj = obj.replace(original, placeholder)
        return obj
    elif isinstance(obj, dict):
        return {k: _replace_in_dict(v, replace_map) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_replace_in_dict(item, replace_map) for item in obj]
    return obj


def _auto_detect_params(data: dict) -> list[str]:
    """自动检测 json 中已有的占位符（中括号内容）"""
    params = []
    _extract_brackets(data, params)
    # 去重保序
    seen = set()
    result = []
    for p in params:
        if p not in seen:
            seen.add(p)
            result.append(p)
    return result


def _extract_brackets(obj, params: list):
    """递归提取所有中括号内容"""
    if isinstance(obj, str):
        import re
        found = re.findall(r'\[([^\]]+)\]', obj)
        params.extend(found)
    elif isinstance(obj, dict):
        for v in obj.values():
            _extract_brackets(v, params)
    elif isinstance(obj, list):
        for item in obj:
            _extract_brackets(item, params)


# ============================================================
# Subcommand: rule-gen
# ============================================================


def cmd_rule_gen(args):
    """
    根据多个同类能力级 json 生成规则级 json 框架。

    输入：多个能力级 json 文件路径（或 --tag 按标签自动选取）
    输出：规则级 json（打印到 stdout 或写入文件）
    """
    input_files = [Path(f) for f in args.files] if args.files else []
    tag = args.tag
    output_file = args.output

    # 获取能力级 json 列表
    caps = []
    if tag:
        for path, data in _iter_capabilities():
            if tag in data.get("tags", []):
                caps.append((path, data))
    elif input_files:
        for f in input_files:
            if not f.exists():
                print(f"[ERROR] 文件不存在: {f}", file=sys.stderr)
                sys.exit(1)
            caps.append((f, _load_json(f)))
    else:
        print("[ERROR] 请提供 --files 或 --tag", file=sys.stderr)
        sys.exit(1)

    if len(caps) < 2:
        print(f"[ERROR] 至少需要 2 个能力级 json，当前: {len(caps)}", file=sys.stderr)
        sys.exit(1)

    # 生成规则级 json
    rule = _generate_rule(caps, tag)

    # 输出
    if output_file:
        out_path = Path(output_file)
        if not out_path.suffix:
            out_path = out_path.with_suffix(".json")
        _save_json(RULE_DIR / out_path.name if not out_path.is_absolute() else out_path, rule)
        print(json.dumps({
            "status": "ok",
            "output_file": out_path.name,
            "source_count": len(caps),
            "condensed_steps_count": len(rule["condensed_steps"]),
            "capability_refs": [r["id"] for r in rule["capability_refs"]]
        }, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(rule, ensure_ascii=False, indent=2))


def _generate_rule(caps: list[tuple[Path, dict]], tag: str = None) -> dict:
    """从多个能力级 json 生成规则级 json"""
    # 收集所有步骤
    all_steps = []
    cap_refs = []
    common_tags = Counter()

    for path, data in caps:
        cap_refs.append({
            "id": data.get("id", path.stem),
            "name": data.get("name", ""),
            "steps_range": f"s1-s{len(data.get('steps', []))}"
        })
        for t in data.get("tags", []):
            common_tags[t] += 1
        for step in data.get("steps", []):
            all_steps.append({
                "capability_id": data.get("id", path.stem),
                "step": step
            })

    # 提取公共步骤模式（按 name 相似度聚合）
    condensed = _condense_steps(all_steps, cap_refs)

    # 确定规则名称
    if tag:
        rule_name = f"{tag}类任务规则"
        rule_id = f"rule_{tag}_v1"
    else:
        # 从 tags 中取出现频率最高的
        top_tag = common_tags.most_common(1)[0][0] if common_tags else "general"
        rule_name = f"{top_tag}类任务规则"
        rule_id = f"rule_{top_tag}_v1"

    # 确定最佳 load_capability 映射
    for cs in condensed:
        if not cs.get("load_capability_if_detail_needed"):
            # 默认映射到第一个包含该步骤的能力级
            for ref in cap_refs:
                cs["load_capability_if_detail_needed"] = ref["id"]
                break

    rule = {
        "id": rule_id,
        "type": "rule",
        "name": rule_name,
        "version": "1.0.0",
        "created_at": str(date.today()),
        "description": f"统合 {len(caps)} 个能力级 json 提炼生成的规则",
        "source_capability_count": len(caps),
        "capability_refs": cap_refs,
        "condensed_steps": condensed,
        "tags": [t for t, c in common_tags.most_common(3) if c >= len(caps) // 2]
    }

    return rule


def _condense_steps(all_steps: list[dict], cap_refs: list[dict]) -> list[dict]:
    """
    将多个能力级的步骤压缩为规则级 condensed_steps。

    策略：
    1. 按 step.name 聚类（相似度匹配）
    2. 每个聚类生成一个 condensed_step
    3. 保留 maps_to 映射
    """
    groups = []
    used = set()

    for i, entry_i in enumerate(all_steps):
        if i in used:
            continue

        step_i = entry_i["step"]
        group = [entry_i]
        used.add(i)

        for j, entry_j in enumerate(all_steps):
            if j in used:
                continue

            step_j = entry_j["step"]
            if _steps_similar(step_i, step_j):
                group.append(entry_j)
                used.add(j)

        groups.append(group)

    # 生成 condensed_steps
    condensed = []
    for idx, group in enumerate(groups, 1):
        representative = group[0]["step"]
        maps_to = [f"{e['capability_id']}.{e['step']['id']}" for e in group]

        # 并行组：如果组内任何步骤有并行组，保留
        pg = None
        for e in group:
            if e["step"].get("parallel_group"):
                pg = f"r{idx}"
                break

        # milestone：如果组内所有步骤都是 milestone
        ms = all(e["step"].get("milestone", False) for e in group)

        cs = {
            "id": f"r{idx}",
            "name": representative.get("name", f"步骤{idx}"),
            "milestone": ms,
            "parallel_group": pg,
            "maps_to": maps_to,
            "load_capability_if_detail_needed": group[0]["capability_id"]
        }
        condensed.append(cs)

    return condensed


def _steps_similar(step_a: dict, step_b: dict) -> bool:
    """判断两个步骤是否相似（用于聚类）"""
    name_a = step_a.get("name", "").lower()
    name_b = step_b.get("name", "").lower()

    # 完全相同
    if name_a == name_b:
        return True

    # 包含关系
    if name_a in name_b or name_b in name_a:
        return True

    # 核心词重叠（去停用词后）
    stopwords = {"的", "与", "和", "及", "或", "等", "进行", "完成", "执行"}
    words_a = set(name_a) - stopwords
    words_b = set(name_b) - stopwords

    if not words_a or not words_b:
        return False

    overlap = len(words_a & words_b) / max(len(words_a), len(words_b))
    return overlap >= 0.6


# ============================================================
# Subcommand: list
# ============================================================


def cmd_list(args):
    """列出所有 json 文件"""
    json_type = args.type
    verbose = args.verbose
    tag_filter = args.tag

    results = []

    if json_type in ("all", "rule"):
        for path, data in _iter_rules():
            if tag_filter and tag_filter not in data.get("tags", []):
                continue
            entry = {
                "type": "rule",
                "id": data.get("id", path.stem),
                "name": data.get("name", ""),
                "version": data.get("version", "?"),
                "file": path.name,
                "tags": data.get("tags", [])
            }
            if verbose:
                entry["capability_refs"] = [r.get("id", "") for r in data.get("capability_refs", [])]
                entry["condensed_steps_count"] = len(data.get("condensed_steps", []))
            results.append(entry)

    if json_type in ("all", "capability"):
        for path, data in _iter_capabilities():
            if tag_filter and tag_filter not in data.get("tags", []):
                continue
            entry = {
                "type": "capability",
                "id": data.get("id", path.stem),
                "name": data.get("name", ""),
                "version": data.get("version", "?"),
                "file": path.name,
                "tags": data.get("tags", [])
            }
            if verbose:
                entry["steps_count"] = len(data.get("steps", []))
                entry["generic_params"] = data.get("generic_params", [])
                entry["milestones"] = [s["id"] for s in data.get("steps", []) if s.get("milestone")]
            results.append(entry)

    output = {
        "total": len(results),
        "filter": {"type": json_type, "tag": tag_filter},
        "items": results
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============================================================
# Subcommand: create
# ============================================================


def cmd_create(args):
    """创建新的能力级/规则级 json 骨架文件"""
    json_type = args.type
    name = args.name
    output = args.output

    if not name:
        print("[ERROR] 请提供 --name", file=sys.stderr)
        sys.exit(1)

    if json_type == "capability":
        data = {
            "id": name,
            "type": "capability",
            "name": name,
            "version": "1.0.0",
            "created_at": str(date.today()),
            "description": "",
            "generic_params": [],
            "steps": [],
            "tags": []
        }
        default_dir = CAP_DIR
        default_file = f"{name}.json"
    elif json_type == "rule":
        data = {
            "id": name,
            "type": "rule",
            "name": name,
            "version": "1.0.0",
            "created_at": str(date.today()),
            "description": "",
            "source_capability_count": 0,
            "capability_refs": [],
            "condensed_steps": [],
            "tags": []
        }
        default_dir = RULE_DIR
        default_file = f"{name}.json"
    else:
        print(f"[ERROR] 未知类型: {json_type}，请使用 capability 或 rule", file=sys.stderr)
        sys.exit(1)

    out_path = Path(output) if output else default_dir / default_file
    _save_json(out_path, data)

    print(json.dumps({
        "status": "ok",
        "type": json_type,
        "file": str(out_path.relative_to(SKILL_DIR)),
        "message": f"骨架文件已创建，请编辑填充内容"
    }, ensure_ascii=False, indent=2))


# ============================================================
# Subcommand: validate
# ============================================================


def cmd_validate(args):
    """验证 json 文件格式正确性"""
    filepath = Path(args.file)

    if not filepath.exists():
        print(f"[ERROR] 文件不存在: {filepath}", file=sys.stderr)
        sys.exit(1)

    errors = []
    warnings = []

    try:
        data = _load_json(filepath)
    except json.JSONDecodeError as e:
        print(json.dumps({
            "valid": False,
            "file": filepath.name,
            "errors": [f"JSON 解析失败: {e}"]
        }, ensure_ascii=False, indent=2))
        return

    json_type = data.get("type", "unknown")

    # 通用必填字段
    required_common = ["id", "type", "name", "version", "created_at", "description", "tags"]
    for field in required_common:
        if field not in data:
            errors.append(f"缺少必填字段: {field}")

    if json_type == "capability":
        cap_required = ["generic_params", "steps"]
        for field in cap_required:
            if field not in data:
                errors.append(f"缺少能力级必填字段: {field}")

        # 验证步骤
        if "steps" in data:
            step_required = ["id", "name", "action", "parallel_group", "milestone", "dependency_heat", "depends_on"]
            for i, step in enumerate(data["steps"]):
                for sf in step_required:
                    if sf not in step:
                        errors.append(f"步骤 {i} ({step.get('id', '?')}) 缺少字段: {sf}")

                # 验证 depends_on 引用
                all_step_ids = {s.get("id") for s in data["steps"]}
                for dep in step.get("depends_on", []):
                    if dep not in all_step_ids:
                        errors.append(f"步骤 {step.get('id')} 的 depends_on 引用不存在: {dep}")

                # 验证 dependency_heat 范围
                dh = step.get("dependency_heat", -1)
                if not isinstance(dh, (int, float)) or dh < 0 or dh > 10:
                    warnings.append(f"步骤 {step.get('id')} dependency_heat={dh} 不在 0-10 范围内")

            # 验证 parallel_group 引用一致性
            pg_members = {}
            for step in data["steps"]:
                pg = step.get("parallel_group")
                if pg:
                    if pg not in pg_members:
                        pg_members[pg] = []
                    pg_members[pg].append(step.get("id"))

            for pg, members in pg_members.items():
                if len(members) < 2:
                    warnings.append(f"并行组 '{pg}' 仅含 {len(members)} 个步骤（至少需要2个）")

    elif json_type == "rule":
        rule_required = ["source_capability_count", "capability_refs", "condensed_steps"]
        for field in rule_required:
            if field not in data:
                errors.append(f"缺少规则级必填字段: {field}")

        # 验证 condensed_steps
        if "condensed_steps" in data:
            cs_required = ["id", "name", "milestone", "parallel_group", "maps_to", "load_capability_if_detail_needed"]
            for i, cs in enumerate(data["condensed_steps"]):
                for sf in cs_required:
                    if sf not in cs:
                        errors.append(f"condensed_step {i} ({cs.get('id', '?')}) 缺少字段: {sf}")

    else:
        warnings.append(f"未知类型: {json_type}，应为 'capability' 或 'rule'")

    # 检查 generic_params 是否在内容中被引用
    if json_type == "capability" and "generic_params" in data and "steps" in data:
        content_str = json.dumps(data["steps"], ensure_ascii=False)
        for param in data["generic_params"]:
            if param not in content_str:
                warnings.append(f"generic_params 中的 '{param}' 未在步骤内容中被引用")

    output = {
        "valid": len(errors) == 0,
        "file": filepath.name,
        "type": json_type,
        "errors": errors,
        "warnings": warnings,
        "summary": {
            "steps": len(data.get("steps", data.get("condensed_steps", []))),
            "tags": len(data.get("tags", [])),
            "errors_count": len(errors),
            "warnings_count": len(warnings)
        }
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))


# ============================================================
# Subcommand: info
# ============================================================


def cmd_info(args):
    """显示 json 文件详情"""
    filepath = Path(args.file)

    if not filepath.exists():
        print(f"[ERROR] 文件不存在: {filepath}", file=sys.stderr)
        sys.exit(1)

    data = _load_json(filepath)
    data["_file"] = str(filepath.relative_to(SKILL_DIR))
    data["_file_size"] = filepath.stat().st_size

    print(json.dumps(data, ensure_ascii=False, indent=2))


# ============================================================
# CLI 入口
# ============================================================


def main():
    parser = argparse.ArgumentParser(
        prog="json_manager",
        description="semantic-split JSON 管理工具 v1.0"
    )
    subparsers = parser.add_subparsers(dest="command", help="可用子命令")

    # --- scan ---
    p_scan = subparsers.add_parser("scan", help="扫描 json 库，按关键词匹配")
    p_scan.add_argument("--keywords", nargs="+", required=True, help="搜索关键词")
    p_scan.add_argument("--threshold", type=float, default=0.1, help="最低匹配分数 (默认 0.1)")
    p_scan.add_argument("--top", type=int, default=5, help="返回前 N 个结果 (0=全部, 默认 5)")
    p_scan.add_argument("--type", choices=["all", "rule", "capability"], default="all", help="搜索范围")

    # --- categorize ---
    p_cat = subparsers.add_parser("categorize", help="归类统计能力级 json")
    p_cat.add_argument("--threshold", type=int, default=5, help="规则级凝练阈值 (默认 5)")

    # --- generalize ---
    p_gen = subparsers.add_parser("generalize", help="通用化（字段替换为占位符）")
    p_gen.add_argument("--input", required=True, help="输入的 json 文件路径")
    p_gen.add_argument("--params", nargs="*", help='替换映射: "原文=占位符" ...')
    p_gen.add_argument("--auto", action="store_true", help="自动检测占位符（仅提取，不替换）")
    p_gen.add_argument("--output", help="输出文件路径（不指定则输出到 stdout）")

    # --- rule-gen ---
    p_rule = subparsers.add_parser("rule-gen", help="生成规则级 json 框架")
    p_rule.add_argument("--files", nargs="*", help="输入的能力级 json 文件路径")
    p_rule.add_argument("--tag", help="按标签自动选取能力级 json")
    p_rule.add_argument("--output", help="输出文件路径（不指定则输出到 stdout）")

    # --- list ---
    p_list = subparsers.add_parser("list", help="列出所有 json 文件")
    p_list.add_argument("--type", choices=["all", "rule", "capability"], default="all", help="文件类型")
    p_list.add_argument("--tag", help="按标签过滤")
    p_list.add_argument("--verbose", "-v", action="store_true", help="显示详细信息")

    # --- create ---
    p_create = subparsers.add_parser("create", help="创建新 json 骨架文件")
    p_create.add_argument("--type", choices=["capability", "rule"], required=True, help="json 类型")
    p_create.add_argument("--name", required=True, help="json id / 名称")
    p_create.add_argument("--output", help="输出路径（不指定则使用默认目录）")

    # --- validate ---
    p_val = subparsers.add_parser("validate", help="验证 json 文件格式")
    p_val.add_argument("--file", required=True, help="要验证的 json 文件路径")

    # --- info ---
    p_info = subparsers.add_parser("info", help="显示 json 文件详情")
    p_info.add_argument("--file", required=True, help="json 文件路径")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 路由到对应子命令
    cmd_map = {
        "scan": cmd_scan,
        "categorize": cmd_categorize,
        "generalize": cmd_generalize,
        "rule-gen": cmd_rule_gen,
        "list": cmd_list,
        "create": cmd_create,
        "validate": cmd_validate,
        "info": cmd_info,
    }

    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
