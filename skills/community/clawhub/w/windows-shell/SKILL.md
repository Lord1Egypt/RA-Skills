---
name: windows-shell
version: 5.3.0
description: "Windows 命令行工作规范：先选对 shell（默认 Git Bash），再避开编码与 MSYS2 参数改写两类陷阱。覆盖 GBK/UTF-8、BOM、MSYS2 路径转换、PowerShell/pwsh、WSL 判定、Python/Node.js、Git 配置与代码生成规则。适用于 Windows 10/11 + MSYS2/Git Bash 环境下的所有命令行操作。细节按需读 references/。"
license: MIT
metadata:
  openclaw:
    emoji: "🪟"
    os: [windows]
    homepage: "https://github.com/Chenmo0414/win-encoding-fix"
---

# Windows 命令行工作规范

用户系统：Windows 10/11（代码页 GBK/936），终端：MSYS2/Git Bash。

**本文件是速查与路由表。** 每条规则下面标了「细读」，只在真正遇到那类问题时再去读对应的
`references/` 文件——不要一次性全部读完。

## 一、先分清是哪一类问题

在 Git Bash 里执行命令出问题，绝大多数是这两类之一。**先判类，再套解法**，两类的解法完全不通用：

| 症状 | 类别 | 第一反应 |
|------|------|------|
| 输出乱码（`涓枃`、`M-DM-c`、方块字） | **编码** | 让源头输出 UTF-8 |
| 没报错但**结果就是不对**（参数变了值、行数少一行） | **静默失败** | 见第 1、3 条，必须交叉验证 |
| 报「无效语法 / invalid / 找不到文件」，或参数悄悄变了值 | **MSYS2 参数改写** | `MSYS_NO_PATHCONV=1` |

拿编码的解法去治参数改写，怎么加前缀都不好使——这是最常见的误诊。

## 二、选对 shell（默认 Git Bash）

| 你要做的事 | 用哪个 |
|------|------|
| npm / node / npx / tsc / vitest / python / pip / pytest / git / ssh | **Git Bash** |
| Windows 服务、注册表、事件日志、计划任务、证书、.NET/COM、对象管道 | **PowerShell**（单条命令切过去，主线不搬家） |
| 跑 Makefile、需要 gcc/rsync，或重 I/O 构建且项目能整个搬进 ext4 | **WSL** |
| 需要管理员权限 | **交给人做**——UAC 弹窗 agent 点不了，命令会一直挂着 |

