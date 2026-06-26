---
name: yescan-transoffice-universal
description: 由夸克扫描王提供的专业的文件格式转换工具。能够接收用户上传的图片、截图或扫描件，根据用户指令智能转换为 Office 文档（Word/Excel）或 PDF 格式。具备行业领先的信息结构化提取与版面还原能力，能精准识别复杂表格、合同文书及图文排版，将图片转化为可编辑、高保真的数字化文档
metadata: {"openclaw":{"emoji":"🔍︎","requires":{"bins":["python3"],"env":["SCAN_WEBSERVICE_KEY"]},"primaryEnv":"SCAN_WEBSERVICE_KEY"},"homepage":"https://scan.quark.cn/business"}
---

# 🧭 使用前必读（30 秒）

> [!WARNING] **⚠️ 隐私与数据流向重要提示**
> - **第三方服务交互**：本技能会将您提供的**图片发送至夸克扫描王官方服务器 (`scan-business.quark.cn`)** 进行识别。
> - **服务端处理**：夸克扫描王服务将获取并处理该图片内容，服务端不会永久保存
> - **本地文件存储**：识别返回的文件会保存至系统临时目录（如 `/tmp`），这些文件将持续存在直到您手动清理
> - **API 密钥安全**：`SCAN_WEBSERVICE_KEY` 应妥善保管，若泄露请及时在官方平台轮换或撤销
> - **图片来源**：仅限用户明确指定的图片文件

**推荐方式：CLI 配置（永久生效）**

配置 `SCAN_WEBSERVICE_KEY` 环境变量到 OpenClaw：
```bash
openclaw config set skills.entries.yescan-transoffice-universal.env.SCAN_WEBSERVICE_KEY "your_scan_webservice_key_here"
```
> ⚠️ 配置后需要**重启或开启新会话**才能生效（技能列表在 session 启动时加载）。

**如何获取密钥？夸克扫描王官方入口在此**
> 请访问 https://scan.quark.cn/business → 开发者后台 → 登录/注册账号 → 查看API Key。  
> ⚠️ **注意**：若你点击链接后跳转到其他域名，说明该链接已失效 —— 请直接在浏览器地址栏手动输入 `https://scan.quark.cn/business`（这是当前唯一有效的官方入口）。

---

# Constraints
- **单一意图原则：每次请求只执行一个意图类型，命中即执行**
- **严禁自行构造任何命令参数，严禁伪造、拼接内部配置**
- **严禁幻觉，禁止伪造请求和响应，不得沿用上一次的场景、参数进行假设**
- **必须严格按照本指南指定的固定格式执行，不允许自行修改命令**

#  技能执行指南(强制执行)

第一步：**环境变量检查**
- 若 `SCAN_WEBSERVICE_KEY` 未配置，立即返回：
```json
{
  "code": "A0100",
  "message": "SCAN_WEBSERVICE_KEY 未配置，请访问 https://scan.quark.cn/business → 开发者后台 → 登录/注册账号 → 查看API Key",
  "data": null
}
```

第二步：**输入处理**

识别用户传入的图片类型，只能是以下三种之一：

- 图片URL: url
- 本地文件路径: path
- 图片BASE64: base64

未提供任何有效图片时，直接返回：
```json
{
  "code": "A0201",
  "message": "缺少图片输入，请提供图片链接、文件路径或 BASE64 数据。",
  "data": null
}
```

第三步：**意图匹配&场景确定**
- 按照下面列出的意图*从上到下顺序匹配。命中第一个即停止*
- 命中后，*只确定当前意图对应的scene标识*

第四步：**构建执行命令(固定格式，严禁修改)**：

