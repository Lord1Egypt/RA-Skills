---
name: spec-developer
description: 自动化 Spec 驱动开发流程 (spec-draft, spec-plan, spec-execute)
domain: engineering
homepage: https://github.com/soponcd/timeflow-skills/tree/main/teams/skills/spec-developer
metadata:
  clawdbot:
    emoji: 📋
---

# Spec Developer Skills

本技能集提供一组简短命令，用于快速驱动 Spec 开发流程。

## 🚀 核心指令

### 0. spec (帮助)
**指令**: `/spec`
**行为**:
1. 输出 Spec 开发模式的完整帮助信息。
2. 列出可用命令及其说明。
3. 显示当前的 specs/ 目录结构概览。

### 1. spec-draft (起草)
**指令**: `/spec-draft "功能描述"`
**行为**:
1. 分析用户描述，生成 kebab-case 文件名 (如 `specs/features/zero-width-sync.md`)
2. 读取模板 `.agent/skills/spec-developer/templates/feature-spec.md`
3. 填充 `Goal`, `User Stories`, `Technical Design` 等章节
4. 写入文件并展示给用户审查

### 2. spec-plan (规划)
**指令**: `/spec-plan specs/features/xxx.md`
**行为**:
1. 读取目标 Spec 文件
2. 读取主任务清单 `specs/tasks.md`
3. 将 Spec 中的 "Tasks Breakdown" 章节提取并追加到 `specs/tasks.md` 的新里程碑中
4. 确保任务编号 (TASK-XXX) 连续且唯一

### 3. spec-execute (执行)
**指令**: `/spec-execute specs/features/xxx.md`
**行为**:
1. 读取 Spec 文件和 `CLAUDE.md` (确保遵循技术红线)
2. **循环执行** Spec 中的每个未完成任务：
   - 使用 `TaskCreate` 创建会话级任务
   - 编写/修改代码 (遵循 Swift 6 并发规则)
   - 编写单元测试
   - 运行 `./tools/run_native_tests.sh fast`
   - 通过后，更新 `specs/tasks.md` 勾选该任务
3. 所有任务完成后，更新 Spec 头部 Status 为 "Implemented"

## 使用示例

```bash
# 1. 起草新功能
/spec-draft "实现 iOS 17 交互式 Widget"

# 2. 注册到任务清单
/spec-plan specs/features/interactive-widget.md

# 3. 开始自动实施
/spec-execute specs/features/interactive-widget.md
```
