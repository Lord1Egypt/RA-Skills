# 小红书运营知识库

把每次分析、选题、发布、回复、复盘中有效的信息沉淀下来，让下一次决策能更快。

**三个核心问题：**
1. 这类内容之前怎么做的？
2. 哪些动作有效、哪些失败？
3. 下一次直接复用什么？

---

## 目录结构

| 目录 | 存什么 |
|------|--------|
| `accounts/` | 账号定位、诊断结论、竞品拆解 |
| `topics/` | 选题候选、争议点、标题骨架 |
| `patterns/` | 爆款结构、封面层级、互动机制、可复用模式 |
| `actions/` | 发布、回复、抓取等操作记录 |
| `reviews/` | 复盘结论、失败原因、下次修正 |

**文件命名规则：** `YYYY-MM-DD-brief.md`（日期前置，按时间排序，brief 保留账号/主题/动作词）

---

## 检索方法

1. 先看本文件"当前重点"和"固定索引"
2. 找最近 7-14 天的同类记录（按日期名排序）
3. 找同账号/同主题记录
4. 找同结构 pattern
5. 最后看历史失败记录

---

## 记录字段约定（精简版）

每条记录的 frontmatter 至少包含：

```yaml
---
id: YYYY-MM-DD-brief
type: account | topic | pattern | action | review
status: active | deprecated | experimental
created_at: YYYY-MM-DDThh:mm:00+08:00
source_url: ""   # 可选
account: ""      # 可选，相关账号
tags: []
summary: "一句话结论"
next_action: "下一次怎么用"
---
```

---

## 当前重点

- **账号定位**：AI 产品经理个人号，记录踩坑和想清楚的事
- **内容支柱**：AI Agent 实践 / AI PM 工作日常 / AI 工具使用心得
- **当前选题**：见 `topics/2026-03-20-xhs-topic-candidates.md`
- **下一步**：XHS-1（8万人调研）本周发，XHS-4（Claude 用法分层）随时可发

---

## 固定索引

> （空）——积累后把高价值 pattern 链接到这里，方便快速取用

---

## 待整理

> （空）——任务中临时结论先挂这里，任务后补写到对应子目录
