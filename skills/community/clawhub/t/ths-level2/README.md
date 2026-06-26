# 同花顺Level2数据接入方案

## 📁 文件结构

```
ths_level2/
├── README.md                    # 本文档
├── example.py                   # 完整使用示例
├── ths_client.py                # TCP客户端实现
├── ths_memory_reader.py         # 内存读取器
├── analyze_protocol.py          # 协议分析工具
├── ths_protocol_analysis.json   # 协议分析结果
└── ths_protocol_generated.py    # 自动生成的协议代码
```

## 概述

本方案通过分析同花顺远航版客户端实现Level2数据获取。

## 发现的资源

### 1. 服务器配置

位置: `D:\同花顺远航版\bin\workspace\DataCenter.xml`

```
行情服务器:
- hevo-h.10jqka.com.cn:9601 (主行情)
- hevo.10jqka.com.cn:8602 (计算/统计服务)

备用服务器:
- 110.41.57.53:9602
- 122.112.248.51:9602
- 124.71.31.234:9602
- 等多个服务器...
```

### 2. 数据请求协议

位置: `D:\同花顺远航版\bin\data\public\DataPushJob.xml`

这是关键文件，记录了所有数据请求格式！

#### Level2 相关数据请求

| 功能 | 请求ID | 参数示例 |
|------|--------|----------|
| 成交明细 | 205 | `id=205&market=USZA&code=002539&start=-20&end=0&datatype=1,12,49,10,18` |
| 集合竞价 | 204 | `id=204&market=USZA&code=000935&start=时间戳&end=时间戳&datatype=10,49,19,27,33` |
| 分时数据 | 207 | `id=207&market=USZA&code=300033&date=0&datatype=13,19,10,1` |
| K线数据 | 210 | `id=210&market=USZA&code=300033&start=-314&end=0&datatype=1,7,8,9,11,13,19&period=16384&fuquan=Q` |
| 实时行情 | 200 | `id=200&market=USHI&codelist=1A0001&datatype=5,6,10,19` |
| 十档行情 | 202 | `id=202&market=USZA&codelist=股票列表&datatype=数据类型` |

### 3. 市场代码

```
USHA - 上海A股
USZA - 深圳A股  
USHI - 上海指数
USZI - 深圳指数
UHKM - 港股主板
UHKG - 港股创业板
UCXF - 期货(纽约商品交易所)
UMEF - 期货(芝加哥期货交易所)
```

### 4. 数据类型ID (datatype)

| ID | 说明 |
|----|------|
| 1 | 价格相关 |
| 5 | 昨收 |
| 6 | 收盘价 |
| 7 | 开盘价 |
| 8 | 最高价 |
| 9 | 最低价 |
| 10 | 最新价 |
| 12 | 成交量 |
| 13 | 成交量(股) |
| 18 | 成交额 |
| 19 | 成交额(元) |
| 27-50 | Level2深度数据 |

### 5. 本地数据库

位置: `D:\同花顺远航版\bin\stockname\stocknameV2.db`

SQLite数据库，包含所有股票的基本信息。

```sql
-- 表结构
CREATE TABLE tablestock (
    CODE TEXT,      -- 股票代码
    NAME TEXT,      -- 股票名称
    MARKET TEXT,    -- 市场代码
    FIRSTPY TEXT,   -- 拼音首字母
    ALLPY TEXT,     -- 完整拼音
    DATATAG TEXT,
    MARKETNAME TEXT,
    PRIMARY KEY('CODE','MARKET','DATATAG')
)
```

## 接入方案

### 方案一: 直接TCP连接 (需要协议分析)

同花顺使用私有TCP协议，需要逆向分析数据包格式。

优点:
- 实时性好
- 数据完整

缺点:
- 协议可能变化
- 需要登录认证
- 可能违反用户协议

### 方案二: 内存读取 (推荐)

通过读取同花顺进程内存获取数据。

实现步骤:
1. 找到同花顺进程
2. 定位数据内存区域
3. 读取并解析数据

优点:
- 不需要网络协议
- 数据已经在本地

缺点:
- 需要同花顺运行
- 内存地址可能变化

### 方案三: 共享内存/IPC

同花顺可能使用共享内存存储实时数据。

检查方法:
- 查找命名共享内存
- 分析DLL导出函数

### 方案四: 网络抓包 + 模拟

使用Wireshark抓包分析协议，然后模拟客户端。

## 快速开始

### 读取本地股票数据

```python
from ths_client import THSLocalReader

reader = THSLocalReader()
stocks = reader.get_all_stocks()
print(f"共 {len(stocks)} 只股票")

# 搜索股票
results = reader.search_stock("平安银行")
print(results)
```

### 连接服务器

```python
from ths_client import THSClient

with THSClient() as client:
    # 获取行情
    quote = client.get_quote('600000')
    print(quote)
    
    # 获取Level2成交明细
    trades = client.get_trade_detail('000001')
    for t in trades:
        print(f"{t.time} {t.price} {t.volume}")
```

## 下一步

1. **协议分析**: 使用Wireshark抓包分析数据格式
2. **内存读取**: 使用 Cheat Engine / x64dbg 分析内存结构
3. **DLL调用**: 分析 `Hevo.Sdk.dll` 等SDK文件

## 相关文件

- `DataPushJob.xml` - 数据请求格式参考
- `Services.xml` - 服务器列表
- `DataCenter.xml` - 数据中心配置
- `market.ini` - 市场配置
- `StockLink.ini` - 股票链接配置

## 注意事项

⚠️ 本方案仅供学习研究使用，请遵守相关法律法规和用户协议。

- 同花顺Level2数据为付费服务，请确保您已开通相关权限
- 大量请求可能导致账号被限制
- 数据格式可能随版本更新变化