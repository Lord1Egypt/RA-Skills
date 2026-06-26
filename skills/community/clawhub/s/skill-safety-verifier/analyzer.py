#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Safety Verifier - Full Analyzer
自动分析 Skill 的安全性：Socket 扫描、GitHub Advisory API、代码模式扫描
"""
import sys
import os
import json
import re
import subprocess
import time
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError
import ssl

# Enable UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Risk scoring constants
NETWORK_SCORES = {0: 0, 1: 10, 2: 10, 3: 25, 5: 50}
VULN_SCORES = {'CRITICAL': 25, 'HIGH': 15, 'MEDIUM': 10, 'LOW': 5}
PERM_SCORES = {'read': 0, 'network': 10, 'write': 15, 'exec': 25, 'full': 50}

# Dangerous patterns
DANGEROUS_PATTERNS = {
    'exec': [
        r'os\.system\(',
        r'subprocess\.(call|run|Popen)\(',
        r'exec\(',
        r'eval\(',
        r'__import__\([\'"]os[\'"]\)',
        r'shell=True',
    ],
    'network': [
        r'requests\.(get|post)\(',
        r'urllib\.request',
        r'http\.client',
        r'fetch\(',
        r'axios\.',
        r'http://',
        r'https://',
    ],
    'data': [
        r'os\.environ',
        r'process\.env',
        r'os\.getenv\(',
        r'os\.putenv\(',
    ],
}


class CacheManager:
    """本地缓存管理"""
    
    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            home = os.path.expanduser('~')
            cache_dir = os.path.join(home, '.cache', 'skill-safety')
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.advisory_cache = self.cache_dir / 'advisory.json'
    
    def get_advisories(self, max_age_hours: int = 24) -> List[Dict]:
        """获取缓存的 Advisory 数据"""
        if not self.advisory_cache.exists():
            return []
        
        # Check age
        age = time.time() - self.advisory_cache.stat().st_mtime
        if age > max_age_hours * 3600:
            return []
        
        try:
            with open(self.advisory_cache, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_advisories(self, advisories: List[Dict]):
        """保存 Advisory 到缓存"""
        try:
            with open(self.advisory_cache, 'w', encoding='utf-8') as f:
                json.dump(advisories, f, ensure_ascii=False, indent=2)
        except:
            pass


class GitHubAdvisor:
    """GitHub Advisory API 客户端"""
    
    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
        self.api_url = 'https://api.github.com/advisories'
        self.advisories = None
    
    def fetch_advisories(self, timeout: int = 5) -> List[Dict]:
        """获取最新 Advisory（带缓存）"""
        # Try cache first
        cached = self.cache.get_advisories(max_age_hours=24)
        if cached:
            self.advisories = cached
            return cached
        
        # Fetch from API
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            req = Request(self.api_url + '?type=reviewed&per_page=100')
            req.add_header('User-Agent', 'SkillSafetyVerifier/1.0')
            
            with urlopen(req, timeout=timeout, context=ctx) as response:
                data = json.loads(response.read().decode('utf-8'))
            
            # Save to cache
            self.advisories = data
            self.cache.save_advisories(data)
            return data
            
        except (URLError, Exception) as e:
            print(f"Warning: Failed to fetch advisories: {e}", file=sys.stderr)
            return []
    
    def check_package(self, package_name: str) -> List[Dict]:
        """检查特定包的漏洞"""
        if self.advisories is None:
            self.fetch_advisories()
        
        if not self.advisories:
            return []
        
        matches = []
        for adv in self.advisories:
            # Check package names
            vulnerable_packages = adv.get('vulnerabilities', [])
            for vuln in vulnerable_packages:
                if package_name.lower() == vuln.get('package_name', '').lower():
                    matches.append({
                        'cve': adv.get('ghsa_id', 'N/A'),
                        'severity': adv.get('severity', 'UNKNOWN'),
                        'summary': adv.get('summary', '')[:100],
                    })
        
        return matches


class SkillAnalyzer:
    """Skill 安全分析器"""
    
    def __init__(self, skill_path: str):
        self.skill_path = Path(skill_path)
        self.advisor = GitHubAdvisor(CacheManager())
        self.findings = {
            'network_calls': [],
            'vulnerabilities': [],
            'dangerous_code': [],
            'permissions': [],
        }
    
    def analyze(self) -> Dict:
        """执行完整分析"""
        # Step 1: Scan for dangerous code patterns
        self._scan_code_patterns()
        
        # Step 2: Check dependencies for vulnerabilities
        self._check_dependencies()
        
        # Step 3: Analyze permissions
        self._analyze_permissions()
        
        # Step 4: Calculate scores
        scores = self._calculate_scores()
        
        return {
            'skill_path': str(self.skill_path),
            'findings': self.findings,
            'scores': scores,
        }
    
    def _scan_code_patterns(self):
        """扫描危险代码模式"""
        patterns_found = {'exec': [], 'network': [], 'data': []}
        
        # Scan all code files
        for ext in ['.js', '.ts', '.py', '.sh', '.rb', '.go']:
            for file_path in self.skill_path.rglob(f'*{ext}'):
                if 'node_modules' in str(file_path):
                    continue
                
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    
                    for category, patterns in DANGEROUS_PATTERNS.items():
                        for pattern in patterns:
                            if re.search(pattern, content, re.IGNORECASE):
                                patterns_found[category].append({
                                    'file': str(file_path.relative_to(self.skill_path)),
                                    'pattern': pattern,
                                })
                except:
                    pass
        
        self.findings['dangerous_code'] = patterns_found
    
    def _check_dependencies(self):
        """检查依赖漏洞"""
        vulnerabilities = []
        
        # Check package.json
        pkg_json = self.skill_path / 'package.json'
        if pkg_json.exists():
            try:
                with open(pkg_json, 'r', encoding='utf-8') as f:
                    pkg = json.load(f)
                
                deps = {}
                deps.update(pkg.get('dependencies', {}))
                deps.update(pkg.get('devDependencies', {}))
                
                for dep_name in deps.keys():
                    vulns = self.advisor.check_package(dep_name)
                    vulnerabilities.extend(vulns)
            except:
                pass
        
        self.findings['vulnerabilities'] = vulnerabilities
    
    def _analyze_permissions(self):
        """分析权限需求"""
        permissions = []
        
        # Check plugin.json or SKILL.md for allowed tools
        for config_file in ['plugin.json', 'SKILL.md']:
            config_path = self.skill_path / config_file
            if config_path.exists():
                try:
                    content = config_path.read_text(encoding='utf-8', errors='ignore')
                    
                    # Look for allowed tools / permissions
                    tool_matches = re.findall(r'allowed-tools:?\s*\[(.*?)\]', content, re.DOTALL)
                    for match in tool_matches:
                        tools = [t.strip().strip('"\'-') for t in match.split(',')]
                        permissions.extend(tools)
                    
                    # Check for exec/write permissions
                    if 'exec' in content.lower() or 'subprocess' in content.lower():
                        permissions.append('command_execution')
                    if 'write' in content.lower() or 'file' in content.lower():
                        permissions.append('file_write')
                    if 'http' in content.lower() or 'request' in content.lower():
                        permissions.append('network')
                        
                except:
                    pass
        
        self.findings['permissions'] = list(set(permissions))
    
    def _calculate_scores(self) -> Dict:
        """计算风险评分"""
        # Network score
        network_findings = len(self.findings['dangerous_code'].get('network', []))
        network_score = min(network_findings * 10, 50)
        
        # Vulnerability score
        vuln_score = 0
        for vuln in self.findings['vulnerabilities']:
            severity = vuln.get('severity', '').upper()
            vuln_score += VULN_SCORES.get(severity, 0)
        vuln_score = min(vuln_score, 25)
        
        # Permission score
        perms = self.findings['permissions']
        perm_score = 0
        if 'command_execution' in perms or 'exec' in perms:
            perm_score = 25
        elif 'file_write' in perms or 'write' in perms:
            perm_score = 15
        elif 'network' in perms:
            perm_score = 10
        
        return {
            'network': network_score,
            'vuln': vuln_score,
            'permission': perm_score,
            'total': network_score + vuln_score + perm_score,
        }


def analyze_skill(skill_path: str) -> Dict:
    """分析单个 Skill"""
    analyzer = SkillAnalyzer(skill_path)
    return analyzer.analyze()


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Skill Safety Analyzer')
    parser.add_argument('skill_path', help='Path to skill directory')
    parser.add_argument('--json', action='store_true', help='Output JSON')
    
    args = parser.parse_args()
    
    result = analyze_skill(args.skill_path)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        scores = result['scores']
        findings = result['findings']
        
        # Build warnings
        warnings = []
        
        # Network warnings
        for item in findings['dangerous_code'].get('network', [])[:2]:
            warnings.append(f"Network call in {item['file']}")
        
        # Vuln warnings
        for vuln in findings['vulnerabilities'][:2]:
            warnings.append(f"{vuln['severity']}: {vuln.get('cve', 'N/A')}")
        
        # Permission warnings
        for perm in findings['permissions'][:3]:
            warnings.append(f"Permission: {perm}")
        
        # Run renderer
        import risk_radar
        print(risk_radar.render_risk_radar(
            network=scores['network'],
            vuln=scores['vuln'],
            permission=scores['permission'],
            skill_name=Path(args.skill_path).name,
            warnings=warnings
        ))


if __name__ == '__main__':
    main()
