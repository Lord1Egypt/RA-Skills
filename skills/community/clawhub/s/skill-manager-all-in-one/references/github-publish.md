# GitHub 上传专项 | GitHub Publishing Guide

本文件定义技能通过独立 GitHub 仓库发布的操作规范。

## 适用场景

- 技能有独立的 GitHub 仓库
- 非 ClawHub 平台发布（如个人仓库、GitHub Pages 等）
- 需与 ClawHub 发布流程区分

## 发布前准备（对照 SKILL.md 第 6 章清单）

发布 GitHub 前，逐项核对 SKILL.md 中的通用质量基线（G01~G06）和 GitHub 专项（GH01~GH06）：

| 项目 | 内容 |
|------|------|
| G01 去标识化 | 无个人信息、内部路径、私有凭证 |
| G02 安全性 | 无代码安全风险（输入校验、权限最小化） |
| G03 逻辑科学性 | 结构清晰、路径准确、模块化 |
| G04 AI 可读性 | agent 可理解、上下文连贯 |
| G05 易维护性 | 代码整洁、注释到位 |
| G06 依赖声明 | 外部包/工具/密钥已声明，无硬编码 |
| GH01 文件结构 | 符合 Skill 目录体系（SKILL.md 在根目录） |
| GH02 README | 英中文双语，有安装/使用说明 |
| GH03 Commit 规范 | 英文在前、中文在后，格式正确 |
| GH04 Release Notes | Markdown 格式，结构清晰 |
| GH05 无敏感信息 | 无 API Key、Token、内部路径 |
| GH06 权限隔离 | 无过度文件权限、无不必要的管理脚本 |

**若涉及多语言 README 或多文件修改：逐个修改，逐个确认。**

## 两步验证流程（对应 SKILL.md Phase 2 步骤 2 两步验证）

### 第一步（AI 内部执行，不输出给用户）

- 对照清单全部项（G01~G06 + GH01~GH06），逐项标注 ✅ / ⚠️
- 检查文件大小（>50MB 需报告）
- 拟定 Commit Message（英文在前，中文在后）
- 检查 `git status`，列出所有未提交的变更
- 若有未提交变更，列出文件名，等待用户确认后再处理

### 第二步（输出给用户，等待明确确认）

⚠️ **未经用户明确确认，不得执行 `git push` / `gh release create` 等任何发布类命令。**

向用户汇报以下全部内容：

| 项目 | 内容 |
|------|------|
| 仓库地址 | `https://github.com/<owner>/<repo>` |
| 当前状态 | 已修改未提交 / 已提交未推送 |
| 未提交文件 | 列出所有变更文件 |
| Commit Message | 拟定的提交信息 |
| 核对清单结果 | G01~G06 + GH01~GH06，✅ / ⚠️ 标注 |
| 文件大小 | 是否超 50MB |
| 问题说明 | 有 ⚠️ 项时，说明具体问题 |
| 解决方案 | 针对 ⚠️ 项的修复方案 |

**确认标志**：用户必须回复「确认-<username>」（电子签名格式），不得用「好」「确认」「上传」「发吧」等语义模糊的词汇替代。

**重启规则**：每次用户提出修改，都必须从第一步重新开始。

## 执行发布（对应 SKILL.md Phase 2 步骤 3）

获得用户确认后，执行以下命令：

```bash
# 1. 进入仓库目录
cd <skill-dir>

# 2. 添加所有变更
git add -A

# 3. 提交（英文在前，中文在后）
git commit -m "[English message]. [中文信息]。"

# 4. 推送到远程
git push
```

## Commit Message 规范

- 英文在前，中文在后
- 正式发布语气
- 禁止：个人纠错、格式调整、私人调试记录、玩笑、道歉式表述
- 示例：`fix: 修复徽章HTML兼容性问题，清理各语言版本中文残留`

## 安全约束

1. **严禁擅自上传** — 未获用户明确确认前不得执行 `git push`
2. **汇报当前状态** — 每次修改后必须汇报状态（已修改/未提交/已上传）
3. **等待电子签名** — 用户回复「确认-<username>」后才执行 push

## Git 状态检查命令

```bash
# 查看当前状态
git status

# 查看变更统计
git diff --stat

# 查看完整变更内容
git diff

# 查看提交历史
git log --oneline -5
```

## 常见问题处理

### 有未提交的变更

用户要求上传前，先检查 `git status`：
- 如有未提交的变更，必须在汇报中列出
- 等待用户确认后再 add/commit/push

### 远程分支落后

```bash
# 先拉取最新
git pull --rebase

# 再推送
git push
```

### 冲突处理

1. 报告用户存在冲突
2. 等待用户指示如何解决
3. 不得强制覆盖远程分支

## GitHub Release 专项 | GitHub Release Guide

创建 GitHub Release 同样需要两步验证。Release Notes 是对外展示的正式说明，必须符合规范。

### 何时需要创建 Release

- 首次正式发布版本（如 v1.0.0）
- 重要版本更新
- 用户明确要求创建 Release

### Release Notes 规范

**格式**：Markdown 语法，结构清晰
**内容**：
- 标题（版本号 + 简短描述）
- 变更说明（功能/修复/优化）
- 技术规格（如适用）
- 安装方式（如适用）

**禁止**：
- 个人调试记录
- 道歉式表述
- 不完整的描述

### 两步验证流程（Release，对应 SKILL.md Phase 2 步骤 2 两步验证）

#### 第一步（AI 内部执行，不输出给用户）

- 检查 git tag 列表，确认版本号未冲突
- 拟定 Release Notes（英文在前，中文在后）
- 检查变更内容是否与 Commit History 一致

#### 第二步（输出给用户，等待明确确认）

| 项目 | 内容 |
|------|------|
| 仓库地址 | `https://github.com/<owner>/<repo>` |
| 当前 tag | 已有 tag 列表 |
| 新版本号 | 如 v1.0.0 |
| Release Notes | 拟定的正式说明 |
| 变更内容 | 列出主要变更 |

**确认标志**：用户必须回复「确认-<username>」（电子签名格式）才可执行。

#### 执行发布（对应 SKILL.md Phase 2 步骤 3）

```bash
# 1. 创建 tag（如尚未创建）
git tag -a <version> -m "<version>"

# 2. 推送 tag
git push origin <version>

# 3. 使用 gh 创建 Release
gh release create <version> \
  --title "<标题>" \
  --notes "<Markdown 格式的 Release Notes>" \
  --target <branch>
```

### Release Notes 示例

```markdown
## What's New

**Skill Name** — 简短描述

基于 xxx，为用户提供 yyy 功能。

### 功能更新
- 新增 xxx 功能
- 优化 xxx 体验
- 修复 xxx 问题

### 技术规格
- 版本：1.0.0
- 支持平台：xxx
- 依赖：xxx

### 安装方式
```bash
xxx install command
```
```

### 验证命令

```bash
# 查看已创建的 Release
gh release list

# 查看特定 Release 详情
gh release view <tag>

# 更新 Release Notes
gh release edit <tag> --notes "<新内容>"
```

## 与 ClawHub 的区别

| 维度 | ClawHub | GitHub（独立仓库） |
|------|---------|-------------------|
| 平台 | clawhub CLI | git + gh CLI |
| 版本管理 | clawhub 内部管理 | git tag + Release |
| 验证方式 | `clawhub inspect` | `git log` + `gh release list` |
| 发布命令 | `clawhub publish` | `git push` + `gh release create` |
| 对外说明 | Changelog | Release Notes |
| 适用场景 | 技能市场分发 | 独立项目/文档站 |
