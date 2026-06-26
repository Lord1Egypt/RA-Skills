# 完整案例：url-to-markdown Skill

这是一个按照四层骨架从头到尾写好的真实 Skill。用这个案例来理解"四层骨架写对了是什么效果"。

---

## 完整 SKILL.md

```markdown
---
name: url-to-markdown
description: 将网页/微信公众号文章抓取并转换为结构化 Markdown 的封装 Skill。
  Use when user asks to 抓取网页文章、URL转Markdown、保存网页、
  下载文章、抓微信文章、公众号文章保存、网页转MD.
  不适用于本地文件转换、PDF处理、图片OCR.
---

# URL to Markdown

将微信公众号和通用网页文章抓取为结构化 Markdown 文件，保存到 workspace。

## 概述

对 WeSpy 抓取能力的封装，聚焦"给一个 URL，得到一个 Markdown 文件"的单一链路。

### 功能范围

- 单篇文章抓取（微信公众号 / 通用网页 / 掘金）
- 微信专辑文章列表获取
- 微信专辑批量下载
- 多格式输出（Markdown / HTML / JSON）

不覆盖：PDF 转换、图片 OCR、需要登录的内容。

## 使用

脚本位置：`scripts/wespy_cli.py`

### 场景一：单篇微信文章抓取

用户给了一个微信文章链接，想要保存为 Markdown。

```bash
python3 scripts/wespy_cli.py "https://mp.weixin.qq.com/s/xxxxx"
```

输出：在 `/sandbox/workspace/outputs/` 下生成以文章标题命名的 `.md` 文件。

### 场景二：专辑批量下载

用户给了一个微信专辑链接，想下载前 20 篇。

```bash
python3 scripts/wespy_cli.py "https://mp.weixin.qq.com/mp/profile_ext?..." --max-articles 20
```

如果用户没指定数量，默认 10 篇。

### 场景三：仅获取专辑文章列表（不下载正文）

用户想先看看专辑里有哪些文章，再决定是否下载。

```bash
python3 scripts/wespy_cli.py "URL" --album-only
```

输出：在终端打印文章标题和链接列表。

### 场景四：指定输出格式

用户想要 HTML 格式而非 Markdown。

```bash
python3 scripts/wespy_cli.py "URL" --format html
```

可选格式：`markdown`（默认）、`html`、`json`。

## 补充说明

- **WeSpy 未安装**：优先使用本地源码路径 `~/Documents/project/WeSpy`；若不存在则自动 `git clone` 到该目录；若 git clone 也失败则报错并提示用户手动安装
- **微信文章需要特殊处理**：通用网页抓取直接用 requests + BeautifulSoup；微信文章走 WeSpy 的专有解析，因为微信页面有反爬和动态加载
- **输出目录不存在**：自动创建 `/sandbox/workspace/outputs/`
- **同名文件已存在**：追加数字后缀（如 `文章标题-2.md`），不覆盖已有文件
- **网络超时**：单次请求 30 秒超时，重试 2 次；重试仍失败则跳过该文章继续处理下一篇，在终端报告失败列表
- **专辑链接格式**：必须是 `mp.weixin.qq.com/mp/profile_ext` 开头的链接；如果用户给的是单篇文章链接但说了"专辑"，提示用户确认意图
```

---

## 案例分析：四层骨架如何体现

### 第一层：头部（description）

| 要素 | 案例中的体现 |
|------|-------------|
| 第一句说做什么 | "将网页/微信公众号文章抓取并转换为结构化 Markdown 的封装 Skill" |
| 触发短语覆盖多种表达 | "抓取网页文章、URL转Markdown、保存网页、下载文章、抓微信文章、公众号文章保存、网页转MD" |
| 不适用边界 | "不适用于本地文件转换、PDF处理、图片OCR" |

### 第二层：概述

| 要素 | 案例中的体现 |
|------|-------------|
| 一句话定位 | "对 WeSpy 抓取能力的封装，聚焦'给一个 URL，得到一个 Markdown 文件'的单一链路" |
| 只列能做什么 | 4 条功能，每条一行，没有命令、没有参数 |
| 明确说清不覆盖 | "不覆盖：PDF 转换、图片 OCR、需要登录的内容" |

### 第三层：操作指南

| 要素 | 案例中的体现 |
|------|-------------|
| 按场景给示例 | 4 个场景：单篇抓取、批量下载、列表获取、指定格式 |
| 注释说明 + 完整命令 | 每个场景先说意图，再给完整命令 |
| 默认值明确 | "默认 10 篇"、"markdown（默认）" |
| 输出位置明确 | "在 `/sandbox/workspace/outputs/` 下生成" |

### 第四层：补充说明

| 坑 | 怎么堵的 |
|----|---------|
| 依赖不存在 | 三级兜底：本地源码 → git clone → 报错提示 |
| 输入类型不同 | 明确区分微信和通用网页的处理路径 |
| 输出目录不存在 | 自动创建 |
| 同名文件冲突 | 追加数字后缀，不覆盖 |
| 网络超时 | 超时时间 + 重试次数 + 降级方案 |
| 用户意图混淆 | 链接格式与用户意图不匹配时提示确认 |

---

## 对比：没有四层骨架的写法

以下是把同样的信息写成"传统文档"的样子——没有层次意识：

```markdown
---
name: url-to-markdown
description: WeSpy 封装，支持文章抓取和格式转换。
---

# URL to Markdown

## 安装

需要 WeSpy，安装方式：pip install wespy 或 git clone ...

## API

wespy_cli.py [URL] [--album-only] [--max-articles N] [--format FORMAT]

参数说明：
- URL：文章或专辑链接
- --album-only：仅获取列表
- --max-articles：批量下载数量
- --format：输出格式，支持 markdown/html/json

## 使用示例

python3 scripts/wespy_cli.py "https://mp.weixin.qq.com/s/xxx"

## 注意事项

请确保网络连接正常。如有问题请联系开发者。
```

**问题清单：**

1. description 没有触发词，用户说"帮我抓一下这篇微信文章"Agent 匹配不到
2. 没有功能边界，不知道这个 Skill 能做什么不能做什么
3. 操作指南是参数说明书，Agent 得自己拼命令
4. 补充说明是空话，遇到依赖缺失/超时/同名冲突没有兜底方案
5. 没有场景区分——用户要批量下载和用户要单篇抓取，应该走不同示例
