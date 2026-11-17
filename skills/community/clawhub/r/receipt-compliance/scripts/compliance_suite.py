#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
合规管理统一出口（v4.4.0）

把原本割裂的两块能力合并为一次执行：
1. 税务风险预警（5 类规则 + 白名单 + YAML 热加载）
2. 电子档案四性检测（真实性 / 完整性 / 可用性 / 安全性）
3. 异常检测（轻量 Isolation Forest，可关闭）

一次执行产出一份完整合规报告，避免「先跑风险、再跑归档」的割裂体验。
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List, Iterable

try:
    from unified_invoice import UnifiedInvoice
    from risk_detector import RiskDetector, load_rules, normalize_rules
    from anomaly_detector import AnomalyDetector
except ImportError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from unified_invoice import UnifiedInvoice
    from risk_detector import RiskDetector, load_rules, normalize_rules
    from anomaly_detector import AnomalyDetector


DEFAULT_ARCHIVE_DIR = Path.home() / ".workbuddy" / "output" / "archive"


class ComplianceSuite:
    """合规管理统一出口"""

    def __init__(self, rules_path: Optional[str] = None,
                 archive_dir: Optional[str] = None,
                 enable_anomaly: bool = True):
        self.rules_path = rules_path
        self.archive_dir = Path(archive_dir) if archive_dir else DEFAULT_ARCHIVE_DIR
        self.enable_anomaly = enable_anomaly
        self.rules = normalize_rules(load_rules(rules_path))

    # ---------- 归档四性检测 ----------

    def check_archive(self, files: Optional[Iterable[str]]) -> Dict[str, Any]:
        """对票据文件做四性检测"""
        files = list(files or [])
        if not files:
            return {"enabled": False, "total": 0,
                    "note": "未提供票据文件，跳过归档四性检测"}

        try:
            from archive_manager import ArchiveManager
        except ImportError:
            return {"enabled": False, "total": len(files),
                    "error": "archive_manager 不可用"}

        self.archive_dir.mkdir(parents=True, exist_ok=True)
        manager = ArchiveManager(output_dir=str(self.archive_dir))

        items: List[Dict[str, Any]] = []
        success = 0
        failed = 0
        passed = 0
        for f in files:
            try:
                result = manager.four_properties_check(str(f))
                ok = bool(result.get("passed", result.get("overall_passed", True)))
                if ok:
                    passed += 1
                success += 1
                items.append({"file": str(f), "ok": ok, "detail": result})
            except Exception as e:
                failed += 1
                items.append({"file": str(f), "ok": False, "error": str(e)})

        return {
            "enabled": True,
            "total": len(files),
            "success": success,
            "failed": failed,
            "passed": passed,
            "pass_rate": round(passed / len(files), 4) if files else 0.0,
            "archive_dir": str(self.archive_dir),
            "items": items,
        }

    # ---------- 主流程 ----------

    def run(self, invoices: List, files: Optional[Iterable[str]] = None,
            output_invoices: Optional[List] = None) -> Dict[str, Any]:
        """
        一次执行：风险预警 + 异常检测 + 归档四性检测

        Args:
            invoices: 进项票据（UnifiedInvoice 或 dict）
            files: 票据原始文件路径列表（可选，用于归档四性检测）
            output_invoices: 销项票据（可选，用于进销项匹配）
        """
        invoices = [_as_invoice(x) for x in (invoices or [])]

        # 1. 规则预警
        detector = RiskDetector(rules_path=self.rules_path)
        detector.load_invoices(invoices)
        if output_invoices:
            detector.load_output_invoices([_as_invoice(x) for x in output_invoices])
        risk_report = detector.detect_all()

        # 2. 异常检测
        anomaly_report: Dict[str, Any] = {"enabled": False}
        if self.enable_anomaly:
            cfg = self.rules.get("anomaly_detection") or {}
            if cfg.get("enabled", True):
                try:
                    anomaly_report = AnomalyDetector(
                        n_trees=int(cfg.get("n_trees", 100)),
                        sample_size=int(cfg.get("sample_size", 256)),
                        warn_score=float(cfg.get("warn_score", 0.65)),
                        high_score=float(cfg.get("high_score", 0.75)),
                        max_samples=int(cfg.get("max_samples", 5000)),
                    ).detect(invoices)
                    anomaly_report["enabled"] = True
                except Exception as e:
                    anomaly_report = {"enabled": False, "error": str(e)}

        # 3. 归档四性检测
        archive_report = self.check_archive(files)

        # 4. 汇总
        status = self._judge(risk_report, anomaly_report, archive_report)
        return {
            "report_date": datetime.now().isoformat(timespec="seconds"),
            "invoice_count": len(invoices),
            "overall_status": status,
            "summary": self._summary(risk_report, anomaly_report, archive_report),
            "risk": risk_report,
            "anomaly": anomaly_report,
            "archive": archive_report,
        }

    # ---------- 汇总判定 ----------

    @staticmethod
    def _judge(risk: Dict, anomaly: Dict, archive: Dict) -> str:
        status = "合规"
        if (risk.get("findings_by_level", {}).get("严重")
                or _count_level(anomaly, "严重")):
            return "需立即处理"

        if risk.get("findings_by_level", {}).get("关注") or _count_level(anomaly, "关注"):
            status = "需关注"
        elif risk.get("findings_by_level", {}).get("提示"):
            status = "需关注"

        if archive.get("enabled") and archive.get("failed"):
            status = "需关注"
        return status

    @staticmethod
    def _summary(risk: Dict, anomaly: Dict, archive: Dict) -> Dict[str, Any]:
        return {
            "风险预警条数": risk.get("total_findings", 0),
            "风险等级": risk.get("overall_risk_level", "无风险"),
            "异常检测条数": anomaly.get("total_findings", 0) if anomaly.get("enabled") else 0,
            "归档检测": {
                "总数": archive.get("total", 0),
                "通过": archive.get("passed", 0),
                "失败": archive.get("failed", 0),
            },
        }

    def export(self, report: Dict[str, Any], output_path: str) -> str:
        p = Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(p)

    @staticmethod
    def format_text(report: Dict[str, Any]) -> str:
        s = report["summary"]
        lines = [
            f"合规管理报告 · {report['report_date']}",
            f"整体状态：{report['overall_status']}",
            f"票据数：{report['invoice_count']}",
            "",
            f"  风险预警：{s['风险预警条数']} 条（等级 {s['风险等级']}）",
            f"  异常检测：{s['异常检测条数']} 条",
            f"  归档四性：{s['归档检测']['总数']} 个文件，通过 {s['归档检测']['通过']}，"
            f"失败 {s['归档检测']['失败']}",
        ]
        return "\n".join(lines)


