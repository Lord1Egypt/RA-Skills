---
name: safe-git-push
description: 从 agent 工作区安全推送文件到 GitHub。父级 git 仓库场景下隔离 init,防止敏感配置文件、构建产物目录、其他无关项目子目录被误推。触发:用户说「上传到 GitHub」「推到 GitHub」「创建 GitHub 仓库」「备份项目到 GitHub」,或 OpenClaw 沙箱内 git push 超时需走 Contents API fallback。
---

# Safe git push from shared workspace

## 适用场景

- 用户要求把当前目录（或其中若干文件）推到 GitHub / GitLab / Bitbucket
- 当前工作目录可能位于一个**父级 git 仓库**内（典型：OpenClaw 的 `~/.openclaw/workspace/` 本身就是 git 仓库, 里面有 `.env` / `skills/` / `node_modules/` / 其他项目目录等大量未跟踪敏感文件)
- 用户没有明确指定独立仓库路径

## 红线（必读）

**不要**直接在当前目录 `git add .` 然后 push. 父级仓库会被污染, 可能把 `.env` (密钥)、`node_modules/` (几百 MB 噪声)、其他无关项目一起推到 GitHub, 后果包括:

- 私密凭证泄露（`.env`, `.aws/`, `~/.ssh/` 误包含）
- 仓库变噪声（几千个无关文件）
- 难以清理（GitHub 上推过就有 commit 历史）

## 工作流（4 步）

### Step 1：探测当前 git 状态

```bash
cd <target_dir>
git rev-parse --is-inside-work-tree     # true = 在某个 git 仓内
git rev-parse --show-toplevel           # 真正的 git 根
git status --short | wc -l              # 未跟踪文件数量
git remote -v                           # 是否已有远端
```

判断:
- `toplevel` == `target_dir` → 目录本身就是独立仓库, 可直接用
- `toplevel` ≠ `target_dir` → 目录在**父级仓库内**, 必须隔离（见 Step 2）

### Step 2：隔离（父级子目录场景）

在子目录内独立 `git init`, 不污染父级:

```bash
cd <target_dir>
git init -b main                       # 或 master, 对齐目标平台
```

**只 `git add` 你要追踪的文件**（永远不要 `git add .`）:

```bash
git add file1 file2 file3 ...          # 显式列出
git status --short                     # 复核
```

最小 `.gitignore`（Python 项目起步）:

```gitignore
__pycache__/
*.pyc
.DS_Store
.vscode/
.idea/
.vs/
*.tmp
```

### Step 3：创建远程仓库

```bash
gh repo create <repo-name> --private --description "..." 
# 注：--confirm 在 gh 2.0+ 已废弃, 任何额外参数(如 --private)即跳过确认
```

也可走网页手动建仓, 然后 `git remote add` 即可.

### Step 4：推送

```bash
git remote add origin https://github.com/<user>/<repo>.git
git commit -m "Initial commit: ..."
git push -u origin main
```

推送后用 `gh repo view <user>/<repo> --json isPrivate,pushedAt` 或网页确认.

### Step 5 (fallback): `git push` 被反复 SIGTERM 杀掉时

**触发条件**（必须先有 2 次以上 SIGTERM 失败才换路径, 避免误诊）:
- `git push` 命令被 sandbox 超时中断（无错误输出就结束）
- `gh api repos/<user>/<repo>/contents` 返回 `"This repository is empty"` 404
- 本地 commit 存在, 但远端 `main` 分支仍是空
- `gh repo view ... --json pushedAt` 显示的时间戳其实是 `gh repo create` 时的, **不是 push 成功的证据**——不要被这个字段误导

**原因**: OpenClaw sandbox 大约 30s 杀长进程。`git push` 上传含图、PDF、docx 的仓库一定会超时, HTTPS / SSH / 带 token URL 三种鉴权方式都同样被杀。

**修复路径**: 用 **GitHub Contents API** (`gh api -X PUT`) 逐文件上传, 走普通 HTTPS POST, 单请求小不会触发超时:

```bash
# payload.json 模板（每个文件一份）
{
  "message": "upload <file>",
  "branch": "main",
  "content": "<base64 编码的文件内容>"
}

# 二进制文件 (PNG/DOCX/PDF): Python 生成
python3 -c "import base64,json; print(json.dumps({'message':'upload x.png','branch':'main','content':base64.b64encode(open('x.png','rb').read()).decode()}))"

# 文本文件 (.md / .py / .json): 直接原文 (注意 JSON 字符串内换行需 \\n 转义)
gh api -X PUT repos/<user>/<repo>/contents/<path> --input payload.json
```

