# readme-craft

AI agent skill，写出让人在 30 秒内决定用不用你项目的 README。

[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Patterns: 22](https://img.shields.io/badge/audit_checks-22-orange)]()
[![Anti-patterns: 15](https://img.shields.io/badge/anti--patterns-15-red)]()

蒸馏自 [OMC](https://github.com/Yeachan-Heo/oh-my-claudecode) / [ECC](https://github.com/affaan-m/everything-claude-code) 实战 README + [awesome-readme](https://github.com/matiassingers/awesome-readme) / [Standard README](https://github.com/RichardLitt/standard-readme) / [Art of README](https://github.com/hackergrrl/art-of-readme) 社区标准 + ClawHub 10+ README skills。

## Quick Start

```bash
# Claude Code
/readme-craft                          # 有 README → audit，无 → create
/readme-craft --mode audit             # 只评分不改
/readme-craft --mode rewrite           # 重写现有
```

```
Score: 73/100 (B)
| Category   | Score | Max | Issues              |
|------------|-------|-----|----------------------|
| Hook       | 18    | 25  | 缺少 Hero Visual     |
| Onboarding | 20    | 25  | Quick Start 超过 5 步 |
| Content    | 15    | 20  | 配置项未文档化        |
| Trust      | 12    | 15  | 无 Contributing 指南  |
...
Top 3: 添加 GIF demo (+7), 简化 Quick Start (+5), 添加 Contributing (+3)
```

## 三个模式

| 模式 | 做什么 | 改不改文件 |
|------|--------|-----------|
| `create` | 扫描项目元数据 + 源码 → 生成 README | 写入 README.md |
| `audit` | 22 项检查 → 0-100 分 + 诊断报告 | 不改 |
| `rewrite` | 内部 audit → 保留好的部分 → 补充缺失 → diff 确认 | 确认后写入 |

## 核心：认知漏斗

README 的每一层都是过滤器——读者在任何一层可以决定深入或离开：

```
项目名          → 0.5s → 和我有关吗？
一行描述        → 2s   → 解决什么问题？
Demo/截图       → 5s   → 长什么样？
Quick Start     → 30s  → 用起来难吗？
功能详情        → 2min → 满足需求吗？
```

规则：不要在漏斗上层放下层的信息。

## 22 项评分体系

| 类别 | 权重 | 核心判定 |
|------|------|----------|
| **Hook** | 25% | 项目名清晰？一行描述 < 120 字符？有 Hero Visual？ |
| **Onboarding** | 25% | Quick Start ≤ 3 步？安装可复制？Usage 有代码块？ |
| **Content** | 20% | Features 用列表不用散文？配置有文档？信息不过时？ |
| **Trust** | 15% | License 在最后？Contributing 存在？CI badge 绿色？ |
| **Structure** | 10% | 认知漏斗顺序？超 100 行有 TOC？ |
| **Polish** | 5% | 无死链？Markdown 正确？移动端可读？ |

等级：**S**(90+) **A**(80-89) **B**(70-79) **C**(60-69) **D**(<60)

完整 22 项检查清单见 [`references/quality-checklist.md`](references/quality-checklist.md)。

## 项目类型适配

| 类型 | Hero Visual | Quick Start 重点 |
|------|------------|------------------|
| CLI 工具 | 终端 GIF (vhs) | `npm i -g && cmd --help` |
| 库/SDK | 代码截图 | `npm i && import` + 3 行用法 |
| Web 应用 | 浏览器截图 | `git clone && npm start` |
| 框架 | Mermaid 架构图 | `npx create-xxx` |
| 插件 | 安装截图 | 一键安装命令 |
| Monorepo | 带注释目录树 | 顶层入口 + 子包导航 |

## 15 个反模式

最常见 5 个：

| # | 反模式 | 修复 |
|---|--------|------|
| 7 | **模糊描述**「A utility for things」 | 说清楚解决什么问题、给谁用 |
| 8 | **省略安装** | 写完整命令，包括前置依赖 |
| 9 | **只说不做**（无代码示例） | 每个功能至少一个代码块 |
| 3 | **垃圾场**（全塞一个文件） | 拆分到 docs/、CONTRIBUTING.md |
| 10 | **时光胶囊**（README 过时） | 改代码时同步改 README |

完整 15 个见 [`references/anti-patterns.md`](references/anti-patterns.md)。

## Project Structure

```
readme-craft/
├── SKILL.md                           # AI 消费的核心指令 (357 行)
├── task_suite.yaml                     # 7 个评估任务
└── references/
    ├── quality-checklist.md            # 22 项评分细则
    ├── anti-patterns.md                # 15 个反模式 + 检测方法
    ├── badge-and-visuals.md            # 徽章格式、视觉资产模板
    ├── community-standards.md          # 6 个社区标准汇总
    └── real-world-patterns.md          # OMC/ECC/ClawHub 实战模式
```

## 蒸馏来源

| 来源 | 提取了什么 |
|------|-----------|
| OMC README (500 行) | 3 步 Quick Start、Magic Keywords 表格 |
| ECC README (1,388 行) | 带注释目录树、折叠 FAQ、跨平台对比表 |
| awesome-readme / Standard README | 认知漏斗、合规检查清单 |
| Art of README | 「无源码测试」原则 |
| ClawHub good-readme | 100 分制评分、反模式目录 |
| ClawHub writing-readme | Golden Structure、项目类型适配 |
| ClawHub readme-roast | 基准对标方法论 |

## Related Skills

| Skill | 关系 |
|-------|------|
| deslop | README 写完后去 AI 味 |
| slopbuster | 更强的去 AI 味，适合对外发布 |
| doc-gen | API 文档、架构文档（README 之外） |
| improvement-learner | 评估 readme-craft 自身质量 |

## License

MIT
