#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
yotta-intel（元情）—— 零依赖自研威胁情报 IOC 提取与规范化引擎
================================================================

跨智能体的威胁情报 IOC 提取能力：从威胁情报文本 / 安全报告 / 钓鱼邮件 / 日志中
提取 IP（IPv4/IPv6）、域名、URL、邮箱、哈希（MD5/SHA1/SHA256/SHA512）与 CVE 编号，
自动识别 defang（去活性）写法并还原，去重、归一化后输出 CSV / JSON / STIX-lite。

特性
----
- 七类 IOC 提取：ipv4 / ipv6 / domain / url / email / hash / cve
- defang / refang：识别常见去活性写法（hxxp、[.]、(.)、[dot]、[:]、[@] 等）并还原；
  输出时给出安全的 defang 形态，便于在邮件 / 文档 / 工单中共享
- 归一化：域名小写 + IDN punycode、URL 去默认端口、哈希小写、IPv6 压缩写法
- 去重计数：同一 IOC 只保留一条，记录出现次数与首次出现的行号 / 上下文
- 三种结构化输出：CSV / JSON / STIX-lite（STIX 2.1 Bundle + indicator pattern）
- 纯本地离线处理：不联网查证、不下载样本、不主动扫描任何系统（红线）

用法
----
  python3 scripts/yotta_intel.py extract --path report.txt
  python3 scripts/yotta_intel.py extract --stdin --format json
  python3 scripts/yotta_intel.py extract --path intel.md --types ipv4,domain,hash --min-count 2
  python3 scripts/yotta_intel.py extract --path intel.md --format stix --output iocs.json
  python3 scripts/yotta_intel.py defang --path report.txt --output safe.txt
  python3 scripts/yotta_intel.py refang --path safe.txt --output raw.txt
  python3 scripts/yotta_intel.py --version

