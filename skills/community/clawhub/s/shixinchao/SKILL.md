---
name: 测试-史新超
description: 测试-史新超
dependency:
  python:
    - requests==2.31.0
---

// turbo-all

# 测试-史新超

## 任务目标

- 本 Skill 用于：测试-史新超
- 能力包含：智能问答、上下文理解、流式输出
- 触发条件：用户提问时自动触发

## 前置准备

- 依赖说明：scripts 脚本所需的依赖包及版本

  ```text
  requests==2.31.0
  ```

- 环境变量配置：
  - `API_KEY`：**必需**，API Key，用于调用接口

## 操作步骤

- 标准流程：
  1. **接收用户输入**
     - 智能体接收用户提出的问题或指令
     - 示例：你好，请问有什么可以帮助你的？
  
  2. **调用脚本**
     - 调用 `scripts/program.py` 处理问题
     - 必需参数：`--question "用户输入文本"`
     - 可选参数：根据应用配置动态生成
     - 脚本自动处理 API 调用和响应解析
  
  3. **返回结果**
     - 脚本返回 API 的答案
     - 智能体将结果以清晰易懂的方式呈现给用户

## 资源索引

- 必要脚本：见 [scripts/program.py](scripts/program.py)
- API 参考：见 [references/api_spec.md](references/api_spec.md)

## 注意事项

- API 调用使用流式输出，脚本会自动处理响应流
- API Key 从环境变量 `API_KEY` 读取，请确保已设置
- API 地址为 `https://developer.jointpilot.com/v1/api/async_chat/completions/`
- 请确保网络连接正常，API Key 有效
- 最后从返回值里获取答案

## 使用示例

### 示例 1：基本调用

```bash
python scripts/program.py --question "请介绍一下你的功能"
```

### 示例 2：完整调用

```bash
python scripts/program.py --question "帮我分析一下这个问题"
```
