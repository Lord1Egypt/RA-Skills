---
name: clawhub-publish
description: |
  把本地 Skill 发布到 ClawHub（clawhub.ai）并同步到 GitHub 合集仓库，从而能被 find-skills 检索到、
  也能让人看到源码。ClawHub 负责分发，GitHub 负责托管，两条链路独立。
  当用户说「发布 skill」「把 skill 发出去」「上架技能」「让更多人用上这个 skill」「publish skill」
  「发到 clawhub」「传到 GitHub」「上传 GitHub 了吗」「建个仓库」时使用。
  包含：发布前内容审查与署名检查、description 场景化改写规范、dry-run 验证、
  沙箱内自助 device-flow 登录、发布命令与发布后验证、GitHub 仓库创建与推送，
  以及 Windows + WorkBuddy 沙箱下的已知环境陷阱。
  不适用于：安装别人的 skill（用 find-skills）、发布 OpenClaw package（用 clawhub package）。
agent_created: true
---

# 把 Skill 发布到 ClawHub

## 分发链路

```
本地 skill 目录
   ↓  clawhub skill publish
ClawHub（clawhub.ai）        ← 也可从 GitHub import（clawhub.ai/import，需登录）
   ↓  自动同步
SkillHub（lightmake.site）
   ↓  find-skills 语义检索
WorkBuddy / CodeBuddy 用户
```

**注意**：WorkBuddy 官方「推荐市场（BuiltinMarket）」是**只读**的，用户无法投稿。自主发布只能走 ClawHub。

---

## 环境准备（Windows + WorkBuddy 沙箱）

> 以下均为本机实测结论，务必遵守。

1. **优先用 PowerShell 工具；Bash 工具只用于直接调用绝对路径的可执行文件。**
   - Bash 工具的 PATH 里 **coreutils 全部缺失**——实测 `dirname` / `basename` / `head` / `tail` /
     `grep` / `sed` / `awk` / `cat` / `ls` 一律 `MISS`，只有 `node`（托管 22）和 `python` 在。
   - 但**直接调绝对路径的 python/node 是可用的**（例：
     `"C:/Users/…/envs/default/Scripts/python.exe" script.py`）。
     带 `|` 管道、`cd`、`grep` 的命令必然失败。
   - **每次 Bash 调用 stderr 都会带两行 shim 噪声**（`dirname: command not found` / `cd: null directory`）。
     那是 shim 自身报错，**不代表命令失败**，看 Exit Code 即可。

2. **不要用管道处理命令输出。**
   PowerShell 的 `| Out-File` 会缓冲，长任务拿不到实时输出。
   → `Out-File` 到日志文件，再用 Read 工具读。需要实时输出时才用 `| Out-File` 之外的方式。

3. **npm 必须用系统 Node 的完整路径。**
   ```powershell
   $env:PATH = "C:\Program Files\nodejs;$env:PATH"
   & "C:\Program Files\nodejs\npm.cmd" install -g --prefix "$env:APPDATA\npm" clawhub
   ```
   PATH 默认会优先命中托管 Node 22 的 shim；clawhub 需要较新 Node（系统 Node 24 + npm 11 实测通过）。
   全局前缀固定 `$env:APPDATA\npm`（即 `%APPDATA%\npm`；`npm prefix -g` 在 Git Bash 下会解析错）。
   安装后 CLI 位于 `$env:APPDATA\npm\clawhub.cmd`（本机已装 v0.23.3，约 47 个包 / 40 秒）。

4. **`cmd.exe` 与 `Start-Process` 被禁止**从 PowerShell 工具调用。

---

## 发布前检查（每次都要做）

### 1. 内容审查——绝不能把本地信息发出去

用 Grep 搜 skill 目录，pattern：
`%USERNAME%|Desktop|C:\\|D:\\|\.workbuddy|\.codex|<你的其他私有标识>`
必须返回 **No matches found**。

### 2. description 必须写「什么时候用我」，不是「我是什么」

