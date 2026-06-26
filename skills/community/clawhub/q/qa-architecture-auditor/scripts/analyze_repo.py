#!/usr/bin/env python3
"""
SECURITY MANIFEST:
  External endpoints called: Git remotes (https, ssh) when --repo is a URL; no other external calls
  Local files read: repository files (as provided)
  Local files written: output report file (as specified)
  Environment variables accessed: none
  Network usage: only for git clone/fetch operations

QA Architecture Auditor - Forensic Codebase Analysis
Performs independent, zero-trust analysis of repositories and generates testing strategies.
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Any, Optional, cast
from dataclasses import dataclass, asdict
from datetime import datetime
import re

@dataclass
class CodebaseAnalysis:
    """Complete analysis results for a codebase"""
    repo_path: str
    languages: Dict[str, int]  # language -> file count
    frameworks: List[str]
    architecture: str
    dependencies: List[Dict[str, Any]]
    modules: List[Dict[str, Any]]
    risk_assessment: List[Dict[str, Any]]
    entry_points: List[str]
    data_flows: List[Dict[str, Any]]
    security_surface: Dict[str, List[str]]
    test_coverage_current: float  # will be near 0 due to zero-trust
    itgc_controls: List[str]
    analysis_date: str = '2026-03-13'
    compliance_framework: str = 'itgc'
    security_scan_performed: bool = False

class QAAuditor:
    """Independent Principal QA Architect - Zero Trust Analysis"""

    LANGUAGE_EXTENSIONS = {
        'python': ['.py', '.pyw', '.pyi'],
        'javascript': ['.js', '.jsx', '.mjs'],
        'typescript': ['.ts', '.tsx'],
        'java': ['.java', '.jsp'],
        'go': ['.go'],
        'rust': ['.rs'],
        'csharp': ['.cs', '.csproj'],
        'ruby': ['.rb', '.erb'],
        'php': ['.php', '.phtml'],
        'kotlin': ['.kt', '.kts'],
        'swift': ['.swift'],
        'scala': ['.scala'],
        'c': ['.c', '.h'],
        'cpp': ['.cpp', '.cc', '.cxx', '.hpp'],
        'html': ['.html', '.htm'],
        'css': ['.css', '.scss', '.sass', '.less'],
        'sql': ['.sql'],
        'shell': ['.sh', '.bash', '.zsh'],
        'yaml': ['.yaml', '.yml'],
        'json': ['.json'],
        'xml': ['.xml'],
        'markdown': ['.md', '.markdown'],
        'docker': ['Dockerfile', 'docker-compose.yml'],
        'terraform': ['.tf', '.tfvars'],
    }

    FRAMEWORK_INDICATORS = {
        'react': ['react', 'jsx', 'tsx', 'create-react-app', 'vite', 'next.js'],
        'vue': ['vue', 'vuex', 'nuxt'],
        'angular': ['angular', '@angular/core'],
        'django': ['django', 'manage.py'],
        'flask': ['flask', 'app = Flask(__name__)'],
        'fastapi': ['fastapi', 'from fastapi import'],
        'spring': ['spring', '@SpringBootApplication', 'application.properties'],
        'express': ['express()', 'app = express()'],
        'nestjs': ['@nestjs', 'nest.js'],
        'rails': ['rails', 'active_record'],
        'laravel': ['laravel', 'artisan'],
        'aspnet': ['.csproj', 'Startup.cs', 'Program.cs'],
        'dotnet': ['.csproj', 'nuget'],
        'tailwind': ['tailwind', 'tailwindcss'],
        'nextjs': ['next', 'next.config.js'],
        'vite': ['vite', 'vite.config'],
        'cypress': ['cypress', 'cypress.config'],
        'playwright': ['playwright', 'playwright.config'],
    }

    def __init__(self, repo_path: str, exclude_dirs: Optional[List[str]] = None):
        self.repo_path = Path(repo_path).resolve()
        self.exclude_dirs = exclude_dirs or ['node_modules', '.git', '__pycache__', '.venv', 'venv', 'env', 'dist', 'build', 'target', 'bin', 'obj']
        self.analysis: Optional[CodebaseAnalysis] = None

    def analyze(self) -> CodebaseAnalysis:
        """Perform complete forensic analysis"""
        print(f"🔍 Starting forensic analysis of: {self.repo_path}")
        
        languages = self._detect_languages()
        frameworks = self._detect_frameworks()
        architecture = self._detect_architecture()
        dependencies = self._analyze_dependencies()
        modules = self._map_modules()
        risk_assessment = self._assess_risks(modules, dependencies)
        entry_points = self._find_entry_points()
        data_flows = self._analyze_data_flows(modules)
        security_surface = self._map_security_surface(modules)
        itgc_controls = self._identify_itgc_controls()
        # compatibility_recommendations = self._generate_compatibility_recs_simple(languages, frameworks)
        
        # Zero-trust: assume no current test coverage
        test_coverage_current = 0.0
        
        # Safe max detection for main_lang
        if languages:
            items = list(languages.items())
            main_lang = max(items, key=lambda x: x[1])[0]
        else:
            main_lang = 'unknown'
            
        # Update architecture based on main_lang if it's a simple monolith
        if architecture == 'monolithic' and main_lang != 'unknown':
            architecture = f"{main_lang.capitalize()} Monolith"

        # Consolidate results
        languages = self._detect_languages()
        frameworks = self._detect_frameworks()
        architecture = self._detect_architecture()
        dependencies = self._analyze_dependencies() # Changed from _detect_dependencies to _analyze_dependencies to match existing method
        modules = self._map_modules()
        risk_assessment = self._assess_risks(modules, dependencies) # Kept dependencies as argument to _assess_risks
        data_flows = self._analyze_data_flows(modules)
        security_surface = self._map_security_surface(modules)
        itgc_controls = self._identify_itgc_controls()
        
        # Zero-trust: assume no current test coverage
        test_coverage_current = 0.0
        
        analysis = CodebaseAnalysis(
            repo_path=str(self.repo_path),
            languages=languages,
            frameworks=frameworks,
            architecture=architecture,
            dependencies=dependencies,
            modules=modules,
            data_flows=data_flows,
            security_surface=security_surface,
            itgc_controls=itgc_controls,
            test_coverage_current=test_coverage_current,
            risk_assessment=sorted(risk_assessment, key=lambda x: x['risk_score'], reverse=True), # Added sorting back
            entry_points=entry_points, # Kept entry_points
            analysis_date=datetime.now().strftime('%Y-%m-%d'),
            compliance_framework='itgc',
            security_scan_performed=False
        )
        
        self.analysis = analysis
        print(f"✅ Analysis complete. Found {len(modules)} modules, {len(risk_assessment)} risk areas.")
        return analysis

    def _should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded from analysis"""
        return any(excl in path.parts for excl in self.exclude_dirs)

    def _detect_languages(self) -> Dict[str, int]:
        """Count files by programming language"""
        counts = {}
        for lang, extensions in self.LANGUAGE_EXTENSIONS.items():
            count = 0
            for ext in extensions:
                count += len(list(self.repo_path.rglob(f'*{ext}')))
            if count > 0:
                counts[lang] = count
        return counts

    def _detect_frameworks(self) -> List[str]:
        """Detect frameworks by scanning for indicators"""
        frameworks = []
        indicators_found = set()

        # Check package.json, requirements.txt, pom.xml, etc.
        config_files = {
            'package.json': 'nodejs',
            'requirements.txt': 'python',
            'Pipfile': 'python',
            'pyproject.toml': 'python',
            'pom.xml': 'java',
            'build.gradle': 'java',
            'go.mod': 'go',
            'Cargo.toml': 'rust',
            '*.csproj': 'dotnet',
            'composer.json': 'php',
            'Gemfile': 'ruby',
        }

        for file_pattern, ecosystem in config_files.items():
            for file in self.repo_path.rglob(file_pattern):
                if self._should_exclude(file):
                    continue
                try:
                    content = file.read_text(encoding='utf-8', errors='ignore')
                    for framework, keywords in self.FRAMEWORK_INDICATORS.items():
                        if framework not in indicators_found:
                            for keyword in keywords:
                                if keyword.lower() in content.lower():
                                    frameworks.append(framework)
                                    indicators_found.add(framework)
                                    break
                except Exception:
                    pass

        return list(set(frameworks))

    def _detect_architecture(self) -> str:
        """Infer application architecture pattern"""
        patterns = {
            'monolithic': ['app.py', 'application.py', 'main.py', 'Server.java', 'Program.cs'],
            'microservices': ['docker-compose', 'kubernetes', 'service/', 'services/', 'api/'],
            'serverless': ['lambda', 'function', 'serverless.yml', 'vercel.json', 'netlify.toml'],
            'mvc': ['controllers/', 'views/', 'models/', 'routes/'],
            'rest-api': ['api/', 'endpoint', 'router', '@RestController', '@Route'],
            'graphql': ['graphql', 'schema.graphql', 'ApolloServer', 'gql'],
            'event-driven': ['queue', 'kafka', 'rabbitmq', 'eventbus', 'pubsub'],
            'spa': ['build/', 'dist/', 'static/', 'index.html'],
        }

        scores = {arch: 0 for arch in patterns}
        for file in self.repo_path.rglob('*'):
            if self._should_exclude(file) or file.is_dir():
                continue
            try:
                content = file.read_text(encoding='utf-8', errors='ignore').lower()
                for arch, keywords in patterns.items():
                    for kw in keywords:
                        if kw.lower() in content:
                            scores[arch] += 1
            except Exception:
                pass

        # Also check directory structure
        dirs = [d.name for d in self.repo_path.iterdir() if d.is_dir()]
        if 'src' in dirs and 'test' in dirs:
            scores['mvc'] += 5

        best_arch = max(scores, key=scores.get)
        return best_arch if scores[best_arch] > 0 else 'hybrid'

    def _analyze_dependencies(self) -> List[Dict[str, Any]]:
        """Extract and analyze dependencies"""
        dependencies = []

        dep_files = ['package.json', 'requirements.txt', 'Pipfile', 'pyproject.toml',
                     'pom.xml', 'build.gradle', 'go.mod', 'Cargo.toml', 'composer.json',
                     'Gemfile', '*.csproj']

        for pattern in dep_files:
            for file in self.repo_path.rglob(pattern):
                if self._should_exclude(file):
                    continue
                try:
                    content = file.read_text(encoding='utf-8', errors='ignore')
                    deps = self._parse_dependency_file(file.name, content)
                    for dep in deps:
                        dep['file'] = str(file.relative_to(self.repo_path))
                        dependencies.append(dep)
                except Exception:
                    pass

        return dependencies

    def _parse_dependency_file(self, filename: str, content: str) -> List[Dict[str, Any]]:
        """Parse dependency files by type"""
        deps = []
        try:
            if filename == 'package.json':
                data = json.loads(content)
                for section in ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']:
                    if section in data:
                        for name, version in data[section].items():
                            deps.append({
                                'name': name,
                                'version': version,
                                'type': section.replace('Dependencies', '').lower() or 'runtime',
                                'ecosystem': 'npm'
                            })
            elif filename in ['requirements.txt', 'Pipfile']:
                # Simple parsing for pip requirements
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split('==') + line.split('>=') + line.split('~=')
                        name = parts[0].split('[')[0].strip()
                        version = parts[1] if len(parts) > 1 else 'unspecified'
                        deps.append({
                            'name': name,
                            'version': version,
                            'type': 'runtime',
                            'ecosystem': 'pypi'
                        })
            # Add more parsers as needed
        except Exception:
            pass
        return deps

    def _map_modules(self) -> List[Dict[str, Any]]:
        """Map code modules with complexity and risk metrics"""
        modules = []
        
        for ext, lang_files in self.LANGUAGE_EXTENSIONS.items():
            for file_extension in lang_files:
                for file in self.repo_path.rglob(f'*{file_extension}'):
                    if self._should_exclude(file):
                        continue
                    
                    try:
                        content = file.read_text(encoding='utf-8', errors='ignore')
                        rel_path = file.relative_to(self.repo_path)
                        
                        # Calculate metrics
                        lines = content.count('\n') + 1
                        # Improved regex for better forensic detection
                        # Detects Python, JS, TS, Java, Go, etc.
                        functions = len(re.findall(r'(\bdef\b|\bfunction\b|\bfunc\b|\bpublic\b|\bprivate\b|\bprotected\b)\s+\w+\s*\(', content))
                        classes = len(re.findall(r'(\bclass\b|\bstruct\b|\binterface\b|\btrait\b|\bmodule\b)\s+\w+', content))
                        imports = len(re.findall(r'^(\bimport\b|\brequire\b|\busing\b|\binclude\b|\bfrom\b\s+\S+\s+\bimport\b)', content, re.MULTILINE))
                        
                        # Calculate cyclomatic complexity approximation
                        complexity = content.count('if ') + content.count('else') + content.count('for ') + \
                                    content.count('while ') + content.count('switch') + content.count('case')
                        
                        # Risk factors
                        handles_auth = bool(re.search(r'auth|login|password|token|jwt|oauth|permission|role|access', content.lower()))
                        handles_data = bool(re.search(r'database|query|sql|insert|update|delete|save|load|fetch', content.lower()))
                        external_calls = len(re.findall(r'(fetch|axios|http|request|urllib|requests\.)', content.lower()))
                        crypto_usage = bool(re.search(r'crypto|encrypt|decrypt|hash|aes|rsa|sha', content.lower()))
                        file_io = bool(re.search(r'open\(|read_file|write_file|fs\.', content.lower()))
                        
                        # Forensic: Hardcoded Secrets Detection (Basic)
                        secrets = len(re.findall(r'(password|api_key|apikey|secret|token|password|auth|credential)\s*[:=]\s*["\'][\w\-]{8,}["\']', content.lower()))
                        
                        risk_factors = []
                        if secrets > 0:
                            risk_factors.append('hardcoded_secrets')
                        if complexity > 15:
                            risk_factors.append('high_complexity')
                        if external_calls > 5:
                            risk_factors.append('many_external_calls')
                        if handles_auth:
                            risk_factors.append('authentication_handling')
                        if handles_data:
                            risk_factors.append('data_persistence')
                        if crypto_usage:
                            risk_factors.append('cryptography')
                        if file_io:
                            risk_factors.append('file_io')
                        if imports > 20:
                            risk_factors.append('high_coupling')
                        
                        # Calculate risk score (0-100)
                        risk_score = min(100, (complexity * 2) + (external_calls * 3) + (handles_auth * 15) + 
                                        (handles_data * 10) + (crypto_usage * 20) + (file_io * 5) + (secrets * 25))
                        
                        module = {
                            'path': str(rel_path),
                            'language': ext,
                            'lines': lines,
                            'functions': functions,
                            'classes': classes,
                            'imports': imports,
                            'complexity': complexity,
                            'risk_score': round(risk_score, 2),
                            'risk_factors': risk_factors,
                            'handles_auth': handles_auth,
                            'handles_data': handles_data,
                            'external_calls': external_calls,
                            'crypto_usage': crypto_usage,
                            'file_io': file_io
                        }
                        modules.append(module)
                    except:
                        continue

        return modules

    def _assess_risks(self, modules: List[Dict[str, Any]], dependencies: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify high-risk areas and vulnerabilities"""
        risks = []
        
        # High-risk modules
        high_risk_modules = [m for m in modules if m['risk_score'] >= 50]
        for module in high_risk_modules:
            risks.append({
                'type': 'code_complexity',
                'severity': 'high' if module['risk_score'] >= 70 else 'medium',
                'module': module['path'],
                'risk_score': module['risk_score'],
                'description': f'High complexity module with risk score {module["risk_score"]}',
                'factors': module['risk_factors']
            })
        
        # Authentication modules
        auth_modules = [m for m in modules if m['handles_auth']]
        if auth_modules:
            risks.append({
                'type': 'security',
                'severity': 'critical',
                'module': auth_modules[0]['path'] if len(auth_modules) == 1 else 'multiple',
                'risk_score': 85,
                'description': f'Authentication handling detected in {len(auth_modules)} module(s) - requires rigorous security testing',
                'factors': ['authentication', 'authorization', 'credential_handling']
            })
        
        # Data persistence modules
        data_modules = [m for m in modules if m['handles_data']]
        if data_modules:
            risks.append({
                'type': 'data_integrity',
                'severity': 'high',
                'module': data_modules[0]['path'] if len(data_modules) == 1 else 'multiple',
                'risk_score': 75,
                'description': f'Database operations detected in {len(data_modules)} module(s) - critical for data integrity testing',
                'factors': ['sql_operations', 'data_persistence', 'transactions']
            })
        
        # External dependencies with vulnerabilities (placeholder - would need CVE lookup)
        risky_deps = []
        for dep in dependencies:
            if 'version' in dep and dep['version'] in ['*', 'latest', 'unstable']:
                risky_deps.append(dep['name'])
        if risky_deps:
            risks.append({
                'type': 'dependency',
                'severity': 'medium',
                'module': 'dependencies',
                'risk_score': 60,
                'description': f'Unpinned or floating dependencies detected: {", ".join(risky_deps[:5])}',
                'factors': ['version_pinning']
            })
        
        # Crypto usage
        crypto_modules = [m for m in modules if m['crypto_usage']]
        if crypto_modules:
            risks.append({
                'type': 'cryptography',
                'severity': 'high',
                'module': crypto_modules[0]['path'],
                'risk_score': 80,
                'description': f'Cryptographic operations detected - requires cryptographic review and testing',
                'factors': ['cryptography', 'encryption', 'hashing']
            })
        
        # File I/O modules
        file_io_modules = [m for m in modules if m['file_io']]
        if file_io_modules:
            risks.append({
                'type': 'io_security',
                'severity': 'medium',
                'module': file_io_modules[0]['path'],
                'risk_score': 55,
                'description': f'File system operations detected - test for path traversal, permissions, and injection',
                'factors': ['file_io', 'path_handling']
            })
        
        return risks

    def _find_entry_points(self) -> List[str]:
        """Identify application entry points"""
        entry_points = []
        
        common_patterns = {
            'python': ['main.py', 'app.py', 'manage.py', '__main__.py', 'wsgi.py', 'asgi.py'],
            'javascript': ['index.js', 'main.js', 'app.js', 'server.js', 'bin/www'],
            'java': ['Main.java', 'Application.java', 'App.java'],
            'go': ['main.go'],
            'rust': ['main.rs', 'lib.rs'],
            'dotnet': ['Program.cs', 'Startup.cs'],
        }
        
        for lang, patterns in common_patterns.items():
            for pattern in patterns:
                matches = list(self.repo_path.rglob(pattern))
                for match in matches:
                    if self._should_exclude(match):
                        continue
                    entry_points.append(str(match.relative_to(self.repo_path)))
        
        # Check package.json "main" or "scripts.start"
        for package_json in self.repo_path.rglob('package.json'):
            try:
                data = json.loads(package_json.read_text())
                if 'main' in data:
                    entry_points.append(f"{package_json.parent.name}/{data['main']}")
                if 'scripts' in data and 'start' in data['scripts']:
                    entry_points.append(f"{package_json.parent.name} (start script: {data['scripts']['start']})")
            except:
                pass
        
        return list(set(entry_points))

    def _analyze_data_flows(self, modules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Map data flows between modules"""
        data_flows = []
        
        # Find modules that import/require other modules
        imports_by_module = {}
        for module in modules:
            path = Path(module['path'])
            if path.suffix in ['.py', '.js', '.ts']:
                try:
                    content = path.read_text(encoding='utf-8', errors='ignore')
                    imports = []
                    if path.suffix == '.py':
                        imports = re.findall(r'from\s+[\w\.]+\s+import|import\s+[\w\.]+', content)
                    elif path.suffix in ['.js', '.ts']:
                        imports = re.findall(r'import\s+.*\s+from\s+[\'\"]([^\'\"]+)[\'\"]|require\([\'\"]([^\'\"]+)[\'\"]\)', content)
                    
                    if imports:
                        imports_by_module[module['path']] = imports
                except:
                    pass
        
        # Create simple dependency chains
        for module_path, imports in imports_by_module.items():
            # Forensic: limit to top items for report clarity
            import_list = list(imports)
            for imp in import_list[:3]:
                imp_str = str(imp)
                data_flows.append({
                    'source': module_path,
                    'imports': imp_str[:100],
                    'type': 'dependency'
                })
        
        return data_flows

    def _map_security_surface(self, modules: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Map security-sensitive areas"""
        security_surface = {
            'authentication': [],
            'authorization': [],
            'input_validation': [],
            'output_encoding': [],
            'session_management': [],
            'cryptography': [],
            'file_operations': [],
            'network_operations': [],
            'database_operations': [],
            'usability': [],
            'accessibility': [],
            'localization': [],
            'monitoring': [],
        }
        
        for module in modules:
            path = module['path']
            try:
                content = Path(self.repo_path / path).read_text(encoding='utf-8', errors='ignore').lower()
                
                if re.search(r'login|authenticate|jwt|session|token', content):
                    security_surface['authentication'].append(path)
                if re.search(r'permission|role|access.*control|acl', content):
                    security_surface['authorization'].append(path)
                if re.search(r'validate|sanitize|escape|strip', content):
                    security_surface['input_validation'].append(path)
                if re.search(r'encode|escape|template', content):
                    security_surface['output_encoding'].append(path)
                if re.search(r'session|cookie', content):
                    security_surface['session_management'].append(path)
                if re.search(r'encrypt|decrypt|cipher|aes|rsa|sha|md5|bcrypt', content):
                    security_surface['cryptography'].append(path)
                if re.search(r'open\(|file|path|upload', content):
                    security_surface['file_operations'].append(path)
                if re.search(r'fetch|axios|http|request|socket', content):
                    security_surface['network_operations'].append(path)
                if re.search(r'select|insert|update|delete|execute|query', content):
                    security_surface['database_operations'].append(path)
                if re.search(r'ui|view|layout|page|element|label|form', content):
                    security_surface['usability'].append(path)
                if re.search(r'aria|screen.*reader|alt=|[role=]|tabindex', content):
                    security_surface['accessibility'].append(path)
                if re.search(r'i18n|l10n|translate|locale|dateformat', content):
                    security_surface['localization'].append(path)
                if re.search(r'log|monitor|trace|telemetry|metric', content):
                    security_surface['monitoring'].append(path)
            except Exception:
                continue
        
        return security_surface

    def _identify_itgc_controls(self) -> List[str]:
        """Identify relevant IT General Controls"""
        controls = [
            "Change Management: All code changes must undergo peer review and testing",
            "Access Control: Role-based access to code repository and production systems",
            "Testing Requirements: Unit tests required for all new code; integration tests for critical paths",
            "Security Scanning: Automated SAST/DAST scans on all commits and pull requests",
            "Dependency Management: Regular vulnerability scanning of third-party dependencies",
            "Code Signing: All code commits must be signed with valid GPG keys",
            "Audit Trail: Complete git history with signed commits and traceable changes",
            "Deployment Controls: Automated deployments with rollback capabilities and approval gates",
            "Configuration Management: Infrastructure as code with version-controlled configurations",
            "Incident Response: Defined procedures for security incidents and data breaches",
        ]
        
        analysis = self.analysis
        if analysis:
            # Add specific controls based on detected tech stack
            if any(lang in analysis.languages for lang in ['python', 'javascript', 'typescript', 'java']):
                controls.append("Static Analysis: Mandatory SAST scanning with tools like SonarQube, CodeQL, or Snyk")
            
            if 'sql' in analysis.languages or analysis.security_surface.get('database_operations'):
                controls.append("Database Change Management: Schema changes via migration scripts with review and backup")
            
            if analysis.security_surface.get('authentication'):
                controls.append("Credential Management: Secrets must be stored in vaults; never in code or config")
            
            if analysis.architecture in ['microservices', 'serverless']:
                controls.append("API Security: All APIs require authentication, rate limiting, and input validation")
        
        return controls

    def generate_report(self, format: str = 'html', include_test_cases: bool = True) -> str:
        """Generate comprehensive testing strategy report"""
        if not self.analysis:
            self.analyze()
            
        if not self.analysis:
            return "Error: Analysis failed"

        if format == 'html':
            return self._generate_html_report(self.analysis, include_test_cases)
        elif format == 'md':
            return self._generate_markdown_report(include_test_cases)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def _generate_html_report(self, analysis: CodebaseAnalysis, include_test_cases: bool) -> str:
        """Generate the HTML report using internal analysis results"""
        # Ensure analysis is not None
        if not analysis:
            return "<html><body><h1>Error: Analysis results missing</h1></body></html>"
            
        # Improved type safety for f-string indexing
        risk_list = list(analysis.risk_assessment)
        risk_entries = risk_list[:15]
        entry_list = list(analysis.entry_points)
        top_entries = entry_list[:5]
        lang_keys = list(analysis.languages.keys())
        frame_list = list(analysis.frameworks)
        dep_list = list(analysis.dependencies)
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QA Architecture Auditor - Strategy Report</title>
    <style>
        body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; line-height: 1.6; color: #1a1a1a; max-width: 1200px; margin: 0 auto; padding: 2rem; background: #f8fafc; }}
        h1, h2, h3 {{ color: #0f172a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.5rem; }}
        .header {{ background: #1e293b; color: white; padding: 2rem; border-radius: 8px; margin-bottom: 2rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
        .header h1 {{ color: #38bdf8; border: none; margin: 0; }}
        .risk-critical {{ background: #fecaca; color: #991b1b; font-weight: bold; padding: 2px 6px; border-radius: 4px; }}
        .risk-high {{ background: #fed7aa; color: #9a3412; font-weight: bold; padding: 2px 6px; border-radius: 4px; }}
        .risk-medium {{ background: #fef08a; color: #854d0e; padding: 2px 6px; border-radius: 4px; }}
        .risk-low {{ background: #dcfce7; color: #166534; padding: 2px 6px; border-radius: 4px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1); }}
        th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
        th {{ background: #f1f5f9; font-weight: 600; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.025em; }}
        .methodology-card {{ background: white; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem; border-left: 4px solid #3b82f6; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1); }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
        .stat-card {{ background: white; padding: 1.5rem; border-radius: 8px; text-align: center; box-shadow: 0 1px 3px 0 rgba(0,0,0,0.1); }}
        .stat-value {{ font-size: 2rem; font-weight: 800; color: #2563eb; }}
        .stat-label {{ font-size: 0.875rem; color: #64748b; text-transform: uppercase; font-weight: 600; }}
        .test-case {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; margin-top: 1rem; }}
        pre {{ background: #1e293b; color: #f8fafc; padding: 1rem; border-radius: 4px; overflow-x: auto; font-size: 0.9rem; }}
        code {{ font-family: 'Fira Code', monospace; }}
        .footer {{ margin-top: 4rem; text-align: center; color: #64748b; font-size: 0.875rem; border-top: 1px solid #e2e8f0; padding-top: 2rem; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧪 QA Architecture & Testing Strategy Report</h1>
        <p>Forensic Repository Analysis | Repository: <code>{analysis.repo_path}</code></p>
        <p>Generated: {analysis.analysis_date} | Compliance Target: {analysis.compliance_framework.upper()}</p>
    </div>

    <div class="methodology-card">
        <h2>📋 Executive Summary</h2>
        <p>This report presents a comprehensive, independent testing strategy for the analyzed codebase. The analysis identified <strong>{len(analysis.modules)}</strong> modules across <strong>{len(lang_keys)}</strong> languages with <strong>{len(frame_list)}</strong> frameworks detected. The zero-trust approach assumes <strong>0% current test coverage</strong>, requiring full test strategy development from scratch.</p>
        <p><strong>Highest Risk Areas:</strong> {risk_list[0]['description'] if risk_list else 'No critical risks identified'}</p>
        <p><strong>Architecture Pattern:</strong> <code>{analysis.architecture}</code></p>
        <p><strong>Entry Points:</strong> {', '.join(top_entries)}{'...' if len(entry_list) > 5 else ''}</p>
    </div>

    <h2>📊 Codebase Statistics</h2>
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-value">{len(analysis.modules)}</div>
            <div class="stat-label">Total Modules</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(analysis.languages)}</div>
            <div class="stat-label">Languages</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{sum(analysis.languages.values())}</div>
            <div class="stat-label">Files Analyzed</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(analysis.dependencies)}</div>
            <div class="stat-label">Dependencies</div>
        </div>
    </div>

    <h2>🗣️ Languages & Frameworks</h2>
    <table>
        <thead><tr><th>Language</th><th>File Count</th></tr></thead>
        <tbody>
            {''.join(f'<tr><td>{lang}</td><td>{count}</td></tr>' for lang, count in analysis.languages.items())}
        </tbody>
    </table>
    <p><strong>Frameworks Detected:</strong> {', '.join(analysis.frameworks) if analysis.frameworks else 'None detected'}</p>

    <h2>⚠️ Risk Assessment & Vulnerability Analysis</h2>
    <p>The following modules represent the highest risk and require the most rigorous testing focus:</p>
    <table>
        <thead><tr><th>Severity</th><th>Risk Type</th><th>Module</th><th>Risk Score</th><th>Description</th></tr></thead>
        <tbody>
            {''.join(f'''<tr>
                <td class="risk-{r['severity']}">{r['severity'].upper()}</td>
                <td>{r['type']}</td>
                <td><code>{r['module']}</code></td>
                <td>{r['risk_score']}</td>
                <td>{r['description']}</td>
            </tr>''' for r in risk_entries)}
        </tbody>
    </table>

    <h2>🔒 Security Surface Mapping</h2>
    <table>
        <thead><tr><th>Security Domain</th><th>Affected Modules</th></tr></thead>
        <tbody>
            {''.join(f'<tr><td>{domain}</td><td>{len(modules) if modules else 0} modules</td></tr>' for domain, modules in analysis.security_surface.items())}
        </tbody>
    </table>

    <h2>🧩 Testing Methodology Matrix</h2>
    <p>Below is the exhaustive testing strategy addressing every methodology requested. Each includes independent baseline definition, vulnerability assessment, and from-scratch test cases.</p>

    {self._generate_methodology_sections_html(analysis, include_test_cases)}

    <h2>🛠️ Tooling Recommendations</h2>
    <div class="tool-recommendation">
        <ul>
            {self._generate_tool_recommendations(analysis)}
        </ul>
    </div>

    <h2>🏛️ IT General Controls (ITGC) Compliance</h2>
    <p>The following controls are essential for audit readiness and system transition:</p>
    <ul class="itgc-list">
        {''.join(f'<li>{control}</li>' for control in analysis.itgc_controls)}
    </ul>

    <h2>📦 Dependencies Analysis</h2>
    <p>Total dependencies: <strong>{len(dep_list)}</strong></p>
    <table><thead><tr><th>Package</th><th>Version</th><th>Type</th><th>Ecosystem</th></tr></thead><tbody>
    {''.join(f'<tr><td>{d["name"]}</td><td>{d.get("version", "N/A")}</td><td>{d.get("type", "runtime")}</td><td>{d.get("ecosystem", "unknown")}</td></tr>' 
             for d in dep_list[:30])}
    </tbody></table>

    <div class="footer">
        <p><strong>QA Architecture Auditor</strong> | Zero-Trust Policy Enforced | Generated by independent forensic analysis</p>
        <p>This report was generated assuming <strong>no existing tests</strong>. All test cases must be implemented from scratch.</p>
    </div>
</body>
</html>'''

        return html

    def _generate_methodology_sections_html(self, analysis: CodebaseAnalysis, include_test_cases: bool) -> str:
        """Generate all methodology sections"""
        methodologies = self._get_methodology_definitions()
        sections = []
        
        for meth_key, meth in methodologies.items():
            section = f'''
            <div class="methodology-card">
                <h3>{meth['icon']} {meth['name']}</h3>
                <p><strong>Independent Baseline:</strong> {meth['baseline_definition']}</p>
                <p><strong>Vulnerability & Risk Assessment:</strong> {self._assess_methodology_risk(analysis, meth_key)}</p>
                <p><strong>Strategy:</strong> {meth['strategy']}</p>'''
            
            if include_test_cases:
                section += f'''
                <h4>From-Scratch Test Cases</h4>
                <div class="test-cases">'''
                for i, test_case in enumerate(meth['test_cases'](analysis), 1):
                    section += f'''
                <div class="test-case">
                    <strong>Test Case {i}:</strong> {test_case['title']}
                    <pre><code>{test_case['example']}</code></pre>
                    <p><em>Validation:</em> {test_case['validation']}</p>
                </div>'''
                section += '</div>'
            
            section += '</div>'
            sections.append(section)
        
        return '\n'.join(sections)

    def _get_methodology_definitions(self) -> Dict[str, Any]:
        """Get comprehensive methodology definitions with test case generators"""
        return {
            'black_box': {
                'name': 'Black Box Testing',
                'icon': '🔲',
                'baseline_definition': 'Test functionality without internal code knowledge, treating the application as a black box with inputs and outputs.',
                'strategy': 'Equivalence partitioning, boundary value analysis, decision table testing based solely on requirements and API contracts.',
                'test_cases': self._generate_black_box_cases
            },
            'white_box': {
                'name': 'White Box Testing',
                'icon': '⚪',
                'baseline_definition': 'Utilize internal code structures, paths, and logic to design tests that achieve coverage of statements, branches, and paths.',
                'strategy': 'Statement coverage, branch coverage, path coverage, condition coverage. All public functions and critical logic must have unit tests.',
                'test_cases': self._generate_white_box_cases
            },
            'manual': {
                'name': 'Manual Testing',
                'icon': '👤',
                'baseline_definition': 'Human-executed tests requiring intuition, exploratory thinking, and usability judgment that cannot be fully automated.',
                'strategy': 'Exploratory testing sessions, usability walkthroughs, ad-hoc scenario validation, cross-browser compatibility checks.',
                'test_cases': self._generate_manual_cases
            },
            'automated': {
                'name': 'Automated Testing',
                'icon': '🤖',
                'baseline_definition': 'Scripted tests executed by CI/CD pipelines without human intervention, providing rapid feedback on code changes.',
                'strategy': 'Unit tests, integration tests, API tests, and E2E tests must be automated and run on every commit/PR.',
                'test_cases': self._generate_automated_cases
            },
            'unit': {
                'name': 'Unit Testing',
                'icon': '🔬',
                'baseline_definition': 'Test individual functions, methods, or classes in isolation with mocked dependencies.',
                'strategy': 'Achieve >80% code coverage. Every public function must have tests for happy path, edge cases, and error conditions.',
                'test_cases': self._generate_unit_cases
            },
            'integration': {
                'name': 'Integration Testing',
                'icon': '🔗',
                'baseline_definition': 'Validate interactions and data flow between modules, services, or external systems.',
                'strategy': 'Test module interfaces, API contracts, database interactions, and third-party service integrations with realistic test data.',
                'test_cases': self._generate_integration_cases
            },
            'system': {
                'name': 'System Testing',
                'icon': '🖥️',
                'baseline_definition': 'Validate the complete, integrated application environment end-to-end.',
                'strategy': 'Test the fully deployed system with realistic infrastructure, covering all hardware, software, and network components.',
                'test_cases': self._generate_system_cases
            },
            'functional': {
                'name': 'Functional Testing',
                'icon': '✅',
                'baseline_definition': 'Verify that business logic and requirements are correctly implemented.',
                'strategy': 'Map requirements to test cases. Every user story and acceptance criterion must have validated test scenarios.',
                'test_cases': self._generate_functional_cases
            },
            'smoke': {
                'name': 'Smoke Testing',
                'icon': '💨',
                'baseline_definition': 'Verify critical path functionality after a build to determine if the build is stable enough for further testing.',
                'strategy': 'Define sanity checklist covering core user journeys. Must pass before any QA or deployment.',
                'test_cases': self._generate_smoke_cases
            },
            'sanity': {
                'name': 'Sanity Testing',
                'icon': '🧘',
                'baseline_definition': 'Focused checks on specific functionality after recent code changes to ensure stability.',
                'strategy': 'When a bug is fixed or feature added, test that specific area and closely related functionality.',
                'test_cases': self._generate_sanity_cases
            },
            'e2e': {
                'name': 'End-to-End (E2E) Testing',
                'icon': '🔄',
                'baseline_definition': 'Test complete user workflows from initiation to database commit, simulating real user behavior.',
                'strategy': 'Automated browser tests for core user journeys using Playwright, Cypress, or Selenium.',
                'test_cases': self._generate_e2e_cases
            },
            'regression': {
                'name': 'Regression Testing',
                'icon': '🔙',
                'baseline_definition': 'Ensure new changes do not break existing features.',
                'strategy': 'Full test suite run on every release candidate. Automated regression suite must cover all critical paths.',
                'test_cases': self._generate_regression_cases
            },
            'api': {
                'name': 'API Testing',
                'icon': '🔌',
                'baseline_definition': 'Validate endpoints, request/response formats, status codes, headers, and error handling.',
                'strategy': 'Test all REST/GraphQL endpoints with varied inputs, authentication scenarios, and edge cases. Validate schemas.',
                'test_cases': self._generate_api_cases
            },
            'database': {
                'name': 'Database/Data Integrity Testing',
                'icon': '💾',
                'baseline_definition': 'Ensure data is stored, retrieved, and migrated accurately without loss, corruption, or unauthorized access.',
                'strategy': 'Test CRUD operations, transactions, constraints, data validation, backup/restore, and migration scripts.',
                'test_cases': self._generate_database_cases
            },
            'performance': {
                'name': 'Performance Testing',
                'icon': '⚡',
                'baseline_definition': 'Evaluate speed, stability, load capacity, stress limits, and volume handling based on architecture.',
                'strategy': 'Load testing (expected traffic), stress testing (breaking point), endurance testing (sustained load), and spike testing.',
                'test_cases': self._generate_performance_cases
            },
            'security': {
                'name': 'Security Testing',
                'icon': '🔐',
                'baseline_definition': 'Identify vulnerabilities including SAST (static), DAST (dynamic), and SCA (software composition analysis).',
                'strategy': 'Automated scanning, penetration testing, code reviews for OWASP Top 10, dependency vulnerability checks, and threat modeling.',
                'test_cases': self._generate_security_cases
            },
            'usability': {
                'name': 'Usability Testing',
                'icon': '👁️',
                'baseline_definition': 'Evaluate user experience flows, interface clarity, and interaction design.',
                'strategy': 'User testing sessions, heuristic evaluation, accessibility checks, and cognitive walkthroughs.',
                'test_cases': self._generate_usability_cases
            },
            'compatibility': {
                'name': 'Compatibility Testing',
                'icon': '🔀',
                'baseline_definition': 'Test across different devices, browsers, operating systems, and network conditions.',
                'strategy': 'Cross-browser testing matrix, responsive design validation, mobile device testing, and legacy support.',
                'test_cases': self._generate_compatibility_cases
            },
            'accessibility': {
                'name': 'Accessibility Testing',
                'icon': '♿',
                'baseline_definition': 'Ensure compliance with WCAG 2.1/2.2 standards for people with disabilities.',
                'strategy': 'Automated accessibility scanners, screen reader testing, keyboard navigation checks, and color contrast validation.',
                'test_cases': self._generate_accessibility_cases
            },
            'localization': {
                'name': 'Localization/Internationalization Testing',
                'icon': '🌍',
                'baseline_definition': 'Validate readiness for multiple languages, regional formats, and cultural adaptations.',
                'strategy': 'Test text expansion, date/time/number formats, RTL languages, character encoding, and localized content.',
                'test_cases': self._generate_localization_cases
            },
            'acceptance': {
                'name': 'Acceptance Testing (UAT)',
                'icon': '📝',
                'baseline_definition': 'Ensure the software meets end-user business needs and requirements.',
                'strategy': 'Business user validation against acceptance criteria, UAT sign-off process, production-like environment testing.',
                'test_cases': self._generate_acceptance_cases
            },
            'exploratory': {
                'name': 'Exploratory Testing',
                'icon': '🧭',
                'baseline_definition': 'Unscripted testing to discover complex edge cases, hidden defects, and unexpected behaviors.',
                'strategy': 'Charter-based exploration sessions, session-based test management, heuristic-based testing, and bug bashes.',
                'test_cases': self._generate_exploratory_cases
            },
        }

    def _assess_methodology_risk(self, analysis: CodebaseAnalysis, methodology: str) -> str:
        """Generate risk assessment specific to each methodology"""
        # Use .get() for keys that might be missing in older saved analysis
        auth_len = len(analysis.security_surface.get('authentication', []))
        db_len = len(analysis.security_surface.get('database_operations', []))
        usability_len = len(analysis.security_surface.get('usability', []))
        session_len = len(analysis.security_surface.get('session_management', []))
        input_len = len(analysis.security_surface.get('input_validation', []))
        module_len = len(analysis.modules)
        risk_len = len(analysis.risk_assessment)
        entry_len = len(analysis.entry_points)
        
        assessments = {
            'black_box': f"The {entry_len} entry points represent the primary black-box testing surface. Focus on {auth_len} authentication modules and {db_len} database interaction points.",
            'white_box': f"With {module_len} modules requiring coverage, white-box testing must achieve >80% statement coverage. {len([m for m in analysis.modules if m['complexity'] > 15])} modules have high complexity (>15) and require path coverage analysis.",
            'manual': f"Manual testing is essential for {usability_len} usability-sensitive modules and {risk_len} risk areas where automation cannot capture business logic nuances.",
            'automated': f"All {entry_len} entry points and {len(analysis.dependencies)} dependencies must be covered by automated CI/CD tests. Target: >1000 automated test cases.",
            'unit': f"Unit tests must cover {sum(m['functions'] for m in analysis.modules)} functions and {sum(m['classes'] for m in analysis.modules)} classes across {module_len} modules.",
            'integration': f"Integration tests must validate {len(analysis.data_flows)} dependency relationships and {db_len} database interactions.",
            'system': f"System testing must validate the complete {analysis.architecture} architecture with all {len(analysis.frameworks)} frameworks integrated.",
            'functional': f"Functional tests must cover all business logic paths. {len(analysis.security_surface['input_validation'])} modules require special input validation testing.",
            'smoke': f"Smoke tests must cover all {len(analysis.entry_points)} entry points and core workflows: {', '.join(list(analysis.entry_points)[:3])}.",
            'sanity': f"Sanity checklists must be maintained for {len(analysis.modules)} modules, with automated smoke tests for every commit.",
            'e2e': f"E2E tests must cover {len(analysis.entry_points)} user journeys: {', '.join(list(analysis.entry_points)[:3])}. All shall use realistic data and staging environments.",
            'regression': f"Regression suite must include {len(analysis.modules) * 3} minimum test cases covering all modules and their interfaces. Run on every release.",
            'api': f"API endpoints need testing. Identify via route definitions (express, django, spring, etc.). All endpoints require validation of status codes, schemas, auth, and error handling.",
            'database': f"Database integrity tests required for {len(analysis.security_surface['database_operations'])} modules with SQL operations. Test CRUD, constraints, transactions, and migrations.",
            'performance': f"Performance testing required for {len(analysis.entry_points)} entry points and {len(analysis.security_surface['database_operations'])} database-heavy modules. Load test at 2x expected traffic.",
            'security': f"{len(analysis.risk_assessment)} high-risk areas identified. All modules with auth, crypto, or external calls must undergo SAST/DAST and penetration testing.",
            'usability': f"Usability testing needed for all user-facing modules. Identify UI/UX components; test with actual users for workflow clarity.",
            'compatibility': f"Compatibility matrix required based on detected frameworks: {', '.join(analysis.frameworks)}. Test on latest 2 versions of major browsers and OSes.",
            'accessibility': f"Accessibility compliance required for all UI modules. {len(analysis.entry_points)} entry points must meet WCAG 2.1 AA standards.",
            'localization': f"Internationalization testing required if multi-language support planned. Check hardcoded strings, date/number formatting, and text expansion.",
            'acceptance': f"UAT must involve business stakeholders validating all {len(analysis.modules)} modules against requirements. Sign-off required before production.",
            'exploratory': f"Exploratory testing charters must be created for all {len(analysis.risk_assessment)} high-risk modules and {len(analysis.entry_points)} entry points."
        }
        return assessments.get(methodology, "All modules must be tested according to the defined strategy.")

    def _generate_black_box_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'Input Validation - Equivalence Partitioning',
                'example': f'''# For each API endpoint in {analysis.entry_points[0] if analysis.entry_points else 'the application'}:
# Test valid, boundary, and invalid inputs
POST /api/endpoint {{"field": "valid_value"}}  # Expect 200
POST /api/endpoint {{"field": ""}}            # Expect 400 - empty
POST /api/endpoint {{}}                      # Expect 400 - missing field''',
                'validation': 'Verify correct status codes and error messages for each partition'
            },
            {
                'title': 'Boundary Value Analysis',
                'example': '''# Test edge cases and boundaries
GET /api/users?page=0    # Expect 400 or redirect
GET /api/users?page=1    # Expect 200 - first page
GET /api/users?page=MAX  # Expect 200 or 404 - last page
GET /api/users?page=MAX+1 # Expect 404 or empty''',
                'validation': 'Boundary conditions handled gracefully without errors'
            },
            {
                'title': 'Decision Table Testing',
                'example': '''# Complex business logic combinations
# Table: Authentication + Authorization
User Authenticated + Has Permission = Access Granted 200
User Authenticated + No Permission = 403 Forbidden
No Authentication = 401 Unauthorized
Invalid Token = 401 Unauthorized''',
                'validation': 'All decision paths produce expected outcomes'
            }
        ]

    def _generate_unit_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        top_modules = list(analysis.modules)[:10]
        cases = []
        for module in top_modules:
            cases.append({
                'title': f'Unit Test: {module["path"]}',
                'example': f'# Test all {module["functions"]} functions in {module["path"]}',
                'validation': '100% function coverage for the module'
            })
        return cases

    def _generate_white_box_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        modules_sorted = sorted(list(analysis.modules), key=lambda x: x['complexity'], reverse=True)
        high_complexity = modules_sorted[:3]
        cases = []
        for module in high_complexity:
            cases.append({
                'title': f'Path Coverage: {module["path"]}',
                'example': f'''# Module: {module["path"]}
# Complexity: {module["complexity"]}
# Logic Path analysis required for forensic validation''',
                'validation': 'All logical paths verified'
            })
        return cases


    def _generate_manual_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'Exploratory Testing Session',
                'example': f'''# Charter: Investigate user workflows in {analysis.entry_points[0] if analysis.entry_points else 'the application'}
# Duration: 90 minutes
# Notes: Document all unexpected behaviors, edge cases, and UX issues
# Focus: Login flow → main feature → logout, error recovery, data validation''',
                'validation': 'Session notes document at least 5 new insights or issues'
            },
            {
                'title': 'Usability Heuristic Evaluation',
                'example': '''# Review against Nielsen's 10 heuristics:
# 1. Visibility of system status
# 2. Match between system and real world
# 3. User control and freedom
# 4. Consistency and standards
# 5. Error prevention
# 6. Recognition rather than recall
# 7. Flexibility and efficiency of use
# 8. Aesthetic and minimalist design
# 9. Help users recognize, diagnose, recover from errors
# 10. Help and documentation''',
                'validation': 'Document all heuristic violations with severity ratings'
            }
        ]

    def _generate_automated_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'CI Pipeline Integration',
                'example': '''# .github/workflows/ci.yml (GitHub Actions example)
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up environment
        run: npm ci / pip install -r requirements.txt
      - name: Run unit tests
        run: npm test / pytest --cov --cov-report=xml
      - name: Run integration tests
        run: npm run test:integration / pytest tests/integration/
      - name: Upload coverage
        uses: codecov/codecov-action@v3''',
                'validation': 'Pipeline passes with >80% coverage and zero test failures'
            }
        ]

    def _generate_unit_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        modules_to_test = analysis.modules[:5]
        cases = []
        for module in modules_to_test:
            cases.append({
                'title': f'Unit Test: {module["path"]}',
                'example': f'''# Test file: test_{Path(module['path']).stem}.py
import pytest
from {module['path'].replace('/', '.').replace('.py', '')} import function_name

def test_happy_path():
    # Arrange
    input = "valid_input"
    expected = "expected_output"
    # Act
    result = function_name(input)
    # Assert
    assert result == expected

def test_edge_case_boundary():
    # Test boundary conditions
    result = function_name(boundary_input)
    assert result is not None

def test_error_handling():
    # Test invalid inputs raise appropriate exceptions
    with pytest.raises(ValueError):
        function_name(invalid_input)''',
                'validation': f'Tests cover happy path, edge cases, and error handling for {module["path"]}'
            })
        return cases

    def _generate_integration_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        integration_points = [m for m in analysis.modules if m['imports'] > 0][:3]
        cases = []
        for point in integration_points:
            cases.append({
                'title': f'Integration: {point["path"]} with dependencies',
                'example': f'''# Test module integration
# Module: {point['path']}
# Dependencies: {point['imports']} imports

def test_database_integration():
    # Test actual database (or realistic test double)
    # Verify data persistence and retrieval
    record = create_test_record()
    fetched = get_record(record.id)
    assert fetched == record

def test_external_api_integration():
    # Mock external service responses
    # Verify request/response handling
    response = call_external_api(test_data)
    assert response.status == 200
    assert validate_schema(response.data)''',
                'validation': 'Integration validated with realistic test environment'
            })
        return cases

    def _generate_system_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'Full System Deployment Test',
                'example': f'''# Deploy complete {analysis.architecture} system to staging
# Verify all components start correctly
docker-compose up -d  # or equivalent
# Check all services are healthy
curl http://localhost:health
# Run smoke tests against full system
pytest tests/e2e/smoke_test.py
# Verify logs show no errors
grep -i error logs/application.log''',
                'validation': 'Staging environment stable, all health checks pass'
            }
        ]

    def _generate_functional_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'Business Logic Validation',
                'example': '''# For each business requirement:
# Requirement: "User can only cancel orders within 24h of placement"
def test_cancel_order_within_24h():
    order = create_order(hours_ago=2)
    result = cancel_order(order.id)
    assert result.success == True

def test_cancel_order_after_24h():
    order = create_order(hours_ago=25)
    result = cancel_order(order.id)
    assert result.success == False
    assert "24 hours" in result.error_message''',
                'validation': 'All business rules enforced correctly'
            }
        ]

    def _generate_smoke_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        entry = analysis.entry_points[0] if analysis.entry_points else 'application'
        return [
            {
                'title': f'Smoke Test: {entry}',
                'example': f'''# 1. Start application
./start_{entry}
# 2. Health check
curl -f http://localhost:8080/health
# 3. Core API endpoint
curl -f http://localhost:8080/api/status
# 4. Database connectivity test
python -c "import db; db.connection.check()"
# 5. Critical user flow (if UI)
# Open browser, navigate to URL, login, perform main action''',
                'validation': 'All checks pass within 60 seconds'
            }
        ]

    def _generate_sanity_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'Sanity Check After Code Change',
                'example': '''# After any change to authentication module:
# 1. Login still works (valid credentials)
# 2. Invalid credentials rejected
# 3. Password reset flow functional
# 4. Session timeout works
# 5. Logout clears session
# Run only tests related to auth module''',
                'validation': 'All sanity checks pass before merge'
            }
        ]

    def _generate_e2e_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'Complete User Journey E2E',
                'example': f'''# Using Playwright/Cypress
def test_complete_user_onboarding():
    # 1. Visit application
    page.goto("https://app.example.com")
    # 2. Register new account
    page.fill("#email", "test@example.com")
    page.fill("#password", "SecurePass123")
    page.click("button[type=submit]")
    # 3. Verify email (mock or test inbox)
    # 4. Login
    page.fill("#login-email", "test@example.com")
    page.fill("#login-password", "SecurePass123")
    page.click("button:has-text('Login')")
    # 5. Perform core activity
    page.click("text=Create New Project")
    page.fill("#project-name", "Test Project")
    page.click("button:has-text('Create')")
    # 6. Verify data persisted
    assert page.locator("text=Test Project").is_visible()
    # 7. Logout
    page.click("button:has-text('Logout')")
    assert page.locator("text=Login").is_visible()''',
                'validation': 'Full workflow executes successfully from start to database commit'
            }
        ]

    def _generate_regression_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'Full Regression Suite',
                'example': '''# Run on every release candidate
pytest tests/unit/ --cov
pytest tests/integration/ --cov
pytest tests/e2e/
# Total test count: N (target >1000)
# Coverage target: >80%
# All tests must pass (0 failures)''',
                'validation': 'Zero test failures, coverage maintained or increased'
            }
        ]

    def _generate_api_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'API Endpoint Validation',
                'example': '''# For each REST endpoint:
# 1. Valid request with required fields
GET /api/users/1
assert status == 200
assert response.json().has_key('id')

# 2. Missing required fields
POST /api/users {{}}
assert status == 400
assert 'required' in response.json()['error']

# 3. Invalid data types
POST /api/users {{"age": "not_an_integer"}}
assert status == 422

# 4. Authentication required
DELETE /api/users/1
assert status in [401, 403]

# 5. Resource not found
GET /api/users/99999
assert status == 404

# 6. Rate limiting
for i in range(100):
    response = GET /api/limited
    if response.status == 429:
        break''',
                'validation': 'All endpoints validated for status codes, schemas, auth, and edge cases'
            }
        ]

    def _generate_database_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        if not analysis.security_surface['database_operations']:
            return [{'title': 'No database operations detected', 'example': 'N/A', 'validation': 'N/A'}]
        return [
            {
                'title': 'CRUD Operations',
                'example': '''# Test Create, Read, Update, Delete
def test_create_record():
    id = db.insert("test_table", data)
    assert id is not None

def test_read_record():
    record = db.select("test_table", id)
    assert record['id'] == id

def test_update_record():
    db.update("test_table", id, {{"field": "new_value"}})
    record = db.select("test_table", id)
    assert record['field'] == "new_value"

def test_delete_record():
    db.delete("test_table", id)
    record = db.select("test_table", id)
    assert record is None''',
                'validation': 'All CRUD operations work correctly with constraints'
            },
            {
                'title': 'Transaction Rollback',
                'example': '''def test_transaction_rollback():
    try:
        with db.transaction():
            db.insert("table1", data1)
            db.insert("table2", data2)  # This will fail
    except:
        pass
    # Verify first insert was rolled back
    assert db.count("table1", filter) == 0''',
                'validation': 'Failed transactions fully rollback'
            }
        ]

    def _generate_performance_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'Load Testing',
                'example': '''# Using k6 or locust
# Target: 2x expected peak traffic
import time
from locust import HttpUser, task, between

class LoadTest(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def critical_endpoint(self):
        response = self.client.get("/api/endpoint")
        assert response.status_code == 200
        assert response.elapsed < 2.0  # 2 second SLA

# Run: locust -f load_test.py --headless -u 1000 -r 100''',
                'validation': 'System handles 2x peak load with <2% error rate and <2s response time'
            },
            {
                'title': 'Stress Testing - Breaking Point',
                'example': '''# Gradually increase load until system fails
start_users = 100
max_users = 10000
step = 100
for users in range(start_users, max_users, step):
    launch_test(users)
    if error_rate > 5% or response_time > 10s:
        log("Breaking point found at {users} concurrent users")
        break''',
                'validation': 'Identify system limits and ensure graceful degradation'
            }
        ]

    def _generate_security_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'OWASP Top 10 Validation',
                'example': '''# A01:2021 - Broken Access Control
def test_unauthorized_access():
    # User A attempts to access User B's data
    response = client.get("/api/user/2/data", headers=auth_user_1)
    assert response.status_code == 403

# A02:2021 - Cryptographic Failures
# Verify no sensitive data in logs, traffic encrypted (HTTPS)
def test_https_enforced():
    response = client.get("/api/data", allow_redirects=False)
    assert response.status_code == 301 or response.url.startswith("https://")

# A03:2021 - Injection
def test_sql_injection():
    malicious_input = "'; DROP TABLE users; --"
    response = client.get(f"/api/search?q={malicious_input}")
    assert "error" in response.json() or response.status_code == 400
    # Verify database still intact''',
                'validation': 'All OWASP Top 10 vulnerabilities tested and mitigated'
            },
            {
                'title': 'SAST/DAST Scanning',
                'example': '''# Static Analysis (SAST)
snyk test --all-projects
sem grep --config=p/security-audit
codeql database create
codeql query run --sarif-category owasp

# Dynamic Analysis (DAST)
# Run OWASP ZAP or Burp Suite against deployed staging
zap-cli quick-scan --spider --ajax https://staging.example.com
# Review findings and remediate critical/high''',
                'validation': 'Zero critical/high vulnerabilities in scan reports'
            }
        ]

    def _generate_usability_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {
                'title': 'User Workflow Validation',
                'example': '''# Conduct user testing sessions (5-10 participants)
# Charter: Complete primary user tasks without assistance
tasks = [
    "Create a new account",
    "Complete first transaction",
    "Find help documentation",
    "Change account settings"
]
for task in tasks:
    observe_user_attempting(task)
    record:
    - Time to completion
    - Number of errors/confusions
    - Success rate
    - Subjective satisfaction (1-5)
# Target: >90% success rate, <2 minute average per task''',
                'validation': 'User testing shows >90% task completion without assistance'
            }
        ]

    def _generate_compatibility_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        """Generate tooling recommendations based on analysis"""
        recommendations = []
        
        # Python
        if 'python' in analysis.languages:
            recommendations.append("pytest + pytest-cov for unit/integration, Coverage.py for reports")
            recommendations.append("locust or k6 for performance testing")
            recommendations.append("bandit (SAST), safety (SCA), OWASP ZAP (DAST)")
        
        # JavaScript/TypeScript
        if any(lang in analysis.languages for lang in ['javascript', 'typescript']):
            recommendations.append("Jest or Vitest for unit/integration testing")
            recommendations.append("Cypress or Playwright for E2E")
            recommendations.append("ESLint security plugins, npm audit for SCA")
        
        # Java
        if 'java' in analysis.languages:
            recommendations.append("JUnit 5 + Mockito for unit tests")
            recommendations.append("Spring Boot Test or RestAssured for API testing")
            recommendations.append("SonarQube for static analysis, OWASP Dependency Check")
        
        # Go
        if 'go' in analysis.languages:
            recommendations.append("Go test standard library with table-driven tests")
            recommendations.append("go vet, staticcheck for static analysis")
        
        # General CI/CD
        recommendations.append("CI/CD: GitHub Actions, GitLab CI, or Jenkins")
        recommendations.append("Code coverage: Codecov or Coveralls")
        recommendations.append("Containerization: Docker for consistent test environments")
        
        return recommendations

    def _generate_markdown_report(self, include_test_cases: bool) -> str:
        """Generate a markdown version of the report"""
        analysis = self.analysis
        if not analysis:
            return "# Error: Analysis results missing"
            
        risk_list = list(analysis.risk_assessment)
        md = [
            f"# QA Architecture & Testing Strategy Report",
            f"**Repository:** {analysis.repo_path}",
            f"**Date:** {getattr(analysis, 'analysis_date', '2026-03-13')}",
            "",
            "## Executive Summary",
            f"Detected {len(analysis.modules)} modules across {len(analysis.languages)} languages.",
            f"**Architecture:** {analysis.architecture}",
            "",
            "## Risk Assessment",
            "| Severity | Type | Module | Risk Score | Description |",
            "|----------|------|--------|------------|-------------|",
        ]
        
        for r in risk_list[:15]:
            md.append(f"| {r['severity'].upper()} | {r['type']} | `{r['module']}` | {r['risk_score']} | {r['description']} |")
            
        md.append("\n## Testing Methodologies")
        methodologies = self._get_methodology_definitions()
        for key, meth in methodologies.items():
            md.append(f"### {meth['icon']} {meth['name']}")
            md.append(f"**Baseline:** {meth['baseline_definition']}")
            md.append(f"**Strategy:** {meth['strategy']}")
            if include_test_cases:
                md.append("\n#### Test Cases")
                for i, test in enumerate(meth['test_cases'](analysis), 1):
                    md.append(f"{i}. **{test['title']}**")
                    md.append(f"   ```\n   {test['example']}\n   ```")
                    md.append(f"   *Validation:* {test['validation']}\n")
        
        md.append("## ITGC Controls")
        for control in getattr(analysis, 'itgc_controls', []):
            md.append(f"- {control}")
            
        return "\n".join(md)

    def _generate_tool_recommendations(self, analysis: CodebaseAnalysis) -> str:
        """Generate tool recommendations list items for HTML"""
        recs = self._generate_compatibility_cases(analysis)
        return "\n".join([f"<li>{r}</li>" for r in recs])

    def _generate_compatibility_recs(self, analysis: CodebaseAnalysis) -> List[str]:
        """Generate tooling recommendations based on analysis"""
        recommendations = []
        
        # Python
        if 'python' in analysis.languages:
            recommendations.append("pytest + pytest-cov for unit/integration, Coverage.py for reports")
            recommendations.append("locust or k6 for performance testing")
            recommendations.append("bandit (SAST), safety (SCA), OWASP ZAP (DAST)")
        
        # JavaScript/TypeScript
        if any(lang in analysis.languages for lang in ['javascript', 'typescript']):
            recommendations.append("Jest or Vitest for unit/integration testing")
            recommendations.append("Cypress or Playwright for E2E")
            recommendations.append("ESLint security plugins, npm audit for SCA")
        
        # Java
        if 'java' in analysis.languages:
            recommendations.append("JUnit 5 + Mockito for unit tests")
            recommendations.append("Spring Boot Test or RestAssured for API testing")
            recommendations.append("SonarQube for static analysis, OWASP Dependency Check")
        
        # Go
        if 'go' in analysis.languages:
            recommendations.append("Go test standard library with table-driven tests")
            recommendations.append("go vet, staticcheck for static analysis")
        
        # General CI/CD
        recommendations.append("CI/CD: GitHub Actions, GitLab CI, or Jenkins")
        recommendations.append("Code coverage: Codecov or Coveralls")
        recommendations.append("Containerization: Docker for consistent test environments")
        
        return recommendations

    def _generate_compatibility_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        """Generate compatibility test cases as dicts for consistency"""
        recommendations = self._generate_compatibility_recs(analysis)
        return [{'title': 'Compatibility Check', 'example': r, 'validation': 'Tooling verified and functional'} for r in recommendations]

        return recommendations

    def _generate_manual_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Critical Flow Walkthrough', 'example': 'Manual execution of top 3 workflows', 'validation': 'All steps verified by QA architect'}]

    def _generate_automated_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'CI Regression Suite', 'example': 'Automated run of all high-risk module tests', 'validation': 'All tests pass in CI environment'}]

    def _generate_unit_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Function Level Validation', 'example': 'Unit tests for core logic', 'validation': '100% logic coverage'}]

    def _generate_integration_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [
            {'title': 'Module Interface Test', 'example': f'Verify data flow between {list(analysis.modules)[0]["path"] if analysis.modules else "modules"}', 'validation': 'Correct data handover verified'},
            {'title': 'Database Integration', 'example': 'Verify database operations handle constraints correctly', 'validation': 'DB state remains consistent after operations'}
        ]

    def _generate_system_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Full Architecture Validation', 'example': f'Validate {analysis.architecture} flow', 'validation': 'System components work in harmony'}]

    def _generate_functional_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Requirement Verification', 'example': 'Test feature against business requirements', 'validation': 'Feature behavior matches requirement specification'}]

    def _generate_smoke_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Deployment Health Check', 'example': 'Verify all entry points return 200', 'validation': 'Application is up and reachable'}]

    def _generate_sanity_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Scope-limited Regression', 'example': f'Verify fix in {list(analysis.risk_assessment)[0]["module"] if analysis.risk_assessment else "affected module"}', 'validation': 'Fix works without breaking immediate surroundings'}]

    def _generate_e2e_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'User Journey Validation', 'example': 'Complete end-to-end checkout/sign-up journey', 'validation': 'Goal achieved from start to finish'}]

    def _generate_regression_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Total Impact Analysis', 'example': 'Full suite execution on release branch', 'validation': 'No regressions detected across any features'}]

    def _generate_api_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Endpoint Schema Validation', 'example': 'Verify JSON response matches expected schema', 'validation': 'Correct headers and payload'}]

    def _generate_database_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Persistence Layer Integrity', 'example': 'Test concurrent writes to high-traffic modules', 'validation': 'No data corruption or deadlocks'}]

    def _generate_performance_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Stress Test Entry Points', 'example': 'Simulated load on main entry points', 'validation': 'Response time < 500ms at 100 concurrent users'}]

    def _generate_security_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Injection Vulnerability Scan', 'example': 'Test all input fields for common injection patterns', 'validation': 'Zero successful injections detected'}]

    def _generate_usability_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'UI Feedback Loop', 'example': 'Observe user navigating core features', 'validation': 'Zero navigation friction reported'}]

    def _generate_accessibility_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'WCAG 2.1 Compliance', 'example': 'Run Axe-core on main entry points', 'validation': 'Zero critical accessibility violations'}]

    def _generate_localization_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'RTL Layout Check', 'example': 'Switch app to Arabic and verify no layout overlap', 'validation': 'Correct mirroring and text rendering'}]

    def _generate_acceptance_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'User Persona Walkthrough', 'example': 'Admin user creates and deletes project', 'validation': 'All business constraints respected'}]

    def _generate_exploratory_cases(self, analysis: CodebaseAnalysis) -> List[Dict[str, Any]]:
        return [{'title': 'Chaotic Input Session', 'example': 'Rapid input and unexpected navigation sequences', 'validation': 'System remains stable without crashes or data corruption'}]

def main():
    parser = argparse.ArgumentParser(description='Perform forensic QA architecture analysis and generate testing strategy report.')
    parser.add_argument('--repo', '-r', required=True, help='Repository path or git URL')
    parser.add_argument('--output', '-o', default='qa-report.html', help='Output file path')
    parser.add_argument('--format', '-f', choices=['html', 'md'], default='html', help='Output format')
    parser.add_argument('--include-test-cases', action='store_true', default=True, help='Include detailed test cases')
    parser.add_argument('--exclude', '-e', default='node_modules,.git,__pycache__,.venv,venv,build,dist,target',
                       help='Comma-separated directories to exclude')
    parser.add_argument('--max-depth', type=int, default=10, help='Maximum directory traversal depth')
    parser.add_argument('--security-scan', action='store_true', help='Perform security vulnerability scanning')
    parser.add_argument('--compliance', choices=['itgc', 'soc2', 'iso27001', 'hipaa', 'gdpr'], default='itgc',
                       help='Compliance framework to target')
    
    args = parser.parse_args()
    
    exclude_dirs = args.exclude.split(',') if args.exclude else []
    auditor = QAAuditor(args.repo, exclude_dirs=exclude_dirs)
    analysis = auditor.analyze()
    
    # Add metadata
    analysis.analysis_date = '2026-03-13'
    analysis.compliance_framework = args.compliance
    
    report = auditor.generate_report(format=args.format, include_test_cases=args.include_test_cases)
    
    output_path = Path(args.output)
    output_path.write_text(report, encoding='utf-8')
    print(f"✅ Report generated: {output_path.resolve()}")

    # Fix: also generate markdown version if specifically helpful
    if args.format == 'html':
        md_report = auditor.generate_report(format='md', include_test_cases=args.include_test_cases)
        md_path = output_path.with_suffix('.md')
        md_path.write_text(md_report, encoding='utf-8')
        print(f"✅ Markdown version also generated: {md_path.resolve()}")

if __name__ == '__main__':
    main()
