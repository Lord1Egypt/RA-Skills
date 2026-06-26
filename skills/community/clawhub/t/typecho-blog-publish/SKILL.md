---
name: typecho-blog-publish
description: 通过 XML-RPC 自动发布文章到 Typecho 博客。支持文件读取、草稿模式、标签管理、智能配图。
metadata:
  openclaw:
    emoji: 📝
    requires:
      bins: ["python3"]
    primaryEnv: "BLOG_PASSWORD"
    optionalEnv: ["BLOG_URL", "BLOG_USERNAME", "BLOG_XMLRPC"]
---

# Typecho 博客发布技能

使用此技能来自动发布文章到你的 Typecho 博客。

## ⚠️ 发布流程规范（铁律！）

**重要提示：发布完成≠工作完成！必须像真实用户一样检查实际效果！**

### 发布前检查清单（必须逐条核对！）

### 1. 配图要求 ✅ 必需（血泪教训！）
- [ ] **必须包含至少一张配图**（不能纯文字）
- [ ] 配图应与文章主题相关
- [ ] 图片应插入在文章开头或前 3 段内
- [ ] **必须使用完整的绝对 URL**（如 `http://yuanblog.tk:9980/usr/uploads/2026/03/xxx.png`）
- [ ] **禁止使用相对路径**（如 `/upload/2026/03/xxx.png` 会失败！）
- [ ] 使用 `upload_image.py` 上传后，复制返回的完整 URL
- [ ] 配图命令示例：
  ```bash
  # 1. 上传图片，获取完整 URL
  python3 scripts/upload_image.py /path/to/screenshot.png
  # 返回：http://yuanblog.tk:9980/usr/uploads/2026/03/2512184318.png
  
  # 2. 在文章中使用完整 URL
  # ![描述](http://yuanblog.tk:9980/usr/uploads/2026/03/2512184318.png)
  
  # 智能搜索配图（基于主题关键词）
  python3 scripts/smart_image.py "ADB Android 技术"
  ```

### 2. YAML 头部格式 ✅ 必需
- [ ] 文章必须包含标准 YAML front matter 头部
- [ ] 使用 `---` 包裹头部信息
- [ ] 必须包含 `title`（标题）字段
- [ ] 必须包含 `categories`（分类）字段
- [ ] 必须包含 `tags`（标签）字段
- [ ] 格式示例：
  ```markdown
  ---
  title: 文章标题
  categories: 技术
  tags: 标签 1, 标签 2
  ---
  ```

### 3. 发布命令 ✅ 必需
- [ ] 使用 `--file` 参数从文件发布（保留 YAML 头部）
- [ ] 不要直接使用标题 + 内容方式发布
- [ ] 命令示例：
  ```bash
  python3 scripts/publish_post.py --file article.md
  ```

### 4. 验证步骤 ✅ 必需（发布后必须检查！铁律！）
- [ ] **立即在浏览器中打开文章链接**（不要只看后台返回的"发布成功"）
- [ ] **检查标题是否正确显示**（不能是文件名）
- [ ] **检查配图是否正常显示**（不能是裂开的图标）
- [ ] **右键点击图片→复制图片地址**（验证是否为完整 URL）
- [ ] **检查分类和标签是否正确显示**
- [ ] **检查内容格式是否正常**（无乱码、无错位）
- [ ] **如发现问题，立即删除并重新发布**（不凑合、不侥幸）

**验证命令：**
```bash
# 检查文章中的图片路径
curl -s "文章 URL" | grep -o 'img src="[^"]*"'
# 应该显示完整 URL，如 http://yuanblog.tk:9980/usr/uploads/...
# 如果显示 /upload/... 说明路径错误！
```

**铁律：不检查就汇报=找死！**
- ❌ 禁止只看后台返回就以为完成
- ❌ 禁止不实际访问文章就汇报"已完成"
- ❌ 禁止发现问题不处理就交差
- ✅ 必须像真实用户一样检查
- ✅ 发现问题立即修复
- ✅ 确保用户看到的是完美效果

