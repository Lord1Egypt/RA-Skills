---
name: "Stock Historical Data Query - 股票历史行情查询"
description: 按代码与时间范围查历史日线，或查列表与详情，便于 K 线与走势分析。当用户说：宁德时代最近一年 K 线数据？这只股票过去一年最高最低价？或类似历史行情问题时，使用本技能。
metadata: { "openclaw": { "emoji": "📊", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据股票历史行情查询（Jisu Stock History）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **股票历史查询**（`/stockhistory/query`）：根据股票代码、开始时间、结束时间获取历史数据，数据粒度为天，返回日期、开盘价、收盘价、最高价、最低价、成交量、成交额、换手率、涨跌幅等，可用于绘制 K 线及走势分析
- **股票列表**（`/stockhistory/list`）：按分类（沪深股市）分页获取股票列表
- **股票详情**（`/stockhistory/detail`）：根据股票代码获取单只股票详情（最新价、涨跌幅、成交量、市盈率等）

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [股票历史行情查询 API](https://www.jisuapi.com/api/stockhistory/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/stockhistory/stockhistory.py`

## 使用方式

### 1. 股票历史查询（/stockhistory/query）

根据股票代码与可选的时间范围获取历史日线数据。

```bash
# 指定时间范围
python3 skills/stockhistory/stockhistory.py query '{"code":"300917","startdate":"2020-12-24","enddate":"2020-12-25"}'

# 仅股票代码（startdate/enddate 可选，不传由接口默认）
python3 skills/stockhistory/stockhistory.py query '{"code":"300917"}'
```

请求 JSON：

```json
{
  "code": "300917",
  "startdate": "2020-12-24",
  "enddate": "2020-12-25"
}
```

| 字段名     | 类型   | 必填 | 说明     |
|------------|--------|------|----------|
| code       | string | 是   | 股票代码 |
| startdate  | string | 否   | 开始日期 |
| enddate    | string | 否   | 结束日期 |

### 2. 股票列表（/stockhistory/list）

按分类分页获取股票列表，当前文档中 classid 为 1（沪深股市）。

```bash
python3 skills/stockhistory/stockhistory.py list '{"classid":1,"pagenum":1,"pagesize":10}'
```

请求 JSON：

```json
{
  "classid": 1,
  "pagenum": 1,
  "pagesize": 10
}
```

| 字段名   | 类型   | 必填 | 说明               |
|----------|--------|------|--------------------|
| classid  | int    | 是   | 1 沪深股市         |
| pagenum  | int    | 否   | 当前页，默认 1     |
| pagesize | int    | 否   | 每页数量，默认 30  |

### 3. 股票详情（/stockhistory/detail）

根据股票代码获取单只股票详情。

```bash
python3 skills/stockhistory/stockhistory.py detail '{"code":"300917"}'
```

请求 JSON：

```json
{
  "code": "300917"
}
```

| 字段名 | 类型   | 必填 | 说明     |
|--------|--------|------|----------|
| code   | string | 是   | 股票代码 |

## 返回结果示例（节选）

### 股票历史查询（query）

```json
{
  "code": "300917",
  "name": "C特发",
  "startdate": "2020-12-24",
  "enddate": "2020-12-25",
  "list": [
    {
      "stockid": 6769,
      "date": "2020-12-24",
      "openningprice": "40.10",
      "closingprice": "53.92",
      "maxprice": "54.20",
      "minprice": "40.10",
      "tradenum": 166623,
      "tradeamount": "756991472.00",
      "turnoverrate": "78.110",
      "changepercent": "32.48",
      "changeamount": "13.22",
      "amplitude": "34.64",
      "per": null,
      "pbr": null,
      "totalmarket": null,
      "circulationmarket": null
    }
  ]
}
```

### 股票列表（list）

```json
{
  "pagesize": 10,
  "pagenum": 1,
  "total": 4486,
  "classid": 1,
  "list": [
    { "name": "信达增利", "code": "166105" },
    { "name": "R003", "code": "201000" }
  ]
}
```

### 股票详情（detail）

与实时股票接口类似，包含 name、code、price、maxprice、minprice、tradenum、tradeamount、turnoverrate、openningprice、lastclosingprice、changepercent、changeamount、amplitude、quantityratio、per、pbr、totalmarket、circulationmarket、updatetime 等字段。

当接口返回业务错误时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "股票代码为空"
}
```

## 常见错误码

来源于 [极速数据股票历史行情文档](https://www.jisuapi.com/api/stockhistory/)：

| 代号 | 说明           |
|------|----------------|
| 201  | 股票代码为空   |
| 202  | 股票代码不存在 |
| 210  | 没有信息       |

系统错误码：101～108（与其它极速数据接口一致）。

## 推荐用法

1. 用户提问：「300917 最近一周的历史走势 / K 线数据有吗？」  
2. 代理根据当前日期计算 startdate/enddate，调用：  
   `python3 skills/stockhistory/stockhistory.py query '{"code":"300917","startdate":"2025-02-24","enddate":"2025-03-02"}'`  
3. 从返回的 `list` 中提取 date、openningprice、closingprice、maxprice、minprice、tradenum、changepercent 等，用文字或建议用户用图表绘制 K 线、涨跌幅走势。  
4. 需要先选股票时，可调用 `list` 获取沪深列表，或结合 `skills/stock` 的实时接口做「历史 + 实时」组合查询。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

