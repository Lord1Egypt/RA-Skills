# 常见问题解答 (FAQ)

关于 SkillIsolator 的常见问题和解答。

---

## 📋 目录

1. [基础概念](#基础概念)
2. [配置相关](#配置相关)
3. [技能安装](#技能安装)
4. [故障排查](#故障排查)
5. [高级用法](#高级用法)

---

## 基础概念

### Q1: 什么是技能隔离？

**A**: 技能隔离是指每个项目可以有自己独立的技能配置，互不干扰。

**示例**：
- 项目 A 使用 `weather` + `feishu-doc`
- 项目 B 使用 `stock-analyzer` + `tvscreener`
- 切换项目时自动切换技能集

### Q2: 为什么需要技能隔离？

**A**: 
1. **减少上下文污染** - 只加载项目需要的技能
2. **避免技能冲突** - 不同项目可能需要不同配置
3. **提高加载速度** - 技能越少，加载越快
4. **版本管理** - 不同项目可以使用不同版本

### Q3: 项目配置和全局配置有什么区别？

**A**:
| 类型 | 位置 | 作用范围 | 优先级 |
|------|------|----------|--------|
| 项目配置 | `项目/.openclaw-skills.json` | 仅当前项目 | 高 |
| 全局配置 | `~/.openclaw/config.yaml` | 所有项目 | 低 |

### Q4: `excludeGlobal` 是什么意思？

**A**: 控制是否使用全局技能。

```json
{
  "excludeGlobal": true   // 只用项目配置的技能
}
```

```json
{
  "excludeGlobal": false  // 项目技能 + 全局技能（默认）
}
```

**使用建议**：
- `true` - 生产环境、严格隔离
- `false` - 开发环境、需要额外工具

---

## 配置相关

### Q5: 配置文件必须放在项目根目录吗？

**A**: 不一定。系统会向上查找最近的 `.openclaw-skills.json`。

**查找规则**：
```
当前目录 → 父目录 → 祖父目录 → ... → 最多 10 层
```

**示例**：
```
my-project/
├── .openclaw-skills.json  ← 放在这里
├── src/
│   ├── component1/
│   └── component2/        ← 在这些子目录也有效
```

### Q6: 配置文件格式错误会怎样？

**A**: 系统会提示错误信息，并回退到全局技能配置。

**错误示例**：
```
❌ Config error: Missing or invalid "skills" array
   Please check the config file format.
```

**解决方案**：
```bash
node scripts/validate-config.js
```

### Q7: 可以动态修改配置吗？

**A**: 可以。修改 `.openclaw-skills.json` 后运行同步即可。

```bash
# 修改配置
vim .openclaw-skills.json

# 重新同步
node scripts/sync-project-skills.js --force
```

### Q8: 配置文件需要提交到 Git 吗？

**A**: **建议提交**。

**好处**：
- 团队成员使用一致的技能配置
- 新人快速上手项目
- 配置版本可追溯

```bash
git add .openclaw-skills.json
git commit -m "Add project skill configuration"
```

---

## 技能安装

### Q9: 技能安装在哪里？

**A**: 默认安装在以下目录（按优先级）：

1. `~/.openclaw/skills/`
2. `~/.openclaw/workspace/skills/`

### Q10: 如何查看已安装的技能？

**A**:
```bash
# 方法 1：查看技能目录
ls ~/.openclaw/skills/

# 方法 2：运行同步脚本（会显示已安装状态）
node scripts/sync-project-skills.js --verbose
```

### Q11: 技能安装失败怎么办？

**A**: 常见原因和解决方案：

**原因 1：技能名称错误**
```bash
# 检查技能名称
clawhub search <skill-name>
```

**原因 2：网络连接问题**
```bash
# 检查网络
ping clawhub.com
```

**原因 3：权限不足**
```bash
# 检查目录权限
ls -la ~/.openclaw/skills/

# 修复权限（Windows）
icacls ~/.openclaw/skills /grant Users:F
```

**原因 4：技能被标记为可疑**
```bash
# 使用 --force 强制安装
clawhub install <skill-name> --force
```

### Q12: 如何卸载技能？

**A**:
```bash
# 方法 1：从配置中移除
# 编辑 .openclaw-skills.json，删除对应技能

# 方法 2：手动删除
rm -rf ~/.openclaw/skills/<skill-name>
```

### Q13: 支持哪些技能来源？

**A**:

| 来源类型 | 说明 | 状态 |
|----------|------|------|
| `registry` | clawhub 官方市场 | ✅ 已实现 |
| `filesystem` | 本地目录 | ✅ 已实现 |
| `git` | Git 仓库 | ⏳ 计划中 |
| `url` | HTTP 下载 | ⏳ 计划中 |

---

## 故障排查

### Q14: 技能未加载怎么办？

**A**: 按顺序排查：

```bash
# 1. 检查配置文件是否存在
ls .openclaw-skills.json

# 2. 验证配置格式
node scripts/validate-config.js

# 3. 查看技能状态
node scripts/sync-project-skills.js --verbose

# 4. 强制同步
node scripts/sync-project-skills.js --force

# 5. 查看日志
cat ~/.openclaw/logs/skills.log
```

### Q15: 缓存失效怎么办？

**A**:
```bash
# 方法 1：强制刷新
node scripts/sync-project-skills.js --force

# 方法 2：删除缓存文件
rm ~/.openclaw/cache/skills.json

# 方法 3：修改配置 TTL
{
  "cache": {
    "enabled": true,
    "ttlHours": 1  // 缩短缓存时间
  }
}
```

### Q16: 切换项目后技能未更新？

**A**: 可能是缓存问题。

```bash
# 强制刷新
node scripts/sync-project-skills.js --force

# 或重启会话
# 重新进入项目目录
```

### Q17: 如何查看详细日志？

**A**:
```bash
# 使用 verbose 模式
node scripts/sync-project-skills.js --verbose

# 查看日志文件
cat ~/.openclaw/logs/skills.log

# 实时查看日志
tail -f ~/.openclaw/logs/skills.log
```

---

## 高级用法

### Q18: 如何为团队创建共享配置？

**A**:

**步骤 1**：创建团队技能仓库
```bash
# GitHub 创建仓库：team-skills
# 将团队技能放入仓库
```

**步骤 2**：配置项目使用团队源
```json
{
  "sources": [
    {
      "name": "team-skills",
      "type": "git",
      "priority": 1,
      "repos": ["github.com/team/skills"],
      "branch": "main"
    },
    { "name": "clawhub", "type": "registry", "priority": 2 }
  ]
}
```

**步骤 3**：提交配置到项目
```bash
git add .openclaw-skills.json
git commit -m "Use team skill configuration"
```

### Q19: 如何开发自己的技能？

**A**:

**步骤 1**：创建技能目录
```bash
mkdir -p ~/.openclaw/workspace/skills/my-skill
cd ~/.openclaw/workspace/skills/my-skill
```

**步骤 2**：创建 SKILL.md
```markdown
---
name: my-skill
description: My custom skill
---

# My Skill

Skill content here...
```

**步骤 3**：配置项目使用本地技能
```json
{
  "skills": ["my-skill"],
  "sources": [
    {
      "name": "local",
      "type": "filesystem",
      "paths": ["~/.openclaw/workspace/skills"]
    }
  ]
}
```

### Q20: 如何为不同环境配置不同技能？

**A**: 使用不同的配置文件。

**开发环境**：
```bash
# .openclaw-skills.dev.json
{
  "skills": ["debugger", "test-helper", "linter"],
  "excludeGlobal": false
}
```

**生产环境**：
```bash
# .openclaw-skills.prod.json
{
  "skills": ["monitor", "logger"],
  "excludeGlobal": true
}
```

**切换方式**：
```bash
# 开发环境
cp .openclaw-skills.dev.json .openclaw-skills.json

# 生产环境
cp .openclaw-skills.prod.json .openclaw-skills.json
```

### Q21: 如何批量管理多个项目的技能？

**A**: 使用脚本批量操作。

**示例脚本**：
```bash
#!/bin/bash
# update-all-projects.sh

for project in ~/projects/*; do
  if [ -f "$project/.openclaw-skills.json" ]; then
    echo "Updating $project..."
    cd "$project"
    node /path/to/sync-project-skills.js --force
  fi
done
```

### Q22: 支持技能版本回滚吗？

**A**: 支持。修改配置中的版本号即可。

```json
{
  "skills": [
    { "name": "weather", "version": "1.0.3" }  // 指定旧版本
  ]
}
```

然后重新同步：
```bash
node scripts/sync-project-skills.js --force
```

---

## 其他问题

### Q23: 技能会占用多少磁盘空间？

**A**: 每个技能约 10-100KB，10 个技能约 1MB。

### Q24: 技能更新会影响正在运行的会话吗？

**A**: 不会。技能更新后需要重新加载会话或重新进入项目。

### Q25: 如何报告 Bug 或提出建议？

**A**: 
- GitHub Issues: https://github.com/openclaw/skills/issues
- Discord: https://discord.com/invite/clawd

---

## 相关资源

- [SKILL.md](../SKILL.md) - 技能完整文档
- [usage-guide.md](./usage-guide.md) - 使用指南
- [quick-reference.md](./quick-reference.md) - 快速参考
