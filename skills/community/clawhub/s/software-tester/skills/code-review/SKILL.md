---
name: code-review
description: 代码评审：缺陷/安全/性能/可读性聚焦，PR 复查清单与严重级判定
source:
  type: derived
  repo: skills-repo/software-tester
  path: skills/code-review/SKILL.md
  version: 1.0.0
  updated: 2026-08-24
  url: https://skills.sh/addyosmani/agent-skills/code-review-and-quality
metadata:
  category: 代码审查
  platform: 通用
  difficulty: 进阶
---

# 代码审查（Code Review）

> 对 diff / PR 做结构化评审：聚焦正确性、安全、性能、可读性与测试覆盖，输出带严重级的可执行意见。改编自社区高安装量技能 addyosmani/agent-skills@code-review-and-quality（30.9K），并参考 sanyuan0704/sanyuan-skills@code-review-expert（12.7K）、getsentry/skills@code-review（4.5K）等多作者实践。

## 能力

- **评审范围判断**：按变更类型（修复/新功能/重构/性能/安全）决定重点，不一把抓
- **多维度检查**：正确性（边界/并发/异常）、安全（注入/越权/密钥）、性能（N+1/锁）、可读性、测试覆盖
- **严重级判定**：Blocker / Major / Minor / Nit，区分「必须改」与「可选建议」
- **可执行意见**：文件:行定位 + 影响说明 + 具体改法，而非泛泛而谈
- **与测试正交**：发现缺测试时转对应 `references/*-testing.md` 补齐，不在此写测试

## 使用方式

```
/code-review 帮我 review 这个 PR
/code-review 看下这段改动的边界和并发问题
/code-review 上线前代码评审，按安全+正确性走一遍
```

## 工作流

1. `git diff main...HEAD` / `gh pr view` 取改动范围与上下文
2. 看变更类型 → 套用 [references/code-review-playbook.md](../../references/code-review-playbook.md) 的「评审范围决策树」定重点
3. 逐文件逐维度过「评审维度清单」，定位问题
4. 按严重级定处置（Blocker 必须改，Nit 不阻塞）
5. 输出带 文件:行 的意见模板，必要时转测试类 playbook 补覆盖

## 适用场景

- 收到 PR 需要评审意见，或提交前自检
- 上线前对关键改动做安全/正确性复查
- 把 AI 评审当第一道筛子，人做最终拍板

## 限制

- 不等于静态分析 / SAST；深度漏洞与架构债需配合工具与资深评审
- AI 评审缺业务上下文，最终结论由人拍板，勿直接 merge
- 完整方法论见整库 [references/code-review-playbook.md](../../references/code-review-playbook.md)
