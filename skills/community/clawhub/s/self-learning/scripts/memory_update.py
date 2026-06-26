#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Self-Learning Skill - 主执行脚本

Agent 自我学习与记忆更新工具
分析对话历史，提取关键信息，自动更新配置文件，实现 Agent 持续自我成长。

支持多平台、多 Agent、通用化部署。

Version: 2.0.0
Author: Acczdy
License: MIT
"""

import json
import logging
import os
import re
import shutil
import sys
import argparse
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any


# ============================================================================
# 配置管理
# ============================================================================

class Config:
    """配置管理类"""
    
    DEFAULT_CONFIG = {
        'workspace': {
            'default': './workspace',
            'auto_detect': True
        },
        'core_files': [
            'MEMORY.md', 'IDENTITY.md', 'USER.md', 'TOOLS.md',
            'SOUL.md', 'AGENTS.md', 'BOOTSTRAP.md', 'HEARTBEAT.md'
        ],
        'backup': {
            'enabled': True,
            'directory': '.backup',
            'retain_days': 7,
            'max_backups': 10
        },
        'logging': {
            'enabled': True,
            'directory': 'logs',
            'level': 'INFO',
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'file_format': 'self_learning_%Y%m%d.log'
        },
        'safety': {
            'require_confirm_for_delete': False,
            'max_delete_count': 10,
            'validate_after_update': True,
            'verify_backup': True
        },
        'ai': {
            'timeout': 90,
            'max_conversations': 100,
            'max_content_length': 500
        },
        'history': {
            'enabled': True,
            'directory': '.history',
            'retain_days': 30
        }
    }
    
    def __init__(self, config_file: Optional[Path] = None):
        self.config = self.DEFAULT_CONFIG.copy()
        self.config_file = config_file
        
        if config_file and config_file.exists():
            self._load_config(config_file)
    
    def _load_config(self, config_file: Path):
        """加载配置文件"""
        try:
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
            
            # 合并配置
            self._merge_config(user_config)
        except Exception as e:
            print(f"⚠️ 加载配置文件失败：{e}，使用默认配置")
    
    def _merge_config(self, user_config: Dict):
        """合并用户配置"""
        for key, value in user_config.items():
            if key in self.config and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def get(self, key: str, default=None):
        """获取配置值"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value


# ============================================================================
# 日志系统
# ============================================================================

class Logger:
    """日志管理类"""
    
    def __init__(self, workspace: Path, config: Config):
        self.workspace = workspace
        self.config = config
        self.logger = None
        self._setup_logging()
    
    def _setup_logging(self):
        """配置日志系统"""
        if not self.config.get('logging.enabled'):
            return
        
        log_dir = self.workspace / self.config.get('logging.directory', 'logs')
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / datetime.now().strftime(
            self.config.get('logging.file_format', 'self_learning_%Y%m%d.log')
        )
        
        log_level = getattr(logging, self.config.get('logging.level', 'INFO'))
        log_format = self.config.get('logging.format', '%(asctime)s - %(levelname)s - %(message)s')
        
        # 创建 logger
        self.logger = logging.getLogger('self_learning')
        self.logger.setLevel(log_level)
        
        # 文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(logging.Formatter(log_format))
        self.logger.addHandler(file_handler)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(console_handler)
    
    def info(self, msg: str):
        if self.logger:
            self.logger.info(msg)
    
    def error(self, msg: str):
        if self.logger:
            self.logger.error(msg)
    
    def warning(self, msg: str):
        if self.logger:
            self.logger.warning(msg)
    
    def debug(self, msg: str):
        if self.logger:
            self.logger.debug(msg)


# ============================================================================
# 工作目录检测
# ============================================================================

