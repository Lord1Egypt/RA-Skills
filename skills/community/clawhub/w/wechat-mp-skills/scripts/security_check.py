#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
安全检查脚本
检查项目的安全配置和潜在风险
"""

import os
import sys
from pathlib import Path
from typing import List, Tuple

# 设置输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class SecurityChecker:
    """安全检查器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.issues: List[Tuple[str, str, str]] = []  # (级别, 问题, 建议)
    
    def check_all(self):
        """运行所有安全检查"""
        print("🔒 开始安全检查...\n")
        
        self.check_sensitive_files()
        self.check_file_permissions()
        self.check_gitignore()
        self.check_env_files()
        self.check_config_files()
        self.check_dependencies()
        
        self.print_report()
    
    def check_sensitive_files(self):
        """检查敏感文件"""
        print("📁 检查敏感文件...")
        
        sensitive_files = [
            '.env',
            'config.local.json',
            'credentials.json',
            '*.pem',
            '*.key',
        ]
        
        for pattern in sensitive_files:
            files = list(self.project_root.glob(pattern))
            for file in files:
                if file.exists():
                    self.issues.append((
                        '⚠️  中危',
                        f"发现敏感文件: {file.name}",
                        "确保此文件不会被提交到版本控制"
                    ))
    
    def check_file_permissions(self):
        """检查文件权限"""
        print("🔐 检查文件权限...")
        
        config_files = ['config.json', '.env']
        
        for filename in config_files:
            file_path = self.project_root / filename
            if file_path.exists():
                # 检查文件权限（仅 Unix 系统）
                if sys.platform != 'win32':
                    stat_info = file_path.stat()
                    mode = oct(stat_info.st_mode)[-3:]
                    
                    if mode != '600':
                        self.issues.append((
                            '⚠️  中危',
                            f"{filename} 权限过于开放: {mode}",
                            "建议设置为 600: chmod 600 " + filename
                        ))
    
    def check_gitignore(self):
        """检查 .gitignore 配置"""
        print("🚫 检查 .gitignore 配置...")
        
        gitignore_path = self.project_root / '.gitignore'
        
        if not gitignore_path.exists():
            self.issues.append((
                '🔴 高危',
                "缺少 .gitignore 文件",
                "创建 .gitignore 文件以保护敏感信息"
            ))
            return
        
        # 检查是否包含必要的忽略规则
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_patterns = ['.env', 'config.local.json', '*.log', '__pycache__']
        
        for pattern in required_patterns:
            if pattern not in content:
                self.issues.append((
                    '⚠️  中危',
                    f".gitignore 缺少规则: {pattern}",
                    f"添加 '{pattern}' 到 .gitignore"
                ))
    
    def check_env_files(self):
        """检查环境变量文件"""
        print("🌍 检查环境变量文件...")
        
        env_example = self.project_root / '.env.example'
        env_file = self.project_root / '.env'
        
        if not env_example.exists():
            self.issues.append((
                'ℹ️  建议',
                "缺少 .env.example 文件",
                "创建 .env.example 作为环境变量模板"
            ))
        
        if env_file.exists():
            # 检查 .env 文件内容
            with open(env_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'your_app_id' in content.lower() or 'your_app_secret' in content.lower():
                self.issues.append((
                    'ℹ️  建议',
                    ".env 文件包含占位符",
                    "请填入真实的凭证"
                ))
    
    def check_config_files(self):
        """检查配置文件"""
        print("⚙️  检查配置文件...")
        
        config_file = self.project_root / 'config.json'
        
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查是否包含真实凭证
            if 'wx' in content and len(content) > 100:
                # 可能包含真实 AppID
                if 'your_app_id' not in content:
                    self.issues.append((
                        '🔴 高危',
                        "config.json 可能包含真实凭证",
                        "将真实凭证替换为占位符，使用环境变量管理"
                    ))
    
    def check_dependencies(self):
        """检查依赖安全"""
        print("📦 检查依赖安全...")
        
        requirements_file = self.project_root / 'requirements.txt'
        
        if not requirements_file.exists():
            self.issues.append((
                'ℹ️  建议',
                "缺少 requirements.txt 文件",
                "创建 requirements.txt 列出项目依赖"
            ))
        else:
            # 检查是否有依赖版本固定
            with open(requirements_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '==' not in line and '>=' not in line:
                        self.issues.append((
                            'ℹ️  建议',
                            f"依赖未固定版本: {line}",
                            "建议固定依赖版本以确保可重现构建"
                        ))
    
    def print_report(self):
        """打印安全报告"""
        print("\n" + "="*60)
        print("🔒 安全检查报告")
        print("="*60 + "\n")
        
        if not self.issues:
            print("✅ 未发现安全问题！\n")
            return
        
        # 按严重程度分组
        high_risk = [i for i in self.issues if '高危' in i[0]]
        medium_risk = [i for i in self.issues if '中危' in i[0]]
        low_risk = [i for i in self.issues if '建议' in i[0]]
        
        # 打印高危问题
        if high_risk:
            print("🔴 高危问题:")
            for level, issue, suggestion in high_risk:
                print(f"  • {issue}")
                print(f"    💡 {suggestion}\n")
        
        # 打印中危问题
        if medium_risk:
            print("⚠️  中危问题:")
            for level, issue, suggestion in medium_risk:
                print(f"  • {issue}")
                print(f"    💡 {suggestion}\n")
        
        # 打印建议
        if low_risk:
            print("ℹ️  改进建议:")
            for level, issue, suggestion in low_risk:
                print(f"  • {issue}")
                print(f"    💡 {suggestion}\n")
        
        # 总结
        print("="*60)
        print(f"总计: {len(self.issues)} 个问题")
        print(f"  🔴 高危: {len(high_risk)}")
        print(f"  ⚠️  中危: {len(medium_risk)}")
        print(f"  ℹ️  建议: {len(low_risk)}")
        print("="*60 + "\n")


def main():
    """主函数"""
    # 获取项目根目录
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # 创建检查器并运行
    checker = SecurityChecker(project_root)
    checker.check_all()


if __name__ == "__main__":
    main()
