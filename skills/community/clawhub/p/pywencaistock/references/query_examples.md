# PyWenCai 常用查询示例

本文档提供常用查询的 query 字符串，方便快速使用。

## 行情监控

```python
# 今日涨停
search('A股涨停')

# 今日跌停
search('A股跌停')

# 涨幅前20
search('沪深A股涨幅前20')

# 跌幅前20
search('沪深A股跌幅前20')

# 换手率前20
search('换手率最高的股票')

# 成交额前20
search('成交额最大的股票')
```

## 资金流向

```python
# 主力净流入最多的股票
search('主力净流入最多的股票')

# 大单净流入最多的股票
search('大单净流入最多的股票')

# 龙虎榜
dragon_tiger_list()

# 龙虎榜机构净买入最多
search('龙虎榜机构净买入最多的股票')
```

## 财务筛选

```python
# 净利润最高的公司
search('净利润最高的公司')

# 市盈率最低的股票
search('市盈率最低的股票')

# 市净率最低的股票
search('市净率最低的股票')

# ROE最高的股票
search('ROE最高的股票')

# 营收增长最快的公司
search('营收增长最快的公司')

# 毛利率最高的股票
search('毛利率最高的股票')
```

## 个股查询

```python
# 查询单只股票行情
search_stock_by_code('600519', '行情')

# 财务指标
search_stock_by_code('600519', '财务指标')

# 股东户数
search_stock_by_code('600519', '股东户数')

# 券商评级
search_stock_by_code('600519', '券商评级')

# 机构调研
search_stock_by_code('600519', '机构调研')
```

## 板块/概念

```python
# 热门概念股
hot_sectors()  # 返回7大概念

# 具体概念
search('芯片概念股')
search('人工智能概念股')
search('新能源汽车概念股')
search('光伏概念股')
search('储能概念股')
search('军工概念股')
```

## 高级用法

### 分页获取完整结果

```python
# 一次性获取所有涨停股（自动翻页）
df = search('A股涨停', loop=True)
```

### 自定义排序

```python
# 按换手率降序排序涨停股
df = search(
    query='A股涨停',
    sort_key='换手率',
    sort_order='desc',
    perpage=100
)
```

### 组合条件

```python
# 创业板涨幅前20
df = search('创业板涨幅前20')

# 科创板跌幅前10
df = search('科创板跌幅前10')
```

## 结果处理

```python
df = search('A股涨停')

# 保存到CSV
df.to_csv('zhangting.csv', encoding='utf-8-sig', index=False)

# 保存到Excel
df.to_excel('zhangting.xlsx', index=False)

# 转为字典列表
records = df.to_dict(orient='records')

# 提取关键列
selected = df[['股票代码', '股票名称', '涨跌幅', '换手率']]
```

---

**提示**：问财的查询语言非常灵活，可以用自然语言描述需求，例如：
- '近期机构调研次数最多的股票'
- '连续3日涨停的股票'
- '破净的银行股'

多尝试不同关键词，发现更多数据洞察。
