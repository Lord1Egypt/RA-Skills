---
name: wps-ocr
description: 一款轻量级高性能文件解析工具，可快速、精准的将文件中的文字、手写体文字、公式、表格、文件、印章提取为Markdown结构，适配各类常见文件场景（文档扫描件、屏幕截图、普通照片等），支持多种文件格式（JPG、PNG、BMP、HEIF、WEBP），是文本数字化处理的高效工具。

metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      pip:
        - requests
    required_env_vars:
      - WPS_OCR_CLIENT_SECRET
    allowed_domains:
      - aiwrite.wps.cn
    security_notes: "Requires WPS OCR credentials via environment variables. No credential hardcoding. Enforces domain allowlist in code."
---

# 🧭 使用前必读（30秒）

> [!WARNING] 
> **⚠️ 隐私与数据流向重要提示**
> - **需要与服务交互**：本技能会将您提供的**文件 发送至金山办公官方服务器 (`aiwrite.wps.cn`)** 进行识别。
> - **数据可见性**：金山办公服务将获取并处理该文件内容。
> - **本skill支持本地文件上传，只会对文件类型做校验，不会对路径做任何校验**

✅ **推荐方式：环境变量（免权限、即时生效、webchat 友好）**
```bash
# 在终端中运行（本次会话立即可用）：
export WPS_OCR_ACCESS_KEY="your_client_access_key_here"
```

```bash
# 将密钥追加写入到 ~/.openclaw/env 文件
echo 'export WPS_OCR_ACCESS_KEY="your_client_access_key_here"' >> ~/.openclaw/env
```

> [!TIP] **🔧 如何获取密钥？**
> - 秘钥申请获取：https://aiwrite.wps.cn/pdf/parse/accesskey/

✅ 环境依赖检查
确保已安装必要库：
```bash
pip install requests
```

# 🎯 技能执行指南

## 1. 适用场景
当用户意图包含以下任一情况时，调用此技能：
- 发送了一张文件并询问“这是什么字？”、“提取文字”、“转成文本”。
- 上传了文档截图、发票、名片、照片、扫描件，文件里中英文混排文本识别。
- 需要对文件内容进行翻译或编辑（先提取文本是必要步骤）。

## 2. 执行动作 
一旦确认需要提取文本，请立即执行以下操作：

**输入处理**:
获取用户提供的文件资源（使用下载链接：`url`或者 本地文件：`path`）。

**执行命令**:
调用python脚本进行识别。若当前环境支持命令行执行，请构造如下命令：

```bash
# 使用下载链接：
python3 skills/wps-ocr/scripts/wps_ocr.py --url <用户提供的文件 URL>
# 本地文件：
python3 skills/wps-ocr/scripts/wps_ocr.py --path <用户提供的文件 PATH>
```

# 执行流程
## 1. 获取文件
将文件数据发往金山办公云服务，服务会下载用户输入的文件。

## 2. 文件校验
校验文件是否为已经支持的文件格式。

## 3. 识别文件内容
识别文件中的文本、图片、表格、公式等等元素，提取其中的文本内容。

**⚠️ 注意：图片元素会以占位符的形式返回，不会返回文件元素**

## 4. 向用户返回结果
如果成功：返回所有识别出的文本（拼接成一句）和详细检测信息。

如果失败：返回错误信息（如“文件中未检测到文本”、“API调用失败”等）。

# OCR接口调用说明：
本技能依托WPS-OCR解析识别能力，已托管在金山云服务，当前版本为免费试用版本，为了保证云服务运行稳定，云服务做了限流处理，并发过高的情况服务将拒绝响应，请合理使用。

体验完整功能可以访问 [demo平台](https://aiwrite.wps.cn/pdf/parse/web/])