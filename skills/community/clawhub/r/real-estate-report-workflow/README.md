# 房地产市场调查报告撰写工作流

> 面向 AI 助手的专业房地产市场调研报告撰写工作流框架

[![Version](https://img.shields.io/badge/version-v1.5-blue)](https://github.com/hoAr12/real-estate-report-flow)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## 这是什么

一套经过 3 个完整项目验证的房地产市场调查报告撰写方法论——不是模板，而是让 AI 助手能够按照专业咨询标准自动完成报告的**工作流**。

**覆盖物业类型**：住宅 / 商业 / 办公 / 工业（含 REITs 专项）

## 安装使用

### 方式一：OpenClaw Skill（推荐）

1. 下载 `real-estate-report-flow.skill`
2. 在 OpenClaw 中安装：
   ```bash
   openclaw skill install real-estate-report-flow.skill
   ```
3. 直接对话："帮我写一份深圳南山区写字楼市场调研报告"

### 方式二：手动集成

将 `SKILL.md` 和 `references/`、`scripts/` 目录复制到你的 AI 助手工作区。

## 工作流概览

```
Step 0 项目定义 ──→ Step 1 框架设计 ──→ Step 2 报告撰写
                                           │
Step 5 项目收尾 ←── Step 4 排版导出 ←── Step 3 质量审核
```

| Step | 名称 | 输出 |
|------|------|------|
| 0 | 项目定义 | 7 维度画像（类型/体量/阶段/日期/场景/立场/读者） |
| 1 | 框架设计 | 6 章 × N 个三级标题 + 字数/数据规划 |
| 2 | 报告撰写 | 正文 ~4-5 万字，含表格、来源标注 |
| 3 | 质量审核 | L1 自动化 + L2 逻辑 + L3 外部抽检 |
| 4 | 排版导出 | 专业 Word 文档（.docx） |
| 5 | 项目收尾 | 交付、复盘、归档 |

## 写作原则体系

```
全局 14 条（底线）  +  章节专项 56 条（增量）
     │                        │
     └──────── 冲突时专项优先 ─┘
```

## 验证数据

本工作流已通过 3 个完整项目实战验证（住宅/商务公寓/商业 REITs），报告体量 38,000~51,000 字，综合审核评分 87+。

## 环境依赖

- `web_search` / `web_fetch` — 联网搜索工具
- `python3` + `python-docx` — 文档处理
- `node` + `docx` (npm) — Word 导出

首次使用自动执行环境自检。

## 版本

v1.5.4 | 更新日期 2026-05-05

## 许可证

MIT License — 欢迎使用、修改、分发。如果能反馈使用体验或贡献改进就更好了 🐱
