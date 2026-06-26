---
name: submit-pr
description: 规范化 PR 提交工作流。当用户需要提交 PR 时使用，自动完成敏感信息扫描、文件范围确认、规范 commit 生成和 PR 创建
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git log:*), Bash(git branch:*), Bash(gh pr create:*), Bash(gh pr view:*)
argument-hint: "[pr-title]"
---

## 当前上下文

- 当前分支：!`git branch --show-current`
- 变更文件：!`git status --short`
- 最近 commit：!`git log --oneline -5`

## 任务

提交 PR，标题：$ARGUMENTS

按以下流程逐步执行，**每个检查不通过时必须停止并告知用户**。

---

## Step 1：敏感信息扫描

对所有待提交的变更文件执行扫描，检测以下模式：

**私钥 / 助记词**
```
0x[0-9a-fA-F]{64}           # 以太坊私钥
[0-9a-fA-F]{64}              # 裸十六进制私钥
PRIVATE_KEY\s*=\s*\S+        # 环境变量赋值
MNEMONIC\s*=\s*\S+
SECRET\s*=\s*\S+
```

**API 密钥 / Token**
```
sk-[a-zA-Z0-9]{20,}          # OpenAI / Anthropic key
ghp_[a-zA-Z0-9]{36}          # GitHub token
[0-9a-f]{32}                  # 通用 32 位 hex token
Authorization:\s*Bearer\s+\S+
```

**敏感文件**
- `.env`、`.env.*`（非 `.env.example`）
- `*.pem`、`*.key`、`*.p12`、`keystore.json`

执行命令：
```bash
git diff HEAD --name-only        # 获取变更文件列表
git diff HEAD -- <file>          # 逐文件检查内容
```

**结果**：
- 发现敏感信息 → **立即停止**，列出具体文件和行号，要求用户处理后重新触发
- 无敏感信息 → 继续 Step 2

---

## Step 2：文件范围确认

列出所有变更文件，按类型分组展示：

```
新增文件：
  + src/Foo.sol

修改文件：
  ~ src/Bar.sol
  ~ test/Bar.t.sol

删除文件：
  - src/Old.sol
```

询问用户：
> 以上文件是否都与本次功能相关？是否有需要排除或补充的文件？

**等待用户确认后**继续 Step 3。如有调整，执行：
```bash
git add <confirmed-files>       # 只暂存用户确认的文件
git restore --staged <excluded> # 移出不相关文件
```

---

## Step 3：生成 commit 信息

根据变更内容，生成符合以下规范的 commit message：

### 格式

```
<type>(<scope>): <subject>

[body - 可选，说明 why 而非 what，每行不超过 72 字符]
```

### type 枚举

| type | 适用场景 |
|------|---------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档变更 |
| `refactor` | 重构（不影响功能） |
| `test` | 测试相关 |
| `chore` | 构建/工具/依赖 |
| `perf` | 性能优化 |

### subject 规范

- **不超过 50 字符**
- 动词开头，使用英文原形：add / fix / remove / update / refactor 等
- **全程使用英文，禁止出现中文字符**
- 不加句号
- 说清楚"做了什么"，不写"update code"、"fix bug"这类无意义描述

### 示例

```
feat(vault): add reentrancy guard to withdraw
fix(token): correct decimal calculation in transfer
docs(readme): add skill usage guide
```

向用户展示生成的 commit message，**确认后**执行提交：

```bash
git commit -m "<confirmed message>"
```

---

## Step 4：推送并创建 PR

```bash
git push origin <current-branch>
```

使用以下模板创建 PR：

```bash
gh pr create \
  --title "$ARGUMENTS" \
  --body "$(cat <<'EOF'
## 变更内容

- <bullet points 说明主要改动>

## 测试

- [ ] 本地编译通过
- [ ] 相关测试通过
- [ ] 无敏感信息泄露

## 关联

EOF
)"
```

---

## 输出模板

```
## PR 提交报告

**分支**：<branch-name>
**标题**：<pr-title>
**Commit**：<hash> <message>

**敏感信息扫描**：✅ 通过
**文件范围**：✅ 已确认（共 N 个文件）

**PR 链接**：<gh pr url>
```

---

## 注意事项

- Step 1 发现敏感信息时**必须停止**，不得跳过
- Step 2 必须等用户明确确认文件列表，不得自动推断
- commit message **必须全程使用英文**，不得包含中文字符
- commit message **不得使用** AI 生成的模糊描述（"various improvements"、"update"等）
- 不得 force push 到 main/master 分支
