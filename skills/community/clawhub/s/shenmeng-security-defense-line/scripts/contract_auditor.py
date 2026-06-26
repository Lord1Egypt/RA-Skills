#!/usr/bin/env python3
"""
智能合约审计器 - 自动化合约安全审计
"""

import logging
import re
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Severity(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

@dataclass
class Vulnerability:
    """漏洞"""
    id: str
    title: str
    severity: Severity
    category: str
    description: str
    location: str
    recommendation: str
    references: List[str]

class ContractAuditor:
    """合约审计器"""
    
    def __init__(self):
        self.vulnerabilities: List[Vulnerability] = []
        self.known_vulnerabilities = {
            'reentrancy': {
                'pattern': r'(call|send|transfer)\{[^}]*\}\s*\([^)]*\)(?!\s*;\s*[^=]*=)',
                'severity': Severity.CRITICAL,
                'description': 'Potential reentrancy vulnerability'
            },
            'unchecked_send': {
                'pattern': r'\.(send|transfer)\([^)]+\)(?!\s*;)',
                'severity': Severity.HIGH,
                'description': 'Unchecked send/transfer return value'
            },
            'tx_origin': {
                'pattern': r'tx\.origin',
                'severity': Severity.HIGH,
                'description': 'Use of tx.origin for authorization'
            },
            'selfdestruct': {
                'pattern': r'selfdestruct|suicide',
                'severity': Severity.MEDIUM,
                'description': 'Contract can be self-destructed'
            },
            'block_timestamp': {
                'pattern': r'block\.timestamp|now\s*[<>=!]',
                'severity': Severity.MEDIUM,
                'description': 'Timestamp dependence'
            },
            'assembly': {
                'pattern': r'assembly\s*\{',
                'severity': Severity.LOW,
                'description': 'Use of inline assembly'
            },
            'delegatecall': {
                'pattern': r'delegatecall',
                'severity': Severity.CRITICAL,
                'description': 'Use of delegatecall can be dangerous'
            }
        }
    
    def fetch_contract_code(self, address: str, network: str = 'ethereum') -> str:
        """获取合约代码（模拟）"""
        # 实际应调用Etherscan API
        mock_code = '''
pragma solidity ^0.8.0;

contract VulnerableContract {
    mapping(address => uint256) public balances;
    
    function withdraw() public {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");
        
        // 漏洞：先转账后更新状态
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        balances[msg.sender] = 0;
    }
    
    function isAuthorized() internal view returns (bool) {
        return tx.origin == owner;  // 漏洞：使用tx.origin
    }
}
'''
        return mock_code
    
    def static_analysis(self, code: str) -> List[Vulnerability]:
        """静态分析"""
        issues = []
        
        for vuln_id, vuln_info in self.known_vulnerabilities.items():
            pattern = vuln_info['pattern']
            matches = list(re.finditer(pattern, code, re.IGNORECASE))
            
            for i, match in enumerate(matches):
                line_num = code[:match.start()].count('\n') + 1
                
                vuln = Vulnerability(
                    id=f"{vuln_id.upper()}-{i+1}",
                    title=vuln_info['description'],
                    severity=vuln_info['severity'],
                    category=self._categorize_vulnerability(vuln_id),
                    description=f"Detected {vuln_id} pattern at line {line_num}",
                    location=f"Line {line_num}",
                    recommendation=self._get_recommendation(vuln_id),
                    references=self._get_references(vuln_id)
                )
                issues.append(vuln)
        
        return issues
    
    def _categorize_vulnerability(self, vuln_type: str) -> str:
        """分类漏洞"""
        categories = {
            'reentrancy': 'Access Control',
            'unchecked_send': 'Error Handling',
            'tx_origin': 'Access Control',
            'selfdestruct': 'Design Issue',
            'block_timestamp': 'Time Manipulation',
            'assembly': 'Code Quality',
            'delegatecall': 'Access Control'
        }
        return categories.get(vuln_type, 'Unknown')
    
    def _get_recommendation(self, vuln_type: str) -> str:
        """获取修复建议"""
        recommendations = {
            'reentrancy': 'Use Checks-Effects-Interactions pattern and consider ReentrancyGuard',
            'unchecked_send': 'Always check return value of send/transfer or use call with validation',
            'tx_origin': 'Use msg.sender instead of tx.origin for authorization',
            'selfdestruct': 'Ensure only authorized parties can call selfdestruct',
            'block_timestamp': 'Use block.number for longer periods or accept small manipulation risk',
            'assembly': 'Document assembly usage and ensure it's necessary',
            'delegatecall': 'Validate target address and ensure proper access control'
        }
        return recommendations.get(vuln_type, 'Review and fix the issue')
    
    def _get_references(self, vuln_type: str) -> List[str]:
        """获取参考资料"""
        refs = {
            'reentrancy': [
                'https://swcregistry.io/docs/SWC-107',
                'https://consensys.github.io/smart-contract-best-practices/attacks/reentrancy/'
            ],
            'unchecked_send': [
                'https://swcregistry.io/docs/SWC-104'
            ],
            'tx_origin': [
                'https://swcregistry.io/docs/SWC-115'
            ]
        }
        return refs.get(vuln_type, [])
    
    def check_compiler_version(self, code: str) -> List[Vulnerability]:
        """检查编译器版本"""
        issues = []
        
        version_match = re.search(r'pragma solidity\s*\^?(\d+)\.(\d+)', code)
        if version_match:
            major = int(version_match.group(1))
            minor = int(version_match.group(2))
            
            if major == 0 and minor < 8:
                issues.append(Vulnerability(
                    id="OUTDATED_COMPILER-1",
                    title="Outdated Solidity version",
                    severity=Severity.HIGH,
                    category="Version Control",
                    description=f"Using Solidity {major}.{minor} without built-in overflow protection",
                    location="Pragma directive",
                    recommendation="Upgrade to Solidity ^0.8.0 or use SafeMath library",
                    references=["https://docs.soliditylang.org/en/v0.8.0/080-breaking-changes.html"]
                ))
        
        return issues
    
    def audit(self, address: str = None, code: str = None, network: str = 'ethereum') -> Dict:
        """执行审计"""
        if not code and address:
            code = self.fetch_contract_code(address, network)
        
        if not code:
            return {'error': 'No code provided'}
        
        logger.info(f"🔍 开始审计合约...")
        
        # 静态分析
        vulns = self.static_analysis(code)
        
        # 编译器版本检查
        vulns.extend(self.check_compiler_version(code))
        
        self.vulnerabilities = vulns
        
        # 生成报告
        return self.generate_report(address or "Unknown")
    
    def generate_report(self, contract_address: str) -> Dict:
        """生成审计报告"""
        severity_counts = {sev: 0 for sev in Severity}
        for v in self.vulnerabilities:
            severity_counts[v.severity] += 1
        
        report = {
            'contract': contract_address,
            'audit_date': '2024-01-01',
            'total_issues': len(self.vulnerabilities),
            'severity_summary': {
                'CRITICAL': severity_counts[Severity.CRITICAL],
                'HIGH': severity_counts[Severity.HIGH],
                'MEDIUM': severity_counts[Severity.MEDIUM],
                'LOW': severity_counts[Severity.LOW],
                'INFO': severity_counts[Severity.INFO]
            },
            'vulnerabilities': [
                {
                    'id': v.id,
                    'title': v.title,
                    'severity': v.severity.value,
                    'category': v.category,
                    'description': v.description,
                    'location': v.location,
                    'recommendation': v.recommendation,
                    'references': v.references
                }
                for v in self.vulnerabilities
            ]
        }
        
        return report
    
    def print_report(self, report: Dict):
        """打印报告"""
        print(f"\n{'='*80}")
        print(f"🔒 智能合约安全审计报告")
        print(f"{'='*80}")
        
        print(f"\n合约地址: {report['contract']}")
        print(f"审计日期: {report['audit_date']}")
        print(f"发现问题: {report['total_issues']} 个")
        
        print(f"\n📊 严重度分布:")
        for sev, count in report['severity_summary'].items():
            emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢',
                'INFO': '⚪'
            }.get(sev, '⚪')
            print(f"   {emoji} {sev}: {count}")
        
        if report['vulnerabilities']:
            print(f"\n🐛 详细发现:")
            for v in report['vulnerabilities']:
                sev_emoji = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟠',
                    'MEDIUM': '🟡',
                    'LOW': '🟢',
                    'INFO': '⚪'
                }.get(v['severity'], '⚪')
                print(f"\n   {sev_emoji} [{v['id']}] {v['title']}")
                print(f"      类别: {v['category']}")
                print(f"      位置: {v['location']}")
                print(f"      描述: {v['description']}")
                print(f"      建议: {v['recommendation']}")
        else:
            print("\n✅ 未发现安全问题")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("🔒 智能合约审计器 - 演示")
    print("="*80)
    
    auditor = ContractAuditor()
    
    # 审计示例合约
    print("\n🔍 审计示例合约...")
    report = auditor.audit(address="0x742d35Cc6634C0532925a3b844Bc9e7595f8dEe")
    
    # 打印报告
    auditor.print_report(report)
    
    # 导出JSON
    with open('audit_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    print("📄 报告已保存到 audit_report.json")
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        address = sys.argv[1]
        network = sys.argv[2] if len(sys.argv) > 2 else 'ethereum'
        auditor = ContractAuditor()
        report = auditor.audit(address=address, network=network)
        auditor.print_report(report)
    else:
        demo()
