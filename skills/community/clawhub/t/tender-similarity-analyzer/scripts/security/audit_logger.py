# -*- coding: utf-8 -*-
"""
审计日志模块
仅记录操作行为和元数据，不记录任何原文内容
"""

import time
import json
import hashlib
from typing import List, Dict, Optional
from pathlib import Path


class AuditLogger:
    """
    审计日志记录器
    
    核心原则：
    - 只记录操作类型、时间戳、哈希等元数据
    - 绝对不记录任何文件原文内容
    - 绝对不记录任何可能被还原的敏感信息
    """
    
    def __init__(self, log_dir: Optional[str] = None):
        self.log_dir = Path(log_dir) if log_dir else Path.home() / '.openclaw' / 'logs'
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_session = self._new_session_id()
        self.operations = []
        
    def _new_session_id(self) -> str:
        """生成新的会话ID"""
        return f"AUDIT-{int(time.time())}"
        
    def _hash_file(self, file_path: str) -> str:
        """
        计算文件哈希（仅用于标识，不记录内容）
        """
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        return hasher.hexdigest()[:16]  # 只保留前16位
            
    def _hash_text(self, text: str) -> str:
        """
        计算文本哈希（用于标识，不记录内容）
        """
        return hashlib.sha256(text.encode()).hexdigest()[:16]
        
    def log_operation(self, op_type: str, file_info: List[str], result: str, **kwargs):
        """
        记录操作日志
        
        @param op_type: 操作类型 (extract / compare / report / modify)
        @param file_info: 文件信息列表（仅哈希和名称，不含内容）
        @param result: 操作结果 (success / fail / warning)
        @param kwargs: 其他元数据
        """
        log_entry = {
            'session_id': self.current_session,
            'timestamp': time.time(),
            'datetime': time.strftime('%Y-%m-%d %H:%M:%S'),
            'operation': op_type,
            'file_count': len(file_info),
            'file_hashes': [],  # 仅记录哈希
            'result': result,
        }
        
        # 只记录文件哈希，不记录内容
        for info in file_info:
            if '(' in info and ')' in info:
                # 从 "filename (hash)" 格式中提取
                name = info.rsplit('(', 1)[0].strip()
                hash_val = info.rsplit('(', 1)[1].replace(')', '').strip()
                log_entry['file_hashes'].append({'name': name, 'hash': hash_val})
            else:
                log_entry['file_hashes'].append({'name': info, 'hash': 'unknown'})
                
        # 添加其他元数据
        for key, value in kwargs.items():
            if key not in ['original_text', 'content', 'text', 'paragraph']:
                log_entry[key] = value
                
        self.operations.append(log_entry)
        
        # 写入日志文件
        self._write_to_file(log_entry)
        
    def _write_to_file(self, entry: dict):
        """写入日志文件"""
        log_file = self.log_dir / f"audit_{time.strftime('%Y%m%d')}.jsonl"
        
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            
    def log_extraction(self, file_path: str, char_count: int, para_count: int, result: str):
        """记录文件提取操作"""
        file_hash = self._hash_file(file_path)
        
        self.log_operation(
            op_type='extract',
            file_info=[f"{Path(file_path).name} ({file_hash})"],
            result=result,
            char_count=char_count,
            para_count=para_count
        )
        
    def log_comparison(self, file1: str, file2: str, similarity: float, duplicate_paras: int):
        """记录文件比对操作"""
        self.log_operation(
            op_type='compare',
            file_info=[file1, file2],
            result='success' if similarity < 0.3 else 'warning',
            similarity=similarity,
            duplicate_paras=duplicate_paras
        )
        
    def log_report_generation(self, output_path: str, total_paras: int, 
                             duplicate_paras: int, overall_rate: float):
        """记录报告生成操作"""
        self.log_operation(
            op_type='report',
            file_info=[f"{Path(output_path).name}"],
            result='success',
            total_paras=total_paras,
            duplicate_paras=duplicate_paras,
            overall_rate=overall_rate
        )
        
    def log_modification(self, file_path: str, para_index: int, 
                        old_hash: str, new_hash: str):
        """记录文档修改操作"""
        self.log_operation(
            op_type='modify',
            file_info=[f"{Path(file_path).name} ({old_hash[:8]})"],
            result='success',
            para_index=para_index,
            old_hash=old_hash[:8],
            new_hash=new_hash[:8]
        )
        
    def get_recent_operations(self, limit: int = 100) -> List[Dict]:
        """获取最近的操作记录"""
        return self.operations[-limit:]
        
    def generate_audit_report(self) -> str:
        """生成审计报告"""
        if not self.operations:
            return "无操作记录"
            
        report_lines = [
            "=" * 50,
            "审计报告",
            "=" * 50,
            f"会话ID: {self.current_session}",
            f"记录数: {len(self.operations)}",
            f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "操作汇总:",
        ]
        
        op_counts = {}
        for op in self.operations:
            op_type = op['operation']
            op_counts[op_type] = op_counts.get(op_type, 0) + 1
            
        for op_type, count in op_counts.items():
            report_lines.append(f"  {op_type}: {count}")
            
        return '\n'.join(report_lines)
