---
name: quickclass-quiz-converter
description: "Convert learning materials (Word, PDF, images) into QuickClass quiz JSON format. Supports SINGLE_CHOICE, MULTIPLE_CHOICE, and TRUE_FALSE question types. Use when user wants to create QuickClass homework/quiz JSON from exam papers, worksheets, or teaching materials, or when user mentions QuickClass, 课堂作业, 题目转换, 试卷转JSON, or converting quiz/exam content to QuickClass format."
name_cn: QuickClass 作业转换器
description_cn: 将学习材料（Word/PDF/图片）转换为 QuickClass 课堂作业 JSON 格式，支持单选、多选、判断三种题型
create_source: super-agent-skill-creator
agent_created: true
author: "管老师"
---

# QuickClass 作业转换器

将 Word、PDF、图片等来源的试卷/练习题转换为 QuickClass 课堂作业 JSON 格式。

## 工作流程

### 第一步：提取题目

根据输入源类型，提取所有题目内容：

**Word 文件**: 使用 docx skill 读取文本，按题号解析。

**PDF 文件**: 使用 pdf skill 提取文本，按题号解析。若 PDF 为扫描件，使用 paddleocr-doc-parsing skill 进行 OCR。

**图片文件**: 使用 image_understanding 工具识别图片中的题目文字。

提取时需识别每道题的：
- 题目内容
- 题型（单选/多选/判断）
- 选项（选择题）
- 正确答案
- 难度（如可推断）
- 解析（如有）

### 第二步：生成中间 JSON

将提取结果整理为如下中间格式数组（保存到 `.temp/` 目录）：

```json
[
  {
    "type": "SINGLE_CHOICE",
    "content": "圆的半径和直径的关系是？",
    "options": {"A": "半径=直径", "B": "半径=直径/2", "C": "半径=直径×2", "D": "半径=直径×π"},
    "answer": "B",
    "difficulty": "BASIC",
    "score": 5,
    "explanation": "直径是半径的2倍，所以半径=直径÷2"
  }
]
```

**字段规范：**
- `type`: `SINGLE_CHOICE` | `MULTIPLE_CHOICE` | `TRUE_FALSE`
- `options`: 对象格式（脚本会自动转 JSON 字符串）；判断题为 `{}`
- `answer`: 单选=`"A"`；多选=`"A,B,C"`（逗号分隔）；判断=`"T"` / `"F"`
- `difficulty`: `BASIC` | `INTERMEDIATE` | `ADVANCED` | `EXPANDED`
- `score`: 数字，课堂作业模式下可为 0
- `explanation`: 解析文本，无则为 `null`
- `has_image`: 布尔值，该题原文含图示时设为 `true`（可选字段，默认 `false`）

### 第三步：运行转换脚本

```bash
python {SKILL_DIR}/scripts/convert_to_quickclass.py \
  --teacher "教师姓名" \
  --grade "三年级下学期" \
  --subject "数学" \
  --task-title "圆的认识" \
  --quiz-title "练习题" \
  --input .temp/questions.json \
  --output "教师_年级_学科_任务标题_课堂作业_测验标题.json"
```

`SKILL_DIR` 为本 skill 目录（即包含 SKILL.md 的目录）；在 WorkBuddy 中通常位于 `~/.workbuddy/skills/quickclass-quiz-converter`。运行脚本前，请先将 `SKILL_DIR` 替换为该技能的实际绝对路径。

### 第四步：含图题目处理

当原始材料中某道题含有图示（几何图、函数图、实验装置等）时，使用两个脚本完成处理：

#### 4a. 提取图片并映射题号

**情况一：Word 文件（内嵌图片）**

```bash
python {SKILL_DIR}/scripts/extract_images.py \
  --input "原始试卷.docx" \
  --output-dir .temp/images \
  --mapping .temp/image_mapping.json
```

输出：
- `--output-dir`：提取的图片文件（image_1.png, image_2.png, ...）
- `--mapping`：题号映射 JSON，格式：
```json
[
  {"image_file": "image_1.png", "question_number": 3, "page": 1, "context": "题干预览..."},
  {"image_file": "image_2.png", "question_number": 5, "page": 1, "context": "题干预览..."}
]
```

**映射原理**：脚本根据图片在文档中的位置（段落/页面），与最近的题号（"1."、"第2题"等格式）关联。映射后检查 `question_number` 为 0 的图片，用 `image_understanding` 工具人工确认题号。

**情况二：扫描件 PDF（整页扫描图，无法提取内嵌图片）**

对于扫描件 PDF，传统 `extract_images.py` 无法按位置就近匹配（整页图不具定位意义），需采用**视觉模型精准裁剪**方案：

1. **渲染整页为高清图片**：
   ```bash
   python {SKILL_DIR}/scripts/extract_images.py \
     --input "扫描件试卷.pdf" \
     --output-dir .temp/page_images \
     --render-pages
   ```
   输出：page_1.png ~ page_N.png（每页一张高清渲染图）

2. **用视觉模型定位含图题目的图片位置**：
   对每页渲染图使用 `image_understanding` 工具，询问"第X题的配图在页面中的精确位置（百分比）"。视觉模型返回坐标，例如：
   ```
   第9题流程图：左上X=15%, 左上Y=61%, 宽=37%, 高=16%
   ```

