---
name: windows-shell
version: 4.1.0
description: "Windows 命令行编码与兼容性规范。覆盖 GBK/UTF-8 编码、PowerShell/pwsh 互操作、Python/Node.js、Git 配置、代码生成规则。适用于 Windows 10/11 + MSYS2/Git Bash 环境下的所有命令行操作。"
metadata:
  openclaw:
    emoji: "🪟"
    os: [windows]
    homepage: "https://github.com/Chenmo0414/win-encoding-fix"
---

# Windows 命令行编码规范

用户系统：Windows 10/11（代码页 GBK/936），终端：MSYS2/Git Bash。以下规则均在真实 GBK 环境逐条实测验证。

## 为什么会乱码（一句话原理）

终端按 **UTF-8** 解码字节流，但 Windows 原生程序（PowerShell 5.1、CMD 工具、默认 Python）按 **GBK/936** 输出中文。字节被错误解码 → 乱码（如 `涓枃`、`M-DM-c`）。修复 = 让源头输出 UTF-8。

## 快速参考

| 场景 | 做法 |
|------|------|
| 执行 PowerShell 命令 | `powershell -Command '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; ...'` |
| PowerShell 中有 `$_`/`$null` | 外层用**单引号**，防止 bash 展开 |
| PowerShell 读文件 | 加 `-Encoding UTF8`（pwsh 7 默认即 UTF-8，可省） |
| 执行系统查询 | 用 `Get-CimInstance` 替代 `wmic` |
| 执行 Python 单行命令 | 加 `-X utf8`：`python -X utf8 -c "..."`（**不要假设** `PYTHONUTF8` 已生效） |
| 生成 Python 代码 | `open()` 必须带 `encoding='utf-8'` |
| Node.js 调系统命令 | execSync 中用 PowerShell 包装 |
| Git 中文文件名乱码 | 确认 `core.quotepath=false` |
| 传统 CMD 工具 | **禁止直接使用**，全部走 PowerShell |

## 环境自检（开工前可选执行）

判断当前 shell 的编码是否已正确配置：

```bash
python -c "import sys; print('utf8_mode=', sys.flags.utf8_mode)"   # 期望 1；为 0 说明 Python 默认 GBK
echo "PYTHONUTF8=$PYTHONUTF8"                                       # 期望 1；为空说明环境变量未加载
```

**关键认知**：`PYTHONUTF8` 等变量若只写在 `~/.bash_profile`，**非登录 / 非交互 shell 不会加载它**（AI 助手与脚本通常正是这种 shell）。因此：

- 持久生效请配置 **Windows 用户级环境变量**（被所有进程继承，重启终端后生效）；
- 当前会话内最可靠的做法是**每条命令显式带编码参数**（见下方各规则）。

## 环境前置条件（持久配置，建议一次性执行）

```bash
# 1) Windows 用户级环境变量 —— 最可靠，所有进程继承（重启终端后生效）
powershell -Command '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8;
  [Environment]::SetEnvironmentVariable("PYTHONUTF8", "1", "User");
  [Environment]::SetEnvironmentVariable("PYTHONIOENCODING", "utf-8", "User")'

# 2) bash 显示相关变量（登录 shell 用），并让 .bashrc 也加载，覆盖非登录交互 shell
cat >> ~/.bash_profile <<'EOF'
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
export LANG=en_US.UTF-8
export LESSCHARSET=utf-8
EOF
grep -q 'bash_profile' ~/.bashrc 2>/dev/null || echo '[ -f ~/.bash_profile ] && . ~/.bash_profile' >> ~/.bashrc

# 3) Git 全局配置
git config --global core.quotepath false        # 中文文件名正常显示
git config --global core.autocrlf input         # 提交 LF，检出保持原样
git config --global i18n.commitEncoding utf-8    # commit 消息 UTF-8
git config --global i18n.logOutputEncoding utf-8
git config --global core.pager "less -R"
```

> 一键配置：`npx win-encoding-fix install --setup-env`

## Shell 命令规则

### 规则 1：PowerShell 命令必须加 UTF-8 前缀 + 外层单引号

```bash
# 标准模板（外层单引号 + UTF-8 前缀）
powershell -Command '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; 你的命令'
```

**两个要点必须同时满足：**
- `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` — 不加则中文输出乱码
- 外层**单引号** — 防止 bash 把 `$_`、`$null` 当作 bash 变量展开

仅当命令中不含 `$` 变量时才可用外层双引号。

**关于 pwsh（PowerShell 7）**：若系统装有 `pwsh`（`which pwsh` 可检测），它读写文件默认即 UTF-8，但**输出到管道仍可能因控制台代码页而乱码**（实测不稳定）。因此 pwsh 同样建议带上述前缀——前缀对 pwsh 无害、对 5.1 必需，统一加最省心。

### 规则 2：PowerShell 读文件必须指定 UTF-8

```bash
powershell -Command '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-Content "path\file.txt" -Encoding UTF8'
```

