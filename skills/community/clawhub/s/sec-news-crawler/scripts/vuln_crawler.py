#!/usr/bin/env python3
"""
漏洞情报爬虫 v2 - 从 NVD + cxsecurity + 安全客 抓取最新漏洞信息
每天一篇漏洞集合笔记存入 IMA「Openclaw生成」笔记本
支持英文内容智能翻译为中文，保留 CVE ID、组件名、技术术语不翻译
"""

import json, os, sys, time, re, ssl, gzip
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
import http.client
import hashlib
import random

# ── 配置 ──────────────────────────────────────────────────────────────────

IMA_CLIENT_ID  = os.environ.get("IMA_OPENAPI_CLIENTID", "")
IMA_API_KEY    = os.environ.get("IMA_OPENAPI_APIKEY", "")
IMA_BASE_URL   = "https://ima.qq.com/openapi/note/v1"
DEFAULT_FOLDER = "foldered9d1a12b2143ffb"  # 漏洞情报

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
DATA_DIR    = os.path.join(SCRIPT_DIR, "..", "data")
VULN_SEEN   = os.path.join(DATA_DIR, "vuln_seen.json")
LAST_RUN    = os.path.join(DATA_DIR, "vuln_last_run.json")
LOG_FILE    = os.path.join(os.path.dirname(SCRIPT_DIR), "..", "..", "logs", "vuln_cron.log")

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# ── 翻译配置（MiniMax API）─────────────────────────────────────────────────
# 优先从环境变量读取，未设置则尝试从 openclaw.json 读取
MINIMAX_API_KEY = os.environ.get("MINIMAX_API_KEY", "")
if not MINIMAX_API_KEY:
    _cfg = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "openclaw.json")
    try:
        with open(_cfg, "r") as f:
            _j = json.load(f)
        raw_key = _j.get("models", {}).get("providers", {}).get("minimax", {}).get("apiKey", "")
        if raw_key and raw_key != "__OPENCLAW_REDACTED__":
            MINIMAX_API_KEY = raw_key
    except Exception:
        pass
MINIMAX_BASE_URL = "https://api.minimaxi.com/anthropic"

