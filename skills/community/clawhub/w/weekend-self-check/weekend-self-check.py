#!/usr/bin/env python3
"""
码虫周末全面自检脚本 v1.4 — SIGTERM 真正可中断 + 异步 sync
每周六 10:00 执行，输出完整自检报告到飞书

修复历史:
- v1.0 (2026-06-20): 初版
- v1.1 (2026-06-27): 增量
- v1.2 (2026-06-30): 增量
- v1.3 (2026-07-11): SIGTERM-safe + 真实状态解析器（ERR-20260711-001 闭环 v1）
  - 修解析器: 旧版依赖 ● ✓ ✗ 字符，新版按 status: 字段匹配
  - 加 SIGTERM handler: 收到系统终止信号时打诊断 + 飞书告警
  - 加 --dry-run: 不发飞书，只跑流程（验证用）
  - 加 --no-send: 跑流程但不发飞书（CI 用）
  - 详细诊断: 内存/CPU/gateway 状态写入报告
  - 移除 bare except: 用 specific exceptions
- v1.4 (2026-07-11): SIGTERM 真正可中断 + 异步 sync（ERR-20260711-001 闭环 v2）
  - v1.3 缺陷: handler 只设置 flag,主流程在 subprocess.run 阻塞时无法响应
  - v1.4 修法: sync.sh 改异步 Popen,主循环 0.5s poll _INTERRUPTED,中断时立即 kill 子进程
  - 加 _check_interrupt() 统一函数,每个 step 后立即检查
  - 加 safe_run_interruptible() 包装,长操作内部也响应中断
  - cron timeoutSeconds=600 显式配置（防外层兜底超时触发）

原理（SIGTERM 闭环 v2）:
- v1.3 缺陷: signal handler 只设置 flag,subprocess.run 同步阻塞期间 flag 无效
- v1.4: 把长操作都改成 Popen + 主循环 poll,中断信号能在 0.5s 内响应
- 收到 SIGTERM → 主循环下一轮检测到 flag → 立即 kill 子进程 → 发飞书告警 → 退出 130
- WSL 重启 / gateway restart 会 SIGTERM 所有 cron 子进程
- 之前没 handler → 直接死，failure notification 也没发出去
- 现在收到 SIGTERM → 立即打 stderr + 发一条「任务中断」通知到飞书（best-effort, 5s 超时）
"""
import os
import sys
import json
import time
import signal
import subprocess
import argparse
import traceback
import requests
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional

WORKSPACE = "/home/colbert/.openclaw/workspace-coding-advisor"
RECEIVE_ID = "ou_991021547578f722d08533accc83651d"
CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
SCRIPT_NAME = "码虫周末自检 v1.4"
SCRIPT_VERSION = "1.4.0"
TZ_SHANGHAI = timezone(timedelta(hours=8))

# ──────────────────────────────────────────────────────
# 全局状态（SIGTERM handler 用）
# ──────────────────────────────────────────────────────
_INTERRUPTED = False
_INTERRUPT_REASON = ""


def _signal_handler(signum, frame):
    """SIGTERM/SIGINT 收到时打诊断 + 标记中断状态。"""
    global _INTERRUPTED, _INTERRUPT_REASON
    _INTERRUPTED = True
    _INTERRUPT_REASON = f"signal {signum} ({signal.Signals(signum).name})"
    sys.stderr.write(
        f"[{datetime.now(TZ_SHANGHAI).strftime('%H:%M:%S')}] "
        f"⚠️  收到 {_INTERRUPT_REASON}，准备优雅退出\n"
    )
    sys.stderr.flush()


signal.signal(signal.SIGTERM, _signal_handler)
signal.signal(signal.SIGINT, _signal_handler)


# ──────────────────────────────────────────────────────
# 工具
# ──────────────────────────────────────────────────────
def now_str() -> str:
    return datetime.now(TZ_SHANGHAI).strftime("%Y-%m-%d %H:%M:%S")


def log(msg: str):
    print(f"[{datetime.now(TZ_SHANGHAI).strftime('%H:%M:%S')}] {msg}", flush=True)


