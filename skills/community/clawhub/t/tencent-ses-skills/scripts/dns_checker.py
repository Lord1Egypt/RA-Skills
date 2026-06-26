#!/usr/bin/env python3
"""
邮件域名 DNS 诊断工具 (Email Domain DNS Checker)

功能：
  - SPF 记录查询、语法验证、lookup 次数统计、冲突检测
  - DKIM 记录查询与密钥验证
  - DMARC 记录查询与策略分析
  - MX 记录查询与验证
  - 全球 DNS 传播检测（通过 DoH）
  - 综合诊断报告

用法:
  python dns_checker.py <command> <domain> [args...]

命令:
  check-all <domain>                     综合诊断（SPF+DKIM+DMARC+MX）
  check-spf <domain>                     SPF 记录诊断
  check-dkim <domain> [selector]         DKIM 记录诊断（默认 selector: qcloud）
  check-dmarc <domain>                   DMARC 记录诊断
  check-mx <domain>                      MX 记录诊断
  check-propagation <domain> <type> [name]  DNS 传播检测
  diagnose <domain> [problem_hint]       根据问题描述自动诊断
"""

import base64
import json
import sys
import re
import urllib.request
import urllib.parse
import urllib.error
import ssl
import binascii

# ============================================================
# ESP SPF include 域名库
# ============================================================
ESP_SPF_INCLUDES = {
    "qcloudmail.com": "腾讯云 SES",
    "spf1.dm.aliyun.com": "阿里云邮件推送",
    "amazonses.com": "Amazon SES",
    "sendgrid.net": "SendGrid",
    "mailgun.org": "Mailgun",
    "mandrillapp.com": "Mandrill (Mailchimp)",
    "email-od.com": "Office 365",
    "spf.protection.outlook.com": "Microsoft 365",
    "_spf.google.com": "Google Workspace",
    "zoho.com": "Zoho Mail",
    "postmarkapp.com": "Postmark",
    "sparkpostmail.com": "SparkPost",
}

# ============================================================
# DNS over HTTPS (DoH) 查询
# ============================================================
DOH_SERVERS = {
    "Google": "https://dns.google/resolve",
    "Cloudflare": "https://cloudflare-dns.com/dns-query",
    "AliDNS(中国)": "https://dns.alidns.com/resolve",
    "DNSPod(中国)": "https://doh.pub/dns-query",
}

# DNS 记录类型映射
DNS_TYPE_MAP = {
    "A": 1, "AAAA": 28, "CNAME": 5, "MX": 15, "TXT": 16, "NS": 2, "SOA": 6,
}


def doh_query(domain, record_type="TXT", server_name=None, server_url=None):
    """通过 DNS over HTTPS 查询 DNS 记录"""
    if server_url is None:
        server_url = DOH_SERVERS.get(server_name, DOH_SERVERS["Google"])

    rtype_num = DNS_TYPE_MAP.get(record_type.upper(), 16)
    params = urllib.parse.urlencode({"name": domain, "type": rtype_num})
    url = f"{server_url}?{params}"

    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={
        "Accept": "application/dns-json",
        "User-Agent": "DNS-Checker/1.0",
    })

    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            answers = data.get("Answer", [])
            results = []
            for ans in answers:
                val = ans.get("data", "").strip('"')
                results.append({
                    "name": ans.get("name", ""),
                    "type": ans.get("type", 0),
                    "ttl": ans.get("TTL", 0),
                    "data": val,
                })
            return {"status": data.get("Status", -1), "answers": results}
    except urllib.error.URLError as e:
        return {"status": -1, "answers": [], "error": str(e)}
    except (json.JSONDecodeError, UnicodeDecodeError, OSError, ValueError) as e:
        return {"status": -1, "answers": [], "error": str(e)}


def query_dns(domain, record_type="TXT"):
    """查询 DNS 记录，自动回退多个 DoH 服务器"""
    for server_url in DOH_SERVERS.values():
        result = doh_query(domain, record_type, server_url=server_url)
        if result.get("error") is None:
            return [a["data"] for a in result.get("answers", [])]
    # 所有服务器都失败，返回空列表
    return []


