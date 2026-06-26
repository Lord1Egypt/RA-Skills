#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Security Scanner - 安全技能扫描器

这是一个用于扫描OpenClaw技能安全性的工具，能够检测潜在的安全风险，
包括但不限于远程代码执行、数据泄露、敏感文件访问等危险模式。

该工具使用分层风险评估方法，根据检测到的风险类型给予不同的风险分数扣减，
最终生成综合安全评估报告。

作者: OpenClaw Team
版本: 1.0.1
"""

import os
import re
import ast
import sys
import io
from pathlib import Path
from typing import List, Dict, Any, Union, Optional

# 修复 Windows 编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# 危险操作检测模式（按风险等级分类）
DANGER_PATTERNS: Dict[str, List[Dict[str, Any]]] = {
    'critical': [
        {
            'name': '远程代码执行',
            'patterns': [
                r'eval\s*\(\s*requests\.get\s*\([^)]+\)\.text\s*\)',
                r'exec\s*\(\s*urllib\.request\.urlopen\s*\([^)]+\)\.read\s*\(\)\s*\)',
                r'__import__\s*\(\s*["\']os["\']\s*\)\.system\s*\(\s*requests\.get\s*\(',
                r'pickle\.loads\s*\(\s*base64\.b64decode\s*\(\s*requests\.get\s*\(',
            ]
        },
        {
            'name': '数据外传',
            'patterns': [
                r'requests\.post\s*\(\s*["\']https?://[^"\']*?(?:ngrok|serveo|'
                r'localtunnel|webhook)[^"\']*["\']',
                r'urllib\.request\.urlopen\s*\(\s*["\']https?://[^"\']*?'
                r'(?:pastebin|gist|discord|slack)',
            ]
        }
    ],
    'high': [
        {
            'name': '敏感文件读取',
            'patterns': [
                r'open\s*\(\s*["\'](?:\.env|config\.(?:json|yml|yaml)|id_rsa|'
                r'\.aws/credentials|\.ssh/|passwd|shadow)["\']',
                r'(?:pwd|token|secret|key|password)\s*=\s*open\s*\([^)]+\)\.read\s*\(\)',
            ]
        },
        {
            'name': '批量文件操作',
            'patterns': [
                r'(?:shutil\.rmtree|os\.remove|os\.unlink)\s*\(\s*(?:["\']/|'
                r'os\.path\.expanduser\(["\']~)',
                r'for\s+\w+\s+in\s+os\.listdir\s*\([^)]+\):\s*(?:(?!if).)*?'
                r'os\.(?:remove|unlink)',
            ]
        }
    ],
    'medium': [
        {
            'name': '系统命令执行',
            'patterns': [
                r'os\.system\s*\(\s*["\'](?:rm|del|wget|curl|chmod|chown)',
                r'subprocess\.(?:Popen|call|run)\s*\(\s*\[?\s*["\']'
                r'(?:rm|sh|bash|cmd|powershell)',
            ]
        },
        {
            'name': '动态导入/执行',
            'patterns': [
                r'__import__\s*\(\s*\w+\s*\)',
                r'globals\(\)\.(?:get|\[\w+\])\s*\([^)]*\)',
            ]
        }
    ]
}


# 安全使用模式
SAFE_PATTERNS: Dict[str, List[str]] = {
    'smtplib': [
        r'smtplib\.SMTP\s*\(\s*["\']smtp\.gmail\.com["\']',
        r'smtp\.sendmail\s*\(\s*["\'].+?@.+?\.[a-z]+["\']',
    ],
    'requests': [
        r'requests\.get\s*\(\s*["\']https?://api\.github\.com',
        r'requests\.get\s*\(\s*["\']https?://[^"\']*?(?:weather|stock|news)',
    ],
}

# 安全上下文关键字
SAFE_CONTEXTS: List[str] = [
    r'def\s+(?:fetch|download|get|load|read)_',
    r'class\s+(?:Fetcher|Downloader|Loader)',
    r'logger\.(?:debug|info)',
]


class SkillSecurityScanner:
    """
    技能安全扫描器类

    用于扫描OpenClaw技能中的安全风险，包括远程代码执行、数据泄露、
    敏感文件访问等危险操作模式。
    """

    def __init__(self) -> None:
        """
        初始化技能安全扫描器

        设置初始风险评分为100（满分），初始化发现列表和风险评分映射。
        """
        self.score: int = 100
        self.findings: List[Dict[str, Any]] = []
        self.risk_score: Dict[str, int] = {
            'critical': 50,
            'high': 30,
            'medium': 15,
            'low': 5
        }

    def scan(self, skill_directory: str) -> Dict[str, Any]:
        """
        扫描指定技能目录的安全风险

        Args:
            skill_directory: 要扫描的技能目录路径

        Returns:
            包含扫描结果的字典

        Raises:
            FileNotFoundError: 当指定目录不存在时抛出
            NotADirectoryError: 当指定路径不是目录时抛出
            PermissionError: 当没有权限访问目录时抛出
        """
        skill_path = Path(skill_directory)
        if not skill_path.exists():
            error_msg = f"错误：指定的技能目录不存在: {skill_directory}\n"
            error_msg += "请检查路径是否正确，确保目录存在且可访问。"
            raise FileNotFoundError(error_msg)

        if not skill_path.is_dir():
            error_msg = f"错误：指定路径不是一个目录: {skill_directory}\n"
            error_msg += "请确保提供的是一个有效的目录路径。"
            raise NotADirectoryError(error_msg)

        if not os.access(skill_directory, os.R_OK):
            error_msg = f"错误：没有权限读取指定目录: {skill_directory}\n"
            error_msg += "请检查目录权限设置。"
            raise PermissionError(error_msg)

        print(f"开始扫描 Skill: {skill_directory}")

        try:
            for py_file in skill_path.rglob("*.py"):
                self._scan_file(py_file)
        except PermissionError as e:
            print(f"警告：无法访问部分文件，可能影响扫描完整性: {e}")
        except Exception as e:
            print(f"扫描过程中发生未知错误: {e}")
            raise

        return self._generate_report()

    def _scan_file(self, file_path: Path) -> None:
        """
        扫描单个Python文件的安全风险

        Args:
            file_path: 要扫描的文件路径
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检测危险模式
            for risk_level, pattern_groups in DANGER_PATTERNS.items():
                for group in pattern_groups:
                    for pattern in group['patterns']:
                        if re.search(pattern, content, re.IGNORECASE):
                            self.findings.append({
                                'file': str(file_path),
                                'type': group['name'],
                                'risk_level': risk_level,
                                'pattern_matched': pattern
                            })
                            self.score -= self.risk_score[risk_level]

                            if risk_level == 'critical':
                                self.score = 0
                                return
        except UnicodeDecodeError:
            print(f"警告：无法解码文件 {file_path}，可能是二进制文件或编码问题")
        except PermissionError:
            print(f"警告：没有权限读取文件 {file_path}")
        except Exception as e:
            error_msg = f"扫描文件时发生错误: {e}\n"
            error_msg += f"文件路径: {file_path}\n"
            error_msg += "这可能是因为文件损坏、权限问题或其他I/O错误导致的。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 检查文件权限是否正确\n"
            error_msg += "- 确认文件不是二进制文件\n"
            error_msg += "- 验证文件编码格式是否为UTF-8\n"
            print(error_msg)

    def _generate_report(self) -> Dict[str, Any]:
        """
        生成扫描报告

        Returns:
            包含扫描结果详细信息的字典
        """
        # 确保分数在合理范围内
        self.score = max(0, min(100, self.score))

        if self.score >= 80:
            status = "安全"
        elif self.score >= 50:
            status = "需要审核"
        else:
            status = "高风险"

        return {
            'overall_risk_score': self.score,
            'overall_risk_level': status,
            'total_findings': len(self.findings),
            'findings': self.findings,
        }


