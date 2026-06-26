---
name: skill-isolator
description: |
  Project-based skill isolation and management. Enables different projects to use different skill sets with automatic loading based on current working directory. Supports multiple skill sources (clawhub, local, git, url) with priority-based resolution, version locking, and auto-sync. Use when: (1) working in a project with .openclaw-skills.json, (2) need to manage project-specific skills, (3) want to isolate skills between projects, (4) need to install skills from clawhub or other sources.
version: 1.0.0
author: Xiao Xia
license: MIT
---

# skill-isolator

为不同项目提供独立的技能配置和隔离管理，实现技能按需加载、项目间完全隔离。

## 快速开始

### 1️⃣ 创建项目配置

在项目根目录创建 `.openclaw-skills.json`：

```bash
# 使用交互向导
node scripts/init-project-config.js

# 或手动创建（最小配置）
echo '{"skills":["weather"],"excludeGlobal":true}' > .openclaw-skills.json
```

### 2️⃣ 同步技能

```bash
# 自动检测并安装缺失技能
node scripts/sync-project-skills.js
```

### 3️⃣ 验证配置

```bash
node scripts/validate-config.js
```

---

## 核心功能

| 功能 | 说明 |
|------|------|
| **🔒 项目隔离** | 每个项目独立技能配置，切换项目自动切换技能 |
| **🌐 多源支持** | clawhub / local / git / url，优先级可配置 |
| **📦 版本控制** | 支持锁定特定版本或 `latest` 自动更新 |
| **⚡ 自动同步** | 进入项目时自动检测并安装缺失技能 |
| **💾 智能缓存** | 减少重复下载，可配置 TTL |
| **🎯 冲突解决** | 项目配置 > 全局配置，同名技能取高优先级源 |

---

## 配置文件详解

### 完整示例

```json
{
  "name": "my-project",
  "skills": [
    { "name": "feishu-doc", "version": "latest" },
    { "name": "weather", "version": "1.2.0" },
    "stock-analyzer"
  ],
  "excludeGlobal": true,
  "sources": [
    {
      "name": "clawhub",
      "type": "registry",
      "priority": 1,
      "enabled": true
    },
    {
      "name": "local",
      "type": "filesystem",
      "priority": 2,
      "paths": ["~/.openclaw/skills", "~/my-skills"]
    }
  ],
  "cache": {
    "enabled": true,
    "ttlHours": 24
  },
  "autoSync": {
    "onProjectEnter": true,
    "onSkillMissing": true
  }
}
```

### 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | string | ❌ | 项目名称（用于显示） |
| `skills` | array | ✅ | 技能列表，支持字符串或对象格式 |
| `excludeGlobal` | boolean | ❌ | `true` 只用项目技能，`false` 项目 + 全局（默认 false） |
| `sources` | array | ❌ | 技能来源列表，按优先级排序 |
| `cache.enabled` | boolean | ❌ | 是否启用缓存（默认 true） |
| `cache.ttlHours` | number | ❌ | 缓存过期时间（小时，默认 24） |
| `autoSync.onProjectEnter` | boolean | ❌ | 进入项目时自动同步（默认 true） |
| `autoSync.onSkillMissing` | boolean | ❌ | 发现缺失技能时自动安装（默认 true） |

### 技能格式

```json
{
  "skills": [
    "weather",                          // 简单格式 - 最新版本的技能
    { "name": "feishu-doc" },           // 对象格式 - 最新版本
    { "name": "stock-analyzer", "version": "1.2.0" }  // 锁定版本
  ]
}
```

### 来源类型

| type | 说明 | 必需字段 | 示例 |
|------|------|----------|------|
| `registry` | 技能市场（clawhub） | - | `{"name":"clawhub","type":"registry"}` |
| `filesystem` | 本地目录 | `paths` | `{"type":"filesystem","paths":["~/.openclaw/skills"]}` |
| `git` | Git 仓库 | `repos` | `{"type":"git","repos":["user/repo"]}` |
| `url` | HTTP 下载 | `baseUrl` | `{"type":"url","baseUrl":"https://..."}` |

---

## 命令接口

### 同步与状态

| 命令 | 说明 |
|------|------|
| `node scripts/sync-project-skills.js` | 同步项目技能 |
| `node scripts/sync-project-skills.js --force` | 强制重新同步 |
| `node scripts/sync-project-skills.js --verbose` | 显示详细信息 |
| `node scripts/validate-config.js` | 验证配置格式 |

### 配置管理

| 命令 | 说明 |
|------|------|
| `node scripts/init-project-config.js` | 交互式创建配置 |

---

## 工作流程

### 项目加载流程

```
1. 检测当前工作目录
   ↓
2. 向上查找最近的 .openclaw-skills.json
   ↓
3. 解析技能列表和来源配置
   ↓
4. 检查每个技能是否已安装
   ↓
5. 缺失技能 → 按源优先级查找并安装
   ↓
6. 激活配置的技能
   ↓
7. 缓存加载状态
```

