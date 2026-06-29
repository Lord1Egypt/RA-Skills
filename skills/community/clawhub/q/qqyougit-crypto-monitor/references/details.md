# 加密货币监控与告警 - 详细内容

## 一、Binance API 完整调用

### 1.1 获取实时价格
```python
import requests

def get_binance_price(symbol="BTCUSDT"):
    """获取Binance实时价格"""
    url = f"https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": symbol}
    response = requests.get(url, params=params)
    data = response.json()
    return {
        "symbol": data["symbol"],
        "price": float(data["price"]),
        "time": data["time"]
    }

# 使用示例
btc_price = get_binance_price("BTCUSDT")
print(f"BTC价格: ${btc_price['price']:,.2f}")
```

### 1.2 获取K线数据（用于技术分析）
```python
def get_klines(symbol="BTCUSDT", interval="1h", limit=100):
    """获取K线数据"""
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    klines = response.json()
    
    # 解析K线数据
    data = []
    for k in klines:
        data.append({
            "open_time": k[0],
            "open": float(k[1]),
            "high": float(k[2]),
            "low": float(k[3]),
            "close": float(k[4]),
            "volume": float(k[5]),
            "close_time": k[6]
        })
    return data
```

### 1.3 获取24小时涨跌
```python
def get_24h_ticker(symbol="BTCUSDT"):
    """获取24小时价格变动"""
    url = "https://api.binance.com/api/v3/ticker/24hr"
    params = {"symbol": symbol}
    response = requests.get(url, params=params)
    data = response.json()
    return {
        "symbol": data["symbol"],
        "price_change": float(data["priceChange"]),
        "price_change_percent": float(data["priceChangePercent"]),
        "weighted_avg_price": float(data["weightedAvgPrice"]),
        "prev_close_price": float(data["prevClosePrice"]),
        "last_price": float(data["lastPrice"]),
        "high_price": float(data["highPrice"]),
        "low_price": float(data["lowPrice"]),
        "volume": float(data["volume"]),
        "quote_volume": float(data["quoteVolume"])
    }
```

### 1.4 获取历史订单簿深度
```python
def get_order_book(symbol="BTCUSDT", limit=20):
    """获取订单簿"""
    url = "https://api.binance.com/api/v3/depth"
    params = {"symbol": symbol, "limit": limit}
    response = requests.get(url, params=params)
    data = response.json()
    return {
        "bids": [(float(p), float(q)) for p, q in data["bids"]],
        "asks": [(float(p), float(q)) for p, q in data["asks"]]
    }
```

## 二、CoinGecko API 完整调用

### 2.1 获取代币详情
```python
def get_coingecko_coin(symbol="bitcoin"):
    """通过符号查找CoinGecko ID"""
    url = "https://api.coingecko.com/api/v3/coins/list"
    response = requests.get(url)
    coins = response.json()
    
    # 符号转小写匹配
    symbol_lower = symbol.lower()
    for coin in coins:
        if coin["symbol"].lower() == symbol_lower:
            return coin
    return None

def get_coingecko_price(coin_ids, vs_currencies="usd"):
    """获取价格"""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": ",".join(coin_ids),
        "vs_currencies": vs_currencies,
        "include_24hr_change": "true",
        "include_market_cap": "true"
    }
    response = requests.get(url, params=params)
    return response.json()
```

### 2.2 获取市场数据
```python
def get_coingecko_markets(per_page=100, page=1):
    """获取全球市场数据"""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "sparkline": "false"
    }
    response = requests.get(url, params=params)
    return response.json()
```

## 三、CoinCap API 完整调用

### 3.1 获取资产数据
```python
def get_coincap_assets(limit=100):
    """获取资产列表"""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    # CoinCap API
    # url = "https://api.coincap.io/v2/assets"
    # params = {"limit": limit}
    # response = requests.get(url, params=params)
    # return response.json()["data"]
    pass

def get_coincap_price(asset_id="bitcoin"):
    """获取单个资产价格"""
    url = f"https://api.coincap.io/v2/assets/{asset_id}"
    response = requests.get(url)
    data = response.json()["data"]
    return {
        "id": data["id"],
        "symbol": data["symbol"],
        "price_usd": float(data["priceUsd"]),
        "change_percent_24hr": float(data["changePercent24Hr"])
    }
```

## 四、告警系统完整实现

