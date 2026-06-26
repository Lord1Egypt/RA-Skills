#!/usr/bin/env python3
"""
工作空间检查脚本 (Windows兼容版)
无Unicode表情符号，纯ASCII输出
支持--fix参数自动修复问题
"""

import os
import sys
import datetime
import re
import shutil
from pathlib import Path

def fix_issues(workspace):
    """自动修复发现的问题"""
    print("\n=== 开始自动修复 ===")
    fixed_count = 0
    
    # 1. 修复根目录冗余文件: 移动到tmp目录
    essential_files = ['AGENTS.md', 'SOUL.md', 'MEMORY.md', 'USER.md', 'TOOLS.md', 'HEARTBEAT.md', '.gitignore', 'IDENTITY.md', 'BOOTSTRAP.md']
    root_files = [f for f in workspace.iterdir() if f.is_file()]
    non_essential = [f for f in root_files if f.name not in essential_files]
    
    if non_essential:
        tmp_dir = workspace / 'tmp'
        tmp_dir.mkdir(exist_ok=True)
        for file in non_essential:
            try:
                shutil.move(str(file), str(tmp_dir / file.name))
                print(f"  [OK] 移动冗余文件到tmp目录: {file.name}")
                fixed_count += 1
            except Exception as e:
                print(f"  [ERROR] 移动文件失败 {file.name}: {e}")
    
    # 2. 修复记忆文件命名规范
    memory_dir = workspace / 'memory'
    if memory_dir.exists():
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}\.md$')
        for file in memory_dir.glob("*.md"):
            if not date_pattern.match(file.name):
                # 尝试提取日期，或者重命名为当前日期+序号
                new_name = None
                # 检查文件名是否包含日期
                date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', file.name)
                if date_match:
                    base_name = f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}"
                    counter = 1
                    new_name = f"{base_name}.md"
                    # 如果文件已存在，添加序号
                    while (memory_dir / new_name).exists():
                        new_name = f"{base_name}_{counter}.md"
                        counter += 1
                else:
                    # 使用当前日期 + 序号
                    today = datetime.date.today().strftime('%Y-%m-%d')
                    counter = 1
                    while (memory_dir / f"{today}_{counter}.md").exists():
                        counter += 1
                    new_name = f"{today}_{counter}.md"
                
                try:
                    file.rename(memory_dir / new_name)
                    print(f"  [OK] 重命名记忆文件: {file.name} → {new_name}")
                    fixed_count += 1
                except Exception as e:
                    print(f"  [ERROR] 重命名失败 {file.name}: {e}")
    
    # 3. 修复scripts目录可执行权限
    scripts_dir = workspace / 'scripts'
    if scripts_dir.exists():
        supported_extensions = ['.py', '.ps1', '.sh', '.bat', '.cmd']
        for file in scripts_dir.iterdir():
            if file.is_file():
                # Windows下添加.ps1文件的执行权限
                if file.suffix == '.ps1':
                    try:
                        import subprocess
                        subprocess.run(
                            ['icacls', str(file), '/grant', f'{os.getlogin()}:RX'],
                            capture_output=True,
                            check=True
                        )
                        print(f"  [OK] 添加执行权限: {file.name}")
                        fixed_count += 1
                    except Exception as e:
                        print(f"  [ERROR] 添加权限失败 {file.name}: {e}")
    
    # 4. 自动提交Git更改
    git_dir = workspace / '.git'
    if git_dir.exists():
        try:
            import subprocess
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True
            )
            
            if status_result.stdout.strip():
                # 添加所有更改
                subprocess.run(['git', 'add', '.'], check=True, capture_output=True)
                # 提交
                commit_msg = f"Auto commit: 工作空间自动修复 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
                subprocess.run(['git', 'commit', '-m', commit_msg], check=True, capture_output=True)
                print(f"  [OK] 自动提交Git更改")
                fixed_count += 1
        except Exception as e:
            print(f"  [ERROR] Git自动提交失败: {e}")
    
    print(f"\n=== 修复完成: 共修复 {fixed_count} 个问题 ===")
    return fixed_count

