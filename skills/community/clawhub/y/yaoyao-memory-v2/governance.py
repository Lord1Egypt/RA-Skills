#!/usr/bin/env python3
"""
治理模块 - v1.0.0 (参考鸽子王架构 L5)
安全性、稳定性和治理功能
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class RiskLevel(Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    CRITICAL = 'critical'


class GovernanceStatus(Enum):
    ALLOW = 'allow'
    DENY = 'deny'
    REVIEW = 'review'
    ROLLBACK = 'rollback'


class AuditLogger:
    """审计日志器"""
    
    def __init__(self, log_dir: Path = None):
        self.log_dir = log_dir or Path.home() / '.openclaw/workspace/memory/.audit'
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_log = self.log_dir / f'audit_{datetime.now().strftime("%Y%m%d")}.jsonl'
    
    def log(self, event_type: str, data: Dict):
        """记录审计日志"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data,
            'trace_id': self._generate_trace_id()
        }
        
        with open(self.current_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def _generate_trace_id(self) -> str:
        """生成追踪ID"""
        import uuid
        return str(uuid.uuid4())[:8]
    
    def query(self, event_type: str = None, limit: int = 100) -> List[Dict]:
        """查询审计日志"""
        results = []
        if not self.current_log.exists():
            return results
        
        with open(self.current_log, 'r', encoding='utf-8') as f:
            for line in f:
                if limit > 0 and len(results) >= limit:
                    break
                try:
                    entry = json.loads(line)
                    if event_type is None or entry.get('event_type') == event_type:
                        results.append(entry)
                except:
                    pass
        
        return results


class SecurityChecker:
    """安全检查器"""
    
    # 危险关键词（用于检测而非执行，黑客工具特征库）
    DANGER_KEYWORDS = [
        # 文件删除/破坏
        'rm -rf', 'delete all', 'drop table', 'truncate',
        # 权限提升
        'sudo', 'chmod 777',
        # 代码执行（检测特征，非实际执行）
        'eval(', 'exec(', 'os.system',
    ]
    
    # 敏感操作
    SENSITIVE_OPERATIONS = [
        'delete_memory', 'wipe_data', 'format_disk',
        'modify_acl', 'change_password', 'reset_config',
    ]
    
    def check_content(self, content: str) -> Dict:
        """检查内容安全性"""
        warnings = []
        blocked = False
        
        content_lower = content.lower()
        
        for keyword in self.DANGER_KEYWORDS:
            if keyword.lower() in content_lower:
                warnings.append(f'危险关键词: {keyword}')
                blocked = True
        
        return {
            'blocked': blocked,
            'warnings': warnings,
            'risk_level': 'critical' if blocked else 'low'
        }
    
    def check_operation(self, operation: str, params: Dict = None) -> Dict:
        """检查操作权限"""
        is_sensitive = operation in self.SENSITIVE_OPERATIONS
        
        return {
            'allowed': True,
            'requires_confirmation': is_sensitive,
            'risk_level': 'high' if is_sensitive else 'low'
        }


class FailoverManager:
    """故障转移管理器"""
    
    def __init__(self):
        self.backup_dir = Path.home() / '.openclaw/workspace/memory/backups'
        self.state_file = Path.home() / '.openclaw/workspace/memory/.failover_state.json'
        self._load_state()
    
    def _load_state(self):
        """加载故障状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file) as f:
                    self.state = json.load(f)
            except:
                self.state = {'failover_count': 0, 'last_failover': None}
        else:
            self.state = {'failover_count': 0, 'last_failover': None}
    
    def _save_state(self):
        """保存故障状态"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f)
    
    def check_health(self) -> Dict:
        """检查健康状态"""
        return {
            'healthy': True,
            'failover_count': self.state.get('failover_count', 0),
            'last_failover': self.state.get('last_failover')
        }
    
    def trigger_failover(self, reason: str) -> Dict:
        """触发故障转移"""
        self.state['failover_count'] = self.state.get('failover_count', 0) + 1
        self.state['last_failover'] = datetime.now().isoformat()
        self.state['last_reason'] = reason
        self._save_state()
        
        return {
            'success': True,
            'failover_id': self.state['failover_count'],
            'reason': reason
        }


class RollbackManager:
    """回滚管理器"""
    
    def __init__(self, backup_dir: Path = None):
        self.backup_dir = backup_dir or Path.home() / '.openclaw/workspace/memory/backups'
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.change_log = self.backup_dir / 'change_log.jsonl'
    
    def record_change(self, operation: str, target: str, before: Any, after: Any):
        """记录变更"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation,
            'target': target,
            'before': before,
            'after': after
        }
        
        with open(self.change_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def get_last_change(self, target: str = None) -> Optional[Dict]:
        """获取最近一次变更"""
        if not self.change_log.exists():
            return None
        
        with open(self.change_log, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line in reversed(lines):
            try:
                entry = json.loads(line)
                if target is None or entry.get('target') == target:
                    return entry
            except:
                pass
        
        return None
    
    def can_rollback(self) -> bool:
        """检查是否可以回滚"""
        return self.change_log.exists()


class Governance:
    """治理主类"""
    
    def __init__(self):
        self.audit = AuditLogger()
        self.security = SecurityChecker()
        self.failover = FailoverManager()
        self.rollback = RollbackManager()
    
    def check(self, operation: str, params: Dict = None, content: str = None) -> Dict:
        """执行治理检查"""
        # 1. 安全检查
        if content:
            security_result = self.security.check_content(content)
            if security_result['blocked']:
                self.audit.log('security_blocked', {
                    'operation': operation,
                    'warnings': security_result['warnings']
                })
                return {
                    'status': GovernanceStatus.DENY.value,
                    'reason': '内容安全检查未通过',
                    'risk_level': security_result['risk_level'],
                    'actions': ['audit_logged']
                }
        
        # 2. 操作权限检查
        op_result = self.security.check_operation(operation, params)
        if op_result.get('requires_confirmation') and not params.get('confirmed'):
            self.audit.log('operation_requires_confirmation', {
                'operation': operation,
                'params': params
            })
            return {
                'status': GovernanceStatus.REVIEW.value,
                'reason': '该操作需要确认',
                'risk_level': op_result['risk_level'],
                'actions': ['awaiting_confirmation']
            }
        
        # 3. 审计记录
        self.audit.log('operation_allowed', {
            'operation': operation,
            'params': params
        })
        
        return {
            'status': GovernanceStatus.ALLOW.value,
            'reason': '检查通过',
            'risk_level': 'low',
            'actions': ['audit_logged']
        }
    
    def get_stats(self) -> Dict:
        """获取治理统计"""
        return {
            'audit_entries': len(self.audit.query(limit=1000)),
            'failover_count': self.failover.state.get('failover_count', 0),
            'rollback_available': self.rollback.can_rollback(),
            'health': self.failover.check_health()
        }


if __name__ == '__main__':
    gov = Governance()
    
    print('=== 治理模块测试 ===\n')
    
    # 测试安全检查
    result = gov.security.check_content('这是一条正常内容')
    print(f'安全检查(正常): {result}')
    
    result = gov.security.check_content('执行 rm -rf / 命令')
    print(f'安全检查(危险): {result}')
    
    # 测试治理检查
    result = gov.check('delete_memory', content='正常删除')
    print(f'治理检查: {result}')
    
    # 获取统计
    print(f'\n治理统计: {gov.get_stats()}')