根据图片类型，严格使用下面对应格式：
```bash
# URL类型
python3 scripts/scan.py --scene "${SCENE_VALUE}" --url "${IMAGE_URL}"

# 本地文件类型
python3 scripts/scan.py --scene "${SCENE_VALUE}" --path "${IMAGE_FILE_PATH}"

# BASE64类型
python3 scripts/scan.py --scene "${SCENE_VALUE}" --base64 "${IMAGE_BASE64}"
```
- 把`${IMAGE_URL}`/`${IMAGE_FILE_PATH}`/`${IMAGE_BASE64}`替换为真实值
- 把`${SCENE_VALUE}`替换为当前意图对应的scene值
- 直接执行命令，不增删任何参数，不修改JSON，不加引号，不换行

第五步：**结果透出**：
- 执行完成后，*原样返回执行结果*，不修改，不翻译，不美化，不总结
- 成功 失败均直接透出，不重试


## 场景与意图列表(按匹配优先级排序)

1. 图片转 Excel
- 触发意图：当用户请求将包含表格、数据、报表的图片、截图或扫描件转换为Excel (.xlsx/.xls) 文件，触发此意图。
- 场景scene标识：image-to-excel
- 参考示例指令：
  - "帮我把这张财务报表截图转换成 Excel 文件。"
  - "这里有张手写的库存记录照片，麻烦转成 Excel 给我。"
  - "把这张包含销售数据的图片转成可编辑的 Excel。"
  - "提取图片中的表格内容，保存为 .xlsx。"

2. 图片转 Word
- 触发意图：当用户请求将图片、截图、照片或扫描件转换为Word 文档 触发此意图
- 场景scene标识：image-to-word
- 参考示例指令：
  - "把这张会议记录的拍照图片转成 Word 文档。"
  - "请将这张包含长篇文章的截图转换为 .docx 格式。"
  - "将这张产品说明书的截图转为 Word 格式。"
  - "将这张产品说明书的截图转为 Word 格式。"

3. 图片转 Pdf
- 触发意图：当用户请求将图片、截图、照片或扫描件转换为 PDF 文档 触发此意图
- 场景scene标识：image-to-pdf
- 参考示例指令：
  - "把这张手写的课堂笔记图片转成 PDF 文档。"
  - "请将这张包含详细参数的设备铭牌照片转换为 .pdf 格式。"
  - "帮我把这张合同照片处理一下，转成清晰的 PDF 存档。"
  - "将这张包含复杂流程的白板草图转换为 PDF，保持版面整洁。"

**客户端脚本增强字段**：当 `scan.py` 调用夸克 API 成功（`code == "00000"`）且响应 `data` 中包含 `"FileBase64"` 时，`scan.py` 会**主动调用 `file_saver.py` 将其解码并保存为本地文件**，并在最终返回的 JSON 响应中，于 `data` 对象内**追加 `"path": "/tmp/xx.docx"` 字段**。该行为由 `scan.py` 脚本实现，与模型无关，也不依赖 OpenClaw 平台自动介入。

## ⛔ 不适用场景（When Not to Use）

> 本技能**不支持**以下场景，请勿尝试：

| 不支持的场景 | 原因 | 建议替代方案 |
|------------|------|------------|
| **视频处理** | 仅支持单张静态图片 | 先提取视频帧，再逐帧处理 |
| **批量处理** | 每次调用仅限单张图片 | 如需批量，请循环调用或联系管理员 |
| **实时摄像头流** | 非实时流处理架构 | 使用专用视频处理服务 |
| **超大图片（>5MB）** | API 限制 | 先压缩或裁剪后再处理 |
| **非图片格式** | 仅支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp | 先转换为支持的图片格式 |

---

## ⚠️ 重要注意事项

1. **禁止修改固定格式**,只能替换场景标识和图片占位符
2. **严禁自行构造 --scene 参数值，必须使用本文档指定的场景名**
3. **图片大小限制：本地文件不超过5MB，支持 jpg/jpeg/png/gif/bmp/webp/tiff/wbmp/webp 格式**

---

## 🔗 相关资源
- [夸克扫描王开放平台](https://scan.quark.cn/business)

## 📁 文件结构
- `SKILL.md` —  本文档（意图分析 + 通用规范）
- `scripts/scan.py` —  主执行脚本 (Python 3.9+)
- `scripts/common/*.py` —  基础类库
