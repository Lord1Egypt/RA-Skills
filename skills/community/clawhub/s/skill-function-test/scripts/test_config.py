"""
test_config.py — 测试配置系统

管理 skill-function-test 的测试配置（维度开关、轮数、修复模式）。
配置持久化在目标技能目录下的 .test-config.json。

支持：
- CLI：查看、修改、重置
- 文字交互：对话中的问答配置
- 与 HTML 配置界面共享同一 JSON 文件
"""
import json
import os
import sys

# ═══════════════════════════════════════════════════════
# 默认配置
# ═══════════════════════════════════════════════════════

DEFAULT_CONFIG = {
    "version": "0.1.0",
    "rounds": 3,                    # 全局默认轮数
    "fix_mode": {
        "scenario": 0,              # S1-S3: 0=仅报告 1=尝试修复
        "function": 0,              # D1-D6: 0=仅报告 1=直接修复 2=询问后修复
    },
    "s4": {
        "enabled": True,            # S4 默认开启（代码默认）
        "rounds": 3,                # S4 独立轮数（覆盖全局 rounds）
        "fix_mode": 0,              # S4: 0=仅报告 1=尝试修复(结构性修复)
    },
    "s4_weights": {                 # S4 正反权重（正向=干净环境, 反向=脏环境）
        "positive": 0.4,            # 正向（干净环境-步骤完成率）
        "negative": 0.6,            # 反向（脏环境-铁律坚守率）
    },
    "scenarios": {
        "S1": {"enabled": True},
        "S2": {"enabled": True},
        "S3": {"enabled": True},
    },
    "functions": {
        "D1": {"enabled": True},
        "D2": {"enabled": True},
        "D3": {"enabled": True},
        "D4": {"enabled": True},
        "D5": {"enabled": True},
        "D6": {"enabled": True},
    },
}


# ═══════════════════════════════════════════════════════
# 配置 I/O
# ═══════════════════════════════════════════════════════

# 数据目录常量（R-12 合规：skills/.standardization/skill-function-test/data/）
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_SKILL_DIR = os.path.dirname(_SCRIPT_DIR)
_SKILLS_ROOT = os.path.dirname(_SKILL_DIR)
# R-12 审计锚点：DATA_DIR 行直接赋值合规字面量（不可用变量替代 skill name）
DATA_DIR = os.path.join(_SKILLS_ROOT, ".standardization", "skill-function-test", "data")


def config_path(skill_dir: str) -> str:
    """目标技能的测试配置文件路径"""
    target_name = os.path.basename(os.path.abspath(skill_dir))
    cfg_dir = os.path.join(DATA_DIR, target_name, "outputs")
    os.makedirs(cfg_dir, exist_ok=True)
    return os.path.join(cfg_dir, ".test-config.json")


