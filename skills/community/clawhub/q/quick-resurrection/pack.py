#!/usr/bin/env python3
"""
一键搬家打包脚本 v2.0(通用版)
功能:自动收集所有资料,生成搬家包

修复:
- v2.0: 改为自动检测当前 active workspace，不再硬编码具体路径
"""

import os
import json
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

# =============================================
# 颜色输出
# =============================================
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

def log(msg): print(f"{GREEN}[✓]{NC} {msg}")
def err(msg): print(f"{RED}[✗]{NC} {msg}")
def warn(msg): print(f"{YELLOW}[!]{NC} {msg}")
def info(msg): print(f"{BLUE}[i]{NC} {msg}")

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

# =============================================
# 核心:自动检测当前 active workspace
# =============================================

def detect_active_workspace():
    """
    自动检测当前 agent 的 active workspace。

    策略:
    1. 读取 ~/.qclaw/openclaw.json 的 agents.list
    2. 找到 main agent 的 workspace 路径
    3. 验证该目录包含 SOUL.md

    返回:Path 对象 或 None
    """
    config_path = Path.home() / ".qclaw" / "openclaw.json"

    if not config_path.exists():
        warn("找不到 openclaw.json,尝试从当前工作目录推断")
        # fallback:从 cwd 推断
        cwd = Path.cwd()
        if (cwd / "SOUL.md").exists():
            return cwd
        return None

    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    agents = config.get('agents', {}).get('list', [])

    # 找 main agent
    for agent in agents:
        if agent.get('id') == 'main':
            workspace = agent.get('workspace', '')
            if workspace:
                wp = Path(workspace)
                if wp.exists() and (wp / "SOUL.md").exists():
                    return wp

    # fallback：从agents.list推断主agent workspace
    # 策略：收集所有workspace路径的父级链，找包含SOUL.md的最深公共父目录
    workspaces = [Path(a['workspace']) for a in agents
                  if a.get('workspace') and Path(a.get('workspace', '')).exists()]
    if workspaces:
        # 收集所有workspace的所有祖先目录（到home为止）
        candidate_dirs = set()
        home = Path.home()
        for ws in workspaces:
            for parent in ws.parents:
                if parent == home or not str(parent).startswith(str(home)):
                    break
                candidate_dirs.add(parent)
        # 在候选目录中找包含SOUL.md+MEMORY.md的，选最深的（最接近workspace）
        for candidate in sorted(candidate_dirs, key=lambda x: len(x.parts), reverse=True):
            if (candidate / 'SOUL.md').exists() and (candidate / 'MEMORY.md').exists():
                return candidate

    # fallback：遍历 workspace- 开头的目录，找包含 SOUL.md + MEMORY.md 的
    workspace_base = Path.home() / ".qclaw"
    candidates = []
    for d in workspace_base.iterdir():
        if not (d.is_dir() and d.name.startswith("workspace-")):
            continue
        has_identity = (d / "SOUL.md").exists() and (d / "MEMORY.md").exists()
        subagent_count = sum(1 for sub in d.iterdir() if sub.is_dir() and (sub / "SOUL.md").exists())
        candidates.append((d, has_identity, subagent_count))
    candidates.sort(key=lambda x: (x[1], x[2]), reverse=True)
    if candidates:
        return candidates[0][0]

    # fallback:找当前 cwd 的父链
    cwd = Path.cwd()
    for parent in [cwd] + list(cwd.parents):
        if (parent / "SOUL.md").exists() and (parent / "MEMORY.md").exists():
            return parent

    return None

