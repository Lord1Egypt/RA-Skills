#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quake CLI wrapper (single-file, portable).

Features:
- Wraps local quake executable
- Interactive input for key and query parameters
- Auto paging for search/domain/host
- Export CSV and raw text
"""

from __future__ import annotations

import argparse
import csv
import platform
import re
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple


DEFAULT_PAGE_SIZE = 100
MAX_PAGE_SIZE = 100


class QuakeCliError(Exception):
    pass


ANSI_ESCAPE_RE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def script_dir() -> Path:
    return Path(__file__).resolve().parent


def resolve_quake_binary(manual_path: Optional[str] = None) -> Path:
    if manual_path:
        candidate = Path(manual_path).expanduser()
        if not candidate.is_absolute():
            candidate = script_dir() / candidate
        if candidate.exists():
            return candidate
        raise QuakeCliError(f"指定的 quake 二进制不存在: {candidate}")

    system_name = platform.system().lower()
    if "windows" in system_name:
        candidate = script_dir() / "quake.exe"
        if candidate.exists():
            return candidate
    elif "darwin" in system_name:
        candidate = script_dir() / "quake_for_Apple"
        if candidate.exists():
            return candidate
    elif "linux" in system_name:
        candidate = script_dir() / "quake_for_Linux"
        if candidate.exists():
            return candidate

    fallback_names = ["quake.exe", "quake_for_Apple", "quake_for_Linux", "quake"]
    for name in fallback_names:
        candidate = script_dir() / name
        if candidate.exists():
            return candidate

    raise QuakeCliError(
        f"未找到可用 Quake 二进制。当前系统: {platform.system()}，"
        f"请确认目录中存在 quake.exe / quake_for_Apple / quake_for_Linux，"
        "或使用 --quake-bin 手动指定。"
    )


def run_quake(args: List[str], quake_bin: Optional[str] = None) -> str:
    exe = resolve_quake_binary(quake_bin)
    cmd = [str(exe)] + args
    proc = subprocess.run(
        cmd,
        cwd=str(script_dir()),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="ignore",
    )
    output = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    if proc.returncode != 0:
        raise QuakeCliError(f"命令失败: {' '.join(args)}\n{output.strip()}")
    return output


def parse_count_total(output: str) -> Tuple[int, Optional[int]]:
    count = 0
    total = None
    clean_output = ANSI_ESCAPE_RE.sub("", output)
    m_count = re.search(r"count:\s*(\d+)", clean_output, flags=re.IGNORECASE)
    if m_count:
        count = int(m_count.group(1))
    m_total = re.search(r"total:\s*(\d+)", clean_output, flags=re.IGNORECASE)
    if m_total:
        total = int(m_total.group(1))
    return count, total


def parse_domain_or_search_rows(output: str, fields: List[str]) -> List[List[str]]:
    rows: List[List[str]] = []
    collect = False
    expected = len(fields)

    for line in output.splitlines():
        s = ANSI_ESCAPE_RE.sub("", line).strip()
        if not s:
            continue
        if "count:" in s and "total:" in s:
            collect = True
            continue
        if not collect:
            continue
        if s.startswith("[") or s.startswith("IP:") or s.startswith("|"):
            continue
        if s.startswith("+]") or s.startswith("[+]") or s.startswith("[-]") or s.startswith("[!]"):
            continue
        if "\t" in s:
            raw_parts = [p.strip() for p in s.split("\t")]
            parts = [p for p in raw_parts]
        else:
            parts = s.split(None, max(0, expected - 1))

        if expected > 0 and len(parts) < expected:
            parts += [""] * (expected - len(parts))
        if expected > 0 and len(parts) > expected:
            parts = parts[:expected]
        if parts:
            rows.append(parts[:expected] if expected > 0 else parts)
    return rows


def parse_host_rows(output: str) -> List[List[str]]:
    rows: List[List[str]] = []
    current_ip = ""
    for line in output.splitlines():
        s = ANSI_ESCAPE_RE.sub("", line).strip()
        if s.startswith("IP:"):
            m = re.search(r"IP:\s*([0-9a-fA-F:\.\/]+)", s)
            if m:
                current_ip = m.group(1)
            continue
        if s.startswith("|"):
            body = s.lstrip("|").strip()
            parts = body.split()
            if len(parts) >= 3:
                port = parts[0]
                protocol = parts[1]
                time_value = parts[-1]
                rows.append([current_ip, port, protocol, time_value])
    return rows


def write_csv(path: Path, header: List[str], rows: List[List[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def init_key(api_key: str, quake_bin: Optional[str] = None) -> None:
    print("[*] 正在初始化 Quake key ...")
    out = run_quake(["init", api_key], quake_bin=quake_bin)
    print(out.strip() or "[+] init 完成")


def run_info(quake_bin: Optional[str] = None) -> None:
    out = run_quake(["info"], quake_bin=quake_bin)
    print(out.strip())


def run_honeypot(ip: str, quake_bin: Optional[str] = None) -> None:
    out = run_quake(["honeypot", ip], quake_bin=quake_bin)
    print(out.strip())


def paged_domain(
    domain: str,
    fields: str,
    page_size: int,
    max_records: int,
    quake_bin: Optional[str],
) -> Tuple[List[List[str]], str, Optional[int]]:
    rows_all: List[List[str]] = []
    raw_chunks: List[str] = []
    fields_list = [x.strip() for x in fields.split(",") if x.strip()]
    start = 0
    total = None

    while len(rows_all) < max_records:
        size = min(page_size, max_records - len(rows_all))
        out = run_quake(
            ["domain", domain, "--start", str(start), "--size", str(size), "-t", fields],
            quake_bin=quake_bin,
        )
        raw_chunks.append(out)
        count, page_total = parse_count_total(out)
        if page_total is not None:
            total = page_total
        page_rows = parse_domain_or_search_rows(out, fields_list)
        rows_all.extend(page_rows)
        print(f"[*] domain 翻页: start={start}, count={count}, 累计={len(rows_all)}")
        if count == 0 or len(page_rows) == 0 or count < size:
            break
        start += size

    return rows_all[:max_records], "\n\n".join(raw_chunks), total


def paged_search(
    query: str,
    fields: str,
    page_size: int,
    max_records: int,
    regex_filter: Optional[str],
    quake_bin: Optional[str],
) -> Tuple[List[List[str]], str, Optional[int]]:
    rows_all: List[List[str]] = []
    raw_chunks: List[str] = []
    fields_list = [x.strip() for x in fields.split(",") if x.strip()]
    start = 0
    total = None

    while len(rows_all) < max_records:
        size = min(page_size, max_records - len(rows_all))
        args = ["search", query, "--start", str(start), "--size", str(size), "-t", fields]
        if regex_filter:
            args += ["-f", regex_filter]
        out = run_quake(args, quake_bin=quake_bin)
        raw_chunks.append(out)
        count, page_total = parse_count_total(out)
        if page_total is not None:
            total = page_total
        page_rows = parse_domain_or_search_rows(out, fields_list)
        rows_all.extend(page_rows)
        print(f"[*] search 翻页: start={start}, count={count}, 累计={len(rows_all)}")
        if count == 0 or len(page_rows) == 0 or count < size:
            break
        start += size

    return rows_all[:max_records], "\n\n".join(raw_chunks), total


def paged_host(
    ip_or_cidr: str,
    page_size: int,
    max_records: int,
    quake_bin: Optional[str],
) -> Tuple[List[List[str]], str, Optional[int]]:
    rows_all: List[List[str]] = []
    raw_chunks: List[str] = []
    start = 0
    total = None

    while len(rows_all) < max_records:
        size = min(page_size, max_records - len(rows_all))
        out = run_quake(
            ["host", ip_or_cidr, "--start", str(start), "--size", str(size)],
            quake_bin=quake_bin,
        )
        raw_chunks.append(out)
        count, page_total = parse_count_total(out)
        if page_total is not None:
            total = page_total
        page_rows = parse_host_rows(out)
        rows_all.extend(page_rows)
        print(f"[*] host 翻页: start={start}, count={count}, 累计={len(rows_all)}")
        if count == 0 or len(page_rows) == 0 or count < size:
            break
        start += size

    return rows_all[:max_records], "\n\n".join(raw_chunks), total


def prompt_required(msg: str) -> str:
    while True:
        v = input(msg).strip()
        if v:
            return v
        print("该项必填，请重新输入。")


def prompt_int(msg: str, default: int, minimum: int, maximum: int) -> int:
    while True:
        raw = input(f"{msg}（默认 {default}）: ").strip()
        if not raw:
            return default
        if not raw.isdigit():
            print("请输入整数。")
            continue
        v = int(raw)
        if v < minimum or v > maximum:
            print(f"请输入 {minimum}-{maximum} 之间的整数。")
            continue
        return v


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Quake CLI 批量查询脚本（单文件）")
    parser.add_argument("--mode", choices=["search", "domain", "host", "info", "honeypot"], help="查询模式")
    parser.add_argument("--key", help="可选，若提供则先执行 quake init <key>")
    parser.add_argument("--quake-bin", help="可选，手动指定 quake 二进制路径")
    parser.add_argument("--query", help="search 模式查询语句")
    parser.add_argument("--domain", help="domain 模式的域名")
    parser.add_argument("--ip", help="host/honeypot 模式的 IP 或网段")
    parser.add_argument("--fields", help="search/domain 显示字段")
    parser.add_argument("--filter", help="search 模式正则过滤")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE, help=f"每页数量(1-{MAX_PAGE_SIZE})")
    parser.add_argument("--max-records", type=int, default=1000, help="最大拉取条数")
    parser.add_argument("--output-csv", default="quake_results.csv", help="CSV 输出文件")
    parser.add_argument("--output-raw", default="quake_results_raw.txt", help="原始输出文件")
    parser.add_argument("--no-interactive", action="store_true", help="无交互模式")
    return parser.parse_args()


def interactive_fill(args: argparse.Namespace) -> argparse.Namespace:
    if args.mode is None:
        args.mode = prompt_required("模式（search/domain/host/info/honeypot）: ").lower()
    if not args.key:
        args.key = input("Quake API key（可选，回车跳过）: ").strip() or None

    if args.mode == "search":
        args.query = args.query or prompt_required("请输入 search 查询语句: ")
        args.fields = args.fields or input("fields（默认 ip,port,title）: ").strip() or "ip,port,title"
    elif args.mode == "domain":
        args.domain = args.domain or prompt_required("请输入域名（如 360.cn）: ")
        args.fields = args.fields or input("fields（默认 domain,ip）: ").strip() or "domain,ip"
    elif args.mode in ("host", "honeypot"):
        args.ip = args.ip or prompt_required("请输入 IP 或网段: ")

    if args.mode in ("search", "domain", "host"):
        args.page_size = prompt_int("每页数量", args.page_size, 1, MAX_PAGE_SIZE)
        args.max_records = prompt_int("最大拉取条数", args.max_records, 1, 1_000_000)
        if args.output_csv == "quake_results.csv":
            custom_csv = input("CSV 输出文件名（默认 quake_results.csv）: ").strip()
            if custom_csv:
                args.output_csv = custom_csv
        if args.output_raw == "quake_results_raw.txt":
            custom_raw = input("RAW 输出文件名（默认 quake_results_raw.txt）: ").strip()
            if custom_raw:
                args.output_raw = custom_raw
    return args


def validate_no_interactive(args: argparse.Namespace) -> None:
    if args.mode is None:
        raise QuakeCliError("--no-interactive 模式下，--mode 必填")
    if args.mode == "search" and not args.query:
        raise QuakeCliError("--no-interactive 模式下，search 需要 --query")
    if args.mode == "domain" and not args.domain:
        raise QuakeCliError("--no-interactive 模式下，domain 需要 --domain")
    if args.mode in ("host", "honeypot") and not args.ip:
        raise QuakeCliError("--no-interactive 模式下，host/honeypot 需要 --ip")
    if args.mode in ("search", "domain", "host") and (args.page_size < 1 or args.page_size > MAX_PAGE_SIZE):
        raise QuakeCliError(f"--page-size 必须在 1~{MAX_PAGE_SIZE}")


def main() -> None:
    args = parse_args()
    if args.no_interactive:
        validate_no_interactive(args)
    else:
        args = interactive_fill(args)

    selected_bin = resolve_quake_binary(args.quake_bin)
    print(f"[*] 使用 Quake 二进制: {selected_bin}")

    if args.key:
        init_key(args.key, quake_bin=str(selected_bin))

    if args.mode == "info":
        run_info(quake_bin=str(selected_bin))
        return

    if args.mode == "honeypot":
        run_honeypot(args.ip, quake_bin=str(selected_bin))
        return

    if args.mode == "domain":
        rows, raw, total = paged_domain(
            domain=args.domain,
            fields=args.fields or "domain,ip",
            page_size=args.page_size,
            max_records=args.max_records,
            quake_bin=str(selected_bin),
        )
        header = [x.strip() for x in (args.fields or "domain,ip").split(",") if x.strip()]
    elif args.mode == "search":
        rows, raw, total = paged_search(
            query=args.query,
            fields=args.fields or "ip,port,title",
            page_size=args.page_size,
            max_records=args.max_records,
            regex_filter=args.filter,
            quake_bin=str(selected_bin),
        )
        header = [x.strip() for x in (args.fields or "ip,port,title").split(",") if x.strip()]
    elif args.mode == "host":
        rows, raw, total = paged_host(
            ip_or_cidr=args.ip,
            page_size=args.page_size,
            max_records=args.max_records,
            quake_bin=str(selected_bin),
        )
        header = ["ip", "port", "protocol", "time"]
    else:
        raise QuakeCliError(f"未知模式: {args.mode}")

    csv_path = Path(args.output_csv)
    raw_path = Path(args.output_raw)
    write_csv(csv_path, header, rows)
    write_text(raw_path, raw)

    print(f"[+] CSV 已导出: {csv_path.resolve()}")
    print(f"[+] RAW 已导出: {raw_path.resolve()}")
    print(f"[+] 导出条数: {len(rows)}")
    if total is not None:
        print(f"[+] 目标总量(平台返回): {total}")


if __name__ == "__main__":
    try:
        main()
    except QuakeCliError as exc:
        print(f"[!] 错误: {exc}")
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\n[!] 用户中断")
        raise SystemExit(130)
