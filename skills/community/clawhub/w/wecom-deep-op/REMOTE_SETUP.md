# GitHub 仓库创建与推送指南

## 📦 当前状态

✅ wecom-deep-op skill 已完成:
- 所有源代码（TypeScript + 构建产物）
- 完整文档（40KB）
- 测试框架
- 已提交到本地 Git（workspace master）

⏳ **待完成**: 创建 GitHub 远程仓库并推送

---

## 🚀 快速推送（3步）

### Step 1: 在 GitHub.com 创建仓库

1. 登录 [GitHub.com](https://github.com)
2. 点击右上角 `+` → `New repository`
3. 填写:
   - **Repository name**: `wecom-deep-op`
   - **Description**: `Enterprise WeChat all-in-one OpenClaw skill`
   - **Public** (推荐) 或 Private
   - ❌ **不要**勾选 "Initialize this repository with a README"
   - ❌ 不要添加 .gitignore 或 license（本地已有）
4. 点击 `Create repository`

### Step 2: 本地添加远程并推送

```bash
# 进入项目目录
cd /root/.openclaw/workspace/skills/wecom-deep-op

# 添加远程仓库（替换 YOUR_GITHUB_USERNAME）
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/wecom-deep-op.git

# 推送到 GitHub
git push -u origin master
```

**注意**:
- 如果 `master` 分支不存在，使用 `main` 或 `git push -u origin HEAD`
- 如果是 HTTPS URL，Git 会提示输入 GitHub 用户名和密码（密码改为 Personal Access Token）
- 推荐使用 SSH（需提前配置 SSH 密钥）

### Step 3: 验证

访问: `https://github.com/YOUR_GITHUB_USERNAME/wecom-deep-op`

应看到所有文件和文档。

---

## 🔑 SSH 方式（推荐）

如果已配置 SSH 密钥：

```bash
# 添加远程（SSH URL）
git remote add origin git@github.com:YOUR_GITHUB_USERNAME/wecom-deep-op.git

# 推送（无需密码）
git push -u origin master
```

---

## 📝 后续步骤（推送完成后）

1. **创建 Release 和 Tag**:
```bash
git tag -a v1.0.0 -m "wecom-deep-op v1.0.0"
git push origin v1.0.0
```

2. **在 GitHub 创建 Release**:
   - 前往仓库 → Releases → Draft a new release
   - Tag: `v1.0.0`
   - Title: `v1.0.0 - Enterprise WeChat All-in-One Skill`
   - 复制 CHANGELOG.md 内容
   - Publish

3. **发布到 Clawhub**:
```bash
# 安装 Clawhub CLI（如果还没有）
npm install -g @clawhub/cli

# 登录
clawhub login
# 输入 API Token（从 https://clawhub.com/settings/tokens）

# dry-run 检查
clawhub publish . --dry-run

# 正式发布
clawhub publish . --tag latest
clawhub publish . --tag v1.0.0
```

4. **验证发布**:
```bash
clawhub info wecom-deep-op
clawhub versions wecom-deep-op
```

访问: https://clawhub.com/skills/wecom-deep-op

---

## 🆘 故障排除

| 问题 | 解决方案 |
|------|----------|
| `remote origin already exists` | `git remote set-url origin https://github.com/...` |
| `Authentication failed` | 使用 Personal Access Token 而非密码（SSH 更佳） |
| `branch 'master' doesn't exist` | 使用 `git push -u origin HEAD` 或检查分支名 |
| `permission denied` | 确认有仓库写入权限，SSH 密钥已添加到 GitHub |

---

## 📞 需要帮助？

查看项目内完整发布指南: `PUBLISHING.md`
