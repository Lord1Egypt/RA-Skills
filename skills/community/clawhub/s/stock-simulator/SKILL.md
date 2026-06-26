---
name: stock-simulator
description: 模拟炒股技能。当用户想要模拟炒股、学习投资、记录股票交易、查看股票收益时使用此技能。支持A股、港股、美股市场，提供股票推荐、购买记录、收益计算等功能。
---

# 模拟炒股技能 (Stock Simulator)

## 概述

这是一个模拟炒股的技能，帮助用户在不投入真实资金的情况下体验股票投资。用户可以：
- 每天获取金融市场分析推荐
- 虚拟买入股票（按市场价格计算份额）
- 查看每日收益和累计收益
- 学习投资分析逻辑

## 前置要求

1. **Python 3.x** - 用于运行数据处理脚本
2. **网络环境** - 访问A股/港股/美股数据

## 数据存储（技能自动管理）

技能会自动在以下位置创建数据目录：
```
workspace/stock_data/{用户ID}/
├── config.json      # 账户配置（自动创建）
├── holdings.json    # 持仓数据（自动创建）
├── transactions.json # 交易记录（自动创建）
└── profits.json    # 收益数据（自动创建）
```

**用户无需手动创建这些目录**。

---

# ⚙️ 代理配置（仅当你的网络无法直接访问A股/港股/美股API时需要）

## 何时需要配置代理

- 如果你在中国大陆，且无法直接访问 Yahoo Finance、东方财富等API → 需要代理
- 如果你在海外或网络可以直接访问这些网站 → 无需配置

## 配置步骤

### 步骤1：创建脚本目录

在你的工作区内创建以下目录结构：
```
workspace/skills/stock-simulator/scripts/
```

### 步骤2：创建 get_market_data.py

在上述目录创建文件 `get_market_data.py`，复制以下代码：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""股票数据获取脚本"""

import json
import urllib.request
import sys
import os

# ====== 代理配置 ======
# 如果需要代理，取消注释以下两行并修改为你的代理地址
# PROXY = {'http': 'http://代理地址:端口', 'https': 'http://代理地址:端口'}
# ======================

def get_stock_data(stock_code, market='cn'):
    url = ""
    
    if market == 'cn':
        url = f"https://push2.eastmoney.com/api/qt/stock/get?secid=1.{stock_code}&fields=f2,f3,f4,f43,f44,f45,f57,f58"
    elif market == 'hk':
        url = f"https://qt.gtimg.cn/q=r_hk{stock_code}"
    elif market == 'us':
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock_code}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        # 只有配置了代理时才使用
        if 'PROXY' in dir():
            proxy_handler = urllib.request.ProxyHandler(PROXY)
            opener = urllib.request.build_opener(proxy_handler)
            response = opener.open(req, timeout=10)
        else:
            response = urllib.request.urlopen(req, timeout=10)
        
        data = json.loads(response.read().decode('utf-8'))
        
        # 解析返回数据（根据市场类型）
        if market == 'cn':
            data_obj = data.get('data', {})
            if data_obj:
                return {
                    'code': data_obj.get('f57'),
                    'name': data_obj.get('f58'),
                    'price': (data_obj.get('f43') or 0) / 100,
                    'change': (data_obj.get('f44') or 0) / 10000,
                    'change_percent': (data_obj.get('f45') or 0) / 10000,
                    'market': 'cn',
                    'source': 'eastmoney'
                }
        elif market == 'hk':
            import re
            text = str(data)
            match = re.search(r'="([^"]+)"', text)
            if match:
                parts = match.group(1).split('~')
                if len(parts) > 4:
                    return {
                        'code': parts[2],
                        'name': parts[1],
                        'price': float(parts[3]) if parts[3] else 0,
                        'change': float(parts[4]) - float(parts[3]) if parts[3] and parts[4] else 0,
                        'change_percent': 0,
                        'currency': 'HKD',
                        'market': 'hk',
                        'source': 'tencent'
                    }
        elif market == 'us':
            result = data.get('chart', {}).get('result', [])
            if result:
                meta = result[0].get('meta', {})
                price = meta.get('regularMarketPrice', 0)
                prev = meta.get('previousClose', price)
                return {
                    'code': stock_code,
                    'name': meta.get('shortName', stock_code),
                    'price': price,
                    'change': price - prev if price and prev else 0,
                    'change_percent': ((price - prev) / prev * 100) if prev and price else 0,
                    'currency': 'USD',
                    'market': 'us',
                    'source': 'yahoo'
                }
    except Exception as e:
        return {'error': str(e), 'code': stock_code, 'market': market}
    
    return {'error': 'No data', 'code': stock_code}

if __name__ == '__main__':
    if len(sys.argv) > 1:
        code = sys.argv[1]
        market = sys.argv[2] if len(sys.argv) > 2 else 'cn'
        print(json.dumps(get_stock_data(code, market), ensure_ascii=False, indent=2))
```

**关键点**：
- 代码使用 `if 'PROXY' in dir()` 判断是否配置了代理
- 如果你没有配置代理变量，脚本会直接访问（无代理）
- 如果你配置了代理变量，脚本会使用代理

### 步骤3：测试脚本

```bash
python workspace/skills/stock-simulator/scripts/get_market_data.py 600519 cn
python workspace/skills/stock-simulator/scripts/get_market_data.py 00700 hk
python workspace/skills/stock-simulator/scripts/get_market_data.py AAPL us
```

---

## 使用方法

### 交互方式

对AI说：
- "模拟炒股" - 开始使用技能
- 根据提示设置初始资金
- 选择操作：查看推荐、买入股票、查看收益

### 直接命令

```
模拟炒股，买入腾讯控股 10000元
模拟炒股，推荐股票
模拟炒股，我的收益
```

---

## 功能说明

### 1. 初始化账户
- 首次使用需设置初始资金（如10万元）
- 多用户/群聊数据自动隔离

### 2. 股票推荐
- 每日市场分析
- 推荐A股、港股、美股

### 3. 买入股票
- 输入金额（人民币）
- 自动按实时汇率转换
- 计算可购份额

### 4. 查看收益
- 多市场持仓展示
- 汇率转换显示人民币价值

---

## 股票代码格式

| 市场 | 代码格式 | 示例 |
|------|----------|------|
| A股 | 6位数字 | 600519, 000001 |
| 港股 | 5位数字 | 00700, 09988 |
| 美股 | 字母 | AAPL, GOOGL, NVDA |

---

## 数据来源

- A股：东方财富 (eastmoney.com)
- 港股：腾讯财经 (gtimg.cn)  
- 美股：Yahoo Finance
- 汇率：Yahoo Finance

---

## 注意事项

1. **虚拟交易**：不涉及真实资金
2. **数据延迟**：免费API可能有延迟
3. **投资风险**：仅供学习参考

---

**版本**: 1.0.0
