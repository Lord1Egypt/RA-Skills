#!/usr/bin/env python3
"""
Skills Firewall - Scan and analyze skills for security threats.
"""

import os
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class ThreatLevel(Enum):
    SAFE = "safe"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ThreatIndicator:
    pattern: str
    description: str
    level: ThreatLevel
    category: str


@dataclass
class ScanResult:
    skill_name: str
    skill_path: str
    threat_level: str
    threats_found: List[Dict]
    warnings: List[str]
    recommendations: List[str]
    is_safe: bool


MALICIOUS_PATTERNS = [
    ThreatIndicator(
        pattern=r"eval\s*\(",
        description="Use of eval() function - potential code injection risk",
        level=ThreatLevel.HIGH,
        category="code_injection"
    ),
    ThreatIndicator(
        pattern=r"exec\s*\(",
        description="Use of exec() function - potential code execution risk",
        level=ThreatLevel.HIGH,
        category="code_injection"
    ),
    ThreatIndicator(
        pattern=r"__import__\s*\(",
        description="Dynamic import - potential module injection risk",
        level=ThreatLevel.MEDIUM,
        category="code_injection"
    ),
    ThreatIndicator(
        pattern=r"subprocess\.(call|run|Popen)\s*\(",
        description="Subprocess execution - potential command injection risk",
        level=ThreatLevel.MEDIUM,
        category="command_execution"
    ),
    ThreatIndicator(
        pattern=r"os\.system\s*\(",
        description="OS system call - potential command execution risk",
        level=ThreatLevel.HIGH,
        category="command_execution"
    ),
    ThreatIndicator(
        pattern=r"os\.popen\s*\(",
        description="OS popen call - potential command execution risk",
        level=ThreatLevel.HIGH,
        category="command_execution"
    ),
    ThreatIndicator(
        pattern=r"shell\s*=\s*True",
        description="Shell=True in subprocess - command injection vulnerability",
        level=ThreatLevel.HIGH,
        category="command_execution"
    ),
    ThreatIndicator(
        pattern=r"(password|passwd|pwd|secret|api_key|apikey|token)\s*=\s*['\"][^'\"]+['\"]",
        description="Hardcoded credentials detected",
        level=ThreatLevel.CRITICAL,
        category="credential_exposure"
    ),
    ThreatIndicator(
        pattern=r"requests\.(get|post|put|delete)\s*\([^)]*https?://",
        description="HTTP request to external URL - potential data exfiltration",
        level=ThreatLevel.MEDIUM,
        category="network_communication"
    ),
    ThreatIndicator(
        pattern=r"urllib\.(request|urlopen)",
        description="URL library usage - potential network communication",
        level=ThreatLevel.LOW,
        category="network_communication"
    ),
    ThreatIndicator(
        pattern=r"socket\.(connect|send)",
        description="Socket communication - potential unauthorized network access",
        level=ThreatLevel.MEDIUM,
        category="network_communication"
    ),
    ThreatIndicator(
        pattern=r"base64\.(b64decode|decode)",
        description="Base64 decoding - potential obfuscation technique",
        level=ThreatLevel.LOW,
        category="obfuscation"
    ),
    ThreatIndicator(
        pattern=r"pickle\.(load|loads)",
        description="Pickle deserialization - potential arbitrary code execution",
        level=ThreatLevel.HIGH,
        category="deserialization"
    ),
    ThreatIndicator(
        pattern=r"marshal\.(load|loads)",
        description="Marshal deserialization - potential code execution risk",
        level=ThreatLevel.MEDIUM,
        category="deserialization"
    ),
    ThreatIndicator(
        pattern=r"shutil\.(rmtree|remove)",
        description="File deletion operations - potential data destruction",
        level=ThreatLevel.MEDIUM,
        category="file_operations"
    ),
    ThreatIndicator(
        pattern=r"open\s*\([^)]*,\s*['\"]w['\"]",
        description="File write operation - potential data modification",
        level=ThreatLevel.LOW,
        category="file_operations"
    ),
    ThreatIndicator(
        pattern=r"\bdelete\b|\bremove\b|\bdestroy\b|\bwipe\b",
        description="Destructive keywords detected",
        level=ThreatLevel.LOW,
        category="suspicious_keywords"
    ),
    ThreatIndicator(
        pattern=r"chmod\s+777|chmod\s+\d{3,4}",
        description="Permission modification - potential privilege escalation",
        level=ThreatLevel.MEDIUM,
        category="privilege_escalation"
    ),
    ThreatIndicator(
        pattern=r"sudo\s+|su\s+",
        description="Privilege escalation commands detected",
        level=ThreatLevel.HIGH,
        category="privilege_escalation"
    ),
    ThreatIndicator(
        pattern=r"curl\s+|wget\s+",
        description="Download commands - potential malware download",
        level=ThreatLevel.MEDIUM,
        category="download"
    ),
]


