---
name: "Silver Price Inquiry - 白银价格查询"
description: 查询国内白银期货/现货相关及伦敦银等参考行情。当用户说：白银现在什么价？伦敦银涨跌多少？或类似白银价格问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🥈", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据白银价格（Jisu Silver）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **上海黄金交易所白银价格**（`/silver/shgold`）
- **上海期货交易所白银价格**（`/silver/shfutures`）
- **伦敦银价格**（`/silver/london`）
- **白银历史行情**（`/silver/history`）：按市场与品种查询历史开高低收

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [白银价格 API](https://www.jisuapi.com/api/silver/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/silver/silver.py`

## 使用方式

### 1. 上海黄金交易所白银价格（/silver/shgold）

```bash
python3 skills/silver/silver.py shgold
```

### 2. 上海期货交易所白银价格（/silver/shfutures）

```bash
python3 skills/silver/silver.py shfutures
```

### 3. 伦敦银价格（/silver/london）

```bash
python3 skills/silver/silver.py london
```

### 4. 白银历史行情（/silver/history）

```bash
python3 skills/silver/silver.py history '{"market":"london","startdate":"2026-06-01","enddate":"2026-06-10","type":"xag"}'
```

请求 JSON：

```json
{
  "market": "london",
  "startdate": "2026-06-01",
  "enddate": "2026-06-10",
  "type": "xag"
}
```

| 字段名    | 类型   | 必填 | 说明                                              |
|-----------|--------|------|---------------------------------------------------|
| market    | string | 是   | `london` 伦敦 / `ny` 纽约 / `td` TD / `futures` 期货 |
| startdate | string | 是   | 开始日期                                          |
| enddate   | string | 是   | 结束日期                                          |
| type      | string | 是   | 品种代码，如 `xag`（伦敦银）等                    |

## 返回结果示例（节选）

### 上海黄金交易所白银价格

```json
[
  {
    "type": "Ag(T+D)",
    "typename": "白银延期",
    "price": "3399.00",
    "openingprice": "3402.00",
    "maxprice": "3407.00",
    "minprice": "3388.00",
    "changepercent": "0.09%",
    "lastclosingprice": "3396.00",
    "tradeamount": "1373982.0000",
    "updatetime": "2015-10-27 15:07:25"
  }
]
```

### 上海期货交易所白银价格

```json
[
  {
    "type": "AG1512",
    "typename": "白银1512",
    "price": "3438",
    "changequantity": "4",
    "buyprice": "3437",
    "buyamount": "41",
    "sellprice": "3438",
    "sellamount": "191",
    "tradeamount": "397592",
    "openingprice": "3438",
    "lastclosingprice": "3434",
    "maxprice": "3447",
    "minprice": "3424",
    "holdamount": "417466",
    "increaseamount": "2212"
  }
]
```

### 伦敦银价格

```json
[
  {
    "type": "白银美元",
    "price": "15.84",
    "changepercent": "-0.13%",
    "changequantity": "-0.02",
    "openingprice": "15.86",
    "maxprice": "15.87",
    "minprice": "15.77",
    "lastclosingprice": "15.86",
    "amplitude": "0.63",
    "buyprice": "15.92",
    "sellprice": "15.84",
    "updatetime": "2015-10-27 15:03:00"
  }
]
```

### 白银历史行情

```json
{
  "market": "london",
  "type": "xag",
  "startdate": "2026-06-01",
  "enddate": "2026-06-10",
  "count": 8,
  "list": [
    {
      "typename": "伦敦银",
      "date": "2026-06-10",
      "openingprice": 65.13,
      "maxprice": 65.73,
      "minprice": 63.29,
      "price": 63.38,
      "change_amount": -1.75,
      "changepercent": "-2.69%"
    }
  ]
}
```

当无数据时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "没有信息"
}
```

## 常见错误码

来源于 [极速数据白银文档](https://www.jisuapi.com/api/silver/)：

| 代号 | 说明     |
|------|----------|
| 201  | 没有信息 |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |

## 推荐用法

1. 用户提问：「现在白银价格大概多少？帮我看看国内和伦敦市场。」  
2. 代理依次调用：  
   - `python3 skills/silver/silver.py shgold`  
   - `python3 skills/silver/silver.py london`  
3. 从返回结果中选取代表性品种（如白银延期、白银9999、伦敦银），为用户总结当前价格、涨跌幅与近期波动区间。
4. 用户需要 **历史区间走势** 时，调用 `history`（如伦敦银 `market: london, type: xag`）。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