语义搜索匹配的是**用户的问法**，不是自我介绍。

| ✗ 错误写法 | ✓ 正确写法 |
|---|---|
| 「某某主题的认知框架。提炼了 N 个心智模型、M 条启发式……」 | 「当用户面临 X 决策、Y 取舍、Z 情境，或问『该不该做』『怎么选』时使用。提供……。Use when: …」 |

要点：
- 把**触发场景**列全（用户会怎么问，就怎么写）
- 保留**口语触发词**（「这仗怎么打」「要不要正面硬刚」这类）
- **补英文触发词**（SkillHub 支持中英双向语义检索）

### 3. 署名检查——派生自他人方法论时必做

若这个 skill 的**方法论或结构**来自他人（典型：女娲 `perspective-distillation`），
发布前必须在文末保留署名尾注。女娲 `skill-template.md` 明确要求：

```
> 本Skill由 [女娲 · Skill造人术](https://github.com/alchaincyf/nuwa-skill) 生成
> 创建者：[花叔](https://x.com/AlchainHust)
```

**这一步最容易漏**——内容审查（查隐私）能过，但署名叫不查就发现不了。
本轮真实教训：`sunzi-perspective` 首次发布时只在一行里提了「与女娲的 perspective-distillation 互为上下游」，
**没有模板要求的署名尾注**，公开后才补发 v1.0.1。

派生关系判断：只要用了别人模板的结构（角色扮演规则 / 心智模型 / 表达DNA / 诚实边界 这套骨架），
就算派生，就要署名。与 ClawHub 默认的 MIT-0（不要求署名）**并不冲突**——
MIT-0 是平台对产物授权的默认值，署名是方法论来源方的要求，两者要分别满足。

### 4. dry-run 验证（不需要登录）

```powershell
& $cli skill publish "<skill目录>" --slug <slug> --name "<显示名>" --version 1.0.0 --dry-run
```

期望输出：`Would publish <slug>@1.0.0`

### 5. 检索**分发面**的竞争格局——别拿 GitHub 覆盖率代替平台覆盖率

**实测教训（2026-09-21）**：曾据「GitHub 319 个仓库里没有中文 humanizer」判定中文去 AI 味是**空白位**，
实际发布时检索 ClawHub，**已有 12+ 个同类**（`humanizer-zh` 17 次安装 / 60 天最高，
12 个里有 5 个是 0 安装）。

**GitHub 仓库 ≠ 平台可安装 skill**——大量中文作者只发平台不发仓库，GitHub 上扫不到不代表平台上没有。

发布前至少跑两次检索，**英文 slug 与中文口语词都要**（覆盖面完全不同）：

```powershell
& $cli search <英文 slug 关键词> --no-input
& $cli search <中文口语关键词>   --no-input
```

看三件事：**同类数量 / 最高的安装量 / 最近的更新时间**。

| 检索结果 | 含义 | 该做什么 |
|---|---|---|
| 同类为 0 | 真空白位 | 也查一下是不是「有人试过又下架了」 |
| 有同类，安装量全在 0–20 | **「有人做，但没人做成」** | 先搞清那批为什么没起量，再决定要不要做下一个；**别把「没人做」当理由** |
| 有同类，且已有上千安装 | 需求被验证 | 必须有明确差异点才下场，否则就是陪跑 |

### 5b. 深挖：把竞品正文拉下来拆（`search` 只给结论，`inspect` 才给证据）

`search` 只能看到 slug / 显示名 / 安装量。要判断「这批为什么没起量」，必须把正文抓下来。
**`inspect --file` 可以在不安装的情况下取任意文件原文**：

```powershell
& $cli inspect <owner>/<slug> --files            # 文件清单 + 审核/安全状态 + Summary
& $cli inspect <owner>/<slug> --file SKILL.md    # 正文原文（<= 10MB）
& $cli inspect <owner>/<slug> --json             # 元数据（含完整 description）
```

