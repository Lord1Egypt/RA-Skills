# 发布指南（Publishing Guide）

> 适用：clawhub-daily v1.0.0+ 维护者

> **⚠️ 维护者文档说明**：本文档面向技能维护者，指导如何发布新版本到 GitHub/ClawHub/SkillHub。
> 文档中提到的 `GH_TOKEN` 仅用于维护者发布新版本时调用 GitHub API，**技能运行时不读取 GH_TOKEN**。
> 技能运行时的凭证和行为详见 SKILL.md 的"数据出口说明"和"权限声明"章节。

## 🎯 发布目标

clawhub-daily 同时发布到 **GitHub** 和 **ClawHub** 两个平台：
- **GitHub**：源代码托管、版本管理、Issue 跟踪
- **ClawHub**：技能市场、用户一键安装

## 📋 发布前检查清单

### 隐私审查

```bash
# 搜索硬编码凭证（覆盖飞书/IMA/GitHub/SkillHub 全部 token 前缀）
grep -rE "cli_[0-9a-f]{16}|sk-[a-zA-Z0-9]{20,}|ou_[0-9a-f]{20,}|ghp_[a-zA-Z0-9]{20,}|gho_[a-zA-Z0-9]{20,}|ghs_[a-zA-Z0-9]{20,}|skh_[a-zA-Z0-9]{20,}|x[A-Za-z0-9]{20,}" \
  --include="*.py" --include="*.md" --include="*.json" \
  --exclude-dir=data --exclude-dir=__pycache__
```

预期：除 `<your_xxx>` 占位符外无匹配。

### 质量审查

- [ ] `SKILL.md` frontmatter 完整（name / description / version / tags）
- [ ] `README.md` 中英双语完整
- [ ] `CHANGELOG.md` 版本记录完整
- [ ] `LICENSE` 文件存在（**MIT-0**）
- [ ] `.claude-plugin/plugin.json` 元数据正确（含 `author` 和 `skills` 字段）
- [ ] `docs/CONTRIBUTING.md` 存在
- [ ] 所有脚本可执行无语法错误：`python -c "import scripts.fetch_clawhub"`
- [ ] 本地流程跑通：fetch → metrics → recommend → push

### 文档审查

- [ ] 触发词完整（在 SKILL.md 和 plugin.json）
- [ ] 双模式说明（Interactive / Cron）
- [ ] 凭证获取说明
- [ ] 故障排查章节

## 🚀 发布到 GitHub

### 方式 A：git push（推荐）

```bash
# 1. 进入项目目录
cd clawhub-daily

# 2. 初始化（如果还没）
git init
git branch -M main

# 3. 添加远程仓库
git remote add origin https://github.com/EdwardWason/clawhub-daily.git

# 4. 首次提交
git add .
git commit -m "feat: initial release v1.0.0"
git push -u origin main
```

### 方式 B：GitHub REST API（git push 超时时）

当 `git push` 因 443 端口问题失败时：

#### 1. 创建仓库

```bash
curl -X POST https://api.github.com/user/repos \
  -H "Authorization: token <GH_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "clawhub-daily", "private": false, "auto_init": true}'
```

#### 2. 逐文件上传

```bash
upload_file() {
  local file_path="$1"
  local content=$(base64 -w 0 "$file_path" 2>/dev/null || base64 "$file_path")
  curl -X PUT "https://api.github.com/repos/EdwardWason/clawhub-daily/contents/$file_path" \
    -H "Authorization: token <GH_TOKEN>" \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Upload $file_path\", \"content\": \"$content\", \"branch\": \"main\"}"
  sleep 0.5  # 避免速率限制
}

# 上传所有文件
for file in $(find . -type f -not -path './data/*' -not -path './.git/*' -not -name '__pycache__' -not -name '*.pyc'); do
  upload_file "$file"
done
```

#### 3. 创建 Release

```bash
curl -X POST https://api.github.com/repos/EdwardWason/clawhub-daily/releases \
  -H "Authorization: token <GH_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "tag_name": "v1.0.0",
    "name": "ClawHub Daily v1.0.0",
    "body": "Initial release. See CHANGELOG.md for details.",
    "draft": false,
    "prerelease": false
  }'
```

### 4. Token 配置

将 `GH_TOKEN` 保存到 `.env.local`（**不入库**）：

```bash
echo "GH_TOKEN=ghp_xxxxxxxxxxxxx" > .env.local
```

确保 `.gitignore` 包含 `.env.local`（默认已包含）。

## 🦞 发布到 ClawHub

### 方式 A：clawhub CLI（推荐）

```bash
# 1. 安装 CLI
npm i -g clawhub

# 2. 登录
clawhub login --token <CLAWHUB_TOKEN> --no-browser

# 3. 验证
clawhub whoami

# 4. 发布
clawhub publish . \
  --slug skill-daily \
  --name "ClawHub Daily · 每日 Skill 洞察" \
  --version 1.0.0 \
  --tags "recommendation,clawhub,feishu,lark,ima,scheduled-task,0-token" \
  --changelog "Initial release. See CHANGELOG.md for details."
```

### 方式 B：HTTP API（不推荐）

**不要使用 HTTP API 发布**：
- `api.clawhub.io/*` SSL 证书过期
- `clawhub.ai/api/v1/skills` POST 端点无法传递 MIT-0 许可证接受字段
- 结论：必须用 `clawhub` CLI

## 🔄 发布新版本

### 1. 更新版本号

- `SKILL.md` frontmatter 中的 `version` 字段
- `.claude-plugin/plugin.json` 中的 `version` 字段
- `CHANGELOG.md` 添加新版本段落

### 2. 提交 + 推送

```bash
git add .
git commit -m "feat: release v1.1.0"
git push origin main
git tag v1.1.0
git push origin v1.1.0
```

### 3. 重新发布到 ClawHub

```bash
clawhub publish . --slug skill-daily --name "..." --version 1.1.0 --tags "..." --changelog "..."
```

CLI 会自动处理版本号更新和 Changelog 展示。

## 🐛 常见问题

### Q: git push 报 443 连接超时

A: 用 GitHub REST API 方式（见上文）。

### Q: ClawHub CLI 报"MIT-0 license terms must be accepted"

A: 这是 ClawHub 强制要求。`LICENSE` 必须是 MIT-0 协议（不是 MIT）。`clawhub publish` 时会自动处理。

### Q: ClawHub 推送时 "Authentication failed"

A: 重新登录：
```bash
clawhub login --token <CLAWHUB_TOKEN> --no-browser
clawhub whoami  # 验证
```

### Q: 怎么撤下某版本？

A: ClawHub 暂不支持撤下版本，但可以发布修复版本覆盖。

GitHub 可以删除 Release：
```bash
# 1. 删除 Tag
git push origin :refs/tags/v1.0.0
# 2. 在 GitHub 网页上删除 Release
```

## 📚 参考

- GitHub 仓库范式：`docs/knowledge/patterns/2026-06-03-github-skill-repo-paradigm.md`
- ClawHub 发布踩坑：`docs/knowledge/pitfalls/2026-06-03-clawhub-publishing.md`
- GitHub API 备选推送：`docs/knowledge/pitfalls/2026-06-03-github-api-alternative-push.md`
