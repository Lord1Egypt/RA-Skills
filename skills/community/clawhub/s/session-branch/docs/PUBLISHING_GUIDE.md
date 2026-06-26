# 发布指南 / Publishing Guide

## ClawHub 发布

```bash
# 1. 确认版本号（semver）
# 修改 SKILL.md frontmatter 和 plugin.json 中的 version

# 2. 更新 CHANGELOG.md

# 3. 发布
clawhub publish . --slug session-branch --version X.Y.Z
```

## GitHub 发布

### 方式一：REST API（无 git 环境）

```powershell
# 1. 逐文件上传（base64）
# 2. 创建 Release
# 3. 上传 zip Asset
```

详见项目知识库：`docs/knowledge/patterns/2026-06-03-dual-platform-publishing.md`

### 方式二：git push

```bash
git tag vX.Y.Z
git push origin main --tags
# 然后在 GitHub 创建 Release
```

## 发布前检查清单

- [ ] 版本号已更新（SKILL.md + plugin.json）
- [ ] CHANGELOG.md 已更新
- [ ] README.md 中英双语完整
- [ ] 无个人信息泄漏（扫描 token、路径、邮箱）
- [ ] zip 白名单打包（排除 .git、.env、*.log、data/）
- [ ] 三维审计：zip + GitHub 仓库 + ClawHub 平台

---

## ClawHub Publishing

```bash
clawhub publish . --slug session-branch --version X.Y.Z
```

## GitHub Publishing

### Option 1: REST API (no git environment)

Upload files via `PUT /repos/{owner}/{repo}/contents/{path}`, then create Release + zip Asset.

### Option 2: git push

```bash
git tag vX.Y.Z
git push origin main --tags
```

## Pre-release Checklist

- [ ] Version updated in SKILL.md + plugin.json
- [ ] CHANGELOG.md updated
- [ ] README.md bilingual (Chinese + English)
- [ ] No personal info leaks (scan tokens, paths, emails)
- [ ] Zip whitelist packaging (exclude .git, .env, *.log, data/)
- [ ] Three-axis audit: zip + GitHub repo + ClawHub platform