> ⚠️ **`inspect` 的 `Owner` 字段带 `@` 前缀**（如 `@junci003`）。
> 若用正则解析输出框并把 `Owner` 写回 `owner` 变量，会**覆盖原始值**，
> 之后用它拼目录名会全部落空。取到后必须 `lstrip("@")`。
> （2026-09-21 实测踩到：22 个样本全部读不到正文，排查了一轮。）

**判重口径——不要用 `difflib.quick_ratio`。**

它只比较**字符多重集**，不关心顺序。同类 skill 共享同一批套话词（「首先/其次/综上所述」），
任意两个之间 quick_ratio 轻松上 0.5，全是噪声。

要用两个硬指标：

| 指标 | 怎么算 | 判据 |
|---|---|---|
| `ratio` | `difflib.SequenceMatcher(None,a,b).ratio()` | > 0.9 基本同源 |
| **LCS** | `max(get_matching_blocks(), key=size).size` | **> 300 字且占较短正文 > 25% → 实质同源**；100–300 需人工确认；< 100 只是共享词表 |

LCS（最长公共连续子串）是最硬的证据：两段文本有上千字**逐字连续相同**，
不可能是独立写作的巧合。

**这一步的验收标准是「能不能回答那批为什么没起量」**，具体看四件事：

1. **谁在抄谁** — 用 `inspect --json` 的 `created` 排时间线，早的才是源
2. **头部是不是原创** — 头部若全是某个外部源的搬运/翻译，那这个赛道的机会就不在「做得更好」
3. **方法论有没有共同缺陷** — 把同类反复出现的主张列出来，看方向是否一致性地错
4. **结构完成度** — 统计有几个同类具备「失效条件 / 验证判据 / 反模式表 / 强度分档 / 量化阈值」，
   这些格子空着的地方才是可用的差异面

> **性能提示**：每个 `inspect` 都是一次 Node 进程启动。20+ 个样本 × 2–4 次调用 ≈ 10 分钟，
> **超过前台时限，必须 `run_in_background`**。

---

## 登录：沙箱内可自助完成，不要让用户去终端手敲

**踩过的坑**：`clawhub login` 是交互式 CLI。在沙箱后台运行时 stdout 被缓冲，
**读不到 user_code**；任务会一直空转（只能强杀），用户在自己终端跑又看不见验证码。

**正解**：绕过 CLI，直连 device flow API —— `scripts/clawhub_device_login.py`

```bash
PY="$HOME/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
"$PY" "<skill目录>/scripts/clawhub_device_login.py" request   # 申请设备码
"$PY" "<skill目录>/scripts/clawhub_device_login.py" poll      # 后台轮询，授权后自动落盘（run_in_background）
```

流程：
1. `request` → 打印 `user_code` 与 `verification_uri`（**代码已内嵌在 URL 里**，用户点链接即可，不用手输）
2. 把 `verification_uri` 给用户，**同一轮内**启动 `poll`（后台，有效期 900 秒）
3. 用户点确认 → poll 拿到 token → 自动写入 `%APPDATA%\clawhub\config.json`
4. `& $cli whoami` 验证

**API 细节**（从 `dist/deviceAuth.js`、`dist/config.js` 读出，实测可用）：

| 项 | 值 |
|---|---|
| 申请 | `POST https://clawhub.ai/api/cli/device/code`，body `{scope:"read write", site_url:"https://clawhub.ai", label}` |
| 轮询 | `POST https://clawhub.ai/api/cli/device/token`，body `{device_code, grant_type:"urn:ietf:params:oauth:grant-type:device_code"}` |
| 成功 | HTTP 200 + `{access_token, token_type, scope}` |
| 等待中 | `{"error":"authorization_pending"}`（继续轮询）；`slow_down` 则 interval +5s |
| 凭据位置 | `%APPDATA%\clawhub\config.json` → `{"registry": "...", "token": "..."}` |

**备选路径**（device flow 不便时）：
用户在 ClawHub 网页 **Settings → API tokens** 生成 token，然后 `& $cli login --token <t>`。
（`--token` 是非交互的，沙箱内可直接跑。）

