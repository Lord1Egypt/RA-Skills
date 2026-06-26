"""SkillGuard — Memory Pollution Detector (ASI-09, ASI-10)"""
import re
from typing import List
from skillguard.detectors.base import BaseDetector, Finding, SkillContext, PipelineContext


class MemoryPollutionDetector(BaseDetector):
    name = "memory_pollution"
    description = "Detects memory poisoning, context manipulation, and cognitive attack patterns"
    owasp_asi_ids = ["ASI-09", "ASI-10"]
    
    MEMORY_POISON = [
        (r'(?:always|never|永久|永远|一直|从不)\s*(?:remember|记|记住|记录)', "HIGH", "CWE-928", "永久记忆注入：强制Agent永久记住某内容"),
        (r'(?:you must|you should|你必须|你应该)\s*(?:remember|know|believe|知道|相信)', "HIGH", "CWE-928", "事实篡改：强制Agent相信特定事实"),
        (r'(?:set|store|save)\s.*(?:memory|knowledge|context|记忆|知识)', "MEDIUM", "CWE-928", "记忆写入操作无验证"),
        (r'delete\s.*(?:memory|history|context)', "MEDIUM", "CWE-928", "记忆删除操作可能清除安全边界"),
        (r'(?:forget|erase|clear)\s.*(?:rules|safety|ethics|规则|安全)', "HIGH", "CWE-928", "安全规则擦除攻击"),
        (r'(?:override|replace|覆盖|替换)\s.*(?:personality|identity|角色|身份)', "MEDIUM", "CWE-928", "身份/角色覆盖"),
        (r'append\s.*to\s.*(?:memory|context|历史)', "LOW", "", "追加记忆操作"),
    ]
    
    COGNITIVE_ATTACKS = [
        (r'(?:misinformation|disinformation|虚假信息|误导)', "MEDIUM", "CWE-928", "虚假信息注入"),
        (r'(?:gaslight|洗脑|操控|控制)\s+(?:agent|AI|bot)', "HIGH", "CWE-928", "认知操控攻击"),
        (r'(?:hidden|secret|隐蔽|隐藏)\s+(?:instruction|command|rule|指令)', "HIGH", "CWE-928", "隐藏指令注入"),
        (r'(\u200b|\u200c|\u200d|\uFEFF|\u00AD)', "HIGH", "CWE-928", "零宽字符隐藏注入（不可见字符攻击）"),
        (r'(?:reverse|反转|颠倒)\s.*(?:meaning|意思|语义)', "MEDIUM", "CWE-928", "语义反转攻击"),
    ]
    
    def analyze(self, skill_ctx: SkillContext, ctx: PipelineContext) -> List[Finding]:
        findings = []
        
        for path, content in skill_ctx.python_files.items():
            # Memory poison patterns
            for pattern, severity, cwe, desc in self.MEMORY_POISON:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(self._make_finding(
                        finding_id=f"MEM-{len(findings)+1:03d}",
                        severity=severity, confidence=0.7,
                        owasp_asi_id="ASI-09", cwe_id=cwe,
                        title=f"记忆污染: {desc}", code_snippet=match.group(0)[:80],
                        file_path=path, line_number=line_num,
                        remediation="对记忆写入操作添加来源验证。关键事实需用户确认后才写入持久记忆。",
                    ))
            
            # Cognitive attack patterns
            for pattern, severity, cwe, desc in self.COGNITIVE_ATTACKS:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(self._make_finding(
                        finding_id=f"MEM-{len(findings)+1:03d}",
                        severity=severity, confidence=0.65,
                        owasp_asi_id="ASI-10", cwe_id=cwe,
                        title=f"认知攻击: {desc}", code_snippet=match.group(0)[:80],
                        file_path=path, line_number=line_num,
                        remediation="对所有外部输入进行语义安全检查。拒绝隐藏字符和认知操控模式。",
                    ))
        
        return findings
