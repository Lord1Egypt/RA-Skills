#!/usr/bin/env python3
"""
定时分发任务

支持定时自动执行内容分发。
"""

import argparse
import logging
import os
import sys
import time
from datetime import datetime, timedelta
from threading import Thread

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ScheduleManager:
    """定时任务管理器"""
    
    DAYS_MAP = {
        'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 
        'fri': 4, 'sat': 5, 'sun': 6
    }
    
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.running = False
        
    def run(self):
        """启动定时任务"""
        logger.info("=" * 60)
        logger.info("启动定时分发任务")
        logger.info("=" * 60)
        logger.info(f"执行时间: {self.args.time}")
        
        if self.args.days:
            logger.info(f"执行日期: {self.args.days}")
        elif self.args.daily:
            logger.info("执行频率: 每天")
            
        self.running = True
        
        try:
            while self.running:
                next_run = self._calculate_next_run()
                wait_seconds = (next_run - datetime.now()).total_seconds()
                
                logger.info(f"下次执行时间: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"等待 {int(wait_seconds)} 秒...")
                
                # 等待到执行时间
                time.sleep(min(wait_seconds, 3600))  # 最多等待1小时后检查
                
                if datetime.now() >= next_run:
                    self._execute_task()
                    
                if not self.args.daily and not self.args.days:
                    # 只执行一次
                    break
                    
        except KeyboardInterrupt:
            logger.info("定时任务已停止")
            
    def _calculate_next_run(self) -> datetime:
        """计算下次执行时间"""
        hour, minute = map(int, self.args.time.split(':'))
        now = datetime.now()
        next_run = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        
        if next_run <= now:
            # 今天的时间已过，设置为明天
            next_run += timedelta(days=1)
        
        # 如果指定了特定日期
        if self.args.days:
            allowed_days = [self.DAYS_MAP[d.strip().lower()] 
                          for d in self.args.days.split(',')]
            
            # 找到下一个允许的日期
            while next_run.weekday() not in allowed_days:
                next_run += timedelta(days=1)
        
        return next_run
    
    def _execute_task(self):
        """执行任务"""
        logger.info("\n" + "=" * 60)
        logger.info("开始执行分发任务")
        logger.info("=" * 60)
        
        import subprocess
        
        cmd = [sys.executable, "scripts/distribute.py"]
        
        if self.args.targets:
            cmd.extend(["--targets", self.args.targets])
        
        if self.args.use_app:
            cmd.append("--use-app")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            logger.info(result.stdout)
            
            if result.returncode == 0:
                logger.info("✅ 定时任务执行成功")
            else:
                logger.error("❌ 定时任务执行失败")
                if result.stderr:
                    logger.error(result.stderr)
                    
        except Exception as e:
            logger.error(f"任务执行异常: {e}")


def main():
    parser = argparse.ArgumentParser(description='定时分发任务')
    
    parser.add_argument('--time', required=True,
                       help='执行时间 (HH:MM)')
    parser.add_argument('--days',
                       help='执行日期 (如: mon,wed,fri)')
    parser.add_argument('--daily', action='store_true',
                       help='每天执行')
    parser.add_argument('--targets',
                       help='目标平台')
    parser.add_argument('--use-app', action='store_true',
                       help='使用桌面端 App')
    
    args = parser.parse_args()
    
    if not args.days and not args.daily:
        parser.error("请指定 --days 或 --daily")
    
    manager = ScheduleManager(args)
    manager.run()


if __name__ == '__main__':
    main()
