# 数据源API参考

## 1. 新浪财经（主数据源，最稳定）

### 实时行情
```
GET http://hq.sinajs.cn/list=sh600519
GET http://hq.sinajs.cn/list=sz000001
GET http://hq.sinajs.cn/list=sh600519,sz000001,sz300750  # 批量
```

响应格式（逗号分隔字符串）：
```
var hq_str_sh600519="贵州茅台,1788.00,1785.00,1800.00,1810.00,1780.00,...,2024-01-15,15:00:00,00"
```
字段顺序：股票名,昨收,今开,当前价,最高,最低,买一价,卖一价,成交量(手),成交额,买一量,...日期,时间

### 大盘指数
```
GET http://hq.sinajs.cn/list=s_sh000001,s_sz399001,s_sz399006,s_sh000688,s_bj899050
```

## 2. 东方财富（备用，数据全面）

### 实时行情
```
GET http://push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f107,f169,f170,f171,f116
```
market: 1=沪市, 0=深市, 2=北交所
关键字段：f43最新价(×0.01)、f44最高、f45最低、f46今开、f47成交量(手)、f48成交额(元)、f57代码、f58名称、f60昨收、f170涨跌幅(%×100)、f169涨跌额、f171换手率(%×100)、f116市盈率(×0.01)

### A股涨幅榜
```
GET http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=50&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f2,f3,f4,f5,f6,f7,f12,f14
```

### 热点板块
```
GET http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2+f:!50&fields=f2,f3,f4,f12,f14,f20,f128,f136
```

### 个股分时
```
GET http://push2.eastmoney.com/api/qt/stock/trends2/get?secid={market}.{code}&fields1=f1,f2,f3,f4,f5&fields2=f51,f52,f53,f54,f55,f56,f57,f58&iscr=0&iscca=0
```

## 3. 腾讯行情（备用二，支持批量）

### 实时行情
```
GET http://qt.gtimg.cn/q=sh600519
GET http://qt.gtimg.cn/q=sh600519,sz000001,sz300750  # 批量（最多900支）
```

返回格式（~分隔的字符串，40+个字段）：
字段索引：1=代码, 2=名称, 3=收盘价, 4=昨收, 5=今开, 6=成交量(手), 32=涨跌幅(%), 33=最高, 34=最低, 37=成交额, 38=换手率, 39=市盈率

### 市场代码前缀
腾讯使用小写：sh=沪市, sz=深市, bj=北交所

## 4. 代码对应表

| 代码前缀 | 新浪 | 东财market | 腾讯 |
|---------|:----:|:---------:|:----:|
| 60xxx/68xxx | sh | 1 | sh |
| 00xxx/30xxx | sz | 0 | sz |
| 8xxxx/4xxxx | bj | 2 | bj |

| 指数 | 新浪code | 东财secid |
|------|---------|----------|
| 上证指数 | s_sh000001 | 1.000001 |
| 深证成指 | s_sz399001 | 0.399001 |
| 创业板指 | s_sz399006 | 0.399006 |
| 科创50 | s_sh000688 | 1.000688 |
| 北证50 | s_bj899050 | 2.899050 |

## 5. 问财查询（需thsdk）

```python
from thsdk import THS
with THS() as ths:
    df = ths.wencai("最近热度前50的行业")
```

## 6. web_search 通用源

当需要财报、新闻、公司基本面等非行情数据时，使用web_search：
- 东方财富网 eastmoney.com — 个股主页/财报
- 新浪财经 finance.sina.com.cn — 新闻/公告
- 雪球 xueqiu.com — 投资者讨论/深度分析
- 巨潮资讯 cninfo.com.cn — 公司公告（官方）
