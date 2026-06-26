# 各平台 SKILL.md / README 格式规范

本文档详细说明各平台对技能描述文件的格式要求，供 `skill-distributor` 生成时参考。

---

## 1. WorkBuddy 格式（本地技能）

**文件**：`SKILL.md`（根目录）  
**特点**：支持 `allowed-tools` 字段，WorkBuddy 特有

```yaml
---
name: skill-name
description: 技能功能描述，触发词：关键词1、关键词2
version: "1.0.0"
author: username
allowed-tools: Read,Write,Bash
agent_created: true   # 可选，模型创建的技能加此标记
---
```

### 字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | 技能名称，小写、URL 安全 |
| `description` | ✅ | 功能描述，建议包含触发词 |
| `version` | 可选 | 语义化版本，字符串格式：`"1.0.0"` |
| `author` | 可选 | 作者标识 |
| `allowed-tools` | 可选 | WorkBuddy 特有，声明技能可使用的工具 |
| `agent_created` | 可选 | 模型创建的技能标记为 `true` |

---

## 2. ClawHub 格式（官方技能市场）

**文件**：`SKILL.md`（根目录）  
**发布命令**：`npx clawhub --workdir . skill publish . --version "1.0.0"`  
**⚠️ 关键**：ClawHub **不支持** `allowed-tools` 字段

```yaml
---
name: skill-name           # 必填，小写、URL 安全，匹配 ^[a-z0-9][a-z0-9-]*$
description: 功能描述     # 必填，用于搜索和展示
version: "1.0.0"        # 必填，字符串格式（加引号）
author: username           # 必填
---
```

### ClawHub 支持的元数据字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `name` | string | 技能名称（slug 格式） |
| `description` | string | 简短描述 |
| `version` | string | 语义化版本号，必须加引号 |
| `metadata.openclaw` | object | 运行时元数据（可选） |

### ClawHub 不支持的字段

- ❌ `allowed-tools`（WorkBuddy 特有）
- ❌ 自定义许可证（统一使用 MIT-0）
- ❌ 付费/定价功能

### `metadata.openclaw` 详细规范

```yaml
metadata:
  openclaw:
    requires:
      env:
        - API_KEY          # 必需的环境变量
      bins:
        - curl            # 必须安装的 CLI 二进制文件
      anyBins:
        - python3        # 至少存在一个的二进制文件
      config:
        - ~/.config/app  # 技能读取的配置文件路径
    primaryEnv: API_KEY   # 主凭证环境变量
    envVars:
      - name: API_KEY
        required: true
        description: API token
      - name: PROJECT_ID
        required: false
        description: Optional project ID
    always: false          # true = 始终激活（无需安装）
    skillKey: my-skill    # 覆盖技能调用键
    emoji: "🤖"           # 显示 emoji
    homepage: https://... # 技能主页 URL
    os:                   # 操作系统限制
      - macos
      - linux
    install:
      - kind: brew
        formula: jq
        bins: [jq]
      - kind: node
        package: typescript
        bins: [tsc]
    nix:
      # Nix 插件规格
    config:
      # Clawdbot 配置规格
```

---

## 3. GitHub README.md 格式

**文件**：`README.md`（根目录）  
**用途**：GitHub 仓库首页展示

```markdown
# 技能名称

> 一句话描述

## 安装

### OpenClaw
\`\`\`bash
clawhub skill install <skill-slug>
\`\`\`

### WorkBuddy
将本仓库下载到 WorkBuddy skills 目录...

## 使用方法

## 示例

## 适用场景

## 作者

```

---

## 4. 常见错误与解决方案

### ClawHub 发布常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `SKILL.md required` | 缺少 `--workdir .` 参数 | 使用 `clawhub --workdir . skill publish .` |
| `--version must be valid semver` | version 格式问题 | 改为 `version: "1.0.0"`（加引号） |
| `Error: Only HTML requests supported` | inspect 命令使用错误 | 用 `clawhub inspect <slug>` |

### WorkBuddy 格式注意

- `allowed-tools` 是 WorkBuddy 特有字段，发布到 ClawHub 前必须移除
- `version` 建议加引号，避免 YAML 解析为数字

---

## 5. 分发时的格式转换规则

| 源格式 | 目标平台 | 需要做的转换 |
|---------|----------|--------------|
| WorkBuddy SKILL.md | ClawHub | 移除 `allowed-tools`，确保 version 为字符串 |
| WorkBuddy SKILL.md | GitHub | 转换为 README.md 格式 |
| ClawHub SKILL.md | WorkBuddy | 可加 `allowed-tools`（可选） |

---

## 6. 文件大小限制

| 平台 | 限制 |
|------|------|
| ClawHub | 总包大小 ≤ 50MB，仅允许文本文件 |
| SkillsBook | ZIP 包 ≤ 10MB |
| GitHub | 无硬性限制，建议 ≤ 100MB |
