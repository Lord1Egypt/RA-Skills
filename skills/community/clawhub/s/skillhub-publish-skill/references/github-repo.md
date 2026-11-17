# GitHub 建仓与推送

## 第 0 步（最重要）：先确认仓库是否**已经存在**

**别直接建仓。** 2026-09-19 实测踩坑：以为 `oracis/workbuddy-checkin` 是新建，
结果它 **2026-09-02 就存在了**，而且内容比本地 staging 更完整
（多出 `install.ps1` / `install.sh` / `.gitattributes`，skill 本体嵌在子目录里）。
当时若按扁平结构强推，会**删掉两个安装脚本并改掉目录布局**——破坏性操作。

动手前一律先探活：

```bash
gh repo view oracis/<repo> --json name,isEmpty,defaultBranchRef,createdAt,pushedAt,url
# 或（无 gh 时）
curl -o /dev/null -w "%{http_code}\n" -H "Authorization: token $TOKEN" \
  https://api.github.com/repos/oracis/<repo>     # 200 = 已存在；404 = 可以建
```

**已存在时不要 `gh repo create`**（会报 `GraphQL: Name already exists on this account`）。
正确路径：`gh repo clone` → 只改需要改的文件 → commit → push。

```bash
gh repo clone oracis/<repo> work && cd work
# 只动该动的文件，commit 时显式限定路径，别 -A 以免带上无关文件
git -c core.autocrlf=false commit -m "..." -- <相对路径>
```

## 凭据：`gh auth login`（2026-09-19 起已登录，此前结论已废）

**旧结论作废**：本文档曾写「`gh` CLI 没登录，token 只在 `~/.git-credentials`」。
2026-09-19 已完成 `gh auth login`（device flow），现状态：

```bash
gh auth status
# ✓ Logged in to github.com account oracis (keyring), scopes: gist, read:org, repo
```

**`gh` 不读 git 的 `http.proxy` 配置**，所以任何 `gh` 联网命令前必须显式给代理，
否则报 `net/http: TLS handshake timeout`：

```bash
export HTTPS_PROXY=http://127.0.0.1:10808 HTTP_PROXY=http://127.0.0.1:10808
```

device flow 注意点：
- `gh auth login --hostname github.com --git-protocol https --web --skip-ssh-key`
- 必须**长驻后台**跑（前台会被命令超时杀掉），用后台任务方式起。
- **每次重跑都会换新 code** —— 别把上一轮的 code 发给用户。
- code 约 15 分钟过期；完成后输出 `✓ Logged in as <user>`。

（`~/.git-credentials` 里的 `gho_` token 仍在，可作为无 gh 环境的兜底。）

## 推送

remote 用 **SSH**（`git@github.com:oracis/<repo>.git`），push 时**清空代理**绕开本机 git 代理的 TLS 问题：

```bash
git -c http.proxy= -c https.proxy= push -u origin main
```

> ⚠️ `-c` 必须放在子命令 `push` **之前**。
> 写成 `git push ... -c http.proxy=` 会报 usage 错误（git 会把它当成 push 的参数）。

## 验证（别信本地 ref）

本地 `git log origin/main` 可能因 packed-refs 未刷新报：

```
fatal: ambiguous argument 'origin/main': unknown revision or path not in the working tree
```

**这不代表 push 失败。** 以 GitHub API 为准：

```bash
curl -s -H "Authorization: token $TOKEN" \
  https://api.github.com/repos/oracis/<repo>/commits/main \
  | python -c "import sys,json;d=json.load(sys.stdin);print(d['sha'],d['commit']['message'])"
```

比对 `git rev-parse HEAD` 与 API 返回的 `sha` 一致即成功。

## 仓库改名后

旧 clone URL 会 301 重定向到新名，但建议把 manifest `homepage`、ClawHub `--source-repo` 一并改成新名，保持干净。
