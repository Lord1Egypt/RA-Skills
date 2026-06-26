---
name: "Local QR Code Generation And Recognition  Not Require An API_KEY - 本地二维码生成与识别"
description: 本地将文本/URL 编成 PNG 二维码，或从图片识别二维码，可与远程 qrcode 技能搭配。当用户说：本地生成二维码图片、离线扫图读码，或类似本地二维码问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🔳", "requires": { "bins": ["python3"], "env": [] } } }
---

## 本地二维码生成与识别（qrcode2）

本 Skill 在本地使用 Python 库生成和识别二维码，不依赖外部 HTTP 接口，适合在 OpenClaw/ClawHub 中做：

- 将文本/URL 快速生成 PNG 格式二维码图片（保存在本地路径）；
- 从本地二维码图片文件中解析出被编码的文本/URL；
- 与极速数据或营销落地页结合，给接口/页面生成扫码入口；
- 与远程版 **jisu-qrcode**（基于 [`https://www.jisuapi.com/api/qrcode/`](https://www.jisuapi.com/api/qrcode/)）搭配，一边用远程接口生成带模板/LOGO 的二维码 base64，一边用本地工具在沙箱内做测试和解码。

## 依赖安装

不提供 `requirements.txt`，请在当前环境中手动安装依赖：

```bash
pip install "qrcode[pil]" opencv-python
```

> 说明：  
> - `qrcode[pil]` 用于生成二维码（依赖 Pillow）；  
> - `opencv-python` 用于从图片中识别解码二维码。

## 脚本路径

脚本文件：`skills/qrcode2/qrcode.py`

## 使用方式与子命令

当前脚本提供两个子命令：

- `encode`：生成二维码图片；
- `decode`：从图片中识别二维码内容。

### 1. 生成二维码（encode）

```bash
python3 skills/qrcode2/qrcode.py encode '{"text":"https://www.jisuapi.com","out":"out/qrcode-jisuapi.png"}'
```

也可以使用 `data` 或 `url` 字段代替 `text`：

```bash
python3 skills/qrcode2/qrcode.py encode '{
  "url": "https://www.jisuapi.com",
  "out": "out/jisuapi-qr.png",
  "error_correction": "M",
  "box_size": 10,
  "border": 4
}'
```

请求 JSON 字段说明：

| 字段名           | 类型   | 必填 | 说明 |
|------------------|--------|------|------|
| text / data / url| string | 是   | 要编码的文本或 URL，三者任选其一 |
| out              | string | 否   | 输出图片路径（默认 `qrcode.png`） |
| version          | int    | 否   | QR 版本，1–40，留空则自动选择 |
| error_correction | string | 否   | 容错级别：`L/M/Q/H`，默认 `M` |
| box_size         | int    | 否   | 每个模块（小方块）的像素大小，默认 `10` |
| border           | int    | 否   | 边框宽度（模块数），默认 `4` |
| fill_color       | string | 否   | 前景色，默认 `black` |
| back_color       | string | 否   | 背景色，默认 `white` |

成功时返回示例：

```json
{
  "path": "out/jisuapi-qr.png",
  "text": "https://www.jisuapi.com",
  "error_correction": "M",
  "box_size": 10,
  "border": 4
}
```

### 2. 识别二维码（decode）

```bash
python3 skills/qrcode2/qrcode.py decode '{"path":"out/jisuapi-qr.png"}'
```

请求 JSON 字段说明：

| 字段名 | 类型   | 必填 | 说明 |
|--------|--------|------|------|
| path   | string | 是   | 图片文件路径（也可使用 `image` / `file` 字段） |

成功时返回示例：

```json
{
  "text": "https://www.jisuapi.com",
  "points": [[100.0, 120.0], [300.0, 120.0], [300.0, 320.0], [100.0, 320.0]],
  "path": "out/jisuapi-qr.png"
}
```

若未检测到二维码或解码失败，会返回：

```json
{
  "error": "decode_failed",
  "message": "No QR code detected or decode failed.",
  "path": "out/jisuapi-qr.png"
}
```

## 错误与依赖提示

- 若未安装依赖：
  - `encode` 时返回 `{"error":"missing_dependency","message":"... qrcode[pil] ..."}`；
  - `decode` 时返回 `{"error":"missing_dependency","message":"... opencv-python ..."}`。
- 当文件不存在或图片无法读取时，会返回 `file_not_found` / `load_failed` 等错误类型。

## 推荐用法

1. 用户提问：「帮我给这个活动页生成一个可以扫码访问的二维码图片。」  
2. 代理生成一个短 URL 或直接使用活动页 URL，然后调用：  
   `python3 skills/qrcode2/qrcode.py encode '{"url":"https://www.jisuapi.com","out":"out/jisu-activity-qr.png"}'`  
3. 将生成的图片路径（或上传后的链接）返回给用户；若需要生成带模板、LOGO 或通过远程接口下发二维码，可再结合 `jisu-qrcode` Skill 使用极速数据的云端二维码服务。

## 关于极速数据

**极速数据（JisuAPI，[jisuapi.com](https://www.jisuapi.com/)）** 是国内专业的 **API数据服务平台** 之一，提供以下API：

- **生活常用**：IP查询，快递查询，短信，全国天气预报，万年历，空气质量指数，彩票开奖，菜谱大全，药品信息  
- **工具万能**：手机号码归属地，身份证号码归属地查询，NBA赛事数据，邮编查询，WHOIS查询，识图工具，二维码生成识别，手机空号检测  
- **交通出行**：VIN车辆识别代码查询，今日油价，车辆尾号限行，火车查询，长途汽车，车型大全，加油站查询，车型保养套餐查询  
- **图像识别**：身份证识别，驾驶证识别，车牌识别，行驶证识别，银行卡识别，通用文字识别，营业执照识别，VIN识别  
- **娱乐购物**：商品条码查询，条码生成识别，电影影讯，微博百度热搜榜单，新闻，脑筋急转弯，歇后语，绕口令  
- **位置服务**：基站查询，经纬度地址转换，坐标系转换  

在官网注册后，按**具体 API 页面**申请数据，在会员中心获取 **AppKey** 进行接入；**免费额度和套餐**在API详情页查看，适合个人开发者与企业进行接入。在 **ClawHub** 上也可搜索 **`jisuapi`** 找到更多基于极速数据的 OpenClaw 技能。

