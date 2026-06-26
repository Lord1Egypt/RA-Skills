---
name: wechat-article
description: |
  微信公众号文章抓取与转换，支持 Markdown/HTML/Text/JSON/Excel 五种格式。
  触发条件：用户发送微信文章链接（https://mp.weixin.qq.com/s/xxx）、
  多链接（换行分隔）、或「帮我转这篇文章」「保存微信文章」等表达。
  格式选择前必须询问用户，支持单选或多选。
---

> 将微信文章转换为离线的 Markdown/HTML/Text/JSON/Excel，无需登录，直接抓取，图片和样式本地化保留。

# 微信公众号文章抓取

## 触发条件

用户发送：
- 微信文章链接：`https://mp.weixin.qq.com/s/xxx`
- 多个链接（换行或空格分隔）
- 「帮我转这篇文章」「保存这篇微信文章」「下载这篇文章」

## 每次导出前必须询问格式（必须）

```
用户: https://mp.weixin.qq.com/s/xxx
→ 询问: "请选择导出格式（支持单选或多选，例如：1 或 1,3,5 或 markdown,html）"
```

**可选格式：**

| 序号 | 格式 | 扩展名 | 说明 |
|------|------|--------|------|
| 1 | Markdown | .md | 带标题/作者/日期/来源链接 |
| 2 | Excel | .xlsx | 表格，含元信息+正文（行高300px） |
| 3 | HTML | .html | 独立网页，CSS+图片本地化，浏览器直接打开 |
| 4 | 纯文本 | .txt | 无格式纯文字 |
| 5 | JSON | .json | 结构化，含完整元数据 |

**格式选择解析（不区分大小写）：**
- 单选：`2` / `excel` / `Excel`
- 多选：`1,3,5` / `markdown,html,json` / `1 和 3`

## HTML 格式详解

HTML 是离线阅读效果最好的格式，结构如下：
```
文章标题_文章ID/
├── index.html        # 完整网页（CSS引用+图片引用）
└── assets/           # 资源文件夹
    ├── *.css         # 样式文件（18个，共约3MB）
    └── *.jpg/png/webp # 图片文件
```

**生成策略：**
- 保留微信原始 HTML 结构（`<!DOCTYPE><html><head><body>`）
- 下载所有 CSS/图片到 `assets/`，用时间戳文件名
- 替换所有资源 URL 为本地相对路径 `href="./assets/xxx"`
- CSS/图片按内容 hash 去重（相同资源只存一份）
- `#js_content` 的 `visibility:hidden` 样式自动移除（防空白页）
- `#js_article_bottom_bar` 底部栏自动保留
- MINIMAL_CSS 内联到 `<style>` 保底样式（字体/行高/图片自适应）
- 空 img 标签（视频/音频占位符）自动清理
- **无需登录**，直接请求 `mp.weixin.qq.com`，Referer 必须带域名

**CSS 处理策略：**
- CSS 总和 ≤ 500KB → 内联到 HTML `<style>`（单文件方便分享）
- CSS 总和 > 500KB → 保存到 `assets/` 用 `<link>` 引用（避免 HTML 臃肿）

**已知限制：**
- 阅读量/点赞/评论数：微信 API 需要登录态 cookies，纯抓取无法获取
- 极少数被删除或违规文章无法抓取（返回错误）

## 单篇处理流程

1. 接收用户链接
2. **必须先询问格式**
3. 调用脚本（每个选定格式一次）
4. 保存到 `~/Desktop/文章标题_文章ID/`
5. 汇报文件名和大小

## 批量处理流程

1. 接收多链接（换行分隔）
2. **必须先询问格式**
3. 每篇每格式各抓一次，保存到 `~/Desktop/微信文章批量/`
4. 汇报成功数/失败数

## 核心脚本

```bash
# 单篇（单格式）
python skills/wechat-article/scripts/fetch_article.py <url> [format] [output_dir]
# format: markdown | html | text | json | excel

# 批量（多链接）
python skills/wechat-article/scripts/batch_fetch.py <urls_file> [formats_csv]
```

## 实现细节

- **依赖**：html5lib（纯 Python，无 C 扩展，pip install html5lib）
- **无需登录**：直接请求 mp.weixin.qq.com，带 Chrome UA + Referer
- **图片处理**：优先用 `data-src`（懒加载），同步到 `src`；空 img 标签自动移除
- **文件名**：文章标题前80字符 + 文章ID，避免重复
- **Excel**：深蓝表头，交替底色，含边框
- **并发下载**：CSS/图片并行（8线程），超时12秒/资源
