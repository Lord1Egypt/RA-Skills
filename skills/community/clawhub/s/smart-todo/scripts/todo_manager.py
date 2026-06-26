#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Todo Manager - 核心管理模块
"""

import json
import os
import re
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TodoManager:
    """代办管理器"""
    
    def __init__(self, config_path: Optional[str] = None):
        """初始化管理器"""
        self.config = self._load_config(config_path)
        self.storage_path = Path(self.config['storage_path'])
        self._ensure_storage_exists()
        
    def _load_config(self, config_path: Optional[str]) -> dict:
        """加载配置文件"""
        if config_path is None:
            # 默认使用脚本所在目录的 config
            script_dir = Path(__file__).parent.parent
            config_path = script_dir / 'assets' / 'config.json'
        else:
            config_path = Path(config_path)
            
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _ensure_storage_exists(self):
        """确保存储目录和文件存在"""
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        active_file = self.storage_path / 'active.md'
        archive_file = self.storage_path / 'archive.md'
        
        if not active_file.exists():
            self._create_empty_active_file(active_file)
        if not archive_file.exists():
            self._create_empty_archive_file(archive_file)
    
    def _create_empty_active_file(self, filepath: Path):
        """创建空的活动代办文件"""
        content = """# 活动代办列表

## 统计
- 总计: 0
- P0: 0
- P1: 0
- 进行中: 0
- 未开始: 0
- 暂停: 0

## 代办列表

---
最后更新: {timestamp}
""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_empty_archive_file(self, filepath: Path):
        """创建空的归档文件"""
        content = """# 归档代办列表

## 统计
- 总计: 0
- 已完成: 0
- 已终止: 0

## 归档列表

---
最后更新: {timestamp}
""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _generate_id(self) -> str:
        """生成新的代办ID"""
        todos = self.get_all_active_todos()
        if not todos:
            return f"{self.config['todo_id_prefix']}001"
        
        # 找到最大的ID号
        max_num = 0
        for todo in todos:
            match = re.search(rf'{self.config["todo_id_prefix"]}(\d+)', todo.get('id', ''))
            if match:
                max_num = max(max_num, int(match.group(1)))
        
        new_num = max_num + 1
        return f"{self.config['todo_id_prefix']}{new_num:03d}"
    
    def _calculate_similarity(self, str1: str, str2: str) -> float:
        """计算两个字符串的相似度"""
        return SequenceMatcher(None, str1, str2).ratio()
    
    def check_duplicate(self, name: str, description: str) -> List[Dict]:
        """
        检查是否有相似的代办
        逻辑：名称相似度 >= name_threshold 或 描述相似度 >= desc_threshold 即触发
        """
        config = self.config
        name_threshold = config.get('similarity_name_threshold', 0.7)
        desc_threshold = config.get('similarity_desc_threshold', 0.8)
        todos = self.get_all_active_todos()
        duplicates = []
        
        for todo in todos:
            name_sim = self._calculate_similarity(name, todo.get('name', ''))
            desc_sim = self._calculate_similarity(description, todo.get('original_description', ''))
            
            # 名称>=70% 或 描述>=80% 就算疑似重复
            if name_sim >= name_threshold or desc_sim >= desc_threshold:
                todo['_similarity'] = {
                    'name': round(name_sim * 100, 1),
                    'description': round(desc_sim * 100, 1)
                }
                duplicates.append(todo)
        
        return duplicates
    
    def add_todo(self, 
                 name: str,
                 original_description: str,
                 confirmed_understanding: str,
                 context: str,
                 priority: str = 'P1',
                 status: str = '未开始',
                 estimated_time: int = 20,
                 tags: List[str] = None) -> Dict:
        """
        添加新代办
        
        Args:
            name: 简略名称（≤10字）
            original_description: 原始描述
            confirmed_understanding: 确认理解
            context: 上下文信息
            priority: 优先级 (P0/P1)
            status: 状态
            estimated_time: 预估时间（分钟）
            tags: 标签列表
            
        Returns:
            创建的代办字典
        """
        # 检查重复
        duplicates = self.check_duplicate(name, original_description)
        
        todo = {
            'id': self._generate_id(),
            'name': name[:self.config['max_name_length']],
            'original_description': original_description,
            'confirmed_understanding': confirmed_understanding,
            'context': context,
            'priority': priority,
            'status': status,
            'estimated_time': estimated_time,
            'tags': tags or [],
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '_duplicates': duplicates  # 内部使用，不保存到文件
        }
        
        return todo
    
    def save_todo(self, todo: Dict) -> bool:
        """保存代办到文件"""
        try:
            # 移除内部字段
            todo_to_save = {k: v for k, v in todo.items() if not k.startswith('_')}
            
            todos = self.get_all_active_todos()
            todos.append(todo_to_save)
            
            self._save_active_todos(todos)
            return True
        except Exception as e:
            print(f"保存代办失败: {e}")
            return False
    
    def _save_active_todos(self, todos: List[Dict]):
        """保存所有活动代办到文件"""
        active_file = self.storage_path / 'active.md'
        
        # 统计
        total = len(todos)
        p0_count = sum(1 for t in todos if t.get('priority') == 'P0')
        p1_count = sum(1 for t in todos if t.get('priority') == 'P1')
        in_progress = sum(1 for t in todos if t.get('status') == '进行中')
        not_started = sum(1 for t in todos if t.get('status') == '未开始')
        paused = sum(1 for t in todos if t.get('status') == '暂停')
        
        # 生成代办列表文本
        todo_list_text = ""
        for todo in todos:
            todo_list_text += self._format_todo_entry(todo)
        
        content = f"""# 活动代办列表

