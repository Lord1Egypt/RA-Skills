---
name: {{skill-name}}
description: {{一句话描述这个 Skill 解决什么问题}}
version: 1.0.0
author: {{作者名称}}
license: MIT
# 如果技能只支持特定平台，取消下面一行的注释并修改
# platforms: [macos, linux, windows]
metadata:
  tags: [{{标签1}}, {{标签2}}]
  related_skills: [{{相关技能名}}]
  # 如果需要条件激活，取消下面的注释并配置（根据 Agent 平台支持情况）
  # requires_toolsets: [web]
  # fallback_for_tools: [browser_navigate]
# 如果需要环境变量，取消下面的注释并配置
# required_environment_variables:
#   - name: API_KEY
#     prompt: "Enter your API key"
#     help: "Get one at https://example.com"
---

# {{Skill 标题}}

{{简要介绍这个 Skill 解决什么问题。1-2 句话。}}

## When to Use

**触发条件：**

- 当用户要求 {{场景 1}} 时
- 当需要 {{场景 2}} 时
- 当遇到 {{场景 3}} 时

**不适用场景：**

- {{不适用场景 1}}
- {{不适用场景 2}}

## Prerequisites

### 环境要求

- 操作系统：{{macOS / Linux / Windows / 全平台}}
- 必需工具：
  - `{{tool1}}` - {{用途说明}}
  - `{{tool2}}` - {{用途说明}}

### 认证/配置（如有）

```bash
# 验证环境是否就绪
{{验证命令}}
```

## Quick Reference

| 操作 | 命令/方法 |
|------|----------|
| {{操作 1}} | `{{命令1}}` |
| {{操作 2}} | `{{命令2}}` |
| {{操作 3}} | `{{命令3}}` |

## Procedure

### Step 1: {{步骤名称}}

{{步骤说明}}

```bash
# {{命令说明}}
{{具体命令}}
```

**预期结果：**
```
{{预期输出}}
```

### Step 2: {{步骤名称}}

{{步骤说明}}

```bash
{{具体命令}}
```

### Step 3: {{步骤名称}}

{{继续添加必要的步骤...}}

## Pitfalls

### ⚠️ {{陷阱 1 名称}}

**症状：**
```
{{错误信息或异常行为}}
```

**原因：** {{为什么会发生}}

**解决方案：**
```bash
{{修复命令或步骤}}
```

### ⚠️ {{陷阱 2 名称}}

**症状：** {{症状描述}}

**解决方案：** {{解决方案}}

## Verification

### 成功标志

- [ ] {{检查项 1}}
- [ ] {{检查项 2}}
- [ ] {{检查项 3}}

### 验证命令

```bash
# 验证任务完成
{{验证命令}}

# 预期输出
{{预期结果}}
```

## Advanced Usage（可选）

{{高级用法、优化建议、边缘情况处理等}}

---

*最后更新: {{日期}}*
