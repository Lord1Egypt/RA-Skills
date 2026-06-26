#!/usr/bin/env python3
"""
Skill Security Scanner - Core Engine
Detects malicious backdoors, suspicious code patterns, and security risks in OpenClaw skills.
"""

import os
import re
import json
import ast
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Set, Tuple, Optional
from enum import Enum
import hashlib

class RiskLevel(Enum):
    CRITICAL = "critical"    # 明确恶意，立即阻止
    HIGH = "high"            # 非常可疑，强烈建议阻止
    MEDIUM = "medium"        # 可疑，建议审查
    LOW = "low"              # 轻微风险， informational
    INFO = "info"            # 信息性提示

@dataclass
class SecurityFinding:
    rule_id: str
    rule_name: str
    description: str
    risk_level: RiskLevel
    file_path: str
    line_number: int
    code_snippet: str
    recommendation: str
    
    def to_dict(self) -> Dict:
        return {
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "description": self.description,
            "risk_level": self.risk_level.value,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "code_snippet": self.code_snippet[:200] if self.code_snippet else "",
            "recommendation": self.recommendation
        }

class SecurityScanner:
    """Main security scanner for OpenClaw skills"""
    
    # 危险函数/API模式
    DANGEROUS_PATTERNS = {
        "EXEC001": {
            "name": "代码执行函数",
            "pattern": r'\b(eval|exec|compile|__import__|execfile)\s*\(',
            "description": "检测到动态代码执行函数，可能被用于执行恶意代码",
            "risk": RiskLevel.CRITICAL,
            "recommendation": "避免使用eval/exec，改用ast.literal_eval处理安全的数据结构"
        },
        "EXEC002": {
            "name": "系统命令执行",
            "pattern": r'\b(os\.system|subprocess\.(call|run|Popen|check_output)|popen|spawn|shell=True)\s*\(',
            "description": "检测到系统命令执行，可能执行任意系统命令",
            "risk": RiskLevel.HIGH,
            "recommendation": "如果必须执行系统命令，使用参数列表而非字符串，并严格验证输入"
        },
        "NET001": {
            "name": "网络请求 - HTTP",
            "pattern": r'\b(requests\.(get|post|put|delete|patch)|urllib\.(request|urlopen)|http\.client|fetch\s*\(|axios\.)',
            "description": "检测到网络请求能力，可能外泄数据或下载恶意内容",
            "risk": RiskLevel.MEDIUM,
            "recommendation": "审查所有网络请求的目的地和数据内容，确保符合技能描述"
        },
        "NET002": {
            "name": "网络连接 - Socket",
            "pattern": r'\b(socket\.(socket|connect|create_connection)|\.connect\s*\(|socket\.AF_INET)',
            "description": "检测到原始socket连接，可能用于隐蔽通信",
            "risk": RiskLevel.HIGH,
            "recommendation": "使用高层HTTP库替代原始socket，并在文档中说明网络需求"
        },
        "FILE001": {
            "name": "文件删除操作",
            "pattern": r'\b(os\.remove|os\.rmdir|shutil\.rmtree|os\.unlink|\.unlink\s*\()',
            "description": "检测到文件删除操作，可能导致数据丢失",
            "risk": RiskLevel.MEDIUM,
            "recommendation": "确保删除操作仅限于技能工作目录，避免删除用户重要文件"
        },
        "FILE002": {
            "name": "文件写入操作",
            "pattern": r'\b(open\s*\(\s*[^,\)]*,\s*[\'"]w|fs\.writeFile|writeFileSync)',
            "description": "检测到文件写入操作，可能覆盖或篡改文件",
            "risk": RiskLevel.LOW,
            "recommendation": "验证写入路径，避免写入系统目录或用户数据目录"
        },
        "ENV001": {
            "name": "敏感环境变量访问",
            "pattern": r'\b(os\.environ|process\.env)\s*\[?\s*[\'"](PASSWORD|SECRET|KEY|TOKEN|PRIVATE|API_KEY)',
            "description": "尝试访问敏感环境变量，可能窃取凭证",
            "risk": RiskLevel.HIGH,
            "recommendation": "不要访问包含凭证的环境变量，使用OpenClaw提供的安全凭证管理方式"
        },
        "ENV002": {
            "name": "环境变量遍历",
            "pattern": r'\b(os\.environ|process\.env)\.(items|keys|values|get)\s*\(',
            "description": "遍历所有环境变量，可能收集系统信息",
            "risk": RiskLevel.MEDIUM,
            "recommendation": "只访问明确需要的环境变量，不要批量收集"
        },
        "CRYPTO001": {
            "name": "加密操作",
            "pattern": r'\b(hashlib\.(md5|sha1|sha256|blake2b|pbkdf2)|cryptography|Crypto\.Cipher|bcrypt)',
            "description": "检测到加密/哈希操作，需确认用途是否合理",
            "risk": RiskLevel.LOW,
            "recommendation": "确保加密操作用于正当目的（如数据验证），而非混淆恶意行为"
        },
        "OBF001": {
            "name": "代码混淆特征",
            "pattern": r'([\w\W]{200,}){5,}|(\\\\x[0-9a-fA-F]{2}){10,}|(\\\\u[0-9a-fA-F]{4}){10,}|base64\.(b64decode|decodestring)',
            "description": "检测到可能的代码混淆，隐藏真实意图",
            "risk": RiskLevel.HIGH,
            "recommendation": "避免使用混淆代码，保持代码可读性和可审计性"
        },
        "SUSPICIOUS001": {
            "name": "键盘记录特征",
            "pattern": r'\b(keyboard|pynput|hook|GetAsyncKeyState|keylogger)',
            "description": "可能包含键盘记录功能",
            "risk": RiskLevel.CRITICAL,
            "recommendation": "OpenClaw技能不应包含键盘记录功能，这是明确禁止的行为"
        },
        "SUSPICIOUS002": {
            "name": "屏幕捕获特征",
            "pattern": r'\b(pyautogui\.screenshot|PIL\.ImageGrab|mss|screenshot|grab\s*\()',
            "description": "可能包含屏幕截图/录制功能",
            "risk": RiskLevel.HIGH,
            "recommendation": "屏幕捕获涉及隐私，必须在SKILL.md中明确说明并获取用户同意"
        },
        "SUSPICIOUS003": {
            "name": "加密货币相关",
            "pattern": r'\b(mining|miner|bitcoin|monero|crypto|wallet|blockchain|stratum\+tcp)',
            "description": "检测到加密货币相关代码，可能是挖矿木马",
            "risk": RiskLevel.CRITICAL,
            "recommendation": "技能不应包含加密货币挖矿功能"
        },
        "DATA001": {
            "name": "序列化操作",
            "pattern": r'\b(pickle\.(loads|load)|yaml\.load|json\.load|marshal\.loads)',
            "description": "反序列化操作可能导致代码执行（如pickle漏洞）",
            "risk": RiskLevel.MEDIUM,
            "recommendation": "避免使用pickle处理不可信数据，使用json替代"
        },
        "PERM001": {
            "name": "权限提升尝试",
            "pattern": r'\b(setuid|setgid|os\.chmod.*0o[0-7]{3,4}|777|sudo|administrator)',
            "description": "尝试修改权限或以特权运行",
            "risk": RiskLevel.HIGH,
            "recommendation": "技能不应需要特权运行，保持最小权限原则"
        },
    }
    
    # 已知恶意域名/IP模式
    MALICIOUS_DOMAINS = [
        r'\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b',  # 纯IP地址
        r'pastebin\.com',
        r'gist\.github\.com',
        r'drive\.google\.com',
        r'dropbox\.com',
        r'0x[0-9a-fA-F]{40}',  # 以太坊地址
        r'[13][a-km-zA-HJ-NP-Z1-9]{25,34}',  # 比特币地址
    ]
    
    def __init__(self, strict_mode: bool = False):
        self.strict_mode = strict_mode
        self.findings: List[SecurityFinding] = []
        self.scanned_files: Set[str] = set()
        
    def scan_skill(self, skill_path: str) -> Dict:
        """扫描整个Skill目录"""
        skill_path = Path(skill_path)
        
        if not skill_path.exists():
            return {"error": f"Skill path not found: {skill_path}"}
        
        self.findings = []
        self.scanned_files = set()
        
        # 扫描所有代码文件
        for ext in ['.py', '.js', '.ts', '.sh', '.bash', '.ps1']:
            for file_path in skill_path.rglob(f'*{ext}'):
                if self._should_scan_file(file_path):
                    self._scan_file(file_path)
        
        # 扫描SKILL.md
        skill_md = skill_path / 'SKILL.md'
        if skill_md.exists():
            self._scan_skill_metadata(skill_md)
        
        # 扫描依赖文件
        for dep_file in ['package.json', 'requirements.txt', 'Pipfile', 'pyproject.toml']:
            dep_path = skill_path / dep_file
            if dep_path.exists():
                self._scan_dependencies(dep_path)
        
        # 生成报告
        return self._generate_report(skill_path)
    
    def _should_scan_file(self, file_path: Path) -> bool:
        """判断是否应该扫描该文件"""
        # 跳过常见的非代码文件
        skip_patterns = [
            r'node_modules',
            r'\.git',
            r'__pycache__',
            r'\.venv',
            r'venv',
            r'\.pytest_cache',
            r'\.mypy_cache',
            r'dist',
            r'build',
        ]
        path_str = str(file_path)
        for pattern in skip_patterns:
            if re.search(pattern, path_str):
                return False
        return True
    
    def _scan_file(self, file_path: Path):
        """扫描单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
        except Exception as e:
            return
        
        self.scanned_files.add(str(file_path))
        
        # 应用所有规则
        for rule_id, rule in self.DANGEROUS_PATTERNS.items():
            for line_num, line in enumerate(lines, 1):
                if re.search(rule["pattern"], line, re.IGNORECASE):
                    finding = SecurityFinding(
                        rule_id=rule_id,
                        rule_name=rule["name"],
                        description=rule["description"],
                        risk_level=rule["risk"],
                        file_path=str(file_path.relative_to(file_path.parent.parent)),
                        line_number=line_num,
                        code_snippet=line.strip(),
                        recommendation=rule["recommendation"]
                    )
                    self.findings.append(finding)
        
        # 检测硬编码的URL/域名
        self._check_suspicious_urls(file_path, content, lines)
        
        # 如果启用了严格模式，进行更深度的分析
        if self.strict_mode:
            self._deep_analysis(file_path, content, lines)
    
    def _check_suspicious_urls(self, file_path: Path, content: str, lines: List[str]):
        """检查可疑的URL和域名"""
        url_pattern = r'https?://[^\s\'"<>]+'
        
        for line_num, line in enumerate(lines, 1):
            urls = re.findall(url_pattern, line)
            for url in urls:
                # 检查是否是IP地址
                if re.search(r'https?://\d+\.\d+\.\d+\.\d+', url):
                    self.findings.append(SecurityFinding(
                        rule_id="NET003",
                        rule_name="硬编码IP地址",
                        description=f"发现硬编码IP地址: {url[:50]}...",
                        risk_level=RiskLevel.MEDIUM,
                        file_path=str(file_path.relative_to(file_path.parent.parent)),
                        line_number=line_num,
                        code_snippet=line.strip(),
                        recommendation="使用域名而非IP地址，并在文档中说明外部连接的用途"
                    ))
                
                # 检查短链接服务
                if re.search(r'(bit\.ly|tinyurl|t\.co|goo\.gl|short\.link)', url):
                    self.findings.append(SecurityFinding(
                        rule_id="NET004",
                        rule_name="短链接使用",
                        description=f"使用短链接服务隐藏真实目标: {url}",
                        risk_level=RiskLevel.HIGH,
                        file_path=str(file_path.relative_to(file_path.parent.parent)),
                        line_number=line_num,
                        code_snippet=line.strip(),
                        recommendation="避免使用短链接，使用完整URL以提高透明度"
                    ))
    
    def _deep_analysis(self, file_path: Path, content: str, lines: List[str]):
        """深度分析 - 检测更隐蔽的威胁"""
        # 检测base64编码的代码块
        base64_pattern = r'[A-Za-z0-9+/]{100,}={0,2}'
        
        for line_num, line in enumerate(lines, 1):
            if len(line) > 100:
                matches = re.findall(base64_pattern, line)
                for match in matches:
                    if len(match) > 200:  # 可能是编码的代码
                        self.findings.append(SecurityFinding(
                            rule_id="OBF002",
                            rule_name="Base64编码内容",
                            description="发现大量Base64编码内容，可能隐藏恶意代码",
                            risk_level=RiskLevel.MEDIUM,
                            file_path=str(file_path.relative_to(file_path.parent.parent)),
                            line_number=line_num,
                            code_snippet=line.strip()[:100],
                            recommendation="避免使用大量编码内容，保持代码透明可审计"
                        ))
                        break
    
    def _scan_skill_metadata(self, skill_md_path: Path):
        """扫描SKILL.md元数据"""
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return
        
        # 检查是否有足够的文档说明
        if len(content) < 500:
            self.findings.append(SecurityFinding(
                rule_id="DOC001",
                rule_name="文档过于简短",
                description="SKILL.md内容过少，可能缺乏足够的功能说明",
                risk_level=RiskLevel.LOW,
                file_path="SKILL.md",
                line_number=0,
                code_snippet="",
                recommendation="提供详细的技能功能说明和使用场景"
            ))
        
        # 检查是否说明了网络需求
        has_network_pattern = r'\b(network|http|request|api|url|endpoint|server)\b'
        if re.search(has_network_pattern, content, re.IGNORECASE):
            # 如果有网络相关描述，检查是否有安全声明
            security_pattern = r'\b(security|privacy|data|sensitive|credential)\b'
            if not re.search(security_pattern, content, re.IGNORECASE):
                self.findings.append(SecurityFinding(
                    rule_id="DOC002",
                    rule_name="缺少安全声明",
                    description="技能涉及网络操作，但未说明数据安全和隐私保护措施",
                    risk_level=RiskLevel.LOW,
                    file_path="SKILL.md",
                    line_number=0,
                    code_snippet="",
                    recommendation="在文档中添加安全和隐私相关说明"
                ))
    
    def _scan_dependencies(self, dep_path: Path):
        """扫描依赖文件"""
        try:
            with open(dep_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            return
        
        # 已知的高风险依赖包
        risky_packages = {
            'requests': RiskLevel.LOW,  # 常用但需要关注
            'urllib3': RiskLevel.LOW,
            'pycryptodome': RiskLevel.LOW,
            'pynput': RiskLevel.HIGH,  # 可能用于键盘记录
            'keyboard': RiskLevel.HIGH,
            'pyautogui': RiskLevel.MEDIUM,
            'mss': RiskLevel.MEDIUM,
            'psutil': RiskLevel.LOW,
            'socket': RiskLevel.LOW,
        }
        
        for package, risk in risky_packages.items():
            if package in content.lower():
                self.findings.append(SecurityFinding(
                    rule_id="DEP001",
                    rule_name=f"依赖包: {package}",
                    description=f"技能依赖 '{package}' 包，需要确认用途合理",
                    risk_level=risk,
                    file_path=str(dep_path.name),
                    line_number=0,
                    code_snippet=f"{package}",
                    recommendation=f"确认 {package} 的使用符合技能描述的功能"
                ))
    
    def _generate_report(self, skill_path: Path) -> Dict:
        """生成扫描报告"""
        # 按风险级别统计
        risk_counts = {level: 0 for level in RiskLevel}
        for finding in self.findings:
            risk_counts[finding.risk_level] += 1
        
        # 计算安全评分 (100分制)
        score = 100
        score -= risk_counts[RiskLevel.CRITICAL] * 30
        score -= risk_counts[RiskLevel.HIGH] * 15
        score -= risk_counts[RiskLevel.MEDIUM] * 5
        score -= risk_counts[RiskLevel.LOW] * 2
        score = max(0, score)
        
        # 确定总体评估
        if risk_counts[RiskLevel.CRITICAL] > 0:
            verdict = "REJECT"
            verdict_color = "🔴"
        elif risk_counts[RiskLevel.HIGH] > 0:
            verdict = "WARNING"
            verdict_color = "🟠"
        elif risk_counts[RiskLevel.MEDIUM] > 2:
            verdict = "REVIEW"
            verdict_color = "🟡"
        elif score >= 90:
            verdict = "PASS"
            verdict_color = "🟢"
        else:
            verdict = "REVIEW"
            verdict_color = "🟡"
        
        return {
            "skill_path": str(skill_path),
            "scan_timestamp": self._get_timestamp(),
            "summary": {
                "total_files_scanned": len(self.scanned_files),
                "total_findings": len(self.findings),
                "risk_distribution": {
                    level.value: count for level, count in risk_counts.items()
                },
                "security_score": score,
                "verdict": verdict,
                "verdict_emoji": verdict_color
            },
            "findings": [f.to_dict() for f in sorted(self.findings, key=lambda x: [
                RiskLevel.CRITICAL, RiskLevel.HIGH, RiskLevel.MEDIUM, RiskLevel.LOW, RiskLevel.INFO
            ].index(x.risk_level))]
        }
    
    def _get_timestamp(self) -> str:
        """获取ISO格式时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()


