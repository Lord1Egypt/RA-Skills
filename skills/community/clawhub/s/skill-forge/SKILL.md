---
name: skill-forge
version: 0.3.0
description: AI 技能自动发现、评估、集成、验证、宣传闭环系统 — 跨生态技能市场引擎
tags: [evolution, skills, automation, mcp, clawhub, x-twitter, sentiment]
---

# SkillForge — 技能自动进化引擎

SkillForge 让 AI agent 自主发现自己缺什么能力，跨生态搜索最佳工具，自动评估兼容性和安全性，一键集成为可用 skill，并自动发布进化成果。

## 核心能力

1. **多源发现** — 同时扫描 9+ 数据源（GitHub/HuggingFace/Reddit/X/ClawHub/OpenAI Skills/Claude Skills/Awesome Lists/Product Hunt）
2. **需求感知** — agent 声明能力缺口，Scout 优先定向搜索填补
3. **真实兼容性检测** — 实际探测本机 runtime（Node/Python/Rust/Go 版本、依赖可行性、平台限制）
4. **安全门控** — YARA 扫描 + 仓库健康检查 + 危险脚本检测
5. **ClawHub 标准输出** — 集成结果直接生成 `skill.json` + `SKILL.md`，可 `clawhub publish`
6. **自动分级** — auto/confirm/manual 三级
7. **舆情监测** — X/Twitter 实时搜索 AI agent 相关话题
8. **自动宣传** — pipeline 完成后自动生成并发布进化成果推文

## 快速开始

```bash
cd /Volumes/data/openclaw/evolution-engine

# 全流程（scout → evaluate → integrate → verify → benchmark → announce）
pnpm pipeline

# 单独运行
pnpm scout          # 情报采集
pnpm evaluate       # 价值评估
pnpm integrate      # 自动集成
pnpm verify         # 安全验证
pnpm announce       # 舆情+宣传
```

## 需求感知（Needs-Driven Scout）

编辑 `data/needs.json` 声明能力缺口：

```json
{
  "needs": [
    {
      "area": "视频处理",
      "description": "本地视频转码、剪辑的轻量 CLI",
      "keywords": ["video transcoding", "ffmpeg wrapper"],
      "priority": "medium"
    }
  ]
}
```

## 6 阶段 Pipeline

| 阶段 | 说明 |
|------|------|
| Scout | 9+ 源情报采集 + 需求驱动搜索 |
| Evaluate | 5 维度加权评估（含真实运行时检测） |
| Integrate | 自动克隆 + 安全扫描 + ClawHub skill 包生成 |
| Verify | 仓库健康 + 依赖安全 + 危险脚本检测 |
| Benchmark | 效能基准对比 |
| Announce | 舆情快照 + 进化成果推文发布 |

## 依赖 Skills

- `x-twitter` — X/Twitter 搜索、发帖、趋势（需 `TWITTER_BEARER_TOKEN`）
- `social-sentiment` — 跨平台舆情分析（需 Xpoz 账号）

## 数据源

| # | 源 | 方式 |
|---|---|------|
| 1 | GitHub Trending | API / SearXNG |
| 2 | HuggingFace | API / SearXNG |
| 3 | Reddit | SearXNG / RSS |
| 4 | Product Hunt | SearXNG |
| 5 | Awesome Lists | GitHub API |
| 6 | X/Twitter | SearXNG + Grok |
| 7 | ClawHub | API → HTML → CLI |
| 8 | OpenAI Skills | GitHub API |
| 9 | Claude Skills | GitHub API |
| 🎯 | 需求驱动 | SearXNG |

## 来源

- GitHub: https://github.com/stakeswky/skill-forge
- 基于天一进化引擎 (Evolution Engine) v0.3 构建
