#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Swagger 2 到 OpenAPI 3.0 - 仅迁移 Import 语句
此脚本只处理 import 语句替换，不处理注解
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


class ImportMigrator:
    """Import 迁移器 - 仅处理 import 语句替换"""
    
    def __init__(self, project_path: str, dry_run: bool = False):
        self.project_path = Path(project_path).resolve()
        self.dry_run = dry_run
        self.stats = {
            'files_processed': 0,
            'files_modified': 0,
            'imports_replaced': 0,
        }
    
    # ========== Import 替换规则 ==========
    
    IMPORT_RULES = [
        # ===== Swagger 注解包替换 =====
        
        # 基础注解
        {
            'old': 'import io.swagger.annotations.Api;',
            'new': 'import io.swagger.v3.oas.annotations.tags.Tag;',
            'category': 'swagger'
        },
        {
            'old': 'import io.swagger.annotations.ApiOperation;',
            'new': 'import io.swagger.v3.oas.annotations.Operation;',
            'category': 'swagger'
        },
        {
            'old': 'import io.swagger.annotations.ApiParam;',
            'new': 'import io.swagger.v3.oas.annotations.Parameter;',
            'category': 'swagger'
        },
        
        # 模型注解
        {
            'old': 'import io.swagger.annotations.ApiModel;',
            'new': 'import io.swagger.v3.oas.annotations.media.Schema;',
            'category': 'swagger'
        },
        {
            'old': 'import io.swagger.annotations.ApiModelProperty;',
            'new': 'import io.swagger.v3.oas.annotations.media.Schema;',
            'category': 'swagger'
        },
        
        # 响应注解
        {
            'old': 'import io.swagger.annotations.ApiResponse;',
            'new': 'import io.swagger.v3.oas.annotations.responses.ApiResponse;',
            'category': 'swagger'
        },
        {
            'old': 'import io.swagger.annotations.ApiResponses;',
            'new': 'import io.swagger.v3.oas.annotations.responses.ApiResponses;',
            'category': 'swagger'
        },
        
        # 隐式参数
        {
            'old': 'import io.swagger.annotations.ApiImplicitParam;',
            'new': 'import io.swagger.v3.oas.annotations.Parameter;',
            'category': 'swagger'
        },
        {
            'old': 'import io.swagger.annotations.ApiImplicitParams;',
            'new': 'import io.swagger.v3.oas.annotations.Parameters;',
            'category': 'swagger'
        },
        
        # 扩展注解
        {
            'old': 'import io.swagger.annotations.Extension;',
            'new': 'import io.swagger.v3.oas.annotations.extensions.Extension;',
            'category': 'swagger'
        },
        {
            'old': 'import io.swagger.annotations.ExtensionProperty;',
            'new': 'import io.swagger.v3.oas.annotations.extensions.ExtensionProperty;',
            'category': 'swagger'
        },
        
        # 通配符导入
        {
            'old': 'import io.swagger.annotations.*;',
            'new': 'import io.swagger.v3.oas.annotations.*;',
            'category': 'swagger'
        },
        
        # ===== Jakarta EE 迁移 =====
        
        {
            'old': 'import javax.annotation.Resource;',
            'new': 'import jakarta.annotation.Resource;',
            'category': 'jakarta'
        },
        {
            'old': 'import javax.annotation.PostConstruct;',
            'new': 'import jakarta.annotation.PostConstruct;',
            'category': 'jakarta'
        },
        {
            'old': 'import javax.persistence.',
            'new': 'import jakarta.persistence.',
            'category': 'jakarta'
        },
        {
            'old': 'import javax.validation.',
            'new': 'import jakarta.validation.',
            'category': 'jakarta'
        },
        {
            'old': 'import javax.servlet.',
            'new': 'import jakarta.servlet.',
            'category': 'jakarta'
        },
        {
            'old': 'import javax.annotation.',
            'new': 'import jakarta.annotation.',
            'category': 'jakarta'
        },
    ]
    
    def find_java_files(self) -> List[Path]:
        """查找项目中所有的 Java 文件"""
        java_files = []
        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in ['.git', '.idea', 'target', 'build', 'node_modules']]
            for file in files:
                if file.endswith('.java'):
                    java_files.append(Path(root) / file)
        return java_files
    
    def migrate_imports_in_file(self, content: str) -> Tuple[str, int]:
        """迁移文件中的 import 语句"""
        count = 0
        
        for rule in self.IMPORT_RULES:
            old_import = rule['old']
            new_import = rule['new']
            
            # 使用正则表达式进行整行匹配
            pattern = r'^' + re.escape(old_import) + r'\b.*?$'
            new_content, n = re.subn(pattern, new_import, content, flags=re.MULTILINE)
            
            if n > 0:
                content = new_content
                count += n
                if self.dry_run:
                    print(f"  [Import替换]: {old_import} -> {new_import}")
        
        return content, count
    
    def process_file(self, file_path: Path) -> bool:
        """处理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 迁移 import
            content, import_count = self.migrate_imports_in_file(content)
            
            self.stats['files_processed'] += 1
            
            if content != original_content:
                self.stats['files_modified'] += 1
                self.stats['imports_replaced'] += import_count
                
                if not self.dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✓ 已修改: {file_path.relative_to(self.project_path)} ({import_count} 处 import 替换)")
                else:
                    print(f"[Dry Run] 将修改: {file_path.relative_to(self.project_path)} ({import_count} 处 import 替换)")
                
                return True
            
            return False
            
        except Exception as e:
            print(f"✗ 错误处理文件 {file_path}: {e}")
            return False
    
    def migrate(self):
        """执行迁移"""
        print(f"{'='*60}")
        print(f"Swagger 2 → OpenAPI 3.0 Import 迁移工具")
        print(f"项目路径: {self.project_path}")
        print(f"模式: {'预览 (dry-run)' if self.dry_run else '实际执行'}")
        print(f"{'='*60}\n")
        
        # 查找所有 Java 文件
        java_files = self.find_java_files()
        print(f"找到 {len(java_files)} 个 Java 文件\n")
        
        if not java_files:
            print("未找到 Java 文件，请检查项目路径")
            return
        
        # 处理每个文件
        for file_path in java_files:
            self.process_file(file_path)
        
        # 打印统计信息
        print(f"\n{'='*60}")
        print("迁移统计:")
        print(f"{'='*60}")
        print(f"处理文件数: {self.stats['files_processed']}")
        print(f"修改文件数: {self.stats['files_modified']}")
        print(f"Import 替换数: {self.stats['imports_replaced']}")
        
        if self.dry_run:
            print(f"\n这是预览模式，实际未修改文件。")
            print(f"如需执行实际迁移，请去掉 --dry-run 参数")


def main():
    parser = argparse.ArgumentParser(
        description='Swagger 2 到 OpenAPI 3.0 Import 迁移工具 - 仅处理 import 语句替换',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 预览模式（不实际修改文件）
  python migrate_imports.py --project-path /path/to/project --dry-run
  
  # 实际执行迁移
  python migrate_imports.py --project-path /path/to/project
  
注意：此脚本仅替换 import 语句，不处理注解。如需同时替换注解，请使用 migrate_annotations.py 或 migrate_swagger_to_openapi.py
        """
    )
    
    parser.add_argument(
        '--project-path',
        required=True,
        help='Java 项目的路径'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式 - 显示将要做的修改但不实际执行'
    )
    
    args = parser.parse_args()
    
    # 验证项目路径
    if not os.path.exists(args.project_path):
        print(f"错误: 项目路径不存在: {args.project_path}")
        sys.exit(1)
    
    # 执行迁移
    migrator = ImportMigrator(
        project_path=args.project_path,
        dry_run=args.dry_run
    )
    migrator.migrate()


if __name__ == '__main__':
    main()
