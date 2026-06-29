# workspace-git-setup

> One command to set up safe, sensible Git tracking for any working directory — with a built-in security audit.
>
> 一条命令，为任意工作区配置安全合理的 Git 版本追踪 —— 内置安全巡检。

A zero-dependency Bash script that initializes Git version control for a project, ships a battle-tested security `.gitignore`, warns about large files before your first commit, and can audit an existing repo for leaked secrets and untracked files.

**Pure `bash` + `git`. No Python, no npm, no third-party packages.**

---

## English

### Why

Setting up Git for a new project usually means:
- copy-pasting a `.gitignore` from somewhere (and hoping it covers secrets),
- accidentally committing a `.env`, a private key, or a 200MB model file,
- never noticing that half your files were never `git add`-ed.

`workspace-git-setup` does all of that for you, safely and idempotently.

### Quick start

```bash
# Clone the repo, then run inside your project:
git clone https://github.com/Songhonglei/better-agent-skills.git
bash better-agent-skills/skills/workspace-git-setup/scripts/setup.sh
```

Or grab just the script with `curl` and run it in the current directory:

```bash
curl -fsSL https://raw.githubusercontent.com/Songhonglei/better-agent-skills/main/skills/workspace-git-setup/scripts/setup.sh -o setup.sh
bash setup.sh
```

That's it. It will:
1. `git init` (skipped if a repo already exists; default branch `main`),
2. write a security-focused `.gitignore`,
3. set `core.autocrlf=input` to avoid CRLF noise,
4. warn you about any file larger than 10MB before committing,
5. make the first commit.

### Specify a path and project name

```bash
bash scripts/setup.sh /path/to/project "MyProject"
```

### Path & identity resolution

| What | Priority |
|------|----------|
| Workspace path | CLI argument → `WORKSPACE_DIR` env var → current directory |
| Git identity | `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` env vars → existing git config → interactive prompt |

If you provide an email but no name, the email prefix is used as the username.

```bash
GIT_AUTHOR_NAME="Jane Doe" GIT_AUTHOR_EMAIL="jane@example.com" bash scripts/setup.sh
```

### Three modes

| Mode | What it does | Mutates? |
|------|--------------|----------|
| *(default)* | init + `.gitignore` + large-file warning + first commit | ✏️ yes |
| `--audit` | read-only health check: tracked secrets, untracked files, config | 👀 no |
| `--dry-run` | preview every action without applying anything | 👀 no |

#### Audit an existing repo

```bash
bash scripts/setup.sh --audit
```

Outputs three checks (read-only, never modifies anything):

1. **Sensitive files** — lists private keys / tokens / credentials already tracked by Git (leak risk). It only *warns* — it never runs destructive commands for you.
2. **Untracked files** — files neither `add`-ed nor ignored, so you can decide.
3. **Config** — whether `core.autocrlf` is sane and `.gitignore` exists.

#### Preview before applying

```bash
bash scripts/setup.sh --dry-run
```

### What the `.gitignore` covers

