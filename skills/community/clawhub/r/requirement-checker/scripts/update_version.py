#!/usr/bin/env python3
"""
版本更新辅助脚本
自动更新所有文件的版本号和版本历史
"""

import re
import json
import sys
from datetime import datetime
from pathlib import Path

def get_today():
    return datetime.now().strftime("%Y-%m-%d")

def update_version_history(file_path, version, changelog, date=None):
    """在版本历史表顶部插入新版本记录（如果不存在）"""
    if date is None:
        date = get_today()

    content = Path(file_path).read_text(encoding='utf-8')

    # 检查是否已存在该版本记录
    version_pattern = rf'\| \*\*v{re.escape(version)}\*\* \|'
    if re.search(version_pattern, content):
        # 已存在，更新该行的 changelog
        old_row_pattern = rf'(\| \*\*v{re.escape(version)}\*\* \| \*\*[\d-]+\*\* \| )([^\|]+)( \|)'
        new_row = f'| **v{version}** | **{date}** | **{changelog}** |'
        new_content = re.sub(old_row_pattern, new_row, content)
        if new_content != content:
            Path(file_path).write_text(new_content, encoding='utf-8')
            return True
        return False

    # 匹配版本历史表的模式
    pattern = r'(\| 版本 \| 日期 \| 更新内容 \|[\s\S]*?\|---+\|---+\|---+\|)'

    new_row = f'| **v{version}** | **{date}** | **{changelog}** |'

    def replacer(match):
        return match.group(1) + '\n' + new_row

    new_content = re.sub(pattern, replacer, content, count=1)

    if new_content != content:
        Path(file_path).write_text(new_content, encoding='utf-8')
        return True
    return False

def update_version_in_file(file_path, patterns):
    """更新文件中的版本号"""
    content = Path(file_path).read_text(encoding='utf-8')
    updated = False

    for pattern, replacement in patterns:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            content = new_content
            updated = True

    if updated:
        Path(file_path).write_text(content, encoding='utf-8')
    return updated

def main():
    if len(sys.argv) < 3:
        print("用法: python3 update_version.py <版本号> <changelog>")
        print("示例: python3 update_version.py 2.5.0 '🎯 新增建议分级体系'")
        sys.exit(1)

    version = sys.argv[1]
    changelog = sys.argv[2]
    date = get_today()

    project_dir = Path(__file__).parent.parent

    print(f"🔧 更新版本号到 {version}...")
    print(f"📝 Changelog: {changelog}")
    print(f"📅 日期: {date}")
    print()

    # 1. clawhub.json
    file_path = project_dir / "clawhub.json"
    if file_path.exists():
        data = json.loads(file_path.read_text(encoding='utf-8'))
        data['version'] = version
        data['meta']['releaseNotes'] = f"v{version}: {changelog}"
        data['meta']['updatedAt'] = date
        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f"   ✅ clawhub.json")

    # 2. install.json
    file_path = project_dir / "install.json"
    if file_path.exists():
        data = json.loads(file_path.read_text(encoding='utf-8'))
        data['version'] = version
        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f"   ✅ install.json")

    # 3. _meta.json
    file_path = project_dir / "_meta.json"
    if file_path.exists():
        data = json.loads(file_path.read_text(encoding='utf-8'))
        data['version'] = version
        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f"   ✅ _meta.json")

    # 4. config.json
    file_path = project_dir / "config.json"
    if file_path.exists():
        data = json.loads(file_path.read_text(encoding='utf-8'))
        data['version'] = version
        file_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f"   ✅ config.json")

    # 5. SKILL.md - 版本号 + 版本历史
    file_path = project_dir / "SKILL.md"
    if file_path.exists():
        update_version_in_file(file_path, [
            (r'version: [\d.]+', f'version: {version}'),
            (r'\*\*版本\*\*: v[\d.]+', f'**版本**: v{version}'),
        ])
        update_version_history(file_path, version, changelog, date)
        print(f"   ✅ SKILL.md (版本号 + 版本历史)")

    # 6. README.md - 版本号 + 版本历史
    file_path = project_dir / "README.md"
    if file_path.exists():
        update_version_in_file(file_path, [
            (r'\*\*版本\*\*: v[\d.]+', f'**版本**: v{version}'),
            (r'\*\*更新日期\*\*: [\d-]+', f'**更新日期**: {date}'),
        ])
        update_version_history(file_path, version, changelog, date)
        print(f"   ✅ README.md (版本号 + 版本历史)")

    # 7. references/checklist.md
    file_path = project_dir / "references" / "checklist.md"
    if file_path.exists():
        update_version_in_file(file_path, [
            (r'\*\*版本\*\*: [\d.]+', f'**版本**: {version}'),
        ])
        update_version_history(file_path, version, changelog, date)
        print(f"   ✅ references/checklist.md")

    print()
    print(f"✅ 所有文件已更新到 v{version}")

if __name__ == '__main__':
    main()