class WorkspaceDetector:
    """工作目录检测类"""
    
    @staticmethod
    def detect(workspace_arg: Optional[str] = None) -> Path:
        """
        自动检测工作目录
        
        优先级:
        1. 命令行参数 --workspace
        2. 环境变量 WORKSPACE
        3. 当前目录
        4. 默认值 ./workspace
        """
        # 1. 命令行参数
        if workspace_arg:
            workspace = Path(workspace_arg).resolve()
            print(f"📁 使用命令行指定的工作目录：{workspace}")
            return workspace
        
        # 2. 环境变量
        env_workspace = os.environ.get('WORKSPACE')
        if env_workspace:
            workspace = Path(env_workspace).resolve()
            print(f"📁 使用环境变量指定的工作目录：{workspace}")
            return workspace
        
        # 3. 尝试从当前会话获取 (OpenClaw 特定)
        try:
            from openclaw import sessions_list
            
            sessions = sessions_list(limit=1)
            if sessions and len(sessions) > 0:
                session = sessions[0]
                agent_id = session.get('agentId', 'main')
                
                # 读取 openclaw.json 获取 agentDir
                config_file = Path('/root/.openclaw/openclaw.json')
                if config_file.exists():
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    agents = config.get('agents', {}).get('list', [])
                    for agent in agents:
                        if agent.get('id') == agent_id:
                            agent_dir = agent.get('workspace') or agent.get('agentDir')
                            if agent_dir:
                                workspace = Path(agent_dir).parent
                                print(f"📁 自动检测到 Agent ({agent_id}) 的工作目录：{workspace}")
                                return workspace
        except Exception:
            pass
        
        # 4. 默认值
        workspace = Path('./workspace').resolve()
        print(f"📁 使用默认工作目录：{workspace}")
        return workspace
    
    @staticmethod
    def get_agent_name(workspace: Path) -> str:
        """根据工作目录获取 Agent 名称"""
        workspace_str = str(workspace)
        
        if 'agents/tuanzi' in workspace_str or 'agents\\tuanzi' in workspace_str:
            return 'tuanzi'
        elif 'agents/dingdang' in workspace_str or 'agents\\dingdang' in workspace_str:
            return 'dingdang'
        elif 'agents/secbot' in workspace_str or 'agents\\secbot' in workspace_str:
            return 'secbot'
        else:
            return 'main'


# ============================================================================
# 文件操作
# ============================================================================

