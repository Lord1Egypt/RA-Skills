[English](README.md) | 中文

# QR Code Skills

为 Agent 赋予二维码生成与解码能力的 Skill 合集。

**完全本地运行**，无需任何远程 API 或 API Key。

**声明：**
- **依赖均为公开开源库**：所有依赖（Python: zxingcpp、Pillow、openpyxl、qrcode；Node.js: qrcode、qr-scanner-wechat、sharp、xlsx、archiver）均为公开的开源项目，可在 PyPI / npm 上查阅源码与许可证
- **所有行为本地完成**：生成与解码均在用户本地执行，不调用任何远程 API，不上传任何数据；仅当解码输入为远程图片 URL 时，会下载该图片到本地后再解码

如需二维码生成 URL（无需保存文件即可预览）、更好的解码效果，可使用 [qrcode-remote-skills](https://github.com/caoliao/qrcode-remote-skills)：`npx skills add caoliao/qrcode-remote-skills`。

## 功能概览

| 功能 | 说明 |
|------|------|
| 生成二维码 | 将文本/URL 转为二维码图片，保存到本地 |
| 解码二维码 | 从本地图片或图片 URL 识别二维码内容 |
| 批量生成 | 从 Excel/CSV/TXT 批量生成二维码图片到本地 |
| 批量解码 | 从 Excel/CSV/TXT 批量解码二维码，结果回写原文件 |

## 安装

### 通过 skills CLI 安装（推荐）

```bash
npx skills add caoliao/qrcode-skills
```

```bash
# 全局安装（跨项目可用）
npx skills add caoliao/qrcode-skills -g

# 安装到指定 Agent
npx skills add caoliao/qrcode-skills -a cursor
npx skills add caoliao/qrcode-skills -a claude-code
```

### 手动安装

直接将本项目 clone 到 Agent 的 skills 目录下：

```bash
git clone https://github.com/caoliao/qrcode-skills
```

### 安装依赖（二选一）

首次使用时 Agent 会自动检测环境并安装依赖，也可以手动安装：

**Python 环境**

```bash
cd qrcode-skills
pip install -r requirements.txt
```

依赖：`zxingcpp`、`Pillow`、`openpyxl`、`qrcode`

**Node.js 环境（无 Python 时）**

```bash
cd qrcode-skills
npm install
```

依赖：`qrcode`、`qr-scanner-wechat`、`sharp`、`xlsx`、`archiver`

> 两套脚本功能和参数完全一致，Agent 会自动检测环境并选择可用的运行时。

### 验证安装

安装完成后，直接发送给 Agent "帮我生成一个二维码"即可触发此 Skill。

## 示例问答

### 生成二维码

> **你：** 帮我生成一个二维码，内容是 https://example.com

> **AI：** *(执行本地生成脚本)*
>
> 二维码已生成并保存到本地：
>
> **本地文件：** `D:\workspace\qrcode.png`

---

### 生成并保存到指定路径

> **你：** 生成一个二维码保存到桌面，内容是 Hello World，SVG 格式

> **AI：** *(执行本地生成脚本)*
>
> 二维码已生成并保存到本地：
>
> **本地文件：** `C:\Users\xxx\Desktop\qrcode.svg`

---

### 解码二维码（本地文件）

> **你：** 帮我识别这个二维码 *(粘贴/拖入一张二维码图片)*

> **AI：** *(获取图片路径，执行解码脚本)*
>
> 二维码解码结果（via zxing）：
> - 内容：https://example.com

---

### 解码二维码（URL）

> **你：** 帮我识别这个二维码 https://example.com/qr.png

> **AI：** *(下载图片到本地，执行解码脚本)*
>
> 二维码解码结果（via zxing）：
> - 内容：https://cli.im

---

### 批量生成

> **你：** 把 products.csv 里的链接列批量生成二维码图片，打包成 zip

> **AI：** *(执行脚本)*
>
> 批量生成完成：共 200 个，成功 200 个，失败 0 个
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
qrcode-skills/
├── README.md                   # English documentation
├── README.zh-cn.md             # 中文文档（本文件）
├── SKILL.md                    # Agent Skill 主指令
├── requirements.txt            # Python 依赖
├── package.json                # Node.js 依赖
└── scripts/
    ├── generate.py / .js       # 单个生成并保存到本地
    ├── batch_generate.py / .js # 批量生成图片
    ├── decode.py / .js         # 单个解码（纯本地）
    └── batch_decode.py / .js   # 批量解码（纯本地）
```

## 技术说明

- **双运行时**：所有脚本同时提供 Python 和 Node.js 版本，参数和输出格式完全一致
- **生成**：使用本地库（Python: `qrcode` / Node: `qrcode`）直接生成二维码图片
- **解码**：使用本地库（Python: `zxingcpp` / Node: `qr-scanner-wechat`）解码，无远程依赖
- **批量操作**：支持 Excel(.xlsx)、CSV、TXT 输入；自动检测数据列，无法判断时交互询问
- **完全离线**：所有生成和解码操作均在本地完成，无需网络连接（除非解码输入为远程图片 URL）
- **全部开源**：所有依赖均为公开的开源库，无任何闭源或专有组件
