#!/usr/bin/env python3
"""
版本管理工具 - 精简版
"""

import json
import sys
from pathlib import Path
from datetime import datetime

class VersionManager:
    """版本管理器（精简版）"""
    
    def __init__(self, skill_dir=None):
        if skill_dir is None:
            skill_dir = Path(__file__).parent.parent
        
        self.skill_dir = Path(skill_dir)
        self.version_file = self.skill_dir / "version.json"
    
    def get_current_version(self):
        """获取当前版本"""
        if self.version_file.exists():
            try:
                with open(self.version_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data.get("current_version", "0.0.0")
            except:
                return "0.0.0"
        return "0.0.0"
    
    def update_version(self, new_version, changelog_items=None):
        """更新版本信息"""
        if self.version_file.exists():
            with open(self.version_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {
                "skill_name": "today-task",
                "display_name": "负一屏任务推送",
                "current_version": "0.0.0",
                "release_date": "",
                "changelog": {}
            }
        
        # 更新版本信息
        old_version = data.get("current_version", "0.0.0")
        data["current_version"] = new_version
        data["release_date"] = datetime.now().strftime("%Y-%m-%d")
        
        # 更新更新日志
        if changelog_items:
            if "changelog" not in data:
                data["changelog"] = {}
            
            data["changelog"][new_version] = changelog_items
        
        # 保存文件
        with open(self.version_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"[成功] 版本已更新: {old_version} → {new_version}")
        return True
    
    def show_info(self):
        """显示版本信息"""
        if self.version_file.exists():
            with open(self.version_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"[技能] {data.get('display_name', '未知')}")
            print(f"[版本] {data.get('current_version', '0.0.0')}")
            print(f"[日期] {data.get('release_date', '未知')}")
            
            changelog = data.get("changelog", {})
            if changelog:
                print(f"\n[更新日志]:")
                for version, items in sorted(changelog.items(), reverse=True):
                    print(f"  {version}:")
                    if isinstance(items, list):
                        for item in items:
                            print(f"    - {item}")
            
            return True
        else:
            print("[错误] 版本文件不存在")
            return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="技能版本管理")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # show命令
    subparsers.add_parser("show", help="显示版本信息")
    
    # update命令
    update_parser = subparsers.add_parser("update", help="更新版本")
    update_parser.add_argument("version", help="新版本号")
    update_parser.add_argument("-c", "--changelog", nargs="+", help="更新日志")
    
    args = parser.parse_args()
    
    manager = VersionManager()
    
    if args.command == "show":
        manager.show_info()
    elif args.command == "update":
        manager.update_version(args.version, args.changelog)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()