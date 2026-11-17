---
name: tool-use
description: |
  函数调用 / 工具编排助手（agent 行动力核心）。把自然语言意图转化为结构化 tool_call（名称 + 参数 JSON），生成符合 OpenAI 函数调用规范的 schema，并提供本地调度器（dispatch）：按 schema 校验参数、安全执行已注册工具、回收结果。当用户需要"定义工具 schema""做 function calling""让 agent 调用工具""tool dispatch""注册并调用工具"时调用。
agent_created: true
visibility: "public"
---

# 工具调用（Tool-Use）· 函数调用与编排

让 agent 从"只会说"变成"能做事"：把意图变成可执行的 tool_call，并按 schema 安全调度真实工具。这是 agent 行动力的核心一环，也是元进化循环能从"规划"落到"执行"的关键。

## 适用场景
- 给大模型/agent 设计可用的工具清单（function schema）
- 把用户一句话意图解析成 `{name, arguments}` 并分发执行
- 在 agent 编排中管理多个工具的注册、校验、调用
- 把已有脚本/命令封装成可被 agent 调用的工具

## 标准工作流
### 1) 生成工具 schema
```bash
python scripts/schema.py --spec tool_spec.json --out schema.json
```
`tool_spec.json` 示例：
```json
{"name":"get_weather","description":"查询城市天气","parameters":[
  {"name":"city","type":"string","required":true,"description":"城市名"}]}
```
输出 OpenAI 风格：`{"type":"function","function":{"name":...,"parameters":{"type":"object","properties":{...},"required":[...]}}}`

### 2) 注册并调度工具
```bash
python scripts/dispatch.py --registry reg.json --call '{"name":"echo","arguments":{"text":"hi"}}' --out result.json
```
`reg.json`：`{"echo":{"type":"command","cmd":"echo {text}"}}`（也支持 type:python 调用已注册函数）

## 安全边界
- 只执行**注册表中显式声明**的工具，拒绝任意代码执行
- 参数先按 schema 校验（类型/必填）再执行，避免注入
- command 类型工具默认禁用 shell 通配/重定向等非必要能力；危险命令需人工确认

## 自进化学习系统
```bash
python scripts/learner.py record . --capability "工具调用" [--fail --error <类型> --note <说明>]
python scripts/learner.py insight .
python scripts/learner.py reflect .
```
- 某类工具的 schema 常被模型填错参数 → 记录，reflect 建议收紧参数描述/枚举
- 高频工具 → `prefer` 记录，未来默认预注册
