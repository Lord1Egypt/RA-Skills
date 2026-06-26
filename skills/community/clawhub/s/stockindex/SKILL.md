---
name: "Shanghai Stock Exchange Composite Index - 上证股票指数"
description: 查询上证、深证、创业板、沪深300、科创50 等主要指数分钟级行情。当用户说：上证指数现在多少点？创业板指涨跌幅？或类似大盘指数问题时，使用本技能。
metadata: { "openclaw": { "emoji": "📉", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据上证股票指数（Jisu Stock Index）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **股票指数**（`/stockindex/sh`）：一次性获取上证指数、深证成指、创业板指、中小板指、沪深300、上证50、科创50、B股指数等品种的最新价、昨收盘价、数据量、更新时间及分钟级趋势（`trend` / `trend_standard`），数据粒度为分钟。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [上证股票指数 API](https://www.jisuapi.com/api/stockindex/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/stockindex/stockindex.py`

## 使用方式

### 股票指数（/stockindex/sh）

无需请求参数，直接调用即可获取各指数品种的实时行情及分钟趋势。

```bash
python3 skills/stockindex/stockindex.py sh
```

## 返回结果示例（节选）

```json
[
  {
    "name": "上证指数",
    "code": "000001",
    "price": "3416.08",
    "lastclosingprice": 3410.18,
    "trendnum": "241",
    "updatetime": 1607509662,
    "openningprice": "3410.18",
    "trend": [
      "2020-12-09 09:30,3416.08,2081381,2544235056.00,3411.749",
      "2020-12-09 09:31,3417.53,4931922,5994410752.00,3411.554"
    ],
    "trend_standard": []
  }
]
```

| 字段名            | 类型   | 说明                                                                 |
|-------------------|--------|----------------------------------------------------------------------|
| name              | string | 品种名称（如上证指数、深证成指）                                       |
| code              | string | 品种代码                                                             |
| price             | string | 最新价                                                               |
| lastclosingprice  | string | 昨收盘价                                                             |
| trendnum          | string | 数据量                                                               |
| updatetime        | string | 更新时间                                                             |
| openningprice     | string | 开盘价                                                               |
| trend             | array  | 趋势：时间、价格、成交量、成交总额、平均价                             |
| trend_standard    | array  | 标准趋势：时间、开盘价、收盘价、最高价、最低价、成交量、成交总额、平均价 |

当接口返回业务错误时，脚本会输出：

```json
{
  "error": "api_error",
  "code": 210,
  "message": "没有信息"
}
```

## 常见错误码

来源于 [极速数据股票指数文档](https://www.jisuapi.com/api/stockindex/)：

| 代号 | 说明     |
|------|----------|
| 210  | 没有信息 |

系统错误码：101～108（与其它极速数据接口一致）。

## 推荐用法

1. 用户提问：「今天大盘指数怎么样？上证、深证、创业板都多少？」  
2. 代理调用：`python3 skills/stockindex/stockindex.py sh`  
3. 从返回数组中按 `name` 筛选「上证指数」「深证成指」「创业板指」等，提取 `price`、`lastclosingprice`、`openningprice`，用自然语言汇总涨跌与点位；若用户需要分钟走势，可说明 `trend` / `trend_standard` 可用于绘图。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

