#!/usr/bin/env python3
"""
🛡️ 安全卫士 - 安全审计脚本
Shield CN - Security Audit Tool

扫描工作区安全问题，生成中文报告
"""

import os
import re
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# ANSI 颜色
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'


class SecurityAuditor:
    """安全审计器"""
    
    # 敏感信息模式
    SENSITIVE_PATTERNS = {
        "api_key": [
            (r"api[_-]?key\s*[=:]\s*['\"]([^'\"]{8,})['\"]", "API Key"),
            (r"apikey\s*[=:]\s*['\"]([^'\"]{8,})['\"]", "API Key"),
        ],
        "password": [
            (r"password\s*[=:]\s*['\"]([^'\"]{8,})['\"]", "密码"),
            (r"passwd\s*[=:]\s*['\"]([^'\"]{8,})['\"]", "密码"),
            (r"pwd\s*[=:]\s*['\"]([^'\"]{8,})['\"]", "密码"),
        ],
        "secret": [
            (r"secret\s*[=:]\s*['\"]([^'\"]{8,})['\"]", "密钥"),
            (r"token\s*[=:]\s*['\"]([^'\"]{8,})['\"]", "Token"),
        ],
        "aliyun": [
            (r"LTAI[a-zA-Z0-9]{20,}", "阿里云 Key ID"),
            (r"access[_-]?key[_-]?id\s*[=:]\s*['\"](LTAI[a-zA-Z0-9]+)['\"]", "阿里云 AccessKey"),
            (r"access[_-]?key[_-]?secret\s*[=:]\s*['\"][^'\"]{16,}['\"]", "阿里云 Secret"),
        ],
        "tencent": [
            (r"secretId\s*[=:]\s*['\"](AKID[a-zA-Z0-9]+)['\"]", "腾讯云 SecretId"),
            (r"secretKey\s*[=:]\s*['\"][a-zA-Z0-9]{32,}['\"]", "腾讯云 SecretKey"),
        ],
        "private_key": [
            (r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----", "私钥文件"),
            (r"-----BEGIN CERTIFICATE-----", "证书文件"),
        ]
    }
    
    # 高危文件
    DANGEROUS_FILES = [
        ".env",
        ".env.local",
        ".env.production",
        "id_rsa",
        "id_ed25519",
        "credentials",
        "*.pem",
        "*.key",
    ]
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace or os.getcwd())
        self.issues = []
        self.score = 100
        
    def scan(self) -> Dict:
        """执行完整扫描"""
        print(f"{CYAN}🔍 开始安全扫描...{RESET}\n")
        
        # 1. 扫描敏感文件
        self._scan_sensitive_files()
        
        # 2. 扫描 Memory 文件
        self._scan_memory_files()
        
        # 3. 检查文件权限
        self._check_file_permissions()
        
        # 4. 检查 AGENTS.md
        self._check_agents_md()
        
        # 5. 计算安全评分
        self._calculate_score()
        
        return {
            "score": self.score,
            "issues": self.issues,
            "workspace": str(self.workspace),
            "timestamp": datetime.now().isoformat()
        }
    
    def _scan_sensitive_files(self):
        """扫描敏感文件"""
        print(f"{BLUE}📄 扫描敏感文件...{RESET}")
        
        for root, dirs, files in os.walk(self.workspace):
            # 跳过 node_modules 等目录
            dirs[:] = [d for d in dirs if d not in ['node_modules', '.git', '__pycache__', 'venv']]
            
            for file in files:
                filepath = Path(root) / file
                rel_path = filepath.relative_to(self.workspace)
                
                # 检查是否为高危文件
                if any(d in str(rel_path).lower() for d in self.DANGEROUS_FILES):
                    self.issues.append({
                        "type": "dangerous_file",
                        "severity": "HIGH",
                        "file": str(rel_path),
                        "description": f"高危文件: {file}",
                        "suggestion": "从版本控制中排除，或移到 ~/.config/ 等目录"
                    })
                
                # 扫描文件内容
                if file.endswith(('.md', '.json', '.txt', '.yaml', '.yml', '.env')):
                    self._scan_file_content(filepath, rel_path)
    
    def _scan_file_content(self, filepath: Path, rel_path: Path):
        """扫描文件内容中的敏感信息"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                for pattern_type, patterns in self.SENSITIVE_PATTERNS.items():
                    for pattern, desc in patterns:
                        matches = re.finditer(pattern, content, re.IGNORECASE)
                        for match in matches:
                            line_num = content[:match.start()].count('\n') + 1
                            
                            severity = "HIGH" if pattern_type in ["private_key", "aliyun", "tencent"] else "MEDIUM"
                            
                            self.issues.append({
                                "type": "sensitive_data",
                                "severity": severity,
                                "file": str(rel_path),
                                "line": line_num,
                                "description": f"发现敏感信息: {desc}",
                                "suggestion": f"使用环境变量替换硬编码的 {desc}",
                                "redacted": match.group(0)[:20] + "***"
                            })
        except Exception:
            pass
    
    def _scan_memory_files(self):
        """扫描 Memory 文件"""
        print(f"{BLUE}🧠 扫描 Memory 文件...{RESET}")
        
        memory_paths = [
            self.workspace / "MEMORY.md",
            self.workspace / "memory"
        ]
        
        for mem_path in memory_paths:
            if mem_path.is_file():
                self._scan_file_content(mem_path, mem_path.relative_to(self.workspace))
            elif mem_path.is_dir():
                for md_file in mem_path.glob("*.md"):
                    self._scan_file_content(md_file, md_file.relative_to(self.workspace))
    
    def _check_file_permissions(self):
        """检查文件权限"""
        print(f"{BLUE}🔐 检查文件权限...{RESET}")
        
        # 检查 .env 文件权限
        env_files = list(self.workspace.glob("**/.env*"))
        
        for env_file in env_files:
            try:
                stat = os.stat(env_file)
                mode = stat.st_mode & 0o777
                
                if mode & 0o077:  # 任何人可读写
                    self.issues.append({
                        "type": "permission",
                        "severity": "MEDIUM",
                        "file": str(env_file.relative_to(self.workspace)),
                        "description": f".env 文件权限过宽: {oct(mode)}",
                        "suggestion": "运行: chmod 600 .env"
                    })
            except Exception:
                pass
    
    def _check_agents_md(self):
        """检查 AGENTS.md 安全规则"""
        print(f"{BLUE}📋 检查 AGENTS.md...{RESET}")
        
        agents_path = self.workspace / "AGENTS.md"
        
        if not agents_path.exists():
            self.issues.append({
                "type": "missing_security",
                "severity": "LOW",
                "file": "AGENTS.md",
                "description": "未找到 AGENTS.md，建议添加安全规则",
                "suggestion": "安装 shield-cn 并整合安全规则"
            })
            return
        
        # 检查是否包含基本安全规则
        with open(agents_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            
        required_keywords = ["安全", "security", "credential", "密码", "凭证"]
        
        if not any(kw in content for kw in required_keywords):
            self.issues.append({
                "type": "weak_security",
                "severity": "LOW",
                "file": "AGENTS.md",
                "description": "AGENTS.md 缺少安全规则",
                "suggestion": "添加安全防护规则到 AGENTS.md"
            })
    
    def _calculate_score(self):
        """计算安全评分"""
        severity_weights = {
            "HIGH": 20,
            "MEDIUM": 10,
            "LOW": 5
        }
        
        for issue in self.issues:
            self.score -= severity_weights.get(issue["severity"], 5)
        
        self.score = max(0, self.score)
    
    def generate_report(self) -> str:
        """生成中文报告"""
        scan_result = self.scan()
        
        # 严重级别颜色
        def severity_color(severity: str) -> str:
            colors = {"HIGH": RED, "MEDIUM": YELLOW, "LOW": BLUE}
            return colors.get(severity, RESET)
        
        # 生成报告
        report = f"""# 🛡️ 安全审计报告 - {datetime.now().strftime('%Y-%m-%d')}

