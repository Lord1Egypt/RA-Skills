"""
x402 Payment Middleware - Agent-to-Agent Commerce
按次实时支付，无需托管用户资金
"""
import os
import json
import asyncio
from decimal import Decimal
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from fastapi import Request, HTTPException, Header
from eth_account import Account
from eth_account.messages import encode_defunct
import httpx
from web3 import Web3
import logging

from app.core.config import get_settings

logger = logging.getLogger(__name__)

# x402 Protocol Constants
X402_VERSION = "0.1.0"
X402_PAYMENT_HEADER = "X-Payment-Response"
X402_REQUIRED_HEADER = "X-Payment-Required"

# Default Configuration
DEFAULT_PRICE = Decimal("0.001")  # 0.001 USDC per request
USDC_DECIMALS = 6
USDC_CONTRACTS = {
    "base": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "base-sepolia": "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
    "polygon": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
}

ERC20_TRANSFER_ABI = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]


class X402PaymentRequired(Exception):
    """402 Payment Required"""
    def __init__(self, payment_details: Dict):
        self.payment_details = payment_details
        super().__init__("Payment Required")


class X402PaymentMiddleware:
    """
    x402 Payment Middleware
    
    Flow:
    1. User makes request without payment header → 402 response with payment requirements
    2. User signs and pays on-chain
    3. User includes payment proof in X-Payment-Response header
    4. Middleware verifies payment and allows request
    """
    
    def __init__(self):
        settings = get_settings()
        self.developer_wallet = settings.DEVELOPER_WALLET
        self.price = Decimal(str(settings.COST_PER_REQUEST))
        self.chain = settings.X402_CHAIN
        self.rpc_url = settings.RPC_URL
        
        if not self.developer_wallet:
            raise ValueError("DEVELOPER_WALLET environment variable is required")
        
        self.w3 = Web3(Web3.HTTPProvider(self.rpc_url))
        self.usdc_contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(
                USDC_CONTRACTS.get(self.chain, USDC_CONTRACTS["base"])
            ),
            abi=ERC20_TRANSFER_ABI
        )
        
        # Cache for verified payments (tx_hash -> timestamp)
        self._verified_payments: Dict[str, datetime] = {}
        self._payment_cache_ttl = timedelta(minutes=5)
    
    async def verify_payment(self, request: Request) -> Dict[str, Any]:
        """
        Main entry point: verify payment or return 402
        
        Returns payment info if valid, raises X402PaymentRequired otherwise
        """
        payment_header = request.headers.get(X402_PAYMENT_HEADER)
        
        if payment_header:
            # User provided payment proof
            try:
                payment_data = json.loads(payment_header)
                return await self._verify_payment_proof(payment_data)
            except json.JSONDecodeError:
                logger.warning("Invalid payment header format")
                raise self._create_402_response()
        
        # No payment provided - request payment
        logger.info(f"Payment required for {request.url.path}")
        raise self._create_402_response()
    
    def _create_402_response(self) -> X402PaymentRequired:
        """Create 402 Payment Required response"""
        payment_request = {
            "x402": {
                "version": X402_VERSION,
                "scheme": "exact",
                "network": self.chain,
                "required": {
                    "amount": str(self.price),
                    "token": "USDC",
                    "token_contract": self.usdc_contract.address,
                    "recipient": self.developer_wallet
                },
                "instructions": {
                    "manual": f"Send {self.price} USDC to {self.developer_wallet}",
                    "auto": "Set USER_EVM_PRIVATE_KEY environment variable for auto-pay"
                }
            }
        }
        raise X402PaymentRequired(payment_request)
    
    async def _verify_payment_proof(self, payment_data: Dict) -> Dict[str, Any]:
        """Verify payment transaction on-chain"""
        tx_hash = payment_data.get("tx_hash")
        if not tx_hash:
            logger.warning("Missing tx_hash in payment proof")
            raise self._create_402_response()
        
        # Check cache
        if self._is_cached_payment(tx_hash):
            logger.debug(f"Payment {tx_hash} found in cache")
            return {"verified": True, "tx_hash": tx_hash, "cached": True}
        
        try:
            # Verify transaction on-chain
            receipt = await self._get_transaction_receipt(tx_hash)
            
            if not receipt or receipt["status"] != 1:
                logger.warning(f"Transaction {tx_hash} failed or not found")
                raise self._create_402_response()
            
            # Verify payment details
            if not self._validate_payment_transaction(receipt):
                logger.warning(f"Transaction {tx_hash} does not match required payment")
                raise self._create_402_response()
            
            # Cache successful payment
            self._cache_payment(tx_hash)
            
            logger.info(f"Payment verified: {tx_hash}")
            return {
                "verified": True,
                "tx_hash": tx_hash,
                "amount": str(self.price),
                "recipient": self.developer_wallet
            }
            
        except Exception as e:
            logger.error(f"Payment verification failed: {e}")
            raise self._create_402_response()
    
    async def _get_transaction_receipt(self, tx_hash: str) -> Optional[Dict]:
        """Fetch transaction receipt from chain"""
        try:
            receipt = self.w3.eth.get_transaction_receipt(tx_hash)
            return receipt
        except Exception as e:
            logger.error(f"Failed to get receipt for {tx_hash}: {e}")
            return None
    
    def _validate_payment_transaction(self, receipt: Dict) -> bool:
        """Validate that the transaction matches our requirements"""
        # Check recipient
        if receipt.get("to", "").lower() != self.usdc_contract.address.lower():
            return False
        
        # Additional validation could check:
        # - Transfer amount
        # - Recipient address in event logs
        # - Token contract
        
        return True
    
    def _is_cached_payment(self, tx_hash: str) -> bool:
        """Check if payment is in cache and not expired"""
        if tx_hash in self._verified_payments:
            cached_time = self._verified_payments[tx_hash]
            if datetime.now() - cached_time < self._payment_cache_ttl:
                return True
            # Expired, remove from cache
            del self._verified_payments[tx_hash]
        return False
    
    def _cache_payment(self, tx_hash: str):
        """Cache verified payment"""
        self._verified_payments[tx_hash] = datetime.now()
        
        # Cleanup old entries
        cutoff = datetime.now() - self._payment_cache_ttl
        expired = [
            tx for tx, ts in self._verified_payments.items() 
            if ts < cutoff
        ]
        for tx in expired:
            del self._verified_payments[tx]
    
    async def auto_pay(
        self, 
        user_private_key: str,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Auto-pay using user's private key
        
        Returns payment proof that can be used in X-Payment-Response header
        """
        try:
            account = Account.from_key(user_private_key)
            user_address = account.address
            
            logger.info(f"Auto-pay initiated from {user_address}")
            
            # Build USDC transfer transaction
            amount_wei = int(self.price * (10 ** USDC_DECIMALS))
            
            tx = self.usdc_contract.functions.transfer(
                Web3.to_checksum_address(self.developer_wallet),
                amount_wei
            ).build_transaction({
                'from': user_address,
                'nonce': self.w3.eth.get_transaction_count(user_address),
                'gas': 100000,
                'gasPrice': self.w3.eth.gas_price,
                'chainId': self.w3.eth.chain_id
            })
            
            # Sign transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, user_private_key)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            tx_hash_hex = tx_hash.hex()
            
            logger.info(f"Transaction sent: {tx_hash_hex}")
            
            # Wait for confirmation
            receipt = await self._wait_for_confirmation(tx_hash_hex, max_retries)
            
            if receipt and receipt["status"] == 1:
                return {
                    "tx_hash": tx_hash_hex,
                    "amount": str(self.price),
                    "token": "USDC",
                    "network": self.chain
                }
            else:
                raise Exception("Transaction failed")
                
        except Exception as e:
            logger.error(f"Auto-pay failed: {e}")
            raise
    
    async def _wait_for_confirmation(
        self, 
        tx_hash: str, 
        max_retries: int = 30,
        delay: float = 2.0
    ) -> Optional[Dict]:
        """Wait for transaction confirmation"""
        for i in range(max_retries):
            try:
                receipt = self.w3.eth.get_transaction_receipt(tx_hash)
                if receipt:
                    return receipt
            except Exception:
                pass
            
            await asyncio.sleep(delay)
        
        logger.error(f"Transaction {tx_hash} confirmation timeout")
        return None


# FastAPI dependency
async def require_x402_payment(request: Request):
    """Dependency for routes requiring payment"""
    middleware = X402PaymentMiddleware()
    return await middleware.verify_payment(request)
