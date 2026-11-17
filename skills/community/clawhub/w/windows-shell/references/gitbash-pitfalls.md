# Git Bash 的五个坑

在 Git Bash 下遇到非编码类异常时读本文：参数被改写、符号链接失效、
venv 激活路径异常、工具缺失、SSH 密钥不通用、管道吞退出码。

## Git Bash 的五个坑

选了 Git Bash，这五个必须知道，否则会以为是代码的问题。

### 坑 1：以 `/` 开头的参数会被改写（静默）

MSYS2 把它们当 Unix 路径转成 Windows 路径再传给程序。**不报错、退出码正常、参数已经变了**：

```bash
node app.js /api/v1/users     # 程序收到 D:/Program Files/Git/api/v1/users
prog /S /C                    # → S:/ C:/
docker run -v /app:/app ...   # -v 后面被吃掉
```

```bash
# 解法：单条命令前置，别全局导出
MSYS_NO_PATHCONV=1 node app.js /api/v1/users
```

全局导出会让 `/c/Users/...` 这类你确实希望被转换的参数也不转了。

### 坑 2：`ln -s` 默认产出的是副本

```bash
ln -s t.txt l.txt && ls -l l.txt      # -rw-r--r--  ← 是副本，不是链接
export MSYS=winsymlinks:nativestrict  # 修复后 → lrwxrwxrwx
```

**pnpm workspace、npm link、monorepo 本地依赖都依赖真符号链接**，退化成副本会表现为「改了源码不生效」。需先启用 Windows 开发者模式。

### 坑 3：venv 的 `activate` 会拼出畸形路径

```bash
source .venv/Scripts/activate    # VIRTUAL_ENV 丢盘符，路径变成 /d/proj/\proj\.venv/Scripts/python
```

虽然仍能解析，但不可靠。**直接调解释器，绕开 activate**：

```bash
./.venv/Scripts/python.exe -m pytest
./.venv/Scripts/python.exe -m pip install -r requirements.txt
```

### 坑 4：工具集不全

`jq`、`make`、`gcc`、`rsync` 都**没有**。跑 Makefile 的项目直接卡住——那种情况上 WSL，不要试图在 Git Bash 里凑。

### 坑 5：SSH 密钥位置与 WSL 不通用

Git Bash 与 Windows 共用 `C:\Users\你\.ssh`，**WSL 用的是独立的 `/root/.ssh`**。在 Windows 配好的 SSH，到 WSL 里等于从零开始。

而且 `/mnt/*` 上的文件在 WSL 眼里权限是 `777`，OpenSSH 会判定 `bad permissions` 直接忽略该密钥。要在 WSL 里用 ssh，密钥必须复制到 ext4 并 `chmod 600`。Git Bash 没有这个问题（它走 Windows ACL，不看 POSIX 权限位）。

### 附：管道会吞掉退出码

这不是 Git Bash 特有，但 agent 最容易在这里误判成功：

```bash
npm install ... | tail -25      # $? 是 tail 的，不是 npm 的
set -o pipefail                 # 或用 ${PIPESTATUS[0]}
```
