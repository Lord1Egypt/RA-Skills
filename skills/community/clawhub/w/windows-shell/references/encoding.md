# 编码细节（GBK / UTF-8 / BOM）

主文件 `SKILL.md` 只放了最常用的两条。遇到下列任一情况时读本文：
读写文件出现乱码、需要处理 GBK 遗留文件、需要写无 BOM 的 UTF-8、
PowerShell 重定向编码不对、管道方向的编码问题、传统 CMD 工具输出乱码。

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

> 一键配置：在 [skill-factory](https://github.com/Chenmo0414/win-encoding-fix) 仓库里执行 `node bin/cli.js setup-env`

### 规则 1：PowerShell 命令必须加 UTF-8 前缀 + 外层单引号

```bash
# 标准模板（外层单引号 + UTF-8 前缀）
powershell -Command '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; 你的命令'
```

**两个要点必须同时满足：**
- `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8` — 不加则中文输出乱码
- 外层**单引号** — 防止 bash 把 `$_`、`$null` 当作 bash 变量展开

仅当命令中不含 `$` 变量时才可用外层双引号。

**前缀到底什么时候必需**（v4.3.0 实测，各采样 12 次，结果完全稳定）：

| 中文的来源 | PS 5.1 无前缀 | PS 5.1 加前缀 | pwsh 7 无前缀 |
|------|------|------|------|
| PowerShell 自己产出（`Write-Output`、cmdlet 结果） | **GBK ×12 → 乱码** | UTF-8 ×12 ✅ | **UTF-8 ×12 ✅** |
| 外部程序产出（`node -e`、`python` 等） | UTF-8 ×12 ✅ | UTF-8 ×12 ✅ | UTF-8 ×12 ✅ |

- **PS 5.1 必须加前缀**：只要中文由 PowerShell 自己产出，不加就是稳定乱码，没有侥幸。
- **pwsh 7 不需要前缀**：实测 12/12 稳定 UTF-8。加了无害，脚本要兼容 5.1 时统一加是合理的，但不必因为「怕 pwsh 不稳」而加。
- **外部程序的输出不受影响**：`node`/`git`/`python` 自己写 UTF-8 到 stdout，穿过 PowerShell 不会被改。所以「PS 包装」只对遵守控制台代码页的 Windows 原生工具才有意义（见规则 3）。

### 规则 2：PowerShell 读写文件 —— `-Encoding` 必须匹配文件真实编码

**读 UTF-8 文件**：PowerShell 5.1 不加 `-Encoding UTF8` 会用 GBK 读取，实测 `中文` → `涓枃`。

```bash
powershell -Command '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; Get-Content "path\file.txt" -Encoding UTF8'
```

**⚠️ 读 GBK 遗留文件（本机最常见）**：反过来，对一个真正的 GBK/936 文件强加 `-Encoding UTF8` 会**读出乱码**。`-Encoding` 的值必须等于文件的真实编码：

| 文件真实编码 | PS 5.1 读法 | pwsh 7 读法 |
|------|------|------|
| UTF-8 | `-Encoding UTF8` | 默认即可（或 `-Encoding utf8`） |
| GBK/936（遗留） | `-Encoding Default` 或不加 | `-Encoding oem` 或 `[System.Text.Encoding]::GetEncoding(936)` |

pwsh 7 默认按 UTF-8 读，遇到 GBK 文件反而会 mojibake，此时**必须显式指定 936**。

**写文件的 BOM 陷阱**：PS 5.1 的 `Set-Content -Encoding UTF8` / `Out-File -Encoding UTF8` 会写入 **UTF-8 BOM**（`EF BB BF`），很多工具（旧编译器、某些 JSON 解析器、shell 脚本）会因此报错。要写**无 BOM** UTF-8：

```powershell
# PS 5.1 无 BOM 写法
[System.IO.File]::WriteAllText("out.txt", $content, (New-Object System.Text.UTF8Encoding($false)))
# pwsh 7
Set-Content out.txt -Value $content -Encoding utf8NoBOM
```

**输出重定向的编码**：PS 5.1 的 `>` 和 `Out-File` **默认写 UTF-16 LE**，不是 UTF-8。若要把命令输出存成 UTF-8 文件给后续读取，务必显式 `... | Out-File -Encoding utf8 out.txt`（注意上面的 BOM 说明），或捕获字符串后用 .NET 写。

**stdin / 管道方向**：`[Console]::OutputEncoding` 只管 PowerShell **输出**。若要把 UTF-8 内容通过管道**喂进** PowerShell（`echo ... | powershell ...`），还需 `[Console]::InputEncoding = [System.Text.Encoding]::UTF8`；而 PowerShell **管道给下游原生命令**（如 `... | findstr`）用的是 `$OutputEncoding` 变量（默认 ASCII，会丢中文）。能用内联 `-Command` 参数就别走 stdin 管道。

### 规则 3：禁止直接使用传统 CMD 工具和 cmd /c

传统 CMD 工具多数输出 GBK 或 UTF-16，在 UTF-8 终端中乱码。`cmd /c` 同样不可用——`chcp 65001` 无法修复子进程编码（实测 `cmd /c "chcp 65001 & echo 你好"` 仍乱码）。

但**并非全都是编码问题**。实测把它们分成了两类，解法完全不同：

**A 类 —— 真·编码问题**（实测输出 GBK 字节，PS 包装可解决）：

| 禁止 | 替代 |
|------|------|
| `wmic` | `Get-CimInstance` |
| `systeminfo` | `Get-ComputerInfo` 或 PS 包装 `systeminfo` |
| `ipconfig` | `Get-NetIPAddress` / `Get-NetIPConfiguration` |
| `netstat` | `Get-NetTCPConnection` |
| `tasklist` | `Get-Process` |
| `net user` | `Get-LocalUser` |
| `sc query` | `Get-Service`（英文输出时不乱码，但中文服务名会） |
| `cmd /c` | **永远不用** |

**B 类 —— 其实是 MSYS2 参数改写，不是编码问题**（实测：加 `MSYS_NO_PATHCONV=1` 后原命令即可正常工作）：

| 命令 | 默认失败表现 | 真实原因 |
|------|------|------|
| `reg query "HKCU\Environment"` | `错误: 无效语法。` | 注册表路径被当成 Unix 路径改写 |
| `findstr 中文 /tmp/x.txt` | `FINDSTR: 无法打开 C:x.txt` | `/tmp/x.txt` 被改写成 `C:x.txt` |
| `schtasks /query /tn "\..."` | 参数错误 | 同上 |

B 类仍然**建议**换成 `Get-ItemProperty` / `Select-String` / `Get-ScheduledTask`——PowerShell 版本输出更结构化、也不受 MSYS2 影响。但要知道：**它们不是「因为乱码」才被禁的**，误诊会让你在别处用错解法（比如给一个路径被改写的命令拼命加编码前缀，怎么加都不好使）。

在 PowerShell 中包装传统命令**通常**可正确转码：
```bash
powershell -Command '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; systeminfo | Select-Object -First 5'
```

> **注意，包装不是万能的**：`[Console]::OutputEncoding` 只对**遵守控制台输出代码页**的工具有效（`systeminfo`、`ipconfig` 等）。对于**输出固定 GBK 字节或原始字节**的工具（部分第三方 CLI、某些日志），包装后仍是乱码——这类需要「先按 936 解码、再转 UTF-8」：`powershell -Command '$s = (& some.exe) ; [Console]::OutputEncoding = [System.Text.Encoding]::UTF8; [System.Text.Encoding]::GetEncoding(936).GetString(...)'`，或在 Node/Python 侧以**字节**捕获再按真实编码解码（见规则 5、规则 9）。

### 规则 4：Python 命令行执行 —— 优先 `-X utf8`，不要假设环境

实测：AI 助手与脚本运行在**非交互 shell**，若 `PYTHONUTF8` 只写在 `~/.bash_profile`，它不会被加载，`sys.flags.utf8_mode` 为 0，`python -c "print('你好')"` 直接乱码。

**注意前提**：一旦按上文「环境前置条件」把 `PYTHONUTF8` 配成了 **Windows 用户级环境变量**，裸 `python -c "print('你好')"` 就已经正常了（实测 `utf8_mode=1`、`getpreferredencoding=utf-8`）。所以 `-X utf8` 的价值不是「不加就一定乱码」，而是**不依赖环境是否配好**——在别人的机器、CI、容器里同样成立。这也正是它值得默认带上的理由。

反证：把 `PYTHONUTF8` 清空后再测，`getpreferredencoding` 立刻退回 `cp936`。环境配置是会失效的，代码里的显式声明不会。

**最可靠做法 —— 单行命令显式带 `-X utf8`：**
```bash
python -X utf8 -c "print('你好世界')"
# 或临时设环境变量
PYTHONUTF8=1 python script.py
```

`-X utf8` 同时让 `print()` 输出与 `open()` 默认读写都走 UTF-8，幂等无副作用，已是 UTF-8 环境时加它也不会出错。**生成代码时**仍应显式写 `encoding='utf-8'`（见规则 8），不依赖运行时标志。

### 规则 5：Node.js 子进程调用系统命令

Node.js 自身输出 UTF-8 没问题，但 `execSync`/`exec`/`spawn` 调用传统 CMD 工具时，输出是 GBK，`toString('utf-8')` 会乱码。

**修复**：让子进程通过 PowerShell 输出 UTF-8：
```javascript
execSync('powershell -Command "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; systeminfo"').toString('utf-8')
```

对于**输出原始 GBK 字节、不认控制台代码页**的工具，PowerShell 包装无效，应以字节捕获再手动解码：
```javascript
const { execSync } = require('child_process')
const buf = execSync('some-gbk-tool.exe')       // 拿 Buffer，不要直接 toString
const text = new TextDecoder('gbk').decode(buf)  // 按真实编码解码
```

### 规则 8：Python 文件 I/O 必须指定编码

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

### 规则 9：Node.js 文件操作和子进程编码

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

### 规则 10：Git 中文支持

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
