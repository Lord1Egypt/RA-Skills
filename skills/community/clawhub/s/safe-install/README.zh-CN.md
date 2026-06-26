# Safe Install

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> 一个为 OpenClaw Skill 安装流程增加安全闸门的工具，先扫描、再激活，并保留可回滚快照。

| 项目 | 内容 |
| --- | --- |
| 包名 | `@mike007jd/openclaw-safe-install` |
| 运行环境 | Node.js 18+ |
| 接口形态 | CLI + JavaScript 模块 |
| 主要命令 | 安装、`history`、`rollback`、`policy validate` |

## 为什么需要它

安装一个 skill 不只是拷贝文件，本质上是在做一次信任决策。Safe Install 在这一步前面增加了一个安全控制层：先校验策略，再用 ClawShield 扫描源内容，记录安装指纹，并保留可回滚快照。

## 它能做什么

- 从本地路径或策略映射的 registry 项解析 skill 源
- 在执行安装前校验策略文件
- 使用 ClawShield 扫描待安装 skill
- 按策略和风险级别决定阻断或放行
- 在 `.openclaw-tools/safe-install` 下保存快照、当前状态和历史
- 将 skill 回滚到上一个已安装快照

## 典型工作流

1. 准备允许来源和阻断规则的策略文件。
2. 对本地路径或命名 skill 执行 Safe Install。
3. 安装后检查历史和当前激活状态。
4. 如果新版本有问题，直接回滚到上一版。

## 快速开始

Safe Install 依赖 ClawShield。在私有 IndieSite workspace 中，这个依赖已经由 npm workspaces 自动链接。

```bash
cd skills/openclaw/safe-install
node ./bin/safe-install.js ./fixtures/safe-skill --yes --format json
node ./bin/safe-install.js history --format table
```

## 命令说明

| 命令 | 作用 |
| --- | --- |
| `safe-install <skill[@version]|local-path>` | 在当前策略下扫描并安装 skill |
| `safe-install history` | 查看安装和阻断历史 |
| `safe-install rollback <skill>` | 恢复到上一个已安装快照 |
| `safe-install policy validate --file <path>` | 校验策略 JSON 文件 |

## 策略模型

Safe Install 会将你的配置与以下默认值合并：

```json
{
  "defaultAction": "prompt",
  "blockedPatterns": [],
  "allowedSources": [],
  "forceRequiredForAvoid": true
}
```

## 它会保存什么

- `snapshots/<skill>/<version>/<hash>`：用于回滚的版本快照
- `active/<skill>`：当前激活版本
- `history.json`：安装与阻断记录
- `state.json`：当前激活状态映射

## 项目结构

```text
safe-install/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## 当前状态

当前实现主要覆盖本地路径安装、策略校验、基于扫描结果的决策、历史追踪和回滚能力。它是一个更安全的安装控制层，而不是完整的远程 registry 客户端。
