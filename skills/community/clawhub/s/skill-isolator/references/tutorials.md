# 实战教程 - SkillIsolator

通过实际案例学习如何使用技能隔离系统。

---

## 📚 教程目录

1. [教程 1：5 分钟快速开始](#教程 15 分钟快速开始)
2. [教程 2：为现有项目添加技能配置](#教程 2 为现有项目添加技能配置)
3. [教程 3：多项目管理](#教程 3 多项目管理)
4. [教程 4：团队技能共享](#教程 4 团队技能共享)
5. [教程 5：开发自定义技能](#教程 5 开发自定义技能)

---

## 教程 1：5 分钟快速开始

**目标**：为新项目创建技能配置

**时间**：5 分钟

### 步骤

#### 1. 创建项目目录

```bash
mkdir my-first-project
cd my-first-project
```

#### 2. 运行配置向导

```bash
node /path/to/project-skills/scripts/init-project-config.js
```

**交互示例**：
```
🚀 Project Skills Configuration Wizard

Project name [my-first-project]: my-first-project
Enter skills to enable (comma-separated): weather, feishu-doc
Exclude global skills? [Y]: Y
Enable clawhub (registry)? [Y]: Y
Enable local filesystem? [Y]: Y
Enable GitHub (git)? [N]: N
Enable caching? [Y]: Y
Cache TTL (hours) [24]: 24
Enable auto-sync on project enter? [Y]: Y
```

#### 3. 查看生成的配置

```bash
cat .openclaw-skills.json
```

**输出**：
```json
{
  "name": "my-first-project",
  "skills": ["weather", "feishu-doc"],
  "excludeGlobal": true,
  "sources": [
    { "name": "clawhub", "type": "registry", "priority": 1 },
    { "name": "local", "type": "filesystem", "priority": 2, "paths": ["~/.openclaw/skills"] }
  ],
  "cache": { "enabled": true, "ttlHours": 24 },
  "autoSync": { "onProjectEnter": true, "onSkillMissing": true }
}
```

#### 4. 同步技能

```bash
node /path/to/project-skills/scripts/sync-project-skills.js
```

**输出**：
```
📁 Project root: /home/user/my-first-project
🔧 Project: my-first-project
📦 Skills: 2 configured

🔄 Syncing skills...
📦 Installing weather from clawhub...
✅ Installed weather
📦 Installing feishu-doc from clawhub...
✅ Installed feishu-doc

============================================================
✅ Installed: 2
```

#### 5. 验证配置

```bash
node /path/to/project-skills/scripts/validate-config.js
```

**完成！** ✅ 你现在有了第一个技能隔离配置的项目。

---

## 教程 2：为现有项目添加技能配置

**目标**：为已有项目添加技能管理

**时间**：10 分钟

### 场景

你有一个现有的前端项目，想添加技能配置。

### 步骤

#### 1. 进入项目目录

```bash
cd ~/projects/existing-frontend
```

#### 2. 创建配置文件

```bash
cat > .openclaw-skills.json << 'EOF'
{
  "name": "existing-frontend",
  "skills": [
    "javascript-helper",
    "react-tools",
    "css-formatter"
  ],
  "excludeGlobal": false,
  "sources": [
    { "name": "clawhub", "type": "registry", "priority": 1 }
  ]
}
EOF
```

#### 3. 验证配置

```bash
node /path/to/project-skills/scripts/validate-config.js
```

#### 4. 同步技能

```bash
node /path/to/project-skills/scripts/sync-project-skills.js --force
```

#### 5. 提交到版本控制

```bash
git add .openclaw-skills.json
git commit -m "Add skill configuration for frontend development"
git push
```

**完成！** ✅ 现有项目现在有了技能配置。

---

## 教程 3：多项目管理

**目标**：管理多个项目的不同技能配置

**时间**：15 分钟

### 场景

你有 3 个项目，每个需要不同的技能：

1. **project-a** (前端) - JavaScript, React
2. **project-b** (数据分析) - Python, Pandas
3. **project-c** (文档) - 飞书文档，翻译

### 步骤

#### 1. 创建项目 A 配置

```bash
cd ~/projects/project-a
cat > .openclaw-skills.json << 'EOF'
{
  "name": "project-a-frontend",
  "skills": ["javascript-helper", "react-tools"],
  "excludeGlobal": true
}
EOF
node /path/to/sync-project-skills.js
```

#### 2. 创建项目 B 配置

```bash
cd ~/projects/project-b
cat > .openclaw-skills.json << 'EOF'
{
  "name": "project-b-data",
  "skills": ["python-helper", "pandas-tools"],
  "excludeGlobal": true
}
EOF
node /path/to/sync-project-skills.js
```

#### 3. 创建项目 C 配置

```bash
cd ~/projects/project-c
cat > .openclaw-skills.json << 'EOF'
{
  "name": "project-c-docs",
  "skills": ["feishu-doc", "translator"],
  "excludeGlobal": false
}
EOF
node /path/to/sync-project-skills.js
```

#### 4. 验证隔离效果

```bash
# 在项目 A 中
cd ~/projects/project-a
node /path/to/sync-project-skills.js
# 显示：javascript-helper, react-tools

# 切换到项目 B
cd ~/projects/project-b
node /path/to/sync-project-skills.js
# 显示：python-helper, pandas-tools

# 切换到项目 C
cd ~/projects/project-c
node /path/to/sync-project-skills.js
# 显示：feishu-doc, translator
```

#### 5. （可选）创建批量管理脚本

```bash
cat > ~/bin/update-all-skills.sh << 'EOF'
#!/bin/bash
for project in ~/projects/*; do
  if [ -f "$project/.openclaw-skills.json" ]; then
    echo "=== Updating $project ==="
    cd "$project"
    node /path/to/sync-project-skills.js --force
  fi
done
EOF
chmod +x ~/bin/update-all-skills.sh
```

**完成！** ✅ 你现在可以同时管理多个项目的技能配置。

---

## 教程 4：团队技能共享

**目标**：为团队创建共享技能配置

**时间**：30 分钟

### 场景

你的团队有 5 个开发者，希望所有项目使用一致的技能配置。

### 步骤

#### 1. 创建团队技能仓库

在 GitHub 创建仓库：`team-name/shared-skills`

```bash
# 本地克隆
cd ~/dev
git clone git@github.com:team-name/shared-skills.git
cd shared-skills
```

#### 2. 添加团队标准配置

```bash
cat > frontend-standard.json << 'EOF'
{
  "name": "team-frontend-standard",
  "skills": [
    "javascript-helper",
    "react-tools",
    "eslint-helper",
    "prettier-formatter"
  ],
  "excludeGlobal": false,
  "sources": [
    { "name": "clawhub", "type": "registry", "priority": 1 }
  ]
}
EOF

cat > backend-standard.json << 'EOF'
{
  "name": "team-backend-standard",
  "skills": [
    "python-helper",
    "api-tester",
    "database-helper"
  ],
  "excludeGlobal": false
}
EOF
```

#### 3. 提交到仓库

```bash
git add *.json
git commit -m "Add team standard skill configurations"
git push
```

#### 4. 在项目中引用团队配置

```bash
cd ~/projects/team-project

# 复制团队标准配置
curl -O https://raw.githubusercontent.com/team-name/shared-skills/main/frontend-standard.json
cp frontend-standard.json .openclaw-skills.json

# 同步技能
node /path/to/sync-project-skills.js
```

#### 5. （可选）创建配置生成器

```bash
cat > init-team-project.sh << 'EOF'
#!/bin/bash
PROJECT_TYPE=$1

if [ "$PROJECT_TYPE" = "frontend" ]; then
  curl -O https://raw.githubusercontent.com/team-name/shared-skills/main/frontend-standard.json
  cp frontend-standard.json .openclaw-skills.json
elif [ "$PROJECT_TYPE" = "backend" ]; then
  curl -O https://raw.githubusercontent.com/team-name/shared-skills/main/backend-standard.json
  cp backend-standard.json .openclaw-skills.json
else
  echo "Usage: $0 <frontend|backend>"
  exit 1
fi

node /path/to/sync-project-skills.js
echo "✅ Project initialized with team standard skills"
EOF
```

**完成！** ✅ 你的团队现在有统一的技能配置标准。

---

## 教程 5：开发自定义技能

**目标**：创建并发布自己的技能

**时间**：45 分钟

### 场景

你想创建一个自定义技能，为团队提供特定功能。

### 步骤

#### 1. 创建技能目录

```bash
mkdir -p ~/.openclaw/workspace/skills/team-helper
cd ~/.openclaw/workspace/skills/team-helper
```

#### 2. 创建 SKILL.md

```bash
cat > SKILL.md << 'EOF'
---
name: team-helper
description: Team-specific helper skill with custom workflows and tools.
---

# Team Helper Skill

为团队定制的技能，提供特定工作流支持。

## 功能

- 代码审查检查清单
- 部署流程自动化
- 团队规范检查

## 使用方法

在聊天中使用：
- `/review` - 启动代码审查
- `/deploy` - 启动部署流程
- `/check-style` - 检查代码风格

## 相关文件

- 团队规范：references/team-standards.md
- 部署脚本：scripts/deploy.sh
EOF
```

#### 3. 创建参考文档

```bash
mkdir references
cat > references/team-standards.md << 'EOF'
# 团队开发规范

## 代码风格

- 使用 2 空格缩进
- 函数名使用驼峰命名
- 常量使用大写 + 下划线

## 提交规范

格式：`type(scope): message`

示例：
- `feat(auth): add login functionality`
- `fix(api): resolve timeout issue`
- `docs(readme): update installation steps`
EOF
```

#### 4. 创建脚本（可选）

```bash
mkdir scripts
cat > scripts/deploy.sh << 'EOF'
#!/bin/bash
# 团队标准部署脚本

echo "🚀 Starting deployment..."
echo "📦 Building..."
npm run build
echo "✅ Deployment complete"
EOF
chmod +x scripts/deploy.sh
```

#### 5. 测试技能

```bash
# 创建测试项目
mkdir ~/test-team-skill
cd ~/test-team-skill

# 创建配置，使用本地技能
cat > .openclaw-skills.json << 'EOF'
{
  "skills": ["team-helper"],
  "sources": [
    {
      "name": "local",
      "type": "filesystem",
      "paths": ["~/.openclaw/workspace/skills"]
    }
  ]
}
EOF

# 同步
node /path/to/sync-project-skills.js
```

#### 6. 发布到 clawhub（可选）

```bash
# 登录 clawhub
clawhub login

# 发布技能
clawhub publish ~/.openclaw/workspace/skills/team-helper \
  --changelog "Initial release - Team helper skill"
```

**完成！** ✅ 你创建了自己的第一个自定义技能。

---

## 总结

通过这些教程，你学会了：

- ✅ 为新项目创建技能配置
- ✅ 为现有项目添加技能管理
- ✅ 管理多个项目的不同技能
- ✅ 创建团队共享配置
- ✅ 开发自定义技能

### 下一步

- 阅读 [usage-guide.md](./usage-guide.md) 了解更多高级用法
- 查看 [faq.md](./faq.md) 解决常见问题
- 参考 [example-config.json](./example-config.json) 获取配置模板

---

## 相关资源

- [SKILL.md](../SKILL.md) - 技能完整文档
- [usage-guide.md](./usage-guide.md) - 使用指南
- [faq.md](./faq.md) - 常见问题
- [quick-reference.md](./quick-reference.md) - 快速参考
