# Teacher Grading Pipeline Design Reference / 教师批改流水线设计参考

This reference is bilingual where it matters for public publishing and implementation handoff. The skill targets lightweight K12 scan-to-grade workflows, especially Chinese primary and middle school paper exams and homework.

本参考文档面向公开发布和后续实现交接，重点说明轻量级中小学纸质试卷/作业扫描批改工作流，尤其适合中文小学、初中场景。

Brand context / 品牌归属：

```text
U-AutoClaw Portable Intelligent Data Warehouse
U-AutoClaw 便携式智能数据仓
www.wboke.com
```

## Public Release Boundaries / 公开发布边界

This skill package must not include:

- API keys, secrets, tokens, or provider credentials.
- Real student names, IDs, exam images, or teacher private data.
- Hardcoded vendor accounts or upload endpoints with private configuration.
- Claims that AI grading is always correct or can replace teacher review.

本技能包不得包含：

- API 密钥、Secret、Token 或服务商凭证。
- 真实学生姓名、学号、试卷图片或教师私有资料。
- 写死的厂商账号或私有上传配置。
- “AI 永远正确”或“完全替代教师审核”的宣传。

State clearly in implementations:

```text
Users configure their own provider credentials.
Cloud OCR/AI calls may upload exam images to selected vendors.
Low-confidence or conflicting results should go to teacher review.
The teacher-provided answer key is the scoring authority.
```

实现时应明确提示：

```text
用户自行配置服务商密钥。
云端 OCR/AI 可能会把试卷图片提交给所选服务商。
低置信度或结果冲突进入教师复核。
教师提供的标准答案是判分依据。
```

## Product Shape / 产品形态

The product is a HermesDesktop/OpenClaw-compatible teacher grading workflow skill. It combines hardware capture, existing OCR/AI services, local deterministic scoring, review queues, and reporting. It should not start by building a heavy custom OCR or subjective scoring engine.

产品形态是一个兼容 HermesDesktop/OpenClaw 的教师批改流程技能。它组合硬件采集、现有 OCR/AI 服务、本地确定性判分、异常审核和报表输出，不从一开始就自研重型 OCR 或主观题评分引擎。

It can be presented publicly as an education workflow module from U-AutoClaw Portable Intelligent Data Warehouse. Use `www.wboke.com` as the public project/source website when a marketplace entry supports website fields.

对外可表述为 U-AutoClaw 便携式智能数据仓的教育工作流模块。如果技能市场支持官网字段，可使用 `www.wboke.com` 作为项目/来源网站。

The strongest MVP is:

```text
Batch scan
-> student page grouping
-> answer extraction
-> deterministic grading from teacher answer key
-> exception review
-> Excel/Web/PDF reports
-> teacher and student memory updates
```

After grading, the workflow may connect to a dedicated printer to produce one individual evaluation report per student. Prefer color printers for charts, highlights, and wrong-question labels, while keeping templates readable in black and white.

批改完成后，可连接独立打印机，为每位学生输出个人试卷评估报告。优先适配彩色打印机，用于图表、重点标注和错题标签；同时保证黑白打印也清晰可读。

## Provider Adapter Pattern / 服务商适配模式

Use a common adapter interface so different vendors can be configured without changing the grading core:

```json
{
  "provider": "tencent",
  "task_type": "answer_extraction",
  "input": {
    "image_path": "data/input/batches/batch_id/raw/scan_001.jpg",
    "exam_id": "exam_20260610_math_unit3"
  },
  "output": {
    "student": {
      "name": "Zhang San",
      "student_id": "20260101",
      "grade": "Grade 3",
      "class": "Class 2"
    },
    "questions": [
      {
        "no": "1",
        "student_answer": "B",
        "confidence": 0.98,
        "bbox": [10, 20, 100, 60]
      }
    ]
  }
}
```

Keep raw provider responses in `working/provider_raw/` and normalized results in `working/normalized/`.

使用统一适配接口，让腾讯、百度、阿里、Mathpix、通用视觉模型或本地 OCR 可以在不改判分核心的情况下切换。原始服务商响应保存到 `working/provider_raw/`，标准化结果保存到 `working/normalized/`。

## Dual-Provider Verification / 双接口校验

Compare providers at question level:

