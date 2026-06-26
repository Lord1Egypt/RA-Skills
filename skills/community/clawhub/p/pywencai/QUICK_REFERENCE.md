# PyWenCai API 快速参考

本文档提供最常用的 PyWenCai 问财选股 API 接口和代码示例。

**维护者**: 大佬量化 (Boss Quant)

## 初始化

```python
import pywencai

# 需要问财网站 Cookie
cookie = 'your_cookie_here'
```

## 基本查询

```python
# 自然语言查询
df = pywencai.get(query='今日涨停股票', cookie=cookie)
# 返回 pandas DataFrame
```

## 查询类型

```python
# 股票查询（默认）
df = pywencai.get(query='市盈率小于20', query_type='stock', cookie=cookie)

# 指数查询
df = pywencai.get(query='沪深300指数', query_type='zhishu', cookie=cookie)

# 基金查询
df = pywencai.get(query='收益率前10的基金', query_type='fund', cookie=cookie)

# 可转债查询
df = pywencai.get(query='转股溢价率小于5%', query_type='conbond', cookie=cookie)
```

## 排序

```python
# 按指定字段排序
df = pywencai.get(query='今日涨幅前100', sort_key='涨跌幅', sort_order='desc', cookie=cookie)

# 升序排列
df = pywencai.get(query='市盈率最低的股票', sort_key='市盈率', sort_order='asc', cookie=cookie)
```

## 自动翻页

```python
# 启用自动翻页，获取全部结果
df = pywencai.get(query='市盈率小于15的股票', loop=True, cookie=cookie)
```

## 常用查询示例

```python
# 涨停板查询
df = pywencai.get(query='今日涨停股票', cookie=cookie)

# 财务筛选
df = pywencai.get(query='市盈率小于20，ROE大于15%，市值大于100亿', cookie=cookie)

# 技术指标筛选
df = pywencai.get(query='MACD金叉，成交量放大2倍以上', cookie=cookie)

# 行业筛选
df = pywencai.get(query='半导体行业，市值大于50亿', cookie=cookie)

# 龙虎榜
df = pywencai.get(query='今日龙虎榜股票', cookie=cookie)

# 北向资金
df = pywencai.get(query='北向资金今日净买入前20', cookie=cookie)
```

## 更多资源

- [PyWenCai GitHub](https://github.com/zsrl/pywencai)
- [问财网站](https://www.iwencai.com/)