def _as_invoice(item) -> UnifiedInvoice:
    """把 dict 转成 UnifiedInvoice，已是对象则原样返回"""
    if isinstance(item, UnifiedInvoice):
        return item
    if isinstance(item, dict):
        fields = UnifiedInvoice().__dict__.keys()
        return UnifiedInvoice(**{k: v for k, v in item.items() if k in fields})
    return item


def _count_level(anomaly: Dict, level: str) -> int:
    if not anomaly.get("enabled"):
        return 0
    return sum(1 for f in anomaly.get("findings", []) if f.get("level") == level)


def _load_invoices(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = data.get("invoices") or data.get("results") or []
    return data


def main():
    import argparse
    parser = argparse.ArgumentParser(description="合规管理统一出口")
    parser.add_argument("--invoices", help="进项票据 JSON 文件")
    parser.add_argument("--outputs", help="销项票据 JSON 文件（可选，用于进销项匹配）")
    parser.add_argument("--db", help="直接从台账数据库读取（替代 --invoices）")
    parser.add_argument("--direction", choices=["input", "output", "all"], default="input")
    parser.add_argument("--files", nargs="*", help="票据原始文件（归档四性检测）")
    parser.add_argument("--files-dir", help="票据目录，自动收集其中文件")
    parser.add_argument("--rules", help="规则 YAML 路径")
    parser.add_argument("--archive-dir", help="归档输出目录")
    parser.add_argument("--no-anomaly", action="store_true", help="关闭异常检测")
    parser.add_argument("--output", help="报告 JSON 输出路径")
    args = parser.parse_args()

    suite = ComplianceSuite(rules_path=args.rules,
                            archive_dir=args.archive_dir,
                            enable_anomaly=not args.no_anomaly)

    if args.db:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from ledger_db import LedgerDB
        db = LedgerDB(args.db)
        direction = None if args.direction == "all" else args.direction
        invoices = db.query_invoices(direction=direction)
        db.close()
    elif args.invoices:
        invoices = _load_invoices(args.invoices)
    else:
        parser.error("需指定 --invoices 或 --db")
        return

    outputs = _load_invoices(args.outputs) if args.outputs else None

    files = list(args.files or [])
    if args.files_dir:
        d = Path(args.files_dir)
        files += [str(p) for p in sorted(d.iterdir()) if p.is_file()]

    report = suite.run(invoices, files=files, output_invoices=outputs)

    if args.output:
        print(suite.export(report, args.output))
        print(f"报告已保存：{args.output}")
    else:
        print(suite.format_text(report))


if __name__ == "__main__":
    main()
