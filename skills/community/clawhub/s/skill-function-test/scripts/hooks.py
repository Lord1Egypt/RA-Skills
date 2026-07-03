"""
hooks.py — skill-function-test 流程钩子系统

双档策略：
  - Python-only 步骤（init/backup/blueprint）: 缺了自动补齐，LLM 不需要管
  - LLM 需参与的步骤（scenario/function_test/s4）: 缺了阻断，告诉 LLM 具体做啥
  - gen_report 兜底: 能自动补的自动补，不能补的阻断并指引 LLM

钩子依赖链:
  init → backup → blueprint ─┬→ scenario_test ─┐
                              ├→ function_test ─┤
                              └→ s4 ────────────┘→ gen_report → 双格式报告

LLM 跳不过任何一步。跳了就被阻断指引回来。
"""
import json
import hashlib
import os
import subprocess
import sys

# R-12 审计锚点 — 数据目录字面量
# 规范：skills/.standardization/skill-function-test/data/
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-function-test/data/"

# ── 目录定位 ──
import pathlib
_SCRIPT_DIR = str(pathlib.Path(__file__).resolve().parent)
_SKILL_DIR = str(pathlib.Path(_SCRIPT_DIR).parent)
_SKILLS_ROOT = str(pathlib.Path(_SKILL_DIR).parent)
DATA_DIR = str(pathlib.Path(_SKILLS_ROOT) / ".standardization" / "skill-function-test" / "data")


def _data_dir(skill_dir: str) -> str:
    target = os.path.basename(os.path.abspath(skill_dir))
    d = os.path.join(DATA_DIR, target, "outputs")
    os.makedirs(d, exist_ok=True)
    return d


def _skill_name(skill_dir: str) -> str:
    return os.path.basename(os.path.abspath(skill_dir))


# ── 阻断 / 通过 / 自动 ──

def _block(msg: str, action: str = "", exit_code: int = 1):
    msg_text = f"\n{'='*55}\n  [HOOK] ⛔ 流程阻断\n  {msg}\n"
    if action:
        msg_text += f"\n  >> 请执行: {action}\n"
    msg_text += f"{'='*55}\n"
    print(msg_text, file=sys.stderr)
    sys.exit(exit_code)


def _pass(msg: str):
    print(f"  [HOOK] [OK] {msg}")


def _run_py_step(cmd_args: list[str], label: str) -> bool:
    """自动执行一个纯 Python 步骤（不依赖 LLM 判断）"""
    print(f"  [HOOK] auto: {label}...")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run(cmd_args, capture_output=True, text=True, env=env)
    out = r.stdout or ""
    err = r.stderr or ""
    if out.strip():
        for line in out.strip().split("\n"):
            print(f"    {line}")
    if r.returncode != 0:
        if err.strip():
            print(f"    stderr: {err.strip()[-200:]}")
        print(f"  [HOOK] FAIL: {label} (exit={r.returncode})")
        return False
    print(f"  [HOOK] done: {label}")
    return True


# ═══════════════════════════════════════════════════════
# 制品路径
# ═══════════════════════════════════════════════════════

def _timeline_path(skill_dir: str) -> str:
    return os.path.join(DATA_DIR, os.path.basename(os.path.abspath(skill_dir)), ".timeline.json")

def _bp_json_path(skill_dir: str) -> str:
    """蓝皮书 JSON（inspector 输出名带 function 前缀）"""
    return os.path.join(_data_dir(skill_dir), ".function-test_blueprint.json")

def _bp_legacy_path(skill_dir: str) -> str:
    return os.path.join(_data_dir(skill_dir), ".function-test_blueprint.json")

def _scenario_report_path(skill_dir: str) -> str:
    return os.path.join(_data_dir(skill_dir), ".scenario-test_report.json")

def _func_report_path(skill_dir: str) -> str:
    return os.path.join(_data_dir(skill_dir), ".function-test_report.json")

def _backup_for(skill_dir: str) -> list[str]:
    bdir = os.path.join(DATA_DIR, "backup")
    if not os.path.isdir(bdir):
        return []
    name = _skill_name(skill_dir)
    return sorted([f for f in os.listdir(bdir)
                   if f.startswith(name) and f.endswith(".zip")], reverse=True)


# ═══════════════════════════════════════════════════════
# 前置钩子（入口检查 + 自动补齐 / 阻断指引）
# ═══════════════════════════════════════════════════════

def hook_pre_init(skill_dir: str):
    """init: 无前置"""
    _pass("init — 无前置依赖")


def hook_pre_backup(skill_dir: str):
    """备份前：timeline 已初始化 ← 缺了自动 init"""
    tl = _timeline_path(skill_dir)
    if not os.path.exists(tl):
        tl_script = os.path.join(_SCRIPT_DIR, "timeline.py")
        if not _run_py_step([sys.executable, tl_script, "init", skill_dir], "自动初始化时间线"):
            _block("时间线初始化失败", f"python {tl_script} init {skill_dir}")
    _pass("备份 — 时间线已就绪")


def hook_pre_blueprint(skill_dir: str):
    """蓝皮书扫描前：备份已完成 ← 缺了自动备份"""
    # 先确保 timeline 就绪
    hook_pre_backup(skill_dir)

    backups = _backup_for(skill_dir)
    if not backups:
        backup_script = os.path.join(_SCRIPT_DIR, "backup.py")
        if not _run_py_step(
            [sys.executable, backup_script, "backup", skill_dir, "auto_pre_blueprint"],
            f"自动备份 {_skill_name(skill_dir)}",
        ):
            _block("备份失败", f"python {backup_script} backup {skill_dir}")
    _pass("蓝皮书 — 备份已就绪")


