# TeacherKit - AI 备课助手 / AI Lesson Prep Kit

> 🎓 为教师打造的一站式 AI 备课工具——一键生成教案、试题、课程大纲、课件PPT大纲、说课稿，覆盖小学到研究生。
>
> 🎓 One-stop AI lesson preparation toolkit for educators — lesson plans, quizzes, syllabi, slide outlines and lesson-presentation scripts, from primary school to graduate level.

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

### 4. 🖥️ 课件PPT大纲 / Slide Outline *(v1.1 新增)*
逐页给出标题、要点、配图/动画建议和讲解备注，可直接交给 PPT 工具生成课件。

Page-by-page slide outline with titles, bullets, visual suggestions and speaker notes.

### 5. 🎤 说课稿 / Lesson Presentation Script *(v1.1 新增)*
按"说教材—说学情—说目标—说教法—说过程—说板书—说反思"标准结构，附评委追问预案，适用于教学比赛、教师招聘面试。

Standard 说课 script for teaching competitions and interviews, with likely judge questions.

### 学段自适应 / Grade-level aware *(v1.1 新增)*
支持小学（1课时=40分钟）、初中、高中、高职、本科、研究生；中小学按新课标核心素养表述教学目标。

## 🚀 Quick Start / 快速开始

### As an Agent Skill / 作为技能安装（ClawHub · SkillHub · Claude Code）

```bash
clawhub install teacher-kit
```

或将本仓库的 `SKILL.md` 放入 `~/.claude/skills/teacher-kit/`。

### As an OpenWebUI Tool / 安装到 OpenWebUI

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

给初二物理"浮力"做一份14页的课件大纲

帮我写一份人教版七年级上册《一元一次方程》的说课稿，15分钟
```

### User Settings / 用户配置

In OpenWebUI → Tools → TeacherKit → User Settings:

| Setting | Options | Default |
|---------|---------|---------|
| Subject | Any (e.g. 计算机科学) | Empty |
| Student Level | 小学 / 初中 / 高中 / 高职 / 本科 / 研究生 | 本科 |
| Language | 中文 / English / Bilingual | 中文 |

## 🔧 Technical Details / 技术说明

- **Zero dependencies** — no external APIs, no pip packages needed
- **Pure prompt engineering** — crafts structured prompts for the LLM to generate professional educational content
- **Works with any model** — compatible with all LLMs supported by OpenWebUI
- **Bilingual support** — output in Chinese, English, or both

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md).

## 📄 License

MIT

## 👤 Author

**dongsheng123132** — [GitHub](https://github.com/dongsheng123132)
