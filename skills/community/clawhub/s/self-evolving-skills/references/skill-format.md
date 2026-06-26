# SKILL.md 格式完整参考

本文档详细说明 SKILL.md 文件的完整格式规范，包括所有可用的 Frontmatter 字段和正文结构建议。

## Frontmatter 字段完整列表

```yaml
---
# ═══════════════════════════════════════════════════════════════════
# 必填字段
# ═══════════════════════════════════════════════════════════════════

name: skill-name                    # 技能名称
                                    # 规则：小写字母、数字、连字符、下划线、点号
                                    # 必须以字母或数字开头
                                    # 最大长度：64 字符
                                    # 示例：git-workflow, api-client, k8s-deploy

description: Brief description      # 技能描述
                                    # 用途：显示在 skills_list() 结果中
                                    # 最大长度：1024 字符
                                    # 建议：一句话说明技能解决什么问题

# ═══════════════════════════════════════════════════════════════════
# 推荐字段
# ═══════════════════════════════════════════════════════════════════

version: 1.0.0                      # 语义化版本号

author: Your Name                   # 作者名称

license: MIT                        # 许可证类型

# ═══════════════════════════════════════════════════════════════════
# 平台限制（可选）
# ═══════════════════════════════════════════════════════════════════

platforms: [macos, linux]           # 支持的操作系统
                                    # 可选值：macos, linux, windows
                                    # 不设置 = 支持所有平台
                                    # 示例：
                                    #   platforms: [macos]           # 仅 macOS
                                    #   platforms: [macos, linux]    # macOS 和 Linux

# ═══════════════════════════════════════════════════════════════════
# 环境变量要求（可选）
# ═══════════════════════════════════════════════════════════════════

required_environment_variables:     # 技能需要的环境变量
  - name: API_KEY                   # 环境变量名
    prompt: "Enter your API key"    # 提示用户输入时显示的文本
    help: "Get one at https://..."  # 帮助文本或获取地址
    required_for: "API access"      # 说明此变量用于什么功能

# ═══════════════════════════════════════════════════════════════════
# 凭证文件要求（可选）
# ═══════════════════════════════════════════════════════════════════

required_credential_files:          # 需要的凭证文件（相对于配置目录）
  - path: google_token.json
    description: Google OAuth2 token
  - path: client_secret.json
    description: OAuth2 client credentials

# ═══════════════════════════════════════════════════════════════════
# 元数据（可选但推荐）
# ═══════════════════════════════════════════════════════════════════

metadata:
  # 标签 - 用于搜索和分类
  tags: [DevOps, Deployment, Kubernetes]
  
  # 相关技能 - 推荐的关联技能
  related_skills: [docker, helm-charts]
  
  # ─────────────────────────────────────────────────────────────
  # 条件激活设置（可选，根据 Agent 平台支持情况使用）
  # ─────────────────────────────────────────────────────────────
  
  # 需要特定工具集才显示
  requires_toolsets: [web]        # 当 web 工具集不可用时隐藏
  
  # 需要特定工具才显示
  requires_tools: [web_search]    # 当 web_search 工具不可用时隐藏
  
  # 作为备用方案（主工具集可用时隐藏）
  fallback_for_toolsets: [browser]  # 当 browser 工具集可用时隐藏
  
  # 作为备用方案（主工具可用时隐藏）
  fallback_for_tools: [browser_navigate]  # 当该工具可用时隐藏
  
  # ─────────────────────────────────────────────────────────────
  # 配置设置（非敏感值）
  # ─────────────────────────────────────────────────────────────
  
  config:
    - key: my.setting.path        # 配置键（dotpath 格式）
      description: "What this controls"
      default: "~/default/path"   # 默认值
      prompt: "Display prompt"    # 设置时的提示文本

---
```

## 字段行为说明

### platforms 字段

| 设置 | 行为 |
|------|------|
| 不设置 | 所有平台都可见 |
| `[macos]` | 仅 macOS 可见 |
| `[linux]` | 仅 Linux 可见 |
| `[windows]` | 仅 Windows 可见 |
| `[macos, linux]` | macOS 和 Linux 可见 |

### 条件激活字段

| 字段 | 逻辑 | 用例 |
|------|------|------|
| `requires_toolsets` | 列表中任一不可用 → 隐藏 | 技能依赖特定工具集 |
| `requires_tools` | 列表中任一不可用 → 隐藏 | 技能依赖特定工具 |
| `fallback_for_toolsets` | 列表中任一可用 → 隐藏 | 作为主工具集的替代方案 |
| `fallback_for_tools` | 列表中任一可用 → 隐藏 | 作为主工具的替代方案 |

### 环境变量 vs 配置设置

| 类型 | 存储位置 | 用途 | 示例 |
|------|---------|------|------|
| `required_environment_variables` | 环境变量文件 (.env) | 敏感信息（API Key、Token） | OPENAI_API_KEY |
| `config` | 配置文件 (config.yaml) | 非敏感设置（路径、偏好） | wiki.path |

## 正文结构模板

```markdown
# Skill 标题

一句话介绍这个 Skill 解决什么问题。

## When to Use

明确的触发条件列表：
- 当用户要求 XXX 时
- 当需要 YYY 功能时
- 当遇到 ZZZ 场景时

## Prerequisites

### 环境要求

- 操作系统：macOS / Linux / Windows
- 必需工具：
  - `tool1` - 用途说明
  - `tool2` - 用途说明

### 认证设置

```bash
# 验证认证状态的命令
command --check-auth
```

## Quick Reference

| 操作 | 命令 |
|------|------|
| 操作 1 | `command1 args` |
| 操作 2 | `command2 args` |

## Procedure

### Step 1: [步骤名称]

步骤说明。

```bash
# 具体命令
command --with-args
```

预期输出：
```
expected output here
```

### Step 2: [步骤名称]

...

## Pitfalls

### ⚠️ 陷阱 1: [陷阱名称]

**症状：** 错误信息或异常行为描述

**原因：** 为什么会发生

**解决方案：**
```bash
# 修复命令
fix-command
```

### ⚠️ 陷阱 2: [陷阱名称]

...

## Verification

### 成功标志

- [ ] 检查项 1
- [ ] 检查项 2

### 验证命令

```bash
# 验证命令
verify-command
# 预期输出
expected result
```

## Advanced Usage

（可选）高级用法、边缘情况、优化建议等。
```

## 文件大小限制

| 资源 | 限制 |
|------|------|
| SKILL.md 内容 | 100,000 字符 (~36k tokens) |
| 支撑文件大小 | 1 MiB (1,048,576 bytes) |
| 技能名称长度 | 64 字符 |
| 描述长度 | 1,024 字符 |

## 命名规范

### 技能名称 (name)

✅ 合法示例：
- `git-workflow`
- `api-client`
- `k8s.deploy`
- `data_processing`

❌ 非法示例：
- `Git-Workflow` (不能有大写)
- `-start-with-dash` (不能以连字符开头)
- `name with spaces` (不能有空格)
- `name/with/slashes` (不能有斜杠)

### 分类名称 (category)

与技能名称规范相同，用于组织技能目录：

```
<skills-directory>/
├── devops/           # 分类
│   ├── k8s-deploy/
│   └── docker-build/
├── data-science/     # 分类
│   └── jupyter-workflow/
└── uncategorized-skill/  # 无分类，直接在根目录
```
