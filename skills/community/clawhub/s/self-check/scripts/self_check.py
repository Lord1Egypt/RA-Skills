#!/usr/bin/env python3
"""
OpenClaw Self-Check Script v2.0
全面检查系统环境、配置、依赖等，并输出报告

⚠️ 核心原则：只检查、汇报、建议，绝不主动修复
- 不自动安装任何包
- 不自动修改任何配置文件  
- 不自动重启任何服务
- 所有修复需用户手动执行

新增：Skills 详细依赖检查、MCP 检查、文件目录结构检查
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field

# 配置
WORKSPACE = Path.home() / ".openclaw"
# 动态检测 workspace 根目录：脚本位于 workspace/skills/self-check/scripts/
WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent
if not WORKSPACE_ROOT.name.startswith("workspace-"):
    # 回退到默认路径检测
    workspaces = list(WORKSPACE.glob("workspace-*"))
    WORKSPACE_ROOT = workspaces[0] if workspaces else WORKSPACE
IS_LINUX = os.name == "posix"


@dataclass
class CheckResult:
    passes: List[str] = field(default_factory=list)
    issues: List[Dict] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def add_pass(self, item: str):
        self.passes.append(f"✅ {item}")
    
    def add_issue(self, item: str, fix: str = None, severity: str = "error"):
        self.issues.append({"item": item, "fix": fix, "severity": severity})
    
    def add_warning(self, item: str):
        self.warnings.append(f"⚠️ {item}")
    
    def report(self) -> str:
        lines = ["# 🔍 OpenClaw 自检报告\n"]
        lines.append("⚠️ 本报告仅检查并汇报问题，不会自动修复任何内容\n")
        lines.append("所有修复命令需用户确认后手动执行\n")
        
        lines.append("## ✅ 通过项")
        for p in self.passes:
            lines.append(f"- {p}")
        
        if self.warnings:
            lines.append("\n## ⚠️ 警告项")
            for w in self.warnings:
                lines.append(f"- {w}")
        
        if self.issues:
            lines.append("\n## ❌ 问题项")
            for i, issue in enumerate(self.issues, 1):
                emoji = "🔴" if issue['severity'] == "error" else "🟡"
                lines.append(f"\n### {i}. {emoji} {issue['item']}")
                if issue['fix']:
                    lines.append(f"   **修复建议:** `{issue['fix']}`")
                    lines.append(f"   ⚠️ 请手动执行上述命令，确认后再操作")
        else:
            lines.append("\n## 🎉 无问题发现")
        
        return "\n".join(lines)


def run_cmd(cmd: str, shell: bool = True, timeout: int = 30) -> Tuple[int, str, str]:
    """运行命令并返回 (returncode, stdout, stderr)"""
    try:
        result = subprocess.run(
            cmd, shell=shell, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)


def check_python_module(module: str) -> bool:
    """检查 Python 模块是否可用"""
    code, _, _ = run_cmd(f"python3 -c 'import {module}' 2>&1", timeout=5)
    return code == 0


def check_node_env(result: CheckResult):
    """检查 Node.js 环境"""
    # Node 版本（系统默认）
    code, stdout, _ = run_cmd("node --version")
    if code == 0:
        version = stdout.replace("v", "")
        result.add_pass(f"Node.js (系统): v{version}")
    else:
        result.add_issue("Node.js 未安装", "安装 Node.js >= 22.12.0", "error")
    
    # nvm 管理的版本
    code, stdout, _ = run_cmd("export NVM_DIR=$HOME/.nvm && [ -s $NVM_DIR/nvm.sh ] && . $NVM_DIR/nvm.sh && nvm current")
    if code == 0 and stdout:
        version = stdout.replace("v", "")
        result.add_pass(f"Node.js (nvm): v{version}")
        
        # 检查版本要求
        major = int(version.split(".")[0])
        if major < 22:
            result.add_issue(
                f"nvm Node.js 版本过低 ({version} < 22.12.0)",
                "nvm install 22 && nvm use 22 && nvm alias default 22",
                "error"
            )
    
    # nvm
    code, stdout, _ = run_cmd("export NVM_DIR=$HOME/.nvm && [ -s $NVM_DIR/nvm.sh ] && . $NVM_DIR/nvm.sh && nvm --version")
    if code == 0:
        result.add_pass(f"nvm: {stdout}")
    else:
        result.add_issue("nvm 不可用", "安装 nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash", "warning")
    
    # npm
    code, stdout, _ = run_cmd("npm --version")
    if code == 0:
        result.add_pass(f"npm: {stdout}")


def check_gateway(result: CheckResult):
    """检查 Gateway 状态"""
    # Gateway 进程
    code, stdout, _ = run_cmd("pgrep -f openclaw-gateway")
    if code == 0:
        pid = stdout.split()[0]
        result.add_pass(f"Gateway 进程运行中 (PID: {pid})")
        
        # 检查进程使用的 node 版本
        code, stdout, _ = run_cmd(f"readlink /proc/{pid}/exe 2>/dev/null || echo 'unknown'")
        if "v22" in stdout:
            result.add_pass(f"Gateway 使用 Node.js v22+")
        elif code == 0:
            result.add_issue(
                f"Gateway 使用了旧版 Node ({stdout})",
                "openclaw gateway restart",
                "warning"
            )
    else:
        result.add_issue("Gateway 未运行", "openclaw gateway start", "error")
    
    # 检查 Gateway 端口
    code, stdout, _ = run_cmd("ss -tlnp | grep 23789")
    if code == 0:
        result.add_pass("Gateway 端口 23789 监听中")
    else:
        result.add_issue("Gateway 端口未监听", "检查 gateway 日志: openclaw logs", "error")


def check_openclaw_json(result: CheckResult):
    """检查 openclaw.json"""
    config_path = WORKSPACE / "openclaw.json"
    
    if not config_path.exists():
        result.add_issue("openclaw.json 不存在", "创建配置文件", "error")
        return
    
    try:
        with open(config_path) as f:
            config = json.load(f)
        result.add_pass("openclaw.json 语法正确")
    except json.JSONDecodeError as e:
        result.add_issue(f"openclaw.json 格式错误: {e}", "修复 JSON 语法", "error")
        return
    
    # 检查 channels
    channels = config.get("channels", {})
    for ch in ["discord", "qqbot", "telegram"]:
        if channels.get(ch, {}).get("enabled"):
            result.add_pass(f"Channel {ch}: 已启用")
        else:
            result.add_warning(f"Channel {ch}: 未启用")


def check_agent_files(result: CheckResult):
    """检查 Agent 文件"""
    # 必需文件
    required = {
        "SOUL.md": WORKSPACE_ROOT / "SOUL.md",
        "USER.md": WORKSPACE_ROOT / "USER.md",
        "AGENTS.md": WORKSPACE_ROOT / "AGENTS.md",
    }
    
    for name, path in required.items():
        if path.exists():
            result.add_pass(f"{name}: 存在")
        else:
            result.add_issue(f"{name}: 不存在（必需）", f"创建 {name}", "error")
    
    # memory/ 目录（每日记录）
    memory_dir = WORKSPACE_ROOT / "memory"
    if memory_dir.exists():
        files = list(memory_dir.glob("*.md"))
        result.add_pass(f"memory/: {len(files)} 个记录")
    else:
        result.add_warning("memory/: 不存在（可选）")
    
    # MEMORY.md（长期记忆）
    memory_longterm = WORKSPACE_ROOT / "MEMORY.md"
    if memory_longterm.exists():
        result.add_pass("MEMORY.md (长期记忆): 存在")
    else:
        result.add_warning("MEMORY.md (长期记忆): 不存在（可选）")
    
    # self-improving/ 目录
    self_improving_dir = WORKSPACE_ROOT / "self-improving"
    if self_improving_dir.exists():
        files = list(self_improving_dir.glob("*.md"))
        result.add_pass(f"self-improving/: {len(files)} 个文件")
    else:
        result.add_warning("self-improving/: 未安装（可选）")


def check_skill_structure(result: CheckResult, skill_name: str, skill_path: Path):
    """检查单个 skill 的目录结构和依赖"""
    if not skill_path.exists():
        return  # skill 未安装，跳过
    
    # 检查必需文件
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        result.add_issue(f"Skill {skill_name}: 缺少 SKILL.md", f"创建 {skill_name}/SKILL.md", "error")
    
    # 检查 scripts/ 目录
    scripts_dir = skill_path / "scripts"
    has_scripts = scripts_dir.exists() and scripts_dir.is_dir()
    
    # 检查 config.json（可选）
    config_file = skill_path / "config.json"
    has_config = config_file.exists()
    
    # 读取 SKILL.md 检查依赖
    if skill_md.exists():
        try:
            content = skill_md.read_text(encoding='utf-8', errors='ignore')
            
            # 检查 Python 依赖
            if "pip install" in content or "requires.*python" in content.lower():
                # 尝试解析依赖
                if skill_name == "bocha-search":
                    if not check_python_module("requests"):
                        result.add_issue(
                            f"Skill {skill_name}: 缺少 Python 模块 'requests'",
                            "pip3 install requests",
                            "error"
                        )
                    else:
                        result.add_pass(f"Skill {skill_name}: requests 模块可用")
                
                if skill_name == "aliyun-stt":
                    if not check_python_module("dashscope"):
                        result.add_issue(
                            f"Skill {skill_name}: 缺少 Python 模块 'dashscope'",
                            "pip3 install dashscope",
                            "error"
                        )
                    else:
                        result.add_pass(f"Skill {skill_name}: dashscope 模块可用")
            
            # 检查 config 要求
            if "config.json" in content and not has_config:
                result.add_warning(f"Skill {skill_name}: 建议创建 config.json")
            
        except Exception as e:
            result.add_warning(f"Skill {skill_name}: 读取 SKILL.md 失败: {e}")
    
    # 汇总
    status = []
    if skill_md.exists():
        status.append("SKILL.md")
    if has_scripts:
        status.append("scripts/")
    if has_config:
        status.append("config.json")
    
    if status:
        result.add_pass(f"Skill {skill_name}: {' '.join(status)}")


def check_skills(result: CheckResult):
    """检查 Skills 详细依赖"""
    skills_dir = WORKSPACE_ROOT / "skills"
    
    if not skills_dir.exists():
        result.add_issue("skills 目录不存在", "检查 workspace 配置", "error")
        return
    
    result.add_pass(f"Skills 目录: {skills_dir}")
    
    # Python 基础
    code, stdout, _ = run_cmd("python3 --version")
    if code == 0:
        result.add_pass(f"Python3: {stdout}")
    else:
        result.add_issue("Python3 不可用", "安装 Python3", "error")
        return  # 没有 Python 无法检查模块
    
    # 检查已安装的 skills
    installed_skills = [d.name for d in skills_dir.iterdir() if d.is_dir()]
    result.add_pass(f"已安装 Skills: {len(installed_skills)} 个")
    
    # 详细检查关键 skills
    key_skills = ["bocha-search", "aliyun-stt", "minimax-stt", "xfyun-stt", "pubmed-search", "semantic-scholar-search"]
    for skill in key_skills:
        skill_path = skills_dir / skill
        check_skill_structure(result, skill, skill_path)
    
    # 检查 self-check 自己
    self_check_path = skills_dir / "self-check"
    if self_check_path.exists():
        result.add_pass("Skill self-check: 已安装")


def check_mcp(result: CheckResult):
    """检查 MCP (Model Context Protocol) 配置"""
    # MCP 配置通常在 ~/.openclaw/ 或其他位置
    # 检查常见的 MCP 工具
    
    mcp_tools = {
        "mcporter": "mcporter --version",
        "acpx": "which acpx 2>/dev/null || echo 'not found'",
    }
    
    result.add_pass("MCP 检查开始")
    
    # 检查 acpx
    acpx_dir = Path("/usr/local/lib/node_modules/openclaw/extensions/acpx")
    if acpx_dir.exists():
        # 检查版本
        pkg_json = acpx_dir / "package.json"
        if pkg_json.exists():
            try:
                with open(pkg_json) as f:
                    data = json.load(f)
                    dep = data.get("dependencies", {}).get("acpx", "")
                    result.add_pass(f"MCP acpx: {dep}")
            except:
                pass
        
        # 检查 node_modules 中的 acpx
        acpx_bin = acpx_dir / "node_modules" / ".bin" / "acpx"
        if acpx_bin.exists():
            result.add_pass("MCP acpx: 二进制文件存在")
        else:
            result.add_issue("MCP acpx: 二进制文件缺失", "npm install", "warning")
        
        # 检查日志中的加载状态
        code, stdout, _ = run_cmd(f"grep -i 'acpx.*ready' /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | tail -1")
        if "ready" in stdout.lower():
            result.add_pass("MCP acpx: 运行时后端已加载")
        else:
            code2, stdout2, _ = run_cmd(f"grep -i 'acpx.*failed' /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log 2>/dev/null | tail -1")
            if "failed" in stdout2.lower():
                result.add_issue(f"MCP acpx: 加载失败", "检查 nvm/node 版本，重启 gateway", "error")
    else:
        result.add_warning("MCP acpx: 插件目录不存在")
    
    # 检查其他 MCP 配置
    mcp_config = WORKSPACE / "mcp.json"
    if mcp_config.exists():
        try:
            with open(mcp_config) as f:
                json.load(f)
            result.add_pass("MCP 配置: mcp.json 语法正确")
        except:
            result.add_issue("MCP 配置: mcp.json 格式错误", "修复 JSON", "error")


def check_api_keys(result: CheckResult):
    """检查 API Key 配置（不显示具体内容）"""
    # 检查常见的 API key 配置位置
    
    # 1. 环境变量
    env_keys = ["OPENAI_API_KEY", "MINIMAX_API_KEY", "BOCHA_API_KEY", "DASHSCOPE_API_KEY"]
    for key in env_keys:
        if os.environ.get(key):
            result.add_pass(f"API Key {key}: 已配置 (环境变量)")
    
    # 2. 配置文件中的 keys
    config_checks = [
        (WORKSPACE / "openclaw.json", "openclaw.json"),
        (WORKSPACE_ROOT / "skills" / "bocha-search" / "config.json", "bocha-search"),
    ]
    
    for config_path, name in config_checks:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    data = json.load(f)
                
                # 检查是否有 api_key 字段（不显示值）
                has_key = False
                def check_dict(d, path=""):
                    nonlocal has_key
                    if isinstance(d, dict):
                        for k, v in d.items():
                            if "key" in k.lower() or "token" in k.lower() or "secret" in k.lower():
                                if v and v != "***" and len(str(v)) > 5:
                                    has_key = True
                            elif isinstance(v, dict):
                                check_dict(v, f"{path}.{k}")
                
                check_dict(data)
                if has_key:
                    result.add_pass(f"API Key {name}: 已配置")
                    
            except:
                pass


def check_permissions(result: CheckResult):
    """检查目录权限"""
    dirs = [WORKSPACE, WORKSPACE_ROOT]
    
    for d in dirs:
        if d.exists():
            stat = os.stat(d)
            owner = stat.st_uid
            mode = oct(stat.st_mode)[-3:]
            
            # 检查所有者是否为当前用户
            if owner == os.getuid():
                result.add_pass(f"权限 {d.name}: 正确")
            else:
                result.add_issue(
                    f"权限 {d.name}: 所有者不正确 (uid={owner})",
                    f"sudo chown -R $(whoami):$(whoami) {d}",
                    "warning"
                )
    
    # 检查 skills 目录权限
    skills_dir = WORKSPACE_ROOT / "skills"
    if skills_dir.exists():
        # 检查是否有可写权限
        if os.access(skills_dir, os.W_OK):
            result.add_pass("权限 skills/: 可写")
        else:
            result.add_issue("权限 skills/: 不可写", "检查目录权限", "warning")


def main():
    print("🔍 正在执行全面自检...\n")
    
    result = CheckResult()
    
    # 执行各项检查
    print("📡 检查 Node.js 环境...")
    check_node_env(result)
    
    print("📡 检查 Gateway...")
    check_gateway(result)
    
    print("📡 检查配置文件...")
    check_openclaw_json(result)
    
    print("📡 检查 Agent 文件...")
    check_agent_files(result)
    
    print("📡 检查 Skills 详细依赖...")
    check_skills(result)
    
    print("📡 检查 MCP...")
    check_mcp(result)
    
    print("📡 检查 API Keys...")
    check_api_keys(result)
    
    print("📡 检查权限...")
    check_permissions(result)
    
    # 输出报告
    print("\n" + "="*50)
    print(result.report())
    
    # 返回码
    errors = [i for i in result.issues if i['severity'] == 'error']
    if errors:
        print(f"\n⚠️ 发现 {len(errors)} 个错误，建议修复")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
