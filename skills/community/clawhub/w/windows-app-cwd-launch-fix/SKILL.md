---
name: windows-app-cwd-launch-fix
description: "Diagnose and fix Windows packaged apps that crash on launch because relative resource paths (res/xxx) resolve against the process working directory. Includes a four-step elimination method (line endings / start inheritance / file truly missing / CWD attribution), an A/B reproduction, and a self-checking hardened launcher template. Use for 'app crashes on double-click', 'PyInstaller exe crash', 'FileNotFoundError res path', 'CWD wrong', 'works in one folder but not another', '打包给客户跑不起来'."
license: MIT
metadata:
  slug: "windows-app-cwd-launch-fix"
  displayName: "Windows App CWD Launch Fix"
  category: "dev-tool"
  version: "1.0.0"
  author: "WorkBuddy"
  description_zh: "Windows 程序启动目录崩溃排查与修复（启动崩溃/双击exe崩溃/CWD/工作目录/相对路径/PyInstaller/FileNotFoundError/res路径找不到/启动器/launch.cmd/bat/cwd不对/换个目录就崩/打包给客户跑不起来）：四步排除法 + A-B 对照复现 + 自检型启动器模板。"
  agent_created: "true"
---

# Windows 打包程序「双击就崩」：工作目录归因与加固启动器

## 症状长这样

客户双击 exe，窗口一闪就没了，或者控制台甩出：

```
FileNotFoundError: [Errno 2] No such file or directory: 'res/language/language.json'
```

而你打开压缩包一看，**那个文件明明在**。

## 根因（先给结论，省得绕弯）

很多打包程序（尤其从 Python/Electron 转出来的）在 Windows 上把资源路径写成**相对路径**：

```python
if platform == 'win32':
    basedir = ''                      # ← 基准是空字符串
...
json.load(open(os.path.join(basedir, 'res/language/language.json')))
```

`basedir = ''` 意味着 `res/...` 是**相对进程工作目录（CWD）**解析的。
⇒ **CWD 不是程序所在文件夹，就一定崩。**

双击通常 CWD = 程序目录，所以开发机上永远好使。但这三种情况会翻车：

- 快捷方式把「起始位置」设成了别处
- 从别的目录 `start xxx.exe`（子进程**继承父进程 CWD**）
- 任务计划程序启动时 CWD 是 `C:\Windows\System32`

## 四步排除法（顺序不能换）

### 第 1 步：文件到底在不在

⛔ 别用"我能看到这个文件"当答案。用**数量对账**：

| 检查 | 做法 | 实测样例 |
|---|---|---|
| 压缩包条目数 | `zipinfo -1 pkg.zip \| wc -l` | 1785 |
| 解压后文件数 | `find dir -type f \| wc -l` | 1803 = 1785 + 18（额外模组） |
| 目标文件本体 | 直接 `ls -l` 看字节数 | `res/language/language.json` 存在，54 B |
| 有没有第二份拷贝 | 全盘搜同名目录 | 只有一份 ⇒ 排除了"跑错版本" |

对上了 ⇒ **问题不在文件**，往下走。

### 第 2 步：行尾与编码

`.cmd` / `.bat` 必须是 **CRLF + 纯 ASCII**。

- LF 行尾的 bat 在 cmd.exe 里会出现诡异行为（`goto` 标签找不到、命令粘连）
- 带 BOM 的 UTF-8 bat 第一行会被当成命令执行，报 `'ï»¿@echo' 不是内部或外部命令`
- 中文路径/中文注释在非中文代码页下直接乱码，甚至中断解析

⛔ 所以启动器里**一个字的中文都不要写**，注释也写英文。

### 第 3 步：`start` 的继承

```bat
start "" program.exe                 rem ✗ 子进程继承当前 CWD
start "" /d "%~dp0" program.exe      rem ✓ 强制指定子进程起始目录
```

`/d` 是给**子进程**指定工作目录的。加不加，决定了"从别的目录启动"这条路通不通。

### 第 4 步：CWD 归因（这一步才是证据）

做 A/B 对照，各跑 8 秒：

| 实验 | 工作目录 | 结果 |
|---|---|---|
| A | `C:\Users\<user>`（任意别的目录） | **复现客户的报错**，traceback 完全一致 |
| B | 程序所在文件夹 | **启动成功** |

**只有 A 复现、B 正常，才能判定是 CWD 问题。** 否则你只是猜。

## 加固启动器

见 `scripts/launch.cmd`。四个要点：

1. `cd /d "%~dp0"` —— 先把 CWD 钉死在自己所在目录，`/d` 连盘符一起切
2. **启动前自检关键文件**，缺了进 `:missing` 分支给人话，而不是静默崩
3. `start "" /d "%~dp0"` —— 双保险，即使 `cd` 被忽略，子进程 CWD 也对
4. 全程 ASCII + CRLF + `setlocal/endlocal`

```bat
setlocal
cd /d "%~dp0"
if not exist "%~dp0res\language\language.json" goto missing
if not exist "%~dp0_internal" goto missinginternal
for %%F in ("%~dp0*.exe") do start "" /d "%~dp0" "%%~fF"
goto done

:missing
echo  [ERROR] res\language\language.json was not found next to this launcher.
echo          The package looks incomplete or was not fully unzipped.
pause
exit /b 1
```

`:missinginternal` 那条分支是专门对付"直接在 zip 预览里双击"的——`_internal` 目录在压缩包里不存在，这条会先拦住，比让客户看 traceback 强。

## 验收：从四个位置各启一次

| 位置 | 怎么测 |
|---|---|
| 资源管理器双击 | 最基础 |
| 桌面快捷方式 | 故意把「起始位置」留空 / 设成别处，两种都试 |
| `Win + R` 运行 | 输入完整路径 |
| 另一个目录里的 cmd | `cd C:\ && D:\app\launch.cmd` |

**四条全过才算修好。** 另外做一次**反向验证**：把 `res` 改个名，启动器必须报 `[ERROR] ... not found` 而不是静默闪退 —— 证明自检分支真的在工作，不是摆设。

## 什么时候不该用这个方案

- 程序**自己**会 `chdir` 到别处（那要在代码里改 `basedir`，启动器救不了）
- 资源是绝对路径写死的（那是另一个 bug：换机器就崩）
- 走的是安装包（Installer）而不是解压即用 ⇒ 应该修安装脚本里的快捷方式「起始位置」字段

启动器是**止血**，不是治本。治本是让程序用 `os.path.dirname(sys.executable)` 算 `basedir`。
但客户手上的包已经发出去了，止血优先。
