# GitHub Sync Authorization

## Purpose

OpenClaw may run on a machine that has no GitHub CLI, no SSH key, and no saved Git credentials. Do not assume GitHub sync is available.

The learning workflow must work in two layers:

1. Always generate local learning files first.
2. Sync to GitHub only after the parent asks for sync/publish, or after `.zhizhi-math-coach/config.json` records that automatic sync/Pages publishing is enabled and the current machine passes Git authorization checks.

The machine-readable config is the durable memory for this setup. README text and prior chat history are not enough for OpenClaw to know that a personal repository is already configured.

## What Is Required

GitHub sync requires standard `git` access from the OpenClaw machine:

- `git` installed;
- the personal learning workspace is a Git repository;
- `origin` points to the target GitHub repository;
- current machine has push authorization through a repository-scoped SSH deploy key, another SSH key, or an HTTPS token.

GitHub CLI `gh` is optional. Do not require it.

ClawHub login is not GitHub repository authorization. Model provider login is not GitHub repository authorization.

## Recommended Authorization: Repository Deploy Key

Prefer a GitHub repository Deploy key for OpenClaw-hosted machines. Many OpenClaw providers do not expose a safe place for user-managed GitHub token environment variables, while SSH deploy keys only require the public key to be added in the target repository settings.

Rules:

- Generate one key per personal learning repository.
- Keep the private key on the OpenClaw machine only.
- Send only the `.pub` public key to the parent.
- The parent adds the public key to the target repository: GitHub repository -> Settings -> Deploy keys -> Add deploy key.
- The parent must enable `Allow write access` if OpenClaw should push commits.
- Use Deploy keys only for the personal learning repository, not for the reusable skill source repository.
- GitHub reference: https://docs.github.com/developers/overview/managing-deploy-keys/

OpenClaw setup command:

```bash
python3 {baseDir}/scripts/prepare_github_deploy_key.py \
  --workspace <personal-learning-workspace> \
  --configure-remote
```

If `origin` is not configured yet, pass the target repository explicitly:

```bash
python3 {baseDir}/scripts/prepare_github_deploy_key.py \
  --workspace <personal-learning-workspace> \
  --github-owner <user> \
  --repo <repo> \
  --configure-remote
```

After the command prints `public-key-start` and `public-key-end`, send only that public key block to the parent. If a Lark/Feishu channel is available, send a message like:

```text
请把下面这个 OpenClaw 公钥加入 GitHub 仓库：

仓库：<user>/<repo>
位置：Settings -> Deploy keys -> Add deploy key
Title：OpenClaw zhizhi-math-coach <repo>
Key：<public-key>
权限：勾选 Allow write access

添加后回复“已添加”，我会再次检查并继续发布。
```

If no Lark/Feishu channel is available, return the same guidance in the OpenClaw reply. Never send the private key.

After the parent confirms the key has been added, run:

```bash
python3 {baseDir}/scripts/check_git_sync.py \
  --workspace <personal-learning-workspace> \
  --check-push \
  --write-config \
  --auto-sync \
  --sync-full-learning-data \
  --public-repository-accepted
```

If the preflight succeeds, this writes `.zhizhi-math-coach/config.json` so future OpenClaw runs can automatically pull, commit, and push the configured learning-data scope.

## Advanced Setup And Publish-Time Guidance

Do not check or prompt for GitHub sync during ordinary grading or PDF worksheet generation unless `.zhizhi-math-coach/config.json` already enables automatic sync or Pages publishing. Default unconfigured use is local learning files plus direct `worksheet.pdf` delivery.

Explicit trigger phrases:

- `进阶：配置 GitHub 云同步`
- `进阶：开启 GitHub Pages 在线访问`
- `生成 GitHub Deploy key`
- `配置云端备份`
- `返回 SSH 公钥`
- `配置公开链接`

When triggered, return the SSH public key and this public guide URL:

```text
https://github.com/linzi007/zhizhi-math-coach-openclaw/blob/main/docs/github-advanced-setup.zh-CN.md
```

When the parent asks for cloud sync, public links, Pages, push, commit, or automatic online publishing, check whether GitHub sync appears ready. If the workspace is missing `.git`, `origin`, or push authorization, include a short guidance note without blocking grading or worksheet generation:

- local learning files will still be generated;
- PDF delivery does not require GitHub;
- cloud backup and public links require GitHub sync and, for Pages, repository Pages setup;
- OpenClaw can generate a repository-specific SSH public key;
- the parent should add it to GitHub Deploy keys with write access.

