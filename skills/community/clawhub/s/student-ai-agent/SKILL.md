---
name: student-ai-agent
version: 1.0.0
description: 学术项目一键工作流。输入作业要求，自动完成 7 步：分析需求 → 方案设计 → 写代码 → 验证运行 → 生成 Word 报告 → 生成 PPT + 演讲稿 → 模拟 Q&A。输出可直接提交的 .docx、.pptx 和配套材料。
triggers: [作业, assignment, 帮我做, 按工作流跑, 学术项目, homework, final project, coursework]
---

# Student AI Agent - 学术项目工作流

## 概述

将一份作业要求转化为完整的交付物：代码、报告、PPT、演讲稿、Q&A 准备。

**适用场景**：
- 用户发来一份作业 PDF/文本，说"帮我做"或"按工作流跑一遍"
- 用户说"帮我做 PPT"/"帮我写报告"等单步请求

## 项目结构

```
student-ai-agent/
├── SKILL.md            ← 本文件
├── input/              ← 用户的作业要求
│   └── assignment.md
├── output/             ← 所有生成产物
│   ├── 01_analysis.json
│   ├── 02_brainstorm.json
│   ├── code/main.py
│   ├── figures/*.png
│   ├── report/report.docx
│   ├── presentation/slides.pptx
│   ├── presentation/speaker_notes.md
│   └── qa/qa_preparation.md
└── scripts/            ← 格式化输出工具
    ├── generate_report.py
    ├── generate_ppt.js
    ├── generate_notes.py
    └── qa_simulator.py
```

## 依赖

```bash
pip install python-docx matplotlib numpy pandas Pillow
npm install -g pptxgenjs
```

安装检查：执行前先确认依赖已就绪，缺什么装什么，不阻塞用户。

## 执行流程（7 步）

收到用户作业要求后，按顺序执行以下步骤。每步完成后告知用户进度。

---

### Step 1: 分析作业要求

**输入**：用户提供的作业文本/PDF/图片
**AI 任务**：
1. 提取：课程名、主题、截止日期
2. 识别：交付物清单（报告、代码、PPT 等）
3. 解析：评分标准（rubric）及各项权重
4. 列出：格式约束（字数限制、引用格式、文件格式等）
5. 提炼：核心问题（作业到底要你解决什么）

**输出**：将结构化分析写入 `output/01_analysis.json`

```json
{
  "course": "课程名",
  "topic": "项目主题",
  "deadline": "截止日期",
  "deliverables": ["report.docx", "code.py", "slides.pptx"],
  "constraints": {"word_limit": 3000, "format": "APA", "language": "English"},
  "grading_criteria": [{"item": "Technical correctness", "weight": 40}],
  "key_questions": ["需要解决的核心问题"],
  "technical_requirements": ["Python", "ML pipeline"]
}
```

---

### Step 2: 方案设计

**AI 任务**：
1. 头脑风暴 2-3 个可行方案
2. 按"创新性 × 可实现性 × 评分匹配度"选择最优方案
3. 确定技术栈、数据来源、预期结果
4. 识别创新点（教授看重的加分项）

**输出**：写入 `output/02_brainstorm.json`

```json
{
  "approaches": [{"name": "方案名", "pros": [], "cons": []}],
  "selected_approach": "选定方案及理由",
  "architecture": "技术架构描述",
  "methodology": "方法论",
  "data_sources": ["数据来源"],
  "innovation_points": ["创新点"]
}
```

---

### Step 3: 写代码

**AI 任务**：
1. 根据方案设计编写完整可运行的 Python 代码
2. 自带 mock 数据（不依赖外部 API 或付费数据集）
3. 代码必须能生成图表（matplotlib/seaborn）
4. 包含清晰注释和 docstring
5. 写 `requirements.txt`

**输出**：
- `output/code/main.py` — 主程序
- `output/code/requirements.txt` — 依赖

**约束**：
- 代码必须能 `python main.py` 一键运行
- 图片输出到 `output/figures/`
- 不使用需要 API key 的服务

---

### Step 4: 验证运行

**AI 任务**：
1. 实际运行 `output/code/main.py`
2. 确认无报错
3. 确认图片已生成到 `output/figures/`
4. 如果报错：修复代码 → 重跑，最多 3 次

**输出**：`output/04_check_results.json`

```json
{
  "syntax_check": true,
  "runs_without_error": true,
  "figures_saved": ["output/figures/fig1.png"],
  "errors_found": [],
  "fix_attempts": 0
}
```

---

### Step 5: 生成 Word 报告

**AI 任务**：
1. 根据分析结果确定报告结构
2. 撰写完整学术内容（Introduction → Methodology → Implementation → Results → Discussion → Conclusion → References）
3. 构造报告 JSON
4. 调用 `scripts/generate_report.py` 生成 .docx

