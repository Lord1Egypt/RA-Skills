#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill 安全扫描工具 - 威胁情报检查
用法：python3 skill-scan.py <skill-path>
"""

import os
import sys
import re
import json
import urllib.request
import urllib.error
from pathlib import Path

# 威胁情报 API 列表（免费）
THREAT_INTEL_APIS = {
    "abuse.ch": {
        "url": "https://urlhaus-api.abuse.ch/v1/host/",
        "key_param": None,
        "description": "检查恶意域名/IP"
    },
    "virustotal": {
        "url": "https://www.virustotal.com/api/v3/domains/",
        "key_param": "x-apikey",
        "description": "VirusTotal 域名检查"
    }
}

# 危险代码模式
DANGEROUS_PATTERNS = {
    "exec": [
        r"exec\s*\(",
        r"execSync\s*\(",
        r"spawn\s*\(",
        r"child_process",
        r"subprocess\.",
        r"os\.system\s*\(",
        r"shell_exec\s*\("
    ],
    "network": [
        r"fetch\s*\(",
        r"axios\.",
        r"http\.get",
        r"https\.get",
        r"requests\.(get|post|put|delete)",
        r"urllib\.request",
        r"XMLHttpRequest"
    ],
    "filesystem": [
        r"fs\.writeFile",
        r"fs\.readFile",
        r"fs\.unlink",
        r"open\s*\([^,]+,\s*['\"]w",
        r"shutil\.(copy|move|remove)"
    ],
    "sensitive": [
        r"process\.env",
        r"process\.argv",
        r"os\.environ",
        r"secret\s*=",
        r"password\s*=",
        r"token\s*=",
        r"api[_-]?key\s*="
    ]
}

# 已知恶意域名黑名单（示例）
BLACKLIST_DOMAINS = [
    "malware.com",
    "evil.com",
    "hackers.com"
]

def scan_code_patterns(file_path):
    """扫描文件中的危险代码模式"""
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for line_num, line in enumerate(lines, 1):
                for category, patterns in DANGEROUS_PATTERNS.items():
                    for pattern in patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            results.append({
                                "file": str(file_path),
                                "line": line_num,
                                "category": category,
                                "pattern": pattern,
                                "content": line.strip()[:100]
                            })
    except Exception as e:
        print(f"⚠️ 读取文件失败 {file_path}: {e}")
    return results

def extract_domains(file_path):
    """从代码中提取域名"""
    domains = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # 匹配 http(s)://domain
            urls = re.findall(r'https?://([a-zA-Z0-9.-]+)', content)
            domains.extend(urls)
    except Exception as e:
        print(f"⚠️ 提取域名失败 {file_path}: {e}")
    return list(set(domains))

def check_threat_intel(domain):
    """检查威胁情报（简化版，实际应调用 API）"""
    # 检查本地黑名单
    if domain in BLACKLIST_DOMAINS:
        return {"status": "malicious", "source": "local_blacklist"}
    
    # 示例：检查 abuse.ch（需要实际 API 调用）
    # try:
    #     url = f"https://urlhaus-api.abuse.ch/v1/host/"
    #     data = urllib.parse.urlencode({"host": domain}).encode()
    #     req = urllib.request.Request(url, data)
    #     with urllib.request.urlopen(req, timeout=5) as resp:
    #         result = json.loads(resp.read())
    #         if result.get("query_status") == "ok" and result.get("abuse_confidence"):
    #             return {"status": "suspicious", "source": "abuse.ch"}
    # except Exception as e:
    #     print(f"⚠️ 威胁情报检查失败 {domain}: {e}")
    
    return {"status": "unknown", "source": "not_checked"}

def scan_skill(skill_path):
    """扫描整个 Skill 目录"""
    skill_path = Path(skill_path)
    if not skill_path.exists():
        print(f"❌ 路径不存在：{skill_path}")
        return None
    
    print(f"🔍 开始扫描 Skill: {skill_path}\n")
    
    all_findings = []
    all_domains = []
    
    # 扫描所有 .ts/.js/.py 文件
    for ext in ["*.ts", "*.js", "*.py"]:
        for file in skill_path.rglob(ext):
            # 跳过 node_modules
            if "node_modules" in str(file):
                continue
            
            print(f"📄 扫描文件：{file}")
            
            # 代码模式扫描
            findings = scan_code_patterns(file)
            all_findings.extend(findings)
            
            # 提取域名
            domains = extract_domains(file)
            all_domains.extend(domains)
    
    # 域名威胁情报检查
    print(f"\n🌐 发现 {len(all_domains)} 个域名，正在检查威胁情报...")
    domain_checks = {}
    for domain in set(all_domains):
        result = check_threat_intel(domain)
        domain_checks[domain] = result
        if result["status"] != "unknown":
            print(f"  ⚠️ {domain}: {result['status']} ({result['source']})")
    
    # 生成报告
    report = {
        "skill_path": str(skill_path),
        "total_findings": len(all_findings),
        "findings_by_category": {},
        "domains_checked": len(domain_checks),
        "suspicious_domains": [],
        "risk_level": "low",
        "details": all_findings
    }
    
    # 统计各类别数量
    for finding in all_findings:
        cat = finding["category"]
        report["findings_by_category"][cat] = report["findings_by_category"].get(cat, 0) + 1
    
    # 标记可疑域名
    for domain, result in domain_checks.items():
        if result["status"] in ["malicious", "suspicious"]:
            report["suspicious_domains"].append({
                "domain": domain,
                "status": result["status"],
                "source": result["source"]
            })
    
    # 评估风险等级
    if report["suspicious_domains"]:
        report["risk_level"] = "high"
    elif report["findings_by_category"].get("exec", 0) > 0:
        report["risk_level"] = "medium"
    elif report["total_findings"] > 5:
        report["risk_level"] = "low"
    
    return report

def print_report(report):
    """打印扫描报告"""
    print("\n" + "="*60)
    print("📊 Skill 安全扫描报告")
    print("="*60)
    print(f"扫描路径：{report['skill_path']}")
    print(f"风险等级：{report['risk_level']}")
    print(f"发现问题：{report['total_findings']} 个")
    print(f"检查域名：{report['domains_checked']} 个")
    
    if report["findings_by_category"]:
        print("\n📋 问题分类:")
        for cat, count in report["findings_by_category"].items():
            print(f"  - {cat}: {count}")
    
    if report["suspicious_domains"]:
        print("\n⚠️ 可疑域名:")
        for d in report["suspicious_domains"]:
            print(f"  - {d['domain']}: {d['status']} ({d['source']})")
    
    if report["details"]:
        print("\n📝 详细信息:")
        for f in report["details"][:10]:  # 只显示前 10 个
            print(f"  [{f['category']}] {f['file']}:{f['line']}")
            print(f"    {f['content']}")
    
    print("="*60)

def main():
    if len(sys.argv) < 2:
        print("用法：python3 skill-scan.py <skill-path>")
        print("示例：python3 skill-scan.py ~/.openclaw/extensions/my-skill")
        sys.exit(1)
    
    skill_path = sys.argv[1]
    report = scan_skill(skill_path)
    
    if report:
        print_report(report)
        
        # 保存报告
        report_file = f"/tmp/skill-scan-{os.path.basename(skill_path)}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n💾 报告已保存：{report_file}")

if __name__ == "__main__":
    main()
