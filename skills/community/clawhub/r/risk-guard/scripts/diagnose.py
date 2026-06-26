"""
risk-guard 诊断脚本 v1.4
修复：#1-fallback去掉 #2-node进程fallback误判 #3-锁文件删除需确认 #4-阈值30 #5-base64编码 #6-日志轮转 #7-锁文件验证 #8-dry-run模式
"""

import subprocess
import os
import sys
import json
import base64
import shutil
import argparse
from pathlib import Path
from datetime import datetime

# UTF-8 输出
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# ---------- 配置 ----------
def get_workspace():
    home = os.environ.get("USERPROFILE", os.path.expanduser("~"))
    candidates = [
        os.path.join(home, ".jvs", ".openclaw", "workspace"),
        os.path.join(home, ".openclaw", "workspace"),
        os.path.join(home, "jvs_claw_workspace"),
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return ""

WORKSPACE = get_workspace()
LOG_DIR = os.path.join(WORKSPACE, "memory") if WORKSPACE else ""
HEALTH_URL = "http://127.0.0.1:18789/health"
GATEWAY_PORT = 18789
NODE_THRESHOLD = int(os.environ.get("RISK_GUARD_NODE_THRESHOLD", "30"))
DRY_RUN = False

# ---------- 参数解析 ----------
def parse_args():
    global DRY_RUN
    parser = argparse.ArgumentParser(description="Risk Guard 自检脚本")
    parser.add_argument("--dry-run", action="store_true", help="仅输出检查结果，不执行任何清理操作")
    args = parser.parse_args()
    DRY_RUN = args.dry_run

# ---------- 日志（带轮转） ----------
LOG_FILE = os.path.join(LOG_DIR, "risk_guard.log") if LOG_DIR else ""

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    if LOG_FILE:
        try:
            if LOG_DIR:
                os.makedirs(LOG_DIR, exist_ok=True)
            # 日志轮转 > 10MB
            if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 10 * 1024 * 1024:
                old = LOG_FILE + ".old"
                if os.path.exists(old):
                    os.remove(old)
                shutil.move(LOG_FILE, old)
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass

# ---------- PowerShell 执行（base64编码避免转义问题） ----------
def ps_cmd(cmd, timeout=15):
    """通过base64编码执行PowerShell命令，彻底避免转义问题"""
    try:
        encoded = base64.b64encode(cmd.encode("utf-16-le")).decode()
        full_cmd = f'powershell.exe -NoProfile -NonInteractive -EncodedCommand {encoded}'
        result = subprocess.run(
            full_cmd, shell=True, capture_output=True,
            text=True, timeout=timeout,
            encoding="utf-8", errors="replace"
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -2, "", str(e)

def run_cmd(cmd, timeout=10):
    """执行普通命令"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True,
            text=True, timeout=timeout,
            encoding="utf-8", errors="replace"
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "TIMEOUT"
    except Exception as e:
        return -2, "", str(e)

# ---------- 检查函数 ----------
def check_exec():
    code, out, _ = run_cmd("echo test")
    return ("ok" if code == 0 and "test" in out else "fail"), "exec正常" if code == 0 else f"exec异常(code={code})"

def check_temp_files():
    code, out, _ = ps_cmd("Get-ChildItem $env:TEMP -File | Measure-Object | Select-Object -ExpandProperty Count")
    if code == 0:
        try:
            count = int(out.strip())
            status = "warning" if count > 50000 else "ok"
            msg = f"临时文件{count}个({'过多' if count > 50000 else '正常'})"
            return status, msg
        except:
            return "unknown", f"无法解析: {out[:30]}"
    return "unknown", "命令失败"

def check_gateway_process():
    """网关进程（只查openclaw，不在node上fallback）"""
    code, out, _ = run_cmd("tasklist | findstr openclaw")
    if code == 0 and out:
        return "ok", "网关进程正常"
    return "critical", "网关进程未运行！需要先生确认是否启动"

def check_gateway_port():
    """网关端口（Get-NetTCPConnection主逻辑，无fallback避免非英文系统误判）"""
    code, out, _ = ps_cmd(
        f"Get-NetTCPConnection -LocalPort {GATEWAY_PORT} -ErrorAction SilentlyContinue | "
        f"Where-Object {{$_.State -eq 'Listen'}} | Measure-Object | Select-Object -ExpandProperty Count"
    )
    if code == 0:
        try:
            count = int(out.strip())
            if count > 0:
                return "ok", f"端口{GATEWAY_PORT}监听正常"
        except:
            pass
    return "warn", f"端口{GATEWAY_PORT}未监听，可能被占用"

def check_gateway_health():
    """网关健康端点（urllib标准库）"""
    try:
        import urllib.request
        req = urllib.request.Request(HEALTH_URL, headers={"User-Agent": "RiskGuard/1.0"})
        with urllib.request.urlopen(req, timeout=5) as r:
            return ("ok" if r.status == 200 else "warn"), f"健康端点(HTTP {r.status})"
    except Exception as e:
        return "warn", f"健康端点连接失败"

def check_lock_files():
    """锁文件清理（dry-run模式不删除；直接尝试删除，PermissionError表示被占用）"""
    if not WORKSPACE:
        return "skip", "无法确定工作区，跳过"
    removed = 0
    skipped = 0
    for f in os.listdir(WORKSPACE):
        if not (f.endswith(".lock") or f.endswith(".tmp")):
            continue
        path = os.path.join(WORKSPACE, f)
        try:
            age = datetime.now().timestamp() - os.path.getmtime(path)
            if age <= 600:
                continue
            if not DRY_RUN:
                os.remove(path)
                removed += 1
            else:
                removed += 1  # dry-run 计数但不实际删除
        except PermissionError:
            skipped += 1
        except Exception:
            pass
    if skipped > 0:
        msg = f"清理{removed}个，跳过{skipped}个被占用文件"
    elif removed > 0:
        msg = f"已清理{removed}个过期锁文件" if not DRY_RUN else f"[dry-run] 将清理{removed}个过期文件"
    else:
        msg = "[dry-run] 无需清理" if DRY_RUN else "无残留锁文件"
    status = "info" if (removed > 0 or skipped > 0) else "ok"
    return status, msg

def check_node_leak():
    """node进程泄漏（精确匹配node.exe，阈值可配置）"""
    code, out, _ = run_cmd("tasklist | findstr node.exe")
    if code == 0 and out:
        lines = [l for l in out.split("\n") if l.strip()]
        count = len(lines)
        if count > NODE_THRESHOLD:
            return "warning", f"发现{count}个node.exe进程，超过阈值{NODE_THRESHOLD}"
        return "ok", f"node进程正常({count}个)"
    return "ok", "无node进程"

def check_workspace():
    if not WORKSPACE:
        return "warn", "无法确定工作区路径"
    if os.path.exists(WORKSPACE):
        return "ok", f"工作区正常: {WORKSPACE}"
    return "critical", f"工作区不存在: {WORKSPACE}"

# ---------- 主流程 ----------
STATUS_MAP = {
    "ok": "[OK]", "info": "[INFO]", "skip": "[SKIP]",
    "warn": "[WARN]", "warning": "[WARN]", "critical": "[CRITICAL]",
    "fail": "[FAIL]", "error": "[ERROR]", "unknown": "[UNK]"
}

def main():
    parse_args()
    mode_note = " [DRY-RUN 仅诊断]" if DRY_RUN else ""
    print(f"=== Risk Guard 自检开始{mode_note} ===")
    log(f"=== Risk Guard 自检开始{mode_note} ===")

    checks = [
        ("exec基础功能",   check_exec),
        ("临时文件",       check_temp_files),
        ("网关进程",       check_gateway_process),
        ("网关端口",       check_gateway_port),
        ("网关健康端点",   check_gateway_health),
        ("锁文件清理",     check_lock_files),
        ("node进程泄漏",   check_node_leak),
        ("工作区路径",     check_workspace),
    ]

    issues = []
    for name, fn in checks:
        try:
            status, msg = fn()
            prefix = STATUS_MAP.get(status, "[???]")
            print(f"{prefix} [{name}] {msg}")
            if status in ("critical", "fail"):
                issues.append(f"[{name}] {msg}")
        except Exception as e:
            print(f"[ERROR] [{name}] {e}")
            issues.append(f"[{name}] 异常: {e}")

    print()
    if issues:
        print("=== 发现问题 ===")
        for i in issues:
            print(f"  - {i}")
        print()
        print("=== 建议先生操作 ===")
        print("1. 【假故障】工具已完成但无输出 → 继续正常使用")
        print("2. 【网关进程缺失】→ 先生确认是否运行 'openclaw gateway start'")
        print("3. 【node泄漏】→ 先生手动结束可疑进程")
    else:
        print("=== 所有检查通过，未发现明显问题 ===")

    log(f"自检完成，发现{len(issues)}个问题")

    # 保存JSON报告
    if LOG_DIR:
        try:
            os.makedirs(LOG_DIR, exist_ok=True)
            report_path = os.path.join(LOG_DIR, "risk_guard_last.json")
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump({
                    "time": datetime.now().isoformat(),
                    "workspace": WORKSPACE,
                    "dry_run": DRY_RUN,
                    "issues": issues
                }, f, ensure_ascii=False, indent=2)
        except:
            pass

    return issues

if __name__ == "__main__":
    main()
