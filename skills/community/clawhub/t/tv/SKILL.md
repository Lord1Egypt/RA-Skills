---
name: "TV Program Preview - 电视节目预告"
description: 按频道与日期查电视节目单，可查频道列表。当用户说：央视一套今晚有什么节目？湖南卫视节目表，或类似电视节目问题时，使用本技能。
metadata: { "openclaw": { "emoji": "📺", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

# 极速数据电视节目预告（Jisu TV）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- **电视节目查询**（`/tv/query`）
- **电视节目频道列表**（`/tv/channel`）

可用于对话中回答「今晚 CCTV-3 有什么节目」「帮我看明天湖南卫视的晚间综艺」「有哪些可用频道及 ID」等问题。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [电视节目预告 API](https://www.jisuapi.com/api/tv/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/tv/tv.py`

## 使用方式

### 1. 获取频道列表（channel）

```bash
python3 skills/tv/tv.py channel
```

返回值为频道数组，每项包含：

- `tvid`：电视频道 ID  
- `name`：电视频道名称  
- `parentid`：上级 ID  
- `istv`：是否为电视频道（1 是，0 否）  

### 2. 查询某频道在某日的节目单（query）

```bash
python3 skills/tv/tv.py query '{"tvid":435,"date":"2015-10-19"}'
```

## 请求参数

### /tv/query

| 字段名 | 类型   | 必填 | 说明           |
|--------|--------|------|----------------|
| tvid   | int    | 是   | 电视频道 ID     |
| date   | string | 是   | 日期，格式 `YYYY-MM-DD` |

### /tv/channel

无请求参数。

## 返回结果示例

### /tv/query

脚本直接输出接口的 `result` 字段，例如（节选自官网示例）：

```json
{
  "tvid": "435",
  "name": "CCTV-3（综艺）",
  "date": "2015-08-09",
  "program": [
    {
      "name": "综艺喜乐汇",
      "starttime": "01:18"
    },
    {
      "name": "2014中国梦-我梦最美",
      "starttime": "03:55"
    }
  ]
}
```

字段说明：

| 字段名    | 类型     | 说明           |
|-----------|----------|----------------|
| tvid      | int      | 电视频道 ID     |
| name      | string   | 电视频道名称    |
| date      | string   | 日期           |
| program   | array    | 节目列表        |
| program[].name | string | 节目名称    |
| program[].starttime | string | 开始时间 |

### /tv/channel

返回数组，每项形如：

```json
{
  "tvid": "2381",
  "name": "中国美食",
  "parentid": "4",
  "istv": "1"
}
```

## 错误返回示例

```json
{
  "error": "api_error",
  "code": 201,
  "message": "电视节目频道为空"
}
```

## 常见错误码

来源于 [极速数据电视节目预告文档](https://www.jisuapi.com/api/tv/)：

| 代号 | 说明           |
|------|----------------|
| 201  | 电视节目频道为空 |
| 202  | 电视节目频道错误 |
| 203  | 没有信息       |

系统错误码：101 APPKEY 为空或不存在、102 已过期、103 无请求此数据权限、104 请求超过次数限制、105 IP 被禁止、106 IP 请求超过限制、107 接口维护中、108 接口已停用。

## 推荐用法

1. 用户：「今晚 8 点有什么好看的综艺？」→ 先通过 `channel` 找到相关卫视或 CCTV 综艺频道的 `tvid`，再用 `query` 拉取当天节目单，根据时间筛选并用自然语言总结。  \n
2. 用户：「列出下周湖南卫视的晚间节目」→ 使用 `channel` 获取湖南卫视 `tvid`，对未来一周的日期依次调用 `query`，抽取 19:00–24:00 时段的节目并按日期分组展示。  \n
3. 用户：「支持哪些频道？」→ 直接调用 `channel`，罗列 `name` 与 `tvid`，便于后续对话中用频道 ID 精确查询。  \n

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

