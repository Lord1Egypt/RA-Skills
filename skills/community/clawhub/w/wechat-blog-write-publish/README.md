# WeChat Blog Write & Publish Skill

基于参考资料自动创作微信公众号文章，并发布到公众号草稿箱的 AI 技能。

## ✨ 特性

- 🎯 **智能创作**：基于参考资料（网页、文档、PDF）自动生成高质量文章
- 📝 **专业排版**：遵循微信公众号排版规范，美观易读
- 🚀 **一键发布**：自动发布到公众号草稿箱，无需手动操作
- 📊 **可视化图表**：支持 Mermaid 语法，自动生成流程图、架构图
- 🎨 **多主题支持**：内置 8 种主题样式，满足不同风格需求

## 📋 工作流程

```mermaid
graph LR
    A[接收参考资料] --> B[内容分析]
    B --> C[文章创作]
    C --> D[保存 Markdown]
    D --> E[发布到草稿箱]
```

### 1️⃣ 接收输入
- 支持网页链接、文档、PDF 等多种格式
- 确认文章主题、内容方向和写作风格

### 2️⃣ 内容创作
严格遵循四大标准：
- ✅ **准确性**：严格依据参考资料，信息可靠
- ✅ **专业性**：提供深度内容和实用价值
- ✅ **可读性**：通俗易懂，必要时解释专业术语
- ✅ **逻辑性**：结构清晰，层次分明

### 3️⃣ 排版设计
- 合理使用 Markdown 标题层级
- 段落分隔清晰，重点突出
- 适度使用表情符号增强可读性

### 4️⃣ 发布文章
使用 `wenyan-cli` 工具一键发布到微信公众号草稿箱

## 🛠️ 安装与配置

### 安装 wenyan-cli

```bash
npm install -g @wenyan-md/cli
```

### 配置公众号凭证

1. **获取 AppID 和 AppSecret**
   - 登录 [微信公众号后台](https://mp.weixin.qq.com)
   - 进入"设置与开发" → "开发接口管理"
   - 复制 AppID 和 AppSecret

2. **配置 IP 白名单** ⚠️
   - 在公众号后台"开发接口管理" → "基本配置" → "IP 白名单"
   - 添加本机公网 IP（访问 [ip.sb](https://ip.sb) 查看）
   - **重要**：未配置白名单会导致 `40164` 错误

3. **配置凭证**
   ```bash
   wenyan config --appid 你的 AppID --appsecret 你的 AppSecret
   ```

## 📖 使用指南

### 快速开始

```bash
# 一键发布 Markdown 文章
wenyan publish -f article.md
```

### 常用命令

```bash
# 指定主题样式
wenyan publish -f article.md --theme blue

# 指定作者
wenyan publish -f article.md --author "作者名"

# 指定封面图
wenyan publish -f article.md --cover ./cover.jpg

# 开启评论
wenyan publish -f article.md --enable-comment

# 查看配置
wenyan config --list

# 查看可用主题
wenyan config --list-themes
```

### 内置主题

`default` · `blue` · `green` · `red` · `yellow` · `brown` · `black` · `orange`

### 高级用法：分步执行

```bash
# Step 1: Markdown 转 HTML
wenyan md2html --from article.md --to article.html --theme blue

# Step 2: 修复 HTML 并上传图片
wenyan fix article.html

# Step 3: 生成封面图
wenyan cover --title "文章标题" --author "作者名" --to cover.jpg

# Step 4: 发布到草稿箱
wenyan publish --article article.html --cover cover.jpg
```

## 📄 Front Matter 支持

在 Markdown 文章开头定义元信息：

```markdown
---
title: 文章标题
author: 作者名
digest: 文章摘要
theme: blue
cover: ./cover.jpg
enableComment: true
---
```

> 💡 命令行参数优先级高于 Front Matter

## 📁 输出目录结构

执行后生成 `.wxgzh/` 目录：

```
.wxgzh/
├── article.html          # 转换后的 HTML（已内联样式）
├── article.cover.jpg     # 自动生成的封面图
└── publish-result.json   # 发布结果（含草稿 ID）
```

## 💡 使用示例

### 示例 1：基于网页链接

**输入：**
```
请根据这个链接写一篇关于 LangChain 的公众号文章：
https://python.langchain.com/docs/get_started/introduction
```

**执行流程：**
1. 抓取并分析网页内容
2. 创作文章（包含 Front Matter、Mermaid 图表、表情符号）
3. 保存为 `langchain-intro.md`
4. 执行 `wenyan publish -f langchain-intro.md` 发布

### 示例 2：基于多个参考资料

**输入：**
```
请根据以下资料写一篇 AI 产品经理的文章：
- 文档：/path/to/product-methods.pdf
- 链接：https://example.com/ai-pm-guide
```

**执行流程：**
1. 读取 PDF 文档和网页内容
2. 整合信息，创作结构化文章
3. 保存为 `ai-product-manager.md`
4. 执行 `wenyan publish -f ai-product-manager.md` 发布

## ⚠️ 常见问题

| 问题 | 解决方案 |
|------|---------|
| `40164` 错误 | IP 不在白名单，需在公众号后台添加本机公网 IP |
| 封面图比例错误 | 微信封面图要求 2.35:1，工具会自动裁剪 |
| 图片上传失败 | 确保图片为本地路径，或已上传至微信图床 |

## 📋 注意事项

1. **内容准确性**：严格基于参考资料，不臆造信息
2. **格式规范**：确保 Markdown 语法正确，标题层级清晰
3. **发布前检查**：确认 wenyan-cli 已正确配置
4. **封面图片**：默认使用 `asset/微信公众号头像.png`，可自定义
5. **IP 白名单**：发布前务必在公众号后台配置本机 IP

## 🔗 相关资源

- [wenyan-cli GitHub]()
- [微信公众号开发文档](https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Overview.html)

## 📝 License

MIT
