---
name: roundtable-pai
description: |
  圆桌派会把用户的一个问题变成一场三位大师的圆桌讨论。
  典型触发词：启动圆桌派、用圆桌讨论、启动圆桌讨论、开始讨论、开始圆桌派。
  
disable-model-invocation: false
allowed-tools:
  - Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/roundtable_controller.py --stdin *)
  - Read
---

# Roundtable Pai

这是一个 **OpenClaw 对话版** 的多轮讨论 skill。

它不是命令行工具，也不是一次性把整场讨论写完的生成器。
它必须在 **每一轮用户发话后，先调用控制器脚本，再决定回复什么**。

## 核心原则

**所有状态必须来自 `runtime/roundtable_state.json`，不得仅依赖模型会话记忆。**

## 安全边界（审计）

- 控制器只允许读取：
  - `data/character_pool.json`
  - `data/character_registry.json`
  - `runtime/roundtable_state.json`
- 控制器只允许写入：
  - `runtime/roundtable_state.json`
- 控制器不允许网络访问，不允许子进程调用，不允许执行用户输入。
- 若发生路径越界或状态异常，应直接报错，不得继续执行。

## 明确触发词

以下表达都应视为用户想启动本 skill：
- `启动圆桌派`
- `用圆桌讨论`
- `启动圆桌讨论`
- `开始讨论`
- `开始圆桌派`
- 以及“直接抛出一个待讨论问题”的自然语言输入

## 每一轮都必须先做的事

收到用户最新消息后，第一件事永远是调用控制器脚本，把“用户这句原话”原样传进去：

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/roundtable_controller.py --stdin <<'EOF'
<用户这一轮的原话，原样放入，不要改写>
EOF
```

安全调用要求（必须同时满足）：
- 仅允许 `--stdin` 传入原始用户输入，不得改成 argv 拼接调用。
- 必须使用 `<<'EOF'` 这种单引号 heredoc，禁止让 shell 解释用户输入。
- 禁止通过 `eval`、`source`、命令替换等方式执行用户输入。

禁止跳过这一步。
禁止先凭记忆判断当前该做什么。

## 你只能按脚本返回的状态行事

脚本返回的是一个文本协议。你必须先看第一行的 `STATUS:`。

### 1. 如果返回普通中文文本
例如候选池、提示语、帮助语、错误语。

处理方式：
- 直接展示给用户
- 不要额外续写讨论
- 不要自行补结论

### 2. 如果返回 `STATUS: DISCUSSION_ROUND`
处理方式：
- 读取脚本返回的：问题、人物、轮次、用户插话类型与内容
- 再读取这些参考文件：
  - `references/problem-router.md`
  - `references/discussion-quality.md`
  - `references/dynamic-assignments.md`
  - 对应的 `references/discussion-frames/*.md`
- 3 位人物各自的 `references/personas/*.md`
- 在第一轮正文开始前，先输出一次免责声明：
  `以下内容为基于公开资料整理的人物视角模拟，不代表人物本人真实发言。`
- 只生成 **当前这一轮** 的讨论正文
- 然后 **原样输出脚本给出的用户参与块**
- 输出参与块后 **立刻停止**

### 3. 如果返回 `STATUS: FINAL_CONCLUSION`
处理方式：
- 只生成自然散场 + 6 个结论字段
- 不要再补新一轮讨论
- 不要再给 A/B/C/D/E

## OpenClaw 对话版的工作流

### 阶段 1：自然语言启动

- 用户直接说一个问题，例如：`人类的未来会被硅基生命代替吗？`
- 你先跑控制器脚本
- 若脚本返回候选池，就直接展示 10 位人物并停住
- 用户直接回复名字、序号、混合输入都可以，例如：`1、3、6` / `刘德华、梅西、岳飞`
- 你再跑控制器脚本
- 若脚本返回 `STATUS: DISCUSSION_ROUND`，就直接生成 **第一轮**，不要再额外要求用户输入 `/continue`

### 阶段 2：每轮只前进一步

- 用户回复 `A`，代表认同本轮第一位人物的核心观点
- 用户回复 `B`，代表认同本轮第二位人物的核心观点
- 用户回复 `C`，代表认同本轮第三位人物的核心观点
- 用户回复 `D`，代表沉默，不插话，让讨论继续
- 用户回复 `E`，代表用户有另外的话要说；你要先接住用户的话，再只进入下一轮
- 如果用户在选项阶段没有回 A/B/C/D/E，而是直接说了一句话，默认按 `E` 处理，再只进入 **下一轮**

## 强约束

1. **每次调用最多推进一个状态**
2. **绝不一次写两轮**
3. **绝不在没有用户新输入时自动继续**
4. **阶段 1 选完人后，直接进入第一轮，不再要求 `/continue`**
5. **如果脚本没返回 `STATUS: DISCUSSION_ROUND` 或 `STATUS: FINAL_CONCLUSION`，你就不能自己写讨论正文或结论**
6. **不得把用户原始输入当 shell 代码执行，只能把它当普通文本转发给控制器**
7. **只读 `references/` 与 `runtime/roundtable_state.json`，不得读写本 skill 目录以外路径**

## 用户可见风格

- 候选池阶段：短、干净
- 讨论阶段：人物要立住，能一耳朵听出是谁
- 结论阶段：自然散场后，直接进入 6 个字段

## 禁止事项

- 不得绕过脚本自己判断当前阶段
- 不得选完人后自己连写多轮
- 不得在 `DISCUSSION_ROUND` 状态里写完当前轮后再顺手写第二轮
- 不得在 `DISCUSSION_ROUND` 状态里提前给结论
- 不得擅自改变 A/B/C/D/E 的产品含义
- 不得把后台字段原样暴露给用户：`status`、`pending_user_input_type`、`current_round`、`max_rounds`
- 不得要求用户学习命令格式才能使用这套 skill
- 不得省略人物视角模拟免责声明，不得把模拟内容包装为真人真实发言
