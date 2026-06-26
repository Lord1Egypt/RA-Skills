#!/usr/bin/env python3
"""
多签钱包管理器 - 多重签名钱包管理与操作
"""

import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TransactionStatus(Enum):
    PENDING = "PENDING"
    EXECUTED = "EXECUTED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

@dataclass
class MultisigTransaction:
    """多签交易"""
    id: int
    to: str
    value: float
    data: str
    executed: bool
    num_confirmations: int
    status: TransactionStatus
    proposer: str
    created_at: str

class MultisigManager:
    """多签钱包管理器"""
    
    def __init__(self, wallet_address: str = None):
        self.wallet_address = wallet_address
        self.owners: List[str] = []
        self.threshold: int = 0  # M-of-N中的M
        self.transactions: List[MultisigTransaction] = []
        self.nonce: int = 0
        
        if wallet_address:
            self._load_wallet_info()
    
    def _load_wallet_info(self):
        """加载钱包信息（模拟）"""
        # 模拟从区块链读取
        self.owners = [
            "0x1111111111111111111111111111111111111111",
            "0x2222222222222222222222222222222222222222",
            "0x3333333333333333333333333333333333333333"
        ]
        self.threshold = 2
        self.balance = 10.5  # ETH
    
    def get_wallet_info(self) -> Dict:
        """获取钱包信息"""
        return {
            'address': self.wallet_address,
            'owners': self.owners,
            'threshold': f"{self.threshold}-of-{len(self.owners)}",
            'balance': self.balance,
            'transaction_count': len(self.transactions),
            'pending_count': sum(1 for t in self.transactions if t.status == TransactionStatus.PENDING)
        }
    
    def propose_transaction(
        self,
        to: str,
        value: float,
        data: str = "0x",
        proposer: str = None
    ) -> Dict:
        """发起交易"""
        tx_id = len(self.transactions)
        
        tx = MultisigTransaction(
            id=tx_id,
            to=to,
            value=value,
            data=data,
            executed=False,
            num_confirmations=1,  # 提议者自动确认
            status=TransactionStatus.PENDING,
            proposer=proposer or self.owners[0],
            created_at="2024-01-01"
        )
        
        self.transactions.append(tx)
        self.nonce += 1
        
        logger.info(f"✅ 交易 #{tx_id} 已发起")
        logger.info(f"   目标: {to}")
        logger.info(f"   金额: {value} ETH")
        logger.info(f"   需要 {self.threshold} 个签名")
        
        return {
            'success': True,
            'tx_id': tx_id,
            'confirmations_needed': self.threshold - 1,
            'tx_hash': f"0x{tx_id:064x}"
        }
    
    def confirm_transaction(self, tx_id: int, signer: str) -> Dict:
        """确认交易"""
        if tx_id >= len(self.transactions):
            return {'success': False, 'error': '交易不存在'}
        
        tx = self.transactions[tx_id]
        
        if tx.status != TransactionStatus.PENDING:
            return {'success': False, 'error': '交易已执行或取消'}
        
        if signer not in self.owners:
            return {'success': False, 'error': '签名者不是钱包所有者'}
        
        tx.num_confirmations += 1
        
        logger.info(f"✅ 交易 #{tx_id} 获得签名 ({tx.num_confirmations}/{self.threshold})")
        
        # 检查是否达到阈值
        if tx.num_confirmations >= self.threshold:
            logger.info(f"🎉 交易 #{tx_id} 已达到执行阈值！")
        
        return {
            'success': True,
            'tx_id': tx_id,
            'confirmations': tx.num_confirmations,
            'threshold': self.threshold,
            'ready_to_execute': tx.num_confirmations >= self.threshold
        }
    
    def execute_transaction(self, tx_id: int, executor: str) -> Dict:
        """执行交易"""
        if tx_id >= len(self.transactions):
            return {'success': False, 'error': '交易不存在'}
        
        tx = self.transactions[tx_id]
        
        if tx.status != TransactionStatus.PENDING:
            return {'success': False, 'error': '交易已执行或取消'}
        
        if tx.num_confirmations < self.threshold:
            return {'success': False, 'error': f'签名不足 ({tx.num_confirmations}/{self.threshold})'}
        
        # 模拟执行
        tx.executed = True
        tx.status = TransactionStatus.EXECUTED
        self.balance -= tx.value
        
        logger.info(f"✅ 交易 #{tx_id} 已执行")
        logger.info(f"   目标: {tx.to}")
        logger.info(f"   金额: {tx.value} ETH")
        
        return {
            'success': True,
            'tx_id': tx_id,
            'executed_at': '2024-01-01',
            'gas_used': 21000,
            'actual_tx_hash': f"0xexec{tx_id:062x}"
        }
    
    def revoke_confirmation(self, tx_id: int, signer: str) -> Dict:
        """撤销确认"""
        if tx_id >= len(self.transactions):
            return {'success': False, 'error': '交易不存在'}
        
        tx = self.transactions[tx_id]
        
        if tx.status != TransactionStatus.PENDING:
            return {'success': False, 'error': '交易已执行或取消'}
        
        if tx.num_confirmations > 0:
            tx.num_confirmations -= 1
            logger.info(f"⚠️ 交易 #{tx_id} 撤销了一个签名")
        
        return {'success': True, 'tx_id': tx_id, 'confirmations': tx.num_confirmations}
    
    def add_owner(self, new_owner: str, proposer: str) -> Dict:
        """添加所有者"""
        if new_owner in self.owners:
            return {'success': False, 'error': '已经是所有者'}
        
        self.owners.append(new_owner)
        logger.info(f"✅ 新所有者已添加: {new_owner}")
        logger.info(f"   当前所有者数: {len(self.owners)}")
        
        return {
            'success': True,
            'new_owner': new_owner,
            'total_owners': len(self.owners)
        }
    
    def remove_owner(self, owner: str, proposer: str) -> Dict:
        """移除所有者"""
        if owner not in self.owners:
            return {'success': False, 'error': '不是所有者'}
        
        if len(self.owners) - 1 < self.threshold:
            return {'success': False, 'error': '移除后签名者数将少于阈值'}
        
        self.owners.remove(owner)
        logger.info(f"✅ 所有者已移除: {owner}")
        logger.info(f"   剩余所有者数: {len(self.owners)}")
        
        return {
            'success': True,
            'removed_owner': owner,
            'total_owners': len(self.owners)
        }
    
    def change_threshold(self, new_threshold: int) -> Dict:
        """修改阈值"""
        if new_threshold > len(self.owners):
            return {'success': False, 'error': '阈值不能大于所有者数'}
        
        if new_threshold < 1:
            return {'success': False, 'error': '阈值至少为1'}
        
        old_threshold = self.threshold
        self.threshold = new_threshold
        
        logger.info(f"✅ 阈值已修改: {old_threshold} -> {new_threshold}")
        
        return {
            'success': True,
            'old_threshold': old_threshold,
            'new_threshold': new_threshold
        }
    
    def get_pending_transactions(self) -> List[Dict]:
        """获取待处理交易"""
        pending = [
            {
                'id': tx.id,
                'to': tx.to,
                'value': tx.value,
                'confirmations': tx.num_confirmations,
                'threshold': self.threshold,
                'proposer': tx.proposer,
                'created_at': tx.created_at
            }
            for tx in self.transactions
            if tx.status == TransactionStatus.PENDING
        ]
        return pending
    
    def print_wallet_status(self):
        """打印钱包状态"""
        info = self.get_wallet_info()
        
        print(f"\n{'='*80}")
        print(f"👥 多签钱包状态")
        print(f"{'='*80}")
        
        print(f"\n📋 钱包地址: {info['address']}")
        print(f"💰 余额: {info['balance']} ETH")
        print(f"🔐 签名阈值: {info['threshold']}")
        
        print(f"\n👤 所有者列表 ({len(info['owners'])}):")
        for i, owner in enumerate(info['owners'], 1):
            print(f"   {i}. {owner}")
        
        print(f"\n📊 交易统计:")
        print(f"   总交易数: {info['transaction_count']}")
        print(f"   待处理: {info['pending_count']}")
        
        # 待处理交易
        pending = self.get_pending_transactions()
        if pending:
            print(f"\n⏳ 待处理交易:")
            for tx in pending:
                status = "✅ 可执行" if tx['confirmations'] >= self.threshold else f"📝 签名中 ({tx['confirmations']}/{self.threshold})"
                print(f"   #{tx['id']}: 发送 {tx['value']} ETH 到 {tx['to'][:20]}... {status}")
        
        print(f"{'='*80}\n")


