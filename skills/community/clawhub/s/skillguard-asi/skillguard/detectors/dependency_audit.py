"""SkillGuard — Dependency Audit Detector (ASI-06)"""
import re
from typing import List, Set
from skillguard.detectors.base import BaseDetector, Finding, SkillContext, PipelineContext


class DependencyAuditDetector(BaseDetector):
    name = "dependency_audit"
    description = "Audits dependencies for known dangerous packages and insecure versions"
    owasp_asi_ids = ["ASI-06"]
    
    # Known dangerous/unnecessary packages
    DANGEROUS_PACKAGES = {
        "pickle": ("HIGH", "CWE-502", "pickle反序列化不安全，建议用json代替"),
        "dill": ("HIGH", "CWE-502", "dill可序列化任意Python对象，攻击面大"),
        "cloudpickle": ("HIGH", "CWE-502", "cloudpickle反序列化风险"),
        "PyYAML": ("MEDIUM", "CWE-502", "yaml.load不安全，用yaml.safe_load"),
        "telnetlib": ("HIGH", "CWE-319", "telnet明文传输，已弃用"),
        "crypt": ("LOW", "CWE-327", "crypt使用弱加密算法，已弃用"),
        "ssl": ("LOW", "", "内置模块，无需在requirements.txt中声明"),
        "socket": ("LOW", "", "内置模块，无需声明。如需原始socket访问需安全审查"),
    }
    
    # Suspicious version patterns
    SUSPICIOUS_VERSIONS = [
        (r"==0\.\d+\.\d+", "LOW", "使用0.x版本可能不稳定或有未修复漏洞"),
        (r">=", "LOW", "不固定版本号可能导致供应链攻击"),
        (r"@\s*(git\+https?://)", "MEDIUM", "直接从git仓库安装存在供应链风险"),
    ]
    
    def analyze(self, skill_ctx: SkillContext, ctx: PipelineContext) -> List[Finding]:
        findings = []
        
        if not skill_ctx.requirements_content:
            return findings
        
        packages = self._parse_requirements(skill_ctx.requirements_content)
        
        # Check for none (empty file or all comments)
        if not packages:
            return findings
        
        # Check each package
        for pkg_name, version in packages:
            if pkg_name in self.DANGEROUS_PACKAGES:
                sev, cwe, desc = self.DANGEROUS_PACKAGES[pkg_name]
                findings.append(self._make_finding(
                    finding_id=f"DEP-{len(findings)+1:03d}",
                    severity=sev, confidence=0.85,
                    owasp_asi_id="ASI-06", cwe_id=cwe,
                    title=f"依赖风险: {pkg_name}", description=desc,
                    code_snippet=f"{pkg_name}{version}",
                    file_path="requirements.txt",
                    remediation=f"评估{pkg_name}的必要性，寻找更安全的替代方案。",
                ))
            
            # Suspicious versions
            for pattern, sev, desc in self.SUSPICIOUS_VERSIONS:
                if re.search(pattern, version or ""):
                    findings.append(self._make_finding(
                        finding_id=f"DEP-{len(findings)+1:03d}",
                        severity=sev, confidence=0.6,
                        owasp_asi_id="ASI-06", cwe_id="CWE-1104",
                        title=f"版本风险: {pkg_name}", description=desc,
                        code_snippet=f"{pkg_name}{version}",
                        file_path="requirements.txt",
                        remediation=f"固定{pkg_name}到已知安全版本（==x.y.z）。",
                    ))
        
        # Too many dependencies
        if len(packages) > 10:
            findings.append(self._make_finding(
                finding_id=f"DEP-{len(findings)+1:03d}",
                severity="LOW", confidence=0.5,
                owasp_asi_id="ASI-06", cwe_id="CWE-1104",
                title=f"依赖过多 ({len(packages)}个)",
                description="依赖越多，供应链攻击面越大。EvoMind等Skill推荐零外部依赖。",
                file_path="requirements.txt",
                remediation="精简依赖，优先使用Python标准库。",
            ))
        
        return findings
    
    @staticmethod
    def _parse_requirements(content: str) -> List[tuple]:
        """Parse pip requirements.txt into (name, version_spec) tuples."""
        packages = []
        for line in content.split('\n'):
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('--'):
                continue
            # Remove comments and extras
            line = re.sub(r'\s*#.*$', '', line).strip()
            if not line:
                continue
            
            # Parse package name and version
            match = re.match(r'^([a-zA-Z0-9_.-]+)\s*([><=!~].*)?$', line)
            if match:
                name = match.group(1)
                version = match.group(2) or ""
                # Normalize name
                name = name.lower().replace('_', '-').replace('.', '-')
                packages.append((name, version.strip()))
        
        return packages
