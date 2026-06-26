"""
X402 Client SDK - 自动支付客户端
用户端 SDK，用于自动签名和支付
"""
import os
import json
from decimal import Decimal
from typing import Optional, Dict
from eth_account import Account
from web3 import Web3


class X402Client:
    """
    x402 支付客户端
    
    使用方法:
    ```python
    client = X402Client(private_key="0x...")
    payment_proof = await client.pay(
        amount="0.001",
        recipient="0x...",
        chain="base"
    )
    # 在请求头中发送 payment_proof
    ```
    """
    
    def __init__(self, private_key: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            private_key: EVM 私钥，如不提供则从环境变量 USER_EVM_PRIVATE_KEY 读取
        """
        self.private_key = private_key or os.getenv("USER_EVM_PRIVATE_KEY")
        if not self.private_key:
            raise ValueError(
                "Private key required. Provide directly or set USER_EVM_PRIVATE_KEY env var."
            )
        
        self.account = Account.from_key(self.private_key)
        self.address = self.account.address
    
    async def pay_from_402_response(
        self, 
        response_data: Dict,
        rpc_url: Optional[str] = None
    ) -> Dict:
        """
        根据 402 响应自动完成支付
        
        Args:
            response_data: 402 响应中的 x402 字段
            rpc_url: 可选，自定义 RPC 节点
            
        Returns:
            payment_proof: 支付凭证，可用于 X-Payment-Response 请求头
        """
        x402_data = response_data.get("x402", {})
        required = x402_data.get("required", {})
        
        amount = required.get("amount")
        recipient = required.get("recipient")
        token_contract = required.get("token_contract")
        network = x402_data.get("network", "base")
        
        if not all([amount, recipient]):
            raise ValueError("Invalid 402 response: missing required fields")
        
        return await self.pay(
            amount=amount,
            recipient=recipient,
            token_contract=token_contract,
            chain=network,
            rpc_url=rpc_url
        )
    
    async def pay(
        self,
        amount: str,
        recipient: str,
        token_contract: Optional[str] = None,
        chain: str = "base",
        rpc_url: Optional[str] = None
    ) -> Dict:
        """
        执行支付
        
        Args:
            amount: 支付金额（人类可读，如 "0.001"）
            recipient: 收款地址
            token_contract: USDC 合约地址（如为 None 则使用默认）
            chain: 链名称
            rpc_url: RPC 节点 URL
            
        Returns:
            {"tx_hash": "0x...", "amount": "0.001", ...}
        """
        # 这里简化实现，实际需要调用合约转账
        # 用户应使用 web3.py 或 x402 官方 SDK
        
        raise NotImplementedError(
            "Auto-pay implementation requires web3.py and contract interaction. "
            "Please implement based on your preferred method: "
            "1. Direct USDC transfer using web3.py\n"
            "2. x402 official SDK (if available)\n"
            "3. Manual payment through wallet UI"
        )
    
    def create_payment_header(self, tx_hash: str) -> str:
        """
        创建支付请求头
        
        Args:
            tx_hash: 交易哈希
            
        Returns:
            JSON 字符串，可直接放入 X-Payment-Response 请求头
        """
        return json.dumps({"tx_hash": tx_hash})


# Convenience function for quick integration
def create_x402_client() -> X402Client:
    """
    从环境变量创建客户端
    
    需要设置 USER_EVM_PRIVATE_KEY
    """
    return X402Client()
