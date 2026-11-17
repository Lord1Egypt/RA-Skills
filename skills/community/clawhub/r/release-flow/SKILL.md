---
name: release-flow
description: redfoxhub-html 项目专用的 Git 发布流程编排器。当用户表达「我要做新功能 / 改个 bug / 优化一下 X / 帮我开个分支」时走 feature-start 子流程；当用户说「更新测试环境 / 发测试 / 部署到 test / 推 develop」时走 deploy-test 子流程；当用户说「更新正式环境 / 发线上 / 部署正式 / 推 master」时走 deploy-prod 子流程。负责分支命名、与 origin/master、origin/develop 同步、合并目标与冲突兜底。
---

# Release Flow

本项目（`redfoxhub-html`）有两套阿里云效流水线：

| 环境 | 流水线 | 触发分支 | 链接 |
| ---- | ------ | -------- | ---- |
| 测试 | `redfoxhub-html-test` | `develop` | https://flow.aliyun.com/pipelines/4962314/current |
| 正式 | `redfoxhub-html` | `master`  | https://flow.aliyun.com/pipelines/4946808/current |

约定的研发流程是：**从 `master` 切工作分支 → 写完合并到 `develop` 走测试 → 验证通过合并到 `master` 走正式**。本 Skill 把这条链路固化下来，覆盖三类语义触发。

## 何时使用本 Skill

