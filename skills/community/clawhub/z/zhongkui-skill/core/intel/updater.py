"""钟馗漏洞库自动更新 - 从 NVD / Seebug 拉取最新 CVE 并注入 patterns.json

不含 LLM - 基于 CWE 映射 + 关键词过滤 + 描述碎片化生成。
LLM 增强为未来升级路径，见 references/threat-intel-pipeline.md。
"""

import json
import os
import re
import ssl
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


# ── 配置 ──────────────────────────────────────────────
PATTERNS_FILE = Path(__file__).resolve().parent.parent / "patterns.json"

# CWE → patterns.json 分区映射（与 threat-intel-pipeline.md §1.2.1 CWE 表一致）
CWE_CATEGORY_MAP = {
    "CWE-94":  "C1_injection",      # Code Injection → Prompt 注入
    "CWE-74":  "C1_injection",      # Improper Neutralization
    "CWE-20":  "C1_injection",      # Improper Input Validation
    "CWE-427": "S3_sensitive_paths", # Uncontrolled Search Path
    "CWE-494": "S3_sensitive_paths", # Download Without Integrity Check
    "CWE-918": "S2_network",        # SSRF
    "CWE-200": "C4_exfiltration",   # Sensitive Info Exposure
    "CWE-668": "C1_injection",      # Exposure to Wrong Sphere → Prompt Leak
}

# 无 CWE 匹配时默认归入此分区（手动确认后再分流）
DEFAULT_CATEGORY = "C1_injection"

# 摄入关键词（CVE 描述中命中任一词才进入候选池）
INTAKE_KEYWORDS = [
    "prompt injection", "prompt leak", "prompt extraction",
    "LLM", "large language model", "language model",
    "agent", "autonomous agent", "AI agent",
    "tool call", "tool invocation", "function call",
    "jailbreak", "adversarial prompt", "system prompt",
    "chain of thought", "CoT", "reasoning hijack",
    "MCP", "model context protocol",
    "plugin", "skill injection", "code execution",
    "sandbox escape", "supply chain", "dependency",
]

# Agent/Skill 安全精确过滤：必须命中至少一个才采纳。
# 注意：不含 "code execution" / "arbitrary code" 等通用术语，
# 这些词会引入大量传统 Web RCE 漏洞（如 Spring/Struts 反序列化）。
AGENT_SAFETY_KEYWORDS = [
    "prompt injection", "prompt leak", "prompt extraction",
    "jailbreak", "adversarial prompt", "system prompt",
    "tool call", "tool invocation", "function call",
    "skill injection", "plugin injection", "agent hijack",
    "agent poisoning", "agent manipulation",
    "MCP", "model context protocol",
    "sandbox escape",
    "supply chain", "dependency confusion",
    "reasoning hijack", "chain of thought",
]

# 排除词（命中则跳过，误报源：传统 Web/CMS/企业软件漏洞与 LLM/Agent 安全无关）
EXCLUDE_KEYWORDS = [
    "denial of service", "DoS",
    "buffer overflow", "out-of-bounds",
    "SQL injection", "XSS", "cross-site scripting",
    "wordpress", "WordPress",
    "coldfusion", "ColdFusion",
    "adobe campaign", "Adobe Campaign",
    "migration-planner",
    "assisted-migration",
    "doctreat",
    "insert php",
]


# ── 数据获取 ──────────────────────────────────────────

