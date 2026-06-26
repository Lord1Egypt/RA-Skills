#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Release Compatibility Checker for Java Projects
Analyzes Git diff to detect SQL compatibility, Java code changes, and configuration changes
Supports MyBatis-Plus projects with code-based SQL

Features:
- Git diff analysis
- SQL compatibility checking
- SQL multi-database conversion (MySQL → PostgreSQL/Oracle) using SQLGlot
- SQL validation after conversion
- Markdown report generation
"""

import os
import re
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime

# SQLGlot for professional SQL parsing and transpilation
try:
    import sqlglot
    from sqlglot import exp
    from sqlglot.dialects import MySQL, PostgreSQL, Oracle
    SQLGLOT_AVAILABLE = True
except ImportError:
    SQLGLOT_AVAILABLE = False
    print("Warning: sqlglot not installed. Run: pip install sqlglot")

# Fix Windows console encoding for emoji output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


@dataclass
class ChangeFile:
    """Represents a changed file"""
    path: str
    change_type: str  # added, modified, deleted
    file_type: str    # java, sql, yml, properties, xml, etc.


@dataclass
class SQLCompatibilityIssue:
    """Represents a SQL compatibility issue"""
    file_path: str
    issue_type: str
    severity: str  # HIGH, MEDIUM, LOW
    description: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


@dataclass
class Report:
    """Final compatibility report"""
    changed_files: List[ChangeFile] = field(default_factory=list)
    java_files: List[str] = field(default_factory=list)
    sql_files: List[str] = field(default_factory=list)
    config_files: List[str] = field(default_factory=list)
    sql_issues: List[SQLCompatibilityIssue] = field(default_factory=list)
    todos: List[str] = field(default_factory=list)
    release_components: Dict[str, bool] = field(default_factory=dict)
    mysql_files_to_convert: List[str] = field(default_factory=list)


# Script type configurations for TODO generation
SCRIPT_TYPES = {
    'push_center': {
        'name': '推送中心配置',
        'description': '涉及推送中心服务相关配置变更',
        'todo_template': '- [ ] 推送中心配置变更：需验证配置在目标环境生效'
    },
    'ugateway': {
        'name': 'UGateway 配置',
        'description': '涉及统一网关相关配置',
        'todo_template': '- [ ] UGateway 配置变更：检查路由规则和权限配置'
    },
    'es': {
        'name': 'ES 变更',
        'description': '涉及 Elasticsearch 索引或查询变更',
        'todo_template': '- [ ] ES 变更：验证索引结构、数据迁移、查询兼容性'
    },
    'sql': {
        'name': 'SQL 脚本',
        'description': '涉及数据库脚本变更（DML/DDL）',
        'todo_template': '- [ ] SQL 脚本：检查多数据库兼容性，验证脚本可执行性'
    },
    'dictionary': {
        'name': '字典变更',
        'description': '涉及数据字典或枚举配置变更',
        'todo_template': '- [ ] 字典变更：同步更新所有数据库版本的字典表'
    },
    'config': {
        'name': '配置文件变更',
        'description': '涉及应用配置文件（yml/properties）变更',
        'todo_template': '- [ ] 配置文件变更：检查多环境配置差异'
    },
    'redis': {
        'name': 'Redis 配置',
        'description': '涉及 Redis 缓存或数据结构变更',
        'todo_template': '- [ ] Redis 变更：检查序列化兼容性，需更新缓存策略'
    },
    'mq': {
        'name': 'MQ 消息',
        'description': '涉及消息队列 topic 或消息格式变更',
        'todo_template': '- [ ] MQ 变更：验证消费者兼容性，需做好版本兼容'
    },
    'file': {
        'name': '文件存储',
        'description': '涉及文件上传、存储路径或处理逻辑变更',
        'todo_template': '- [ ] 文件存储变更：检查存储路径和权限配置'
    },
    'api': {
        'name': 'API 接口',
        'description': '涉及对外 API 接口变更',
        'todo_template': '- [ ] API 接口变更：更新接口文档，做好向后兼容'
    },
    'java': {
        'name': 'Java 代码',
        'description': '涉及 Java 代码变更（新增/修改服务、实体等）',
        'todo_template': '- [ ] Java 代码变更：需回归测试，验证新增功能'
    }
}


class SQLConverter:
    """Converts MySQL SQL to PostgreSQL and Oracle versions using SQLGlot"""
    
    def __init__(self):
        # Import sqlglot directly in __init__ to avoid module-level import issues
        try:
            import sqlglot
            self.sqlglot = sqlglot
        except ImportError as e:
            raise ImportError("sqlglot is required. Install with: pip install sqlglot")
    
    def convert_to_postgresql(self, sql_content: str) -> Tuple[str, List[str]]:
        """Convert MySQL SQL to PostgreSQL using SQLGlot"""
        changes = []
        
        try:
            # Parse MySQL and transpile to PostgreSQL
            result = self.sqlglot.transpile(
                sql_content,
                read='mysql',
                write='postgres'
            )
            converted = '\n'.join(result)
            
            # Track key changes
            if 'SERIAL' in converted:
                changes.append('AUTO_INCREMENT → SERIAL (handled by SQLGlot)')
            if 'COALESCE' in converted:
                changes.append('IFNULL → COALESCE (handled by SQLGlot)')
            if 'TIMESTAMP' in converted:
                changes.append('DATETIME → TIMESTAMP (handled by SQLGlot)')
            
            # Additional post-processing for MySQL-specific syntax
            # SQLGlot handles most, but some need manual adjustment
            if 'ENGINE' in sql_content:
                changes.append('ENGINE clause removed (MySQL-specific)')
            
            if 'CHARSET' in sql_content:
                changes.append('CHARSET clause removed (MySQL-specific)')
            
            # Ensure CREATE TABLE uses IF NOT EXISTS
            if 'CREATE TABLE' in converted:
                converted = re.sub(
                    r'CREATE\s+TABLE\s+(\w+)',
                    r'CREATE TABLE IF NOT EXISTS \1',
                    converted,
                    flags=re.IGNORECASE
                )
                changes.append('Added IF NOT EXISTS to CREATE TABLE')
            
            # Post-process: PostgreSQL doesn't support DECIMAL, use NUMERIC
            if 'DECIMAL' in converted:
                converted = converted.replace('DECIMAL', 'NUMERIC')
                changes.append('DECIMAL → NUMERIC (PostgreSQL)')
            
            # Post-process: PostgreSQL uses INTEGER instead of INT
            if re.search(r'\bINT\b', converted):
                converted = re.sub(r'\bINT\b', 'INTEGER', converted)
                changes.append('INT → INTEGER (PostgreSQL)')
            
            # Post-process: Remove inline COMMENT from CREATE TABLE (PostgreSQL uses separate COMMENT ON)
            # Move comments to separate COMMENT ON statements
            print(f"DEBUG: sql_content has COMMENT: {'COMMENT' in sql_content}")
            print(f"DEBUG: sql_content has quote: {'" in sql_content}")
            
            if 'COMMENT' in sql_content and "'" in sql_content:
                # Extract table name
                table_match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', converted, re.IGNORECASE)
                if table_match:
                    table_name = table_match.group(1)
                    print(f"DEBUG: Found table {table_name}, processing comments...")
                    # Remove inline comments from CREATE TABLE
                    converted = re.sub(r"\s+COMMENT '[^']+'", '', converted)
                    
                    # Extract column names and comments by scanning each line
                    comment_lines = []
                    
                    for line in sql_content.split('\n'):
                        # Match: column_name ... COMMENT 'text' (at start of line)
                        match = re.search(r"^\s*(\w+).*?COMMENT\s+'([^']+)'", line, re.IGNORECASE)
                        if match:
                            col_name = match.group(1)
                            comment_text = match.group(2).replace("'", "''")
                            comment_lines.append(f"COMMENT ON COLUMN {table_name}.{col_name} IS '{comment_text}';")
                            print(f"DEBUG: Found comment for column {col_name}")
                    
                    if comment_lines:
                        converted = converted.rstrip() + '\n\n' + '\n'.join(comment_lines)
                        changes.append(f'Generated {len(comment_lines)} COMMENT ON statements')
            
            # Post-process: Fix NULLS FIRST for unique index (optional in PostgreSQL)
            converted = re.sub(r'NULLS FIRST', '', converted)
            
        except Exception as e:
            # Fallback to regex-based conversion if SQLGlot fails
            converted, changes = self._fallback_convert_postgresql(sql_content)
            changes.append(f'Fallback conversion used: {str(e)}')
        
        return converted, changes
    
    def convert_to_oracle(self, sql_content: str) -> Tuple[str, List[str]]:
        """Convert MySQL SQL to Oracle using SQLGlot"""
        changes = []
        
        try:
            # Parse MySQL and transpile to Oracle
            result = self.sqlglot.transpile(
                sql_content,
                read='mysql',
                write='oracle'
            )
            converted = '\n'.join(result)
            
            # Track key changes
            if 'NUMBER' in converted:
                changes.append('Integer types → NUMBER (handled by SQLGlot)')
            if 'NVL' in converted:
                changes.append('IFNULL → NVL (handled by SQLGlot)')
            if 'SYSTIMESTAMP' in converted:
                changes.append('NOW() → SYSTIMESTAMP (handled by SQLGlot)')
            if 'TIMESTAMP' in converted:
                changes.append('DATETIME → TIMESTAMP (handled by SQLGlot)')
            
            # Handle AUTO_INCREMENT - Oracle needs SEQUENCE + TRIGGER
            auto_increment_pattern = r'AUTO_INCREMENT'
            if re.search(auto_increment_pattern, sql_content, re.IGNORECASE):
                # Extract table names with AUTO_INCREMENT
                tables = re.findall(
                    r'CREATE\s+TABLE\s+(\w+).*?(\w+)\s+\w+\s+AUTO_INCREMENT',
                    sql_content,
                    re.IGNORECASE | re.DOTALL
                )
                
                sequence_blocks = []
                for table_name, col_name in tables:
                    seq_name = f"SEQ_{table_name.upper()}"
                    trg_name = f"TRG_{table_name.upper()}"
                    
                    sequence_blocks.append(f"""