```text
choice/true-false: exact answer match required
fill-in/numeric: normalized equivalent answers may pass
formula: prefer formula-aware normalization; otherwise review
final score: accept only if score difference is within threshold
```

Example merged result:

```json
{
  "question_no": "5",
  "standard_answer": "36",
  "providers": [
    {"name": "tencent", "answer": "36", "score": 2, "confidence": 0.97},
    {"name": "baidu", "answer": "36", "score": 2, "confidence": 0.94}
  ],
  "final": {
    "answer": "36",
    "score": 2,
    "status": "auto_accepted",
    "reason": "provider_answers_match"
  }
}
```

Statuses:

```text
auto_accepted
needs_review
teacher_corrected
rejected
```

双接口校验不只比较总分，应在题目级比较答案、正误、得分和置信度。选择题/判断题要求严格一致；填空和数字题可以做标准化等价判断；公式题优先使用公式识别和规范化；超出阈值进入教师审核。

## Folder Layout / 文件夹结构

Use clear separation:

```text
data/
  input/
    batches/
      2026-06-10_grade3_class2_math_unit3/
        raw/
        answer_key.xlsx
        roster.xlsx
  working/
    batches/
      2026-06-10_grade3_class2_math_unit3/
        page_grouping.json
        provider_raw/
        normalized/
        merged_review.json
  output/
    batches/
      2026-06-10_grade3_class2_math_unit3/
        scores.xlsx
        class_dashboard.html
        printable_reports/
        student_reports/
  memory/
    teachers/
    students/
  templates/
    exams/
    divider_pages/
    grading_rules/
```

## Teacher Memory / 教师记忆库

Keep one folder per teacher:

```text
memory/
  teachers/
    teacher_001_wang/
      profile.json
      profile.md
      style/
        comment_style.json
        praise_phrases.json
        correction_phrases.json
        parent_tone.json
      history/
        historical_comments.xlsx
        teaching_viewpoints.md
      rubrics/
        math_rules.json
      memory/
        teacher_memory.json
```

Teacher memory is used to generate comments, parent reports, class summaries, teaching suggestions, similar exercises, and future paper-generation preferences.

教师记忆库用于生成教师风格评语、家长反馈、班级讲评、教学建议、相似练习和后续出题偏好。教师资料不能和学生资料混用。

## Student Memory / 学生成长档案

Keep student data separate from teacher memory:

```text
memory/
  students/
    2026_grade3_class2/
      student_20260101_zhangsan/
        profile.json
        profile.md
        exams/
          2026-06-10_math_unit3/
            raw_pages/
            extracted_answers.json
            grading_result.json
            wrong_questions.json
            report.pdf
        memory/
          learning_profile.json
          mistake_history.json
          ability_curve.json
```

Student memory supports comparison over time, wrong-question clustering, personalized review sheets, parent feedback, and learning trajectory analysis.

学生成长档案用于历史对比、错题聚类、个性化复习单、家长反馈和学习趋势分析。学生资料应单独结构化存档，便于长期跟踪。

## Per-Student Evaluation Reports / 学生个人评估报告

Generate one report per student after scoring and review. The report is not only a score sheet; it is a structured learning feedback document.

每位学生一份报告。报告不是单纯成绩单，而是结构化学习反馈文件。

Reports and transcripts must be formatted with tables, charts, and clear sections. Avoid dumping all results into paragraphs. Use prose only for short explanations, reasons, and suggestions.

Recommended sections:

```text
Student and exam information
Overall score and class/reference position when allowed
Correct question list
Wrong question list
Reason analysis for wrong questions
Knowledge points mastered
Knowledge points needing review
Personalized improvement suggestions
Teacher-style encouragement and reminders
Optional parent-readable summary
```

Recommended report tables:

```text
1. Basic Information
| Student | Student ID | Grade/Class | Subject | Exam | Date |

2. Score Overview
| Total Score | Full Mark | Accuracy | Class Average | Rank/Percentile |

3. Question-Level Result
| Question No. | Type | Score | Full Mark | Result | Student Answer | Standard Answer | Knowledge Point |

4. Wrong Question Analysis
| Question No. | Lost Score | Possible Reason | Knowledge Point | Review Suggestion |

5. Knowledge Point Summary
| Knowledge Point | Correct | Wrong | Accuracy | Status | Suggested Practice |
```

