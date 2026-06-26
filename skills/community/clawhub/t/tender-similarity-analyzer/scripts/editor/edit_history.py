# -*- coding: utf-8 -*-
"""
修改历史记录模块
支持修改回滚和差异导出
"""

import time
from typing import List, Dict, Optional
from pathlib import Path


class EditHistory:
    """
    修改历史记录器
    
    记录所有文档修改操作，支持回滚和差异导出
    """
    
    def __init__(self):
        self.operations = []
        self._enabled = True
        
    def record(self, para_index: int, run_index: int, 
               old_text: str, new_text: str, 
               file_path: str = None):
        """
        记录一次修改操作
        
        @param para_index: 段落索引
        @param run_index: run索引
        @param old_text: 原始文字
        @param new_text: 新文字
        @param file_path: 文件路径
        """
        if not self._enabled:
            return
            
        self.operations.append({
            'timestamp': time.time(),
            'datetime': time.strftime('%Y-%m-%d %H:%M:%S'),
            'para_index': para_index,
            'run_index': run_index,
            'old_text': old_text,
            'new_text': new_text,
            'file_path': file_path
        })
        
    def record_batch(self, operations: List[Dict]):
        """
        批量记录修改操作
        
        @param operations: 操作列表
        """
        for op in operations:
            self.record(
                para_index=op.get('para_index'),
                run_index=op.get('run_index', 0),
                old_text=op.get('old_text', ''),
                new_text=op.get('new_text', ''),
                file_path=op.get('file_path')
            )
            
    def rollback(self) -> List[Dict]:
        """
        生成回滚操作列表（逆向操作）
        
        @return: 回滚操作列表
        """
        rollbacks = []
        
        for op in reversed(self.operations):
            rollbacks.append({
                'para_index': op['para_index'],
                'run_index': op['run_index'],
                'old_text': op['new_text'],  # 交换
                'new_text': op['old_text'],  # 交换
                'file_path': op['file_path']
            })
            
        return rollbacks
        
    def export_diff(self) -> str:
        """
        导出修改差异报告
        
        @return: 差异报告文本
        """
        if not self.operations:
            return "无修改记录"
            
        lines = [
            "=" * 50,
            "文档修改差异报告",
            "=" * 50,
            f"总修改次数: {len(self.operations)}",
            f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "-" * 50,
        ]
        
        for i, op in enumerate(self.operations, 1):
            lines.append(f"\n修改 #{i}")
            lines.append(f"  时间: {op['datetime']}")
            lines.append(f"  位置: 段落{op['para_index']}, Run{op['run_index']}")
            lines.append(f"  原文: 「{op['old_text']}」")
            lines.append(f"  新文: 「{op['new_text']}」")
            
            # 标记改动
            old_len = len(op['old_text'])
            new_len = len(op['new_text'])
            diff = new_len - old_len
            
            if diff > 0:
                lines.append(f"  变化: +{diff} 字符")
            elif diff < 0:
                lines.append(f"  变化: {diff} 字符")
            else:
                lines.append(f"  变化: 0 字符（内容替换）")
                
        return '\n'.join(lines)
        
    def export_json(self) -> List[Dict]:
        """
        导出JSON格式的修改历史
        
        @return: 修改历史列表
        """
        return self.operations.copy()
        
    def get_operation_count(self) -> int:
        """获取操作总数"""
        return len(self.operations)
        
    def clear(self):
        """清空历史记录"""
        self.operations = []
        
    def enable(self):
        """启用记录"""
        self._enabled = True
        
    def disable(self):
        """禁用记录"""
        self._enabled = False
        
    def save_to_file(self, file_path: str):
        """
        保存历史到文件
        
        @param file_path: 文件路径
        """
        import json
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({
                'operations': self.operations,
                'export_time': time.strftime('%Y-%m-%d %H:%M:%S')
            }, f, ensure_ascii=False, indent=2)
            
    def load_from_file(self, file_path: str):
        """
        从文件加载历史
        
        @param file_path: 文件路径
        """
        import json
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.operations = data.get('operations', [])
