---
name: skill-evolver
description: Use this skill when evolving skills and extracting patterns from execution data. Provides automatic feedback collection, AI suggestion generation, impact tracking, and A/B testing framework for continuous skill improvement.
origin: meta-skill
version: 0.3.0
tags: ["evolution", "learning", "pattern-extraction", "infrastructure", "meta-skill"]
tools: ["Read", "Write", "Bash", "Exec"]
model: sonnet
---

# skill-evolver - 技能进化器

**版本**：v0.3.0  
**定位**：L3 进化层 - Instinct→Skill 自动进化引擎

---

## 📖 技能说明

skill-evolver 是一个技能自动进化引擎，能够：
1. **收集反馈** - 从技能执行中收集使用数据和评分
2. **分析模式** - 识别高效模式和待改进点
3. **生成改进** - 自动生成技能优化建议
4. **执行进化** - 将成熟的 Instinct 转化为技能
5. **验证效果** - A/B 测试验证进化效果

**核心价值**：
- 让技能系统能够自我进化
- 减少人工维护成本
- 持续优化技能质量

---

## 🎯 使用场景

| 场景 | 示例 |
|------|------|
| **技能优化** | 「分析 first-principle-analyzer 的使用数据，生成优化建议」 |
| **Instinct 进化** | 「将成熟的 instinct-ecc-001 进化为技能」 |
| **效果验证** | 「对比 skill-evolver v0.1.0 和 v0.3.0 的效果」 |
| **反馈收集** | 「收集过去 7 天的技能使用反馈」 |
| **A/B 测试** | 「为技能创建 A/B 测试方案」 |
| **模式提取** | 「从历史会话中提取可复用模式」 |
| **置信度评估** | 「评估这个 Instinct 的置信度」 |

---

## 💰 定价方案

| 版本 | 价格 | 功能 | 适用对象 |
|------|------|------|----------|
| **个人版** | ¥199/年 | 基础反馈收集、10 次提取/月、基础分析 | 个人开发者、学生 |
| **商业版** | ¥1999/年 | 个人版 + AI 建议生成、100 次提取/月、效果追踪、A/B 测试 | 小型团队、创业公司 |
| **企业版** | ¥19999/年 | 商业版 + 无限提取、私有部署、定制模型、专属支持、SLA 保障 | 中大型企业、知识密集型团队 |

---

## ❓ FAQ（常见问题）

**Q1: skill-evolver 如何收集反馈？**
A: 通过 Hook 系统自动捕获技能执行数据，包括输入、输出、执行时间、用户反馈（确认/反对）等。支持手动导入历史数据。

**Q2: 置信度如何计算？**
A: 置信度 = 基础置信度（基于观测次数）+ 用户反馈调整 + 时间衰减。观测≥10 次且反馈正面可达 0.85+。

**Q3: 支持多少技能的进化？**
A: 个人版 10 个技能，商业版 100 个技能，企业版无限。支持技能批量导入和导出。

**Q4: A/B 测试如何工作？**
A: 自动创建实验组和对照组，分配流量，统计显著性计算（t 检验、p 值、效应量），自动生成推荐报告。

**Q5: 如何保护技能知识产权？**
A: 所有提取的 Instinct 和技能本地加密存储，支持敏感信息自动识别和脱敏。企业版支持私有部署和数据访问审计。

---

## 📖 完整 README（上架版本）

[完整的 README 内容，包含功能说明、技术架构、实战案例、安装指南、API 参考、贡献指南、技术支持等]

---

**文件版本**：v0.3.0  
**创建时间**：2026-04-01  
**上架时间**：2026-04-01  
**上架用户**：pagoda111king