**执行命令**：
```bash
cd ~/Desktop/student-ai-agent
python scripts/generate_report.py output/report/report_data.json
```

**报告 JSON 格式**（写入 `output/report/report_data.json`）：
```json
{
  "title": "报告标题",
  "student_name": "学生姓名",
  "course_name": "课程名",
  "sections": [
    {"heading": "1. Introduction", "content": "完整段落文字...", "level": 1}
  ],
  "figures": ["output/figures/fig1.png"],
  "code_file": "output/code/main.py"
}
```

**输出**：`output/report/report.docx`

---

### Step 6: 生成 PPT + 演讲稿

**AI 任务**：
1. 设计 10-15 页 PPT 结构
2. 每页写清标题 + 要点（bullet points）
3. 选择配色主题（dark_modern / ocean / forest）
4. 为每页写演讲稿
5. 调用脚本生成

**PPT 大纲 JSON**（写入 `output/presentation/presentation_outline.json`）：
```json
{
  "author": "Student Name",
  "design": {"theme": "dark_modern"},
  "slides": [
    {"type": "title", "title": "标题", "subtitle": "副标题", "notes": "演讲稿"},
    {"type": "content", "title": "标题", "points": ["要点1", "要点2"], "notes": "演讲稿"},
    {"type": "chart", "title": "Results", "image": "output/figures/fig1.png", "notes": "演讲稿"},
    {"type": "qa", "content": "Thank you!"}
  ]
}
```

**执行命令**：
```bash
cd ~/Desktop/student-ai-agent
node scripts/generate_ppt.js output/presentation/presentation_outline.json output/presentation/slides.pptx
```

**演讲稿**：单独写一份详细的逐页演讲稿到 `output/presentation/speaker_notes.md`，包含：
- 每页说什么（逐字稿级别）
- 过渡句
- 时间控制建议

**输出**：
- `output/presentation/slides.pptx`
- `output/presentation/speaker_notes.md`

---

### Step 7: 模拟 Q&A

**AI 任务**：
1. 基于项目内容，预测教授最可能问的 10-15 个问题
2. 按难度分类：基础 / 方法论 / 挑战性
3. 为每个问题写回答框架（不是完整答案，是思路 + 关键词）
4. 附上回答技巧

**输出**：写入 `output/qa/qa_preparation.md`，格式：

```markdown
# Q&A 准备

## 🟢 基础问题（一定会被问到）
### Q: Why did you choose this approach?
**回答框架**: 列 2-3 个备选方案 → 说评估标准 → 解释为什么选这个
**关键词**: scalability, simplicity, alignment with rubric

## 🟡 方法论问题
...

## 🔴 挑战性问题
...

## 💡 万能应对策略
- 不知道的：承认 → 假设 → 下一步
- 被 challenge 的：acknowledge → 解释 reasoning → 提出改进方向
```

---

## 单步执行

用户也可以要求只跑其中一步：

| 用户说 | 执行 |
|--------|------|
| "先分析一下这个作业" | 只跑 Step 1 |
| "帮我写代码" | Step 1-4 |
| "帮我写报告" | Step 1-5 |
| "帮我做 PPT" | Step 1-2 + Step 6 |
| "帮我准备 Q&A" | Step 1-2 + Step 7 |
| "按工作流跑一遍" | Step 1-7 全部 |

---

## 输出交付

全部完成后，告诉用户：

```
✅ 全部完成！文件都在 output/ 目录下：

📁 output/
├── code/main.py          — 源代码（可直接运行）
├── figures/              — 图表
├── report/report.docx   — Word 报告
├── presentation/
│   ├── slides.pptx      — PPT
│   └── speaker_notes.md — 演讲稿
└── qa/qa_preparation.md  — Q&A 准备

需要我调整哪个部分吗？
```

---

## 配色主题参考

| 主题 | 适用 | 主色 |
|------|------|------|
| `dark_modern` | 技术/CS课程 | 深蓝 + 靛蓝 + 青色 |
| `ocean` | 数据分析/商业 | 海蓝 + 深蓝 + 绿 |
| `forest` | 环境/可持续 | 深绿 + 黄绿 + 金色 |

---

## 注意事项

1. **语言**：默认英文输出（报告、PPT、Q&A），用户要求中文时切换
2. **格式**：报告默认 APA 格式，可按要求切换 IEEE/Harvard
3. **原创性**：代码和内容必须原创生成，不直接复制现有解决方案
4. **引用**：报告中的 References 需使用真实的学术引用（作者/年份/DOI），不编造
5. **图表**：代码生成的图表必须有标题、坐标轴标签、图例