**其它登录命令**：`& $cli whoami` 验证 · `& $cli token` 打印已存 token · `& $cli logout` 本地登出。

---

## 发布

```powershell
& $cli skill publish "$env:USERPROFILE\.workbuddy\skills\<name>" `
  --slug <slug> `
  --name "<中文显示名>" `
  --version 1.0.0 `
  --categories research,operations `
  --changelog "<版本说明>"
```

常用参数：`--categories` / `--topics` / `--tags` / `--owner`（组织）/ `--fork-of` / `--json`

**分类 slug —— ⚠️ 必须用 ClawHub 的集合，不能用 SkillHub 的**

SkillHub（lightmake.site）与 ClawHub（clawhub.ai）是**两套不同的分类体系**。
用 SkillHub 的分类（如 `business-ops`）会被 ClawHub 直接拒绝：

```
Error: Unknown skill category slug "business-ops" (reset in 17s)
```

且**失败后会触发冷却**（约 17 秒不可重试），dry-run 检查不出来，只有真发才发现。

**ClawHub 合法分类（14 个，2026-09-21 从 806 个 skill 反查实测）**：

| slug | 含义 | 抽样占比 |
|---|---|---|
| `other` | 其它（多数框架类落在这里） | 最高 |
| `knowledge` | 知识管理 | 高 |
| `creative` | 创作 | 高 |
| `productivity` | 效率 | 高 |
| `integrations` | 集成对接 | 中 |
| `development` | 开发 | 中 |
| `research` | 研究分析 | 中 |
| `finance` | 金融 | 中 |
| `lifestyle` | 生活 | 中 |
| `automation` | 自动化 | 中 |
| `communication` | 沟通 | 低 |
| `agents` | 智能体 | 低 |
| `security` | 安全 | 低 |
| `operations` | 运营 | 低 |

支持多分类逗号分隔（实测存在 `research,operations` 这类多分类 skill）。
**映射参考**：原 `business-ops` → `operations`；方法论/分析框架 → `research` 或 `knowledge`。

> 无法确认分类是否合法时，**直接省略 `--categories`**（该参数可选），
> 比赌一个 slug 触发冷却划算。发布后仍可用 `& $cli skill tag` 等命令调整。

**slug 冲突检查**：发布前先搜一下。

```powershell
& $cli search <关键词> --no-input
```

（ClawHub 的 slug 按 owner 命名空间区分，同名可共存，但同 owner 下唯一。）

### 发布后验证

**必须知道**：`clawhub skill info` **不存在**。`clawhub skill` 下只有
`publish` / `verify` / `tag` / `rename` / `merge` / `help`。

正确做法是用顶层的 `inspect`：

```powershell
& $cli inspect <owner>/<slug>   # ★ 查自己发布的必须带 owner
& $cli search <关键词> --no-input
```

> ⚠️ **`inspect <slug>` 不带 owner 会命中别人的同名 skill。**
> 2026-09-21 实测：`inspect zh-humanizer` 显示的是 **@nanbingxyz** 的 skill
> （2026-02 创建、v1.0.0、已公开），而自己刚发的 `junci003/zh-humanizer` 完全看不见。
>
> slug 只在 **owner 命名空间内**唯一，跨 owner 可以同名——所以 `zh-humanizer` 这种通用词
> 大概率先被别人占掉。**发布后核对一律写 `inspect <owner>/<slug>`**
> （`@<owner>/<slug>` 也行），否则会拿别人的数据当自己的战绩。
>
> 判断「自己那个是否存在」的信号：带 owner 查会返回
> `Skill is hidden by moderation (pending.publication)` + `Moderate CLEAN`——
> 这说明**已注册且扫描通过**，只是还没转公开。

发布成功的输出长这样：

```
Update submitted for <slug>@<版本>; pending security scans before it becomes public.
```

**发布后不是立刻公开**，要走安全扫描。`inspect` 会显示：

```
<slug> is not publicly visible.
Detail: Skill is hidden by moderation (pending.publication).
  Moderate CLEAN
  Reason   pending.publication
  Engine   v2.4.26
  Mod Note No suspicious patterns detected.