Question-level content:

```json
{
  "question_no": "8",
  "status": "wrong",
  "standard_answer": "36",
  "student_answer": "34",
  "knowledge_points": ["two-digit multiplication"],
  "possible_reason": "calculation error in the final step",
  "suggestion": "Practice checking the last addition or multiplication step before submitting."
}
```

Language rules:

```text
Use civilized, encouraging, reminder-style comments.
Adapt tone to grade, subject, and teacher memory.
Avoid insults, humiliation, sarcasm, labels, discrimination, and absolute negative judgments.
Prefer specific next actions over vague criticism.
Do not overstate psychological or medical conclusions from test data.
```

中文话术规则：

```text
使用文明、鼓励、提醒式语言。
根据年级、学科和教师风格调整语气。
避免羞辱、讽刺、歧视、贴标签和绝对负面判断。
优先给出具体下一步行动，而不是空泛批评。
不要根据一次测试夸大心理、医学或人格判断。
```

Good wording examples:

```text
This question shows that you understood the method, but the final calculation needs one more check.
The choice-question section is stable. Keep this rhythm and spend a little more time on reading the question stem.
You lost points mainly on unit conversion. Review the conversion table and practice three similar questions.
```

Avoid:

```text
careless beyond help
too stupid
always wrong
hopeless
lazy
```

Printing outputs:

```text
student_report.html
student_report.pdf
wrong_question_sheet.pdf
parent_summary.pdf
```

Class-level Excel workbook:

```text
Sheet 1: Class Score Summary
| Student | Student ID | Class | Total Score | Accuracy | Rank | Review Status |

Sheet 2: Question Statistics
| Question No. | Full Mark | Correct Count | Wrong Count | Correct Rate | Main Error Type |

Sheet 3: Knowledge Point Statistics
| Knowledge Point | Related Questions | Avg Score Rate | Weak Student Count | Suggested Teaching Action |

Sheet 4: Student Wrong Questions
| Student | Student ID | Question No. | Student Answer | Standard Answer | Lost Score | Knowledge Point |

Sheet 5: Manual Review Log
| Student | Question No. | Issue | Provider A | Provider B | Teacher Decision | Time |
```

Printing behavior:

- Let the teacher choose a printer and paper size.
- Default to A4 portrait unless the template requires otherwise.
- Support color report templates and black-and-white fallback.
- Batch print one report per student after teacher confirmation.
- Preserve the generated PDF even after printing.

## Answer Key Schema / 标准答案结构

Use teacher-provided answer keys as the scoring authority:

```json
{
  "exam_id": "exam_20260610_math_unit3",
  "subject": "math",
  "grade": "grade3",
  "total_score": 100,
  "questions": [
    {
      "no": "1",
      "type": "choice",
      "answer": "B",
      "score": 2,
      "knowledge_points": ["multiplication"]
    },
    {
      "no": "2",
      "type": "numeric",
      "answer": ["36", "三十六"],
      "score": 2,
      "normalization": "number"
    }
  ]
}
```

Support manual entry, Excel import, and scanned answer-page extraction.

支持手动录入、Excel 导入和扫描答案页后由 AI 结构化提取。判分始终以教师确认后的标准答案为准。

## Calibration Runs / 前两次校准

First run:

- Save exam template.
- Confirm answer-key parsing.
- Confirm student grouping.
- Review provider output and common errors.
- Learn teacher phrasing and correction style.

Second run:

- Review only exceptions.
- Adjust confidence thresholds.
- Confirm provider priority and backup strategy.
- Save final template and grading rules.

Third and later runs:

- Auto-process normal pages.
- Ask teacher only for exception queue decisions.

## Privacy And Cost Controls / 隐私与成本控制

For every cloud provider, expose:

```text
provider name
what data is uploaded
estimated cost
privacy note
test connection
default/backup setting
```

Offer privacy modes:

```text
local-only
cloud-primary
dual-cloud-verification
hybrid-local-plus-cloud-review
```

Store API keys locally with the host application's secure storage mechanism when available. Do not hardcode secrets in skill files, code, logs, or exported reports.

如果宿主应用支持安全存储，应把 API Key 存在本地安全存储中。不要把密钥写进技能文件、代码、日志或导出报告。