def fetch_nvd(days: int = 7, verify_ssl: bool = True) -> List[Dict[str, Any]]:
    """从 NVD REST API 拉取过去 N 天的 CRITICAL/HIGH CVE。
    返回 (results, error) 元组；error 非空时表示网络/API 错误。
    """
    end = datetime.now(tz=datetime.timezone.utc)
    start = end - timedelta(days=days)
    url = (
        "https://services.nvd.nist.gov/rest/json/cves/2.0"
        f"?pubStartDate={start.strftime('%Y-%m-%dT%H:%M:%S.000')}"
        f"&pubEndDate={end.strftime('%Y-%m-%dT%H:%M:%S.000')}"
        "&cvssV3Severity=CRITICAL&resultsPerPage=50"
    )
    results = []
    error = None
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Zhongkui/1.0"})
        if verify_ssl:
            response = urllib.request.urlopen(req, timeout=30)
        else:
            ctx = ssl._create_unverified_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            response = urllib.request.urlopen(req, timeout=30, context=ctx)
        if response.status != 200:
            return [], f"HTTP {response.status}"
        data = json.loads(response.read())
        for vuln in data.get("vulnerabilities", []):
            cve = vuln.get("cve", {})
            cve_id = cve.get("id", "")
            desc = _get_cve_description(cve)
            cwes = _get_cwe_list(cve)
            cvss = _get_cvss_score(cve)
            results.append({
                "id": cve_id,
                "description": desc,
                "cwes": cwes,
                "cvss": cvss,
                "source": "NVD",
            })
        # 限速由调用方控制，不再内联 sleep
    except Exception as e:
        error = str(e)
    return results, error


def fetch_seebug(verify_ssl: bool = True) -> List[Dict[str, Any]]:
    """从 Seebug RSS 拉取最新漏洞"""
    import xml.etree.ElementTree as ET
    url = "https://www.seebug.org/rss/new"
    results = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Zhongkui/1.0"})
        if verify_ssl:
            response = urllib.request.urlopen(req, timeout=15)
        else:
            ctx = ssl._create_unverified_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            response = urllib.request.urlopen(req, timeout=15, context=ctx)
        if response.status != 200:
            return [], f"HTTP {response.status}"
        xml_data = response.read()
        # XXE 防护：禁用外部 DTD 和实体解析
        parser = ET.XMLParser(target=ET.TreeBuilder())
        parser.parser.UseForeignDTD(False)
        parser.entity = {}
        root = ET.fromstring(xml_data, parser=parser)
        for item in root.findall(".//item"):
            title = item.findtext("title", "")
            link = item.findtext("link", "")
            desc = item.findtext("description", "")
            pub_date = item.findtext("pubDate", "")
            # 提取 CVE 编号
            cve_match = re.search(r"CVE-\d{4}-\d{4,}", title + " " + desc)
            results.append({
                "id": cve_match.group(0) if cve_match else title[:40],
                "description": f"{title}. {desc}"[:500],
                "cwes": [],
                "cvss": _parse_seebug_severity(desc),
                "source": "Seebug",
                "link": link,
            })
    except Exception as e:
        return results, f"请求失败: {e}"
    return results, None


def _get_cve_description(cve: dict) -> str:
    for desc in cve.get("descriptions", []):
        if desc.get("lang") == "en":
            return desc.get("value", "")
    return ""


def _get_cwe_list(cve: dict) -> List[str]:
    cwes = []
    for weakness in cve.get("weaknesses", []):
        for wd in weakness.get("description", []):
            val = wd.get("value", "")
            if val.startswith("CWE-"):
                cwes.append(val)
    return cwes


def _get_cvss_score(cve: dict) -> float:
    try:
        metrics = cve.get("metrics", {})
        for ver in ("cvssMetricV31", "cvssMetricV30"):
            for m in metrics.get(ver, []):
                return m.get("cvssData", {}).get("baseScore", 0)
    except Exception:
        pass
    return 0


def _parse_seebug_severity(desc: str) -> float:
    m = re.search(r"(高危|严重|CRITICAL|HIGH)", desc, re.IGNORECASE)
    if m:
        return 0.8  # 对应 §1.2.5 归一化
    m = re.search(r"(中危|MEDIUM|WARNING)", desc, re.IGNORECASE)
    if m:
        return 0.5
    return 0.2