### 4.1 告警规则引擎
```python
import json
from datetime import datetime, timedelta
from enum import Enum

class AlertCondition(Enum):
    ABOVE = "above"      # 价格突破
    BELOW = "below"      # 价格跌破
    CHANGE_UP = "change_up"    # 涨幅超限
    CHANGE_DOWN = "change_down"  # 跌幅超限
    CROSS = "cross"       # 均线穿越

class PriceAlert:
    def __init__(self, alert_id, coin, condition, target, 
                 current_price, interval=300, created_at=None):
        self.alert_id = alert_id
        self.coin = coin
        self.condition = AlertCondition(condition)
        self.target = float(target)
        self.current_price = float(current_price)
        self.interval = interval  # 秒
        self.created_at = created_at or datetime.now()
        self.triggered = False
        self.triggered_at = None
    
    def check(self, new_price):
        """检查是否触发告警"""
        new_price = float(new_price)
        
        if self.condition == AlertCondition.ABOVE:
            triggered = new_price >= self.target
        elif self.condition == AlertCondition.BELOW:
            triggered = new_price <= self.target
        elif self.condition == AlertCondition.CHANGE_UP:
            pct_change = (new_price - self.current_price) / self.current_price * 100
            triggered = pct_change >= self.target
        elif self.condition == AlertCondition.CHANGE_DOWN:
            pct_change = (new_price - self.current_price) / self.current_price * 100
            triggered = pct_change <= -self.target
        
        if triggered:
            self.triggered = True
            self.triggered_at = datetime.now()
        
        return triggered, new_price

    def to_dict(self):
        return {
            "alert_id": self.alert_id,
            "coin": self.coin,
            "condition": self.condition.value,
            "target": self.target,
            "current_price": self.current_price,
            "interval": self.interval,
            "created_at": self.created_at.isoformat(),
            "status": "triggered" if self.triggered else "active"
        }
```

### 4.2 告警存储管理器
```python
import uuid
import os
from datetime import datetime

class AlertManager:
    def __init__(self, storage_path="./alerts.json"):
        self.storage_path = storage_path
        self.alerts = self._load()
    
    def _load(self):
        """加载告警列表"""
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                return [self._dict_to_alert(a) for a in data]
        return []
    
    def _save(self):
        """保存告警列表"""
        with open(self.storage_path, 'w') as f:
            json.dump([a.to_dict() for a in self.alerts], f, indent=2)
    
    def _dict_to_alert(self, d):
        alert = PriceAlert(
            alert_id=d["alert_id"],
            coin=d["coin"],
            condition=d["condition"],
            target=d["target"],
            current_price=d["current_price"],
            interval=d.get("interval", 300),
            created_at=datetime.fromisoformat(d["created_at"])
        )
        if d.get("triggered"):
            alert.triggered = True
            alert.triggered_at = datetime.fromisoformat(d["triggered_at"])
        return alert
    
    def create_alert(self, coin, condition, target, current_price, interval=300):
        """创建新告警"""
        alert_id = str(uuid.uuid4())[:8]
        alert = PriceAlert(alert_id, coin, condition, target, 
                          current_price, interval)
        self.alerts.append(alert)
        self._save()
        return alert
    
    def get_active_alerts(self):
        """获取活跃告警"""
        return [a for a in self.alerts if not a.triggered]
    
    def delete_alert(self, alert_id):
        """删除告警"""
        self.alerts = [a for a in self.alerts if a.alert_id != alert_id]
        self._save()
```

### 4.3 监控循环实现
```python
import time
import logging

class CryptoMonitor:
    def __init__(self, alert_manager, price_func):
        self.alert_manager = alert_manager
        self.get_price = price_func
        self.logger = logging.getLogger(__name__)
    
    def start_monitoring(self, check_interval=60):
        """启动监控循环"""
        self.logger.info("开始加密货币监控...")
        
        while True:
            try:
                active_alerts = self.alert_manager.get_active_alerts()
                
                for alert in active_alerts:
                    current_price = self.get_price(alert.coin)
                    triggered, new_price = alert.check(current_price)
                    
                    if triggered:
                        self._send_notification(alert, new_price)
                        self.alert_manager._save()
                
                time.sleep(check_interval)
                
            except Exception as e:
                self.logger.error(f"监控异常: {e}")
                time.sleep(check_interval * 2)
    
    def _send_notification(self, alert, current_price):
        """发送告警通知"""
        change_pct = (current_price - alert.current_price) / alert.current_price * 100
        
        message = f"""
🪙 币种：{alert.coin}
💰 触发价格：${current_price:,.2f}
📊 变化幅度：{change_pct:+.2f}%
⏰ 触发时间：{alert.triggered_at.strftime('%Y-%m-%d %H:%M:%S')}
🎯 告警条件：{alert.condition.value.upper()} ${alert.target:,.2f}
"""
        print(message)
        # 实际使用时调用飞书/微信/Telegram API推送
        return message
```

## 五、行情报告生成器

