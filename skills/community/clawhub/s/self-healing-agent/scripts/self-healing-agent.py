#!/usr/bin/env python3
"""
self-healing-agent.py — Self-Recovery and Auto-Repair for OpenClaw Agents
Built by GetAgentIQ — https://getagentiq.ai

Monitors agent health, detects failures, diagnoses root causes,
and applies automatic fixes. The watchdog that keeps your agent running.
"""

import argparse
import datetime
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# ─── Constants ───────────────────────────────────────────────────────────────

WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
HEAL_LOG = os.path.join(MEMORY_DIR, "self-healing-log.json")

# Thresholds
MAX_MEMORY_FILE_MB = 1.0
MAX_SESSION_MB = 2.0
WARN_SESSION_MB = 1.0
MAX_CONSECUTIVE_ERRORS = 3
CRON_STUCK_HOURS = 2

# ─── Utility ─────────────────────────────────────────────────────────────────

def file_size_mb(path):
    """Get file size in MB."""
    try:
        return os.path.getsize(path) / (1024 * 1024)
    except OSError:
        return 0


def load_json(path):
    """Safely load a JSON file."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def save_json(path, data):
    """Save JSON data to file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


def log_action(issue, diagnosis, action, result):
    """Log a healing action to the heal log."""
    entry = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "issue": issue,
        "diagnosis": diagnosis,
        "action": action,
        "result": result,
    }

    log = []
    if os.path.exists(HEAL_LOG):
        log = load_json(HEAL_LOG) or []

    log.append(entry)

    # Keep last 500 entries
    if len(log) > 500:
        log = log[-500:]

    save_json(HEAL_LOG, log)
    return entry


class Issue:
    """Represents a detected health issue."""
    def __init__(self, subsystem, severity, title, detail, auto_fixable=False, fix_fn=None):
        self.subsystem = subsystem
        self.severity = severity  # critical, warning, info
        self.title = title
        self.detail = detail
        self.auto_fixable = auto_fixable
        self.fix_fn = fix_fn  # callable that returns (success: bool, message: str)

    def __repr__(self):
        icon = {'critical': '🔴', 'warning': '🟡', 'info': '🔵'}
        fix_tag = ' 🔧' if self.auto_fixable else ''
        return f"{icon.get(self.severity, '❓')} [{self.subsystem}] {self.title}{fix_tag}"


# ─── Health Checks ───────────────────────────────────────────────────────────

