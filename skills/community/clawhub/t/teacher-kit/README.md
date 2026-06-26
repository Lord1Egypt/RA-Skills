# TeacherKit - AI 备课助手 / AI Lesson Prep Kit

> 🎓 为教师打造的一站式 AI 备课工具——一键生成教案、试题、课程大纲。
>
> 🎓 One-stop AI lesson preparation toolkit for educators — generate lesson plans, quizzes, and course outlines in one click.

## ✨ Features / 功能

### 1. 📋 生成教案 / Generate Lesson Plan
输入课程名称和章节主题，自动生成包含教学目标、重难点、教学过程、板书设计、课后作业的完整教案。

Input course name and topic to auto-generate a complete lesson plan with objectives, key points, teaching process, board design, and homework.

### 2. 📝 智能出题 / Generate Quiz
基于课程内容自动生成多题型试题（选择题、判断题、填空题、简答题），含参考答案和详细解析。

Auto-generate multi-type questions (MCQ, T/F, fill-in-the-blank, short answer) with answers and explanations.

### 3. 📘 课程大纲 / Generate Course Outline
输入课程名称和总学时，生成完整的学期教学大纲，含周次安排、教学内容、考核方式。

Input course name and total hours to generate a full semester syllabus with weekly schedule, content, and assessments.

## 🚀 Quick Start / 快速开始

### Installation / 安装

1. Open your OpenWebUI instance
2. Go to **Workspace → Tools → "+"**
3. Paste the contents of `teacher_kit.py`
4. Click **Save**

### Usage / 使用

Start a new chat and try:

```
帮我生成一份《数据结构》第3章"栈与队列"的教案，2学时

根据以下内容出5道选择题和3道简答题：二叉树是一种重要的非线性数据结构...

帮我做一份《Python程序设计》16周（32学时）的课程大纲
```

### User Settings / 用户配置

In OpenWebUI → Tools → TeacherKit → User Settings:

| Setting | Options | Default |
|---------|---------|---------|
| Subject | Any (e.g. 计算机科学) | Empty |
| Student Level | 本科 / 研究生 / 高职 / 高中 | 本科 |
| Language | 中文 / English / Bilingual | 中文 |

## 🔧 Technical Details / 技术说明

- **Zero dependencies** — no external APIs, no pip packages needed
- **Pure prompt engineering** — crafts structured prompts for the LLM to generate professional educational content
- **Works with any model** — compatible with all LLMs supported by OpenWebUI
- **Bilingual support** — output in Chinese, English, or both

## 📄 License

MIT

## 👤 Author

**dongsheng123132** — [GitHub](https://github.com/dongsheng123132)
