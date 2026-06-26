# 发布流程

## 版本规范

采用语义化版本 (SemVer)：
- MAJOR.MINOR.PATCH
- 例如: 1.0.0

## 发布准备

### 1. 更新版本号

编辑 `package.json`:
```json
{
  "version": "1.0.0"
}
```

### 2. 更新变更日志

编辑 `github/CHANGELOG.md`:
```markdown
## [1.0.0] - 2026-04-13

### Added
- 初始版本发布
- 7层目录结构
- 1760个梦境记忆
- 混合搜索系统

### Fixed
- 修复了查询性能问题

### Changed
- 优化了存储结构
```

### 3. 完整测试

```bash
# 运行所有测试
npm test

# 运行系统验证
node memory/scripts/verify-system.cjs

# 代码检查
npm run lint
```

## 发布步骤

### 1. 创建 Git Tag

```bash
git add .
git commit -m "Release v1.0.0"
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin master --tags
```

### 2. 构建发布包

```bash
# 创建发布目录
mkdir -p release/v1.0.0

# 复制文件
cp -r memory release/v1.0.0/
cp README.md release/v1.0.0/
cp -r docs release/v1.0.0/
cp -r examples release/v1.0.0/

# 创建 ZIP
cd release
zip -r unified-memory-architect-v1.0.0.zip v1.0.0/
```

### 3. GitHub Release

1. 创建 GitHub Release
2. 上传 ZIP 文件
3. 填写 Release Notes

### 4. ClawHub 发布

```bash
# 发布到 ClawHub
openclaw skill publish ./clawhub/skill.json
```

## 发布后

1. 验证 GitHub Release
2. 验证 ClawHub 页面
3. 更新文档链接
4. 通知社区

## 紧急修复

如需紧急修复：

```bash
# 创建热修复分支
git checkout -b hotfix/v1.0.1

# 修复并提交
git commit -m "Fix: critical bug"

# 合并回 master
git checkout master
git merge hotfix/v1.0.1

# 创建补丁版本
git tag v1.0.1
git push --tags
```
