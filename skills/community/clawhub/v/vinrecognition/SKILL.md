---
name: "VIN Recognition OCR - VIN识别"
description: 对车架号/VIN 图片做识别并返回 VIN 及品牌厂家等信息。当用户说：拍了一张车架号照片帮我识别、从图里读出 VIN，或类似 VIN 图片识别时，使用本技能。
metadata: { "openclaw": { "emoji": "🚗", "requires": { "bins": ["python3"], "env": ["JISU_API_KEY"] }, "primaryEnv": "JISU_API_KEY" } }
---

## 极速数据 VIN 识别（Jisu VINRecognition）

> 数据由 **[极速数据（JisuAPI）](https://www.jisuapi.com/)** 提供 — 国内专业的 API 数据服务平台，提供生活常用、交通出行、工具万能等数据接口。

- 对车辆挡风玻璃处或行驶证上的车架号照片进行 OCR 识别；
- 返回车架号 VIN、是否正确标记、品牌、厂家名称等信息。

适合用于车辆验真、档案录入、二手车评估等场景。

## 前置配置：获取 API Key

1. 前往 [极速数据官网](https://www.jisuapi.com/) 注册账号
2. 进入 [VIN 识别 API](https://www.jisuapi.com/api/vinrecognition/) 页面，点击「申请数据」
3. 在会员中心获取 **AppKey**
4. 配置 Key：


```bash
# Linux / macOS
export JISU_API_KEY="your_appkey_here"

# Windows PowerShell
$env:JISU_API_KEY="your_appkey_here"
```

## 脚本路径

脚本文件：`skills/vinrecognition/vinrecognition.py`

## 使用方式

当前脚本通过调用 `/vinrecognition/recognize` 接口，对单张图片进行 VIN 识别。

### 1. 从本地图片识别 VIN

```bash
python3 skills/vinrecognition/vinrecognition.py '{"path":"vin.jpg"}'
```

### 2. 直接传 base64 图片内容

```bash
python3 skills/vinrecognition/vinrecognition.py '{
  "pic": "<base64-encoded-image>"
}'
```

> 提示：`pic` 字段是图片二进制内容的 base64 编码（不带 `data:image/...;base64,` 前缀），  
> 也可以使用 `image` / `file` 字段传本地路径，脚本会自动读取并转为 base64。

## 请求参数

JSON 请求体字段说明：

| 字段名 | 类型   | 必填 | 说明 |
|--------|--------|------|------|
| pic    | string | 否   | 图片 base64 内容（与 `path/image/file` 至少二选一） |
| path   | string | 否   | 本地图片路径 |
| image  | string | 否   | 本地图片路径（同 `path`） |
| file   | string | 否   | 本地图片路径（同 `path`） |

当未提供 `pic` 时，脚本会优先从 `path`/`image`/`file` 中读取本地图片并进行 base64 编码。

## 返回字段

成功时，脚本直接输出接口 `result` 字段，典型结构：

```json
{
  "vin": "LFV2A21K0G4053021",
  "iscorrect": 1,
  "brand": "大众",
  "manufacturer": "一汽大众"
}
```

字段说明：

| 字段名       | 类型   | 说明                         |
|--------------|--------|------------------------------|
| vin          | string | 识别出的车架号               |
| iscorrect    | int    | 是否返回正确车架号：1 是，0 否 |
| brand        | string | 品牌                         |
| manufacturer | string | 厂家名称                     |

当出现错误（如图片为空、格式不对、超过大小限制等）时，脚本会输出统一错误结构：

```json
{
  "error": "api_error",
  "code": 201,
  "message": "图片为空"
}
```

## 常见错误码

业务错误码（来源于官网文档）：

| 代号 | 说明               |
|------|--------------------|
| 201  | 图片为空           |
| 202  | 图片格式错误       |
| 203  | 图片大小超过 300K  |
| 204  | 识别失败           |

系统错误码：

| 代号 | 说明             |
|------|------------------|
| 101  | APPKEY 为空或不存在 |
| 102  | APPKEY 已过期    |
| 103  | APPKEY 无请求此数据权限 |
| 104  | 请求超过次数限制   |
| 105  | IP 被禁止       |
| 106  | IP 请求超过限制   |
| 107  | 接口维护中       |
| 108  | 接口已停用       |

## 推荐用法

1. 用户上传一张挡风玻璃或行驶证照片，提问：「帮我识别下这辆车的 VIN、品牌和厂家」。  
2. 代理将图片保存为临时文件路径（如 `vin.jpg`），调用：  
   `python3 skills/vinrecognition/vinrecognition.py '{"path":"vin.jpg"}'`  
3. 从返回结果中读取 `vin/iscorrect/brand/manufacturer` 字段，用自然语言总结给用户；如有需要，还可以结合 `vin/query` 接口获取更详细的车辆配置信息。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