# 不应翻译的专业术语（保持英文原样）
TECH_TERMS = {
    # 漏洞类型/攻击手法
    "RCE", "Remote Code Execution", "LFI", "RFI", "SSRF", "SQLi", "XSS", "XXE",
    "CSRF", "IDOR", "Buffer Overflow", "Heap Overflow", "Stack Overflow",
    "Race Condition", "Use After Free", "Double Free", "Format String",
    "Path Traversal", "Command Injection", "Code Injection", "Deserialization",
    "Privilege Escalation", "Authentication Bypass", "Authorization Bypass",
    "Information Disclosure", "Denial of Service", "DoS", "DDoS",
    "Man-in-the-Middle", "MITM", "ARP Spoofing", "DNS Spoofing",
    "Session Hijacking", "Clickjacking", "UI Redressing",
    "WebShell", "Backdoor", "Trojan", "Rootkit", "Keylogger",
    "Brute Force", "Dictionary Attack", "Rainbow Table",
    "Zero-day", "Zero Day", "N-day", "Exploit", "Payload", "Shellcode",
    "Memory Corruption", "Type Confusion", "Integer Overflow",
    "CSV Injection", "XML Injection", "LDAP Injection", "XPATH Injection",
    "HTTP Response Splitting", "HTTP Request Smuggling",
    # 安全协议/框架
    "TLS", "SSL", "HTTPS", "SSH", "SFTP", "FTPS",
    "OAuth", "OpenID", "SAML", "JWT",
    "PKI", "CA", "Certificate", "Root Certificate",
    "WAF", "IDS", "IPS", "SIEM", "SOC", "EDR",
    "DMZ", "VPC", "VPN", "Zero Trust", "Micro-segmentation",
    # 漏洞类型/概念
    "CVE", "CVSS", "CPE", "CWE", "OWASP",
    "NVD", "CNVD", "CNNVD", "EDB", "OSV",
    # 数据库/中间件组件
    "MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch",
    "Apache", "Nginx", "Tomcat", "JBoss", "WebLogic", "WebSphere",
    "Spring", "Struts", "Django", "Flask", "Rails", "Laravel",
    "jQuery", "React", "Vue", "Angular", "Node.js", "Express",
    "WordPress", "Drupal", "Joomla",
    "Docker", "Kubernetes", "K8s", "Helm",
    # 操作系统
    "Windows", "Linux", "macOS", "Android", "iOS",
    "Ubuntu", "Debian", "CentOS", "RHEL", "Fedora", "Kali",
    "Active Directory", "AD DS", "SMB", "SAMBA",
    # 网络协议
    "TCP", "UDP", "HTTP", "HTTPS", "FTP", "DNS", "DHCP",
    "SMTP", "IMAP", "POP3", "LDAP", "NTP", "SNMP",
    "REST", "GraphQL", "SOAP", "gRPC", "WebSocket",
    # 加密/哈希
    "AES", "RSA", "ECC", "SHA", "MD5", "HMAC", "PBKDF2", "BCrypt",
    # 权限/认证
    "RBAC", "ABAC", "DAC", "MAC", "UAC", "SELinux",
    "Sudo", "su", "chmod", "chown",
    # 工具/平台
    "Metasploit", "Burp Suite", "OWASP ZAP", "Nmap", "Wireshark",
    "Censys", "Nuclei", "Dirbuster",
    # 其他常用术语
    "API", "SDK", "CLI", "GUI", "UI", "UX",
    "IoT", "ICS", "SCADA", "PLC", "HMI",
    "IPv4", "IPv6", "MAC Address", "VLAN", "VXLAN",
    "APT", "TTP", "IOC", "IOA", "STIX", "TAXII",
    "MFA", "2FA", "OTP", "TOTP", "HOTP",
    "Sandbox", "Sandboxing", "Jail", "Chroot",
    "Proxy", "Reverse Proxy", "Load Balancer", "CDN",
    "Firewall", "iptables", "nftables", "pfSense",
    "Kernel", "Userland", "Ring 0", "Ring 3",
    "Heap", "Stack", "Memory", "Register", "Buffer",
    "DLL", "SO", "ELF", "PE", "Mach-O",
    "Firmware", "UEFI", "BIOS", "Bootloader",
    "Container", "Virtual Machine", "VM", "Hypervisor",
    "Backup", "Snapshot", "Replication", "Failover",
    "Patch", "Hotfix", "Update", "Upgrade",
    "Source Code", "Binary", "Bytecode", "Obfuscation",
    "Fuzzing", "Penetration Testing", "Red Team", "Blue Team",
    "Purple Team", "Threat Hunting", "Incident Response",
    "Malware", "Virus", "Worm", "Trojan Horse", "Ransomware",
    "Spyware", "Adware", "Botnet", "Zombie",
    "Phishing", "Spear Phishing", "Whaling", "Vishing", "Smishing",
    "Social Engineering", "Pretexting", "Baiting", "Tailgating",
    "MITRE", "ATT&CK", "Cyber Kill Chain",
}