# ============================================================
# CNAME 冲突检测
# ============================================================
def check_cname_conflict(domain, record_label=""):
    """检测指定域名是否存在 CNAME 记录，如果存在则与 TXT/MX 等记录冲突。

    根据 RFC1034 和 RFC2181，CNAME 记录具有最高优先级。
    当同一主机记录同时存在 CNAME 和其他类型记录（TXT/MX/A/AAAA 等）时，
    递归 DNS 会优先返回 CNAME 记录，导致其他记录无法被正常解析。
    腾讯云 SES 域名验证不支持 CNAME 模式，必须使用 TXT 记录。

    参考：https://cloud.tencent.com/document/product/302/38661

    Args:
        domain: 要检查的完整域名
        record_label: 记录用途标签（如 "SPF"、"DKIM"、"DMARC"、"MX"），用于提示信息

    Returns:
        dict: {"has_cname": bool, "cname_target": str or None}
    """
    cnames = query_dns(domain, "CNAME")
    if cnames:
        cname_target = cnames[0]
        print(f"\n  ❌ 检测到 CNAME 冲突！")
        print(f"  域名 {domain} 存在 CNAME 记录：")
        print(f"    CNAME → {cname_target}")
        print(f"")
        print(f"  ⚠️  根据 DNS 协议（RFC1034/RFC2181），CNAME 具有最高优先级，")
        print(f"  与 TXT、MX 等记录类型冲突。当同一主机记录同时存在 CNAME 和")
        print(f"  其他类型记录时，递归 DNS 会优先返回 CNAME，导致{record_label}等")
        print(f"  记录无法被正常解析，从而造成腾讯云 SES 域名验证失败。")
        print(f"")
        print(f"  🔧 解决方案：")
        print(f"  请在 DNS 管理后台删除 {domain} 的 CNAME 记录，")
        print(f"  然后添加正确的 TXT{'/MX' if record_label == 'MX' else ''} 记录。")
        print(f"  如果该 CNAME 记录用于 CDN 等服务，请考虑：")
        print(f"    1. 使用不同的子域名分别用于 CDN 和邮件发送")
        return {"has_cname": True, "cname_target": cname_target}

    return {"has_cname": False, "cname_target": None}


# ============================================================
# SPF 检查
# ============================================================
def parse_spf_record(spf_text):
    """解析 SPF 记录，提取各机制"""
    parts = spf_text.strip().split()
    mechanisms = []
    for part in parts:
        if part.lower() == "v=spf1":
            continue
        mechanisms.append(part)
    return mechanisms


def count_spf_lookups(domain, depth=0, visited=None):
    """递归统计 SPF DNS lookup 次数（include/a/mx/ptr/exists/redirect）"""
    if visited is None:
        visited = set()
    if domain in visited or depth > 10:
        return 0, []
    visited.add(domain)

    txts = query_dns(domain, "TXT")
    spf_records = [t for t in txts if t.startswith("v=spf1")]
    if not spf_records:
        return 0, []

    spf = spf_records[0]
    mechanisms = parse_spf_record(spf)
    lookup_count = 0
    details = []

    lookup_mechs = {"include", "a", "mx", "ptr", "exists", "redirect"}

    for mech in mechanisms:
        mech_lower = mech.lower()
        # 去掉前面的 +/-/~/? 限定符
        clean = re.sub(r'^[+\-~?]', '', mech_lower)

        # 单独处理 redirect= 机制（使用 = 分隔，不是 :）
        if clean.startswith("redirect="):
            lookup_count += 1
            sub_target = clean.split("=", 1)[1]
            details.append({"mechanism": mech, "target": sub_target, "depth": depth})
            sub_count, sub_details = count_spf_lookups(sub_target, depth + 1, visited)
            lookup_count += sub_count
            details.extend(sub_details)
            break

        for lm in lookup_mechs - {"redirect"}:
            if clean.startswith(lm + ":") or clean == lm:
                lookup_count += 1
                target = clean.split(":", 1)[1] if ":" in clean else domain
                details.append({"mechanism": mech, "target": target, "depth": depth})

                if clean.startswith("include:"):
                    sub_target = clean.split(":", 1)[1]
                    sub_count, sub_details = count_spf_lookups(sub_target, depth + 1, visited)
                    lookup_count += sub_count
                    details.extend(sub_details)
                break

    return lookup_count, details


