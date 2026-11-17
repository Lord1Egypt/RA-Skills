---
name: workbuddy-health-check
title: "WorkBuddy环境安全体检"
displayName: "WorkBuddy环境安全体检"
description: 一条命令给 WorkBuddy 环境做八维安全稳定体检：磁盘/备份新鲜度/自动化存活/凭据硬编码/备份包完整性/配置/记忆/同步载体，输出体检报告+分级处置清单。适用"WorkBuddy 安不安全/稳不稳定/体检一下/备份还好吗/凭据有没有泄露"等场景。
description_en: One command, 8-dimension health check for your WorkBuddy environment — disk, backup freshness, automation health, hardcoded credential scan, backup package integrity, config audit, memory sync and cross-machine carrier. Outputs a report with prioritized action items. Zero network, read-only, fully local.
version: 1.0.0
category: 开发工具
platforms: ["workbuddy"]
author: 注册老炮
license: MIT
tags: ["workbuddy", "运维", "体检", "安全", "health-check", "备份", "凭据扫描"]
---

# WorkBuddy 环境安全体检

> 一句话体检 WorkBuddy 环境是否安全稳定运行：磁盘够不够、备份新不新、自动化活没活、凭据有没有硬编码泄露、备份包干不干净。

**English**: One command to health-check your WorkBuddy environment — 8 dimensions, zero network, read-only, fully local, with a prioritized action report.

**日本語**: WorkBuddy 環境の安全・安定運行を 8 次元で一括検診。ローカル完結・読み取り専用・要ネットワークなし。

## 全景图

```
        ┌─────────────────────────────────────────────┐
        │  workbuddy-health-check（环境体检总入口）      │
        │  一条命令：python scripts/wb_health_check.py │
        └──────────────────┬──────────────────────────┘
                           │ 只读 + 报告（不删不改）
   ┌───────┬───────┬───────┼───────┬───────┬───────┬───────┬───────┐
   H1      H2      H3      H4      H5      H6      H7      H8
 磁盘健康 备份新鲜 自动化  凭据硬  备份包  配置    记忆    跨机
          度      存活    编码    完整性  审计    同步    载体
   │       │       │       │       │       │       │       │
   ▼       ▼       ▼       ▼       ▼       ▼       ▼       ▼
  处置建议 P0/P1/P2 分级清单（危急→建议→长效）
```

## 触发场景

- 用户说"WorkBuddy 体检 / 安不安全 / 稳不稳定 / 维护一下 / 数据还好吗"。
- 跨机同步、恢复、收工前——先跑一遍，确认无 P0。
- 关键词：体检 / 安全稳定 / 备份 / 凭据泄露 / 备份包 / 自动化存活 / 磁盘。

## 使用流程（3 步）

```bash
# ① 跑体检（--quick 跳过备份包全量哈希校验，快）
python scripts/wb_health_check.py --quick

# ② 看报告
#    ~/.workbuddy/health-check/wb_health_<时间戳>.md （体检表+处置清单）
#    ~/.workbuddy/health-check/wb_health_<时间戳>.json （机器可读，供自动化门禁）

# ③ 处置：按 P0 → P1 → P2 清单执行；敏感操作先人工确认
```

可选参数：

```bash
python scripts/wb_health_check.py --out D:/out          # 指定报告输出目录
python scripts/wb_health_check.py --golden-dir D:/bk1   # 追加备份包目录（可多次）
python scripts/wb_health_check.py --workspace-root D:/Workbuddy  # 指定工作区根（检测今日记忆日志）
python scripts/wb_health_check.py --json                # 打印 JSON 摘要
```

退出码：`0` 全通过 / `1` 有 WARN / `2` 有 CRIT——可挂自动化做门禁。

## 八维体检表

| 维度 | 体检什么 | 阈值 | 危急时的处置 |
|------|----------|------|--------------|
| H1 磁盘健康 | 系统盘/数据盘剩余 | 已用 >75% WARN / >90% CRIT | 清日志/缓存/临时包，目标 <75% |
| H2 备份新鲜度 | 最新备份包（wb_golden_*.zip）龄 | >7d WARN / >14d CRIT / 无包 CRIT | 重跑备份打包，上传到异地备份位置 |
| H3 自动化存活 | ACTIVE 数 / 疑似卡死 / last_error | 非 ACTIVE 或卡死即告警 | 查运行时状态，停摆的按需启用 |
| H4 凭据硬编码 | 对外文本层 secret 扫描 | 高置信格式命中即 CRIT | 真凭据→移入系统凭证库并清除明文；示例→忽略 |
| H5 备份包完整性 | 包内 `_` 元数据/凭据目录/manifest 哈希 | 任一命中 CRIT | 重新打包（剔除安装元数据与凭据目录）并复核 |
| H6 配置审计 | 技能/连接器/专家/MCP 数 | 技能>150 提示冗余 | 「前提验证+配置审计」三棱镜盘点 |
| H7 记忆同步 | MEMORY.md 龄 + 今日工作区日志 | 今日无日志 WARN | 收工前补今日工作日志 |
| H8 跨机载体 | 自动化配置备份最新龄 | >7d WARN | 检查备份包是否含自动化配置导出 |

## 脚本铁律（脚本内置）

1. 纯标准库、**零网络**、只读 + 只写报告，不删不改。
2. 命中 secret **一律脱敏**（前 4 后 4），绝不输出明文。
3. 凭据合法存放点（credentials/ connectors/ connector-keys/）不扫。
4. 报告不含主机名、任务明细等个人信息，只给指标与处置建议。

## 隐私与安全

- 全本地运行，不联网、不上传任何数据。
- 报告不含主机名、不含自动化任务明细、不含备份包路径（仅文件名）。
- 命中的凭据一律脱敏展示，需人工判断真伪后再处置。

## 版权与许可

- **© 2026 注册老炮**。本作品基于 MIT License 开源。
- **知识版权声明**：本技能中的方法、结构与脚本为原创合成知识，归作者所有；禁止未经授权的复制、转售或用于模型训练。
- **免责声明**：本技能按「现状」(AS IS) 提供，作者不对使用本技能产生的任何直接或间接损失承担责任；请在使用前自行验证与备份数据。
- 发布版本随附时间戳与文件指纹（见 ATTESTATION.md / manifest.json），任何篡改都会导致指纹不一致。

## 验证清单

- `python scripts/wb_health_check.py --quick` → 出报告 + 退出码 0/1/2，无异常栈。
- 报告内 secret 命中值全部打码（无明文）。
- 首次跑完把报告过目，P0/P1 逐项确认处置。

## 输出位置

- 报告：`~/.workbuddy/health-check/wb_health_<时间戳>.md`（保留最近 10 份）
- JSON：同目录 `wb_health_<时间戳>.json`（自动化门禁用）
