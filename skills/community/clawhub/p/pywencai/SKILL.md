---
name: pywencai
description: 同花顺问财自然语言数据查询工具 - 使用中文自然语言查询A股、指数、基金、港美股、可转债等市场数据。
version: 1.2.0
homepage: https://github.com/zsrl/pywencai
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["python3","node"]}}}
---

# PyWenCai（同花顺问财数据查询）

通过Python使用中文自然语言从[同花顺问财](https://www.iwencai.com/)查询A股及其他市场数据。

> ⚠️ **需要Cookie**：必须提供问财网站的有效Cookie。获取方法见下文。

## 环境要求

- **Python 3.7+**
- **Node.js v16+** (pywencai internally executes JS code)
- **pip** package manager

## 安装

```bash
pip install pywencai --upgrade
```

## 如何获取Cookie

1. 在浏览器中打开 https://www.iwencai.com/ 并登录。
2. 按F12打开开发者工具 → 切换到Network标签。
3. 在问财页面执行任意查询。
4. 找到发往`iwencai.com`的请求，从请求头中复制`Cookie`值。
5. 将该字符串作为`cookie`参数使用。

## 基本用法

```python
import pywencai

# 查询今日涨幅前10的股票，需要有效cookie
res = pywencai.get(query='今日涨幅前10', cookie='your_cookie_here')
print(res)
```

## API参考：`pywencai.get(**kwargs)`

### 必选参数

- **query** — 中文自然语言查询字符串，如 `'今日涨停股票'`、`'市盈率小于20的股票'`
- **cookie** — 从问财网站获取的Cookie字符串（必需）


### 可选参数

- **sort_key** — 排序字段名，如 `'退市@退市日期'`
- **sort_order** — 排序方向：`'asc'`（升序）或 `'desc'`（降序）
- **page** — 页码（默认：`1`）
- **perpage** — 每页结果数（默认和最大：`100`）
- **loop** — 设为`True`获取所有页；或设为整数`n`获取前n页
- **query_type** — 查询类别（默认：`'stock'`），可选值：
  - `stock` — A股股票
  - `zhishu` — 指数
  - `fund` — 基金
  - `hkstock` — 港股
  - `usstock` — 美股
  - `threeboard` — 新三板
  - `conbond` — 可转债
  - `insurance` — 保险
  - `futures` — 期货
  - `lccp` — 理财产品
- **retry** — 失败重试次数（默认：`10`）
- **sleep** — 分页请求间延迟秒数（默认：`0`）
- **log** — 设为`True`在控制台打印日志
- **pro** — 设为`True`使用付费版（需要对应的cookie）
- **no_detail** — 设为`True`始终返回`DataFrame`或`None`（不返回dict）
- **find** — 优先返回的股票代码列表，如 `['600519', '000010']`
- **request_params** — 传递给`requests`的额外参数，如 `{'proxies': proxies}`

### 返回值

- **列表类查询** → 返回 `pandas.DataFrame`
- **详情类查询** → 返回 `dict`（可能包含文本和DataFrame）


## 使用示例

### 查询市盈率低于20的股票

```python
import pywencai

# 使用自然语言查询低市盈率股票
res = pywencai.get(query='市盈率小于20的股票', cookie='xxx')
print(res)
```

### 获取退市股票按日期排序

```python
import pywencai

# 查询退市股票，按退市日期升序排列
res = pywencai.get(
    query='退市股票',
    sort_key='退市@退市日期',  # 指定排序字段
    sort_order='asc',          # 升序
    cookie='xxx'
)
print(res)
```

### 使用代理分页获取全部数据

```python
import pywencai

# 配置HTTP代理
proxies = {'http': 'http://proxy:8080', 'https': 'http://proxy:8080'}

# loop=True自动分页获取所有数据；log=True打印请求日志
res = pywencai.get(
    query='昨日涨幅',
    sort_order='asc',          # 升序
    loop=True,                 # 自动获取所有页面
    log=True,                  # 打印日志信息
    cookie='xxx',
    request_params={'proxies': proxies}  # 传入代理配置
)
print(res)
```

### 查询指数数据

```python
import pywencai

# 设置query_type='zhishu'查询指数数据
res = pywencai.get(
    query='上证指数近5日涨跌幅',
    query_type='zhishu',       # 设置查询类型为指数
    cookie='xxx'
)
print(res)
```

### 查询可转债数据

```python
import pywencai

# 设置query_type='conbond'查询可转债数据
res = pywencai.get(
    query='可转债溢价率小于10%',
    query_type='conbond',      # 设置查询类型为可转债
    cookie='xxx'
)
print(res)
```


## 使用技巧

- **适度使用** — 高频调用可能被问财服务器封禁。
- 始终使用**最新版本**：`pip install pywencai --upgrade`
- 查询字符串使用**中文自然语言** — 像在问财网站搜索一样编写查询。
- 当`loop=True`且设置了`find`时，`loop`被忽略，仅返回前100条结果。
- 使用付费数据时，设置`pro=True`并提供有效`cookie`。

---

## 进阶示例

### 查询涨停股详情

```python
import pywencai

# 查询今日涨停股票，获取详细信息
res = pywencai.get(
    query='今日涨停的股票',
    cookie='xxx'
)
# 返回DataFrame：包含股票代码、名称、涨停时间、封单金额等
print(res)
```

### 查询连板股

```python
import pywencai

# 查询连续涨停天数大于2天的股票
res = pywencai.get(
    query='连续涨停天数大于2天的股票',
    cookie='xxx'
)
print(res)
```

### 查询财务数据

```python
import pywencai

# 查询ROE大于15%且营收同比增长大于20%的股票
res = pywencai.get(
    query='ROE大于15%且营收同比增长率大于20%的股票',
    cookie='xxx'
)
print(res)

# 查询市盈率小于10且市净率小于1的股票（低估值筛选）
res = pywencai.get(
    query='市盈率小于10且市净率小于1的股票',
    cookie='xxx'
)
print(res)
```


### 查询技术指标数据

```python
import pywencai

# 查询今日MACD金叉的股票
res = pywencai.get(
    query='今日MACD金叉的股票',
    cookie='xxx'
)
print(res)

# 查询KDJ超卖信号的股票
res = pywencai.get(
    query='KDJ的J值小于0的股票',
    cookie='xxx'
)
print(res)

# 查询放量突破的股票
res = pywencai.get(
    query='今日成交量是5日均量2倍以上且涨幅大于5%的股票',
    cookie='xxx'
)
print(res)
```

### 查询资金流向数据

```python
import pywencai

# 查询今日主力资金净流入前20的股票
res = pywencai.get(
    query='今日主力资金净流入前20的股票',
    cookie='xxx'
)
print(res)

# 查询北向资金持股比例最高的股票
res = pywencai.get(
    query='北向资金持股比例最高的前20只股票',
    cookie='xxx'
)
print(res)
```

### 查询基金数据

```python
import pywencai

# 查询近一年收益率最高的前20只基金
res = pywencai.get(
    query='近一年收益率最高的前20只基金',
    query_type='fund',     # 设置查询类型为基金
    cookie='xxx'
)
print(res)
```

### 查询港股数据

```python
import pywencai

# 查询港股市值最大的股票
res = pywencai.get(
    query='港股市值最大的前20只股票',
    query_type='hkstock',  # 设置查询类型为港股
    cookie='xxx'
)
print(res)
```


### 多条件选股

```python
import pywencai

# 复杂多条件筛选：低估值+高成长+机构持仓
res = pywencai.get(
    query='市盈率小于20且营收同比增长大于30%且机构持仓比例大于10%的股票',
    cookie='xxx'
)
print(res)

# 技术面+基本面综合筛选
res = pywencai.get(
    query='今日站上20日均线且市盈率小于30且ROE大于10%的股票',
    cookie='xxx'
)
print(res)
```

### 获取历史数据

```python
import pywencai

# 查询指定日期的数据
res = pywencai.get(
    query='2024年1月2日涨幅前10的股票',
    cookie='xxx'
)
print(res)

# 查询日期范围内的涨幅
res = pywencai.get(
    query='2024年上半年涨幅最大的前20只股票',
    cookie='xxx'
)
print(res)
```

### 完整示例：自动化选股并导出

```python
import pywencai
import pandas as pd
import time

cookie = 'your_cookie_here'

# 定义多个筛选策略
strategies = {
    "低估值高分红": "市盈率小于15且股息率大于3%的股票",
    "高成长": "营收同比增长大于30%且净利润同比增长大于30%的股票",
    "技术突破": "今日放量突破20日均线且涨幅大于3%的股票",
    "机构关注": "近一个月机构调研次数大于3次的股票",
    "北向资金": "北向资金今日净买入前20的股票",
}

results = {}
for name, query in strategies.items():
    try:
        res = pywencai.get(query=query, cookie=cookie, no_detail=True)
        if res is not None and not res.empty:
            results[name] = res
            print(f"Strategy [{name}] selected {len(res)} stocks")
        else:
            print(f"Strategy [{name}] returned no results")
    except Exception as e:
        print(f"Strategy [{name}] query failed: {e}")
    time.sleep(2)  # 每次查询间隔2秒，避免被封禁

# 保存结果到Excel（每个策略一个工作表）
if results:
    with pd.ExcelWriter("选股结果.xlsx") as writer:
        for name, df in results.items():
            df.to_excel(writer, sheet_name=name, index=False)
    print("筛选结果已保存到 选股结果.xlsx")
```

## 常见错误处理

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `Cookie expired` | Cookie过期 | 重新登录问财网站获取新Cookie |
| 返回`None` | 查询无结果或被限流 | 检查查询语句，降低调用频率 |
| `Node.js not found` | 未安装Node.js | 安装Node.js v16+ |
| `JSONDecodeError` | 服务端返回异常 | 增加`retry`参数，稍后重试 |
| 返回dict而非DataFrame | 查询为详情类 | 设置`no_detail=True`强制返回DataFrame |

## Cookie管理最佳实践

```python
import os
import pywencai

# 方法1：从环境变量读取Cookie（推荐）
cookie = os.environ.get('WENCAI_COOKIE', '')

# 方法2：从文件读取Cookie
def load_cookie(path='~/.wencai_cookie'):
    path = os.path.expanduser(path)
    if os.path.exists(path):
        with open(path) as f:
            return f.read().strip()
    return ''

# 方法3：封装查询函数，统一管理Cookie和错误处理
def query(q, **kwargs):
    cookie = load_cookie()
    try:
        return pywencai.get(
            query=q, cookie=cookie,
            no_detail=True, retry=3, sleep=1,
            **kwargs
        )
    except Exception as e:
        print(f"查询失败: {e}")
        return None

# 使用
df = query('今日涨停的股票')
```

## 进阶示例：定时监控与告警

```python
import pywencai
import time
import datetime

cookie = 'your_cookie_here'

# 监控条件列表
alerts = [
    {'名称': '大盘跳水', '查询': '上证指数今日跌幅大于2%', '类型': 'zhishu'},
    {'名称': '涨停潮', '查询': '今日涨停股票数量', '类型': 'stock'},
    {'名称': '北向大额流出', '查询': '北向资金今日净卖出大于50亿', '类型': 'stock'},
]

def check_alerts():
    now = datetime.datetime.now().strftime('%H:%M')
    for alert in alerts:
        try:
            res = pywencai.get(
                query=alert['查询'],
                query_type=alert.get('类型', 'stock'),
                cookie=cookie, no_detail=True
            )
            if res is not None and not res.empty:
                print(f"[{now}] 告警触发 [{alert['名称']}]: {len(res)} 条结果")
        except Exception as e:
            print(f"[{now}] 查询失败 [{alert['名称']}]: {e}")
        time.sleep(2)

# 交易时间内每5分钟检查一次
while True:
    now = datetime.datetime.now()
    if 9 <= now.hour < 15:
        check_alerts()
    time.sleep(300)
```

---

---

## 🤖 AI Agent 高阶使用指南

对于 AI Agent，在使用该量化/数据工具时应遵循以下高阶策略和最佳实践，以确保任务的高效完成：

### 1. 数据校验与错误处理
在获取数据或执行操作后，AI 应当主动检查返回的结果格式是否符合预期，以及是否存在缺失值（NaN）或空数据。
* **示例策略**：在通过 API 获取数据框（DataFrame）后，使用 `if df.empty:` 进行校验；捕获 `Exception` 以防网络或接口错误导致进程崩溃。

### 2. 多步组合分析
AI 经常需要进行宏观经济分析或跨市场对比。应善于将当前接口与其他数据源或工具组合使用。
* **示例策略**：先获取板块或指数的宏观数据，再筛选成分股，最后对具体标的进行深入的财务或技术面分析，形成完整的决策链条。

### 3. 构建动态监控与日志
对于交易和策略类任务，AI 可以定期拉取数据并建立监控机制。
* **示例策略**：使用循环或定时任务检查特定标的的异动（如涨跌停、放量），并在发现满足条件的信号时输出结构化日志或触发预警。

---

## 社区与支持

由 **大佬量化** 维护 — 量化交易教学与策略研发团队。

微信客服: **bossquant1** · [Bilibili](https://space.bilibili.com/48693330) · 搜索 **大佬量化** — 微信公众号 / Bilibili / 抖音
