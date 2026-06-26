#!/usr/bin/env python3
"""Clean and upload to GitHub"""
import os
import shutil
import subprocess

base = r'E:\桌面\wechat-allauto-gzh'

def clean():
    """Clean up files"""
    print("Cleaning up...")
    
    # Remove __pycache__
    pycache = os.path.join(base, 'scripts', '__pycache__')
    if os.path.exists(pycache):
        shutil.rmtree(pycache)
        print(f"✅ Removed: {pycache}")
    
    # Remove _drafts
    drafts = os.path.join(base, 'scripts', '_drafts')
    if os.path.exists(drafts):
        shutil.rmtree(drafts)
        print(f"✅ Removed: {drafts}")
    
    # Remove nul file
    nul_file = os.path.join(base, 'nul')
    if os.path.exists(nul_file):
        os.remove(nul_file)
        print(f"✅ Removed: {nul_file}")
    
    # Remove cleanup scripts
    for f in ['cleanup.py', 'cleanup.bat']:
        filepath = os.path.join(base, f)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"✅ Removed: {f}")
    
    print("\n✅ Cleanup complete!")

def git_init_and_push():
    """Initialize git and push to GitHub"""
    os.chdir(base)
    
    print("\n=== Git 初始化 ===")
    subprocess.run(['git', 'init'], check=True)
    print("✅ Git initialized")
    
    print("\n=== 添加文件 ===")
    subprocess.run(['git', 'add', '.'], check=True)
    print("✅ Files added")
    
    print("\n=== 提交更改 ===")
    subprocess.run(['git', 'commit', '-m', 'Initial commit: WeChat Official Account Auto-Writing System\n\nFeatures:\n- 8 built-in themes\n- Auto and guided writing modes\n- Smart theme recommendation\n- WeChat draft push integration\n- OpenCode skill standard compliant'], check=True)
    print("✅ Committed")
    
    print("\n=== 请手动执行以下命令完成上传 ===")
    print(f"""
cd "{base}"

# 1. 在 https://github.com/new 创建仓库，命名为 wechat-allauto-gzh

# 2. 连接远程仓库（替换 YOUR_USERNAME 为您的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/wechat-allauto-gzh.git

# 3. 推送代码
git branch -M main
git push -u origin main
""")

if __name__ == '__main__':
    clean()
    git_init_and_push()