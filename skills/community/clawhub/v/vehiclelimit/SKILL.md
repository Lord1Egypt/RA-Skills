---
name: "Vehicle License Plate Number Restriction - 车辆尾号限行"
description: 查询城市限行规则与尾号，可查支持城市列表。当用户说：北京明天限行尾号是几？成都限行区域怎么算？或类似限行问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🚗", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据车辆尾号限行（Jisu VehicleLimit）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **获取城市列表**（`/vehiclelimit/city`）
- **城市限行查询**（`/vehiclelimit/query`）

目前支持北京、天津、杭州、成都、兰州、贵阳、南昌、长春、哈尔滨、武汉、上海、深圳等城市。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [车辆尾号限行 API](https://www.jisuapi.com/api/vehiclelimit/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/vehiclelimit/vehiclelimit.py`

## 使用方式

### 1. 获取支持限行的城市列表（/vehiclelimit/city）

```bash
python3 skills/vehiclelimit/vehiclelimit.py cities
```

返回结果示例：

```json
[
  {
    "city": "beijing",
    "cityname": "北京"
  },
  {
    "city": "hangzhou",
    "cityname": "杭州"
  }
]
```

### 2. 查询城市在某日的限行信息（/vehiclelimit/query）

```bash
python3 skills/vehiclelimit/vehiclelimit.py '{"city":"hangzhou","date":"2015-12-02"}'
```

请求 JSON 示例：

```json
{
  "city": "hangzhou",
  "date": "2015-12-02"
}
```

## 请求参数

### 城市列表

无需额外参数，仅需 `appkey`。

### 限行查询

| 字段名 | 类型   | 必填 | 说明                           |
|--------|--------|------|--------------------------------|
| city   | string | 是   | 城市代号，如 `hangzhou`       |
| date   | string | 是   | 日期，格式如 `2015-12-02`      |

## 返回结果示例（限行查询）

```json
{
  "city": "hangzhou",
  "cityname": "杭州",
  "date": "2015-12-03",
  "week": "星期四",
  "time": [
    "07:00-09:00",
    "16:30-18:30"
  ],
  "area": "1、本市号牌：留祥路—石祥路—石桥路……\n2、外地号牌：上述“错峰限行”区域以及绕城高速合围区域内的其他高架道路……",
  "summary": "本市号牌尾号限行，外地号牌全部限行。法定上班的周六周日不限行。",
  "numberrule": "最后一位数字",
  "number": "4和6"
}
```

## 常见错误码

来源于 [极速数据车辆尾号限行文档](https://www.jisuapi.com/api/vehiclelimit/)：

| 代号 | 说明       |
|------|------------|
| 201  | 城市为空   |
| 202  | 城市不存在 |
| 210  | 没有信息   |

系统错误码：

| 代号 | 说明                 |
|------|----------------------|
| 101  | APPKEY 为空或不存在  |
| 102  | APPKEY 已过期        |
| 103  | APPKEY 无请求权限    |
| 104  | 请求超过次数限制     |
| 105  | IP 被禁止            |

## 推荐用法

1. 用户提问：「明天杭州限行什么尾号？」  
2. 代理先使用 `cities` 子命令确认 `hangzhou` 在支持列表中（可缓存），然后构造 JSON：`{"city":"hangzhou","date":"2025-04-22"}` 并调用：  
   `python3 skills/vehiclelimit/vehiclelimit.py '{"city":"hangzhou","date":"2025-04-22"}'`  
3. 从返回结果中读取 `time`、`area`、`summary`、`numberrule` 和 `number` 字段，为用户生成简要说明：当天何时、何地、哪些尾号限行。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

