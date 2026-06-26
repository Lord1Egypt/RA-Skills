# 热梗百科 Skill 安装指南

本文档介绍如何将 `trending-meme-encyclopedia` Skill 安装到不同的 Agent 产品中。

---

## 快速安装

### 使用安装脚本（推荐）

```bash
# 1. 进入 Skill 目录
cd /path/to/trending-meme-encyclopedia

# 2. 运行安装脚本
./install.sh

# 3. 重启 Claude Code
```

### 手动安装

```bash
# 1. 创建 Claude Code skills 目录
mkdir -p ~/.claude/skills

# 2. 复制 Skill 到该目录
cp -r /path/to/trending-meme-encyclopedia ~/.claude/skills/

# 3. 重启 Claude Code
```

---

## Claude Code 安装方法

### 方法一：全局安装

```bash
# 创建 skills 目录
mkdir -p ~/.claude/skills

# 复制 Skill
cp -r trending-meme-encyclopedia ~/.claude/skills/

# 验证安装
ls ~/.claude/skills/trending-meme-encyclopedia/SKILL.md
```

### 方法二：项目级安装

```bash
# 在项目根目录
mkdir -p your-project/.claude/skills
cp -r trending-meme-encyclopedia your-project/.claude/skills/
```

### 方法三：环境变量配置

```bash
# 设置环境变量
export CLAUDE_SKILLS_PATH="/path/to/your/skills/dir"

# 启动 Claude Code
claude
```

---

## 验证安装

安装完成后，启动 Claude Code 并测试：

```
用户：帮我整理一下今天的热梗
```

或

```
用户：解释一下"科目三"这个梗
```

---

## 常见问题

### Q1: Skill 没有被识别

**检查清单**：
- [ ] SKILL.md 文件存在
- [ ] 目录名与 SKILL.md 中的 `name` 字段一致
- [ ] 目录权限正确

**解决方法**：
```bash
# 检查文件
cat ~/.claude/skills/trending-meme-encyclopedia/SKILL.md

# 检查权限
chmod -R 755 ~/.claude/skills/trending-meme-encyclopedia
```

### Q2: 如何更新 Skill

```bash
# 直接覆盖
cp -rf trending-meme-encyclopedia ~/.claude/skills/

# 重启 Claude Code
```

### Q3: 如何卸载 Skill

```bash
rm -rf ~/.claude/skills/trending-meme-encyclopedia
```

---

## 详细安装说明

### 查找 Skills 目录

```bash
# 查看 Claude Code 配置
claude config get skillsDir

# 或者使用默认位置
# macOS/Linux: ~/.claude/skills
# Windows: %APPDATA%\Claude\skills
```

### 设置 Skills 目录

```bash
# 设置全局 skills 目录
claude config set skillsDir ~/.claude/skills
```

---

## 许可证

MIT License
