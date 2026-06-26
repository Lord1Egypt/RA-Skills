---
name: "Train Ticket Inquiry - 火车查询"
description: 支持站站、车次、余票查询，返回时刻、票价与余票等。当用户说：北京到上海今天还有高铁票吗？帮我查一下 G1 次列车经停站，或类似火车票、余票问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🚆", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据火车查询（Jisu Train）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **站站查询**（`/train/station2s`）
- **车次查询**（`/train/line`）
- **余票查询**（`/train/ticket`）

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [火车查询 API](https://www.jisuapi.com/api/train/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/train/train.py`

## 使用方式

### 1. 站站查询（/train/station2s）

```bash
python3 skills/train/train.py station2s '{"start":"杭州","end":"北京","ishigh":0}'
```

可选参数 `date`（不填则按接口默认）：

```bash
python3 skills/train/train.py station2s '{"start":"杭州","end":"北京","ishigh":0,"date":"2025-04-03"}'
```

### 2. 车次查询（/train/line）

```bash
python3 skills/train/train.py line '{"trainno":"G34"}'
```

可选参数 `date`：

```bash
python3 skills/train/train.py line '{"trainno":"G34","date":"2025-04-04"}'
```

### 3. 余票查询（/train/ticket）

```bash
python3 skills/train/train.py ticket '{"start":"杭州","end":"北京","date":"2015-10-20"}'
```

## 请求参数

### 站站查询

| 字段名  | 类型   | 必填 | 说明       |
|---------|--------|------|------------|
| start   | string | 是   | 出发站（中文） |
| end     | string | 是   | 到达站（中文） |
| ishigh  | int    | 否   | 是否高铁（0/1） |
| date    | string | 否   | 日期（可选） |

### 车次查询

| 字段名  | 类型   | 必填 | 说明     |
|---------|--------|------|----------|
| trainno | string | 是   | 车次号   |
| date    | string | 否   | 日期（可选） |

### 余票查询

| 字段名 | 类型   | 必填 | 说明       |
|--------|--------|------|------------|
| start  | string | 是   | 出发站（中文） |
| end    | string | 是   | 到达站（中文） |
| date   | string | 是   | 日期，格式如 `2015-10-20` |

## 返回结果示例（节选）

### 站站查询

```json
[
  {
    "trainno": "G34",
    "type": "高铁",
    "station": "杭州东",
    "endstation": "北京南",
    "departuretime": "07:18",
    "arrivaltime": "13:07",
    "costtime": "5时49分",
    "distance": "1279",
    "priceyd": "907.0",
    "priceed": "538.5"
  }
]
```

### 车次查询

```json
{
  "trainno": "G34",
  "type": "高铁",
  "list": [
    {
      "sequenceno": "1",
      "station": "杭州东",
      "arrivaltime": "-",
      "departuretime": "07:18",
      "stoptime": "0"
    }
  ]
}
```

### 余票查询

```json
[
  {
    "trainno": "G42",
    "type": "高铁",
    "station": "杭州东",
    "endstation": "北京南",
    "departuretime": "09:26",
    "arrivaltime": "16:06",
    "costtime": "06:40",
    "numsw": "6",
    "numyd": "无",
    "numed": "无"
  }
]
```

## 常见错误码

来源于 [极速数据火车文档](https://www.jisuapi.com/api/train/)：

| 代号 | 说明                 |
|------|----------------------|
| 201  | 车次为空             |
| 202  | 始发站或到达站为空   |
| 203  | 没有信息             |

## 推荐用法

1. 用户提问：「帮我查杭州到北京今天有哪些高铁？」  
2. 代理构造 JSON：`{"start":"杭州","end":"北京","ishigh":1}` 并调用：  
   `python3 skills/train/train.py station2s '{"start":"杭州","end":"北京","ishigh":1}'`  
3. 从返回结果中挑选合适车次（出发时间/到达时间/用时/票价），再用 `line` 查看经停站，或用 `ticket` 查询余票数量。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