退出码：extract 0 = 无 IOC；1 = 发现 IOC；4 = 用法或读取错误。
defang / refang：0 = 成功；4 = 用法或读取错误。
Windows 下用 python 代替 python3。
"""

import argparse
import csv
import io
import ipaddress
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from urllib.parse import urlsplit

try:
    sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VERSION = "0.2.4"
TOOL = "yotta-intel"
TOOL_CN = "元情"

# 七类 IOC：顺序即文本 / CSV / JSON 输出的分组顺序
IOC_TYPES = ("ipv4", "ipv6", "domain", "url", "email", "hash", "cve")
IOC_LABELS = {
    "ipv4": "IPv4 地址",
    "ipv6": "IPv6 地址",
    "domain": "域名",
    "url": "URL",
    "email": "邮箱",
    "hash": "哈希",
    "cve": "CVE 编号",
}

# 哈希长度 -> 算法名
HASH_ALGO = {32: "MD5", 40: "SHA1", 64: "SHA256", 128: "SHA512"}
HASH_STIX = {"MD5": "MD5", "SHA1": "SHA-1", "SHA256": "SHA-256", "SHA512": "SHA-512"}

# 常见 gTLD 与主流新 gTLD（域名判定的白名单；不在列表内的多段名不当作域名）
GTLD = frozenset("""
com net org edu gov mil int info biz name pro museum coop aero asia cat jobs mobi
post tel travel xxx app dev io ai xyz top vip shop cloud click link site online
tech store live digital network systems security software tools wiki media news
blog press agency consulting solutions services company center care club community
cool design directory download email expert express fail finance fit fun gift guru
host institute international kim life limited lol management marketing moe monster
partners party photo pics pink plus rent reviews rocks sale science social studio
support team technology today trading training university vision voting win works
world zone art auto baby bank bar beauty bio buzz cab camera capital casino chat
city coffee college crypto date eco energy engineering events exchange faith
family fashion film fitness food football forex forum fun games glass gold golf
green group health help home hospital hotel house immo inc insure jet kaufen kids
kitchen lawyer lease legal life lighting llc loan love ltd luxury makeup market
media memorial men moda money movie music news ninja page park party pet plumbing
plus poker porn press pro productions promo properties racing realty repair report
rest restaurant review rich rip rocks run sale salon save school search services
sex shoes shop show singles site ski soccer social software solar solutions soy
space sport storage stream studio style supplies supply support surgery systems
tax taxi team tech tel tenis theater tickets tienda tips tires today tools town
toys trade training travel tube university uno vacation vegas ventures video villas
vision vodka vote voting voyage watch webcam website wedding wiki wine work wtf yoga
""".split())

# 全部 ISO 3166-1 ccTLD
CCTLD = frozenset("""
ac ad ae af ag ai al am ao aq ar as at au aw ax az ba bb bd be bf bg bh bi bj bl bm
bn bo bq br bs bt bv bw by bz ca cc cd cf cg ch ci ck cl cm cn co cr cu cv cw cx cy
cz de dj dk dm do dz ec ee eg eh er es et eu fi fj fk fm fo fr ga gb gd ge gf gg gh
gi gl gm gn gp gq gr gs gt gu gw gy hk hm hn hr ht hu id ie il im in io iq ir is it
je jm jo jp ke kg kh ki km kn kp kr kw ky kz la lb lc li lk lr ls lt lu lv ly ma mc
md me mf mg mh mk ml mm mn mo mp mq mr ms mt mu mv mw mx my mz na nc ne nf ng ni nl
no np nr nu nz om pa pe pf pg ph pk pl pm pn pr ps pt pw py qa re ro rs ru rw sa sb
sc sd se sg sh si sj sk sl sm sn so sr ss st su sv sx sy sz tc td tf tg th tj tk tl
tm tn to tr tt tv tw tz ua ug uk us uy uz va vc ve vg vi vn vu wf ws ye yt za zm zw
""".split())

TLD_SET = GTLD | CCTLD

# 与常见文件扩展名重叠的 TLD：二段域名命中这些时判为文件名而非域名（如 README.md、test.py）
FILE_EXT_TLDS = frozenset("""
md py sh js ts json txt log xml html css png jpg jpeg gif webp svg pdf doc docx xls
xlsx pptx ppt csv zip rar 7z tar gz tgz bz2 xz exe dll so dylib apk deb rpm iso bin
bat cmd ps1 vbs tmp bak old swp lock env gitignore pyc class jar war o a lib ini cfg
conf yml yaml key pem crt pfx cer db sqlite db3 mdb accdb mp3 mp4 avi mov mkv wav
flac map img dmg
""".split())

# ---------------------------------------------------------------------------
# defang / refang
# ---------------------------------------------------------------------------
# defang（去活性）是威胁情报共享的常见做法：把 IOC 中可被自动识别的分隔符替换成
# 「安全」写法，避免收件人 / 平台把纯文本误识别为可点击链接或可解析地址。
# 本引擎识别常见 defang 写法，先还原成规范形态（refang），再输出统一的 defang 形态。


def refang_text(text):
    """把文本中的常见 defang 写法还原为原始形态（行数保持不变）。"""
    t = text
    t = re.sub(r"(?i)\[\.\]|\(\.\)|\{\.\}|\[dot\]|\(dot\)|\{dot\}", ".", t)
    t = re.sub(r"(?i)\[:\]|\(:\)|\{:\}|\[colon\]|\(colon\)|\{colon\}", ":", t)
    t = re.sub(r"(?i)\[@\]|\(@\)|\{@\}|\[at\]|\(at\)|\{at\}", "@", t)
    t = re.sub(r"\[/\]|\(/\)|\[\\/\]|\[/\\\]", "/", t)
    t = re.sub(r"\[\\\]", lambda m: "\\", t)
    t = re.sub(r"(?i)\bhxxps", "https", t)
    t = re.sub(r"(?i)\bhxxp", "http", t)
    return t


def defang_value(value, ioc_type):
    """把规范化后的 IOC 转为统一的 defang 形态（用于安全共享展示）。"""
    if ioc_type == "ipv4":
        return value.replace(".", "[.]")
    if ioc_type == "ipv6":
        return value.replace(":", "[:]")
    if ioc_type == "domain":
        return value.replace(".", "[.]")
    if ioc_type == "url":
        if value.lower().startswith("https://"):
            scheme = "hxxps"
            rest = value[8:]
        elif value.lower().startswith("http://"):
            scheme = "hxxp"
            rest = value[7:]
        elif value.lower().startswith("ftp://"):
            scheme = "fxp"
            rest = value[6:]
        else:
            scheme, _, rest = value.partition("://")
        host, sep, tail = rest.partition("/")
        host = host.replace(".", "[.]").replace("@", "[@]")
        return scheme + "://" + host + sep + tail
    if ioc_type == "email":
        return value.replace("@", "[@]").replace(".", "[.]")
    # hash / cve 本身不会被自动链接或解析，保持原样即可
    return value


def prune_overlaps(matches):
    """在 (start, end, type, value) 列表中保留互不重叠的最长覆盖（供 defang 流式替换用）。"""
    ms = sorted(matches, key=lambda m: (m[0], -m[1]))
    keep = []
    for m in ms:
        if keep and m[0] < keep[-1][1]:
            continue
        keep.append(m)
    return keep

# ---------------------------------------------------------------------------
# IOC 提取（在 refang 后的文本上工作；refang 只替换分隔符，不改变行结构）
# ---------------------------------------------------------------------------
URL_RE = re.compile(r"(?i)(?:(?:https?|ftp)://)[^\s<>\"'，。！？；：、（）【】《》“”‘’]+")
EMAIL_RE = re.compile(r"(?i)[a-z0-9._%+\-]+@[a-z0-9\-]+(?:\.[a-z0-9\-]+)+")
DOMAIN_RE = re.compile(r"(?<![\w@.])(?:[\w\-]{1,63}\.)+[\w\-]{2,63}(?![\-\w])")
IPV4_RE = re.compile(r"(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)")


def normalize_ipv4_octets(raw):
    """把前导零写法（010.000.000.001）归一为 10.0.0.1。

    Python 3.9.5 起 ipaddress.IPv4Address 拒绝前导零八位组，旧版本接受；
    这里先做十进制归一，保证跨版本行为一致（999.1.1.1 仍会被判非法）。
    """
    parts = raw.split(".")
    if len(parts) != 4:
        return raw
    out = []
    for part in parts:
        if not part.isdigit() or len(part) > 3:
            return raw
        out.append(str(int(part)))
    return ".".join(out)


def canonical_ipv6(ip6):
    """Return one stable IPv6 spelling across Python patch versions."""
    mapped = ip6.ipv4_mapped
    if mapped is not None:
        value = int(mapped)
        return "::ffff:%x:%x" % ((value >> 16) & 0xFFFF, value & 0xFFFF)
    return ip6.compressed


IPV6_TOKEN_RE = re.compile(r"(?i)(?<![\w:])(?:[0-9a-f:.]{2,45})(?![\w:])")
HASH_RE = re.compile(r"(?i)(?<![0-9a-f])[0-9a-f]{32,128}(?![0-9a-f])")
CVE_RE = re.compile(r"(?i)\bcve-\d{4}-\d{4,7}\b")


def valid_domain(dom):
    """域名判定：TLD 白名单 + 标签结构 + 文件名误报过滤。"""
    d = dom.lower().rstrip(".")
    if not d or len(d) > 253 or d.count(".") < 1:
        return False
    labels = d.split(".")
    if len(labels) < 2:
        return False
    tld = labels[-1]
    if not tld.startswith("xn--") and tld not in TLD_SET:
        return False
    # 二段名 + 常见文件扩展名 -> 判为文件名（如 README.md、test.py），不算域名
    if len(labels) == 2 and tld in FILE_EXT_TLDS:
        return False
    for lab in labels:
        if len(lab) > 63 or not re.match(r"^[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?$", lab):
            return False
    return True


def norm_domain(value):
    """域名归一：小写、去尾点、IDN -> punycode。"""
    d = value.lower().strip().rstrip(".")
    if not d or d.count(".") < 1:
        return None
    try:
        d = d.encode("idna").decode("ascii").lower()
    except (UnicodeError, ValueError):
        return None
    return d


def norm_url(value):
    """URL 归一：scheme/host 小写、IDN host、去默认端口、去 fragment。"""
    try:
        parts = urlsplit(value)
        port = parts.port
    except ValueError:
        return None
    scheme = parts.scheme.lower()
    if scheme not in ("http", "https", "ftp"):
        return None
    host = parts.hostname
    if not host:
        return None
    try:
        host = host.encode("idna").decode("ascii").lower()
    except (UnicodeError, ValueError):
        return None
    is_ipv6 = False
    try:
        ipaddress.ip_address(host)
        is_ipv6 = ":" in host
    except ValueError:
        if not valid_domain(host):
            return None
    if port is not None:
        if (scheme == "http" and port == 80) or (scheme == "https" and port == 443) or (scheme == "ftp" and port == 21):
            port = None
        if port is not None:
            host = "%s:%d" % (host, port)
    if is_ipv6 and not host.startswith("["):
        host = "[" + host + "]"
    userinfo = ""
    if parts.username:
        ui = parts.username
        if parts.password is not None:
            ui += ":" + parts.password
        userinfo = ui + "@"
    path = parts.path or ""
    query = ("?" + parts.query) if parts.query else ""
    return "%s://%s%s%s%s" % (scheme, userinfo, host, path, query)


def norm_email(value):
    """邮箱归一：小写 + 域名段 IDN。"""
    v = value.strip().lower()
    if "@" not in v:
        return None
    user, _, dom = v.partition("@")
    if not user or not dom:
        return None
    nd = norm_domain(dom)
    if not nd or not valid_domain(nd):
        return None
    return user + "@" + nd


def find_iocs_in_line(line):
    """在一行（已 refang）中找出所有 IOC，返回 (start, end, type, canonical)。"""
    found = []
    for m in IPV4_RE.finditer(line):
        raw = m.group(0)
        try:
            ip = ipaddress.IPv4Address(normalize_ipv4_octets(raw))
        except ValueError:
            continue
        found.append((m.start(), m.end(), "ipv4", str(ip)))
    for m in IPV6_TOKEN_RE.finditer(line):
        tok = m.group(0)
        if ":" not in tok:
            continue
        for cand in (tok.rstrip("."), tok):
            try:
                ip6 = ipaddress.IPv6Address(cand)
            except ValueError:
                continue
            found.append((m.start(), m.start() + len(cand), "ipv6", canonical_ipv6(ip6)))
            break
    for m in DOMAIN_RE.finditer(line):
        d = norm_domain(m.group(0))
        if d and valid_domain(d):
            found.append((m.start(), m.end(), "domain", d))
    for m in EMAIL_RE.finditer(line):
        e = norm_email(m.group(0))
        if e:
            found.append((m.start(), m.end(), "email", e))
    for m in URL_RE.finditer(line):
        raw = m.group(0).rstrip(".,;:!?\"')]")
        u = norm_url(raw)
        if u:
            found.append((m.start(), m.end(), "url", u))
    for m in HASH_RE.finditer(line):
        h = m.group(0).lower()
        if len(h) in HASH_ALGO:
            found.append((m.start(), m.end(), "hash", h))
    for m in CVE_RE.finditer(line):
        found.append((m.start(), m.end(), "cve", m.group(0).upper()))
    return found


def extract_iocs(text, types=None, min_count=1):
    """在文本上提取 IOC：refang -> 逐行提取 -> 归一 -> 去重计数。

    返回记录列表，每条约含：type / value / defanged / count / first_line / snippet。
    """
    rtext = refang_text(text)
    rlines = rtext.split("\n")
    orig_lines = text.split("\n")
    want = set(types) if types else set(IOC_TYPES)
    buckets = {}
    for idx, line in enumerate(rlines, start=1):
        for start, end, ioc_type, canonical in find_iocs_in_line(line):
            if ioc_type not in want:
                continue
            rec = buckets.setdefault(ioc_type, {})
            entry = rec.get(canonical)
            if entry is None:
                snippet = ""
                if 0 < idx <= len(orig_lines):
                    snippet = orig_lines[idx - 1].strip()
                entry = {
                    "type": ioc_type,
                    "value": canonical,
                    "defanged": defang_value(canonical, ioc_type),
                    "count": 0,
                    "first_line": idx,
                    "snippet": snippet,
                }
                rec[canonical] = entry
            entry["count"] += 1
    records = []
    for ioc_type in IOC_TYPES:
        if ioc_type not in want:
            continue
        items = buckets.get(ioc_type, {})
        for entry in sorted(items.values(), key=lambda r: (-r["count"], r["value"])):
            if entry["count"] >= min_count:
                records.append(entry)
    return records


def defang_line(line):
    """把一行文本中识别到的 IOC 替换为 defang 形态（其余原样保留）。"""
    rline = refang_text(line)
    matches = prune_overlaps(find_iocs_in_line(rline))
    if not matches:
        return line
    buf = list(rline)
    for start, end, ioc_type, canonical in sorted(matches, key=lambda m: -m[0]):
        d = defang_value(canonical, ioc_type)
        buf[start:end] = list(d)
    return "".join(buf)


def defang_text(text):
    """流式 defang：逐行处理，行结构不变。"""
    return "".join(defang_line(line) for line in text.splitlines(keepends=True))

# ---------------------------------------------------------------------------
# 输出：文本 / JSON / CSV / STIX-lite
# ---------------------------------------------------------------------------
def stix_pattern(ioc_type, value):
    """STIX 2.1 indicator pattern（确定性生成）。"""
    if ioc_type == "ipv4":
        return "[ipv4-addr:value = '%s']" % value
    if ioc_type == "ipv6":
        return "[ipv6-addr:value = '%s']" % value
    if ioc_type == "domain":
        return "[domain-name:value = '%s']" % value
    if ioc_type == "url":
        return "[url:value = '%s']" % value
    if ioc_type == "email":
        return "[email-addr:value = '%s']" % value
    if ioc_type == "hash":
        algo = HASH_ALGO[len(value)]
        return "[file:hashes.'%s' = '%s']" % (HASH_STIX[algo], value)
    if ioc_type == "cve":
        return "[vulnerability:name = '%s']" % value
    return "[x-yottameta:value = '%s']" % value


def build_stix(records, generated):
    """把记录打包成 STIX 2.1 Bundle（lite：只含 indicator 对象 + 自定义扩展属性）。"""
    objects = []
    for r in records:
        oid = uuid.uuid5(uuid.NAMESPACE_URL, "yotta-intel:" + r["type"] + ":" + r["value"])
        objects.append({
            "type": "indicator",
            "spec_version": "2.1",
            "id": "indicator--" + str(oid),
            "created": generated,
            "modified": generated,
            "name": IOC_LABELS[r["type"]] + ": " + r["value"],
            "pattern": stix_pattern(r["type"], r["value"]),
            "pattern_type": "stix",
            "valid_from": generated,
            "labels": ["malicious-activity"],
            "x_yottameta_type": r["type"],
            "x_yottameta_value": r["value"],
            "x_yottameta_defanged": r["defanged"],
            "x_yottameta_count": r["count"],
        })
    return {
        "type": "bundle",
        "id": "bundle--" + str(uuid.uuid5(uuid.NAMESPACE_URL, "yotta-intel:" + generated)),
        "spec_version": "2.1",
        "objects": objects,
    }


def build_json(records, generated, source):
    by_type = {}
    for r in records:
        by_type[r["type"]] = by_type.get(r["type"], 0) + 1
    return json.dumps({
        "tool": TOOL,
        "tool_cn": TOOL_CN,
        "version": VERSION,
        "generated": generated,
        "source": source,
        "summary": {"total": len(records), "by_type": by_type},
        "indicators": records,
    }, ensure_ascii=False, indent=2)


def build_csv(records):
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["type", "value", "defanged", "count", "first_line", "snippet"])
    for r in records:
        w.writerow([r["type"], r["value"], r["defanged"], r["count"], r["first_line"], r["snippet"]])
    return out.getvalue()


def build_text(records, context=120):
    lines = ["元情 %s v%s —— IOC 提取结果" % (TOOL, VERSION)]
    if not records:
        lines.append("未发现 IOC。")
        return "\n".join(lines)
    lines.append("共发现 %d 个 IOC：\n" % len(records))
    cur = None
    for r in records:
        if r["type"] != cur:
            cur = r["type"]
            lines.append("■ %s（%s）" % (IOC_LABELS[cur], cur))
        lines.append("  %s  ×%d  行 %d" % (r["value"], r["count"], r["first_line"]))
        lines.append("    defang: %s" % r["defanged"])
        sn = r["snippet"]
        if len(sn) > context:
            sn = sn[:context] + "…"
        lines.append("    上下文: %s" % sn)
        lines.append("")
    return "\n".join(lines)


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
def read_input(args):
    if getattr(args, "stdin", False):
        return sys.stdin.read(), "<stdin>"
    path = getattr(args, "path", None)
    if path:
        if not os.path.isfile(path):
            raise IOError("文件不存在或不是普通文件: %s" % path)
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(), os.path.basename(path)
    raise IOError("必须提供 --path 或 --stdin")


def main():
    ap = argparse.ArgumentParser(
        prog=TOOL,
        description="元情 yotta-intel —— 零依赖威胁情报 IOC 提取与规范化引擎（%s v%s）" % (TOOL_CN, VERSION),
    )
    ap.add_argument("--version", action="store_true", help="显示版本并退出")
    sub = ap.add_subparsers(dest="command")

    p_extract = sub.add_parser("extract", help="提取 IOC 并输出结构化结果（text/json/csv/stix）")
    p_extract.add_argument("--path", metavar="FILE", help="输入文件")
    p_extract.add_argument("--stdin", action="store_true", help="从标准输入读取")
    p_extract.add_argument("--types", default=",".join(IOC_TYPES),
                           help="要提取的 IOC 类型（逗号分隔），默认全部")
    p_extract.add_argument("--format", choices=["text", "json", "csv", "stix"], default="text")
    p_extract.add_argument("--output", metavar="FILE", help="写入文件（默认打印到 stdout）")
    p_extract.add_argument("--min-count", type=int, default=1, help="只保留出现次数 >= N 的 IOC")
    p_extract.add_argument("--context", type=int, default=120, help="文本输出上下文截断宽度")

    p_defang = sub.add_parser("defang", help="把文本中识别到的 IOC 替换为安全 defang 形态")
    p_defang.add_argument("--path", metavar="FILE")
    p_defang.add_argument("--stdin", action="store_true")
    p_defang.add_argument("--output", metavar="FILE")

    p_refang = sub.add_parser("refang", help="把 defang 文本还原为原始形态")
    p_refang.add_argument("--path", metavar="FILE")
    p_refang.add_argument("--stdin", action="store_true")
    p_refang.add_argument("--output", metavar="FILE")

    args = ap.parse_args()

    if args.version:
        print("%s %s（%s）" % (TOOL, VERSION, TOOL_CN))
        return 0
    if not args.command:
        ap.print_help()
        return 4

    try:
        if args.command == "extract":
            data, source = read_input(args)
            types = [t.strip().lower() for t in args.types.split(",") if t.strip()]
            unknown = [t for t in types if t not in IOC_TYPES]
            if unknown:
                sys.stderr.write("未知 IOC 类型: %s（可选: %s）\n" % (",".join(unknown), ",".join(IOC_TYPES)))
                return 4
            if args.min_count < 1:
                sys.stderr.write("--min-count 必须 >= 1\n")
                return 4
            records = extract_iocs(data, types=types, min_count=args.min_count)
            generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
            if args.format == "json":
                out = build_json(records, generated, source)
            elif args.format == "csv":
                out = build_csv(records)
            elif args.format == "stix":
                out = json.dumps(build_stix(records, generated), ensure_ascii=False, indent=2)
            else:
                out = build_text(records, context=args.context)
            emit(out, args.output)
            return 1 if records else 0
        if args.command == "defang":
            data, _source = read_input(args)
            emit(defang_text(data), args.output)
            return 0
        if args.command == "refang":
            data, _source = read_input(args)
            emit(refang_text(data), args.output)
            return 0
    except IOError as e:
        sys.stderr.write("错误: %s\n" % e)
        return 4
    except KeyboardInterrupt:
        return 130
    return 4


if __name__ == "__main__":
    sys.exit(main())
