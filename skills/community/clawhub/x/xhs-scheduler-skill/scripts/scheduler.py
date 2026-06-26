#!/usr/bin/env python3
"""
定时调度器
负责定时检查并执行发布任务
"""

import time
import json
from datetime import datetime, timedelta
from typing import Dict, Optional
from pathlib import Path

from queue_manager import QueueManager
from publisher import XiaohongshuPublisher
from notifier import NotificationManager


class TaskScheduler:
    """任务调度器"""
    
    def __init__(self, config_path: str = None):
        """
        初始化调度器
        
        Args:
            config_path: 配置文件路径
        """
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 初始化组件
        self.queue = QueueManager()
        self.publisher = XiaohongshuPublisher(base_url=self.config.get('mcp_server_url', 'http://localhost:18060').replace('/mcp', ''))
        
        # 初始化通知器（如果配置了）
        self.notifier = None
        if any(k in self.config for k in ['feishu_webhook', 'dingtalk_webhook', 'telegram_bot_token']):
            self.notifier = NotificationManager(self.config)
        
        self.running = False
    
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置文件"""
        if config_path is None:
            # 默认配置文件路径
            base_dir = Path(__file__).parent.parent
            config_path = base_dir / 'config.yaml'
        
        if Path(config_path).exists():
            import yaml
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        
        # 默认配置
        return {
            'mcp_server_url': 'http://localhost:18060/mcp',
            'check_interval': 60,  # 检查间隔（秒）
            'max_publish_per_run': 3,  # 单次最大发布数量
            'publish_interval': 30,  # 发布间隔（秒）
        }
    
    def check_and_publish(self) -> Dict:
        """
        检查并执行发布任务
        
        Returns:
            执行结果统计
        """
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 检查待发布任务...")
        
        # 获取待发布任务
        pending_tasks = self.queue.get_pending_tasks()
        
        if not pending_tasks:
            print("  没有待发布的任务")
            return {'published': 0, 'failed': 0, 'skipped': 0}
        
        print(f"  发现 {len(pending_tasks)} 个待发布任务")
        
        # 限制单次发布数量
        tasks_to_publish = pending_tasks[:self.config.get('max_publish_per_run', 3)]
        
        results = {'published': 0, 'failed': 0, 'skipped': 0}
        
        for i, task in enumerate(tasks_to_publish):
            print(f"\n  [{i+1}/{len(tasks_to_publish)}] 发布: {task.title}")
            
            # 检查登录状态
            login_check = self.publisher.check_login_status()
            if not login_check.get('logged_in'):
                error_msg = login_check.get('error', '未登录')
                print(f"    [FAIL] 登录检查失败: {error_msg}")
                
                self.queue.update_task_status(task.task_id, 'failed', error_msg)
                
                if self.notifier:
                    self.notifier.notify_publish_failure(task.title, error_msg)
                
                results['failed'] += 1
                continue
            
            # 执行发布
            publish_result = self.publisher.publish_note(
                title=task.title,
                content=task.content,
                images=task.images,
                tags=task.tags
            )
            
            if publish_result['success']:
                # 更新状态为已发布
                self.queue.update_task_status(
                    task_id=task.task_id,
                    status='published',
                    platform_task_id=publish_result.get('note_id')
                )
                
                print(f"    [OK] 发布成功: {publish_result.get('url', '')}")
                
                # 发送成功通知
                if self.notifier:
                    self.notifier.notify_publish_success(
                        task.title,
                        publish_result.get('url', ''),
                        datetime.now()
                    )
                
                results['published'] += 1
            else:
                # 更新状态为失败
                error_msg = publish_result.get('error', '未知错误')
                self.queue.update_task_status(task.task_id, 'failed', error_msg)
                
                print(f"    [FAIL] 发布失败: {error_msg}")
                
                # 发送失败通知
                if self.notifier:
                    self.notifier.notify_publish_failure(task.title, error_msg)
                
                results['failed'] += 1
            
            # 发布间隔（避免触发风控）
            if i < len(tasks_to_publish) - 1:
                interval = self.config.get('publish_interval', 30)
                print(f"    等待 {interval} 秒后发布下一篇...")
                time.sleep(interval)
        
        # 汇总
        print(f"\n  本次执行结果:")
        print(f"    [OK] 成功: {results['published']}")
        print(f"    [FAIL] 失败: {results['failed']}")
        print(f"    [SKIP] 跳过: {results['skipped']}")
        
        return results
    
    def run(self, once: bool = False):
        """
        运行调度器
        
        Args:
            once: 是否只执行一次
        """
        print("=" * 50)
        print("小红书智能排期发布器 - 调度器")
        print("=" * 50)
        print(f"MCP服务: {self.config.get('mcp_server_url')}")
        print(f"检查间隔: {self.config.get('check_interval', 60)}秒")
        print(f"单次最大发布: {self.config.get('max_publish_per_run', 3)}篇")
        print("=" * 50)
        
        if once:
            # 只执行一次
            self.check_and_publish()
            return
        
        # 持续运行
        self.running = True
        print("\n调度器已启动，按 Ctrl+C 停止\n")
        
        try:
            while self.running:
                self.check_and_publish()
                
                # 等待下一次检查
                interval = self.config.get('check_interval', 60)
                print(f"\n  下次检查: {interval}秒后")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n调度器已停止")
            self.running = False
    
    def stop(self):
        """停止调度器"""
        self.running = False
    
    def get_status(self) -> Dict:
        """获取调度器状态"""
        stats = self.queue.get_statistics(days=7)
        pending = self.queue.get_pending_tasks()
        
        return {
            'running': self.running,
            'mcp_server': self.config.get('mcp_server_url'),
            'pending_count': len(pending),
            'statistics': stats
        }


class HeartbeatScheduler:
    """
    OpenClaw Heartbeat 调度器
    用于与OpenClaw的heartbeat机制集成
    """
    
    def __init__(self, scheduler: TaskScheduler):
        self.scheduler = scheduler
    
    def on_heartbeat(self, trigger_info: Dict) -> str:
        """
        处理heartbeat触发
        
        Args:
            trigger_info: 触发信息
            
        Returns:
            执行结果报告
        """
        print(f"\n[Heartbeat] 触发时间: {datetime.now()}")
        print(f"[Heartbeat] 触发信息: {trigger_info}")
        
        # 执行发布检查
        results = self.scheduler.check_and_publish()
        
        # 生成报告
        report = f"""