def translate_to_chinese(text, fallback_text=""):
    """
    将英文漏洞描述翻译为中文。
    规则：
    - CVE ID（如 CVE-2024-1234）保留不翻译
    - CPE 组件名（如 cpe:/a:apache:http_server）保留不翻译
    - 技术术语（见 TECH_TERMS）保留不翻译
    - 其他内容翻译为中文
    """
    if not text or not text.strip():
        return fallback_text or text
    
    # 如果文本大部分是中文（含有大量 CJK 字符），不翻译
    cjk_count = len(re.findall(r'[\u4e00-\u9fff]', text))
    if cjk_count > len(text) * 0.3:
        return text

    # 提取 CVE ID 并保护
    cve_ids = re.findall(r'CVE-\d{4}-\d+', text, re.IGNORECASE)
    cve_placeholders = {}
    for i, cve in enumerate(cve_ids):
        ph = f"__CVE_{i}__"
        cve_placeholders[ph] = cve
        text = text.replace(cve, ph)

    # 提取 CPE 字符串并保护
    cpe_patterns = re.findall(r'cpe:?/[^;\s]+', text, re.IGNORECASE)
    cpe_placeholders = {}
    for i, cpe in enumerate(cpe_patterns):
        ph = f"__CPE_{i}__"
        cpe_placeholders[ph] = cpe
        text = text.replace(cpe, ph)

    # 提取 URLs 并保护
    urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', text)
    url_placeholders = {}
    for i, url in enumerate(urls):
        ph = f"__URL_{i}__"
        url_placeholders[ph] = url
        text = text.replace(url, ph)

    # 替换技术术语为占位符
    term_placeholders = {}
    sorted_terms = sorted(TECH_TERMS, key=len, reverse=True)  # 长词优先
    for term in sorted_terms:
        if term in text:
            ph = f"__TERM_{len(term_placeholders)}__"
            term_placeholders[ph] = term
            text = text.replace(term, ph)

    # 调用 MiniMax API 翻译
    translated = _call_minimax_translate(text)
    
    if translated and translated != text:
        result = translated
    else:
        # 翻译失败，返回原文
        result = text

    # 还原 CPE
    for ph, cpe in cpe_placeholders.items():
        result = result.replace(ph, f"[{cpe}]")
    
    # 还原 URLs
    for ph, url in url_placeholders.items():
        result = result.replace(ph, url)

    # 还原技术术语
    for ph, term in term_placeholders.items():
        result = result.replace(ph, term)

    # 还原 CVE ID
    for ph, cve in cve_placeholders.items():
        result = result.replace(ph, f"**{cve}**")

    return result

