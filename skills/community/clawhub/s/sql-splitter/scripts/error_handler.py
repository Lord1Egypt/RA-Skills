#!/usr/bin/env python3
"""
SQL 拆分工具 - 错误处理模块
提供详细的错误信息和修复建议
"""

from dataclasses import dataclass
from typing import Optional, List
from enum import Enum


class ErrorType(Enum):
    """错误类型"""
    SYNTAX_ERROR = "syntax_error"
    MISSING_SEMICOLON = "missing_semicolon"
    MISSING_KEYWORD = "missing_keyword"
    INVALID_DIALECT = "invalid_dialect"
    FILE_READ_ERROR = "file_read_error"
    FILE_WRITE_ERROR = "file_write_error"
    DEPENDENCY_ERROR = "dependency_error"
    BOUNDARY_DETECTION_ERROR = "boundary_detection_error"
    UNKNOWN_ERROR = "unknown_error"


@dataclass
class SplitError:
    """拆分错误详情"""
    error_type: ErrorType
    message: str  # 错误消息
    line_num: Optional[int] = None
    column: Optional[int] = None
    context: Optional[str] = None
    suggestion: Optional[str] = None
    object_name: Optional[str] = None
    object_type: Optional[str] = None
    
    def __str__(self) -> str:
        """格式化错误信息"""
        parts = [f"[{self.error_type.value}]"]
        
        if self.object_type and self.object_name:
            parts.append(f"{self.object_type}:{self.object_name}")
        
        if self.line_num:
            parts.append(f"行{self.line_num}")
            if self.column:
                parts.append(f"列{self.column}")
        
        if self.context:
            parts.append(f"\n  上下文: {self.context}")
        
        if self.suggestion:
            parts.append(f"\n  建议: {self.suggestion}")
        
        return " ".join(parts) if len(parts) <= 2 else "\n".join(parts)


@dataclass
class SplitWarning:
    """拆分警告"""
    warning_type: str
    message: str
    object_name: Optional[str] = None
    object_type: Optional[str] = None
    
    def __str__(self) -> str:
        parts = [f"[警告] {self.warning_type}"]
        if self.object_type and self.object_name:
            parts.append(f"{self.object_type}:{self.object_name}")
        parts.append(f"- {self.message}")
        return " ".join(parts)


@dataclass
class SplitResult:
    """拆分结果"""
    success: bool
    output_dir: Optional[str]
    files_created: List[str]
    errors: List[SplitError]
    warnings: List[SplitWarning]
    stats: dict
    total: int
    merge_script: Optional[str] = None
    dry_run: bool = False
    
    def has_errors(self) -> bool:
        """是否有错误"""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """是否有警告"""
        return len(self.warnings) > 0
    
    def get_summary(self) -> str:
        """获取结果摘要"""
        lines = [
            f"{'[预览] ' if self.dry_run else ''}拆分完成",
            f"成功: {self.total} 个文件",
        ]
        
        if self.has_errors():
            lines.append(f"错误: {len(self.errors)} 个")
        
        if self.has_warnings():
            lines.append(f"警告: {len(self.warnings)} 个")
        
        if self.stats:
            lines.append("\n统计:")
            for obj_type, count in sorted(self.stats.items()):
                lines.append(f"  {obj_type}: {count}")
        
        return "\n".join(lines)


class ErrorHandler:
    """错误处理器"""
    
    @staticmethod
    def create_syntax_error(line_num: int, context: str, suggestion: str = None) -> SplitError:
        """创建语法错误"""
        return SplitError(
            error_type=ErrorType.SYNTAX_ERROR,
            message=f"语法错误: {context}",
            line_num=line_num,
            context=context,
            suggestion=suggestion or "检查SQL语法是否正确"
        )
    
    @staticmethod
    def create_missing_semicolon_error(object_name: str, object_type: str, 
                                       line_num: int = None) -> SplitError:
        """创建缺少分号错误"""
        return SplitError(
            error_type=ErrorType.MISSING_SEMICOLON,
            message=f"{object_type} {object_name} 缺少分号结束符",
            line_num=line_num,
            object_name=object_name,
            object_type=object_type,
            context=f"{object_type} {object_name} 缺少分号结束符",
            suggestion="在对象末尾添加分号 (;)"
        )
    
    @staticmethod
    def create_missing_keyword_error(keyword: str, object_name: str, 
                                     object_type: str, line_num: int = None) -> SplitError:
        """创建缺少关键字错误"""
        return SplitError(
            error_type=ErrorType.MISSING_KEYWORD,
            message=f"{object_type} {object_name} 缺少 {keyword} 关键字",
            line_num=line_num,
            object_name=object_name,
            object_type=object_type,
            context=f"{object_type} {object_name} 缺少 {keyword} 关键字",
            suggestion=f"添加 {keyword} 关键字"
        )
    
    @staticmethod
    def create_boundary_detection_error(object_name: str, object_type: str,
                                        start_pos: int, end_pos: int) -> SplitError:
        """创建边界检测错误"""
        return SplitError(
            error_type=ErrorType.BOUNDARY_DETECTION_ERROR,
            message=f"无法确定 {object_type} {object_name} 的结束位置",
            object_name=object_name,
            object_type=object_type,
            context=f"无法确定 {object_type} {object_name} 的结束位置 (起始: {start_pos}, 结束: {end_pos})",
            suggestion="检查对象语法是否规范，确保有正确的结束符"
        )
    
    @staticmethod
    def create_file_read_error(filepath: str, reason: str) -> SplitError:
        """创建文件读取错误"""
        return SplitError(
            error_type=ErrorType.FILE_READ_ERROR,
            message=f"无法读取文件 {filepath}",
            context=f"无法读取文件 {filepath}",
            suggestion=reason or "检查文件是否存在且有读取权限"
        )
    
    @staticmethod
    def create_file_write_error(filepath: str, reason: str) -> SplitError:
        """创建文件写入错误"""
        return SplitError(
            error_type=ErrorType.FILE_WRITE_ERROR,
            message=f"无法写入文件 {filepath}",
            context=f"无法写入文件 {filepath}",
            suggestion=reason or "检查目录是否存在且有写入权限"
        )
    
    @staticmethod
    def create_dependency_warning(object_name: str, object_type: str, 
                                  message: str) -> SplitWarning:
        """创建依赖警告"""
        return SplitWarning(
            warning_type="dependency",
            message=message,
            object_name=object_name,
            object_type=object_type
        )