def check_spf(domain):
    """SPF 记录完整诊断"""
    print(f"\n{'='*60}")
    print(f"  SPF 诊断报告 — {domain}")
    print(f"{'='*60}")

    # CNAME 冲突检测
    cname_result = check_cname_conflict(domain, "SPF(TXT)")
    if cname_result["has_cname"]:
        return {"status": "cname_conflict", "record": None, "cname_target": cname_result["cname_target"]}

    txts = query_dns(domain, "TXT")
    spf_records = [t for t in txts if t.startswith("v=spf1")]

    if not spf_records:
        print(f"\n  ❌ 未找到 SPF 记录")
        print(f"  建议: 添加 TXT 记录到 {domain}")
        print(f"  推荐值: v=spf1 include:qcloudmail.com ~all")
        return {"status": "missing", "record": None}

    if len(spf_records) > 1:
        print(f"\n  ⚠️  检测到 {len(spf_records)} 条 SPF 记录（应该只有 1 条）")
        print(f"  问题: 多条 SPF 记录会导致验证失败")
        print(f"  建议: 合并为一条 SPF 记录")
        for i, r in enumerate(spf_records):
            print(f"    [{i+1}] {r}")

    spf = spf_records[0]
    print(f"\n  当前 SPF 记录:")
    print(f"  {spf}")

    # 检查 all 策略
    mechanisms = parse_spf_record(spf)
    all_policy = None
    for m in mechanisms:
        # 严格匹配 all 机制：[+\-~?]?all，避免误匹配含 "all" 的其他字符串
        if re.fullmatch(r'[+\-~?]?all', m.lower()):
            all_policy = m
            break

    print(f"\n  ── 策略分析 ──")
    if all_policy:
        if all_policy == "-all":
            print(f"  ✅ all 策略: {all_policy} (严格 — 拒绝所有未授权发件源)")
        elif all_policy == "~all":
            print(f"  ✅ all 策略: {all_policy} (软拒绝 — 标记但不拒绝，推荐初期使用)")
        elif all_policy == "?all":
            print(f"  ⚠️  all 策略: {all_policy} (中性 — 不做任何处理，安全性较低)")
        elif all_policy == "+all":
            print(f"  ❌ all 策略: {all_policy} (允许所有 — 极不安全！)")
            print(f"  建议: 立即修改为 ~all 或 -all")
    else:
        print(f"  ⚠️  未检测到 all 机制，建议添加 ~all 或 -all")

    # 检查 ESP include
    print(f"\n  ── ESP 识别 ──")
    found_esp = False
    for m in mechanisms:
        clean = re.sub(r'^[+\-~?]', '', m.lower())
        if clean.startswith("include:"):
            inc_domain = clean.split(":", 1)[1]
            esp_name = ESP_SPF_INCLUDES.get(inc_domain, "未知 ESP")
            print(f"  📧 {inc_domain} → {esp_name}")
            found_esp = True
    if not found_esp:
        print(f"  (未检测到已知 ESP)")

    # 检查腾讯云 SES
    has_qcloud = any("qcloudmail.com" in m for m in mechanisms)
    if not has_qcloud:
        print(f"\n  ⚠️  未包含腾讯云 SES 的 SPF 记录")
        print(f"  建议: 在 SPF 记录中添加 include:qcloudmail.com")

    # 统计 lookup 次数
    print(f"\n  ── Lookup 统计 ──")
    lookup_count, lookup_details = count_spf_lookups(domain)
    status_icon = "✅" if lookup_count <= 10 else "❌"
    print(f"  {status_icon} DNS Lookup 次数: {lookup_count}/10")
    if lookup_count > 10:
        print(f"  ❌ 超过 10 次 lookup 限制！")
        print(f"  建议: 使用 SPF flattening（将 include 展开为 ip4/ip6）")
    if lookup_details:
        for d in lookup_details[:15]:
            indent = "    " + "  " * d["depth"]
            print(f"{indent}→ {d['mechanism']} (lookup #{d['depth']+1})")

    # 检查字符长度
    if len(spf) > 255:
        print(f"\n  ⚠️  SPF 记录长度 {len(spf)} 字符，超过 255 字符")
        print(f"  建议: 部分 DNS 提供商不支持超长 TXT 记录，可能需要拆分为多个字符串")

    overall = (
        "pass"
        if len(spf_records) == 1 and lookup_count <= 10 and has_qcloud and all_policy in ["-all", "~all"]
        else "warning"
    )
    return {"status": overall, "record": spf, "lookup_count": lookup_count}


