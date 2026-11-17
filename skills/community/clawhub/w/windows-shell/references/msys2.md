# MSYS2 参数改写与符号链接

主文件已给出 `MSYS_NO_PATHCONV=1` 这一条速查。需要完整解释、
其它两种绕法、或遇到符号链接/工具缺失问题时读本文。

### 规则 6：MSYS2 会改写以 `/` 开头的参数

Git Bash（MSYS2）在把参数交给 **非 MSYS2 程序**（即所有 Windows 原生 .exe）之前，会把看起来像 Unix 路径的参数自动转换成 Windows 路径。这是 MSYS2 的设计，不是 bug——但它**静默生效**，不报错、退出码正常，参数已经变了。

```bash
node app.js /api/v1/users
# 程序实际收到：D:/Program Files/Git/api/v1/users   ← 前面被拼上了 Git 安装目录

prog /S /C                  # → 变成  S:/ C:/
docker run -v /app:/app ... # → -v 后面的参数被破坏
reg query "HKCU\Environment"   # → 错误: 无效语法。
findstr 中文 /tmp/x.txt        # → FINDSTR: 无法打开 C:x.txt
```

**什么时候会中招**：参数以 `/` 开头，且接收方是 Windows 原生程序。典型场景——REST 路径、Docker 卷映射、Windows 风格开关（`/S` `/C` `/query`）、注册表路径、传给 `.exe` 的 Unix 路径。

**三种解法**（均实测有效）：

```bash
# A. 单条命令临时关闭（推荐，作用域最小）
MSYS_NO_PATHCONV=1 reg query "HKCU\Environment" /v PYTHONUTF8
MSYS_NO_PATHCONV=1 node app.js /api/v1/users

# B. 按参数排除
MSYS2_ARG_CONV_EXCL='*' node app.js /api/v1/users

# C. 双斜杠转义（只想保护单个参数时）
node app.js //api/v1/users
```

**不要全局导出 `MSYS_NO_PATHCONV=1`**：关掉转换后，`/c/Users/...` 这类你确实希望被转成 `C:\Users\...` 的参数也不再转换，会引入另一批问题。按需在单条命令前加。

> 与编码问题的区别：编码问题表现为**乱码**，参数改写表现为**语法错/找不到文件/行为不对但不报错**。诊断时先看报错形态，别拿编码的解法去治路径的病。

### 规则 7：Git Bash 的 `ln -s` 默认产出的是副本

```bash
ln -s t.txt l.txt && ls -l l.txt
# 默认：  -rw-r--r--  ← 普通文件副本，不是链接
```

对普通脚本无所谓，但 **pnpm workspace、npm link、monorepo 的本地依赖都依赖真符号链接**，退化成副本会导致改了源码却不生效、或磁盘占用异常。

```bash
# 修复：产出真正的符号链接（lrwxrwxrwx）
export MSYS=winsymlinks:nativestrict
ln -s t.txt l.txt && ls -l l.txt      # → lrwxrwxrwx ... l.txt -> t.txt
```

Windows 10/11 需先启用**开发者模式**（设置 → 隐私和安全性 → 开发者选项），否则创建符号链接要管理员权限。检查是否已启用：

```bash
powershell -NoProfile -Command '(Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock").AllowDevelopmentWithoutDevLicense'
# 返回 1 = 已启用
```

## 不需要包装的工具

以下工具本身输出 UTF-8，可直接使用：
- `git`、`node`、`npm`、`pnpm`、`bun`、`cargo`、`go`
- bash 内置：`echo`、`cat`、`ls`、`grep` 等
- `python`：加 `-X utf8` 后可直接使用（见规则 4）

> **编码没问题 ≠ 完全没坑**：这些工具的**输出编码**是干净的，但只要给它们传以 `/` 开头的参数，
> 仍会被 MSYS2 改写（见规则 6）；`pnpm` 的 workspace 还依赖真符号链接（见规则 7）。
> 两件事互相独立，别因为「这个工具在白名单里」就放松警惕。