-- Sequence for {table_name}.{col_name}
CREATE SEQUENCE {seq_name}
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;
/

-- Trigger for {table_name}.{col_name}
CREATE OR REPLACE TRIGGER {trg_name}
    BEFORE INSERT ON {table_name}
    FOR EACH ROW
BEGIN
    IF :NEW.{col_name} IS NULL THEN
        SELECT {seq_name}.NEXTVAL INTO :NEW.{col_name} FROM DUAL;
    END IF;
END;
/
""")
                    changes.append(f'AUTO_INCREMENT → SEQUENCE({seq_name}) + TRIGGER({trg_name})')
                
                # Remove AUTO_INCREMENT from CREATE TABLE
                converted = re.sub(
                    r'\s+AUTO_INCREMENT\b',
                    '',
                    converted,
                    flags=re.IGNORECASE
                )
                
                # Add sequence/trigger blocks at the beginning
                if sequence_blocks:
                    header = "-- Oracle: Sequences and Triggers for AUTO_INCREMENT columns\n"
                    converted = header + '\n'.join(sequence_blocks) + '\n' + converted
            
            # Handle LIMIT - Oracle doesn't support it
            if re.search(r'\bLIMIT\b', sql_content, re.IGNORECASE):
                changes.append('LIMIT clause - needs manual conversion to ROWNUM or FETCH')
            
            # Remove MySQL-specific syntax
            if 'ENGINE' in sql_content:
                changes.append('ENGINE clause removed (MySQL-specific)')
            
            if 'CHARSET' in sql_content:
                changes.append('CHARSET clause removed (MySQL-specific)')
            
            # Post-process: Oracle uses TIMESTAMP, not DATETIME
            if 'DATETIME' in converted:
                converted = converted.replace('DATETIME', 'TIMESTAMP')
                changes.append('DATETIME → TIMESTAMP (Oracle)')
            
            # Post-process: Oracle doesn't support inline COMMENT in CREATE TABLE
            # Remove inline comments - they need to be separate COMMENT ON statements
            if "COMMENT '" in sql_content:
                # Extract table name
                table_match = re.search(r'CREATE\s+TABLE\s+(\w+)', converted, re.IGNORECASE)
                if table_match:
                    table_name = table_match.group(1)
                    # Remove inline comments from CREATE TABLE
                    converted = re.sub(r"\s+COMMENT '[^']+'", '', converted)
                    
                    # Extract column names and comments by scanning each line
                    comment_lines = []
                    
                    for line in sql_content.split('\n'):
                        # Match: column_name ... COMMENT 'text' (at start of line)
                        match = re.search(r"^\s*(\w+).*?COMMENT\s+'([^']+)'", line, re.IGNORECASE)
                        if match:
                            col_name = match.group(1)
                            comment_text = match.group(2).replace("'", "''")
                            comment_lines.append(f"COMMENT ON COLUMN {table_name}.{col_name} IS '{comment_text}';")
                    
                    if comment_lines:
                        converted = converted.rstrip() + '\n\n' + '\n'.join(comment_lines)
                        changes.append(f'Generated {len(comment_lines)} COMMENT ON statements')
            
            # Post-process: Fix NULLS FIRST for unique index (not supported in Oracle)
            converted = re.sub(r'NULLS FIRST', '', converted)
            
            # Post-process: Oracle uses VARCHAR2, not VARCHAR
            if re.search(r'\bVARCHAR\(', converted):
                converted = re.sub(r'\bVARCHAR\(', 'VARCHAR2(', converted)
                changes.append('VARCHAR → VARCHAR2 (Oracle)')
            
            # Post-process: Convert BIGINT to NUMBER for Oracle
            if 'BIGINT' in converted:
                converted = converted.replace('BIGINT', 'NUMBER(19)')
                changes.append('BIGINT → NUMBER(19) (Oracle)')
            
            # Post-process: Convert INT to NUMBER(10) for Oracle
            if re.search(r'\bINT\b', converted):
                converted = re.sub(r'\bINT\b', 'NUMBER(10)', converted)
                changes.append('INT → NUMBER(10) (Oracle)')
            
        except Exception as e:
            # Fallback to regex-based conversion if SQLGlot fails
            converted, changes = self._fallback_convert_oracle(sql_content)
            changes.append(f'Fallback conversion used: {str(e)}')
        
        return converted, changes
    
    def _fallback_convert_postgresql(self, sql_content: str) -> Tuple[str, List[str]]:
        """Fallback regex-based conversion for PostgreSQL"""
        converted = sql_content
        changes = []
        
        replacements = [
            (r'`([^`]*)`', r'"\1"'),
            (r'\bAUTO_INCREMENT\b', r'SERIAL'),
            (r'\bNOW\(\)', r'CURRENT_TIMESTAMP'),
            (r'\bIFNULL\(', r'COALESCE('),
            (r'\bTINYINT\b(?:\(\d+\))?', r'SMALLINT'),
            (r'\bDATETIME\b', r'TIMESTAMP'),
            (r'\bMEDIUMINT\b(?:\(\d+\))?', r'INTEGER'),
            (r'\bINT\b(?:\(\d+\))?', r'INTEGER'),
            (r'ENGINE\s*=\s*\w+', r''),
            (r'DEFAULT\s+CHARSET\s*=\s*\w+', r''),
            (r'\bUNSIGNED\b', r''),
        ]
        
        for pattern, replacement in replacements:
            if re.search(pattern, converted, re.IGNORECASE):
                converted = re.sub(pattern, replacement, converted, flags=re.IGNORECASE)
                changes.append(f'Fallback: {pattern} → {replacement}')
        
        return converted, changes
    
    def _fallback_convert_oracle(self, sql_content: str) -> Tuple[str, List[str]]:
        """Fallback regex-based conversion for Oracle"""
        converted = sql_content
        changes = []
        
        replacements = [
            (r'`([^`]*)`', r'"\1"'),
            (r'\bNOW\(\)', r'SYSTIMESTAMP'),
            (r'\bIFNULL\(', r'NVL('),
            (r'\bTINYINT\b(?:\(\d+\))?', r'NUMBER(3)'),
            (r'\bDATETIME\b', r'TIMESTAMP'),
            (r'\bMEDIUMINT\b(?:\(\d+\))?', r'NUMBER(10)'),
            (r'\bINT\b(?:\(\d+\))?', r'NUMBER(10)'),
            (r'ENGINE\s*=\s*\w+', r''),
            (r'DEFAULT\s+CHARSET\s*=\s*\w+', r''),
            (r'\bUNSIGNED\b', r''),
        ]
        
        for pattern, replacement in replacements:
            if re.search(pattern, converted, re.IGNORECASE):
                converted = re.sub(pattern, replacement, converted, flags=re.IGNORECASE)
                changes.append(f'Fallback: {pattern} → {replacement}')
        return converted, changes


class SQLValidator:
    """Validates converted SQL for syntax correctness"""
    
    # PostgreSQL validation rules
    PG_VALIDATION_RULES = [
        {
            'name': '反引号检查',
            'pattern': r'`[^`]+`',
            'status': 'FAIL',
            'message': 'PostgreSQL 不支持反引号，请使用双引号'
        },
        {
            'name': 'AUTO_INCREMENT 检查',
            'pattern': r'\bAUTO_INCREMENT\b',
            'status': 'FAIL',
            'message': 'PostgreSQL 使用 SERIAL 或 GENERATED ALWAYS AS IDENTITY'
        },
        {
            'name': 'ENGINE 检查',
            'pattern': r'ENGINE\s*=\s*InnoDB',
            'status': 'FAIL',
            'message': 'PostgreSQL 无 ENGINE 概念，请移除'
        },
        {
            'name': 'NOW() 函数检查',
            'pattern': r'\bNOW\(\)',
            'status': 'WARN',
            'message': '建议使用 CURRENT_TIMESTAMP 替代 NOW()'
        },
        {
            'name': 'IFNULL 函数检查',
            'pattern': r'\bIFNULL\(',
            'status': 'FAIL',
            'message': 'PostgreSQL 使用 COALESCE() 替代 IFNULL()'
        },
        {
            'name': 'TINYINT 类型检查',
            'pattern': r'\bTINYINT\b',
            'status': 'FAIL',
            'message': 'PostgreSQL 使用 SMALLINT 替代 TINYINT'
        },
        {
            'name': 'DATETIME 类型检查',
            'pattern': r'\bDATETIME\b',
            'status': 'FAIL',
            'message': 'PostgreSQL 使用 TIMESTAMP 替代 DATETIME'
        },
        {
            'name': 'DEFAULT CHARSET 检查',
            'pattern': r'DEFAULT\s+CHARSET',
            'status': 'FAIL',
            'message': 'PostgreSQL 无 CHARSET 概念，请移除'
        },
        {
            'name': 'UNSIGNED 检查',
            'pattern': r'\bUNSIGNED\b',
            'status': 'FAIL',
            'message': 'PostgreSQL 无 UNSIGNED 概念，请移除'
        },
    ]
    
    # Oracle validation rules
    ORACLE_VALIDATION_RULES = [
        {
            'name': '反引号检查',
            'pattern': r'`[^`]+`',
            'status': 'FAIL',
            'message': 'Oracle 不支持反引号，请使用双引号'
        },
        {
            'name': 'AUTO_INCREMENT 检查',
            'pattern': r'\bAUTO_INCREMENT\b',
            'status': 'FAIL',
            'message': 'Oracle 使用 SEQUENCE + TRIGGER 或 GENERATED ALWAYS AS IDENTITY'
        },
        {
            'name': 'ENGINE 检查',
            'pattern': r'ENGINE\s*=\s*InnoDB',
            'status': 'FAIL',
            'message': 'Oracle 无 ENGINE 概念，请移除'
        },
        {
            'name': 'NOW() 函数检查',
            'pattern': r'\bNOW\(\)',
            'status': 'FAIL',
            'message': 'Oracle 使用 SYSTIMESTAMP 替代 NOW()'
        },
        {
            'name': 'IFNULL 函数检查',
            'pattern': r'\bIFNULL\(',
            'status': 'FAIL',
            'message': 'Oracle 使用 NVL() 或 COALESCE() 替代 IFNULL()'
        },
        {
            'name': 'TINYINT 类型检查',
            'pattern': r'\bTINYINT\b',
            'status': 'FAIL',
            'message': 'Oracle 使用 NUMBER(3) 替代 TINYINT'
        },
        {
            'name': 'DATETIME 类型检查',
            'pattern': r'\bDATETIME\b',
            'status': 'FAIL',
            'message': 'Oracle 使用 TIMESTAMP 替代 DATETIME'
        },
        {
            'name': 'IF NOT EXISTS 检查',
            'pattern': r'IF\s+NOT\s+EXISTS',
            'status': 'FAIL',
            'message': 'Oracle 不支持 IF NOT EXISTS，需手动处理'
        },
        {
            'name': 'LIMIT 检查',
            'pattern': r'LIMIT\s+\d+',
            'status': 'FAIL',
            'message': 'Oracle 使用 ROWNUM 或 FETCH FIRST n ROWS ONLY'
        },
        {
            'name': 'DEFAULT CHARSET 检查',
            'pattern': r'DEFAULT\s+CHARSET',
            'status': 'FAIL',
            'message': 'Oracle 无 CHARSET 概念，请移除'
        },
        {
            'name': 'UNSIGNED 检查',
            'pattern': r'\bUNSIGNED\b',
            'status': 'FAIL',
            'message': 'Oracle 无 UNSIGNED 概念，请移除'
        },
    ]
    
    def validate_postgresql(self, sql_content: str) -> List[Dict]:
        """Validate PostgreSQL SQL"""
        return self._validate(sql_content, self.PG_VALIDATION_RULES)
    
    def validate_oracle(self, sql_content: str) -> List[Dict]:
        """Validate Oracle SQL"""
        return self._validate(sql_content, self.ORACLE_VALIDATION_RULES)
    
    def _validate(self, sql_content: str, rules: List[Dict]) -> List[Dict]:
        """Run validation rules against SQL content"""
        results = []
        
        for rule in rules:
            matches = re.findall(rule['pattern'], sql_content, re.IGNORECASE)
            if matches:
                results.append({
                    'rule': rule['name'],
                    'status': rule['status'],
                    'message': rule['message'],
                    'occurrences': len(matches)
                })
            else:
                results.append({
                    'rule': rule['name'],
                    'status': 'PASS',
                    'message': f'{rule["name"]} 通过',
                    'occurrences': 0
                })
        
        return results
    
    def get_validation_summary(self, results: List[Dict]) -> Dict:
        """Get validation summary"""
        total = len(results)
        passed = sum(1 for r in results if r['status'] == 'PASS')
        failed = sum(1 for r in results if r['status'] == 'FAIL')
        warnings = sum(1 for r in results if r['status'] == 'WARN')
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'warnings': warnings,
            'is_valid': failed == 0
        }


class GitAnalyzer:
    """Analyzes Git diff to find changed files"""
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
    
    def get_changed_files(self, compare_branch: Optional[str] = None) -> List[ChangeFile]:
        """Get list of all changed files"""
        try:
            if compare_branch:
                cmd = f"git diff {compare_branch} --name-status"
            else:
                cmd = "git diff --name-status"
            
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"Warning: Git command failed: {result.stderr}")
                return self._get_unstaged_changed_files()
            
            files = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        status = parts[0].strip()
                        path = parts[1].strip()
                        
                        # Determine file type
                        file_type = self._get_file_type(path)
                        
                        files.append(ChangeFile(
                            path=path,
                            change_type=status,
                            file_type=file_type
                        ))
            
            return files
        except Exception as e:
            print(f"Error running git: {e}")
            return self._get_unstaged_changed_files()
    
    def _get_unstaged_changed_files(self) -> List[ChangeFile]:
        """Get unstaged changes as fallback"""
        try:
            result = subprocess.run(
                "git diff --name-status",
                shell=True,
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            
            files = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split('\t')
                    if len(parts) >= 2:
                        status = parts[0].strip()
                        path = parts[1].strip()
                        file_type = self._get_file_type(path)
                        
                        files.append(ChangeFile(
                            path=path,
                            change_type=status,
                            file_type=file_type
                        ))
            
            return files
        except:
            return []
    
    def _get_file_type(self, path: str) -> str:
        """Determine file type from path"""
        if path.endswith('.java'):
            return 'java'
        elif path.endswith('.sql'):
            return 'sql'
        elif path.endswith(('.yml', '.yaml')):
            return 'yml'
        elif path.endswith('.properties'):
            return 'properties'
        elif path.endswith('.xml'):
            return 'xml'
        elif path.endswith('.http'):
            return 'http'
        else:
            return 'other'


class SQLAnalyzer:
    """Analyzes SQL scripts for compatibility issues"""
    
    # SQL compatibility rules
    COMPATIBILITY_RULES = [
        # (pattern, databases_affected, severity, description, suggestion)
        (r'NOW\(\)', ['oracle'], 'MEDIUM', 'NOW() not supported in Oracle', 'Use SYSTIMESTAMP from DUAL'),
        (r'LIMIT\s+\d+', ['oracle'], 'MEDIUM', 'LIMIT not supported in Oracle', 'Use OFFSET ... ROWS FETCH NEXT'),
        (r'IF NOT EXISTS', ['oracle'], 'LOW', 'IF NOT EXISTS not supported in Oracle', 'Add condition check manually'),
        (r'AUTO_INCREMENT', ['postgresql', 'oracle'], 'MEDIUM', 'AUTO_INCREMENT not supported', 'Use SERIAL (PG) or SEQUENCE (Oracle)'),
        (r'ENUM\(', ['postgresql', 'oracle'], 'MEDIUM', 'ENUM type not supported', 'Use VARCHAR + CHECK constraint'),
        (r'IFNULL\(', ['oracle'], 'LOW', 'IFNULL not in Oracle', 'Use NVL or COALESCE'),
        (r'CREATE\s+INDEX\s+IF\s+NOT\s+EXISTS', ['oracle'], 'MEDIUM', 'CREATE INDEX IF NOT EXISTS not in Oracle', 'Drop index before create or handle manually'),
    ]
    
    def __init__(self):
        pass
    
    def analyze_sql_file(self, file_path: str) -> List[SQLCompatibilityIssue]:
        """Analyze a SQL file for compatibility issues"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    for pattern, dbs, severity, desc, suggestion in self.COMPATIBILITY_RULES:
                        if re.search(pattern, line, re.IGNORECASE):
                            issues.append(SQLCompatibilityIssue(
                                file_path=file_path,
                                issue_type='incompatible_syntax',
                                severity=severity,
                                description=f"{desc} (line {line_num})",
                                line_number=line_num,
                                suggestion=suggestion
                            ))
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
        
        return issues
    
    def compare_ddl_files(self, mysql_file: str, pg_file: str, ora_file: str) -> Dict:
        """Compare DDL files across databases"""
        result = {
            'mysql': {'exists': False, 'content': []},
            'postgresql': {'exists': False, 'content': []},
            'oracle': {'exists': False, 'content': []},
            'differences': []
        }
        
        # Read MySQL
        if os.path.exists(mysql_file):
            result['mysql']['exists'] = True
            with open(mysql_file, 'r', encoding='utf-8') as f:
                result['mysql']['content'] = f.readlines()
        
        # Read PostgreSQL
        if os.path.exists(pg_file):
            result['postgresql']['exists'] = True
            with open(pg_file, 'r', encoding='utf-8') as f:
                result['postgresql']['content'] = f.readlines()
        
        # Read Oracle
        if os.path.exists(ora_file):
            result['oracle']['exists'] = True
            with open(ora_file, 'r', encoding='utf-8') as f:
                result['oracle']['content'] = f.readlines()
        
        return result