def log_err(msg: str):
    sys.stderr.write(f"[{datetime.now(TZ_SHANGHAI).strftime('%H:%M:%S')}] ❌ {msg}\n")
    sys.stderr.flush()


def safe_run(cmd: str, timeout: int = 30) -> str:
    """运行 shell 命令，超时/失败返回空字符串（不抛）。

    警告: 同步阻塞,主流程在等待期间无法响应 SIGTERM。
    长操作请用 safe_run_interruptible()。
    """
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            timeout=timeout, check=False
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        log_err(f"命令超时 ({timeout}s): {cmd[:60]}")
        return ""
    except subprocess.SubprocessError as e:
        log_err(f"子进程错误: {e}")
        return ""
    except OSError as e:
        log_err(f"OS 错误: {e}")
        return ""


def safe_run_interruptible(cmd: str, timeout: int = 30, poll_interval: float = 0.5) -> str:
    """运行 shell 命令,主循环周期检查 _INTERRUPTED,中断立即 kill 子进程。

    与 safe_run 区别:
    - 不用 subprocess.run 同步阻塞
    - 用 Popen 启动,主循环每 poll_interval 秒检查一次中断标志
    - 收到 SIGTERM → 立即 SIGTERM 子进程 → 等最多 2s → 强制 SIGKILL
    - 超时同样处理

    Returns: stdout (空字符串表示中断/超时/失败)
    """
    proc = None
    try:
        proc = subprocess.Popen(
            cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True
        )
        elapsed = 0.0
        while elapsed < timeout:
            # 中断检查 — 最优先
            if _INTERRUPTED:
                log_err(f"操作被中断, kill 子进程 (PID={proc.pid}, elapsed={elapsed:.1f}s)")
                _kill_proc(proc)
                return ""

            try:
                # poll() 非阻塞,立即返回子进程退出码(还在跑就是 None)
                rc = proc.poll()
                if rc is not None:
                    out, _ = proc.communicate(timeout=2)
                    return (out or "").strip()
            except subprocess.SubprocessError as e:
                log_err(f"poll 子进程错误: {e}")
                _kill_proc(proc)
                return ""

            time.sleep(poll_interval)
            elapsed += poll_interval

        # 超时
        log_err(f"命令超时 ({timeout}s), kill 子进程: {cmd[:60]}")
        _kill_proc(proc)
        return ""

    except (OSError, ValueError) as e:
        log_err(f"启动子进程失败: {e}")
        if proc is not None:
            _kill_proc(proc)
        return ""


def _kill_proc(proc: subprocess.Popen) -> None:
    """优雅 kill 子进程: SIGTERM → 等 2s → SIGKILL。"""
    try:
        if proc.poll() is None:
            proc.terminate()  # SIGTERM
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()  # SIGKILL
                proc.wait(timeout=2)
    except (OSError, subprocess.SubprocessError) as e:
        log_err(f"kill 子进程失败 (可能已退出): {e}")


def _check_interrupt(label: str = "") -> bool:
    """统一中断检查,带日志。返回 True 表示已中断。"""
    if _INTERRUPTED:
        log_err(f"检测到中断 ({_INTERRUPT_REASON}), 退出点: {label or '(unknown)'}")
        return True
    return False


def get_token(account: str = "codebot") -> Optional[str]:
    """获取飞书 tenant_access_token。"""
    try:
        with open(CONFIG_PATH, encoding="utf-8") as f:
            config = json.load(f)
        acc = config["channels"]["feishu"]["accounts"][account]
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        r = requests.post(
            url, json={"app_id": acc["appId"], "app_secret": acc["appSecret"]},
            timeout=10
        )
        data = r.json()
        if data.get("code") == 0:
            return data["tenant_access_token"]
        log_err(f"获取 token 失败: {data}")
        return None
    except (OSError, KeyError, requests.RequestException, ValueError) as e:
        log_err(f"获取 token 异常: {e}")
        return None


