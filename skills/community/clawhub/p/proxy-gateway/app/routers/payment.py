"""
支付路由
"""

from typing import Optional
from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.exceptions import (
    InvalidUserIdError,
    InvalidTxHashError,
    DepositAlreadyProcessedError,
    TransactionFailedError,
)
from app.core.security import validate_user_id
from app.managers.factory import get_payment_manager

router = APIRouter()
payment_manager = get_payment_manager()


class DepositConfirmRequest(BaseModel):
    """充值确认请求"""
    user_id: str
    tx_hash: str


@router.get("/deposit-info")
async def get_deposit_info(user_id: Optional[str] = None):
    """
    获取充值信息
    
    - 无 user_id: 返回充值说明页面
    - 有 user_id: 返回 JSON 数据
    """
    if not user_id:
        # 返回 HTML 页面
        from fastapi.responses import HTMLResponse
        return HTMLResponse(content=DEPOSIT_UI_HTML)
    
    if not validate_user_id(user_id):
        raise HTTPException(status_code=400, detail="Invalid user_id format")
    
    return payment_manager.get_deposit_address(user_id)


@router.post("/confirm-deposit")
async def confirm_deposit(request: DepositConfirmRequest):
    """
    确认充值
    
    用户提交交易哈希，平台确认后更新余额
    """
    try:
        result = await payment_manager.confirm_deposit(request.user_id, request.tx_hash)
        return result
    except InvalidUserIdError:
        raise HTTPException(status_code=400, detail="Invalid user_id format")
    except InvalidTxHashError:
        raise HTTPException(status_code=400, detail="Invalid transaction hash format")
    except DepositAlreadyProcessedError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except TransactionFailedError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/balance")
async def get_balance(user_id: str = Query(..., description="User ID")):
    """
    查询余额
    """
    if not validate_user_id(user_id):
        raise HTTPException(status_code=400, detail="Invalid user_id format")
    
    balance = payment_manager.get_balance(user_id)
    history = payment_manager.get_transaction_history(user_id, limit=5)
    
    return {
        "user_id": user_id,
        "balance": float(balance),
        "currency": "USDC",
        "network": get_settings().NETWORK,
        "recent_transactions": history
    }


@router.post("/reset-test-balance")
async def reset_test_balance(
    user_id: str,
    amount: float = 100.0,
    authorization: Optional[str] = Header(None)
):
    """
    重置测试余额（仅测试网可用）
    
    需要 Admin Token 授权
    """
    settings = get_settings()
    
    # 仅在测试网可用
    if not settings.is_testnet:
        raise HTTPException(
            status_code=403,
            detail="This endpoint is only available in testnet mode"
        )
    
    # 验证 user_id
    if not validate_user_id(user_id):
        raise HTTPException(status_code=400, detail="Invalid user_id format")
    
    # 验证 Admin Token
    if not settings.ADMIN_TOKEN:
        raise HTTPException(
            status_code=500,
            detail="ADMIN_TOKEN not configured"
        )
    
    if authorization != f"Bearer {settings.ADMIN_TOKEN}":
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    # 执行重置
    from app.managers.testnet_payment import TestnetPaymentManager
    
    if isinstance(payment_manager, TestnetPaymentManager):
        from decimal import Decimal
        result = payment_manager.reset_test_balance(user_id, Decimal(str(amount)))
        
        return {
            "success": True,
            "message": result,
            "new_balance": float(payment_manager.get_balance(user_id))
        }
    else:
        raise HTTPException(status_code=500, detail="Payment manager type mismatch")


# 充值页面 HTML 模板
DEPOSIT_UI_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proxy Gateway - 充值</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            max-width: 500px;
            width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 10px;
            font-size: 28px;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        input[type="text"] {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }
        .btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }
        .info-box {
            background: #f5f5f5;
            border-radius: 10px;
            padding: 20px;
            margin-top: 20px;
        }
        .info-box h3 {
            color: #333;
            margin-bottom: 10px;
        }
        .info-box p {
            color: #666;
            line-height: 1.6;
            margin-bottom: 8px;
        }
        .price-tag {
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
        }
        .steps {
            margin-top: 20px;
        }
        .step {
            display: flex;
            align-items: flex-start;
            margin-bottom: 15px;
        }
        .step-number {
            background: #667eea;
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            margin-right: 12px;
            flex-shrink: 0;
        }
        .step-content {
            flex: 1;
        }
        .step-title {
            font-weight: 600;
            color: #333;
            margin-bottom: 4px;
        }
        .step-desc {
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Proxy Gateway</h1>
        <p class="subtitle">AI Agent 外网访问服务</p>
        
        <div class="info-box">
            <h3>💰 价格说明</h3>
            <p><span class="price-tag">0.001 USDC</span> / 请求</p>
            <p>🎁 新用户免费试用 10 次</p>
            <p>🔗 网络: Polygon</p>
            <p>💳 支付方式: USDC</p>
        </div>
        
        <div class="steps">
            <h3 style="margin-bottom: 15px;">充值步骤</h3>
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <div class="step-title">输入用户ID</div>
                    <div class="step-desc">填写您的用户标识（字母、数字、下划线、横线）</div>
                </div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <div class="step-title">获取充值地址</div>
                    <div class="step-desc">系统将生成您的专属充值地址</div>
                </div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <div class="step-title">转账 USDC</div>
                    <div class="step-desc">从您的钱包转账 USDC 到平台地址，务必备注您的用户ID</div>
                </div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <div class="step-title">确认到账</div>
                    <div class="step-desc">提交交易哈希确认充值，余额将自动到账</div>
                </div>
            </div>
        </div>
        
        <form id="depositForm" style="margin-top: 30px;">
            <div class="form-group">
                <label for="userId">用户 ID</label>
                <input type="text" id="userId" name="user_id" placeholder="例如: my_agent_001" required>
            </div>
            <button type="submit" class="btn">获取充值地址</button>
        </form>
        
        <div id="result" style="margin-top: 20px;"></div>
    </div>
    
    <script>
        document.getElementById('depositForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            const userId = document.getElementById('userId').value;
            const resultDiv = document.getElementById('result');
            
            try {
                const response = await fetch(`/deposit-info?user_id=${encodeURIComponent(userId)}`);
                const data = await response.json();
                
                resultDiv.innerHTML = `
                    <div class="info-box" style="background: #e8f5e9; border: 2px solid #4caf50;">
                        <h3>✅ 充值信息</h3>
                        <p><strong>充值地址:</strong></p>
                        <p style="background: white; padding: 10px; border-radius: 5px; font-family: monospace; word-break: break-all;">${data.address}</p>
                        <p><strong>网络:</strong> ${data.network}</p>
                        <p><strong>Token:</strong> ${data.token}</p>
                        <p><strong>备注 (Memo):</strong> <span style="color: #f44336; font-weight: bold;">${data.memo}</span></p>
                        <hr style="margin: 15px 0; border: none; border-top: 1px solid #ddd;">
                        <p style="color: #f44336; font-weight: bold;">⚠️ 重要：转账时务必备注您的用户ID: ${data.memo}</p>
                    </div>
                `;
            } catch (error) {
                resultDiv.innerHTML = `
                    <div class="info-box" style="background: #ffebee; border: 2px solid #f44336;">
                        <p style="color: #f44336;">❌ 错误: ${error.message}</p>
                    </div>
                `;
            }
        });
    </script>
</body>
</html>"""