```

含义：扫描引擎已跑完且**结论 CLEAN**（无可疑模式），只是状态仍是「待发布」，
过一段时间会自动转为公开。所以**刚发完搜不到是正常的，不要以为失败**。

再查 SkillHub 是否同步：`curl "https://lightmake.site/api/v1/search?q=<关键词>&limit=8"`
（返回含 `downloads` / `installs` / `stars`，可作基线，后续观察变化。）

**注意：SkillHub 同步有明显延迟。** 实测 ClawHub 已公开且可搜到之后，
SkillHub 上仍搜不到（发布后 3 分钟内）。**不要因为 SkillHub 搜不到就判定发布失败**——
以 ClawHub 的 `inspect` 为准。

**公开地址规律**：`https://clawhub.ai/<owner>/skills/<slug>`
（例：`https://clawhub.ai/junci003/skills/sunzi-perspective`）。
`inspect` 输出里的 `Owner` 就是 `<owner>`。

**默认许可证是 MIT-0**——发布时若不指定，ClawHub 会以
`MIT-0 (Free to use, modify, and redistribute. No attribution required.)` 授权。
发布前需与用户确认这一点：
- 若用户希望**保留署名要求**（例如蒸馏方法论源自女娲 MIT，规范要求保留出处），
  MIT-0 会与之冲突，需在 SKILL.md 内保留署名段并在发布时另行说明。
- 尽量在发布**前**把许可证预期和用户对齐，事后改不如事前定。

---

## 第二条链路：同步到 GitHub（源码托管）

ClawHub 是**分发**，GitHub 是**托管**，两者独立——
**用户在 ClawHub 登录时用的 GitHub 账号只是 OAuth 身份验证，不会把文件传到 GitHub。**
用户问「传 GitHub 了吗」时，先确认这一区别，别答错。

### 合集仓库模式（推荐）

每个视角一个子目录，便于持续追加：

```
perspectives/                    ← 仓库根
├── README.md                    ← 仓库说明（含证据层级、设计原则、安装方式）
├── LICENSE                      ← MIT
├── .gitignore
├── sync.ps1                     ← 从 ~/.workbuddy/skills/ 同步全部 *-perspective
└── sunzi-perspective/           ← 每个视角一个目录
    ├── SKILL.md
    └── references/
```

本机已建：**https://github.com/junci003/perspectives**（PUBLIC，默认分支 `main`）
本地副本：`<你 clone 到本地的路径>\perspectives\`

### 首次创建并推送

```powershell
$env:PATH = "C:\Program Files\Git\cmd;C:\Program Files\GitHub CLI;" + $env:PATH
Push-Location <本地目录>
gh repo create <repo> --public --source=. --remote=origin --push --description "<ASCII 描述的更稳>"
Pop-Location
```

### 日常更新（已有仓库）

```powershell
.\sync.ps1                             # 从 ~/.workbuddy/skills/ 同步全部 *-perspective
git -C <repo> add -A
git -C <repo> commit -m "add <name>-perspective"    # 中文 message 见陷阱 1
git -C <repo> push
```

### ⚠️ 四个已知陷阱（均已实测）

**1. PowerShell 传非 ASCII 参数给 native exe 会被转成 ANSI**

`gh repo create --description "中文…"` 传出去会变成 `鎶婁竴鏈功…`
（UTF-8 字节被按 GBK 重新编码）。git 的 `-m` 中文 message 同样中招。

→ **解法：改用 Python `subprocess`**（Windows 上走宽字符 API，中文无损）：

```python
import subprocess
subprocess.run([r"C:\Program Files\GitHub CLI\gh.exe",
                "repo", "edit", "owner/repo", "--description", "中文描述"],
               capture_output=True)