3. **构建含裁剪坐标的映射 JSON**：
   ```json
   [
     {
       "image_file": "",
       "question_number": 9,
       "page": 2,
       "context": "题干预览...",
       "crop": {"x": 12, "y": 58, "width": 43, "height": 22},
       "source_page": "page_2.png"
     }
   ]
   ```
   - `crop`：裁剪坐标（百分比），留少量边距（±3%）
   - `source_page`：来源整页渲染图文件名

4. **生成图示说明 Word 时自动裁剪**：
   使用 `generate_image_doc.py --pages-dir` 参数，脚本自动从整页渲染图中裁剪子区域并插入 Word。

> **重要**：扫描件场景不要使用位置就近匹配，因为：① 整页扫描图不具定位意义；② 答案/图示可能集中放置（如答案集中在最后几页），与题目不在同一页。必须用视觉模型逐页识别图片属于哪道题，再精准定位裁剪。

#### 4b. 识别图片内容并补充文字描述

对每张含图题目，用 `image_understanding` 工具读取图片，在中间 JSON 的 `content` 中补充简短文字描述。

示例：原文 `"如下图，求阴影面积"` → 补充后 `"如下图，直角三角形ABC中∠C=90°，AC=3cm，BC=4cm，求阴影面积"`

同时在中间 JSON 中为该题设置 `"has_image": true`。

#### 4c. 生成图示说明 Word 文档

**独立图片模式**（Word 内嵌图片）：
```bash
python {SKILL_DIR}/scripts/generate_image_doc.py \
  --mapping .temp/image_mapping.json \
  --images-dir .temp/images \
  --output "{teacher}_{grade}_{subject}_{taskTitle}_课堂作业_{quizTitle}_图示说明.docx" \
  --title "圆的认识 图示说明"
```

**裁剪模式**（扫描件 PDF，映射 JSON 中含 `crop` 和 `source_page` 字段）：
```bash
python {SKILL_DIR}/scripts/generate_image_doc.py \
  --mapping .temp/image_mapping.json \
  --images-dir .temp/page_images \
  --pages-dir .temp/page_images \
  --output "{teacher}_{grade}_{subject}_{taskTitle}_课堂作业_{quizTitle}_图示说明.docx" \
  --title "模拟试题 图示说明"
```

`--pages-dir` 指定整页渲染图所在目录。脚本检测到映射条目中有 `crop` + `source_page` 时，自动从整页渲染图中裁剪子区域；否则使用 `--images-dir` 中的独立图片文件。

生成的 Word 文档包含：
- 文档标题 + 深蓝色分隔线
- 说明文字：本文件为 QuickClass 课堂作业 JSON 的配套图示说明文档
- 每道题：`【第X题图示】` 标签 + 原图居中显示 + 题干预览
- 末尾说明文字

**无图的题目不生成此文档。**

### 第五步：输出文件命名

按 QuickClass 规范命名输出文件：
`{teacher}_{grade}_{subject}_{taskTitle}_课堂作业_{quizTitle}.json`

示例：`脸盆_三年级下学期_数学_圆的认识_课堂作业_圆的练习题.json`

## 题型识别规则

从原始材料中识别题型：

| 特征 | 题型 |
|------|------|
| 题干含"选择"、"以下哪项"，有 A/B/C/D 选项，答案为单个字母 | `SINGLE_CHOICE` |
| 题干含"多选"、"哪些"，有 A/B/C/D 选项，答案为多个字母 | `MULTIPLE_CHOICE` |
| 题干含"判断"、"正确/错误"、"对/错"，选项为"正确/错误" | `TRUE_FALSE` |

## 难度推断规则

| 特征 | 难度 |
|------|------|
| 直接记忆、定义识别、基础概念 | `BASIC` |
| 简单应用、一步推理、基本计算 | `INTERMEDIATE` |
| 综合应用、多步推理、跨知识点 | `ADVANCED` |
| 拓展延伸、开放性、超纲应用 | `EXPANDED` |

## 完整 Schema 参考

详见 [references/quickclass_schema.md](references/quickclass_schema.md)，包含所有字段定义、题型示例和注意事项。

## 常见问题

**Q: 判断题的 options 字段为什么是 `"{}"`？**
A: QuickClass 规范中判断题无需选项，固定传空 JSON 对象字符串。

**Q: 多选题答案格式？**
A: 逗号分隔且按字母序排列，如 `"A,B,C"`，不要加空格。

**Q: id 字段怎么生成？**
A: 使用脚本自动生成 CUID2 风格 ID，无需手动填写。

**Q: score 为 0 是否正常？**
A: 正常。QuickClass 课堂作业模式下，score 常设为 0，由系统另行计分。

**Q: 原题有图片怎么办？**
A: QuickClass JSON 不支持图片嵌入。当原题含图时，生成两个文件：JSON 中 content 补充文字描述，同时生成配套图示说明 Word 文档（原图+题号标注），学生对照查看。

**Q: 扫描件 PDF 的图片怎么处理？**
A: 扫描件每页是一整张扫描图，不能用传统的内嵌图片提取。需要：1) 将每页渲染为高清 PNG；2) 用视觉模型定位含图题目在页面中的精确位置（百分比坐标）；3) 在映射 JSON 中添加 `crop` 和 `source_page` 字段；4) 用 `generate_image_doc.py --pages-dir` 自动裁剪并生成图示说明。

**Q: 为什么扫描件不能用位置就近匹配？**
A: 扫描件的图片可能集中放置（如答案区域在最后几页），与题目不在同一页。位置就近匹配会导致图片被错误关联到其他题目。必须用视觉模型逐页识别图片属于哪道题。
