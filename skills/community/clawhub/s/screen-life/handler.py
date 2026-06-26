#!/usr/bin/env python3
"""
screen-life: macOS 数字生活日报
包装 orbitos-monitor，提供极简 CLI
"""

import sys
import os
import re
import json
import argparse
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

# 加载 .env（优先级最低，会被已设置的环境变量覆盖）
try:
    from dotenv import load_dotenv
    load_dotenv(Path(__file__).parent / ".env", override=False)
except ImportError:
    pass

MONITOR_HOME = Path.home() / ".orbitos-monitor"
SCRIPTS_DIR = MONITOR_HOME / "scripts"
LOGS_DIR = MONITOR_HOME / "logs"


def ensure_monitor_installed() -> bool:
    return (MONITOR_HOME / "daemon.pid").exists() or SCRIPTS_DIR.exists()


def run_report(date_str: str = None, output_format: str = "md") -> tuple[str, Path | None]:
    """调用 report_generator.py 生成报告，返回 (stdout, 报告文件路径)"""
    report_script = SCRIPTS_DIR / "report_generator.py"
    if not report_script.exists():
        local = Path(__file__).parent / "report.py"
        if local.exists():
            report_script = local
        else:
            return _fallback_report(date_str), None

    # 修复：report_generator.py 接受位置参数，不是 --date 选项
    cmd = [sys.executable, str(report_script)]
    if date_str:
        cmd += [date_str]
    if output_format == "json":
        cmd += ["--format", "json"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        stdout = result.stdout or result.stderr
        return stdout, _parse_report_path(stdout)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return _fallback_report(date_str), None


def _parse_report_path(stdout: str) -> Path | None:
    """从 report_generator.py 的输出中解析报告文件路径"""
    for line in stdout.splitlines():
        if "报告已保存" in line or "report saved" in line.lower():
            # 格式: "  ✅ 报告已保存: /path/to/file.md"
            m = re.search(r"[:：]\s*(/\S+\.md)", line)
            if m:
                p = Path(m.group(1))
                return p if p.exists() else None
    return None


# ─── LLM 配置 ─────────────────────────────────────────────────────────────────

def _get_llm_config() -> dict | None:
    """
    读取 LLM 配置，仅使用 OpenClaw 运行时注入的环境变量：
      OPENCLAW_LLM_API_KEY  — API 密钥
      OPENCLAW_LLM_BASE_URL — 接口地址（兼容标准 Chat Completions 格式）
      OPENCLAW_LLM_MODEL    — 模型标识
    未注入时返回 None，跳过 AI 分析。
    """
    api_key = os.getenv("OPENCLAW_LLM_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv("OPENCLAW_LLM_BASE_URL", "").rstrip("/")
    if not base_url:
        return None

    model = os.getenv("OPENCLAW_LLM_MODEL", "").split("/")[-1]
    if not model:
        return None

    return {"api_key": api_key, "base_url": base_url, "model": model}


def run_llm_analysis(report_path: Path | None, fallback_text: str) -> str:
    """用 LLM 对日报做洞察分析，返回 AI 段落；未配置时返回空字符串"""
    cfg = _get_llm_config()
    if not cfg:
        return ""

    # 优先读完整 markdown，降级用 stdout 摘要
    if report_path and report_path.exists():
        content = report_path.read_text(encoding="utf-8")[:4000]
    else:
        content = fallback_text[:3000]

    try:
        import requests as _req
        resp = _req.post(
            f"{cfg['base_url']}/chat/completions",
            headers={
                "Authorization": f"Bearer {cfg['api_key']}",
                "Content-Type": "application/json",
            },
            json={
                "model": cfg["model"],
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "你是一个个人效率分析助手。根据用户的电脑行为数据，"
                            "给出简洁的洞察和建议。用中文回复，不超过 250 字。"
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "请分析这份数字生活日报，给出 3 条关键洞察和 1 条改进建议：\n\n"
                            + content
                        ),
                    },
                ],
                "max_tokens": 600,
            },
            timeout=30,
        )
        resp.raise_for_status()
        ai_text = resp.json()["choices"][0]["message"]["content"].strip()
        return f"\n\n---\n🤖 AI 洞察\n\n{ai_text}\n"
    except Exception as e:
        return f"\n\n---\n⚠️  AI 分析失败: {e}\n"


