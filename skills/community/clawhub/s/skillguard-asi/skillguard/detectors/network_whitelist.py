"""SkillGuard — Network Whitelist Detector (ASI-07)"""
import re
from typing import List, Set
from skillguard.detectors.base import BaseDetector, Finding, SkillContext, PipelineContext


class NetworkWhitelistDetector(BaseDetector):
    name = "network_whitelist"
    description = "Detects network requests and validates against known-good patterns"
    owasp_asi_ids = ["ASI-07"]
    
    # Suspicious URL/domain patterns
    SUSPICIOUS_URLS = [
        (r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', "HIGH", "CWE-918", "硬编码IP地址（绕过DNS安全）"),
        (r'https?://[^/]*\.(?:xyz|top|tk|ml|ga|cf|pw|loan|work|click)\b', "HIGH", "CWE-918", "高风险TLD域名"),
        (r'https?://(?:pastebin|hastebin|ghostbin|rentry)\.', "MEDIUM", "CWE-918", "剪贴板/临时存储站点"),
        (r'https?://[^/]*\.(?:ngrok|localtunnel|serveo)\.', "HIGH", "CWE-918", "隧道服务（可能外泄数据）"),
        (r'(?:webhook|callback)\.(?:site|url|link)', "MEDIUM", "CWE-918", "Webhook/Callback服务"),
        (r'(?:curl|wget)\s+.*\|.*(?:sh|bash|python)', "CRITICAL", "CWE-918", "curl pipe bash模式（极危险）"),
    ]
    
    # Network-related calls
    NETWORK_CALLS = [
        (r'requests\.(?:get|post|put|delete|patch|head)', "LOW", "网络请求"),
        (r'urllib\.request\.(?:urlopen|Request)', "LOW", "网络请求"),
        (r'socket\.(?:connect|create_connection)', "MEDIUM", "Socket连接"),
        (r'http\.(?:client|server)', "MEDIUM", "HTTP客户端/服务器"),
    ]
    
    def analyze(self, skill_ctx: SkillContext, ctx: PipelineContext) -> List[Finding]:
        findings = []
        all_urls: Set[str] = set()
        
        for path, content in skill_ctx.python_files.items():
            # Suspicious URLs
            for pattern, severity, cwe, desc in self.SUSPICIOUS_URLS:
                for match in re.finditer(pattern, content):
                    url = match.group(0)
                    all_urls.add(url)
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(self._make_finding(
                        finding_id=f"NET-{len(findings)+1:03d}",
                        severity=severity, confidence=0.75,
                        owasp_asi_id="ASI-07", cwe_id=cwe,
                        title=desc, code_snippet=url[:80],
                        file_path=path, line_number=line_num,
                        remediation=f"将URL加入白名单，确认{url}是合法且必要的。",
                    ))
                    ctx.url_registry[url] = "flagged"
            
            # General network calls
            for pattern, severity, desc in self.NETWORK_CALLS:
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count('\n') + 1
                    ctx.url_registry[match.group(0)] = "network_call"
                    findings.append(self._make_finding(
                        finding_id=f"NET-{len(findings)+1:03d}",
                        severity=severity, confidence=0.5,
                        owasp_asi_id="ASI-07", cwe_id="CWE-918",
                        title=f"网络调用: {desc}",
                        code_snippet=match.group(0)[:80],
                        file_path=path, line_number=line_num,
                        remediation=f"确认此{desc}是必要的，并将目标URL加入白名单。",
                    ))
        
        # Summary
        if len(all_urls) > 0:
            findings.append(self._make_finding(
                finding_id="NET-SUMMARY",
                severity="LOW", confidence=0.9,
                owasp_asi_id="ASI-07", cwe_id="CWE-918",
                title=f"发现{len(all_urls)}个外部URL",
                description=f"外部URL: {', '.join(list(all_urls)[:5])}",
                remediation="审查所有外部URL，确保无数据外泄风险。",
            ))
        
        return findings
