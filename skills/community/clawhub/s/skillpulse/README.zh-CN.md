# Skill Profiler

[English](./README.md) | [简体中文](./README.zh-CN.md) | [한국어](./README.ko-KR.md)

> 一个面向 OpenClaw Skill 运行样本的性能分析 CLI，用原始日志快速生成瓶颈报告。

| 项目 | 内容 |
| --- | --- |
| 包名 | `@mike007jd/openclaw-skill-profiler` |
| 运行环境 | Node.js 18+ |
| 接口形态 | CLI + JavaScript 模块 |
| 主要命令 | `run`、`report`、`compare` |

## 为什么需要它

很多 OpenClaw 工作流在表面上是“能跑”的，但真正的问题往往出在尾延迟、CPU 消耗或者瞬时内存峰值。Skill Profiler 的作用就是把一组 JSON 样本快速汇总成可读结果，让你在上线前先看到哪个 skill 正在拖慢整体链路。

## 它能做什么

- 从 JSON 样本数组中汇总 `latencyMs`、`cpuMs`、`memoryMb`
- 按 skill 计算平均延迟、P95 延迟、平均 CPU 与峰值内存
- 按可配置阈值识别性能瓶颈
- 导出 JSON 或 HTML 报告，方便共享和复盘
- 对比两次采样结果，找出新增、删除和变化的 skill

## 典型工作流

1. 把运行样本整理成 JSON 数组。
2. 使用 `skill-profiler run` 快速检查热点。
3. 用 `skill-profiler report` 导出正式报告。
4. 用 `skill-profiler compare` 对比优化前后差异。

## 快速开始

```bash
git clone https://github.com/mike007jd/openclaw-skills.git
cd openclaw-skills/skill-profiler
npm install
node ./bin/skill-profiler.js run --input ./fixtures/samples-a.json
```

## 命令说明

| 命令 | 作用 |
| --- | --- |
| `skill-profiler run --input <samples.json>` | 分析一组样本，并根据瓶颈情况返回 `0` 或 `2` |
| `skill-profiler report --input <samples.json> --out <file>` | 导出 JSON 或 HTML 报告 |
| `skill-profiler compare --left <samples.json> --right <samples.json>` | 对比两次性能快照 |

## 示例输入

```json
[
  {
    "sessionId": "s1",
    "skill": "clawshield",
    "latencyMs": 1320,
    "cpuMs": 910,
    "memoryMb": 240
  }
]
```

## 输出重点

- `run` 会输出摘要表格或 JSON，并在超出阈值时以退出码 `2` 返回
- `report` 会生成可归档、可分享的分析结果
- `compare` 会直接指出回归、改善以及新增或删除的 skill

## 项目结构

```text
skill-profiler/
├── bin/
├── fixtures/
├── src/
├── test.js
└── SKILL.md
```

## 当前状态

当前实现更适合离线性能样本分析，而不是在线 tracing。已经覆盖阈值检测、报告导出和会话对比这三类核心能力。