## 统计
- 总计: {total}
- P0: {p0_count}
- P1: {p1_count}
- 进行中: {in_progress}
- 未开始: {not_started}
- 暂停: {paused}

## 代办列表

{todo_list_text}

---
最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(active_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _format_todo_entry(self, todo: Dict) -> str:
        """格式化单个代办条目"""
        tags_str = ', '.join(todo.get('tags', [])) if todo.get('tags') else '无'
        
        return f"""### [{todo['id']}] {todo['priority']} {todo['name']}
**状态**: {todo['status']}
**创建时间**: {todo['created_at']}
**更新时间**: {todo['updated_at']}
**预估时间**: {todo['estimated_time']}分钟

**原始描述**:
{todo['original_description']}

**确认理解**:
{todo['confirmed_understanding']}

**上下文**:
{todo['context']}

**标签**: {tags_str}

---

"""
    
    def get_all_active_todos(self) -> List[Dict]:
        """获取所有活动代办"""
        active_file = self.storage_path / 'active.md'
        
        if not active_file.exists():
            return []
        
        with open(active_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return self._parse_todos_from_markdown(content)
    
    def _parse_todos_from_markdown(self, content: str) -> List[Dict]:
        """从 Markdown 内容解析代办列表"""
        todos = []
        
        # 使用正则匹配代办条目
        pattern = r'###\s*\[(\w+)\]\s*(P\d)\s*(.+?)\n' \
                  r'\*\*状态\*\*:\s*(.+?)\n' \
                  r'\*\*创建时间\*\*:\s*(.+?)\n' \
                  r'\*\*更新时间\*\*:\s*(.+?)\n' \
                  r'\*\*预估时间\*\*:\s*(\d+)分钟\n' \
                  r'\n\*\*原始描述\*\*:\n(.+?)\n' \
                  r'\n\*\*确认理解\*\*:\n(.+?)\n' \
                  r'\n\*\*上下文\*\*:\n(.+?)\n' \
                  r'\n\*\*标签\*\*:\s*(.+?)(?:\n|$)'
        
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            todo = {
                'id': match.group(1),
                'priority': match.group(2),
                'name': match.group(3).strip(),
                'status': match.group(4).strip(),
                'created_at': match.group(5).strip(),
                'updated_at': match.group(6).strip(),
                'estimated_time': int(match.group(7)),
                'original_description': match.group(8).strip(),
                'confirmed_understanding': match.group(9).strip(),
                'context': match.group(10).strip(),
                'tags': [t.strip() for t in match.group(11).split(',') if t.strip() != '无']
            }
            todos.append(todo)
        
        return todos
    
    def get_todo_by_id(self, todo_id: str) -> Optional[Dict]:
        """通过ID获取代办"""
        todos = self.get_all_active_todos()
        for todo in todos:
            if todo['id'] == todo_id:
                return todo
        return None
    
    def update_todo_status(self, todo_id: str, new_status: str) -> bool:
        """更新代办状态"""
        todos = self.get_all_active_todos()
        
        for todo in todos:
            if todo['id'] == todo_id:
                old_status = todo['status']
                todo['status'] = new_status
                todo['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # 如果状态变为已完成或终止，归档
                if new_status in ['已完成', '终止']:
                    self._archive_todo(todo, old_status)
                    todos = [t for t in todos if t['id'] != todo_id]
                
                self._save_active_todos(todos)
                return True
        
        return False
    
    def _archive_todo(self, todo: Dict, original_status: str):
        """归档代办"""
        archive_file = self.storage_path / 'archive.md'
        
        archive_entry = {
            **todo,
            'original_status': original_status,
            'completed_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'archive_reason': '已完成' if todo['status'] == '已完成' else '已终止'
        }
        
        # 读取现有归档
        archives = []
        if archive_file.exists():
            with open(archive_file, 'r', encoding='utf-8') as f:
                content = f.read()
            archives = self._parse_archives_from_markdown(content)
        
        archives.append(archive_entry)
        self._save_archives(archives)
    
    def _parse_archives_from_markdown(self, content: str) -> List[Dict]:
        """从 Markdown 解析归档列表"""
        archives = []
        
        pattern = r'###\s*\[(\w+)\]\s*(P\d)\s*(.+?)\n' \
                  r'\*\*原状态\*\*:\s*(.+?)\n' \
                  r'\*\*创建时间\*\*:\s*(.+?)\n' \
                  r'\*\*完成/终止时间\*\*:\s*(.+?)\n' \
                  r'\*\*归档原因\*\*:\s*(.+?)\n'
        
        matches = re.finditer(pattern, content, re.DOTALL)
        
        for match in matches:
            archive = {
                'id': match.group(1),
                'priority': match.group(2),
                'name': match.group(3).strip(),
                'original_status': match.group(4).strip(),
                'created_at': match.group(5).strip(),
                'completed_at': match.group(6).strip(),
                'archive_reason': match.group(7).strip()
            }
            archives.append(archive)
        
        return archives
    
    def _save_archives(self, archives: List[Dict]):
        """保存归档列表"""
        archive_file = self.storage_path / 'archive.md'
        
        total = len(archives)
        completed = sum(1 for a in archives if a.get('archive_reason') == '已完成')
        terminated = sum(1 for a in archives if a.get('archive_reason') == '已终止')
        
        archive_list_text = ""
        for archive in archives:
            archive_list_text += f"""### [{archive['id']}] {archive['priority']} {archive['name']}
**原状态**: {archive['original_status']}
**创建时间**: {archive['created_at']}
**完成/终止时间**: {archive['completed_at']}
**归档原因**: {archive['archive_reason']}

**原始描述**:
{archive.get('original_description', 'N/A')}

**确认理解**:
{archive.get('confirmed_understanding', 'N/A')}

**上下文**:
{archive.get('context', 'N/A')}

---

"""
        
        content = f"""# 归档代办列表

## 统计
- 总计: {total}
- 已完成: {completed}
- 已终止: {terminated}

## 归档列表

{archive_list_text}

---
最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        with open(archive_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def get_summary(self) -> Dict:
        """获取代办摘要"""
        todos = self.get_all_active_todos()
        
        return {
            'total': len(todos),
            'p0': sum(1 for t in todos if t.get('priority') == 'P0'),
            'p1': sum(1 for t in todos if t.get('priority') == 'P1'),
            'in_progress': sum(1 for t in todos if t.get('status') == '进行中'),
            'not_started': sum(1 for t in todos if t.get('status') == '未开始'),
            'paused': sum(1 for t in todos if t.get('status') == '暂停'),
            'p0_in_progress': [t for t in todos if t.get('priority') == 'P0' and t.get('status') == '进行中']
        }
    
    def check_p0_alerts(self) -> List[Dict]:
        """检查需要提醒的 P0 代办"""
        threshold_hours = self.config.get('p0_alert_threshold_hours', 1)
        todos = self.get_all_active_todos()
        alerts = []
        
        now = datetime.now()
        
        for todo in todos:
            if todo.get('priority') == 'P0' and todo.get('status') == '进行中':
                try:
                    updated = datetime.strptime(todo['updated_at'], '%Y-%m-%d %H:%M:%S')
                    hours_elapsed = (now - updated).total_seconds() / 3600
                    
                    if hours_elapsed >= threshold_hours:
                        todo['_hours_elapsed'] = round(hours_elapsed, 1)
                        alerts.append(todo)
                except:
                    pass
        
        return alerts


# 便捷函数
def create_manager(config_path: Optional[str] = None) -> TodoManager:
    """创建管理器实例"""
    return TodoManager(config_path)


if __name__ == '__main__':
    # 简单测试
    manager = TodoManager()
    print(f"存储路径: {manager.storage_path}")
    print(f"配置: {json.dumps(manager.config, indent=2, ensure_ascii=False)}")
