---
name: "Windows Shell Encoding Doctor - Windows Shell编码修复工具"
description: 诊断修复 Windows 下 PowerShell/cmd/Git Bash 的乱码、引号转义、路径空格与 CRLF 等问题。当用户说：PowerShell 里跑 bash 命令报错、中文乱码怎么修、JSON 怎么安全传给命令行，或类似 Windows 终端编码问题时，使用本技能。
metadata: { "openclaw": { "emoji": "🪟", "requires": { "bins": [] } } }
---

# Windows Shell 与编码排障

在 **Windows** 上排查 **PowerShell / cmd / Git Bash** 下的命令失败、乱码与换行问题。先识别 **当前 shell**，再归类：**shell 混用**、**引号与转义**、**编码与 code page**、**路径与空格**、**CRLF/LF**。用 **可粘贴命令** 与 **references** 中的清单/剧本修复；写无 BOM UTF-8 见正文与 `encoding-checklist.md` 中的 `[System.IO.File]::WriteAllText` 示例。不要一上来盲改命令。

## 何时使用本技能

- **bash 命令在 PowerShell 里报错**（heredoc、`export`、`grep | xargs` 等）
- **PowerShell 语法误贴在 Git Bash / cmd** 里
- **Windows 下中文乱码**、`\uXXXX` 字面量、mojibake、控制台编码
- **PowerShell 里安全传 JSON**、多行 payload、stdin
- **路径明明存在却找不到**（未加引号、工作目录错、分隔符习惯）
- **脚本在 Windows 编辑后到 Linux 失效**（CRLF、BOM）
- **文档或 Agent 给的 Linux 一键命令**在本地 PowerShell 粘贴失败

典型问法示例：「这个 bash 命令在 PowerShell 为什么报错？」「同样命令在 Linux 能跑，Windows 不行。」

## 核心工作流

1. 先识别当前 shell。
   - PowerShell：优先给 PowerShell 原生写法。
   - cmd.exe：避免 PowerShell 专属语法，尽量保持简单。
   - Git Bash / MSYS / WSL：通常可以接受 Unix 风格语法。
2. 再看失败命令长什么样。
   - 如果在 PowerShell 里出现 `<<EOF`、`cat <<'EOF'`、`export`、`/dev/null`、`grep | xargs` 之类，优先怀疑是 bash 语法被直接贴进来了。
   - 如果在 bash 里出现 `$env:NAME=...`、`ConvertTo-Json`、`Out-File`、反引号转义，优先怀疑是 PowerShell 语法被贴错地方。
3. 归类错误。
   - 在 `<`、`|`、`&`、`@`、`{`、`}` 附近报解析错误：通常是 shell 不匹配或转义问题。
   - 中文乱码、`\uXXXX` 字面量、mojibake：通常是编码问题。
   - 文件明明存在却提示找不到：通常是路径没加引号、分隔符不对、或工作目录不对。
   - 脚本能跑但输出在别的工具里坏掉：通常是 CRLF/LF 或编码链路问题。
4. 用**最低风险**的方式重写。
   - 大段 JSON 不要硬塞 one-liner。
   - PowerShell 下优先用 hashtable + `ConvertTo-Json`，或先写临时文件再由工具读取。
   - 路径带空格时优先整体加引号。
5. 最后简短说明根因。
   - 说清楚：原命令错在哪、是哪个 shell 假设失效了、为什么新的写法更稳。

## 回答结构（输出风格）

修命令时，优先按这个结构回答：

1. **原因**：一句话说清楚。
2. **修好的命令**：可以直接粘贴运行。
3. **更稳的文件版写法**：如果涉及 JSON、多行文本、中文内容，优先给。
4. **Shell 说明**：只有在用户明显混用了 PowerShell / bash 时才补充。

保持实用，不要上来长篇讲 shell 理论。

## 常用修复模式

### JSON、多行文本与 stdin（PowerShell）

在 PowerShell 里优先用：

- Hashtable + `ConvertTo-Json -Depth N`
- 先写成 UTF-8 文件，再交给目标工具读取
- Here-string 承载可读性更好的多行文本

避免直接照搬 bash heredoc：

```bash
python - <<'PY'
...
PY
```

这不是合法的 PowerShell 语法。

PowerShell 里更稳的是：

```powershell
@'
print("hello")
'@ | python -
```

如果引号层次复杂，优先写临时文件。

### 中文乱码与编码（UTF-8 / GBK / BOM）

先检查：

- 终端编码
- 文件编码
- 是否把 Unicode 变成了字面量 `\uXXXX`
- 是否被旧版 PowerShell / 某些 cmdlet 写成了 UTF-16 或别的编码

优先做法：

- `Set-Content -Encoding UTF8`
- 需要控制 BOM 时，用 `[System.IO.File]::WriteAllText(..., [System.Text.UTF8Encoding]::new($false))`
- 中文内容、富文本、长 JSON 尽量走 UTF-8 文件，不要依赖控制台直接传参

详见 `references/encoding-checklist.md`。

### 路径、空格与工作目录

优先检查：

- 路径里有没有空格
- 分隔符是否被目标工具正确理解
- 当前工作目录是不是你以为的那个目录
- 是否错误依赖了 bash 的路径扩展习惯

优先给出带引号路径：

```powershell
python ".\scripts\tool.py"
Get-Content ".\data\input file.json"
```

### bash → PowerShell 翻译

当用户把 Unix 风格命令贴到 Windows shell：

- 直接翻译成 PowerShell，不要只说「这是 bash 语法」
- 保留行为，不要求保留原 token 形状
- 如果完全等价写法很别扭，优先给一个更稳的 Windows 原生方案

详见 `references/powershell-vs-bash.md`。

## 判断启发式

- 命令里有多行代码或 JSON：优先考虑文件方案。
- 命令里有中文：默认把编码当成潜在风险，优先 UTF-8 文件传输。
- 错误指向 `<` 或 heredoc：先怀疑 bash 语法被贴进 PowerShell。
- 用户说「在 macOS/Linux 能跑，在 Windows 不行」：先比较 shell 语义，不要先怪程序。
- 如果原因可能有多个：先修 shell 不匹配，再看编码。

## 附带的 references

路径相对本技能目录（仓库中多为 `skill/windows-shell-encoding-doctor/...`）。

| 文件 | 何时读 |
|------|--------|
| `references/powershell-vs-bash.md` | Shell 翻译、bash/PowerShell 混用判断 |
| `references/encoding-checklist.md` | 乱码、UTF-8/BOM、JSON 转义、CRLF/LF |
| `references/common-failures.md` | 有具体报错模式、快速归因 |
| `references/repair-playbooks.md` | 按「输入 → 诊断 → 修复」救火 |
| `references/json-and-stdin-patterns.md` | JSON、stdin、多行 payload、中文经管道/文件传递 |

## 安全与质量要求

- 不要在没有必要时推荐破坏性命令。
- 不要把「去用 WSL / Git Bash」当成默认答案；如果 PowerShell 能原生解决，优先原生方案。
- 优先降低转义复杂度，而不是炫技写 one-liner。
- 给 PowerShell 命令时，要保证用户能直接复制粘贴。
