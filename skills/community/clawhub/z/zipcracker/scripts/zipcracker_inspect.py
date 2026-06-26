#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from zipcracker_core import (
    HAS_PYZIPPER,
    collect_archive_encryption_profile,
    compress_type_label,
    detect_template_kpa_suggestions,
    find_best_verification_entry,
    fix_zip_encrypted,
    format_os_label,
    detect_os_info,
    get_bkcrack_version,
    is_regular_member,
    is_zip_encrypted,
    loc,
    _has_winzip_aes_extra,
    find_bkcrack_executable,
)


SCRIPT_DIR = Path(__file__).resolve().parent
WRAPPER_PATH = SCRIPT_DIR / "openclaw_zipcracker.py"


def default_lang() -> str:
    for env_name in ("ZIPCRACKER_SKILL_LANG", "LC_ALL", "LC_MESSAGES", "LANG"):
        value = os.environ.get(env_name, "").strip().lower()
        if value.startswith("en"):
            return "en"
        if value.startswith("zh"):
            return "zh"
    return "zh"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect a ZIP archive and suggest the best ZipCracker attack path."
    )
    parser.add_argument("zip_path", help="Target ZIP file")
    parser.add_argument(
        "--lang",
        choices=("zh", "en"),
        default=default_lang(),
        help="Output language",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit structured JSON instead of the human summary.",
    )
    parser.add_argument(
        "--max-entries",
        type=int,
        default=50,
        help="Maximum number of member entries to include in the report.",
    )
    return parser.parse_args(argv)


def shell_quote(value: str) -> str:
    return shlex.quote(value)


def detect_pseudo_encryption(zip_path: str) -> dict[str, Any]:
    if not os.path.exists(zip_path):
        return {"status": "missing"}
    if not is_zip_encrypted(zip_path):
        return {"status": "not-encrypted"}

    fd, temp_path = tempfile.mkstemp(prefix="zipcracker_inspect_", suffix=".fixed.zip")
    os.close(fd)
    try:
        fix_zip_encrypted(zip_path, temp_path)
        with zipfile.ZipFile(temp_path, "r") as zf:
            bad_member = zf.testzip()
        if bad_member:
            return {"status": "not-confirmed", "detail": f"bad member: {bad_member}"}
        return {"status": "confirmed"}
    except Exception as exc:
        return {"status": "not-confirmed", "detail": str(exc)}
    finally:
        try:
            os.remove(temp_path)
        except OSError:
            pass


def collect_entries(zip_path: str, max_entries: int) -> dict[str, Any]:
    result: dict[str, Any] = {
        "entries": [],
        "total_regular_entries": 0,
        "truncated": False,
        "best_verification_entry": None,
    }
    with zipfile.ZipFile(zip_path, "r") as zf:
        infos = [info for info in zf.infolist() if is_regular_member(info)]
        result["total_regular_entries"] = len(infos)
        result["best_verification_entry"] = find_best_verification_entry(zf)
        for index, info in enumerate(infos):
            if index >= max_entries:
                result["truncated"] = True
                break
            result["entries"].append(
                {
                    "name": info.filename,
                    "file_size": info.file_size,
                    "compress_size": info.compress_size,
                    "compress_type": compress_type_label(info.compress_type),
                    "encrypted": bool(info.flag_bits & 0x1),
                    "aes": bool(_has_winzip_aes_extra(info)),
                    "short_plaintext_candidate": 0 < info.file_size <= 6,
                }
            )
    return result


