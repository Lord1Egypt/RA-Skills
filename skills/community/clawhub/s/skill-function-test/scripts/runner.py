"""
runner.py — 场景测试全流程编排器

10 阶段流程（配置驱动，钩子强制阻断）：
  1 备份 → 2 蓝皮书 → 3 配置确认 → 4 S1-S3 场景测试 →
  5 D1-D6 功能测试 → 6 S4 执行忠实度 → 7 修复 →
  8 bump → 9 报告 → 10 结论写入

LLM 交互点：
  - Stage 3: 展示配置，确认一致性
  - Stage 4-6: LLM 编写测试用例/噪声方案，按轮次执行
  - Stage 7: LLM 执行修复（fix_mode 开启时）
"""
import json
import os
import shutil
import subprocess as _sp
import sys
from datetime import datetime

# R-12 合规
DATA_DIR = os.path.join(".standardization", "skill-function-test", "data")

STAGES = {
    1: "备份",
    2: "蓝皮书扫描 + 约束提取",
    3: "强制确认配置一致性",
    4: "S1-S3 场景测试（写用例 → 轮次执行）",
    5: "D1-D6 功能测试（轮次执行）",
    6: "S4 执行忠实度（写噪声方案 → 轮次回放）",
    7: "修复",
    8: "版本号 bump",
    9: "报告输出 + S4 坚守率矩阵",
    10: "结论写入 target-skill/references/test-report.md",
}