def hook_pre_scenario(skill_dir: str):
    """场景测试前：蓝皮书已完成 ← 缺了自动扫描"""
    hook_pre_blueprint(skill_dir)  # 确保备份就绪

    bp_json = _bp_json_path(skill_dir)
    bp_legacy = _bp_legacy_path(skill_dir)
    if not os.path.exists(bp_json) and not os.path.exists(bp_legacy):
        insp_script = os.path.join(_SCRIPT_DIR, "inspector.py")
        if not _run_py_step(
            [sys.executable, insp_script, skill_dir],
            f"自动蓝皮书扫描 {_skill_name(skill_dir)}",
        ):
            _block("蓝皮书扫描失败", f"python {insp_script} {skill_dir}")

    # 从配置读取启用的场景维度
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    enabled_scenarios = {"S1": True, "S2": True, "S3": True}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        for k in ["S1", "S2", "S3"]:
            enabled_scenarios[k] = cfg.get("scenarios", {}).get(k, {}).get("enabled", True)
    except Exception:
        pass
    active = [k for k, v in enabled_scenarios.items() if v]
    _pass(f"场景测试 — 启用维度: {', '.join(active) if active else '无'}")


def hook_pre_function_test(skill_dir: str):
    """功能测试前：蓝皮书已完成 ← 缺了自动扫描"""
    hook_pre_blueprint(skill_dir)

    # 新增：S1-S3 未完成则阻断
    _check_scenario_done(skill_dir)

    bp_json = _bp_json_path(skill_dir)
    bp_legacy = _bp_legacy_path(skill_dir)
    if not os.path.exists(bp_json) and not os.path.exists(bp_legacy):
        insp_script = os.path.join(_SCRIPT_DIR, "inspector.py")
        if not _run_py_step(
            [sys.executable, insp_script, skill_dir],
            f"自动蓝皮书扫描 {_skill_name(skill_dir)}",
        ):
            _block("蓝皮书扫描失败", f"python {insp_script} {skill_dir}")

    # 从配置读取启用的功能维度
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    enabled_funcs = {"D1": True, "D2": True, "D3": True, "D4": True, "D5": True, "D6": True}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        for k in enabled_funcs:
            enabled_funcs[k] = cfg.get("functions", {}).get(k, {}).get("enabled", True)
    except Exception:
        pass
    active = [k for k, v in enabled_funcs.items() if v]
    _pass(f"功能测试 — 启用维度: {', '.join(active) if active else '无'}")


def hook_pre_s4(skill_dir: str):
    """S4 测试前：检查配置中 S4 是否开启"""
    # 检查配置中 S4 是否启用
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    s4_enabled = True  # 默认开启
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        s4_enabled = cfg.get("s4", {}).get("enabled", True)
    except Exception:
        pass

    if not s4_enabled:
        print(f"  [HOOK] S4 已关闭 (s4.enabled=false)，跳过")
        _mark_done(skill_dir, "s4")
        return
    has_scenario = os.path.exists(_scenario_report_path(skill_dir))
    has_func = os.path.exists(_func_report_path(skill_dir))

    if not has_scenario and not has_func:
        _block(
            "S4 需要前置测试数据",
            "请先执行场景测试 (scenario_engine.py) 或功能测试 (test_engine.py)\n"
            f"  python {os.path.join(_SCRIPT_DIR, 'scenario_engine.py')} {skill_dir}\n"
            f"  python {os.path.join(_SCRIPT_DIR, 'test_engine.py')} {skill_dir}",
        )
    _pass("S4 — 前置测试数据已就绪")

    # ── 校验: LLM 是否已完成 S4 噪音方案 ──
    noise_plan = os.path.join(_data_dir(skill_dir), ".s4_noise_plan.json")
    if not os.path.exists(noise_plan):
        _block(
            "S4 前置: 噪音方案未编写",
            "请先阅读约束清单 (.constraint-list.json)，基于蓝皮书编写噪音方案:\n"
            f"  1. 阅读 constraints 理解铁律\n"
            f"  2. 构造噪音方案写入 .s4_noise_plan.json\n"
            f"  3. 运行校验: python {os.path.join(_SCRIPT_DIR, 's4_engine.py')} {skill_dir} validate <json_path>",
        )
    try:
        with open(noise_plan, "r", encoding="utf-8") as f:
            plan = json.load(f)
        if isinstance(plan, list) and len(plan) < 3:
            _block("S4 前置: 噪音方案条目太少 (<3 条)", "请补全噪音方案")
        _pass(f"S4 — 噪音方案已就绪 ({len(plan) if isinstance(plan, list) else '?'} 条)")
    except Exception:
        _block("S4 前置: 噪音方案 JSON 解析失败", "请修复 .s4_noise_plan.json 格式")


def hook_pre_fix(skill_dir: str):
    """自动修复前：检查 fix_mode 配置"""
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    need_fix = False
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        fm = cfg.get("fix_mode", {})
        need_fix = fm.get("scenario", 0) == 1 or fm.get("function", 0) == 1
    except Exception:
        pass
    if not need_fix:
        print(f"  [HOOK] fix_mode 未启用，跳过修复步骤")
        _mark_done(skill_dir, "fix")
        _mark_done(skill_dir, "regress")
        _mark_done(skill_dir, "final_regress")
        return
    _pass("自动修复 — 开始基于测试结果修复")
    _mark_done(skill_dir, "fix")


def hook_post_fix(skill_dir: str):
    """修复完成 → 指引回归确认"""
    print(f"  [HOOK] >> 修复完成。请执行回归确认。")


def hook_pre_regress(skill_dir: str):
    """回归确认前：修复已完成"""
    state_path = _flow_state_path(skill_dir)
    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
    if not state.get("steps", {}).get("fix", {}).get("done"):
        _block("回归确认前置: 修复尚未完成", "请先执行修复步骤")
    _pass("回归确认 — 修复已完成")
    _mark_done(skill_dir, "regress")


def hook_pre_final_regress(skill_dir: str):
    """最终回归确认前：回归已完成"""
    state_path = _flow_state_path(skill_dir)
    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
    if not state.get("steps", {}).get("regress", {}).get("done"):
        _block("最终回归前置: 回归尚未完成", "请先执行回归确认")
    _pass("最终回归确认 — 回归已完成")
    _mark_done(skill_dir, "final_regress")