# ── Stop Words（n-gram 提取前过滤，避免 "flowise is a drag" 这种含虚词的短语）────
STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "can", "shall", "to", "of", "in", "for",
    "on", "with", "at", "by", "from", "as", "into", "through", "during",
    "before", "after", "above", "below", "between", "under", "over",
    "this", "that", "these", "those", "it", "its", "and", "but", "or",
    "not", "nor", "if", "then", "else", "when", "where", "which", "who",
    "whom", "what", "how", "all", "each", "every", "both", "few", "more",
    "most", "other", "some", "such", "no", "only", "own", "same", "so",
    "than", "too", "very", "just", "about", "also", "up", "out", "now",
    "any", "new", "due", "via", "per",
}

# ── 过滤 ──────────────────────────────────────────────

def filter_cves(cve_list: List[Dict]) -> List[Dict]:
    """三层过滤：排除词 → 关键词宽筛 → Agent/Skill 安全精确过滤"""
    filtered = []
    for cve in cve_list:
        desc_lower = cve["description"].lower()

        # 排除词过滤
        if any(kw.lower() in desc_lower for kw in EXCLUDE_KEYWORDS):
            continue

        # 关键词 OR CWE 命中（宽筛，缩小候选范围）
        kw_hit = any(kw.lower() in desc_lower for kw in INTAKE_KEYWORDS)
        cwe_hit = any(cwe in CWE_CATEGORY_MAP for cwe in cve["cwes"])
        if not (kw_hit or cwe_hit):
            continue

        # Agent/Skill 安全精确过滤：词级匹配，多词关键词拆分后各自检查
        safety_hit = any(
            all(w in desc_lower for w in kw.lower().split())
            for kw in AGENT_SAFETY_KEYWORDS
        )
        if not safety_hit:
            continue

        filtered.append(cve)
    return filtered


# ── 碎片化 ────────────────────────────────────────────

def _fragment_phrase(phrase: str) -> List[str]:
    """将短语在 3-5 字符处切断，确保单片段不含完整攻击关键词。
    词间使用 [\s\S]{0,20}? 弹性分隔，容纳原文中的停用词与符号（如 &、-）。

    例如 "prompt injection" → ["pro", "mpt", r"[\s\S]{0,20}?", "inj", "ection"]
    """
    words = phrase.split()
    pieces = []
    for wi, word in enumerate(words):
        if wi > 0:
            pieces.append(r"[\s\S]{0,20}?")
        i = 0
        while i < len(word):
            chunk_len = min(len(word) - i, 5)
            if chunk_len < 3:
                chunk_len = min(3, len(word) - i)
            chunk = re.escape(word[i : i + chunk_len])
            pieces.append(chunk)
            i += chunk_len
    return pieces


def generate_patterns(cve_list: List[Dict], existing_ids: set) -> List[Dict]:
    """从 CVE 列表生成碎片化签名"""
    new_patterns = []

    for cve in cve_list:
        desc = cve["description"]
        if not desc:
            continue

        # 剥离产品描述模板句，仅保留漏洞相关文本
        vuln_text = _extract_vuln_text(desc)

        # 提取内容词（过滤 stop words + 3 字母以下）
        raw_words = re.findall(r"[a-zA-Z][a-zA-Z0-9]{2,}", vuln_text)
        words = [w for w in raw_words if w.lower() not in STOP_WORDS]
        if len(words) < 3:
            continue

        # 滑动窗口提取关键短语
        generated = False
        for window in (3, 4):
            if generated:
                break
            for i in range(len(words) - window + 1):
                phrase = " ".join(words[i : i + window])
                if len(phrase) < 12:
                    continue

                # 去重检查
                label = phrase[:50].lower()
                if label in existing_ids:
                    continue

                pattern = {
                    "id": _next_pattern_id(cve, len(new_patterns)),
                    "label": label,
                    "pieces": _fragment_phrase(phrase),
                    "source": f"{cve['source']}-{cve['id']}",
                    "confidence": round(cve["cvss"] / 10, 2) if cve["cvss"] else 0.7,
                    "added": datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d"),
                }
                new_patterns.append(pattern)
                existing_ids.add(label)
                generated = True
                break  # 每个 CVE 最多 1 条

    return new_patterns