def load_config(skill_dir: str) -> dict:
    """加载配置（不存在则用默认值并保存）"""
    cpath = config_path(skill_dir)
    if os.path.exists(cpath):
        with open(cpath, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        # 合并缺失字段（保证版本升级时旧配置不丢字段）
        cfg = _merge_defaults(cfg)
        return cfg
    return _merge_defaults(DEFAULT_CONFIG)


def save_config(skill_dir: str, cfg: dict):
    """保存配置到目标技能目录

    如果当前测试会话进行中，拒绝保存（配置清单已锁定）。
    """
    # 会话锁定检查
    target_name = os.path.basename(os.path.abspath(skill_dir))
    flow_path = os.path.join(DATA_DIR, target_name, ".flow-state.json")
    if os.path.exists(flow_path):
        try:
            with open(flow_path, "r", encoding="utf-8") as f:
                fs = json.load(f)
            steps = fs.get("steps", {})
            auto_steps = {"init", "backup", "blueprint"}
            session_active = any(
                isinstance(v, dict) and v.get("done", False)
                for k, v in steps.items()
                if k not in auto_steps
            )
            if session_active:
                print(f"[CFG] ❌ 测试会话进行中，禁止修改配置！")
                print(f"[CFG]   配置清单已锁定，请按清单执行到底")
                return
        except Exception:
            pass

    cpath = config_path(skill_dir)
    with open(cpath, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f"[CFG] ✅ 配置已保存: {cpath}")


def _merge_defaults(cfg: dict) -> dict:
    """递归合并缺失字段（不覆盖已存在字段）"""
    def _merge(base, patch):
        result = dict(patch)
        for k, v in base.items():
            if k not in result:
                result[k] = v
            elif isinstance(v, dict) and isinstance(result[k], dict):
                result[k] = _merge(v, result[k])
        return result
    return _merge(DEFAULT_CONFIG, cfg)


# ═══════════════════════════════════════════════════════
# 配置查询与修改
# ═══════════════════════════════════════════════════════

def get_active_tests(cfg: dict) -> list[str]:
    """返回当前启用的测试维度列表"""
    enabled = []
    for k, v in cfg.get("scenarios", {}).items():
        if v.get("enabled", True):
            enabled.append(k)
    for k, v in cfg.get("functions", {}).items():
        if v.get("enabled", True):
            enabled.append(k)
    if cfg.get("s4", {}).get("enabled", False):
        enabled.append("S4")
    return enabled


def get_s4_rounds(cfg: dict) -> int:
    """获取 S4 实际轮数：优先用 S4 独立配置，否则用全局 rounds"""
    s4 = cfg.get("s4", {})
    return s4.get("rounds", cfg.get("rounds", 3))


def set_value(cfg: dict, path: str, value) -> dict:
    """
    通过点路径设置配置值。

    路径格式:
      rounds -> cfg["rounds"]
      s4.enabled -> cfg["s4"]["enabled"]
      scenarios.S1.enabled -> cfg["scenarios"]["S1"]["enabled"]
    """
    parts = path.split(".")
    target = cfg
    for p in parts[:-1]:
        if p not in target:
            target[p] = {}
        target = target[p]
    target[parts[-1]] = value
    return cfg


def get_value(cfg: dict, path: str):
    """通过点路径读取配置值"""
    parts = path.split(".")
    target = cfg
    for p in parts:
        if p not in target:
            return None
        target = target[p]
    return target


# ═══════════════════════════════════════════════════════
# 显示配置（可读格式）
# ═══════════════════════════════════════════════════════

def format_config(cfg: dict) -> str:
    """格式化为人类可读的配置摘要"""
    lines = []
    lines.append("=" * 56)
    lines.append(f"  测试配置 v{cfg.get('version', '?')}")
    lines.append("=" * 56)
    lines.append("")
    lines.append(f"  全局轮数:  {cfg.get('rounds', 3)} 轮")
    lines.append("")
    lines.append("  ── 修复模式 ──")
    fm = cfg.get("fix_mode", {})
    lines.append(f"    场景测试(S1-S3): {_fix_mode_text_scenario(fm.get('scenario', 0))}")
    lines.append(f"    功能测试(D1-D6): {_fix_mode_text_function(fm.get('function', 0))}")
    lines.append("")
    lines.append("  ── 场景测试 ──")
    for k in ["S1", "S2", "S3"]:
        v = cfg.get("scenarios", {}).get(k, {})
        icon = "✅" if v.get("enabled", True) else "❌"
        lines.append(f"    {icon} {k}")
    lines.append("")
    lines.append("  ── 功能测试 ──")
    for k in ["D1", "D2", "D3", "D4", "D5", "D6"]:
        v = cfg.get("functions", {}).get(k, {})
        icon = "✅" if v.get("enabled", True) else "❌"
        lines.append(f"    {icon} {k}")
    lines.append("")
    lines.append("  ── S4 执行忠实度测试（LLM编写用例）──")
    s4 = cfg.get("s4", {})
    s4_icon = "✅" if s4.get("enabled", False) else "❌"
    s4_rounds = s4.get("rounds", cfg.get("rounds", 3))
    s4_fm = s4.get("fix_mode", 1)
    factors = cfg.get("s4_weights", {"positive": 0.4, "negative": 0.6})
    s4_fm = s4.get("fix_mode", 1)
    fm_label = {0:"仅报告", 1:"尝试修复"}.get(s4_fm, "仅报告")
    lines.append(f"    {s4_icon} S4（{s4_rounds} 轮, {fm_label}, 权重正{factors['positive']}/反{factors['negative']}）")
    lines.append("")
    lines.append(f"  ⚡ 当前测试集: {', '.join(get_active_tests(cfg))}")
    lines.append("=" * 56)
    return "\n".join(lines)


def _fix_mode_text_scenario(mode: int) -> str:
    return {0: "仅报告", 1: "尝试修复"}.get(mode, "未知")


def _fix_mode_text_function(mode: int) -> str:
    return {0: "仅报告", 1: "直接修复", 2: "询问后修复"}.get(mode, "未知")


def _fix_mode_text_s4(mode: int) -> str:
    return {0: "仅报告", 1: "尝试修复"}.get(mode, "仅报告")


# ═══════════════════════════════════════════════════════
# 文字交互配置
# ═══════════════════════════════════════════════════════

INTERACTIVE_HELP = """
配置命令（对话中使用）：

  cfg show                      — 查看当前配置
  cfg rounds N                  — 设置全局轮数（1-5）
  cfg fix_mode scenario <0|1>   — 场景修复模式（0=仅报告 1=尝试修复）
  cfg fix_mode function <0|1|2> — 功能修复模式（0=仅报告 1=直接 2=询问）
  cfg s4 on/off                 — 开启/关闭 S4（LLM编写噪声方案）
  cfg s4 rounds N               — 设置 S4 独立轮数
  cfg s4 fix <0|1>              — S4 修复模式（0=仅报告 1=尝试修复）
  cfg <dim> on/off              — 开启/关闭某个维度（如 S1, D2 等）
  cfg reset                     — 重置为默认配置
  cfg server                    — 启动 HTML 配置界面（自动打开浏览器）

示例：
  cfg s4 on              → 开启 S4
  cfg rounds 5           → 全部测试跑 5 轮
  cfg fix_mode scenario 1 → S1-S3 开启尝试修复
  cfg D4 off             → 关闭 D4 噪音检测
"""


def interactive_edit(cfg: dict, cmd_args: list[str], skill_dir: str) -> dict:
    """处理对话中的配置修改命令"""
    if not cmd_args:
        print(INTERACTIVE_HELP)
        return cfg

    action = cmd_args[0]

    if action == "show":
        print(format_config(cfg))

    elif action == "rounds":
        if len(cmd_args) < 2 or not cmd_args[1].isdigit():
            print("用法: cfg rounds <1-5>")
            return cfg
        n = int(cmd_args[1])
        if n < 1 or n > 5:
            print("轮数必须在 1-5 之间")
            return cfg
        cfg["rounds"] = n
        save_config(skill_dir, cfg)
        print(f"[CFG] 全局轮数已设置为 {n} 轮")

    elif action == "fix_mode":
        if len(cmd_args) < 3 or not cmd_args[2].isdigit():
            print("用法: cfg fix_mode scenario <0|1>   或   cfg fix_mode function <0|1|2>")
            return cfg
        target = cmd_args[1]
        n = int(cmd_args[2])
        if target == "scenario":
            if n not in (0, 1):
                print("场景修复模式: 0=仅报告 1=尝试修复")
                return cfg
            cfg.setdefault("fix_mode", {})["scenario"] = n
            save_config(skill_dir, cfg)
            print(f"[CFG] 场景修复模式已设置为 {n} = {_fix_mode_text_scenario(n)}")
        elif target == "function":
            if n not in (0, 1, 2):
                print("功能修复模式: 0=仅报告 1=直接修复 2=询问后修复")
                return cfg
            cfg.setdefault("fix_mode", {})["function"] = n
            save_config(skill_dir, cfg)
            print(f"[CFG] 功能修复模式已设置为 {n} = {_fix_mode_text_function(n)}")
        else:
            print(f"未知修复目标: {target}（仅支持 scenario/function）")

    elif action == "s4":
        if len(cmd_args) < 2:
            print("用法: cfg s4 on/off 或 cfg s4 rounds <N>")
            return cfg
        sub = cmd_args[1]
        if sub == "on":
            cfg["s4"]["enabled"] = True
            save_config(skill_dir, cfg)
            print("[CFG] S4 已开启")
        elif sub == "off":
            cfg["s4"]["enabled"] = False
            save_config(skill_dir, cfg)
            print("[CFG] S4 已关闭")
        elif sub == "rounds" and len(cmd_args) >= 3:
            n = int(cmd_args[2])
            if 1 <= n <= 5:
                cfg["s4"]["rounds"] = n
                save_config(skill_dir, cfg)
                print(f"[CFG] S4 轮数已设置为 {n}")
        elif sub == "pf" and len(cmd_args) >= 3:
            v = float(cmd_args[2])
            if 0.0 <= v <= 1.0:
                cfg.setdefault("s4_weights", {})["positive"] = v
                if __import__("builtins").sum(cfg["s4_weights"].values()) > 0:
                    save_config(skill_dir, cfg)
                    print(f"[CFG] S4 正向因子已设置为 {v}")
        elif sub == "nf" and len(cmd_args) >= 3:
            v = float(cmd_args[2])
            if 0.0 <= v <= 1.0:
                cfg.setdefault("s4_weights", {})["negative"] = v
                save_config(skill_dir, cfg)
                print(f"[CFG] S4 反向因子已设置为 {v}")
        elif sub == "fix" and len(cmd_args) >= 3:
            n = int(cmd_args[2])
            if n in (0, 1):
                cfg.setdefault("s4", {})["fix_mode"] = n
                save_config(skill_dir, cfg)
                print(f"[CFG] S4 修复模式已设置为 {n} = {_fix_mode_text_s4(n)}")

    elif action in ("S1", "S2", "S3", "D1", "D2", "D3", "D4", "D5", "D6"):
        group = "scenarios" if action.startswith("S") else "functions"
        if len(cmd_args) < 2:
            print(f"用法: cfg {action} on/off")
            return cfg
        sub = cmd_args[1]
        if sub == "on":
            cfg[group][action]["enabled"] = True
            save_config(skill_dir, cfg)
            print(f"[CFG] {action} 已开启")
        elif sub == "off":
            cfg[group][action]["enabled"] = False
            save_config(skill_dir, cfg)
            print(f"[CFG] {action} 已关闭")

    elif action == "reset":
        cfg = _merge_defaults(DEFAULT_CONFIG)
        save_config(skill_dir, cfg)
        print("[CFG] 已重置为默认配置")

    elif action == "html" or action == "server":
        # 启动 HTTP 配置服务器
        print("[CFG] 启动配置服务器...")
        start_server(skill_dir)

    else:
        print(f"未知配置命令: {action}")
        print(INTERACTIVE_HELP)

    return cfg


# ═══════════════════════════════════════════════════════
# HTML 配置界面生成
# ═══════════════════════════════════════════════════════

def render_html(cfg: dict) -> str:
    """生成自包含 HTML 配置界面"""
    s4_enabled = "true" if cfg.get("s4", {}).get("enabled", True) else "false"
    s4_rounds = cfg.get("s4", {}).get("rounds", cfg.get("rounds", 3))
    rounds = cfg.get("rounds", 3)
    fm = cfg.get("fix_mode", {})
    scenario_fm = fm.get("scenario", 0)
    function_fm = fm.get("function", 0)
    s4_fm = cfg.get("s4", {}).get("fix_mode", 0)
    s4_fm_label = {0:"仅报告", 1:"尝试修复"}.get(s4_fm, "仅报告")

    # 构建各维度开关状态
    s_labels = {"S1": "场景触发测试（LLM编写用例）", "S2": "核心能力测试（LLM编写用例）", "S3": "工作流测试（LLM编写用例）"}
    scenarios_checks = ""
    for k in ["S1", "S2", "S3"]:
        enabled = cfg.get("scenarios", {}).get(k, {}).get("enabled", True)
        checked = "checked" if enabled else ""
        scenarios_checks += f"""
            <label class="toggle-row">
              <span>{k} {s_labels[k]}</span>
              <input type="checkbox" id="{k}" {checked} data-group="scenarios">
              <span class="slider"></span>
            </label>"""

    functions_checks = ""
    labels = {"D1": "基础功能完整性", "D2": "流程断点检测", "D3": "数据污染检测",
              "D4": "噪音/干扰检测", "D5": "计算正确性", "D6": "边界鲁棒性"}
    for k, label in labels.items():
        enabled = cfg.get("functions", {}).get(k, {}).get("enabled", True)
        checked = "checked" if enabled else ""
        functions_checks += f"""
            <label class="toggle-row">
              <span>{k} {label}</span>
              <input type="checkbox" id="{k}" {checked} data-group="functions">
              <span class="slider"></span>
            </label>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>skill-function-test 配置</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, #f5f3ff 0%, #e0f2fe 100%);
    min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px;
  }}
  .card {{
    background: white; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    padding: 32px; max-width: 520px; width: 100%;
  }}
  h1 {{ font-size: 20px; color: #1a1a2e; margin-bottom: 4px; }}
  .subtitle {{ font-size: 13px; color: #64748b; margin-bottom: 24px; }}
  .section {{ margin-bottom: 20px; }}
  .section-title {{ font-size: 14px; font-weight: 600; color: #334155; margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid #e2e8f0; }}
  .toggle-row {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 6px 0; font-size: 14px; color: #1e293b;
  }}
  .toggle-row span:first-child {{ flex: 1; }}
  .slider {{
    position: relative; width: 40px; height: 22px; background: #cbd5e1;
    border-radius: 11px; cursor: pointer; transition: background 0.3s;
    flex-shrink: 0;
  }}
  .slider::after {{
    content: ''; position: absolute; width: 18px; height: 18px;
    background: white; border-radius: 50%; top: 2px; left: 2px;
    transition: transform 0.3s; box-shadow: 0 1px 3px rgba(0,0,0,0.15);
  }}
  input:checked + .slider {{ background: #7c3aed; }}
  input:checked + .slider::after {{ transform: translateX(18px); }}
  input[type="checkbox"] {{ display: none; }}
  .param-row {{
    display: flex; align-items: center; justify-content: space-between;
    padding: 8px 0; font-size: 14px; color: #1e293b;
  }}
  .param-row input[type="number"],
  .param-row select {{
    width: 100px; padding: 6px 8px; border: 1px solid #cbd5e1; border-radius: 8px;
    font-size: 14px; text-align: center; outline: none;
  }}
  .param-row input[type="number"]:focus,
  .param-row select:focus {{ border-color: #7c3aed; }}
  .badge {{
    display: inline-block; font-size: 11px; padding: 2px 8px; border-radius: 10px;
    background: #f1f5f9; color: #64748b; margin-left: 6px;
  }}
  .btn-row {{ display: flex; gap: 10px; margin-top: 20px; }}
  .btn {{
    flex: 1; padding: 10px; border: none; border-radius: 10px;
    font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s;
  }}
  .btn-primary {{ background: #7c3aed; color: white; }}
  .btn-primary:hover {{ background: #6d28d9; }}
  .btn-secondary {{ background: #e2e8f0; color: #475569; }}
  .btn-secondary:hover {{ background: #cbd5e1; }}
  .btn-danger {{ background: #fee2e2; color: #dc2626; }}
  .btn-danger:hover {{ background: #fecaca; }}
  .toast {{
    position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%);
    background: #1a1a2e; color: white; padding: 10px 24px; border-radius: 8px;
    font-size: 14px; opacity: 0; transition: opacity 0.3s; pointer-events: none;
  }}
  .toast.show {{ opacity: 1; }}
</style>
</head>
<body>
<div class="card">
  <h1>⚙️ skill-function-test 配置</h1>
  <div class="subtitle">修改后点击「保存配置」直接写入磁盘</div>

  <div class="section">
    <div class="section-title">轮数</div>
    <div class="param-row">
      <span>场景/功能测试轮数 <span class="badge">S1-S3 / D1-D6</span></span>
      <input type="number" id="rounds" value="{rounds}" min="1">
    </div>
    <div class="param-row">
      <span>S4 独立轮数 <span class="badge">覆盖默认轮数</span></span>
      <input type="number" id="s4_rounds" value="{s4_rounds}" min="1">
    </div>
  </div>

  <div class="section">
    <div class="section-title">修复模式</div>
    <div class="param-row">
      <span>场景测试 <span class="badge">S1-S3</span></span>
      <select id="fix_scenario">
        <option value="0" {"selected" if scenario_fm==0 else ""}>0 - 仅报告</option>
        <option value="1" {"selected" if scenario_fm==1 else ""}>1 - 尝试修复</option>
      </select>
    </div>
    <div class="param-row">
      <span>功能测试 <span class="badge">D1-D6</span></span>
      <select id="fix_function">
        <option value="0" {"selected" if function_fm==0 else ""}>0 - 仅报告</option>
        <option value="1" {"selected" if function_fm==1 else ""}>1 - 直接修复</option>
      </select>
    </div>
  </div>

  <div class="section">
    <div class="section-title">场景测试</div>
    {scenarios_checks}
  </div>

  <div class="section">
    <div class="section-title">功能测试</div>
    {functions_checks}
  </div>

  <div class="section">
    <div class="section-title">S4 执行忠实度测试（LLM编写用例）</div>
    <label class="toggle-row">
      <span>S4 执行忠实度 <span class="badge">仅报告</span></span>
      <input type="checkbox" id="S4" {"checked" if s4_enabled=="true" else ""}>
      <span class="slider"></span>
    </label>
  </div>

    <div class="btn-row" id="save_btn_row">
    <button class="btn btn-secondary" onclick="resetUI()">重置为默认</button>
    <button class="btn btn-primary" onclick="saveAndDone()">保存配置</button>
  </div>
  <div class="btn-row" id="done_btn_row" style="display:none">
    <button class="btn btn-primary" onclick="finishSetup()" style="background:#059669;">✅ 完成配置</button>
  </div>
</div>
<div class="toast" id="toast"></div>
<script>
function showMsg(msg) {{
  const t = document.getElementById('toast');
  t.textContent = msg; t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}}

function collectConfig() {{
  return {{
    version: "0.1.0",
    rounds: parseInt(document.getElementById('rounds').value) || 3,
    fix_mode: {{
      scenario: parseInt(document.getElementById('fix_scenario').value) || 0,
      function: parseInt(document.getElementById('fix_function').value) || 0,
    }},
    s4: {{
      enabled: document.getElementById('S4').checked,
      rounds: parseInt(document.getElementById('s4_rounds').value) || 3,
      fix_mode: 0,
    }},
    scenarios: {{
      S1: {{ enabled: document.getElementById('S1').checked }},
      S2: {{ enabled: document.getElementById('S2').checked }},
      S3: {{ enabled: document.getElementById('S3').checked }},
    }},
    functions: {{
      D1: {{ enabled: document.getElementById('D1').checked }},
      D2: {{ enabled: document.getElementById('D2').checked }},
      D3: {{ enabled: document.getElementById('D3').checked }},
      D4: {{ enabled: document.getElementById('D4').checked }},
      D5: {{ enabled: document.getElementById('D5').checked }},
      D6: {{ enabled: document.getElementById('D6').checked }},
    }},
  }};
}}

function saveAndDone() {{
  const cfg = collectConfig();
  const text = JSON.stringify(cfg, null, 2);
  localStorage.setItem('test_config', text);

  fetch('/save', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: text,
  }})
  .then(function(r) {{ return r.json(); }})
  .then(function(data) {{
    if (data.ok) {{
      showMsg('✅ 配置已保存，点击「完成配置」关闭服务器');
      document.getElementById('save_btn_row').style.display = 'none';
      document.getElementById('done_btn_row').style.display = 'flex';
    }} else {{
      showMsg('❌ 保存失败: ' + (data.error || '未知错误'));
    }}
  }})
  .catch(function() {{
    showMsg('⚠️ 服务器未响应');
  }});
}}

function finishSetup() {{
  fetch('/done')
  .then(function(r) {{ return r.json(); }})
  .then(function(data) {{
    if (data.ok) {{
      showMsg('✅ 配置已完成，可关闭此页面');
      document.getElementById('done_btn_row').style.display = 'none';
    }}
  }})
  .catch(function() {{
    showMsg('⚠️ 服务器未响应');
  }});
}}

function setUI(cfg) {{
  document.getElementById('rounds').value = cfg.rounds || {rounds};
  document.getElementById('s4_rounds').value = (cfg.s4 && cfg.s4.rounds) || {s4_rounds};
  document.getElementById('fix_scenario').value = (cfg.fix_mode && cfg.fix_mode.scenario) || 0;
  document.getElementById('fix_function').value = (cfg.fix_mode && cfg.fix_mode.function) || 0;
  document.getElementById('S4').checked = cfg.s4 ? cfg.s4.enabled : true;
  ['S1','S2','S3','D1','D2','D3','D4','D5','D6'].forEach(function(id) {{
    var group = id.startsWith('S') ? 'scenarios' : 'functions';
    document.getElementById(id).checked = cfg[group] ? (cfg[group][id] ? cfg[group][id].enabled !== false : true) : true;
  }});
}}

function resetUI() {{
  var def = {{
    version: "0.1.0",
    rounds: {rounds},
    fix_mode: {{ scenario: 0, function: 0 }},
    s4: {{ enabled: true, rounds: {s4_rounds} }},
    scenarios: {{ S1:{{enabled:true}}, S2:{{enabled:true}}, S3:{{enabled:true}} }},
    functions: {{ D1:{{enabled:true}}, D2:{{enabled:true}}, D3:{{enabled:true}}, D4:{{enabled:true}}, D5:{{enabled:true}}, D6:{{enabled:true}} }},
  }};
  setUI(def);
  showMsg('🔄 UI 已重置为默认，点击「保存配置」生效');
}}
</script>
</body>
</html>"""
    return html


# ═══════════════════════════════════════════════════════
# HTTP 配置服务器（供 HTML 界面直接写盘）
# ═══════════════════════════════════════════════════════

import http.server
import threading
import webbrowser
from datetime import datetime
from pathlib import Path


class ConfigHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP 请求处理器 — 支持 GET /config, POST /save, GET /done"""

    skill_dir = ""  # 由 start_server 注入
    html_path = ""  # HTML 文件路径

    def do_GET(self):
        if self.path == "/":
            self._serve_html()
        elif self.path == "/config":
            self._send_json(load_config(self.skill_dir))
        elif self.path == "/done":
            self._handle_done()
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/save":
            self._handle_save()
        else:
            self.send_error(404)

    def _serve_html(self):
        if os.path.exists(self.html_path):
            with open(self.html_path, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, f"HTML not found: {self.html_path}")

    def _send_json(self, data: dict):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-cache, no-store")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _handle_save(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            self._send_json({"ok": False, "error": "空请求体"})
            return
        raw = self.rfile.read(content_length)
        try:
            new_cfg = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as e:
            self._send_json({"ok": False, "error": f"JSON 解析失败: {e}"})
            return

        # 立即返回成功
        self._send_json({"ok": True, "data": new_cfg})

        # 后台线程写入磁盘
        threading.Thread(target=self._do_save, args=(new_cfg,), daemon=True).start()

    def _do_save(self, cfg: dict):
        cfg["_updated_at"] = datetime.now().isoformat()
        save_config(self.skill_dir, cfg)

    def _handle_done(self):
        self._send_json({"ok": True, "closed": True})
        # 创建标志文件，通知主线程关闭服务器
        try:
            flag = os.path.join(self.skill_dir, ".settings_done")
            with open(flag, "w") as f:
                f.write("done")
        except Exception:
            pass

    def log_message(self, format, *args):
        pass  # 安静模式，不打印 HTTP 日志


def find_available_port(start=8080, end=8999):
    """扫描可用端口"""
    for port in range(start, end + 1):
        try:
            s = http.server.HTTPServer(("localhost", port), ConfigHandler)
            s.server_close()
            return port
        except OSError:
            continue
    return None


def start_server(skill_dir: str):
    """启动 HTTP 配置服务器（自动重试端口）"""
    # 兼容两种调用模式
    try:
        from test_config import render_html
    except ModuleNotFoundError:
        from scripts.test_config import render_html

    # 总是用最新配置重新生成 HTML（现有 HTML 是静态快照，不和最新配置同步）
    html_file = os.path.join(os.path.dirname(__file__), "test_config.html")
    cfg = load_config(skill_dir)
    html_content = render_html(cfg)
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    # 注入路径到 handler
    ConfigHandler.skill_dir = skill_dir
    ConfigHandler.html_path = html_file

    # 尝试绑定端口（重试机制，避免竞争条件）
    server = None
    for attempt in range(10):
        port = find_available_port(8080 + attempt, 8080 + attempt)
        if port is None:
            continue
        try:
            server = http.server.HTTPServer(("localhost", port), ConfigHandler)
            break
        except OSError:
            continue

    if server is None:
        print("\n[CFG] ❌ 无法绑定端口（8080-8089 均不可用）")
        return

    url = f"http://localhost:{port}/"

    print(f"\n[CFG] 🌐 配置服务器已启动: {url}")
    print(f"[CFG] 按 Ctrl+C 关闭服务器")
    print(f"[CFG] ⚡ 保存即写盘，无需手动操作")
    import sys as _sys; _sys.stdout.flush()

    # 自动打开浏览器
    threading.Thread(target=lambda: webbrowser.open(url), daemon=True).start()

    # 轮询 .settings_done 标志文件，用户点击"完成"后关闭服务器
    done_flag = os.path.join(skill_dir, ".settings_done")
    try:
        while True:
            server.handle_request()
            if os.path.exists(done_flag):
                break
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        if os.path.exists(done_flag):
            os.remove(done_flag)
        print("\n[CFG] 服务器已关闭")


# ═══════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python test_config.py <skill-dir> show           — 查看配置")
        print("  python test_config.py <skill-dir> set <path> <val>  — 设置值")
        print("  python test_config.py <skill-dir> reset          — 重置")
        print("  python test_config.py <skill-dir> server         — 启动配置服务器(HTML)")
        print("  python test_config.py <skill-dir> interactive    — 文字交互模式")
        return

    skill_dir = sys.argv[1]
    if len(sys.argv) < 3:
        print(format_config(load_config(skill_dir)))
        return

    cmd = sys.argv[2]
    cfg = load_config(skill_dir)

    if cmd == "show":
        print(format_config(cfg))

    elif cmd == "set":
        if len(sys.argv) < 5:
            print("用法: set <path> <value> 例: set s4.enabled true")
            return
        path = sys.argv[3]
        val = sys.argv[4]
        # 类型推断
        if val.lower() in ("true", "false"):
            val = val.lower() == "true"
        elif val.isdigit():
            val = int(val)
        set_value(cfg, path, val)
        save_config(skill_dir, cfg)

    elif cmd == "reset":
        cfg = _merge_defaults(DEFAULT_CONFIG)
        save_config(skill_dir, cfg)

    elif cmd in ("html", "server"):
        start_server(skill_dir)

    elif cmd == "interactive":
        print("配置交互模式（输入 'q' 退出）:")
        print(format_config(cfg))
        while True:
            try:
                inp = input("\ncfg> ").strip()
                if not inp or inp == "q":
                    break
                parts = inp.split()
                cfg = interactive_edit(cfg, parts, skill_dir)
            except (EOFError, KeyboardInterrupt):
                break

    else:
        print(f"未知命令: {cmd}")


if __name__ == "__main__":
    main()
