#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session Reset Tool - OpenClaw Session 管理工具
Phase 1: Python 脚本版本
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# 配置
OPENCLAW_BASE = Path.home() / ".openclaw"
AGENTS_DIR = OPENCLAW_BASE / "agents"
BACKUP_DIR = OPENCLAW_BASE / "session-backups"

# 配置路径
CONFIG_PATH = OPENCLAW_BASE / "session-reset-config.json"

# 默认 agents（如果没有配置文件）
DEFAULT_AGENTS = []


def discover_agents() -> List[str]:
    """自动发现所有 agents"""
    agents = []
    if not AGENTS_DIR.exists():
        return agents
    
    for agent_dir in AGENTS_DIR.iterdir():
        if agent_dir.is_dir() and (agent_dir / "sessions").exists():
            agents.append(agent_dir.name)
    
    return sorted(agents)


def load_config() -> Dict:
    """加载配置"""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}


def save_config(config: Dict):
    """保存配置"""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)


def init_config():
    """初始化配置 - 交互式选择 agents"""
    print_banner()
    
    print(f"\n{Colors.CYAN}🔧 初始化 Session Reset 配置{Colors.END}\n")
    
    # 发现 agents
    agents = discover_agents()
    
    if not agents:
        print(f"{Colors.YELLOW}⚠️  未发现任何 agents{Colors.END}")
        print(f"   请确保 OpenClaw 已正确安装并有 agents 配置")
        return False
    
    print(f"{Colors.GREEN}✓{Colors.END} 发现 {len(agents)} 个 agents:\n")
    
    for i, agent in enumerate(agents, 1):
        sessions = get_session_files(agent)
        session_count = len(sessions)
        print(f"  {i}. {agent:<15} ({session_count} sessions)")
    
    print(f"\n{Colors.CYAN}选择导入方式:{Colors.END}")
    print(f"  1. 导入全部 agents")
    print(f"  2. 多选 agents")
    print(f"  3. 取消初始化")
    
    choice = input(f"\n{Colors.YELLOW}请选择 (1/2/3): {Colors.END}").strip()
    
    selected_agents = []
    
    if choice == "1":
        selected_agents = agents
        print(f"\n{Colors.GREEN}✓ 已选择全部 {len(agents)} 个 agents{Colors.END}")
    
    elif choice == "2":
        print(f"\n{Colors.CYAN}请输入要导入的 agents 编号（逗号分隔，如: 1,3,5）:{Colors.END}")
        indices = input("编号: ").strip()
        
        try:
            for idx in indices.split(","):
                idx = int(idx.strip()) - 1
                if 0 <= idx < len(agents):
                    selected_agents.append(agents[idx])
        except:
            print(f"{Colors.RED}✗ 输入格式错误{Colors.END}")
            return False
        
        if selected_agents:
            print(f"\n{Colors.GREEN}✓ 已选择 {len(selected_agents)} 个 agents:{Colors.END}")
            for agent in selected_agents:
                print(f"   - {agent}")
    
    elif choice == "3":
        print(f"{Colors.YELLOW}已取消初始化{Colors.END}")
        return False
    
    else:
        print(f"{Colors.RED}✗ 无效选择{Colors.END}")
        return False
    
    if not selected_agents:
        print(f"{Colors.RED}✗ 未选择任何 agents{Colors.END}")
        return False
    
    # 保存配置
    config = {
        "default_agents": selected_agents,
        "initialized_at": datetime.now().isoformat(),
    }
    save_config(config)
    
    print(f"\n{Colors.GREEN}✓ 配置已保存到: {CONFIG_PATH}{Colors.END}")
    print(f"\n现在可以使用:")
    print(f"  reset-session --scope agents     # 重置配置的 agents")
    print(f"  reset-session --help             # 查看所有命令")
    
    return True


def get_default_agents() -> List[str]:
    """获取默认 agents（优先从配置读取）"""
    config = load_config()
    if config.get("default_agents"):
        return config["default_agents"]
    
    # 如果没有配置，返回空列表
    return []