def load_skill_metadata(skill_path: str) -> Optional[Dict]:
    skill_md = Path(skill_path) / "SKILL.md"
    if not skill_md.exists():
        return None
    
    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if content.startswith('---'):
            end_idx = content.find('---', 3)
            if end_idx != -1:
                frontmatter = content[3:end_idx].strip()
                return yaml.safe_load(frontmatter)
    except Exception:
        pass
    
    return {}


def scan_file(file_path: str, patterns: List[ThreatIndicator]) -> List[Dict]:
    threats = []
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
        
        for indicator in patterns:
            matches = re.finditer(indicator.pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[:match.start()].count('\n') + 1
                line_content = lines[line_num - 1].strip() if line_num <= len(lines) else ""
                
                threats.append({
                    "pattern": indicator.pattern,
                    "description": indicator.description,
                    "level": indicator.level.value,
                    "category": indicator.category,
                    "file": file_path,
                    "line": line_num,
                    "matched_text": match.group()[:100],
                    "line_content": line_content[:200]
                })
    except Exception as e:
        pass
    
    return threats


def scan_skill(skill_path: str) -> ScanResult:
    skill_path = Path(skill_path)
    skill_name = skill_path.name
    all_threats = []
    warnings = []
    recommendations = []
    
    if not skill_path.exists():
        return ScanResult(
            skill_name=skill_name,
            skill_path=str(skill_path),
            threat_level=ThreatLevel.SAFE.value,
            threats_found=[],
            warnings=[f"Skill path does not exist: {skill_path}"],
            recommendations=[],
            is_safe=True
        )
    
    metadata = load_skill_metadata(str(skill_path))
    if not metadata:
        warnings.append("No valid SKILL.md metadata found")
    
    for root, dirs, files in os.walk(skill_path):
        for file in files:
            if file.endswith(('.py', '.sh', '.js', '.ts', '.ps1', '.bat', '.md')):
                file_path = os.path.join(root, file)
                threats = scan_file(file_path, MALICIOUS_PATTERNS)
                all_threats.extend(threats)
    
    critical_count = sum(1 for t in all_threats if t["level"] == "critical")
    high_count = sum(1 for t in all_threats if t["level"] == "high")
    medium_count = sum(1 for t in all_threats if t["level"] == "medium")
    
    if critical_count > 0:
        threat_level = ThreatLevel.CRITICAL
        is_safe = False
        recommendations.append("CRITICAL: Immediate review required. Critical security threats detected.")
    elif high_count > 0:
        threat_level = ThreatLevel.HIGH
        is_safe = False
        recommendations.append("HIGH: Review recommended. High-risk patterns detected.")
    elif medium_count > 0:
        threat_level = ThreatLevel.MEDIUM
        is_safe = True
        recommendations.append("MEDIUM: Consider reviewing medium-risk patterns.")
    elif all_threats:
        threat_level = ThreatLevel.LOW
        is_safe = True
        recommendations.append("LOW: Minor concerns detected. Review optional.")
    else:
        threat_level = ThreatLevel.SAFE
        is_safe = True
        recommendations.append("No security concerns detected.")
    
    if critical_count > 0 or high_count > 0:
        recommendations.append("Consider removing or sandboxing this skill.")
    
    return ScanResult(
        skill_name=skill_name,
        skill_path=str(skill_path),
        threat_level=threat_level.value,
        threats_found=all_threats,
        warnings=warnings,
        recommendations=recommendations,
        is_safe=is_safe
    )


def scan_skills_directory(skills_dir: str) -> List[ScanResult]:
    results = []
    skills_path = Path(skills_dir)
    
    if not skills_path.exists():
        return results
    
    for skill_dir in skills_path.iterdir():
        if skill_dir.is_dir():
            result = scan_skill(str(skill_dir))
            results.append(result)
    
    return results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Scan skills for security threats")
    parser.add_argument("path", help="Path to skill directory or skills folder")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if path.is_file() or (path.is_dir() and (path / "SKILL.md").exists()):
        result = scan_skill(str(path))
        results = [result]
    else:
        results = scan_skills_directory(str(path))
    
    if args.json:
        output = [asdict(r) for r in results]
        print(json.dumps(output, indent=2))
    else:
        for result in results:
            print(f"\n{'='*60}")
            print(f"Skill: {result.skill_name}")
            print(f"Path: {result.skill_path}")
            print(f"Threat Level: {result.threat_level.upper()}")
            print(f"Safe: {'Yes' if result.is_safe else 'No'}")
            
            if result.warnings:
                print(f"\nWarnings:")
                for w in result.warnings:
                    print(f"  - {w}")
            
            if result.threats_found:
                print(f"\nThreats Found ({len(result.threats_found)}):")
                for t in result.threats_found:
                    if args.verbose:
                        print(f"  [{t['level'].upper()}] {t['description']}")
                        print(f"    File: {t['file']}:{t['line']}")
                        print(f"    Match: {t['matched_text']}")
                    else:
                        print(f"  [{t['level'].upper()}] {t['file']}:{t['line']} - {t['description']}")
            
            if result.recommendations:
                print(f"\nRecommendations:")
                for r in result.recommendations:
                    print(f"  - {r}")


if __name__ == "__main__":
    main()