# ============================================================
# DKIM 检查
# ============================================================
def check_dkim(domain, selector="qcloud"):
    """DKIM 记录诊断"""
    print(f"\n{'='*60}")
    print(f"  DKIM 诊断报告 — {domain} (selector: {selector})")
    print(f"{'='*60}")

    dkim_domain = f"{selector}._domainkey.{domain}"
    print(f"\n  查询: {dkim_domain}")

    # CNAME 冲突检测：腾讯云 SES 不支持 CNAME 模式验证 DKIM，
    # 必须使用 TXT 记录。如果存在 CNAME 记录会导致 TXT 无法被正常解析。
    cname_result = check_cname_conflict(dkim_domain, "DKIM(TXT)")
    if cname_result["has_cname"]:
        print(f"\n  ⚠️  补充说明：腾讯云 SES 的 DKIM 验证不支持 CNAME 模式，")
        print(f"  必须使用 TXT 记录直接配置 DKIM 公钥。")
        print(f"  即使 CNAME 指向的目标域名配置了正确的 DKIM TXT 记录，")
        print(f"  腾讯云 SES 也无法通过 CNAME 方式完成验证。")
        return {"status": "cname_conflict", "record": None, "cname_target": cname_result["cname_target"]}

    txts = query_dns(dkim_domain, "TXT")

    # 标准 DKIM 记录必须以 v=DKIM1 开头，避免 "k=rsa" 误匹配其他 TXT 记录
    dkim_records = [t for t in txts if re.search(r'v=dkim1', t, re.IGNORECASE)]

    if not dkim_records:
        # 检查是否所有 TXT 都不是 DKIM
        if txts:
            print(f"\n  ⚠️  找到 TXT 记录但不是有效的 DKIM 记录:")
            for t in txts:
                print(f"    {t[:100]}...")
        else:
            print(f"\n  ❌ 未找到 DKIM 记录")
        print(f"  建议: 在 DNS 中添加 TXT 记录，域名为 {dkim_domain}")
        print(f"  值从腾讯云 SES 控制台获取（创建域名时提供）")
        return {"status": "missing", "record": None}

    dkim = dkim_records[0]
    print(f"\n  当前 DKIM 记录:")
    print(f"  {dkim[:120]}{'...' if len(dkim) > 120 else ''}")

    # 检查 key 部分
    print(f"\n  ── 密钥分析 ──")
    p_match = re.search(r'p=([A-Za-z0-9+/=]+)', dkim)
    if p_match:
        key_b64 = p_match.group(1)
        if not key_b64 or key_b64 == "":
            print(f"  ❌ 空密钥（p=），通常表示密钥已撤销")
        else:
            try:
                key_bytes = base64.b64decode(key_b64, validate=True)
                key_bits = len(key_bytes) * 8
                print(f"  密钥长度: ~{key_bits} bits")
                if key_bits >= 1024:
                    print(f"  ⚠️  密钥长度 1024 bit（可用）")
                else:
                    print(f"  ❌ 密钥长度 < 1024 bit（不安全）")
            except (binascii.Error, ValueError):
                print(f"  ⚠️  无法解码密钥，可能格式不正确")
    else:
        print(f"  ❌ 未找到 p= 公钥参数")

    # 检查 k= 算法
    k_match = re.search(r'k=(\w+)', dkim)
    if k_match:
        algo = k_match.group(1)
        print(f"  签名算法: {algo}")
        if algo.lower() == "rsa":
            print(f"  ✅ RSA 算法（广泛支持）")
        elif algo.lower() == "ed25519":
            print(f"  ⚠️  Ed25519 算法（部分邮件服务商可能不支持）")

    return {"status": "found", "record": dkim}


