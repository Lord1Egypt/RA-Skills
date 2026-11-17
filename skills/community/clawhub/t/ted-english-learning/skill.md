---
name: ted-english-learning
description: 解析 TED 演讲，生成中英文对照文本、生词表、内容总结、长难句解析、阅读理解题目和 Canvas 总结分析图，帮助用户通过 TED 演讲学习英语。每当用户提到 TED 演讲、英语学习、演讲分析、TED 文稿解析时，都应该使用这个技能。
user-invocable: true
---

# TED 英语学习助手

将 TED 演讲 PDF 转化为结构化的中英文对照学习笔记和思维导图。

## 安装

### 方式一：让 Claude Code 自动安装

在 Claude Code 中输入：

```
帮我从这个 GitHub 仓库安装 skill：https://github.com/xiao2769433/ted-english-learning
```

### 方式二：手动安装

```bash
git clone https://github.com/xiao2769433/ted-english-learning.git ~/.claude/skills/ted-english-learning
cd ~/.claude/skills/ted-english-learning
pip install -r requirements.txt
```

## 使用方法

```
/ted-english-learning <PDF文件路径>
```

也可以直接粘贴英文文本，无需 PDF。

## 核心流程（严格执行）

1. **提取内容**：如果提供 PDF，直接调用 `python <skill目录>/tools/extract_pdf.py <PDF路径>` 提取文本，**不要自己写提取脚本**
2. **生成 MD 笔记**：使用模板 `<skill目录>/tools/templates/ted_note_template.md` 填空，输出到 `{工作目录}/English/TED/[源文件名].md`
3. **生成 Canvas**：使用模板 `<skill目录>/tools/templates/ted_canvas_template.json` 替换内容，输出到 `{工作目录}/English/TED/CANVAS/[源文件名].canvas`
4. **更新索引**：按规则更新 `{工作目录}/English/English.md` 的TED文章列表，不需要更新学习进度

> **路径说明**：
> - `<skill目录>` = Claude Code 的 skills 目录下的 `ted-english-learning` 文件夹
> - `{工作目录}` = 用户当前的工作目录（即执行命令时所在的目录）

## 固定规则

### 命名规则
- **必须使用源PDF文件名作为输出文件名**，不要自动提取英文标题重命名
- 例如：输入 `你可以冒一点风险来增加你的运气.pdf` → 输出 `你可以冒一点风险来增加你的运气.md`

### 路径规则
- MD 笔记路径：`{工作目录}/English/TED/{源文件名}.md`
- Canvas 路径：`{工作目录}/English/TED/CANVAS/{源文件名}.canvas`
- 详细输出规范见：`<skill目录>/tools/templates/ted_output_spec.md`（按需查阅，不用每次完整读）

### 索引更新规则
1. **TED文章列表**：新条目以 `## {演讲中文标题}` 的二级标题格式插入到第一篇 TED 文章之前（倒序，最新在上）
2. **不需要更新学习进度**：不要修改学习进度部分的内容

## 内容质量要求
- 中英文对照按语义切分 5-15 段，交替出现，不要编号
- 生词表 20-30 个核心词，排除基础词
- 长难句 3-5 句，分析清晰
- 阅读理解 5 道题，符合考研风格
- Canvas 使用模板预设的坐标和节点，只替换 text 内容，不要重新计算布局

## Canvas 生成强制规则（不遵守会导致文件打不开）
1. **JSON格式绝对正确**：所有text字段中绝对不能出现未转义的英文双引号 `"`，统一使用中文引号「」或『』代替，生成后必须用 `json.loads()` 校验格式合法
2. **color字段必须有值**：使用 `"1"`-`"7"` 的字符串，不允许空字符串 `""`
3. **禁止修改节点结构**：不要增删节点、不要修改坐标和尺寸，只替换text字段的内容
4. **编码统一**：使用 UTF-8 编码，不允许出现乱码

## 输出示例

### 学习笔记 (.md)

```
📝 TED 学习笔记
├── 演讲标题 + 演讲者信息
├── 中英文对照全文（5-15 段）
├── 生词表（20-30 个核心词）
│   └── 音标 + 词性 + 中文释义 + 例句
├── 内容摘要
│   ├── 核心观点
│   ├── 演讲结构
│   └── 金句摘录
├── 长难句分析（3-5 句）
├── 阅读理解（5 道考研风格题）
└── 学习拓展
    ├── 口语模仿
    ├── 写作练习
    └── 讨论话题
```

### 思维导图 (.canvas)

Obsidian Canvas 格式，包含 7 个节点：
- 中心节点：标题、演讲者、核心隐喻
- 演讲结构
- 核心观点
- 金句摘录
- 关键词汇
- 学习收获
- 行动清单

## 故障排除

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| PDF 提取失败 | PDF 为扫描图片格式 | 使用 OCR 工具先转换 |
| Canvas 打不开 | JSON 格式错误 | 检查 text 字段是否有未转义的引号 |
| 找不到模板文件 | skill 目录不完整 | 重新克隆仓库 |
| PyPDF2 未安装 | 缺少依赖 | `pip install PyPDF2` |

## 注意事项

- 仅支持文字型 PDF（不支持纯图片扫描件）
- Canvas 文件需要 Obsidian 打开
- 输出文件名与源 PDF 文件名保持一致
- 提取的学习内容仅供个人学习使用
