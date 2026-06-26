#!/usr/bin/env python3
"""
钱包安全卫士 - 钱包地址安全检测与防护
"""

import logging
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    SAFE = "SAFE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class SecurityCheck:
    """安全检查项"""
    name: str
    passed: bool
    risk_level: RiskLevel
    details: str
    recommendation: str

class WalletGuardian:
    """钱包安全卫士"""
    
    def __init__(self):
        self.blacklist = set([
            "0x0000000000000000000000000000000000000000",  # 零地址
            "0xdead00000000000000000000000000000000dead",  # 销毁地址
        ])
        self.known_scams = set()
        self.checks: List[SecurityCheck] = []
    
    def check_address_format(self, address: str) -> SecurityCheck:
        """检查地址格式"""
        # 检查格式
        is_valid = (
            len(address) == 42 and
            address.startswith('0x') and
            all(c in '0123456789abcdefABCDEF' for c in address[2:])
        )
        
        return SecurityCheck(
            name="地址格式验证",
            passed=is_valid,
            risk_level=RiskLevel.SAFE if is_valid else RiskLevel.CRITICAL,
            details="地址格式正确" if is_valid else "地址格式无效",
            recommendation="使用正确的以太坊地址格式" if not is_valid else "无"
        )
    
    def check_blacklist(self, address: str) -> SecurityCheck:
        """检查黑名单"""
        is_blacklisted = address.lower() in (a.lower() for a in self.blacklist)
        
        return SecurityCheck(
            name="黑名单检查",
            passed=not is_blacklisted,
            risk_level=RiskLevel.CRITICAL if is_blacklisted else RiskLevel.SAFE,
            details="地址在黑名单中" if is_blacklisted else "地址不在黑名单中",
            recommendation="立即停止与该地址的任何交互" if is_blacklisted else "无"
        )
    
    def check_contract_verification(self, address: str) -> SecurityCheck:
        """检查合约验证（模拟）"""
        # 模拟：70%的地址有验证合约
        is_verified = random.random() < 0.7
        
        return SecurityCheck(
            name="合约验证状态",
            passed=is_verified,
            risk_level=RiskLevel.LOW if is_verified else RiskLevel.MEDIUM,
            details="合约已开源验证" if is_verified else "合约未开源验证",
            recommendation="谨慎与未验证合约交互" if not is_verified else "无"
        )
    
    def check_scam_reports(self, address: str) -> SecurityCheck:
        """检查诈骗报告（模拟）"""
        # 模拟：10%的地址有诈骗报告
        has_reports = random.random() < 0.1
        
        return SecurityCheck(
            name="诈骗举报检查",
            passed=not has_reports,
            risk_level=RiskLevel.HIGH if has_reports else RiskLevel.SAFE,
            details=f"发现 {random.randint(1, 10)} 条诈骗举报" if has_reports else "未发现诈骗举报",
            recommendation="避免与该地址交互" if has_reports else "无"
        )
    
    def check_taint_analysis(self, address: str) -> SecurityCheck:
        """污点分析（模拟）"""
        # 模拟：检查是否与恶意地址有关联
        is_tainted = random.random() < 0.05
        
        return SecurityCheck(
            name="关联风险分析",
            passed=not is_tainted,
            risk_level=RiskLevel.HIGH if is_tainted else RiskLevel.SAFE,
            details="发现与恶意地址的关联" if is_tainted else "未发现可疑关联",
            recommendation="进一步调查资金来源" if is_tainted else "无"
        )
    
    def check_approvals(self, address: str) -> SecurityCheck:
        """检查授权情况（模拟）"""
        # 模拟授权风险
        unlimited_approvals = random.randint(0, 3)
        
        return SecurityCheck(
            name="Token授权检查",
            passed=unlimited_approvals == 0,
            risk_level=RiskLevel.MEDIUM if unlimited_approvals > 0 else RiskLevel.SAFE,
            details=f"发现 {unlimited_approvals} 个无限授权",
            recommendation="定期清理不必要的授权" if unlimited_approvals > 0 else "无"
        )
    
    def check_balance_diversity(self, address: str) -> SecurityCheck:
        """检查资产分散度（模拟）"""
        # 模拟资产分布
        token_count = random.randint(1, 20)
        
        return SecurityCheck(
            name="资产分散度",
            passed=token_count >= 3,
            risk_level=RiskLevel.LOW if token_count >= 3 else RiskLevel.MEDIUM,
            details=f"持有 {token_count} 种不同Token",
            recommendation="考虑分散投资降低风险" if token_count < 3 else "无"
        )
    
    def calculate_security_score(self, checks: List[SecurityCheck]) -> int:
        """计算安全评分"""
        score = 100
        
        for check in checks:
            if not check.passed:
                if check.risk_level == RiskLevel.CRITICAL:
                    score -= 30
                elif check.risk_level == RiskLevel.HIGH:
                    score -= 20
                elif check.risk_level == RiskLevel.MEDIUM:
                    score -= 10
                elif check.risk_level == RiskLevel.LOW:
                    score -= 5
        
        return max(0, score)
    
    def scan(self, address: str, full_scan: bool = False) -> Dict:
        """执行扫描"""
        logger.info(f"🔍 开始扫描钱包: {address}")
        
        checks = []
        
        # 基础检查
        checks.append(self.check_address_format(address))
        checks.append(self.check_blacklist(address))
        
        if full_scan:
            checks.append(self.check_contract_verification(address))
            checks.append(self.check_scam_reports(address))
            checks.append(self.check_taint_analysis(address))
            checks.append(self.check_approvals(address))
            checks.append(self.check_balance_diversity(address))
        
        self.checks = checks
        
        # 计算评分
        score = self.calculate_security_score(checks)
        
        # 确定总体风险等级
        risk_levels = [c.risk_level for c in checks if not c.passed]
        
        if RiskLevel.CRITICAL in risk_levels:
            overall_risk = RiskLevel.CRITICAL
        elif RiskLevel.HIGH in risk_levels:
            overall_risk = RiskLevel.HIGH
        elif RiskLevel.MEDIUM in risk_levels:
            overall_risk = RiskLevel.MEDIUM
        elif RiskLevel.LOW in risk_levels:
            overall_risk = RiskLevel.LOW
        else:
            overall_risk = RiskLevel.SAFE
        
        return {
            'address': address,
            'scan_date': '2024-01-01',
            'security_score': score,
            'overall_risk': overall_risk.value,
            'checks': [
                {
                    'name': c.name,
                    'passed': c.passed,
                    'risk_level': c.risk_level.value,
                    'details': c.details,
                    'recommendation': c.recommendation
                }
                for c in checks
            ]
        }
    
    def print_report(self, report: Dict):
        """打印报告"""
        print(f"\n{'='*80}")
        print(f"🛡️ 钱包安全扫描报告")
        print(f"{'='*80}")
        
        print(f"\n📋 钱包地址: {report['address']}")
        print(f"扫描时间: {report['scan_date']}")
        
        # 安全评分
        score = report['security_score']
        score_color = '🟢' if score >= 80 else '🟡' if score >= 60 else '🔴'
        print(f"\n🔐 安全评分: {score_color} {score}/100")
        
        # 风险等级
        risk_emoji = {
            'SAFE': '🟢',
            'LOW': '🔵',
            'MEDIUM': '🟡',
            'HIGH': '🟠',
            'CRITICAL': '🔴'
        }.get(report['overall_risk'], '⚪')
        print(f"⚠️ 风险等级: {risk_emoji} {report['overall_risk']}")
        
        # 详细检查
        print(f"\n🔍 详细检查:")
        for check in report['checks']:
            status = '✅' if check['passed'] else '❌'
            risk_emoji = {
                'SAFE': '🟢',
                'LOW': '🔵',
                'MEDIUM': '🟡',
                'HIGH': '🟠',
                'CRITICAL': '🔴'
            }.get(check['risk_level'], '⚪')
            print(f"\n   {status} {check['name']}")
            print(f"      风险: {risk_emoji} {check['risk_level']}")
            print(f"      详情: {check['details']}")
            if check['recommendation'] != "无":
                print(f"      建议: {check['recommendation']}")
        
        # 总结建议
        failed_checks = [c for c in report['checks'] if not c['passed']]
        if failed_checks:
            print(f"\n💡 优先处理建议:")
            for check in failed_checks[:3]:
                print(f"   • {check['name']}: {check['recommendation']}")
        else:
            print(f"\n✅ 所有检查通过，钱包状态良好")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("🛡️ 钱包安全卫士 - 演示")
    print("="*80)
    
    guardian = WalletGuardian()
    
    # 扫描钱包
    address = "0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe"
    print(f"\n🔍 扫描地址: {address}")
    
    report = guardian.scan(address, full_scan=True)
    guardian.print_report(report)
    
    # 保存报告
    with open('wallet_security_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print("📄 报告已保存到 wallet_security_report.json")
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        address = sys.argv[1]
        full = '--full' in sys.argv
        guardian = WalletGuardian()
        report = guardian.scan(address, full_scan=full)
        guardian.print_report(report)
    else:
        demo()
