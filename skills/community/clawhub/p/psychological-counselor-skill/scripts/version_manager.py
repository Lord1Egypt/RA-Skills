
#!/usr/bin/env python3
"""
版本管理工具
"""

import os
import json
import argparse
import shutil
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="版本管理工具")
    parser.add_argument("--action", choices=["rollback", "list", "archive"], required=True, help="操作类型")
    parser.add_argument("--slug", required=True, help="咨询师代号")
    parser.add_argument("--version", help="版本号（回滚时需要）")
    parser.add_argument("--base-dir", default="./counselors", help="基础目录")
    return parser.parse_args()

def archive_version(slug, base_dir):
    """存档当前版本"""
    counselor_dir = os.path.join(base_dir, slug)
    versions_dir = os.path.join(counselor_dir, "versions")
    
    if not os.path.exists(counselor_dir):
        print(f"咨询师 {slug} 不存在")
        return False
    
    if not os.path.exists(versions_dir):
        os.makedirs(versions_dir)
    
    version = datetime.now().strftime("%Y%m%d_%H%M%S")
    version_dir = os.path.join(versions_dir, version)
    
    # 存档当前版本
    for file in ["SKILL.md", "counselor.md", "meta.json"]:
        src = os.path.join(counselor_dir, file)
        if os.path.exists(src):
            if not os.path.exists(version_dir):
                os.makedirs(version_dir)
            shutil.copy2(src, os.path.join(version_dir, file))
    
    print(f"版本 {version} 已存档")
    return version

def list_versions(slug, base_dir):
    """列出所有版本"""
    versions_dir = os.path.join(base_dir, slug, "versions")
    
    if not os.path.exists(versions_dir):
        print("暂无版本记录")
        return
    
    versions = sorted([d for d in os.listdir(versions_dir) 
                      if os.path.isdir(os.path.join(versions_dir, d))], reverse=True)
    
    if not versions:
        print("暂无版本记录")
        return
    
    print("版本历史：")
    for version in versions:
        print(f"  - {version}")

def rollback_version(slug, version, base_dir):
    """回滚到指定版本"""
    counselor_dir = os.path.join(base_dir, slug)
    version_dir = os.path.join(counselor_dir, "versions", version)
    
    if not os.path.exists(version_dir):
        print(f"版本 {version} 不存在")
        return False
    
    # 先存档当前版本
    archive_version(slug, base_dir)
    
    # 回滚到指定版本
    for file in ["SKILL.md", "counselor.md", "meta.json"]:
        src = os.path.join(version_dir, file)
        dst = os.path.join(counselor_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
    
    print(f"已回滚到版本 {version}")
    return True

def main():
    args = parse_args()
    
    if args.action == "archive":
        archive_version(args.slug, args.base_dir)
    elif args.action == "list":
        list_versions(args.slug, args.base_dir)
    elif args.action == "rollback":
        if not args.version:
            print("回滚需要指定 --version")
            return
        rollback_version(args.slug, args.version, args.base_dir)

if __name__ == "__main__":
    main()