- 用户说「我要做新功能 / 改个 bug / 优化下 xx / 帮我新开个分支」 → [feature-start](#子流程一feature-start开始新功能)
- 用户说「更新测试环境 / 发测试包 / 部署到 test / 推送到 develop」 → [deploy-test](#子流程二deploy-test更新测试环境)
- 用户说「更新正式环境 / 发线上 / 部署正式 / 推 master」 → [deploy-prod](#子流程三deploy-prod更新正式环境)

如果用户的语义不能明确归类，先用一句话和用户对齐意图后再进入对应子流程，**不要混合执行**。

## 公共强约束

执行任何子流程都必须遵守以下规则，违反时立刻停下并向用户说明：

1. **远端固定为 `origin`**，只与 `origin/master`、`origin/develop` 交互。
2. **`master` / `develop` 上禁止直接修改代码**，仅做合并和推送。
3. **每一步开始前先 `git status --porcelain`**，工作区/暂存区不干净时停下询问用户（让用户自己 stash 或 commit，不要替用户做）。
4. **破坏性命令前先打印命令清单**（push、合并到 master/develop、checkout 切走当前未提交改动等），等用户确认。
5. **遇到 merge 冲突立刻停止**，输出冲突文件列表并提示用户手工解决；不要 `git merge --abort`，也不要使用 `-X ours/theirs` 强行解决。
6. 全程使用 `git config user.name` 的实际值，不再生成额外缩写或后缀。

## 工具使用约定（给 Agent）

- 所有 Git 操作通过 Bash 工具执行；不要拼接到一条 `&&` 链里执行多步破坏性操作，分步执行便于在中途失败时停下。
- 在每个子流程开头**先调用 `git rev-parse --abbrev-ref HEAD` 与 `git status --porcelain`** 拿到上下文，再决定后续命令。
- 命令失败时**不要重试也不要自动绕过**，把 stderr 原样回报用户。

---

## 子流程一：feature-start（开始新功能）

### 触发语义
> 「我要做新功能 / 我要改个 bug / 我要优化下 xx / 帮我开个分支做 xx」

### 步骤

1. **询问意图**：让用户用一句话描述要做的事（如果消息里已经说清楚了，跳过这一步）。

2. **判定类型**：基于描述自动归类，把判定结果回显给用户确认：
   - 全新能力 → `feat`
   - 已有功能调整、文案、样式、交互优化等常规迭代 → `update`
   - 修复 Bug → `fix`
   - 不确定时优先 `update`，并在确认环节告诉用户。

3. **生成分支名**：
   - 格式：`<type>/<slug>_<gitUser>`
   - `slug`：从用户描述里抽取核心名词，**英文小写、下划线连接，长度 ≤ 24 字符**。中文功能名要给出英文译名（例如「价格模块」→ `price`、「用户余额展示」→ `user_balance`）。
   - `gitUser`：执行 `git config user.name`，原样使用；若该值含空格或大写，做小写化并去空格。读不到时回退为 `dev` 并提示用户后续可以补全。
   - 同名分支已存在 → 末尾追加 `_v2`/`_v3`，最多到 `_v9`，仍冲突则停下让用户改名。
   - **生成后先把分支名给用户确认**，再执行后续命令。

4. **同步 master 并切出新分支**（确认后整段执行）：
   ```bash
   git status --porcelain                 # 必须为空
   git fetch origin
   git checkout master
   git pull --ff-only origin master       # fast-forward，避免本地 master 误产生分叉
   git checkout -b <type>/<slug>_<gitUser>
   ```

5. **完成后输出**：
   - 新分支名
   - 起点 commit hash（`git rev-parse --short HEAD`）
   - 与 `origin/master` 的差异（`git rev-list --count master..HEAD`，应为 0）
   - 提示「现在可以开始编码」

### 失败兜底
- 工作区有改动 → 提示用户先 `git stash` 或先 commit，**不要替用户做**。
- `git pull --ff-only` 失败 → 说明本地 master 已分叉，告知用户原因，让用户决定是否 `git reset --hard origin/master`，Agent 不强行 reset。
- `git config user.name` 为空 → 提示用户配置后重试，临时使用 `dev` 作为后缀。

---

## 子流程二：deploy-test（更新测试环境）

### 触发语义
> 「更新测试环境 / 发个测试包 / 部署到 test / 推送到 develop」

### 前置假设
当前在某个工作分支（**非 `master`/`develop`**），代码已经写完且已 commit。若仍有未提交改动，先停下提醒用户提交，commit message 由用户提供（业务 commit message 不由 Skill 代写）。

### 步骤

1. **环境校验**：
   - `git rev-parse --abbrev-ref HEAD` 不能是 `master` 或 `develop`；否则提示「请回到工作分支再执行」。
   - `git status --porcelain` 必须为空。
   - 记录当前分支名为 `WORK_BRANCH`。

2. **同步并合入 master 最新代码**（在工作分支上完成）：
   ```bash
   git fetch origin
   git merge origin/master                # 把 master 最新代码合进工作分支
   ```
   有冲突 → 立刻停下提示，列出冲突文件，**不要继续后续步骤**。

3. **推送工作分支到远程**（保留分支历史 / 方便回溯）：
   ```bash
   git push -u origin <WORK_BRANCH>
   ```

4. **合并到 develop 并推送**：
   ```bash
   git checkout develop
   git pull --ff-only origin develop
   git merge --no-ff <WORK_BRANCH>        # --no-ff 保留特性分支拓扑
   git push origin develop
   ```

5. **回到工作分支**：
   ```bash
   git checkout <WORK_BRANCH>
   ```

6. **结束输出**：
   - 提示「已推送到 develop，redfoxhub-html-test 流水线将自动触发」
   - 给出流水线链接：https://flow.aliyun.com/pipelines/4962314/current

### 失败兜底
- merge 冲突（无论是 `merge origin/master` 还是 `merge <WORK_BRANCH>` 到 develop）→ 列出冲突文件，提示用户手工解决后重新触发 Skill；**不要 `--abort`**。
- `push origin develop` 被拒（非快进、保护分支）→ 把错误原文交给用户，建议改走 Codeup MR 流程，不强推。

---

## 子流程三：deploy-prod（更新正式环境）

### 触发语义
> 「更新正式环境 / 发线上 / 部署正式 / 推 master」

### 前置假设
工作分支已经在 `deploy-test` 流程中验证通过；当前分支应为该工作分支，工作区干净。

### 步骤

1. **环境校验**：当前分支非 `master`/`develop`，工作区干净。记录当前分支为 `WORK_BRANCH`。

2. **二次确认**：明确告诉用户「⚠️ 此操作将合并到 master 并触发线上发布流水线 redfoxhub-html，请确认」，**等待用户回复 `yes` / `确认` / `确定` 之类的肯定词后再继续**。否定或未回复一律视为取消。

3. **同步并合入 master 最新代码**：
   ```bash
   git fetch origin
   git merge origin/master
   git push -u origin <WORK_BRANCH>
   ```

4. **合并到 master 并推送**：
   ```bash
   git checkout master
   git pull --ff-only origin master
   git merge --no-ff <WORK_BRANCH>
   git push origin master
   ```

5. **回到工作分支**：
   ```bash
   git checkout <WORK_BRANCH>
   ```

6. **结束输出**：
   - 提示「已推送到 master，redfoxhub-html 流水线将自动触发线上发布」
   - 给出流水线链接：https://flow.aliyun.com/pipelines/4946808/current

### 失败兜底
- 推送 master 被拒（分支保护、需要 MR）→ 输出错误原文，建议走 Codeup Merge Request 流程，**不强推**。
- merge 冲突 → 列出冲突文件，提示用户手工解决；不要 `--abort`。

---

## 附：与项目其他规范的关系

- 提交类型 `feat` / `update` / `fix` 与 [agents.md](../../../agents.md) 和 [docs/development/code-standards.md](../../../docs/development/code-standards.md) 中的 commit 规范一致；其他类型（`docs` / `chore` / `refactor` 等）由用户在写 commit message 时自行选择，本 Skill 不对其作分支级编排。
- 本 Skill **不修改任何业务代码或 CI 配置**，仅编排 Git 流程。
