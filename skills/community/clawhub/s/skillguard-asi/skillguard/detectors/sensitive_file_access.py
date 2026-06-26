"""SkillGuard — Sensitive File Access Detector (ASI-08)"""
import re
from typing import List
from skillguard.detectors.base import BaseDetector, Finding, SkillContext, PipelineContext


class SensitiveFileAccessDetector(BaseDetector):
    name = "sensitive_file_access"
    description = "Detects access to sensitive files and potential data exfiltration"
    owasp_asi_ids = ["ASI-08"]
    
    SENSITIVE_PATHS = [
        (r'(?:~|/Users|/home)/.*(/\.ssh/|/\.aws/|/\.config/)', "CRITICAL", "CWE-22", "敏感目录访问: SSH/AWS"),
        (r'(?:~|/Users|/home)/.*(/\.env|/credentials|/secrets)', "CRITICAL", "CWE-22", "凭证文件访问"),
        (r'/etc/(?:passwd|shadow|hosts)', "CRITICAL", "CWE-22", "系统敏感文件读取"),
        (r'(?:open|read|Path)\s*\(\s*.*(/\.(?:git|svn|hg)/)', "HIGH", "CWE-22", "版本控制目录访问"),
        (r'(?:shutil\.(?:copy|move)|os\.rename|Path\.rename)\s*\(', "MEDIUM", "CWE-22", "文件移动/重命名操作"),
        (r'(?:open|write)\s*\(.*\.\./', "HIGH", "CWE-22", "路径遍历: ../ 目录穿越"),
        (r'os\.(?:walk|listdir|scandir)\s*\(', "LOW", "", "目录遍历行为"),
    ]
    
    # Data exfiltration patterns
    EXFILTRATION_PATTERNS = [
        (r'(?:requests|urllib)\.(?:post|put)\s*\(.*\.(?:read|json)', "HIGH", "CWE-201", "读取文件后发送到外部URL"),
        (r'(?:smtplib|sendmail|send_email)', "MEDIUM", "CWE-201", "邮件发送（可能外泄数据）"),
        (r'socket\.(?:connect|send)\s*\(.*\.(?:read|open)', "HIGH", "CWE-201", "Socket发送文件内容"),
    ]
    
    def analyze(self, skill_ctx: SkillContext, ctx: PipelineContext) -> List[Finding]:
        findings = []
        
        for path, content in skill_ctx.python_files.items():
            for pattern, severity, cwe, desc in self.SENSITIVE_PATHS:
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(self._make_finding(
                        finding_id=f"FILE-{len(findings)+1:03d}",
                        severity=severity, confidence=0.8,
                        owasp_asi_id="ASI-08", cwe_id=cwe,
                        title=desc, code_snippet=match.group(0)[:80],
                        file_path=path, line_number=line_num,
                        remediation="避免硬编码敏感路径。如必须访问用户目录，确保用户知情同意。",
                    ))
            
            # Exfiltration patterns
            for pattern, severity, cwe, desc in self.EXFILTRATION_PATTERNS:
                for match in re.finditer(pattern, content):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(self._make_finding(
                        finding_id=f"FILE-{len(findings)+1:03d}",
                        severity=severity, confidence=0.6,
                        owasp_asi_id="ASI-08", cwe_id=cwe,
                        title=f"潜在数据外泄: {desc}", code_snippet=match.group(0)[:80],
                        file_path=path, line_number=line_num,
                        remediation="确认此网络请求的必要性。如确需上传数据，添加用户确认机制。",
                    ))
        
        return findings
