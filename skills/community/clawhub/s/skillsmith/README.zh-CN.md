# Skill Starter

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> 一个用于生成 OpenClaw Skill 项目骨架的 CLI，默认就带上更干净、更安全的起步结构。

| 项目 | 内容 |
| --- | --- |
| 包名 | `@mike007jd/openclaw-skill-starter` |
| 运行环境 | Node.js 18+ |
| 接口形态 | CLI + 项目生成器 |
| 模板 | `standard`、`strict-security` |

## 为什么需要它

一个 skill 的第一版目录结构，通常会直接决定后续项目是持续干净，还是迅速堆出一堆临时文件和遗漏的安全约束。Skill Starter 的目标就是把“正确的起点”变成默认值，让你一开始就拥有可编辑的 `SKILL.md`、测试占位、变更日志、样例数据和可选 CI 工作流。

## 它会生成什么

- 统一的 OpenClaw Skill 项目结构
- 自带 frontmatter 和安全说明的 `SKILL.md`
- `docs/`、`scripts/`、`.env.example`、`CHANGELOG.md`
- `tests/` 下的 smoke test 模板
- 性能分析样例与辅助脚本
- 可选的 GitHub Actions 安全扫描工作流
- 更严格模板下的 `.openclaw-tools/safe-install.policy.json`

## 典型工作流

1. 选择 skill 名称和模板。
2. 用交互式或无交互方式生成项目。
3. 填入真实业务逻辑、策略与文档。
4. 跑通内置 smoke test，再补上正式 lint / test。

## 快速开始

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/skill-starter
npm install
node ./bin/create-openclaw-skill.js review-assistant --no-prompts --template strict-security --ci --out /tmp
```

## 命令说明

| 命令 | 作用 |
| --- | --- |
| `create-openclaw-skill <name> [--template <standard|strict-security>] [--ci] [--no-prompts] [--force] [--out <dir>]` | 生成一个新的 skill 项目 |

## 生成结果示意

```text
<skill-name>/
├── SKILL.md
├── docs/README.md
├── scripts/README.md
├── fixtures/profile-input.json
├── tests/smoke.test.js
├── .env.example
└── CHANGELOG.md
```

## 模板选择

| 模板 | 适用场景 |
| --- | --- |
| `standard` | 快速内部原型和通用型 skill |
| `strict-security` | 需要更强安全默认值、CI 扫描和策略骨架的 skill |

## 项目结构

```text
skill-starter/
├── bin/
├── src/
├── test.js
└── SKILL.md
```

## 当前状态

Skill Starter 是一个有明确意见但保持轻量的脚手架工具。它不试图一次生成完整生产系统，而是优先把新 skill 拉到“可 review、可继续扩展”的状态。