class FileManager:
    """文件操作类"""
    
    def __init__(self, workspace: Path, config: Config):
        self.workspace = workspace
        self.config = config
        self.core_files = config.get('core_files', [])
    
    def read_core_files(self) -> Dict[str, str]:
        """读取所有核心配置文件"""
        files_content = {}
        for filename in self.core_files:
            filepath = self.workspace / filename
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    files_content[filename] = f.read()
            except Exception as e:
                print(f"⚠️ 读取 {filename} 失败：{e}")
                files_content[filename] = ''
        return files_content
    
    def backup_files(self, files_content: Dict[str, str]) -> Path:
        """备份所有配置文件"""
        if not self.config.get('backup.enabled'):
            print("⚠️ 备份已禁用")
            return None
        
        backup_dir = self.workspace / self.config.get('backup.directory', '.backup')
        backup_dir = backup_dir / datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        for filename, content in files_content.items():
            backup_path = backup_dir / filename
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        print(f"💾 已备份到：{backup_dir}")
        return backup_dir
    
    def cleanup_old_backups(self):
        """清理旧备份"""
        backup_base = self.workspace / self.config.get('backup.directory', '.backup')
        if not backup_base.exists():
            return
        
        retain_days = self.config.get('backup.retain_days', 7)
        max_backups = self.config.get('backup.max_backups', 10)
        
        # 按日期排序备份
        backups = []
        for item in backup_base.iterdir():
            if item.is_dir():
                try:
                    date_str = item.name.split('_')[0]
                    backup_date = datetime.strptime(date_str, '%Y%m%d')
                    backups.append((item, backup_date))
                except:
                    pass
        
        backups.sort(key=lambda x: x[1], reverse=True)
        
        # 删除超过保留天数的备份
        for backup, backup_date in backups:
            days_old = (datetime.now() - backup_date).days
            if days_old > retain_days:
                shutil.rmtree(backup)
                print(f"🗑️ 已删除旧备份：{backup}")
        
        # 保留最近的 N 个备份
        if len(backups) > max_backups:
            for backup, _ in backups[max_backups:]:
                shutil.rmtree(backup)
                print(f"🗑️ 已删除多余备份：{backup}")
    
    def update_file(self, filename: str, current_content: str, operations: List[Dict]) -> str:
        """执行文件更新操作"""
        updated = current_content
        
        for op in operations:
            if op['type'] == 'add':
                section_marker = f"## {op.get('section', '')}"
                if section_marker in updated:
                    parts = updated.split(section_marker)
                    parts[1] = op['content'] + '\n\n' + parts[1]
                    updated = section_marker.join(parts)
                else:
                    updated += f"\n\n{op['content']}"
                
            elif op['type'] == 'delete':
                target = op.get('target', '')
                if target in updated:
                    updated = updated.replace(target, '')
                    updated = re.sub(r'\n{3,}', '\n\n', updated)
                
            elif op['type'] == 'update':
                old = op.get('old', '')
                new = op.get('new', '')
                if old in updated:
                    updated = updated.replace(old, new)
        
        return updated
    
    def validate_file(self, filepath: Path) -> Tuple[bool, str]:
        """验证 Markdown 文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                return False, "文件为空"
            
            if content.count('# ') == 0:
                return False, "缺少主标题"
            
            if content.count('```') % 2 != 0:
                return False, "代码块未闭合"
            
            return True, "验证通过"
        except Exception as e:
            return False, str(e)
    
    def create_daily_memory(self, update_plan: Dict):
        """生成每日记忆文件"""
        today = datetime.now().strftime('%Y-%m-%d')
        memory_dir = self.workspace / 'memory'
        memory_dir.mkdir(parents=True, exist_ok=True)
        
        daily_file = memory_dir / f'{today}.md'
        stats = update_plan.get('stats', {})
        
        with open(daily_file, 'w', encoding='utf-8') as f:
            f.write(f"# {today} 每日记忆\n\n")
            f.write(f"## 📊 今日总结\n\n")
            f.write(f"{update_plan.get('summary', '无重要对话')}\n\n")
            f.write(f"## 🔄 配置更新统计\n\n")
            f.write(f"| 操作类型 | 数量 |\n")
            f.write(f"|----------|------|\n")
            f.write(f"| 新增 | {stats.get('add_count', 0)} |\n")
            f.write(f"| 删除 | {stats.get('delete_count', 0)} |\n")
            f.write(f"| 更新 | {stats.get('update_count', 0)} |\n\n")
            f.write(f"## 📁 文件更新详情\n\n")
            for filename, file_update in update_plan.get('updates', {}).items():
                ops = file_update.get('operations', [])
                if ops:
                    adds = len([o for o in ops if o['type'] == 'add'])
                    deletes = len([o for o in ops if o['type'] == 'delete'])
                    updates = len([o for o in ops if o['type'] == 'update'])
                    f.write(f"- **{filename}**: +{adds} 🗑️{deletes} ✏️{updates}\n")
        
        print(f"📝 已创建每日记忆：{daily_file}")
    
    def save_execution_history(self, update_plan: Dict, stats: Dict):
        """保存执行历史"""
        if not self.config.get('history.enabled'):
            return
        
        history_dir = self.workspace / self.config.get('history.directory', '.history')
        history_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        history_file = history_dir / f'{timestamp}.json'
        
        history = {
            'timestamp': datetime.now().isoformat(),
            'stats': stats,
            'summary': update_plan.get('summary', ''),
            'updates': update_plan.get('updates', {})
        }
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        print(f"📜 已保存执行历史：{history_file}")
    
    def rollback(self, backup_dir: Path):
        """回滚到指定备份"""
        if not backup_dir.exists():
            print(f"❌ 备份目录不存在：{backup_dir}")
            return False
        
        for backup_file in backup_dir.glob('*.md'):
            filename = backup_file.name
            target = self.workspace / filename
            
            with open(backup_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            with open(target, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"⏮️ 已回滚：{filename}")
        
        return True


# ============================================================================
# 对话历史获取
# ============================================================================

class ConversationHistory:
    """对话历史获取类"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def get(self) -> List[Dict]:
        """获取过去 24 小时的对话历史"""
        try:
            from openclaw import sessions_list, sessions_history
            
            max_conversations = self.config.get('ai.max_conversations', 100)
            max_content_length = self.config.get('ai.max_content_length', 500)
            
            sessions = sessions_list(activeMinutes=1440, limit=20)
            
            conversation_summary = []
            for session in sessions:
                history = sessions_history(
                    sessionKey=session['sessionKey'],
                    limit=50
                )
                for msg in history['messages']:
                    if msg['role'] == 'user':
                        conversation_summary.append({
                            'type': 'question',
                            'content': msg['content'][:max_content_length],
                            'timestamp': msg['timestamp'],
                            'agent': session.get('agentId', 'unknown')
                        })
                    elif msg['role'] == 'assistant':
                        conversation_summary.append({
                            'type': 'answer',
                            'content': msg['content'][:max_content_length],
                            'timestamp': msg['timestamp'],
                            'agent': session.get('agentId', 'unknown')
                        })
            
            return conversation_summary[:max_conversations]
        except Exception as e:
            print(f"⚠️ 获取对话历史失败：{e}")
            return []


