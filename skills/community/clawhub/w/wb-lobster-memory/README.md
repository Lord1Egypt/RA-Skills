# wb-lobster-memory

WorkBuddy 接入 [lobster-memory](https://github.com/LittleLollipop/lobster-memory) 长期图记忆的桥接技能。

作为 WorkBuddy 现有"云端 profile + 工作区 markdown"记忆**之外的并行补充层**，用知识图谱（实体-关系-情绪 valence）记录用户的偏好、项目脉络与反馈，支持按需回忆与定期巩固遗忘。抽取 JSON 由 WorkBuddy 自身兼任 LLM 生成（无平台 post-turn 钩子，靠惯例触发）。

## 文件

- `SKILL.md` — 技能说明、使用惯例、抽取 JSON schema
- `runner.py` — 命令行桥接脚本（status / remember / recall / feedback / should / consolidate）

## 前提

- 已安装并编译好的 [lobster-memory](https://github.com/LittleLollipop/lobster-memory)（底层 `axolotl_rs`）。
- `SKILL.md` 与 `runner.py` 中的路径**默认指向作者本机**（`/Users/sai/.workbuddy/...`），但均可经环境变量覆盖，他人无需改代码：
  - `LOBSTER_MEMORY_ENGINE`：lobster-memory 的 `engine/` 目录
  - `LOBSTER_MEMORY_DIR`：图文件存储目录（图文件名为 `memory.axeb`）
  - `LOBSTER_MEMORY_CONSOLIDATE_EVERY`：巩固周期（轮，默认 20）
  - 调用 `runner.py` 的 python 必须是有 `axolotl_rs` 的 lobster-memory venv 的 python

## 用法

加载技能后见 `SKILL.md` 中的"WorkBuddy 使用惯例"。核心流程：

```
# 可选：覆盖默认路径（他人使用前按需设置）
export LOBSTER_MEMORY_ENGINE=/your/path/lobster-memory
export LOBSTER_MEMORY_DIR=~/.lobster-memory

PY=/path/to/venvs/lobster-memory/bin/python
RUN=wb-lobster-memory/runner.py
$PY $RUN status                 # 会话起步：感知当前记忆规模
$PY $RUN remember --json '<抽取JSON>'   # 每轮有实质内容后落盘（WB 兼任 LLM 产出 JSON）
$PY $RUN recall <关键词>        # 按需回忆
$PY $RUN consolidate --round N  # 约每 20 轮或容量告警时巩固
```

## 更新日志

### v0.2.1 (2026-07-23)
- 版本对齐 lobster-memory v0.2.1（无功能改动，仅 SKILL.md 版本号）

### v0.2.0 (2026-07-23)
- 新增 `consolidate --dry-run`：先预览合并/遗忘计划表，再决定是否实跑，避免误删
- 渲染合并与遗忘计划，列出每个候选节点的类型、分数、休眠天数与处置原因

### v0.1.0 (2026-07-10)
- 初始版本：WorkBuddy 桥接层（status / remember / recall / feedback / should / consolidate）
- 抽取 JSON 由 WorkBuddy 自身兼任 LLM 生成
- 声明仅支持 Apple Silicon（M 系列）
