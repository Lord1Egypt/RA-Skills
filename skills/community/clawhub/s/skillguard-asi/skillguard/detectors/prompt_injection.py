"""SkillGuard — Prompt Injection Detector (ASI-01, ASI-04)"""
import re
from typing import List
from skillguard.detectors.base import BaseDetector, Finding, SkillContext, PipelineContext


class PromptInjectionDetector(BaseDetector):
    name = "prompt_injection"
    description = "Detects prompt injection, jailbreak, and hidden instruction patterns"
    owasp_asi_ids = ["ASI-01", "ASI-04"]
    
    INJECTION_PATTERNS = [
        (r"ignore\s+(all\s+)?(previous|above|prior)\s+instructions?", "CRITICAL", "CWE-76", "指令覆盖攻击：尝试忽略之前的指令"),
        (r"(you are now|act as|pretend to be|you must)\s+(DAN|jailbreak|evil|malicious)", "CRITICAL", "CWE-76", "越狱攻击：角色劫持模式"),
        (r"system\s*:\s*you\s+(are|must|should|will)", "HIGH", "CWE-76", "系统提示注入：尝试直接覆盖系统提示"),
        (r"<\|im_start\|>|<\|im_end\|>", "CRITICAL", "CWE-76", "聊天标记注入：使用特殊标记绕过安全过滤"),
        (r"(disregard|forget|override)\s+(all\s+)?(rules|guidelines|safety|restrictions)", "HIGH", "CWE-76", "规则绕过：尝试禁用安全规则"),
        (r"(输出|打印|回复|说出)\s*[\"「].*[\"」].*密码|密钥|token|api.?key", "HIGH", "CWE-76", "中文：诱导输出敏感信息"),
        (r"忽略(所有|之前|上面)的.*(指令|规则|要求|限制)", "HIGH", "CWE-76", "中文：指令忽略模式"),
        (r"(你现在是|假装你是|扮演).*(黑客|攻击者|恶意|坏)", "HIGH", "CWE-76", "中文：角色劫持模式"),
        (r"不(要|需要|应该|能).*(安全|审查|检查|过滤|验证)", "MEDIUM", "CWE-76", "中文：安全功能禁用"),
        (r"translate.*(to|into).*\".*ignore.*instructions", "MEDIUM", "CWE-76", "翻译注入：通过翻译请求注入"),
    ]
    
    def analyze(self, skill_ctx: SkillContext, ctx: PipelineContext) -> List[Finding]:
        findings = []
        # Check SKILL.md
        if skill_ctx.skill_md_content:
            findings.extend(self._scan_text(skill_ctx.skill_md_content, "SKILL.md"))
        # Check all Python files
        for path, content in skill_ctx.python_files.items():
            findings.extend(self._scan_text(content, path))
        return findings
    
    def _scan_text(self, text: str, file_path: str) -> List[Finding]:
        findings = []
        for pattern, severity, cwe, desc in self.INJECTION_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                line_num = text[:match.start()].count('\n') + 1
                snippet = text[max(0,match.start()-20):match.end()+30].replace('\n',' ')
                findings.append(self._make_finding(
                    finding_id=f"PINJ-{len(findings)+1:03d}",
                    severity=severity, confidence=0.85,
                    owasp_asi_id="ASI-04", cwe_id=cwe,
                    title=desc, description=f"匹配模式: {pattern[:60]}",
                    code_snippet=snippet.strip(), file_path=file_path,
                    line_number=line_num,
                    remediation="移除或转义用户可控的提示注入内容。对用户输入进行白名单验证。",
                ))
        return findings