# ============================================================
# DMARC 检查
# ============================================================
def check_dmarc(domain):
    """DMARC 记录诊断"""
    print(f"\n{'='*60}")
    print(f"  DMARC 诊断报告 — {domain}")
    print(f"{'='*60}")

    dmarc_domain = f"_dmarc.{domain}"

    # CNAME 冲突检测
    cname_result = check_cname_conflict(dmarc_domain, "DMARC(TXT)")
    if cname_result["has_cname"]:
        return {"status": "cname_conflict", "record": None, "cname_target": cname_result["cname_target"]}

    txts = query_dns(dmarc_domain, "TXT")
    dmarc_records = [t for t in txts if t.lower().startswith("v=dmarc1")]

    if not dmarc_records:
        print(f"\n  ❌ 未找到 DMARC 记录")
        print(f"  建议: 添加 TXT 记录到 {dmarc_domain}")
        print(f"  推荐初始值: v=DMARC1; p=none; rua=mailto:dmarc@{domain}")
        return {"status": "missing", "record": None}

    if len(dmarc_records) > 1:
        print(f"\n  ⚠️  检测到 {len(dmarc_records)} 条 DMARC 记录（应该只有 1 条）")

    dmarc = dmarc_records[0]
    print(f"\n  当前 DMARC 记录:")
    print(f"  {dmarc}")

    # 解析各标签
    tags = {}
    for part in dmarc.split(";"):
        part = part.strip()
        if "=" in part:
            k, v = part.split("=", 1)
            tags[k.strip().lower()] = v.strip()

    print(f"\n  ── 策略分析 ──")

    # p= 策略
    policy = tags.get("p", "none")
    if policy == "reject":
        print(f"  ✅ 策略: p=reject (严格 — 拒绝不合规邮件)")
    elif policy == "quarantine":
        print(f"  ✅ 策略: p=quarantine (隔离 — 标记为垃圾邮件)")
    elif policy == "none":
        print(f"  ⚠️  策略: p=none (监控模式 — 不执行任何操作)")
        print(f"  建议渐进升级路径:")
        print(f"    1. p=none (当前) → 收集报告，确认合法发件源")
        print(f"    2. p=quarantine    → 隔离不合规邮件到垃圾箱")
        print(f"    3. p=reject        → 完全拒绝不合规邮件")

    # sp= 子域名策略
    sp = tags.get("sp")
    if sp:
        print(f"  子域名策略: sp={sp}")
    else:
        print(f"  子域名策略: (继承主策略 p={policy})")

    # pct= 百分比
    pct = tags.get("pct", "100")
    print(f"  应用比例: pct={pct}%")
    if pct != "100":
        print(f"  ⚠️  仅对 {pct}% 的邮件应用策略，建议逐步提升到 100%")

    # rua= 聚合报告
    rua = tags.get("rua")
    if rua:
        print(f"  ✅ 聚合报告: rua={rua}")
    else:
        print(f"  ⚠️  未配置聚合报告地址 (rua)")
        print(f"  建议: 添加 rua=mailto:dmarc-reports@{domain}")

    # ruf= 法务报告
    ruf = tags.get("ruf")
    if ruf:
        print(f"  ✅ 失败报告: ruf={ruf}")
    else:
        print(f"  ℹ️  未配置失败报告地址 (ruf)，可选配置")

    # adkim / aspf 对齐模式
    adkim = tags.get("adkim", "r")
    aspf = tags.get("aspf", "r")
    print(f"\n  ── 对齐模式 ──")
    print(f"  DKIM 对齐: adkim={'strict' if adkim == 's' else 'relaxed'} ({adkim})")
    print(f"  SPF 对齐:  aspf={'strict' if aspf == 's' else 'relaxed'} ({aspf})")

    return {"status": "found", "record": dmarc, "policy": policy, "tags": tags}


# ============================================================
# MX 检查
# ============================================================
def check_mx(domain):
    """MX 记录诊断"""
    print(f"\n{'='*60}")
    print(f"  MX 诊断报告 — {domain}")
    print(f"{'='*60}")

    # CNAME 冲突检测
    cname_result = check_cname_conflict(domain, "MX")
    if cname_result["has_cname"]:
        return {"status": "cname_conflict", "records": [], "cname_target": cname_result["cname_target"]}

    result = doh_query(domain, "MX", server_name="Google")
    mx_records = result.get("answers", [])

    if not mx_records:
        print(f"\n  ⚠️  未找到 MX 记录")
        print(f"  注意: MX 记录对于腾讯云 SES 发信不是必需的")
        print(f"  但如果需要在该域名上接收邮件，则必须配置 MX")
        return {"status": "missing", "records": []}

    print(f"\n  共 {len(mx_records)} 条 MX 记录:")
    print(f"  {'优先级':<8} {'邮件服务器':<40} {'TTL':<8}")
    print(f"  {'-'*56}")

    parsed = []
    for mx in mx_records:
        data = mx.get("data", "")
        parts = data.split()
        if len(parts) >= 2:
            priority = parts[0]
            server = parts[1]
            parsed.append({"priority": priority, "server": server, "ttl": mx.get("ttl", 0)})
            print(f"  {priority:<8} {server:<40} {mx.get('ttl', 'N/A'):<8}")

    # 检查常见 ESP 的 MX
    known_mx = {
        "mxbiz1.qq.com": "腾讯企业邮箱",
        "mxbiz2.qq.com": "腾讯企业邮箱(备)",
        "mx01.dm.aliyun.com": "阿里云邮件推送",
        "mx.google.com": "Google Workspace",
        "aspmx.l.google.com": "Google Workspace",
        "protection.outlook.com": "Microsoft 365",
    }

    print(f"\n  ── MX 指向分析 ──")
    for p in parsed:
        srv_lower = p["server"].lower().rstrip(".")
        matched = False
        for mx_key, mx_name in known_mx.items():
            if mx_key in srv_lower:
                print(f"  📧 {p['server']} → {mx_name}")
                matched = True
                break
        if not matched:
            print(f"  📧 {p['server']} → 未知邮件服务")

    return {"status": "found", "records": parsed}


