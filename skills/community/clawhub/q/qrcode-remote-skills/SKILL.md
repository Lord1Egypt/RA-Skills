---
name: qrcode-remote-skills
description: Generate and decode QR codes using CaoLiao QR Code API. Use when the user wants to create a QR code from text/URL, decode/read QR code content from an image, or asks about QR code generation and scanning.
---

# QR Code Generation & Decoding

使用草料二维码开放 API 生成和解码二维码，无需 API Key。

## 安全声明

- **隐私保护**：上传到服务端解码的二维码图片均为临时文件，过一段时间后会自动删除，不会长期存储，保障用户隐私。
- **依赖透明**：本 skill 使用的第三方库（zxingcpp、Pillow、qrcode、草料 API 等）均为公开、开源的第三方库，可自行审查。
- **本地优先**：解码优先在本地完成，仅在本地失败时才调用远程 API，减少数据传输。


## 运行时选择：Python 或 Node.js

所有脚本同时提供 Python 和 Node.js 两个版本，功能和参数完全一致。**执行任何脚本前，先确定运行时。**

**选择策略（首次执行脚本前完成）：**

1. 检测 Python 是否可用：`python --version`（或 `python3 --version`）
2. 若 Python 不可用，检测 Node.js：`node --version`
3. 两者都有时默认用 Python

**依赖检查与自动安装：**

确定运行时后，检查依赖是否已安装。若缺失则自动安装，无需询问用户：

- **Python**：检查 `pip list` 中是否包含关键包（如 `Pillow`），若缺失则执行：
  ```bash
  pip install -r requirements.txt
  ```
- **Node.js**：检查 skill 目录下是否存在 `node_modules/`，若缺失则执行：
  ```bash
  npm install
  ```

安装完成后再执行脚本。若安装失败，提示用户手动安装。

**命令对照表：**

| 功能 | Python | Node.js |
|------|--------|---------|
| 单个生成保存 | `python scripts/generate.py ...` | `node scripts/generate.js ...` |
| 单个解码 | `python scripts/decode.py ...` | `node scripts/decode.js ...` |
| 批量生成 | `python scripts/batch_generate.py ...` | `node scripts/batch_generate.js ...` |
| 批量解码 | `python scripts/batch_decode.py ...` | `node scripts/batch_decode.js ...` |

所有参数名、输出 JSON 格式完全相同，仅将 `python` 替换为 `node`、`.py` 替换为 `.js`。

