---
name: epub-exporter
description: 将小说章节导出为 EPUB 格式电子书。支持合并所有章节、生成目录、自定义封面和元数据。
version: 0.1.0
---

# EPUB Exporter - 电子书导出器

将 Time Weaver 创作的小说章节导出为 EPUB 格式电子书，方便在手机、平板、电子阅读器上阅读。

## 功能特性

- 📚 **自动合并章节**：读取所有章节文件，按顺序合并
- 📑 **生成目录**：自动提取章节标题，生成可点击的目录
- 🎨 **自定义封面**：支持自定义封面图片
- 📝 **元数据配置**：书名、作者、简介等元数据
- 📱 **标准 EPUB 格式**：兼容主流阅读器和阅读软件

## 使用方法

### 基本导出

```
导出小说为电子书
```

系统会自动：
1. 扫描 `chapters/` 目录下的所有章节文件
2. 按章节序号排序
3. 读取 `.learnings/PUBLISH_STATUS.md` 获取书名信息
4. 生成 EPUB 文件

### 自定义导出

```
导出小说，书名叫《XXX》，作者 XXX
```

可以指定：
- 书名（如果与发布时的书名不同）
- 作者名
- 封面图片路径
- 输出文件名

## 依赖安装

首次使用前需要安装 Node.js 依赖：

```bash
cd ~/.openclaw/workspace/skills/time-weaver/scripts
npm install epub-gen
```

## 输出文件

生成的 EPUB 文件保存在：
```
~/.openclaw/workspace/skills/time-weaver/output/
```

文件名格式：`{书名}_{日期}.epub`

## 技术实现

使用 `epub-gen` npm 包生成 EPUB：

```javascript
const Epub = require('epub-gen');

const options = {
  title: '烂尾之王',
  author: 'Time Weaver',
  publisher: 'Time Weaver Studio',
  description: '穿越小说',
  tocTitle: '目录',
  content: [
    {
      title: '第一章：金光',
      data: '<h1>第一章：金光</h1><p>...</p>'
    },
    // ... 更多章节
  ]
};

new Epub(options, outputPath);
```

## 章节文件格式

支持的章节文件命名：
- `chapter_01.md`, `chapter_02.md` ...
- `第1章.md`, `第2章.md` ...
- `chapter-1.md`, `chapter-2.md` ...

章节内容应为 Markdown 格式，会被自动转换为 HTML 嵌入 EPUB。

## 元数据来源

按优先级读取：
1. 用户指定的元数据
2. `.learnings/PUBLISH_STATUS.md` 中的书名
3. 默认使用 "Time Weaver 小说"

## 示例输出

```
✅ 开始导出《烂尾之王》
📖 读取到 8 个章节
📝 解析章节内容...
🎨 生成 EPUB...
✅ 导出成功！
📂 文件路径: ~/.openclaw/workspace/skills/time-weaver/output/烂尾之王_2026-03-30.epub
```

## 使用场景

- 📱 在手机上离线阅读
- 📚 导入 Kindle/微信读书等阅读器
- 💾 备份本地副本
- 📤 分享给朋友

---

*EPUB Exporter - 让小说随时随地可读*
