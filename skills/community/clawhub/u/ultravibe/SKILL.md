---
name: ultravibe
description: UltraVibe 意图路由表。收到 /uv 命令后识别意图,分派到对应流程 skill,由 Codex 会话内自主推进,不依赖外部状态机驱动。
---

# Skill: ultravibe — 意图识别路由(自动生成)

> ⚠️ 此文件由 generate-skill 自动生成,请勿手动修改。修改路由请编辑 `intent-map.json`。

## 输入
- 用户原始描述
- `auto_mode`(bool,默认 true):v3 下直接执行,不等待逐阶段确认

## 运行方式

### 方式一:结构化配置路由(推荐)
存在 `intent-map.json` 或 `uv.config.json.intentMap` 时,调:
```bash
npx tsx src/index.ts route-intent --description "<用户描述>"
```
返回 flowId,然后加载对应 flow 定义(`flows/<flowId>.json` 或内置默认)。

### 方式二:关键词硬编码路由(向后兼容)

| 分类 | 关键词 | 目标 skill | 阶段数 |
|------|--------|-----------|--------|
| bugfix | bug、修复、报错、崩溃、异常、不工作、错误 | ultravibe-bugfix | 5 (BF-1/BF-2/BF-3/BF-4/BF-5) |
| feature | 新增、开发、实现、功能、支持、添加、feature | ultravibe-feature | 5 (FE-1/FE-2/FE-3/FE-4/FE-5) |
| refactor | 重构、优化代码、整理、提取、拆分、refactor | ultravibe-refactor | 4 (RF-1/RF-2/RF-3/RF-4) |
| review | 审查、检查、audit、安全、合规、review | ultravibe-review | 4 (RV-1/RV-2/RV-3/RV-4) |
| feature | (默认) | ultravibe-feature | - |

冲突时默认 feature。显式指定(如 `/uv bugfix xxx`)由入口命令表直接路由。

### 可用流程
- **Bug 修复** (`bugfix`): BF-1 → BF-2 → BF-3 → BF-4 → BF-5 → done
- **功能开发** (`feature`): FE-1 → FE-2 → FE-3 → FE-4 → FE-5 → done
- **代码重构** (`refactor`): RF-1 → RF-2 → RF-3 → RF-4 → done
- **代码审查** (`review`): RV-1 → RV-2 → RV-3 → RV-4 → done

### 3. 分派
- 读取目标 skill SKILL.md(`.codex/skills/ultravibe-<target>/SKILL.md`)
- 传递:用户需求全文 + 当前工作目录
- 本 skill 任务结束;后续阶段推进在目标 skill 会话内完成

### 4. 约定
- 不修改用户原始需求文本
- v3 不引入外部状态机干预;TS 工具集仅在被调用时执行机械验证
- 所有流程共享前缀:preflight-check → checkpoint read → timeout-check
