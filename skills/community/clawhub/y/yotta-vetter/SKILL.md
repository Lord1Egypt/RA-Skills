---
name: yotta-vetter
slug: yotta-vetter
version: 0.2.9
displayName: 元审·技能安全审查
summary: 安装任何技能前的安全审查协议：来源、代码、权限、风险四阶段清单，联动深度扫描。
description: '元审 —— 安装任何技能前的安全审查协议：四阶段 checklist（来源→代码→权限→风险）+ 轻量 checker，与元安联动深度扫描。触发：安装/评估任何技能前、从市场或 GitHub 获取技能、审查他人分享的技能、任何「要装未知代码」的场景；或用户说 审查/审查技能/vetting/技能安全审查/检查技能 等。边界：checker 只做初审与报告，结论需人工确认；绝不代替最终决策。'
tags: [技能审查, 安全审查, 来源验证, 风险评级, vetting, security]
category: it-ops-security
license: MIT
homepage: https://github.com/YottaMeta/yotta-vetter
---
# 元审（yotta-vetter）

安装任何技能前的「安全审查协议」——四阶段 checklist + 轻量检查脚本，与元安（yotta-security-audit）联动：

- **check**：对技能目录做四阶段初审（来源/代码/权限/风险），输出 SKILL VETTING REPORT。
- **source**：GitHub 仓库来源半自动化检查（stars/更新时间/许可证），本地缓存，无网络自动降级。
- **联动元安**：初审发现 high 及以上风险时，输出一条命令引导跑 yotta-security-audit 深度扫描。

零依赖（Python 3.8+ 标准库），Windows + Linux 通用。危险模式规则与元安共用（scripts/vetter_rules.py 为同步副本，勿手改）。

## 何时使用

- 从技能市场、GitHub 或任何来源获取技能后、安装前；
- 评估他人分享的技能是否安全；
- 需要给「要不要装这个技能」一个结构化决策依据时。

**Do NOT trigger**：本工具只做审查与报告，不执行安装、修复或删除；最终结论必须由人类确认。

## 四阶段审查协议

| 阶段 | 检查点 | 对应命令/参考 |
|---|---|---|
| 1. 来源 | 来源平台、作者信誉、stars/更新时间、许可证 | source github:owner/repo；references/checklist.md |
| 2. 代码 | SKILL.md 完整性、脚本清单、危险模式规则扫描 | check <path> |
| 3. 权限 | 可执行位、全局可写、符号链接、需读取/写入/联网的范围 | check <path> |
| 4. 风险 | 风险等级判定 + 结论 + 决策记录 | 报告中的 结论/决策记录 段 |

## 快速使用

```bash
# 初审一个技能目录
python3 scripts/yotta_vetter.py check ./some-skill

# 输出 JSON + 生成报告文件
python3 scripts/yotta_vetter.py check ./some-skill --json --report report.md

# 只报告 high 及以上
python3 scripts/yotta_vetter.py check ./some-skill --severity high

# 来源半自动化检查（本地缓存，无网络自动降级）
python3 scripts/yotta_vetter.py source github:YottaMeta/yotta-memory
```

## 结论判定

| 风险等级 | 结论 | 动作 |
|---|---|---|
| critical | DO NOT INSTALL | 拒绝安装并人工复核 |
| high | INSTALL WITH CAUTION | 人工复核后决定 |
| medium | REVIEW REQUIRED | 复核后安装 |
| low/info | SAFE TO INSTALL | 仍建议按协议完整审查 |

exit code 与元安一致：0 = 干净/仅 low；1 = medium；2 = high；3 = critical；4 = 错误。

## 与元安的分工

- 元审 = 初审：快、轻，四阶段 checklist + 规则扫描 + 来源检查。
- 元安 = 深度扫描：13 类检测器 + 系统安全基线。
- 元审发现 high 及以上 → 输出命令引导跑元安深度扫描。

## 自扫说明

元审自身含来源检查功能（source 命令使用标准库 urllib 访问 GitHub API）。
用元审或元安自扫时会命中 urllib 网络调用提示（medium），属预期行为，非风险。

## 授权与法律红线

- 授权：仅审查已获授权、自有或教学用途的技能包，不扫描未授权目标。
- 法律红线：不用于绕过许可、破解或未授权访问；结论需人工复核，不替代法律意见。

## 参考文档

- references/checklist.md — 四阶段详细清单
- references/vetting-report-template.md — SKILL VETTING REPORT 模板
