#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yotta-triage（元鉴）—— 零依赖自研恶意样本静态初筛引擎
================================================================

跨智能体的恶意样本静态初筛能力：对给定文件 / 目录做**纯静态**特征分析，
不反混淆、不解包、不动态执行。输出 triage 报告与 IOC（hash / URL / 域 / IP / 邮箱），
供元情（yotta-intel）等下游消费。

特性
----
- 哈希：MD5 / SHA1 / SHA256（流式计算，大文件不吃内存）
- 类型：魔数识别（PE / ELF / Mach-O / PDF / ZIP / gzip / 7z / RAR / OLE / 图片 / pyc / Java class）
- 熵：整体 Shannon 熵 + PE 区段熵（加壳 / 加密 / 压缩线索）
- 字符串：可打印字符串（ASCII + UTF-16LE），分类提取 URL / 域名 / IP / 邮箱 /
  可疑命令 / 路径 / 长 base64
- PE 头解析：机器类型 / 时间戳 / 可选头 / 区段表（名称 / 特性 / 熵），识别加壳区段与 RWX 区段
- ELF 头解析：位宽 / 字节序 / 机器 / 类型 / 入口 / 段表（RWX 段 / 区段标志）
- 风险分级提示：静态指标加权给出 info/low/medium/high/critical 的**线索级**提示
  （triage 只提示可疑，不定性恶意，结论需人工 / 其他情报源核实）
- IOC 输出：hash / URL / 域 / IP / 邮箱 -> JSON（供元情消费）
- 纯本地离线：不联网查证、不下载、不执行任何样本（红线）

用法
----
  python3 scripts/yotta_triage.py triage --path sample.exe
  python3 scripts/yotta_triage.py triage --path samples/ --recursive
  python3 scripts/yotta_triage.py triage --path sample.exe --format json --output report.json
  python3 scripts/yotta_triage.py triage --path samples/ --format markdown --output report.md
  python3 scripts/yotta_triage.py triage --path samples/ --ioc-only --output iocs.json
  python3 scripts/yotta_triage.py --version

