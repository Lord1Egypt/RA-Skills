#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查 Python 环境和所需库
用法:
    python check_env.py check_python   - 检查 Python
    python check_env.py check_library  - 检查指定库
    python check_env.py check_all      - 检查所有
"""
import sys
import json

def check_python():
    """检查 Python 版本"""
    version = sys.version_info
    return {
        'installed': True,
        'version': f"{version.major}.{version.minor}.{version.micro}",
        'executable': sys.executable
    }

def check_library(lib_name):
    """检查库是否安装"""
    try:
        if lib_name == 'pypdf':
            __import__('pypdf')
        elif lib_name == 'PyMuPDF':
            __import__('fitz')
        elif lib_name == 'pdfplumber':
            __import__('pdfplumber')
        return {'installed': True}
    except ImportError:
        return {'installed': False}

def get_install_command(lib_name):
    """获取安装命令"""
    return f"{sys.executable} -m pip install {lib_name} -q"

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'No command specified'}, ensure_ascii=False))
        return
    
    command = sys.argv[1]
    
    if command == 'check_python':
        result = check_python()
        print(json.dumps(result, ensure_ascii=False))
    
    elif command == 'check_library':
        if len(sys.argv) < 3:
            print(json.dumps({'error': 'No library name specified'}, ensure_ascii=False))
            return
        lib_name = sys.argv[2]
        result = check_library(lib_name)
        result['name'] = lib_name
        result['install_command'] = get_install_command(lib_name)
        print(json.dumps(result, ensure_ascii=False))
    
    elif command == 'check_all':
        libraries = ['pypdf', 'PyMuPDF']
        results = {
            'python': check_python(),
            'libraries': {}
        }
        for lib in libraries:
            results['libraries'][lib] = check_library(lib)
            results['libraries'][lib]['install_command'] = get_install_command(lib)
        print(json.dumps(results, indent=2, ensure_ascii=False))
    
    else:
        print(json.dumps({'error': f'Unknown command: {command}'}, ensure_ascii=False))

if __name__ == '__main__':
    main()
