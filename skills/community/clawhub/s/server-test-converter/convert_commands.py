#!/usr/bin/env python3
"""
服务器测试命令转换器
将每个 txt 命令文件转换为独立的 pytest 测试用例（优化版：合并到一个函数）
"""

import os
import re
import sys
from pathlib import Path

# 配置
INPUT_DIR = "/home/admin/.openclaw/tytest/txt_contents/txt"
OUTPUT_DIR = "/home/admin/.openclaw/tytest"


def sanitize_filename(name, exists_names=None):
    """将文件名转换为合法的 Python 标识符"""
    name = os.path.splitext(name)[0]
    name = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fff]', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    
    if not name:
        name = 'unnamed'
    
    if exists_names and name in exists_names:
        counter = 1
        while f"{name}_{counter}" in exists_names:
            counter += 1
        name = f"{name}_{counter}"
    
    return name


def parse_file(filepath):
    """解析单个 txt 文件，返回命令列表"""
    commands = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and not line.startswith('//'):
                    if not re.match(r'^[A-Z_]+=.+', line):
                        if re.search(r'\b(qtype|port|tc|qstart|qnum|DEV|TEID|PTEID)\b', line, re.IGNORECASE):
                            continue
                        commands.append(line)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return commands


def get_executor_type(cmd):
    """判断命令应该使用哪个执行函数"""
    cmd = cmd.strip()
    
    if cmd.startswith('md ') or cmd.startswith('mw '):
        return 'send_r5_wait', 'TARGET_R5'
    if cmd.startswith('txsch_test_') or cmd.startswith('dmif_txsch'):
        return 'send_r5_wait', 'TARGET_R5'
    if 'dmif_eoc_' in cmd or '_show_dfx' in cmd or cmd.startswith('dmif_lan_'):
        return 'send_r5_wait', 'TARGET_R5'
    if (cmd.startswith('ice_') or cmd.startswith('test_') or 
        cmd.startswith('nicif_') or cmd.startswith('sce_') or
        cmd.startswith('dmif_')):
        return 'send_r5_wait', 'TARGET_R5'
    
    return 'send_host_wait', 'TARGET'


def escape_cmd(cmd):
    """转义单引号"""
    return cmd.replace("'", "''")


def generate_test_file(txt_path, commands, module_name=None):
    """为单个 txt 文件生成 pytest 测试文件（优化版）"""
    txt_name = os.path.basename(txt_path)
    if module_name is None:
        module_name = sanitize_filename(txt_name)
    
    filename = os.path.join(OUTPUT_DIR, f"test_{module_name}.py")
    
    # 去重
    seen_cmds = set()
    unique_commands = []
    for cmd in commands:
        if cmd not in seen_cmds:
            seen_cmds.add(cmd)
            unique_commands.append(cmd)
    
    # 按执行方式分组
    r5_commands = []
    host_commands = []
    
    for cmd in unique_commands:
        executor, target = get_executor_type(cmd)
        if executor == 'send_r5_wait':
            r5_commands.append(cmd)
        else:
            host_commands.append(cmd)
    
    # 构建测试代码
    test_code = ""
    
    if r5_commands and not host_commands:
        # 只有 R5 命令
        cmd_list = ",\n        ".join([f"'{escape_cmd(cmd)}'" for cmd in r5_commands])
        test_code = f'''    def test_all_commands(self, env):
        """执行所有命令（共 {len(r5_commands)} 条）"""
        commands = [
        {cmd_list}
        ]
        for cmd in commands:
            tl_log.info(f"Executing: {{cmd}}")
            send_r5_wait(TARGET_R5, cmd)
'''
    elif host_commands and not r5_commands:
        # 只有 Host 命令
        cmd_list = ",\n        ".join([f"'{escape_cmd(cmd)}'" for cmd in host_commands])
        test_code = f'''    def test_all_commands(self, env):
        """执行所有命令（共 {len(host_commands)} 条）"""
        commands = [
        {cmd_list}
        ]
        for cmd in commands:
            tl_log.info(f"Executing: {{cmd}}")
            send_host_wait(TARGET, cmd)
'''
    else:
        # 两种都有
        r5_list = ",\n        ".join([f"'{escape_cmd(cmd)}'" for cmd in r5_commands])
        host_list = ",\n        ".join([f"'{escape_cmd(cmd)}'" for cmd in host_commands])
        
        test_code = f'''    def test_r5_commands(self, env):
        """执行 R5 命令（共 {len(r5_commands)} 条）"""
        commands = [
        {r5_list}
        ]
        for cmd in commands:
            tl_log.info(f"R5: {{cmd}}")
            send_r5_wait(TARGET_R5, cmd)

    def test_host_commands(self, env):
        """执行 Host 命令（共 {len(host_commands)} 条）"""
        commands = [
        {host_list}
        ]
        for cmd in commands:
            tl_log.info(f"Host: {{cmd}}")
            send_host_wait(TARGET, cmd)
'''
    
    # 生成完整文件
    content = f'''#!/usr/bin/env python3
"""
自动生成的测试用例: {txt_name}
由 server-test-converter 生成
共 {len(unique_commands)} 条命令（去重后）
"""

import pytest
import sys
import os

# 导入通用框架（优先使用当前目录的 test_framework）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from test_framework import send_r5, send_host, send_r5_wait, send_host_wait, tl_log, TARGET, TARGET_R5
except ImportError:
    # 兼容旧版本
    try:
        from test_cs100_slt import send_r5, send_host, send_r5_wait, send_host_wait, tl_log, SXE_HOST as TARGET, SW as TARGET_R5
    except ImportError:
        pass


class Test{module_name.title().replace('_', '')}:
    """{txt_name} 测试用例"""

{test_code}
'''
    
    # 写入文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename, len(unique_commands)


def main():
    """主函数"""
    print(f"Reading commands from: {INPUT_DIR}")
    
    txt_files = sorted(Path(INPUT_DIR).glob('*.txt'))
    print(f"Found {len(txt_files)} txt files\n")
    
    used_names = set()
    total_tests = 0
    
    for txt_file in txt_files:
        commands = parse_file(txt_file)
        if commands:
            module_name = sanitize_filename(txt_file.name, used_names)
            used_names.add(module_name)
            
            filename, count = generate_test_file(txt_file, commands, module_name)
            print(f"Generated: {filename} ({count} commands)")
            total_tests += 1
    
    print(f"\nDone! Generated {total_tests} test files.")


if __name__ == '__main__':
    main()
