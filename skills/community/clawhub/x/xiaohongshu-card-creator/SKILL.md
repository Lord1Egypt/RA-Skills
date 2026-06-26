---
name: xiaohongshu-card-creator
description: 将小红书文案转换为HTML图文卡片网页，支持智能内容识别和通用模板两种模式，生成标准3:4竖版卡片，支持一键下载所有卡片图为PNG
version: 1.4.0
triggers:
  - "将这篇文案转为小红书卡片"
  - "生成小红书卡片"
  - "转为小红书图文"
  - "制作小红书卡片"
  - "小红书卡片生成"
  - "xhs卡片"
  - "xiaohongshu card"
metadata:
  author: Dunden
  license: MIT
  tags: [xiaohongshu, html, card, visual, content, screenshot, download, ai]
---

# xiaohongshu-card-creator

将 Markdown 文章转换为小红书风格的图文卡片，支持**智能内容识别**和**通用模板**两种模式。

## 功能特性

- ✅ **智能内容识别**：自动分析 Markdown 结构，根据内容类型选择最佳卡片布局
- ✅ **通用模板模式**：使用预设模板循环生成，适合任何内容类型
- ✅ **自定义卡片数量**：支持 1-20 张卡片
- ✅ **一键下载**：自动生成 1242×1660px PNG 图片
- ✅ **响应式设计**：浏览器直接预览
- ✅ **快捷键支持**：Ctrl+S 快速触发下载

## 使用方法

### 两种工作模式

#### 1. 智能内容识别模式（推荐）

自动分析 Markdown 结构，智能选择卡片布局。

```bash
# 启用智能模式
./scripts/generate.sh article.md -s

# 智能模式 + 指定卡片数量
./scripts/generate.sh article.md -s -n 7
```

**智能识别规则**：

| Markdown 标题关键词 | 识别类型 | 卡片样式 |
|:---|:---|:---|
| 一句话/定义/是什么 | definition | 定义卡片（高亮框） |
| 类比/比喻/像什么 | analogy | 类比卡片（渐变背景） |
| 特点/特性/优势 | features | 特点卡片（列表展示） |
| 举例/示例/案例 | examples | 示例卡片 |
| 对比/区别/vs | comparison | 对比卡片 |
| 步骤/流程/阶段 | process | 流程卡片 |
| 其他内容 | content | 通用内容卡片 |

#### 2. 通用模板模式

使用预设模板循环生成卡片。

```bash
# 默认生成7张卡片
./scripts/generate.sh article.md

# 生成指定数量的卡片
./scripts/generate.sh article.md -n 5
```

### 参数说明

| 参数 | 说明 | 默认值 |
|:---|:---|:---|
| `input-file` | Markdown文件路径 | 必填 |
| `-n, --num-cards` | 指定卡片数量 | 7 |
| `-o, --output` | 输出目录 | `./output` |
| `-s, --smart` | 启用智能内容识别 | false |
| `-h, --help` | 显示帮助 | - |

### 使用示例

```bash
# 智能模式：自动分析文章结构
cd /path/to/xiaohongshu-card-creator
./scripts/generate.sh /path/to/article.md -s

# 通用模式：快速生成固定模板卡片
./scripts/generate.sh /path/to/article.md -n 3

# 指定输出目录
./scripts/generate.sh article.md -s -n 5 -o ./my-cards
```

### 导出 PNG 图片

1. 浏览器打开生成的 `xiaohongshu-cards.html`
2. 点击 **"📸 下载卡片图"** 按钮
3. 自动下载所有 PNG 图片

**快捷键**：`Ctrl+S` (或 `Cmd+S`) 快速触发下载

## 内容编写建议

### 适合智能模式的文章结构

```markdown
# 文章主标题

## 一句话解释
简明扼要的定义...

## 生活类比
用生活化的比喻解释...

## 关键特点
- 特点一
- 特点二
- 特点三

## 举例说明
具体的例子...

## 对比分析
与其他事物的区别...
```

### Markdown 支持

- `#` 一级标题 → 卡片主标题
- `##` 二级标题 → 卡片章节标题
- `**粗体**` → 高亮文字
- `-` 或 `*` 列表 → 列表展示
- 代码块 → 保留格式

## 输出文件

- **HTML文件**: `xiaohongshu-cards.html`
- **PNG图片**: `xhs-card-01.png` ~ `xhs-card-{N}.png`
- **尺寸**: 1242×1660px（小红书标准3:4）
- **位置**: `./output`（可自定义）

## 技术实现

- **html2canvas**: 浏览器端截图
- **3倍缩放**: 确保高清输出
- **纯前端**: 无需服务器

## 自定义样式

编辑 `templates/card-template.html` 可自定义：
- 配色方案
- 卡片布局
- 字体样式

## 更新日志

### v1.3.0
- ✅ **新增智能内容识别模式** (`-s` 参数)
- ✅ 自动分析 Markdown 结构
- ✅ 根据内容类型选择最佳卡片布局
- ✅ 保留通用模板模式作为默认选项

### v1.2.1
- ✅ 移除 hardcode 路径
- ✅ SKILL_DIR 动态检测

### v1.2.0
- ✅ 支持自定义卡片数量
- ✅ 新增命令行参数

### v1.1.0
- ✅ 初始版本
