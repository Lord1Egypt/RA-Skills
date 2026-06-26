#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
回滚模块
恢复SDK集成前的所有修改
"""

import os
import sys
import shutil
import argparse
from typing import Tuple


class Rollback:
    """SDK集成回滚器"""
    
    def __init__(self, backup_dir: str, project_path: str):
        self.backup_dir = os.path.abspath(backup_dir)
        self.project_path = os.path.abspath(project_path)
    
    def rollback(self) -> Tuple[bool, str]:
        """
        执行回滚(恢复整个工程目录)
        
        Returns:
            (是否成功, 详细信息)
        """
        print("\n🔄 开始回滚SDK集成...\n")
        
        # 验证备份目录
        if not os.path.exists(self.backup_dir):
            return False, f"备份目录不存在: {self.backup_dir}"
        
        print(f"📁 备份目录: {self.backup_dir}")
        print(f"📂 项目路径: {self.project_path}\n")
        
        try:
            # 删除当前工程目录
            print("🗑️  删除当前工程目录...")
            if os.path.exists(self.project_path):
                shutil.rmtree(self.project_path)
                print(f"  ✅ 已删除: {self.project_path}")
            
            # 恢复备份的工程目录
            print("\n📂 恢复备份的工程目录...")
            shutil.copytree(self.backup_dir, self.project_path)
            print(f"  ✅ 已恢复: {self.project_path}")
            
            print(f"\n✅ 回滚完成")
            print(f"   工程已恢复到集成前状态\n")
            
            return True, "回滚完成"
            
        except Exception as e:
            print(f"\n❌ 回滚失败: {str(e)}\n")
            return False, f"回滚失败: {str(e)}"
    
    def _restore_files(self) -> int:
        """恢复备份的文件"""
        print("恢复备份文件...")
        
        restored_count = 0
        
        # 遍历备份目录
        for root, dirs, files in os.walk(self.backup_dir):
            for file in files:
                backup_file = os.path.join(root, file)
                
                # 计算相对路径
                rel_path = os.path.relpath(backup_file, self.backup_dir)
                target_file = os.path.join(self.project_path, rel_path)
                
                # 恢复文件
                if os.path.exists(target_file):
                    shutil.copy2(backup_file, target_file)
                    print(f"  ✅ 恢复: {rel_path}")
                    restored_count += 1
                else:
                    print(f"  ⚠️  目标文件不存在(可能已删除): {rel_path}")
        
        return restored_count
    
    def _delete_new_files(self) -> int:
        """删除SDK集成可能新增的文件"""
        print("\n检查新增文件...")
        
        deleted_count = 0
        
        # 检查可能的Application类文件
        app_module = self._find_app_module()
        
        if app_module:
            src_main = os.path.join(self.project_path, app_module, 'src', 'main')
            
            # 在java和kotlin目录中查找UmengApplication
            for subdir in ['java', 'kotlin']:
                base_dir = os.path.join(src_main, subdir)
                if os.path.exists(base_dir):
                    for root, dirs, files in os.walk(base_dir):
                        if 'UmengApplication.kt' in files or 'UmengApplication.java' in files:
                            # 询问用户是否删除
                            umeng_app = os.path.join(root, 'UmengApplication.kt')
                            if not os.path.exists(umeng_app):
                                umeng_app = os.path.join(root, 'UmengApplication.java')
                            
                            rel_path = os.path.relpath(umeng_app, self.project_path)
                            print(f"  发现SDK创建的Application类: {rel_path}")
                            
                            # 检查是否在备份中(如果备份中有说明是修改而非新建)
                            backup_umeng_app = os.path.join(self.backup_dir, rel_path)
                            if not os.path.exists(backup_umeng_app):
                                # 备份中没有,说明是新建的文件
                                confirm = input(f"  是否删除此文件? (y/n, 默认y): ").strip().lower()
                                if confirm != 'n':
                                    os.remove(umeng_app)
                                    print(f"  ✅ 删除: {rel_path}")
                                    deleted_count += 1
                            else:
                                print(f"  ⚠️  文件已存在于备份中,跳过删除")
        
        return deleted_count
    
    def _find_app_module(self) -> str:
        """查找app模块名称"""
        # 常见模块名
        for module in ['app', 'main', 'mobile']:
            module_path = os.path.join(self.project_path, module)
            if os.path.exists(module_path) and os.path.isdir(module_path):
                # 检查是否有build.gradle文件
                if (os.path.exists(os.path.join(module_path, 'build.gradle.kts')) or
                    os.path.exists(os.path.join(module_path, 'build.gradle'))):
                    return module
        
        return None
    
    def verify_rollback(self) -> bool:
        """验证回滚是否成功"""
        print("\n验证回滚结果...")
        
        # 检查工程目录是否存在
        if not os.path.exists(self.project_path):
            print("  ❌ 工程目录不存在")
            return False
        
        # 检查关键文件是否存在
        required_files = [
            'build.gradle.kts',
            'settings.gradle.kts',
            'gradle.properties'
        ]
        
        all_exist = True
        for file in required_files:
            file_path = os.path.join(self.project_path, file)
            if not os.path.exists(file_path):
                # 检查Groovy版本
                if file.endswith('.kts'):
                    groovy_file = file.replace('.kts', '')
                    file_path = os.path.join(self.project_path, groovy_file)
            
            if os.path.exists(file_path):
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file} 不存在")
                all_exist = False
        
        if all_exist:
            print("\n✅ 回滚验证通过\n")
        else:
            print("\n⚠️  回滚验证未通过,请手动检查\n")
        
        return all_exist


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='友盟统计SDK集成回滚工具')
    
    parser.add_argument(
        '--backup-dir',
        required=True,
        help='备份目录路径'
    )
    
    parser.add_argument(
        '--project-path',
        required=True,
        help='Android项目路径'
    )
    
    args = parser.parse_args()
    
    rollback = Rollback(args.backup_dir, args.project_path)
    success, message = rollback.rollback()
    
    if success:
        # 验证回滚
        rollback.verify_rollback()
        print("✅ 回滚成功")
        sys.exit(0)
    else:
        print(f"❌ 回滚失败: {message}")
        sys.exit(1)


if __name__ == '__main__':
    main()