| Category | Patterns |
|----------|----------|
| Credentials | `.env`, `.env.*`, `*.pem`, `secrets/`, `.credentials/`, `*token*.json`, `*secret*.json` |
| TLS / SSH keys | `**/certs/*.key`, `id_rsa`, `id_dsa`, `id_ecdsa`, `id_ed25519`, `*.p12`, `*.keystore` |
| Temp / cache | `tmp/`, `*.tmp`, `*.cache`, `*.log`, `*.pid` |
| OS / editor | `.DS_Store`, `._*`, `Thumbs.db`, `.vscode/`, `.idea/`, `*.swp` |
| Dependencies | `node_modules/`, `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `.pytest_cache/` |
| Build output | `output/`, `dist/`, `build/`, `out/`, `*.egg-info/` |

> Note: it scopes private-key ignores to `**/certs/*.key` (instead of a blanket `*.key`) so it won't accidentally hide legitimate `.key` files elsewhere.

### Design notes

- **Idempotent** — run it as many times as you like; existing config is preserved, not clobbered. If a `.gitignore` already exists, it shows a diff and asks before overwriting.
- **No surprises** — large files (>10MB) trigger a confirmation prompt before the first commit, so you don't bloat your repo by accident.
- **Local only** — it does not add a remote. Add one yourself when ready:
  ```bash
  git remote add origin <your-repo-url>
  ```

### Requirements

- `git` — https://git-scm.com/downloads
- `bash` 4.0+
- `coreutils` (`numfmt`/`stat`/`realpath`) — preinstalled on most Unix-like systems; `numfmt` is optional (falls back to raw byte counts).

---

## 中文

### 为什么需要它

给新项目配 Git 通常会遇到：
- 到处粘贴 `.gitignore`（也不知道有没有覆盖到敏感信息），
- 不小心把 `.env`、私钥或 200MB 的模型文件提交进 git，
- 半个项目的文件根本没 `git add` 进去都没察觉。

`workspace-git-setup` 一条命令安全幂等地搞定。

### 快速开始

```bash
# 克隆仓库，然后在你的项目目录运行：
git clone https://github.com/Songhonglei/better-agent-skills.git
bash better-agent-skills/skills/workspace-git-setup/scripts/setup.sh
```

或者只下载脚本本身在当前目录跑：

```bash
curl -fsSL https://raw.githubusercontent.com/Songhonglei/better-agent-skills/main/skills/workspace-git-setup/scripts/setup.sh -o setup.sh
bash setup.sh
```

会自动完成：
1. `git init`（已有仓库则跳过；默认分支 `main`）,
2. 写入安全 `.gitignore`,
3. 设置 `core.autocrlf=input` 避免 CRLF 假 diff,
4. 提交前预警 >10MB 的大文件,
5. 完成首次 commit。

### 指定路径和项目名

```bash
bash scripts/setup.sh /path/to/project "MyProject"
```

### 路径与身份解析

| 项 | 优先级 |
|----|--------|
| 工作区路径 | 命令行参数 → 环境变量 `WORKSPACE_DIR` → 当前目录 |
| Git 身份 | 环境变量 `GIT_AUTHOR_NAME`/`GIT_AUTHOR_EMAIL` → 已有 git config → 手动输入 |

只给邮箱不给用户名时，自动用邮箱前缀作为用户名（可后续 `git config` 修改）。

```bash
GIT_AUTHOR_NAME="Jane Doe" GIT_AUTHOR_EMAIL="jane@example.com" bash scripts/setup.sh
```

### 三种模式

| 模式 | 作用 | 是否改动 |
|------|------|----------|
| 默认（初始化/对齐） | git init + `.gitignore` + 大文件预警 + 首次 commit | ✏️ 会改 |
| `--audit` | 只读巡检：已 tracked 敏感文件、未跟踪文件、`core.autocrlf` 配置 | 👀 只读 |
| `--dry-run` | 预览所有改动，不落地 | 👀 只读 |

#### 巡检已有仓库

```bash
bash scripts/setup.sh --audit
```

输出三类只读体检结果，**不自动修改**：

1. **敏感文件** —— 列出已被 git 跟踪的私钥/token/凭证类文件（泄露风险），只报警不给执行命令
2. **未跟踪文件** —— 既没 add 也没被 .gitignore 排除的文件
3. **配置** —— `core.autocrlf` 是否为推荐值、`.gitignore` 是否存在

#### 落地前预览

```bash
bash scripts/setup.sh --dry-run
```

### `.gitignore` 默认规则覆盖范围

| 类型 | 规则 |
|------|------|
| 敏感凭证 | `.env`, `.env.*`, `*.pem`, `secrets/`, `.credentials/`, `*token*.json`, `*secret*.json` |
| TLS / SSH 私钥 | `**/certs/*.key`, `id_rsa`, `id_dsa`, `id_ecdsa`, `id_ed25519`, `*.p12`, `*.keystore` |
| 临时/缓存 | `tmp/`, `*.tmp`, `*.cache`, `*.log`, `*.pid` |
| 系统/编辑器 | `.DS_Store`, `._*`, `Thumbs.db`, `.vscode/`, `.idea/`, `*.swp` |
| 依赖 | `node_modules/`, `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `.pytest_cache/` |
| 构建产物 | `output/`, `dist/`, `build/`, `out/`, `*.egg-info/` |

> 注意：私钥忽略规则用的是 `**/certs/*.key`（不是 `*.key` 通配），避免误屏蔽其他地方合法的 `.key` 文件。

### 设计要点

- **幂等** —— 想跑多少次跑多少次，已有配置不会被清掉。`.gitignore` 已存在则展示 diff，由你拍板是否覆盖
- **无意外** —— 首次 commit 前 >10MB 的大文件会要求确认，不会让仓库静默膨胀
- **纯本地** —— 不加 remote，需要时自己加：
  ```bash
  git remote add origin <your-repo-url>
  ```

### 依赖

- `git` —— https://git-scm.com/downloads
- `bash` 4.0+
- `coreutils`（`numfmt`/`stat`/`realpath`）—— 类 Unix 系统通常内置；`numfmt` 缺失会降级为原始字节数显示，不影响功能

---

## Author

**Evan Song** — [github.com/Songhonglei](https://github.com/Songhonglei)

## License

MIT © 2026 Evan Song — see [LICENSE](LICENSE).