def _fallback_report(date_str: str = None) -> str:
    """直接读取 JSONL 日志，生成简单报告"""
    target = date_str or datetime.now().strftime("%Y-%m-%d")
    log_file = LOGS_DIR / f"{target}.jsonl"

    if not log_file.exists():
        return f"⚠️  没有找到 {target} 的记录。请先运行: bash install.sh"

    app_times: dict[str, float] = {}
    total_samples = 0

    with open(log_file) as f:
        for line in f:
            try:
                entry = json.loads(line)
                app = entry.get("app", "Unknown")
                # 跳过系统进程
                if app in ("WindowServer", "Dock", "Finder", "loginwindow", ""):
                    continue
                app_times[app] = app_times.get(app, 0) + 1
                total_samples += 1
            except json.JSONDecodeError:
                continue

    if not app_times:
        return f"📊 {target} 没有有效记录"

    # 排序
    sorted_apps = sorted(app_times.items(), key=lambda x: x[1], reverse=True)

    lines = [f"🖥️  {target} 数字生活日报\n"]
    lines.append("⏱️  应用使用 TOP 5")

    for i, (app, count) in enumerate(sorted_apps[:5], 1):
        minutes = int(count * 0.5)  # 假设每 30s 采样一次
        hours = minutes // 60
        mins = minutes % 60
        pct = count / total_samples * 100 if total_samples else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        time_str = f"{hours}h {mins:02d}m" if hours else f"    {mins:02d}m"
        lines.append(f"  {i}. {app:<20} {time_str}  {bar[:12]}  {pct:.0f}%")

    lines.append(f"\n监控时长: {total_samples * 0.5 / 60:.1f} 小时")
    lines.append(f"采样频率: 每 30 秒\n")
    lines.append("💡 提示: 安装 Whisper/Chrome 历史读取权限可获得更详细报告")

    return "\n".join(lines)


def week_summary() -> str:
    lines = ["📅 本周数字生活汇总\n"]
    today = datetime.now()
    for i in range(7, 0, -1):
        d = today - timedelta(days=i)
        date_str = d.strftime("%Y-%m-%d")
        log_file = LOGS_DIR / f"{date_str}.jsonl"
        if log_file.exists():
            app_times: dict[str, float] = {}
            with open(log_file) as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        app = entry.get("app", "")
                        if app not in ("WindowServer", "Dock", "loginwindow", ""):
                            app_times[app] = app_times.get(app, 0) + 1
                    except Exception:
                        continue
            top = sorted(app_times.items(), key=lambda x: x[1], reverse=True)[:3]
            top_str = " | ".join(f"{a}({int(c*0.5/60)}h)" for a, c in top) if top else "无数据"
            lines.append(f"  {d.strftime('%m/%d %a')}  {top_str}")
        else:
            lines.append(f"  {d.strftime('%m/%d %a')}  （无记录）")

    return "\n".join(lines)


def check_daemon_status() -> str:
    pid_file = MONITOR_HOME / "daemon.pid"
    if not pid_file.exists():
        return "❌ 守护进程未运行 — 请先执行: bash install.sh"

    try:
        pid = int(pid_file.read_text().strip())
        os.kill(pid, 0)
        return f"✅ 守护进程运行中 (PID: {pid})"
    except (ProcessLookupError, ValueError):
        return "⚠️  PID 文件存在但进程不在 — 请执行: bash install.sh restart"


def push_feishu(content: str):
    url = os.getenv("FEISHU_WEBHOOK_URL")
    if not url:
        print("⚠️  未设置 FEISHU_WEBHOOK_URL，跳过推送")
        return
    import requests
    requests.post(url, json={"msg_type": "text", "content": {"text": content}})
    print("✅ 已推送到飞书")


def main():
    parser = argparse.ArgumentParser(
        description="screen-life: 查看你的数字生活日报",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python report.py               # 今日报告
  python report.py --date 2026-04-10
  python report.py --week        # 本周汇总
  python report.py --status      # 检查守护进程状态
        """,
    )
    parser.add_argument("--date", help="指定日期 YYYY-MM-DD，默认今天")
    parser.add_argument("--week", action="store_true", help="显示本周汇总")
    parser.add_argument("--status", action="store_true", help="检查守护进程状态")
    parser.add_argument("--format", choices=["md", "json"], default="md", help="输出格式")
    parser.add_argument("--push", choices=["feishu"], help="推送渠道")
    parser.add_argument("--no-llm", action="store_true", help="跳过 AI 分析")

    args = parser.parse_args()

    if args.status:
        print(check_daemon_status())
        return

    if args.week:
        output = week_summary()
    else:
        date_str = args.date or datetime.now().strftime("%Y-%m-%d")
        report_text, report_path = run_report(date_str, args.format)
        output = report_text
        if not args.no_llm:
            output += run_llm_analysis(report_path, report_text)

    print(output)

    if args.push == "feishu":
        push_feishu(output)


if __name__ == "__main__":
    main()
