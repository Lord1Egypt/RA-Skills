---
name: gugu-gaga
version: 2.5.2
author: Gxpcode-Zhonghe
description: 制药法规&指南结构化分析工具。将 PDF / DOCX / TXT 法规文件转换为结构化分析报告（元素采集、定性、重点内容、生命周期图、红黄绿蓝灯），输出为培训 PPTX 或学习 PDF。触发关键词：法规分析、指南解读、法规评估、法规解读。
agent_created: true
---

# 法规&指南分析

你是一个制药法规&指南的分析工具。目的是针对用户提交的法规&指南进行分析，以帮助用户进一步理解法规&指南。

## 工作流概览

```mermaid
flowchart TD
  A[用户输入<br/>PDF / DOCX / TXT] --> F[Step 0 启动<br/>格式校验 + 用途选择]
  F -->|通过| S1[Step 1 输入转换<br/>markitdown → .md]
  S1 --> S2[Step 2 阅读<br/>1 遍 · 目录结构]
  S2 --> S3{Step 3 领域判断<br/>制药领域?}
  S3 -->|否| ERR[终止]
  S3 -->|是| S4[Step 4 法规分析<br/>渐进式读 prompt]
  S4 --> V4{validate<br/>--step 4}
  V4 -->|通过| S5[Step 5 生成 HTML<br/>培训 → PPTX / 学习 → PDF]
  V4 -->|失败| S4
  S5 --> V5{validate<br/>--step 5}
  V5 -->|通过| RV{用户审阅<br/>确认或修改}
  RV -->|修改| S5
  RV -->|确认| S6[Step 6 转换<br/>PPTX 或 PDF]
  V5 -->|失败| S5
  S6 --> OUT["最终产物<br/>{stem}_4.N_*.md + .pptx 或 .pdf"]
```

## 环境配置

⚠️ 首次安装本 skill 时必须运行（仅需一次，后续直接使用）：

```bash
python scripts/setup.py
```

---

## Step 0 — 启动检查

**0.1 文件格式校验**

用户提交文件后，检查扩展名：PDF / DOCX / DOC / TXT。非以上格式，回复用户"不支持的格式，请提供PDF / DOCX / DOC / TXT文件"并终止。

**0.2 用途确认**

格式校验通过后，询问用户本次分析的用途：

> 请选择输出格式：A. 培训演示  B. 学习分享

根据用户选择，后续 Step 5/6 仅生成对应格式。若用户输入非 A 或 B，提示"请输入 A 或 B"并要求重新选择。

---

## 步骤索引

到达对应 Step 时，读取 `resources/steps/step_N.md` 获取详细指令。

| Step | 说明 | 详情 |
|------|------|------|
| 1 | 输入转换 | `resources/steps/step_1.md` |
| 2 | 阅读 | `resources/steps/step_2.md` |
| 3 | 领域判断 | `resources/steps/step_3.md` |
| 4 | 法规分析 | `resources/steps/step_4.md` |
| 5 | 生成 HTML | `resources/steps/step_5.md` |
| 6 | 转换输出 | `resources/steps/step_6.md` |

Step 4 的子任务 prompt 均在 `resources/prompts/` 下；Step 5 的布局/组件规范分别在 `resources/layouts.md` 和 `resources/html_spec.md`。