def _call_minimax_translate(text):
    """调用 MiniMax API（Anthropic 兼容接口）进行文本翻译
    使用 MiniMax-M2.1（无 thinking），更快更稳。
    """
    if not MINIMAX_API_KEY:
        return ""  # 无 API Key 时返回空，让调用方使用原文

    model = "MiniMax-M2.1"
    max_retries = 2

    for attempt in range(max_retries):
        try:
            import http.client

            conn = http.client.HTTPSConnection("api.minimaxi.com", timeout=20)

            payload = json.dumps({
                "model": model,
                "max_tokens": 300,
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Translate to Chinese. Rules:\n"
                            "1. Keep CVE IDs in English (CVE-YYYY-NNNNN)\n"
                            "2. Keep component names in English (apache, nginx, mysql, etc.)\n"
                            "3. Keep technical terms in English (RCE, SSRF, XSS, SQL Injection, zero-day, etc.)\n"
                            "4. Translate rest to fluent Chinese.\n"
                            "5. Output ONLY the translated text, no notes or explanations.\n\n"
                            f"Text: {text}"
                        ),
                    }
                ],
            }).encode("utf-8")

            headers = {
                "Content-Type": "application/json",
                "x-api-key": MINIMAX_API_KEY,
                "anthropic-version": "2023-06-01",
            }

            conn.request("POST", "/anthropic/v1/messages", body=payload, headers=headers)
            resp = conn.getresponse()
            raw = resp.read().decode("utf-8")
            conn.close()

            if resp.status == 200:
                data = json.loads(raw)
                text_result = ""
                for block in data.get("content", []):
                    if block.get("type") == "text":
                        text_result = block.get("text", "").strip()
                        break

                if not text_result:
                    log(f"  [WARN] MiniMax 响应无 text block，重试({attempt+1})")
                    continue

                # 检测是否是 thinking 内容（包含 "The user wants", "Rules:", "Translate" 等关键词）
                thinking_indicators = ["The user wants me to translate", "Rules:", "Translate the following",
                                       "Looking at the text:", "I need to identify", "So there are"]
                is_thinking = any(text_result[:40].startswith(ind) or ind in text_result[:100]
                                   for ind in thinking_indicators)

                if is_thinking and attempt < max_retries - 1:
                    log(f"  [WARN] MiniMax 返回 thinking 内容，重试({attempt+1})")
                    time.sleep(1)
                    continue

                return text_result

            log(f"  [WARN] MiniMax 翻译失败({resp.status}): {raw[:150]}")
            return ""

        except Exception as e:
            log(f"  [WARN] MiniMax 翻译异常(attempt {attempt+1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
            continue

    return ""

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ── 工具函数 ───────────────────────────────────────────────────────────────

def load_json(path, default=None):
    if default is None:
        default = {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def http_get(url, timeout=15, verify_ssl=True):
    headers = {"User-Agent": "Mozilla/5.0 (compatible; VulnBot/2.0)"}
    ctx = ssl.create_default_context()
    if not verify_ssl:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    try:
        req = Request(url, headers=headers)
        resp = urlopen(req, timeout=timeout, context=ctx)
        raw = resp.read()
        if url.endswith(".gz"):
            raw = gzip.decompress(raw)
        return raw.decode("utf-8", errors="replace")
    except Exception as e:
        log(f"  [WARN] 获取失败 {url}: {e}")
        return ""

# ── NVD JSON API v2 ─────────────────────────────────────────────────────────

def fetch_nvd(day_count=7):
    """
    每天单独查 NVD API v2，拼出近 day_count 天所有漏洞。
    NVD API 对日期范围查询有边界 bug，每天单独查能绕过。
    """
    all_vulns = []
    today_utc = datetime.now(timezone.utc)

    for i in range(day_count):
        # 查当天 UTC 00:00 到 23:59
        day_start = (today_utc - timedelta(days=i)).strftime("%Y-%m-%dT00:00:00.000")
        day_end   = (today_utc - timedelta(days=i)).strftime("%Y-%m-%dT23:59:59.999")

        params = urlencode({
            "resultsPerPage": 200,
            "pubStartDate":   day_start,
            "pubEndDate":     day_end,
        })
        url = f"https://services.nvd.nist.gov/rest/json/cves/2.0/?{params}"

        raw = http_get(url, timeout=20)
        if not raw:
            continue

        try:
            d = json.loads(raw)
        except json.JSONDecodeError:
            continue

        day_vulns = 0
        for v in d.get("vulnerabilities", []):
            cve = v.get("cve", {})
            cve_id = cve.get("id", "")

            descriptions = cve.get("descriptions", [])
            description = ""
            for desc in descriptions:
                if desc.get("lang") == "en":
                    description = desc.get("value", "")
                    break
            if not description:
                description = descriptions[0].get("value", "") if descriptions else ""

            severity = "未知"
            score = ""
            cvss = cve.get("metrics", {})
            for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
                if cvss.get(key):
                    severity = cvss[key][0].get("cvssData", {}).get("baseSeverity", "未知")
                    score = str(cvss[key][0].get("cvssData", {}).get("baseScore", ""))
                    break

            cpe_list = []
            for config in cve.get("configurations", []):
                for node in config.get("nodes", []):
                    for cpe in node.get("cpeMatch", []):
                        cpe_list.append(cpe.get("criteria", ""))

            published = cve.get("published", "")[:10]
            references = cve.get("references", [])[:2]
            ref_urls = [r.get("url", "") for r in references]

            all_vulns.append({
                "id":          cve_id,
                "date":        published,
                "severity":    severity,
                "score":       score,
                "description": description[:300],
                "cpe":         "；".join(cpe_list[:2]),
                "refs":        ref_urls,
                "source":      "NVD",
            })
            day_vulns += 1

        log(f"  NVD {day_start[:10]}: {day_vulns} 条")
        time.sleep(0.5)  # 避免请求过快

    return all_vulns

# ── cxsecurity RSS ─────────────────────────────────────────────────────────

def fetch_cxsecurity():
    raw = http_get("https://cxsecurity.com/rss/wl", verify_ssl=False)
    if not raw:
        return []
    try:
        import feedparser
        fp = feedparser.parse(raw)
        vulns = []
        for e in fp.entries:
            title = re.sub(r"<[^>]+>", "", e.get("title", ""))
            link = e.get("link", "")
            m = re.search(r"(CVE-\d+-\d+)", title)
            cve_id = m.group(1) if m else ""
            sm = re.search(r"CVSS:\s*([\d.]+)", title)
            score = sm.group(1) if sm else ""
            severity = ""
            if score:
                try:
                    f = float(score)
                    severity = "CRITICAL" if f >= 9.0 else "HIGH" if f >= 7.0 else "MEDIUM" if f >= 4.0 else "LOW"
                except ValueError:
                    pass
            pub = ""
            for t in ("published_parsed", "updated_parsed"):
                tp = getattr(e, t, None)
                if tp:
                    pub = time.strftime("%Y-%m-%d", tp)
                    break
            if cve_id:
                vulns.append({
                    "id": cve_id, "date": pub, "severity": severity,
                    "score": score, "description": title[:300],
                    "cpe": "", "refs": [link], "source": "cxsecurity",
                })
        return vulns
    except Exception as e:
        log(f"  [WARN] cxsecurity 解析失败: {e}")
        return []

# ── 安全客 RSS ─────────────────────────────────────────────────────────────

def fetch_anquanke():
    """安全客是国内为数不多仍然可用的安全资讯 RSS"""
    raw = http_get("https://api.anquanke.com/feed", verify_ssl=False)
    if not raw:
        return []
    try:
        import feedparser
        fp = feedparser.parse(raw)
        vulns = []
        for e in fp.entries:
            title = re.sub(r"<[^>]+>", "", e.get("title", ""))
            link = e.get("link", "")
            pub = ""
            for t in ("published_parsed", "updated_parsed"):
                tp = getattr(e, t, None)
                if tp:
                    pub = time.strftime("%Y-%m-%d", tp)
                    break
            # 安全客的文章中可能包含 CVE ID
            cve_ids = re.findall(r"(CVE-\d{4}-\d+)", title + " " + e.get("summary", ""))
            for cve_id in cve_ids[:1]:  # 只取第一个
                vulns.append({
                    "id": cve_id, "date": pub, "severity": "未知",
                    "score": "", "description": title[:300],
                    "cpe": "", "refs": [link], "source": "anquanke",
                })
                break
        return vulns
    except Exception as e:
        log(f"  [WARN] anquanke 解析失败: {e}")
        return []

# ── IMA API ────────────────────────────────────────────────────────────────

def ima_headers():
    return {
        "ima-openapi-clientid": IMA_CLIENT_ID,
        "ima-openapi-apikey":   IMA_API_KEY,
        "Content-Type":         "application/json",
    }

def ima_post(endpoint, payload):
    data = json.dumps(payload).encode("utf-8")
    req  = Request(f"{IMA_BASE_URL}/{endpoint}", data=data,
                   headers=ima_headers(), method="POST")
    try:
        with urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        log(f"  [ERROR] IMA {endpoint}: {e}")
        return {"code": -1, "msg": str(e)}

def import_doc(content, title, folder_id):
    result = ima_post("import_doc", {
        "content":        content,
        "content_format": 1,
        "title":          title,
        "folder_id":      folder_id,
    })
    doc_id = result.get("data", {}).get("doc_id", result.get("doc_id", ""))
    if result.get("code") != 0:
        log(f"  [WARN] import_doc 失败({result.get('code')}): {result.get('msg')}")
    return doc_id

# ── 渲染笔记 ──────────────────────────────────────────────────────────────

def badge(s):
    return {"CRITICAL": "🔴 CRITICAL", "HIGH": "🟠 HIGH", "MEDIUM": "🟡 MEDIUM",
            "LOW": "🟢 LOW", "未知": "⚪ 未知"}.get(s, "⚪ " + s)

def render_note(vulns, date_str):
    groups = {}
    for v in vulns:
        groups.setdefault(v["severity"], []).append(v)

    lines = [
        f"# 🔐 漏洞情报 {date_str}",
        f"",
        f"> 自动抓取 · 更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} · 共 {len(vulns)} 条漏洞",
        f"> 英文描述已智能翻译为中文，CVE/组件名/技术术语保留英文",
        "",
        "## 📊 概览",
        "",
    ]
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "未知"]:
        if sev in groups:
            lines.append(f"- {badge(sev)}：{len(groups[sev])} 条")

    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "未知"]:
        if sev not in groups:
            continue
        lines += ["", f"### {badge(sev)} 漏洞（{len(groups[sev])} 条）", ""]
        for v in groups[sev]:
            score_str = f'CVSS {v["score"]}' if v["score"] else ""
            lines.append(f"**{v['id']}** {badge(v['severity'])} {score_str}")
            if v["description"]:
                # 调用翻译函数，将英文描述翻译为中文
                translated_desc = translate_to_chinese(v["description"])
                lines.append(f"  {translated_desc[:300]}")
            if v["refs"] and v["refs"][0]:
                lines.append(f"  📎 {v['refs'][0]}")
            if v["cpe"]:
                lines.append(f"  🔧 受影响：CPE {v['cpe'][:80]}")
            lines.append("")

    lines += ["---", "", f"*数据来源：NVD · cxsecurity · 安全客 | {datetime.now().strftime('%Y-%m-%d %H:%M')}*"]
    return "\n".join(lines)