def get_agent_name(workspace):
    """从 workspace 推断 agent 名称"""
    soul = workspace / "SOUL.md"
    identity = workspace / "IDENTITY.md"

    # 优先从 IDENTITY.md 的 Name 字段读取
    if identity.exists():
        with open(identity, 'r', encoding='utf-8') as f:
            for line in f.read().split('\n'):
                if line.startswith('- **Name:**'):
                    name = line.split('**Name:**')[1].strip()
                    if name:
                        return name

    # 从 SOUL.md 的第一个 # 标题读取
    if soul.exists():
        with open(soul, 'r', encoding='utf-8') as f:
            for line in f.read().split('\n'):
                if line.startswith('# '):
                    title = line[2:].strip()
                    # 去掉 SOUL.md 标记
                    title = title.replace('SOUL.md', '').replace('—', '').strip()
                    if title:
                        return title

    return workspace.name  # 默认用目录名

# =============================================
# 主流程
# =============================================

def get_agent_info():
    """获取 agent 配置信息"""
    config_path = Path.home() / ".qclaw" / "openclaw.json"
    if not config_path.exists():
        return []
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config.get('agents', {}).get('list', [])

def get_cron_tasks():
    """从 ~/.qclaw/cron/jobs.json 读取 cron 任务定义"""
    cron_file = Path.home() / ".qclaw" / "cron" / "jobs.json"
    if not cron_file.exists():
        return []
    try:
        data = json.loads(cron_file.read_text(encoding="utf-8"))
        jobs = data.get("jobs", [])
        # 只取 enabled=True 的任务
        return [j for j in jobs if j.get("enabled", True)]
    except Exception:
        return []