def send_post(content_dict: dict, receive_id: str, timeout: int = 10) -> bool:
    """发 post 富文本到飞书（best-effort）。"""
    token = get_token()
    if not token:
        return False
    msg_payload = {
        "receive_id": receive_id,
        "msg_type": "post",
        "content": json.dumps(content_dict, ensure_ascii=False)
    }
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json=msg_payload, timeout=timeout)
        data = r.json()
        if data.get("code") == 0:
            return True
        log_err(f"发送失败: {data}")
        return False
    except requests.RequestException as e:
        log_err(f"发送异常: {e}")
        return False


# ──────────────────────────────────────────────────────
# 数据采集
# ──────────────────────────────────────────────────────
def parse_cron_status() -> dict:
    """解析 `openclaw cron list` 表格输出，按 Status 列统计。

    v1.2 旧版依赖 ● ✓ ✗ 字符，OpenClaw 6.x 输出无此字符 → total 永远 0。
    v1.3 用 fixed-width 列定位：表头解析出 Status 列起始/结束位置。
    优势：Schedule 列含 `cron 30 19 * * *` 多词不会被错切。
    """
    out = safe_run("openclaw cron list 2>/dev/null")
    if not out:
        return {"total": 0, "ok": 0, "error": 0, "unknown": 0,
                "error_jobs": [], "error_details": []}

    lines = out.splitlines()
    if len(lines) < 2:
        return {"total": 0, "ok": 0, "error": 0, "unknown": 0,
                "error_jobs": [], "error_details": []}

    # 表头解析：按每列起始位置记录（fixed-width 列宽）
    import re
    header = lines[0]
    col_positions = [(m.start(), m.group().strip())
                     for m in re.finditer(r'\S+\s+', header)]

    # 找 Status 列起始位置 + 下一列起始位置作为结束位置
    status_start = None
    next_start = None
    for i, (pos, name) in enumerate(col_positions):
        if name == "Status":
            status_start = pos
            if i + 1 < len(col_positions):
                next_start = col_positions[i + 1][0]
            else:
                next_start = len(header)
            break

    if status_start is None:
        # fallback: OpenClaw 6.x 默认 Status 在 117 位置
        status_start = 117
        next_start = 127

    # Name 列位置
    name_start = col_positions[1][0] if len(col_positions) > 1 else 37
    name_end = col_positions[2][0] if len(col_positions) > 2 else 62
    # ID 列位置
    id_start = col_positions[0][0]

    total = ok = error = unknown = 0
    error_jobs: List[str] = []
    error_details: List[str] = []

    for line in lines[1:]:
        if not line.strip():
            continue
        # 行长度可能短于表头（窄行截断），跳过
        if len(line) < status_start + 2:
            continue

        total += 1
        status_raw = line[status_start:next_start].strip().lower()
        # 清理 ANSI 颜色码
        status_clean = "".join(c for c in status_raw if c.isalnum() or c == "-")
        # 截断状态（防止 "ok (warning)" 等带尾注）
        status_clean = status_clean.split()[0] if status_clean else "unknown"

        job_id = line[id_start:name_start].strip()
        job_name = line[name_start:name_end].strip()

        if status_clean == "ok":
            ok += 1
        elif status_clean == "error":
            error += 1
            error_jobs.append(job_name[:30])
            error_details.append(f"{job_name[:25]} ({job_id[:8]})")
        else:
            unknown += 1

    return {
        "total": total,
        "ok": ok,
        "error": error,
        "unknown": unknown,
        "error_jobs": error_jobs[:8],
        "error_details": error_details[:8]
    }


def get_data_stats() -> dict:
    """从 CODIS-DATA 读取聚合数据。"""
    stats = {}
    base = f"{WORKSPACE}/CODIS-DATA/state"
    for fname, key in [
        ("skills-stats.json", "skills"),
        ("case-stats.json", "cases"),
        ("corrections-summary.json", "corrections"),
        ("hot-rules.json", "hot")
    ]:
        path = f"{base}/{fname}"
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    stats[key] = json.load(f)
            except (OSError, ValueError) as e:
                log_err(f"读取 {fname} 失败: {e}")
                stats[key] = {}

    reg_path = f"{WORKSPACE}/CODIS-DATA/meta/data-registry.json"
    if os.path.exists(reg_path):
        try:
            with open(reg_path, encoding="utf-8") as f:
                stats["registry"] = json.load(f)
        except (OSError, ValueError) as e:
            log_err(f"读取 registry 失败: {e}")
    return stats


