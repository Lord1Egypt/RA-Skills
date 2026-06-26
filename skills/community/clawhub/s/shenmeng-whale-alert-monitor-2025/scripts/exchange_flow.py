#!/usr/bin/env python3
"""
交易所资金流向监控器 - 监控交易所的资金流入流出
"""

import logging
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FlowType(Enum):
    INFLOW = "inflow"      # 流入交易所
    OUTFLOW = "outflow"    # 流出交易所

@dataclass
class FlowRecord:
    """资金流向记录"""
    timestamp: datetime
    exchange: str
    flow_type: FlowType
    token: str
    amount: float
    usd_value: float
    tx_hash: str
    from_addr: str
    to_addr: str

@dataclass
class ExchangeMetrics:
    """交易所指标"""
    exchange: str
    total_inflow_24h: float
    total_outflow_24h: float
    net_flow: float
    token_breakdown: Dict[str, Dict]

class ExchangeFlowMonitor:
    """交易所资金流向监控器"""
    
    def __init__(self):
        # 主要交易所地址库
        self.exchange_addresses = {
            'binance': {
                'name': 'Binance',
                'addresses': [
                    '0x3f5CE5FBFe3E9af3971dD833D26bA9b5C936f0bE',
                    '0xdB3c617cDd2fBf0c8611C04A49d34C7B332e2BB6',
                    '0x5a52E96BAcdaBb82fd05763E25335261B270Efcb'
                ]
            },
            'coinbase': {
                'name': 'Coinbase',
                'addresses': [
                    '0x71660c4005BA85c37ccec55d0C4493E66Fe775d3',
                    '0x503828976D22510aad0201ac7EC88293211D23Da'
                ]
            },
            'okx': {
                'name': 'OKX',
                'addresses': [
                    '0x6b75d8AF000000e20B7a7DD000000090D0000000'
                ]
            },
            'bybit': {
                'name': 'Bybit',
                'addresses': [
                    '0xf89d7b9c864f589bbF53f821d7EfC68c91d70958'
                ]
            },
            'kucoin': {
                'name': 'KuCoin',
                'addresses': [
                    '0x2B6eD29a95753C3Ad948348e3e7b1A251039FBB9'
                ]
            }
        }
        
        self.flow_history: List[FlowRecord] = []
    
    def get_exchange_name(self, address: str) -> Optional[str]:
        """根据地址获取交易所名称"""
        address = address.lower()
        
        for exchange_id, info in self.exchange_addresses.items():
            for addr in info['addresses']:
                if addr.lower() == address:
                    return info['name']
        
        return None
    
    def is_exchange_address(self, address: str) -> bool:
        """检查是否为交易所地址"""
        return self.get_exchange_name(address) is not None
    
    def fetch_flow_data(self, exchange: str, hours: int = 24) -> List[FlowRecord]:
        """获取资金流向数据（模拟）"""
        import random
        
        records = []
        base_time = datetime.now() - timedelta(hours=hours)
        
        exchange_info = self.exchange_addresses.get(exchange)
        if not exchange_info:
            return records
        
        # 生成10-30笔流向记录
        tokens = ['ETH', 'BTC', 'USDT', 'USDC']
        
        for i in range(random.randint(10, 30)):
            tx_time = base_time + timedelta(minutes=random.uniform(0, hours * 60))
            
            token = random.choice(tokens)
            flow_type = random.choice([FlowType.INFLOW, FlowType.OUTFLOW])
            
            # 生成金额
            if token in ['ETH']:
                amount = random.uniform(100, 5000)
                price = 3500
            elif token in ['BTC', 'WBTC']:
                amount = random.uniform(10, 200)
                price = 65000
            else:
                amount = random.uniform(100000, 10000000)
                price = 1
            
            usd_value = amount * price
            
            if flow_type == FlowType.INFLOW:
                from_addr = f"0x{''.join([random.choice('0123456789abcdef') for _ in range(40)])}"
                to_addr = random.choice(exchange_info['addresses'])
            else:
                from_addr = random.choice(exchange_info['addresses'])
                to_addr = f"0x{''.join([random.choice('0123456789abcdef') for _ in range(40)])}"
            
            record = FlowRecord(
                timestamp=tx_time,
                exchange=exchange_info['name'],
                flow_type=flow_type,
                token=token,
                amount=amount,
                usd_value=usd_value,
                tx_hash=f"0x{''.join([random.choice('0123456789abcdef') for _ in range(64)])}",
                from_addr=from_addr,
                to_addr=to_addr
            )
            
            records.append(record)
        
        # 按时间排序
        records.sort(key=lambda x: x.timestamp, reverse=True)
        return records
    
    def calculate_metrics(self, records: List[FlowRecord]) -> ExchangeMetrics:
        """计算交易所指标"""
        if not records:
            return None
        
        exchange = records[0].exchange
        
        inflows = [r for r in records if r.flow_type == FlowType.INFLOW]
        outflows = [r for r in records if r.flow_type == FlowType.OUTFLOW]
        
        total_inflow = sum(r.usd_value for r in inflows)
        total_outflow = sum(r.usd_value for r in outflows)
        net_flow = total_outflow - total_inflow  # 正数表示净流出，负数表示净流入
        
        # 代币细分
        token_breakdown = {}
        for token in set(r.token for r in records):
            token_in = sum(r.usd_value for r in inflows if r.token == token)
            token_out = sum(r.usd_value for r in outflows if r.token == token)
            
            token_breakdown[token] = {
                'inflow': token_in,
                'outflow': token_out,
                'net': token_out - token_in
            }
        
        return ExchangeMetrics(
            exchange=exchange,
            total_inflow_24h=total_inflow,
            total_outflow_24h=total_outflow,
            net_flow=net_flow,
            token_breakdown=token_breakdown
        )
    
    def detect_significant_flows(self, records: List[FlowRecord], threshold: float = 5000000) -> List[FlowRecord]:
        """检测显著的流向"""
        return [r for r in records if r.usd_value >= threshold]
    
    def print_flow_report(self, metrics: ExchangeMetrics):
        """打印流向报告"""
        print(f"\n{'='*80}")
        print(f"🏛️  {metrics.exchange} 资金流向报告 (24h)")
        print(f"{'='*80}")
        
        print(f"\n💰 总体流向:")
        print(f"   总流入: ${metrics.total_inflow_24h:,.0f}")
        print(f"   总流出: ${metrics.total_outflow_24h:,.0f}")
        
        # 净流入/流出
        if metrics.net_flow > 0:
            print(f"   净流向: 🟢 净流出 ${metrics.net_flow:,.0f}")
            print(f"   信号: 用户提币，可能看涨")
        else:
            print(f"   净流向: 🔴 净流入 ${abs(metrics.net_flow):,.0f}")
            print(f"   信号: 用户充值，可能看跌")
        
        print(f"\n📊 代币细分:")
        for token, data in metrics.token_breakdown.items():
            net = data['net']
            emoji = "🟢" if net > 0 else "🔴"
            direction = "流出" if net > 0 else "流入"
            print(f"   {emoji} {token}: {direction} ${abs(net):,.0f}")
        
        print(f"{'='*80}\n")
    
    def compare_exchanges(self, exchanges: List[str]) -> Dict:
        """对比多个交易所"""
        comparison = {}
        
        for exchange in exchanges:
            records = self.fetch_flow_data(exchange, hours=24)
            metrics = self.calculate_metrics(records)
            
            if metrics:
                comparison[exchange] = {
                    'net_flow': metrics.net_flow,
                    'inflow': metrics.total_inflow_24h,
                    'outflow': metrics.total_outflow_24h
                }
        
        return comparison
    
    def print_comparison(self, comparison: Dict):
        """打印对比结果"""
        print(f"\n{'='*80}")
        print(f"📊 交易所资金流向对比 (24h)")
        print(f"{'='*80}")
        print(f"{'交易所':<15} {'净流入':<20} {'流入':<20} {'流出':<20}")
        print(f"{'-'*80}")
        
        # 按净流量排序
        sorted_exchanges = sorted(
            comparison.items(),
            key=lambda x: x[1]['net_flow'],
            reverse=True
        )
        
        for exchange, data in sorted_exchanges:
            net = data['net_flow']
            emoji = "🟢" if net > 0 else "🔴"
            net_str = f"{emoji} ${net:,.0f}"
            
            print(f"{exchange:<15} {net_str:<20} ${data['inflow']:<19,.0f} ${data['outflow']:<19,.0f}")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("🏛️ 交易所资金流向监控器 - 演示")
    print("="*80)
    
    monitor = ExchangeFlowMonitor()
    
    # 监控单个交易所
    print("\n🔍 监控 Binance...")
    binance_records = monitor.fetch_flow_data('binance', hours=24)
    binance_metrics = monitor.calculate_metrics(binance_records)
    
    if binance_metrics:
        monitor.print_flow_report(binance_metrics)
        
        # 检测大额流向
        significant = monitor.detect_significant_flows(binance_records, threshold=5000000)
        if significant:
            print(f"⚠️  检测到 {len(significant)} 笔大额流向:\n")
            for flow in significant[:5]:
                direction = "流入" if flow.flow_type == FlowType.INFLOW else "流出"
                print(f"   {flow.timestamp.strftime('%m-%d %H:%M')} | "
                      f"{direction} ${flow.usd_value:,.0f} {flow.token}")
    
    # 对比多个交易所
    print("\n📊 对比主要交易所...")
    exchanges = ['binance', 'coinbase', 'okx']
    comparison = monitor.compare_exchanges(exchanges)
    monitor.print_comparison(comparison)
    
    # 整体分析
    total_inflow = sum(d['inflow'] for d in comparison.values())
    total_outflow = sum(d['outflow'] for d in comparison.values())
    total_net = sum(d['net_flow'] for d in comparison.values())
    
    print(f"📈 整体市场信号:")
    print(f"   总流入: ${total_inflow:,.0f}")
    print(f"   总流出: ${total_outflow:,.0f}")
    if total_net > 0:
        print(f"   总体: 🟢 净流出 ${total_net:,.0f} - 可能看涨信号")
    else:
        print(f"   总体: 🔴 净流入 ${abs(total_net):,.0f} - 可能看跌信号")
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    demo()