### 5.1 完整日报模板
```python
def generate_daily_report(market_data):
    """生成每日行情报告"""
    report = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 加密货币每日行情报告
📅 {datetime.now().strftime('%Y-%m-%d')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 📈 市场概览

**总市值**: ${market_data.get('total_market_cap', 0):,.0f}
**24h交易量**: ${market_data.get('total_volume', 0):,.0f}
**BTC主导**: {market_data.get('btc_dominance', 0):.1f}%

## 🪙 主流币行情

| 币种 | 价格 | 24h涨跌 | 7d涨跌 |
|------|------|---------|--------|
"""
    
    for coin in market_data.get('coins', []):
        change_24h = coin.get('change_24h', 0)
        emoji = "📈" if change_24h >= 0 else "📉"
        sign = "+" if change_24h >= 0 else ""
        report += f"| {coin['name']} | ${coin['price']:,.2f} | {emoji} {sign}{change_24h:.2f}% | {sign}{coin.get('change_7d', 0):.2f}% |\n"
    
    report += f"""
## 🔥 市场情绪

| 指标 | 数值 | 解读 |
|------|------|------|
| 恐惧贪婪指数 | {market_data.get('fear_greed', 50)}/100 | {market_data.get('fear_greed_text', '中立')} |
| 多空比 | {market_data.get('long_short_ratio', 1.0)} | {'偏多' if market_data.get('long_short_ratio', 1) > 1 else '偏空'} |
| 合约持仓量 | ${market_data.get('open_interest', 0):,.0f} | {'高' if market_data.get('open_interest', 0) > 10000000000 else '正常'} |

## 💡 操作建议

{market_data.get('analysis', '市场分析生成中...')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 本报告仅供参考，不构成投资建议
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    return report
```

### 5.2 技术指标计算
```python
def calculate_sma(prices, period):
    """简单移动平均"""
    return sum(prices[-period:]) / period

def calculate_ema(prices, period):
    """指数移动平均"""
    multiplier = 2 / (period + 1)
    ema = prices[0]
    for price in prices[1:]:
        ema = (price - ema) * multiplier + ema
    return ema

def calculate_rsi(prices, period=14):
    """RSI相对强弱指数"""
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change >= 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def calculate_macd(prices, fast=12, slow=26, signal=9):
    """MACD指标"""
    ema_fast = calculate_ema(prices, fast)
    ema_slow = calculate_ema(prices, slow)
    macd_line = ema_fast - ema_slow
    # Signal线需要历史EMA计算，此处简化
    return macd_line, macd_line * 0.9, macd_line * 0.1
```

## 六、常用币种代码对照表

| 币种 | Binance | CoinGecko ID | Symbol |
|------|---------|--------------|--------|
| 比特币 | BTCUSDT | bitcoin | BTC |
| 以太坊 | ETHUSDT | ethereum | ETH |
| 索拉纳 | SOLUSDT | solana | SOL |
| 狗狗币 | DOGEUSDT | dogecoin | DOGE |
| 柴犬币 | SHIBUSDT | shiba-inu | SHIB |
| XRP | XRPUSDT | ripple | XRP |
| ADA | ADAUSDT | cardano | ADA |
| DOT | DOTUSDT | polkadot | DOT |
| AVAX | AVAXUSDT | avalanche-2 | AVAX |
| MATIC | MATICUSDT | polygon | MATIC |

## 七、常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| API返回空 | 符号格式错误 | 使用大写，如"BTCUSDT" |
| 频率限制 | 请求过快 | 添加延迟，使用缓存 |
| 价格异常 | 交易所差异 | 多个数据源交叉验证 |
| 连接超时 | 网络问题 | 增加超时时间，重试机制 |
| 告警不触发 | 条件设置错误 | 检查条件类型和目标价格 |

## 八、风险提示模板

```python
RISK_DISCLAIMER = """
⚠️ 风险提示：
1. 加密货币市场24/7运行，波动剧烈
2. 杠杆交易风险极高，可能损失全部本金
3. 历史上类似情况不代表未来走势
4. 请根据自身风险承受能力理性投资
5. 本工具仅供参考，不构成投资建议
6.DYOR (Do Your Own Research) - 做好自己的研究
"""
```

## 九、Meme币监控特殊处理

### 9.1 Meme币特点
- 流动性低，价格波动大
- 容易被大户操控
- 社交媒体情绪影响大
- 缺乏基本面支撑

### 9.2 Meme币监控要点
```python
MEMECOIN_ALERT_TEMPLATE = {
    "volume_threshold": 1000000,  # 24h成交量阈值（USDT）
    "price_change_threshold": 50,  # 单小时涨跌幅阈值（%）
    "social_mentions_increase": 200,  # 社交媒体提及增量（%）
    "whale_wallet_threshold": 10000000  # 大户钱包门槛（代币数量）
}
```

### 9.3Rug Pull检测
```python
def detect_rug_pull_indicators(coin_data):
    """检测Rug Pull指标"""
    indicators = []
    
    # 1. 流动性突然移除
    if coin_data.get('liquidity_change_24h') < -50:
        indicators.append("⚠️ 流动性24h内下降超过50%")
    
    # 2. 大户持仓集中度
    if coin_data.get('top_10_holders_pct') > 80:
        indicators.append("⚠️ 前10地址持仓超过80%")
    
    # 3. 合约未验证
    if not coin_data.get('contract_verified'):
        indicators.append("⚠️ 合约未通过审计验证")
    
    # 4. Ownership renounced
    if not coin_data.get('ownership_renounced'):
        indicators.append("⚠️ 所有权未放弃，开发者可修改合约")
    
    return indicators
```