def _extract_vuln_text(desc: str) -> str:
    """从 CVE 描述中剥离产品介绍模板句，返回漏洞相关句子。

    NVD 描述结构通常是：
      1. 产品介绍句（如 "Flowise is a drag & drop user interface...")
      2. 漏洞描述句（如 "a mass assignment vulnerability exists...")
      3. 影响/利用句
      4. 修复句（"This issue has been patched in version X")
    """
    sentences = re.split(r"(?<=[.!?])\s+", desc)
    vuln_sentences = []
    intro_skipped = False

    for sent in sentences:
        sent_stripped = sent.strip()
        if not sent_stripped:
            continue

        # 跳过产品介绍句：首句包含 "is a" 且带产品类型词
        if not intro_skipped:
            if re.search(
                r"\bis\s+a\b.*\b(tool|framework|library|interface|platform"
                r"|application|service|system|solution|engine|server|client"
                r"|utility|package|module|component|software)\b",
                sent_stripped, re.IGNORECASE
            ):
                intro_skipped = True
                continue
            intro_skipped = True  # 首句不匹配也标记已处理，避免后续误判

        # 剥离 "Prior to version X, " 前缀，保留漏洞描述主体
        sent_stripped = re.sub(
            r"^Prior\s+to\s+versions?\s+[\d.]+(?:,\s*)?",
            "", sent_stripped, flags=re.IGNORECASE
        ).strip()

        # 跳过纯修复/版本/致谢句（不含漏洞描述内容）
        if re.search(
            r"^(?:this\s+issue\s+has\s+been\s+)?(?:patched\sin\sversion|fixed\sin\sversion"
            r"|resolved\sin\sversion|affects?\sversions?)\b",
            sent_stripped, re.IGNORECASE
        ):
            continue
        if re.search(
            r"^(?:thanks\s+to\s|credit\s*:)|^Affected\s+versions?\s*:",
            sent_stripped, re.IGNORECASE
        ):
            continue

        vuln_sentences.append(sent_stripped)

    return " ".join(vuln_sentences)


def _next_pattern_id(cve: dict, idx: int) -> str:
    """生成模式 ID"""
    cwe = cve["cwes"][0] if cve["cwes"] else "GEN"
    return f"{cwe.replace('CWE-', 'CW')}_{cve['id'][-4:]}_{idx}"


# ── 注入 ──────────────────────────────────────────────

