# 发布到 ClawHub 指南

## 当前状态

✅ Skill 文件已创建完成
- SKILL.md
- README.md  
- templates/
- scripts/
- examples/
- docs/
- package.json

## 发布步骤

### 1. 登录 ClawHub

```bash
clawhub login
```

这会打开浏览器进行登录认证。

### 2. 发布 Skill

```bash
cd ~/.openclaw/extensions/qa-reviewer
clawhub publish . \
  --slug qa-reviewer \
  --name "QA Reviewer" \
  --version 1.0.0 \
  --tags "qa,testing,code-review,quality-assurance" \
  --changelog "Initial release based on SRM project experience"
```

### 3. 验证发布

```bash
# 检查发布状态
clawhub inspect qa-reviewer

# 搜索确认
clawhub search qa-reviewer
```

## 更新流程

### 更新内容后

```bash
# 更新版本
# 修改 package.json version

# 发布更新
clawhub publish . --version 1.0.1 --changelog "Updated templates and scripts"
```

## 安装验证

其他用户安装后：

```bash
# 安装
clawhub install qa-reviewer

# 使用
~/.openclaw/extensions/qa-reviewer/scripts/code_review.sh
```

---

*创建时间：2026-03-04*