# ============================================================
# DNS 传播检测
# ============================================================
def check_propagation(domain, record_type="TXT", record_name=None):
    """全球 DNS 传播检测"""
    if record_name:
        # 使用精确的域名后缀匹配，避免 endswith 误判（如 record_name="myexample.com", domain="example.com"）
        if record_name == domain or record_name.endswith("." + domain):
            full_domain = record_name
        else:
            full_domain = f"{record_name}.{domain}"
    else:
        full_domain = domain

    print(f"\n{'='*60}")
    print(f"  DNS 传播状态报告 — {full_domain}")
    print(f"  记录类型: {record_type.upper()}")
    print(f"{'='*60}")

    # 检测 CNAME 冲突（静默模式，仅在有冲突时提示）
    cnames = query_dns(full_domain, "CNAME")
    if cnames:
        print(f"\n  ❌ 警告：检测到 {full_domain} 存在 CNAME 记录！")
        print(f"     CNAME → {cnames[0]}")
        print(f"     CNAME 与 {record_type.upper()} 记录冲突，可能导致验证失败。")
        print(f"     请先删除该 CNAME 记录。")

    results = []
    total = 0
    success = 0

    for name, url in DOH_SERVERS.items():
        total += 1
        result = doh_query(full_domain, record_type, server_url=url)
        answers = result.get("answers", [])
        error = result.get("error")

        if error:
            status = "⚠️ 错误"
            value = error[:50]
        elif answers:
            status = "✅ 已生效"
            # 取第一条相关记录
            values = [a["data"] for a in answers]
            value = values[0][:60] + ("..." if len(values[0]) > 60 else "")
            if len(values) > 1:
                value += f" (+{len(values)-1}条)"
            success += 1
        else:
            status = "❌ 未生效"
            value = "(无记录)"

        results.append({"server": name, "status": status, "value": value})

    print(f"\n  {'DNS 节点':<18} {'状态':<10} {'返回值'}")
    print(f"  {'-'*70}")
    for r in results:
        print(f"  {r['server']:<18} {r['status']:<10} {r['value']}")

    print(f"\n  {'─'*70}")
    if success == total:
        print(f"  ✅ 结论: {success}/{total} 节点已生效，DNS 已全局传播。")
    elif success > 0:
        print(f"  ⚠️  结论: {success}/{total} 节点已生效，部分区域尚未传播。")
        print(f"  建议: 等待 4-8 小时后再次检测，或检查 DNS 提供商的 TTL 设置。")
    else:
        print(f"  ❌ 结论: 0/{total} 节点生效，DNS 记录可能尚未配置或传播。")
        print(f"  建议: 检查 DNS 配置是否正确，确认已保存更改。")

    return {"total": total, "success": success, "results": results}


