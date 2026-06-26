#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
依赖检查与自动安装模块
首次使用时自动检测并安装缺失的依赖
"""

import subprocess
import sys
from pathlib import Path


# 必需依赖列表
# key是包名(import用), value是pip包名
REQUIREMENTS = {
    'docx': 'python-docx>=1.0.0',          # import docx, not python-docx
    'pdfplumber': 'pdfplumber>=0.10.0',
    'jieba': 'jieba>=0.42.1',
    'sklearn': 'scikit-learn>=1.0.0',        # import sklearn, not scikit-learn
    'lxml': 'lxml>=4.9.0',
    'bs4': 'beautifulsoup4>=4.12.0',         # import bs4, not beautifulsoup4
    'jinja2': 'Jinja2>=3.0.0',               # import jinja2, not Jinja2
}

# 可选依赖
OPTIONAL_REQUIREMENTS = {
    'sentence_transformers': 'sentence-transformers>=2.2.0',
    'simhash': 'simhash>=2.1.2',
}


def check_module_available(module_name: str) -> bool:
    """检查模块是否可用"""
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def get_missing_requirements() -> dict:
    """获取缺失的必需依赖"""
    missing = {}
    for module, package in REQUIREMENTS.items():
        if not check_module_available(module):
            missing[module] = package
    return missing


def get_missing_optional() -> dict:
    """获取缺失的可选依赖"""
    missing = {}
    for module, package in OPTIONAL_REQUIREMENTS.items():
        if not check_module_available(module):
            missing[module] = package
    return missing


def install_requirements(packages: list, verbose: bool = True) -> bool:
    """
    安装依赖包
    
    @param packages: 包名列表
    @param verbose: 是否显示详细信息
    @return: 是否安装成功
    """
    if not packages:
        return True
        
    try:
        cmd = [sys.executable, '-m', 'pip', 'install', '--upgrade'] + packages
        
        if verbose:
            print(f"[*] 正在安装依赖: {', '.join(packages)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )
        
        if result.returncode == 0:
            if verbose:
                print("[+] 依赖安装成功")
            return True
        else:
            if verbose:
                print(f"[!] 安装失败: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        if verbose:
            print("[!] 安装超时，请检查网络连接")
        return False
    except Exception as e:
        if verbose:
            print(f"[!] 安装出错: {e}")
        return False


def ensure_dependencies(auto_install: bool = False, verbose: bool = True) -> bool:
    """
    确保所有依赖可用
    
    @param auto_install: 是否自动安装缺失依赖
    @param verbose: 是否显示详细信息
    @return: 是否所有依赖都可用
    """
    missing = get_missing_requirements()
    missing_optional = get_missing_optional()
    
    if not missing and not missing_optional:
        if verbose:
            print("[+] 所有依赖已满足")
        return True
    
    # 缺失可选依赖
    if missing_optional:
        if verbose:
            print(f"[*] 可选依赖缺失: {', '.join(missing_optional.keys())}")
            print("    (部分高级功能可能不可用)")
    
    # 缺失必需依赖
    if missing:
        if verbose:
            print(f"[!] 必需依赖缺失: {', '.join(missing.keys())}")
        
        if auto_install:
            packages = list(missing.values())
            success = install_requirements(packages, verbose)
            
            if success:
                # 重新检查
                still_missing = get_missing_requirements()
                if still_missing:
                    if verbose:
                        print(f"[!] 仍有依赖缺失: {', '.join(still_missing.keys())}")
                    return False
                return True
            else:
                return False
        else:
            return False
    
    return True


def get_installation_instructions() -> str:
    """获取手动安装说明"""
    missing = get_missing_requirements()
    
    if not missing:
        return ""
    
    packages = list(missing.values())
    
    return f"""
⚠️ 检测到缺失依赖，请执行以下命令安装：

方式1: pip安装
  pip install {' '.join(packages)}

方式2: 通过AI自动安装
  回复"安装依赖"，AI将自动为您安装

方式3: 在skill目录执行
  cd ~/.openclaw/workspace/skills/tender-similarity-analyzer
  pip install -r requirements.txt
"""


if __name__ == '__main__':
    # 单独运行此脚本时执行检查
    print("=" * 50)
    print("tender-similarity-analyzer 依赖检查")
    print("=" * 50)
    
    missing = get_missing_requirements()
    missing_opt = get_missing_optional()
    
    if not missing and not missing_opt:
        print("[+] 所有依赖已安装")
        sys.exit(0)
    
    if missing_opt:
        print(f"[*] 可选依赖缺失: {', '.join(missing_opt.keys())}")
    
    if missing:
        print(f"[!] 必需依赖缺失: {', '.join(missing.keys())}")
        print("")
        
        # 尝试自动安装
        packages = list(missing.values()) + list(missing_opt.values())
        
        if input("是否自动安装？(y/n): ").lower() == 'y':
            install_requirements(packages)
            
            # 验证
            still_missing = get_missing_requirements()
            if not still_missing:
                print("[+] 所有必需依赖已安装")
            else:
                print(f"[!] 仍有缺失: {', '.join(still_missing.keys())}")