```

已写坏的字段用 `gh repo edit --description` 补一次即可。

> **根因（本机实测）**：系统启用了 **UTF-8 代码页（Beta）**，而 PowerShell 5.1 的
> `[Console]::OutputEncoding` 仍是 GBK。于是所有 native exe（git / gh / python）
> 输出 UTF-8 中文时，PowerShell 按 GBK 解码 → 写进日志就是乱码。
> **数据本身没坏**，坏的是显示层。判断真实内容必须用 Python 解码：
> `subprocess.run(["git","log","-1","--pretty=%s"], capture_output=True).stdout.decode("utf-8")`
>
> **推论：给本机写工具脚本时，输出尽量用 ASCII**——否则不仅日志乱码，用户终端也未必正常。
> （脚本入参是中文路径没问题，Python 走宽字符 API 读取 argv。）

→ **更省事的替代（推荐先试）：`git commit -F <UTF-8 消息文件>`**

把 commit message 写进一个 UTF-8 文本文件，用 `-F` 传入——
**命令行上不出现任何非 ASCII 字符**，编码环节整个绕开，不需要 Python。

```powershell
# msg.txt 用 UTF-8 写（Write 工具生成的文件就是 UTF-8）
git -C <repo> commit -F "C:\path\to\msg.txt"
```

2026-09-21 实测：message 落盘正确，用 Python 解码回读为
`feat: 新增 zh-humanizer，补齐 sunzi 的反模式与验证判据`，无乱码。

**只在「非把中文放在命令行上不可」时才需要 Python subprocess**——
例如 `gh repo edit --description "中文"`（没有 `-F` 这类参数）。

**2. git 创建 `refs/remotes/origin/` 嵌套目录会静默失败（本机 git 2.55）**

症状：push 成功、`git ls-remote` 能看到远程分支，但
`git branch -vv` 显示 `[origin/main: gone]`；
而 `git fetch` 与 `git update-ref` 都**报告成功却完全不落盘**
（`refs/remotes/` 仍是空目录，无 `packed-refs`、非 reftable、目录权限 0777 正常）。
**全新 clone 的仓库无此问题**——所以别以为是网络或权限。

→ **解法：手动建目录并写 ref 文件**

```python
import os
d = r"<repo>\.git\refs\remotes\origin"
os.makedirs(d, exist_ok=True)
open(os.path.join(d, "main"), "w").write("<40 位 sha>\n")
```

随后 `git branch --set-upstream-to=origin/main main` 即正常。

→ **已封装为脚本**：`scripts/fix_git_upstream.py`
（自动读远程 SHA → 写 loose ref → 设 upstream → 自检，全程幂等）

```powershell
$env:PATH = "C:\Program Files\Git\cmd;" + $env:PATH
python "$env:USERPROFILE\.workbuddy\skills\clawhub-publish\scripts\fix_git_upstream.py" "<仓库路径>" [remote] [branch]
```

**教训：新建仓库后必须核实 `refs/remotes/` 真的有内容，不要相信 fetch 的「成功」输出。**

```powershell
git -C <repo> for-each-ref --format="%(refname)" refs/remotes/
```

**3. `github.com` 只在 PowerShell 通道可达**

| 域名 | Bash 沙箱 | PowerShell（走系统代理） |
|---|---|---|
| `api.github.com` | ✅ 可达 | ✅ 可达 |
| `github.com` | ❌ 超时 | ✅ 200 |
| `codeload.github.com` | ❌ 502 | — |
| `raw.githubusercontent.com` | ❌ 超时 | — |

→ **`git clone` / `git push` 必须走 PowerShell 通道。**
但 `gh api` 走的是 `api.github.com`，两边都能用。
本机系统代理：WinINET `127.0.0.1:7897`（Clash Verge）。

**4. 沙箱注入的 `HTTPS_PROXY` 覆盖 git config，导致 push 静默失败（rc=128）**

症状：`git push` 返回 **128，且 stderr 空**，完全看不出原因。

诊断（2026-09-21 实测）：
- `git config --get http.proxy` = `http://127.0.0.1:7897`（Clash Verge，正常，`ls-remote` 也通）
- 但环境变量 `HTTPS_PROXY` = `http://127.0.0.1:5xxxx` ——**WorkBuddy 沙箱自己注入的**，
  端口每会话随机，带域名白名单，**`github.com` 不在白名单里**
