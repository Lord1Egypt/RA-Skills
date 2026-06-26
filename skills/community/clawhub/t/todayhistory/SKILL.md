---
name: "Today in History - 历史上的今天"
description: 按月日查询历史上同日大事、诞辰与逝世等。当用户说：历史上的今天发生了什么？3 月 15 日有什么大事？或类似历史纪事问题时，使用本技能。
metadata: { "openclaw": { "emoji": "📜", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据历史上的今天（Jisu TodayHistory）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

适合在对话中回答「今天在历史上发生了什么」「1 月 2 日有哪些大事」「帮我找几个今天相关的历史故事」等问题。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [历史上的今天 API](https://www.jisuapi.com/api/todayhistory/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/todayhistory/todayhistory.py`

## 使用方式与请求参数

当前脚本提供一个子命令：`query`，对应 `/todayhistory/query` 接口。

### 历史上的今天查询（/todayhistory/query）

```bash
python3 skills/todayhistory/todayhistory.py query '{"month":1,"day":2}'
```

请求 JSON：

```json
{
  "month": 1,
  "day": 2
}
```

| 字段名 | 类型   | 必填 | 说明 |
|--------|--------|------|------|
| month  | int    | 是   | 月   |
| day    | int    | 是   | 日   |

## 返回结果示例（节选）

```json
[
  {
    "title": "日俄战争：驻守旅顺的俄军向日军投降。",
    "year": "1905",
    "month": "1",
    "day": "2",
    "content": "……"
  },
  {
    "title": "意大利墨西拿发生地震，20万人丧生。",
    "year": "1909",
    "month": "1",
    "day": "2",
    "content": "……"
  }
]
```

常见字段说明：

| 字段名  | 类型     | 说明   |
|---------|----------|--------|
| title   | string   | 事件标题 |
| year    | string   | 年份    |
| month   | string   | 月份    |
| day     | string   | 日期    |
| content | string   | 事件内容 |

## 常见错误码

业务错误码（参考官网错误码参照）：

| 代号 | 说明     |
|------|----------|
| 201  | 没有信息 |

系统错误码：

| 代号 | 说明                     |
|------|--------------------------|
| 101  | APPKEY 为空或不存在     |
| 102  | APPKEY 已过期           |
| 103  | APPKEY 无请求此数据权限 |
| 104  | 请求超过次数限制         |
| 105  | IP 被禁止               |
| 106  | IP 请求超过限制         |
| 107  | 接口维护中               |
| 108  | 接口已停用               |

## 推荐用法

1. 用户提问：「今天在历史上发生了什么？」代理先确定当前日期，例如 1 月 2 日。  
2. 调用：`python3 skills/todayhistory/todayhistory.py query '{"month":1,"day":2}'`。  
3. 从返回列表中选取 3–5 条代表性事件，将 `year`、`title` 与 `content` 整理成时间线式的自然语言描述，作为回答给用户。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

