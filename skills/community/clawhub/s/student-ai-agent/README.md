# 🤖 Student AI Agent - 项目工作流

一键完成学术项目的完整工作流：从作业分析到Q&A准备。

**ClawHub Skill**: 本项目是一个 OpenClaw Skill，安装后可直接对 AI 说“帮我做这个作业”即可自动执行完整工作流。

## 🚀 怎么用

### 方法一：直接跟 AI 对话（推荐）

把作业要求直接发给我，说一句：

> "帮我做这个作业"  或  "按工作流跑一遍"

我会按照7步流程自动完成所有工作。

### 方法二：手动运行脚本

```bash
# 1. 把作业要求放入 input/assignment.md
mkdir -p input
cp your_assignment.pdf input/

# 2. 安装依赖
pip install python-docx matplotlib numpy pandas Pillow
npm install -g pptxgenjs

# 3. 运行工作流
python scripts/workflow_runner.py
```

## 📋 7步工作流详解

| 步骤 | 做什么 | 输出 |
|------|--------|------|
| 1️⃣ 分析作业 | 解析要求、提取评分标准、识别约束 | `01_analysis.json` |
| 2️⃣ 扩展想法 | 头脑风暴、方案设计、技术选型 | `02_brainstorm.json` |
| 3️⃣ 写代码 | 实现核心逻辑、mock数据、生成结果 | `code/main.py` |
| 4️⃣ 检查代码 | 语法检查、运行测试、生成图片 | `figures/`, `04_check_results.json` |
| 5️⃣ 生成报告 | 学术格式的Word文档 | `report/report.docx` |
| 6️⃣ 做PPT | 演示文稿 + 逐页演讲稿 | `presentation/slides.pptx` + `speaker_notes.md` |
| 7️⃣ 模拟Q&A | 可能的问题 + 回答框架 | `qa/qa_preparation.md` |

## 📁 项目结构

```
student-ai-agent/
├── README.md              # 本文件
├── input/                 # ← 把作业要求放这里
│   └── assignment.md
├── output/                # ← 所有生成的文件在这里
│   ├── 01_analysis.json
│   ├── 02_brainstorm.json
│   ├── 04_check_results.json
│   ├── code/
│   │   ├── main.py
│   │   └── requirements.txt
│   ├── figures/
│   │   └── *.png
│   ├── report/
│   │   └── report.docx
│   ├── presentation/
│   │   ├── slides.pptx
│   │   ├── speaker_notes.md
│   │   └── presentation_outline.json
│   └── qa/
│       └── qa_preparation.md
├── scripts/               # 工作流脚本
│   ├── workflow_runner.py
│   ├── generate_report.py
│   ├── generate_ppt.js
│   ├── generate_notes.py
│   └── qa_simulator.py
└── templates/             # 模版（PPT配色、报告格式等）
```

## 🎨 PPT主题

内置3种配色方案：

| 主题 | 适用场景 |
|------|----------|
| `dark_modern` | 技术展示、CS课程 |
| `ocean` | 数据分析、商业课程 |
| `forest` | 可持续/环境相关课程 |

## ⚡ AI 工作模式

当你把作业发给我时，我会：

1. **分析**: 精确提取作业要求中的所有评分标准、约束、格式要求
2. **设计**: 选择最适合拿高分的方案（创新性 + 可实现性平衡）
3. **编码**: 写出能跑通的Python代码，自带mock数据，不依赖外部API
4. **验证**: 运行代码确认无错，生成所有图表
5. **报告**: 按学术格式生成完整的.docx报告
6. **演示**: 精美PPT + 逐页演讲稿，教你怎么讲
7. **Q&A**: 预测教授会问什么，准备好回答

## 💡 Tips

- 作业要求越详细越好（rubric/评分标准一定要给我）
- 如果有参考论文/课件，一起发给我效果更好
- 可以分步进行，比如"先分析一下这个作业要什么"
- 代码默认用Python，需要其他语言告诉我
- 报告默认英文，需要中文说一声
