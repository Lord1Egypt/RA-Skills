#!/usr/bin/env python3
"""
clone.py - 一键分身脚本 v1.0
功能：在同一环境下复制整个团队（避免 ID/路径冲突）

用法：
    python3 clone.py                    # 交互式
    python3 clone.py --suffix "测试"    # 指定后缀

流程：
    1. 检测当前团队
    2. 询问分身后缀
    3. 备份配置
    4. 复制所有 workspace（加后缀）
    5. 复制所有 agentDir（加后缀）
    6. 重命名所有 agent ID（加后缀）
    7. 追加到 openclaw.json（不覆盖）
    8. 重启 Gateway
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# =============================================
# 颜色输出
# =============================================
GREEN  = '\033[0;32m'
RED    = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE   = '\033[0;34m'
NC     = '\033[0m'

def log(msg):   print(f"{GREEN}[✓]{NC} {msg}")
def err(msg):   print(f"{RED}[✗]{NC} {msg}")
def warn(msg):  print(f"{YELLOW}[!]{NC} {msg}")
def info(msg):  print(f"{BLUE}[i]{NC} {msg}")

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

# =============================================
# 路径常量
# =============================================

QCLAW_DIR      = Path.home() / ".qclaw"
OPENCLAW_JSON  = QCLAW_DIR / "openclaw.json"
BACKUP_DIR     = QCLAW_DIR / "backup"

# =============================================
# 备份
# =============================================

def backup_config():
    """备份 openclaw.json"""
    if not OPENCLAW_JSON.exists():
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"clone备份_{timestamp}" / "openclaw.json"
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OPENCLAW_JSON, backup_path)
    log(f"配置已备份到 {backup_path.parent}")
    return backup_path.parent

# =============================================
# 团队检测
# =============================================

def detect_team():
    """检测当前团队结构，返回 main + members + config"""
    if not OPENCLAW_JSON.exists():
        err("未找到 openclaw.json")
        sys.exit(1)

    with open(OPENCLAW_JSON, "r", encoding="utf-8") as f:
        config = json.load(f)

    agents_list = config.get("agents", {}).get("list", [])

    main_agent = None
    team_members = []

    for agent in agents_list:
        aid = agent.get("id", "")
        if aid == "main":
            main_agent = agent
        elif agent.get("workspace"):
            team_members.append(agent)

    # fallback: 通过 workspace 特征找 main
    if not main_agent:
        for agent in agents_list:
            ws = agent.get("workspace", "")
            if ws and Path(ws).exists():
                p = Path(ws)
                if (p / "SOUL.md").exists() and (p / "MEMORY.md").exists():
                    main_agent = agent
                    break

    if not main_agent:
        err("未检测到 main agent")
        sys.exit(1)

    return {
        "main": main_agent,
        "members": team_members,
        "config": config,
    }

# =============================================
# 复制 & 重命名
# =============================================

def rename_id(original_id: str, suffix: str) -> str:
    """给 agent ID 加后缀，避免重复"""
    if original_id.endswith(f"-{suffix}"):
        return original_id
    return f"{original_id}-{suffix}"


def rename_workspace_path(original_path: str, suffix: str) -> str:
    """给 workspace 路径加后缀"""
    p = Path(original_path)
    return str(p.parent / f"{p.name}-{suffix}")


def rename_agentdir_path(original_path: str, suffix: str) -> str:
    """给 agentDir 路径加后缀"""
    p = Path(original_path)
    return str(p.parent / f"{p.name}-{suffix}")


def safe_copytree(src: Path, dst: Path, label: str = ""):
    """安全复制目录，目标已存在则跳过"""
    if dst.exists():
        warn(f"  目标已存在，跳过：{dst.name}")
        return False
    shutil.copytree(src, dst)
    log(f"  复制 {label or src.name} → {dst.name}")
    return True


def patch_agents_md(workspace: Path, suffix: str):
    """
    更新 AGENTS.md 中引用的 agent ID，给所有成员 ID 加后缀。
    简单正则替换，不破坏格式。
    """
    agents_md = workspace / "AGENTS.md"
    if not agents_md.exists():
        return

    import re
    content = agents_md.read_text(encoding="utf-8")

    # 替换 agent-xxxx 格式的 ID
    def _replace(m):
        aid = m.group(0)
        if aid.endswith(f"-{suffix}"):
            return aid
        return f"{aid}-{suffix}"

    new_content = re.sub(r"agent-[a-f0-9]+", _replace, content)

    if new_content != content:
        agents_md.write_text(new_content, encoding="utf-8")
        log(f"  更新 {agents_md.name}（agent ID 已加后缀）")

# =============================================
# 配置合并
# =============================================

def deep_merge(base, patch):
    """深度合并 dict"""
    result = base.copy()
    for k, v in patch.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def merge_agents_config(original_config: dict, new_agents: list, suffix: str) -> dict:
    """
    把分身后的 agent 追加到 openclaw.json。
    只追加，不覆盖原有。
    """
    config = json.loads(json.dumps(original_config))  # deep copy

    if "agents" not in config:
        config["agents"] = {}
    if "list" not in config["agents"]:
        config["agents"]["list"] = []

    existing_ids = {a.get("id") for a in config["agents"]["list"]}

    for agent in new_agents:
        if agent["id"] in existing_ids:
            warn(f"  agent 已存在，跳过: {agent['id']}")
            continue
        config["agents"]["list"].append(agent)
        log(f"  追加 agent: {agent['id']} ({agent.get('name', 'N/A')})")

    # 确保 allowAgents（最小白名单，不用通配符）
    all_ids = [a["id"] for a in config["agents"]["list"] if a.get("id") != "main"]
    if "defaults" not in config["agents"]:
        config["agents"]["defaults"] = {}
    if "subagents" not in config["agents"]["defaults"]:
        config["agents"]["defaults"]["subagents"] = {}
    existing_allow = config["agents"]["defaults"]["subagents"].get("allowAgents", [])
    if existing_allow != ["*"]:
        # 合并白名单，不用通配符
        config["agents"]["defaults"]["subagents"]["allowAgents"] = sorted(set(existing_allow + all_ids))
    # 如果已有通配符，保留用户原有设置

    # hooks.allowedAgentIds 追加
    new_member_ids = [a["id"] for a in new_agents if a["id"] != "main"]
    if new_member_ids:
        if "hooks" not in config:
            config["hooks"] = {}
        existing_hook_ids = set(config.get("hooks", {}).get("allowedAgentIds", []))
        config["hooks"]["allowedAgentIds"] = sorted(existing_hook_ids | set(new_member_ids))

    return config

# =============================================
# Gateway 重启
# =============================================

def restart_gateway():
    """重启 Gateway（用户已通过确认流程）"""
    info("重启 Gateway...")
    print()
    warn("⚠️ 重启将中断当前所有会话和正在运行的任务")
    output, code = run_cmd("openclaw gateway restart")
    if code == 0:
        log("  Gateway 已重启")
        info("  等待 5 秒让 channel 注册...")
        import time
        time.sleep(5)
    else:
        warn("  Gateway 重启可能失败")
        warn("  请手动执行：openclaw gateway restart")
    return True

# =============================================
# 主流程
# =============================================

def main():

    print()
    print("=" * 60)
    print("  一键分身 - Team Clone v1.0")
    print("=" * 60)
    print()

    # ---- Step 1: 检测团队 ----
    info("检测当前团队...")
    team = detect_team()

    main_agent = team["main"]
    members    = team["members"]

    main_name = main_agent.get("name", main_agent.get("id", "Unknown"))
    main_ws   = main_agent.get("workspace", "N/A")

    log(f"Main Agent: {main_name}")
    log(f"Workspace:  {main_ws}")
    log(f"团队成员:   {len(members)} 人")
    for m in members:
        log(f"  - {m.get('name', m.get('id'))} ({m.get('id')})")
    print()

    # ---- Step 2: 询问后缀 ----
    suffix = "copy"
    if "--suffix" in sys.argv:
        idx = sys.argv.index("--suffix")
        if idx + 1 < len(sys.argv):
            suffix = sys.argv[idx + 1]
    else:
        user_input = input("请输入分身后缀（默认 copy，回车使用默认）: ").strip()
        if user_input:
            suffix = user_input

    log(f"分身后缀: {suffix}")
    print()

    # ---- 预检：新路径是否冲突 ----
    new_main_ws = rename_workspace_path(main_agent.get("workspace", ""), suffix)
    if new_main_ws and Path(new_main_ws).exists():
        err(f"目标 workspace 已存在：{new_main_ws}")
        err("请更换后缀或手动删除后再试")
        return

    # ---- Step 2.5: 操作确认 ----
    print("─" * 40)
    print()
    print("即将执行以下操作：")
    print(f"  · 复制 {1 + len(members)} 个 workspace（加后缀 -{suffix}）")
    print(f"  · 追加 {1 + len(members)} 个 agent 到 openclaw.json")
    print(f"  · allowAgents 白名单将更新为包含新成员 ID")
    print(f"  · 自动重启 Gateway（将中断当前会话）")
    print()
    warn("⚠️ 确认后将自动执行以上所有操作")
    print()
    
    confirm = input("确认继续？（y/n）：").strip().lower()
    if confirm != 'y':
        err("用户取消，分身中止")
        return
    print()
    log("用户已确认，开始执行...")
    print()

    # ---- Step 3: 备份 ----
    backup_config()
    print()

    # ---- Step 4: 复制 workspace & agentDir ----
    new_agents = []

    # 4.1 Main Agent
    info("复制 Main Agent...")
    old_main_ws = Path(main_agent["workspace"])
    new_main_ws_path = Path(new_main_ws)
    safe_copytree(old_main_ws, new_main_ws_path, main_name)
    patch_agents_md(new_main_ws_path, suffix)

    new_main_agent = {
        "id":   rename_id(main_agent.get("id", "main"), suffix),
        "name": f"{main_agent.get('name', 'Main')}-{suffix}",
        "workspace": new_main_ws,
    }

    # agentDir
    if main_agent.get("agentDir"):
        old_dir = Path(main_agent["agentDir"])
        new_dir_path = rename_agentdir_path(main_agent["agentDir"], suffix)
        if old_dir.exists():
            safe_copytree(old_dir, Path(new_dir_path), "agentDir")
        new_main_agent["agentDir"] = new_dir_path

    new_agents.append(new_main_agent)
    print()

    # 4.2 团队成员
    if members:
        info(f"复制 {len(members)} 个团队成员...")
        for member in members:
            old_ws = Path(member["workspace"])
            if not old_ws.exists():
                warn(f"  workspace 不存在，跳过: {old_ws}")
                continue

            new_ws_path = rename_workspace_path(member["workspace"], suffix)
            safe_copytree(old_ws, Path(new_ws_path), member.get("name", ""))
            patch_agents_md(Path(new_ws_path), suffix)

            new_member = {
                "id":   rename_id(member.get("id", ""), suffix),
                "name": f"{member.get('name', '')}-{suffix}",
                "workspace": new_ws_path,
            }

            if member.get("agentDir"):
                old_dir = Path(member["agentDir"])
                new_dir_path = rename_agentdir_path(member["agentDir"], suffix)
                if old_dir.exists():
                    safe_copytree(old_dir, Path(new_dir_path))
                new_member["agentDir"] = new_dir_path

            new_agents.append(new_member)
            log(f"  {member.get('name')} → {new_member['name']} ({new_member['id']})")
        print()

    # ---- Step 5: 合并配置 ----
    info("合并配置到 openclaw.json...")
    new_config = merge_agents_config(team["config"], new_agents, suffix)

    with open(OPENCLAW_JSON, "w", encoding="utf-8") as f:
        json.dump(new_config, f, indent=2, ensure_ascii=False)

    log(f"openclaw.json 已更新")
    print()

    # ---- Step 6: 提醒重启 Gateway ----
    restart_gateway()
    print()

    # ---- 完成报告 ----
    print("=" * 60)
    print("  ✅ 分身完成！")
    print("=" * 60)
    print()
    print(f"新团队信息:")
    for a in new_agents:
        role = "Main" if a == new_agents[0] else "成员"
        print(f"  [{role}] {a.get('name')} (id={a['id']})")
        print(f"         workspace: {a.get('workspace')}")
        if a.get("agentDir"):
            print(f"         agentDir:  {a['agentDir']}")
    print()
    print("📋 验证步骤:")
    print("  1. openclaw gateway status")
    print("  2. 测试 spawn 分身 agent（用新的 ID）")
    print("  3. 如需回滚：cp -r ~/.qclaw/backup/clone备份_xxx/openclaw.json ~/.qclaw/openclaw.json")
    print()


if __name__ == "__main__":
    import sys
    main()