def build_recommendations(report: dict[str, Any], locale: str) -> list[dict[str, str]]:
    zip_path = report["zip_path"]
    wrapper = str(WRAPPER_PATH)
    quoted_wrapper = shell_quote(wrapper)
    quoted_zip = shell_quote(zip_path)
    recommendations: list[dict[str, str]] = []

    def add(title_zh: str, title_en: str, reason_zh: str, reason_en: str, args: list[str]) -> None:
        command = " ".join([shell_quote(sys.executable), quoted_wrapper, *args, quoted_zip])
        recommendations.append(
            {
                "title": loc(locale, title_zh, title_en),
                "reason": loc(locale, reason_zh, reason_en),
                "command": command,
            }
        )

    if not report["is_valid_zip"]:
        return recommendations

    if not report["is_encrypted"]:
        add(
            "直接解压/校验",
            "Extract directly",
            "当前档案没有发现加密条目，不需要走破解流程。",
            "No encrypted members were detected, so cracking is unnecessary.",
            [],
        )
        return recommendations

    pseudo_status = report["pseudo_encryption"]["status"]
    if pseudo_status == "confirmed":
        add(
            "优先按伪加密处理",
            "Handle as pseudo-encryption first",
            "清除加密位后校验通过，极可能是伪加密题。",
            "Clearing the encryption bit validated successfully, so this strongly resembles pseudo-encryption.",
            [],
        )
        return recommendations

    if report["short_plaintext_entries"]:
        add(
            "先试短明文 CRC32",
            "Try short-plaintext CRC32 first",
            "存在 1-6 字节的条目，适合先走短明文 CRC32 枚举恢复。",
            "The archive contains 1-6 byte entries, so short-plaintext CRC32 enumeration is a strong first move.",
            ["--auto-crc"],
        )

    if report["template_suggestions"]:
        add(
            "默认流程并自动跟进模板 KPA",
            "Run default flow with template KPA follow-up",
            "检测到与 png/zip/exe/pcapng 模板相符的加密条目。",
            "Encrypted members look compatible with built-in png/zip/exe/pcapng template KPA cases.",
            ["--auto-template-kpa"],
        )

    add(
        "先跑标准默认流程",
        "Run the standard default flow",
        "先让引擎按原始策略依次尝试伪加密、默认字典、数字字典，再决定是否切换其他战术。",
        "Let the engine follow its original strategy first: pseudo-encryption check, bundled dictionary, numeric fallback, then escalate if needed.",
        [],
    )

    if report["encryption_profile"]["aes_entries"] > 0 and not report["pyzipper_ready"]:
        recommendations.append(
            {
                "title": loc(locale, "AES 注意事项", "AES caution"),
                "reason": loc(
                    locale,
                    "该包含有 AES 条目，但当前环境未启用 pyzipper。掩码/字典前应优先补齐 AES 依赖。",
                    "This archive contains AES entries, but pyzipper is not enabled. Install/enable AES support before relying on dictionary or mask workflows.",
                ),
                "command": "",
            }
        )

    if report["bkcrack_available"]:
        recommendations.append(
            {
                "title": loc(locale, "已知明文时优先用 KPA", "Prefer KPA when plaintext exists"),
                "reason": loc(
                    locale,
                    "系统已检测到 bkcrack；如果你手里有完整/部分明文、参考 ZIP 或文件头线索，应优先切到 KPA 路线。",
                    "bkcrack is available; if you have full/partial plaintext, a reference ZIP, or strong file-signature clues, prefer the KPA path over blind brute force.",
                ),
                "command": "",
            }
        )

    return recommendations


def build_report(zip_path: str, locale: str, max_entries: int) -> dict[str, Any]:
    report: dict[str, Any] = {
        "zip_path": os.path.abspath(zip_path),
        "is_valid_zip": False,
        "exists": os.path.exists(zip_path),
        "is_encrypted": False,
        "pyzipper_ready": bool(HAS_PYZIPPER),
        "bkcrack_available": False,
        "bkcrack_version": None,
        "system_label": format_os_label(locale, detect_os_info()),
        "encryption_profile": {},
        "pseudo_encryption": {"status": "unknown"},
        "entries": [],
        "total_regular_entries": 0,
        "entries_truncated": False,
        "best_verification_entry": None,
        "short_plaintext_entries": [],
        "template_suggestions": [],
        "recommendations": [],
    }

    if not report["exists"]:
        report["recommendations"] = []
        return report

    try:
        with zipfile.ZipFile(zip_path, "r"):
            pass
    except Exception as exc:
        report["invalid_reason"] = str(exc)
        return report

    report["is_valid_zip"] = True
    report["is_encrypted"] = is_zip_encrypted(zip_path)
    report["encryption_profile"] = collect_archive_encryption_profile(zip_path)
    report["pseudo_encryption"] = detect_pseudo_encryption(zip_path)

    entry_info = collect_entries(zip_path, max_entries)
    report["entries"] = entry_info["entries"]
    report["total_regular_entries"] = entry_info["total_regular_entries"]
    report["entries_truncated"] = entry_info["truncated"]
    report["best_verification_entry"] = entry_info["best_verification_entry"]
    report["short_plaintext_entries"] = [
        entry for entry in report["entries"] if entry["short_plaintext_candidate"]
    ]

    suggestions = detect_template_kpa_suggestions(zip_path, locale)
    report["template_suggestions"] = [
        {
            "inner_name": item.inner_name,
            "template_name": item.template_name,
            "file_size": item.file_size,
            "compress_type": compress_type_label(item.compress_type),
            "confidence": item.confidence,
            "reason": item.reason,
        }
        for item in suggestions
    ]

    bk_path = find_bkcrack_executable()
    if bk_path:
        report["bkcrack_available"] = True
        report["bkcrack_path"] = bk_path
        report["bkcrack_version"] = get_bkcrack_version(bk_path)

    report["recommendations"] = build_recommendations(report, locale)
    return report


