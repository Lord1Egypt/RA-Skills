---
name: "social-parser"
description: "解析抖音视频和小红书笔记，提取标题、封面、描述、标签、作者等核心信息。当用户想解析、获取、抓取、提取抖音视频数据、小红书笔记内容，或粘贴了抖音/小红书链接希望查看内容详情时调用。常见表达：'帮我解析这个抖音链接'、'获取小红书笔记内容'、'抓取视频信息'、'提取这条小红书的标题标签'、'分析这个视频'。"
---

# 社交媒体作品解析指南

## 能力说明

通过 `gnomic` CLI 工具，可以解析抖音视频和小红书笔记链接，提取作品的核心信息（标题、封面图、描述、标签、作者、点赞数等），适用于：

- 快速获取抖音视频的无水印数据和元信息
- 读取小红书笔记的正文、图片、视频链接
- 批量分析社交媒体内容用于选题、竞品研究
- 提取创作者信息和作品标签

---

## 使用方式

### 抖音视频解析

```bash
gnomic social dy-video <抖音视频链接>
```

**示例：**
```bash
gnomic social dy-video "https://v.douyin.com/xxxxxx"
```

**JSON 输出结构：**
```json
{
  "success": true,
  "data": {
    "title": "视频标题",
    "cover": "封面图片URL",
    "video_url": "无水印视频地址",
    "author": "作者昵称",
    "author_id": "作者ID",
    "like_count": 12345,
    "comment_count": 678,
    "share_count": 90,
    "tags": ["标签1", "标签2"]
  }
}
```

---

### 小红书笔记解析

```bash
gnomic social xhs-note <小红书笔记链接>
```

**示例：**
```bash
gnomic social xhs-note "https://www.xiaohongshu.com/explore/xxxxxx"
```

**JSON 输出结构：**
```json
{
  "success": true,
  "data": {
    "success": true,
    "message": "小红书笔记信息提取成功",
    "title": "笔记标题",
    "content": "笔记正文内容",
    "image_urls": ["图片URL1", "图片URL2"],
    "video_url": "视频链接（图文笔记时为空字符串）",
    "video_duration": "视频时长（图文笔记时为空字符串）"
  }
}
```

> 注意：小红书接口**不返回互动数据**（点赞、收藏、评论数）及作者信息，仅包含正文、图片和视频内容。

---

### 文本格式输出

加 `-f text` 参数可返回更易阅读的文本格式：

```bash
gnomic social dy-video "https://v.douyin.com/xxxxxx" -f text
gnomic social xhs-note "https://www.xiaohongshu.com/explore/xxxxxx" -f text
```

---

## 操作流程

### 第一步：识别链接类型

- **抖音链接** 通常形如：`https://v.douyin.com/xxx` 或 `https://www.douyin.com/video/xxx`
- **小红书链接** 通常形如：`https://www.xiaohongshu.com/explore/xxx` 或 `http://xhslink.com/xxx`

> 如果用户粘贴的是 App 分享的短链或带文字的分享文案，提取其中的链接即可直接传入命令。

### 第二步：执行对应命令

| 平台 | 命令 |
|------|------|
| 抖音 | `gnomic social dy-video <url>` |
| 小红书 | `gnomic social xhs-note <url>` |

### 第三步：解析并展示数据

从返回的 JSON 中提取 `data` 字段，按需向用户展示：

- **抖音**：展示标题、作者、互动数据（点赞/收藏/评论/分享），封面图用 Markdown `![](url)` 渲染，`url` 字段为无水印视频下载地址
- **小红书**：展示标题、`content` 正文，`image_urls` 数组中的图片用 Markdown `![](url)` 渲染；如 `video_url` 不为空则告知用户可下载视频

---

## 注意事项

- 链接需为完整 URL，短链（如抖音分享文案中的 `https://v.douyin.com/xxx`）也支持
- 请求会访问远端 API，通常需要 5~15 秒，请耐心等待
- 小红书部分账号的笔记如设为私密，可能无法获取
- 数据仅供内容分析，请遵守平台使用条款

---

## 补充：命令不可用时

如果执行 `gnomic` 命令时提示找不到命令，说明 `gnomic-cli` 尚未安装，执行以下命令安装：

```bash
npm install -g gnomic-cli
```

`gnomic-cli`开源地址：https://github.com/huyi9531/gnomic_cli