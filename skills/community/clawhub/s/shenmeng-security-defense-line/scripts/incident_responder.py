#!/usr/bin/env python3
"""
安全事件响应器 - 安全事件应急处理与恢复
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IncidentSeverity(Enum):
    P0_CRITICAL = "P0-CRITICAL"
    P1_HIGH = "P1-HIGH"
    P2_MEDIUM = "P2-MEDIUM"
    P3_LOW = "P3-LOW"

class IncidentStatus(Enum):
    DETECTED = "DETECTED"
    CONTAINED = "CONTAINED"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

@dataclass
class SecurityIncident:
    """安全事件"""
    id: str
    timestamp: datetime
    severity: IncidentSeverity
    status: IncidentStatus
    title: str
    description: str
    affected_assets: List[str]
    indicators: List[str]
    response_actions: List[str]
    lessons_learned: List[str]

class IncidentResponder:
    """事件响应器"""
    
    def __init__(self):
        self.incidents: List[SecurityIncident] = []
        self.response_playbooks = {
            'private_key_leak': {
                'name': '私钥泄露响应',
                'immediate_actions': [
                    '立即将资产转移到安全钱包',
                    '撤销所有授权',
                    '通知交易所冻结相关账户'
                ],
                'investigation_steps': [
                    '确定泄露范围',
                    '检查所有关联地址',
                    '分析泄露原因'
                ]
            },
            'suspicious_transaction': {
                'name': '可疑交易响应',
                'immediate_actions': [
                    '暂停所有交易',
                    '检查授权情况',
                    '验证签名者身份'
                ],
                'investigation_steps': [
                    '分析交易详情',
                    '检查合约安全性',
                    '确认是否有权限被滥用'
                ]
            },
            'phishing_attack': {
                'name': '钓鱼攻击响应',
                'immediate_actions': [
                    '断开可疑网站连接',
                    '撤销可疑授权',
                    '检查资产是否被转移'
                ],
                'investigation_steps': [
                    '记录攻击证据',
                    '分析钓鱼手法',
                    '通知社区警告他人'
                ]
            }
        }
    
    def detect_incident(self, detection_data: Dict) -> Optional[SecurityIncident]:
        """检测安全事件"""
        # 模拟检测逻辑
        indicators = []
        severity = None
        title = ""
        
        # 检查大额异常转出
        if detection_data.get('large_transfer'):
            indicators.append(f"大额转出: {detection_data['amount']} ETH")
            severity = IncidentSeverity.P0_CRITICAL
            title = "大额异常资产转出"
        
        # 检查可疑授权
        if detection_data.get('suspicious_approval'):
            indicators.append("可疑的无限授权")
            severity = severity or IncidentSeverity.P1_HIGH
            title = title or "可疑授权操作"
        
        # 检查新设备登录
        if detection_data.get('new_device'):
            indicators.append("新设备访问")
            severity = severity or IncidentSeverity.P2_MEDIUM
            title = title or "新设备登录"
        
        if not indicators:
            return None
        
        incident = SecurityIncident(
            id=f"INC-{len(self.incidents)+1:04d}",
            timestamp=datetime.now(),
            severity=severity,
            status=IncidentStatus.DETECTED,
            title=title,
            description="检测到潜在安全威胁",
            affected_assets=detection_data.get('affected_assets', []),
            indicators=indicators,
            response_actions=[],
            lessons_learned=[]
        )
        
        self.incidents.append(incident)
        
        logger.warning(f"🚨 安全事件 detected: {title}")
        logger.warning(f"   严重度: {severity.value}")
        logger.warning(f"   指标: {', '.join(indicators)}")
        
        return incident
    
    def emergency_freeze(self, wallet_address: str) -> Dict:
        """紧急冻结"""
        logger.critical(f"🚨 执行紧急冻结: {wallet_address}")
        
        actions = [
            "撤销所有Token授权",
            "取消待处理交易",
            "通知交易所监控",
            "启用多签紧急模式"
        ]
        
        for action in actions:
            logger.info(f"   ✅ {action}")
        
        return {
            'success': True,
            'wallet': wallet_address,
            'actions_taken': actions,
            'timestamp': datetime.now().isoformat()
        }
    
    def analyze_transaction(self, tx_hash: str) -> Dict:
        """分析交易"""
        logger.info(f"🔍 分析交易: {tx_hash}")
        
        # 模拟分析结果
        analysis = {
            'tx_hash': tx_hash,
            'type': 'Transfer',
            'from': '0xSender...',
            'to': '0xRecipient...',
            'value': '10 ETH',
            'gas_used': 21000,
            'risk_indicators': [
                '目标地址在黑名单中',
                '交易金额超过日常限额'
            ],
            'recommended_actions': [
                '调查目标地址',
                '确认转账意图',
                '考虑撤销交易（如可能）'
            ]
        }
        
        return analysis
    
    def assess_loss(self, wallet_address: str, incident_date: str) -> Dict:
        """损失评估"""
        logger.info(f"💰 评估损失: {wallet_address}")
        
        # 模拟损失评估
        losses = {
            'wallet': wallet_address,
            'incident_date': incident_date,
            'total_loss_usd': 50000,
            'assets': [
                {'token': 'ETH', 'amount': 10, 'value_usd': 20000},
                {'token': 'USDC', 'amount': 30000, 'value_usd': 30000}
            ],
            'recoverable': False,
            'insurance_eligible': True
        }
        
        return losses
    
    def generate_incident_report(self, incident_id: str) -> Dict:
        """生成事件报告"""
        incident = next((i for i in self.incidents if i.id == incident_id), None)
        
        if not incident:
            return {'error': '事件不存在'}
        
        report = {
            'incident_id': incident.id,
            'title': incident.title,
            'severity': incident.severity.value,
            'status': incident.status.value,
            'timeline': [
                {'time': incident.timestamp.isoformat(), 'event': '事件检测'},
                {'time': incident.timestamp.isoformat(), 'event': '响应启动'}
            ],
            'affected_assets': incident.affected_assets,
            'indicators': incident.indicators,
            'response_actions': incident.response_actions,
            'lessons_learned': incident.lessons_learned,
            'recommendations': [
                '加强安全意识培训',
                '实施更严格的访问控制',
                '定期进行安全审计'
            ]
        }
        
        return report
    
    def get_playbook(self, incident_type: str) -> Dict:
        """获取响应手册"""
        return self.response_playbooks.get(incident_type, {
            'name': '通用响应手册',
            'immediate_actions': ['确认事件', '启动响应', '通知相关方'],
            'investigation_steps': ['收集证据', '分析原因', '制定修复方案']
        })
    
    def print_incident_summary(self):
        """打印事件摘要"""
        print(f"\n{'='*80}")
        print(f"🚨 安全事件摘要")
        print(f"{'='*80}")
        
        print(f"\n总事件数: {len(self.incidents)}")
        
        # 按严重度统计
        severity_counts = {}
        for inc in self.incidents:
            severity_counts[inc.severity.value] = severity_counts.get(inc.severity.value, 0) + 1
        
        print(f"\n严重度分布:")
        for sev in ['P0-CRITICAL', 'P1-HIGH', 'P2-MEDIUM', 'P3-LOW']:
            count = severity_counts.get(sev, 0)
            emoji = {'P0-CRITICAL': '🔴', 'P1-HIGH': '🟠', 'P2-MEDIUM': '🟡', 'P3-LOW': '🟢'}.get(sev, '⚪')
            print(f"   {emoji} {sev}: {count}")
        
        # 最近事件
        if self.incidents:
            print(f"\n🆕 最近事件:")
            for inc in sorted(self.incidents, key=lambda x: x.timestamp, reverse=True)[:5]:
                sev_emoji = {
                    IncidentSeverity.P0_CRITICAL: '🔴',
                    IncidentSeverity.P1_HIGH: '🟠',
                    IncidentSeverity.P2_MEDIUM: '🟡',
                    IncidentSeverity.P3_LOW: '🟢'
                }.get(inc.severity, '⚪')
                print(f"   {sev_emoji} [{inc.id}] {inc.title} ({inc.status.value})")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("🚨 安全事件响应器 - 演示")
    print("="*80)
    
    responder = IncidentResponder()
    
    # 模拟检测事件
    print("\n🔍 检测安全事件...")
    incident = responder.detect_incident({
        'large_transfer': True,
        'amount': 100,
        'affected_assets': ['ETH']
    })
    
    if incident:
        print(f"\n检测到事件: {incident.id}")
        
        # 紧急冻结
        print("\n🚫 执行紧急冻结...")
        result = responder.emergency_freeze("0xVictimWallet")
        
        # 分析交易
        print("\n🔍 分析可疑交易...")
        analysis = responder.analyze_transaction("0xSuspiciousTx")
        print(f"发现风险指标: {len(analysis['risk_indicators'])}")
        
        # 损失评估
        print("\n💰 评估损失...")
        losses = responder.assess_loss("0xVictimWallet", "2024-01-01")
        print(f"总损失: ${losses['total_loss_usd']:,}")
        
        # 获取响应手册
        print("\n📖 响应手册:")
        playbook = responder.get_playbook('private_key_leak')
        print(f"手册名称: {playbook['name']}")
        print("立即行动:")
        for action in playbook['immediate_actions'][:3]:
            print(f"   • {action}")
    
    # 打印摘要
    responder.print_incident_summary()
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
