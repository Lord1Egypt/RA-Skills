# 使用指南 - SkillIsolator

详细的使用教程和实际案例。

---

## 📖 目录

1. [快速入门](#快速入门)
2. [配置详解](#配置详解)
3. [命令行参考](#命令行参考)
4. [实际用例](#实际用例)
5. [最佳实践](#最佳实践)
6. [故障排查](#故障排查)

---

## 快速入门

### 场景 1：新项目从零开始

```bash
# 1. 进入项目目录
cd my-new-project

# 2. 运行配置向导
node /path/to/project-skills/scripts/init-project-config.js

# 3. 同步技能
node /path/to/project-skills/scripts/sync-project-skills.js
```

### 场景 2：为现有项目添加配置

```bash
# 1. 在项目根目录创建配置文件
cat > .openclaw-skills.json << 'EOF'
{
  "skills": ["weather", "feishu-doc"],
  "excludeGlobal": true
}
EOF

# 2. 验证配置
node /path/to/project-skills/scripts/validate-config.js

# 3. 安装技能
node /path/to/project-skills/scripts/sync-project-skills.js --force
```

### 场景 3：切换到不同项目

```bash
# 项目 A - 使用文档和天气技能
cd ~/projects/project-a
# 自动加载 project-a/.openclaw-skills.json

# 项目 B - 使用金融分析技能
cd ~/projects/project-b
# 自动加载 project-b/.openclaw-skills.json
```

---

## 配置详解

### 基础配置

最简单的配置，只指定技能列表：

```json
{
  "skills": ["weather", "feishu-doc"]
}
```

**说明**：
- 默认 `excludeGlobal: false`（项目技能 + 全局技能）
- 默认从 clawhub 安装
- 默认启用缓存（24 小时）

### 进阶配置

完整配置示例：

```json
{
  "name": "finance-dashboard",
  "skills": [
    { "name": "stock-analyzer", "version": "1.2.0" },
    { "name": "tvscreener", "version": "latest" },
    { "name": "finance-news-analyzer" }
  ],
  "excludeGlobal": true,
  "sources": [
    {
      "name": "local",
      "type": "filesystem",
      "priority": 1,
      "paths": ["~/dev/my-skills"]
    },
    {
      "name": "clawhub",
      "type": "registry",
      "priority": 2
    }
  ],
  "cache": {
    "enabled": true,
    "ttlHours": 12
  },
  "autoSync": {
    "onProjectEnter": true,
    "onSkillMissing": true
  }
}
```

### 配置字段说明

#### `skills` - 技能列表

支持两种格式：

```json
{
  "skills": [
    // 格式 1：简单字符串（默认最新版本）
    "weather",
    "feishu-doc",
    
    // 格式 2：对象（可指定版本）
    { "name": "stock-analyzer", "version": "1.2.0" },
    { "name": "tvscreener", "version": "latest" }
  ]
}
```

**版本策略**：
- `"latest"` - 总是使用最新版本
- `"1.2.0"` - 锁定特定版本
- 省略 - 默认为 `"latest"`

#### `excludeGlobal` - 排除全局技能

```json
{
  "excludeGlobal": true  // 只使用项目配置的技能
}
```

```json
{
  "excludeGlobal": false  // 使用项目技能 + 全局技能（默认）
}
```

**使用建议**：
- `true` - 生产项目、需要严格隔离的项目
- `false` - 开发项目、需要额外工具的项目

#### `sources` - 技能来源

按优先级排序，从上到下查找：

```json
{
  "sources": [
    {
      "name": "local-dev",
      "type": "filesystem",
      "priority": 1,
      "paths": ["~/dev/my-skills"]
    },
    {
      "name": "clawhub",
      "type": "registry",
      "priority": 2
    },
    {
      "name": "team-shared",
      "type": "git",
      "priority": 3,
      "repos": ["github.com/team/skills"],
      "branch": "main"
    }
  ]
}
```

**来源类型**：

| 类型 | 说明 | 必需字段 | 使用场景 |
|------|------|----------|----------|
| `registry` | 技能市场 | - | clawhub 官方技能 |
| `filesystem` | 本地目录 | `paths` | 开发中技能、私有技能 |
| `git` | Git 仓库 | `repos` | 团队共享技能 |
| `url` | HTTP 下载 | `baseUrl` | 静态托管技能 |

#### `cache` - 缓存配置

```json
{
  "cache": {
    "enabled": true,      // 是否启用缓存
    "ttlHours": 24        // 缓存过期时间（小时）
  }
}
```

**缓存策略**：
- 缓存有效期内：跳过网络请求，直接使用缓存
- 缓存过期：重新检查源，更新缓存
- `--force`：忽略缓存，强制刷新

#### `autoSync` - 自动同步

```json
{
  "autoSync": {
    "onProjectEnter": true,    // 进入项目时自动同步
    "onSkillMissing": true     // 发现缺失技能时自动安装
  }
}
```

---

## 命令行参考

### sync-project-skills.js

同步项目技能。

```bash
# 基本用法
node scripts/sync-project-skills.js

# 强制重新同步（忽略缓存）
node scripts/sync-project-skills.js --force

# 显示详细信息
node scripts/sync-project-skills.js --verbose

# 组合使用
node scripts/sync-project-skills.js --force --verbose

# 简写
node scripts/sync-project-skills.js -f -v
```

**参数**：
- `--force`, `-f`: 强制重新同步
- `--verbose`, `-v`: 显示详细信息
- `--help`, `-h`: 显示帮助

**输出示例**：
```
📁 Project root: /home/user/my-project
📄 Config: /home/user/my-project/.openclaw-skills.json

🔧 Project: my-project
📦 Skills: 3 configured
🌐 Exclude Global: Yes

🔄 Syncing skills...
✅ weather (already installed)
📦 Installing feishu-doc from clawhub...
✅ Installed feishu-doc
✅ stock-analyzer (already installed)

============================================================
✅ Installed: 3
```

### validate-config.js

验证配置文件格式。

```bash
# 验证当前目录配置
node scripts/validate-config.js

# 验证指定文件
node scripts/validate-config.js path/to/config.json

# 验证并显示示例
node scripts/validate-config.js invalid-config.json
```

**输出示例**：
```
🔍 Validating: .openclaw-skills.json

✅ Configuration is valid!
```

或错误时：
```
🔍 Validating: .openclaw-skills.json

❌ Errors:
   - skills: must be an array
   - sources[0]: missing required field "type"

📖 Example config:
{
  "name": "my-project",
  "skills": ["weather"],
  ...
}
```

### init-project-config.js

交互式创建配置。

```bash
node scripts/init-project-config.js
```

**交互流程**：
```
🚀 Project Skills Configuration Wizard

This will create a .openclaw-skills.json file in the current directory.

Project name [my-project]: 
Enter skills to enable (comma-separated): weather, feishu-doc
Exclude global skills? [Y]: 
Enable clawhub (registry)? [Y]: 
Enable local filesystem? [Y]: 
Enable GitHub (git)? [N]: 
Enable caching? [Y]: 
Cache TTL (hours) [24]: 
Enable auto-sync on project enter? [Y]: 

✅ Configuration created!
```

---

## 实际用例

### 用例 1：前端开发项目

```json
{
  "name": "frontend-app",
  "skills": [
    "javascript-helper",
    "react-tools",
    "css-formatter"
  ],
  "sources": [
    { "name": "clawhub", "type": "registry", "priority": 1 }
  ]
}
```

### 用例 2：数据分析项目

```json
{
  "name": "data-analysis",
  "skills": [
    { "name": "python-helper", "version": "2.0.0" },
    { "name": "pandas-tools" },
    { "name": "chart-generator" }
  ],
  "excludeGlobal": true
}
```

### 用例 3：多语言团队项目

```json
{
  "name": "team-project",
  "skills": [
    "translator",
    "code-reviewer",
    "documentation-helper"
  ],
  "sources": [
    {
      "name": "team-skills",
      "type": "git",
      "priority": 1,
      "repos": ["github.com/team/shared-skills"],
      "branch": "main"
    },
    { "name": "clawhub", "type": "registry", "priority": 2 }
  ]
}
```

### 用例 4：开发中技能测试

```json
{
  "name": "skill-development",
  "skills": [
    "my-new-skill",
    "test-helper"
  ],
  "sources": [
    {
      "name": "local-dev",
      "type": "filesystem",
      "priority": 1,
      "paths": ["~/dev/my-skills"]
    }
  ],
  "cache": {
    "enabled": false
  }
}
```

### 用例 5：临时项目（最小配置）

```json
{
  "skills": ["weather"]
}
```

---

## 最佳实践

### 1. 版本锁定

生产项目锁定技能版本，避免意外更新：

```json
{
  "skills": [
    { "name": "feishu-doc", "version": "2.1.0" },
    { "name": "weather", "version": "1.0.3" }
  ]
}
```

### 2. 配置最小化

只配置项目真正需要的技能：

```json
{
  "skills": ["feishu-doc", "weather"],
  "excludeGlobal": true
}
```

### 3. 本地开发优先

开发中的技能使用本地源：

```json
{
  "sources": [
    {
      "name": "local-dev",
      "type": "filesystem",
      "paths": ["~/dev/my-skills"],
      "priority": 1
    }
  ]
}
```

### 4. 团队共享配置

提交配置到版本控制：

```bash
git add .openclaw-skills.json
git commit -m "Add project skill configuration"
```

### 5. 定期更新

定期检查和更新技能：

```bash
# 每月一次强制同步
node scripts/sync-project-skills.js --force --verbose
```

### 6. 配置模板

为常用项目类型创建模板：

```bash
# frontend-template.json
{
  "skills": ["javascript-helper", "react-tools"],
  "excludeGlobal": true
}

# 使用时复制
cp ~/templates/frontend-template.json .openclaw-skills.json
```

---

## 故障排查

### 问题 1：技能未加载

**症状**：进入项目后技能未生效

**排查步骤**：
```bash
# 1. 检查配置文件是否存在
ls -la .openclaw-skills.json

# 2. 验证配置格式
node scripts/validate-config.js

# 3. 查看已安装技能
node scripts/sync-project-skills.js --verbose

# 4. 强制同步
node scripts/sync-project-skills.js --force
```

### 问题 2：安装失败

**症状**：`Failed to install <skill-name>`

**可能原因**：
- 技能名称错误
- 网络连接问题
- 权限不足

**解决方案**：
```bash
# 1. 检查技能名称（在 clawhub 搜索）
clawhub search <skill-name>

# 2. 检查网络连接
ping clawhub.com

# 3. 检查技能目录权限
ls -la ~/.openclaw/skills/

# 4. 查看详细日志
cat ~/.openclaw/logs/skills.log
```

### 问题 3：配置错误

**症状**：`Config error: ...`

**解决方案**：
```bash
# 运行验证工具
node scripts/validate-config.js

# 根据错误提示修复配置
# 参考示例配置
cat references/example-config.json
```

### 问题 4：缓存问题

**症状**：配置已更新但技能未同步

**解决方案**：
```bash
# 强制刷新缓存
node scripts/sync-project-skills.js --force

# 或手动删除缓存
rm ~/.openclaw/cache/skills.json
```

### 问题 5：多项目冲突

**症状**：切换项目后技能混乱

**解决方案**：
```bash
# 确保每个项目有独立的配置
cd project-a && ls .openclaw-skills.json
cd project-b && ls .openclaw-skills.json

# 检查 excludeGlobal 设置
# 如果需要严格隔离，设置 excludeGlobal: true
```

---

## 常见问题 FAQ

### Q: 可以在不同项目使用同一技能的不同版本吗？

A: 目前不支持同时激活多个版本。切换项目时会使用该项目配置的版本。

### Q: 配置文件可以放在子目录吗？

A: 可以。系统会向上查找最近的 `.openclaw-skills.json`。

### Q: 如何禁用自动同步？

A: 设置 `autoSync.onProjectEnter: false`。

### Q: 支持哪些技能来源？

A: 支持 registry (clawhub)、filesystem (本地)、git (仓库)、url (HTTP)。

### Q: 如何查看技能安装日志？

A: 查看 `~/.openclaw/logs/skills.log`。

---

## 相关资源

- [SKILL.md](../SKILL.md) - 技能完整文档
- [quick-reference.md](./quick-reference.md) - 快速参考
- [example-config.json](./example-config.json) - 配置示例
