#!/usr/bin/env python3
"""
Tiger 交易客户端封装
支持：账户查询、持仓查询、交易下单
"""
import os
import json
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.common.util.signature_utils import read_private_key
from tigeropen.trade.trade_client import TradeClient
from tigeropen.trade.domain.order import Order
from tigeropen.trade.domain.contract import Contract


class TigerClient:
    def __init__(self, tiger_id: str, account: str, license: str, private_key: str):
        """
        初始化 Tiger 客户端
        
        Args:
            tiger_id: Tiger ID
            account: 账户ID
            license: 许可证 (如 TBNZ)
            private_key: 私钥内容或私钥文件路径
        """
        self.tiger_id = tiger_id
        self.account = account
        self.license = license
        self.private_key = private_key
        self._client = None
    
    def _get_client(self) -> TradeClient:
        """获取或创建交易客户端"""
        if self._client is None:
            client_config = TigerOpenClientConfig()
            
            # 判断是私钥内容还是文件路径
            if os.path.isfile(self.private_key):
                client_config.private_key = read_private_key(self.private_key)
            else:
                # 直接使用私钥内容
                from tigeropen.common.util.signature_utils import read_private_key_from_text
                client_config.private_key = read_private_key_from_text(self.private_key)
            
            client_config.tiger_id = self.tiger_id
            client_config.account = self.account
            client_config.license = self.license
            
            self._client = TradeClient(client_config)
        
        return self._client
    
    def get_account(self) -> dict:
        """获取账户信息"""
        client = self._get_client()
        accounts = client.get_managed_accounts()
        return {
            'success': True,
            'accounts': [
                {
                    'id': acc.account,
                    'name': str(acc.account_type),
                    'type': str(acc.capability),
                    'status': str(acc.status)
                }
                for acc in (accounts or [])
            ]
        }
    
    def get_positions(self) -> dict:
        """获取持仓"""
        client = self._get_client()
        try:
            positions = client.get_positions()
            return {
                'success': True,
                'positions': [
                    {
                        'symbol': p.contract.symbol if p.contract else None,
                        'quantity': p.quantity,
                        'avg_cost': p.average_cost,
                        'market_value': p.market_value,
                        'unrealized_pnl': p.unrealized_pnl,
                        'unrealized_pnl_percent': p.unrealized_pnl_percent
                    }
                    for p in (positions or [])
                ]
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_balance(self) -> dict:
        """获取账户余额"""
        client = self._get_client()
        try:
            assets = client.get_assets()
            if assets:
                a = assets[0]
                summary = a.summary
                return {
                    'success': True,
                    'balance': {
                        'cash': summary.cash,
                        'buying_power': summary.buying_power,
                        'net_liquidation': summary.net_liquidation,
                        'unrealized_pnl': summary.unrealized_pnl,
                        'currency': summary.currency
                    }
                }
            return {'success': False, 'message': '无资产信息'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def place_order(self, symbol: str, side: str, quantity: int, 
                    order_type: str = 'LMT', price: float = None) -> dict:
        """
        下单
        
        Args:
            symbol: 股票代码 (如 AAPL)
            side: buy/sell
            quantity: 数量
            order_type: LMT (限价) / MKT (市价)
            price: 价格 (限价单需要)
        """
        client = self._get_client()
        
        try:
            contract = Contract(symbol=symbol, currency='USD', sec_type='STK')
            tiger_order = Order(
                account=self.account,
                contract=contract,
                action=side.upper(),
                order_type=order_type,
                quantity=quantity,
                limit_price=price
            )
            
            result = client.place_order(tiger_order)
            
            return {
                'success': True,
                'order_id': result,
                'message': f'订单已提交: {symbol} {side.upper()} {quantity}'
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def get_orders(self, states: list = None) -> dict:
        """查询订单"""
        client = self._get_client()
        try:
            orders = client.get_orders(states=states)
            result = []
            for o in (orders or []):
                result.append({
                    'order_id': str(o.order_id),
                    'symbol': o.contract.symbol if o.contract else None,
                    'side': str(o.action),
                    'quantity': o.quantity,
                    'filled': o.filled,
                    'status': str(o.status) if o.status else None,
                    'order_type': str(o.order_type) if o.order_type else None
                })
            return {
                'success': True,
                'orders': result
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}
    
    def cancel_order(self, order_id: str) -> dict:
        """取消订单"""
        client = self._get_client()
        try:
            result = client.cancel_order(order_id)
            return {
                'success': True,
                'order_id': order_id,
                'message': '订单已取消'
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}


# ============ CLI ============
if __name__ == '__main__':
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description='Tiger 交易客户端')
    parser.add_argument('--tiger-id', required=True, help='Tiger ID')
    parser.add_argument('--account', required=True, help='账户ID')
    parser.add_argument('--license', default='TBNZ', help='许可证')
    parser.add_argument('--private-key', required=True, help='私钥路径或内容')
    
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 账户查询
    subparsers.add_parser('account', help='查询账户')
    
    # 持仓查询
    subparsers.add_parser('positions', help='查询持仓')
    
    # 余额查询
    subparsers.add_parser('balance', help='查询余额')
    
    # 下单
    order_parser = subparsers.add_parser('order', help='下单')
    order_parser.add_argument('--symbol', required=True, help='股票代码')
    order_parser.add_argument('--side', required=True, help='buy/sell')
    order_parser.add_argument('--quantity', type=int, required=True, help='数量')
    order_parser.add_argument('--price', type=float, help='价格')
    order_parser.add_argument('--type', default='LMT', help='LMT/MKT')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    client = TigerClient(args.tiger_id, args.account, args.license, args.private_key)
    
    if args.command == 'account':
        result = client.get_account()
    elif args.command == 'positions':
        result = client.get_positions()
    elif args.command == 'balance':
        result = client.get_balance()
    elif args.command == 'order':
        result = client.place_order(args.symbol, args.side, args.quantity, args.type, args.price)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
