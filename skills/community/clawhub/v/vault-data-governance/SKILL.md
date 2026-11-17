---
name: vault-data-governance
description: "Vault 数据治理规范：对所有智能体/团队的采集、审核、研究成果执行每日审计、清理、去重、归档。"
version: 1.0.0
author: Michael + Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [data-cleaning, archive, dedup, governance, audit, all-agents]
    related_skills: [teamwork, vault-research-workflow]
---

# Vault 数据治理规范（全智能体通用）

## 适用范围
- 所有智能体：`main`、`side_research`、`technical_team`、`export_team`、`aron`、`vicky`、`marcy`、`lynn`、`research_lead`、`whois_agent`、`company_agent`、`quality_inspection`
- 所有采集目录：`by-country/`、`算电/`、`专项研究/`、`日审/`
- 所有任务目录：`.agent-coordination/tasks/`
- 所有团队 workspace：`/root/.openclaw/workspace_teams/*`

## 触发时机
- 每日 03:00 审计 cron 执行后
- 侧线日采集完成后
- 政策抓取完成后
- 手动审计/统计/优化时
- 任何 agent 完成一批采集后

## 核心规则

### 1. 审计即清理
每次审计/统计/优化时，**同步执行**：
- 采集信息中**过期、无效、证伪**的内容 → 立即汇报，移出活跃目录，归档到 `专项研究/归档/`
- **不得堆积垃圾数据**，审计报告必须包含清理动作

### 2. 去重常态化
- 按文件名去重：`find . -name '*.md' | sort | uniq -d`
- 按标题去重：提取每篇文件第一个 `# ` 标题，`sort | uniq -d`
- 保留规则：保留最新修改时间的版本，旧版归档
- 例外：同日多次抓取保留全部（标注版本号）

### 3. 错误/临时文件归档
- `*_错误日志.md`、`*_抓取日报.md`、`*_临时*.md` 等临时文件 → 归档，不留在生产目录
- 覆盖所有产品线、所有 team

### 4. 研究成果归档
- 完成的研究成果（概念设计、规模基准、技术方案）→ 移入对应产品目录 `归档/`
- 待确认项 → `待Michael人工确认/`
- 完成后 → `archive/`

## 执行流程

```
1. 扫描：find + grep 识别需清理文件
2. 备份：mv 到 archive/（不要 rm）
3. 去重：find + sort + uniq -d
4. 统计：记录清理数量
5. 提交：git add -A && git commit && git push
6. 报告：audit 文件记录清理动作
```

## 禁止行为
- ❌ 用 `rm` 删除，必须用 `mv` 归档
- ❌ 审计报告只列数据不执行清理
- ❌ 重复文件并存不清理
- ❌ 错误日志留在生产目录
- ❌ 研究成果不归档堆积在主目录

## 输出格式
```
清理归档：
- 过期/无效文件：N 个 → 专项研究/归档/YYYY-MM-DD/
- 重复文件：N 个（保留最新，旧版归档）
- 去重后有效文件：N 个
- 研究成果归档：N 个
```

## 所有智能体职责
| 智能体 | 采集/审核范围 | 清理职责 |
|---|---|---|
| main | 全局 orchestrator | 确保 cron/脚本包含清理步骤 |
| side_research | 侧线日采集 | 每日去重 + 过期文件归档 |
| technical_team | 技术研究/报告 | 研究成果归档 + 旧版本清理 |
| export_team | 认证/展会/客户 | 过期展会信息/客户跟进表清理 |
| aron/vicky/marcy/lynn | 外销团队 | 各子领域定期清理 |
| research_lead | 研究方向 | 过期研究主题归档 |
| whois_agent/company_agent | 企业/竞品 | 过期企业信息清理 |
| quality_inspection | 质量审核 | 不合格成果移出生产目录 |
