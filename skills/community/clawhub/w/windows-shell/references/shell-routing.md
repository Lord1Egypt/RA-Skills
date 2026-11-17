# Shell 选型（Git Bash / PowerShell / WSL）

主文件给了速查表。需要判断依据、完整决策表、或想知道为什么默认 Git Bash 时读本文。

## 为什么默认 Git Bash

四个独立 agent 在同一台 Windows 10 机器上做同一份任务（zod + TypeScript + vitest，pydantic + pytest，共 9 步），每个只准用一种 shell。实测结果：

| 执行方式 | 输出 token | 轮次 | 失败 | 重试 | 三道闸门 |
|------|------|------|------|------|------|
| **Git Bash** | **8,114（基准）** | **34** | **0** | **0** | 全过 |
| WSL → `/mnt/d` | 11,543（1.42x） | 34 | 0 | 1（静默） | 全过 |
| WSL → ext4 | 15,159（1.87x） | 49 | 1 | 2 | 全过 |
| pwsh 7 | 18,808（**2.32x**） | 46 | 0 | 0 | 全过 |

另一组 12 个典型场景的合成基准独立复现了同一系数：PowerShell 5.1 的输出体积是 POSIX 的 **2.22 倍**（同一个「文件不存在」错误，POSIX 是 50 字节一行，PS 5.1 是 370 字节七行）。

命令启动开销（中位数，发 100 条命令的累计代价）：

| Git Bash | `wsl.exe` | PowerShell 5.1 | pwsh 7 |
|------|------|------|------|
| 0.064s（6.4s） | 0.130s（13.0s） | 0.189s（18.9s） | 0.216s（21.6s） |

三条结论：

- **Git Bash 是唯一零失败零重试的一臂**，且 token 最省。
- **PowerShell 不是「更容易出错」，而是「更啰嗦」**——它同样零失败，但写同样的东西用了 80 条语句（Git Bash 38 条），错误对象带调用栈、字符位置、CategoryInfo、FullyQualifiedErrorId 一起打印。
- **token 消耗与文件系统快慢无关，只与踩坑次数有关**：跑在最快的 ext4 上那一臂，因为踩了两个 `wsl.exe` 的坑、多花 15 轮，反而 token 最高。

## 决策表

| 你要做的事 | 用哪个 | 理由 |
|------|------|------|
| npm / pnpm / node / npx / tsc / vitest / jest | **Git Bash** | 直通，零摩擦 |
| python / pip / venv / pytest | **Git Bash** | 直通（venv 见下方坑 3） |
| git 全套 | **Git Bash** | 原生，且 worktree 在 WSL 里根本用不了 |
| **native 模块编译**（node-gyp + MSVC） | **Git Bash** | 与 pwsh **完全等价**：产物字节数相同，都经 vswhere 找到同一套 VS 工具链 |
| ssh / scp / git over ssh | **Git Bash** | 与 Windows 共用 `~/.ssh`，密钥无需 chmod（见坑 5） |
| curl / grep / sed / awk / find / jq* | **Git Bash** | POSIX 工具链（`jq` 需另装，见坑 4） |
| Windows 服务、注册表、事件日志、计划任务、证书 | **PowerShell** | Git Bash 没有对应能力 |
| 需要 .NET 类型 / COM 对象 / 对象管道 | **PowerShell** | 硬边界，无替代 |
| 需要管理员权限 | **交给人做** | UAC 弹窗 agent 点不了，命令会挂死 |
| 跑 Makefile / 需要 gcc、rsync | **WSL** | Git Bash 的 MSYS2 工具集撑不住 |
| 重 I/O 的构建（大型 monorepo 反复编译） | **WSL + 项目放 ext4** | 见下方「什么时候才值得上 WSL」 |

## 必须切 PowerShell 的四类

这四类没有 Git Bash 替代品，别硬试：

1. **Windows 系统层面** —— `Get-Service` / `Get-ScheduledTask` / `Get-WinEvent` / `Get-NetTCPConnection` / 证书存储 / 注册表写入。
2. **.NET 与 COM** —— `[System.Guid]::NewGuid()`、`New-Object -ComObject`、任何 `[类型]::方法()` 调用。
3. **对象管道** —— 需要 `Select-Object Id,WS` 这种结构化字段筛选，而不是文本切割时。
4. **提权操作** —— 但注意：**这类应该交给人执行**。Git Bash 没有 `sudo`，唯一提权路径是 `Start-Process -Verb RunAs`，它会弹 UAC，agent 无法点击，命令就一直挂着。需要管理员权限的步骤，写进说明让人来做，不要让 agent 去试。

切过去的正确写法是**单条命令**，不是切换会话：

```bash
# 在 Git Bash 里调一条 PowerShell，用完即回
powershell -NoProfile -Command '[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; (Get-Service wuauserv).Status'
```

外层务必单引号（防 bash 展开 `$_`、`$null`），UTF-8 前缀对 PS 5.1 必需——细节见 `windows-shell` skill 规则 1。

## 反模式

| 别这样 | 该这样 |
|------|------|
| 因为「Windows 就该用 PowerShell」而默认 PowerShell | 默认 Git Bash，只在四类边界处单条切过去 |
| 为了性能把 Windows 盘上的项目改用 WSL 操作 | 要么整个搬进 ext4，要么留在 Git Bash。别跨 `/mnt/*` |
| 用小 demo 验证「WSL 访问 `/mnt` 快不快」 | 惩罚随规模放大，小项目试不出来 |
| 让 agent 尝试提权 | UAC 弹窗会挂死，写进说明让人做 |
| 遇到报错先怀疑编码 | 先分清：乱码 → 编码问题；语法错/找不到文件 → 参数被改写 |
| 整个会话切到 PowerShell 或 WSL | 单条命令切换，主线留在 Git Bash |

## 一句话总结

**Git Bash 做主力，PowerShell 管 Windows 系统层面，WSL 只在项目能整个住进 ext4 时才值得。** 三者是分工，不是替代——而分工的默认值应该是 Git Bash。
