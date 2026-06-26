# 销售助手数字员工

> 版本：2026-05-26  
> 部署建议：本地/云端部署，飞书入口“小销”，Hermes Agent 员工 ID：`sales_assistant`

## 1. 员工定位

通过飞书接收客户信息、拜访记录、聊天记录和需求材料，调用 Hermes Agent skills 完成商机卡、客户画像、拜访纪要、需求提炼、跟进建议、风险提示和客户归档。

## 2. 场景包与子角色

| 场景包 | 子角色/责任位 | 目标 | 关键 skills |
| --- | --- | --- | --- |
| 商机录入 | 商机助理 | 将零散客户信息整理为标准商机卡和跟进阶段。 | S01_opportunity_record, S07_customer_archive |
| 客户画像 | 客户研究员 | 分析客户背景、组织结构、决策链、预算、痛点和潜在需求。 | S02_customer_profile, S04_customer_need_extract |
| 拜访纪要 | 销售秘书 | 将拜访记录、聊天记录或录音转写整理成纪要。 | S03_visit_minutes, S04_customer_need_extract |
| 需求归纳 | 需求分析员 | 提炼显性需求、隐性需求、约束条件和待确认问题。 | S04_customer_need_extract, S05_followup_suggestion |
| 跟进建议 | 销售参谋 | 生成下一步动作、话术、资料准备和飞书提醒。 | S05_followup_suggestion, S08_sales_roleplay |
| 商务风险 | 风险提示员 | 识别付款、承诺、交付、竞品和关系风险。 | S06_business_risk_hint, S05_followup_suggestion |
| 客户归档 | 客户档案员 | 沉淀客户记录、项目阶段、关键联系人和下一步动作。 | S07_customer_archive, S01_opportunity_record |

## 3. 领域 skills

| Skill ID | 名称 | 用途 | 主要输出 |
| --- | --- | --- | --- |
| S01_opportunity_record | 商机信息整理 | 将客户线索、聊天记录和拜访信息整理为标准商机卡。 | opportunity_card, stage, missing_info |
| S02_customer_profile | 客户画像生成 | 生成客户背景、业务场景、决策链、预算判断和痛点分析。 | customer_profile, decision_chain, pain_points, budget_signal |
| S03_visit_minutes | 拜访纪要生成 | 从拜访记录、录音转写或聊天记录生成结构化纪要。 | visit_minutes, key_points, decisions |
| S04_customer_need_extract | 客户需求提炼 | 提取显性需求、隐性需求、约束条件、疑问和待确认事项。 | need_summary, constraints, open_questions |
| S05_followup_suggestion | 跟进动作建议 | 生成下一步跟进动作、话术、资料清单、责任人和提醒时间。 | next_actions, talk_tracks, material_list, reminders |
| S06_business_risk_hint | 商务风险提示 | 识别付款、交付、承诺、竞品、关系和合规风险。 | risk_items, risk_level, mitigation_suggestions |
| S07_customer_archive | 客户档案归档 | 生成 CRM 或客户台账更新草稿并归档过程记录。 | crm_update_draft, archive_record |
| S08_sales_roleplay | 销售话术陪练 | 围绕客户问题生成回应话术、追问问题和异议处理建议。 | reply_options, probing_questions, objection_handling |

## 4. 关键边界

- 可以生成草稿、建议、清单、摘要、风险提示和归档记录。
- 涉及报价口径、商务承诺、交付周期、客户敏感信息、对外发送材料时必须人工确认。
- 演示样例必须使用脱敏或虚拟数据，不使用真实客户、员工、财务、合同或技术敏感信息。
- 所有 Hermes Agent skill 调用需要记录输入、输出、确认人和归档位置。

## 5. 文件结构

```text
sales-assistant/
  README.md
  employee.yaml
  system_prompt.md
  workflows.md
  runbook.md
  skills/
  knowledge/
  templates/
  test_cases/
  demo/
```
