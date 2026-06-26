"""SkillGuard — Code Execution Detector (ASI-03)"""
import ast, re
from typing import List
from skillguard.detectors.base import BaseDetector, Finding, SkillContext, PipelineContext


class CodeExecutionDetector(BaseDetector):
    name = "code_execution"
    description = "Detects dangerous code execution patterns (eval, exec, subprocess, etc.)"
    owasp_asi_ids = ["ASI-03"]
    
    DANGEROUS_CALLS = {
        "eval": ("CRITICAL", "CWE-95", "eval() 可执行任意代码"),
        "exec": ("CRITICAL", "CWE-95", "exec() 可执行任意代码"),
        "compile": ("MEDIUM", "CWE-95", "compile() 可与eval/exec组合实现代码执行"),
        "__import__": ("HIGH", "CWE-94", "__import__() 动态导入可能引入恶意模块"),
        "os.system": ("CRITICAL", "CWE-78", "os.system() 存在命令注入风险"),
        "os.popen": ("CRITICAL", "CWE-78", "os.popen() 存在命令注入风险"),
        "subprocess.call": ("HIGH", "CWE-78", "subprocess调用需shell=False"),
        "subprocess.run": ("MEDIUM", "CWE-78", "subprocess.run需验证参数"),
        "subprocess.Popen": ("HIGH", "CWE-78", "subprocess.Popen需安全审查"),
        "pickle.load": ("HIGH", "CWE-502", "pickle.load 反序列化不安全"),
        "pickle.loads": ("HIGH", "CWE-502", "pickle.loads 反序列化不安全"),
        "marshal.loads": ("HIGH", "CWE-502", "marshal.loads 反序列化不安全"),
        "yaml.load": ("HIGH", "CWE-502", "yaml.load需用yaml.safe_load替代"),
    }
    
    DANGEROUS_PATTERNS = [
        (r'(?:os|subprocess)\.(system|popen|call)\s*\(\s*f["\']', "CRITICAL", "CWE-78", "f-string命令注入"),
        (r'(?:eval|exec)\s*\(\s*(?:request|input|raw_input|sys\.argv)', "CRITICAL", "CWE-95", "用户输入送入eval/exec"),
        (r'shell\s*=\s*True', "HIGH", "CWE-78", "subprocess shell=True不安全"),
        (r'pickle\.(?:load|loads)\s*\(', "HIGH", "CWE-502", "pickle反序列化无安全限制"),
        (r'(?:eval|exec)\s*\(\s*.*format\s*\(', "HIGH", "CWE-95", "format注入可能触发代码执行"),
    ]
    
    def analyze(self, skill_ctx: SkillContext, ctx: PipelineContext) -> List[Finding]:
        findings = []
        for path, content in skill_ctx.python_files.items():
            # AST analysis
            try:
                tree = ast.parse(content)
                ctx.ast_cache[path] = tree
                findings.extend(self._ast_scan(tree, path, content))
            except SyntaxError:
                pass
            
            # Regex patterns
            for pattern, severity, cwe, desc in self.DANGEROUS_PATTERNS:
                for match in re.finditer(pattern, content, re.IGNORECASE):
                    line_num = content[:match.start()].count('\n') + 1
                    findings.append(self._make_finding(
                        finding_id=f"EXEC-{len(findings)+1:03d}",
                        severity=severity, confidence=0.8,
                        owasp_asi_id="ASI-03", cwe_id=cwe,
                        title=desc, code_snippet=match.group(0)[:80],
                        file_path=path, line_number=line_num,
                        remediation="避免将用户输入送入eval/exec。使用subprocess.run(shell=False, args=list)。",
                    ))
        
        return findings
    
    def _ast_scan(self, tree: ast.AST, path: str, content: str) -> List[Finding]:
        findings = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_func_name(node)
                if func_name in self.DANGEROUS_CALLS:
                    sev, cwe, desc = self.DANGEROUS_CALLS[func_name]
                    line_num = node.lineno
                    snippet = content.split('\n')[line_num-1].strip()[:80] if line_num else ""
                    findings.append(self._make_finding(
                        finding_id=f"EXEC-{len(findings)+1:03d}",
                        severity=sev, confidence=0.95,
                        owasp_asi_id="ASI-03", cwe_id=cwe,
                        title=desc, code_snippet=snippet,
                        file_path=path, line_number=line_num,
                        remediation=f"评估{func_name}()的必要性。如不可避免，严格限制输入来源。",
                    ))
        return findings
    
    @staticmethod
    def _get_func_name(node: ast.Call) -> str:
        """Extract fully qualified function name from Call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        if isinstance(node.func, ast.Attribute):
            obj = node.func
            parts = []
            while isinstance(obj, ast.Attribute):
                parts.insert(0, obj.attr)
                obj = obj.value
            if isinstance(obj, ast.Name):
                parts.insert(0, obj.id)
            return ".".join(parts)
        return ""
