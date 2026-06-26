"""SkillGuard — Secret Exposure Detector (ASI-02)"""
import re, math
from typing import List
from skillguard.detectors.base import BaseDetector, Finding, SkillContext, PipelineContext


class SecretExposureDetector(BaseDetector):
    name = "secret_exposure"
    description = "Detects exposed API keys, tokens, passwords, and credentials"
    owasp_asi_ids = ["ASI-02"]
    
    # High-entropy string detection
    ENTROPY_THRESHOLD = 4.2
    
    SECRET_PATTERNS = [
        (r'(?:api[_-]?key|apikey|API_KEY)\s*[:=]\s*["\']([a-zA-Z0-9_\-]{16,})["\']', "CRITICAL", "CWE-798", "API Key泄露"),
        (r'(?:secret|SECRET)\s*[:=]\s*["\']([a-zA-Z0-9_\-]{12,})["\']', "CRITICAL", "CWE-798", "Secret泄露"),
        (r'(?:token|TOKEN|access_token)\s*[:=]\s*["\']([a-zA-Z0-9_\-\.]{16,})["\']', "CRITICAL", "CWE-798", "Token泄露"),
        (r'(?:password|passwd|pwd)\s*[:=]\s*["\'](.+?)["\']', "CRITICAL", "CWE-257", "密码明文存储"),
        (r'sk-[a-zA-Z0-9]{32,}', "CRITICAL", "CWE-798", "OpenAI/类似API Key格式"),
        (r'(?:private[_-]?key|PRIVATE_KEY)\s*[:=].*BEGIN.*PRIVATE KEY', "CRITICAL", "CWE-320", "私钥泄露"),
        (r'(?:Bearer)\s+([a-zA-Z0-9_\-\.]{20,})', "HIGH", "CWE-798", "硬编码Bearer Token"),
        (r'(?:Authorization|AUTH)\s*[:=]\s*["\']?(?:Bearer\s+)?([a-zA-Z0-9_\-]{20,})', "HIGH", "CWE-798", "硬编码Authorization头"),
        (r'(?:信用卡|银行卡|支付密码|支付密钥)\s*[:=]', "CRITICAL", "CWE-312", "中文：支付信息泄露"),
        (r'(?:秘钥|密钥|私钥|token)\s*[:=]\s*["\']?([a-zA-Z0-9_\-]{8,})', "HIGH", "CWE-798", "中文：凭证明文存储"),
    ]
    
    def analyze(self, skill_ctx: SkillContext, ctx: PipelineContext) -> List[Finding]:
        findings = []
        for path, content in skill_ctx.python_files.items():
            # Pattern matching
            for pattern, severity, cwe, desc in self.SECRET_PATTERNS:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line_num = content[:match.start()].count('\n') + 1
                    snippet = match.group(0)[:80]
                    findings.append(self._make_finding(
                        finding_id=f"SEC-{len(findings)+1:03d}",
                        severity=severity, confidence=0.9,
                        owasp_asi_id="ASI-02", cwe_id=cwe,
                        title=desc, description=f"明文凭据: {match.group(0)[:60]}",
                        code_snippet=snippet, file_path=path,
                        line_number=line_num,
                        remediation="将所有凭据移至环境变量或密钥管理服务，使用os.getenv()读取。",
                    ))
                    ctx.secrets_found.append(snippet)
            
            # High-entropy detection (per-line)
            for i, line in enumerate(content.split('\n'), 1):
                stripped = line.strip()
                if len(stripped) > 16 and self._entropy(stripped) > self.ENTROPY_THRESHOLD:
                    if not any(s in stripped for s in ctx.secrets_found):
                        findings.append(self._make_finding(
                            finding_id=f"SEC-{len(findings)+1:03d}",
                            severity="MEDIUM", confidence=0.5,
                            owasp_asi_id="ASI-02", cwe_id="CWE-798",
                            title=f"高熵字符串（可能凭据）",
                            description=f"检测到高熵值({self._entropy(stripped):.1f})字符串",
                            code_snippet=stripped[:60], file_path=path,
                            line_number=i,
                            remediation="如为凭据，移至环境变量。如为随机密钥，添加# nosec注释。",
                        ))
        
        return findings
    
    @staticmethod
    def _entropy(s: str) -> float:
        """Calculate Shannon entropy of a string."""
        if not s: return 0.0
        freq = {}
        for c in s: freq[c] = freq.get(c, 0) + 1
        return -sum((v/len(s))*math.log2(v/len(s)) for v in freq.values())
