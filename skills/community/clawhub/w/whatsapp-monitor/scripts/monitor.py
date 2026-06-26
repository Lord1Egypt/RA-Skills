#!/usr/bin/env python3
"""
WhatsApp Monitor - 主监控脚本
实时监测 WhatsApp 消息，过滤关键词，批量导出到飞书多维表格
"""

import json
import re
import time
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from scripts.config_manager import ConfigManager
from scripts.whatsapp_client import WhatsAppClient
from scripts.feishu_client import FeishuClient
from scripts.message_processor import MessageProcessor


class WhatsAppMonitor:
    """WhatsApp 消息监控器"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.config_manager = ConfigManager(config_dir)
        self.message_processor = MessageProcessor()
        self.feishu_client = None
        self.whatsapp_client = None
        
        # 设置日志
        self.setup_logging()
        self.logger = logging.getLogger(__name__)
        
    def setup_logging(self):
        """设置日志配置"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "whatsapp-monitor.log", encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    async def initialize(self):
        """初始化组件"""
        self.logger.info("初始化 WhatsApp 监控器...")
        
        # 加载配置
        self.config_manager.load_configs()
        
        # 初始化飞书客户端
        feishu_config = self.config_manager.get_feishu_config()
        if feishu_config:
            self.feishu_client = FeishuClient(feishu_config)
            await self.feishu_client.initialize()
        else:
            self.logger.error("飞书配置未找到或无效")
            return False
        
        # 初始化 WhatsApp 客户端
        whatsapp_config = self.config_manager.get_whatsapp_config()
        if whatsapp_config:
            self.whatsapp_client = WhatsAppClient(whatsapp_config)
            await self.whatsapp_client.initialize()
        else:
            self.logger.error("WhatsApp 配置未找到或无效")
            return False
        
        self.logger.info("初始化完成")
        return True
    
    async def start_monitoring(self):
        """开始监控"""
        if not await self.initialize():
            self.logger.error("初始化失败，无法启动监控")
            return
        
        self.logger.info("开始 WhatsApp 消息监控...")
        
        try:
            while True:
                # 获取新消息
                new_messages = await self.whatsapp_client.fetch_messages()
                
                if new_messages:
                    # 处理消息
                    processed_messages = []
                    for msg in new_messages:
                        matched = self.message_processor.process_message(msg)
                        if matched:
                            processed_messages.append(matched)
                            self.logger.info(f"匹配到关键词消息: {msg.get('sender')} - {msg.get('content')[:50]}...")
                    
                    # 保存匹配的消息
                    if processed_messages:
                        self.config_manager.save_matched_messages(processed_messages)
                        
                        # 检查是否达到批量阈值
                        batch_threshold = self.config_manager.get_batch_threshold()
                        stored_messages = self.config_manager.get_stored_messages()
                        
                        if len(stored_messages) >= batch_threshold:
                            await self.export_to_feishu(stored_messages)
                
                # 按配置间隔等待
                scan_interval = self.config_manager.get_scan_interval()
                self.logger.debug(f"等待 {scan_interval} 秒后再次扫描...")
                await asyncio.sleep(scan_interval)
                
        except KeyboardInterrupt:
            self.logger.info("监控被用户中断")
        except Exception as e:
            self.logger.error(f"监控过程中出现错误: {str(e)}", exc_info=True)
        finally:
            await self.cleanup()
    
    async def export_to_feishu(self, messages: List[Dict[str, Any]]):
        """导出消息到飞书多维表格"""
        if not self.feishu_client:
            self.logger.error("飞书客户端未初始化")
            return
        
        self.logger.info(f"开始导出 {len(messages)} 条消息到飞书...")
        
        try:
            # 格式化消息数据
            formatted_data = self.format_messages_for_feishu(messages)
            
            # 导出到飞书
            success = await self.feishu_client.batch_add_records(formatted_data)
            
            if success:
                self.logger.info(f"成功导出 {len(messages)} 条消息到飞书")
                # 清空已导出的消息
                self.config_manager.clear_stored_messages()
            else:
                self.logger.error("导出到飞书失败")
                
        except Exception as e:
            self.logger.error(f"导出过程中出现错误: {str(e)}", exc_info=True)
    
    def format_messages_for_feishu(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """格式化消息数据为飞书表格格式"""
        formatted = []
        
        for msg in messages:
            # 根据飞书表格字段结构格式化
            formatted_msg = {
                "timestamp": msg.get("timestamp"),
                "source": msg.get("source"),
                "sender": msg.get("sender"),
                "message_content": msg.get("content"),
                "keyword_matched": ", ".join(msg.get("matched_keywords", [])),
                "priority": msg.get("priority", "medium"),
                "message_type": msg.get("type", "text"),
                "attachment": msg.get("attachment", ""),
                "chat_link": msg.get("chat_link", "")
            }
            formatted.append(formatted_msg)
        
        return formatted
    
    async def cleanup(self):
        """清理资源"""
        self.logger.info("清理资源...")
        if self.whatsapp_client:
            await self.whatsapp_client.cleanup()
        if self.feishu_client:
            await self.feishu_client.cleanup()
    
    def get_status(self) -> Dict[str, Any]:
        """获取监控状态"""
        status = {
            "initialized": bool(self.whatsapp_client and self.feishu_client),
            "config_loaded": self.config_manager.configs_loaded(),
            "stored_messages": len(self.config_manager.get_stored_messages()),
            "batch_threshold": self.config_manager.get_batch_threshold(),
            "scan_interval": self.config_manager.get_scan_interval(),
            "targets": self.config_manager.get_targets_count(),
            "keywords": self.config_manager.get_keywords_count(),
            "last_export": self.config_manager.get_last_export_time()
        }
        return status


async def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WhatsApp 消息监控器")
    parser.add_argument("--start", action="store_true", help="启动监控")
    parser.add_argument("--export", action="store_true", help="强制导出存储的消息")
    parser.add_argument("--status", action="store_true", help="查看监控状态")
    parser.add_argument("--test-config", action="store_true", help="测试配置")
    parser.add_argument("--config-dir", default="config", help="配置目录路径")
    
    args = parser.parse_args()
    
    monitor = WhatsAppMonitor(args.config_dir)
    
    if args.status:
        # 查看状态
        monitor.config_manager.load_configs()
        status = monitor.get_status()
        print(json.dumps(status, indent=2, ensure_ascii=False))
        
    elif args.test_config:
        # 测试配置
        print("测试配置文件...")
        if monitor.config_manager.load_configs():
            print("✓ 配置文件加载成功")
            print(f"  监控目标数量: {monitor.config_manager.get_targets_count()}")
            print(f"  关键词总数: {monitor.config_manager.get_keywords_count()}")
            print(f"  批量阈值: {monitor.config_manager.get_batch_threshold()}")
            print(f"  扫描间隔: {monitor.config_manager.get_scan_interval()}秒")
        else:
            print("✗ 配置文件加载失败")
            
    elif args.export:
        # 强制导出
        monitor.config_manager.load_configs()
        stored_messages = monitor.config_manager.get_stored_messages()
        
        if not stored_messages:
            print("没有存储的消息可导出")
            return
            
        if await monitor.initialize():
            await monitor.export_to_feishu(stored_messages)
        else:
            print("初始化失败")
            
    elif args.start:
        # 启动监控
        await monitor.start_monitoring()
        
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())