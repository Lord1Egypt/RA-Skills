---
name: tencent-finance
description: 腾讯财经实时行情接口，查询A股、港股、美股、期货、外汇、ETF的实时行情数据。触发关键词：查股价、查行情、查指数、腾讯接口、股票报价、实时行情
---

# 腾讯财经行情接口（Tencent Finance API）

## 接口信息

**Base URL：** `https://qt.gtimg.cn/q=代码`

**特点：**
- 毫秒级响应，无需注册，即插即用
- 支持 A股、港股、美股、期货、外汇、ETF
- 查询频率建议间隔 100ms 以上，避免封 IP

---

## 代码规则

### A 股

| 前缀 | 市场 | 示例 |
|------|------|------|
| `sh` | 上交所 | `sh000001`（上证指数）、`sh600519`（茅台） |
| `sz` | 深交所 | `sz399001`（深证成指）、`sz000858`（五粮液） |

### 港 股

| 前缀 | 市场 | 示例 |
|------|------|------|
| `hk` | 港交所 | `hkHSI`（恒生指数）、`hkHSTECH`（恒生科技） |
| `hk` | 港交所个股 | `hk00700`（腾讯）、`hk09988`（阿里） |

### 美 股（指数）

| 代码 | 名称 |
|------|------|
| `usNDX` | 纳斯达克 100 |
| `usSPX` | 标普 500 |
| `usDJI` | 道琼斯 |

### 大宗商品

| 代码 | 名称 |
|------|------|
| `hf_GC` | 黄金（COMEX） |
| `hf_CL` | WTI 原油 |
| `hf_SI` | 白银 |

### 外汇

| 代码 | 名称 |
|------|------|
| `fx_usr` | 美元/人民币（USD/CNY） |

---

## 数据字段说明

返回字段以 `~` 分隔，关键字段索引：

| 索引 | 含义 |
|------|------|
| `[3]` | 当前价格 |
| `[4]` | 昨收价格 |
| `[5]` | 今开价格 |
| `[31]` | 涨跌额 |
| `[32]` | 涨跌幅（%） |
| `[33]` | 最高价 |
| `[34]` | 最低价 |
| `[36]` | 成交量（手） |
| `[37]` | 成交额（万元） |
| `[38]` | 换手率（%） |
| `[39]` | 市盈率（PE） |
| `[43]` | 振幅（%） |
| `[44]` | 流通市值 |
| `[45]` | 总市值 |

---

## 使用方式

### 直接在脚本中调用

```python
import requests

def get_quote(code):
    url = f"https://qt.gtimg.cn/q={code}"
    resp = requests.get(url, timeout=10)
    data = resp.text
    # 解析 v_xxx="51~名称~代码~价格~..."
    parts = data.split('="')[1].strip().strip('";')
    fields = parts.split('~')
    return {
        "name": fields[1],
        "code": fields[2],
        "price": fields[3],
        "yesterday_close": fields[4],
        "open": fields[5],
        "change": fields[31],
        "change_pct": fields[32],
        "high": fields[33],
        "low": fields[34],
        "volume": fields[36],
        "turnover": fields[37],
        "turnover_rate": fields[38],
        "pe": fields[39],
        "amplitude": fields[43],
    }

# 示例
quote = get_quote("sh000001")
print(f"{quote['name']}: {quote['price']} ({quote['change_pct']}%)")
```

### 多只股票同时查询

```python
def get_quotes(codes):
    # codes: list，如 ["sh000001", "sz399001", "hkHSI"]
    url = "https://qt.gtimg.cn/q=" + ",".join(codes)
    resp = requests.get(url, timeout=10)
    results = []
    for line in resp.text.strip().split('\n'):
        if '="v_' in line:
            parts = line.split('="')[1].strip().strip('";')
            fields = parts.split('~')
            results.append({
                "name": fields[1],
                "code": fields[2],
                "price": fields[3],
                "change": fields[31],
                "change_pct": fields[32],
                "high": fields[33],
                "low": fields[34],
            })
    return results

# 同时查询多只
quotes = get_quotes(["sh000001", "sz399001", "hkHSI", "hkHSTECH", "sh560860"])
for q in quotes:
    print(f"{q['name']}: {q['price']} ({q['change_pct']}%)")
```

---

## 常用代码速查

### A 股指数

| 名称 | 代码 |
|------|------|
| 上证指数 | `sh000001` |
| 深证成指 | `sz399001` |
| 创业板指 | `sz399006` |
| 沪深300 | `sh000300` |
| 科创50 | `sh000688` |
| 北证50 | `sz899050` |

### A 股个股

| 名称 | 代码 |
|------|------|
| 贵州茅台 | `sh600519` |
| 宁德时代 | `sz300750` |
| 比亚迪 | `sz002594` |
| 招商银行 | `sh600036` |
| 中国平安 | `sh601318` |
| 工业有色ETF | `sh560860` |

### 港股

| 名称 | 代码 |
|------|------|
| 恒生指数 | `hkHSI` |
| 恒生科技 | `hkHSTECH` |
| 腾讯控股 | `hk00700` |
| 阿里巴巴 | `hk09988` |
| 美团 | `hk03690` |
| 小米集团 | `hk01810` |
| 京东集团 | `hk09618` |
| 快手 | `hk01024` |

### ETF

| 名称 | 代码 |
|------|------|
| 工业有色ETF | `sh560860` |
| 沪深300ETF | `sh510300` |
| 恒生ETF | `sh159920` |

---

## 定时任务中的用法

在 cron 任务中调用腾讯接口获取行情数据：

```python
import requests

codes = ["sh000001", "sz399001", "hkHSI", "hkHSTECH"]
url = "https://qt.gtimg.cn/q=" + ",".join(codes)
resp = requests.get(url, timeout=10)
# 解析并输出
```

---

## 注意事项

1. **查询频率**：建议每次调用间隔 100ms 以上，高频调用可能被封 IP
2. **数据用途**：仅供参考，不构成投资建议
3. **接口稳定**：腾讯接口稳定性和速度均优于国内大多数免费 API
4. **字段缺失**：部分股票（如港股一些股票）字段可能不全，返回空字符串时跳过即可
5. **时区**：港股交易时间 9:30-16:00 香港时间（A 股 9:30-15:00 北京时间）