# ── 主逻辑 ─────────────────────────────────────────────────────────────────

def run():
    if not IMA_CLIENT_ID or not IMA_API_KEY:
        log("[ERROR] 缺少 IMA 凭证")
        sys.exit(1)

    log("开始抓取漏洞情报...")

    seen_db = load_json(VULN_SEEN, {})
    today_local = datetime.now().strftime("%Y-%m-%d")

    # 近7天的 UTC 和本地日期都要算（因为 NVD 用 UTC）
    allowed_dates = set()
    for i in range(7):
        d_utc   = (datetime.now(timezone.utc) - timedelta(days=i)).strftime("%Y-%m-%d")
        d_local = (datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d")
        allowed_dates.add(d_utc)
        allowed_dates.add(d_local)

    all_vulns = []
    # NVD
    all_vulns.extend(fetch_nvd(day_count=7))
    # cxsecurity
    all_vulns.extend(fetch_cxsecurity())
    # 安全客
    all_vulns.extend(fetch_anquanke())

    # 去重 + 日期过滤
    new_vulns = []
    for v in all_vulns:
        if not v["id"]:
            continue
        if v["id"] in seen_db:
            continue
        date_str = v.get("date", "")
        if date_str and date_str not in allowed_dates:
            continue
        seen_db[v["id"]] = date_str
        new_vulns.append(v)

    log(f"去重后新增: {len(new_vulns)} 条")

    if new_vulns:
        # 按日期分组，每天一篇
        by_date = {}
        for v in new_vulns:
            d = v.get("date") or today_local
            by_date.setdefault(d, []).append(v)

        for date_str, vulns in sorted(by_date.items()):
            title = f"🔐 漏洞情报 {date_str}"
            content = render_note(vulns, date_str)
            doc_id = import_doc(content, title, DEFAULT_FOLDER)
            if doc_id:
                log(f"  ✅ 写入: {title}（{len(vulns)} 条）doc_id={doc_id}")
            else:
                for v in vulns:
                    seen_db.pop(v["id"], None)

    save_json(VULN_SEEN, seen_db)
    save_json(LAST_RUN, {
        "last_run":   datetime.now().isoformat(),
        "new_count":  len(new_vulns),
        "total_seen": len(seen_db),
    })
    log(f"完成！本期新增 {len(new_vulns)} 条漏洞")

if __name__ == "__main__":
    run()