class Colors:
    """终端颜色"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_banner():
    """打印标题"""
    print(f"""
{Colors.CYAN}╔══════════════════════════════════════════════════════════════╗
║           OpenClaw Session Reset Tool v1.0                   ║
╚══════════════════════════════════════════════════════════════╝{Colors.END}
""")


def get_session_files(agent_id: str) -> List[Path]:
    """获取指定 agent 的所有 session 文件"""
    sessions_dir = AGENTS_DIR / agent_id / "sessions"
    if not sessions_dir.exists():
        return []
    return list(sessions_dir.glob("*.jsonl"))


def get_all_sessions(scope: str = "default") -> Dict[str, List[Dict]]:
    """
    获取所有 session 信息
    
    scope:
        - default: Discord 频道 sessions (默认)
        - all: 全部 sessions
        - agents: 仅六部+秘书
        - cron: 仅 Cron 任务
        - subagent: 仅 Subagent
    """
    sessions = {}
    
    if not AGENTS_DIR.exists():
        return sessions
    
    for agent_dir in AGENTS_DIR.iterdir():
        if not agent_dir.is_dir():
            continue
        
        agent_id = agent_dir.name
        sessions_dir = agent_dir / "sessions"
        
        if not sessions_dir.exists():
            continue
        
        agent_sessions = []
        for session_file in sessions_dir.glob("*.jsonl"):
            # 解析 session 信息
            session_info = parse_session_file(session_file)
            
            # 根据 scope 过滤
            if scope == "default":
                # 默认：Discord 频道，排除 cron/subagent
                if session_info.get("kind") in ["cron", "subagent"]:
                    continue
            elif scope == "agents":
                # 仅配置的默认 agents
                default_agents = get_default_agents()
                if not default_agents:
                    print(f"{Colors.YELLOW}⚠️  未配置默认 agents，请先运行: reset-session --init{Colors.END}")
                    return {}
                if agent_id not in default_agents:
                    continue
                if session_info.get("kind") in ["cron", "subagent"]:
                    continue
            elif scope == "cron":
                if session_info.get("kind") != "cron":
                    continue
            elif scope == "subagent":
                if session_info.get("kind") != "subagent":
                    continue
            elif scope.startswith("agent:"):
                # 指定 agent
                target_agent = scope.replace("agent:", "")
                if agent_id != target_agent:
                    continue
            
            agent_sessions.append(session_info)
        
        if agent_sessions:
            sessions[agent_id] = agent_sessions
    
    return sessions


def parse_session_file(session_file: Path) -> Dict:
    """解析 session 文件，提取元数据"""
    info = {
        "file": session_file,
        "agent": session_file.parent.parent.name,
        "session_id": session_file.stem,
        "size": session_file.stat().st_size,
        "modified": datetime.fromtimestamp(session_file.stat().st_mtime),
    }
    
    # 尝试从文件名或内容推断类型
    # 简单启发：通过 agent 和 session key 模式判断
    info["kind"] = infer_session_kind(session_file)
    
    # 统计 tokens (估算)
    info["tokens"] = estimate_tokens(session_file)
    
    return info


def infer_session_kind(session_file: Path) -> str:
    """推断 session 类型"""
    # 通过分析文件路径和可能的 session key 推断
    # 这是一个简化版本，实际可以通过解析 session key 更精确判断
    
    agent_dir = session_file.parent.parent
    
    # 读取第一行获取 session key 信息
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if first_line:
                data = json.loads(first_line)
                session_key = data.get("sessionKey", "")
                
                if ":cron:" in session_key:
                    return "cron"
                elif ":subagent:" in session_key:
                    return "subagent"
                elif ":discord:" in session_key:
                    return "discord"
    except:
        pass
    
    return "other"


def estimate_tokens(session_file: Path) -> int:
    """估算 session 的 tokens 数量"""
    try:
        # 读取最后一条记录，通常包含 token 统计
        with open(session_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if lines:
                last_line = lines[-1]
                data = json.loads(last_line)
                return data.get("totalTokens", 0)
    except:
        pass
    
    # 无法读取时按文件大小估算 (粗略: 4 bytes/token)
    return session_file.stat().st_size // 4


def create_backup(sessions: Dict[str, List[Dict]]) -> Path:
    """创建备份"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / timestamp
    backup_path.mkdir(parents=True, exist_ok=True)
    
    manifest = {
        "timestamp": timestamp,
        "created_at": datetime.now().isoformat(),
        "agents": {},
    }
    
    total_files = 0
    total_size = 0
    
    for agent_id, agent_sessions in sessions.items():
        agent_backup_dir = backup_path / agent_id
        agent_backup_dir.mkdir(exist_ok=True)
        
        manifest["agents"][agent_id] = []
        
        for session in agent_sessions:
            src_file = session["file"]
            dst_file = agent_backup_dir / src_file.name
            
            shutil.copy2(src_file, dst_file)
            
            manifest["agents"][agent_id].append({
                "session_id": session["session_id"],
                "file": src_file.name,
                "size": session["size"],
                "tokens": session["tokens"],
            })
            
            total_files += 1
            total_size += session["size"]
    
    # 保存清单
    manifest["total_files"] = total_files
    manifest["total_size"] = total_size
    
    with open(backup_path / "backup.manifest", 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    return backup_path


def display_preview(sessions: Dict[str, List[Dict]], dry_run: bool = True):
    """显示预览信息"""
    print(f"\n{Colors.CYAN}📋 将要处理的 Sessions:{Colors.END}\n")
    
    total_sessions = 0
    total_tokens = 0
    total_size = 0
    
    print(f"{'Agent':<12} {'Session ID':<38} {'Tokens':<12} {'Size':<10}")
    print("-" * 80)
    
    for agent_id in sorted(sessions.keys()):
        agent_sessions = sessions[agent_id]
        for session in agent_sessions:
            tokens_str = f"{session['tokens']:,}" if session['tokens'] else "-"
            size_str = f"{session['size'] / 1024:.1f} KB"
            print(f"{agent_id:<12} {session['session_id']:<38} {tokens_str:<12} {size_str:<10}")
            total_sessions += 1
            total_tokens += session['tokens']
            total_size += session['size']
    
    print("-" * 80)
    print(f"{'Total':<12} {'':<38} {total_tokens:>12,} {total_size / 1024 / 1024:>9.2f} MB")
    
    if dry_run:
        print(f"\n{Colors.YELLOW}⚠️  这是预览模式，未执行任何操作。{Colors.END}")
    
    return total_sessions, total_tokens, total_size


def confirm_action(message: str = "确认执行?") -> bool:
    """请求用户确认"""
    print(f"\n{Colors.YELLOW}⚠️  {message} (yes/no): {Colors.END}", end="")
    response = input().strip().lower()
    return response in ['yes', 'y']


def execute_reset(sessions: Dict[str, List[Dict]]) -> Tuple[int, int]:
    """执行重置"""
    success = 0
    failed = 0
    
    print(f"\n{Colors.CYAN}🔄 执行重置...{Colors.END}\n")
    
    for agent_id, agent_sessions in sessions.items():
        for session in agent_sessions:
            try:
                session_file = session["file"]
                session_file.unlink()
                print(f"  {Colors.GREEN}✓{Colors.END} {agent_id}/{session['session_id']}")
                success += 1
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.END} {agent_id}/{session['session_id']}: {e}")
                failed += 1
    
    return success, failed


