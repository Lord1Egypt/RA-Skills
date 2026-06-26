#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
上传 Universal AutoStart 技能到 SkillHub（仅纯文本文件）
"""

import os
import sys
import zipfile
import requests

# 配置
SKILLHUB_API_KEY = "sk-skillhubs-JNpqszhN_oGF3u3xGEAMpJIjG6V2_etC"
SKILLHUB_BASE_URL = "https://www.skillhub.club/api/v1"
SKILL_FOLDER = r"C:\Users\Administrator\.copaw\workspaces\default\skills\universal-autostart"

# 允许的纯文本文件扩展名
ALLOWED_EXTENSIONS = [
    '.py', '.sh', '.txt', '.md', '.json', '.yaml', '.yml',
    '.toml', '.cfg', '.ini', '.conf', '.example', '.license',
    '.gitignore', '.version'
]

# 需要排除的文件和目录
EXCLUDE_FILES = [
    'publish_to_skillhub.py',  # 上传脚本不需要包含
    '.git', '.github', '__pycache__', '.pyc',
    'oldfile', 'temp-check', 'temp'
]

def is_text_file(filename):
    """检查是否为纯文本文件"""
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXTENSIONS or filename.lower() in ['license', 'version.txt', 'version']

def should_exclude(filename):
    """检查是否应该排除"""
    for exclude in EXCLUDE_FILES:
        if exclude.lower() in filename.lower():
            return True
    return False

def create_skill_package(skill_path, output_path):
    """创建纯文本技能压缩包"""
    print(f"[INFO] Packing skill (text-only): {skill_path}")
    
    file_count = 0
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_path):
            # 排除不需要的目录
            dirs[:] = [d for d in dirs if not should_exclude(d) and not d.startswith('.')]
            
            for file in files:
                # 排除不必要文件
                if should_exclude(file) or file.startswith('.'):
                    continue
                    
                # 只包含纯文本文件
                if not is_text_file(file):
                    print(f"  - Skipping non-text: {file}")
                    continue
                    
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, skill_path)
                
                print(f"  + {arc_name}")
                zipf.write(file_path, arc_name)
                file_count += 1
    
    print(f"[OK] Skill package created: {output_path}")
    print(f"[INFO] Total text files: {file_count}")
    return output_path

def upload_to_skillhub(skill_package_path):
    """上传到 SkillHub"""
    print("\n[INFO] Uploading to SkillHub...")
    
    url = f"{SKILLHUB_BASE_URL}/skills"
    
    headers = {
        "Authorization": f"Bearer {SKILLHUB_API_KEY}"
    }
    
    with open(skill_package_path, 'rb') as f:
        files = {
            'skill': ('universal-autostart.skill', f, 'application/zip')
        }
        
        data = {
            'name': 'Universal AutoStart Service Manager',
            'slug': 'universal-autostart',
            'version': '1.1.0',
            'description': 'Cross-platform auto-start service manager for Windows and macOS. Supports installing, uninstalling, starting, stopping, and monitoring services with automatic restart. Use when you need to set up persistent background services that survive system reboots on Windows (sc/schtasks) or macOS (launchd).'
        }
        
        try:
            response = requests.post(url, headers=headers, files=files, data=data, timeout=120)
            
            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                print("[OK] Upload successful!")
                print(f"\nSkill details:")
                print(f"  Name: {result.get('name')}")
                print(f"  Slug: {result.get('slug')}")
                print(f"  Version: {result.get('version')}")
                print(f"  URL: https://www.skillhub.club/skills/{result.get('slug')}")
                return True
            else:
                print(f"[ERROR] Upload failed (HTTP {response.status_code})")
                print(f"Response: {response.text}")
                return False
                
        except requests.exceptions.Timeout:
            print("[ERROR] Request timeout, please check network connection")
            return False
        except Exception as e:
            print(f"[ERROR] Upload error: {e}")
            return False

def main():
    """Main function"""
    print("=" * 60)
    print("  Universal AutoStart - SkillHub Publisher (Text-Only)")
    print("=" * 60)
    print()
    
    # Check skill folder
    if not os.path.exists(SKILL_FOLDER):
        print(f"[ERROR] Skill folder does not exist: {SKILL_FOLDER}")
        return False
    
    # Create skill package
    package_name = "universal-autostart.skill"
    package_path = os.path.join(os.path.dirname(SKILL_FOLDER), package_name)
    
    try:
        create_skill_package(SKILL_FOLDER, package_path)
        
        # Upload
        success = upload_to_skillhub(package_path)
        
        if success:
            print("\n" + "=" * 60)
            print("  [SUCCESS] Publishing complete!")
            print("=" * 60)
        else:
            print("\n[WARNING] Publishing failed, please try again later")
            print(f"[INFO] Skill package saved at: {package_path}")
            print("[INFO] You can manually upload via: https://www.skillhub.club/dashboard")
        
        return success
        
    finally:
        pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)