# ============================================================
# 综合诊断
# ============================================================
def check_all(domain):
    """综合 DNS 诊断"""
    print(f"\n{'#'*60}")
    print(f"  邮件域名综合诊断 — {domain}")
    print(f"{'#'*60}")

    spf_result = check_spf(domain)
    dkim_result = check_dkim(domain)
    dmarc_result = check_dmarc(domain)
    mx_result = check_mx(domain)

    # 汇总
    print(f"\n{'='*60}")
    print(f"  综合诊断结论 — {domain}")
    print(f"{'='*60}")

    items = [
        ("SPF", spf_result["status"] not in ["missing", "cname_conflict"], spf_result["status"]),
        ("DKIM", dkim_result["status"] not in ["missing", "cname_conflict"], dkim_result["status"]),
        ("DMARC", dmarc_result["status"] not in ["missing", "cname_conflict"], dmarc_result["status"]),
        ("MX", mx_result["status"] not in ["missing", "cname_conflict"], mx_result["status"]),
    ]

    for name, exists, status in items:
        if status == "cname_conflict":
            icon = "❌"
            desc = "CNAME 冲突"
        elif not exists:
            icon = "❌"
            desc = "未配置"
        elif status in ["pass", "found"]:
            icon = "✅"
            desc = "正常"
        else:
            icon = "⚠️ "
            desc = "需关注"
        print(f"  {icon} {name:<8} {desc}")

    # 检查是否有 CNAME 冲突
    cname_conflicts = [name for name, _, status in items if status == "cname_conflict"]
    if cname_conflicts:
        print(f"\n  ❌ 以下记录存在 CNAME 冲突: {', '.join(cname_conflicts)}")
        print(f"  CNAME 记录具有最高优先级（RFC1034/RFC2181），会导致同一主机记录")
        print(f"  下的 TXT/MX 等记录无法被正常解析，腾讯云 SES 验证将失败。")
        print(f"  请先删除相关 CNAME 记录，再配置正确的 TXT/MX 记录。")
        print(f"  参考文档：https://cloud.tencent.com/document/product/302/38661")

    all_ok = all(e for _, e, _ in items)
    if all_ok:
        print(f"\n  🎉 所有 DNS 记录已配置！请确认腾讯云 SES 验证是否通过。")
    else:
        missing = [name for name, exists, status in items if not exists and status != "cname_conflict"]
        if missing:
            print(f"\n  ⚠️  以下记录需要配置: {', '.join(missing)}")
            print(f"  请在 DNS 服务商后台添加对应的记录后重新验证。")

    return {
        "spf": spf_result,
        "dkim": dkim_result,
        "dmarc": dmarc_result,
        "mx": mx_result,
    }


# ============================================================
# 自动诊断
# ============================================================
def diagnose(domain, problem_hint=""):
    """根据问题描述自动诊断"""
    hint_lower = problem_hint.lower() if problem_hint else ""

    print(f"\n{'#'*60}")
    print(f"  自动诊断 — {domain}")
    if problem_hint:
        print(f"  问题描述: {problem_hint}")
    print(f"{'#'*60}")

    # 根据问题描述决定检查项
    if "spf" in hint_lower:
        check_spf(domain)
        print(f"\n  ── SPF 传播检测 ──")
        check_propagation(domain, "TXT")
    elif "dkim" in hint_lower:
        check_dkim(domain)
        print(f"\n  ── DKIM 传播检测 ──")
        check_propagation(domain, "TXT", f"qcloud._domainkey")
    elif "dmarc" in hint_lower:
        check_dmarc(domain)
        print(f"\n  ── DMARC 传播检测 ──")
        check_propagation(domain, "TXT", f"_dmarc")
    elif "mx" in hint_lower:
        check_mx(domain)
    elif "传播" in hint_lower or "propagation" in hint_lower:
        check_propagation(domain, "TXT")
        check_propagation(domain, "TXT", f"qcloud._domainkey")
        check_propagation(domain, "TXT", f"_dmarc")
        check_propagation(domain, "MX")
    else:
        # 全量检查
        check_all(domain)
        # 额外做传播检测
        print(f"\n{'='*60}")
        print(f"  全球 DNS 传播检测")
        print(f"{'='*60}")
        check_propagation(domain, "TXT")
        check_propagation(domain, "TXT", f"qcloud._domainkey")
        check_propagation(domain, "TXT", f"_dmarc")