**血的教训（2026-03-31）：**
- 第一次发布：标题显示为文件名（❌ 未发现）
- 第二次发布：配图路径错误，图片不显示（❌ 未检查）
- 第三次发布：亲自检查后发现问题，修复（✅）
- **教训**：不亲自检查就不知道问题在哪！发布完成≠工作完成！

## 配置

在 `.env` 文件中配置以下环境变量：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `BLOG_URL` | 博客地址 | `http://yuanblog.tk:9980` |
| `BLOG_USERNAME` | 博客用户名 | `admin` |
| `BLOG_PASSWORD` | 博客密码（必需） | - |
| `BLOG_XMLRPC` | XML-RPC 路径 | `/index.php/action/xmlrpc` |

## 使用方法

### 1. 发布文章（推荐方式）

```bash
# 从文件发布（保留 YAML 头部）
python3 {baseDir}/scripts/publish_post.py --file article.md

# 保存为草稿
python3 {baseDir}/scripts/publish_post.py --file article.md --draft
```

### 2. 智能配图与上传

```bash
# 智能搜索配图（基于主题关键词）
python3 {baseDir}/scripts/smart_image.py "AI 技术 未来"

# 上传图片到博客媒体库
python3 {baseDir}/scripts/upload_image.py image.jpg

# 从 URL 下载并上传图片
python3 {baseDir}/scripts/upload_image.py --url "https://example.com/image.jpg"
```

### 3. 批量发布

```bash
# 批量发布草稿箱文章
python3 {baseDir}/scripts/batch_publish.py

# 管理文章（查看、删除）
python3 {baseDir}/scripts/manage.py
```

## 完整发布流程

### 步骤 1: 准备文章内容

创建 Markdown 文件，包含 YAML 头部：

```markdown
---
title: 文章标题
categories: 技术
tags: 标签 1, 标签 2
---

这里是正文内容...
```

### 步骤 2: 智能配图

```bash
python3 scripts/smart_image.py "文章主题关键词"
```

或在文章中使用图片语法：

```markdown
![描述](image.jpg)
```

### 步骤 3: 发布文章

```bash
python3 scripts/publish_post.py --file article.md
```

### 步骤 4: 验证发布结果

1. 访问返回的文章链接
2. 检查标题、配图、标签是否正确
3. 如有问题，删除文章并重新发布

## 错误处理

### 常见问题

**问题 1: 标题显示为文件名**
- 原因：YAML 头部格式错误或不存在
- 解决：确保使用标准 YAML 格式，用 `---` 包裹

**问题 2: 没有配图或图片不显示**
- 原因：使用了相对路径（如 `/upload/xxx.png`）
- 解决：**必须使用完整 URL**（如 `http://yuanblog.tk:9980/usr/uploads/xxx.png`）
- 验证：右键图片→复制图片地址，检查是否是完整 URL

**问题 3: 链接 404**
- 原因：未开启伪静态
- 解决：使用正确链接格式 `http://blog/index.php/archives/ID/`

### 血泪教训（2026-03-31 实战总结）

**教训：配图路径错误导致图片不显示**
- **错误做法**：`![描述](/upload/2026/03/adb_unlock_demo.png)`
- **正确做法**：`![描述](http://yuanblog.tk:9980/usr/uploads/2026/03/2512184318.png)`
- **原因**：Typecho 不支持相对路径的图片 URL
- **解决方案**：上传后复制完整 URL，直接写在文章中

## 相关文件

- `publish_post.py` - 主要发布脚本
- `smart_image.py` - 智能配图脚本
- `upload_image.py` - 图片上传脚本
- `batch_publish.py` - 批量发布工具
- `manage.py` - 文章管理工具

## 最佳实践

1. **始终使用 YAML 头部** - 确保标题、分类、标签正确解析
2. **必分配图** - 文章开头插入相关图片
3. **使用 --file 参数** - 保留完整的元数据
4. **发布后立即验证** - 检查标题、配图、标签
5. **及时清理错误文章** - 发现问题立即删除重发

---

*维护者：团子 🌟*  
*版本：1.1.0*  
*更新时间：2026-03-31*