def list_backups():
    """列出所有备份"""
    if not BACKUP_DIR.exists():
        print(f"{Colors.YELLOW}暂无备份记录{Colors.END}")
        return
    
    backups = sorted(BACKUP_DIR.iterdir(), key=lambda x: x.name, reverse=True)
    
    if not backups:
        print(f"{Colors.YELLOW}暂无备份记录{Colors.END}")
        return
    
    print(f"\n{Colors.CYAN}📦 备份列表:{Colors.END}\n")
    print(f"{'Timestamp':<20} {'Agents':<8} {'Files':<8} {'Size':<12} {'Date'}")
    print("-" * 70)
    
    for backup in backups:
        manifest_file = backup / "backup.manifest"
        if not manifest_file.exists():
            continue
        
        try:
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
            
            agents_count = len(manifest.get("agents", {}))
            files_count = manifest.get("total_files", 0)
            size_mb = manifest.get("total_size", 0) / 1024 / 1024
            created = manifest.get("created_at", "")[:19].replace("T", " ")
            
            print(f"{backup.name:<20} {agents_count:<8} {files_count:<8} {size_mb:>8.2f} MB  {created}")
        except:
            pass


def restore_backup(timestamp: str) -> bool:
    """从备份恢复"""
    backup_path = BACKUP_DIR / timestamp
    manifest_file = backup_path / "backup.manifest"
    
    if not manifest_file.exists():
        print(f"{Colors.RED}✗ 备份不存在: {timestamp}{Colors.END}")
        return False
    
    with open(manifest_file, 'r') as f:
        manifest = json.load(f)
    
    print(f"\n{Colors.CYAN}📦 备份信息:{Colors.END}")
    print(f"  时间戳: {timestamp}")
    print(f"  创建时间: {manifest.get('created_at', 'N/A')}")
    print(f"  Agents: {len(manifest.get('agents', {}))}")
    print(f"  文件数: {manifest.get('total_files', 0)}")
    
    if not confirm_action("确认恢复此备份? (将覆盖现有 session 文件)"):
        print(f"{Colors.YELLOW}已取消{Colors.END}")
        return False
    
    print(f"\n{Colors.CYAN}🔄 执行恢复...{Colors.END}\n")
    
    success = 0
    failed = 0
    
    for agent_id, sessions in manifest.get("agents", {}).items():
        agent_sessions_dir = AGENTS_DIR / agent_id / "sessions"
        agent_sessions_dir.mkdir(parents=True, exist_ok=True)
        
        for session_info in sessions:
            src_file = backup_path / agent_id / session_info["file"]
            dst_file = agent_sessions_dir / session_info["file"]
            
            try:
                shutil.copy2(src_file, dst_file)
                print(f"  {Colors.GREEN}✓{Colors.END} {agent_id}/{session_info['session_id']}")
                success += 1
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.END} {agent_id}/{session_info['session_id']}: {e}")
                failed += 1
    
    print(f"\n{Colors.GREEN}✓ 恢复完成: {success} 成功, {failed} 失败{Colors.END}")
    return True


