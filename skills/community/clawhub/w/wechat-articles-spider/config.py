# x402 Payment Configuration
# x402 支付配置

# 基础配置
NETWORK = "base"  # Base 链
USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"

# 收款地址（需要替换为实际地址）
RECEIVING_ADDRESS = "0x172444FC64e2E370fCcF297dB865831A1555b07A"

# 定价（USDC）
PRICING = {
    "per_article": 0.1,      # $0.1/篇
    "per_account": 10.0,     # $10/号
    "monthly": 100.0,        # $100/月
}

# 免费额度
FREE_TIER = {
    "articles": 10,          # 免费10篇
    "reset_period": None,    # 一次性，不重置
}

# 支付模式阈值（超过此金额使用异步支付）
ASYNC_THRESHOLD = 5.0  # $5

# 链上确认配置
CONFIRMATION_BLOCKS = 3  # 3个区块确认
CONFIRMATION_TIMEOUT = 300  # 5分钟超时

# 异步任务配置
QUEUE_CONFIG = {
    "max_retries": 3,
    "retry_delay": 60,  # 失败重试间隔（秒）
    "notification_channels": ["console", "webhook"],  # 通知方式
}

# Webhook 配置（飞书通知）
WEBHOOK_URL = ""  # 飞书 webhook URL
