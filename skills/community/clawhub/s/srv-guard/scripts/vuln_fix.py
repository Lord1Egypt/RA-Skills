#!/usr/bin/env python3
"""vuln_fix.py — 漏洞修复（默认 dry-run）

用法:
    python vuln_fix.py --input scan-result.json --dry-run [--apply] [--items CFG-01,CFG-03] [--output fix-result.json]

默认仅打印将执行的命令；需 --apply 才真正改动。修改配置前先备份。
"""

import argparse
import json
import os
import re
import shlex
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common
from _common import run_cmd, emit_json, log, parse_target, write_audit

TS = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
_BACKUPS = {}  # path -> 备份路径；同一文件在一次运行内只备份一次


def planned_backup_path(path):
    """dry-run 时用于展示「将会创建的备份路径」，不实际创建。"""
    return f"{path}.guard-bak.{TS}"


def backup(target, path):
    """备份文件，返回备份路径或 None。

    同一进程内同一 path 只备份一次：多个修复项共享第一份（真正的改动前快照）。
    否则后一项的 cp -a 会用「已被改过」的内容覆盖备份，回滚只能恢复半成品。
    """
    cached = _BACKUPS.get(path)
    if cached:
        return cached
    bak = f"{path}.guard-bak.{TS}"
    r = run_cmd(target, f"cp -a {shlex.quote(path)} {shlex.quote(bak)}", timeout=10)
    if r["rc"] != 0:
        return None
    _BACKUPS[path] = bak
    return bak


def fix_result(item_id, status, dry_run, commands=None, backups=None, rollback=None,
               reboot=False, message=""):
    # dry-run 不得声称已修复：状态改记为 would_fix，消息也标注为预览
    if dry_run:
        if status == "fixed":
            status = "would_fix"
        if message and not message.startswith("[DRY-RUN]"):
            message = "[DRY-RUN] " + message
        if backups:
            message += "；备份将在 --apply 时创建"
    return {
        "item_id": item_id, "status": status, "dry_run": dry_run,
        "commands": commands or [], "backup_files": backups or [],
        "rollback_commands": rollback or [], "reboot_required": reboot, "message": message,
    }


def _exec(target, cmd, dry_run):
    """执行或打印命令。"""
    if dry_run:
        return {"rc": 0, "stdout": f"[DRY-RUN] {cmd}", "stderr": ""}
    return run_cmd(target, cmd, timeout=60)


# ---------- fix functions ----------
# reload 命令统一取自 _common.RELOAD_SSHD（兼容 sshd/ssh/openssh-server 三种服务名）
RELOAD_SSHD = _common.RELOAD_SSHD


def fix_cfg01(target, dry_run):
    path = "/etc/ssh/sshd_config"
    bak = backup(target, path) if not dry_run else planned_backup_path(path)
    if not dry_run and bak is None:
        return fix_result("CFG-01", "failed", dry_run, message=f"备份失败，中止修复: {path}")
    cmd = f"sed -i 's/^PermitRootLogin yes/PermitRootLogin no/' {shlex.quote(path)} && {RELOAD_SSHD}"
    r = _exec(target, cmd, dry_run)
    ok = r["rc"] == 0
    return fix_result("CFG-01", "fixed" if ok else "failed", dry_run,
                      commands=[cmd], backups=[bak] if bak else [],
                      rollback=[f"cp {shlex.quote(bak)} {shlex.quote(path)} && {RELOAD_SSHD}"] if bak else [],
                      message="已禁用 root SSH 登录" if ok else f"失败: {r['stderr']}")


def fix_cfg02(target, dry_run):
    path = "/etc/ssh/sshd_config"
    # 前置检查: 至少一个 authorized_keys 非空
    chk = run_cmd(target, "find /home -name authorized_keys -size +0c 2>/dev/null | head -1", timeout=10)
    if not chk["stdout"].strip():
        return fix_result("CFG-02", "skipped", dry_run,
                          message="前置检查失败: 未发现非空 authorized_keys，禁用密码登录将锁死远程访问")
    bak = backup(target, path) if not dry_run else planned_backup_path(path)
    if not dry_run and bak is None:
        return fix_result("CFG-02", "failed", dry_run, message=f"备份失败，中止修复: {path}")
    cmd = f"sed -i 's/^PasswordAuthentication yes/PasswordAuthentication no/' {shlex.quote(path)} && {RELOAD_SSHD}"
    r = _exec(target, cmd, dry_run)
    ok = r["rc"] == 0
    return fix_result("CFG-02", "fixed" if ok else "failed", dry_run,
                      commands=[cmd], backups=[bak] if bak else [],
                      rollback=[f"cp {shlex.quote(bak)} {shlex.quote(path)} && {RELOAD_SSHD}"] if bak else [],
                      message="已禁用 SSH 密码登录" if ok else f"失败: {r['stderr']}")


def fix_cfg03(target, dry_run):
    path = "/etc/ssh/sshd_config"
    bak = backup(target, path) if not dry_run else planned_backup_path(path)
    if not dry_run and bak is None:
        return fix_result("CFG-03", "failed", dry_run, message=f"备份失败，中止修复: {path}")
    cmd = f"sed -i 's/^PermitEmptyPasswords yes/PermitEmptyPasswords no/' {shlex.quote(path)} && {RELOAD_SSHD}"
    r = _exec(target, cmd, dry_run)
    ok = r["rc"] == 0
    return fix_result("CFG-03", "fixed" if ok else "failed", dry_run,
                      commands=[cmd], backups=[bak] if bak else [],
                      rollback=[f"cp {shlex.quote(bak)} {shlex.quote(path)} && {RELOAD_SSHD}"] if bak else [],
                      message="已禁用 SSH 空口令" if ok else f"失败: {r['stderr']}")


