# Project Skills - Quick Reference

## 快速开始

### 1. 创建项目配置

在项目根目录创建 `.openclaw-skills.json`：

```bash
# 使用模板
node scripts/validate-config.js --init
```

### 2. 最小配置

```json
{
  "skills": ["feishu-doc", "weather"],
  "excludeGlobal": true
}
```

### 3. 同步技能

```bash
# 进入项目后自动同步
cd my-project

# 或手动同步
node scripts/sync-project-skills.js
```

---

## 常用命令

| 命令 | 说明 |
|------|------|
| `/skills status` | 查看当前状态 |
| `/skills sync` | 同步项目技能 |
| `/skills add <name>` | 添加技能 |
| `/skills remove <name>` | 移除技能 |
| `/skills list` | 列出已安装技能 |

---

## 配置模板

### 基础模板

```json
{
  "skills": ["feishu-doc"],
  "excludeGlobal": false
}
```

### 完整模板

```json
{
  "name": "my-project",
  "skills": [
    { "name": "feishu-doc", "version": "latest" }
  ],
  "excludeGlobal": true,
  "sources": [
    { "name": "clawhub", "type": "registry", priority: 1 }
  ],
  "cache": { "enabled": true, "ttlHours": 24 },
  "autoSync": { "onProjectEnter": true }
}
```

### 多源配置

```json
{
  "skills": ["my-custom-skill"],
  "sources": [
    { "name": "clawhub", "type": "registry", priority: 1 },
    { "name": "local", "type": "filesystem", paths: ["~/dev/skills"], priority: 2 },
    { "name": "github", "type": "git", repos: ["user/repo"], priority: 3 }
  ]
}
```

---

## 故障排查

### 技能未加载

```bash
# 检查配置
node scripts/validate-config.js

# 强制同步
node scripts/sync-project-skills.js --force

# 查看详细日志
node scripts/sync-project-skills.js --verbose
```

### 安装失败

```bash
# 测试 clawhub 连接
clawhub status

# 检查技能目录权限
ls -la ~/.openclaw/skills/
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

## 最佳实践

1. **提交配置**：将 `.openclaw-skills.json` 提交到版本控制
2. **锁定版本**：生产环境使用具体版本号
3. **最小化技能**：只配置项目需要的技能
4. **本地开发**：使用 local 源测试开发中的技能