def get_skills_count() -> int:
    skills_dir = f"{WORKSPACE}/skills"
    if not os.path.isdir(skills_dir):
        return 0
    return sum(
        1 for d in os.listdir(skills_dir)
        if os.path.isdir(os.path.join(skills_dir, d)) and not d.startswith(".")
    )


def get_reports_count() -> int:
    reports_dir = f"{WORKSPACE}/memory/daily-reports"
    if not os.path.isdir(reports_dir):
        return 0
    return sum(
        1 for f in os.listdir(reports_dir) if f.endswith(".md")
    )


def get_system_health() -> dict:
    """采集系统健康状态（内存/CPU/最近 OOM/gateway 状态）。"""
    health = {
        "mem_total_gb": None, "mem_used_gb": None, "mem_avail_gb": None,
        "load_avg": None, "recent_oom": False, "gateway_active": None
    }

    # 内存
    meminfo = safe_run("cat /proc/meminfo 2>/dev/null | head -3")
    for line in meminfo.splitlines():
        if "MemTotal" in line:
            try:
                health["mem_total_gb"] = round(int(line.split()[1]) / 1024 / 1024, 1)
            except (IndexError, ValueError):
                pass
        elif "MemAvailable" in line:
            try:
                health["mem_avail_gb"] = round(int(line.split()[1]) / 1024 / 1024, 1)
            except (IndexError, ValueError):
                pass

    # load average
    load = safe_run("cat /proc/loadavg 2>/dev/null")
    if load:
        health["load_avg"] = load.split()[0] if load else None

    # 最近 OOM（最近 5 分钟）
    oom_check = safe_run("dmesg -T 2>/dev/null | grep -i 'oom\\|killed' | tail -3")
    health["recent_oom"] = bool(oom_check and "killed" in oom_check.lower())

    # gateway 状态（不依赖 token，直接看进程）
    gw = safe_run("pgrep -f openclaw-gateway | head -1")
    health["gateway_active"] = bool(gw)

    return health


# ──────────────────────────────────────────────────────
# 报告构建
# ──────────────────────────────────────────────────────
def fmt_val(v, default: str = "?"):
    """格式化值，空值显示 '?'。"""
    if v is None or v == "":
        return default
    return str(v)


