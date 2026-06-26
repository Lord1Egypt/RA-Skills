#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Swagger 2 到 OpenAPI 3.0 - 仅迁移注解
此脚本只处理注解替换，不处理 import 语句
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


class AnnotationMigrator:
    """注解迁移器 - 仅处理注解替换"""
    
    def __init__(self, project_path: str, dry_run: bool = False):
        self.project_path = Path(project_path).resolve()
        self.dry_run = dry_run
        self.stats = {
            'files_processed': 0,
            'files_modified': 0,
            'replacements': 0,
        }
    
    ANNOTATION_RULES = [
        # @Api -> @Tag
        {
            'name': 'Api-tags',
            'pattern': r'@Api\s*\(\s*tags?\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Tag(name = "\1")',
        },
        {
            'name': 'Api-value',
            'pattern': r'@Api\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Tag(name = "\1")',
        },
        {
            'name': 'Api-description',
            'pattern': r'@Api\s*\(\s*description\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Tag(name = "\1")',
        },
        
        # @ApiOperation -> @Operation
        {
            'name': 'ApiOperation-value',
            'pattern': r'@ApiOperation\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Operation(summary = "\1")',
        },
        {
            'name': 'ApiOperation-value-notes',
            'pattern': r'@ApiOperation\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*,\s*notes\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Operation(summary = "\1", description = "\2")',
        },
        {
            'name': 'ApiOperation-notes',
            'pattern': r'@ApiOperation\s*\(\s*notes\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Operation(description = "\1")',
        },
        
        # @ApiParam -> @Parameter
        {
            'name': 'ApiParam-value',
            'pattern': r'@ApiParam\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Parameter(description = "\1")',
        },
        {
            'name': 'ApiParam-name',
            'pattern': r'@ApiParam\s*\(\s*name\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Parameter(name = "\1")',
        },
        
        # @ApiModel -> @Schema
        {
            'name': 'ApiModel-value',
            'pattern': r'@ApiModel\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Schema(description = "\1")',
        },
        {
            'name': 'ApiModel-description',
            'pattern': r'@ApiModel\s*\(\s*description\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Schema(description = "\1")',
        },
        
        # @ApiModelProperty -> @Schema
        {
            'name': 'ApiModelProperty-value',
            'pattern': r'@ApiModelProperty\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Schema(description = "\1")',
        },
        {
            'name': 'ApiModelProperty-name',
            'pattern': r'@ApiModelProperty\s*\(\s*name\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Schema(name = "\1")',
        },
        
        # @ApiImplicitParam -> @Parameter
        {
            'name': 'ApiImplicitParam-value',
            'pattern': r'@ApiImplicitParam\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Parameter(description = "\1")',
        },
        {
            'name': 'ApiImplicitParam-name',
            'pattern': r'@ApiImplicitParam\s*\(\s*name\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Parameter(name = "\1")',
        },
        
        # @ApiImplicitParams -> @Parameters
        {
            'name': 'ApiImplicitParams',
            'pattern': r'@ApiImplicitParams',
            'replacement': r'@Parameters',
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
    
    def migrate_file(self, file_path: Path) -> bool:
        """迁移单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            total_replacements = 0
            
            for rule in self.ANNOTATION_RULES:
                pattern = rule['pattern']
                replacement = rule['replacement']
                new_content, count = re.subn(pattern, replacement, content)
                if count > 0:
                    content = new_content
                    total_replacements += count
                    if self.dry_run:
                        print(f"  [{rule['name']}]: {count} 处替换")
            
            self.stats['files_processed'] += 1
            
            if content != original:
                self.stats['files_modified'] += 1
                self.stats['replacements'] = self.stats.get('replacements', 0) + total_replacements
                
                if not self.dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✓ 已修改: {file_path.relative_to(self.project_path)} ({total_replacements} 处替换)")
                else:
                    print(f"[Dry Run] 将修改: {file_path.relative_to(self.project_path)} ({total_replacements} 处替换)")
                
                return True
            
            return False
            
        except Exception as e:
            print(f"✗ 错误处理文件 {file_path}: {e}")
            return False
    
    def migrate(self):
        """执行迁移"""
        print(f"{'='*60}")
        print(f"Swagger 2 → OpenAPI 3.0 注解迁移工具")
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
            self.migrate_file(file_path)
        
        # 打印统计信息
        print(f"\n{'='*60}")
        print("迁移统计:")
        print(f"{'='*60}")
        print(f"处理文件数: {self.stats['files_processed']}")
        print(f"修改文件数: {self.stats['files_modified']}")
        print(f"注解替换数: {self.stats.get('replacements', 0)}")
        
        if self.dry_run:
            print(f"\n这是预览模式，实际未修改文件。")
            print(f"如需执行实际迁移，请去掉 --dry-run 参数")


def main():
    parser = argparse.ArgumentParser(
        description='Swagger 2 到 OpenAPI 3.0 注解迁移工具 - 仅处理注解，不处理 import',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 预览模式（不实际修改文件）
  python migrate_annotations.py --project-path /path/to/project --dry-run
  
  # 实际执行迁移
  python migrate_annotations.py --project-path /path/to/project
  
注意：此脚本仅替换注解，不处理 import 语句。如需同时替换 import，请使用 migrate_imports.py 或 migrate_swagger_to_openapi.py
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
    migrator = AnnotationMigrator(
        project_path=args.project_path,
        dry_run=args.dry_run
    )
    migrator.migrate()


if __name__ == '__main__':
    main()
