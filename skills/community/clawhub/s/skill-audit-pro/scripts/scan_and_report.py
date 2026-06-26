#!/usr/bin/env python3
"""
Scan all installed skills and send security report to all active channels.
This script automatically discovers active channels and sends reports to all of them.
"""

import os
import sys
import json
from pathlib import Path

# Add scripts path
sys.path.insert(0, Path(__file__).parent.parent)

from skill_audit import SkillScanner

def get_openclaw_skills_dir():
    """Find the OpenClaw skills directory with installed skills."""
    # Try to find skills in npm package FIRST (these are the "ready" skills)
    npm_base = Path.home() / ".local/share/pnpm/global/5"
    if npm_base.exists():
        for openclaw_dir in npm_base.glob(".pnpm/openclaw@*/node_modules/openclaw"):
            skills_dir = openclaw_dir / "skills"
            if skills_dir.exists() and any(skills_dir.iterdir()):
                return skills_dir
    
    # Fallback: check workspace skills directory
    possible_paths = [
        Path.home() / ".openclaw" / "workspace" / "skills",
        Path.home() / ".openclaw" / "skills",
        Path("/root/.openclaw/skills"),
    ]
    
    for p in possible_paths:
        if p.exists() and any(p.iterdir()):
            return p
    
    return possible_paths[0]

def get_active_channels():
    """Discover all active channels from session configurations."""
    channels = []
    
    # Try to read sessions.json to find active channels
    sessions_file = Path.home() / ".openclaw" / "agents" / "main" / "sessions" / "sessions.json"
    
    if sessions_file.exists():
        try:
            with open(sessions_file) as f:
                sessions = json.load(f)
            
            for session_key, info in sessions.items():
                delivery = info.get('deliveryContext', {})
                channel = delivery.get('channel')
                to = delivery.get('to')
                
                if channel and to:
                    # Deduplicate by channel+to
                    entry = {'channel': channel, 'to': to}
                    if entry not in channels:
                        channels.append(entry)
        except Exception as e:
            print(f"Warning: Could not read sessions: {e}", file=sys.stderr)
    
    # Always add default channels if they seem active
    # Check openclaw config for enabled channels
    config_file = Path.home() / ".openclaw" / "openclaw.json"
    if config_file.exists():
        try:
            with open(config_file) as f:
                config = json.load(f)
            
            channel_configs = config.get('channels', {})
            for channel_name, channel_cfg in channel_configs.items():
                if channel_cfg.get('enabled'):
                    # Try to find a recent session for this channel
                    for session_key, info in sessions.items() if 'sessions' in dir() else []:
                        if info.get('lastChannel') == channel_name:
                            to = info.get('lastTo', '')
                            if to:
                                entry = {'channel': channel_name, 'to': to}
                                if entry not in channels:
                                    channels.append(entry)
        except Exception as e:
            print(f"Warning: Could not read config: {e}", file=sys.stderr)
    
    return channels

