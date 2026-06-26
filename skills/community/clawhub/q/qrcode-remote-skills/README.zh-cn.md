[English](README.md) | 中文

# QR Code Remote Skills

为 Agent 赋予二维码生成与解码能力的 Skill 合集。

基于[草料二维码开放 API](https://cli.im/open-api/qrcode-api/quick-start.html) 和本地库，无需 API Key。

本 skills 不生成草料活码，生成的二维码是静态码。

## 安全声明

- **隐私保护**：上传到服务端解码的二维码图片均为临时文件，过一段时间后会自动删除，不会长期存储，保障用户隐私。
- **依赖透明**：本 skill 使用的第三方库（zxingcpp、Pillow、qrcode、草料 API 等）均为公开、开源的第三方库，可自行审查。
- **本地优先**：解码优先在本地完成，仅在本地失败时才调用远程 API，减少数据传输。

## 功能概览

| 功能 | 说明 |
|------|------|
| 生成二维码 | 将文本/URL 转为二维码，返回链接并预览 |
| 生成并保存到本地 | 下载二维码图片到指定路径 |
| 解码二维码 | 从图片 URL 或本地文件识别二维码内容 |
| 批量生成（URL） | 从 Excel/CSV/TXT 批量生成二维码链接列表 |
| 批量生成（图片） | 从 Excel/CSV/TXT 批量生成二维码图片到本地 |
| 批量解码 | 从 Excel/CSV/TXT 批量解码二维码，结果回写原文件 |

## 安装

### 通过 skills CLI 安装（推荐）

```bash
npx skills add caoliao/qrcode-remote-skills
```

```bash
# 全局安装（跨项目可用）
npx skills add caoliao/qrcode-remote-skills -g

# 安装到指定 Agent
npx skills add caoliao/qrcode-remote-skills -a cursor
npx skills add caoliao/qrcode-remote-skills -a claude-code
```

### 手动安装

直接将本项目 clone 到 Agent 的 skills 目录下：

```bash
git clone https://github.com/caoliao/qrcode-remote-skills
```

### 安装依赖（二选一）

首次使用时 Agent 会自动检测环境并安装依赖，也可以手动安装：

**Python 环境**

```bash
cd qrcode-remote-skills
pip install -r requirements.txt
```

依赖：`zxingcpp`、`Pillow`、`openpyxl`、`qrcode`

**Node.js 环境（无 Python 时）**

```bash
cd qrcode-remote-skills
npm install
```

依赖：`qrcode`、`jsqr`、`jimp`、`xlsx`、`archiver`

> 两套脚本功能和参数完全一致，Agent 会自动检测环境并选择可用的运行时。

### 验证安装

安装完成后，直接发送给 Agent "帮我生成一个二维码"即可触发此 Skill。

## 示例问答

### 生成二维码

> **你：** 帮我生成一个二维码，内容是 https://cli.im

> **AI：** 二维码已生成：
>
> ![QR Code](https://api.2dcode.biz/v1/create-qr-code?data=https%3A%2F%2Fcli.im&size=400x400)
>
> **二维码链接：** `https://api.2dcode.biz/v1/create-qr-code?data=https%3A%2F%2Fcli.im&size=400x400`

---

### 生成并保存到本地

> **你：** 生成一个二维码保存到桌面，内容是 Hello World，SVG 格式

> **AI：** *(执行脚本下载图片)*
>
> 二维码已生成并保存到本地：
>
> **二维码链接：** `https://api.2dcode.biz/v1/create-qr-code?data=Hello%20World&size=400x400&format=svg`
> **本地文件：** `C:\Users\xxx\Desktop\qrcode.svg`

---

### 解码二维码（URL）

> **你：** 帮我识别这个二维码 https://example.com/qr.png

> **AI：** *(执行解码脚本)*
>
> 二维码解码结果（via zxing）：
> - 内容：https://cli.im

---

### 解码二维码（发送图片）

> **你：** 帮我识别这个二维码 *(粘贴/拖入一张二维码图片)*

> **AI：** *(获取图片路径，执行解码脚本)*
>
> 二维码解码结果（via zxing）：
> - 内容：https://example.com

---

### 批量生成（URL 链接）

> **你：** 我有一个 data.xlsx，帮我批量生成二维码

> **AI：** 请问需要生成二维码 URL 链接，还是生成图片保存到本地？

> **你：** 生成链接就行

> **AI：** *(执行脚本)*
>
> 批量生成完成，共 50 个二维码链接，已保存到：`D:\output\urls.txt`

---

### 批量生成（图片）

> **你：** 把 products.csv 里的链接列批量生成二维码图片，打包成 zip

> **AI：** *(执行脚本)*
>
> 批量生成完成（via local）：共 200 个，成功 200 个，失败 0 个
> 输出目录：`D:\output\qrcodes`
> ZIP 文件：`D:\output\qrcodes.zip`

---

### 批量解码

> **你：** 帮我批量解码 images.xlsx 里的二维码图片

> **AI：** 检测到以下列，请问二维码图片 URL 在哪一列？
>
> | 列索引 | 列名 |
> |--------|------|
> | 0 | 产品名称 |
> | 1 | 图片链接 |
> | 2 | 备注 |

> **你：** 第 1 列

> **AI：** *(执行脚本)*
>
> 批量解码完成：共 50 个，成功 48 个，失败 2 个
> 结果已写入：`D:\data\images.xlsx`（新增"解码结果"列）

## 工程结构

```
qrcode-remote-skills/
├── README.md                   # 本文件
├── SKILL.md                    # Agent Skill 主指令
├── reference.md                # 草料 API 完整参考文档
├── requirements.txt            # Python 依赖
├── package.json                # Node.js 依赖
└── scripts/
    ├── generate.py / .js       # 单个生成并保存到本地
    ├── batch_generate.py / .js # 批量生成（URL 链接 / 图片）
    ├── decode.py / .js         # 单个解码（本地优先 + API 回退）
    └── batch_decode.py / .js   # 批量解码（回写原文件 / 输出 TXT）
```

## 技术说明

- **双运行时**：所有脚本同时提供 Python 和 Node.js 版本，参数和输出格式完全一致
- **生成**：默认直接拼接草料 API URL 返回（零延迟）；保存本地时下载图片；批量生成图片默认用本地库（Python: `qrcode` / Node: `qrcode`）
- **解码**：优先本地库解码（Python: `zxingcpp` / Node: `jsQR` + `jimp`），失败时自动回退草料 API
- **批量操作**：支持 Excel(.xlsx)、CSV、TXT 输入；自动检测数据列，无法判断时交互询问
- **草料 API**：免费、无需认证，[官方文档](https://cli.im/open-api/qrcode-api/quick-start.html)
