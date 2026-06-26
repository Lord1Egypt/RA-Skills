"""
title: TeacherKit - AI 备课助手
author: dongsheng123132
author_url: https://github.com/dongsheng123132
funding_url: https://github.com/dongsheng123132
version: 1.0.0
license: MIT
description: AI-powered lesson preparation toolkit for educators. Generate lesson plans, quizzes, and course outlines with structured, professional output. Zero dependencies, works with any LLM. 为教师打造的 AI 备课助手——一键生成教案、试题、课程大纲。
required_open_webui_version: 0.4.0
"""

from pydantic import BaseModel, Field
from typing import Callable, Awaitable, Any, Optional


class Tools:
    class Valves(BaseModel):
        max_quiz_questions: int = Field(
            default=20,
            description="Maximum number of quiz questions allowed per generation",
        )

    class UserValves(BaseModel):
        subject: str = Field(
            default="",
            description="Default subject/discipline (e.g. 计算机科学, Mathematics). Leave empty to specify each time.",
        )
        student_level: str = Field(
            default="本科",
            description="Student level: 本科(Undergraduate) / 研究生(Graduate) / 高职(Vocational) / 高中(High School)",
        )
        language: str = Field(
            default="中文",
            description="Output language: 中文(Chinese) / English / Bilingual",
        )

    def __init__(self):
        self.valves = self.Valves()

    async def generate_lesson_plan(
        self,
        course_name: str,
        topic: str,
        duration: str = "2学时",
        teaching_goals: str = "",
        __user__: dict = {},
        __event_emitter__: Callable[[dict], Awaitable[None]] = None,
    ) -> str:
        """
        Generate a complete lesson plan (教案) for a specific topic.
        Use this when the user wants to prepare a lesson plan, teaching plan, or 教案.
        The output includes teaching objectives, key points, difficulties, teaching process,
        board design, and homework assignments.

        :param course_name: Name of the course (e.g. 数据结构, Python程序设计, Linear Algebra)
        :param topic: Specific topic or chapter (e.g. 二叉树的遍历, 第3章 栈与队列)
        :param duration: Class duration (e.g. 2学时, 90 minutes). Default: 2学时
        :param teaching_goals: Optional specific teaching goals or requirements
        :return: A structured prompt for the LLM to generate the lesson plan
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"正在生成「{course_name} - {topic}」教案...",
                        "done": False,
                    },
                }
            )

        user_valves = __user__.get("valves", self.UserValves())
        subject = user_valves.subject or ""
        level = user_valves.student_level or "本科"
        lang = user_valves.language or "中文"

        subject_hint = f"学科领域：{subject}\n" if subject else ""
        goals_hint = f"\n用户特别要求：{teaching_goals}" if teaching_goals else ""

        lang_instruction = self._get_lang_instruction(lang)

        prompt = f"""你是一位经验丰富的大学教学专家和教学设计师。请根据以下信息，生成一份完整、专业、可直接使用的教案。

## 基本信息
- 课程名称：{course_name}
- 授课主题：{topic}
- 授课时长：{duration}
- 学生层次：{level}
{subject_hint}{goals_hint}

## 教案要求

请严格按照以下结构输出教案：

### 📋 教案基本信息
| 项目 | 内容 |
|------|------|
| 课程名称 | {course_name} |
| 授课主题 | {topic} |
| 授课时长 | {duration} |
| 授课对象 | {level}学生 |
| 编写日期 | （当前日期） |

### 🎯 教学目标
分三个层次编写：
1. **知识目标**（Knowledge）：学生应掌握的核心知识点（3-5条）
2. **能力目标**（Skills）：学生应获得的能力提升（2-3条）
3. **素养目标**（Competence）：思维方式、职业素养等（1-2条）

### 🔑 教学重点与难点
- **重点**：（2-3个核心知识点）
- **难点**：（1-2个学生容易困惑的点）
- **突破策略**：针对每个难点给出具体的教学策略

### 📚 教学过程

按时间线详细展开，包含以下环节：

#### 1️⃣ 课程导入（约{self._calc_time(duration, 0.1)}）
- 引入方式（案例/问题/回顾）
- 具体内容

#### 2️⃣ 新知讲授（约{self._calc_time(duration, 0.5)}）
- 知识点分解与讲授顺序
- 每个知识点的讲解方式
- 关键例题/案例
- 师生互动设计

#### 3️⃣ 实践环节（约{self._calc_time(duration, 0.25)}）
- 课堂练习/讨论/实验
- 具体任务描述

#### 4️⃣ 总结提升（约{self._calc_time(duration, 0.1)}）
- 知识梳理与总结
- 思维导图/知识框架

#### 5️⃣ 课后作业（约{self._calc_time(duration, 0.05)}）
- 必做题（巩固基础）
- 选做题（拓展提升）

### 🖊️ 板书设计
用文字描述板书的布局和关键内容。

### 📖 教学反思（预设）
- 可能遇到的教学问题
- 备选方案

