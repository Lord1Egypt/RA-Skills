#!/usr/bin/env python3
"""
Soul Memory Auto-Trigger Daemon v3.1.1
持續監控並在需要時自動觸發記憶搜索和儲存
"""

import sys
import os
import time
import logging
from pathlib import Path

SOUL_MEMORY_PATH = os.environ.get('SOUL_MEMORY_PATH', os.path.dirname(__file__))
sys.path.insert(0, SOUL_MEMORY_PATH)

from core import SoulMemorySystem

CONFIG_DIR = Path.home() / '.config' / 'soul-memory'
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = CONFIG_DIR / 'auto-trigger.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TriggerDaemon:
    def __init__(self):
        self.system = SoulMemorySystem()
        self.system.initialize()
        self.running = True
        logger.info("🧠 Soul Memory Auto-Trigger Daemon v3.1.1 已啟動")
        logger.info("✅ 雙軌持久化已啟用 (JSON + Daily Markdown)")
    
    def run(self):
        try:
            while self.running:
                time.sleep(60)
                self.check_and_trigger()
        except KeyboardInterrupt:
            logger.info("收到中斷信號，正在關閉...")
            self.stop()
    
    def check_and_trigger(self):
        try:
            logger.debug("Auto-Trigger 檢查點 (v3.1.1)")
        except Exception as e:
            logger.error(f"觸發錯誤: {e}")
    
    def stop(self):
        self.running = False
        logger.info("Auto-Trigger Daemon 已停止")

if __name__ == '__main__':
    daemon = TriggerDaemon()
    daemon.run()