# ============================================================
# 生成建议的 DNS 记录
# ============================================================
def generate_dns_guide(domain, ses_attributes=None):
    """根据腾讯云 SES 返回的 Attributes 和当前 DNS 状态，生成配置指导"""
    print(f"\n{'#'*60}")
    print(f"  域名邮件认证配置指南 — {domain}")
    print(f"{'#'*60}")

    if ses_attributes:
        print(f"\n  ── 腾讯云 SES 要求的 DNS 记录 ──")
        print(f"  {'类型':<6} {'记录名':<45} {'值'}")
        print(f"  {'-'*100}")
        for attr in ses_attributes:
            status = "✅" if attr.get("Status") else "❌"
            record_type = attr.get("Type", "N/A")
            send_domain = attr.get("SendDomain", "N/A")
            expected_value = attr.get("ExpectedValue", "N/A")[:80]
            print(f"  {status} {record_type:<5} {send_domain:<44} {expected_value}")
            if not attr.get("Status"):
                current = attr.get("CurrentValue", "")
                if current:
                    print(f"         {'当前值:':<44} {current[:80]}")
                else:
                    print(f"         {'当前值:':<44} (未配置)")

    # 通用指导
    print(f"\n  ── 通用配置步骤 ──")
    print(f"""
  ⚠️  重要提醒：CNAME 记录冲突检查
  配置 DNS 记录前，请确认发信域名及其子域名（如 qcloud._domainkey、_dmarc 等）
  不存在 CNAME 记录。根据 DNS 协议（RFC1034/RFC2181），CNAME 具有最高优先级，
  会与 TXT、MX 等记录冲突，导致腾讯云 SES 验证失败。
  如果存在 CNAME 记录，请先删除后再添加 TXT/MX 记录。
  参考文档：https://cloud.tencent.com/document/product/302/38661

  1. 登录您的 DNS 管理后台（如阿里云 DNS、Cloudflare、DNSPod 等）

  2. 添加/修改以下 DNS 记录：

     📌 SPF 记录（TXT）
     记录名: {domain}
     类型:   TXT
     值:     v=spf1 include:qcloudmail.com ~all
     说明:   如已有 SPF 记录，请在 ~all 前追加 include:qcloudmail.com

     📌 DKIM 记录（TXT）
     记录名: qcloud._domainkey.{domain}
     类型:   TXT（不支持 CNAME 模式，必须使用 TXT 记录）
     值:     (从腾讯云 SES 控制台获取)

     📌 DMARC 记录（TXT）
     记录名: _dmarc.{domain}
     类型:   TXT
     值:     v=DMARC1; p=none; rua=mailto:dmarc@{domain}

     📌 MX 记录（可选，用于接收退信）
     记录名: {domain}
     类型:   MX
     优先级: 10
     值:     mxbiz1.qq.com

  3. 保存后等待 DNS 传播（通常 5 分钟 ~ 48 小时）

  4. 使用以下命令检测传播状态：
     python3 dns_checker.py check-propagation {domain} TXT

  5. 确认传播后，在腾讯云 SES 控制台请求验证
""")

    return True


# ============================================================
# 主入口
# ============================================================
def print_usage():
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    cmd = sys.argv[1]

    try:
        if cmd == "check-all":
            if len(sys.argv) < 3:
                print("用法: dns_checker.py check-all <domain>")
                sys.exit(1)
            check_all(sys.argv[2])

        elif cmd == "check-spf":
            if len(sys.argv) < 3:
                print("用法: dns_checker.py check-spf <domain>")
                sys.exit(1)
            check_spf(sys.argv[2])

        elif cmd == "check-dkim":
            if len(sys.argv) < 3:
                print("用法: dns_checker.py check-dkim <domain> [selector]")
                sys.exit(1)
            selector = sys.argv[3] if len(sys.argv) > 3 else "qcloud"
            check_dkim(sys.argv[2], selector)

        elif cmd == "check-dmarc":
            if len(sys.argv) < 3:
                print("用法: dns_checker.py check-dmarc <domain>")
                sys.exit(1)
            check_dmarc(sys.argv[2])

        elif cmd == "check-mx":
            if len(sys.argv) < 3:
                print("用法: dns_checker.py check-mx <domain>")
                sys.exit(1)
            check_mx(sys.argv[2])

        elif cmd == "check-propagation":
            if len(sys.argv) < 4:
                print("用法: dns_checker.py check-propagation <domain> <type> [name]")
                sys.exit(1)
            name = sys.argv[4] if len(sys.argv) > 4 else None
            check_propagation(sys.argv[2], sys.argv[3], name)

        elif cmd == "diagnose":
            if len(sys.argv) < 3:
                print("用法: dns_checker.py diagnose <domain> [problem_hint]")
                sys.exit(1)
            hint = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
            diagnose(sys.argv[2], hint)

        elif cmd == "guide":
            if len(sys.argv) < 3:
                print("用法: dns_checker.py guide <domain> [ses_attributes_json]")
                sys.exit(1)
            attrs = None
            if len(sys.argv) > 3:
                try:
                    attrs = json.loads(sys.argv[3])
                except json.JSONDecodeError:
                    pass
            generate_dns_guide(sys.argv[2], attrs)

        else:
            print(f"未知命令: {cmd}")
            print_usage()
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n操作已取消。")
        sys.exit(130)
    except (OSError, ValueError, UnicodeError) as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
