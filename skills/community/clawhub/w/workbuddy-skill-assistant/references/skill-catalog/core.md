---
catalog_version: 0.1.0-draft
scope: core
title: 通用核心清单 · 人人必备的底座积木（~10 个）
last_synced: 2026-08-27
note: >
  通用核心底座，与用户画像/岗位无关，所有用户先装这一层。
  类型字段：skill=用户技能 / mcp=连接器能力 / guide=引导动作（非技能）。
  本清单不分档、不评分——核心必装，无需排序。
---

# 通用核心清单（底座积木 · 人人必备）

> 使用指引：这是「底座积木」。无论画像如何，先铺这 ~10 块，再按画像倾斜叠加主题积木。
> 一个 skill 只出现在一处（核心或某个主题），避免跨清单重复维护。

- name: 腾讯文档
  slug: tencent-docs
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 在线云文档创建/编辑/推送，文档协作分发中枢
  install_cmd: "skillhub install tencent-docs --dir ~/.workbuddy/skills"
  risk: 低

- name: 文档生成管线
  slug: Work_document_pipeline
  type: skill
  source: installed
  version: "1.0.0"
  purpose: Markdown/TXT/数据 → HTML/PDF/EPUB/DOCX/PPT/Kindle 端到端路由
  install_cmd: "skillhub install Work_document_pipeline --dir ~/.workbuddy/skills"
  risk: 低

- name: 浏览器自动化（skill）
  slug: "@rez0/agent-browser"
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 浏览器自动化 CLI，导航/填表/点击/截图/抓取
  install_cmd: "skillhub install agent-browser --namespace @rez0 --dir ~/.workbuddy/skills"
  risk: 低

- name: 浏览器自动化（Playwright）
  slug: playwright
  type: mcp
  source: connector
  version: ""
  purpose: Playwright MCP，网页操作/表单/截图/网络抓取，与 agent-browser 互补
  install_cmd: "（连接器管理页启用 Playwright 即可）"
  risk: 低

- name: 记忆体系引导
  slug: memory-onboarding
  type: guide
  source: builtin
  version: ""
  purpose: 初始化 SOUL.md / USER.md / MEMORY.md，让 AI 认识你是谁、怎么聊
  install_cmd: "（初始化引导完成，非安装项）"
  risk: 无

- name: skill 管理三件套
  slug: skill-ecosystem-trio
  type: guide
  source: installed
  version: "1.0.0"
  purpose: skill-map（全景）+ skill-check（体检）+ skill-auto-upgrade（升级）连贯自管理流，由 skill 生态三件套编排统一处理
  install_cmd: "（三件套编排，逐个确认安装，非本清单直接装）"
  risk: 低

- name: 智能体邮箱
  slug: agent-mail
  type: mcp
  source: connector
  version: ""
  purpose: 邮件收发/附件/搜索，报告推送与外部通信
  install_cmd: "（连接器管理页启用 agent-mail 并授权）"
  risk: 低

- name: 企业微信统一套件
  slug: wecom-unified
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 通讯录/文档/表格/日程/会议/待办/邮件，团队协作与通知
  install_cmd: "skillhub install wecom-unified --dir ~/.workbuddy/skills"
  risk: 中

- name: 腾讯 ima 知识库
  slug: ima-skills
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 笔记管理 + 知识库操作，资料沉淀与检索
  install_cmd: "skillhub install ima-skills --dir ~/.workbuddy/skills"
  risk: 低

- name: 个人每日工作台
  slug: working-bench__skillhub
  type: skill
  source: installed
  version: "1.0.0"
  purpose: 每日计划/打卡/记账/长期目标/灵感，纯前端零依赖
  install_cmd: "skillhub install personal-workbench --dir ~/.workbuddy/skills"
  risk: 低
