#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Swagger 2 到 OpenAPI 3.0 完整迁移脚本
包含注解替换和包名替换
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import List, Tuple


class SwaggerToOpenApiMigrator:
    """Swagger 2 到 OpenAPI 3.0 迁移器"""
    
    def __init__(self, project_path: str, dry_run: bool = False):
        self.project_path = Path(project_path).resolve()
        self.dry_run = dry_run
        self.stats = {
            'files_processed': 0,
            'files_modified': 0,
            'annotations_replaced': 0,
            'imports_replaced': 0,
        }
    
    # ========== 注解替换规则 ==========
    
    ANNOTATION_RULES = [
        # @Api -> @Tag
        {
            'pattern': r'@Api\s*\(\s*tags?\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Tag(name = "\1")',
            'description': '@Api(tags) -> @Tag(name)'
        },
        {
            'pattern': r'@Api\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Tag(name = "\1")',
            'description': '@Api(value) -> @Tag(name)'
        },
        
        # @ApiOperation -> @Operation
        {
            'pattern': r'@ApiOperation\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Operation(summary = "\1")',
            'description': '@ApiOperation(value) -> @Operation(summary)'
        },
        {
            'pattern': r'@ApiOperation\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*,\s*notes\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Operation(summary = "\1", description = "\2")',
            'description': '@ApiOperation(value, notes) -> @Operation(summary, description)'
        },
        
        # @ApiParam -> @Parameter
        {
            'pattern': r'@ApiParam\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Parameter(description = "\1")',
            'description': '@ApiParam(value) -> @Parameter(description)'
        },
        
        # @ApiModel -> @Schema
        {
            'pattern': r'@ApiModel\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Schema(description = "\1")',
            'description': '@ApiModel(value) -> @Schema(description)'
        },
        {
            'pattern': r'@ApiModel\s*\(\s*description\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Schema(description = "\1")',
            'description': '@ApiModel(description) -> @Schema(description)'
        },
        
        # @ApiModelProperty -> @Schema
        {
            'pattern': r'@ApiModelProperty\s*\(\s*value\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Schema(description = "\1")',
            'description': '@ApiModelProperty(value) -> @Schema(description)'
        },
        {
            'pattern': r'@ApiModelProperty\s*\(\s*name\s*=\s*["\']([^"\']+)["\']\s*\)',
            'replacement': r'@Schema(name = "\1")',
            'description': '@ApiModelProperty(name) -> @Schema(name)'
        },
    ]
    
    # ========== 包名替换规则 ==========
    
    IMPORT_RULES = [
        # Swagger 包替换
        ('io.swagger.annotations.Api', 'io.swagger.v3.oas.annotations.tags.Tag'),
        ('io.swagger.annotations.ApiOperation', 'io.swagger.v3.oas.annotations.Operation'),
        ('io.swagger.annotations.ApiParam', 'io.swagger.v3.oas.annotations.Parameter'),
        ('io.swagger.annotations.ApiModel', 'io.swagger.v3.oas.annotations.media.Schema'),
        ('io.swagger.annotations.ApiModelProperty', 'io.swagger.v3.oas.annotations.media.Schema'),
        ('io.swagger.annotations.ApiResponse', 'io.swagger.v3.oas.annotations.responses.ApiResponse'),
        ('io.swagger.annotations.ApiResponses', 'io.swagger.v3.oas.annotations.responses.ApiResponses'),
        ('io.swagger.annotations.ApiImplicitParam', 'io.swagger.v3.oas.annotations.Parameter'),
        ('io.swagger.annotations.ApiImplicitParams', 'io.swagger.v3.oas.annotations.Parameters'),
        ('io.swagger.annotations.Extension', 'io.swagger.v3.oas.annotations.extensions.Extension'),
        ('io.swagger.annotations.ExtensionProperty', 'io.swagger.v3.oas.annotations.extensions.ExtensionProperty'),
        
        # 包级替换
        ('import io.swagger.annotations.*', 'import io.swagger.v3.oas.annotations.*'),
        ('import io.swagger.annotations', 'import io.swagger.v3.oas.annotations'),
        
        # javax → jakarta
        ('javax.annotation.Resource', 'jakarta.annotation.Resource'),
        ('javax.annotation.PostConstruct', 'jakarta.annotation.PostConstruct'),
        ('javax.persistence', 'jakarta.persistence'),
        ('javax.validation', 'jakarta.validation'),
        ('javax.servlet', 'jakarta.servlet'),
    ]
    
    def find_java_files(self) -> List[Path]:
        """查找项目中所有的 Java 文件"""
        java_files = []
        for root, dirs, files in os.walk(self.project_path):
            # 排除常见的非源代码目录
            dirs[:] = [d for d in dirs if d not in ['.git', '.idea', 'target', 'build', 'node_modules']]
            for file in files:
                if file.endswith('.java'):
                    java_files.append(Path(root) / file)
        return java_files
    
    def replace_annotations(self, content: str) -> Tuple[str, int]:
        """替换注解"""
        count = 0
        for rule in self.ANNOTATION_RULES:
            new_content, n = re.subn(rule['pattern'], rule['replacement'], content)
            if n > 0:
                content = new_content
                count += n
                if self.dry_run:
                    print(f"  [{rule['description']}]: {n} 处替换")
        return content, count
    
    def replace_imports(self, content: str) -> Tuple[str, int]:
        """替换 import 语句"""
        count = 0
        for old, new in self.IMPORT_RULES:
            new_content, n = re.subn(rf'^{re.escape(old)}\b', new, content, flags=re.MULTILINE)
            if n > 0:
                content = new_content
                count += n
        return content, count
    
    def process_file(self, file_path: Path) -> bool:
        """处理单个文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 替换注解
            content, anno_count = self.replace_annotations(content)
            
            # 替换 import
            content, import_count = self.replace_imports(content)
            
            self.stats['files_processed'] += 1
            
            if content != original_content:
                self.stats['files_modified'] += 1
                self.stats['annotations_replaced'] += anno_count
                self.stats['imports_replaced'] += import_count
                
                if not self.dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✓ 已修改: {file_path.relative_to(self.project_path)}")
                else:
                    print(f"[Dry Run] 将修改: {file_path.relative_to(self.project_path)}")
                
                return True
            
            return False
            
        except Exception as e:
            print(f"✗ 错误处理文件 {file_path}: {e}")
            return False
    
    def migrate(self):
        """执行迁移"""
        print(f"{'='*60}")
        print(f"Swagger 2 → OpenAPI 3.0 迁移工具")
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
        print(f"注解替换数: {self.stats['annotations_replaced']}")
        print(f"Import替换数: {self.stats['imports_replaced']}")
        
        if self.dry_run:
            print(f"\n这是预览模式，实际未修改文件。")
            print(f"如需执行实际迁移，请去掉 --dry-run 参数")


def main():
    parser = argparse.ArgumentParser(
        description='Swagger 2 到 OpenAPI 3.0 迁移工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 预览模式（不实际修改文件）
  python migrate_swagger_to_openapi.py --project-path /path/to/project --dry-run
  
  # 实际执行迁移
  python migrate_swagger_to_openapi.py --project-path /path/to/project
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
    migrator = SwaggerToOpenApiMigrator(
        project_path=args.project_path,
        dry_run=args.dry_run
    )
    migrator.migrate()


if __name__ == '__main__':
    main()
