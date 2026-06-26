---
name: shiyi
description: >
  拾遗 · 通用考试备考追踪 Skill。适用于任何考试——GRE、雅思、考研、注会、高考、期末……
  核心功能：识别错题截图 → 自由标签分类 → 词库积累复用 → 二刷提醒 → 导出 Excel。
  触发关键词：做了题、错了、截图发来、导出错题、待二刷、记得、不记得、换考试。
  图片消息直接触发识别。
---

# 拾遗 · 通用备考追踪 Skill

## 一、首次安装

Skill 加载时发一条消息，问你在备考什么考试，之后不再重复。

```
拾遗已安装。

你在备考什么考试？比如：
  GRE、雅思、考研英语、注会、高考、期末……
  不在列表里也没关系。
```

输入考试名称后，Skill 加载对应的识别背景知识，之后截图识别精度更高。
如果后来换考试，发「换考试」即可重新配置，不影响已有错题记录。

---

## 二、与朱批录的核心差异

| | 朱批录 | 拾遗 |
|---|---|---|
| 适用范围 | 考公（国考/省考） | 任意考试 |
| 科目结构 | 固定5科（言语/数量/判断/资料/申论） | 自由标签，AI 自动生成 |
| 标签复用 | 不需要（科目是固定的） | tag_library 跨题目积累 |
| 考试切换 | 不支持 | 「换考试」指令随时切换 |

---

## 三、触发场景

| 用户说的话                           | 执行                            |
|------------------------------------|-------------------------------|
| 发来截图                            | 多模态识别 + 标签归档             |
| 发来截图附带"粗心"                   | 识别后直接归档，不追问            |
| "Verbal-Text Completion-词汇量不足" | 快捷格式，直接归档               |
| "记得" / "不记得"                   | 二刷自评，连续2次记得→已掌握      |
| "导出错题本"                        | 导出全部                        |
| "只导出待二刷的"                     | 筛选导出                        |
| "导出Verbal的错题"                  | 按 section 筛选                 |
| "导出最近两周的"                     | 按时间筛选                      |
| "换考试"                            | 重新配置考试类型                 |

---

## 四、数据结构

```
~/.openclaw/skills/shiyi/data/
├── config.json              ← 当前考试配置
├── tag_library.json         ← 各考试的标签词库
├── wrong_questions.json     ← 所有错题
├── review_state.json        ← 二刷状态
├── review_session.json      ← 当前二刷进度
├── stats_cache.json         ← 打卡连续天数
├── daily/                   ← 每日记录
├── backups/                 ← wrong_questions 自动备份（最近10个）
└── exports/                 ← 导出文件
```

错题记录字段：

```json
{
  "id": "uuid",
  "date": "2026-03-19",
  "exam": "GRE",
  "exam_name": "GRE",
  "section": "Verbal",
  "question_type": "Text Completion",
  "knowledge_point": "逻辑关系词 — 转折",
  "question_text": "完整题目文字",
  "visual_description": null,
  "answer": "B",
  "error_reason": "知识点不会",
  "keywords": ["逻辑关系词", "Text Completion"],
  "status": "待二刷"
}
```

---

## 五、核心流程

### 图片识别

1. 读取 `config.json` 里的 `exam_key`，加载对应的考试背景知识
2. 从 `tag_library.json` 取最近30天用过的标签注入 prompt（提升复用率）
3. 调用 OpenClaw 配置的多模态模型识别
4. 识别结果写入 `wrong_questions.json`，新标签追加进 `tag_library.json`
5. 调用失败 → 提示手动复制文字

### 标签词库（tag_library）

- 每次识别后自动追加新标签（去重）
- 同一考试内复用，不同考试互不干扰
- 每类最多保留：知识点200个、题型50个（超出删最旧的）
- 注入 prompt 时只传最近30天用过的（避免 prompt 过长）

### 定时推送

| 时间 | 内容 |
|------|------|
| 每天 21:00 | 当日错题汇总 + 高频考点 + 打卡天数 |
| 隔天 20:00 | 随机抽3道待二刷题，用户自评 |

---

## 六、文件索引

| 文件 | 作用 |
|------|------|
| `assets/exam_prompts.js` | 各考试背景知识（识别精度的核心） |
| `scripts/tag_library.js` | 标签词库读写与统计 |
| `scripts/onboarding.js`  | 首次配置考试类型 |
| `scripts/parse_input.js` | 消息路由 + 识别入口 |
| `scripts/update_daily.js` | 写入错题和每日记录 |
| `scripts/export_xlsx.js` | 导出 Excel（含筛选和截图嵌入） |
| `scripts/review_reminder.js` | 二刷提醒和自评处理 |
| `scripts/daily_summary.js` | 每日定时总结 |

---

## 七、新增考试

在 `assets/exam_prompts.js` 的 `EXAM_PROMPTS` 对象里加一条字符串：

```javascript
'驾照科目一': `
驾照科目一为交规理论考试，100道题，90分及格。
题型：判断题、单选题。
标 knowledge_point 时请具体到交规条款（如"禁止标志与警告标志区别"）。`,
```

PR 欢迎。

---

## 八、如果这个 Skill 对你有帮助

⭐ Star 一下，让更多备考的人找到它
🍴 Fork 加上你的考试类型，欢迎 PR

> https://github.com/KaguraNanaga/shiyi
