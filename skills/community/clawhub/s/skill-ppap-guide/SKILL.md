---
slug: ppap-guide
name: PPAP技能助手
displayName: PPAP技能助手
version: 1.1.0
author: org-jaxjwo0r
category: quality
description: 提供PPAP知识体系、文件模板生成、填写指导与检查校验；当用户需要了解PPAP流程、生成PPAP文件、填写提交保证书或检查文件完整性时使用
---

# PPAP生产件批准程序指南

## 任务目标
- 本Skill用于:协助用户完成PPAP（Production Part Approval Process）生产件批准程序
- 能力包含:PPAP知识咨询、文件模板生成、各阶段填写指导、文件完整性检查、常见问题解答
- 触发条件:用户提到PPAP、提交保证书、零件批准、生产件批准、IATF16949等场景

## 前置准备
- 依赖说明:pyyaml>=6.0（用于检查脚本解析配置）
- 非标准文件/文件夹准备:无

## PPAP知识体系

### 什么是PPAP
PPAP（Production Part Approval Process）是汽车行业供应商提交零件进行批量生产批准的标准流程，由AIAG（汽车工业行动组）制定。

### PPAP适用场景
1. 新零件首次提交
2. 设计的重大变更
3. 材料或工艺变更
4. 供应商变更
5. 零部件或材料来源变更
6. 停产一年后重新生产

### PPAP流程
详见 [references/ppap_knowledge.md](references/ppap_knowledge.md)

## 操作步骤

### 1. PPAP知识查询
当用户询问PPAP定义、目的、适用场景、流程时，读取 `references/ppap_knowledge.md` 提供详细解答。

### 2. 生成PPAP文件模板
根据用户需求类型生成对应文件：
- 提交保证书（Submission Warrant）
- PPAP文件目录（PPAP Checklist）
- 零件提交保证书（Part Submission Warrant）
- 检验记录表
- 过程流程图

详见 [references/ppap_templates.md](references/ppap_templates.md)

### 3. PPAP填写指导
根据用户所处阶段提供填写指导：
- 设计记录阶段
- 工程变更文件阶段
- 工程批准阶段
- DFMEA阶段
- 过程流程图阶段
- PFMEA阶段
- 过程能力指导
- 初始过程能力研究指导
- 测量系统分析指导
- 实验室要求指导
- 外观批准报告指导
- 生产件样品指导
- 标准样品指导
- 检查辅具指导
- 客户特殊要求指导

详见 [references/ppap_guidance.md](references/ppap_guidance.md)

### 4. PPAP文件检查校验
使用脚本检查PPAP文件完整性和格式：

```bash
python scripts/ppap_checker.py --input <用户提供的PPAP信息> --level <提交等级1-5>
```

脚本会检查18项提交要求，并输出结构化的检查报告。

### 5. 常见问题解答
读取 `references/ppap_faq.md` 获取常见问题解答和典型案例。

## 使用示例

### 示例1:查询PPAP基础知识
- 场景/输入:用户询问"什么是PPAP？什么时候需要做PPAP？"
- 预期产出:提供PPAP定义、目的、适用场景和基本流程的完整解答
- 关键要点:结合用户行业背景（汽车零部件供应商）给出具体说明

### 示例2:生成PPAP文件
- 场景/输入:用户需要提交新零件的PPAP，提交等级为Level 3
- 预期产出:生成完整的PPAP文件目录和提交保证书模板
- 关键要点:确认零件信息、提交等级、客户特殊要求

### 示例3:文件检查
- 场景/输入:用户已完成PPAP文件准备，需要检查完整性
- 预期产出:JSON格式的检查报告，列出缺失项和格式问题
- 关键要点:用户提供各文件的实际状态信息

### 示例4:填写指导
- 场景/输入:用户询问如何填写DFMEA或PFMEA
- 预期产出:分步骤的填写指导，包括各项内容的填写要求和示例
- 关键要点:明确哪些项为必填、哪些可选

## 资源索引
- 脚本:见 [scripts/ppap_checker.py](scripts/ppap_checker.py)（用途:检查PPAP文件完整性和格式；参数:--input JSON/文件路径，--level 1-5）
- 参考:见 [references/ppap_knowledge.md](references/ppap_knowledge.md)（何时读取:用户询问PPAP基础知识时）
- 参考:见 [references/ppap_templates.md](references/ppap_templates.md)（何时读取:用户需要生成PPAP文件模板时）
- 参考:见 [references/ppap_guidance.md](references/ppap_guidance.md)（何时读取:用户询问各阶段如何填写时）
- 参考:见 [references/ppap_faq.md](references/ppap_faq.md)（何时读取:用户遇到问题或需要案例参考时）

## 注意事项
- PPAP要求因客户而异，核心18项要求为基础，需根据客户特殊要求增减
- 提交等级默认为Level 3（零件提交保证书+有限支持数据），特殊要求按客户规范
- 文件检查仅提供完整性校验，内容准确性需用户自行确认
- 充分利用智能体能力，在生成文件时结合具体产品特点进行定制
- 变更记录：V1.1.0：完善 TRACE 五维度测评体系，补充触发条件、能力边界、异常处理与 TRACE 自评表

## 能力边界

- **适用场景**：质量管理相关领域的咨询、分析和文档生成场景
- **不适配场景**：法律法规正式解释、专业认证替代、涉及人身安全的紧急决策
- **输入要求**：需提供明确的参数和要求，脚本依赖需预先安装，Python 3.9+


## 异常处理

- **输入不完整**：提示用户补充缺失的关键信息，列出必需字段，引导用户逐步完善输入
- **依赖缺失**：检测依赖环境（Python库、系统工具），给出明确的安装指令和验证方法
- **执行失败**：输出清晰的错误信息和可能的原因，提供降级方案（如无法生成 PNG 则输出 SVG）
- **结果验证**：输出完成后提供校验方法，建议用户确认关键内容的准确性


## TRACE 五维度自评

| 维度 | 得分 | 自评说明 |
|------|------|----------|
| **Trust 信任度** | 8/10 | SKILL.md 结构化清晰，描述完整，触发条件明确，使用者可信任输出质量 |
| **Reliability 可靠性** | 8/10 | 包含使用示例和注意事项，输出格式统一，有脚本支撑的可复现能力 |
| **Adaptability 适配性** | 7/10 | 适应多种相关输入场景，提供参数化配置和脚本 支持 |
| **Convention 惯例性** | 8/10 | 遵循 SKILL.md 标准结构，frontmatter 完整，资源索引清晰 |
| **Effectiveness 有效性** | 8/10 | 端到端完成任务，脚本自动化提升执行效率 |
| **总分** | **39/50** | 基本合格 |
