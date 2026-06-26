"""
Data Sync - 数据同步模块
使用现有的 whoop-health-analysis 脚本获取数据
"""

import os
import sys
import json
import subprocess
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 路径设置 - 使用环境变量
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # lib/ -> whoop-guru/
WORKSPACE_DIR = os.environ.get("OPENCLAW_WORKSPACE", os.path.dirname(os.path.dirname(SKILL_DIR)))  # whoop-guru/ -> skill/ -> workspace
DATA_DIR = os.environ.get("WHOOP_SKILL_DIR", os.path.join(os.path.dirname(os.path.dirname(SKILL_DIR)), "skills", "whoop-health-analysis"))
PROCESSED_DIR = os.environ.get("WHOOP_DATA_DIR", os.path.join(WORKSPACE_DIR, "data", "processed"))
EXISTING_SCRIPT = os.path.join(DATA_DIR, "scripts", "whoop_data.py")


class WhoopDataIntegrator:
    """整合现有WHOOP数据系统"""
    
    def __init__(self):
        self.data_dir = DATA_DIR
        self.processed_dir = PROCESSED_DIR
        os.makedirs(self.data_dir, exist_ok=True)
    
    def fetch_from_existing(self, data_type: str, days: int = 7) -> List[Dict]:
        """
        使用现有脚本获取数据
        
        Args:
            data_type: recovery/sleep/cycles/workouts
            days: 天数
        
        Returns:
            数据列表
        """
        try:
            result = subprocess.run(
                ["python3", EXISTING_SCRIPT, data_type, "--days", str(days)],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return data.get("records", [])
            else:
                logger.error(f"Failed to fetch {data_type}: {result.stderr}")
                return []
        except Exception as e:
            logger.error(f"Error fetching {data_type}: {e}")
            return []
    
    def get_latest_from_processed(self) -> Dict:
        """从已处理的数据获取最新数据"""
        latest_file = os.path.join(self.processed_dir, "latest.json")
        if os.path.exists(latest_file):
            try:
                with open(latest_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading latest.json: {e}")
        return {}
    
    def sync_recovery(self, days: int = 7) -> List[Dict]:
        """同步恢复数据"""
        return self.fetch_from_existing("recovery", days)
    
    def sync_sleep(self, days: int = 7) -> List[Dict]:
        """同步睡眠数据"""
        return self.fetch_from_existing("sleep", days)
    
    def sync_cycles(self, days: int = 7) -> List[Dict]:
        """同步周期数据"""
        return self.fetch_from_existing("cycles", days)
    
    def sync_all(self, days: int = 30) -> Dict:
        """同步所有数据"""
        result = {
            "timestamp": datetime.now().isoformat(),
            "recovery": [],
            "sleep": [],
            "cycles": [],
            "success": True,
            "errors": []
        }
        
        # 恢复数据
        try:
            result["recovery"] = self.sync_recovery(days)
        except Exception as e:
            result["errors"].append(f"Recovery: {e}")
        
        # 睡眠数据
        try:
            result["sleep"] = self.sync_sleep(days)
        except Exception as e:
            result["errors"].append(f"Sleep: {e}")
        
        # 周期数据
        try:
            result["cycles"] = self.sync_cycles(days)
        except Exception as e:
            result["errors"].append(f"Cycles: {e}")
        
        result["success"] = len(result["errors"]) == 0
        return result


class DataRetention:
    """数据保留管理"""
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or os.path.join(
            os.path.dirname(SKILL_DIR), "..", "workspace-healthgao", "data", "processed"
        )
        self.retention_days = 90
    
    def cleanup_old_files(self):
        """清理过期文件"""
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        cleaned = 0
        
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                if not file.endswith('.json'):
                    continue
                filepath = os.path.join(root, file)
                try:
                    mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
                    if mtime < cutoff:
                        os.remove(filepath)
                        cleaned += 1
                except Exception:
                    pass
        
        logger.info(f"Cleanup: {cleaned} files removed")
        return cleaned
    
    def get_storage_stats(self) -> Dict:
        """获取存储统计"""
        stats = {"total_files": 0, "total_size_mb": 0}
        for root, dirs, files in os.walk(self.data_dir):
            for file in files:
                if file.endswith('.json'):
                    filepath = os.path.join(root, file)
                    stats["total_files"] += 1
                    stats["total_size_mb"] += os.path.getsize(filepath) / (1024 * 1024)
        stats["total_size_mb"] = round(stats["total_size_mb"], 2)
        return stats


def run_sync():
    """运行同步任务"""
    logger.info("Starting WHOOP data sync...")
    integrator = WhoopDataIntegrator()
    result = integrator.sync_all(days=7)
    
    # 清理过期文件
    retention = DataRetention()
    retention.cleanup_old_files()
    
    logger.info(f"Sync complete: {result.get('success')}")
    return result


if __name__ == "__main__":
    result = run_sync()
    print(json.dumps(result, indent=2))