def cleanup_backups(days: int = 30, max_count: int = 10):
    """清理旧备份"""
    if not BACKUP_DIR.exists():
        return
    
    backups = sorted(BACKUP_DIR.iterdir(), key=lambda x: x.name)
    
    if not backups:
        print(f"{Colors.YELLOW}暂无备份可清理{Colors.END}")
        return
    
    cutoff_date = datetime.now() - timedelta(days=days)
    to_delete = []
    to_keep = []
    
    for backup in backups:
        try:
            backup_time = datetime.strptime(backup.name, "%Y%m%d_%H%M%S")
            if backup_time < cutoff_date:
                to_delete.append(backup)
            else:
                to_keep.append(backup)
        except:
            pass
    
    # 保留最新的 max_count 个
    if len(to_keep) > max_count:
        to_delete.extend(to_keep[:-max_count])
        to_keep = to_keep[-max_count:]
    
    if not to_delete:
        print(f"{Colors.GREEN}✓ 没有需要清理的备份{Colors.END}")
        return
    
    print(f"\n{Colors.CYAN}🧹 将要清理的备份:{Colors.END}")
    for backup in to_delete:
        size = sum(f.stat().st_size for f in backup.rglob('*') if f.is_file())
        print(f"  {backup.name} ({size / 1024 / 1024:.2f} MB)")
    
    if confirm_action("确认删除这些备份?"):
        for backup in to_delete:
            shutil.rmtree(backup)
        print(f"{Colors.GREEN}✓ 已清理 {len(to_delete)} 个备份{Colors.END}")
    else:
        print(f"{Colors.YELLOW}已取消{Colors.END}")


