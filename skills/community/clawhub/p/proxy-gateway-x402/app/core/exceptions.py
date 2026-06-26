"""
自定义异常类
"""


class ProxyGatewayException(Exception):
    """基础异常"""
    pass


class ValidationError(ProxyGatewayException):
    """输入验证错误"""
    def __init__(self, message: str = "Validation error"):
        self.message = message
        super().__init__(self.message)


class AuthenticationError(ProxyGatewayException):
    """认证错误"""
    def __init__(self, message: str = "Authentication required"):
        self.message = message
        super().__init__(self.message)


class FreeTrialExhaustedError(ProxyGatewayException):
    """免费试用次数已用完"""
    def __init__(self, limit: int = 10):
        self.limit = limit
        self.message = f"Free trial exhausted ({limit} calls)"
        super().__init__(self.message)


class InsufficientBalanceError(ProxyGatewayException):
    """余额不足"""
    def __init__(self, balance: float = 0.0, required: float = 0.001):
        self.balance = balance
        self.required = required
        self.message = f"Insufficient balance: {balance} USDC (required: {required})"
        super().__init__(self.message)


class InvalidUserIdError(ProxyGatewayException):
    """无效的用户ID"""
    def __init__(self, message: str = "Invalid user_id format"):
        self.message = message
        super().__init__(self.message)


class InvalidTxHashError(ProxyGatewayException):
    """无效的交易哈希"""
    def __init__(self, message: str = "Invalid transaction hash format"):
        self.message = message
        super().__init__(self.message)


class DepositAlreadyProcessedError(ProxyGatewayException):
    """充值已处理（重放攻击）"""
    def __init__(self, tx_hash: str):
        self.tx_hash = tx_hash
        self.message = f"Deposit already processed: {tx_hash}"
        super().__init__(self.message)


class ProxyNotAvailableError(ProxyGatewayException):
    """代理不可用"""
    def __init__(self, message: str = "No proxy available"):
        self.message = message
        super().__init__(self.message)


class TransactionFailedError(ProxyGatewayException):
    """交易失败"""
    def __init__(self, tx_hash: str, reason: str = ""):
        self.tx_hash = tx_hash
        self.reason = reason
        self.message = f"Transaction failed: {tx_hash} {reason}"
        super().__init__(self.message)