def format_report(scanner_path=None):
    """Scan skills and format a report."""
    
    if scanner_path is None:
        scanner_path = get_openclaw_skills_dir()
    
    scanner_path = Path(scanner_path)
    
    # Find all .skill files and skill directories
    skills = []
    exclude = {'skill-audit'}
    
    if scanner_path.is_file() and scanner_path.suffix == '.skill':
        if scanner_path.stem not in exclude:
            skills.append(scanner_path)
    else:
        for item in scanner_path.iterdir():
            if item.is_dir() and (item / "SKILL.md").exists():
                if item.name not in exclude:
                    skills.append(item)
            elif item.suffix == '.skill':
                if item.stem not in exclude:
                    skills.append(item)
    
    # Also scan extensions (like feishu skills)
    npm_base = Path.home() / ".local/share/pnpm/global/5"
    for openclaw_dir in npm_base.glob(".pnpm/openclaw@*/node_modules/openclaw"):
        extensions_dir = openclaw_dir / "extensions"
        if extensions_dir.exists():
            for ext_dir in extensions_dir.iterdir():
                ext_skills_dir = ext_dir / "skills"
                if ext_skills_dir.exists():
                    for item in ext_skills_dir.iterdir():
                        if item.is_dir() and (item / "SKILL.md").exists():
                            if item.name not in exclude:
                                skills.append(item)
    
    # Scan each skill
    all_issues = []
    skill_results = []
    
    for skill_path in skills:
        scanner = SkillScanner(str(skill_path))
        issues, summary = scanner.scan_skill()
        
        skill_name = skill_path.name
        
        # Only count CRITICAL, HIGH, MEDIUM as real issues
        real_issues = [i for i in issues if i["severity"] in ("CRITICAL", "HIGH", "MEDIUM")]
        
        if issues:
            all_issues.extend([(skill_name, i) for i in issues])
            status = "🔴 ISSUE" if scanner.should_block_install() else ("🟠 WARNING" if real_issues else "✅ CLEAN")
        else:
            status = "✅ CLEAN"
        
        skill_results.append({
            "name": skill_name,
            "status": status,
            "summary": summary,
            "issues": real_issues
        })
    
    # Format report
    report = []
    report.append("🛡️ *Skill Audit Report*")
    report.append("*AI技能安全扫描 — 守护你的Agent*")
    report.append("━━━━━━━━━━━━━━━━━━━━")
    
    # Summary
    total = len(skill_results)
    clean = sum(1 for s in skill_results if "CLEAN" in s["status"])
    issues_found = sum(1 for s in skill_results if "ISSUE" in s["status"] or "WARNING" in s["status"])
    
    report.append(f"\n📊 *扫描概况*")
    report.append(f"已扫描：{total} 个技能")
    report.append(f"✅ 安全：{clean} 个")
    report.append(f"⚠️ 有隐患：{issues_found} 个")
    
    if issues_found == 0:
        report.append("\n🎉 所有技能都安全！")
        return "\n".join(report)
    
    # List skills with issues
    report.append(f"\n📋 *隐患详情*")
    
    if not skill_results:
        report.append("📦 暂未安装任何技能")
        report.append("使用 clawhub install <skill> 安装技能后再扫描")
    
    for skill in skill_results:
        if "ISSUE" in skill["status"] or "WARNING" in skill["status"]:
            report.append(f"\n🔸 *{skill['name']}*")
            
            critical = skill['summary']['CRITICAL']
            high = skill['summary']['HIGH']
            medium = skill['summary']['MEDIUM']
            
            if critical > 0:
                report.append(f"   🔴 严重 {critical} 个")
            if high > 0:
                report.append(f"   🟠 高危 {high} 个")
            if medium > 0:
                report.append(f"   🟡 中危 {medium} 个")
            
            # Top issues
            crit_issues = [i for i in skill['issues'] if i['severity'] == 'CRITICAL'][:1]
            high_issues = [i for i in skill['issues'] if i['severity'] == 'HIGH'][:1]
            
            for issue in crit_issues + high_issues:
                report.append(f"   → {issue['check']}")
    
    # Recommendations
    report.append(f"\n💡 *处理建议*")
    critical_skills = [s for s in skill_results if s['summary']['CRITICAL'] > 0]
    if critical_skills:
        report.append("🔴 立即卸载以下技能：")
        for s in critical_skills:
            report.append(f"   /remove {s['name']}")
        report.append("\n这些技能存在严重安全隐患！")
    
    high_skills = [s for s in skill_results if s['summary']['HIGH'] > 0 and s['summary']['CRITICAL'] == 0]
    if high_skills:
        report.append("🟠 建议检查以下技能：")
        for s in high_skills:
            report.append(f"   {s['name']}")
        report.append("确认来源可信后再使用")
    
    report.append("\n━━━━━━━━━━━━━━━━━━━━")
    report.append("💡 输入 /scan 随时重新扫描")
    
    return "\n".join(report)

def main():
    # Get active channels
    channels = get_active_channels()
    
    # Generate report
    report = format_report()
    
    # Output for each channel (in JSON format for OpenClaw to pickup)
    # The cron job uses --announce which expects a text output
    # So we just print the report - OpenClaw will deliver it via the configured channel
    
    print(report)
    print(f"\n<!-- CHANNELS: {json.dumps(channels)} -->")

if __name__ == "__main__":
    main()
