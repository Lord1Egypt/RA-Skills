#!/usr/bin/env python3
"""
skill-publisher: 自动更新 GitHub 仓库并发布到 ClawHub
功能：
1. 更新 package.json 和 _meta.json 版本号
2. 更新 README.md 更新日志
3. 提交到 Git 并推送到 GitHub
4. 发布到 ClawHub

注意：本脚本使用可靠的字符串替换方法，避免 edit 工具的精确匹配问题。
"""

import sys
import os
import json
import subprocess
import argparse
from datetime import datetime
import re

def run_cmd(cmd, cwd=None):
    """执行 shell 命令"""
    print(f"🔧 执行：{cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0 and result.stderr:
        print(f"❌ 错误：{result.stderr.strip()}")
    return result.returncode == 0, result.stdout, result.stderr

def parse_version(version):
    """解析版本号"""
    match = re.match(r'(\d+)\.(\d+)\.(\d+)', version)
    if match:
        return [int(match.group(1)), int(match.group(2)), int(match.group(3))]
    return None

def bump_version(version, bump_type='patch'):
    """版本号递增"""
    parts = parse_version(version)
    if not parts:
        return None
    
    if bump_type == 'major':
        parts[0] += 1
        parts[1] = 0
        parts[2] = 0
    elif bump_type == 'minor':
        parts[1] += 1
        parts[2] = 0
    else:  # patch
        parts[2] += 1
    
    return f"{parts[0]}.{parts[1]}.{parts[2]}"

def update_json_file(filepath, version):
    """更新 JSON 文件的版本号（使用 JSON 解析，可靠）"""
    if not os.path.exists(filepath):
        print(f"⚠️  文件不存在：{filepath}")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data['version'] = version
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')
    
    print(f"✅ 已更新：{filepath} → v{version}")
    return True

def update_readme_changelog(filepath, version, changelog):
    """
    更新 README.md 的更新日志（使用正则表达式，可靠）
    
    策略：
    1. 如果存在"## 更新日志"部分，在其后插入新条目
    2. 如果不存在，在文件末尾创建该部分
    """
    if not os.path.exists(filepath):
        print(f"⚠️  文件不存在：{filepath}")
        return False
    
    today = datetime.now().strftime('%Y-%m-%d')
    new_entry = f"\n### v{version} ({today})\n- {changelog}\n"
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找更新日志部分
    changelog_header = "## 更新日志"
    
    if changelog_header in content:
        # 使用正则表达式在标题后插入
        # 匹配"## 更新日志"后的第一个空行之后
        pattern = r'(## 更新日志\n)'
        replacement = r'\1' + new_entry
        content = re.sub(pattern, replacement, content, count=1)
        print(f"✅ 已更新 README.md 更新日志 → v{version}")
    else:
        # 在文件末尾添加更新日志部分
        content += f"\n## 更新日志\n{new_entry}"
        print(f"✅ 已创建 README.md 更新日志 → v{version}")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def init_git(cwd):
    """初始化 Git 仓库（如果尚未初始化）"""
    # 检查是否已有 .git 目录
    if not os.path.exists(os.path.join(cwd, '.git')):
        print("📦 初始化 Git 仓库...")
        success, _, _ = run_cmd("git init", cwd=cwd)
        if not success:
            return False
    
    # 检查是否有远程仓库
    success, output, _ = run_cmd("git remote -v", cwd=cwd)
    if not output.strip():
        print("⚠️  未配置远程仓库，跳过推送")
        return True  # 不视为错误
    
    return True

def git_commit_push(cwd, version, message, collection_root=None):
    """提交并推送代码"""
    # 如果是集合仓库，使用集合根目录作为 Git 仓库
    git_cwd = collection_root if collection_root else cwd
    
    # 添加所有文件
    success, _, _ = run_cmd("git add -A", cwd=git_cwd)
    if not success:
        return False
    
    # 检查是否有更改
    success, output, _ = run_cmd("git status --porcelain", cwd=git_cwd)
    if not output.strip():
        print("ℹ️  没有文件更改")
        return True
    
    # 提交
    commit_msg = f"v{version}: {message}"
    success, _, _ = run_cmd(f'git commit -m "{commit_msg}"', cwd=git_cwd)
    if not success:
        return False
    
    # 推送
    success, _, stderr = run_cmd("git push", cwd=git_cwd)
    if not success:
        if "could not read Username" in stderr or "Authentication failed" in stderr:
            print("⚠️  Git 认证失败，请配置 Git 凭证或 SSH 密钥")
        else:
            print("⚠️  推送失败，请检查远程仓库配置")
        return True  # 不视为致命错误
    
    return True

def publish_to_clawhub(cwd, slug, version, changelog):
    """发布到 ClawHub"""
    print(f"🚀 发布到 ClawHub: {slug}@{version}")
    
    cmd = f"npx clawhub@latest publish {cwd} --slug {slug} --version {version} --changelog \"{changelog}\""
    success, output, stderr = run_cmd(cmd)
    
    if success and "Published" in output:
        # 提取 Skill ID
        match = re.search(r'Published [^@]+@[\d.]+ \(([^)]+)\)', output)
        if match:
            skill_id = match.group(1)
            print(f"✅ ClawHub 发布成功!")
            print(f"📦 Skill ID: {skill_id}")
            print(f"🔗 链接：https://clawhub.ai/{skill_id}/{slug}")
            return True, skill_id
    
    # 检查错误原因
    if "Version already exists" in output or "Version already exists" in stderr:
        print(f"⚠️  版本 v{version} 已存在!")
        print(f"💡 建议：使用 --bump 参数自动递增版本号，或手动指定新版本号")
    elif "Slug is already taken" in output or "Slug is already taken" in stderr:
        print(f"⚠️  Slug '{slug}' 已被占用!")
        print(f"💡 建议：更换唯一的 slug 名称")
    else:
        print("❌ ClawHub 发布失败")
    
    return False, None

def main():
    parser = argparse.ArgumentParser(description='发布 Skill 到 GitHub 和 ClawHub')
    parser.add_argument('path', help='Skill 目录路径')
    parser.add_argument('--slug', required=True, help='Skill slug')
    parser.add_argument('--name', help='Display name（可选）')
    parser.add_argument('--bump', choices=['major', 'minor', 'patch'], default='patch', help='版本号递增类型（默认：patch）')
    parser.add_argument('--changelog', required=True, help='更新日志')
    parser.add_argument('--skip-git', action='store_true', help='跳过 Git 操作')
    parser.add_argument('--skip-clawhub', action='store_true', help='跳过 ClawHub 发布')
    parser.add_argument('--collection-root', help='集合仓库根目录（可选，用于 monorepo 结构）')
    
    args = parser.parse_args()
    
    # 转换为绝对路径
    skill_path = os.path.abspath(args.path)
    
    if not os.path.isdir(skill_path):
        print(f"❌ 目录不存在：{skill_path}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"  📦 Skill Publisher")
    print(f"  路径：{skill_path}")
    print(f"  Slug: {args.slug}")
    if args.collection_root:
        print(f"  集合根目录：{args.collection_root}")
    print(f"{'='*60}\n")
    
    # 读取当前版本
    package_json = os.path.join(skill_path, 'package.json')
    meta_json = os.path.join(skill_path, '_meta.json')
    
    current_version = '0.0.0'
    if os.path.exists(package_json):
        with open(package_json, 'r', encoding='utf-8') as f:
            data = json.load(f)
            current_version = data.get('version', '0.0.0')
    
    print(f"📋 当前版本：v{current_version}")
    
    # 计算新版本
    new_version = bump_version(current_version, args.bump)
    print(f"📋 新版本：v{new_version}\n")
    
    # 1. 更新版本号（使用 JSON 解析，100% 可靠）
    print("━━━ 步骤 1: 更新版本号 ━━━")
    update_json_file(package_json, new_version)
    update_json_file(meta_json, new_version)
    
    # 2. 更新 README 更新日志（使用正则表达式，可靠）
    print("\n━━━ 步骤 2: 更新 README.md ━━━")
    readme_path = os.path.join(skill_path, 'README.md')
    update_readme_changelog(readme_path, new_version, args.changelog)
    
    # 3. Git 提交和推送
    if not args.skip_git:
        print("\n━━━ 步骤 3: Git 提交和推送 ━━━")
        # 如果是集合仓库，使用集合根目录
        git_root = args.collection_root if args.collection_root else skill_path
        init_git(git_root)
        git_commit_push(skill_path, new_version, args.changelog, git_root)
    
    # 4. 发布到 ClawHub
    if not args.skip_clawhub:
        print("\n━━━ 步骤 4: 发布到 ClawHub ━━━")
        success, skill_id = publish_to_clawhub(skill_path, args.slug, new_version, args.changelog)
        if not success:
            print("\n⚠️  ClawHub 发布失败，但文件已更新")
    
    print(f"\n{'='*60}")
    print(f"  ✅ 发布完成!")
    print(f"  版本：v{new_version}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
