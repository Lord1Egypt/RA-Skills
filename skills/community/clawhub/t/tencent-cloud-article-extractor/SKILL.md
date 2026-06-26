---
name: tencent-cloud-article-extractor
description: 提取腾讯云开发者社区文章内容并转换为 Markdown 格式。当用户需要抓取、解析或保存腾讯云文章时使用此技能。支持自动提取标题、作者、发布时间、正文内容，并生成格式规范的 Markdown 文档。触发词：腾讯云文章、抓取文章、解析文章、cloud.tencent.com/developer/article
---

# 腾讯云文章提取器

从腾讯云开发者社区提取文章内容并转换为 Markdown 格式。

## 快速开始

```bash
node ~/.openclaw/workspace/skills/tencent-cloud-article-extractor/scripts/extract_article.mjs <文章URL> [输出文件]
```

**示例：**

```bash
# 输出到控制台
node ~/.openclaw/workspace/skills/tencent-cloud-article-extractor/scripts/extract_article.mjs https://cloud.tencent.com/developer/article/2636150

# 保存到文件
node ~/.openclaw/workspace/skills/tencent-cloud-article-extractor/scripts/extract_article.mjs https://cloud.tencent.com/developer/article/2636150 article.md
```

## 支持的文章格式

- URL 格式：`https://cloud.tencent.com/developer/article/<文章ID>`
- 自动提取：标题、作者、发布时间、字数统计、阅读时长
- 支持的内容类型：标题、段落、代码块、图片、列表、引用、链接

## 输出格式

生成的 Markdown 文档包含：

```markdown
# 文章标题

> 作者：作者名
> 发布时间：2026-03-10 14:29
> 来源：腾讯云开发者社区
> 原文链接：https://cloud.tencent.com/developer/article/xxx

---

**文章统计**：字数 4738 | 预计阅读 17 分钟

---

## 正文内容...
```

## 工作原理

1. 发送 HTTP 请求获取文章页面
2. 从页面 `__NEXT_DATA__` 中提取 JSON 数据
3. 解析结构化内容并转换为 Markdown
4. 输出到控制台或保存到文件

## 注意事项

- 需要网络访问腾讯云网站
- 文章必须是公开可访问的
- 部分需要登录的文章可能无法提取
- 图片以原始 URL 引用，不会下载到本地

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `无效的腾讯云文章 URL` | URL 格式不正确 | 检查 URL 是否符合 `cloud.tencent.com/developer/article/xxx` 格式 |
| `未找到文章数据` | 页面结构变化或需要登录 | 确认文章公开可访问 |
| `文章内容为空` | 文章可能已被删除 | 检查原文链接是否有效 |

## 更新日志

### v1.0.0 (2026-03-16)
- ✅ 初始版本
- ✅ 支持腾讯云文章提取
- ✅ Markdown 格式输出
