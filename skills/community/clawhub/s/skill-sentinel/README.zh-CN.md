# ClawShield

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> 一个面向 OpenClaw Skill 的静态安全扫描器，在安装前识别高风险 shell 模式、可疑回调和社工式内容。

| 项目 | 内容 |
| --- | --- |
| 包名 | `@mike007jd/openclaw-clawshield` |
| 运行环境 | Node.js 18+ |
| 接口形态 | CLI + JavaScript 模块 |
| 主命令 | `scan` |

## 为什么需要它

无论是 Skill 市场还是内部仓库，都会引入供应链风险。ClawShield 的目标是在“不执行代码”的前提下尽早暴露这些风险，并返回可用于 CI 或安装流程的风险等级。

## 它会扫描什么

- `curl | sh` 这类下载即执行链路
- `eval()`、base64 解码等混淆或动态执行模式
- 指向未知或一次性端点的可疑外部回调
- 诱导用户绕过安全限制的社工式指令
- 通过 shell 包装隐藏远程执行的模式

## 典型工作流

1. 把 ClawShield 指向一个 skill 目录。
2. 查看风险等级和详细发现项。
3. 如有需要，导出 JSON 或 SARIF 供自动化使用。
4. 在 CI 中使用 `--fail-on caution|avoid` 阻止高风险变更进入主线。

## 快速开始

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/clawshield
npm install
node ./bin/clawshield.js scan ./fixtures/malicious-skill --format table --fail-on caution
```

## 命令说明

| 命令 | 作用 |
| --- | --- |
| `clawshield scan <skill-path> --format <table|json|sarif> --fail-on <caution|avoid> [--suppressions <path>]` | 扫描 skill，并在达到指定风险级别时让执行失败 |

## 风险模型

| 风险级别 | 含义 |
| --- | --- |
| `Safe` | 经 suppressions 处理后没有发现问题 |
| `Caution` | 存在中等级别问题，需要人工复核 |
| `Avoid` | 存在高等级问题，代表实质性风险 |

## Suppressions

ClawShield 支持 `.clawshield-suppressions.json` 文件，其中可声明 rule ID、文件路径、行号和 justification。没有 justification 的 suppressions 会被忽略。

## 项目结构

```text
clawshield/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## 当前状态

当前规则集刻意保持窄而实用，优先覆盖高信号的常见风险模式，适合本地审查、CI 阻断和 Safe Install 这类上游工具集成。