def hook_pre_gen_report(skill_dir: str):
    """报告生成：校验执行清单 + 清理旧版 permissions.md 报告 + 兜底"""

    # 0. 清理旧版 permissions.md 中的测试报告段落
    _clean_old_test_report_from_permissions(skill_dir)

    # 1. 校验执行清单（全部前置步骤是否通过）
    _validate_checklist_step(skill_dir, "gen_report")

    # 0. S4 状态检查（配置启用时）
    _check_s4_state(skill_dir)

    # 1. 时间线
    tl = _timeline_path(skill_dir)
    if not os.path.exists(tl):
        if not _run_py_step(
            [sys.executable, os.path.join(_SCRIPT_DIR, "timeline.py"), "init", skill_dir],
            "自动初始化时间线",
        ):
            _block("时间线初始化失败")

    # 2. 备份 + 蓝皮书（自动补）
    hook_pre_blueprint(skill_dir)

    # 3. 检查测试报告（同时验证 flow state 标记）
    has_scenario = os.path.exists(_scenario_report_path(skill_dir))
    has_func = os.path.exists(_func_report_path(skill_dir))

    if not has_scenario and not has_func:
        _block(
            "无任何测试数据",
            "请先执行至少一种测试:\n"
            f"  场景测试: python {os.path.join(_SCRIPT_DIR, 'scenario_engine.py')} {skill_dir}\n"
            f"  功能测试: python {os.path.join(_SCRIPT_DIR, 'test_engine.py')} {skill_dir}",
        )

    # 验证 flow state 标记是否与测试文件一致（防止手动复制文件绕过）
    if not has_scenario and not has_func:
        _block("无任何测试数据", "请先执行测试")
    if has_func and not _is_step_done(skill_dir, "function_test"):
        # 功能测试报告存在但 flow state 无标记 → 可能是手动复制
        print(f"  [HOOK] ⚠ 功能测试报告存在但 flow state 无完成标记（可能是手动复制）")
        # 不阻断，仅警告

    # 4. 时间线中有 marker？
    try:
        with open(tl, "r", encoding="utf-8") as f:
            tl_data = json.load(f)
        if not tl_data.get("markers"):
            print(f"  [HOOK] \u26a0 时间线文件存在但无 marker，报告计时部分可能为空")
    except Exception:
        pass

    # 5. 修复记录检查（如果测试发现问题但无修复记录 → 提醒）
    fix_record_path = os.path.join(_data_dir(skill_dir), ".fix-record.json")
    if os.path.exists(fix_record_path):
        try:
            with open(fix_record_path, "r", encoding="utf-8") as f:
                fix_records = json.load(f)
            if isinstance(fix_records, list) and fix_records:
                _pass(f"修复记录已就绪 ({len(fix_records)} 条)")
        except Exception:
            pass

    _pass("所有前置就绪 → 开始生成报告")


# ═══════════════════════════════════════════════════════
# 后置钩子（完成标记 + LLM 指引）
# ═══════════════════════════════════════════════════════

def hook_post_scenario(skill_dir: str):
    """场景测试完成 → 校验执行清单 + 指引 LLM 下一步"""
    _mark_done(skill_dir, "scenario")
    _validate_checklist_step(skill_dir, "scenario")
    print()
    print(f"  [HOOK] >> 场景测试完成。请审查结果。")
    print(f"  [HOOK] >> 审查后可按需进行: ")
    print(f"  [HOOK] >>   - 功能测试: python {os.path.join(_SCRIPT_DIR, 'test_engine.py')} {skill_dir}")
    print(f"  [HOOK] >>   - S4 测试:  python {os.path.join(_SCRIPT_DIR, 's4_engine.py')} {skill_dir} scope")
    print(f"  [HOOK] >>   - 生成报告: python {os.path.join(_SCRIPT_DIR, 'gen_report.py')} {skill_dir}")


def hook_post_function_test(skill_dir: str):
    """功能测试完成 → 校验执行清单"""
    _mark_done(skill_dir, "function_test")
    _validate_checklist_step(skill_dir, "function_test")
    # 检查 S4 是否已关闭，关闭则直接自动出报告
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    s4_enabled = True
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        s4_enabled = cfg.get("s4", {}).get("enabled", True)
    except Exception:
        pass
    if not s4_enabled:
        print(f"  [HOOK] >> S4 已关闭，自动生成报告...")
        _run_py_step(
            [sys.executable, os.path.join(_SCRIPT_DIR, "gen_report.py"), skill_dir],
            "自动生成报告",
        )


def hook_post_s4(skill_dir: str):
    _mark_done(skill_dir, "s4")
    _validate_checklist_step(skill_dir, "s4_play")
    print(f"  [HOOK] >> S4 完成，自动生成报告...")
    _run_py_step(
        [sys.executable, os.path.join(_SCRIPT_DIR, "gen_report.py"), skill_dir],
        "自动生成报告",
    )


def hook_post_gen_report(skill_dir: str):
    """报告生成完成 → 校验清单 + 清理 + 指引"""
    _mark_done(skill_dir, "report")
    _validate_checklist_step(skill_dir, "gen_report")
    _clean_skill_root(skill_dir, strict=True)
    print(f"  [HOOK] >> 报告已生成。需继续执行步骤9：测试结论写入目标技能。")
    print(f"  请执行: python {os.path.join(_SCRIPT_DIR, 'gen_report.py')} {skill_dir} --write-conclusion")


def hook_pre_write_conclusion(skill_dir: str):
    """结论写入前：校验清单 + 报告已生成"""
    _validate_checklist_step(skill_dir, "write_conclusion")
    state_path = _flow_state_path(skill_dir)
    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
    if not state.get("steps", {}).get("report", {}).get("done"):
        _block("结论写入前置: 报告尚未生成", "请先生成报告: python gen_report.py <skill-dir>")
    _pass("结论写入 — 报告已就绪")