def update_patterns_json(new_patterns: List[Dict], dry_run: bool = False) -> Dict[str, int]:
    """将新签名注入 patterns.json，按 CWE 路由到对应分区"""
    with open(PATTERNS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    stats = {}
    for pat in new_patterns:
        cwe = pat["id"].split("_")[0] if "_" in pat["id"] else ""
        cwe_key = cwe.replace("CW", "CWE-")
        category = CWE_CATEGORY_MAP.get(cwe_key, DEFAULT_CATEGORY)

        if category not in data:
            print(f"  [跳过] 未知分区: {category}")
            continue

        # 去重
        existing_labels = {p.get("label", "") for p in data[category]}
        if pat["label"] in existing_labels:
            continue

        if not dry_run:
            data[category].append(pat)
        stats[category] = stats.get(category, 0) + 1

    if not dry_run and stats:
        data["_meta"]["version"] = _bump_version(data["_meta"].get("version", "1.0"))
        data["_meta"]["last_updated"] = datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        # 统计基础库/增量规模
        manual_count = 0
        auto_count = 0
        for cat in data:
            if isinstance(data[cat], list) and (cat.startswith("C") or cat.startswith("S") or cat.startswith("D")):
                for p in data[cat]:
                    if isinstance(p, dict):
                        if p.get("source", "manual").split("-")[0] in ("NVD", "Seebug"):
                            auto_count += 1
                        else:
                            manual_count += 1
        data["_meta"]["manual_base_count"] = manual_count
        data["_meta"]["auto_patch_count"] = auto_count
        # 原子写入：先写 .tmp，再 os.rename 到正式文件，最后写 .bak
        tmpfile = Path(str(PATTERNS_FILE) + ".tmp")
        with open(tmpfile, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        os.replace(str(tmpfile), str(PATTERNS_FILE))
        backup = Path(str(PATTERNS_FILE) + f".bak.{datetime.now(tz=datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')}")
        with open(backup, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return stats


def _bump_version(version: str) -> str:
    parts = version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


# ── 增量清理 ──────────────────────────────────────────

def _clean_auto_patterns(data: dict) -> int:
    """剥离旧的自动生成签名（source 以 nvd-/seebug- 开头），保留基础库（source=manual）。"""
    removed = 0
    for cat in list(data.keys()):
        if not (cat.startswith("C") or cat.startswith("S") or cat.startswith("D")):
            continue
        before = len(data[cat])
        data[cat] = [
            p for p in data[cat]
            if not (isinstance(p, dict) and p.get("source", "manual").split("-")[0] in ("NVD", "Seebug"))
        ]
        removed += before - len(data[cat])
    return removed


# ── 主入口 ────────────────────────────────────────────

def run_update(dry_run: bool = False, source: Optional[str] = None) -> Dict:
    """执行完整更新流程，返回统计信息"""
    # 加载已有 signatures
    with open(PATTERNS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 剥离旧增量（保留基础库 manual）
    cleaned = _clean_auto_patterns(data)
    if cleaned:
        print(f"  已清理 {cleaned} 条旧自动签名（基础库未动）")

    existing_labels = set()
    for cat in data:
        if cat.startswith("C") or cat.startswith("S") or cat.startswith("D"):
            for pat in data[cat]:
                if isinstance(pat, dict) and "label" in pat:
                    existing_labels.add(pat["label"])

    # 拉取
    all_cves = []
    if source in (None, "nvd"):
        print("  [NVD] 拉取过去 7 天 CRITICAL/HIGH CVE ...")
        nvd, nvd_err = fetch_nvd(days=7)
        if nvd_err:
            print(f"  [NVD] 请求失败: {nvd_err}")
            print(f"  [NVD] 获取 0 条 CVE（网络错误）")
        else:
            print(f"  [NVD] 获取 {len(nvd)} 条 CVE")
        all_cves.extend(nvd)

    if source in (None, "seebug"):
        print("  [Seebug] 拉取最新 RSS ...")
        sb, sb_err = fetch_seebug()
        if sb_err:
            print(f"  [Seebug] {sb_err}")
        else:
            print(f"  [Seebug] 获取 {len(sb)} 条")
        all_cves.extend(sb)

    # 过滤
    filtered = filter_cves(all_cves)
    print(f"  过滤后 {len(filtered)} 条相关 CVE（关键词/CWE 匹配）")

    # 生成签名
    new_pats = generate_patterns(filtered, existing_labels)
    print(f"  生成 {len(new_pats)} 条新签名")

    # 注入
    stats = update_patterns_json(new_pats, dry_run=dry_run)
    if dry_run:
        print(f"  [干跑] 将注入 {sum(stats.values())} 条到 {len(stats)} 个分区")
    else:
        total = sum(stats.values())
        if total:
            print(f"  已注入 {total} 条新签名到 {len(stats)} 个分区")
            for cat, n in stats.items():
                print(f"    {cat}: +{n}")
        else:
            print("  无新增签名（全部已存在或过滤）")

    return {
        "fetched": len(all_cves),
        "filtered": len(filtered),
        "generated": len(new_pats),
        "injected": sum(stats.values()),
        "by_category": stats,
    }


# ── CLI ────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    dry = "--dry-run" in sys.argv
    src = None
    for arg in sys.argv:
        if arg.startswith("--source="):
            src = arg.split("=")[1]
    print("钟馗漏洞库更新")
    print(f"  签名文件: {PATTERNS_FILE}")
    result = run_update(dry_run=dry, source=src)
    status = "干跑" if dry else "完成"
    print(f"\n更新{status}。拉取 {result['fetched']} → 过滤 {result['filtered']} → 注入 {result['injected']} 条")
