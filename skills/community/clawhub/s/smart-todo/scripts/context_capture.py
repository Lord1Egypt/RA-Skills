#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Context Capture - 上下文捕获模块
用于捕获当前工作状态的完整上下文
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class ContextCapture:
    """上下文捕获器"""
    
    def __init__(self, workspace_root: Optional[str] = None):
        """
        初始化捕获器
        
        Args:
            workspace_root: 工作空间根目录，默认为当前目录
        """
        self.workspace_root = Path(workspace_root) if workspace_root else Path.cwd()
        self.captured_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def capture_full_context(self, 
                            conversation_history: Optional[List[str]] = None,
                            current_goal: Optional[str] = None,
                            todo_list_state: Optional[List[Dict]] = None,
                            notes: Optional[str] = None) -> Dict:
        """
        捕获完整的工作上下文
        
        Args:
            conversation_history: 最近的对话历史（最后 N 条）
            current_goal: 当前工作目标
            todo_list_state: 当前的 todo 列表状态
            notes: 额外备注
            
        Returns:
            完整的上下文字典
        """
        context = {
            'captured_at': self.captured_at,
            'workspace_root': str(self.workspace_root),
            'open_files': self._get_open_files(),
            'recent_files': self._get_recent_files(),
            'current_goal': current_goal or '未指定',
            'todo_list_state': todo_list_state or [],
            'conversation_history': conversation_history or [],
            'environment': self._get_environment_info(),
            'notes': notes or ''
        }
        
        return context
    
    def _get_open_files(self) -> List[str]:
        """
        获取当前打开的文件列表
        
        注意：此功能依赖于 IDE/编辑器提供的接口
        在 WorkBuddy 环境中，可以通过以下方式获取：
        1. 检查最近修改的文件
        2. 检查 .workbuddy/memory/ 中的记录
        3. 检查当前工作目录下的文件状态
        """
        open_files = []
        
        # 方法1：检查最近修改的文件（5分钟内）
        try:
            recent_files = self._find_recently_modified_files(minutes=5)
            open_files.extend(recent_files)
        except Exception as e:
            open_files.append(f"[无法获取最近文件: {e}]")
        
        # 方法2：检查 .workbuddy/memory/ 目录
        try:
            memory_files = self._check_memory_files()
            if memory_files:
                open_files.extend(memory_files)
        except:
            pass
        
        # 去重
        return list(dict.fromkeys(open_files)) if open_files else ['[无打开文件]']
    
    def _find_recently_modified_files(self, minutes: int = 5) -> List[str]:
        """查找最近修改的文件"""
        recent_files = []
        cutoff_time = datetime.now().timestamp() - (minutes * 60)
        
        # 遍历工作目录，查找最近修改的文件
        # 限制遍历深度和文件数量，避免性能问题
        max_files = 20
        count = 0
        
        for root, dirs, files in os.walk(self.workspace_root):
            # 跳过常见的不相关目录
            dirs[:] = [d for d in dirs if d not in [
                'node_modules', '.git', '__pycache__', '.workbuddy',
                'dist', 'build', '.idea', '.vscode', 'venv', '.venv'
            ]]
            
            for file in files:
                if count >= max_files:
                    break
                    
                # 只关注代码文件
                if not file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', 
                                      '.html', '.css', '.scss', '.java',
                                      '.cpp', '.c', '.h', '.go', '.rs',
                                      '.md', '.json', '.yaml', '.yml')):
                    continue
                
                filepath = Path(root) / file
                try:
                    mtime = filepath.stat().st_mtime
                    if mtime > cutoff_time:
                        recent_files.append(str(filepath.relative_to(self.workspace_root)))
                        count += 1
                except:
                    pass
            
            if count >= max_files:
                break
        
        return recent_files
    
    def _check_memory_files(self) -> List[str]:
        """检查 memory 目录中的记录"""
        memory_files = []
        memory_dir = self.workspace_root / '.workbuddy' / 'memory'
        
        if not memory_dir.exists():
            return memory_files
        
        # 读取最近的 memory 文件
        try:
            md_files = sorted(memory_dir.glob('*.md'), key=lambda x: x.stat().st_mtime, reverse=True)
            
            if md_files:
                # 读取最近的一个文件，提取提及的文件路径
                with open(md_files[0], 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 简单的启发式：查找可能的路径
                # 匹配常见的文件路径模式
                import re
                path_pattern = r'[\w\-./\\]+\.(?:py|js|ts|jsx|tsx|html|css|java|go|rs|md|json)'
                matches = re.findall(path_pattern, content)
                
                # 去重并限制数量
                seen = set()
                for match in matches[:10]:
                    if match not in seen:
                        seen.add(match)
                        memory_files.append(f"[来自记忆] {match}")
        except Exception as e:
            pass
        
        return memory_files
    
    def _get_recent_files(self, count: int = 5) -> List[str]:
        """获取最近访问的文件"""
        recent_files = []
        
        try:
            # 获取所有文件按修改时间排序
            all_files = []
            for root, dirs, files in os.walk(self.workspace_root):
                # 跳过不相关目录
                dirs[:] = [d for d in dirs if d not in [
                    'node_modules', '.git', '__pycache__', '.workbuddy',
                    'dist', 'build', '.idea', '.vscode'
                ]]
                
                for file in files:
                    if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', 
                                    '.html', '.css', '.md', '.json')):
                        filepath = Path(root) / file
                        try:
                            mtime = filepath.stat().st_mtime
                            all_files.append((mtime, str(filepath.relative_to(self.workspace_root))))
                        except:
                            pass
            
            # 按时间排序，取最近的
            all_files.sort(reverse=True)
            recent_files = [f[1] for f in all_files[:count]]
            
        except Exception as e:
            recent_files.append(f"[无法获取: {e}]")
        
        return recent_files if recent_files else ['[无]']
    
    def _get_environment_info(self) -> Dict:
        """获取环境信息"""
        return {
            'platform': os.name,
            'current_directory': str(Path.cwd()),
            'workspace': str(self.workspace_root),
            'timestamp': self.captured_at
        }
    
    def format_context_for_todo(self, context: Dict) -> str:
        """
        将上下文格式化为待办可用的文本格式
        
        Args:
            context: 上下文字典
            
        Returns:
            格式化的文本
        """
        lines = [
            f"捕获时间: {context['captured_at']}",
            f"",
            f"【当前目标】",
            context['current_goal'],
            f"",
            f"【打开的文件】",
        ]
        
        for f in context['open_files']:
            lines.append(f"  - {f}")
        
        lines.extend([
            f"",
            f"【最近文件】",
        ])
        
        for f in context['recent_files'][:5]:
            lines.append(f"  - {f}")
        
        if context.get('todo_list_state'):
            lines.extend([
                f"",
                f"【相关待办】",
            ])
            for todo in context['todo_list_state'][:3]:
                lines.append(f"  - [{todo.get('id', 'N/A')}] {todo.get('name', 'N/A')}")
        
        if context.get('conversation_history'):
            lines.extend([
                f"",
                f"【对话摘要】",
            ])
            for msg in context['conversation_history'][-5:]:
                lines.append(f"  > {msg[:100]}..." if len(msg) > 100 else f"  > {msg}")
        
        if context.get('notes'):
            lines.extend([
                f"",
                f"【备注】",
                context['notes']
            ])
        
        return '\n'.join(lines)
    
    def capture_for_interruption(self,
                                 current_task_description: str,
                                 conversation_history: Optional[List[str]] = None,
                                 reason: Optional[str] = None) -> Dict:
        """
        专门为工作中断场景捕获上下文
        
        Args:
            current_task_description: 当前任务的描述
            conversation_history: 对话历史
            reason: 中断原因
            
        Returns:
            包含完整中断信息的上下文
        """
        context = self.capture_full_context(
            conversation_history=conversation_history,
            current_goal=current_task_description,
            notes=f"工作中断 | 原因: {reason or '未指定'}"
        )
        
        # 添加中断特定信息
        context['interruption'] = {
            'reason': reason or '未指定',
            'task_description': current_task_description,
            'suggested_resume_point': self._suggest_resume_point(conversation_history)
        }
        
        return context
    
    def _suggest_resume_point(self, conversation_history: Optional[List[str]]) -> str:
        """建议恢复点"""
        if not conversation_history:
            return "从头开始"
        
        # 简单的启发式：取最后一条非空消息作为恢复点
        for msg in reversed(conversation_history):
            if msg and len(msg) > 10:
                return f"从以下位置继续: {msg[:80]}..."
        
        return "查看上下文后决定"


# 便捷函数
def capture_current_context(**kwargs) -> Dict:
    """快速捕获当前上下文"""
    capture = ContextCapture()
    return capture.capture_full_context(**kwargs)


def capture_for_interruption(task_description: str, **kwargs) -> Dict:
    """快速捕获中断上下文"""
    capture = ContextCapture()
    return capture.capture_for_interruption(task_description, **kwargs)


def format_context(context: Dict) -> str:
    """格式化上下文为可读文本"""
    capture = ContextCapture()
    return capture.format_context_for_todo(context)


if __name__ == '__main__':
    # 简单测试
    capture = ContextCapture()
    context = capture.capture_full_context(
        current_goal="测试上下文捕获功能",
        conversation_history=["用户: 测试一下", "助手: 好的"]
    )
    print("上下文捕获测试:")
    print(json.dumps(context, indent=2, ensure_ascii=False))
    print("\n格式化输出:")
    print(capture.format_context_for_todo(context))