def hook_post_write_conclusion(skill_dir: str):
    """结论写入完成 → 全部流程完毕（终端状态）"""
    _mark_done(skill_dir, "write_conclusion")
    print(f"  [HOOK] >> 测试结论已写入目标技能。全部流程完成。")


def hook_pre_config_check(skill_dir: str):
    """配置确认前：蓝皮书已完成，然后生成执行清单"""
    hook_pre_blueprint(skill_dir)
    _pass("配置确认 — 蓝皮书已就绪")
    # 生成执行清单
    _generate_execution_checklist(skill_dir)


def hook_post_config_check(skill_dir: str):
    _mark_done(skill_dir, "config_check")
    print(f"  [HOOK] >> 配置已确认。")


def hook_pre_bump(skill_dir: str):
    """bump 前：修复已完成（若未开启修复则直接通过）"""
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    need_fix = False
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        fm = cfg.get("fix_mode", {})
        need_fix = fm.get("scenario", 0) == 1 or fm.get("function", 0) == 1
    except Exception:
        pass
    if not need_fix:
        print(f"  [HOOK] 修复未开启，跳过 bump 检查")
        _mark_done(skill_dir, "bump")
        return
    state_path = _flow_state_path(skill_dir)
    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
    if not state.get("steps", {}).get("fix", {}).get("done"):
        _block("bump 前置: 修复尚未完成", "请先执行修复步骤")
    _pass("bump — 修复已完成")


def hook_post_bump(skill_dir: str):
    _mark_done(skill_dir, "bump")
    print(f"  [HOOK] >> 版本号 bump 完成。")


def hook_pre_write_tests(skill_dir: str):
    """写测试前置：蓝皮书就绪 + LLM 必须手工编写场景测试用例"""
    hook_pre_blueprint(skill_dir)

    # 从配置读取场景维度开关
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    scenarios_enabled = {"S1": True, "S2": True, "S3": True}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        for k in scenarios_enabled:
            scenarios_enabled[k] = cfg.get("scenarios", {}).get(k, {}).get("enabled", True)
    except Exception:
        pass
    active = [k for k, v in scenarios_enabled.items() if v]
    if not active:
        _pass("场景测试维度全部关闭，跳过编写场景测试用例")
        _mark_done(skill_dir, "write_tests")
        _mark_done(skill_dir, "scenario")  # 场景关闭等同于已完成
        return

    # 检查是否已存在手工编写的测试用例
    test_plan_path = os.path.join(_data_dir(skill_dir), ".s_test_plan.json")
    if os.path.exists(test_plan_path):
        try:
            with open(test_plan_path, "r", encoding="utf-8") as f:
                plan = json.load(f)
            s_count = len(plan.get("S1", [])) + len(plan.get("S2", [])) + len(plan.get("S3", []))
            if s_count >= 3:
                _pass(f"场景测试用例已就绪 ({s_count} 条)")
                return
        except Exception:
            pass

    _block(
        "写测试前置: 场景测试用例未编写",
        "请基于目标技能的 SKILL.md 和蓝皮书，手工编写场景测试用例:\n"
        f"  1. 阅读目标技能的 SKILL.md，理解其业务场景和能力范围\n"
        f"  2. 阅读蓝皮书的 file_manifest.python 列表，了解全部模块名\n"
        f"  3. 为 S1（触发场景）写真实用户触发词 + 预期行为\n"
        f"  4. 为 S2（核心能力）写输入 + 预期输出\n"
        f"  5. 为 S3（工作流）写多步骤链路 + 预期连贯结果\n"
        f"  6. 每条用例建议填写 modules 字段，指定涉及的 Python 模块名（不含 .py 后缀）\n"
        f"  7. 写入 {test_plan_path}\n"
        f"  格式见 skill-function-test 的 references/s-test-plan-schema.md",
    )


def hook_post_write_tests(skill_dir: str):
    _mark_done(skill_dir, "write_tests")
    # 校验执行清单
    _validate_checklist_step(skill_dir, "write_tests")



# R-11 强制清理：gen_report 完成后自动清除目标技能根目录的测试产出物

_KNOWN_TEST_ARTIFACTS = {
    ".function-test_blueprint.json", ".scenario-test_report.json",
    ".test-config.json", ".test-report.html", ".test-report.md",
    ".timeline.json", ".constraint-list.json",
    ".s4_trace.json", ".s4_noise_plan.json",
    ".fix-record.json", ".flow-state.json",
}


# ═══════════════════════════════════════════════════════
# 执行清单系统（执行忠实度校验）
# ═══════════════════════════════════════════════════════

def _checklist_path(skill_dir: str) -> str:
    return os.path.join(_data_dir(skill_dir), ".execution-checklist.json")