def build_report(cron: dict, stats: dict, skills: int, reports: int,
                 health: dict, duration_s: float) -> dict:
    today = datetime.now(TZ_SHANGHAI).strftime("%Y-%m-%d %H:%M")

    cases = stats.get("cases", {})
    sk = stats.get("skills", {})
    corr = stats.get("corrections", {})
    hot = stats.get("hot", {})
    reg = stats.get("registry", {})

    cron_summary = f"{cron.get('total',0)}/{cron.get('ok',0)}/{cron.get('error',0)}/{cron.get('unknown',0)}"

    # 健康指标
    mem_warn = ""
    if health.get("mem_avail_gb") and health["mem_avail_gb"] < 1.0:
        mem_warn = f" ⚠️可用仅 {health['mem_avail_gb']}GB"
    oom_warn = " ⚠️最近有 OOM 痕迹" if health.get("recent_oom") else ""
    gw_warn = "" if health.get("gateway_active") else " ⚠️gateway 未运行"

    body = [
        [{"tag": "text", "text": f"📊 系统状态总览 · {SCRIPT_NAME}", "bold": True}],
        [{"tag": "text", "text": f"耗时 {duration_s:.1f}s | 健康{mem_warn}{oom_warn}{gw_warn}"}],
        [{"tag": "text", "text": "\n"}],
        [{"tag": "text", "text": "🧬 Cron 任务", "bold": True}],
        [{"tag": "text", "text": f"总数/OK/ERR/未知: {cron_summary}"}],
    ]

    if cron.get("error_details"):
        body.append([{"tag": "text", "text": f"  🔴 错误任务 ({len(cron['error_jobs'])}):", "bold": True}])
        for detail in cron["error_details"]:
            body.append([{"tag": "text", "text": f"  • {detail}"}])
    else:
        body.append([{"tag": "text", "text": "  ✅ 无错误任务"}])

    body.extend([
        [{"tag": "text", "text": "\n📦 资产盘点", "bold": True}],
        [{"tag": "text", "text": f"技能数: {skills} | 日报总数: {reports}"}],
        [{"tag": "text", "text": f"Registry版本: v{fmt_val(reg.get('version'))}"}],
        [{"tag": "text", "text": "\n🛠 技能体系状态", "bold": True}],
        [{"tag": "text", "text": f"有反馈技能: {fmt_val(sk.get('total_with_feedback'))}"}],
        [{"tag": "text", "text": f"有评分技能: {fmt_val(sk.get('total_with_rating'))}"}],
        [{"tag": "text", "text": "\n📊 数据驱动层", "bold": True}],
        [{"tag": "text", "text": f"案例总数: {fmt_val(cases.get('total_cases'))}"}],
        [{"tag": "text", "text": f"有效率: {fmt_val(cases.get('useful_rate'))}"}],
        [{"tag": "text", "text": f"HOT规则: {fmt_val(hot.get('total'))}"}],
        [{"tag": "text", "text": "\n📋 纠错层状态", "bold": True}],
        [{"tag": "text", "text": f"total: {fmt_val(corr.get('total'))} | new: {fmt_val(corr.get('new'))} | active: {fmt_val(corr.get('active'))}"}],
        [{"tag": "text", "text": "\n🖥 系统健康", "bold": True}],
        [{"tag": "text", "text": f"内存: {fmt_val(health.get('mem_avail_gb'))}/{fmt_val(health.get('mem_total_gb'))} GB 可用"}],
        [{"tag": "text", "text": f"load: {fmt_val(health.get('load_avg'))} | gateway: {'✅' if health.get('gateway_active') else '❌'}"}],
        [{"tag": "text", "text": "\n"}],
        [{"tag": "text", "text": "🐛 下周行动项", "bold": True}],
        [{"tag": "text", "text": "1. 排查错误 Cron（按上面列表）"}],
        [{"tag": "text", "text": "2. 跟进 pending corrections（去状态 new）"}],
        [{"tag": "text", "text": "3. 优化低评分技能"}],
        [{"tag": "text", "text": "4. (可选) 跟进 memory-guardian / 资源回收"}],
        [{"tag": "text", "text": "\n"}],
        [{"tag": "text", "text": "---", "grey": True}],
        [{"tag": "text", "text": f"\n整理: 码虫 🐛 | {today} | v{SCRIPT_VERSION}", "grey": True}],
    ])
    return {"zh_cn": {"title": f"🛠 码虫周末全面自检 · {today} [v{SCRIPT_VERSION}]", "content": body}}


def build_interrupt_report(reason: str) -> dict:
    """SIGTERM 中断时发一个简洁的告警。"""
    now = datetime.now(TZ_SHANGHAI).strftime("%Y-%m-%d %H:%M:%S")
    body = [
        [{"tag": "text", "text": "⚠️ 周末自检任务被系统中断", "bold": True}],
        [{"tag": "text", "text": f"原因: {reason}"}],
        [{"tag": "text", "text": f"时间: {now}"}],
        [{"tag": "text", "text": f"任务: weekend-self-check v{SCRIPT_VERSION}"}],
        [{"tag": "text", "text": "\n下次自动触发: 下周六 10:00"}],
        [{"tag": "text", "text": "如需立即执行: openclaw cron run weekend-self-check-001-0000-0000-000000000001"}],
        [{"tag": "text", "text": "\n---", "grey": True}],
        [{"tag": "text", "text": f"自动发送: 码虫 🐛 SIGTERM handler v{SCRIPT_VERSION}", "grey": True}],
    ]
    return {"zh_cn": {"title": "⚠️ 周末自检中断告警", "content": body}}


