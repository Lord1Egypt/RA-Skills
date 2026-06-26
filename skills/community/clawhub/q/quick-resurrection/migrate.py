#!/usr/bin/env python3
"""
一键搬家执行脚本 v2.2（审查确认后全自动执行）
功能：检测环境 → 备份 → 合并配置 → 复制文件 → 完成搬家

v3.0 变更：
- 新增 --dry-run / --no-cron / --no-restart 细粒度控制
- merge_config 写入前展示 openclaw.json 的 diff（before → after）
- agents.list 按 agent.id 追加/更新，不整体替换
- 审查步骤移到修改配置之前
- copy_team_members 使用配置中的实际 workspace 路径
- Zip Slip 路径穿越防御
"""

import os
import sys
import json
import shutil
import subprocess
import time
import zipfile
import argparse
import difflib
from datetime import datetime
from pathlib import Path

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
    """执行命令，返回 (stdout, returncode)。仅用于只读操作。"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

# =============================================
# 备份模块
# =============================================

BACKUP_DIR = Path.home() / ".qclaw" / "backup"

def backup_existing():
    """
    搬家前备份现有配置到 ~/.qclaw/backup/
    每次搬家创建带时间戳的子目录
    """
    info("检查是否需要备份...")
    
    targets = []
    qclaw_base = Path.home() / ".qclaw"
    
    if not qclaw_base.exists():
        info("  ~/.qclaw/ 不存在，无需备份")
        return
    
    # 检查 workspace
    for d in qclaw_base.iterdir():
        if d.is_dir() and d.name.startswith("workspace-"):
            targets.append(d)
    
    # 检查 openclaw.json
    config = Path.home() / ".qclaw" / "openclaw.json"
    if config.exists():
        targets.append(config)
    
    if not targets:
        info("  未检测到现有配置，无需备份")
        return
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_sub = BACKUP_DIR / f"搬家备份_{timestamp}"
    backup_sub.mkdir(parents=True, exist_ok=True)
    
    info(f"  备份现有配置到：{backup_sub}")
    count = 0
    for t in targets:
        try:
            dst = backup_sub / t.name
            shutil.copytree(t, dst, dirs_exist_ok=True)
            count += 1
        except Exception as e:
            warn(f"  备份失败 {t.name}：{e}")
    
    log(f"  已备份 {count} 项")

# =============================================
# 配置合并模块
# =============================================

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def deep_merge(base, patch):
    """
    深度合并两个 dict。
    - patch 中有而 base 中无的键：直接添加
    - 两者都有且都是 dict：递归合并
    - 两者都有但类型不同：patch 覆盖 base
    """
    result = base.copy()
    for k, v in patch.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result

def merge_config(package_dir):
    """
    将搬家包中的 agents 配置与现有 openclaw.json 深度合并。
    只合并 agents 和 hooks 相关字段，保留其他所有配置。
    """
    info("合并 agent 配置（保护新环境原有配置）...")
    
    agents_file = package_dir / "openclaw-agents.json"
    if not agents_file.exists():
        warn("  找不到 openclaw-agents.json，跳过配置更新")
        return True
    
    agents_patch = load_json(agents_file)
    
    config_path = Path.home() / ".qclaw" / "openclaw.json"
    
    if config_path.exists():
        existing = load_json(config_path)
        info(f"  现有配置 keys：{list(existing.keys())}")
    else:
        existing = {}
        warn("  openclaw.json 不存在，将从零创建")
    
    # 深度合并 agents 和 hooks
    merged = existing.copy()
    
    if 'agents' in agents_patch:
        if 'agents' not in merged:
            merged['agents'] = {}
        
        # agents.defaults: deep merge（保留现有模型等配置）
        if 'defaults' in agents_patch['agents']:
            if 'defaults' not in merged['agents']:
                merged['agents']['defaults'] = {}
            merged['agents']['defaults'] = deep_merge(
                merged['agents']['defaults'], agents_patch['agents']['defaults'])
        
        # agents.list: 按 agent.id 追加/更新，不整体替换（保护新环境其他 agent）
        if 'list' in agents_patch['agents']:
            if 'list' not in merged['agents']:
                merged['agents']['list'] = []
            existing_ids = {a.get('id') for a in merged['agents']['list']}
            for agent in agents_patch['agents']['list']:
                aid = agent.get('id')
                if aid in existing_ids:
                    # 更新现有 agent（替换整个条目）
                    merged['agents']['list'] = [
                        agent if a.get('id') == aid else a
                        for a in merged['agents']['list']
                    ]
                else:
                    # 追加新 agent
                    merged['agents']['list'].append(agent)
            added = len(agents_patch['agents']['list'])
            log(f"  agents.list: 追加/更新 {added} 个 agent（保留现有 {len(existing_ids)} 个）")
        
        # allowAgents: 如果搬家包含 ["*"]，转换为最小白名单（仅实际成员ID）
        defaults = merged.get('agents', {}).get('defaults', {})
        subagents = defaults.get('subagents', {})
        if subagents.get('allowAgents') == ["*"]:
            all_agent_ids = [a.get('id') for a in merged.get('agents', {}).get('list', [])
                             if a.get('id') and a.get('id') != 'main']
            subagents['allowAgents'] = all_agent_ids
            log(f'  allowAgents 已转为最小白名单（{len(all_agent_ids)} 个成员ID）')
        
        log("  agents 配置已合并")
    
    if 'hooks' in agents_patch:
        if 'hooks' not in merged:
            merged['hooks'] = {}
        # hooks.allowedAgentIds 需要合并（追加而非覆盖）
        existing_ids = set(merged['hooks'].get('allowedAgentIds', []))
        patch_ids = set(agents_patch['hooks'].get('allowedAgentIds', []))
        merged['hooks']['allowedAgentIds'] = list(existing_ids | patch_ids)
        log("  hooks 配置已合并")
    
    # 展示 diff（before → after）
    if config_path.exists():
        existing_text = json.dumps(existing, indent=2, ensure_ascii=False).splitlines(keepends=True)
        merged_text = json.dumps(merged, indent=2, ensure_ascii=False).splitlines(keepends=True)
        diff = list(difflib.unified_diff(existing_text, merged_text,
                                          fromfile="现有 openclaw.json", tofile="合并后",
                                          n=3))
        if diff:
            info("  openclaw.json 变更 diff：")
            for line in diff[:60]:
                line = line.rstrip("\n")
                if line.startswith("+") and not line.startswith("+++"):
                    print(f"    {GREEN}{line}{NC}")
                elif line.startswith("-") and not line.startswith("---"):
                    print(f"    {RED}{line}{NC}")
                elif line.startswith("@@"):
                    print(f"    {YELLOW}{line}{NC}")
                else:
                    print(f"    {line}")
            if len(diff) > 60:
                info(f"    ...（共 {len(diff)} 行 diff，已截断）")
        else:
            info("  openclaw.json 无变更")
    else:
        info("  将创建新的 openclaw.json")

    # 写回
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, indent=2, ensure_ascii=False)
    
    log(f"  openclaw.json 已更新（合并后）")
    return True

# =============================================
# 主流程步骤
# =============================================

def find_package_dir():
    """
    找到搬家包目录。
    优先顺序：
    1. 命令行参数传入（zip 路径或目录路径）
    2. 当前目录本身就是包目录（解压后直接 cd 进去）
    3. 当前目录下有 搬家包_* 目录
    4. 当前目录下有 *.zip
    """
    # 检查命令行参数
    if len(sys.argv) > 1:
        arg = Path(sys.argv[1])
        if arg.is_file() and arg.suffix == '.zip':
            extract_dir = arg.with_suffix("")
            if not extract_dir.exists():
                info(f"  解压：{arg.name}")
                with zipfile.ZipFile(arg, 'r') as zip_ref:
                    # 防御 Zip Slip：检查解压路径不超出目标目录
                    for member in zip_ref.namelist():
                        member_path = (arg.parent / member).resolve()
                        if not str(member_path).startswith(str(arg.parent.resolve())):
                            err(f"  安全警告：zip 包含路径穿越文件 {member}，中止解压")
                            return None
                    zip_ref.extractall(arg.parent)
            if (extract_dir / "身份层").exists():
                return extract_dir
        elif arg.is_dir() and (arg / "身份层").exists():
            return arg

    # 如果目录里有人身份层，说明当前就在包目录里
    if Path("身份层").exists():
        return Path.cwd()
    
    # 找搬家包_* 子目录
    for d in Path.cwd().iterdir():
        if d.is_dir() and d.name.startswith("搬家包_") and (d / "身份层").exists():
            return d
    
    # 找 zip 文件并解压
    zips = list(Path.cwd().glob("*.zip")) + list(Path.cwd().glob("搬家*.zip"))
    for zf in zips:
        info(f"  发现搬家包：{zf.name}")
        extract_dir = zf.with_suffix("")  # 去掉 .zip
        if extract_dir.exists():
            warn(f"  解压目录已存在，跳过解压")
        else:
            info(f"  解压到：{extract_dir}")
            with zipfile.ZipFile(zf, 'r') as zip_ref:
                # 防御 Zip Slip
                for member in zip_ref.namelist():
                    member_path = (Path.cwd() / member).resolve()
                    if not str(member_path).startswith(str(Path.cwd().resolve())):
                        err(f"  安全警告：zip 包含路径穿越文件 {member}，跳过此包")
                        continue
                zip_ref.extractall(Path.cwd())
        if (extract_dir / "身份层").exists():
            return extract_dir
    
    return None

def copy_identity_files(package_dir):
    """复制身份文件（backup 已在前面做过）"""
    info("复制身份文件...")
    
    identity_dir = package_dir / "身份层"
    if not identity_dir.exists():
        err("  找不到身份层目录")
        return False
    
    workspace = Path.home() / ".qclaw"
    workspace.mkdir(parents=True, exist_ok=True)
    
    # 找到 main agent workspace（从 agents 配置中读）
    config_path = workspace / "openclaw.json"
    main_ws = None
    
    if config_path.exists():
        config = load_json(config_path)
        for agent in config.get('agents', {}).get('list', []):
            if agent.get('id') == 'main':
                main_ws = agent.get('workspace', '')
                break
    
    # fallback：找 workspace-agent-* 目录
    if not main_ws:
        candidates = [d for d in workspace.iterdir()
                      if d.is_dir() and d.name.startswith("workspace-")]
        if candidates:
            # 直接取第一个候选 workspace（由 openclaw.json 的 main agent 配置决定）
            main_ws = str(candidates[0])
    
    if not main_ws:
        # 最后一个 fallback
        main_ws = str(workspace / "workspace-main")
    
    ws_path = Path(main_ws)
    ws_path.mkdir(parents=True, exist_ok=True)
    
    copied = 0
    for fname in ["SOUL.md", "MEMORY.md", "TOOLS.md", "AGENTS.md", "IDENTITY.md", "USER.md"]:
        src = identity_dir / fname
        if src.exists():
            shutil.copy2(src, ws_path / fname)
            copied += 1
    
    memory_src = identity_dir / "memory"
    if memory_src.exists():
        memory_dst = ws_path / "memory"
        memory_dst.mkdir(parents=True, exist_ok=True)
        for f in memory_src.glob("*.md"):
            shutil.copy2(f, memory_dst / f.name)
        copied += 1
    
    log(f"  已复制 {copied} 项到 {ws_path.name}/")
    return True

def copy_team_members(package_dir):
    """复制团队成员（自动检测）"""
    info("检查团队成员...")
    
    team_dir = package_dir / "团队成员层"
    if not team_dir.exists():
        info("  未检测到团队成员，跳过")
        return True
    
    workspace_base = Path.home() / ".qclaw"
    
    # 找到 main workspace 父目录
    main_ws = None
    config_path = workspace_base / "openclaw.json"
    if config_path.exists():
        config = load_json(config_path)
        for agent in config.get('agents', {}).get('list', []):
            if agent.get('id') == 'main':
                main_ws = agent.get('workspace', '')
                break
    
    if not main_ws:
        candidates = [d for d in workspace_base.iterdir()
                      if d.is_dir() and d.name.startswith("workspace-")]
        if candidates:
            main_ws = str(candidates[0])
    
    if not main_ws:
        info("  未找到 main workspace，跳过")
        return True
    
    main_ws_path = Path(main_ws)
    
    # 读 openclaw-agents.json 获取每个成员的实际 workspace 路径
    agents_file = package_dir / "openclaw-agents.json"
    member_workspaces = {}
    if agents_file.exists():
        try:
            agents_data = load_json(agents_file)
            for a in agents_data.get('agents', {}).get('list', []):
                if a.get('id') != 'main' and a.get('workspace'):
                    member_workspaces[a.get('name', a.get('id'))] = a['workspace']
        except:
            pass
    
    count = 0
    for member_dir in team_dir.iterdir():
        if member_dir.is_dir():
            # 优先使用 openclaw-agents.json 中配置的 workspace 路径
            member_name = member_dir.name
            if member_name in member_workspaces:
                dst = Path(member_workspaces[member_name])
            else:
                dst = main_ws_path / member_name
            dst.mkdir(parents=True, exist_ok=True)
            for fname in ["SOUL.md", "MEMORY.md", "TOOLS.md"]:
                src = member_dir / fname
                if src.exists():
                    shutil.copy2(src, dst / fname)
            count += 1
    
    log(f"  已复制 {count} 个团队成员")
    return True

def copy_skills(package_dir):
    """复制 skills"""
    info("复制 skills...")
    
    skills_src = package_dir / "skills"
    if not skills_src.exists():
        warn("  未检测到 skills")
        return True
    
    workspace_base = Path.home() / ".qclaw"
    
    # 找 main workspace
    main_ws = None
    config_path = workspace_base / "openclaw.json"
    if config_path.exists():
        config = load_json(config_path)
        for agent in config.get('agents', {}).get('list', []):
            if agent.get('id') == 'main':
                main_ws = agent.get('workspace', '')
                break
    
    if not main_ws:
        candidates = [d for d in workspace_base.iterdir()
                      if d.is_dir() and d.name.startswith("workspace-")]
        if candidates:
            main_ws = str(candidates[0])
    
    if not main_ws:
        info("  未找到 main workspace，跳过")
        return True
    
    ws_path = Path(main_ws)
    
    skills_dst = ws_path / "skills"
    skills_dst.mkdir(parents=True, exist_ok=True)
    
    count = 0
    for skill_dir in skills_src.iterdir():
        if skill_dir.is_dir():
            dst = skills_dst / skill_dir.name
            shutil.copytree(skill_dir, dst, dirs_exist_ok=True)
            count += 1
    
    log(f"  已复制 {count} 个 skills")
    return True

def create_cron_tasks(package_dir):
    """从 cron_jobs.json 重建定时任务"""
    info("重建 cron 任务...")
    
    cron_file = package_dir / "cron_jobs.json"
    if not cron_file.exists():
        info("  未检测到 cron 配置，跳过")
        return True
    
    jobs = load_json(cron_file)
    if not jobs:
        info("  cron_jobs.json 为空，跳过")
        return True
    
    # 读取当前已有任务名
    cron_dir = Path.home() / ".qclaw" / "cron" / "jobs.json"
    existing_names = set()
    if cron_dir.exists():
        try:
            existing_jobs = json.loads(cron_dir.read_text(encoding="utf-8")).get("jobs", [])
            existing_names = {j.get("name", "") for j in existing_jobs}
        except:
            pass
    
    created = skipped = failed = 0
    for job in jobs:
        job_name = job.get("name", "unnamed")
        if job_name in existing_names:
            skipped += 1
            info(f"  跳过已存在：{job_name}")
            continue
        
        # 构造 openclaw tasks add --job JSON（去掉运行时 state 字段）
        job_copy = {k: v for k, v in job.items()
                    if k not in ("id", "createdAtMs", "updatedAtMs", "state")}
        # 确保 delivery 有 sessionTarget
        if "sessionTarget" not in job_copy:
            job_copy["sessionTarget"] = "isolated"
        
        job_json = json.dumps(job_copy, ensure_ascii=False)
        result = subprocess.run(
            ["openclaw", "tasks", "add", "--job", job_json],
            capture_output=True, text=True
        )
        output = result.stdout.strip()
        code = result.returncode
        
        if code == 0:
            log(f"  创建：{job_name}")
            created += 1
        else:
            err(f"  创建失败：{job_name} - {output[:100]}")
            failed += 1
    
    info(f"  结果：{created}个创建，{skipped}个跳过，{failed}个失败")
    return True

def restart_gateway():
    """重启 Gateway（用户已在审查步骤确认）"""
    info("重启 Gateway...")
    result = subprocess.run(
        ["openclaw", "gateway", "restart"],
        capture_output=True, text=True
    )
    output = result.stdout.strip()
    code = result.returncode
    
    if code == 0:
        log("  Gateway 已重启")
        info("  等待5秒让 channel 注册...")
        time.sleep(5)
    else:
        warn("  Gateway 重启命令可能失败")
        warn("  请手动执行：openclaw gateway restart")
    
    return True

# =============================================
# 用户交互
# =============================================

def prompt_main_agent_handling():
    """
    让用户选择如何处理 main agent。
    这次做完整逻辑：选项1/2/3 都有实际执行内容。
    """
    workspace_base = Path.home() / ".qclaw"
    config_path = workspace_base / "openclaw.json"
    
    has_main = False
    if config_path.exists():
        config = load_json(config_path)
        agents = config.get('agents', {}).get('list', [])
        has_main = any(a.get('id') == 'main' for a in agents)
    
    print()
    print("请选择如何处理 Main Agent：")
    print()
    print("  1. 指向现有 agent（把当前 agent 变成你的主控）")
    print("  2. 新建 main agent 实例（另起一个，保留当前配置）")
    if has_main:
        print("  3. 覆盖现有 main agent（⚠️ 替换现有主控）")
    print()
    
    choices = ["1", "2"]
    if has_main:
        choices.append("3")
    
    while True:
        choice = input("请输入选项（" + "/".join(choices) + "）：").strip()
        if choice in choices:
            break
        err("无效选项，请重新输入")
    
    # ---- 选项 1：指向现有 agent ----
    if choice == "1":
        info("将当前 agent 配置为 main...")
        
        if not config_path.exists():
            err("  openclaw.json 不存在，无法配置")
            return False
        
        config = load_json(config_path)
        
        # 找当前 agent 的 workspace
        candidates = [d for d in workspace_base.iterdir()
                      if d.is_dir() and d.name.startswith("workspace-")]
        
        if not candidates:
            warn("  未能找到任何 workspace 目录")
            warn("  请手动在 openclaw.json 中设置 main agent 的 workspace")
            return False
        
        main_ws = str(candidates[0])
        
        if main_ws:
            log(f"  找到 workspace：{main_ws}")
            
            # 把这个 agent 设为 main（添加或更新 agents.list）
            agents_list = config.get('agents', {}).get('list', [])
            
            # 移除已有的 main
            agents_list = [a for a in agents_list if a.get('id') != 'main']
            
            # 添加 main
            agents_list.insert(0, {
                "id": "main",
                "workspace": main_ws,
                "name": "Main Agent"
            })
            
            config['agents']['list'] = agents_list
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            log("  已将当前 agent 设为 main")
        else:
            warn("  未能自动找到 agent workspace")
            warn("  请手动在 openclaw.json 中设置 main agent 的 workspace")
        
        return True
    
    # ---- 选项 2：新建 main agent 实例 ----
    elif choice == "2":
        info("创建新的 main agent 实例...")
        
        # 创建目录结构
        new_ws = workspace_base / "workspace-new-main"
        new_ws.mkdir(parents=True, exist_ok=True)
        (new_ws / "memory").mkdir(exist_ok=True)
        (new_ws / "skills").mkdir(exist_ok=True)
        
        # 创建 agentDir
        agent_dir = workspace_base / "agents" / "main" / "agent"
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建 models.json
        models_config = {
            "providers": {
                "qclaw": {
                    "baseUrl": "http://127.0.0.1:19000/proxy/llm",
                    "apiKey": "__QCLAW_AUTH_GATEWAY_MANAGED__",
                    "api": "openai-completions",
                    "models": [
                        {"id": "modelroute", "name": "modelroute", "input": ["text", "image"]}
                    ]
                }
            }
        }
        with open(agent_dir / "models.json", 'w', encoding='utf-8') as f:
            json.dump(models_config, f, indent=2)
        
        # 更新 openclaw.json：添加 main agent
        if not config_path.exists():
            config = {}
        else:
            config = load_json(config_path)
        
        if 'agents' not in config:
            config['agents'] = {}
        if 'list' not in config['agents']:
            config['agents']['list'] = []
        
        # 移除已有的 main
        config['agents']['list'] = [a for a in config['agents']['list']
                                     if a.get('id') != 'main']
        # 添加新 main
        config['agents']['list'].insert(0, {
            "id": "main",
            "workspace": str(new_ws),
            "name": "Main Agent",
            "agentDir": str(agent_dir)
        })
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        log(f"  已创建 main agent：{new_ws}")
        return True
    
    # ---- 选项 3：覆盖 ----
    elif choice == "3":
        print()
        confirm = input("⚠️ 确认覆盖现有 main agent？输入 'yes' 继续：").strip()
        if confirm.lower() != 'yes':
            err("取消操作")
            return False
        
        info("将覆盖现有 main agent...")
        # 更新 main agent 的 workspace 路径（从搬家包读取）
        agents_file = None
        # 找搬家包目录
        for d in [Path.cwd()] + list(Path.cwd().iterdir()):
            if d.is_dir() and (d / "openclaw-agents.json").exists():
                agents_file = d / "openclaw-agents.json"
                break
        
        if agents_file:
            try:
                agents_patch = load_json(agents_file)
                patch_main = next(
                    (a for a in agents_patch.get('agents', {}).get('list', [])
                     if a.get('id') == 'main'), None)
                if patch_main and patch_main.get('workspace'):
                    new_ws = patch_main['workspace']
                    # 更新 openclaw.json 中 main agent 的 workspace
                    config = load_json(config_path)
                    for a in config.get('agents', {}).get('list', []):
                        if a.get('id') == 'main':
                            a['workspace'] = new_ws
                            break
                    with open(config_path, 'w', encoding='utf-8') as f:
                        json.dump(config, f, indent=2, ensure_ascii=False)
                    log(f"  main agent workspace 已更新为：{new_ws}")
            except Exception as e:
                warn(f"  无法更新 main workspace：{e}")
        
        return True
    
    return True

# =============================================
# 主流程
# =============================================

def review_and_confirm(package_dir, args=None):
    """
    搬家前审查步骤——在执行任何敏感操作之前，
    展示即将写入的配置内容，由用户确认后继续。
    
    这是安全关键步骤，不允许跳过。
    """
    print()
    print("🔍 Step 0.8: 搬家包内容审查")
    print("─" * 40)
    print()
    print("以下内容将从搬家包写入你的系统，请仔细核对：")
    print()
    
    # ---- 1. agents 配置 ----
    agents_file = package_dir / "openclaw-agents.json"
    if agents_file.exists():
        print("【1/3】Agent 配置（将写入 ~/.qclaw/openclaw.json）：")
        agents_patch = load_json(agents_file)
        
        agents_list = agents_patch.get('agents', {}).get('list', [])
        if agents_list:
            print(f"  将追加/更新 {len(agents_list)} 个 agent（不删除现有 agent）：")
            for a in agents_list:
                aid = a.get('id', '?')
                name = a.get('name', '?')
                ws = a.get('workspace', '?')
                print(f"    · {aid}（{name}）→ {ws}")
        
        defaults = agents_patch.get('agents', {}).get('defaults', {})
        allow = defaults.get('subagents', {}).get('allowAgents', [])
        if allow == ["*"]:
            print()
            print('  ⚠️ 注意：搬家包设置了 allowAgents 为 ["*"]')
            print("    安装时会改为最小白名单（仅实际成员ID）。")
            print("    如确实需要通配符，请安装后手动修改。")
        
        hooks_ids = agents_patch.get('hooks', {}).get('allowedAgentIds', [])
        if hooks_ids:
            print()
            print(f"  hooks.allowedAgentIds 将追加：{hooks_ids}")
    else:
        print("【1/3】Agent 配置：无")
    
    print()
    
    # ---- 2. cron 任务 ----
    cron_file = package_dir / "cron_jobs.json"
    if cron_file.exists():
        cron_tasks = load_json(cron_file)
        print(f"【2/3】Cron 定时任务（将创建 {len(cron_tasks)} 个）：")
        for t in cron_tasks:
            tname = t.get('name', 'unnamed')
            schedule = t.get('schedule', '?')
            payload_preview = str(t.get('payload', ''))[:80]
            print(f"    · {tname} — {schedule}")
            if payload_preview:
                print(f"      payload: {payload_preview}...")
    else:
        print("【2/3】Cron 任务：无")
    
    print()
    
    # ---- 3. 文件清单 ----
    print("【3/3】将从搬家包复制的文件：")
    
    identity_dir = package_dir / "身份层"
    if identity_dir.exists():
        identity_files = list(identity_dir.glob("*.md"))
        print(f"  身份文件（→ main workspace）：{len(identity_files)} 个")
        for f in identity_files:
            print(f"    · {f.name}")
        if (identity_dir / "MEMORY.md").exists():
            print("    ⚠️ 含 MEMORY.md（可能含私人信息）")
        if (identity_dir / "TOOLS.md").exists():
            print("    ⚠️ 含 TOOLS.md（可能含 API keys）")
    
    team_dir = package_dir / "团队成员层"
    if team_dir.exists():
        members = [d for d in team_dir.iterdir() if d.is_dir()]
        print(f"  团队成员：{len(members)} 个")
        for m_item in members:
            print(f"    · {m_item.name}/")
    
    skills_src = package_dir / "skills"
    if skills_src.exists():
        skills = [d for d in skills_src.iterdir() if d.is_dir()]
        print(f"  Skills：{len(skills)} 个")
        for s_item in skills:
            print(f"    · {s_item.name}/")
    
    print()
    print("─" * 40)
    print()
    
    if args and args.dry_run:
        print("🔍 DRY RUN 模式：以下操作只展示不执行")
    else:
        print("⚠️ 确认后将执行：复制文件 → 合并配置（写入前展示diff）" + (" → 创建 cron" if not (args and args.no_cron) else "（跳过cron）") + (" → 重启 Gateway" if not (args and args.no_restart) else "（跳过重启）"))
    
    while True:
        print("是否确认执行以上操作？")
        print()
        print("  y  — 确认，继续搬家")
        print("  n  — 取消，中止操作")
        print()
        choice = input("请输入（y/n）：").strip().lower()
        if choice == 'y':
            print()
            log("用户已确认，继续执行...")
            return True
        elif choice == 'n':
            print()
            err("用户取消，搬家中止")
            return False
        else:
            err("无效选项，请输入 y 或 n")


def parse_args():
    parser = argparse.ArgumentParser(description="一键搬家执行脚本 v3.0")
    parser.add_argument("package", nargs="?", help="搬家包 zip 或目录路径")
    parser.add_argument("--dry-run", action="store_true", help="只展示将要执行的操作和diff，不实际执行")
    parser.add_argument("--no-cron", action="store_true", help="跳过 cron 任务创建")
    parser.add_argument("--no-restart", action="store_true", help="跳过 Gateway 重启")
    return parser.parse_args()

def main():
    args = parse_args()

    print()
    print("=" * 60)
    print("  一键搬家执行脚本 v3.0（审查确认 + diff 展示 + 细粒度控制）")
    if args.dry_run:
        print("  🔍 DRY RUN 模式——只展示不执行")
    print("=" * 60)
    print()

    # ---- 找到搬家包 ----
    info("定位搬家包...")
    package_dir = find_package_dir()

    if not package_dir:
        err("找不到搬家包！")
        print()
        print("用法：python3 migrate.py <搬家包路径> [--dry-run] [--no-cron] [--no-restart]")
        return

    log(f"  搬家包目录：{package_dir.name}/")
    print()

    # ---- 搬家包审查（必须在修改配置之前） ----
    if not review_and_confirm(package_dir, args):
        return

    # ---- dry-run: 展示 merge diff 但不写入 ----
    if args.dry_run:
        print()
        info("DRY RUN: 展示配置合并 diff（不写入文件）...")
        agents_file = package_dir / "openclaw-agents.json"
        if agents_file.exists():
            agents_patch = load_json(agents_file)
            config_path = Path.home() / ".qclaw" / "openclaw.json"
            existing = load_json(config_path) if config_path.exists() else {}
            merged = existing.copy()
            if 'agents' in agents_patch:
                if 'agents' not in merged:
                    merged['agents'] = {}
                if 'defaults' in agents_patch['agents']:
                    if 'defaults' not in merged['agents']:
                        merged['agents']['defaults'] = {}
                    merged['agents']['defaults'] = deep_merge(
                        merged['agents']['defaults'], agents_patch['agents']['defaults'])
                if 'list' in agents_patch['agents']:
                    if 'list' not in merged['agents']:
                        merged['agents']['list'] = []
                    existing_ids = {a.get('id') for a in merged['agents']['list']}
                    for agent in agents_patch['agents']['list']:
                        aid = agent.get('id')
                        if aid in existing_ids:
                            merged['agents']['list'] = [
                                agent if a.get('id') == aid else a
                                for a in merged['agents']['list']
                            ]
                        else:
                            merged['agents']['list'].append(agent)
            if 'hooks' in agents_patch:
                if 'hooks' not in merged:
                    merged['hooks'] = {}
                existing_ids = set(merged['hooks'].get('allowedAgentIds', []))
                patch_ids = set(agents_patch['hooks'].get('allowedAgentIds', []))
                merged['hooks']['allowedAgentIds'] = list(existing_ids | patch_ids)

            existing_text = json.dumps(existing, indent=2, ensure_ascii=False).splitlines(keepends=True)
            merged_text = json.dumps(merged, indent=2, ensure_ascii=False).splitlines(keepends=True)
            diff = list(difflib.unified_diff(existing_text, merged_text,
                                              fromfile="现有 openclaw.json", tofile="合并后", n=3))
            if diff:
                info("  openclaw.json 变更 diff：")
                for line in diff[:80]:
                    line = line.rstrip("\n")
                    if line.startswith("+") and not line.startswith("+++"):
                        print(f"    {GREEN}{line}{NC}")
                    elif line.startswith("-") and not line.startswith("---"):
                        print(f"    {RED}{line}{NC}")
                    elif line.startswith("@@"):
                        print(f"    {YELLOW}{line}{NC}")
                    else:
                        print(f"    {line}")
            else:
                info("  openclaw.json 无变更")

        print()
        print("=" * 60)
        print("  🔍 DRY RUN 完成——以上操作未实际执行")
        print("  去掉 --dry-run 参数后重新运行以执行搬家")
        print("=" * 60)
        return

    # ---- 备份 ----
    print("🔒 Step 0: 备份现有配置...")
    backup_existing()
    print()

    # ---- 用户选择 main agent 处理方式 ----
    print("🔧 Step 0.5: Main Agent 配置...")
    if not prompt_main_agent_handling():
        err("Main Agent 配置失败，中止搬家")
        return
    print()

    # ---- 主流程 ----
    steps = [
        ("Step 1: 复制身份文件",     copy_identity_files),
        ("Step 2: 复制团队成员",     copy_team_members),
        ("Step 3: 复制 skills",       copy_skills),
        ("Step 4: 合并 agent 配置（写入前展示diff）",  merge_config),
    ]

    if not args.no_cron:
        steps.append(("Step 5: 创建 cron 任务", create_cron_tasks))
    else:
        info("跳过 cron 任务创建（--no-cron）")

    if not args.no_restart:
        steps.append(("Step 6: 重启 Gateway", restart_gateway))
    else:
        info("跳过 Gateway 重启（--no-restart），请手动执行：openclaw gateway restart")

    for label, fn in steps:
        print(f"{label}...")
        result = fn(package_dir)
        if not result:
            err(f"{label} 失败")
        print()

    # ---- 完成 ----
    print("=" * 60)
    print("  ✅ 一键搬家完成！")
    print("=" * 60)
    print()
    print("📋 验证步骤：")
    print()
    print("  1. 检查 SOUL.md：")
    print("     ls ~/.qclaw/workspace-*/SOUL.md")
    print()
    print("  2. 测试子代理激活：")
    print("     在 agent 对话中说：测试激活团队成员")
    print()
    if args.no_restart:
        print("  3. 手动重启 Gateway：")
        print("     openclaw gateway restart")
        print()
    print("  检查 cron 任务：")
    print("     openclaw tasks list")
    print()
    print("  如需回滚：")
    backup_list = sorted(BACKUP_DIR.iterdir(), key=lambda d: d.name)
    if backup_list:
        latest = backup_list[-1].name
        print(f"     cp -r {BACKUP_DIR / latest}/* ~/.qclaw/")
    print()
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