class JavaAnalyzer:
    """Analyzes Java code changes"""
    
    def __init__(self):
        pass
    
    def analyze_java_files(self, files: List[ChangeFile]) -> Dict:
        """Analyze Java file changes"""
        result = {
            'new_entities': [],
            'new_services': [],
            'modified_services': [],
            'new_mappers': [],
            'other_changes': []
        }
        
        for f in files:
            if f.file_type != 'java':
                continue
            
            # Categorize by path
            if '/dao/entity/' in f.path:
                result['new_entities'].append(f.path)
            elif '/service/' in f.path:
                if f.change_type.startswith('A'):
                    result['new_services'].append(f.path)
                else:
                    result['modified_services'].append(f.path)
            elif '/mapper/' in f.path:
                result['new_mappers'].append(f.path)
            else:
                result['other_changes'].append(f.path)
        
        return result


class ConfigAnalyzer:
    """Analyzes configuration file changes"""
    
    def __init__(self):
        pass
    
    def analyze_config_files(self, files: List[ChangeFile]) -> List[str]:
        """Get list of changed config files"""
        config_files = []
        
        for f in files:
            if f.file_type in ('yml', 'properties'):
                config_files.append(f.path)
        
        return config_files


class TodoGenerator:
    """Generates TODO items from analysis results"""
    
    def __init__(self):
        pass
    
    def generate_todos(self, report: Report) -> List[str]:
        """Generate structured TODO list"""
        todos = []
        
        # Section 1: Release Components
        todos.append("## 📋 发布清单确认")
        todos.append("")
        
        for key, config in SCRIPT_TYPES.items():
            if report.release_components.get(key):
                template = config['todo_template']
                todos.append(template)
        
        if not any(report.release_components.values()):
            todos.append("- [ ] 暂无明确的发布组件标记")
        
        todos.append("")
        
        # Section 2: SQL Script Analysis
        todos.append("## 🗄️ SQL 脚本分析")
        todos.append("")
        
        if report.sql_files:
            todos.append("### 变更的 SQL 文件")
            for sql_file in report.sql_files:
                todos.append(f"- `{sql_file}`")
            todos.append("")
        
        if report.sql_issues:
            todos.append("### 兼容性问题")
            for issue in report.sql_issues:
                severity_map = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}
                severity = severity_map.get(issue.severity, '⚪')
                todos.append(f"- {severity} [{issue.severity}] {issue.description}")
                if issue.suggestion:
                    todos.append(f"  - 💡 建议: {issue.suggestion}")
            todos.append("")
        else:
            todos.append("未发现明显的 SQL 兼容性问题")
            todos.append("")
        
        # Section 3: Java Code Changes
        todos.append("## 💻 Java 代码变更")
        todos.append("")
        todos.append("| 类别 | 数量 | 说明 |")
        todos.append("|------|------|------|")
        
        # This will be filled by the main function
        todos.append("- [ ] 需回归测试")
        todos.append("")
        
        return todos


