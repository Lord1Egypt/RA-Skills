"""
Fluid Memory Skill - OpenClaw Interface
将流体大脑封装为 OpenClaw 可调用的 Skill
"""
import sys
import os
import subprocess
import shutil

def get_python_path():
    """动态查找 Python 路径"""
    import os
    
    # 1. 尝试 CONDA_PREFIX 环境变量
    conda_prefix = os.environ.get('CONDA_PREFIX', '')
    if conda_prefix:
        conda_python = os.path.join(conda_prefix, 'python.exe')
        if os.path.exists(conda_python):
            return conda_python
    
    # 2. 尝试 CONDA 环境变量
    conda = os.environ.get('CONDA', '')
    if conda:
        conda_python = os.path.join(conda, 'python.exe')
        if os.path.exists(conda_python):
            return conda_python
    
    # 3. 尝试常见 conda 安装位置 (用户目录)
    home = os.path.expanduser('~')
    common_paths = [
        os.path.join(home, 'miniconda3', 'python.exe'),
        os.path.join(home, 'anaconda3', 'python.exe'),
    ]
    for p in common_paths:
        if os.path.exists(p):
            return p
    
    # 4. 尝试系统 PATH 中的 python
    python_cmd = shutil.which('python')
    if python_cmd:
        return python_cmd
    
    # 5. 尝试 py launcher (Windows 内置)
    py_cmd = shutil.which('py')
    if py_cmd:
        return py_cmd
    
    # 6. 找不到则抛出异常
    raise RuntimeError("未找到 Python。请确保已安装 Python 或在 PATH 中。")

# 动态获取 Python 路径
PYTHON_PATH = get_python_path()
SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "fluid_skill.py")

def execute(action, content="", query="", conversation=""):
    cmd = [PYTHON_PATH, SCRIPT_PATH, action]
    
    if action == "remember" and content:
        cmd.extend(["--content", content])
    elif action == "recall" and query:
        cmd.extend(["--query", query])
    elif action == "forget" and content:
        cmd.extend(["--content", content])
    elif action in ["summarize", "increment_summarize"] and conversation:
        cmd.extend(["--conversation", conversation])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

# OpenClaw 会调用这个文件
if __name__ == "__main__":
    # 简单的 CLI 接口
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    parser.add_argument("--content", default="")
    parser.add_argument("--query", default="")
    parser.add_argument("--conversation", default="")
    args = parser.parse_args()
    
    print(execute(args.action, args.content, args.query, args.conversation))