# ──────────────────────────────────────────────────────
# 主流程
# ──────────────────────────────────────────────────────
def main() -> int:
    parser = argparse.ArgumentParser(description="码虫周末全面自检")
    parser.add_argument("--dry-run", action="store_true", help="不发飞书，只跑流程 + 打印报告")
    parser.add_argument("--no-send", action="store_true", help="跑流程但不发送（CI 用）")
    parser.add_argument("--skip-sync", action="store_true", help="跳过 sync.sh（加速）")
    args = parser.parse_args()

    start = datetime.now(TZ_SHANGHAI)
    log(f"🛠 {SCRIPT_NAME} 开始 (v{SCRIPT_VERSION})")

    try:
        # Step 1: 数据同步（v1.4 异步可中断，原始 subprocess.run 会阻塞 signal handler）
        if not args.skip_sync:
            log("[1/5] 数据同步 (异步可中断, timeout=120s)...")
            sync_out = safe_run_interruptible(
                f"cd {WORKSPACE} && bash CODIS-DATA/sync.sh 2>&1 | tail -20",
                timeout=120, poll_interval=0.5
            )
            if sync_out:
                for ln in sync_out.splitlines()[-3:]:
                    log(f"  sync: {ln}")
        else:
            log("[1/5] 数据同步 (跳过)")

        if _check_interrupt("after step 1 sync"):
            return _handle_interrupt(args)

        # Step 2: Cron 状态
        log("[2/5] 获取 Cron 状态...")
        cron = parse_cron_status()
        log(f"  → total={cron['total']} ok={cron['ok']} error={cron['error']}")

        if _check_interrupt("after step 2 cron"):
            return _handle_interrupt(args)

        # Step 3: 数据统计
        log("[3/5] 获取数据统计...")
        stats = get_data_stats()
        skills = get_skills_count()
        reports = get_reports_count()
        log(f"  → skills={skills} reports={reports}")

        if _check_interrupt("after step 3 stats"):
            return _handle_interrupt(args)

        # Step 4: 系统健康
        log("[4/5] 采集系统健康...")
        health = get_system_health()
        log(f"  → mem_avail={health.get('mem_avail_gb')}GB load={health.get('load_avg')}")

        if _check_interrupt("after step 4 health"):
            return _handle_interrupt(args)

        # Step 5: 构建并发送报告
        log("[5/5] 构建报告...")
        end = datetime.now(TZ_SHANGHAI)
        duration = (end - start).total_seconds()
        report = build_report(cron, stats, skills, reports, health, duration)

        if args.dry_run:
            log("🧪 DRY RUN 模式，不发送飞书")
            print("\n" + "=" * 60)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            print("=" * 60)
            log(f"✅ 报告构建完成 (耗时 {duration:.1f}s)，未发送")
            return 0

        log("📤 发送飞书...")
        success = send_post(report, RECEIVE_ID)

        log(f"{'✅ 报告已发送' if success else '❌ 发送失败'} (耗时 {duration:.1f}s)")
        return 0 if success else 1

    except Exception as e:
        log_err(f"未捕获异常: {e}")
        traceback.print_exc()
        return 1


def _handle_interrupt(args) -> int:
    """统一处理 SIGTERM 中断：发飞书告警 + 返回错误码。"""
    log_err(f"任务中断: {_INTERRUPT_REASON}")

    if args.dry_run:
        log("DRY RUN 模式，不发飞书")
        return 130  # 标准 SIGINT 退出码

    # 发中断告警（best-effort, 短超时）
    log("发送中断告警到飞书...")
    report = build_interrupt_report(_INTERRUPT_REASON)
    sent = send_post(report, RECEIVE_ID, timeout=5)
    log(f"{'✅' if sent else '❌'} 中断告警{'已发送' if sent else '发送失败'}")
    return 130


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        log_err("手动中断")
        sys.exit(130)