**为什么这个路径可靠**:
- 每次单 HTTP POST, 请求体积小, 不会被 sandbox 超时杀
- **幂等**: 重复 PUT 同一文件返回 422 no-op, 被打断的部分文件不会丢, 重跑即可补齐
- 不需要 git 协议, 不需要 SSH key 配置

**为什么不选这些替代方案**:
- `gh repo sync` —— 要求远端**已有** main 分支, 首次推送时是空仓库, 不能用
- `gh repo push` —— 该子命令在 gh CLI 中**不存在**
- `git push https://x-access-token:TOKEN@github.com/...` —— 仍走 git 协议, 同样被杀

**完成后验证**:
```bash
gh api repos/<user>/<repo>/contents --jq 'if type == "array" then [.[].name] else .message end'
```
返回数组 = 推送成功; 返回 `"This repository is empty"` = 还没推完, 重跑脚本。

## 关键避坑

1. **`git add .` 是高危** —— 永远显式列出要追踪的文件, 或至少用 `git add <file>` 加 `git status --short` 复核
2. **父级仓库探测必须做** —— `git rev-parse --show-toplevel` 输出不等于当前目录就是隔离信号
3. **`.gitignore` 别忘** —— 至少屏蔽常见噪声: `__pycache__/` / `.DS_Store` / 编辑器配置 / 大目录（`node_modules/` / `venv/` / `.venv/` / `dist/` / `build/`）
4. **gh CLI `--confirm` 已废弃** —— 不要照旧教程写, 会报错
5. **默认分支对齐** —— GitHub 2020 后默认 `main`; 老仓库可能是 `master`, 推送前先 `git branch --show-current` 看
6. **敏感文件最后一道防线** —— 推送前 `git status --short` + 抽查文件列表, 确认没有 `.env` / `*.key` / `*secret*` / `id_rsa` 等
7. **`git push` 在 OpenClaw sandbox 常被 SIGTERM 杀掉** —— 含图/PDF/docx 的仓库必超时。多次失败后改走 Step 5 的 Contents API fallback; 不要被 `gh repo view --json pushedAt` 的时间戳误导（那是 `gh repo create` 时写入的, 不是 push 成功的证据）

## 完整最小示例（典型场景）

```bash
# 1. 探测
cd /home/lv/.openclaw/workspace/my-project
git rev-parse --show-toplevel
# → /home/lv/.openclaw/workspace  ← 与 target_dir 不同, 需隔离

# 2. 隔离
git init -b main
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.DS_Store
EOF
git add README.md src/  # 显式列出
git status --short       # 复核
git commit -m "Initial commit"

# 3+4. 创建并推送
gh repo create my-project --private --description "..."
git remote add origin https://github.com/<user>/my-project.git
git push -u origin main
```

## 完成标准

- [ ] 已确认目标目录 git 状态（独立仓库 vs 父级子目录）
- [ ] 父级子目录场景下已独立 `git init`
- [ ] `git status --short` 显示的文件就是要追踪的全部（无 `.env` / `node_modules` / 其他项目文件）
- [ ] `.gitignore` 至少覆盖 `__pycache__/` / `.DS_Store` / 编辑器配置
- [ ] 远端仓库已创建（明确公开/私有）
- [ ] push 成功, 已拿到仓库 URL 并交付用户

## 不适用

- 用户明确说「在当前仓库加个目录」 → 走标准 `git add <dir>`, 不需要隔离
- 用户明确说「推送到这个具体仓库」且已配置 remote → 直接 push, 不需要新仓库
- 工作目录不是父级仓库的子目录（如 `/tmp/project`） → 可直接 init, 但仍避免 `git add .`

## 关联技能

- `sandbox-web-fetch` —— 同在 OpenClaw sandbox 下, 但管的是**从公网拉**内容; push 走 Contents API, fetch 走 curl/tarball
- `openclaw-credential-injection` —— push 通常不需要 LLM key, 但若脚本里要调用 OpenAI/DeepSeek 等 LLM 做 release notes / commit message 润色, 用本技能接 key