def main():
    parser = argparse.ArgumentParser(
        description="OpenClaw Session Reset Tool - 安全重置 agent sessions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --init                          # 初始化配置（首次使用）
  %(prog)s --scope default --dry-run       # 预览将要重置的内容
  %(prog)s --scope default                 # 重置所有 Discord 频道 sessions
  %(prog)s --scope all                     # 重置所有 sessions (含 cron/subagent)
  %(prog)s --scope agents                  # 重置配置的默认 agents
  %(prog)s --scope cron                    # 仅重置 cron 任务
  %(prog)s --scope main,libu,hubu          # 重置指定 agents
  %(prog)s --list-backups                  # 查看备份列表
  %(prog)s --restore 20250305_143022       # 恢复到指定备份
  %(prog)s --cleanup                       # 清理旧备份 (30天/最多10个)
        """
    )
    
    parser.add_argument(
        "--init",
        action="store_true",
        help="初始化配置，交互式选择默认 agents"
    )
    parser.add_argument(
        "--scope",
        default="default",
        help="重置范围: default(默认,Discord频道), all(全部), agents(配置的默认agents), cron(仅cron), subagent(仅subagent), 或 agent1,agent2..."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览模式，不执行实际重置"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制执行，跳过确认"
    )
    parser.add_argument(
        "--list-backups",
        action="store_true",
        help="列出所有备份"
    )
    parser.add_argument(
        "--restore",
        metavar="TIMESTAMP",
        help="从指定备份恢复"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="清理旧备份"
    )
    parser.add_argument(
        "--cleanup-days",
        type=int,
        default=30,
        help="清理 N 天前的备份 (默认: 30)"
    )
    parser.add_argument(
        "--cleanup-max",
        type=int,
        default=10,
        help="最多保留 N 个备份 (默认: 10)"
    )
    
    args = parser.parse_args()
    
    # 处理初始化命令
    if args.init:
        success = init_config()
        sys.exit(0 if success else 1)
    
    print_banner()
    
    # 处理备份相关命令
    if args.list_backups:
        list_backups()
        return
    
    if args.restore:
        restore_backup(args.restore)
        return
    
    if args.cleanup:
        cleanup_backups(args.cleanup_days, args.cleanup_max)
        return
    
    # 解析 scope
    if "," in args.scope:
        # 指定多个 agents
        scope = args.scope
    else:
        scope = args.scope
    
    # 获取 sessions
    if "," in scope:
        # 多 agent 模式
        sessions = {}
        for agent_id in scope.split(","):
            agent_id = agent_id.strip()
            agent_sessions = get_session_files(agent_id)
            if agent_sessions:
                sessions[agent_id] = [parse_session_file(f) for f in agent_sessions]
    else:
        sessions = get_all_sessions(scope)
    
    if not sessions:
        print(f"{Colors.YELLOW}⚠️  未找到符合条件的 sessions{Colors.END}")
        return
    
    # 显示预览
    total_sessions, total_tokens, total_size = display_preview(sessions, args.dry_run)
    
    if args.dry_run:
        return
    
    # 请求确认
    if not args.force:
        if not confirm_action(f"确认重置 {total_sessions} 个 sessions?"):
            print(f"{Colors.YELLOW}已取消{Colors.END}")
            return
    
    # 创建备份
    print(f"\n{Colors.CYAN}📦 创建备份...{Colors.END}")
    backup_path = create_backup(sessions)
    print(f"  {Colors.GREEN}✓{Colors.END} 备份已保存: {backup_path}")
    
    # 执行重置
    success, failed = execute_reset(sessions)
    
    # 结果
    print(f"\n{Colors.CYAN}📊 执行结果:{Colors.END}")
    print(f"  成功: {Colors.GREEN}{success}{Colors.END}")
    print(f"  失败: {Colors.RED}{failed}{Colors.END}")
    
    if failed == 0:
        print(f"\n{Colors.GREEN}✓ Session 重置完成！{Colors.END}")
        print(f"  下次消息触发时将自动创建新的 sessions")
    else:
        print(f"\n{Colors.YELLOW}⚠️ 部分 sessions 重置失败，请检查日志{Colors.END}")


if __name__ == "__main__":
    main()
