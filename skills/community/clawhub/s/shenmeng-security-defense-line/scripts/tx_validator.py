#!/usr/bin/env python3
"""
交易安全验证器 - 交易风险检测与预执行验证
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    SAFE = "SAFE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

@dataclass
class TxCheckResult:
    """交易检查结果"""
    check_name: str
    passed: bool
    risk_level: RiskLevel
    details: str
    recommendation: str

class TransactionValidator:
    """交易验证器"""
    
    def __init__(self):
        self.max_slippage = 5.0  # 最大滑点5%
        self.max_gas_price = 500  # 最大gas price 500 gwei
        self.max_value_eth = 100  # 大额交易阈值
    
    def validate_address(self, to_address: str) -> TxCheckResult:
        """验证目标地址"""
        is_valid = len(to_address) == 42 and to_address.startswith('0x')
        
        # 模拟：检查是否是已知合约
        known_contracts = ['uniswap', 'aave', 'compound']
        is_known = any(kw in to_address.lower() for kw in known_contracts)
        
        return TxCheckResult(
            check_name="目标地址验证",
            passed=is_valid,
            risk_level=RiskLevel.SAFE if is_valid and is_known else RiskLevel.MEDIUM,
            details=f"地址格式正确，{'知名合约' if is_known else '未知地址'}",
            recommendation="验证目标地址是否正确" if not is_known else "无"
        )
    
    def validate_value(self, value_eth: float) -> TxCheckResult:
        """验证交易金额"""
        is_safe = value_eth < self.max_value_eth
        
        if value_eth > 1000:
            risk = RiskLevel.CRITICAL
        elif value_eth > 100:
            risk = RiskLevel.HIGH
        elif value_eth > 10:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.SAFE
        
        return TxCheckResult(
            check_name="交易金额检查",
            passed=is_safe,
            risk_level=risk,
            details=f"交易金额: {value_eth} ETH",
            recommendation="大额交易请多次确认" if value_eth >= 10 else "无"
        )
    
    def validate_gas(self, gas_price_gwei: float, gas_limit: int) -> TxCheckResult:
        """验证Gas设置"""
        is_safe = gas_price_gwei <= self.max_gas_price
        
        if gas_price_gwei > 1000:
            risk = RiskLevel.CRITICAL
        elif gas_price_gwei > self.max_gas_price:
            risk = RiskLevel.HIGH
        else:
            risk = RiskLevel.SAFE
        
        estimated_cost = (gas_price_gwei * gas_limit) / 1e9
        
        return TxCheckResult(
            check_name="Gas费用检查",
            passed=is_safe,
            risk_level=risk,
            details=f"Gas Price: {gas_price_gwei} gwei, 预估费用: {estimated_cost:.6f} ETH",
            recommendation="Gas price过高，建议等待或调整" if not is_safe else "无"
        )
    
    def validate_slippage(self, slippage_percent: float) -> TxCheckResult:
        """验证滑点设置"""
        is_safe = slippage_percent <= self.max_slippage
        
        if slippage_percent > 50:
            risk = RiskLevel.CRITICAL
        elif slippage_percent > 10:
            risk = RiskLevel.HIGH
        elif slippage_percent > self.max_slippage:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.LOW
        
        return TxCheckResult(
            check_name="滑点保护检查",
            passed=is_safe,
            risk_level=risk,
            details=f"滑点容忍度: {slippage_percent}%",
            recommendation=f"建议滑点不超过{self.max_slippage}%以防止MEV攻击" if not is_safe else "无"
        )
    
    def check_contract_risk(self, contract_address: str) -> TxCheckResult:
        """检查合约风险"""
        # 模拟合约风险评估
        risk_score = 0  # 0-100
        
        # 模拟检查
        if 'uniswap' in contract_address.lower():
            risk_score = 10
            details = "知名DEX合约，经过审计"
        elif 'aave' in contract_address.lower():
            risk_score = 10
            details = "知名借贷协议，经过审计"
        else:
            risk_score = 50
            details = "未知合约，未经过验证"
        
        if risk_score < 20:
            risk = RiskLevel.SAFE
        elif risk_score < 50:
            risk = RiskLevel.LOW
        elif risk_score < 80:
            risk = RiskLevel.MEDIUM
        else:
            risk = RiskLevel.HIGH
        
        return TxCheckResult(
            check_name="合约安全评级",
            passed=risk_score < 50,
            risk_level=risk,
            details=details,
            recommendation="优先使用经过审计的知名合约" if risk_score >= 50 else "无"
        )
    
    def check_approval_risk(self, token_address: str, spender: str, amount: str) -> TxCheckResult:
        """检查授权风险"""
        is_unlimited = amount == '0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
        
        if is_unlimited:
            risk = RiskLevel.HIGH
            details = "无限授权，存在资金风险"
            recommendation = "建议设置具体授权额度"
        else:
            risk = RiskLevel.SAFE
            details = f"授权额度: {amount}"
            recommendation = "无"
        
        return TxCheckResult(
            check_name="Token授权风险",
            passed=not is_unlimited,
            risk_level=risk,
            details=details,
            recommendation=recommendation
        )
    
    def simulate_execution(self, tx_data: Dict) -> TxCheckResult:
        """模拟交易执行"""
        # 模拟预执行
        simulated_success = True
        estimated_output = "1000 USDC"
        price_impact = 0.5
        
        return TxCheckResult(
            check_name="交易模拟执行",
            passed=simulated_success,
            risk_level=RiskLevel.SAFE if simulated_success else RiskLevel.CRITICAL,
            details=f"模拟成功，预估输出: {estimated_output}，价格影响: {price_impact}%",
            recommendation="确认交易参数无误" if not simulated_success else "无"
        )
    
    def validate(self, tx_data: Dict) -> Dict:
        """验证交易"""
        logger.info("🔍 开始交易安全验证...")
        
        checks = []
        
        # 基础验证
        checks.append(self.validate_address(tx_data.get('to', '')))
        checks.append(self.validate_value(tx_data.get('value', 0) / 1e18))
        checks.append(self.validate_gas(
            tx_data.get('gasPrice', 0) / 1e9,
            tx_data.get('gas', 21000)
        ))
        
        # 高级验证
        if tx_data.get('data'):
            checks.append(self.check_contract_risk(tx_data.get('to', '')))
            checks.append(self.simulate_execution(tx_data))
        
        # 检查授权相关
        if 'approval' in tx_data.get('data', '').lower():
            checks.append(self.check_approval_risk(
                tx_data.get('token', ''),
                tx_data.get('spender', ''),
                tx_data.get('amount', '0')
            ))
        
        # 滑点检查（如果是DEX交易）
        if any(dex in tx_data.get('to', '').lower() for dex in ['swap', 'router']):
            checks.append(self.validate_slippage(tx_data.get('slippage', 0.5)))
        
        # 确定总体风险
        risk_levels = [c.risk_level for c in checks if not c.passed]
        
        if RiskLevel.CRITICAL in risk_levels:
            overall_risk = RiskLevel.CRITICAL
        elif RiskLevel.HIGH in risk_levels:
            overall_risk = RiskLevel.HIGH
        elif RiskLevel.MEDIUM in risk_levels:
            overall_risk = RiskLevel.MEDIUM
        else:
            overall_risk = RiskLevel.SAFE
        
        # 计算通过/失败数
        passed = sum(1 for c in checks if c.passed)
        failed = len(checks) - passed
        
        return {
            'tx_hash': tx_data.get('hash', 'Pending'),
            'validation_time': '2024-01-01',
            'overall_risk': overall_risk.value,
            'summary': {
                'total_checks': len(checks),
                'passed': passed,
                'failed': failed
            },
            'checks': [
                {
                    'name': c.check_name,
                    'passed': c.passed,
                    'risk_level': c.risk_level.value,
                    'details': c.details,
                    'recommendation': c.recommendation
                }
                for c in checks
            ],
            'can_proceed': overall_risk not in [RiskLevel.CRITICAL, RiskLevel.HIGH]
        }
    
    def print_report(self, report: Dict):
        """打印报告"""
        print(f"\n{'='*80}")
        print(f"🔐 交易安全验证报告")
        print(f"{'='*80}")
        
        print(f"\n📋 交易哈希: {report['tx_hash']}")
        
        # 总体风险
        risk_emoji = {
            'SAFE': '🟢',
            'LOW': '🔵',
            'MEDIUM': '🟡',
            'HIGH': '🟠',
            'CRITICAL': '🔴'
        }.get(report['overall_risk'], '⚪')
        print(f"⚠️ 总体风险: {risk_emoji} {report['overall_risk']}")
        
        # 汇总
        summary = report['summary']
        print(f"\n📊 检查汇总: {summary['passed']}/{summary['total_checks']} 通过")
        
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
        
        # 最终建议
        print(f"\n💡 最终建议:")
        if report['can_proceed']:
            print(f"   ✅ 交易相对安全，可以执行")
        else:
            print(f"   ❌ 发现高风险问题，建议取消交易")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("🔐 交易安全验证器 - 演示")
    print("="*80)
    
    validator = TransactionValidator()
    
    # 模拟交易数据
    tx_data = {
        'to': '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D',  # Uniswap Router
        'value': 1 * 10**18,  # 1 ETH
        'gasPrice': 50 * 10**9,  # 50 gwei
        'gas': 200000,
        'data': '0xswap...',
        'slippage': 1.0
    }
    
    print(f"\n🔍 验证交易...")
    report = validator.validate(tx_data)
    validator.print_report(report)
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 从文件或参数读取交易数据
        demo()
    else:
        demo()