小红书定时发布执行报告
========================
执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

发布结果:
- 成功: {results['published']} 篇
- 失败: {results['failed']} 篇
- 跳过: {results['skipped']} 篇

待发布队列中还有 {self.scheduler.queue.get_pending_tasks().__len__()} 个任务等待执行。
        """
        
        return report


# CLI接口
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='小红书定时调度器')
    parser.add_argument('--config', help='配置文件路径')
    parser.add_argument('--once', action='store_true', help='只执行一次')
    parser.add_argument('--status', action='store_true', help='显示状态')
    
    args = parser.parse_args()
    
    scheduler = TaskScheduler(args.config)
    
    if args.status:
        status = scheduler.get_status()
        print("\n📊 调度器状态")
        print(f"  运行中: {'是' if status['running'] else '否'}")
        print(f"  MCP服务: {status['mcp_server']}")
        print(f"  待发布任务: {status['pending_count']}")
        print(f"\n  最近7天统计:")
        stats = status['statistics']
        print(f"    总任务: {stats['total_tasks']}")
        print(f"    已发布: {stats['published']}")
        print(f"    失败: {stats['failed']}")
        print(f"    成功率: {stats['success_rate']}%")
        print(f"    今日已发布: {stats['today_published']}")
    
    else:
        scheduler.run(once=args.once)