class PipelineState:
    """全流程状态对象"""
    def __init__(self, skill_dir: str, continue_mode: bool = False):
        self.skill_dir = os.path.abspath(skill_dir)
        self.skill_name = os.path.basename(self.skill_dir)
        self.continue_mode = continue_mode
        self.current_stage = 0
        self.stage_log = {}

        self.backup_path: str = ""
        self.blueprint: dict = {}
        self.blueprint_text: str = ""
        self.constraints: list[dict] = []
        self.test_plan: dict = {}
        self.scenario_report: dict = {}
        self.function_report: dict = {}
        self.scenario_text: str = ""
        self.function_text: str = ""
        self.s4_matrix: dict = {}
        self.s4_matrix_text: str = ""
        self.s4_score: dict = {}
        self.s4_trace: list = []
        self.fix_results: list[dict] = []
        self.regression_report: dict = {}
        self.regression_text: str = ""
        self.final_report: str = ""
        self.blocked: bool = False
        self.block_reason: str = ""
        self.pending_stage: int = 0
        self.pending_reason: str = ""

    def log_stage(self, stage: int, status: str, result: str = ""):
        self.stage_log[stage] = {
            "stage": STAGES.get(stage, f"阶段{stage}"),
            "status": status,
            "result": result[:500],
            "timestamp": datetime.now().isoformat(),
        }
        self.current_stage = stage

    def summary(self) -> str:
        lines = [f"=== 流程进度: {self.skill_name} ==="]
        for s in sorted(self.stage_log):
            entry = self.stage_log[s]
            icon = {"ok": "✅", "skip": "⏭️", "blocked": "❌", "pending": "⏳"}.get(
                entry["status"], "❓")
            lines.append(f"  {icon} 阶段{s} {entry['stage']}: {entry['status']}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════
# 阶段执行函数
# ═══════════════════════════════════════════════════════

def stage_1_backup(state: PipelineState) -> PipelineState:
    from backup import backup_skill
    print(f"\n{'='*50}")
    print(f"  阶段1/10: 备份")
    print(f"{'='*50}")
    if not os.path.exists(state.skill_dir):
        raise FileNotFoundError(f"目标目录不存在: {state.skill_dir}")
    state.backup_path = backup_skill(state.skill_dir, "pre_test")
    state.log_stage(1, "ok", f"备份路径: {state.backup_path}")
    return state


def stage_2_blueprint(state: PipelineState) -> PipelineState:
    from inspector import scan, print_bluebook, extract_constraints
    from s4_engine import _data_dir_for, generate_test_scope, save_test_scope
    print(f"\n{'='*50}")
    print(f"  阶段2/10: 蓝皮书扫描 + 约束提取")
    print(f"{'='*50}")
    bb = scan(state.skill_dir)
    state.blueprint = bb.to_dict()
    state.blueprint_text = print_bluebook(bb)
    print(state.blueprint_text)

    s4_data_dir = _data_dir_for(state.skill_dir)
    os.makedirs(s4_data_dir, exist_ok=True)
    bp_path = os.path.join(s4_data_dir, ".scenario-test_blueprint.json")
    with open(bp_path, "w", encoding="utf-8") as f:
        json.dump(state.blueprint, f, ensure_ascii=False, indent=2)
    print(f"\n  蓝皮书已保存: {bp_path}")

    print("\n  [S4 阶段A] 提取约束...")
    constraints = extract_constraints(state.skill_dir)
    state.constraints = constraints
    cpath = os.path.join(s4_data_dir, ".constraint-list.json")
    with open(cpath, "w", encoding="utf-8") as f:
        json.dump(constraints, f, ensure_ascii=False, indent=2)
    print(f"  [S4] 约束清单已保存: {cpath} ({len(constraints)} 条)")

    print("\n  [S4 阶段A] 生成全量测试范围...")
    full_scope = generate_test_scope(state.skill_dir)
    save_test_scope(state.skill_dir, full_scope)

    if constraints:
        from s4_engine import print_constraint_summary
        print(print_constraint_summary(full_scope))

    state.log_stage(2, "ok",
        f"文件: {state.blueprint['file_count']} | 函数: {len(state.blueprint.get('functions',[]))}")
    return state


def stage_3_config_check(state: PipelineState) -> PipelineState:
    """
    阶段3: 强制确认配置一致性
    自动校验 .test-config.json + 蓝皮书的一致性，自动修正不合理项。
    不询问用户，直接继续。
    """
    from test_config import load_config, format_config, get_active_tests, get_s4_rounds
    print(f"\n{'='*50}")
    print(f"  阶段3/10: 强制确认配置一致性")
    print(f"{'='*50}")

    cfg = load_config(state.skill_dir)
    bp = state.blueprint

    # ── 展示蓝皮书摘要 ──
    print(f"""
╔══════════════════════════════════════════════╗
║  技能蓝皮书摘要                            ║
╠══════════════════════════════════════════════╣
║  技能: {bp.get('skill_name','?'):<35s} ║
║  版本: {bp.get('version','?'):<35s} ║
║  文件: {bp.get('file_count',0):<4d} 个         ║
║  函数: {len(bp.get('functions',[])):<4d} 个    ║
║  约束: {len(state.constraints):<4d} 条 (S4)    ║
╚══════════════════════════════════════════════╝
""".strip())
    print()

    # ── 展示当前配置 ──
    print("=== 当前配置（来自 .test-config.json）===")
    print(format_config(cfg))

    # ── 自动校验 ──
    print("\n── 配置自检 ──")
    checks = []
    auto_fixes = []

    # Check 1: rounds > 0
    r = cfg.get("rounds", 3)
    if not isinstance(r, int) or r < 1:
        old_r = r
        cfg["rounds"] = 1
        auto_fixes.append(f"轮数 {old_r} 不合理 → 自动修正为 1")
        r = 1

    # Check 2: s4.enabled 但无约束数据
    s4_enabled = cfg.get("s4", {}).get("enabled", True)
    s4_rounds = cfg.get("s4", {}).get("rounds", r)
    if s4_enabled and not isinstance(s4_rounds, int) or s4_rounds < 1:
        old_s4r = s4_rounds
        cfg["s4"]["rounds"] = 1
        auto_fixes.append(f"S4 轮数 {old_s4r} 不合理 → 自动修正为 1")
        s4_rounds = 1

    # Check 3: fix_mode 格式
    fm = cfg.get("fix_mode", {"scenario": 0, "function": 0})
    if isinstance(fm, int):
        fm = {"scenario": fm, "function": fm}
        cfg["fix_mode"] = fm
        auto_fixes.append(f"fix_mode 为整数格式 → 自动转换为 dict: {fm}")

    # Check 4: 维度开关是否存在
    dims_on = []
    for group_name, dims in [("scenarios", ["S1", "S2", "S3"]),
                              ("functions", ["D1", "D2", "D3", "D4", "D5", "D6"])]:
        for d in dims:
            if cfg.get(group_name, {}).get(d, {}).get("enabled", True):
                dims_on.append(d)
    if s4_enabled:
        dims_on.append("S4")

    if not any(d.startswith("S") for d in dims_on) and not any(d.startswith("D") for d in dims_on) and not s4_enabled:
        checks.append(("WARN", "所有场景/功能/S4 维度均已关闭，直接执行将无任何测试内容"))
    elif not any(d.startswith("S") for d in dims_on):
        checks.append(("INFO", "场景维度全部关闭，仅执行功能测试(+S4)"))
    elif not any(d.startswith("D") for d in dims_on):
        checks.append(("INFO", "功能维度全部关闭，仅执行场景测试(+S4)"))

    # Check 5: s4.enabled 无 constraints
    if s4_enabled and not state.constraints:
        checks.append(("WARN", "S4 已开启但蓝皮书中未提取到约束，S4 忠实度测试可能无噪声依据"))

    # Check 6: fix_mode=1 但无启用维度
    if (fm.get("scenario", 0) == 1 or fm.get("function", 0) == 1) and not dims_on:
        checks.append(("WARN", "修复模式已开启但无启用维度，修复步骤将无问题可修"))

    # Check 7: S4 正向/反向权重合理
    sw = cfg.get("s4_weights", {})
    pf = sw.get("positive", 0.4)
    nf = sw.get("negative", 0.6)
    if not (0 <= pf <= 1) or not (0 <= nf <= 1) or abs(pf + nf - 1.0) > 0.01:
        checks.append(("WARN", f"S4 权重 ({pf},{nf}) 不合理，总和应 ≈ 1.0"))

    # ── 输出校验结果 ──
    if auto_fixes:
        for fix_msg in auto_fixes:
            print(f"  🔧 [AUTO-FIX] {fix_msg}")
    for level, msg in checks:
        icon = {"WARN": "⚠️", "INFO": "ℹ️"}.get(level, "ℹ️")
        print(f"  {icon} [{level}] {msg}")

    if not auto_fixes and not any(l == "WARN" for l, _ in checks):
        print("\n  ✅ 配置一致性校验通过，所有项自洽")
    elif auto_fixes:
        print(f"\n  🔧 已自动修正 {len(auto_fixes)} 项不一致，其余无问题")
    else:
        print(f"\n  ⚠️ 配置有 {sum(1 for l,_ in checks if l=='WARN')} 项警告（不阻断，按配置执行）")

    # ── 更新 state ──
    active = get_active_tests(cfg)
    state.test_plan = {
        "dimensions": active,
        "fix_mode": fm,
        "rounds": r,
        "s4_enabled": s4_enabled,
        "s4_rounds": s4_rounds,
    }

    # ── 生成执行清单（供后续 hooks 校验）──
    try:
        from hooks import _generate_execution_checklist
        _generate_execution_checklist(state.skill_dir)
    except ImportError:
        pass

    print(f"\n  按此配置执行: {', '.join(active) if active else '无维度'}")
    state.log_stage(3, "ok", f"自检通过, 维度: {', '.join(active) if active else '无'}")
    return state


def stage_4_scenario(state: PipelineState) -> PipelineState:
    """阶段4: S1-S3 场景测试 — LLM 编写用例 → 按轮次执行"""
    from scenario_engine import run_scenario_test
    from test_config import load_config
    from s4_engine import _data_dir_for
    print(f"\n{'='*50}")
    print(f"  阶段4/10: S1-S3 场景测试")
    print(f"{'='*50}")

    config = load_config(state.skill_dir)
    test_rounds = config.get("rounds", 3)
    dims = state.test_plan.get("dimensions", "all")

    def _has_s_dim(name):
        if dims == "all":
            return True
        if isinstance(dims, str):
            return name in dims
        if isinstance(dims, list):
            return name in dims
        return False

    # ① 先检查 S1-S3 是否启用，没开直接跳过
    if not any(_has_s_dim(f"S{i}") for i in (1, 2, 3)):
        print("  [SKIP] 场景维度均未启用")
        state.log_stage(4, "skip", "场景维度未启用")
        return state

    # ② S 已启用 → 检查测试计划文件
    plan_path = os.path.join(_data_dir_for(state.skill_dir), ".s_test_plan.json")
    if not os.path.exists(plan_path):
        if not state.continue_mode:
            bp = state.blueprint
            print(f"\n{'='*60}")
            print(f"  需要编写场景测试计划 (S1-S3)")
            print(f"{'─'*60}")
            print(f"  格式: references/s-test-plan-schema.md")
            print(f"  目标: {plan_path}")
            print()
            print(f"  ── 蓝皮书摘要 ──")
            print(f"  技能: {bp.get('skill_name', '?')}")
            print(f"  版本: {bp.get('version', '?')}")
            print(f"  文件: {bp.get('file_count', 0)} 个")
            print(f"  核心函数: {len(bp.get('functions', []))} 个")
            print()
            top_funcs = [f.get('name','') for f in bp.get('functions',[])[:10]]
            if top_funcs:
                print(f"  主要函数: {', '.join(top_funcs)}")
            print()
            print(f"  ── S1 触发场景 ──")
            print(f"  编写至少 2 条：用户输入自然语言触发词")
            print(f"  + 期望技能如何响应")
            print()
            print(f"  ── S2 核心能力 ──")
            print(f"  编写至少 2 条：给定参数调用核心函数")
            print(f"  + 期望返回值特征")
            print()
            print(f"  ── S3 工作流链路 ──")
            print(f"  编写至少 1 条：多步骤连贯执行")
            print(f"  + 每步之间数据传递的期望")
            print(f"{'='*60}")
            # 写入一个骨架模板到目标路径，LLM 直接编辑即可
            skeleton = {
                "S1": [{"id":"S1-01","name":"示例场景","trigger":"用户输入","expected":"期望输出","type":"trigger","modules":[]}],
                "S2": [{"id":"S2-01","name":"示例能力","input":"函数调用","expected":"期望返回值","type":"capability","modules":[]}],
                "S3": [{"id":"S3-01","name":"示例流程","steps":["步骤1","步骤2"],"expected":"期望结果","type":"workflow","modules":[]}]
            }
            with open(plan_path, 'w', encoding='utf-8') as f:
                json.dump(skeleton, f, ensure_ascii=False, indent=2)
            print(f"\n  ✅ 已生成骨架文件: {plan_path}")
            print(f"  LLM 请直接编辑此文件，填充真实场景用例后重新运行。")
            print()
            state.pending_stage = 4
            state.pending_reason = "已生成骨架 .s_test_plan.json，LLM 编辑后 --continue"
            state.log_stage(4, "pending", state.pending_reason)
            return state
        else:
            print("  [SKIP] 未提供 .s_test_plan.json，跳过 S1-S3")
            state.log_stage(4, "skip", "无计划文件")
            return state

    all_reports, all_texts = [], []
    for r in range(1, test_rounds + 1):
        if test_rounds > 1:
            print(f"\n  ── 场景测试 第 {r}/{test_rounds} 轮 ──")
        s_report, s_text = run_scenario_test(state.skill_dir, state.blueprint)
        all_reports.append(s_report)
        all_texts.append(s_text)
        if test_rounds == 1:
            print(s_text)
        else:
            print(f"  [场景] 第 {r} 轮完成")

    state.scenario_report = all_reports[-1] if all_reports else {}
    state.scenario_text = all_texts[-1] if all_texts else ""
    if test_rounds > 1:
        state.scenario_text += f"\n--- 场景测试共执行 {test_rounds} 轮 ---\n"

    state.log_stage(4, "ok", f"{test_rounds}轮完成")
    return state


def stage_5_function_test(state: PipelineState) -> PipelineState:
    """阶段5: D1-D6 功能测试 — 按轮次执行"""
    from test_config import load_config
    print(f"\n{'='*50}")
    print(f"  阶段5/10: D1-D6 功能测试")
    print(f"{'='*50}")

    config = load_config(state.skill_dir)
    test_rounds = config.get("rounds", 3)
    dims = state.test_plan.get("dimensions", "all")

    def _has_d_dim(name):
        if dims == "all":
            return True
        if isinstance(dims, str):
            return name in dims
        if isinstance(dims, list):
            return name in dims
        return False

    if not any(_has_d_dim(f"D{i}") for i in (1, 2, 3, 4, 5, 6)):
        print("  [SKIP] 功能维度均未启用")
        state.log_stage(5, "skip", "功能维度未启用")
        return state

    all_texts, all_reports = [], []
    for r in range(1, test_rounds + 1):
        if test_rounds > 1:
            print(f"\n  ── 功能测试 第 {r}/{test_rounds} 轮 ──")
        te_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_engine.py")
        r_proc = _sp.run([sys.executable, te_script, state.skill_dir],
                         capture_output=True, text=True, timeout=300)
        f_text = r_proc.stdout
        if r_proc.returncode != 0:
            f_text += f"\n[WARN] test_engine exit={r_proc.returncode}, stderr={r_proc.stderr[:200]}"
        f_report = {}
        from s4_engine import _data_dir_for
        fr_path = os.path.join(_data_dir_for(state.skill_dir), ".function-test_report.json")
        if os.path.exists(fr_path):
            try:
                with open(fr_path, "r", encoding="utf-8") as _fh:
                    f_report = json.load(_fh)
            except Exception:
                pass
        # fallback: parse from stdout
        if not f_report:
            for line in f_text.split("\n"):
                if line.strip().startswith("{") and "results" in line:
                    try:
                        f_report = json.loads(line.strip())
                    except Exception:
                        pass
        all_texts.append(f_text)
        all_reports.append(f_report)
        if test_rounds == 1:
            print(f_text)
        else:
            print(f"  [功能] 第 {r} 轮完成 (exit={r_proc.returncode})")

    state.function_report = all_reports[-1] if all_reports else {}
    state.function_text = all_texts[-1] if all_texts else ""
    if test_rounds > 1:
        n_pass = sum(1 for rp in all_reports if rp.get("status") == "pass")
        state.function_text += f"\n--- 功能测试共执行 {test_rounds} 轮，通过 {n_pass}/{test_rounds} ---\n"

    state.log_stage(5, "ok", f"{test_rounds}轮完成")
    return state


def stage_6_s4(state: PipelineState) -> PipelineState:
    """阶段6: S4 执行忠实度 — LLM 编写噪声方案 → 按轮次回放"""
    from test_config import load_config
    print(f"\n{'='*50}")
    print(f"  阶段6/10: S4 执行忠实度")
    print(f"{'='*50}")

    config = load_config(state.skill_dir)
    s4_enabled = config.get("s4", {}).get("enabled", state.test_plan.get("s4_enabled", True))
    if not s4_enabled:
        print("  [SKIP] S4 已关闭")
        state.log_stage(6, "skip", "S4 关闭")
        return state

    # S4 已启用 → 检查噪音方案文件
    from s4_engine import _data_dir_for as _s4_data
    noise_plan_path = os.path.join(_s4_data(state.skill_dir), ".s4_noise_plan.json")
    if not os.path.exists(noise_plan_path):
        if not state.continue_mode:
            constraints = state.constraints
            print(f"\n{'='*60}")
            print(f"  需要编写 S4 噪声方案")
            print(f"{'─'*60}")
            print(f"  格式: references/s4-noise-testing.md")
            print(f"  目标: {noise_plan_path}")
            print()
            print(f"  ── 约束清单摘要 ({len(constraints)} 条) ──")
            for i, c in enumerate(constraints[:8]):
                print(f"  {i+1}. [{c.get('level','?')}] {c.get('text','')[:80]}")
            if len(constraints) > 8:
                print(f"  ... 还有 {len(constraints)-8} 条")
            print()
            print(f"  ── 噪音分级 ──")
            print(f"  L1 软干扰: 轻量质疑/建议")
            print(f"  L2 跳过质疑: 明确要求跳过步骤")
            print(f"  L3 反向指令: 直接违背铁律")
            print(f"  L4 环境污染: 伪造产物/信息污染")
            print(f"  L5 条件篡改: 中途更新前提条件")
            print(f"{'='*60}")
            skeleton = {
                "test_scenarios": [
                    {"id":"S4-L1-01","level":"L1","noise":"这步挺麻烦的","target_constraint":"","expected_action":"不跳过"}
                ]
            }
            with open(noise_plan_path, 'w', encoding='utf-8') as f:
                json.dump(skeleton, f, ensure_ascii=False, indent=2)
            print(f"\n  ✅ 已生成骨架文件: {noise_plan_path}")
            print(f"  LLM 请基于约束清单编辑此文件，填充噪声方案后重新运行。")
            print()
            state.pending_stage = 6
            state.pending_reason = "已生成骨架 .s4_noise_plan.json，LLM 编辑后 --continue"
            state.log_stage(6, "pending", state.pending_reason)
            return state
        else:
            print("  [SKIP] 未提供 .s4_noise_plan.json，跳过 S4")
            state.log_stage(6, "skip", "无噪音方案")
            return state

    s4_rounds = config.get("s4", {}).get("rounds",
        state.test_plan.get("s4_rounds", config.get("rounds", 3)))

    print(f"\n  [RUN] S4 脏环境忠实度测试 ({s4_rounds} 轮)...")

    try:
        from s4_engine import NoisePlayer
        player = NoisePlayer(state.skill_dir)
        if player.plan:
            player.playback_all_rounds(rounds=s4_rounds)
    except ImportError:
        pass

    s4_fix_mode = state.test_plan.get("fix_mode", {}).get("s4", 0) if isinstance(state.test_plan.get("fix_mode"), dict) else 0
    if s4_fix_mode == 1:
        print("\n  [S4-修复] 检查可修复项...")
        try:
            from s4_engine import s4_scope_repair, load_test_scope
            scope = load_test_scope(state.skill_dir)
            if scope:
                s4_scope_repair(state.skill_dir, scope, dry_run=False)
        except ImportError:
            pass

    all_rounds = []
    from s4_engine import _data_dir_for
    s4_data_dir = _data_dir_for(state.skill_dir)
    os.makedirs(s4_data_dir, exist_ok=True)

    for r in range(1, s4_rounds + 1):
        print(f"\n  ── S4 第 {r}/{s4_rounds} 轮 ──")
        round_file = os.path.join(s4_data_dir, f".s4_trace_r{r}.json")
        if os.path.exists(round_file):
            with open(round_file, "r", encoding="utf-8") as f:
                round_trace = json.load(f)
        else:
            from s4_engine import load_trace
            round_trace = load_trace(state.skill_dir)
            if round_trace and s4_rounds > 1:
                trace_backup = os.path.join(s4_data_dir, f".s4_trace_round{r}.json")
                with open(trace_backup, "w", encoding="utf-8") as fb:
                    json.dump(round_trace, fb, ensure_ascii=False, indent=2)

        if round_trace:
            all_rounds.extend(round_trace)
            print(f"  [S4] 第 {r} 轮完成: {len(round_trace)} 条噪音")
        else:
            print(f"\n  ╔══ S4 第 {r}/{s4_rounds} 轮：LLM 必须执行 ═══╗")
            print(f"  ║  1. 读取约束清单 → 设计噪音方案              ║")
            print(f"  ║  2. 写入 .s4_noise_plan.json                ║")
            print(f"  ║  3. 执行噪音 → 记录到 .s4_trace_r{r}.json  ║")
            print(f"  ╚════════════════════════════════════════════════╝")

    from s4_engine import generate_fidelity_matrix, print_fidelity_matrix, \
        extract_workflow_steps, print_workflow_steps, \
        generate_fidelity_score, print_fidelity_score

    s4_weights = config.get("s4_weights", {"positive": 0.4, "negative": 0.6})
    negative_rate = 0.0
    if all_rounds:
        s4_matrix = generate_fidelity_matrix(all_rounds)
        state.s4_matrix = s4_matrix
        state.s4_matrix_text = print_fidelity_matrix(s4_matrix)
        print(state.s4_matrix_text)
        n_held = sum(1 for t in all_rounds if t.get('llm_behavior') == '坚守')
        n_total = len(all_rounds)
        negative_rate = n_held / n_total if n_total > 0 else 0.0
        print(f"  [S4] 反向坚守率: {n_held}/{n_total} ({negative_rate*100:.0f}%)")

        # load s4 trace for report (must happen before positive check)
        s4_trace_path = os.path.join(s4_data_dir, ".s4_trace.json")
        if os.path.exists(s4_trace_path):
            try:
                with open(s4_trace_path, "r", encoding="utf-8") as _tf:
                    state.s4_trace = json.load(_tf)
            except Exception:
                pass

        print(f"\n  [S4-正向] 提取工作流步骤...")
        steps = extract_workflow_steps(state.skill_dir)
        print(print_workflow_steps(steps))

        positive_file = os.path.join(s4_data_dir, ".s4_positive.json")
        if os.path.exists(positive_file):
            with open(positive_file, "r", encoding="utf-8") as f:
                positive_trace = json.load(f)
            completed = sum(1 for p in positive_trace if p.get("completed", False))
            total_steps = len(positive_trace)
            positive_rate = completed / total_steps if total_steps > 0 else 0.0
            print(f"  [S4-正向] 步骤完成率: {completed}/{total_steps} ({positive_rate*100:.0f}%)")
        else:
            print("  [S4-正向] ⚠️ 无正向追踪记录，S4 综合评分仅基于反向（噪音坚守率）")
            positive_rate = 0.0
            state.pending_stage = 6
            state.pending_reason = "缺少 .s4_positive.json（可选），仅反向评分"

        score_result = generate_fidelity_score(
            positive_rate, negative_rate,
            s4_weights.get("positive", 0.4),
            s4_weights.get("negative", 0.6),
        )
        state.s4_score = score_result
        # load s4 trace for report
        s4_trace_path = os.path.join(s4_data_dir, ".s4_trace.json")
        if os.path.exists(s4_trace_path):
            try:
                with open(s4_trace_path, "r", encoding="utf-8") as _tf:
                    state.s4_trace = json.load(_tf)
            except Exception:
                pass
        print()
        print(print_fidelity_score(score_result))
    else:
        noise_path = os.path.join(s4_data_dir, ".s4_noise_plan.json")
        print(f"\n{'='*60}")
        print("  ⛔ S4 受阻：无噪音方案")
        print("  ──────────────────────────────────────────")
        print("  配置要求执行 S4，但未找到噪音方案文件。")
        print("  LLM 必须按以下步骤操作后重新运行：")
        print()
        print("  1. 读取约束清单")
        print(f"     path: {os.path.join(s4_data_dir, '.constraint-list.json')}")
        print("  2. 设计噪音方案（L1-L5 级别）")
        print(f"  3. 写入: {noise_path}")
        print("  4. 校验: python s4_engine.py <skill> validate <json>")
        print(f"{'='*60}")
        print("  此阶段完成前不会继续后续阶段。")
        state.blocked = True
        state.block_reason = "S4 无噪音方案: 请创建 .s4_noise_plan.json 后重试"
        return state

    state.log_stage(6, "ok",
        f"S4矩阵{'已生成' if state.s4_matrix else '跳过'}")
    return state


def stage_7_fix(state: PipelineState) -> PipelineState:
    """阶段7: 修复 — LLM 过滤误报 + 自动修复"""
    from test_config import load_config
    print(f"\n{'='*50}")
    print(f"  阶段7/10: 修复")
    print(f"{'='*50}")

    config = load_config(state.skill_dir)
    fm = config.get("fix_mode", state.test_plan.get("fix_mode", {}))
    if isinstance(fm, int):
        fm = {"scenario": fm, "function": fm, "s4": fm}
    scenario_fix = fm.get("scenario", 0)
    function_fix = fm.get("function", 0)

    if scenario_fix == 0 and function_fix == 0:
        print("  仅报告模式，不执行修复")
        state.log_stage(7, "skip", "仅报告模式")
        return state

    # 收集所有待判断问题
    all_issues = []
    for src, data in [("场景", state.scenario_report), ("功能", state.function_report)]:
        for r in data.get("results", []):
            if r.get("level") in ("block", "warn") and r.get("status") == "fail":
                issue = {
                    "source": src,
                    "dim": r.get("sid", r.get("dim", "?")),
                    "level": r.get("level"),
                    "name": r.get("name", ""),
                    "message": r.get("message", ""),
                    "file": r.get("file", ""),
                    "lineno": r.get("lineno", 0),
                    "suggestion": r.get("suggestion", ""),
                    "llm_judgment": "",
                }
                if issue["file"] and issue["lineno"]:
                    fpath = os.path.join(state.skill_dir, issue["file"]) \
                        if not os.path.isabs(issue["file"]) else issue["file"]
                    if os.path.exists(fpath):
                        try:
                            with open(fpath, "r", encoding="utf-8") as f:
                                src_lines = f.read().split("\n")
                            start = max(0, issue["lineno"] - 4)
                            end = min(len(src_lines), issue["lineno"] + 3)
                            ctx = []
                            for i in range(start, end):
                                marker = "→" if i == issue["lineno"] - 1 else " "
                                ctx.append(f"{marker} {i+1:4d}| {src_lines[i]}")
                            issue["source_context"] = "\n".join(ctx)
                        except Exception:
                            issue["source_context"] = "(无法读取)"
                all_issues.append(issue)

    state.fix_results = all_issues

    if not all_issues:
        print("  无待判断问题，跳过修复")
        state.log_stage(7, "ok", "无问题")
        return state

    print(f"  共 {len(all_issues)} 条问题待 LLM 判断（FP/真问题）:")
    for i, issue in enumerate(all_issues, 1):
        print(f"\n  [{i}/{len(all_issues)}] {'⚠️' if issue['level']=='warn' else '🔴'} "
              f"[{issue['source']}:{issue['dim']}] {issue['name']}")
        print(f"    级别: F-{'0 BLOCK' if issue['level']=='block' else '1 WARN'}")
        print(f"    文件: {issue['file']}:{issue['lineno']}")
        print(f"    信息: {issue['message']}")
        if issue.get("source_context"):
            print(f"    代码上下文:\n{issue['source_context']}")
        print(f"    建议: {issue['suggestion']}")
        print(f"    ── LLM 判断: [FP] 误报 / [FIX] 真问题 ──")

    state.log_stage(7, "ok", f"待判断: {len(all_issues)} 条")
    return state


def stage_8_bump(state: PipelineState) -> PipelineState:
    """阶段8: 版本号 bump — 仅在修复有变更时执行"""
    print(f"\n{'='*50}")
    print(f"  阶段8/10: 版本号 bump")
    print(f"{'='*50}")

    fm = state.test_plan.get("fix_mode", {})
    if isinstance(fm, int):
        fm = {"scenario": fm, "function": fm}
    has_fix = fm.get("scenario", 0) == 1 or fm.get("function", 0) == 1
    if not has_fix:
        print("  未开启修复模式，跳过 bump")
        state.log_stage(8, "skip", "未开启修复")
        return state

    if not state.fix_results:
        print("  无修复记录，跳过 bump")
        state.log_stage(8, "skip", "无修复")
        return state

    try:
        from bump_version import auto_bump, get_current_version, detect_bump_type
        old = get_current_version(state.skill_dir)
        if not old:
            print("  [BUMP] 无法读取版本号，跳过")
            state.log_stage(8, "skip", "无版本号")
            return state

        btype = detect_bump_type(state.skill_dir)
        print(f"  当前版本: {old}, 检测变更类型: {btype}")
        new_ver = auto_bump(state.skill_dir, btype,
                           ["场景测试修复后自动版本更新"])
        if new_ver:
            print(f"  [BUMP] ✅ 版本已更新: {old} → {new_ver}")
        else:
            print(f"  [BUMP] ⚠️ 版本更新失败")
    except Exception as e:
        print(f"  [BUMP] 异常: {e}")

    state.log_stage(8, "ok", "bump 执行完毕")
    return state


def stage_9_report(state: PipelineState) -> PipelineState:
    """阶段9: 报告输出 + S4 坚守率矩阵"""
    from gen_report import gen_markdown as _gen_md, gen_html as _gen_html
    print(f"\n{'='*50}")
    print(f"  阶段9/10: 报告输出")
    print(f"{'='*50}")

    # 构造 data 字典给 gen_report 使用
    from timeline import _load_timeline
    data = {
        "skill_dir": state.skill_dir,
        "skill_name": state.skill_name,
        "timeline": _load_timeline(state.skill_dir) or {},
        "rounds": [],
        "s4_rounds": state.test_plan.get("s4_rounds", 1),
        "scenario": state.scenario_report,
        "function": state.function_report,
        "s4_trace": state.s4_trace,
        "fix_record": state.fix_results,
        "test_reports": {},
        "s4_score": state.s4_score,
        "regression": state.regression_report,
    }

    # 保存到数据目录
    from s4_engine import _data_dir_for
    outputs_dir = _data_dir_for(state.skill_dir)
    os.makedirs(outputs_dir, exist_ok=True)

    md = _gen_md(data)
    md_path = os.path.join(outputs_dir, ".test-report.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"  [REPORT] Markdown 报告: {md_path}")

    html = _gen_html(data)
    html_path = os.path.join(outputs_dir, ".test-report.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  [REPORT] HTML 报告: {html_path}")

    lines = ["=" * 60,
             f"  测试最终报告: {state.skill_name}",
             "=" * 60, "",
             state.summary(), ""]
    if state.scenario_text:
        lines.append("── 场景测试结果 ──")
        lines.append(state.scenario_text[:500])
    if state.function_text:
        lines.append("── 功能测试结果 ──")
        lines.append(state.function_text[:500])
    if state.s4_matrix_text:
        lines.append("── S4 脏环境忠实度 ──")
        lines.append(state.s4_matrix_text)
    if state.s4_score:
        from s4_engine import print_fidelity_score
        lines.append(print_fidelity_score(state.s4_score))
    if state.regression_text:
        lines.append(state.regression_text)

    state.final_report = "\n".join(lines)
    print(state.final_report)

    state.log_stage(9, "ok", f"报告已保存: {md_path}, {html_path}")
    return state


def stage_10_conclusion(state: PipelineState) -> PipelineState:
    """阶段10: 结论写入 target-skill/references/test-report.md"""
    from gen_report import _write_conclusion
    print(f"\n{'='*50}")
    print(f"  阶段10/10: 结论写入 test-report.md")
    print(f"{'='*50}")

    data = {
        "skill_dir": state.skill_dir,
        "skill_name": state.skill_name,
        "scenario": state.scenario_report,
        "function": state.function_report,
        "s4_trace": state.s4_trace,
        "fix_record": state.fix_results,
        "s4_score": state.s4_score,
        "regression": state.regression_report,
        "test_plan": state.test_plan,
    }
    _write_conclusion(state.skill_dir, data)
    state.log_stage(10, "ok", "结论已写入 test-report.md")
    return state


# ═══════════════════════════════════════════════════════
# 全流程执行
# ═══════════════════════════════════════════════════════

def _run_stage(state, stage_fn, stage_num, name):
    """Run a stage, catching sys.exit(1) from engines and converting to blocked state."""
    from timeline import cmd_mark
    cmd_mark(state.skill_dir, f"stage{stage_num}", name, "start")
    try:
        result = stage_fn(state)
        cmd_mark(state.skill_dir, f"stage{stage_num}", name, "end")
        return result
    except SystemExit as e:
        cmd_mark(state.skill_dir, f"stage{stage_num}", name, "end")
        state.blocked = True
        state.block_reason = f"阶段{stage_num} {name} 受阻: 需要 LLM 介入后重试"
        state.log_stage(stage_num, "blocked", state.block_reason)
        print(f"\n  ❌ 阶段{stage_num} {name} 受阻 — 请按上方提示操作后重新运行")
        return state


def run_full(skill_dir: str, continue_mode: bool = False) -> PipelineState:
    from test_config import load_config, get_active_tests

    state = PipelineState(skill_dir, continue_mode=continue_mode)
    from timeline import cmd_init, cmd_mark
    cmd_init(skill_dir)
    cmd_mark(skill_dir, "pipeline", "全流程启动", "start")
    cfg = load_config(skill_dir)
    active_dims = get_active_tests(cfg)
    fm = cfg.get("fix_mode", {"scenario": 0, "function": 0})
    if isinstance(fm, int):
        fm = {"scenario": fm, "function": fm}
    state.test_plan = {
        "dimensions": active_dims,
        "fix_mode": fm,
        "rounds": cfg.get("rounds", 3),
        "s4_enabled": cfg.get("s4", {}).get("enabled", True),
        "s4_rounds": cfg.get("s4", {}).get("rounds", cfg.get("rounds", 3)),
    }

    print(f"\n{'=' * 50}")
    print(f"  全流程启动 — 基于 .test-config.json")
    print(f"{'=' * 50}")
    print(f"  维度: {', '.join(active_dims)}")
    print(f"  场景修复: {['仅报告', '尝试修复'][fm.get('scenario', 0)]}")
    print(f"  功能修复: {['仅报告', '直接修复'][fm.get('function', 0)]}")
    print(f"  S4: {'开启' if state.test_plan['s4_enabled'] else '关闭'} ({state.test_plan['s4_rounds']}轮)")
    print()

    state = _run_stage(state, stage_1_backup, 1, "备份")
    if hasattr(state, 'pending_stage') and state.pending_stage: return state
    if getattr(state, 'blocked', False): return state
    state = _run_stage(state, stage_2_blueprint, 2, "蓝皮书")
    if hasattr(state, 'pending_stage') and state.pending_stage: return state
    if getattr(state, 'blocked', False): return state
    state = _run_stage(state, stage_3_config_check, 3, "配置确认")
    if hasattr(state, 'pending_stage') and state.pending_stage: return state
    if getattr(state, 'blocked', False): return state
    state = _run_stage(state, stage_4_scenario, 4, "S1-S3场景测试")
    if hasattr(state, 'pending_stage') and state.pending_stage: return state
    if getattr(state, 'blocked', False): return state
    state = _run_stage(state, stage_5_function_test, 5, "D1-D6功能测试")
    if hasattr(state, 'pending_stage') and state.pending_stage: return state
    if getattr(state, 'blocked', False): return state
    state = _run_stage(state, stage_6_s4, 6, "S4执行忠实度")
    if hasattr(state, 'pending_stage') and state.pending_stage: return state
    if getattr(state, 'blocked', False): return state
    state = _run_stage(state, stage_7_fix, 7, "修复")
    if hasattr(state, 'pending_stage') and state.pending_stage: return state
    if getattr(state, 'blocked', False): return state
    state = _run_stage(state, stage_8_bump, 8, "版本号bump")
    if hasattr(state, 'pending_stage') and state.pending_stage: return state
    if getattr(state, 'blocked', False): return state
    state = _run_stage(state, stage_9_report, 9, "报告输出")
    if hasattr(state, 'pending_stage') and state.pending_stage: return state
    if getattr(state, 'blocked', False): return state
    state = _run_stage(state, stage_10_conclusion, 10, "结论写入")
    return state


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="skill-function-test 全流程编排器")
    parser.add_argument("skill_dir", help="目标技能目录")
    parser.add_argument("--continue", action="store_true", dest="continue_mode",
                        help="继续模式：跳过 LLM 编写计划的提示，有文件则执行，无文件则跳过")
    args = parser.parse_args()

    state = run_full(args.skill_dir, continue_mode=args.continue_mode)

    if state.pending_stage:
        stage_name = STAGES.get(state.pending_stage, f"阶段{state.pending_stage}")
        print(f"\n{'='*60}")
        print(f"  ⏸ 流程暂停: {stage_name}")
        print(f"  {state.pending_reason}")
        print(f"{'='*60}")
        print(f"  编写完成后运行: python runner.py {args.skill_dir} --continue")
    elif state.blocked:
        print(f"\n{'='*60}")
        print(f"  ❌ 流程受阻: {state.block_reason}")
        print(f"{'='*60}")
    else:
        print("用法: python runner.py <skill-dir>")