def check_cron():
    """Check cron job health."""
    issues = []

    try:
        result = subprocess.run(
            ['openclaw', 'cron', 'list', '--json'],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0:
            issues.append(Issue('cron', 'warning', 'Cannot query cron jobs',
                                f'openclaw cron list failed: {result.stderr[:100]}'))
            return issues

        parsed = json.loads(result.stdout) if result.stdout.strip() else {}
        jobs = parsed.get('jobs', []) if isinstance(parsed, dict) else (parsed if isinstance(parsed, list) else [])

        for job in jobs:
            name = job.get('name', job.get('id', 'unknown'))
            enabled = job.get('enabled', True)
            if not enabled:
                continue

            # Check consecutive errors
            consec_errors = job.get('consecutiveErrors', 0)
            if consec_errors >= MAX_CONSECUTIVE_ERRORS:
                def make_fix(job_id=job.get('id')):
                    def fix():
                        try:
                            r = subprocess.run(
                                ['openclaw', 'cron', 'run', job_id],
                                capture_output=True, text=True, timeout=30
                            )
                            return r.returncode == 0, f"Restarted job {job_id}"
                        except Exception as e:
                            return False, str(e)
                    return fix

                issues.append(Issue(
                    'cron', 'critical',
                    f'Cron job "{name}" has {consec_errors} consecutive errors',
                    f'Job has been failing repeatedly. Last error may indicate a persistent issue.',
                    auto_fixable=True,
                    fix_fn=make_fix(),
                ))

            # Check for stuck jobs (last run duration > threshold)
            last_duration = job.get('lastDurationMs', 0)
            if last_duration > CRON_STUCK_HOURS * 3600 * 1000:
                issues.append(Issue(
                    'cron', 'warning',
                    f'Cron job "{name}" took {last_duration / 1000:.0f}s last run',
                    'Job may be stuck or hitting timeouts.',
                ))

            # Check last run status
            last_status = job.get('lastStatus', '')
            if last_status == 'error':
                issues.append(Issue(
                    'cron', 'warning',
                    f'Cron job "{name}" last run failed',
                    f'Status: {last_status}. Check logs for details.',
                ))

    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as e:
        issues.append(Issue('cron', 'info', 'Cron check unavailable', str(e)))

    return issues


def check_memory():
    """Check memory file health."""
    issues = []

    if not os.path.isdir(MEMORY_DIR):
        issues.append(Issue('memory', 'warning', 'Memory directory missing',
                            f'{MEMORY_DIR} does not exist.'))
        return issues

    # Check individual file sizes
    total_size = 0
    large_files = []
    for f in glob.glob(os.path.join(MEMORY_DIR, '*.md')):
        size = file_size_mb(f)
        total_size += size
        if size > MAX_MEMORY_FILE_MB:
            large_files.append((f, size))

    if large_files:
        for fpath, size in large_files:
            fname = os.path.basename(fpath)

            def make_archive_fix(path=fpath):
                def fix():
                    archive = path + '.archived'
                    try:
                        shutil.copy2(path, archive)
                        # Truncate to last 200 lines
                        with open(path, 'r') as rf:
                            lines = rf.readlines()
                        if len(lines) > 200:
                            with open(path, 'w') as wf:
                                wf.write(f"<!-- Archived {len(lines) - 200} older lines to {os.path.basename(archive)} -->\n")
                                wf.writelines(lines[-200:])
                        return True, f"Archived to {archive}, kept last 200 lines"
                    except IOError as e:
                        return False, str(e)
                return fix

            issues.append(Issue(
                'memory', 'warning',
                f'Memory file "{fname}" is {size:.1f}MB (>{MAX_MEMORY_FILE_MB}MB)',
                'Large memory files slow down agent context loading.',
                auto_fixable=True,
                fix_fn=make_archive_fix(),
            ))

    # Check total memory directory size
    if total_size > 50:
        issues.append(Issue(
            'memory', 'warning',
            f'Total memory directory: {total_size:.1f}MB',
            'Consider archiving old daily files.',
        ))

    # Check MEMORY.md specifically
    memory_md = os.path.join(WORKSPACE, 'MEMORY.md')
    if os.path.exists(memory_md):
        size = file_size_mb(memory_md)
        if size > MAX_MEMORY_FILE_MB:
            issues.append(Issue(
                'memory', 'warning',
                f'MEMORY.md is {size:.1f}MB — consider pruning',
                'Large MEMORY.md increases token usage on every main session.',
            ))

    return issues


def check_config():
    """Check OpenClaw configuration health."""
    issues = []

    if not os.path.exists(CONFIG_PATH):
        issues.append(Issue('config', 'critical', 'Config file missing',
                            f'{CONFIG_PATH} not found.'))
        return issues

    # Check JSON validity
    config = load_json(CONFIG_PATH)
    if config is None:
        # Try to detect common JSON errors
        try:
            with open(CONFIG_PATH, 'r') as f:
                content = f.read()

            # Common fix: trailing commas
            def fix_json():
                fixed = re.sub(r',\s*([}\]])', r'\1', content)
                try:
                    json.loads(fixed)  # verify fix works
                    with open(CONFIG_PATH, 'w') as wf:
                        wf.write(fixed)
                    return True, "Removed trailing commas from JSON"
                except json.JSONDecodeError:
                    return False, "Could not auto-fix JSON syntax"

            issues.append(Issue(
                'config', 'critical',
                'Config file has invalid JSON',
                'openclaw.json cannot be parsed.',
                auto_fixable=True,
                fix_fn=fix_json,
            ))
        except IOError:
            issues.append(Issue('config', 'critical', 'Config file unreadable', ''))
        return issues

    # Check for required fields
    if 'models' not in config and 'channels' not in config:
        issues.append(Issue('config', 'warning', 'Config appears minimal',
                            'No models or channels configured.'))

    return issues


def check_sessions():
    """Check for session health issues."""
    issues = []

    # Check for large session files
    session_dir = os.path.expanduser("~/.openclaw/sessions")
    if os.path.isdir(session_dir):
        for f in glob.glob(os.path.join(session_dir, '*.json')):
            size = file_size_mb(f)
            fname = os.path.basename(f)

            if size > MAX_SESSION_MB:
                def make_clear_fix(path=f):
                    def fix():
                        archive = path + f'.archived-{datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
                        try:
                            shutil.move(path, archive)
                            return True, f"Archived bloated session to {os.path.basename(archive)}"
                        except IOError as e:
                            return False, str(e)
                    return fix

                issues.append(Issue(
                    'sessions', 'critical',
                    f'Session "{fname}" is {size:.1f}MB (emergency threshold)',
                    'Bloated sessions cause timeouts and context loss.',
                    auto_fixable=True,
                    fix_fn=make_clear_fix(),
                ))
            elif size > WARN_SESSION_MB:
                issues.append(Issue(
                    'sessions', 'warning',
                    f'Session "{fname}" is {size:.1f}MB (approaching limit)',
                    'Monitor closely — clear soon to prevent timeout.',
                ))

    # Check for zombie processes
    try:
        result = subprocess.run(
            ['ps', 'aux'], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            zombie_count = sum(1 for line in result.stdout.split('\n') if ' Z ' in line or '<defunct>' in line)
            if zombie_count > 5:
                issues.append(Issue(
                    'sessions', 'warning',
                    f'{zombie_count} zombie processes detected',
                    'Zombie processes consume PIDs. Consider reaping.',
                ))
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    return issues


def check_skills():
    """Check installed skills for issues."""
    issues = []
    skills_dir = os.path.join(WORKSPACE, "skills")

    if not os.path.isdir(skills_dir):
        return issues

    for skill_dir in sorted(os.listdir(skills_dir)):
        skill_path = os.path.join(skills_dir, skill_dir)
        if not os.path.isdir(skill_path):
            continue

        # Check SKILL.md exists
        skill_md = os.path.join(skill_path, "SKILL.md")
        if not os.path.exists(skill_md):
            issues.append(Issue(
                'skills', 'warning',
                f'Skill "{skill_dir}" missing SKILL.md',
                'Skills require a SKILL.md file to function.',
            ))
            continue

        # Check for Python syntax errors in scripts
        scripts_dir = os.path.join(skill_path, "scripts")
        if os.path.isdir(scripts_dir):
            for py_file in glob.glob(os.path.join(scripts_dir, "*.py")):
                try:
                    result = subprocess.run(
                        ['python3', '-m', 'py_compile', py_file],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode != 0:
                        issues.append(Issue(
                            'skills', 'warning',
                            f'Syntax error in {skill_dir}/{os.path.basename(py_file)}',
                            result.stderr[:200] if result.stderr else 'Compilation failed.',
                        ))
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    pass

    return issues


def check_network():
    """Check network connectivity to key endpoints."""
    issues = []

    endpoints = [
        ("https://api.anthropic.com", "Anthropic API"),
        ("https://api.openai.com", "OpenAI API"),
        ("https://ollama.com", "Ollama Registry"),
    ]

    for url, name in endpoints:
        try:
            result = subprocess.run(
                ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '5', url],
                capture_output=True, text=True, timeout=10
            )
            status = result.stdout.strip()
            if status and int(status) >= 500:
                issues.append(Issue(
                    'network', 'warning',
                    f'{name} returning HTTP {status}',
                    f'Endpoint {url} may be experiencing issues.',
                ))
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            issues.append(Issue(
                'network', 'info',
                f'Cannot reach {name}',
                f'Network check for {url} timed out.',
            ))

    return issues


# ─── Commands ────────────────────────────────────────────────────────────────

def cmd_check(args):
    """Run health checks."""
    print("🏥 Self-Healing Agent — Health Check")
    print("=" * 50)

    target = getattr(args, 'target', None)

    checkers = {
        'cron': ('⏰ Cron Jobs', check_cron),
        'memory': ('🧠 Memory', check_memory),
        'config': ('⚙️  Config', check_config),
        'sessions': ('💬 Sessions', check_sessions),
        'skills': ('🔧 Skills', check_skills),
        'network': ('🌐 Network', check_network),
    }

    all_issues = []

    for key, (label, checker) in checkers.items():
        if target and target != key:
            continue
        print(f"\n{label}...")
        issues = checker()
        all_issues.extend(issues)
        if not issues:
            print(f"  ✅ Healthy")
        else:
            for issue in issues:
                print(f"  {issue}")
                if args.verbose if hasattr(args, 'verbose') else False:
                    print(f"     {issue.detail}")

    # Summary
    print(f"\n{'=' * 50}")
    crits = sum(1 for i in all_issues if i.severity == 'critical')
    warns = sum(1 for i in all_issues if i.severity == 'warning')
    fixable = sum(1 for i in all_issues if i.auto_fixable)

    if not all_issues:
        print("✅ All systems healthy!")
    else:
        print(f"📊 {len(all_issues)} issues: 🔴 {crits} critical, 🟡 {warns} warnings")
        if fixable:
            print(f"🔧 {fixable} auto-fixable. Run: self-healing-agent heal")

    if hasattr(args, 'json') and args.json:
        output = [{
            'subsystem': i.subsystem,
            'severity': i.severity,
            'title': i.title,
            'auto_fixable': i.auto_fixable,
        } for i in all_issues]
        print(json.dumps(output, indent=2))

    return all_issues


def cmd_heal(args):
    """Auto-heal detected issues."""
    print("🔧 Self-Healing Agent — Auto-Heal")
    print("=" * 50)

    dry_run = getattr(args, 'dry_run', False)
    if dry_run:
        print("🏃 DRY RUN — no changes\n")

    # Run all checks
    all_issues = []
    for checker in [check_cron, check_memory, check_config, check_sessions]:
        all_issues.extend(checker())

    fixable = [i for i in all_issues if i.auto_fixable and i.fix_fn]

    if not fixable:
        print("\n✅ Nothing to heal — all clear!")
        return

    print(f"\n🩺 Found {len(fixable)} auto-fixable issues:\n")

    healed = 0
    failed = 0

    for issue in fixable:
        print(f"  🔧 {issue.title}")

        if dry_run:
            print(f"     [DRY RUN] Would apply fix")
            continue

        try:
            success, message = issue.fix_fn()
            if success:
                print(f"     ✅ {message}")
                log_action(issue.title, issue.detail, message, "success")
                healed += 1
            else:
                print(f"     ❌ {message}")
                log_action(issue.title, issue.detail, message, "failed")
                failed += 1
        except Exception as e:
            print(f"     ❌ Error: {e}")
            log_action(issue.title, issue.detail, str(e), "error")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"✅ Healed: {healed} | ❌ Failed: {failed}")

    if healed > 0:
        print(f"📝 Actions logged to: {HEAL_LOG}")


def cmd_monitor(args):
    """Continuous monitoring mode."""
    interval = getattr(args, 'interval', 300)
    max_heals = getattr(args, 'max_heals', 5)

    print(f"👁️  Self-Healing Agent — Monitor Mode")
    print(f"   Interval: {interval}s | Max heals per cycle: {max_heals}")
    print(f"   Press Ctrl+C to stop\n")

    cycle = 0
    try:
        while True:
            cycle += 1
            now = datetime.datetime.utcnow().strftime('%H:%M:%S')
            print(f"[{now}] Cycle {cycle}...")

            # Run checks
            all_issues = []
            for checker in [check_cron, check_memory, check_config, check_sessions]:
                all_issues.extend(checker())

            fixable = [i for i in all_issues if i.auto_fixable and i.fix_fn]

            if not all_issues:
                print(f"  ✅ All healthy")
            else:
                crits = sum(1 for i in all_issues if i.severity == 'critical')
                print(f"  ⚠️  {len(all_issues)} issues ({crits} critical)")

                # Auto-heal up to max_heals
                for issue in fixable[:max_heals]:
                    try:
                        success, msg = issue.fix_fn()
                        status = "✅" if success else "❌"
                        print(f"  {status} Healed: {issue.title} — {msg}")
                        log_action(issue.title, issue.detail, msg,
                                   "success" if success else "failed")
                    except Exception as e:
                        print(f"  ❌ Error healing {issue.title}: {e}")

            print(f"  ⏳ Next check in {interval}s...")
            time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n\n👋 Monitor stopped after {cycle} cycles.")


def cmd_report(args):
    """Generate health report from heal log."""
    print("📊 Self-Healing Agent — Health Report")
    print("=" * 50)

    if not os.path.exists(HEAL_LOG):
        print("\nNo healing log found. Run `self-healing-agent heal` first.")
        return

    log = load_json(HEAL_LOG) or []
    if not log:
        print("\nHealing log is empty.")
        return

    # Last 24h
    cutoff = (datetime.datetime.utcnow() - datetime.timedelta(hours=24)).isoformat()
    recent = [e for e in log if e.get('timestamp', '') >= cutoff]

    print(f"\n📅 Last 24 hours: {len(recent)} healing actions")

    # Count by result
    success = sum(1 for e in recent if e.get('result') == 'success')
    failed = sum(1 for e in recent if e.get('result') != 'success')
    print(f"   ✅ Successful: {success}")
    print(f"   ❌ Failed: {failed}")

    # Most common issues
    from collections import Counter
    issue_counts = Counter(e.get('issue', 'unknown') for e in recent)
    if issue_counts:
        print(f"\n🔝 Most common issues:")
        for issue, count in issue_counts.most_common(5):
            print(f"   {count}x — {issue}")

    # All-time stats
    print(f"\n📈 All-time: {len(log)} total healing actions")
    total_success = sum(1 for e in log if e.get('result') == 'success')
    if log:
        print(f"   Success rate: {total_success / len(log) * 100:.1f}%")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Self-Healing Agent — Automated Recovery for OpenClaw'
    )
    sub = parser.add_subparsers(dest='command')

    p_check = sub.add_parser('check', help='Run health checks')
    p_check.add_argument('--target', choices=['cron', 'memory', 'config', 'sessions', 'skills', 'network'])
    p_check.add_argument('--json', action='store_true')
    p_check.add_argument('--verbose', '-v', action='store_true')

    p_heal = sub.add_parser('heal', help='Auto-repair detected issues')
    p_heal.add_argument('--dry-run', action='store_true')
    p_heal.add_argument('--aggressive', action='store_true')

    p_monitor = sub.add_parser('monitor', help='Continuous monitoring')
    p_monitor.add_argument('--interval', type=int, default=300)
    p_monitor.add_argument('--max-heals', type=int, default=5)

    sub.add_parser('report', help='Health report from heal log')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    {'check': cmd_check, 'heal': cmd_heal, 'monitor': cmd_monitor, 'report': cmd_report}[args.command](args)


if __name__ == '__main__':
    main()