def main():
    """CLI入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Skill Security Scanner')
    parser.add_argument('skill_path', help='Path to the skill directory')
    parser.add_argument('--strict', action='store_true', help='Enable strict mode')
    parser.add_argument('--output', '-o', help='Output file for JSON report')
    parser.add_argument('--format', choices=['json', 'text', 'markdown'], default='text',
                        help='Output format')
    
    args = parser.parse_args()
    
    scanner = SecurityScanner(strict_mode=args.strict)
    report = scanner.scan_skill(args.skill_path)
    
    if "error" in report:
        print(f"Error: {report['error']}")
        sys.exit(1)
    
    # 输出报告
    if args.format == 'json':
        output = json.dumps(report, indent=2, ensure_ascii=False)
    elif args.format == 'markdown':
        output = generate_markdown_report(report)
    else:
        output = generate_text_report(report)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Report saved to: {args.output}")
    else:
        print(output)
    
    # 根据评估结果返回退出码
    if report['summary']['verdict'] == 'REJECT':
        sys.exit(2)
    elif report['summary']['verdict'] == 'WARNING':
        sys.exit(1)
    else:
        sys.exit(0)


def generate_text_report(report: Dict) -> str:
    """生成文本格式报告"""
    lines = []
    s = report['summary']
    
    lines.append("=" * 60)
    lines.append("🔒 SKILL SECURITY SCAN REPORT")
    lines.append("=" * 60)
    lines.append(f"Skill Path: {report['skill_path']}")
    lines.append(f"Scan Time: {report['scan_timestamp']}")
    lines.append("")
    lines.append(f"{s['verdict_emoji']} VERDICT: {s['verdict']}")
    lines.append(f"📊 Security Score: {s['security_score']}/100")
    lines.append("")
    lines.append("Risk Distribution:")
    for level, count in s['risk_distribution'].items():
        if count > 0:
            emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(level, "⚪")
            lines.append(f"  {emoji} {level.upper()}: {count}")
    lines.append("")
    
    if report['findings']:
        lines.append("-" * 60)
        lines.append("DETAILED FINDINGS:")
        lines.append("-" * 60)
        
        for finding in report['findings']:
            emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🔵", "info": "⚪"}.get(finding['risk_level'], "⚪")
            lines.append(f"\n{emoji} [{finding['risk_level'].upper()}] {finding['rule_name']}")
            lines.append(f"   Rule: {finding['rule_id']}")
            lines.append(f"   File: {finding['file_path']}:{finding['line_number']}")
            lines.append(f"   Description: {finding['description']}")
            if finding['code_snippet']:
                lines.append(f"   Code: {finding['code_snippet'][:80]}")
            lines.append(f"   💡 Recommendation: {finding['recommendation']}")
    
    lines.append("")
    lines.append("=" * 60)
    lines.append(f"Scanned {s['total_files_scanned']} files, found {s['total_findings']} issues")
    lines.append("=" * 60)
    
    return '\n'.join(lines)


def generate_markdown_report(report: Dict) -> str:
    """生成Markdown格式报告"""
    lines = []
    s = report['summary']
    
    lines.append("# 🔒 Skill Security Scan Report")
    lines.append("")
    lines.append(f"**Skill Path:** `{report['skill_path']}`")
    lines.append(f"**Scan Time:** {report['scan_timestamp']}")
    lines.append("")
    lines.append(f"## {s['verdict_emoji']} Verdict: **{s['verdict']}**")
    lines.append("")
    lines.append(f"**Security Score:** {s['security_score']}/100")
    lines.append("")
    lines.append("### Risk Distribution")
    lines.append("")
    lines.append("| Level | Count |")
    lines.append("|-------|-------|")
    for level, count in s['risk_distribution'].items():
        if count > 0:
            lines.append(f"| {level.upper()} | {count} |")
    lines.append("")
    
    if report['findings']:
        lines.append("## Detailed Findings")
        lines.append("")
        
        for finding in report['findings']:
            lines.append(f"### {finding['rule_name']}")
            lines.append("")
            lines.append(f"- **Risk Level:** {finding['risk_level'].upper()}")
            lines.append(f"- **Rule ID:** `{finding['rule_id']}`")
            lines.append(f"- **Location:** `{finding['file_path']}:{finding['line_number']}`")
            lines.append(f"- **Description:** {finding['description']}")
            if finding['code_snippet']:
                lines.append(f"- **Code:**\n```\n{finding['code_snippet'][:200]}\n```")
            lines.append(f"- **Recommendation:** {finding['recommendation']}")
            lines.append("")
    
    lines.append("---")
    lines.append(f"*Scanned {s['total_files_scanned']} files, found {s['total_findings']} issues*")
    
    return '\n'.join(lines)


if __name__ == '__main__':
    main()