**差异说明：**
- Python 版本地解码使用 `zxingcpp`，输出 `"source": "zxing"`
- Node.js 版本地解码使用 [`qr-scanner-wechat`](https://github.com/antfu/qr-scanner-wechat)（基于 OpenCV + 微信算法，识别率更高），输出 `"source": "wechat-qr"`

---

## 生成二维码

将文本或 URL 编码为二维码图片，直接返回图片 URL 并提供预览。

**API 端点：** `https://api.2dcode.biz/v1/create-qr-code`

### 使用步骤

1. 获取用户要编码的文本内容
2. 对文本内容进行 URL 编码
3. 拼接生成 API URL
4. 将 URL 直接返回给用户，并以 Markdown 图片语法提供预览

### 参数说明

| 参数 | 必选 | 默认值 | 说明 |
|------|------|--------|------|
| data | 是 | - | 二维码中的文本内容（需 URL 编码），建议不超过 900 字符 |
| size | 否 | 256x256 | 图片尺寸，格式 `WxH` 或单个整数 |
| format | 否 | png | 输出格式：`png`（位图）或 `svg`（矢量） |
| error_correction | 否 | M | 纠错级别：L(7%) / M(15%) / Q(25%) / H(30%) |
| border | 否 | 2 | 边框宽度（码点为单位） |

### 场景一：仅生成（默认）

用户没有明确要求保存到本地时，直接拼接 URL 返回，**无需执行脚本**。

输出格式：

```
二维码已生成：

![QR Code](https://api.2dcode.biz/v1/create-qr-code?data=<URL编码文本>&size=400x400)

**二维码链接：** https://api.2dcode.biz/v1/create-qr-code?data=<URL编码文本>&size=400x400
```

### 场景二：生成并保存到本地

当满足以下任一条件时，使用 Shell 工具执行 `scripts/generate.py` 保存到本地：

- 用户明确要求"保存到本地"、"下载"、"导出文件"
- 用户指定了具体的保存路径（如 `保存到 D:\qr.png`、`放到桌面`、`存到 ./output/` 等）

```bash
python scripts/generate.py --data <文本内容> --output <保存路径> [--size 400x400] [--format png] [--error-correction M] [--border 2]
```

- `--output` 为用户指定的保存路径，若用户未指定文件名则默认使用 `qrcode.png`（svg 格式用 `qrcode.svg`）
- 脚本会自动创建不存在的父目录

脚本输出 JSON：

```json
{"url": "https://api.2dcode.biz/v1/create-qr-code?data=...", "file": "D:\\path\\to\\qrcode.png"}
```

失败时：

```json
{"error": "下载失败: ..."}
```

呈现给用户的格式：

```
二维码已生成并保存到本地：

![QR Code](<url>)

**二维码链接：** <url>
**本地文件：** <file>
```

### 示例

用户输入：`帮我生成一个二维码，内容是 https://example.com`

```
二维码已生成：

![QR Code](https://api.2dcode.biz/v1/create-qr-code?data=https%3A%2F%2Fexample.com&size=400x400)

**二维码链接：** https://api.2dcode.biz/v1/create-qr-code?data=https%3A%2F%2Fexample.com&size=400x400
```

用户输入：`生成一个二维码保存到桌面，内容是 Hello World，SVG 格式、最高纠错`

执行：`python scripts/generate.py --data "Hello World" --output "C:\Users\xxx\Desktop\qrcode.svg" --format svg --error-correction H`

```
二维码已生成并保存到本地：

![QR Code](https://api.2dcode.biz/v1/create-qr-code?data=Hello%20World&size=400x400&format=svg&error_correction=H)

**二维码链接：** https://api.2dcode.biz/v1/create-qr-code?data=Hello%20World&size=400x400&format=svg&error_correction=H
**本地文件：** C:\Users\xxx\Desktop\qrcode.svg
```

### 场景三：批量生成

当用户提供 Excel/CSV/TXT 文件要求批量生成二维码时，**先询问用户需要生成 URL 链接还是图片文件**，然后使用 `scripts/batch_generate.py` 对应模式执行。

**交互流程：**

1. 用户提供批量数据文件
2. **询问用户**：需要生成二维码 URL 链接，还是生成图片保存到本地？
3. 执行对应模式的脚本
4. 若返回 `need_column`，展示列信息，询问用户选哪一列，加 `--column` 重新执行
5. 成功后向用户报告结果

**列检测逻辑（Excel/CSV）：**
- 自动检测：扫描首行表头，匹配关键词（data/text/content/url/内容/文本/数据/链接 等）
- 若只有一列，直接使用
- 若无法判断，脚本返回 `need_column` JSON，此时**需要询问用户指定哪一列**

**TXT：** 每行一条数据，无需列选择。

#### URL 模式（生成链接）

直接拼接二维码 URL 列表返回，无需网络、无需本地库，速度最快。

```bash
python scripts/batch_generate.py --input <文件> --mode url [--column <列名或索引>] [--output-txt <保存路径>] [--size 400] [--error-correction M] [--border 2]
```

- 不加 `--output-txt`：返回 JSON 中直接包含 `urls` 数组
- 加 `--output-txt`：额外将链接列表保存到 TXT 文件（每行一个链接）

脚本输出 JSON：

```json
{"mode": "url", "total": 100, "urls": ["https://api.2dcode.biz/v1/create-qr-code?data=...", ...], "output_txt": "D:\\output\\urls.txt"}
```

呈现给用户的格式（数量较少时直接列出）：

```
批量生成完成，共 <total> 个二维码链接：
1. <url1>
2. <url2>
...
```

数量较多时（>20）建议保存到 TXT：

```
批量生成完成，共 <total> 个二维码链接，已保存到：<output_txt>
```

#### Image 模式（生成图片）

生成图片保存到本地目录。默认用本地 `qrcode` 库，单条失败时 API 兜底。

```bash
python scripts/batch_generate.py --input <文件> --mode image --output-dir <输出目录> [--column <列名或索引>] [--zip] [--size 400] [--format png] [--error-correction M] [--border 2] [--use-api]
```

- 默认本地 `qrcode` 库生成，本地库未安装时报错提示安装
- 单条本地生成失败时自动用远程 API 兜底
- `--use-api`：强制全部走远程 API
- 以索引命名（`1.png`, `2.png`, ...）
- `--zip`：打包输出目录为 zip

脚本输出 JSON：

```json
{"mode": "image", "source": "local", "total": 100, "success": 98, "failed": 2, "api_fallback": 3, "output_dir": "D:\\output", "zip_file": "D:\\output.zip", "errors": [...]}
```

呈现给用户的格式：

```
批量生成完成（via <source>）：共 <total> 个，成功 <success> 个，失败 <failed> 个
输出目录：<output_dir>
ZIP 文件：<zip_file>（仅打包时显示）
```

---

## 解码二维码

从二维码图片中读取/解码内容。优先使用本地 zxing 解码，失败时自动回退到草料 API。

### 前置依赖

首次使用前，需安装 Python 依赖（skill 目录下执行）：

```bash
pip install -r requirements.txt
```

### 解码策略（所有解码场景共用）

1. **本地 zxing 优先**：使用 `zxingcpp` + `Pillow` 在本地解码，速度快、无网络依赖
2. **API 回退**：若 zxing 未安装或解码失败，自动调用草料 API（`https://api.2dcode.biz/v1/read-qr-code`）
   - 本地文件 → POST multipart 上传
   - 图片 URL → GET 请求

### 场景一：单张解码

通过 Shell 工具执行 `scripts/decode.py`，支持本地文件、图片 URL、用户直接发送的图片：

```bash
python scripts/decode.py <图片路径或URL>
python scripts/decode.py --file <本地文件路径>
python scripts/decode.py --url <图片URL>
python scripts/decode.py --force-api <图片路径或URL>
```

- `--force-api`：跳过本地 zxing，强制使用远程 API 解码。当用户明确要求用 API 解码时使用。

**用户直接发送图片时的处理：**
- 用户在对话中粘贴/拖入/附加图片时，图片会作为附件提供，可通过文件路径访问
- 获取到图片的本地路径后，直接传给 `decode.py --file <路径>` 即可
- 若图片是通过 @ 引用的文件，同样使用其文件路径

**SKILL_DIR 定位**：脚本路径相对于本 skill 目录，执行时需 `cd` 到 skill 目录或使用绝对路径。

脚本输出 JSON，根据 `source` 字段判断解码来源：

```json
{"source": "zxing", "contents": ["解码内容"]}
{"source": "api", "contents": ["解码内容"]}
```

失败时：

```json
{"error": "无法解码: 本地 zxing 和远程 API 均未识别到二维码"}
```

呈现给用户的格式：

单个二维码：

```
二维码解码结果（via <source>）：
- 内容：<解码出的文本>
```

多个二维码：

```
二维码解码结果（共识别到 N 个二维码，via <source>）：
1. <内容1>
2. <内容2>
```

### 场景二：批量解码

当用户提供 Excel/CSV/TXT 文件要求批量解码二维码图片时，使用 `scripts/batch_decode.py`：

```bash
python scripts/batch_decode.py --input <文件> [--column <列名或索引>] [--output-txt <输出TXT路径>]
```

**列检测逻辑（Excel/CSV）：**
- 自动检测：扫描首行表头，匹配关键词（url/link/image/img/图片/链接/网址/二维码 等）
- 若只有一列，直接使用
- 若无法判断，脚本返回 `need_column` JSON，此时**需要询问用户指定哪一列**

**TXT：** 每行一个图片 URL，无需列选择。

**默认行为：** 在原文件中新增"解码结果"列（Excel 新增列 / CSV 新增列），直接回写原文件。

**单独输出 TXT：** 用户明确要求时加 `--output-txt` 参数，所有结果按行分隔写入 TXT。

**未解析的图片：** 对应行写入 `未解析到二维码`。

脚本输出 JSON：

```json
{"total": 50, "success": 48, "failed": 2, "output_file": "D:\\data.xlsx", "output_txt": null}
```

需要用户选列时：

```json
{"need_column": true, "columns": ["名称", "图片链接", "备注"], "preview": [...], "message": "无法自动判断 URL 列，请指定 --column 参数"}
```

**交互流程：**

1. 执行脚本
2. 若返回 `need_column`，将 `columns` 和 `preview` 展示给用户，询问使用哪一列
3. 用户回答后，加上 `--column` 重新执行
4. 成功后向用户报告结果统计

呈现给用户的格式：

```
批量解码完成：共 <total> 个，成功 <success> 个，失败 <failed> 个
结果已写入：<output_file>
TXT 输出：<output_txt>（仅单独输出时显示）
```

---

## 注意事项

- 生成二维码默认无需网络请求，直接拼接 URL 即可；保存本地或批量生成时才需要下载
- 解码二维码优先本地库（Python: zxingcpp / Node: qr-scanner-wechat），仅在本地失败时才调用远程 API
- data 参数需要正确的 URL 编码（空格→%20，中文等特殊字符需编码）
- 草料 API 无需认证、免费使用，但禁止恶意滥用
- 批量操作时，若脚本返回 `need_column`，必须先向用户展示列信息并确认后再重新执行

## 工程结构

```
qrcode-remote-skills/
├── SKILL.md              # 主指令文件
├── reference.md          # API 完整参考文档
├── requirements.txt      # Python 依赖
├── package.json          # Node.js 依赖
└── scripts/
    ├── generate.py / .js       # 单个生成并保存到本地
    ├── batch_generate.py / .js # 批量生成（URL 链接 / 图片）
    ├── decode.py / .js         # 单个解码（本地优先 + API 回退）
    └── batch_decode.py / .js   # 批量解码（回写原文件 / 输出 TXT）
```

## 更多信息

- 完整 API 参数详情见 [reference.md](reference.md)