def check_workspace(auto_fix=False):
    """检查工作空间健康状态"""
    workspace = Path(".").resolve()
    print(f"工作空间检查: {workspace.name}")
    print("=" * 50)
    
    issues = []
    warnings = []
    successes = []
    
    # 1. 核心配置文件
    essential_files = ['AGENTS.md', 'SOUL.md', 'MEMORY.md', 'USER.md', 'TOOLS.md', 'HEARTBEAT.md']
    missing_files = []
    for file in essential_files:
        if not (workspace / file).exists():
            missing_files.append(file)
    
    if missing_files:
        issues.append(f"缺失核心配置文件: {', '.join(missing_files)}")
    else:
        successes.append("所有核心配置文件完整")
    
    # 2. 必要目录
    essential_dirs = ['memory', 'learning', 'scripts']
    missing_dirs = []
    for dir_name in essential_dirs:
        if not (workspace / dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        issues.append(f"缺失必要目录: {', '.join(missing_dirs)}")
    else:
        successes.append("基本目录结构完整")
    
    # 3. memory目录最近文件
    memory_dir = workspace / 'memory'
    if memory_dir.exists():
        date_files = []
        for file in memory_dir.glob("*.md"):
            if file.name.endswith('.md'):
                date_files.append(file.name.replace('.md', ''))
        
        # 检查最近3天
        today = datetime.date.today()
        missing_recent = []
        for i in range(3):
            date_str = (today - datetime.timedelta(days=i)).strftime('%Y-%m-%d')
            if date_str not in date_files:
                missing_recent.append(date_str)
        
        if missing_recent:
            warnings.append(f"缺少最近{len(missing_recent)}天的记忆文件")
        else:
            successes.append("近期记忆文件完整")
    else:
        issues.append("memory/目录不存在")
    
    # 4. 根目录非核心文件
    root_files = [f.name for f in workspace.iterdir() if f.is_file()]
    non_essential = [f for f in root_files if f not in essential_files and f not in ['.gitignore', 'IDENTITY.md', 'BOOTSTRAP.md']]
    
    if non_essential:
        warnings.append(f"根目录有{len(non_essential)}个非核心文件")
    else:
        successes.append("根目录无冗余文件，符合规范")
    
    # 5. 记忆文件命名规范检查
    if memory_dir.exists():
        invalid_memory_files = []
        # 允许的格式: YYYY-MM-DD.md 或者 YYYY-MM-DD_*.md
        pattern = re.compile(r'^\d{4}-\d{2}-\d{2}(_\d+)?\.md$')
        for file in memory_dir.glob("*.md"):
            filename = file.name
            if not pattern.match(filename):
                invalid_memory_files.append(filename)
        
        if invalid_memory_files:
            warnings.append(f"有{len(invalid_memory_files)}个记忆文件命名不符合规范")
        else:
            successes.append("所有记忆文件命名符合规范")
    
    # 6. scripts目录脚本可执行性检查
    scripts_dir = workspace / 'scripts'
    if scripts_dir.exists():
        invalid_scripts = []
        supported_extensions = ['.py', '.ps1', '.sh', '.bat', '.cmd']
        for file in scripts_dir.iterdir():
            if file.is_file() and file.suffix not in supported_extensions:
                invalid_scripts.append(file.name)
        
        if invalid_scripts:
            warnings.append(f"scripts目录有{len(invalid_scripts)}个非可执行文件")
        else:
            successes.append("scripts目录所有文件都是可执行脚本，符合规范")
    
    # 7. Git状态
    git_dir = workspace / '.git'
    if git_dir.exists():
        try:
            import subprocess
            status_result = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True
            )
            
            if status_result.stdout.strip():
                warnings.append("存在未提交的Git更改")
            else:
                successes.append("Git状态干净")
        except Exception:
            warnings.append("无法检查Git状态")
    
    # 打印报告
    if issues:
        print("\n[ERROR] 问题:")
        for issue in issues:
            print(f"  * {issue}")
    
    if warnings:
        print("\n[WARNING] 警告:")
        for warning in warnings:
            print(f"  * {warning}")
    
    if successes:
        print("\n[OK] 成功:")
        for success in successes:
            print(f"  * {success}")
    
    print("\n" + "=" * 50)
    
    # 计算健康分数
    total_checks = len(issues) + len(warnings) + len(successes)
    if total_checks == 0:
        health_score = 100
    else:
        health_score = int((len(successes) / total_checks) * 100)
    
    print(f"健康分数: {health_score}/100")
    
    if health_score >= 90:
        print("状态: 优秀")
    elif health_score >= 70:
        print("状态: 良好")
    elif health_score >= 50:
        print("状态: 需要关注")
    else:
        print("状态: 需要立即处理")
    
    print("\n建议:")
    if issues:
        print("  * 立即处理上述问题")
    if warnings:
        print("  * 考虑处理警告项")
    if health_score >= 90:
        print("  * 继续保持良好习惯")
    
    # 自动修复
    if auto_fix and (issues or warnings):
        fix_issues(workspace)
        # 重新检查
        print("\n=== 重新检查工作空间 ===")
        return check_workspace(auto_fix=False)
    
    # 返回退出代码
    if issues:
        return 2
    elif warnings:
        return 1
    else:
        return 0

if __name__ == "__main__":
    try:
        auto_fix = '--fix' in sys.argv
        exit_code = check_workspace(auto_fix)
        sys.exit(exit_code)
    except Exception as e:
        print(f"检查过程中出错: {e}")
        sys.exit(3)