PowerShell 5.1 不加 `-Encoding UTF8` 会用 GBK 读取 UTF-8 文件（实测 `中文` → `涓枃`）。写文件同理用 `Set-Content -Encoding UTF8`。pwsh 7 默认 UTF-8 可省此参数，但加上无害。

### 规则 3：禁止直接使用传统 CMD 工具和 cmd /c

传统 CMD 工具输出 GBK 或 UTF-16，在 UTF-8 终端中全部乱码。`cmd /c` 同样不可用——`chcp 65001` 无法修复子进程编码（实测 `cmd /c "chcp 65001 & echo 你好"` 仍乱码）。

**必须使用 PowerShell 替代：**

| 禁止 | 替代 |
|------|------|
| `wmic` | `Get-CimInstance` |
| `systeminfo` | `Get-ComputerInfo` 或 PS 包装 `systeminfo` |
| `ipconfig` | `Get-NetIPAddress` / `Get-NetIPConfiguration` |
| `netstat` | `Get-NetTCPConnection` |
| `tasklist` | `Get-Process` |
| `sc query` | `Get-Service` |
| `reg query` | `Get-ItemProperty 'HKLM:\...'` |
| `net user` | `Get-LocalUser` |
| `schtasks` | `Get-ScheduledTask` |
| `findstr` | `Select-String` |
| `cmd /c` | **永远不用** |

在 PowerShell 中包装传统命令也可正确转码：
```bash
powershell -Command '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; systeminfo | Select-Object -First 5'
```

### 规则 4：Python 命令行执行 —— 优先 `-X utf8`，不要假设环境

实测：AI 助手与脚本运行在**非交互 shell**，`~/.bash_profile` 中的 `PYTHONUTF8` 不会被加载，`sys.flags.utf8_mode` 仍为 0，`python -c "print('你好')"` 直接乱码。

**最可靠做法 —— 单行命令显式带 `-X utf8`：**
```bash
python -X utf8 -c "print('你好世界')"
# 或临时设环境变量
PYTHONUTF8=1 python script.py
```

`-X utf8` 同时让 `print()` 输出与 `open()` 默认读写都走 UTF-8，幂等无副作用，已是 UTF-8 环境时加它也不会出错。**生成代码时**仍应显式写 `encoding='utf-8'`（见规则 6），不依赖运行时标志。

### 规则 5：Node.js 子进程调用系统命令

Node.js 自身输出 UTF-8 没问题，但 `execSync`/`exec`/`spawn` 调用传统 CMD 工具时，输出是 GBK，`toString('utf-8')` 会乱码。

**修复**：让子进程通过 PowerShell 输出 UTF-8：
```javascript
execSync('powershell -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; systeminfo"').toString('utf-8')
```

## 代码生成规则

AI 生成代码时必须遵循以下规则，确保产出的代码在 Windows 上编码正确。

### 规则 6：Python 文件 I/O 必须指定编码

```python
# 正确 — 显式指定 encoding
with open('data.txt', 'r', encoding='utf-8') as f:
    content = f.read()

with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(content)

# 错误 — 裸 open() 在 Windows 上默认 GBK（实测 locale.getpreferredencoding() = cp936）
with open('data.txt', 'r') as f:  # 不要这样写
    content = f.read()
```

同样适用于 `json.load`/`json.dump`、`csv.reader`、`pathlib.Path.read_text()` 等需要文件对象的场景。

Python subprocess 调用系统命令时也需注意编码：
```python
import subprocess
result = subprocess.run(
    ['powershell', '-Command', '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-Process'],
    capture_output=True, text=True, encoding='utf-8'
)
```

### 规则 7：Node.js 文件操作和子进程编码

```javascript
// 文件读写 — 显式指定 utf-8
fs.readFileSync('data.txt', 'utf-8')
fs.writeFileSync('output.txt', content, 'utf-8')

// 子进程调用 Windows 原生命令 — 通过 PowerShell 包装
const { execSync } = require('child_process')
const output = execSync(
  'powershell -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-Service"'
).toString('utf-8')
```

### 规则 8：Git 中文支持

环境已配置 `core.quotepath=false`，中文文件名在 `git status`/`git diff` 中正常显示。

如果发现中文文件名仍显示为 `\346\265\213\350\257\225` 形式，执行：
```bash
git config --global core.quotepath false
```

## 格式化技巧

- 宽表格加 `| Out-String -Width 200` 防截断
- `Format-Table -AutoSize` 自适应列宽
- `Format-List` 展示详细单条记录
- `Select-Object` 控制返回字段数量

## 不需要包装的工具

以下工具本身输出 UTF-8，可直接使用：
- `git`、`node`、`npm`、`pnpm`、`bun`、`cargo`、`go`
- bash 内置：`echo`、`cat`、`ls`、`grep` 等
- `python`：加 `-X utf8` 后可直接使用（见规则 4）
