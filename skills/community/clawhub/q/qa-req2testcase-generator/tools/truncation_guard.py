#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
truncation_guard.py — 四级截断检测 + auto-mv + gate pass 生成 + revision管理
用法: python3 truncation_guard.py --file <tmp_file> --step <P0-P7> --data-dir <dir> [--auto-mv] [--dry-run] [--task-id ID] [--revision N] [--bump-revision]
退出码: 0=PASS, 1=L1失败, 2=L2失败, 3=L3失败, 4=L4失败
"""
import argparse, json, os, sys, shutil, hashlib, hmac as _hmac_mod
from datetime import datetime, timezone, timedelta

# ── L3 必检字段定义 ──────────────────────────────────────────────
L3_SCHEMA = {
    "P0": {"top_keys": ["quality_score", "blocks", "objective"], "array_key": None, "item_keys": []},
    "P1": {"top_keys": ["feature_tree", "coverage_check"], "array_key": None, "item_keys": []},  # Bugfix V4.6.8: feature_tree是array，modules不是顶层key
    "P2": {"top_keys": [], "array_key": "test_points", "item_keys": ["id", "description"]},
    "P3": {"top_keys": [], "array_key": "risk_points", "item_keys": ["id", "description"]},
    "P4": {"top_keys": [], "array_key": "pci_list", "item_keys": ["id", "description"]},
    "P5": {"top_keys": ["merge_log", "coverage_summary"], "array_key": "test_points", "item_keys": ["id", "source", "priority", "status"]},
    "P6": {"top_keys": [], "array_key": "testcases", "item_keys": [
        "project", "case_type", "case_id", "requirement", "priority", "title",
        "menu_path", "preconditions", "steps", "expected_results", "is_smoke",
        "creator", "assignee", "test_case_type", "test_category", "status",
        "screenshot", "test_suite", "remarks"
    ]},
    "P7": {"top_keys": ["gate_result"], "array_key": None, "item_keys": []},
}

# 下游映射：bump-revision时需要清除的gate pass
DOWNSTREAM_MAP = {
    "P0": ["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7"],
    "P1": ["P1", "P2", "P3", "P4", "P5", "P6", "P7"],
    "P2": ["P2", "P3", "P4", "P5", "P6", "P7"],
    "P3": ["P3", "P5", "P6", "P7"],
    "P4": ["P4", "P5", "P6", "P7"],
    "P5": ["P5", "P6", "P7"],
    "P6": ["P6", "P7"],
    "P7": ["P7"],
}

# 全局变量：auto-mv模式下失败时需要清理tmp文件
_auto_mv_enabled = False
_current_tmp_file = None

def fail(level, code, msg):
    """输出失败信息并退出。auto-mv模式下，失败时自动删除tmp文件"""
    if _auto_mv_enabled and _current_tmp_file and os.path.exists(_current_tmp_file):
        try:
            os.remove(_current_tmp_file)
        except Exception:
            pass
    print(f"TRUNCATION_DETECTED:L{level}:{msg}")
    sys.exit(code)

# ── L1: 文件存在性 ───────────────────────────────────────────────
def check_l1(filepath):
    if not os.path.exists(filepath):
        fail(1, 1, f"文件不存在 file missing: {filepath}")
    if os.path.getsize(filepath) == 0:
        fail(1, 1, f"文件为空 file empty: {filepath}")

# ── L2: JSON 有效性 ──────────────────────────────────────────────
def check_l2(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError as e:
        fail(2, 2, f"JSON解析失败 invalid JSON: {e}")
    except Exception as e:
        fail(2, 2, f"文件读取失败 read error: {e}")

# ── L3: 结构完整性 ───────────────────────────────────────────────
def check_l3(data, step):
    schema = L3_SCHEMA.get(step)
    if not schema:
        return  # 未定义schema的step跳过L3

    # 检查顶层必需字段
    for key in schema["top_keys"]:
        if key not in data:
            fail(3, 3, f"{step} 缺少顶层字段 missing top key: {key}")

    # P7 特殊: gate_result 下需有 status
    if step == "P7":
        gr = data.get("gate_result")
        if isinstance(gr, dict) and "status" not in gr:
            fail(3, 3, "P7 gate_result 缺少 status 字段")
        elif isinstance(gr, str):
            pass  # gate_result 直接是字符串也合法
        elif gr is None:
            # 兼容: 顶层有 status 也可
            if "status" not in data:
                fail(3, 3, "P7 缺少 gate_result/status")

    # 检查数组字段
    arr_key = schema["array_key"]
    if arr_key:
        arr = data.get(arr_key)
        if not isinstance(arr, list) or len(arr) == 0:
            fail(3, 3, f"{step} 数组为空或缺失 array empty/missing: {arr_key}")
        # 检查数组项必需字段
        item_keys = schema["item_keys"]
        if item_keys:
            for idx, item in enumerate(arr):
                # V4.6.12改进：同时检查fields嵌套和顶层字段，优先选择字段更完整的那一个
                nested_fields = item.get("fields") if isinstance(item, dict) else None
                top_fields = {k: v for k, v in item.items()} if isinstance(item, dict) else {}

                # 计算各自匹配了多少必需字段
                nested_count = len([k for k in item_keys if isinstance(nested_fields, dict) and k in nested_fields]) if nested_fields else 0
                top_count = len([k for k in item_keys if k in top_fields])

                # 选择字段更完整的一个，同时兼容只有嵌套/只有顶层/两者都有的情况
                if isinstance(nested_fields, dict) and nested_count >= top_count:
                    obj = nested_fields
                else:
                    obj = top_fields

                missing = [k for k in item_keys if k not in obj]
                if missing:
                    fail(3, 3, f"{step} {arr_key}[{idx}] 缺少字段 missing keys: {missing}")

# ── L4: 内容完整性(数量阈值 + 组合校验) ──────────────────────────
def load_thresholds(step):
    """从 thresholds.json 读取阈值配置"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    th_path = os.path.join(script_dir, "thresholds.json")
    if not os.path.exists(th_path):
        return None
    try:
        with open(th_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        th = cfg.get("thresholds", {}).get(step, cfg.get("defaults", {}))
        if not th.get("check_enabled", False):
            return None
        return th
    except Exception:
        return None

def count_upstream(data_dir, step):
    """读取上游产物数量, 用于L4比率计算"""
    if step == "P5":
        p2_path = os.path.join(data_dir, "p2_output.json")
        if os.path.exists(p2_path):
            try:
                d = json.load(open(p2_path, "r", encoding="utf-8"))
                return len(d.get("test_points", []))
            except Exception:
                pass
        return 0
    elif step == "P6":
        p5_path = os.path.join(data_dir, "p5_output.json")
        if os.path.exists(p5_path):
            try:
                d = json.load(open(p5_path, "r", encoding="utf-8"))
                return len(d.get("test_points", []))
            except Exception:
                pass
        return 0
    return 0

def _load_upstream_data(data_dir, filename):
    """加载上游产物JSON数据"""
    path = os.path.join(data_dir, filename)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def _check_p5_l4_extra(data, data_dir, combo_cfg):
    """P5 L4组合校验：模块覆盖 + 优先级保留 + merge_log一致性"""
    warnings = []
    p2_data = _load_upstream_data(data_dir, "p2_output.json")

    # 1. 关键模块覆盖
    if combo_cfg.get("module_coverage", False) and p2_data:
        p2_tps = p2_data.get("test_points", [])
        # 提取P2中所有unique的source_scenario一级模块前缀
        p2_modules = set()
        for tp in p2_tps:
            src = tp.get("source_scenario", tp.get("source", ""))
            if src:
                prefix = src.split("/")[0].split(".")[0].split("_")[0]
                if prefix:
                    p2_modules.add(prefix)

        # 检查P5中这些模块是否都有对应测试点
        if p2_modules:
            p5_tps = data.get("test_points", [])
            p5_modules = set()
            for tp in p5_tps:
                src = tp.get("source_scenario", tp.get("source", ""))
                if src:
                    prefix = src.split("/")[0].split(".")[0].split("_")[0]
                    if prefix:
                        p5_modules.add(prefix)
            missing_modules = p2_modules - p5_modules
            if missing_modules:
                warnings.append(f"模块覆盖缺失 module_coverage_gap: {sorted(missing_modules)}")

    # 2. P0/P1优先级测试点不能全丢
    if combo_cfg.get("priority_preservation", False) and p2_data:
            p2_tps = p2_data.get("test_points", [])
            p2_high = [t for t in p2_tps if t.get("priority") in ("P0", "P1")]
            if p2_high:
                p5_tps = data.get("test_points", [])
                p5_high = [t for t in p5_tps if t.get("priority") in ("P0", "P1")]
                if len(p5_high) == 0:
                    fail(4, 4, f"P5 P0/P1优先级测试点全部丢失 priority_preservation_fail: P2有{len(p2_high)}个P0/P1, P5有0个")

    # 3. merge_log一致性
    if combo_cfg.get("merge_log_consistency", False):
        merge_log = data.get("merge_log", {})
        final_count = merge_log.get("final_count")
        actual_count = len(data.get("test_points", []))
        if final_count is not None and final_count != actual_count:
            fail(4, 4, f"P5 merge_log不一致 merge_log_mismatch: merge_log.final_count={final_count}, len(test_points)={actual_count}")

    return warnings

def _check_p6_l4_extra(data, data_dir, combo_cfg):
    """P6 L4组合校验：P0测试点100%展开"""
    warnings = []

    # 1. P0测试点100%展开
    if combo_cfg.get("p0_fully_expanded", False):
        p5_data = _load_upstream_data(data_dir, "p5_output.json")
        if p5_data:
            p5_tps = p5_data.get("test_points", [])
            # 找出P5中status=active且priority=P0的测试点ID
            p0_active_ids = set()
            for tp in p5_tps:
                if tp.get("status") == "active" and tp.get("priority") == "P0":
                    tp_id = tp.get("id", "")
                    if tp_id:
                        p0_active_ids.add(tp_id)

            if p0_active_ids:
                # 检查P6 testcases中通过source_test_point追溯
                cases = data.get("testcases", [])
                covered_tp_ids = set()
                for case in cases:
                    obj = case.get("fields", case) if isinstance(case, dict) else {}
                    src_tp = obj.get("source_test_point", "")
                    if src_tp:
                        covered_tp_ids.add(src_tp)

                uncovered = p0_active_ids - covered_tp_ids
                if uncovered:
                    warnings.append(f"P0测试点未全部展开 p0_expansion_gap: 未覆盖{len(uncovered)}个: {sorted(uncovered)[:5]}")

    return warnings

def check_l4(data, step, data_dir):
    """L4校验：数量阈值 + 组合校验，返回warnings列表"""
    th = load_thresholds(step)
    if th is None:
        return []  # L4不启用

    min_count = th.get("min_count", 5)
    input_ratio = th.get("input_ratio", 0.5)
    upstream_count = count_upstream(data_dir, step)
    warnings = []

    # 数量阈值校验（原有逻辑）
    if step == "P1":
        # V4.8.4: P1覆盖率硬控 — coverage < 50% → FAIL
        min_cov = th.get("min_operations_coverage", 0.5)
        ft = data.get("feature_tree", [])
        if isinstance(ft, list):
            total_ops = 0
            covered_ops = 0
            for mod in ft:
                scenarios = mod.get("scenarios", []) if isinstance(mod, dict) else []
                for sc in scenarios:
                    cc = sc.get("coverage_check", {})
                    if isinstance(cc, dict):
                        total_ops += cc.get("total_operations", 0)
                        covered_ops += cc.get("covered_operations", 0)
            if total_ops > 0:
                rate = covered_ops / total_ops
                if rate < min_cov:
                    fail(4, 4, f"P1 操作覆盖率不足 operations_coverage: {covered_ops}/{total_ops}={rate:.1%} < 要求{min_cov:.0%}。P1输出可能被截断，请重跑P1。")
    elif step == "P5":
        actual = len(data.get("test_points", []))
        required = max(min_count, int(upstream_count * input_ratio))
        if actual < required:
            fail(4, 4, f"P5 测试点数量不足 count insufficient: 实际{actual} < 要求{required} (上游P2={upstream_count}, ratio={input_ratio})")
    elif step == "P6":
        actual = len(data.get("testcases", []))
        required = max(min_count, int(upstream_count * input_ratio))
        if actual < required:
            fail(4, 4, f"P6 用例数量不足 count insufficient: 实际{actual} < 要求{required} (上游P5={upstream_count}, ratio={input_ratio})")

    # 组合校验（Phase 3新增）
    combo_cfg = th.get("combo_checks", {})
    if combo_cfg:
        if step == "P5":
            warnings = _check_p5_l4_extra(data, data_dir, combo_cfg)
        elif step == "P6":
            warnings = _check_p6_l4_extra(data, data_dir, combo_cfg)

    return warnings

# ── Gate Pass 生成 ────────────────────────────────────────────────
def build_summary(data, step):
    """根据step构建summary"""
    if step == "P5":
        tps = data.get("test_points", [])
        active = sum(1 for t in tps if t.get("status") != "blocked")
        blocked = len(tps) - active
        return {"test_point_count": len(tps), "active_count": active, "blocked_count": blocked}
    elif step == "P6":
        cases = data.get("testcases", [])
        stats = data.get("statistics", {})
        return {"case_count": len(cases), "degraded": stats.get("degraded", False)}
    elif step == "P0":
        return {"quality_score": data.get("quality_score")}
    elif step == "P1":
        ft = data.get("feature_tree", {})
        modules = ft if isinstance(ft, list) else data.get("modules", ft.get("modules", []) if isinstance(ft, dict) else [])  # Bugfix V4.6.9: feature_tree是list时直接作为modules
        return {"module_count": len(modules) if isinstance(modules, list) else 0}
    elif step in ("P2", "P3", "P4"):
        arr_key = L3_SCHEMA[step]["array_key"]
        arr = data.get(arr_key, [])
        return {f"{arr_key}_count": len(arr)}
    elif step == "P7":
        gr = data.get("gate_result", data.get("status", "UNKNOWN"))
        status = gr.get("status", gr) if isinstance(gr, dict) else gr
        return {"gate_status": status}
    return {}

# ── Revision 管理 ────────────────────────────────────────────────
def _read_current_revision(data_dir):
    """读取current_revision.json，不存在则返回None"""
    rev_path = os.path.join(data_dir, "current_revision.json")
    if not os.path.exists(rev_path):
        return None
    try:
        with open(rev_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def _write_current_revision(data_dir, revision):
    """写入current_revision.json"""
    rev_path = os.path.join(data_dir, "current_revision.json")
    with open(rev_path, "w", encoding="utf-8") as f:
        json.dump({"revision": revision, "updated_at": datetime.now(
            timezone(timedelta(hours=8))).strftime("%Y-%m-%dT%H:%M:%S+08:00")},
            f, ensure_ascii=False, indent=2)

def _resolve_revision(args_revision, data_dir):
    """解析最终revision值：CLI --revision优先，否则从current_revision.json读取，都没有则默认1"""
    # 检查用户是否显式传了--revision（argparse默认值为1，需要特殊处理）
    # 通过_revision_explicitly_set标志判断
    if getattr(args_revision, '_explicitly_set', False) if hasattr(args_revision, '_explicitly_set') else False:
        return args_revision
    # 尝试从文件读取
    rev_data = _read_current_revision(data_dir)
    if rev_data and isinstance(rev_data.get("revision"), int):
        return rev_data["revision"]
    return args_revision  # 回退到CLI参数（默认1）

def _bump_revision(data_dir, step):
    """bump revision: +1并清除下游gate pass"""
    rev_data = _read_current_revision(data_dir)
    if rev_data and isinstance(rev_data.get("revision"), int):
        new_rev = rev_data["revision"] + 1
    else:
        new_rev = 1
    _write_current_revision(data_dir, new_rev)

    # 清除该step及所有下游step的旧gate pass
    downstream = DOWNSTREAM_MAP.get(step, [step])
    gates_dir = os.path.join(data_dir, "gates")
    if os.path.isdir(gates_dir):
        for ds in downstream:
            gp = os.path.join(gates_dir, f"{ds}.pass.json")
            if os.path.exists(gp):
                try:
                    os.remove(gp)
                except Exception:
                    pass

    return new_rev

# ── 备份策略 ──────────────────────────────────────────────────────
def _backup_if_exists(filepath):
    """如果正式文件已存在，备份为 {filename}.prev.json"""
    if os.path.exists(filepath):
        d = os.path.dirname(filepath)
        name = os.path.basename(filepath)
        # foo.json → foo.prev.json
        if name.endswith(".json"):
            backup_name = name[:-5] + ".prev.json"
        else:
            backup_name = name + ".prev"
        backup_path = os.path.join(d, backup_name)
        try:
            shutil.copy2(filepath, backup_path)
        except Exception:
            pass  # 备份失败不阻塞主流程

def _get_sign_gate():
    """从orchestrator.py导入_sign_gate，保持HMAC密钥一致。"""
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
        from orchestrator import _sign_gate as _orch_sign_gate
        return _orch_sign_gate
    except (ImportError, AttributeError):
        # Fallback: 使用与orchestrator相同的固定密钥
        def _fallback_sign(gate_data, task_id):
            HMAC_SECRET = "xy-req2testcase-v4-hmac-2026"
            data_copy = {k: v for k, v in gate_data.items() if k != "hmac"}
            data_copy["_task_id"] = task_id
            payload = json.dumps(data_copy, sort_keys=True, ensure_ascii=False)
            key = HMAC_SECRET.encode("utf-8")
            return _hmac_mod.new(key, payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return _fallback_sign

_sign_gate = _get_sign_gate()

def write_gate_pass(step, task_id, revision, summary, data_dir):
    gates_dir = os.path.join(data_dir, "gates")
    os.makedirs(gates_dir, exist_ok=True)
    tz = timezone(timedelta(hours=8))
    gate = {
        "step": step,
        "status": "PASS",
        "task_id": task_id or "",
        "revision": revision,
        "source": "truncation_guard",
        "summary": summary,
        "validated_at": datetime.now(tz).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    }
    # V4.6.5: HMAC签名改用与orchestrator相同的密钥
    gate["hmac"] = _sign_gate(gate, task_id)
    path = os.path.join(gates_dir, f"{step}.pass.json")
    _backup_if_exists(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(gate, f, ensure_ascii=False, indent=2)
    return path


# ── auto-mv 逻辑 ─────────────────────────────────────────────────
def derive_final_path(tmp_file):
    """从 tmp 文件名推导正式文件名: pX_output.tmp.json → pX_output.json"""
    d = os.path.dirname(tmp_file)
    name = os.path.basename(tmp_file)
    final_name = name.replace(".tmp.json", ".json").replace(".tmp.", ".")
    if final_name == name:
        # 没有 .tmp 后缀, 原地不动
        return tmp_file
    return os.path.join(d, final_name)

# ── 主流程 ────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="四级截断检测工具 Truncation Guard — 校验JSON产物完整性",
        epilog="退出码: 0=PASS, 1=L1(文件缺失), 2=L2(JSON无效), 3=L3(结构不完整), 4=L4(内容不完整)"
    )
    parser.add_argument("--file", required=True, help="待校验的JSON文件路径(通常是.tmp.json)")
    parser.add_argument("--step", required=True, choices=["P0","P1","P2","P3","P4","P5","P6","P7"], help="当前步骤")
    parser.add_argument("--data-dir", required=True, help="数据目录(用于gate pass输出和上游文件读取)")
    parser.add_argument("--task-id", default="", help="任务ID")
    parser.add_argument("--revision", type=int, default=None, help="修订版本号(override, 优先级高于current_revision.json)")
    parser.add_argument("--auto-mv", action="store_true", help="校验通过后自动mv tmp→正式文件并生成gate pass")
    parser.add_argument("--dry-run", action="store_true", help="仅校验,不执行mv和gate pass写入")
    parser.add_argument("--bump-revision", action="store_true", help="校验通过后bump revision并清除下游gate pass")
    args = parser.parse_args()

    filepath = os.path.expanduser(args.file)
    data_dir = os.path.expanduser(args.data_dir)
    step = args.step

    # 解析revision：CLI --revision优先 > current_revision.json > 默认1
    if args.revision is not None:
        revision = args.revision
    else:
        rev_data = _read_current_revision(data_dir)
        if rev_data and isinstance(rev_data.get("revision"), int):
            revision = rev_data["revision"]
        else:
            revision = 1

    # 设置全局变量，供fail()在auto-mv模式下清理tmp
    global _auto_mv_enabled, _current_tmp_file
    _auto_mv_enabled = args.auto_mv and not args.dry_run
    _current_tmp_file = filepath

    # L1
    check_l1(filepath)
    # L2
    data = check_l2(filepath)
    # L3
    check_l3(data, step)
    # L4（返回warnings列表）
    warnings = check_l4(data, step, data_dir)

    # 全部通过
    summary = build_summary(data, step)
    if warnings:
        summary["warnings"] = warnings
    summary_val = next(iter(summary.values()), 0) if summary else 0

    if args.dry_run:
        if warnings:
            print(f"DRY_RUN_PASS:{step}:{summary_val}:WARNINGS:{len(warnings)}")
        else:
            print(f"DRY_RUN_PASS:{step}:{summary_val}")
        sys.exit(0)

    if args.auto_mv:
        final_path = derive_final_path(filepath)
        try:
            if final_path != filepath:
                _backup_if_exists(final_path)
                shutil.move(filepath, final_path)
        except Exception as e:
            fail(1, 1, f"mv失败 move failed: {filepath} → {final_path}: {e}")
        gp_path = write_gate_pass(step, args.task_id, revision, summary, data_dir)

        # bump-revision: 校验通过+mv+gate pass之后执行
        if args.bump_revision:
            new_rev = _bump_revision(data_dir, step)
            # bump后用新revision重写当前step的gate pass
            gp_path = write_gate_pass(step, args.task_id, new_rev, summary, data_dir)

        if warnings:
            print(f"GUARD_PASS:{step}:{summary_val}:WARNINGS:{len(warnings)}")
        else:
            print(f"GUARD_PASS:{step}:{summary_val}")
    else:
        # 不auto-mv, 仅校验
        if warnings:
            print(f"GUARD_PASS:{step}:{summary_val}:WARNINGS:{len(warnings)}")
        else:
            print(f"GUARD_PASS:{step}:{summary_val}")

    sys.exit(0)

if __name__ == "__main__":
    main()
