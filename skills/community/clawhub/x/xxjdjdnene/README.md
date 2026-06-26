# AI PM Coach

> 我是教练，不是工具。我引导你思考，不替你做决策。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skill Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/openclaw/ai-pm-coach)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-Compatible-green.svg)](https://openclaw.ai)

---

## 核心理念

```
❌ 旧思路：一键生成 → AI 替你做 → 你只是执行者

✅ 新思路：引导式对话 → 你做决策 → 你是导演
```

---

## 与传统工具的区别

| 传统工具 | AI PM Coach |
|----------|-------------|
| 命令-输出模式 | 对话-引导模式 |
| AI 替你做决策 | 你做决策，AI 引导 |
| 输出即最终结果 | 输出是你的决策汇总 |
| 用户是使用者 | 用户是学习者 |
| 单次交互 | 持续对话 |

---

## 工作流程

```
痛点诊断 → AI 适用性评估 → 能力边界定义 → 置信度设计 → 幻觉应对 → PRD 整合
   ↓            ↓              ↓             ↓            ↓          ↓
 澄清问题     评分判断       边界确认       阈值设置     容忍度定义   决策汇总
```

---

## 使用示例

### 启动对话

```
用户：我想设计一个 AI 客服助手

教练：很好！让我们一步步来。首先，这个产品要解决什么核心问题？

用户：用户抱怨客服响应太慢

教练：明白了。这个问题影响有多大？

用户：大概 70% 的用户都抱怨过

教练：那确实是个大问题。目前是怎么解决的？

用户：加了很多客服，但成本太高

教练：所以降本是主要诉求。那你觉得 AI 能处理多少比例的问题？

用户：70% 吧

教练：这个目标很积极！但 AI 不是万能的，我们来看看它具体能做什么...
```

---

## 决策节点

在以下节点，你需要做出选择：

| 节点 | 你需要决策 |
|------|-----------|
| 痛点确认 | 是否值得用 AI 解决？ |
| 边界确认 | AI 能做什么、不能做什么？ |
| 阈值设置 | 置信度设多少？转人工比例上限？ |
| 容忍度定义 | 什么错误可以接受？ |
| 责任划分 | AI 出错谁负责？ |

---

## 内部架构

本 Sub Agent 内部包装以下 Skill：

| Skill | 功能 | 调用时机 |
|-------|------|----------|
| pain-check-skill | 痛点评估 | 评估 AI 适用性时 |
| boundary-skill | 边界定义 | 定义能力边界时 |
| confidence-skill | 置信度设计 | 设计置信度机制时 |
| hallucination-skill | 幻觉应对 | 规划错误应对时 |
| prd-skill | PRD 生成 | 整合输出时 |

---

## 安装

```bash
# OpenClaw
cp -r ai-pm-coach ~/.openclaw/skills/

# 重启 Agent
```

---

## 对话风格

- 提问而非陈述
- 一步步深入
- 让你做决策
- 记录你的选择

---

## 留白声明

> 我是教练，不是替你做作业的人。
>
> 所有的决策，都需要你来确认。
>
> 因为这是你的产品，你才是导演。

---

<p align="center">
  Made with ❤️ by OpenClaw Team
</p>
