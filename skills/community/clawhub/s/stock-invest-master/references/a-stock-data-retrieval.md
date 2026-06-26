# A股数据检索指南 — 国电南瑞实战经验

## 可用的API数据源

### 1. 腾讯财经行情API（实时行情 + 估值指标）

```
https://qt.gtimg.cn/q=sh600406
```

返回格式：`~` 分隔的文本字段。关键字段索引：
- [3] 现价, [4] 昨收, [5] 今开
- [31] 涨跌额, [32] 涨跌幅
- [33] 涨停价, [34] 跌停价
- [38] 振幅, [49] 换手率
- [44] 流通市值(亿), [45] 总市值(亿)
- [46] PB, [47] 静态PE, [48] 动态PE
- [62] ROE, [63] 每股收益, [64] 每股净资产
- [74] 52周高, [75] 52周低
- [72] 总股本(股), [73] 流通股本(股)
- [85] 股息率

### 2. 新浪行情API（日线K线）

```
https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=sh600406&scale=240&ma=no&datalen=100
```

返回JSON数组，每条包含 day/open/high/low/close/volume。

### 3. 东方财富财务数据API

**利润表**（收入/净利润/毛利率等）：
```
https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_DMSK_FN_INCOME&columns=ALL&filter=(SECURITY_CODE="600406")&pageNumber=1&pageSize=8&sortTypes=-1&sortColumns=REPORT_DATE&source=HSF10&client=PC
```

**资产负债表**（总资产/负债/应收账款/存货等）：
```
https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_DMSK_FN_BALANCE&columns=ALL&filter=(SECURITY_CODE="600406")&pageNumber=1&pageSize=4&sortTypes=-1&sortColumns=REPORT_DATE&source=HSF10&client=PC
```

**现金流量表**（经营现金流/投资现金流等）：
```
https://datacenter.eastmoney.com/securities/api/data/v1/get?reportName=RPT_DMSK_FN_CASHFLOW&columns=ALL&filter=(SECURITY_CODE="600406")&pageNumber=1&pageSize=4&sortTypes=-1&sortColumns=REPORT_DATE&source=HSF10&client=PC
```

关键字段：
- REPORT_DATE: 报告期
- PARENT_NETPROFIT: 净利润
- TOTAL_OPERATE_INCOME: 营业收入
- TOE_RATIO: ROE(加权)
- PARENT_NETPROFIT_RATIO: 净利润同比%
- INCOME_GROWTHRATE: 营收同比%
- OPERATE_EXPENSE_RATIO: 毛利率%
- NETCASH_OPERATE: 经营现金流净额
- TOTAL_ASSETS: 总资产
- TOTAL_LIABILITIES: 总负债
- DEBT_ASSET_RATIO: 资产负债率%
- CURRENT_RATIO: 流动比率%
- ACCOUNTS_RECE: 应收账款
- INVENTORY: 存货

**注意**：响应可能有UTF-8 BOM，需 `raw[3:]` 处理。

### 4. 失败的API（已验证不可用）
- EastMoney ZYFX API → 返回HTML页面
- EastMoney KEYINDICATORS → "报表配置不存在"
- EastMoney MUTUAL_HOLDSTOCKNORTH → "报表配置不存在"
- EastMoney CUSTOM_STOCK_RESEARCH → "报表配置不存在"
- 雪球API → 需要Cookie认证
- CNINFO → 需要Token
- 同花顺10jqka → 超时或404

## 数据交叉校验

```python
# PE ≈ PB / ROE
pe_check = pb / roe  # 应与PE相近，偏差<20%可接受

# EPS推算
eps = price / pe_static  # 从PE和价格推算每股收益

# 净利润推算
net_profit = eps * total_shares  # 总股本需从API获取
```

## 北向资金/机构持仓

东方财富相关API经常返回"报表配置不存在"，建议：
- 使用 WebSearch 搜索 "600406 北向资金" 获取最新数据
- 机构研报同样建议通过 WebSearch 获取

## 中文报告图片生成

浏览器无CJK字体时，HTML渲染中文会显示方框。解决方案：
1. **SVG方案**：直接生成SVG图片，使用 `system-ui, -apple-system, sans-serif` 作为字体回退
2. **Webfont方案**：HTML中引入 Google Fonts Noto Sans SC
3. **安装系统字体**：`fonts-noto-cjk`（需要apt权限）

优先使用SVG方案，最可靠且不依赖外部资源。