def fix_cfg06(target, dry_run, keyfile):
    pr = run_cmd(target, f"stat -c '%a' {shlex.quote(keyfile)}", timeout=5)
    orig = pr["stdout"].strip() if pr["rc"] == 0 else "?"
    cmd = f"chmod 600 {shlex.quote(keyfile)}"
    r = _exec(target, cmd, dry_run)
    ok = r["rc"] == 0
    return fix_result("CFG-06", "fixed" if ok else "failed", dry_run,
                      commands=[cmd], rollback=[f"chmod {orig} {shlex.quote(keyfile)}"] if orig != "?" else [],
                      message=f"已修复 {keyfile} 权限" if ok else f"失败: {r['stderr']}")


def fix_cfg07(target, dry_run, user):
    cmd = f"passwd -l {shlex.quote(user)}"
    r = _exec(target, cmd, dry_run)
    ok = r["rc"] == 0
    return fix_result("CFG-07", "fixed" if ok else "failed", dry_run,
                      commands=[cmd], rollback=[f"passwd -u {shlex.quote(user)}"],
                      message=f"已锁定空口令账户 {user}" if ok else f"失败: {r['stderr']}")


def fix_svc01(target, dry_run, svc):
    cmd = f"systemctl stop {shlex.quote(svc)} && systemctl disable {shlex.quote(svc)}"
    r = _exec(target, cmd, dry_run)
    ok = r["rc"] == 0
    return fix_result("SVC-01", "fixed" if ok else "failed", dry_run,
                      commands=[cmd], rollback=[f"systemctl enable --now {shlex.quote(svc)}"],
                      message=f"已禁用服务 {svc}" if ok else f"失败: {r['stderr']}")


FIX_DISPATCH = {
    "CFG-01": lambda t, d, f: fix_cfg01(t, d),
    "CFG-02": lambda t, d, f: fix_cfg02(t, d),
    "CFG-03": lambda t, d, f: fix_cfg03(t, d),
    "CFG-06": lambda t, d, f: fix_cfg06(t, d, f.get("keyfile", "")),
    "CFG-07": lambda t, d, f: fix_cfg07(t, d, f.get("user", "")),
    "SVC-01": lambda t, d, f: fix_svc01(t, d, re.search(r':\s*(\S+)', f.get("title", "")).group(1) if re.search(r':\s*(\S+)', f.get("title", "")) else "unknown"),
}


def main():
    parser = argparse.ArgumentParser(description="漏洞修复（默认 dry-run）")
    parser.add_argument("--input", required=True, help="scan-result.json 路径")
    parser.add_argument("--target", required=True, help="local 或 ssh://user@host[:port]")
    parser.add_argument("--apply", action="store_true", help="真正执行（默认 dry-run）")
    parser.add_argument("--items", help="仅修复指定 ID（逗号分隔）")
    parser.add_argument("--output", help="输出 JSON 文件路径")
    args = parser.parse_args()

    dry_run = not args.apply
    try:
        parse_target(args.target)
    except ValueError as e:
        log(str(e), "ERROR")
        sys.exit(2)

    if not os.path.exists(args.input):
        log(f"输入文件不存在: {args.input}", "ERROR")
        sys.exit(2)
    with open(args.input, "r", encoding="utf-8") as f:
        scan = json.load(f)

    target = args.target
    if not dry_run and not _common.is_root(target):
        # 权限不足时绝不静默降级为 dry-run：明确拒绝，避免调用方误以为已修复
        msg = ("修复需要 root/sudo 权限，当前用户非 root：已拒绝执行，未对目标做任何变更。"
               "请用 root 或已授权的 sudo 账号重试。")
        log(msg, "ERROR")
        out = {
            "target": target, "dry_run": False, "status": "requires_privilege",
            "privilege_required": True, "error": msg, "results": [],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": {"fixed": 0, "would_fix": 0, "skipped": 0, "failed": 0},
        }
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
        emit_json(out)
        sys.exit(3)

    wanted = set(args.items.split(",")) if args.items else None
    results = []
    for fnd in scan.get("findings", []):
        fid = fnd["id"]
        if wanted and fid not in wanted:
            continue
        if not fnd.get("auto_fixable", True):
            results.append(fix_result(fid, "skipped", dry_run,
                                      message="该项不可自动修复，需人工处理"))
            continue
        handler = FIX_DISPATCH.get(fid)
        if not handler:
            results.append(fix_result(fid, "skipped", dry_run,
                                      message=f"无 {fid} 的自动修复实现"))
            continue
        try:
            res = handler(target, dry_run, fnd)
            results.append(res)
            if not dry_run:
                write_audit(target, f"FIX ITEM={fid} STATUS={res['status']} DRY_RUN=false")
        except Exception as e:
            results.append(fix_result(fid, "failed", dry_run, message=f"异常: {e}"))

    ok = sum(1 for r in results if r["status"] == "fixed")
    would = sum(1 for r in results if r["status"] == "would_fix")
    skipped = sum(1 for r in results if r["status"] == "skipped")
    failed = sum(1 for r in results if r["status"] == "failed")
    out = {
        "target": target, "dry_run": dry_run, "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": results,
        "summary": {"fixed": ok, "would_fix": would, "skipped": skipped, "failed": failed},
    }
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        log(f"结果已写入 {args.output}")
    emit_json(out)
    log(f"修复完成: {ok} fixed, {skipped} skipped, {failed} failed (dry_run={dry_run})")


if __name__ == "__main__":
    main()
