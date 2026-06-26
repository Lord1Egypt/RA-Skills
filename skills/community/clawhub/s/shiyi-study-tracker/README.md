<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/KaguraNanaga/shiyi/main/assets/crane_shiyi.png">
    <img src="https://raw.githubusercontent.com/KaguraNanaga/shiyi/main/assets/crane_shiyi.png" alt="拾遗" width="160">
  </picture>
</p>

<h1 align="center">拾遗 · shiyi</h1>

<p align="center">
  通用考试备考追踪 OpenClaw Skill<br>
  任何考试——GRE、雅思、考研、注会、高考、期末——发截图或文字，自动归档错题、积累标签、二刷提醒。
</p>

<p align="center">
  <a href="https://openclaw.ai">
    <img src="https://img.shields.io/badge/OpenClaw-Skill-orange?style=for-the-badge" alt="OpenClaw Skill">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License">
  </a>
  <a href="https://nodejs.org">
    <img src="https://img.shields.io/badge/node-%3E%3D18-green?style=for-the-badge" alt="Node ≥18">
  </a>
</p>

---

## 和朱批录的关系

[朱批录](https://github.com/KaguraNanaga/kaogong-study-tracker) 是专门为考公设计的，科目固定（言语/数量/判断/资料/申论），识别逻辑针对行测优化。

拾遗是通用版，核心差异是**自由标签**——不预设科目结构，AI 根据你的考试类型自动决定标签粒度：

- GRE 标到"Text Completion 双空逻辑"
- 雅思标到"T/F/NG 绝对词识别"
- 考研数学标到"换元积分法"
- 期末考标到你的课程和章节

同一考试内的标签会积累复用，不同考试互不干扰。

---

## 它能做什么

| 你做什么 | 拾遗做什么 |
|---------|----------|
| 告诉它你在备考什么 | 加载对应考试的识别背景知识 |
| 发一张错题截图 | 自动识别题型、知识点、错误原因，归档 |
| 发"Verbal-Text Completion-词汇量不足" | 快捷录入，直接归档 |
| 说"导出GRE的错题" | 生成 Excel，按考试筛选 |
| 回复"记得"或"不记得" | 二刷自评，连续2次记得自动标为已掌握 |
| 什么都不说 | 每天21:00总结，隔天20:00二刷提醒 |

---

## 已预置的考试类型

| 类别 | 考试 |
|------|------|
| 标化英语 | GRE、GMAT、TOEFL、雅思、四六级 |
| 考研 | 考研英语、考研数学、考研政治、专业课 |
| 职业资格 | 注会、司法考试、教师资格证 |
| 公务员 | 国考、省考 |
| 学校考试 | 高考、期末考试 |

不在列表里的考试用通用模式，AI 自行判断标签。

---

## 快速安装

```bash
cd ~/.openclaw/skills
git clone https://github.com/KaguraNanaga/shiyi

cd shiyi
npm install
```

在 `workspace.yaml` 里启用：

```yaml
skills:
  - shiyi

cron_jobs:
  - name: "每日总结"
    schedule: "0 21 * * *"
    action:
      type: run_script
      script: skills/shiyi/scripts/daily_summary.js
      channel: feishu

  - name: "二刷提醒"
    schedule: "0 20 1-31/2 * *"
    action:
      type: run_script
      script: skills/shiyi/scripts/review_reminder.js
      channel: feishu
```

安装后发任意消息，拾遗会问你备考什么考试，一句话配置完成。

---

## 数据结构

```
~/.openclaw/skills/shiyi/data/
├── config.json          ← 当前考试（exam_key + exam_name）
├── tag_library.json     ← 各考试标签词库（自动积累，不需要维护）
├── wrong_questions.json ← 所有错题
├── daily/               ← 每日记录
├── backups/             ← 自动备份（最近10个）
└── exports/             ← 导出文件
```

---

## 文件结构

```
shiyi/
├── SKILL.md
├── package.json
├── assets/
│   └── exam_prompts.js        ← 各考试背景知识（新增考试在这里加）
└── scripts/
    ├── onboarding.js          ← 首次配置考试类型
    ├── parse_input.js         ← 消息路由 + 识别入口
    ├── tag_library.js         ← 标签词库读写
    ├── update_daily.js        ← 写入错题和每日记录
    ├── export_xlsx.js         ← 导出 Excel
    ├── review_reminder.js     ← 二刷提醒
    └── daily_summary.js       ← 每日总结
```

---

## 新增考试

在 `assets/exam_prompts.js` 里加一条：

```javascript
'驾照科目一': `
驾照科目一为交规理论考试，100道题，90分及格。
题型：判断题、单选题。
标 knowledge_point 时请具体到交规条款。`,
```

同时在 `EXAM_ALIASES` 里加别名映射，PR 欢迎。

---

## 如果这个项目对你有帮助

⭐ **Star 一下**，让更多备考的人找到它
🍴 **Fork**，加上你的考试类型，欢迎 PR

---

## License

MIT © 2026