项目文件在 `C:\`/`D:\` 上时，**不要用 WSL 去操作它**：跨 `/mnt/*` 比纯 Windows 还慢 4–6 倍，
且惩罚随项目规模线性放大。

> 细读：判断依据与完整决策表 → [shell-routing.md](references/shell-routing.md)；
> WSL 值不值得上 → [wsl.md](references/wsl.md)

## 三、必须知道的六条

下面六条是实测中真正拉开差距的。其余规则都在 `references/`。

### 1. 以 `/` 开头的参数会被静默改写

Git Bash 把它当 Unix 路径转成 Windows 路径再传给原生程序。**不报错、退出码 0、参数已经变了**：

```bash
node app.js /api/v1/users          # 程序实收 D:/Program Files/Git/api/v1/users
docker run -v /app:/app ...        # -v 后面被吃掉
reg query "HKCU\Environment"       # 错误: 无效语法。
```

```bash
MSYS_NO_PATHCONV=1 node app.js /api/v1/users    # 单条前置，不要全局导出
```

全局导出会让 `/c/Users/...` 这类本该转换的参数也不转。

> 细读：另两种绕法、符号链接退化 → [msys2.md](references/msys2.md)

### 2. PowerShell 5.1 输出中文必须加前缀

```bash
powershell -Command '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; 你的命令'
```

外层用**单引号**（防 bash 展开 `$_`、`$null`）。pwsh 7 不需要这个前缀，加了也无害。
外部程序（node/python）自己写的 UTF-8 穿过 PowerShell 不会被改。

### 3. 读遗留文件前先验编码，别硬套 UTF-8

对一个真正的 GBK/936 文件强加 `-Encoding UTF8` 会读出乱码。先看字节再决定：

```bash
od -c legacy.txt | head -2        # 或 xxd；Git Bash 没有 hexdump
```

| 文件真实编码 | PS 5.1 | pwsh 7 |
|------|------|------|
| UTF-8 | `-Encoding UTF8`（**必须显式写**） | 默认即可 |
| GBK/936 | `-Encoding Default` | `[System.Text.Encoding]::GetEncoding(936)` |

**PS 5.1 读无 BOM 的 UTF-8 不加 `-Encoding UTF8` 会静默出错**——不是乱码那么显眼，
而是行数直接算错、退出码仍为 0。实测：一个 3 行的 UTF-8 文件，某行末尾字节是
`a1 8c 0a`，PS 按 GBK 把 `8c` 当双字节前导、吞掉紧随的换行，`Get-Content` 返回
**2 行**且 `$?` 为 `True`。性质与上面第 1 条的参数改写相同：**结果错、不报错**。
所以 **PS 5.1 读任何文本文件都显式指定 `-Encoding`**，别赌默认值。

**含中文的 `.ps1` 脚本文件必须存成 UTF-8 with BOM**。PS 5.1 读脚本时没有 BOM 就按
ANSI/GBK 解析，中文字面量被拆错——而且多数情况**不报错**：

```
同一段 $s = "腾讯"，只差 BOM：
  PS 5.1 无 BOM  →  $s.Length = 3   ✗   字符串在内存里是 3 个错字符
  PS 5.1 有 BOM  →  $s.Length = 2   ✓
```

最阴险的是 `Write-Output $s` **打印出来是对的**——脚本按 GBK 误读、输出时又按 GBK 编码，
两次错误相互抵消。但凡是取长度、截取、正则、比较、哈希的地方全是错的。
（历史会话里这条也会以 `Unexpected token '鑵捐'` 的语法错形式爆出来，那只是误读的字节
恰好构成非法 token 的少数情况。）pwsh 7 默认按 UTF-8 读脚本，无此问题。

**只影响脚本文件，不影响命令行参数。** 中文直接写在 `-Command '...'` 里是安全的：

```bash
powershell -NoProfile -Command '$s="中文测试"; Write-Output $s.Length'   # → 4，正确
```

这条容易被反向误判——实测有 agent 因为担心参数被 ANSI 吃掉，绕道去写带 BOM 的 `.ps1`，
白花两条命令。**要 BOM 的是脚本文件，`-Command` 参数不用。**

**写出去也有坑**：PS 5.1 的 `-Encoding UTF8` 会带 BOM，`>` 重定向默认写 UTF-16。要无 BOM 的 UTF-8：

```powershell
[System.IO.File]::WriteAllText("out.txt", $s, (New-Object System.Text.UTF8Encoding($false)))
```

> 细读：更多 BOM/重定向陷阱、`$OutputEncoding`、传统 CMD 工具替代表
> → [encoding.md](references/encoding.md)

### 4. Git Bash 少几个你以为有的工具

`iconv`、`jq`、`make`、`gcc`、`rsync`、`hexdump` **都没有**。转码不要指望 `iconv`，
验字节用 `od -c`，其余场景改用 Python 或 Node 顶上；真需要完整 GNU 工具链就上 WSL。

```bash
python -c "import io;io.open('out.txt','w',encoding='utf-8').write(io.open('in.txt',encoding='gbk').read())"
```

### 5. 生成代码时显式写编码，不依赖环境

```python
open('data.txt', encoding='utf-8')          # 裸 open() 在 Windows 上默认 cp936
```

```bash
python -X utf8 -c "..."                      # 单行命令，不假设 PYTHONUTF8 已生效
```

环境变量会失效，代码里的显式声明不会。

### 6. venv 直接调解释器，绕开 activate

```bash
./.venv/Scripts/python.exe -m pytest         # source activate 会拼出正反斜杠混拼的畸形路径
```

同理，管道会吞掉上游退出码，要用 `set -o pipefail` 或 `${PIPESTATUS[0]}`。
**但 `PIPESTATUS` 会被下一条命令重置——包括赋值语句本身**：

```bash
cmd | tail -1; a=${PIPESTATUS[0]}; b=${PIPESTATUS[1]}   # ✗ b 恒为 0，赋值 a 就把数组冲了
cmd | tail -1; st=("${PIPESTATUS[@]}")                  # ✓ 紧邻、一次取完
echo "上游=${st[0]} 下游=${st[1]}"
```

实测：`(exit 7) | tail -1` 后紧邻读得 7；中间隔一条命令再读得 0。

> 细读：venv、工具集不全、SSH 密钥、符号链接 → [gitbash-pitfalls.md](references/gitbash-pitfalls.md)

## 四、一次性环境配置

```bash
powershell -Command '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8;
  [Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User");
  [Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")'
git config --global core.quotepath false
git config --global core.autocrlf input
```

写进 `~/.bash_profile` 的变量**非登录 shell 不会加载**（agent 正是这种 shell），
所以要设成 Windows 用户级环境变量。

> 细读：完整配置与每条的理由 → [encoding.md](references/encoding.md) 的「环境前置条件」

## 五、按需索引

| 遇到什么 | 读哪个 |
|------|------|
| 乱码、BOM、UTF-16、GBK 遗留文件、CMD 工具替代 | [encoding.md](references/encoding.md) |
| 参数被改写、符号链接变成副本 | [msys2.md](references/msys2.md) |
| 不确定该用哪个 shell、想看实测依据 | [shell-routing.md](references/shell-routing.md) |
| venv、工具缺失、SSH 密钥、管道退出码 | [gitbash-pitfalls.md](references/gitbash-pitfalls.md) |
| 要不要上 WSL、`wsl.exe` 变量吞噬 | [wsl.md](references/wsl.md) |