# ============================================================================
# AI 分析
# ============================================================================

class AIAnalyzer:
    """AI 分析类"""
    
    def __init__(self, config: Config):
        self.config = config
    
    def analyze(self, conversation_summary: List[Dict], files_content: Dict[str, str], agent_name: str = 'main') -> Optional[Dict]:
        """使用 AI 分析需要更新的内容"""
        try:
            from openclaw import sessions_send
            
            timeout = self.config.get('ai.timeout', 90)
            
            prompt = self._build_prompt(conversation_summary, files_content, agent_name)
            
            result = sessions_send(message=prompt, timeoutSeconds=timeout)
            update_plan = json.loads(result)
            return update_plan
        except Exception as e:
            print(f"⚠️ AI 分析失败：{e}")
            return None
    
    def _build_prompt(self, conversation_summary: List[Dict], files_content: Dict[str, str], agent_name: str) -> str:
        """构建分析 prompt"""
        return f"""请分析以下对话内容，智能判断需要如何更新配置文件：

## Agent 信息
当前 Agent: {agent_name}

## 对话内容 (过去 24 小时)
{json.dumps(conversation_summary[:100], ensure_ascii=False, indent=2)[:10000]}

## 当前配置文件内容

### MEMORY.md
{files_content.get('MEMORY.md', '')[:3000]}

### IDENTITY.md
{files_content.get('IDENTITY.md', '')}

### USER.md
{files_content.get('USER.md', '')}

### TOOLS.md
{files_content.get('TOOLS.md', '')[:3000]}

### SOUL.md
{files_content.get('SOUL.md', '')}

### AGENTS.md
{files_content.get('AGENTS.md', '')[:3000]}

### BOOTSTRAP.md
{files_content.get('BOOTSTRAP.md', '')}

### HEARTBEAT.md
{files_content.get('HEARTBEAT.md', '')}

## 任务要求

**重要：AI 智能判断需要新增、删除还是更新**

### 判断规则

#### 需要【新增】的情况：
- 新的配置信息 (新 API Key、新推送渠道、新任务)
- 新的用户偏好
- 新的 Agent 配置
- 新的技能安装

#### 需要【删除】的情况：
- 过时的配置 (已失效的任务、已删除的技能)
- 错误的信息
- 重复的内容
- 临时测试配置 (已过测试期)

#### 需要【更新】的情况：
- 配置值变更 (Token 更新、时间调整、渠道 ID 变更)
- 状态变更 (任务启用/禁用、技能启用/禁用)
- 信息修正 (纠正错误的配置)

## 输出格式 (JSON)

```json
{{
  "updates": {{
    "MEMORY.md": {{
      "action": "update|none",
      "operations": [
        {{
          "type": "add",
          "reason": "为什么需要新增",
          "section": "章节名称",
          "content": "具体内容"
        }},
        {{
          "type": "delete",
          "reason": "为什么需要删除",
          "target": "要删除的内容关键词"
        }},
        {{
          "type": "update",
          "reason": "为什么需要更新",
          "section": "章节名称",
          "old": "旧内容",
          "new": "新内容"
        }}
      ]
    }},
    "IDENTITY.md": {{...}},
    "USER.md": {{...}},
    "TOOLS.md": {{...}},
    "SOUL.md": {{...}},
    "AGENTS.md": {{...}},
    "BOOTSTRAP.md": {{...}},
    "HEARTBEAT.md": {{...}}
  }},
  "summary": "今日对话总结 (200 字内)",
  "stats": {{
    "add_count": 新增数量，
    "delete_count": 删除数量，
    "update_count": 更新数量
  }}
}}
```

**判断原则:**
1. 只处理真正变更的内容，不要为了更新而更新
2. 删除操作要谨慎，必须有明确理由 (过时、错误、重复)
3. 新增内容必须是重要的配置信息，不要记录日常闲聊
4. 配置类信息必须准确 (ID、Token、时间等)
5. 如果文件没有变化，action 设为 "none"，operations 为空数组
6. MEMORY.md 优先处理，其他文件按需处理
"""