def print_report(report: Dict[str, Any]) -> None:
    """
    打印格式化的安全扫描报告

    Args:
        report: 包含扫描结果的字典
    """
    print("\n" + "="*60)
    print("Skill 安全扫描报告")
    print("="*60)
    print(f"总体风险评分: {report['overall_risk_score']}/100")
    print(f"总体风险等级: {report['overall_risk_level']}")
    print(f"发现的安全问题数量: {report['total_findings']}")

    # 根据风险等级显示不同颜色的提示
    risk_level = report['overall_risk_level']
    if risk_level == "高风险":
        print("\n🚨 检测到高风险问题！建议立即审查代码！")
    elif risk_level == "需要审核":
        print("\n⚠️ 检测到中等风险问题！建议进一步审查。")
    else:
        print("\n✅ 未检测到严重安全问题。")

    # 显示具体发现
    if report['findings']:
        print("\n详细发现:")
        print("-" * 60)
        for i, finding in enumerate(report['findings'], 1):
            print(f"{i}. 文件: {finding['file']}")
            print(f"   类型: {finding['type']}")
            print(f"   风险等级: {finding['risk_level']}")
            print(f"   匹配模式: {finding['pattern_matched'][:50]}...")
            print()
    else:
        print("\n🎉 未发现安全问题！")

    print("="*60)


def main() -> int:
    """
    主函数

    解析命令行参数并执行安全扫描

    Returns:
        退出码: 0表示成功，非0表示错误
    """
    if len(sys.argv) != 2:
        print("用法: python scanner.py <skill_directory>")
        print("示例: python scanner.py ./my_skill/")
        return 1

    skill_directory = sys.argv[1]

    try:
        scanner = SkillSecurityScanner()
        report = scanner.scan(skill_directory)
        print_report(report)
        return 0
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return 2
    except PermissionError as e:
        print(f"❌ 权限错误: {e}")
        return 3
    except NotADirectoryError as e:
        print(f"❌ 路径错误: {e}")
        return 4
    except Exception as e:
        print(f"❌ 扫描过程中发生未知错误: {e}")
        return 5


if __name__ == "__main__":
    sys.exit(main())