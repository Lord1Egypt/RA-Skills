---
name: report-generation
description: 初评报告的结构化生成——从分析和 eval 数据合成最终报告文档。输出 DOCX 格式。
aliases: [报告生成, 初评输出, docx生成]
---

# Report Generation — 初评报告生成

## Overview

所有分析完成后的最后一步——将各 skill 的输出汇总为一份结构化的初评报告。

报告不是分析的复制粘贴，而是**对分析的重新组织和提炼**——让读者用最少的时间抓住核心结论。

## When to Use

- 第一轮初评完成后
- 第二轮/第三轮/第四轮的最终输出
- 用户要求更新报告时（需结合 iteration-merge skill）

## The Process

### Step 1: 收集各 Skill 的输出

从本轮使用的各 skill 收集关键输出：
- 核心技术分析 → Claim 判断表（✅/🟡/❌）
- 团队评估 → 逐人匹配表 + 结构性缺口
- 供应链审计 → BOM 成本 + 供应风险清单
- 竞品发现 → 竞品对比表 + BP遗漏列表
- 各 skill 的 Verification 自检结果

### Step 2: 搭建报告结构

```
封面 → 概述页（第一页）→ 技术分析 → 团队评估 → 供应链分析
→ 竞争格局 → 综合评价 → 待验证问题清单（P0/P1/P2）
→ 下一轮建议 → 附录（含修改逻辑说明，如适用）
```

### Step 3: 写概述页（第一页）

概述页是报告最重要的部分——很多读者只翻这一页：

- 项目核心定位（一句话）
- Claim 判断表（4-6 行，每行 claim + 判断 + 一句话理由）
- 核心评级（综评 + 最关键的风险点一句）
- 关键发现：3-5 条，每行开头标注 正面/风险

### Step 4: 组装正文

每个章节包含：
1. 核心结论（一句话）
2. 支撑证据（引用 source：scholarclaw 检索、technology-news-search 结果、sn-deep-research 分析、web_search 核实等）
3. 不确定性说明（如果有信息缺口）
4. 对本轮决策的意义（如：这个结论是否影响推进优先级）

### Step 5: 运行质量门控

加载 skills/quality-gate/SKILL.md，检查 10 项清单是否全部通过。

### Step 6: 输出

使用 docx-js（JavaScript）或 python-docx 生成 DOCX 格式报告。文件命名规则：`Deeptechnic_<项目英文名>_<轮次>_<日期>.docx`

## Verification

- [ ] 概述页已完成（Claim 判断表 + 概要评级）
- [ ] 每个章节有可追溯的信源引用
- [ ] 所有待验证问题已按 P0/P1/P2 优先级排序
- [ ] 质量门控 10 项全部通过
- [ ] 报告文件已输出到 reports/ 目录