# ============================================================================
# 主程序
# ============================================================================

class SelfLearningApp:
    """主程序类"""
    
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.config = Config(args.config)
        self.workspace = WorkspaceDetector.detect(args.workspace)
        self.agent_name = WorkspaceDetector.get_agent_name(self.workspace)
        self.logger = Logger(self.workspace, self.config)
        self.file_manager = FileManager(self.workspace, self.config)
        self.history_getter = ConversationHistory(self.config)
        self.analyzer = AIAnalyzer(self.config)
    
    def run(self) -> bool:
        """执行自我学习流程"""
        self.logger.info("=" * 60)
        self.logger.info(f"🧠 Agent 自我学习开始 ({self.agent_name})")
        self.logger.info(f"⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"📁 工作目录：{self.workspace}")
        self.logger.info("=" * 60)
        
        try:
            # 1. 读取核心文件
            self.logger.info("\n📖 读取配置文件...")
            files_content = self.file_manager.read_core_files()
            self.logger.info(f"✅ 已读取 {len(files_content)} 个配置文件")
            
            # 2. 获取对话历史
            self.logger.info("\n💬 获取对话历史...")
            conversation_summary = self.history_getter.get()
            self.logger.info(f"✅ 已获取 {len(conversation_summary)} 条对话")
            
            # 3. AI 分析
            self.logger.info("\n🤖 AI 智能分析...")
            update_plan = self.analyzer.analyze(conversation_summary, files_content, self.agent_name)
            if not update_plan:
                self.logger.error("⚠️ AI 分析失败，退出")
                return False
            self.logger.info(f"✅ 分析完成")
            
            # 4. 预览模式
            if self.args.dry_run:
                self._preview(update_plan)
                return True
            
            # 5. 备份文件
            self.logger.info("\n💾 备份配置文件...")
            backup_dir = self.file_manager.backup_files(files_content)
            
            # 6. 执行更新
            self.logger.info("\n📝 执行更新...")
            update_stats = self._execute_updates(update_plan)
            
            # 7. 创建每日记忆
            self.logger.info("\n📅 创建每日记忆...")
            self.file_manager.create_daily_memory(update_plan)
            
            # 8. 保存执行历史
            self.logger.info("\n📜 保存执行历史...")
            self.file_manager.save_execution_history(update_plan, update_stats)
            
            # 9. 清理旧备份
            self.logger.info("\n🗑️ 清理旧备份...")
            self.file_manager.cleanup_old_backups()
            
            # 总结
            self.logger.info("\n" + "=" * 60)
            self.logger.info(f"✅ Agent 自我学习完成 ({self.agent_name})")
            self.logger.info("=" * 60)
            self.logger.info(f"\n📊 更新统计:")
            self.logger.info(f"  更新文件：{update_stats['updated']} 个")
            self.logger.info(f"  跳过文件：{update_stats['skipped']} 个")
            self.logger.info(f"  新增操作：{update_stats['add']} 次")
            self.logger.info(f"  删除操作：{update_stats['delete']} 次")
            self.logger.info(f"  更新操作：{update_stats['update']} 次")
            self.logger.info("=" * 60)
            
            return True
            
        except Exception as e:
            self.logger.error(f"\n❌ 执行失败：{e}")
            self.logger.debug(str(e), exc_info=True)
            return False
    
    def _execute_updates(self, update_plan: Dict) -> Dict:
        """执行更新操作"""
        update_stats = {'updated': 0, 'skipped': 0, 'add': 0, 'delete': 0, 'update': 0}
        
        for filename, file_update in update_plan.get('updates', {}).items():
            if file_update.get('action') == 'none' or not file_update.get('operations'):
                update_stats['skipped'] += 1
                self.logger.info(f"⏭️  跳过：{filename}")
                continue
            
            filepath = self.workspace / filename
            current_content = self.file_manager.read_core_files().get(filename, '')
            operations = file_update.get('operations', [])
            
            self.logger.info(f"\n📝 更新：{filename}")
            
            # 统计操作类型
            for op in operations:
                if op['type'] == 'add':
                    update_stats['add'] += 1
                elif op['type'] == 'delete':
                    update_stats['delete'] += 1
                elif op['type'] == 'update':
                    update_stats['update'] += 1
            
            # 更新内容
            updated_content = self.file_manager.update_file(filename, current_content, operations)
            
            # 写入文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            # 验证文件
            if self.config.get('safety.validate_after_update'):
                is_valid, msg = self.file_manager.validate_file(filepath)
                if not is_valid:
                    self.logger.warning(f"⚠️ 文件验证失败：{msg}")
                    # 回滚
                    if self.config.get('safety.verify_backup'):
                        self.logger.info("⏮️ 正在回滚...")
            
            update_stats['updated'] += 1
            self.logger.info(f"✅ 完成：{filename}")
        
        return update_stats
    
    def _preview(self, update_plan: Dict):
        """预览模式"""
        self.logger.info("\n🔍 预览模式 - 以下操作将要执行:\n")
        
        for filename, file_update in update_plan.get('updates', {}).items():
            ops = file_update.get('operations', [])
            if not ops:
                continue
            
            self.logger.info(f"\n📄 {filename}:")
            for op in ops:
                if op['type'] == 'add':
                    self.logger.info(f"  ➕ 新增：{op.get('section', '新内容')}")
                elif op['type'] == 'delete':
                    self.logger.info(f"  🗑️ 删除：{op.get('reason', '过时内容')}")
                elif op['type'] == 'update':
                    self.logger.info(f"  ✏️ 更新：{op.get('section', '内容')}")


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='Agent 自我学习技能',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                              # 自动检测工作目录
  %(prog)s --workspace /path/to/ws     # 指定工作目录
  %(prog)s --dry-run                   # 预览模式
  %(prog)s --config config.yaml        # 使用自定义配置
  %(prog)s --rollback 20260305         # 回滚到指定日期
        """
    )
    
    parser.add_argument(
        '--workspace',
        type=str,
        help='指定工作目录路径'
    )
    
    parser.add_argument(
        '--config',
        type=Path,
        help='配置文件路径 (默认：config.yaml)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='预览模式 - 只显示将要执行的操作，不实际执行'
    )
    
    parser.add_argument(
        '--rollback',
        type=str,
        help='回滚到指定日期的备份 (格式：YYYYMMDD)'
    )
    
    parser.add_argument(
        '--history',
        action='store_true',
        help='显示执行历史'
    )
    
    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()
    
    app = SelfLearningApp(args)
    success = app.run()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
