---
name: "Historical Weather - 历史天气"
description: 按城市与日期查询历史天气（温湿度、风、气压、AQI 等）。当用户说：去年今天北京多少度？查一下 2023 年 7 月上海历史天气，或类似历史气温问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🌤", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据历史天气（Jisu Weather2）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [历史天气 API](https://www.jisuapi.com/api/weather2/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/weather2/weather2.py`

## 使用方式

### 1. 历史天气查询（query）

```bash
python3 skills/weather2/weather2.py query '{"city":"北京","date":"2018-01-01"}'
python3 skills/weather2/weather2.py query '{"cityid":111,"date":"2018-01-01"}'
```

| 参数   | 类型   | 必填 | 说明 |
|--------|--------|------|------|
| city   | string | 否   | 城市名（与 cityid 二选一） |
| cityid | int    | 否   | 城市 ID（见 city 命令）   |
| date   | string | 是   | 日期，格式 2018-01-01，默认为昨天 |

返回字段示例：cityid, cityname, date, weather, temphigh, templow, img, humidity, pressure, windspeed, windpower, sunrise, sunset, aqi, primarypollutant 等。

### 2. 获取城市列表（city）

```bash
python3 skills/weather2/weather2.py city '{}'
```

无参数，返回支持历史天气查询的城市列表（cityid, parentid, citycode, city）。

## 常见错误码

| 代号 | 说明           |
|------|----------------|
| 201  | 城市和城市ID都为空 |
| 202  | 城市不存在     |
| 203  | 查询日期为空   |
| 204  | 日期格式不正确 |
| 210  | 没有信息       |

系统错误码 101–108 见极速数据官网。

## 推荐用法

1. 用户问「北京 2018 年 1 月 1 日天气如何」时，先调用 `query`，传入 `city`（或 `cityid`）与 `date`。
2. 若需城市 ID，可先调用 `city` 获取列表再查。
3. 从返回的 result 中取 weather、temphigh、templow、aqi 等用自然语言回复。更多接口与计费见 [极速数据](https://www.jisuapi.com/)。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

