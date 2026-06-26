---
name: push-flow
description: Professional code review and Git commit workflow management. Use this skill when users mention 'push', 'commit', '提交', or any Git submission operations. Provides comprehensive pre-commit checks, code quality review, build verification, and Git workflow guidance following industry best practices.
---

# Push Flow

## Overview

This skill provides professional code review and Git commit workflow management. It ensures code quality through systematic pre-commit checks, build verification, and adherence to Git best practices before any code submission.

## Critical Rules

**NEVER automatically commit or push code without explicit user approval.**

All Git operations require user confirmation at each step.

**ALWAYS use Chinese for commit messages.**

All commit messages must be written in Chinese, following the conventional commits format with Chinese descriptions.

## Workflow Decision Tree

When user mentions push/commit/提交:

1. **Check for uncommitted changes** → If exists, proceed to step 2
2. **Offer code review** → Ask user if they want code review
3. **If code review requested** → Perform comprehensive review
4. **Generate commit message** → Present to user for approval
5. **Execute git commit** → Only after user approves message
6. **Run build verification** → Execute `go build` to ensure compilation
7. **Execute git pull** → Sync with remote before push
8. **If pull brings new changes** → Run `go build` again
9. **Execute git push** → Only after all checks pass

## Pre-Commit Workflow

### Step 1: Auto-Commit Existing Changes

Before making any code modifications, automatically commit existing uncommitted changes:

```bash
# Check for uncommitted changes
git status

# If changes exist, commit them
git add .
git commit -m "chore: 保存当前工作进度"
```

**Note:** This is a local commit only (no push). It preserves work-in-progress state.

### Step 2: Offer Code Review

Ask user explicitly:

> "检测到有代码变更，是否需要进行 Code Review？"

If user agrees, proceed to comprehensive code review.

### Step 3: Code Review Process

Perform systematic review covering:

**Code Quality:**
- Logic correctness and edge cases
- Error handling completeness
- Code readability and maintainability
- Performance considerations

**Go-Specific Standards:**
- Adherence to Go coding conventions
- Proper error handling patterns
- Goroutine and concurrency safety
- Resource management (defer usage)

**Project Standards:**
- Compliance with project coding guidelines
- Naming conventions
- Comment completeness
- Test coverage

**Security:**
- Input validation
- SQL injection prevention
- Sensitive data handling

Provide actionable feedback with specific line references and improvement suggestions.

### Step 4: Generate Commit Message

Create concise, descriptive commit message in Chinese following conventional commits format:

```
<type>: <description>

[optional body]
```

**Types:**
- `feat`: 新功能
- `fix`: 修复bug
- `refactor`: 重构
- `docs`: 文档更新
- `style`: 代码格式调整
- `test`: 测试相关
- `chore`: 构建/工具相关

**Example:**
```
feat: 添加用户认证中间件

- 实现JWT token验证
- 添加权限检查逻辑
- 完善错误处理
```

**Present to user for approval:**

> "建议的 commit message：
> 
> [commit message]
> 
> 是否同意使用此 commit message？"

### Step 5: Execute Commit

Only after user approval:

```bash
git add .
git commit -m "[approved commit message]"
```

### Step 6: Build Verification

Before any push operation, verify build succeeds:

```bash
go build
```

If build fails:
- Report errors to user
- Do NOT proceed with push
- Offer to help fix build issues

### Step 7: Pull Before Push

Always pull latest changes before pushing:

```bash
git pull
```

**If pull brings new changes:**
- Run `go build` again to verify compatibility
- If build fails, resolve conflicts before pushing

### Step 8: Execute Push

Only after all checks pass:

```bash
git push
```

## File Size and Type Restrictions

**Before committing, verify:**

1. **No binary files** (unless explicitly required)
2. **No files > 1MB**
3. **No sensitive data** (credentials, keys, tokens)

If violations detected, warn user and request confirmation or exclusion.

## Git Configuration Preferences

**Remote URL format:** Always use SSH format (`git@github.com:user/repo.git`) instead of HTTPS.

If HTTPS remote detected, suggest converting to SSH:

```bash
git remote set-url origin git@github.com:user/repo.git
```

## Go Build Requirements

**For Go projects:**

- Always run `go build` before commit
- Always run `go build` after pull if new changes merged
- Ensure compilation succeeds before any push operation

## Summary Checklist

Before push, ensure:

- [ ] Existing changes auto-committed (if any)
- [ ] Code review completed (if requested)
- [ ] Commit message approved by user
- [ ] `go build` succeeds
- [ ] `git pull` executed
- [ ] `go build` succeeds again (if pull brought changes)
- [ ] No binary files or files > 1MB
- [ ] User explicitly approved push operation

## Example Interaction

**User:** "帮我提交代码"

**Assistant:**
1. "检测到有未提交的代码变更，是否需要进行 Code Review？"
2. [If yes] Perform code review and provide feedback
3. "建议的 commit message：`feat: 添加用户登录功能`，是否同意？"
4. [After approval] Execute `git commit`
5. Execute `go build` to verify
6. Execute `git pull`
7. [If pull brought changes] Execute `go build` again
8. "所有检查通过，是否执行 git push？"
9. [After approval] Execute `git push`

## 其他
1. 密码检测规则 🔒
在 Critical Rules 部分新增：
禁止提交包含密码的文件
提交前自动扫描敏感信息，包括：
明文密码
API keys、tokens、secrets
数据库凭证
私钥
任何敏感认证信息
如果检测到敏感数据，立即停止提交并警告用户
检测模式包括：
password =, PASSWORD =, pwd =
api_key =, secret =, token =
private_key, 密码, 口令
数据库连接字符串中的凭证
JWT secrets、加密密钥

2. 多功能分离提交规则 📦
   在 Critical Rules 部分新增：
   当变更包含多个不同功能时，必须分别提交
   自动分析和分组文件：
   按文件路径和模块结构分组
   按相关功能分组（认证、API、数据库、UI等）
   按逻辑功能边界分组
   为每个功能组生成独立的 commit message
   按顺序依次提交，而不是一次性提交所有文件
   示例： 如果变更包含"用户认证"和"数据导出"两个功能，会创建两个独立的 commit：
   feat: 添加用户认证功能 (认证相关文件)
   feat: 实现数据导出功能 (导出相关文件)
