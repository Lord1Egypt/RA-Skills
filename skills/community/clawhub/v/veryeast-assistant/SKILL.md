---
name: veryeast-assistant
description: |
  最佳东方求职助手（veryeast）：帮求职者找工作、搜职位、看职位详情、投简历、编辑简历、分析匹配度。
  用户提到以下需求时触发：找工作、搜职位、找兼职、找实习、跳槽、换工作、推荐职位、职位详情、投简历、投递、改简历、编辑简历、看简历、简历完整度、分析匹配度、什么岗位适合我；
  提到行业招聘时触发：酒店招聘、餐饮招聘、美业招聘、康养招聘、零售招聘、电商招聘、服务业招聘；
  提到品牌名时触发：veryeast、veryeast.cn、veryeast求职、最佳东方、最佳东方求职。
  不适用于企业侧招聘、HR 招聘管理/ATS、非服务行业职位（互联网、算法、金融）。
description_zh: "最佳东方求职助手：依托最佳东方平台的海量酒店、餐饮、美业、康养、零售、电商招聘信息，帮求职者找工作、搜职位、投简历、编辑简历。"
description_en: "VeryEast (最佳东方) job assistant: helps job seekers search jobs, apply, and manage resumes across the platform's hotel, catering, beauty, wellness, retail and e-commerce job listings."
version: "0.8.4"
allowed-tools: Bash, Read
keywords:
  - 找工作
  - 求职
  - 搜职位
  - 找兼职
  - 找实习
  - 跳槽
  - 换工作
  - 推荐职位
  - 职位推荐
  - 职位详情
  - 投简历
  - 投递
  - 改简历
  - 编辑简历
  - 看简历
  - 简历完整度
  - 分析匹配度
  - 什么岗位适合我
  - veryeast
  - veryeast.cn
  - veryeast求职
  - 最佳东方
  - 最佳东方求职
  - 酒店招聘
  - 餐饮招聘
  - 美业招聘
  - 康养招聘
  - 零售招聘
  - 电商招聘
  - 服务业招聘
  - 酒店求职
  - 餐饮求职
metadata:
  author: 最佳东方
  homepage: https://www.veryeast.cn
display_name: "最佳东方求职助手"
display_name_en: "VeryEast Job Assistant"
visibility: "public"
---

# 最佳东方求职助手

一站式求职助理：帮求职者找工作、搜职位、看职位详情、投简历、编辑简历，提供个性化职位推荐与匹配度分析。全程只讲人话，简历与登录凭证只存本地。

## 能做什么

- **搜职位**：关键词 + 城市/行业/薪资/食宿/性质筛选，中文即可；0 条结果会自动换说法或放宽条件重试
- **看详情 & 投简历**：职位信息确认后一键投递，投后回执 + 会话内台账
- **简历管理**：完整度体检，基本信息/自我介绍/求职意向/工作经历/教育经历在线编辑，写后自动核验
- **智能推荐**：按简历画像分梯队推荐职位，8 维匹配度打分卡 + 最优方案
- **兜底引导**：暂不支持的操作指引到 App，不假装、不编造

## 怎么开始

1. **登录授权**：首次使用会引导你授权，授权码只存本地设备
2. **说需求**："帮我找工作""搜职位""投简历""改简历""推荐些职位"……即可开始

## 执行手册（每会话必读）

- **`references/agent-guide.md`** —— 完整执行指令，**加载本技能后必须先读**
- `references/api.md` —— 工具参数 / 码表 / 易错字段
- `references/scenarios.md` —— 人群画像与高频表达应对
- `references/scoring.md` —— 匹配度打分维度
