#!/usr/bin/env python3
"""
Solana 生态概览监控脚本
获取 Solana 生态关键指标
"""

import json
import sys
from datetime import datetime
from typing import Dict, Optional

try:
    import requests
except ImportError:
    print("Warning: requests library not available. Using urllib.")
    requests = None


class SolanaEcosystemMonitor:
    """Solana 生态监控器"""
    
    def __init__(self):
        self.base_urls = {
            'defillama': 'https://api.llama.fi',
            'coingecko': 'https://api.coingecko.com/api/v3',
        }
    
    def get_tvl(self) -> Optional[Dict]:
        """获取 Solana TVL 数据"""
        try:
            if requests:
                resp = requests.get(f"{self.base_urls['defillama']}/chain/Solana", timeout=10)
                data = resp.json()
            else:
                import urllib.request
                with urllib.request.urlopen(f"{self.base_urls['defillama']}/chain/Solana", timeout=10) as resp:
                    data = json.loads(resp.read().decode())
            
            return {
                'tvl': data.get('tvl', 0),
                'tvl_7d_change': data.get('change_7d', 0),
                'tvl_1d_change': data.get('change_1d', 0),
                'mcap_tvl_ratio': data.get('mcap/tvl', 0),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_top_protocols(self, limit: int = 10) -> Optional[list]:
        """获取 Solana 顶级协议"""
        try:
            if requests:
                resp = requests.get(f"{self.base_urls['defillama']}/protocols", timeout=10)
                protocols = resp.json()
            else:
                import urllib.request
                with urllib.request.urlopen(f"{self.base_urls['defillama']}/protocols", timeout=10) as resp:
                    protocols = json.loads(resp.read().decode())
            
            # 筛选 Solana 协议
            solana_protocols = [
                p for p in protocols 
                if any(chain.get('chain') == 'Solana' for chain in p.get('chainTvls', []))
            ]
            
            # 按 TVL 排序
            solana_protocols.sort(key=lambda x: x.get('tvl', 0), reverse=True)
            
            return [
                {
                    'name': p['name'],
                    'tvl': p.get('tvl', 0),
                    'category': p.get('category', 'Unknown'),
                    'change_7d': p.get('change_7d', 0)
                }
                for p in solana_protocols[:limit]
            ]
        except Exception as e:
            return [{'error': str(e)}]
    
    def get_market_overview(self) -> Dict:
        """获取市场概览"""
        overview = {
            'timestamp': datetime.now().isoformat(),
            'solana': {
                'tvl_data': self.get_tvl(),
                'top_protocols': self.get_top_protocols(5)
            }
        }
        return overview
    
    def format_report(self, data: Dict) -> str:
        """格式化报告"""
        report = f"""
{'='*60}
🌊 Solana 生态概览报告
⏰ 更新时间: {data['timestamp']}
{'='*60}

"""
        # TVL 数据
        tvl_data = data['solana'].get('tvl_data', {})
        if 'error' not in tvl_data:
            report += f"📊 TVL 数据:\n"
            report += f"  • 总锁定价值: ${tvl_data.get('tvl', 0)/1e9:.2f}B\n"
            report += f"  • 7日变化: {tvl_data.get('tvl_7d_change', 0):+.2f}%\n"
            report += f"  • 1日变化: {tvl_data.get('tvl_1d_change', 0):+.2f}%\n"
            report += f"  • 市值/TVL 比率: {tvl_data.get('mcap_tvl_ratio', 0):.2f}\n"
        else:
            report += f"⚠️ TVL 数据获取失败: {tvl_data.get('error')}\n"
        
        # 顶级协议
        protocols = data['solana'].get('top_protocols', [])
        if protocols and 'error' not in protocols[0]:
            report += f"\n🏆 顶级协议 (按 TVL):\n"
            for i, p in enumerate(protocols, 1):
                tvl = p.get('tvl', 0)
                if tvl > 1e9:
                    tvl_str = f"${tvl/1e9:.2f}B"
                elif tvl > 1e6:
                    tvl_str = f"${tvl/1e6:.2f}M"
                else:
                    tvl_str = f"${tvl:,.0f}"
                report += f"  {i}. {p['name']} ({p['category']}) - {tvl_str}\n"
        
        report += f"\n{'='*60}\n"
        return report


def main():
    """主函数"""
    monitor = SolanaEcosystemMonitor()
    data = monitor.get_market_overview()
    print(monitor.format_report(data))
    
    # 保存 JSON 数据
    output_file = f"/tmp/solana_overview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n💾 数据已保存到: {output_file}")


if __name__ == '__main__':
    main()