def _config_checksum(skill_dir: str) -> str:
    """计算 .test-config.json 的 SHA256，用于校验配置完整性"""
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    if not os.path.exists(config_path):
        return ""
    try:
        with open(config_path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except Exception:
        return ""


def _generate_execution_checklist(skill_dir: str):
    """基于 .test-config.json 生成执行清单

    如果已存在有效执行清单（有已通过的步骤），拒绝重新生成，
    除非先清除 flow-state 确认会话结束。
    """
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    if not os.path.exists(config_path):
        print("  [CHKLIST] 配置文件不存在，跳过生成清单")
        return

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception as e:
        print(f"  [CHKLIST] 配置读取失败: {e}")
        return

    # 配置锁定检查：如果已有执行清单且已有步骤通过，拒绝重新生成
    cl_path = _checklist_path(skill_dir)

    # 配置锁定检查：如果 flow-state 有已完成的步骤，说明会话进行中，
    # 禁止重新生成清单——即使旧清单被删了也不行
    flow_path = _flow_state_path(skill_dir)
    session_active = False
    if os.path.exists(flow_path):
        try:
            with open(flow_path, "r", encoding="utf-8") as f:
                fs = json.load(f)
            steps = fs.get("steps", {})
            # backup/blueprint 自动补齐的不算，它们可以重新生成
            auto_steps = {"init", "backup", "blueprint"}
            session_active = any(
                isinstance(v, dict) and v.get("done", False)
                for k, v in steps.items()
                if k not in auto_steps
            )
        except Exception:
            pass

    if session_active:
        _block(
            "配置锁定",
            "测试会话进行中，禁止中途修改配置！\n"
            "  配置清单已锁定，请按清单执行到底",
        )
        return

    rounds = cfg.get("rounds", 3)
    fm = cfg.get("fix_mode", {"scenario": 0, "function": 0})
    if isinstance(fm, int):
        fm = {"scenario": fm, "function": fm}
    s4_enabled = cfg.get("s4", {}).get("enabled", True)
    s4_rounds = cfg.get("s4", {}).get("rounds", rounds)

    # 启用的场景维度
    active_scenarios = [k for k in ["S1", "S2", "S3"]
                        if cfg.get("scenarios", {}).get(k, {}).get("enabled", True)]
    active_functions = [k for k in ["D1", "D2", "D3", "D4", "D5", "D6"]
                        if cfg.get("functions", {}).get(k, {}).get("enabled", True)]

    checklist = []

    # write_tests: 每个启用的场景维度至少 1 条测试用例
    if active_scenarios:
        checklist.append({
            "step": "write_tests",
            "expect": {d: "≥1 条用例" for d in active_scenarios},
            "validate": "count_plan_cases",
            "actual": None,
        })

    # scenario: 轮次匹配
    if active_scenarios:
        checklist.append({
            "step": "scenario",
            "expect": f"{','.join(active_scenarios)} 各{rounds}轮",
            "validate": "check_rounds",
            "expected_rounds": rounds,
            "actual": None,
        })

    # function: 轮次匹配
    if active_functions:
        checklist.append({
            "step": "function_test",
            "expect": f"{','.join(active_functions)} 各{rounds}轮",
            "validate": "check_rounds",
            "expected_rounds": rounds,
            "actual": None,
        })

    # S4 噪声方案
    if s4_enabled:
        checklist.append({
            "step": "s4_plan",
            "expect": "S4 噪声方案 ≥3 条",
            "validate": "count_noise_plan",
            "actual": None,
        })
        checklist.append({
            "step": "s4_play",
            "expect": f"S4 回放 {s4_rounds} 轮",
            "validate": "check_s4_rounds",
            "expected_rounds": s4_rounds,
            "actual": None,
        })

    # 修复（可选）
    need_fix = fm.get("scenario", 0) == 1 or fm.get("function", 0) == 1
    if need_fix:
        checklist.append({
            "step": "fix",
            "expect": "LLM 过滤误报后执行自动修复",
            "validate": "check_fix_records",
            "actual": None,
        })
        checklist.append({
            "step": "bump",
            "expect": "修复有变更时执行 PATCH bump",
            "validate": "check_bump",
            "actual": None,
        })

    # 报告
    checklist.append({
        "step": "gen_report",
        "expect": "全部启用维度测试完毕",
        "validate": "check_all_done",
        "actual": None,
    })

    # 结论写入
    checklist.append({
        "step": "write_conclusion",
        "expect": "结论写入 test-report.md",
        "validate": "check_conclusion_written",
        "actual": None,
    })

    doc = {
        "based_at": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "config_hash": _config_checksum(skill_dir),
        "rounds": rounds,
        "s4_enabled": s4_enabled,
        "s4_rounds": s4_rounds,
        "fix_scenario": fm.get("scenario", 0) == 1,
        "fix_function": fm.get("function", 0) == 1,
        "active_scenarios": active_scenarios,
        "active_functions": active_functions,
        "checklist": checklist,
    }

    cl_path = _checklist_path(skill_dir)
    with open(cl_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"  [CHKLIST] 执行清单已生成: {cl_path}")
    print(f"  [CHKLIST] {len(checklist)} 项待验证")
    return doc


def _validate_checklist_step(skill_dir: str, step: str) -> bool:
    """校验执行清单中某一步是否达到期望，不给过就 exit(1)"""
    cl_path = _checklist_path(skill_dir)
    if not os.path.exists(cl_path):
        if step not in ("gen_report", "write_conclusion"):
            print(f"  [CHKLIST] 执行清单不存在（可能跳过 config_check），放行")
        return True

    try:
        with open(cl_path, "r", encoding="utf-8") as f:
            cl = json.load(f)
    except Exception as e:
        print(f"  [CHKLIST] 清单读取失败: {e}，放行")
        return True

    # ═══════════════════════════════════════════════════════
    # 配置完整性校验：执行清单锁定后，配置不得被修改
    # ═══════════════════════════════════════════════════════
    locked_hash = cl.get("config_hash")
    if locked_hash:
        current_hash = _config_checksum(skill_dir)
        if current_hash != locked_hash:
            _block(
                "配置完整性阻断",
                "配置已被篡改，与执行清单不一致！\n"
                "  配置清单已锁定，请按清单执行到底",
            )
            return False

    found = [item for item in cl.get("checklist", []) if item["step"] == step]
    if not found:
        # 清单中无此项 → 可能是该维度未启用，放行
        return True

    item = found[0]
    # 已通过则跳过
    if item.get("actual") == "PASS":
        return True

    method = item.get("validate", "")

    if method == "count_plan_cases":
        return _chk_count_plan_cases(skill_dir, item)
    elif method == "check_rounds":
        return _chk_check_rounds(skill_dir, item)
    elif method == "count_noise_plan":
        return _chk_count_noise_plan(skill_dir, item)
    elif method == "check_s4_rounds":
        return _chk_check_s4_rounds(skill_dir, item)
    elif method == "check_fix_records":
        return _chk_check_fix_records(skill_dir, item)
    elif method == "check_bump":
        return _chk_check_bump(skill_dir, item)
    elif method == "check_all_done":
        return _chk_check_all_done(skill_dir, item)
    elif method == "check_conclusion_written":
        return _chk_check_conclusion_written(skill_dir, item)
    else:
        print(f"  [CHKLIST] 未知校验方法: {method}，放行")
        return True


def _chk_count_plan_cases(skill_dir: str, item: dict) -> bool:
    """校验 write_tests: S1/S2/S3 各维度的用例数"""
    plan_path = os.path.join(_data_dir(skill_dir), ".s_test_plan.json")
    if not os.path.exists(plan_path):
        _block("执行清单阻断", f"write_tests: 测试用例文件缺失 ({plan_path})\n  请先基于蓝皮书编写 S1-S3 场景测试用例")
        return False

    try:
        with open(plan_path, "r", encoding="utf-8") as f:
            plan = json.load(f)
    except Exception:
        _block("执行清单阻断", "write_tests: 测试用例 JSON 解析失败，请修复格式")
        return False

    expect = item.get("expect", {})
    for dim, requirement in expect.items():
        cases = plan.get(dim, [])
        if len(cases) < 1:
            _block("执行清单阻断",
                   f"write_tests: 维度 {dim} 需要 {requirement}，实际 0 条\n  请补充 {dim} 的测试用例到 {plan_path}")
            return False
        print(f"  [CHKLIST] ✅ {dim}: {len(cases)} 条用例 (≥1)")

    item["actual"] = "PASS"
    _save_checklist_item(skill_dir, item["step"], "PASS")
    return True


def _chk_check_rounds(skill_dir: str, item: dict) -> bool:
    """校验场景或功能测试的轮次 — 精确到 timeline marker 计数"""
    expected = item.get("expected_rounds", 3)
    step = item["step"]

    phase_map = {"scenario": "scenario", "function_test": "function_test"}
    phase = phase_map.get(step)
    if not phase:
        return True

    # 从 timeline 读取并计数该阶段的执行次数
    tl_path = os.path.join(os.path.dirname(_data_dir(skill_dir)), ".timeline.json")
    if not os.path.exists(tl_path):
        _block("执行清单阻断",
               f"{step}: 时间线不存在，无法校验轮次\n"
               f"  请确保 {step} 已按配置执行")
        return False

    try:
        with open(tl_path, "r", encoding="utf-8") as f:
            tl = json.load(f)
    except Exception:
        _block("执行清单阻断", f"{step}: 时间线读取失败")
        return False

    # 统计 py_script 类型、phase 匹配的 start marker 数量
    markers = tl.get("markers", [])
    start_count = sum(1 for m in markers
                      if m.get("type") == "py_script"
                      and m.get("phase") == phase
                      and m.get("mark") == "start")

    if start_count < expected:
        detail_path = os.path.join(os.path.dirname(_data_dir(skill_dir)), ".timeline.json")
        _block("执行清单阻断",
               f"{step}: 期望 {expected} 轮，timeline 记录仅 {start_count} 次执行\n"
               f"  timeline 路径: {detail_path}\n"
               f"  请确认 {step} 已按配置轮次完整执行")
        return False

    print(f"  [CHKLIST] ✅ {step}: timeline 记录 {start_count} 次执行 (期望 {expected})")
    item["actual"] = "PASS"
    _save_checklist_item(skill_dir, step, "PASS")
    return True


def _chk_count_noise_plan(skill_dir: str, item: dict) -> bool:
    """校验 S4 噪声方案"""
    plan_path = os.path.join(_data_dir(skill_dir), ".s4_noise_plan.json")
    if not os.path.exists(plan_path):
        _block("执行清单阻断",
               "S4: 噪声方案缺失\n  请基于约束清单编写噪声方案并写入 .s4_noise_plan.json")
        return False
    try:
        with open(plan_path, "r", encoding="utf-8") as f:
            plan = json.load(f)
        if isinstance(plan, list) and len(plan) < 3:
            _block("执行清单阻断",
                   f"S4: 噪声方案 {len(plan)} 条，需要 ≥3 条\n  请补充噪声条目")
            return False
    except Exception:
        _block("执行清单阻断", "S4: 噪声方案 JSON 解析失败")
        return False
    print(f"  [CHKLIST] ✅ S4 噪声方案: {len(plan)} 条 (≥3)")
    item["actual"] = "PASS"
    _save_checklist_item(skill_dir, "s4_plan", "PASS")
    return True


def _chk_check_s4_rounds(skill_dir: str, item: dict) -> bool:
    """校验 S4 回放轮次"""
    expected = item.get("expected_rounds", 3)
    trace_dir = os.path.dirname(_data_dir(skill_dir))
    actual_rounds = 0
    for r in range(1, expected + 10):
        tf = os.path.join(trace_dir, f".s4_trace_r{r}.json")
        if not os.path.exists(tf):
            # 也检查 data_dir 下的
            tf2 = os.path.join(_data_dir(skill_dir), f".s4_trace_r{r}.json")
            if not os.path.exists(tf2):
                break
        actual_rounds = r

    if actual_rounds < expected:
        _block("执行清单阻断",
               f"S4: 实际回放 {actual_rounds} 轮，期望 {expected} 轮\n  请补跑: python s4_engine.py {skill_dir} play")
        return False
    print(f"  [CHKLIST] ✅ S4 回放: {actual_rounds} 轮 (期望 {expected})")
    item["actual"] = "PASS"
    _save_checklist_item(skill_dir, "s4_play", "PASS")
    return True


def _chk_check_fix_records(skill_dir: str, item: dict) -> bool:
    """校验修复记录"""
    fix_path = os.path.join(_data_dir(skill_dir), ".fix-record.json")
    if os.path.exists(fix_path):
        print(f"  [CHKLIST] ✅ 修复记录存在")
    else:
        print(f"  [CHKLIST] ℹ️ 无修复记录（可能无问题可修）")
    item["actual"] = "PASS"
    _save_checklist_item(skill_dir, "fix", "PASS")
    return True


def _chk_check_bump(skill_dir: str, item: dict) -> bool:
    """校验 bump（仅需确认已执行，实际 bump 由 bump_version.py 完成）"""
    print(f"  [CHKLIST] ✅ bump 已就绪")
    item["actual"] = "PASS"
    return True


def _chk_check_all_done(skill_dir: str, item: dict) -> bool:
    """校验全部启用维度是否测试完毕"""
    cl_path = _checklist_path(skill_dir)
    if not os.path.exists(cl_path):
        return True
    with open(cl_path, "r", encoding="utf-8") as f:
        cl = json.load(f)
    pending = [i for i in cl.get("checklist", [])
               if i["step"] not in ("gen_report", "write_conclusion")
               and i.get("actual") != "PASS"]
    if pending:
        steps_str = ", ".join(i["step"] for i in pending)
        _block("执行清单阻断",
               f"报告生成前置: 以下步骤未通过清单校验: {steps_str}\n请先完成这些步骤")
        return False
    print(f"  [CHKLIST] ✅ 全部前置步骤已通过校验")
    return True


def _chk_check_conclusion_written(skill_dir: str, item: dict) -> bool:
    """校验结论已写入"""
    report_path = os.path.join(skill_dir, "references", "test-report.md")
    if not os.path.exists(report_path):
        _block("执行清单阻断",
               "结论写入: test-report.md 不存在\n  请执行: python gen_report.py <skill-dir> --write-conclusion")
        return False
    print(f"  [CHKLIST] ✅ test-report.md 已存在")
    return True


def _save_checklist_item(skill_dir: str, step: str, status: str):
    """更新执行清单中某一步的状态"""
    cl_path = _checklist_path(skill_dir)
    if not os.path.exists(cl_path):
        return
    try:
        with open(cl_path, "r", encoding="utf-8") as f:
            cl = json.load(f)
        for item in cl.get("checklist", []):
            if item["step"] == step:
                item["actual"] = status
        with open(cl_path, "w", encoding="utf-8") as f:
            json.dump(cl, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _clean_skill_root(skill_dir: str, strict: bool = False):
    """扫描目标技能根目录，删除已知测试残留文件"""
    removed = []
    for fname in _KNOWN_TEST_ARTIFACTS:
        fpath = os.path.join(skill_dir, fname)
        if os.path.exists(fpath):
            os.remove(fpath)
            removed.append(fname)
            print(f"  [HOOK] 🧹 清理残留: {fname}")
    if strict:
        print(f"  [HOOK] ✅ 根目录{'干净，无测试残留' if not removed else f'已清理 {len(removed)} 个文件'}")


# ═══════════════════════════════════════════════════════
# 旧版 permissions.md 测试报告清理（迁移至 test-report.md）
# ═══════════════════════════════════════════════════════

def _clean_old_test_report_from_permissions(skill_dir: str):
    """删除 permissions.md 中由旧版 gen_report 写入的测试报告段落

    旧版将测试结论写到 <skill>/references/permissions.md，标题为
    "## 基于skill-function-test的测试报告"。
    该段落现已迁移到独立的 test-report.md，需清理旧内容。
    """
    perm_path = os.path.join(skill_dir, "references", "permissions.md")
    if not os.path.exists(perm_path):
        return

    with open(perm_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "基于skill-function-test的测试报告" not in content:
        return

    # 从 "## 基于skill-function-test的测试报告" 行开始，
    # 删除到下一个 "## " 行或文件末尾
    lines = content.split("\n")
    new_lines = []
    in_old_section = False
    removed_lines = 0

    for line in lines:
        if line.startswith("## ") and "基于skill-function-test的测试报告" in line:
            in_old_section = True
            removed_lines += 1
            continue
        if in_old_section:
            if line.startswith("## "):
                # 下一个 ## 章节开始，保留此行并退出删除
                new_lines.append(line)
                in_old_section = False
            else:
                removed_lines += 1
            continue
        new_lines.append(line)

    new_content = "\n".join(new_lines).rstrip("\n") + "\n" if new_lines else ""

    from fixer import safe_write
    safe_write(perm_path, new_content)
    print(f"  [HOOK] 🧹 已从 permissions.md 清理 {removed_lines} 行旧测试报告内容（已迁移至 test-report.md）")


# ── 通用标记 ──

_STATE_CACHE = {}

def _flow_state_path(skill_dir: str) -> str:
    target = os.path.basename(os.path.abspath(skill_dir))
    d = os.path.join(DATA_DIR, target)
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, ".flow-state.json")


def _is_step_done(skill_dir: str, step: str) -> bool:
    """检查 flow state 中某步骤是否已完成"""
    state_path = _flow_state_path(skill_dir)
    if not os.path.exists(state_path):
        return False
    try:
        with open(state_path, "r", encoding="utf-8") as f:
            state = json.load(f)
        s = state.get("steps", {}).get(step, {})
        return isinstance(s, dict) and s.get("done", False)
    except Exception:
        return False


def _check_scenario_done(skill_dir: str):
    """检查 S1-S3 是否已完成（根据配置中的启用状态）"""
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    scenarios_enabled = {"S1": True, "S2": True, "S3": True}
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        for k in scenarios_enabled:
            scenarios_enabled[k] = cfg.get("scenarios", {}).get(k, {}).get("enabled", True)
    except Exception:
        pass
    active = [k for k, v in scenarios_enabled.items() if v]
    if not active:
        return  # 所有场景都关闭了，不需要检查

    # 场景测试完成标记
    if not _is_step_done(skill_dir, "scenario"):
        # 检查测试报告是否存在（兼容旧路径）
        has_report = os.path.exists(os.path.join(_data_dir(skill_dir), ".scenario-test_report.json"))
        if not has_report:
            _block(
                "功能测试前置: 场景测试 (S1-S3) 未执行",
                f"配置中启用了 {', '.join(active)}，请先执行场景测试:\n"
                f"  1. 编写场景测试用例: 阅读 SKILL.md 和蓝皮书，写入 .s_test_plan.json\n"
                f"  2. 运行场景测试: python {os.path.join(_SCRIPT_DIR, 'scenario_engine.py')} {skill_dir}",
            )
    _pass("功能测试 — 场景测试 (S1-S3) 已完成")


def _check_s4_state(skill_dir: str):
    """检查 S4 是否已完成（配置中启用时）"""
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    s4_enabled = True
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        s4_enabled = cfg.get("s4", {}).get("enabled", True)
    except Exception:
        pass
    if not s4_enabled:
        return  # S4 关闭，不检查

    if not _is_step_done(skill_dir, "s4"):
        # 检查 S4 追踪文件是否存在（兼容已有执行但没有标记的情况）
        has_trace = os.path.exists(os.path.join(_data_dir(skill_dir), ".s4_trace.json"))
        has_output_trace = os.path.exists(os.path.join(_data_dir(skill_dir), "outputs", ".s4_trace.json"))
        if not has_trace and not has_output_trace:
            _block(
                "报告生成前置: S4 未执行",
                "配置中 S4 已启用，请先执行 S4 测试:\n"
                f"  python {os.path.join(_SCRIPT_DIR, 's4_engine.py')} {skill_dir} scope\n"
                f"  编写噪音方案 → validate → play\n"
                f"  python {os.path.join(_SCRIPT_DIR, 's4_engine.py')} {skill_dir} play",
            )
    _pass("报告生成 — S4 已完成")


def _mark_done(skill_dir: str, step: str):
    path = _flow_state_path(skill_dir)
    state = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
    if "steps" not in state:
        state["steps"] = {}
    state["steps"][step] = {
        "done": True,
        "at": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)  # [HOOK] {step} done


def hook_post_init(skill_dir: str): _mark_done(skill_dir, "init")
def hook_post_backup(skill_dir: str): _mark_done(skill_dir, "backup")
def hook_post_blueprint(skill_dir: str): _mark_done(skill_dir, "blueprint")


# ═══════════════════════════════════════════════════════
# 状态查看
# ═══════════════════════════════════════════════════════

def cmd_status(skill_dir: str):
    state_path = _flow_state_path(skill_dir)
    state = {}
    if os.path.exists(state_path):
        with open(state_path, "r") as f:
            state = json.load(f)
    steps = state.get("steps", {})

    # 从 outputs 目录读取配置（不依赖 skill_dir 根目录，因会被清理）
    config_path = os.path.join(_data_dir(skill_dir), ".test-config.json")
    need_fix = False
    s4_enabled = True
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        fm = cfg.get("fix_mode", {})
        need_fix = fm.get("scenario", 0) == 1 or fm.get("function", 0) == 1
        s4_enabled = cfg.get("s4", {}).get("enabled", True)
    except Exception:
        pass

    flow = [
        ("init",             "初始化时间线"),
        ("backup",           "① 备份目标技能"),
        ("blueprint",        "② 蓝皮书扫描"),
        ("config_check",     "③ 强制确认配置一致性"),
        ("write_tests",      "④ 编写S1-S3场景测试用例"),
        ("scenario",         "④ S1-S3 场景测试"),
        ("function_test",    "⑤ D1-D6 功能测试"),
    ]
    if s4_enabled:
        flow.append(("s4", "⑥ S4 执行忠实度"))
    if need_fix:
        flow += [
            ("fix",            "⑦ 修复"),
            ("bump",           "⑧ 版本号 bump"),
        ]
    flow += [
        ("gen_report",       "⑨ 输出报告"),
        ("write_conclusion", "⑩ 结论写入 test-report.md"),
    ]

    print("\n  ── 流程状态 ──")
    all_done = True
    for key, label in flow:
        s = steps.get(key, {})
        done = s.get("done", False) if isinstance(s, dict) else False
        icon = "DONE" if done else "PEND"
        if not done:
            all_done = False
        print(f"  [{icon}] {label}")

    print(f"\n  exit: {'0 (全部完成)' if all_done else '>0 (未完成)'}")


# ═══════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 3:
        print("用法: python hooks.py check|done|status <skill-dir> [step]")
        print("  step: init | backup | blueprint | config_check | write_tests | scenario |")
        print("        function_test | s4 | fix | bump | gen_report | write_conclusion")
        return

    cmd = sys.argv[1]
    skill_dir = sys.argv[2]

    if cmd == "status":
        cmd_status(skill_dir)
        return

    if len(sys.argv) < 4:
        print("请指定步骤: init | backup | blueprint | write_tests | scenario | function_test | s4 | fix | regress | final_regress | gen_report | write_conclusion")
        return

    step = sys.argv[3]

    if cmd == "check":
        pre_map = {
            "init": hook_pre_init,
            "backup": hook_pre_backup,
            "blueprint": hook_pre_blueprint,
            "config_check": hook_pre_config_check,
            "write_tests": hook_pre_write_tests,
            "scenario": hook_pre_scenario,
            "function_test": hook_pre_function_test,
            "s4": hook_pre_s4,
            "fix": hook_pre_fix,
            "bump": hook_pre_bump,
            "gen_report": hook_pre_gen_report,
            "write_conclusion": hook_pre_write_conclusion,
        }
        fn = pre_map.get(step)
        if fn:
            fn(skill_dir)
        else:
            print(f"未知步骤: {step}")
            sys.exit(1)

    elif cmd == "done":
        post_map = {
            "init": hook_post_init,
            "backup": hook_post_backup,
            "blueprint": hook_post_blueprint,
            "config_check": hook_post_config_check,
            "write_tests": hook_post_write_tests,
            "scenario": hook_post_scenario,
            "function_test": hook_post_function_test,
            "s4": hook_post_s4,
            "fix": hook_post_fix,
            "bump": hook_post_bump,
            "gen_report": hook_post_gen_report,
            "write_conclusion": hook_post_write_conclusion,
        }
        fn = post_map.get(step)
        if fn:
            fn(skill_dir)
        else:
            print(f"未知步骤: {step}")
            sys.exit(1)

    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
