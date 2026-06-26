#!/usr/bin/env python3
"""
批量内容分发工具

支持批量同步多篇笔记到多个平台。
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import List, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BatchDistributor:
    """批量分发器"""
    
    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.processed_count = 0
        self.success_count = 0
        self.failed_count = 0
        
    def run(self):
        """执行批量分发"""
        logger.info("=" * 60)
        logger.info("开始批量内容分发")
        logger.info("=" * 60)
        
        # 获取笔记列表
        notes = self._get_notes()
        if not notes:
            logger.warning("没有找到需要分发的笔记")
            return
        
        logger.info(f"共找到 {len(notes)} 篇笔记")
        
        # 逐个处理
        for i, note_id in enumerate(notes, 1):
            logger.info(f"\n[{i}/{len(notes)}] 处理笔记: {note_id}")
            
            try:
                success = self._distribute_single(note_id)
                if success:
                    self.success_count += 1
                else:
                    self.failed_count += 1
            except Exception as e:
                logger.error(f"处理失败: {e}")
                self.failed_count += 1
            
            self.processed_count += 1
            
            # 批次间隔
            if i < len(notes) and self.args.interval > 0:
                logger.info(f"等待 {self.args.interval} 秒后处理下一篇...")
                time.sleep(self.args.interval)
        
        # 输出统计
        self._print_summary()
    
    def _get_notes(self) -> List[str]:
        """获取笔记ID列表"""
        notes = []
        
        if self.args.recent:
            # 获取最近发布的笔记
            logger.info(f"获取最近 {self.args.recent} 篇笔记...")
            notes = self._fetch_recent_notes(self.args.recent)
            
        elif self.args.file:
            # 从文件读取
            if os.path.exists(self.args.file):
                with open(self.args.file, 'r', encoding='utf-8') as f:
                    notes = [line.strip() for line in f if line.strip()]
                logger.info(f"从文件读取 {len(notes)} 篇笔记")
            else:
                logger.error(f"文件不存在: {self.args.file}")
                
        elif self.args.note_ids:
            # 从命令行参数
            notes = [id.strip() for id in self.args.note_ids.split(',')]
            
        return notes
    
    def _fetch_recent_notes(self, count: int) -> List[str]:
        """获取最近发布的笔记"""
        # TODO: 实现实际获取逻辑
        # 这里返回示例数据
        logger.info("注意：当前使用示例数据，请实现实际获取逻辑")
        return [f"note_{i}" for i in range(1, count + 1)]
    
    def _distribute_single(self, note_id: str) -> bool:
        """分发单篇笔记"""
        import subprocess
        
        cmd = [
            sys.executable,
            "scripts/distribute.py",
            "--note-id", note_id
        ]
        
        if self.args.targets:
            cmd.extend(["--targets", self.args.targets])
        
        if self.args.debug:
            cmd.append("--debug")
        
        if self.args.use_app:
            cmd.append("--use-app")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info(f"✅ 笔记 {note_id} 分发成功")
                return True
            else:
                logger.error(f"❌ 笔记 {note_id} 分发失败")
                if result.stderr:
                    logger.error(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"⏱️ 笔记 {note_id} 处理超时")
            return False
        except Exception as e:
            logger.error(f"❌ 笔记 {note_id} 处理异常: {e}")
            return False
    
    def _print_summary(self):
        """打印汇总信息"""
        logger.info("\n" + "=" * 60)
        logger.info("批量分发完成")
        logger.info("=" * 60)
        logger.info(f"总计处理: {self.processed_count}")
        logger.info(f"成功: {self.success_count}")
        logger.info(f"失败: {self.failed_count}")
        
        if self.processed_count > 0:
            success_rate = (self.success_count / self.processed_count) * 100
            logger.info(f"成功率: {success_rate:.1f}%")


def main():
    parser = argparse.ArgumentParser(description='批量内容分发')
    
    # 笔记来源
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument('--recent', type=int,
                             help='同步最近 N 篇笔记')
    source_group.add_argument('--file',
                             help='从文件读取笔记ID列表')
    source_group.add_argument('--note-ids',
                             help='指定笔记ID，逗号分隔')
    
    # 目标平台
    parser.add_argument('--targets',
                       help='目标平台，逗号分隔')
    
    # 运行选项
    parser.add_argument('--interval', type=int, default=60,
                       help='笔记间处理间隔（秒，默认 60）')
    parser.add_argument('--use-app', action='store_true',
                       help='使用桌面端 App')
    parser.add_argument('--debug', action='store_true',
                       help='调试模式')
    
    args = parser.parse_args()
    
    distributor = BatchDistributor(args)
    distributor.run()


if __name__ == '__main__':
    main()
