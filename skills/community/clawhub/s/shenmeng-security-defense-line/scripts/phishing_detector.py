#!/usr/bin/env python3
"""
钓鱼检测器 - 恶意网站与诈骗识别
"""

import logging
import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ThreatType(Enum):
    SAFE = "SAFE"
    SUSPICIOUS = "SUSPICIOUS"
    PHISHING = "PHISHING"
    MALWARE = "MALWARE"
    SCAM = "SCAM"

@dataclass
class ThreatCheck:
    """威胁检查"""
    check_name: str
    threat_type: ThreatType
    confidence: float
    details: str
    indicators: List[str]

class PhishingDetector:
    """钓鱼检测器"""
    
    def __init__(self):
        # 知名项目域名（用于检测仿冒）
        self.legitimate_domains = {
            'uniswap': ['uniswap.org', 'app.uniswap.org'],
            'ethereum': ['ethereum.org', 'etherscan.io'],
            'aave': ['aave.com', 'app.aave.com'],
            'compound': ['compound.finance'],
            'binance': ['binance.com'],
            'coinbase': ['coinbase.com'],
            'metamask': ['metamask.io'],
            'opensea': ['opensea.io'],
        }
        
        # 已知恶意模式
        self.malicious_patterns = [
            r'claim.*free.*token',
            r'send.*eth.*get.*double',
            r'airdrop.*now',
            r'verify.*wallet',
            r'connect.*wallet.*urgent',
        ]
        
        # 可疑TLD
        self.suspicious_tlds = ['.tk', '.ml', '.ga', '.cf']
        
        self.threats: List[ThreatCheck] = []
    
    def check_domain_similarity(self, url: str) -> ThreatCheck:
        """检查域名相似度（检测仿冒）"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        indicators = []
        threat_type = ThreatType.SAFE
        confidence = 0.0
        
        # 检查字符替换攻击 (homograph attack)
        for brand, legit_domains in self.legitimate_domains.items():
            for legit in legit_domains:
                # 检查是否包含品牌名但有差异
                if brand in domain and legit not in domain:
                    indicators.append(f"疑似仿冒 {brand}: {domain}")
                    threat_type = ThreatType.PHISHING
                    confidence = 0.85
        
        # 检查可疑字符
        suspicious_chars = ['0', '1', 'l', 'i']
        for char in suspicious_chars:
            if char in domain:
                for brand in self.legitimate_domains.keys():
                    if brand.replace('o', char) in domain or brand.replace('l', char) in domain:
                        indicators.append(f"使用可疑字符 '{char}' 仿冒域名")
                        threat_type = ThreatType.PHISHING
                        confidence = max(confidence, 0.9)
        
        return ThreatCheck(
            check_name="域名仿冒检测",
            threat_type=threat_type,
            confidence=confidence,
            details=f"检测到 {len(indicators)} 个仿冒指标" if indicators else "未发现仿冒迹象",
            indicators=indicators
        )
    
    def check_suspicious_tld(self, url: str) -> ThreatCheck:
        """检查可疑顶级域名"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        indicators = []
        threat_type = ThreatType.SAFE
        
        for tld in self.suspicious_tlds:
            if domain.endswith(tld):
                indicators.append(f"使用可疑顶级域名: {tld}")
                threat_type = ThreatType.SUSPICIOUS
        
        # 检查域名长度（过长的域名通常可疑）
        if len(domain) > 50:
            indicators.append(f"域名过长: {len(domain)} 字符")
            threat_type = ThreatType.SUSPICIOUS
        
        return ThreatCheck(
            check_name="域名可信度",
            threat_type=threat_type,
            confidence=0.6 if indicators else 0.0,
            details="域名可信度低" if indicators else "域名可信度正常",
            indicators=indicators
        )
    
    def check_ssl_certificate(self, url: str) -> ThreatCheck:
        """检查SSL证书（模拟）"""
        # 实际实现需要真实检查
        has_ssl = url.startswith('https://')
        
        return ThreatCheck(
            check_name="SSL证书检查",
            threat_type=ThreatType.SAFE if has_ssl else ThreatType.SUSPICIOUS,
            confidence=0.5 if not has_ssl else 0.0,
            details="使用HTTPS加密" if has_ssl else "未使用HTTPS，存在中间人攻击风险",
            indicators=[] if has_ssl else ["无SSL加密"]
        )
    
    def check_content_patterns(self, url: str, content: str = "") -> ThreatCheck:
        """检查内容中的恶意模式"""
        indicators = []
        threat_type = ThreatType.SAFE
        confidence = 0.0
        
        # 模拟内容分析
        suspicious_content = [
            "Connect your wallet to claim",
            "Send ETH to receive double back",
            "Limited time airdrop",
            "Verify your seed phrase",
            "Urgent: Wallet compromise detected"
        ]
        
        for pattern in suspicious_content:
            if pattern.lower() in content.lower():
                indicators.append(f"发现可疑文案: '{pattern}'")
                threat_type = ThreatType.PHISHING
                confidence = 0.8
        
        # 检查钱包连接请求
        if 'connect' in content.lower() and 'wallet' in content.lower():
            if any(x in url for x in ['claim', 'free', 'airdrop', 'gift']):
                indicators.append("可疑的钱包连接请求")
                threat_type = ThreatType.PHISHING
                confidence = max(confidence, 0.75)
        
        return ThreatCheck(
            check_name="内容安全分析",
            threat_type=threat_type,
            confidence=confidence,
            details=f"发现 {len(indicators)} 个可疑内容模式" if indicators else "内容分析正常",
            indicators=indicators
        )
    
    def check_age_reputation(self, url: str) -> ThreatCheck:
        """检查域名年龄和声誉（模拟）"""
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # 模拟域名年龄检查
        indicators = []
        threat_type = ThreatType.SAFE
        
        # 新注册域名（模拟）
        is_new = 'new' in domain or '2024' in domain
        
        if is_new:
            indicators.append("新注册域名")
            threat_type = ThreatType.SUSPICIOUS
        
        return ThreatCheck(
            check_name="域名声誉",
            threat_type=threat_type,
            confidence=0.4 if is_new else 0.0,
            details="域名较新，需谨慎" if is_new else "域名声誉良好",
            indicators=indicators
        )
    
    def detect(self, url: str, content: str = "") -> Dict:
        """执行检测"""
        logger.info(f"🔍 开始检测: {url}")
        
        self.threats = []
        
        # 执行各项检查
        self.threats.append(self.check_domain_similarity(url))
        self.threats.append(self.check_suspicious_tld(url))
        self.threats.append(self.check_ssl_certificate(url))
        self.threats.append(self.check_content_patterns(url, content))
        self.threats.append(self.check_age_reputation(url))
        
        # 确定总体威胁等级
        threat_types = [t.threat_type for t in self.threats]
        
        if ThreatType.MALWARE in threat_types:
            overall = ThreatType.MALWARE
        elif ThreatType.PHISHING in threat_types:
            overall = ThreatType.PHISHING
        elif ThreatType.SCAM in threat_types:
            overall = ThreatType.SCAM
        elif ThreatType.SUSPICIOUS in threat_types:
            overall = ThreatType.SUSPICIOUS
        else:
            overall = ThreatType.SAFE
        
        # 计算平均置信度
        avg_confidence = sum(t.confidence for t in self.threats) / len(self.threats)
        
        # 汇总所有指标
        all_indicators = []
        for t in self.threats:
            all_indicators.extend(t.indicators)
        
        return {
            'url': url,
            'scan_time': '2024-01-01',
            'threat_level': overall.value,
            'confidence': avg_confidence,
            'is_safe': overall == ThreatType.SAFE,
            'indicators': all_indicators,
            'checks': [
                {
                    'name': t.check_name,
                    'threat_type': t.threat_type.value,
                    'confidence': t.confidence,
                    'details': t.details
                }
                for t in self.threats
            ],
            'recommendation': self._get_recommendation(overall)
        }
    
    def _get_recommendation(self, threat_type: ThreatType) -> str:
        """获取建议"""
        recommendations = {
            ThreatType.SAFE: "✅ 网站安全，可以访问",
            ThreatType.SUSPICIOUS: "⚠️ 发现可疑迹象，建议谨慎访问",
            ThreatType.PHISHING: "🚫 疑似钓鱼网站，请勿访问或输入任何信息",
            ThreatType.MALWARE: "🚫 检测到恶意软件，强烈建议立即离开",
            ThreatType.SCAM: "🚫 疑似诈骗网站，请勿进行任何交易"
        }
        return recommendations.get(threat_type, "请谨慎判断")
    
    def print_report(self, report: Dict):
        """打印报告"""
        print(f"\n{'='*80}")
        print(f"🎣 钓鱼检测器报告")
        print(f"{'='*80}")
        
        print(f"\n🌐 检测URL: {report['url']}")
        
        # 威胁等级
        threat_emoji = {
            'SAFE': '🟢',
            'SUSPICIOUS': '🟡',
            'PHISHING': '🔴',
            'MALWARE': '🔴',
            'SCAM': '🔴'
        }.get(report['threat_level'], '⚪')
        
        print(f"⚠️ 威胁等级: {threat_emoji} {report['threat_level']}")
        print(f"📊 置信度: {report['confidence']:.0%}")
        
        # 发现的指标
        if report['indicators']:
            print(f"\n🚩 风险指标 ({len(report['indicators'])}):")
            for indicator in report['indicators']:
                print(f"   • {indicator}")
        
        # 详细检查
        print(f"\n🔍 详细检查:")
        for check in report['checks']:
            emoji = {
                'SAFE': '🟢',
                'SUSPICIOUS': '🟡',
                'PHISHING': '🔴',
                'MALWARE': '🔴',
                'SCAM': '🔴'
            }.get(check['threat_type'], '⚪')
            print(f"   {emoji} {check['name']}: {check['details']}")
        
        # 建议
        print(f"\n💡 建议:")
        print(f"   {report['recommendation']}")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("🎣 钓鱼检测器 - 演示")
    print("="*80)
    
    detector = PhishingDetector()
    
    # 检测可疑URL
    test_urls = [
        "https://uniswap.org",
        "https://uniswop.org",  # 仿冒
        "https://claim-free-tokens.xyz",
        "https://ethereum.org"
    ]
    
    for url in test_urls:
        print(f"\n{'-'*40}")
        report = detector.detect(url, content="Connect your wallet to claim free tokens")
        detector.print_report(report)
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        url = sys.argv[1]
        detector = PhishingDetector()
        report = detector.detect(url)
        detector.print_report(report)
    else:
        demo()
