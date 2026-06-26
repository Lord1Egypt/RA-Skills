"""
ClawGuard Code Analyzer
Scans skill files for dangerous patterns using regex and AST analysis.
"""

import ast
import re
import os
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

from patterns import (
    ALL_PATTERNS,
    Pattern,
    extract_urls,
    is_safe_domain,
    SEVERITY_WEIGHTS,
)

@dataclass
class Finding:
    """Security finding"""
    file_path: str
    line_number: int
    pattern_name: str
    category: str
    severity: str
    weight: int
    description: str
    code_snippet: str

@dataclass
class AnalysisResult:
    """Complete analysis result"""
    findings: List[Finding]
    urls: List[Tuple[str, bool]]  # (url, is_safe)
    risk_score: int
    risk_level: str  # SAFE, CAUTION, DANGEROUS
    files_scanned: int
    lines_scanned: int

class CodeAnalyzer:
    """Main code analyzer"""
    
    def __init__(self, skill_path: Path):
        self.skill_path = Path(skill_path)
        self.findings: List[Finding] = []
        self.urls: List[str] = []
        self.files_scanned = 0
        self.lines_scanned = 0
    
    def analyze(self) -> AnalysisResult:
        """Analyze all files in skill directory"""
        self.findings = []
        self.urls = []
        self.files_scanned = 0
        self.lines_scanned = 0
        
        # Scan all text files
        for file_path in self._get_scannable_files():
            self._analyze_file(file_path)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score()
        risk_level = self._get_risk_level(risk_score)
        
        # Process URLs
        url_list = [(url, is_safe_domain(url)) for url in set(self.urls)]
        
        return AnalysisResult(
            findings=self.findings,
            urls=url_list,
            risk_score=risk_score,
            risk_level=risk_level,
            files_scanned=self.files_scanned,
            lines_scanned=self.lines_scanned,
        )
    
    def _get_scannable_files(self) -> List[Path]:
        """Get all scannable files (code, scripts, configs)"""
        extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx',
            '.sh', '.bash', '.zsh',
            '.yaml', '.yml', '.json',
            '.md', '.txt',
        }
        
        files = []
        for root, dirs, filenames in os.walk(self.skill_path):
            # Skip common ignore directories
            dirs[:] = [d for d in dirs if d not in {
                'node_modules', '.git', '__pycache__', 
                '.venv', 'venv', 'dist', 'build'
            }]
            
            for filename in filenames:
                file_path = Path(root) / filename
                
                # Check extension or no extension (scripts)
                if file_path.suffix in extensions or not file_path.suffix:
                    files.append(file_path)
                
                # Check for hidden files
                if filename.startswith('.') and filename not in {'.gitignore', '.npmignore'}:
                    self._add_finding(
                        file_path=file_path,
                        line_number=0,
                        pattern_name="hidden_file",
                        category="hidden_file",
                        severity="LOW",
                        weight=10,
                        description=f"Hidden file detected: {filename}",
                        code_snippet="",
                    )
        
        return files
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single file"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            # Skip unreadable files
            return
        
        self.files_scanned += 1
        lines = content.split('\n')
        self.lines_scanned += len(lines)
        
        # Extract URLs
        self.urls.extend(extract_urls(content))
        
        # Python AST analysis
        if file_path.suffix == '.py':
            self._analyze_python_ast(file_path, content)
        
        # Regex pattern matching (all files)
        self._analyze_patterns(file_path, lines)
    
    def _analyze_python_ast(self, file_path: Path, content: str):
        """Python-specific AST analysis"""
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                # Detect eval() calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == 'eval':
                        self._add_finding(
                            file_path=file_path,
                            line_number=node.lineno,
                            pattern_name="eval_call_ast",
                            category="obfuscation",
                            severity="HIGH",
                            weight=15,
                            description="eval() call detected via AST",
                            code_snippet=self._get_line(content, node.lineno),
                        )
                
                # Detect exec() calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id == 'exec':
                        self._add_finding(
                            file_path=file_path,
                            line_number=node.lineno,
                            pattern_name="exec_call_ast",
                            category="obfuscation",
                            severity="HIGH",
                            weight=15,
                            description="exec() call detected via AST",
                            code_snippet=self._get_line(content, node.lineno),
                        )
        
        except SyntaxError:
            # Skip files with syntax errors
            pass
    
    def _analyze_patterns(self, file_path: Path, lines: List[str]):
        """Regex pattern matching on file lines"""
        for line_num, line in enumerate(lines, start=1):
            for pattern in ALL_PATTERNS:
                if re.search(pattern.regex, line, re.IGNORECASE):
                    # Special handling for hidden file pattern (filename only)
                    if pattern.name == "dotfile":
                        continue  # Already handled in _get_scannable_files
                    
                    self._add_finding(
                        file_path=file_path,
                        line_number=line_num,
                        pattern_name=pattern.name,
                        category=pattern.category,
                        severity=pattern.severity,
                        weight=pattern.weight,
                        description=pattern.description,
                        code_snippet=line.strip(),
                    )
    
    def _add_finding(
        self,
        file_path: Path,
        line_number: int,
        pattern_name: str,
        category: str,
        severity: str,
        weight: int,
        description: str,
        code_snippet: str,
    ):
        """Add a finding to results"""
        relative_path = file_path.relative_to(self.skill_path)
        
        self.findings.append(Finding(
            file_path=str(relative_path),
            line_number=line_number,
            pattern_name=pattern_name,
            category=category,
            severity=severity,
            weight=weight,
            description=description,
            code_snippet=code_snippet,
        ))
    
    def _calculate_risk_score(self) -> int:
        """Calculate risk score (0-100)"""
        if not self.findings:
            return 0
        
        # Sum weighted scores
        total_weight = sum(
            f.weight * SEVERITY_WEIGHTS[f.severity]
            for f in self.findings
        )
        
        # Cap at 100
        return min(100, int(total_weight))
    
    def _get_risk_level(self, score: int) -> str:
        """Get risk level from score"""
        if score <= 30:
            return "SAFE"
        elif score <= 60:
            return "CAUTION"
        else:
            return "DANGEROUS"
    
    def _get_line(self, content: str, line_num: int) -> str:
        """Get specific line from content"""
        lines = content.split('\n')
        if 0 < line_num <= len(lines):
            return lines[line_num - 1].strip()
        return ""
