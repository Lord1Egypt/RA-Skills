# OpenClaw Quickstart

## Purpose

Use this reference when onboarding a parent or when the first reply in a personal learning workspace needs setup guidance.

Keep the user-facing reply short. Prefer a checklist and the next command/action over long architecture explanations.

## First-Use Checklist

1. Confirm the current workspace is the personal learning repository, not `zhizhi-math-coach-openclaw`.
2. Check `.zhizhi-math-coach/config.json` when present. It is the durable record for whether Git sync and Pages auto-publishing are already enabled.
3. If the learning files are missing, initialize:

```bash
python3 {baseDir}/scripts/init_learning_workspace.py \
  --workspace . \
  --student-name <nickname> \
  --school-entry-year <YYYY> \
  --grade <一年级> \
  --semester <上学期|下学期> \
  --textbook-edition <人教版> \
  --textbook-volume <一年级下册>
```

4. For normal unconfigured use, no GitHub setup is required. Generate worksheets locally and return or send `worksheet.pdf`.

## Advanced Cloud Sync And Pages

Use this section only when the parent asks for cloud sync, GitHub backup, public links, Pages, push, or automatic online publishing.

Trigger phrases:

- `进阶：配置 GitHub 云同步`
- `进阶：开启 GitHub Pages 在线访问`
- `生成 GitHub Deploy key`
- `配置云端备份`
- `返回 SSH 公钥`
- `配置公开链接`

When triggered, return this public guide URL:

```text
https://github.com/linzi007/zhizhi-math-coach-openclaw/blob/main/docs/github-advanced-setup.zh-CN.md
```

The reply should include:

- SSH public key copied only from `public-key-start` to `public-key-end`;
- GitHub path: `Settings -> Deploy keys -> Add deploy key`;
- instruction to enable `Allow write access`;
- next step: parent replies `已添加`, then run `check_git_sync.py --workspace . --check-push --write-config --auto-sync --sync-full-learning-data --public-repository-accepted`.

If GitHub owner/repo is missing and cannot be inferred from `origin`, ask:

```text
请告诉我你的 GitHub 用户名和个人学习数据仓库名，例如 linzi007 / zhizhi-math-learning-data。
```

1. Check GitHub sync only if the parent wants sync, public links, automatic Pages publishing, or `.zhizhi-math-coach/config.json` already enables it:

```bash
python3 {baseDir}/scripts/check_git_sync.py \
  --workspace . \
  --check-push \
  --write-config \
  --auto-sync \
  --sync-full-learning-data \
  --public-repository-accepted
```

2. If sync is not ready, generate a repository deploy key and send only the public key:

```bash
python3 {baseDir}/scripts/prepare_github_deploy_key.py \
  --workspace . \
  --github-owner <user> \
  --repo <repo> \
  --configure-remote
```

3. If public Pages is desired, confirm GitHub Settings -> Pages -> Source is `GitHub Actions`, then ensure the workflow exists:

```bash
python3 {baseDir}/scripts/setup_github_pages_workflow.py \
  --workspace . \
  --public-repository-accepted
```

If a workspace is already configured and the task changes learning files, run:

```bash
python3 {baseDir}/scripts/sync_learning_repo.py --workspace . --mode before-task
python3 {baseDir}/scripts/sync_learning_repo.py --workspace . --mode after-task --message "Update learning data"
```

## Quick Prompt Reference

Use these prompt shapes in examples and replies:

- `$zhizhi-math-coach 批改这张练习卷，记录薄弱项。`
- `$zhizhi-math-coach 根据最近错题生成变式练习。`
- `$zhizhi-math-coach 针对退位减法薄弱项出专项练习。`
- `$zhizhi-math-coach 生成期末错因复习卷，并发布学生版链接。`
- `$zhizhi-math-coach 开启定时任务，每天提醒到期复习和待批改练习。`

## Scheduled Reminders

Use this only after the parent asks for scheduled reminders or `.zhizhi-math-coach/config.json` already has `automation.enabled` and `automation.auto_register_when_supported` true.

```bash
python3 {baseDir}/scripts/setup_scheduled_tasks.py \
  --workspace . \
  --enable-config \
  --auto-register \
  --timezone Asia/Shanghai
```

Use the parent's local IANA timezone for `--timezone`. If `openclaw` is not installed in the current environment, the script prints the `openclaw cron add` commands to run in an OpenClaw Gateway environment. Scheduled reminders should not write records or generate worksheets unless the parent explicitly enables those config flags.

## Publish-Ready Checklist

This is an advanced online-access checklist. It is not needed when the worksheet is delivered as a PDF file.

Automatic Pages publishing is allowed when all are true:

- `.zhizhi-math-coach/config.json` exists with `pages.enabled` and `pages.auto_publish_worksheets` true.
- `.github/workflows/pages.yml` exists.
- The GitHub repository Pages source is `GitHub Actions`.
- The repository deploy key has write access.
- `check_git_sync.py --check-push` succeeds.
- The parent accepts public visibility of committed files in a public repository.

When ready, generate the worksheet PDF first, then publish and wait only if a public link is needed:

```bash
python3 {baseDir}/scripts/publish_and_wait_pages.py \
  worksheets/YYYY-MM-DD-topic \
  --workspace . \
  --base-url https://<github-user>.github.io/<repo>
```

Reply with:

- Local or sent `worksheet.pdf`.
- Pages index URL.
- Newly generated worksheet URL.
- Local `worksheet.html` and `answer-key.md` paths.
- Any caveat if Actions failed or timed out.

## Public Repository Ruleset

Recommended ruleset for direct OpenClaw publishing:

- Name: `main protect`.
- Status: `Active`.
- Bypass:
  - `Deploy keys`: `Always allow`.
  - `Repository admin`: `Always allow`.
- Target: `main`, or `Default` if default branch is `main`.
- Enable: `Restrict updates`, `Restrict deletions`, `Block force pushes`.
- Do not enable: required PRs, status checks, signed commits, or deployment gates.

This lets OpenClaw push through the deploy key while public viewers cannot edit `main`.
