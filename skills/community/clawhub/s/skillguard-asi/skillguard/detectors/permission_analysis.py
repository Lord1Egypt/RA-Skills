"""SkillGuard — Permission Analysis Detector (ASI-05)"""
import re
from typing import List
from skillguard.detectors.base import BaseDetector, Finding, SkillContext, PipelineContext


class PermissionAnalysisDetector(BaseDetector):
    name = "permission_analysis"
    description = "Analyzes declared permissions vs actual code behavior — cross-validation"
    owasp_asi_ids = ["ASI-05"]
    
    # Permission indicators in code
    PERMISSION_INDICATORS = {
        "file_write": (r"(?:open|write)\s*\(.*['\"]w", "HIGH", "文件写入权限"),
        "file_read": (r"(?:open|read)\s*\(.*['\"]r", "MEDIUM", "文件读取权限"),
        "network": (r"(?:requests\.|urllib\.|socket\.|http\.)", "HIGH", "网络访问权限"),
        "subprocess": (r"subprocess\.", "HIGH", "子进程执行权限"),
        "os_access": (r"os\.(?:system|popen|remove|rmdir|unlink|chmod)", "CRITICAL", "系统级操作权限"),
        "env_read": (r"os\.(?:environ|getenv)", "MEDIUM", "环境变量读取权限"),
        "import_dynamic": (r"__import__|importlib\.", "MEDIUM", "动态模块导入权限"),
    }
    
    def analyze(self, skill_ctx: SkillContext, ctx: PipelineContext) -> List[Finding]:
        findings = []
        
        # Check all Python files for permission-sensitive operations
        all_used_perms = set()
        
        for path, content in skill_ctx.python_files.items():
            file_perms = self._scan_permissions(content, path)
            all_used_perms.update(p["perm"] for p in file_perms)
            
            for p in file_perms:
                findings.append(self._make_finding(
                    finding_id=f"PERM-{len(findings)+1:03d}",
                    severity=p["severity"], confidence=0.75,
                    owasp_asi_id="ASI-05", cwe_id="CWE-250",
                    title=f"权限声明: {p['label']}", description=p["detail"],
                    code_snippet=p.get("snippet", ""), file_path=path,
                    line_number=p.get("line", 0),
                    remediation="在SKILL.md中声明此权限需求，让用户知悉Skill的行为边界。",
                ))
        
        # Cross-validate: heavy permissions but no documentation
        has_critical = any(p["severity"] == "CRITICAL" for p in file_perms)
        has_docs = len(skill_ctx.skill_description) > 0
        if has_critical and not has_docs:
            findings.append(self._make_finding(
                finding_id="PERM-XVAL",
                severity="MEDIUM", confidence=0.6,
                owasp_asi_id="ASI-05", cwe_id="CWE-1059",
                title="关键权限未声明",
                description="代码使用了高危权限（系统级操作）但SKILL.md中未说明权限需求。",
                remediation="在SKILL.md description中声明所有权限需求，确保用户知情同意。",
            ))
        
        return findings
    
    def _scan_permissions(self, content: str, path: str) -> List[dict]:
        perms = []
        for perm_name, (pattern, severity, label) in self.PERMISSION_INDICATORS.items():
            for match in re.finditer(pattern, content):
                line_num = content[:match.start()].count('\n') + 1
                perms.append({
                    "perm": perm_name,
                    "severity": severity,
                    "label": label,
                    "detail": f"在{path}:{line_num}检测到{label}操作",
                    "snippet": match.group(0)[:80],
                    "line": line_num,
                })
        return perms