### 技能安装流程

```
1. 遍历配置的技能列表
   ↓
2. 检查技能是否已安装（多目录检测）
   ↓
3. 未安装 → 按优先级遍历来源
   ↓
4. 找到技能 → 下载/克隆
   ↓
5. 验证技能格式（SKILL.md 必需）
   ↓
6. 安装到本地技能目录
   ↓
7. 更新缓存
```

---

## 脚本工具

### sync-project-skills.js

同步项目技能的主脚本。

```bash
# 基本用法
node scripts/sync-project-skills.js

# 强制重新同步（忽略缓存）
node scripts/sync-project-skills.js --force

# 显示详细信息
node scripts/sync-project-skills.js --verbose

# 组合使用
node scripts/sync-project-skills.js --force --verbose
```

**参数**：
- `--force`, `-f`: 强制重新同步，忽略缓存
- `--verbose`, `-v`: 显示详细信息

### validate-config.js

验证配置文件格式和完整性。

```bash
# 验证当前目录配置
node scripts/validate-config.js

# 验证指定文件
node scripts/validate-config.js path/to/config.json
```

**验证内容**：
- JSON 格式正确性
- 必需字段存在性
- 字段类型正确性
- 来源类型有效性
- 重复技能检测

### init-project-config.js

交互式配置创建向导。

```bash
node scripts/init-project-config.js
```

**引导内容**：
- 项目名称
- 技能列表
- 是否排除全局技能
- 技能来源配置
- 缓存设置
- 自动同步设置

---

## 缓存机制

### 缓存位置

```
~/.openclaw/cache/skills.json
```

### 缓存内容

```json
{
  "skills": {
    "weather": { "installed": true, "timestamp": 1710000000000 },
    "feishu-doc": { "installed": true, "timestamp": 1710000000000 }
  },
  "sources": {
    "clawhub": { "reachable": true, "lastCheck": 1710000000000 }
  },
  "lastSync": 1710000000000
}
```

### 缓存策略

| 场景 | 行为 |
|------|------|
| 缓存有效 | 直接使用，跳过网络请求 |
| 缓存过期 | 重新检查源，更新缓存 |
| `--force` | 忽略缓存，强制重新检查 |
| 缓存损坏 | 自动重建 |

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `Config error` | JSON 格式错误 | 运行 `validate-config.js` 检查 |
| `Skill not found` | 技能在配置源中不存在 | 检查技能名称，确认源配置 |
| `Failed to install` | 安装失败（网络/权限） | 检查网络连接和目录权限 |
| `Cache valid, skipping` | 缓存未过期 | 使用 `--force` 强制刷新 |

---

## 最佳实践

### 1️⃣ 配置最小化

只配置项目真正需要的技能：

```json
{
  "skills": ["feishu-doc", "weather"],
  "excludeGlobal": true
}
```

### 2️⃣ 版本锁定

生产项目锁定技能版本：

```json
{
  "skills": [
    { "name": "feishu-doc", "version": "2.1.0" },
    { "name": "weather", "version": "1.0.3" }
  ]
}
```

### 3️⃣ 本地开发

开发中的技能使用本地源：

```json
{
  "sources": [
    { "name": "local-dev", "type": "filesystem", "paths": ["~/dev/my-skills"], "priority": 1 }
  ]
}
```

### 4️⃣ 团队共享

提交配置到版本控制：

```bash
git add .openclaw-skills.json
git commit -m "Add project skill configuration"
```

---

## 故障排查

### 技能未加载

```bash
# 1. 检查配置文件是否存在
ls .openclaw-skills.json

# 2. 验证配置格式
node scripts/validate-config.js

# 3. 强制同步
node scripts/sync-project-skills.js --force --verbose
```

### 安装失败

```bash
# 1. 检查网络连接
ping clawhub.com

# 2. 检查技能目录权限
ls -la ~/.openclaw/skills/

# 3. 查看详细日志
node scripts/sync-project-skills.js --verbose
```

### 配置错误

```bash
# 验证配置并查看示例
node scripts/validate-config.js
```

---

## 文件位置

| 文件 | 位置 |
|------|------|
| 配置文件 | `项目根目录/.openclaw-skills.json` |
| 缓存文件 | `~/.openclaw/cache/skills.json` |
| 技能目录 | `~/.openclaw/skills/` |
| 日志文件 | `~/.openclaw/logs/skills.log` |

---

## 与其他技能协作

### clawhub

本技能依赖 `clawhub` 技能来安装 registry 源的技能。确保 clawhub 技能已安装。

### skill-creator

创建新技能后，可以用本技能将新技能添加到项目配置中。

---

## 更新历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-03-10 | 初始版本，支持基础配置和多源安装 |

---

## 许可证

MIT License
