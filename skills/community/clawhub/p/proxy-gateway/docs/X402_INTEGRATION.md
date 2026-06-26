# x402 集成指南 - Proxy Gateway

## 概述

将 proxy-gateway 从 SkillPay 迁移到 x402 协议，实现：
- 更低的 gas 成本 (Polygon)
- 100% 收入归你
- 开放标准，无平台依赖

## 架构对比

### SkillPay (当前)
```
用户 → SkillPay API → 你收 95%
      (托管服务)
```

### x402 (目标)
```
用户 → x402 协议 → 链上结算 → 你收 100%
      (自托管 facilitator)
```

## 技术栈

- **协议**: x402 (Coinbase 标准)
- **网络**: Polygon (137) 或 Base (8453)
- **代币**: USDC
- **Python 库**: `x402`
- **Facilitator**: 自建或 https://x402.org/facilitator

## 安装依赖

```bash
pip install x402[fastapi,httpx,evm]
```

## 快速开始

### 1. 配置 Facilitator

```python
from x402 import x402ResourceServer
from x402.http import HTTPFacilitatorClient
from x402.mechanisms.evm.exact import ExactEvmServerScheme

# 使用公共 facilitator 或自建
facilitator = HTTPFacilitatorClient(url="https://x402.org/facilitator")

server = x402ResourceServer(facilitator)
server.register("eip155:*", ExactEvmServerScheme())
server.initialize()
```

### 2. 配置收费

```python
from x402 import ResourceConfig

config = ResourceConfig(
    scheme="exact",
    network="eip155:137",  # Polygon
    pay_to="0xYourWalletAddress",
    price="$0.001",  # 0.001 USDC
)

requirements = server.build_payment_requirements(config)
```

### 3. FastAPI 集成

```python
from fastapi import FastAPI, Request, HTTPException
from x402.http import x402_middleware

app = FastAPI()

# 添加 x402 中间件
app.add_middleware(
    x402_middleware,
    resource_server=server,
    protected_paths=["/api/v1/proxy"]
)

@app.post("/api/v1/proxy")
async def get_proxy(request: Request):
    # x402 中间件已自动验证支付
    # 这里直接返回代理
    return {"proxy": {...}}
```

## 完整集成代码

### payment_x402.py

```python
import os
from typing import Dict, Optional
from decimal import Decimal

from x402 import x402ResourceServer, ResourceConfig
from x402.http import HTTPFacilitatorClient
from x402.mechanisms.evm.exact import ExactEvmServerScheme

class X402PaymentManager:
    """
    x402 payment integration for proxy-gateway
    """
    
    # Network configurations
    NETWORKS = {
        'polygon': 'eip155:137',
        'base': 'eip155:8453',
        'ethereum': 'eip155:1',
    }
    
    # USDC contract addresses
    USDC_ADDRESSES = {
        'eip155:137': '0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174',  # Polygon
        'eip155:8453': '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',  # Base
    }
    
    def __init__(
        self,
        pay_to_address: str,
        network: str = 'polygon',
        facilitator_url: str = 'https://x402.org/facilitator'
    ):
        self.pay_to = pay_to_address
        self.network = self.NETWORKS.get(network, network)
        self.usdc_address = self.USDC_ADDRESSES.get(self.network)
        
        # Initialize x402
        self.facilitator = HTTPFacilitatorClient(url=facilitator_url)
        self.server = x402ResourceServer(self.facilitator)
        self.server.register("eip155:*", ExactEvmServerScheme())
        self.server.initialize()
        
        # Default config: 0.001 USDC per call
        self.default_config = ResourceConfig(
            scheme="exact",
            network=self.network,
            pay_to=self.pay_to,
            price="$0.001",
        )
    
    def get_payment_requirements(self) -> Dict:
        """Get payment requirements for client"""
        requirements = self.server.build_payment_requirements(self.default_config)
        return requirements[0].to_dict()
    
    async def verify_payment(self, payment_payload: str) -> bool:
        """
        Verify payment payload from client
        
        Args:
            payment_payload: Base64-encoded payment payload
            
        Returns:
            True if payment is valid
        """
        try:
            requirements = self.server.build_payment_requirements(self.default_config)
            result = await self.server.verify_payment(payment_payload, requirements[0])
            
            if result.is_valid:
                # Settle the payment
                settle_result = await self.server.settle_payment(payment_payload, requirements[0])
                return settle_result.success
            
            return False
        except Exception as e:
            print(f"Payment verification failed: {e}")
            return False
    
    def get_payment_url(self, user_address: str) -> str:
        """
        Generate payment URL for user
        
        In x402, users pay directly via their wallet
        """
        # Return a deeplink or web interface for payment
        return f"https://x402.org/pay?to={self.pay_to}&amount=0.001&network={self.network}"
    
    def get_deposit_instructions(self) -> Dict:
        """Instructions for user to deposit"""
        return {
            "network": self.network,
            "token": "USDC",
            "token_address": self.usdc_address,
            "pay_to": self.pay_to,
            "price_per_call": "0.001 USDC",
            "instructions": [
                "1. Ensure you have USDC on Polygon network",
                "2. Use any x402-compatible wallet",
                "3. Each API call will auto-deduct 0.001 USDC"
            ]
        }

# Singleton instance
_payment_manager = None

def get_payment_manager() -> X402PaymentManager:
    """Get or create payment manager instance"""
    global _payment_manager
    if _payment_manager is None:
        pay_to = os.getenv('X402_PAY_TO_ADDRESS')
        network = os.getenv('X402_NETWORK', 'polygon')
        
        if not pay_to:
            raise ValueError("X402_PAY_TO_ADDRESS environment variable required")
        
        _payment_manager = X402PaymentManager(
            pay_to_address=pay_to,
            network=network
        )
    
    return _payment_manager
```

