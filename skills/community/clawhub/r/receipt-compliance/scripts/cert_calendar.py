#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
到期与认证期日历（v4.4.0）

功能：
1. 台账认证期限字段：全电发票自动取数（开票日期 + 窗口），纸票手工补录
2. 每日扫描：30 天 / 7 天两档提醒，另列已过期
3. CSV 导出，供日历软件（Outlook / 谷歌日历 / 手机日历）二次提醒
4. 计划任务注册：Windows 用 schtasks，由 Python 直接调用，不落任何 .bat/.ps1 文件

说明：自 2020-03-01 起增值税专用发票已取消 360 天认证确认期限，
本模块的窗口仅作企业内部「勾选所属期」管理提醒，窗口天数可配置。
"""

import csv
import json
import platform
import subprocess
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List

try:
    from ledger_db import LedgerDB, DEFAULT_CERT_WINDOW_DAYS
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from ledger_db import LedgerDB, DEFAULT_CERT_WINDOW_DAYS


TASK_NAME = "receipt-compliance-cert-reminder"
DEFAULT_WARN_DAYS = (30, 7)
DEFAULT_CSV_PATH = Path.home() / ".workbuddy" / "output" / "cert_calendar.csv"


def _parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    s = s.strip().replace("/", "-")
    for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y年%m月%d日"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


class CertCalendar:
    """认证期限日历"""

    def __init__(self, ledger: Optional[LedgerDB] = None, db_path: Optional[str] = None):
        self.ledger = ledger or LedgerDB(db_path)

    # ---------- 取数 ----------

    def ensure_deadlines(self, window_days: int = DEFAULT_CERT_WINDOW_DAYS) -> int:
        """全电发票自动取数：为缺失认证期限的记录按开票日期补算"""
        return self.ledger.fill_missing_deadlines(window_days)

    def fetch_deadlines(self) -> List[Dict[str, Any]]:
        """从台账取出全部含认证期限的记录"""
        rows = self.ledger.conn.execute(
            """
            SELECT id, invoice_number, invoice_code, seller_name, total,
                   billing_date, certification_deadline, certification_source, direction
            FROM invoices
            WHERE certification_deadline IS NOT NULL AND certification_deadline != ''
            ORDER BY certification_deadline
            """
        ).fetchall()
        return [dict(r) for r in rows]

    # ---------- 扫描 ----------

    def scan(self, warn_days=DEFAULT_WARN_DAYS, today: Optional[date] = None) -> Dict[str, Any]:
        """
        扫描到期情况

        返回结构：
        {
          "overdue": [...],        # 已过期
          "warn_7":  [...],        # 7 天内到期
          "warn_30": [...],        # 30 天内到期（不含 7 天内）
          "safe":    [...]         # 30 天以上
        }
        """
        today = today or date.today()
        items = []
        for r in self.fetch_deadlines():
            dl = _parse_date(r.get("certification_deadline"))
            if not dl:
                continue
            days_left = (dl - today).days
            item = {
                "id": r["id"],
                "invoice_number": r["invoice_number"],
                "invoice_code": r["invoice_code"],
                "seller_name": r["seller_name"],
                "total": r["total"],
                "billing_date": r["billing_date"],
                "deadline": r["certification_deadline"],
                "source": r.get("certification_source") or "unknown",
                "days_left": days_left,
            }
            items.append(item)

        overdue = [i for i in items if i["days_left"] < 0]
        warn_7 = [i for i in items if 0 <= i["days_left"] <= 7]
        warn_30 = [i for i in items if 7 < i["days_left"] <= 30]
        safe = [i for i in items if i["days_left"] > 30]

        return {
            "scan_date": today.isoformat(),
            "total": len(items),
            "overdue": overdue,
            "warn_7": warn_7,
            "warn_30": warn_30,
            "safe_count": len(safe),
            "summary": {
                "已过期": len(overdue),
                "7天内到期": len(warn_7),
                "30天内到期": len(warn_30),
                "30天以上": len(safe),
            },
        }

    def format_text(self, result: Dict[str, Any]) -> str:
        """人类可读的扫描结果"""
        lines = [f"认证期限扫描 · {result['scan_date']} · 共 {result['total']} 张"]
        s = result["summary"]
        lines.append(f"  已过期 {s['已过期']} 张 | 7 天内 {s['7天内到期']} 张 | "
                     f"30 天内 {s['30天内到期']} 张 | 30 天以上 {s['30天以上']} 张")
        for level in ("overdue", "warn_7", "warn_30"):
            label = {"overdue": "已过期", "warn_7": "7 天内到期",
                     "warn_30": "30 天内到期"}[level]
            for i in result[level]:
                flag = "（已过期）" if i["days_left"] < 0 else f"（剩 {i['days_left']} 天）"
                lines.append(
                    f"  [{label}] {i['invoice_number']} {i['seller_name'] or ''} "
                    f"{i['total'] or 0:.2f} 元 到期 {i['deadline']} {flag}")
        return "\n".join(lines)

    # ---------- 导出 ----------

    def export_csv(self, output_path: Optional[str] = None,
                   warn_days=DEFAULT_WARN_DAYS) -> str:
        """导出 CSV 供日历软件二次提醒"""
        out = Path(output_path) if output_path else DEFAULT_CSV_PATH
        out.parent.mkdir(parents=True, exist_ok=True)
        result = self.scan(warn_days)

        rows = []
        for level in ("overdue", "warn_7", "warn_30"):
            for i in result[level]:
                rows.append({
                    "Subject": f"发票认证到期提醒：{i['invoice_number']}",
                    "Start Date": i["deadline"],
                    "All Day Event": "True",
                    "Description": (f"销售方：{i['seller_name'] or '-'}；"
                                    f"金额：{i['total'] or 0:.2f} 元；"
                                    f"开票日期：{i['billing_date'] or '-'}；"
                                    f"剩余天数：{i['days_left']}"),
                    "Category": "发票认证",
                })

        if not rows:
            rows.append({
                "Subject": "当前无到期发票",
                "Start Date": date.today().isoformat(),
                "All Day Event": "True",
                "Description": "扫描结果为空",
                "Category": "发票认证",
            })

        with open(out, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)
        return str(out)

    # ---------- 计划任务 ----------

    def register_schedule(self, hour: int = 9, minute: int = 0,
                          csv_path: Optional[str] = None) -> Dict[str, Any]:
        """
        注册每日扫描计划任务

        Windows 用 schtasks 直接注册，不生成任何 .bat/.ps1 文件；
        非 Windows 输出 crontab 建议，由用户自行添加。
        """
        script = str(Path(__file__).resolve())
        py = sys.executable
        target_csv = csv_path or str(DEFAULT_CSV_PATH)

        if platform.system() != "Windows":
            return {
                "status": "manual",
                "message": "非 Windows 系统请手动添加 crontab",
                "crontab": f"{minute} {hour} * * * {py} {script} --scan --export-csv {target_csv}",
            }

        tr = f'"{py}" "{script}" --scan --export-csv "{target_csv}"'
        cmd = [
            "schtasks", "/Create",
            "/TN", TASK_NAME,
            "/TR", tr,
            "/SC", "DAILY",
            "/ST", f"{hour:02d}:{minute:02d}",
            "/F",
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            ok = proc.returncode == 0
            return {
                "status": "success" if ok else "failed",
                "task_name": TASK_NAME,
                "schedule": f"每天 {hour:02d}:{minute:02d}",
                "message": (proc.stdout or proc.stderr or "").strip(),
            }
        except FileNotFoundError:
            return {"status": "failed", "message": "系统未找到 schtasks 命令"}
        except subprocess.TimeoutExpired:
            return {"status": "failed", "message": "schtasks 执行超时"}

    def unregister_schedule(self) -> Dict[str, Any]:
        """取消每日扫描计划任务"""
        if platform.system() != "Windows":
            return {"status": "manual", "message": "非 Windows 系统请手动移除 crontab 行"}
        try:
            proc = subprocess.run(["schtasks", "/Delete", "/TN", TASK_NAME, "/F"],
                                  capture_output=True, text=True, timeout=30)
            return {
                "status": "success" if proc.returncode == 0 else "failed",
                "message": (proc.stdout or proc.stderr or "").strip(),
            }
        except FileNotFoundError:
            return {"status": "failed", "message": "系统未找到 schtasks 命令"}

    def schedule_status(self) -> Dict[str, Any]:
        """查询计划任务是否存在"""
        if platform.system() != "Windows":
            return {"status": "unknown", "message": "非 Windows 系统不支持查询"}
        try:
            proc = subprocess.run(["schtasks", "/Query", "/TN", TASK_NAME],
                                  capture_output=True, text=True, timeout=30)
            return {
                "exists": proc.returncode == 0,
                "raw": (proc.stdout or "").strip(),
            }
        except FileNotFoundError:
            return {"exists": False, "message": "系统未找到 schtasks 命令"}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="到期与认证期日历")
    parser.add_argument("--db", help="台账数据库路径")
    parser.add_argument("--ensure-deadlines", action="store_true", help="全电发票自动补算认证期限")
    parser.add_argument("--window-days", type=int, default=DEFAULT_CERT_WINDOW_DAYS,
                        help=f"认证期限窗口天数（默认 {DEFAULT_CERT_WINDOW_DAYS}）")
    parser.add_argument("--set-deadline", nargs=2, metavar=("NUMBER", "DATE"),
                        help="手工补录纸票认证期限")
    parser.add_argument("--scan", action="store_true", help="扫描到期情况")
    parser.add_argument("--export-csv", nargs="?", const="", help="导出 CSV 供日历软件导入")
    parser.add_argument("--register", action="store_true", help="注册每日扫描计划任务")
    parser.add_argument("--unregister", action="store_true", help="取消计划任务")
    parser.add_argument("--status", action="store_true", help="查询计划任务状态")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    args = parser.parse_args()

    cal = CertCalendar(db_path=args.db)

    if args.ensure_deadlines:
        n = cal.ensure_deadlines(args.window_days)
        print(f"已补算认证期限：{n} 张")

    if args.set_deadline:
        ok = cal.ledger.set_certification_deadline(args.set_deadline[0], args.set_deadline[1])
        print("补录成功" if ok else "未找到该发票号码，请确认")

    if args.register:
        print(json.dumps(cal.register_schedule(), ensure_ascii=False, indent=2))

    if args.unregister:
        print(json.dumps(cal.unregister_schedule(), ensure_ascii=False, indent=2))

    if args.status:
        print(json.dumps(cal.schedule_status(), ensure_ascii=False, indent=2))

    if args.scan or args.export_csv is not None or not any(
            [args.ensure_deadlines, args.set_deadline, args.register,
             args.unregister, args.status]):
        result = cal.scan()
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(cal.format_text(result))

    if args.export_csv is not None:
        path = cal.export_csv(args.export_csv or None)
        print(f"CSV 已导出：{path}")


if __name__ == "__main__":
    main()