class MarkdownReportGenerator:
    """Generates Markdown format report"""
    
    def __init__(self):
        pass
    
    def generate_report(self, report: Report, config: Dict, java_analysis: Dict) -> str:
        """Generate comprehensive Markdown report"""
        lines = []
        lines.append("# 📋 发版兼容性检查报告")
        lines.append("")
        lines.append(f"> 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"> 项目: {config.get('project_path', 'N/A')}")
        lines.append(f"> 对比分支: {config.get('compare_branch', 'N/A')}")
        lines.append("")
        lines.append("---")
        lines.append("")
        
        # Section 1: Release Components
        lines.append("## 一、发布清单确认")
        lines.append("")
        lines.append("| 组件 | 状态 | 说明 |")
        lines.append("|------|------|------|")
        
        component_names = {
            'push_center': '推送中心配置',
            'ugateway': 'UGateway 配置',
            'es': 'ES 变更',
            'sql': 'SQL 脚本',
            'dictionary': '字典变更',
            'config': '配置文件变更',
            'redis': 'Redis 配置',
            'mq': 'MQ 消息',
            'file': '文件存储',
            'api': 'API 接口',
            'java': 'Java 代码'
        }
        
        release_components = config.get('release_components', {})
        for key, name in component_names.items():
            status = "✅ 是" if release_components.get(key, False) else "❌ 否"
            desc = "-" if not release_components.get(key, False) else ""
            lines.append(f"| {name} | {status} | {desc} |")
        
        lines.append("")
        
        # Section 2: Changed Files Summary
        lines.append("## 二、变更文件汇总")
        lines.append("")
        lines.append("| 类型 | 数量 |")
        lines.append("|------|------|")
        
        java_count = len([f for f in report.changed_files if f.file_type == 'java'])
        sql_count = len([f for f in report.changed_files if f.file_type == 'sql'])
        config_count = len([f for f in report.changed_files if f.file_type in ('yml', 'properties')])
        
        lines.append(f"| Java 代码 | {java_count} |")
        lines.append(f"| SQL 脚本 | {sql_count} |")
        lines.append(f"| 配置文件 | {config_count} |")
        lines.append("")
        
        # Section 3: SQL Analysis
        lines.append("## 三、SQL 脚本分析")
        lines.append("")
        
        if report.sql_files:
            lines.append("### 变更的 SQL 文件")
            lines.append("")
            for sql_file in report.sql_files:
                lines.append(f"- `{sql_file}`")
            lines.append("")
        
        if report.sql_issues:
            lines.append("### 兼容性问题")
            lines.append("")
            lines.append("| 严重程度 | 文件 | 问题 | 建议 |")
            lines.append("|----------|------|------|------|")
            for issue in report.sql_issues:
                severity_map = {'HIGH': '🔴 HIGH', 'MEDIUM': '🟡 MEDIUM', 'LOW': '🟢 LOW'}
                severity = severity_map.get(issue.severity, issue.severity)
                filename = os.path.basename(issue.file_path)
                suggestion = issue.suggestion or '-'
                lines.append(f"| {severity} | {filename} | {issue.description} | {suggestion} |")
        else:
            lines.append("未发现明显的 SQL 兼容性问题")
        
        lines.append("")
        
        # Section 4: Java Code Analysis
        lines.append("## 四、Java 代码变更分析")
        lines.append("")
        
        if java_analysis:
            lines.append("### 新增实体类")
            if java_analysis.get('new_entities'):
                for e in java_analysis['new_entities']:
                    lines.append(f"- `{e}`")
            else:
                lines.append("无")
            lines.append("")
            
            lines.append("### 新增服务")
            if java_analysis.get('new_services'):
                for s in java_analysis['new_services']:
                    lines.append(f"- `{s}`")
            else:
                lines.append("无")
            lines.append("")
            
            lines.append("### 修改的服务")
            if java_analysis.get('modified_services'):
                for s in java_analysis['modified_services']:
                    lines.append(f"- `{s}`")
            else:
                lines.append("无")
            lines.append("")
        
        # Section 5: Config Files
        lines.append("## 五、配置文件变更")
        lines.append("")
        
        if report.config_files:
            for cf in report.config_files:
                lines.append(f"- `{cf}`")
        else:
            lines.append("无配置文件变更")
        
        lines.append("")
        
        # Section 6: TODO
        lines.append("## 六、待处理 TODO")
        lines.append("")
        
        for todo in report.todos:
            lines.append(todo)
        
        lines.append("")
        
        # Section 7: Summary
        lines.append("## 七、总结")
        lines.append("")
        lines.append("| 类别 | 状态 |")
        lines.append("|------|------|")
        
        confirmed_count = sum(1 for v in release_components.values() if v)
        lines.append(f"| 发布组件确认 | ✅ 完成 ({confirmed_count} 项) |")
        lines.append(f"| 变更文件分析 | ✅ 完成 |")
        lines.append(f"| SQL 兼容性检查 | ✅ 完成 |")
        lines.append(f"| TODO 清单生成 | ✅ 完成 |")
        
        lines.append("")
        lines.append("---")
        lines.append("*报告生成工具: release-checker skill*")
        
        return '\n'.join(lines)
    
    def save_report(self, content: str, output_path: str) -> bool:
        """Save report to file"""
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error saving report: {e}")
            return False


class ReleaseComponentDetector:
    """自动检测发布组件"""
    
    # 组件检测规则（更严格的匹配）
    DETECTION_RULES = {
        'push_center': {
            'file_types': [],
            'keywords': ['pushcenter', 'pushcenter', 'msgpush', 'notificationcenter'],
            'paths': ['*/push/*', '*/notification/*']
        },
        'ugateway': {
            'file_types': [],
            'keywords': ['ugateway', 'apigateway'],
            'paths': ['*/gateway/*', '*/ugateway/*', '*/apigateway/*']
        },
        'es': {
            'file_types': [],
            'keywords': ['elasticsearch'],
            'paths': ['*/elasticsearch/*', '*/es-index/*', '*/es-config/*']
        },
        'sql': {
            'file_types': ['sql'],
            'keywords': []
        },
        'dictionary': {
            'file_types': [],
            'keywords': ['dictionary', 'dictmanager'],
            'paths': ['*/dict/*', '*/enum/*']
        },
        'config': {
            'file_types': ['yml', 'properties', 'yaml'],
            'keywords': []
        },
        'redis': {
            'file_types': [],
            'keywords': ['redis'],
            'paths': ['*/redis/*', '*/cache/*']
        },
        'mq': {
            'file_types': [],
            'keywords': ['kafka', 'rocketmq', 'rabbitmq', 'pulsar'],
            'paths': ['*/mq/*', '*/kafka/*', '*/rocket/*']
        },
        'file': {
            'file_types': [],
            'keywords': ['fileupload', 'filestorage', 'oss', 'minio'],
            'paths': ['*/upload/*', '*/storage/*']
        },
        'api': {
            'file_types': [],
            'keywords': ['openapi', 'restapi'],
            'paths': ['*/openapi/*', '*/rest/*']
        },
        'java': {
            'file_types': ['java'],
            'keywords': []
        }
    }
    
    def __init__(self):
        pass
    
    def detect_components(self, changed_files: List[ChangeFile]) -> Dict[str, bool]:
        """根据变更文件自动检测发布组件"""
        components = {key: False for key in self.DETECTION_RULES.keys()}
        
        # 添加 Java 代码组件（默认存在）
        has_java = any(f.file_type == 'java' for f in changed_files)
        components['java'] = has_java
        
        # 添加 SQL 脚本组件
        has_sql = any(f.file_type == 'sql' for f in changed_files)
        components['sql'] = has_sql
        
        # 添加配置文件组件
        has_config = any(f.file_type in ('yml', 'properties') for f in changed_files)
        components['config'] = has_config
        
        # 根据文件路径关键词检测（更严格的匹配）
        for f in changed_files:
            path_lower = f.path.lower()
            filename_lower = os.path.basename(f.path).lower()
            
            for comp_key, rule in self.DETECTION_RULES.items():
                # 跳过已通过文件类型检测的组件
                if components[comp_key]:
                    continue
                
                # 检查文件类型
                if 'file_types' in rule and rule['file_types']:
                    if f.file_type in rule['file_types']:
                        components[comp_key] = True
                        continue
                
                # 检查路径关键词（必须是完整单词或路径段）
                if 'paths' in rule:
                    for path_pattern in rule['paths']:
                        # 移除 * 后进行匹配
                        pattern_clean = path_pattern.replace('*', '').replace('/', '\\')
                        if pattern_clean in path_lower.replace('/', '\\'):
                            components[comp_key] = True
                            break
                
                # 检查文件名关键词（需要是独立单词）
                if 'keywords' in rule and rule['keywords']:
                    for keyword in rule['keywords']:
                        # 检查是否在文件名中（避免误匹配如 transaction 中的 es）
                        if keyword in filename_lower:
                            components[comp_key] = True
                            break
        
        return components


class InteractiveQuestionnaire:
    """Handles interactive questioning for release components"""
    
    def __init__(self):
        pass
    
    def ask_release_components(self) -> Dict[str, bool]:
        """Ask user which components are involved in this release"""
        print("\n" + "=" * 60)
        print("📋 发布清单生成器")
        print("=" * 60)
        print("\n请确认本次发布涉及哪些变更（输入 y/n 或直接回车跳过）：\n")
        
        results = {}
        for key, config in SCRIPT_TYPES.items():
            prompt = f"  是否涉及【{config['name']}】? ({config['description']}) [y/N]: "
            response = input(prompt).strip().lower()
            results[key] = response in ['y', 'yes']
        
        return results
    
    def ask_mysql_files(self) -> List[str]:
        """Ask user for MySQL file paths to convert"""
        print("\n" + "=" * 60)
        print("🔄 SQL 多数据库版本生成")
        print("=" * 60)
        print("\n请提供需要转换的 MySQL 文件路径（每行一个文件路径）：")
        print("（直接回车结束输入）\n")
        
        files = []
        while True:
            line = input("  > ").strip()
            if not line:
                break
            if os.path.exists(line):
                files.append(line)
            else:
                print(f"  ⚠️ 文件不存在: {line}")
        
        return files
    
    def confirm_generation(self) -> bool:
        """Ask user to confirm generation"""
        response = input("\n  是否立即生成转换脚本？ [y/N]: ").strip().lower()
        return response in ['y', 'yes']


def main():
    parser = argparse.ArgumentParser(description='Release Compatibility Checker - 自动化发版兼容性检查')
    parser.add_argument('--project', '-p', required=True, help='项目路径（必填）')
    parser.add_argument('--branch', '-b', required=True, help='对比分支（必填）')
    parser.add_argument('--output', '-o', choices=['json', 'markdown', 'plain'], 
                        default='markdown', help='输出格式')
    parser.add_argument('--report', '-r', help='Markdown 报告输出路径')
    parser.add_argument('--no-git', action='store_true', 
                        help='跳过 git diff，扫描 scripts/db 目录下的所有 SQL 文件')
    
    # SQL conversion arguments
    parser.add_argument('--convert-sql', action='store_true',
                        help='执行 SQL 多数据库转换')
    parser.add_argument('--sql-files', nargs='+',
                        help='需要转换的 MySQL SQL 文件路径（可多个）')
    parser.add_argument('--output-dir', default=None,
                        help='SQL 转换输出目录（默认与源文件同目录）')
    
    args = parser.parse_args()
    
    print(f"Analyzing project: {args.project}")
    print("=" * 60)
    
    # Handle SQL conversion mode FIRST to avoid premature initialization
    if args.convert_sql and args.sql_files:
        print("\n" + "=" * 60)
        print("🔄 SQL 多数据库转换")
        print("=" * 60)
        
        # Initialize SQL components for conversion
        sql_converter = SQLConverter()
        sql_validator = SQLValidator()
        print("\n" + "=" * 60)
        print("🔄 SQL 多数据库转换")
        print("=" * 60)
        
        for sql_file in args.sql_files:
            if not os.path.exists(sql_file):
                print(f"  ⚠️ 文件不存在: {sql_file}")
                continue
            
            print(f"\n📄 处理文件: {sql_file}")
            
            with open(sql_file, 'r', encoding='utf-8') as f:
                sql_content = f.read()
            
            # Convert to PostgreSQL
            pg_content, pg_changes = sql_converter.convert_to_postgresql(sql_content)
            print(f"  ✅ PostgreSQL 转换完成 ({len(pg_changes)} 项变更)")
            for change in pg_changes:
                print(f"    - {change}")
            
            # Convert to Oracle
            ora_content, ora_changes = sql_converter.convert_to_oracle(sql_content)
            print(f"  ✅ Oracle 转换完成 ({len(ora_changes)} 项变更)")
            for change in ora_changes:
                print(f"    - {change}")
            
            # Validate PostgreSQL
            print(f"\n  🔍 PostgreSQL 验证:")
            pg_results = sql_validator.validate_postgresql(pg_content)
            pg_summary = sql_validator.get_validation_summary(pg_results)
            print(f"    通过: {pg_summary['passed']}/{pg_summary['total']}, "
                  f"失败: {pg_summary['failed']}, 警告: {pg_summary['warnings']}")
            for r in pg_results:
                if r['status'] == 'FAIL':
                    print(f"    ❌ {r['rule']}: {r['message']}")
                elif r['status'] == 'WARN':
                    print(f"    ⚠️  {r['rule']}: {r['message']}")
            
            # Validate Oracle
            print(f"\n  🔍 Oracle 验证:")
            ora_results = sql_validator.validate_oracle(ora_content)
            ora_summary = sql_validator.get_validation_summary(ora_results)
            print(f"    通过: {ora_summary['passed']}/{ora_summary['total']}, "
                  f"失败: {ora_summary['failed']}, 警告: {ora_summary['warnings']}")
            for r in ora_results:
                if r['status'] == 'FAIL':
                    print(f"    ❌ {r['rule']}: {r['message']}")
                elif r['status'] == 'WARN':
                    print(f"    ⚠️  {r['rule']}: {r['message']}")
            
            # Save converted files
            output_dir = args.output_dir or os.path.dirname(sql_file)
            base_name = os.path.splitext(os.path.basename(sql_file))[0]
            
            pg_output = os.path.join(output_dir, f"{base_name}-postgres.sql")
            ora_output = os.path.join(output_dir, f"{base_name}-oracle.sql")
            
            with open(pg_output, 'w', encoding='utf-8') as f:
                f.write(f"-- PostgreSQL version (auto-converted from MySQL)\n")
                f.write(f"-- Source: {sql_file}\n")
                f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(pg_content)
            print(f"\n  💾 PostgreSQL 已保存: {pg_output}")
            
            with open(ora_output, 'w', encoding='utf-8') as f:
                f.write(f"-- Oracle version (auto-converted from MySQL)\n")
                f.write(f"-- Source: {sql_file}\n")
                f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(ora_content)
            print(f"  💾 Oracle 已保存: {ora_output}")
        
        print("\n" + "=" * 60)
        print("✅ SQL 转换完成")
        print("=" * 60)
        return
    
    # Get changed files
    if args.no_git:
        # Scan scripts/db directory
        changed_files = []
        db_dir = os.path.join(args.project, 'scripts', 'db')
        if os.path.exists(db_dir):
            for root, dirs, files in os.walk(db_dir):
                for f in files:
                    if f.endswith('.sql'):
                        full_path = os.path.join(root, f)
                        rel_path = os.path.relpath(full_path, args.project)
                        changed_files.append(ChangeFile(
                            path=rel_path,
                            change_type='A',
                            file_type='sql'
                        ))
    else:
        # Initialize components for normal analysis mode
        git_analyzer = GitAnalyzer(args.project)
        sql_analyzer = SQLAnalyzer()
        java_analyzer = JavaAnalyzer()
        config_analyzer = ConfigAnalyzer()
        component_detector = ReleaseComponentDetector()
        todo_generator = TodoGenerator()
        report_generator = MarkdownReportGenerator()
        
        changed_files = git_analyzer.get_changed_files(args.branch)
    
    print(f"Found {len(changed_files)} changed files")
    
    # Categorize files
    sql_files = [f.path for f in changed_files if f.file_type == 'sql']
    java_files = [f.path for f in changed_files if f.file_type == 'java']
    config_files = [f.path for f in changed_files if f.file_type in ('yml', 'properties')]
    
    print(f"  - SQL files: {len(sql_files)}")
    print(f"  - Java files: {len(java_files)}")
    print(f"  - Config files: {len(config_files)}")
    
    # Build report
    report = Report(
        changed_files=changed_files,
        sql_files=sql_files,
        java_files=java_files,
        config_files=config_files
    )
    
    # Analyze SQL files
    sql_issues = []
    for sql_file in sql_files:
        full_path = os.path.join(args.project, sql_file)
        if os.path.exists(full_path):
            issues = sql_analyzer.analyze_sql_file(full_path)
            sql_issues.extend(issues)
    
    report.sql_issues = sql_issues
    
    # Analyze Java files
    java_analysis = java_analyzer.analyze_java_files(changed_files)
    
    # Analyze config files
    config_analysis = config_analyzer.analyze_config_files(changed_files)
    
    # 自动检测发布组件（替代交互式询问）
    # 检测规则：
    # 1. 根据变更文件自动推断
    # 2. SQL 文件存在 → SQL 脚本
    # 3. Java 文件存在 → Java 代码
    # 4. 配置文件存在 → 配置文件变更
    # 5. 根据关键词匹配其他组件
    # 收集变更文件后，显示统计信息
    # 发布组件确认由 Skill 通过 Question 工具让用户选择
    # 这里只显示文件变更统计
    
    # 显示变更文件统计
    print("\n" + "=" * 60)
    print("📊 变更文件统计")
    print("=" * 60)
    print(f"  - SQL 文件: {len(sql_files)}")
    print(f"  - Java 文件: {len(java_files)}")
    print(f"  - 配置文件: {len(config_files)}")
    
    if sql_files:
        print("\n  SQL 变更文件:")
        for f in sql_files:
            print(f"    - {f}")
    
    # 显示检测到的变更类型（用于提示用户，但不自动设置组件）
    print("\n" + "=" * 60)
    print("💡 提示：请通过 Question 工具确认涉及哪些发布组件")
    print("=" * 60)
    
    # Default config - 发布组件将由 Skill 通过 Question 获取用户选择后传入
    config = {
        'release_components': {},  # 由 Skill 注入
        'project_path': args.project,
        'compare_branch': args.branch or 'main',
        'output_report': args.report is not None,
        'output_path': args.report or 'release-check-report.md'
    }
    
    # Generate todos
    report.todos = todo_generator.generate_todos(report)
    
    # Generate Markdown report
    if args.report:
        print("\n" + "=" * 60)
        print("📝 正在生成 Markdown 报告...")
        
        report_content = report_generator.generate_report(report, config, java_analysis)
        
        if report_generator.save_report(report_content, args.report):
            print(f"  ✅ 报告已保存: {args.report}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 检查结果汇总")
    print("=" * 60)
    print(f"变更文件总数: {len(changed_files)}")
    print(f"SQL 文件: {len(sql_files)}")
    print(f"Java 文件: {len(java_files)}")
    print(f"配置文件: {len(config_files)}")
    print(f"SQL 兼容性问题: {len(sql_issues)}")
    
    if sql_issues:
        print("\n⚠️ 兼容性问题:")
        for issue in sql_issues:
            print(f"  - [{issue.severity}] {issue.description}")


if __name__ == '__main__':
    main()