def main():
    print()
    print("=" * 60)
    print("  一键搬家打包脚本 v2.0")
    print(f"  时间:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()

    # ---- 自动检测 active workspace ----
    info("检测当前 active workspace...")
    main_workspace = detect_active_workspace()

    if not main_workspace:
        err("无法自动检测 active workspace")
        err("请手动设置 MAIN_WORKSPACE 环境变量,或确保 openclaw.json 中有 main agent 配置")
        print()
        print("手动指定示例:")
        print("  export MAIN_WORKSPACE=/Users/xxx/.qclaw/workspace-agent-xxx")
        print("  python3 pack.py")
        return

    agent_name = get_agent_name(main_workspace)
    log(f"检测到 workspace:{main_workspace}")
    log(f"Agent 名称:{agent_name}")
    print()

    # 创建输出目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"{agent_name}搬家包_{timestamp}"
    OUTPUT_DIR = Path.home() / "一键搬家包"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    package_dir = OUTPUT_DIR / package_name
    package_dir.mkdir(parents=True, exist_ok=True)
    info(f"输出目录:{package_dir}")
    print()

    # ------------------------------------------
    # Step 1: 收集 Main Agent 信息
    # ------------------------------------------
    print("📦 Step 1: 收集 Main Agent 信息...")

    main_dir = package_dir / "身份层"
    main_dir.mkdir(exist_ok=True)

    core_files = ["SOUL.md", "MEMORY.md", "TOOLS.md", "AGENTS.md", "IDENTITY.md", "USER.md", "SKILLS.md"]
    for filename in core_files:
        src = main_workspace / filename
        if src.exists():
            shutil.copy2(src, main_dir / filename)
            log(f"  {filename}")

    memory_src = main_workspace / "memory"
    if memory_src.exists():
        memory_dst = main_dir / "memory"
        memory_dst.mkdir(exist_ok=True)
        for f in memory_src.glob("*.md"):
            shutil.copy2(f, memory_dst / f.name)
        log(f"  memory/")

    print()

    # ------------------------------------------
    # Step 2: 收集团队成员(自动检测)
    # ------------------------------------------
    print("👥 Step 2: 收集团队成员...")

    agents = get_agent_info()
    team_members = []

    # 自动检测是否有团队成员
    has_team = False
    if agents:
        for agent in agents:
            if agent.get('id') != 'main':
                has_team = True
                break

    if not has_team:
        info("  未检测到团队成员,跳过")
    else:
        for agent in agents:
            agent_id = agent.get('id', '')
            if agent_id == 'main':
                continue

            name = agent.get('name', agent_id)
            workspace = agent.get('workspace', '')

            if workspace and Path(workspace).exists():
                team_dir = package_dir / "团队成员层" / name
                team_dir.mkdir(parents=True, exist_ok=True)

                for filename in ["SOUL.md", "MEMORY.md", "TOOLS.md"]:
                    src = Path(workspace) / filename
                    if src.exists():
                        shutil.copy2(src, team_dir / filename)

                team_members.append({"id": agent_id, "name": name, "workspace": workspace})
                log(f"  {name} ({agent_id})")

    info(f"  共 {len(team_members)} 个团队成员")
    print()

    # ------------------------------------------
    # Step 3: 收集 Skills
    # ------------------------------------------
    print("🔧 Step 3: 收集 Skills...")

    skills_src = main_workspace / "skills"
    skill_count = 0
    if skills_src.exists():
        skills_dst = package_dir / "skills"
        skills_dst.mkdir(exist_ok=True)

        for skill_dir in skills_src.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                dst = skills_dst / skill_dir.name
                shutil.copytree(skill_dir, dst, dirs_exist_ok=True)
                log(f"  {skill_dir.name}/")
                skill_count += 1

    if skill_count == 0:
        warn("  未检测到 skills")
    print()

    # ------------------------------------------
    # Step 4: 收集 Cron 任务配置
    # ------------------------------------------
    print("⏰ Step 4: 收集 Cron 任务配置...")

    cron_tasks = get_cron_tasks()
    if cron_tasks:
        # 存完整 jobs 定义，migrate 时直接重建
        with open(package_dir / "cron_jobs.json", 'w', encoding='utf-8') as f:
            json.dump(cron_tasks, f, indent=2, ensure_ascii=False)

        log(f"  cron_jobs.json ({len(cron_tasks)} 个任务)")
    else:
        warn("  未能获取 cron 任务列表")
    print()

    # ------------------------------------------
    # Step 4.5: 检测工作目录
    # ------------------------------------------
    print("📁 Step 4.5: 检测工作目录...")

    # 扫描常见工作目录
    common_work_dirs = [
        Path.home() / "tales",
        Path.home() / "work",
        Path.home() / "projects",
        Path.home() / "workspace",
    ]

    found_work_dirs = []
    for d in common_work_dirs:
        if d.exists() and d.is_dir():
            # 检查是否 git 仓库
            if (d / ".git").exists():
                found_work_dirs.append(str(d))
                log(f"  {d} (git仓库)")

    # 生成工作目录提示文件
    work_dir_note = f"""# 工作目录

打包时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 检测到的 git 工作目录

{chr(10).join(f'- {d}' for d in found_work_dirs) if found_work_dirs else '(未检测到常见工作目录)'}

## 搬家后请手动处理

1. 将上述目录的 git remote 设置为新环境的地址
2. 如果是新 clone，确保 .git/config 中的 user.name 和 user.email 正确
3. 建议: 在新环境执行一次 `git status` 确认仓库正常

## 提示

tales/ 目录是团队的创作成果仓库。
建议把它放在固定位置，并在新环境 clone 后更新路径配置。
"""

    with open(package_dir / "工作目录说明.md", 'w', encoding='utf-8') as f:
        f.write(work_dir_note)
    log("  工作目录说明.md")
    print()

    # ------------------------------------------
    # Step 5: 生成 Agent 配置片段
    # ------------------------------------------
    print("📝 Step 5: 生成 Agent 配置片段...")

    if agents:
        agents_config = {
            "agents": {
                "defaults": {
                    "model": {"primary": "qclaw/modelroute"},
                    "maxConcurrent": 10,
                    "subagents": {"allowAgents": [a["id"] for a in agents if a.get("id") != "main"]}
                },
                "list": agents
            },
            "hooks": {
                "allowedAgentIds": [a['id'] for a in agents if a['id'] != 'main']
            }
        }

        with open(package_dir / "openclaw-agents.json", 'w', encoding='utf-8') as f:
            json.dump(agents_config, f, indent=2, ensure_ascii=False)

        log("  openclaw-agents.json")
    print()

    # ------------------------------------------
    # Step 6: 生成 README.md
    # ------------------------------------------
    print("📄 Step 6: 生成 README.md...")

    team_tree = ""
    if has_team:
        team_tree = f"""
├── 团队成员层/          ← {len(team_members)} 个团队成员
│   ├── 小A/
│   └── 小B/
│   └── ..."""

    readme_content = f"""# 一键搬家包

**生成时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Agent:** {agent_name}
**Workspace:** {main_workspace}
"""

    if has_team:
        readme_content += f"**团队成员:** {len(team_members)} 人\n\n成员列表:\n"
        for m in team_members:
            readme_content += f"- **{m['name']}** (`{m['id']}`)\n"

    readme_content += f"""
---

## 包内容

```
搬家包/
├── 身份层/              ← Main Agent 核心文件
│   ├── SOUL.md
│   ├── MEMORY.md
│   ├── TOOLS.md
│   ├── AGENTS.md
│   ├── IDENTITY.md
│   ├── USER.md
│   └── memory/{team_tree}
│
├── skills/              ← Skills({skill_count}个)
│
├── openclaw-agents.json ← Agent 配置片段
├── cron_jobs.json       ← Cron 任务配置
├── 工作目录说明.md      ← git工作目录提示
│
├── README.md            ← 本文件
└── migrate.py           ← 一键执行脚本
```

---

## 使用方法

### 自动执行(推荐)

把这个包丢给 agent,说:

```
这是一键搬家包,帮我搬家
```

agent 会自动执行:
1. 备份现有配置
2. 合并 agent 配置(不覆盖其他配置)
3. 复制身份文件 + 团队成员 + skills
4. 创建 cron 任务
5. 重启 Gateway

### 手动执行

```bash
unzip 搬家包.zip
cd 搬家包
python3 migrate.py
```

---

## 注意事项

1. 搬家前会**自动备份**现有配置到 `~/.qclaw/backup/`
2. agent 配置会与现有配置**合并**,不会覆盖其他配置
3. 完成后请重启一次 Gateway(如果未自动重启)

---

**生成脚本:** skills/quick-resurrection/pack.py v2.0
"""

    with open(package_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)

    # 把 migrate.py 也复制进包(从 skill 目录复制)
    skill_dir = main_workspace / "skills" / "quick-resurrection"
    migrate_src = skill_dir / "migrate.py"
    if migrate_src.exists():
        shutil.copy2(migrate_src, package_dir / "migrate.py")
        log("  migrate.py")

    log("  README.md")
    print()

    # ------------------------------------------
    # Step 7: 打包
    # ------------------------------------------
    print("📦 Step 7: 打包...")

    zip_file = str(package_dir) + ".zip"
    shutil.make_archive(str(package_dir), 'zip', package_dir)

    zip_size = os.path.getsize(zip_file)
    size_mb = zip_size / (1024 * 1024)

    log(f"  打包完成:{zip_file}")
    info(f"  包大小:{size_mb:.2f} MB")

    shutil.rmtree(package_dir)

    print()

    # 完成报告
    print("=" * 60)
    print("  打包完成")
    print("=" * 60)
    print()
    print(f"✅ 输出文件:{zip_file}")
    print(f"✅ 包大小:{size_mb:.2f} MB")
    print()
    print("📋 包内容:")
    print(f"   - Main Agent({agent_name})")
    print(f"   - 团队成员:{len(team_members)} 人")
    print(f"   - Skills:{skill_count} 个")
    print(f"   - Cron任务:{len(cron_tasks)} 个")
    if found_work_dirs:
        print(f"   - 工作目录:{len(found_work_dirs)} 个(含git仓库)")
    print()
    print("📋 后续步骤:")
    print()
    print("   1. 把搬家包复制到新环境")
    print("   2. 把搬家包丢给 agent,说:'这是一键搬家包,帮我搬家'")
    print()
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