- **git 的优先级是「环境变量 > config」**，所以 push 实际走的是那条被墙的路

→ **解法：调 git 时临时覆盖 env，强制走 Clash**

```python
import os, subprocess
env = os.environ.copy()
for k in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"):
    env[k] = "http://127.0.0.1:7897"
subprocess.run(["git", "-C", REPO, "push"], capture_output=True, env=env)
```

**诊断口诀**：`git push` rc=128 且 stderr 为空 → 先比对
`git config --get http.proxy` 与 `$env:HTTPS_PROXY` 的**端口是否一致**。不一致就是这个坑。

**注意 PowerShell 的诱饵**：`git push 2>&1 | Out-File log` 会把 stderr 变成
`NativeCommandError` 记录而**被吞掉**，看起来像「没有任何错误输出」。
要拿到真实报错必须用 Python `capture_output=True` 把两个流分开取。

### GitHub 环境基线

- `gh` CLI **v2.100.0**，已登录 `junci003`，scope：`gist, read:org, repo, workflow`
- `git` **v2.55.0.windows.5**（`C:\Program Files\Git\cmd\git.exe`）
- **用仓库级 git 身份，别动全局**（本机全局 `user.name` / `user.email` 为空）：
  ```powershell
  git -C <repo> config user.name "junci003"
  git -C <repo> config user.email "298531191+junci003@users.noreply.github.com"
  ```

---

## 发布后的现实预期（重要）

实测 2026-09-21：框架/方法论类 skill 在 SkillHub 上**结构性冷门**。

| 类型 | 下载量级 | 安装量级 |
|---|---|---|
| 工具类（海报设计、公文排版） | 4.7–4.9 万 | 239–784 |
| 框架类（孙子兵法，10+ 版本） | 最高 1,870 | **几乎全为 0** |

「孙子兵法」类目下 13 个版本，合计下载不足 4,000，**安装数几乎全为 0**——下载了但没人真装起来用。

**所以不要向用户承诺「发布 = 有人用」。** 发布是零成本试一次（伐交），不是增长方案。
真正的转化断点有三个：搜不到 / 看不出好在哪 / 装了不用。

---

## 相关命令速查

```powershell
& $cli whoami                 # 验证登录（输出 GitHub handle）
& $cli token                  # 打印存储的 token
& $cli search <q>             # 搜索
& $cli inspect <slug>         # 看可见性 + 审核结果（★ 唯一的「查详情」入口）
& $cli star / unstar <slug>   # 收藏
& $cli sync                   # 扫描本地 skills，批量发布新增/变更的
& $cli hide / delete <slug>   # 下架 / 软删除

# skill 子命令（只有这 5 个）
& $cli skill publish <path>                 # 发布（--dry-run 预检）
& $cli skill verify <slug>                  # 用 ClawHub 安全证据校验已发布 skill
& $cli skill tag <skill> <version>          # 给已有版本打 tag
& $cli skill rename <skill> <new-slug>      # 改名（旧 slug 保留重定向）
& $cli skill merge <source> <target>        # 合并两个自有 skill（旧 slug 重定向）
```

**不存在的命令**：`skill info`、`skill list`、`skill delete` → 会报 `unknown command`。

## 边界

- 只发布**自己创建**的 skill（frontmatter 带 `agent_created: true` 或用户明确授权的）。
- 发布前必须确认 skill 内容**不含他人版权材料**（含版权的译注、他人原创解读等）。
  公版文本（如《孙子兵法》原文）可发，但在版图书的独创解读不可整段搬运。
- 不美化发布效果：见「发布后的现实预期」。