When the parent later asks to publish a worksheet, send a public link, sync, push, or commit, or when the workspace config already enables automatic publishing:

1. Generate the worksheet and local `site/` output first.
2. Run the Git preflight.
3. If preflight fails, run or suggest `prepare_github_deploy_key.py`, send the public key and Deploy key steps through Lark/Feishu when available, and return the local file paths.
4. After the parent adds the key, rerun preflight and then push.

Do not treat missing GitHub authorization as worksheet-generation failure.

## Alternative Authorization: Existing SSH

Use SSH when possible because it does not require storing a token in commands.

Parent setup checklist:

```bash
git --version
ssh -T git@github.com
git remote -v
git remote set-url origin git@github.com:<user>/<repo>.git
git push --dry-run origin HEAD
```

If `ssh -T git@github.com` fails, the parent must add an SSH public key to GitHub on that machine/account.

## Last Resort: HTTPS Token

Use HTTPS tokens only when deploy keys or SSH are not available. The parent should create a fine-grained GitHub personal access token (PAT) scoped to the personal learning repository only.

Recommended token settings:

- Create path: GitHub web -> profile photo -> Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens -> Generate new token.
- Token type: fine-grained personal access token.
- Resource owner: the GitHub user or organization that owns the personal learning repository.
- Repository access: `Only select repositories`, then select only the personal learning repository, such as `zhizhi-math-learning-data`.
- Expiration: choose a finite expiry, for example 30 to 90 days, unless the parent has a managed secret-rotation process.
- Repository permissions for normal sync: `Contents: Read and write`.
- Repository permissions for optional workflow file setup: add `Workflows: Read and write` only if OpenClaw or local git will commit files under `.github/workflows/`.
- Repository permissions for GitHub Pages API management: add `Pages: Read and write` only if an automation will enable or update Pages through the GitHub API. This is not needed when the parent enables Pages in the GitHub web UI, and not needed for ordinary `git push` of `site/`.

Do not grant broad access such as `All repositories` or classic `repo` scope unless fine-grained tokens cannot satisfy the user's GitHub account or organization policy.

Do not ask the parent to paste tokens into chat. Do not write tokens into repository files.

Acceptable storage options depend on the machine:

- Git Credential Manager;
- OS keychain/credential helper;
- environment secret outside the repository;
- platform-managed secret store.

Parent setup checklist for HTTPS:

```bash
git --version
git remote -v
git remote set-url origin https://github.com/<user>/<repo>.git
git push --dry-run origin HEAD
```

When Git prompts for credentials, enter the GitHub username and use the PAT as the password. Never place the PAT in the remote URL, worksheet files, README files, prompts, or chat messages.

## Preflight

Before any automatic commit/push, run:

```bash
python3 {baseDir}/scripts/check_git_sync.py --workspace <personal-learning-workspace> --check-push
```

If the check fails, do not treat worksheet generation as failed. Return:

- local generated file paths;
- missing authorization item;
- exact command the parent can run to fix it;
- a note that sync can be retried later.

## Configured Automatic Sync Policy

Do not run `git add`, `git commit`, or `git push` for ordinary grading or local-only generation unless the parent says "同步", "发布", "push", "提交到 GitHub", "发链接", or equivalent, or `.zhizhi-math-coach/config.json` enables automatic Git sync or automatic Pages publishing.

Before reading long-term records in a configured workspace:

```bash
python3 {baseDir}/scripts/sync_learning_repo.py \
  --workspace <personal-learning-workspace> \
  --mode before-task
```

After local files are changed in a configured workspace:

```bash
python3 {baseDir}/scripts/sync_learning_repo.py \
  --workspace <personal-learning-workspace> \
  --mode after-task \
  --message "Update learning data"
```

If sync is requested:

1. Generate or update local files.
2. If a child-facing link is requested or Pages auto-publishing is enabled, run `publish_html_site.py` or `publish_and_wait_pages.py`.
3. Run the Git preflight.
4. If preflight passes, commit and push the requested scope.
5. If preflight fails, return local paths and setup guidance.

For public repositories, warn before committing `memory/`, `records/`, `mistakes/`, `weak-points/`, answer keys, uploads, or student identifiers.

For private repositories, full learning-state sync is acceptable after the parent asks for sync.

## GitHub Pages Note

GitHub Pages availability for private repositories depends on the user's GitHub plan. If Pages is not available or not authorized, keep local HTML output and Git sync separate: the worksheet still exists locally even if no public URL can be produced.
