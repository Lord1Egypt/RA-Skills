#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base Chain On-chain Verification
Base 链上验证模块 - 验证 USDC 转账

支持:
- Base Mainnet (主网)
- Base Sepolia (测试网)

验证内容:
1. 交易是否存在且成功
2. 转账金额是否正确
3. 接收地址是否正确
4. 确认数是否足够
"""

import json
import requests
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass


# Base 链配置
BASE_CONFIG = {
    "mainnet": {
        "rpc_url": "https://mainnet.base.org",  # 公共 RPC
        "usdc_contract": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "chain_id": 8453,
        "explorer": "https://basescan.org",
    },
    "sepolia": {
        "rpc_url": "https://sepolia.base.org",  # 测试网 RPC
        "usdc_contract": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
        "chain_id": 84532,
        "explorer": "https://sepolia.basescan.org",
    }
}

# USDC Transfer 事件签名
USDC_TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"


@dataclass
class TransactionInfo:
    """交易信息"""
    tx_hash: str
    from_address: str
    to_address: str
    amount: float  # USDC 金额
    token_contract: str
    block_number: int
    confirmations: int
    status: str  # "success" | "pending" | "failed"
    timestamp: int


class BaseChainVerifier:
    """Base 链验证器"""
    
    def __init__(self, network: str = "mainnet", api_key: str = None):
        """
        初始化验证器
        
        Args:
            network: "mainnet" 或 "sepolia"
            api_key: Alchemy/Infura API Key (可选，使用公共节点时不需要)
        """
        self.network = network
        self.config = BASE_CONFIG[network]
        
        # 如果有 API Key，使用 Alchemy/Infura
        if api_key:
            if "alchemy" in api_key:
                self.rpc_url = f"https://base-{network}.g.alchemy.com/v2/{api_key}"
            elif "infura" in api_key:
                self.rpc_url = f"https://base-{network}.infura.io/v3/{api_key}"
            else:
                self.rpc_url = self.config["rpc_url"]
        else:
            self.rpc_url = self.config["rpc_url"]
    
    def _rpc_call(self, method: str, params: list) -> Dict:
        """发送 RPC 调用"""
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": 1
        }
        
        try:
            response = requests.post(
                self.rpc_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"RPC 调用失败: {e}")
            return {"error": str(e)}
    
    def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict]:
        """获取交易收据"""
        # 确保 tx_hash 有 0x 前缀
        if not tx_hash.startswith("0x"):
            tx_hash = "0x" + tx_hash
        
        result = self._rpc_call("eth_getTransactionReceipt", [tx_hash])
        
        if "error" in result:
            print(f"获取交易收据失败: {result['error']}")
            return None
        
        return result.get("result")
    
    def get_transaction(self, tx_hash: str) -> Optional[Dict]:
        """获取交易详情"""
        if not tx_hash.startswith("0x"):
            tx_hash = "0x" + tx_hash
        
        result = self._rpc_call("eth_getTransactionByHash", [tx_hash])
        
        if "error" in result:
            print(f"获取交易详情失败: {result['error']}")
            return None
        
        return result.get("result")
    
    def get_block_number(self) -> int:
        """获取最新区块号"""
        result = self._rpc_call("eth_blockNumber", [])
        
        if "error" in result:
            return 0
        
        return int(result.get("result", "0x0"), 16)
    
    def parse_usdc_transfer(self, receipt: Dict, expected_to: str) -> Optional[Dict]:
        """
        解析 USDC 转账事件
        
        Args:
            receipt: 交易收据
            expected_to: 期望的接收地址
        
        Returns:
            转账信息或 None
        """
        logs = receipt.get("logs", [])
        
        for log in logs:
            # 检查 topic[0] 是否是 Transfer 事件
            topics = log.get("topics", [])
            if len(topics) < 3:
                continue
            
            if topics[0].lower() != USDC_TRANSFER_TOPIC.lower():
                continue
            
            # 检查合约地址是否是 USDC
            contract = log.get("address", "").lower()
            if contract != self.config["usdc_contract"].lower():
                continue
            
            # 解析接收地址 (topic[2])
            to_address = "0x" + topics[2][-40:]
            
            # 检查接收地址是否匹配
            if to_address.lower() != expected_to.lower():
                continue
            
            # 解析金额 (data 字段)
            data = log.get("data", "0x0")
            amount_raw = int(data, 16)
            amount = amount_raw / 1e6  # USDC 是 6 位小数
            
            # 解析发送地址 (topic[1])
            from_address = "0x" + topics[1][-40:]
            
            return {
                "from": from_address,
                "to": to_address,
                "amount": amount,
                "contract": contract,
            }
        
        return None
    
    def verify_payment(
        self, 
        tx_hash: str, 
        expected_amount: float, 
        expected_to: str,
        min_confirmations: int = 3
    ) -> Tuple[bool, str, Optional[TransactionInfo]]:
        """
        验证 USDC 支付
        
        Args:
            tx_hash: 交易哈希
            expected_amount: 期望金额 (USDC)
            expected_to: 期望接收地址
            min_confirmations: 最小确认数
        
        Returns:
            (是否成功, 消息, 交易信息)
        """
        print(f"\n🔍 验证交易: {tx_hash}")
        print(f"   网络: {self.network}")
        print(f"   期望金额: ${expected_amount} USDC")
        print(f"   期望接收地址: {expected_to}")
        
        # 1. 获取交易收据
        receipt = self.get_transaction_receipt(tx_hash)
        
        if not receipt:
            return False, "交易不存在或尚未确认", None
        
        # 2. 检查交易状态
        status = receipt.get("status")
        if status != "0x1":
            return False, "交易失败 (status != 1)", None
        
        print(f"   ✅ 交易状态: 成功")
        
        # 3. 解析 USDC 转账
        transfer_info = self.parse_usdc_transfer(receipt, expected_to)
        
        if not transfer_info:
            return False, "未找到 USDC 转账到指定地址", None
        
        print(f"   ✅ 找到 USDC 转账")
        print(f"      发送方: {transfer_info['from']}")
        print(f"      接收方: {transfer_info['to']}")
        print(f"      金额: ${transfer_info['amount']} USDC")
        
        # 4. 验证金额
        if transfer_info["amount"] < expected_amount:
            return False, f"金额不足: {transfer_info['amount']} < {expected_amount}", None
        
        print(f"   ✅ 金额验证通过")
        
        # 5. 计算确认数
        current_block = self.get_block_number()
        tx_block = int(receipt.get("blockNumber", "0x0"), 16)
        confirmations = current_block - tx_block
        
        print(f"   当前区块: {current_block}")
        print(f"   交易区块: {tx_block}")
        print(f"   确认数: {confirmations}")
        
        if confirmations < min_confirmations:
            return False, f"确认数不足: {confirmations} < {min_confirmations}", None
        
        print(f"   ✅ 确认数通过 (≥{min_confirmations})")
        
        # 构建交易信息
        tx_info = TransactionInfo(
            tx_hash=tx_hash,
            from_address=transfer_info["from"],
            to_address=transfer_info["to"],
            amount=transfer_info["amount"],
            token_contract=transfer_info["contract"],
            block_number=tx_block,
            confirmations=confirmations,
            status="success",
            timestamp=0  # 可以从区块获取
        )
        
        return True, "验证通过", tx_info


# ==================== BaseScan API 验证（备选方案）====================

class BaseScanVerifier:
    """使用 BaseScan API 验证（不需要 RPC 节点）"""
    
    def __init__(self, api_key: str, network: str = "mainnet"):
        """
        初始化
        
        Args:
            api_key: BaseScan API Key (从 https://basescan.org/myapikey 获取)
            network: "mainnet" 或 "sepolia"
        """
        self.api_key = api_key
        
        if network == "mainnet":
            self.base_url = "https://api.basescan.org/api"
            self.usdc_contract = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
        else:
            self.base_url = "https://api-sepolia.basescan.org/api"
            self.usdc_contract = "0x036CbD53842c5426634e7929541eC2318f3dCF7e"
    
    def get_transaction_receipt(self, tx_hash: str) -> Optional[Dict]:
        """通过 BaseScan API 获取交易收据"""
        url = f"{self.base_url}"
        params = {
            "module": "proxy",
            "action": "eth_getTransactionReceipt",
            "txhash": tx_hash,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if data.get("status") == "0":
                print(f"BaseScan 错误: {data.get('result')}")
                return None
            
            return data.get("result")
        except Exception as e:
            print(f"BaseScan API 调用失败: {e}")
            return None
    
    def get_internal_transactions(self, tx_hash: str) -> list:
        """获取内部交易（ERC20 转账）"""
        url = f"{self.base_url}"
        params = {
            "module": "account",
            "action": "tokentx",
            "txhash": tx_hash,
            "apikey": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            data = response.json()
            
            if data.get("status") != "1":
                return []
            
            return data.get("result", [])
        except Exception as e:
            print(f"BaseScan API 调用失败: {e}")
            return []
    
    def verify_payment(
        self, 
        tx_hash: str, 
        expected_amount: float, 
        expected_to: str
    ) -> Tuple[bool, str, Optional[Dict]]:
        """验证支付（使用 BaseScan）"""
        print(f"\n🔍 使用 BaseScan 验证交易: {tx_hash}")
        
        # 获取交易收据
        receipt = self.get_transaction_receipt(tx_hash)
        
        if not receipt:
            return False, "交易不存在", None
        
        if receipt.get("status") != "0x1":
            return False, "交易失败", None
        
        # 获取 ERC20 转账记录
        token_txs = self.get_internal_transactions(tx_hash)
        
        for tx in token_txs:
            # 检查是否是 USDC
            if tx.get("contractAddress", "").lower() != self.usdc_contract.lower():
                continue
            
            # 检查接收地址
            if tx.get("to", "").lower() != expected_to.lower():
                continue
            
            # 解析金额
            amount_raw = int(tx.get("value", "0"))
            amount = amount_raw / (10 ** int(tx.get("tokenDecimal", "6")))
            
            if amount >= expected_amount:
                return True, "验证通过", {
                    "from": tx.get("from"),
                    "to": tx.get("to"),
                    "amount": amount,
                    "token": tx.get("tokenSymbol"),
                }
        
        return False, "未找到匹配的 USDC 转账", None


# ==================== 集成到 x402_core ====================

def create_verifier(network: str = "mainnet", use_basescan: bool = False, api_key: str = None):
    """
    创建验证器工厂函数
    
    Args:
        network: "mainnet" 或 "sepolia"
        use_basescan: 是否使用 BaseScan API
        api_key: API Key (Alchemy/Infura/BaseScan)
    
    Returns:
        验证器实例
    """
    if use_basescan:
        if not api_key:
            raise ValueError("使用 BaseScan 需要提供 API Key")
        return BaseScanVerifier(api_key, network)
    
    return BaseChainVerifier(network, api_key)


# ==================== 测试 ====================

def test_verifier():
    """测试验证器"""
    print("\n" + "="*60)
    print("🔧 Base 链上验证测试")
    print("="*60)
    
    # 使用公共 RPC (主网)
    verifier = BaseChainVerifier(network="mainnet")
    
    # 测试：获取最新区块
    block = verifier.get_block_number()
    print(f"\n📦 最新区块号: {block}")
    
    # 测试：验证一个已知的 USDC 转账交易
    # 这是一个示例交易（需要替换为真实交易）
    test_tx = "0x1234567890abcdef..."  # 替换为真实交易哈希
    
    print(f"\n⚠️  要测试真实交易验证，请:")
    print(f"   1. 替换 test_tx 为真实的 Base 链 USDC 交易哈希")
    print(f"   2. 重新运行测试")
    
    print(f"\n✅ 验证器初始化成功")
    print(f"   RPC: {verifier.rpc_url}")
    print(f"   USDC: {verifier.config['usdc_contract']}")


if __name__ == "__main__":
    test_verifier()