def render_summary(report: dict[str, Any], locale: str) -> str:
    lines: list[str] = []
    lines.append(loc(locale, f"[+] 目标 ZIP: {report['zip_path']}", f"[+] Target ZIP: {report['zip_path']}"))
    if not report["exists"]:
        lines.append(loc(locale, "[-] 文件不存在。", "[-] File does not exist."))
        return "\n".join(lines)
    if not report["is_valid_zip"]:
        reason = report.get("invalid_reason", "")
        lines.append(loc(locale, f"[-] 不是有效 ZIP: {reason}", f"[-] Not a valid ZIP: {reason}"))
        return "\n".join(lines)

    lines.append(
        loc(
            locale,
            f"[+] 常规文件条目: {report['total_regular_entries']}，加密条目: {report['encryption_profile'].get('encrypted_entries', 0)}，未加密条目: {report['encryption_profile'].get('unencrypted_entries', 0)}",
            f"[+] Regular members: {report['total_regular_entries']}, encrypted: {report['encryption_profile'].get('encrypted_entries', 0)}, unencrypted: {report['encryption_profile'].get('unencrypted_entries', 0)}",
        )
    )
    lines.append(
        loc(
            locale,
            f"[*] 加密构成: ZipCrypto={report['encryption_profile'].get('zipcrypto_entries', 0)}, AES={report['encryption_profile'].get('aes_entries', 0)}",
            f"[*] Encryption mix: ZipCrypto={report['encryption_profile'].get('zipcrypto_entries', 0)}, AES={report['encryption_profile'].get('aes_entries', 0)}",
        )
    )
    lines.append(
        loc(
            locale,
            f"[*] pyzipper: {'已启用' if report['pyzipper_ready'] else '未启用'}，bkcrack: {'可用' if report['bkcrack_available'] else '不可用'}",
            f"[*] pyzipper: {'enabled' if report['pyzipper_ready'] else 'unavailable'}, bkcrack: {'available' if report['bkcrack_available'] else 'unavailable'}",
        )
    )
    if report["bkcrack_available"] and report.get("bkcrack_version"):
        lines.append(
            loc(
                locale,
                f"[*] bkcrack 版本: {report['bkcrack_version']}",
                f"[*] bkcrack version: {report['bkcrack_version']}",
            )
        )

    pseudo = report["pseudo_encryption"]
    pseudo_status_map = {
        "confirmed": loc(locale, "可直接按伪加密处理", "confirmed pseudo-encryption"),
        "not-confirmed": loc(locale, "未确认伪加密，更像真加密", "not confirmed; likely truly encrypted"),
        "not-encrypted": loc(locale, "未发现加密", "archive is not encrypted"),
        "missing": loc(locale, "文件不存在", "file missing"),
        "unknown": loc(locale, "未知", "unknown"),
    }
    lines.append(
        loc(
            locale,
            f"[*] 伪加密判断: {pseudo_status_map.get(pseudo['status'], pseudo['status'])}",
            f"[*] Pseudo-encryption check: {pseudo_status_map.get(pseudo['status'], pseudo['status'])}",
        )
    )

    if report["best_verification_entry"]:
        lines.append(
            loc(
                locale,
                f"[*] 推荐验证条目: {report['best_verification_entry']}",
                f"[*] Best verification entry: {report['best_verification_entry']}",
            )
        )

    if report["short_plaintext_entries"]:
        names = ", ".join(
            f"{item['name']}({item['file_size']}B)" for item in report["short_plaintext_entries"]
        )
        lines.append(
            loc(
                locale,
                f"[*] 短明文候选: {names}",
                f"[*] Short-plaintext candidates: {names}",
            )
        )

    if report["template_suggestions"]:
        lines.append(loc(locale, "[*] 模板 KPA 候选:", "[*] Template KPA candidates:"))
        for item in report["template_suggestions"]:
            lines.append(
                loc(
                    locale,
                    f"    - {item['inner_name']} -> {item['template_name']} ({item['confidence']}, {item['compress_type']}, {item['file_size']}B)",
                    f"    - {item['inner_name']} -> {item['template_name']} ({item['confidence']}, {item['compress_type']}, {item['file_size']}B)",
                )
            )

    if report["entries"]:
        lines.append(loc(locale, "[*] 成员概览:", "[*] Member overview:"))
        for item in report["entries"]:
            tag_parts = []
            if item["encrypted"]:
                tag_parts.append("enc")
            if item["aes"]:
                tag_parts.append("aes")
            if item["short_plaintext_candidate"]:
                tag_parts.append("short")
            tag_text = ",".join(tag_parts) if tag_parts else "plain"
            lines.append(
                f"    - {item['name']} | {item['file_size']}B | {item['compress_type']} | {tag_text}"
            )
        if report["entries_truncated"]:
            lines.append(
                loc(locale, "    - ... 其余条目已省略", "    - ... additional entries omitted")
            )

    if report["recommendations"]:
        lines.append(loc(locale, "[+] 推荐下一步:", "[+] Recommended next steps:"))
        for index, rec in enumerate(report["recommendations"], start=1):
            lines.append(f"{index}. {rec['title']}")
            lines.append(f"   {rec['reason']}")
            if rec["command"]:
                lines.append(f"   {rec['command']}")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    report = build_report(args.zip_path, args.lang, args.max_entries)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_summary(report, args.lang))
    return 0 if report["exists"] and report["is_valid_zip"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