def demo():
    """演示"""
    print("👥 多签钱包管理器 - 演示")
    print("="*80)
    
    # 创建多签钱包
    wallet = MultisigManager("0xMultisigWallet1234567890abcdef")
    
    # 显示状态
    wallet.print_wallet_status()
    
    # 发起交易
    print("\n📝 发起交易...")
    result = wallet.propose_transaction(
        to="0xRecipientAddress1234567890abcdef",
        value=1.5,
        proposer=wallet.owners[0]
    )
    print(f"交易ID: {result['tx_id']}")
    
    # 第二个所有者确认
    print("\n✍️ 第二个所有者确认...")
    result = wallet.confirm_transaction(0, wallet.owners[1])
    print(f"确认数: {result['confirmations']}/{result['threshold']}")
    print(f"可执行: {result['ready_to_execute']}")
    
    # 执行交易
    print("\n🚀 执行交易...")
    result = wallet.execute_transaction(0, wallet.owners[0])
    print(f"执行结果: {'成功' if result['success'] else '失败'}")
    if result['success']:
        print(f"交易哈希: {result['actual_tx_hash']}")
    
    # 最终状态
    wallet.print_wallet_status()
    
    print("\n✅ 演示完成!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        wallet = MultisigManager(sys.argv[1])
        wallet.print_wallet_status()
    else:
        demo()
