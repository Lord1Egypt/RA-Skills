---
name: structured-extraction
description: |
  把任意非结构化文本/网页/PDF 稳定抽取为机器可读的 JSON。固化 2025 一线实践：JSON mode + JSON Schema 约束 + few-shot + 输出引导 + 失败修复启发式。内置 json_repair 脚本（提取/修复/校验 JSON 块）。适用于文档抽取、网页字段提取、数据管道预处理。
version: 1.0.0
author: WorkBuddy
agent_created: true
visibility: "public"
tags:
  - extraction
  - 结构化
  - json
  - 数据抽取
  - schema
---

# structured-extraction — 稳定结构化抽取

_让 LLM 输出"代码能 json.loads()"的 JSON，而不是一段聊天。_

## 核心四要素（强制 JSON 的提示词范式）
1. **硬锁格式**：「只输出 JSON，不要任何解释/注释/多余文本」。更稳：用标记包裹 `---BEGIN JSON--- ... ---END JSON---`，代码只取标记间内容。
2. **具象模板**：给出 fill-in-the-blank 的 JSON 结构（键名、类型、必填、枚举、可选字段用 null 而非空串）。
3. **校验规则**：类型约束 + required 字段 + allowed values（枚举）。
4. **few-shot 示例**：1–3 个「输入→JSON」样例，教模型处理融合词/字段映射。

## 进阶手段（按稳定性递增）
- **JSON mode / function calling**：OpenAI 需在 prompt 含 "JSON" 字样；Claude 支持 XML；Ollama `format=json`。
- **JSON Schema 约束**（首选）：配合 JSON mode，true schema 强制，模型只能生成合法 JSON。
- **Pydantic 模型**：Python 侧用 `model_validate_json()` 强类型解析，失败显式报错。
- **降低 temperature**（如 0–0.2）提升输出稳定性。
- **输出引导（Output Priming）**：prompt 末尾留 `{` 引导模型续写结构，省 token。

## 脚本：JSON 提取 / 修复 / 校验
模型偶尔抽风生成非法 JSON，用本技能脚本兜底：
```bash
# 从模型混合输出中提取 JSON 块并修复
python scripts/json_repair.py <模型输出文件> --out clean.json

# 带 schema 校验（可选，传 schema json）
python scripts/json_repair.py out.txt --schema schema.json
```
修复启发式：补齐未闭合括号、给字符串补引号、清理尾随逗号、剥离标记外文本。

## 标准工作流
1. 定义目标 schema（字段/类型/必填/枚举）
2. 构造 prompt：硬锁格式 + 模板 + 校验规则 + 1–2 few-shot
3. 调模型（开 JSON mode + 低 temp）
4. 用 `json_repair.py` 提取并校验输出 → 进入下游管道
5. 失败则重试（最多 2–3 次）或换 schema 表述

## 自我进化学习系统
```bash
python scripts/learner.py record <技能目录> --capability JSON修复 --note "模型输出带 markdown 代码块，已剥离"
python scripts/learner.py record <技能目录> --capability 字段抽取 --fail --error 类型错误 --note "price 偶发字符串需 coerce"
python scripts/learner.py insight <技能目录>
python scripts/learner.py reflect <技能目录>
```
记忆落盘 `learned_patterns.json`，跨会话积累。

## 安全边界
- 抽取公开/授权数据；不处理个人隐私、密级文档。
- 校验失败要明确报错，禁止静默数据损坏。