{lang_instruction}

请确保教案内容专业、详实、可操作，适合直接用于课堂教学。"""

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": "教案生成提示已准备就绪", "done": True},
                }
            )

        return prompt

    async def generate_quiz(
        self,
        content_or_topic: str,
        num_questions: int = 5,
        question_types: str = "选择题,判断题,简答题",
        difficulty: str = "中等",
        __user__: dict = {},
        __event_emitter__: Callable[[dict], Awaitable[None]] = None,
    ) -> str:
        """
        Generate quiz questions from given content or topic.
        Use this when the user wants to create exam questions, quiz, test, or 出题/试题.
        Supports multiple question types: multiple choice, true/false, fill-in-the-blank, short answer.

        :param content_or_topic: The content text or topic to generate questions from
        :param num_questions: Number of questions to generate (default: 5)
        :param question_types: Comma-separated question types: 选择题(MCQ),判断题(T/F),填空题(Fill),简答题(Short Answer). Default: 选择题,判断题,简答题
        :param difficulty: Difficulty level: 简单(Easy)/中等(Medium)/困难(Hard). Default: 中等
        :return: A structured prompt for the LLM to generate quiz questions
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"正在准备出题（{num_questions}道，难度：{difficulty}）...",
                        "done": False,
                    },
                }
            )

        user_valves = __user__.get("valves", self.UserValves())
        level = user_valves.student_level or "本科"
        lang = user_valves.language or "中文"

        max_q = self.valves.max_quiz_questions
        if num_questions > max_q:
            num_questions = max_q

        lang_instruction = self._get_lang_instruction(lang)

        # Parse question types
        type_map = {
            "选择题": "选择题（单选，4个选项A/B/C/D）",
            "MCQ": "选择题（单选，4个选项A/B/C/D）",
            "判断题": "判断题（对/错）",
            "T/F": "判断题（对/错）",
            "填空题": "填空题",
            "Fill": "填空题",
            "简答题": "简答题",
            "Short Answer": "简答题",
            "多选题": "多选题（多选，4-5个选项）",
        }

        requested_types = [t.strip() for t in question_types.split(",")]
        formatted_types = []
        for t in requested_types:
            formatted_types.append(type_map.get(t, t))

        types_str = "、".join(formatted_types)

        difficulty_desc = {
            "简单": "基础概念理解，直接考查知识点记忆和简单应用",
            "Easy": "基础概念理解，直接考查知识点记忆和简单应用",
            "中等": "需要理解和分析，考查知识点的综合运用",
            "Medium": "需要理解和分析，考查知识点的综合运用",
            "困难": "需要深度分析和创新思维，考查高阶思维能力",
            "Hard": "需要深度分析和创新思维，考查高阶思维能力",
        }
        diff_desc = difficulty_desc.get(difficulty, difficulty_desc["中等"])

        prompt = f"""你是一位专业的教育测评专家。请根据以下内容和要求，生成高质量的试题。

## 出题依据

{content_or_topic}

## 出题要求

- **题目数量**：共 {num_questions} 道题
- **题型分布**：{types_str}（请合理分配各题型数量）
- **难度级别**：{difficulty}——{diff_desc}
- **适用对象**：{level}学生

## 输出格式

请严格按照以下格式输出：

---

# 📝 测验试题

**主题**：（根据内容自动提取）
**难度**：{difficulty} | **适用**：{level} | **题量**：{num_questions}题

---

## 一、试题部分

对每道题按以下格式输出：

**第 X 题**（题型 | 难度：⭐/⭐⭐/⭐⭐⭐）

题目内容...

（如果是选择题）
A. 选项1
B. 选项2
C. 选项3
D. 选项4

---

## 二、参考答案与解析

**第 X 题**
- **答案**：X
- **解析**：详细解释为什么选这个答案，以及其他选项为什么不对（如适用）
- **考查知识点**：该题考查的核心知识点

---

## 三、试题分析

| 题号 | 题型 | 难度 | 考查知识点 |
|------|------|------|-----------|
| 1 | ... | ... | ... |

{lang_instruction}

请确保：
1. 题目表述清晰、无歧义
2. 选择题的干扰项具有合理性
3. 答案解析详细、有教学价值
4. 知识点覆盖全面，难度分布合理"""

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": "试题生成提示已准备就绪", "done": True},
                }
            )

        return prompt

    async def generate_course_outline(
        self,
        course_name: str,
        total_hours: str = "32学时",
        textbook: str = "",
        additional_requirements: str = "",
        __user__: dict = {},
        __event_emitter__: Callable[[dict], Awaitable[None]] = None,
    ) -> str:
        """
        Generate a complete course outline/syllabus (课程大纲).
        Use this when the user wants to create a course outline, syllabus, teaching plan for an entire course, or 课程大纲.
        The output includes weekly schedule, topics, teaching content, and assessment methods.

        :param course_name: Name of the course (e.g. Python程序设计, 数据库原理)
        :param total_hours: Total teaching hours (e.g. 32学时, 48学时, 64 hours). Default: 32学时
        :param textbook: Textbook information (optional, e.g. 书名+作者+版次)
        :param additional_requirements: Any additional requirements for the outline
        :return: A structured prompt for the LLM to generate the course outline
        """
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": f"正在生成「{course_name}」课程大纲（{total_hours}）...",
                        "done": False,
                    },
                }
            )

        user_valves = __user__.get("valves", self.UserValves())
        subject = user_valves.subject or ""
        level = user_valves.student_level or "本科"
        lang = user_valves.language or "中文"

        subject_hint = f"- **学科领域**：{subject}\n" if subject else ""
        textbook_hint = f"- **参考教材**：{textbook}\n" if textbook else ""
        extra_hint = (
            f"\n### 特殊要求\n{additional_requirements}"
            if additional_requirements
            else ""
        )

        lang_instruction = self._get_lang_instruction(lang)

        # Calculate weeks
        weeks = self._calc_weeks(total_hours)

        prompt = f"""你是一位资深的课程设计专家和教学管理者。请根据以下信息，生成一份完整、专业的课程教学大纲。

## 课程基本信息

- **课程名称**：{course_name}
- **总学时**：{total_hours}
- **教学周数**：约 {weeks} 周
- **授课对象**：{level}学生
{subject_hint}{textbook_hint}{extra_hint}

## 大纲要求

请严格按照以下结构输出课程大纲：

---

# 📘 {course_name} 课程教学大纲

## 一、课程基本信息

| 项目 | 内容 |
|------|------|
| 课程名称 | {course_name} |
| 总学时 | {total_hours} |
| 授课对象 | {level} |
| 课程性质 | （必修/选修，请根据课程判断） |
| 先修课程 | （列出建议的先修课程） |

## 二、课程简介
（200字左右的课程描述）

## 三、课程目标
1. **知识目标**：（3-4条）
2. **能力目标**：（3-4条）
3. **素养目标**：（2-3条）

## 四、教学内容与学时分配

请用表格形式列出每周的教学安排：

| 周次 | 教学主题 | 主要内容 | 学时 | 教学方式 | 备注 |
|------|---------|---------|------|---------|------|
| 第1周 | ... | ... | ... | 讲授/实验/讨论 | |
| ... | ... | ... | ... | ... | |

**要求**：
- 覆盖全部 {total_hours}
- 内容由浅入深，循序渐进
- 包含适当的实践/实验环节
- 安排期中复习和期末复习

## 五、教学方法

列出本课程采用的教学方法及说明（讲授法、案例教学、项目驱动、翻转课堂等）

## 六、考核方式

| 考核项目 | 占比 | 说明 |
|---------|------|------|
| 平时成绩 | X% | （出勤、课堂表现） |
| 作业 | X% | （次数、形式） |
| 实验/项目 | X% | （如适用） |
| 期中考试 | X% | （形式） |
| 期末考试 | X% | （形式） |

## 七、推荐教材与参考资料

### 主教材
（如用户提供了教材信息则使用，否则推荐合适的教材）

### 参考书籍
（3-5本参考书）

### 在线资源
（推荐相关的 MOOC、网站等）

## 八、教学日历（详细版）

对每周展开更详细的教学内容说明，包括：
- 知识点清单
- 课前预习要求
- 课后作业安排

{lang_instruction}

请确保大纲：
1. 内容体系完整、逻辑清晰
2. 学时分配合理
3. 考核方式科学
4. 符合{level}教学规范"""

        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": "课程大纲生成提示已准备就绪", "done": True},
                }
            )

        return prompt

    # ── Helper Methods ──────────────────────────────────────

    def _get_lang_instruction(self, lang: str) -> str:
        if lang.lower() in ["english", "英文", "en"]:
            return "\n## Language\nPlease write the entire output in **English**."
        elif lang.lower() in ["bilingual", "双语"]:
            return "\n## Language\nPlease write the output in **bilingual format** (中英双语), with Chinese as the primary language and English translations for key terms and headings."
        else:
            return "\n## 语言\n请使用**中文**输出全部内容。专业术语可附英文标注。"

    def _calc_time(self, duration: str, ratio: float) -> str:
        """Calculate time allocation based on duration string and ratio."""
        import re

        match = re.search(r"(\d+)", duration)
        if match:
            total_min = int(match.group(1))
            # If the number looks like 学时 (small number), convert to minutes
            if total_min <= 10:
                total_min = total_min * 45  # 1学时 = 45分钟
            minutes = int(total_min * ratio)
            return f"{minutes}分钟"
        return f"{int(ratio * 100)}%时间"

    def _calc_weeks(self, total_hours: str) -> int:
        """Estimate number of teaching weeks from total hours."""
        import re

        match = re.search(r"(\d+)", total_hours)
        if match:
            hours = int(match.group(1))
            # Assume 2-4 hours per week, use 2 as default
            weeks = max(8, hours // 2)
            return min(weeks, 20)
        return 16