退出码：0 = 最高风险 <= low；1 = medium；2 = high；3 = critical；4 = 用法或读取错误。
Windows 下用 python 代替 python3。
"""

import argparse
import hashlib
import json
import math
import os
import re
import struct
import sys
from datetime import datetime, timezone

try:
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VERSION = "0.1.6"
TOOL = "yotta-triage"
TOOL_CN = "元鉴"

# 内存分析窗口：文件哈希流式算，特征分析只取前 N 字节（大文件不整体读入）
MAX_ANALYZE_BYTES = 16 * 1024 * 1024
# 超过该大小的文件直接跳过（可配 --max-file-mb）
DEFAULT_MAX_FILE_MB = 256

RISK_LEVELS = ("info", "low", "medium", "high", "critical")
RISK_EXIT = {"info": 0, "low": 0, "medium": 1, "high": 2, "critical": 3}
RISK_LABELS = {
    "info": "无明显异常",
    "low": "低风险线索",
    "medium": "中等风险线索",
    "high": "高风险线索",
    "critical": "严重风险线索",
}

# ---------------------------------------------------------------------------
# 魔数识别
# ---------------------------------------------------------------------------
MAGIC_RULES = (
    (b"MZ", "pe", "DOS/PE executable (MZ)"),
    (b"\x7fELF", "elf", "ELF executable"),
    (b"\xcf\xfa\xed\xfe", "macho", "Mach-O 64-bit"),
    (b"\xce\xfa\xed\xfe", "macho", "Mach-O 32-bit"),
    (b"\xfe\xed\xfa\xcf", "macho", "Mach-O 64-bit (big-endian)"),
    (b"\xfe\xed\xfa\xce", "macho", "Mach-O 32-bit (big-endian)"),
    (b"\xca\xfe\xba\xbe", "macho", "Mach-O fat / Java class"),
    (b"\x25\x50\x44\x46", "pdf", "PDF document"),
    (b"PK\x03\x04", "zip", "ZIP archive (PK)"),
    (b"PK\x05\x06", "zip", "ZIP empty archive"),
    (b"\x1f\x8b", "gzip", "gzip compressed"),
    (b"7z\xbc\xaf\x27\x1c", "7z", "7-Zip archive"),
    (b"Rar!", "rar", "RAR archive"),
    (b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1", "ole", "OLE2/CFB (Office/MSI)"),
    (b"\x89PNG\r\n\x1a\n", "image", "PNG image"),
    (b"\xff\xd8\xff", "image", "JPEG image"),
    (b"GIF8", "image", "GIF image"),
    (b"\x00\x00\x01\x00", "icon", "Windows ICO/CUR"),
    (b"\x03\xf3\x0d\x0a", "pyc", "Python bytecode (pyc)"),
    (b"\x1a\x2b\x3c\x4d", "class", "Java class (old magic)"),
)

PE_MACHINES = {
    0x014C: "x86 (i386)",
    0x01C0: "ARM",
    0x01C2: "ARM Thumb-2",
    0x01C4: "ARMv7",
    0x0200: "IA64",
    0x8664: "x86-64",
    0xAA64: "ARM64",
    0x5032: "RISC-V 32",
    0x5064: "RISC-V 64",
}
PE_SUBSYSTEMS = {
    1: "NATIVE", 2: "WINDOWS_GUI", 3: "WINDOWS_CUI",
    7: "POSIX_CUI", 9: "WINDOWS_CE_GUI", 10: "EFI_APPLICATION",
}
PACKED_SECTION_HINTS = {
    ".upx0", ".upx1", ".upx2", ".upx3", ".packed", ".aspack", ".adata", ".nsp0",
    ".nsp1", ".nsp2", ".petite", ".mpress1", ".mpress2", ".enigma1", ".enigma2",
    ".themida", ".vmp0", ".vmp1", ".vmp2", ".sforce3", ".pklst", ".boom",
}

ELF_MACHINES = {
    3: "x86 (i386)", 8: "MIPS", 20: "PowerPC", 21: "PowerPC64",
    40: "ARM", 62: "x86-64", 183: "ARM64", 243: "RISC-V", 247: "RISC-V",
}
ELF_TYPES = {0: "NONE", 1: "REL", 2: "EXEC", 3: "DYN", 4: "CORE"}

# ---------------------------------------------------------------------------
# 基础函数
# ---------------------------------------------------------------------------
def shannon_entropy(data):
    """返回 0..8 的 Shannon 熵（对空数据返回 0）。"""
    if not data:
        return 0.0
    n = len(data)
    counts = [0] * 256
    for b in data:
        counts[b] += 1
    ent = 0.0
    for c in counts:
        if c:
            p = c / float(n)
            ent -= p * math.log2(p)
    return ent


def file_hashes(path):
    """流式计算 MD5 / SHA1 / SHA256。"""
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            md5.update(chunk)
            sha1.update(chunk)
            sha256.update(chunk)
    return {
        "md5": md5.hexdigest(),
        "sha1": sha1.hexdigest(),
        "sha256": sha256.hexdigest(),
    }


def detect_type(data):
    """魔数识别文件类型。返回 (kind, label, magic_name)。"""
    head = data[:16]
    for magic, kind, label in MAGIC_RULES:
        if head.startswith(magic):
            return kind, label, magic.hex()
    # 文本 / 脚本启发
    sample = data[:4096]
    if sample:
        printable = sum(1 for b in sample if 0x09 <= b <= 0x0D or 0x20 <= b <= 0x7E)
        if printable / float(len(sample)) >= 0.85:
            if sample.startswith(b"#!"):
                return "script", "script (shebang)", "text"
            return "text", "text / script", "text"
        try:
            sample.decode("utf-8")
            return "text", "text / script (utf-8)", "text"
        except UnicodeDecodeError:
            pass
    return "data", "data / unknown", ""


# ---------------------------------------------------------------------------
# 字符串提取与分类
# ---------------------------------------------------------------------------
ASCII_STRINGS_MIN = 4

URL_RE = re.compile(r"(?i)(?:https?|ftp)://[^\s\"'<>()\[\]{}\\\x00-\x1f]+")
DOMAIN_RE = re.compile(r"(?<![\w.@-])(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}(?![\w@.-])", re.IGNORECASE)
IPV4_RE = re.compile(r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)")
EMAIL_RE = re.compile(r"(?<![\w.+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?![\w.@-])")
BASE64_RE = re.compile(r"(?<![A-Za-z0-9+/=])(?:[A-Za-z0-9+/]{60,}={0,2})(?![A-Za-z0-9+/=])")

PATH_RE = re.compile(
    r"(?i)(?:[a-z]:\\[^\s\"'<>]{3,}|\\\\[^\s\"'<>]{3,}|%[a-z]+%\\[^\s\"'<>]{3,}"
    r"|/etc/[^\s\"'<>]{3,}|/tmp/[^\s\"'<>]{3,}|/var/[^\s\"'<>]{3,}|/usr/[^\s\"'<>]{3,}"
    r"|/bin/[^\s\"'<>]{3,}|/dev/[^\s\"'<>]{3,}|\\windows\\[^\s\"'<>]{3,}|\\system32\\[^\s\"'<>]{3,}"
    r"|\\appdata\\[^\s\"'<>]{3,}|\\users\\[^\s\"'<>]{3,})"
)

# 常见文件扩展名 / 非 TLD 后缀（域名判定黑名单，避免 payload.exe / a.exe 之类被误判为域名）
NON_TLD = frozenset("""
exe dll py js ts txt md png jpg jpeg gif svg webp zip gz tar 7z rar pdf doc docx
xls xlsx ppt pptx csv json yml yaml xml html htm css sh bat ps1 cmd vbs sys ini
cfg conf log bak tmp dat bin so a o obj class jar apk app msi iso img deb rpm
toml lock mp3 mp4 avi png wav
""".split())

# 可疑命令关键字 -> 标签（按优先级；命中即记标签）
SUSPICIOUS_COMMANDS = (
    (re.compile(r"powershell.{0,24}-(enc|encodedcommand)", re.I), "powershell-encoded-command"),
    (re.compile(r"certutil.{0,48}(-urlcache|-decode|-download)", re.I), "certutil-download-decode"),
    (re.compile(r"bitsadmin.{0,40}/transfer", re.I), "bitsadmin-transfer"),
    (re.compile(r"regsvr32.{0,40}/s.{0,24}/i:", re.I), "regsvr32-sct"),
    (re.compile(r"mshta", re.I), "mshta"),
    (re.compile(r"rundll32", re.I), "rundll32"),
    (re.compile(r"schtasks.{0,40}/create", re.I), "schtasks-create"),
    (re.compile(r"cmd(\.exe)?.{0,12}/c.{0,12}(powershell|cmd|wmic)", re.I), "cmd-spawn-shell"),
    (re.compile(r"(?i)\biex\b|invoke-expression", re.I), "invoke-expression"),
    (re.compile(r"(?i)invoke-webrequest|invoke-restmethod|iwr\b|curl\b|wget\b", re.I), "download-command"),
    (re.compile(r"(downloadstring|downloadfile|start-process).{0,60}(https?|ftp)://", re.I), "download-execute"),
    (re.compile(r"(frombase64string|convert\.frombase64string|base64.{0,20}-d)", re.I), "base64-decode"),
    (re.compile(r"(reflection\.assembly|assembly\.load|\.load\()", re.I), "reflective-load"),
    (re.compile(r"\b(wscript|cscript)\b", re.I), "wscript-cscript"),
    (re.compile(r"powershell.{0,24}-windowstyle", re.I), "powershell-hidden-window"),
    (re.compile(r"(?i)start-process.{0,40}-windowstyle", re.I), "start-process-hidden"),
)


def extract_strings(data, min_len=ASCII_STRINGS_MIN, max_strings=5000):
    """提取可打印字符串：ASCII + UTF-16LE。返回 [{"kind","offset","value"}]。"""
    out = []
    n = len(data)
    # ASCII runs
    start = None
    for i in range(n + 1):
        b = data[i] if i < n else None
        ok = (b is not None and 0x20 <= b <= 0x7E)
        if ok:
            if start is None:
                start = i
        else:
            if start is not None:
                end = i
                if end - start >= min_len:
                    out.append({"kind": "ascii", "offset": start,
                                "value": data[start:end].decode("latin-1")})
                    if len(out) >= max_strings:
                        return out
                start = None
    # UTF-16LE runs（偶数偏移为可打印 ASCII，奇数偏移为 0x00）
    start = None
    i = 0
    while i + 1 < n:
        lo, hi = data[i], data[i + 1]
        if hi == 0 and 0x20 <= lo <= 0x7E:
            if start is None:
                start = i
            i += 2
        else:
            if start is not None:
                end = i
                raw = data[start:end:2]
                if len(raw) >= min_len:
                    out.append({"kind": "utf16le", "offset": start,
                                "value": raw.decode("latin-1")})
                    if len(out) >= max_strings:
                        return out
                start = None
            i += 1
    if start is not None:
        end = n
        if end > start and (end - start) % 2 == 1:
            end -= 1
        raw = data[start:end:2]
        if len(raw) >= min_len:
            out.append({"kind": "utf16le", "offset": start, "value": raw.decode("latin-1")})
    return out


def _strip_url_tail(url):
    return url.rstrip(".,;:!?)]}>\"'\x60")


def classify_strings(strings):
    """把字符串列表分类成 URL / 域名 / IP / 邮箱 / 命令 / 路径 / base64。"""
    urls, domains, ips, emails, paths, base64 = [], [], [], [], [], []
    suspicious = []
    seen = {"urls": set(), "domains": set(), "ips": set(), "emails": set(),
            "paths": set(), "base64": set()}
    cmd_seen = set()

    def add(lst, seen_set, value):
        key = value.lower()
        if key not in seen_set:
            seen_set.add(key)
            lst.append(value)

    for s in strings:
        val = s["value"]
        # URL
        for m in URL_RE.finditer(val):
            u = _strip_url_tail(m.group(0))
            if len(u) > len("http://") + 2:
                add(urls, seen["urls"], u)
        # base64（先于普通分类，避免长 base64 块被误拆）
        for m in BASE64_RE.finditer(val):
            b = m.group(0)
            if len(b) >= 60:
                add(base64, seen["base64"], b)
        # 域名 / IP / 邮箱
        for m in DOMAIN_RE.finditer(val):
            d = m.group(0).lower()
            if d.rsplit(".", 1)[-1] in NON_TLD:
                continue
            add(domains, seen["domains"], d)
        for m in IPV4_RE.finditer(val):
            octets = m.group(0)
            if all(0 <= int(o) <= 255 for o in octets.split(".")):
                add(ips, seen["ips"], octets)
        for m in EMAIL_RE.finditer(val):
            add(emails, seen["emails"], m.group(0).lower())
        for m in PATH_RE.finditer(val):
            add(paths, seen["paths"], m.group(0))
        # 可疑命令
        for rx, label in SUSPICIOUS_COMMANDS:
            if rx.search(val):
                if label not in cmd_seen:
                    cmd_seen.add(label)
                    suspicious.append(label)

    return {
        "urls": urls,
        "domains": domains,
        "ips": ips,
        "emails": emails,
        "paths": paths,
        "base64": base64,
        "commands": sorted(cmd_seen),
    }


# ---------------------------------------------------------------------------
# PE / ELF 解析
# ---------------------------------------------------------------------------
def _ts_text(ts):
    try:
        return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception:
        return "invalid"


def parse_pe(data):
    """解析 PE 头。返回 dict 或 None。"""
    if data[:2] != b"MZ":
        return None
    if len(data) < 0x40:
        return {"note": "truncated-dos-header"}
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    if e_lfanew + 4 > len(data) or data[e_lfanew:e_lfanew + 4] != b"PE\x00\x00":
        return {"note": "mz-without-pe-signature", "e_lfanew": e_lfanew}
    off = e_lfanew + 4
    if off + 20 > len(data):
        return {"note": "truncated-coff-header"}
    machine, nsects, ts, _p_sym, _n_sym, opt_size, chars = struct.unpack_from("<HHIIIHH", data, off)
    pe = {
        "machine": PE_MACHINES.get(machine, "0x%04x" % machine),
        "machine_code": machine,
        "sections": nsects,
        "timestamp": ts,
        "timestamp_text": _ts_text(ts),
        "characteristics": chars,
        "dll": bool(chars & 0x2000),
    }
    opt = off + 20
    pe["optional_magic"] = None
    pe["subsystem"] = None
    if opt + 2 <= len(data):
        magic = struct.unpack_from("<H", data, opt)[0]
        pe["optional_magic"] = {0x10B: "PE32", 0x20B: "PE32+"}.get(magic, "0x%04x" % magic)
        if magic in (0x10B, 0x20B) and opt + 70 <= len(data):
            subsystem = struct.unpack_from("<H", data, opt + 68)[0]
            pe["subsystem"] = PE_SUBSYSTEMS.get(subsystem, subsystem)
            pe["subsystem_code"] = subsystem
    # 区段表
    secs = []
    sec_off = opt + opt_size
    for i in range(min(nsects, 96)):
        base = sec_off + i * 40
        if base + 40 > len(data):
            break
        name_raw = data[base:base + 8]
        v_size, v_addr, r_size, r_addr = struct.unpack_from("<IIII", data, base + 8)
        s_chars = struct.unpack_from("<I", data, base + 36)[0]
        name = name_raw.split(b"\x00")[0].decode("latin-1", "replace") or "(noname)"
        sec = {
            "name": name,
            "virtual_size": v_size,
            "raw_size": r_size,
            "executable": bool(s_chars & 0x20000000),
            "writable": bool(s_chars & 0x80000000),
            "code": bool(s_chars & 0x20),
            "entropy": None,
        }
        if r_addr and r_size and r_addr + r_size <= len(data):
            sec["entropy"] = round(shannon_entropy(data[r_addr:r_addr + r_size]), 3)
        secs.append(sec)
    pe["sections_detail"] = secs
    pe["suspicious_sections"] = [s["name"] for s in secs if s["name"].lower() in PACKED_SECTION_HINTS]
    pe["rwx_sections"] = [s["name"] for s in secs if s["executable"] and s["writable"]]
    pe["high_entropy_sections"] = [
        {"name": s["name"], "entropy": s["entropy"]} for s in secs
        if s["entropy"] is not None and s["entropy"] >= 7.0
    ]
    return pe


def parse_elf(data):
    """解析 ELF 头。返回 dict 或 None。"""
    if data[:4] != b"\x7fELF":
        return None
    ei_class = data[4]
    ei_data = data[5]
    if ei_class not in (1, 2) or ei_data not in (1, 2):
        return {"note": "invalid-elf-header"}
    endian = "<" if ei_data == 1 else ">"
    elf = {"class": "ELF32" if ei_class == 1 else "ELF64",
           "endian": "little" if ei_data == 1 else "big"}
    try:
        if ei_class == 1:
            (e_type, e_machine, _ver, e_entry, e_phoff, e_shoff, _flags,
             _ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx) = (
                struct.unpack_from(endian + "HHIIIIIHHHHHH", data, 16))
        else:
            (e_type, e_machine, _ver, e_entry, e_phoff, e_shoff, _flags,
             _ehsize, e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx) = (
                struct.unpack_from(endian + "HHIQQQIHHHHHH", data, 16))
    except struct.error:
        return {"note": "truncated-elf-header"}
    elf.update({
        "type": ELF_TYPES.get(e_type, "0x%04x" % e_type),
        "type_code": e_type,
        "machine": ELF_MACHINES.get(e_machine, "0x%04x" % e_machine),
        "machine_code": e_machine,
        "entry": e_entry,
        "phnum": e_phnum,
        "shnum": e_shnum,
        "rwx_segments": [],
        "segments": [],
        "sections": [],
    })
    # 程序头：找 RWX 段（p_flags = R|W|X = 7）
    if e_phoff and e_phnum and e_phentsize:
        for i in range(min(e_phnum, 128)):
            base = e_phoff + i * e_phentsize
            try:
                if ei_class == 1:
                    (p_type, p_flags, _off, _vaddr, _paddr, p_filesz, p_memsz, _align) = (
                        struct.unpack_from(endian + "IIIIIIII", data, base))
                else:
                    (p_type, p_flags, _off, _vaddr, _paddr, p_filesz, p_memsz, _align) = (
                        struct.unpack_from(endian + "IIQQQQQQ", data, base))
            except struct.error:
                break
            seg = {"type": p_type, "flags": p_flags, "filesz": p_filesz, "memsz": p_memsz}
            elf["segments"].append(seg)
            if p_type == 1 and p_flags == 7:  # PT_LOAD + RWX
                elf["rwx_segments"].append(seg)
    # 节头：RWX 节（SHF_WRITE|SHF_EXECINSTR）
    if e_shoff and e_shnum and e_shentsize:
        for i in range(min(e_shnum, 256)):
            base = e_shoff + i * e_shentsize
            try:
                if ei_class == 1:
                    (_name, s_type, s_flags, _addr, _off, s_size, _link, _info, _al, _es) = (
                        struct.unpack_from(endian + "IIIIIIIIII", data, base))
                else:
                    (_name, s_type, s_flags, _addr, _off, s_size, _link, _info, _al, _es) = (
                        struct.unpack_from(endian + "IIQQQQIIQQ", data, base))
            except struct.error:
                break
            if s_flags & 0x4 and s_flags & 0x1:  # EXECINSTR | WRITE
                elf["sections"].append({"flags": s_flags, "size": s_size})
    return elf


# ---------------------------------------------------------------------------
# 风险分级
# ---------------------------------------------------------------------------
def grade_risk(rec):
    """静态指标加权给出线索级风险。返回 (level, score, reasons)。"""
    reasons = []
    score = 0
    kind = rec["type"]["kind"]
    exe = kind in ("pe", "elf", "macho", "script")
    entropy = rec.get("entropy") or 0.0

    if entropy >= 7.5:
        score += 3
        reasons.append("整体熵 %.2f >= 7.5（疑似加密 / 压缩 / 加壳）" % entropy)
    elif entropy >= 6.5:
        score += 2
        reasons.append("整体熵 %.2f >= 6.5（偏高，常见于加密 / 压缩载荷）" % entropy)
    elif entropy >= 5.5:
        score += 1
        reasons.append("整体熵 %.2f >= 5.5" % entropy)

    pe = rec.get("pe") or {}
    if pe.get("suspicious_sections"):
        score += 3
        reasons.append("疑似加壳区段: %s" % ", ".join(pe["suspicious_sections"]))
    if pe.get("rwx_sections"):
        score += 2
        reasons.append("可写可执行区段: %s" % ", ".join(pe["rwx_sections"]))
    if pe.get("high_entropy_sections"):
        score += 1
        reasons.append("高熵区段: %s" % ", ".join(
            "%s(%.2f)" % (h["name"], h["entropy"]) for h in pe["high_entropy_sections"]))
    ts = pe.get("timestamp")
    if ts is not None:
        if ts == 0:
            reasons.append("PE 时间戳为 0（疑似人为抹除）")
        elif ts > 4102444800:  # 2100-01-01
            reasons.append("PE 时间戳异常（%s，疑似伪造）" % pe.get("timestamp_text", ""))
        elif ts < 631152000 and ts != 0:  # 1990-01-01 之前
            reasons.append("PE 时间戳异常偏旧（%s）" % pe.get("timestamp_text", ""))

    elf = rec.get("elf") or {}
    if elf.get("rwx_segments"):
        score += 3
        reasons.append("ELF 存在 RWE 段（%d 个，可疑）" % len(elf["rwx_segments"]))
    if elf.get("sections"):
        score += 2
        reasons.append("ELF 存在可写可执行节（%d 个）" % len(elf["sections"]))

    cls = rec["strings"]["classified"]
    n_url = len(cls["urls"])
    n_dom = len(cls["domains"])
    n_cmd = len(cls["commands"])
    n_b64 = len(cls["base64"])
    if n_cmd:
        score += 2 * min(n_cmd, 3)
        reasons.append("可疑命令关键字: %s" % ", ".join(cls["commands"]))
    if n_url and exe:
        score += 1
        reasons.append("可执行文件内嵌 URL（%d 条）" % n_url)
    elif n_url:
        reasons.append("内嵌 URL（%d 条，非可执行，仅提示）" % n_url)
    if n_dom and exe:
        reasons.append("可执行文件内嵌域名（%d 条）" % n_dom)
    if n_b64:
        score += 1
        reasons.append("长 base64 块（%d 条，疑似编码载荷）" % n_b64)
    if exe and not reasons:
        reasons.append("可执行文件，未发现明显静态风险线索")

    if score >= 7:
        level = "critical"
    elif score >= 5:
        level = "high"
    elif score >= 3:
        level = "medium"
    elif score >= 1:
        level = "low"
    else:
        level = "info"
    if not reasons:
        reasons.append("未发现静态风险线索")
    return level, score, reasons


# ---------------------------------------------------------------------------
# 单文件 triage
# ---------------------------------------------------------------------------
def triage_one(path, strings_min=ASCII_STRINGS_MIN, strings_limit=500,
               no_strings=False, max_file_mb=DEFAULT_MAX_FILE_MB):
    size = os.path.getsize(path)
    if size == 0:
        return {"path": path, "name": os.path.basename(path), "size": 0,
                "error": "empty-file"}
    if size > max_file_mb * 1024 * 1024:
        return {"path": path, "name": os.path.basename(path), "size": size,
                "error": "too-large"}
    hashes = file_hashes(path)
    with open(path, "rb") as f:
        data = f.read(MAX_ANALYZE_BYTES)
    analyzed_capped = size > len(data)
    kind, label, magic = detect_type(data)
    entropy = round(shannon_entropy(data), 3)

    strings_data = {
        "count": 0, "classified": {
            "urls": [], "domains": [], "ips": [], "emails": [],
            "commands": [], "paths": [], "base64": []},
        "suspicious": [], "skipped": bool(no_strings),
    }
    if not no_strings:
        strings = extract_strings(data, min_len=strings_min, max_strings=strings_limit)
        strings_data["count"] = len(strings)
        cls = classify_strings(strings)
        strings_data["classified"] = cls
        strings_data["suspicious"] = cls["commands"]

    rec = {
        "path": path,
        "name": os.path.basename(path),
        "size": size,
        "analyzed_bytes": len(data),
        "analyzed_capped": analyzed_capped,
        "hashes": hashes,
        "type": {"kind": kind, "label": label, "magic": magic},
        "entropy": entropy,
        "strings": strings_data,
        "pe": parse_pe(data) if kind == "pe" else None,
        "elf": parse_elf(data) if kind == "elf" else None,
        "risk": None,
    }
    level, score, reasons = grade_risk(rec)
    rec["risk"] = {"level": level, "score": score, "reasons": reasons}
    return rec


def iter_files(path, recursive=False):
    """遍历文件 / 目录，返回 (display_path, abspath)。"""
    if os.path.isfile(path):
        yield path, os.path.abspath(path)
        return
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            dirs.sort()
            for name in sorted(files):
                full = os.path.join(root, name)
                if os.path.isfile(full):
                    yield full, os.path.abspath(full)
            if not recursive:
                break
        return
    raise IOError("路径不存在或不可访问: %s" % path)


def build_iocs(records):
    """汇总 IOC（hash / url / domain / ipv4 / email）供元情消费。"""
    iocs = []
    seen = set()
    for rec in records:
        if rec.get("error"):
            continue
        name = rec["name"]
        for algo in ("md5", "sha1", "sha256"):
            iocs.append({"type": "hash", "value": rec["hashes"][algo],
                         "algo": algo, "file": name})
        for t, lst in (("url", "urls"), ("domain", "domains"),
                       ("ipv4", "ips"), ("email", "emails")):
            for v in rec["strings"]["classified"][lst]:
                key = (t, v.lower())
                if key in seen:
                    continue
                seen.add(key)
                iocs.append({"type": t, "value": v, "file": name})
    return iocs


# ---------------------------------------------------------------------------
# 输出
# ---------------------------------------------------------------------------
def build_report(records):
    max_risk = "info"
    order = {lvl: i for i, lvl in enumerate(RISK_LEVELS)}
    for rec in records:
        if rec.get("error"):
            continue
        lvl = rec["risk"]["level"]
        if order[lvl] > order[max_risk]:
            max_risk = lvl
    iocs = build_iocs(records)
    return {
        "tool": TOOL,
        "version": VERSION,
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "summary": {
            "files": len(records),
            "analyzed": sum(1 for r in records if not r.get("error")),
            "errors": [{"file": r["name"], "error": r["error"]}
                       for r in records if r.get("error")],
            "max_risk": max_risk,
            "ioc_count": len(iocs),
        },
        "files": records,
        "iocs": iocs,
    }


def _risk_flag(level):
    return {"critical": "**", "high": "!!", "medium": "::", "low": "..", "info": ".."}.get(level, "..")


def build_text(report):
    s = report["summary"]
    lines = []
    lines.append("=== 元鉴 yotta-triage 静态初筛报告 ===")
    lines.append("工具: %s v%s | 生成: %s" % (TOOL, VERSION, report["generated"]))
    lines.append("文件: %d（成功 %d）| 最高风险: %s | IOC: %d 条" % (
        s["files"], s["analyzed"], s["max_risk"], s["ioc_count"]))
    if s["errors"]:
        lines.append("跳过: %s" % "; ".join("%s(%s)" % (e["file"], e["error"]) for e in s["errors"]))
    lines.append("")
    for rec in report["files"]:
        if rec.get("error"):
            lines.append("** %s - 跳过（%s）" % (rec["name"], rec["error"]))
            lines.append("")
            continue
        r = rec["risk"]
        lines.append("%s %s  (%s, %d bytes)" % (_risk_flag(r["level"]), rec["name"],
                                                rec["type"]["label"], rec["size"]))
        lines.append("  MD5   : %s" % rec["hashes"]["md5"])
        lines.append("  SHA1  : %s" % rec["hashes"]["sha1"])
        lines.append("  SHA256: %s" % rec["hashes"]["sha256"])
        lines.append("  熵     : %.3f（%s）" % (rec["entropy"], "分析窗口" if rec["analyzed_capped"] else "全文"))
        if rec["pe"]:
            pe = rec["pe"]
            lines.append("  PE    : %s | %s | 时间戳 %s | 区段 %d" % (
                pe.get("optional_magic") or "?", pe.get("machine", "?"),
                pe.get("timestamp_text", "?"), pe.get("sections", 0)))
            for s in pe.get("sections_detail", []):
                ent = (" 熵 %.2f" % s["entropy"]) if s["entropy"] is not None else ""
                lines.append("    - %-9s %s%s" % (s["name"],
                                                  "RWX" if s["executable"] and s["writable"] else
                                                  ("R-X" if s["executable"] else "RW-"),
                                                  ent))
        if rec["elf"]:
            elf = rec["elf"]
            lines.append("  ELF   : %s %s | %s | 入口 0x%x | 段 %d 节 %d" % (
                elf.get("class", "?"), elf.get("machine", "?"), elf.get("type", "?"),
                elf.get("entry", 0), elf.get("phnum", 0), elf.get("shnum", 0)))
        cls = rec["strings"]["classified"]
        if rec["strings"].get("skipped"):
            lines.append("  字符串: 已跳过（--no-strings）")
        else:
            lines.append("  字符串: %d 条 | %d URL | %d 域 | %d IP | %d 邮箱 | %d 命令 | %d base64" % (
                rec["strings"]["count"], len(cls["urls"]), len(cls["domains"]),
                len(cls["ips"]), len(cls["emails"]), len(cls["commands"]), len(cls["base64"])))
        if cls["urls"]:
            for u in cls["urls"][:8]:
                lines.append("    URL  : %s" % u)
        if cls["commands"]:
            lines.append("    命令 : %s" % ", ".join(cls["commands"]))
        lines.append("  风险 : %s（评分 %d）" % (RISK_LABELS[r["level"]], r["score"]))
        for reason in r["reasons"]:
            lines.append("    - %s" % reason)
        lines.append("")
    if report["iocs"]:
        lines.append("IOC 汇总（%d 条，供元情消费）:" % len(report["iocs"]))
        for ioc in report["iocs"][:50]:
            lines.append("  %-6s %s  [%s]" % (ioc["type"], ioc["value"], ioc["file"]))
        if len(report["iocs"]) > 50:
            lines.append("  ...（共 %d 条）" % len(report["iocs"]))
    return "\n".join(lines)


def build_markdown(report):
    text = build_text(report)
    bt = chr(96)
    return bt * 3 + "\n" + text + "\n" + bt * 3


def emit(text, output):
    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        prog=TOOL,
        description="元鉴 yotta-triage - 零依赖恶意样本静态初筛引擎（%s v%s）" % (TOOL_CN, VERSION),
    )
    ap.add_argument("--version", action="store_true", help="显示版本并退出")
    sub = ap.add_subparsers(dest="command")

    p = sub.add_parser("triage", help="对文件 / 目录做静态初筛")
    p.add_argument("--path", metavar="PATH", required=True, help="文件或目录")
    p.add_argument("--recursive", action="store_true", help="目录递归扫描子目录")
    p.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    p.add_argument("--output", metavar="FILE", help="写入文件（默认打印到 stdout）")
    p.add_argument("--ioc-only", action="store_true", help="只输出 IOC JSON（供元情消费）")
    p.add_argument("--strings-min", type=int, default=ASCII_STRINGS_MIN,
                   help="字符串最小长度（默认 %d）" % ASCII_STRINGS_MIN)
    p.add_argument("--strings-limit", type=int, default=500, help="每文件字符串提取上限（默认 500）")
    p.add_argument("--no-strings", action="store_true", help="跳过字符串提取")
    p.add_argument("--max-file-mb", type=int, default=DEFAULT_MAX_FILE_MB,
                   help="超过该大小(MB)的文件跳过（默认 %d）" % DEFAULT_MAX_FILE_MB)

    args = ap.parse_args()

    if args.version:
        print("%s %s（%s）" % (TOOL, VERSION, TOOL_CN))
        return 0
    if not args.command:
        ap.print_help()
        return 4
    if args.command == "triage":
        if args.strings_min < 1:
            sys.stderr.write("--strings-min 必须 >= 1\n")
            return 4
        if args.strings_limit < 1:
            sys.stderr.write("--strings-limit 必须 >= 1\n")
            return 4
        if args.max_file_mb < 1:
            sys.stderr.write("--max-file-mb 必须 >= 1\n")
            return 4
        try:
            paths = list(iter_files(args.path, recursive=args.recursive))
        except IOError as e:
            sys.stderr.write("错误: %s\n" % e)
            return 4
        records = []
        errors = 0
        for _display, abspath in paths:
            try:
                rec = triage_one(abspath, strings_min=args.strings_min,
                                 strings_limit=args.strings_limit,
                                 no_strings=args.no_strings,
                                 max_file_mb=args.max_file_mb)
                if rec.get("error"):
                    errors += 1
                records.append(rec)
            except OSError as e:
                errors += 1
                records.append({
                    "path": abspath, "name": os.path.basename(abspath),
                    "size": 0, "error": "unreadable: %s" % e,
                })
        report = build_report(records)
        if args.ioc_only:
            out = json.dumps(report["iocs"], ensure_ascii=False, indent=2)
            emit(out, args.output)
        elif args.format == "json":
            out = json.dumps(report, ensure_ascii=False, indent=2)
            emit(out, args.output)
        elif args.format == "markdown":
            emit(build_markdown(report), args.output)
        else:
            emit(build_text(report), args.output)
        if not records:
            return 4
        if errors == len(records):
            return 4
        return RISK_EXIT.get(report["summary"]["max_risk"], 0)
    return 4


if __name__ == "__main__":
    sys.exit(main())
