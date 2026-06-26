---
name: young-post-downloader
slug: young-post-downloader
version: 1.0.0
description: 自动下载 Young Post Club Spark 网站文章并生成 PDF。使用场景：用户要求下载 Today's Read 文章、获取 Young Post 内容、批量抓取教育文章、生成学习材料 PDF、上传飞书云空间。支持：自动解析文章列表、批量下载、HTML 排版、PDF 转换、飞书上传。
---

# Young Post Club Spark 文章下载器

自动化下载 Young Post Club Spark 网站的「Today's Read」文章，生成精美排版的 PDF 文档并上传到飞书云空间。

## 快速开始

当用户要求：
- 「下载 Young Post Spark 的文章」
- 「把 Today's Read 转成 PDF」
- 「获取这个网站的文章并上传飞书」
- 「批量下载教育文章」

触发此技能。

## 工作流程

```
1. 访问 Spark 页面 → 2. 解析文章列表 → 3. 批量下载 → 4. 生成 HTML → 5. 转换 PDF → 6. 上传飞书
```

## 使用脚本

### 完整流程

```bash
python scripts/download_articles.py
```

### 自定义参数

```bash
python scripts/download_articles.py \
  --url "https://www.youngpostclub.com/spark" \
  --output-dir "/path/to/workspace" \
  --upload-to-feishu true
```

## 详细步骤

### 步骤 1: 访问 Spark 页面

使用 `web_fetch` 工具获取 Spark 主页内容：

```python
web_fetch(url="https://www.youngpostclub.com/spark", extractMode="markdown")
```

### 步骤 2: 解析文章列表

从页面提取所有文章链接，识别模式：
- `/yp/news/...` - 新闻类
- `/spark/learning-zone/...` - 学习区
- `/yp/being-well/...` - 健康生活
- `/spark/share-us/...` - 读者投稿

### 步骤 3: 批量下载文章

对每篇文章调用 `web_fetch`：

```python
for article_url in article_urls:
    content = web_fetch(url=article_url, extractMode="markdown")
    articles.append({
        "title": content["title"],
        "content": content["text"],
        "url": article_url,
        "date": extract_date(content)
    })
```

### 步骤 4: 生成 HTML 文档

创建带目录、样式排版的 HTML：

- 添加可点击目录
- 按类别分组文章
- 保留原文引用
- 添加日期和分类标签

输出路径：`{workspace}/young-post-spark-{date}.html`

### 步骤 5: 转换为 PDF

使用 Chrome 无头模式：

```bash
google-chrome --headless --disable-gpu \
  --print-to-pdf={output}.pdf \
  --print-to-pdf-no-header \
  --paper-size=A4 \
  {input}.html
```

### 步骤 6: 上传飞书

使用 `feishu_drive_file` 上传：

```python
feishu_drive_file(
    action="upload",
    file_path=pdf_path,
    file_name=f"Young Post Spark 文章合集 - {date}.pdf",
    size=file_size
)
```

## 输出文件

| 文件 | 说明 | 大小 |
|------|------|------|
| `young-post-spark-{date}.html` | HTML 版本，可用 Word 打开 | ~40 KB |
| `young-post-spark-{date}.pdf` | PDF 版本，A4 打印优化 | ~300 KB |

## 错误处理

### 常见问题

1. **网页加载失败**
   - 检查网络连接
   - 重试 `web_fetch`
   - 使用备用 URL

2. **PDF 转换失败**
   - 确认 Chrome 已安装：`which google-chrome`
   - 检查 HTML 语法
   - 增加超时时间

3. **飞书上传失败**
   - 检查 OAuth 授权
   - 确认文件大小限制 (<100MB)
   - 验证文件名格式

## 自定义配置

### 修改输出目录

编辑脚本中的 `WORKSPACE` 变量：

```python
WORKSPACE = "/your/custom/path"
```

### 添加文章过滤

只下载特定类别的文章：

```python
CATEGORIES = ["news", "learning-zone"]  # 只下载这些类别
```

### 调整 PDF 样式

修改 HTML 中的 CSS：

```css
body {
    font-family: "Calibri", "Arial", sans-serif;
    font-size: 11pt;
    line-height: 1.6;
}
```

## 相关技能

- **feishu-create-doc**: 创建飞书云文档
- **feishu-drive-file**: 飞书云空间文件管理
- **web-fetch**: 网页内容提取

## 使用示例

### 示例 1: 下载今日文章

用户：「下载 Young Post Spark 今天的文章」

```
1. 访问 spark 页面
2. 解析 17 篇文章
3. 批量下载
4. 生成 HTML + PDF
5. 上传飞书
→ 回复：✅ 已下载 17 篇文章并上传到飞书云空间
```

### 示例 2: 只要 PDF

用户：「把 Young Post 的文章转成 PDF」

```
跳过 HTML 预览，直接生成 PDF
→ 回复：📄 PDF 已生成并上传
```

### 示例 3: 指定类别

用户：「只下载学习区的文章」

```
过滤 URL 包含 learning-zone 的文章
→ 回复：📚 已下载 5 篇学习区文章
```

## 注意事项

1. **版权说明**: 在生成的文档中添加版权声明
2. **使用限制**: 仅供个人学习使用
3. **频率限制**: 避免短时间内大量请求
4. **内容审核**: 确保内容适合目标受众

## 更新日志

- **v1.0** (2026-04-05): 初始版本，支持完整流程
