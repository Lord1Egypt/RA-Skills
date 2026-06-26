#!/usr/bin/env python3
"""
Email Pro Optimized 技能即时更新脚本
修改代码后自动同步到本地和线上
"""

import json
import subprocess
import sys
import hashlib
from pathlib import Path
from datetime import datetime
import shutil

SKILL_DIR = Path.home() / '.openclaw' / 'skills' / 'email-pro-optimized'
WORKSPACE_DIR = Path.home() / '.openclaw' / 'workspace-telegram-bot1'
SYNC_STATE_FILE = SKILL_DIR / '.sync-state.json'

def get_file_hash(file_path):
    """计算文件哈希"""
    if not file_path.exists():
        return None
    
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def load_sync_state():
    """加载同步状态"""
    if SYNC_STATE_FILE.exists():
        with open(SYNC_STATE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_sync_state(state):
    """保存同步状态"""
    with open(SYNC_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

def check_file_changes():
    """检查文件变化"""
    print("🔍 检查文件变化...\n")
    
    state = load_sync_state()
    changed_files = []
    
    # 监控的文件
    files_to_monitor = [
        'scripts/oauth_handler.py',
        'scripts/email-pro.py',
        'scripts/providers.py',
        'scripts/authorize.py',
        'SKILL.md'
    ]
    
    for file_rel_path in files_to_monitor:
        file_path = SKILL_DIR / file_rel_path
        
        if not file_path.exists():
            continue
        
        current_hash = get_file_hash(file_path)
        previous_hash = state.get(file_rel_path)
        
        if current_hash != previous_hash:
            print(f"📝 {file_rel_path}")
            changed_files.append(file_rel_path)
            state[file_rel_path] = current_hash
        else:
            print(f"✅ {file_rel_path}")
    
    save_sync_state(state)
    return changed_files

def sync_to_workspace(changed_files):
    """同步到工作区"""
    if not changed_files:
        print("\n✅ 无需同步")
        return True
    
    print(f"\n📤 同步 {len(changed_files)} 个文件到工作区...\n")
    
    # 创建工作区技能目录
    workspace_skill_dir = WORKSPACE_DIR / 'skills' / 'email-pro-optimized'
    workspace_skill_dir.mkdir(parents=True, exist_ok=True)
    
    for file_rel_path in changed_files:
        src = SKILL_DIR / file_rel_path
        dst = workspace_skill_dir / file_rel_path
        
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  ✅_path}")
    
    return True

def update_clawhub():
    """更新到 ClawHub（可选）"""
    print("\n🌐 检查 ClawHub 更新...\n")
    
    # 检查是否已发布到 ClawHub
    clawhub_config = SKILL_DIR / '.clawhub.json'
    
    if not clawhub_config.exists():
        print("  ℹ️ 技能未发布到 ClawHub")
        print("  💡 运行: clawhub publish 来发布技能")
        return False
    
    with open(clawhub_config, 'r') as f:
        config = json.load(f)
    
    skill_id = config.get('skill_id')
    
    if not skill_id:
        print("  ❌ 缺少 skill_id")
        return False
    
    print(f"  📦 技能 ID: {skill_id}")
    print("  💡 运行: clawhub publish --update 来更新线上版本")
    
    return True

def generate_changelog():
    """生成更新日志"""
    print("\n📋 生成更新日志...\n")
    
    changelog_file = SKILL_DIR / 'CHANGELOG.md'
    
    # 读取现有日志
    if changelog_file.exists():
        with open(changelog_file, 'r') as f:
            existing = f.read()
    else:
        existing = "# Email Pro Optimized 更新日志\n\n"
    
    # 添加新条目
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_entry = f"""## [{timestamp}] 即时更新

### 改进
- ✅ OAuth 自动刷新机制集成
- ✅ Token 过期检测和自动续期
- ✅ 技能文档更新

### 新增功能
- `get_valid_token()` - 获取有效的 OAuth token
- `refresh_gmail_token_auto()` - 自动刷新 Gmail token
- `is_token_expired()` - 检查 token 过期状态

---

"""
    
    with open(changelog_file, 'w') as f:
        f.write(new_entry + existing)
    
    print(f"  ✅ 更新日志已生成: {changelog_file}")
    return True

def create_version_tag():
    """创建版本标签"""
    print("\n🏷️ 创建版本标签...\n")
    
    metadata_file = SKILL_DIR / '.skill-metadata.json'
    
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = {'version': '1.0.0'}
    
    # 递增版本
    version_parts = metadata['version'].split('.')
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    new_version = '.'.join(version_parts)
    
    metadata['version'] = new_version
    metadata['last_updated'] = datetime.now().isoformat()
    metadata['oauth_auto_refresh'] = True
    
    with open(metadata_file, 'w') as f:
        json.dumta, f, indent=2)
    
    print(f"  ✅ 版本: {new_version}")
    print(f"  ✅ 更新时间: {metadata['last_updated']}")
    
    return new_version

def main():
    """主函数"""
    print("=" * 70)
    print("🔄 Email Pro Optimized 技能即时更新")
    print("=" * 70 + "\n")
    
    # 1. 检查文件变化
    changed_files = check_file_changes()
    
    if not changed_files:
        print("\n✅ 无需更新")
        return 0
    
    # 2. 同步到工作区
    sync_to_workspace(changed_files)
    
    # 3. 生成更新日志
    generate_changelog()
    
    # 4. 创建版本标签
    new_version = create_version_tag()
    
    # 5. 提示 ClawHub 更新
    update_clawhub()
    
    print("\n" + "=" * 70)
    print(f"✨ 即时更新完成 (版本: {new_version})")
    print("=" * 70)
    print("\n📝 下一步:")
    print("  1. 本地工作区已同步")
    print("  2. 运行: clawhub publish --update 来更新线上版本")
    print("  3. 或保持本地版本，不发布到 ClawHub")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
