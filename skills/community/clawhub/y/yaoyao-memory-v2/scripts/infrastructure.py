#!/usr/bin/env python3
"""
基础设施模块 - v1.0.0 (参考鸽子王架构 L6)
资产管理、运维工具、备份、监控
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


class AssetManager:
    """资产管理器"""
    
    def __init__(self, asset_file: Path = None):
        self.asset_file = asset_file or Path.home() / '.openclaw/workspace/memory/.assets.json'
        self._load_assets()
    
    def _load_assets(self):
        """加载资产"""
        if self.asset_file.exists():
            try:
                with open(self.asset_file) as f:
                    self.assets = json.load(f)
            except:
                self.assets = {'configs': {}, 'devices': {}, 'credentials': {}}
        else:
            self.assets = {'configs': {}, 'devices': {}, 'credentials': {}}
    
    def _save_assets(self):
        """保存资产"""
        with open(self.asset_file, 'w') as f:
            json.dump(self.assets, f, indent=2)
    
    def register_config(self, name: str, value: any, metadata: Dict = None):
        """注册配置资产"""
        self.assets['configs'][name] = {
            'value': value,
            'metadata': metadata or {},
            'updated_at': datetime.now().isoformat()
        }
        self._save_assets()
    
    def get_config(self, name: str) -> Optional[Dict]:
        """获取配置"""
        return self.assets['configs'].get(name)
    
    def list_configs(self) -> List[str]:
        """列出所有配置"""
        return list(self.assets['configs'].keys())


class MonitoringMetrics:
    """监控指标收集器"""
    
    # 指标采集间隔 (秒)
    COLLECTION_INTERVAL = 300  # 5分钟
    
    def __init__(self, metrics_file: Path = None):
        self.metrics_file = metrics_file or Path.home() / '.openclaw/workspace/memory/.metrics.json'
        self.last_collection = 0
        self.metrics = {
            'performance': {},
            'usage': {},
            'health': {}
        }
        self._load_metrics()
    
    def _load_metrics(self):
        """加载历史指标"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file) as f:
                    self.metrics = json.load(f)
            except:
                pass
    
    def _save_metrics(self):
        """保存指标"""
        if len(self.metrics.get('history', [])) > 1000:
            self.metrics['history'] = self.metrics['history'][-1000:]
        
        with open(self.metrics_file, 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def should_collect(self) -> bool:
        """判断是否应该采集"""
        return time.time() - self.last_collection > self.COLLECTION_INTERVAL
    
    def collect(self) -> Dict:
        """采集当前指标"""
        self.last_collection = time.time()
        
        # 系统指标
        if HAS_PSUTIL:
            try:
                cpu_percent = psutil.cpu_percent(interval=0.1)
                memory = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                
                system_metrics = {
                    'timestamp': datetime.now().isoformat(),
                    'cpu_percent': cpu_percent,
                    'memory_used_mb': memory.used // (1024 * 1024),
                    'memory_percent': memory.percent,
                    'disk_used_gb': disk.used // (1024 * 1024 * 1024),
                    'disk_percent': disk.percent,
                }
            except:
                system_metrics = {'error': 'Failed to collect system metrics', 'psutil_available': True}
        else:
            system_metrics = {'error': 'psutil not installed', 'psutil_available': False}
        
        # 应用指标
        app_metrics = self._collect_app_metrics()
        
        # 合并指标
        snapshot = {
            'timestamp': datetime.now().isoformat(),
            'system': system_metrics,
            'app': app_metrics
        }
        
        # 保存历史
        if 'history' not in self.metrics:
            self.metrics['history'] = []
        self.metrics['history'].append(snapshot)
        
        # 更新当前值
        self.metrics['latest'] = snapshot
        self._save_metrics()
        
        return snapshot
    
    def _collect_app_metrics(self) -> Dict:
        """采集应用指标"""
        from memory import Memory
        
        try:
            m = Memory()
            stats = m.stats()
            
            return {
                'memory_count': stats.get('total', 0),
                'file_count': stats.get('file_count', 0),
            }
        except:
            return {'error': 'Failed to collect app metrics'}
    
    def get_latest(self) -> Optional[Dict]:
        """获取最新指标"""
        return self.metrics.get('latest')
    
    def get_history(self, hours: int = 24) -> List[Dict]:
        """获取历史指标"""
        cutoff = datetime.now() - timedelta(hours=hours)
        history = self.metrics.get('history', [])
        
        return [
            m for m in history
            if datetime.fromisoformat(m['timestamp'].replace('Z', '+00:00')) > cutoff
        ]


class BackupManager:
    """备份管理器"""
    
    def __init__(self, backup_dir: Path = None):
        self.backup_dir = backup_dir or Path.home() / '.openclaw/workspace/memory/backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_file = self.backup_dir / 'manifest.json'
        self._load_manifest()
    
    def _load_manifest(self):
        """加载备份清单"""
        if self.manifest_file.exists():
            try:
                with open(self.manifest_file) as f:
                    self.manifest = json.load(f)
            except:
                self.manifest = {'backups': []}
        else:
            self.manifest = {'backups': []}
    
    def _save_manifest(self):
        """保存备份清单"""
        with open(self.manifest_file, 'w') as f:
            json.dump(self.manifest, f, indent=2)
    
    def create_backup(self, name: str, data: Dict) -> Dict:
        """创建备份"""
        backup_id = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_file = self.backup_dir / f'{backup_id}.json'
        
        # 保存备份数据
        with open(backup_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # 更新清单
        entry = {
            'id': backup_id,
            'name': name,
            'file': str(backup_file),
            'created_at': datetime.now().isoformat(),
            'size_bytes': backup_file.stat().st_size
        }
        self.manifest['backups'].append(entry)
        self._save_manifest()
        
        return entry
    
    def list_backups(self) -> List[Dict]:
        """列出所有备份"""
        return self.manifest.get('backups', [])
    
    def restore_backup(self, backup_id: str) -> Optional[Dict]:
        """恢复备份"""
        for entry in self.manifest.get('backups', []):
            if entry['id'] == backup_id:
                backup_file = Path(entry['file'])
                if backup_file.exists():
                    with open(backup_file) as f:
                        return json.load(f)
        return None


class Infrastructure:
    """基础设施主类"""
    
    def __init__(self):
        self.assets = AssetManager()
        self.monitoring = MonitoringMetrics()
        self.backup = BackupManager()
    
    def collect_metrics(self) -> Dict:
        """采集指标"""
        return self.monitoring.collect()
    
    def get_health_report(self) -> Dict:
        """获取健康报告"""
        latest = self.monitoring.get_latest()
        
        # 判断健康状态
        if latest and 'system' in latest:
            sys = latest['system']
            healthy = (
                sys.get('cpu_percent', 100) < 90 and
                sys.get('memory_percent', 100) < 90 and
                sys.get('disk_percent', 100) < 90
            )
        else:
            healthy = False
        
        return {
            'healthy': healthy,
            'timestamp': latest.get('timestamp') if latest else None,
            'metrics': latest
        }
    
    def get_stats(self) -> Dict:
        """获取基础设施统计"""
        return {
            'assets': {
                'config_count': len(self.assets.list_configs()),
            },
            'monitoring': {
                'has_latest': self.monitoring.get_latest() is not None,
                'history_count': len(self.monitoring.get_history(hours=1)),
            },
            'backup': {
                'count': len(self.backup.list_backups()),
            }
        }


if __name__ == '__main__':
    infra = Infrastructure()
    
    print('=== 基础设施模块测试 ===\n')
    
    # 测试资产管理
    infra.assets.register_config('test_config', {'key': 'value'}, {'source': 'test'})
    print(f'配置: {infra.assets.get_config("test_config")}')
    
    # 测试指标采集
    if infra.monitoring.should_collect():
        metrics = infra.collect_metrics()
        print(f'指标采集成功: {metrics.get("timestamp")}')
    
    # 测试健康报告
    health = infra.get_health_report()
    print(f'健康报告: {health}')
    
    # 获取统计
    print(f'\n统计: {infra.get_stats()}')
