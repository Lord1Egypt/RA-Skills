# thsdk API 参考文档

## THS 类

### 初始化

```python
from thsdk import THS

# 使用上下文管理器（推荐）
with THS() as ths:
    # 执行操作
    pass

# 直接实例化
ths = THS()
ths.close()  # 记得关闭连接
```

### 配置选项

```python
# 账户配置
config = {
    "username": "your_username",
    "password": "your_password", 
    "mac": "your_mac_address"
}
ths = THS(config)

# 或使用环境变量
# export THS_USERNAME=your_username
# export THS_PASSWORD=your_password  
# export THS_MAC=your_mac_address
```

## 主要API方法

### K线数据

```python
response = ths.klines(
    ths_code,           # 股票代码
    start_time=None,    # 开始时间
    end_time=None,      # 结束时间  
    adjust="",          # 复权方式：""(不复权), "forward"(前复权), "backward"(后复权)
    interval="day",     # 周期：1m, 5m, 15m, 30m, 60m, 120m, day, week, month, quarter, year
    count=-1           # 数据条数
)
```

### 市场数据

#### A股市场数据
```python
response = ths.market_data_cn(
    ths_code,       # 股票代码
    query_key       # 查询类型："基础数据", "资金流向", "财务数据", "估值指标"等
)
```

#### 美股市场数据
```python
response = ths.market_data_us(
    ths_code,       # 股票代码（如：AAPL）
    query_key       # 查询类型
)
```

#### 港股市场数据
```python
response = ths.market_data_hk(
    ths_code,       # 股票代码（如：00700）
    query_key       # 查询类型
)
```

### 分时数据

```python
# 当前分时数据
response = ths.intraday_data(ths_code)

# 历史分时数据
response = ths.min_snapshot(ths_code, date="2025-03-12")
```

### 成交数据

```python
# 3秒tick成交数据
response = ths.tick_level1(ths_code)

# 超级盘口数据
response = ths.tick_super_level1(ths_code, date="2025-03-12")
```

### 深度数据

```python
# 5档深度数据
response = ths.depth(ths_code)

# 买卖盘口
response = ths.order_book_ask(ths_code)  # 卖方
response = ths.order_book_bid(ths_code)  # 买方
```

### 板块数据

```python
# 板块数据
response = ths.block(block_id)

# 板块成分股
response = ths.block_constituents(link_code)

# 行业板块
response = ths.ths_industry()

# 概念板块  
response = ths.ths_concept()
```

### 证券查询

```python
# 模糊查询证券代码
response = ths.query_securities(
    pattern,        # 查询模式（名称或缩写）
    needmarket=""  # 市场代码（空表示所有市场）
)
```

## Response对象

所有API调用返回Response对象，包含以下属性：

```python
response.success    # bool: 是否成功
response.error      # str: 错误信息（失败时）
response.data       # 原始响应数据
response.df         # 转换为Pandas DataFrame的方法
```

### 使用示例

```python
response = ths.klines("000001", count=100)

if response.success:
    # 获取DataFrame
    df = response.df
    print(df.head())
    
    # 获取原始数据
    data = response.data
    print(data)
else:
    print(f"错误: {response.error}")
```

## 数据字段说明

### K线数据字段
- `time`: 时间戳
- `open`: 开盘价
- `high`: 最高价  
- `low`: 最低价
- `close`: 收盘价
- `volume`: 成交量
- `amount`: 成交额

### 基础数据字段
- `股票名称`: 股票名称
- `最新价`: 最新价格
- `涨跌幅`: 涨跌幅百分比
- `成交量`: 成交量
- `成交额`: 成交金额
- `换手率`: 换手率
- `市盈率`: 市盈率
- `市净率`: 市净率

### 资金流向字段
- `主力净流入`: 主力资金净流入
- `散户净流入`: 散户资金净流入
- `资金净流入`: 总资金净流入
- `净流入率`: 净流入比率

## 错误处理

### 常见错误

1. **连接错误**: 检查网络连接和账户配置
2. **参数错误**: 验证股票代码和查询参数
3. **权限错误**: 检查账户权限和有效期

### 错误处理示例

```python
try:
    response = ths.klines("000001")
    if not response.success:
        print(f"API错误: {response.error}")
        # 重试或处理错误
        
        # 检查特定错误类型
        if "连接" in response.error:
            print("网络连接问题")
        elif "权限" in response.error:
            print("账户权限问题")
            
except Exception as e:
    print(f"异常: {e}")
```

## 最佳实践

1. **使用上下文管理器**: 确保连接正确关闭
2. **批量查询**: 使用批量查询减少API调用次数
3. **错误重试**: 实现简单的重试机制
4. **数据缓存**: 对不变的数据进行缓存
5. **限流控制**: 避免过于频繁的API调用