## 评分: {self._score_color(scan_result['score'])}/100

---

## 总体概览

| 指标 | 数值 |
|------|------|
| 扫描目录 | `{scan_result['workspace']}` |
| 发现问题 | {len(scan_result['issues'])} 个 |
| 安全评分 | {scan_result['score']}/100 |
| 扫描时间 | {scan_result['timestamp']} |

"""
        
        # 按严重级别分组
        by_severity = {"HIGH": [], "MEDIUM": [], "LOW": []}
        for issue in scan_result['issues']:
            by_severity[issue["severity"]].append(issue)
        
        # 高危问题
        if by_severity["HIGH"]:
            report += f"## 🔴 高危问题 ({len(by_severity['HIGH'])}项)\n\n"
            for issue in by_severity["HIGH"]:
                report += f"""### ⚠️ {issue['description']}
- 文件: `{issue['file']}`
{f"- 行号: {issue.get('line', 'N/A')}" if issue.get('line') else ""}
- 建议: {issue['suggestion']}

"""
        
        # 中危问题
        if by_severity["MEDIUM"]:
            report += f"## 🟡 中危问题 ({len(by_severity['MEDIUM'])}项)\n\n"
            for issue in by_severity["MEDIUM"]:
                report += f"""### ⚠️ {issue['description']}
- 文件: `{issue['file']}`
- 建议: {issue['suggestion']}

"""
        
        # 低危问题
        if by_severity["LOW"]:
            report += f"## 🟢 低危/建议 ({len(by_severity['LOW'])}项)\n\n"
            for issue in by_severity["LOW"]:
                report += f"""### 💡 {issue['description']}
- 文件: `{issue['file']}`
- 建议: {issue['suggestion']}

"""
        
        # 改进建议
        report += f"""---

## 📝 改进建议

1. **立即修复高危问题** - 删除或移动敏感文件
2. **使用环境变量** - 不要在代码中硬编码凭证
3. **启用实时防护** - 运行 `python3 shield-cn/scripts/shield-guard.py`
4. **定期审计** - 建议每周运行一次安全扫描

---

*由 🛡️ 安全卫士 v1.0.0 生成*
*扫描时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return report
    
    def _score_color(self, score: int) -> str:
        if score >= 80:
            return f"{GREEN}{score}{RESET}"
        elif score >= 60:
            return f"{YELLOW}{score}{RESET}"
        else:
            return f"{RED}{score}{RESET}"


def main():
    parser = argparse.ArgumentParser(description="🛡️ 安全卫士 - 安全审计")
    parser.add_argument("--workspace", "-w", help="工作区路径 (默认: 当前目录)")
    parser.add_argument("--output", "-o", help="报告输出文件")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    auditor = SecurityAuditor(args.workspace)
    report = auditor.generate_report()
    
    # 输出到文件
    if args.output:
        output_path = Path(args.output)
    else:
        output_dir = Path.home() / ".openclaw" / "reports" / "shield-cn"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / f"security-report-{datetime.now().strftime('%Y%m%d')}.md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n{GREEN}✅ 审计完成{RESET}")
    print(f"报告已保存到: {output_path}")
    print(f"安全评分: {auditor.score}/100")


if __name__ == "__main__":
    main()