## 网络选择建议

| 网络 | Gas 成本 | 速度 | 推荐度 |
|------|----------|------|--------|
| **Polygon** | ~$0.0001 | 2s | ⭐⭐⭐⭐⭐ 最佳 |
| **Base** | ~$0.001 | 2s | ⭐⭐⭐⭐ 备选 |
| **Ethereum** | ~$1+ | 12s | ⭐⭐ 太贵 |

**推荐**: Polygon (137) - 成本最低，生态成熟

## 成本对比

| 方案 | 单次成本 | 你的收入 | 月收入 (1万次) |
|------|----------|----------|----------------|
| SkillPay | $0.001 | $0.00095 | $9.50 |
| x402 Polygon | ~$0.0011 (含gas) | ~$0.0009 | $9.00 |
| x402 Base | ~$0.002 (含gas) | ~$0.0008 | $8.00 |

**结论**: x402 Polygon 略低于 SkillPay，但差距极小，且完全自主。

## 用户支付流程

### 1. 首次使用 (无余额)
```
用户 → 调用 API → 402 Payment Required
          ↓
    返回 requirements
          ↓
    用户用钱包签名支付
          ↓
    重试 API → 成功
```

### 2. 后续使用
```
用户 → 调用 API (带 payment header) → 自动扣款 → 成功
```

## 前端/客户端集成

用户可以使用任何 x402 客户端：

```javascript
// 使用 x402 fetch 客户端
import { x402Fetch } from '@x402/fetch';

const client = x402Fetch({
  wallet: myWallet,
  network: 'eip155:137' // Polygon
});

// 自动处理支付
const response = await client('https://your-gateway.com/api/v1/proxy', {
  method: 'POST',
  body: JSON.stringify({ region: 'us', duration: 300 })
});
```

## 迁移计划

### Phase 1: 并行运行 (1周)
- 保留 SkillPay
- 新增 x402 端点 `/api/v2/proxy`
- 对比两套系统

### Phase 2: 切换 (1周)
- 默认使用 x402
- SkillPay 作为备选
- 监控收入差异

### Phase 3: 完全迁移 (2周后)
- 停用 SkillPay
- 100% x402

## 部署步骤

1. **准备钱包**
   ```bash
   # 创建收款钱包
   export X402_PAY_TO_ADDRESS="0xYourPolygonAddress"
   export X402_NETWORK="polygon"
   ```

2. **安装依赖**
   ```bash
   pip install x402[fastapi,httpx,evm]
   ```

3. **更新代码**
   - 替换 `payment.py` 为 x402 版本
   - 更新 API 端点处理 payment headers

4. **测试**
   ```bash
   # 使用 x402 测试客户端
   python test_x402.py
   ```

5. **上线**
   ```bash
   docker-compose up -d
   ```

## 注意事项

1. **Gas 费**: 需要确保 facilitator 有少量 MATIC (Polygon gas)
2. **私钥安全**: 收款地址可以是普通地址，无需私钥
3. **网络稳定性**: Polygon 偶尔拥堵，备选 Base

## 参考文档

- x402 Python: https://github.com/coinbase/x402/tree/main/python
- x402 Specs: https://github.com/coinbase/x402/tree/main/specs
- Facilitator: https://x402.org/facilitator
