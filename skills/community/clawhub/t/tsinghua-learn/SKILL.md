---
name: tsinghua-learn
description: 清华网络学堂（learn.tsinghua.edu.cn）自动化。要求用户提供网络学堂登录密码（本地 DPAPI 加密存储），自动登录、查看待办、下载课件、提交作业、批量标记已读。当需要操作网络学堂完成日常学习任务时使用。
metadata:
  openclaw:
    requires:
      env:
        - CAS_PASSWORD
    primaryEnv: CAS_PASSWORD
    os:
      - windows
---

# tsinghua-learn skill

清华网络学堂（learn.tsinghua.edu.cn）自动化 Skill。

---

## 如果你是人类，请阅读以下内容

### 前置要求

使用前请确保已安装 **Python 3.10+** 或 **Conda**（推荐 Python 3.11 或 3.12）。建议安装 **7-Zip** 并添加到环境变量 PATH 中，方便后续处理压缩文件。

初始化时会自动安装 Python 依赖（requests、playwright、pillow 等）以及 Chromium 浏览器（~150MB），无需手动操作。

如果没有安装上述环境，请先安装后再对 AI 说 **"开始初始化"**。

### 如何与 AI 沟通

你只需要像聊天一样告诉 AI 你想做什么，AI 会帮你完成所有操作。

#### 初始化

对 AI 说：**"开始初始化"**

AI 会依次：
1. 询问你的网络学堂登录账号、密码、学号、姓名
2. 检查 Python 环境并自动安装所需依赖
3. 安装 Chromium 浏览器
4. 尝试登录网络学堂
5. 登录成功后询问你的偏好设置（是否自动标已读等）
6. 完成后即可正常使用

> **四个字段说明：**
> - **网络学堂登录账号**（`--learn-account`）— 用于登录 learn.tsinghua.edu.cn 的账号，可能和学号不同
> - **登录密码**（`--password`）— 网络学堂登录密码，仅发送至 id.tsinghua.edu.cn（CAS）和 learn.tsinghua.edu.cn
> - **学号**（`--username`）— 你的学生证号，如 2025013187
> - **姓名**（`--name`）— 你的真实姓名

#### 查看待办

对 AI 说：**"查看待办"** 或 **"看看有什么作业"**

AI 会列出所有课程的最新动态：
- 未交作业及截止日期
- 未读公告和未浏览课件
- 已提交但老师还没批的作业（老师批改后会自动汇报评语和分数）
- 工作区缓存大小

AI 还会主动问你是否需要标已读、清理缓存。

> 你也可以设置每日自动查看：将 `todos_api.py` 配置为定时任务即可。

#### 提交作业

**方式一：直接发送 PDF 文件**

对 AI 说：**"我要交某某课程的作业"**，然后发送 PDF 文件即可。

**方式二：发送多张图片合并为 PDF**

先说：**"我要交某某课程的作业，我发几张图片给你"**

然后**按顺序**发送图片（先发的会在最终 PDF 的第一页，后发的在后面）。最后说：**"已经上传完毕"**

AI 会先列出要提交的课程、作业标题、文件名，请你确认。确认后自动：
1. 按你发送的顺序命名图片（001、002...）
2. 合并为 PDF（按文件名排序，所以先发的在 PDF 前面）
3. 重命名为 `学号_姓名.pdf`
4. 提交到指定作业

#### 下载课件

对 AI 说：**"帮我下载微积分的课件"**

AI 会列出课程的全部课件文件。你也可以更精确地指定：

- **"下载未读课件"** — 只下载还没看过的课件
- **"下载概率论第 8 讲的课件"** — 下载指定名称的文件
- **"把微积分的课件全部下载到 D 盘"** — 批量下载到指定目录

AI 会在下载前列出文件清单让你确认。

#### 查看通知和作业详情

对 AI 说：

- **"看看微积分最近有什么通知"** — 查看指定课程的公告
- **"概率论 HW10 的作业内容是什么"** — 查看作业的题目和附件
- **"上次交的物理作业老师批了吗"** — 查看已批改作业的评语和分数
- **"看看英语课有什么讨论"** — 查看课程讨论区

#### 清理工作区

AI 在查看待办时会主动提醒你工作区有缓存。这些缓存是下载的课件、合并 PDF 时的临时图片、调试日志等文件，不影响功能但会占用磁盘空间。

只需说 **"好"** 或 **"清理吧"**，AI 会先列出待清理的文件让你确认，确认后自动删除。

#### 其他

如果有这里没列出的需求，直接告诉 AI 你想做什么即可。AI 会根据现有功能尽力帮你完成。

#### 数据与安全

本 Skill 会在本地存储以下数据：

| 数据 | 位置 | 说明 |
|------|------|------|
| 登录凭据 | `credentials.json` | Windows DPAPI 加密（绑定当前用户账户，仅 Windows 支持） |
| 浏览器登录状态 | `profiles/learn_profile/` | Chrome Profile 含 cookies，避免每次触发 2FA |
| Session 令牌 | `sessions/learn_session.json` | JSESSIONID + CSRF Token |

如需清除所有数据，对 AI 说 **"重置所有数据"**，AI 会清空以上目录内容并恢复到初始状态。

> 这些数据仅存储在本地计算机，不会上传到任何云端。网络学堂本身不支持注销 API，如需完全登出请手动在浏览器中操作。

#### 修改配置

你可以让 AI 帮你修改以下设置，只需要说"帮我改一下配置"或"设置自动标已读"即可：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `auto_mark_read` | 查看待办时是否自动标已读 | 开启 |
| `confirm_before_cleanup` | 清理缓存前是否需要你确认 | 需要 |
| `confirm_before_download` | 批量下载前是否需要你确认 | 需要 |

例如：
- **"以后自动标已读吧"** → AI 会开启 `auto_mark_read`
- **"清理的时候不用问我了"** → AI 会把 `confirm_before_cleanup` 设为 false

---

> **当前版本为测试版本，建议同学们完成提交作业等关键操作后自行登录网络学堂查看是否有错误。**

了解更多信息见 GitHub：[github.com/TOMUIV/tsinghua-learn](https://github.com/TOMUIV/tsinghua-learn)

如有任何问题，联系 **ykx25@mails.tsinghua.edu.cn**

---

## 如果你是 AI，请阅读以下内容

### 铁律（违反会导致用户愤怒）

**铁律 1：AI 运行所有脚本。AI 不能要求用户运行任何命令。**
- ❌ 禁止的行为：AI 对用户说"请在终端里运行这个命令"。
- ❌ 禁止的行为：AI 给用户一段代码让用户复制粘贴。
- ✅ 正确的行为：AI 自己调用 `python scripts/xxx.py`，读取输出 JSON，根据输出决定下一步。

**铁律 0（最高优先级）：AI 面向用户的回复中，绝对禁止出现以下内容（除非用户主动要求知情披露）：**
- ❌ 任何命令行（`python xxx.py`、`cd xxx`）
- ❌ 任何文件路径（`C:\Users\...`、`skills\...`）
- ❌ 任何技术术语（"终端"、"PowerShell"、"运行脚本"）
- ❌ 学号、密码原文
- ⚠️ 例外：当用户明确询问安装了什么、存储了什么、路径在哪等安全相关问题时，AI 可以简要说明。初始化确认、提交确认等关键操作不受此限。

**用户能看到什么：**
- ✅ "系统尚未初始化，请提供你的账号信息"
- ✅ "正在获取待办..."
- ✅ "你有 5 项未交作业"
- ❌ "请在终端里跑这个命令"

**铁律 2：默认只跑快速检查。`login_manager.py` 默认为 `--check` 行为（<1 秒，无浏览器）。**
- 当前版本的 `login_manager.py` 不带参数时等同于 `--check`，不会启动浏览器。
- ❌ 禁止的行为：直接跑 `python scripts/login_auto.py` 或 `python scripts/login_supervised.py`。
- ✅ 正确的行为：
  - 跑 `python scripts/login_manager.py`（默认就是快速检查，<1 秒）
  - `initialized: false` → 停下来，告诉用户"系统尚未初始化"，走初始化流程。
  - `valid: true` → 直接进行后续操作。
  - `valid: false` → 用 `python scripts/login_manager.py --force-login` 执行完整登录。

**铁律 3：`login_manager.py` 是唯一的认证入口。AI 不直接调用其他登录脚本。**
- AI 不直接调用 `login_auto.py`。
- AI 不直接调用 `login_supervised.py`。
- AI 不直接调用 `install_playwright.py`。
- 上述脚本由 `login_manager.py` 在内部自动调用。

**铁律 4：AI 不凭经验推断问题。所有判断基于脚本输出的 JSON。**

**铁律 5：密码仅用于初始化收集，之后绝不在对话中重复展示。**
- 初始化时 AI 询问密码，收集后立即传入脚本，不在后续对话中提及密码值。
- AI 展示 `fields` 内容时，密码字段已脱敏（显示为 `xxx***`）。
- ❌ 禁止的行为：AI 在初始化之外的对话中说密码原文。

**铁律 6（提交确认）：提交作业必须先调用不带 --confirm 的上传预览，获得用户明确同意后才能加 --confirm 执行。**
- ❌ 禁止的行为：AI 直接加 --confirm 提交，不展示预览。
- ✅ 正确的行为：先不带 --confirm 调 upload 得到 preview JSON → 展示用户 → 同意后再加 --confirm

---

### 凭据字段速查

| 字段 | CLI 参数 | 说明 |
|------|---------|------|
| 网络学堂登录账号 | `--learn-account` | 登录 learn.tsinghua.edu.cn 用的账号 |
| 登录密码 | `--password` | 网络学堂登录密码，仅发送至 id.tsinghua.edu.cn（CAS）和 learn.tsinghua.edu.cn |
| 学号 | `--username` | 学生证号 |
| 姓名 | `--name` | 真实姓名 |

> 学号和网络学堂登录账号可能相同也可能不同，分别问清楚。
> ⚠️ 表中没有示例值。AI 不要编造学号或任何数字作为示例。

---

### 脚本速查

| 脚本 | AI 什么时候需要调用它 | 速度 |
|------|---------------------|------|
| `login_manager.py` | 默认快速检查（<1s），有--init/--reset/--force-login/--verify | ⚡快/🐢慢 |
| `todos_api.py` | 用户要求查看待办时 | ⚡快（2-5s） |
| `ops.py` | 下载文件、上传作业、合并PDF、清理工作区 | ⚡快 |
| `learn_api.py` | 查询课程列表、公告详情、作业内容 | ⚡快 |
| `pdf_merge.py` | 图片合并PDF（ops.py内部调用） | ⚡快 |
| `install_deps.py` | AI不直接调用（--verify内部自动调用） | 🐢慢 |
| `install_playwright.py` | AI不直接调用 | 🐢慢 |
| `login_auto.py` | AI不直接调用 | 🐢慢（有浏览器） |
| `login_supervised.py` | AI不直接调用 | 🐢慢（有浏览器） |

> ⚠️ 标🐢的脚本涉及浏览器/docker/下载，AI不应直接调用。它们由 `login_manager.py --force-login` 或 `--verify` 内部自动调用。

---

### 初始化流程

用户说"开始初始化"时，AI 按以下步骤执行：

**Step 1：向用户收集信息**
```
AI 依次问用户（不要一次全问，分步问）：
第一部分（必须）：
1. 网络学堂登录账号是什么？
2. 登录密码是什么？
3. 学号是什么？
4. 姓名是什么？

第二部分（选填，用户回答了必须信息后再问）：
5. 是否需要自动标已读？（默认：是）
6. 清理工作区前是否需要确认？（默认：是）
7. 批量下载前是否需要确认？（默认：是）

⚠️ AI 不编造示例值（不要写"如 2025013187"之类的数字）
⚠️ AI 不显示学号或密码在对话中
```

**Step 2：AI 调用 `--init` 保存凭据**
```
1. AI 将凭据 JSON 写入临时文件（不包含在任何命令字符串中）
2. 命令：python scripts/login_manager.py --init --cred-stdin < /tmp/cred_temp.json
3. AI 立即删除临时文件
输出：{"status":"ok", "fields":{"learn_account":"...", "username":"...", "name":"..."}}
```
> 使用临时文件 + stdin 重定向，密码只存在于临时文件中（随即删除），不出现在任何命令行参数或 echo 字符串中。

**Step 3：AI 向用户展示 fields 内容，请用户确认**

**Step 4：用户确认后，AI 调用 `--verify` 验证环境并尝试登录**
```
命令：python scripts/login_manager.py --verify
输出：{"python":true, "deps":true, "chromium":true, "login":true, "needs_2fa":false}

login=true       → Step 5
needs_2fa=true   → AI 告诉用户"自动登录失败，请打开浏览器完成二次验证"
                   用户说"好了"后，AI 调用：python scripts/login_manager.py
```

**Step 5：AI 调用 `todos_api.py` 首次查看待办**
```
命令：python scripts/todos_api.py
输出：JSON（含课程列表、待办数量等，submissions 日志自动初始化）
```

---

### 日常查看待办流程

任何时候用户说"查看待办""有什么作业""看看通知"时：

**Step 1：AI 检查凭据和 session**

跑默认命令（快速检查，<1 秒，无浏览器）：
```
命令：python scripts/login_manager.py
输出：{"initialized": false/true, "valid": false/true, "age_h": ...}
```

根据输出决定下一步：

① `initialized: false` → AI 停下来，告诉用户"系统尚未初始化"，走初始化流程
② `initialized: true, valid: true` → 跳到 Step 2（获取待办）
③ `initialized: true, valid: false` → AI 跑 `python scripts/login_manager.py --force-login`（会启动浏览器，约30-60秒）

**Step 2：AI 获取待办数据**
```
命令：python scripts/todos_api.py
输出：JSON 包含 courses、suggestions、graded_homeworks、cleanup_suggestion
```

**Step 3：AI 根据输出中的字段决定问用户什么**

检查 `graded_homeworks` 字段：
- 如果有内容 → AI 告诉用户"老师批改了你的作业：[课程名][标题]，评语：[comment]，得分：[score]"

检查 `submissions_tracked` 字段：
- 如果 > 0 → AI 告诉用户"有 N 个已提交的作业等待老师批改，批改后我会通知你"

检查 `suggestions` 数组：
- 如果包含 "运行 --mark-read" → AI 问用户"需要把未读公告和课件标为已读吗？" 同意后加 --confirm 执行
- 如果包含 "运行 --cleanup-preview" → AI 问用户"需要看看工作区有哪些垃圾文件吗？"

检查 `suggestions` 和 `graded_homeworks` 都不存在时：
- AI 告诉用户"目前没有新的待办事项"

**Step 4：用户同意后，AI 自己运行对应命令**
```
标已读：        python scripts/todos_api.py --mark-read
清理预览：      python scripts/ops.py --action cleanup --dry-run
执行清理：      python scripts/ops.py --action cleanup
```

---

### 提交作业流程

用户说"我要交作业"或发来文件/图片时：

**Step 1：AI 确认要交到哪个作业**
```
命令：python scripts/learn_api.py --action courses
输出：课程列表（AI 找到用户说的课程，记录 wlkcid）

命令：python scripts/learn_api.py --action homeworks --course <wlkcid>
输出：作业列表（AI 找到用户说的作业，记录 xszyid）
```

**Step 2：AI 处理文件**

情况 A — 用户直接发送了 PDF 文件：
```
AI 将文件保存到 uploads/，进入 Step 3
```

情况 B — 用户发送多张图片（如 QQ 传图）：
```
AI 每收到一张图，保存到 uploads/，按顺序命名为 001.jpg、002.jpg...
用户说"已经上传完毕"后：
命令：python scripts/ops.py --action pdf-merge --input-dir uploads/
输出：merged.pdf
AI 删除 uploads/ 下的所有图片文件
进入 Step 3
```

**Step 3：AI 展示确认信息，获得同意后提交**

```
先执行未确认的提交（展示详情，不实际提交）：
命令：python scripts/ops.py --action upload --course <wlkcid> --xszyid <xszyid> --file <path>
输出：{"status":"pending", "requiring":"confirmation", "details":{...}}

AI 必须向用户展示：
- 课程名称
- 作业标题
- 待提交的文件名
- 提交账号（姓名+学号脱敏）

例："准备提交 微积分(2) 的 第四次书面作业，文件：2025013187_张三.pdf。确认吗？"

用户明确说"确认"/"好"/"提交"后，AI 添加 --confirm 重新执行：
命令：python scripts/ops.py --action upload --course <wlkcid> --xszyid <xszyid> --file <path> --confirm
输出：{"status":"ok"}
```

**Step 4：AI 通知用户提交成功，清理临时文件**

---

### 下载课件流程

用户说"帮我下载课件"时：

**Step 1：AI 获取课程列表**
```
命令：python scripts/learn_api.py --action courses
输出：课程列表（AI 找到用户说的课程，记录 wlkcid）
```

**Step 2：AI 下载文件**
```
命令：python scripts/ops.py --action download-all --course <wlkcid> --save-dir <目录>
输出：下载结果
```
如果用户指定了具体文件名或模式，在 `--pattern` 参数中指定。

---

### 常见问题处理

**Session 过期**
```
AI 不分析 session 文件。不检查时间戳。不自己调 login_auto.py。
只做一件事：
命令：python scripts/login_manager.py
输出：session 有效则返回，无效则自动续期
```

**需要二次验证（2FA）**
```
login_manager.py 或 --verify 返回 needs_2fa=true 时：
Step 1：AI 告诉用户"自动登录失败，请打开浏览器完成二次验证"
Step 2：用户说"好了"后，AI 调用：
命令：python scripts/login_manager.py
输出：验证 session 是否已建立
```

**凭据未初始化**
```
login_manager.py --check 返回 initialized=false 时：
AI 告诉用户"系统尚未初始化"，然后按初始化流程的 Step 1 开始收集信息
```

### 脚本概览

| 脚本 | 职责 | 什么时候用 |
|------|------|-----------|
| `login_manager.py` | 认证网关 | 任何操作前确保 session；初始化；验证环境 |
| `todos_api.py` | 日常管理 | 用户问待办、标已读、清理 |
| `ops.py` | 文件操作 | 下载、上传、合并 PDF、清理工作区 |
| `learn_api.py` | 数据查询 | 查课程列表、公告详情、作业内容 |
| `pdf_merge.py` | 图片→PDF | 用户发图片要交作业时 |
| `install_deps.py` | 依赖安装 | --verify 会自动调用，你不直接碰 |
| `_config.py` | 配置读取 | 你不直接碰 |
| `login_auto.py` | 无头登录 | 你不直接碰，login_manager 内部调用 |
| `login_supervised.py` | 2FA 登录 | 你不直接碰，login_manager 内部调用 |
| `install_playwright.py` | Chromium 安装 | --verify 会自动调用，你不直接碰 |

### 日常运行流程

任何时候用户问"查看待办""有什么作业"等：

```
① 先确保 session:
   python scripts/login_manager.py
   ← 如果 session 过期会自动续期

② 获取待办:
   python scripts/todos_api.py
   ← 得到 JSON {"courses": [...], "total_unread": N, "suggestions": [...], ...}

③ 解析输出，主动问用户:
   - suggestions 里有 "运行 --mark-read" → "需要帮你把未读公告和课件标为已读吗？"
   - cleanup_suggestion 不为空 → "工作区有垃圾文件，需要看看吗？"
   - graded_homeworks 有内容 → "老师批了你的作业，评语是..."

④ 用户确认后，自己跑对应命令:
    - 标已读: python scripts/todos_api.py --mark-read
   - 清理预览: python scripts/ops.py --action cleanup --dry-run
   - 执行清理: python scripts/ops.py --action cleanup
```

### 详细 CLI 命令

#### login_manager.py

```bash
python scripts/login_manager.py                                # 确保 session
python scripts/login_manager.py --check                        # 检查状态
python scripts/login_manager.py --init --learn-account=... --password=... --username=... --name=...
python scripts/login_manager.py --reset                        # 清空所有数据
python scripts/login_manager.py --verify                       # 验证环境（依赖+Chromium+登录）
```

退出码: 0=有效, 1=错误, 2=需人工 2FA, 3=未初始化

#### learn_api.py

```bash
python scripts/learn_api.py --action courses                               # 课程列表
python scripts/learn_api.py --action announcements --course <wlkcid>       # 公告列表
python scripts/learn_api.py --action announcement-detail --course <wlkcid> --id <ggid>  # 公告详细内容
python scripts/learn_api.py --action files --course <wlkcid>               # 课件列表
python scripts/learn_api.py --action homeworks --course <wlkcid>           # 作业列表
python scripts/learn_api.py --action homework-full --course <wlkcid> --id <zyid> --xszyid <xszyid>  # 作业完整信息（含评语）
python scripts/learn_api.py --action discussions --course <wlkcid>         # 讨论列表
python scripts/learn_api.py --action questionnaires --course <wlkcid>      # 问卷列表
python scripts/learn_api.py --action aggregated --course <wlkcid>          # 聚合查询
python scripts/learn_api.py --action mark-all-announcements-read --course <wlkcid>
python scripts/learn_api.py --action mark-all-files-read --course <wlkcid>
```

#### ops.py

```bash
python scripts/ops.py --action list-files --course <wlkcid> [--pattern "*.pdf"]
python scripts/ops.py --action download --course <wlkcid> --wjid <wjid>
python scripts/ops.py --action download --course <wlkcid> --wjid-list "id1,id2,..."
python scripts/ops.py --action download-all --course <wlkcid> [--pattern "*.pdf"]
python scripts/ops.py --action upload --course <wlkcid> --xszyid <xszyid> --file <path>
python scripts/ops.py --action upload --course <wlkcid> --xszyid <xszyid> --file <path> --confirm  # 确认后实际提交
python scripts/ops.py --action pdf-merge --input-dir <目录> [--output <路径>]
python scripts/ops.py --action move-in --file <source_path>
python scripts/ops.py --action cleanup --dry-run
python scripts/ops.py --action cleanup
```

#### todos_api.py

```bash
python scripts/todos_api.py                           # 代办汇总
python scripts/todos_api.py --mark-read --confirm              # + 标记可读项已读
python scripts/todos_api.py --cleanup-preview         # + 清理预览
python scripts/todos_api.py --cleanup                 # + 执行清理
```

**输出解析**：
- `suggestions` — AI 读取后应主动询问用户："需要帮你把未读公告和课件标为已读吗？""需要帮你看看工作区有哪些垃圾文件吗？"
- `graded_homeworks` — 老师新批改的作业及其评语/分数
- `new_submissions_logged` — 本次新增的已提交未批改作业数量

#### pdf_merge.py

```bash
python scripts/pdf_merge.py --input-dir <目录> [--output <路径>]
```

支持: jpg, jpeg, png, webp, bmp, heic, heif

### 常见任务工作流

#### 图片作业提交（QQ 发送图片）

```
1. 用户每发一张图 → AI 保存到 uploads/，按顺序命名为 001.jpg、002.jpg...
2. 用户说"发送完毕"
3. ops.py --action pdf-merge --input-dir uploads/ → merged.pdf
4. 删除 uploads/ 下所有图片（保留 merged.pdf）
5. ops.py --action upload --course ... --xszyid ... --file uploads/merged.pdf --confirm
   → 自动重命名为 学号_姓名.pdf
6. 删除 uploads/merged.pdf
```

#### 下载课件

```
learn_api.py --action courses                    # 获取课程列表+ID
ops.py --action download-all --course <wlkcid>   # 下载全部
```

### 提交日志机制

文件: `submissions/submissions_log.json`

```
todos_api.py 每次运行时:
  1. sync_submissions_log() → 扫描所有已交未批改作业，新出现的追加到日志（已存在则跳过）
  2. check_graded_submissions() → 遍历日志，检查是否有作业已被批改
     有 → 获取评语/分数，从日志中移除，在输出中加入 graded_homeworks
```

### 配置 (config.json)

```json
{
  "auto_mark_read": false,
  "confirm_before_cleanup": true,
  "confirm_before_download": true
}
```

| 选项 | 说明 | 默认 |
|------|------|------|
| `auto_mark_read` | 运行 `todos_api.py` 时自动标已读 | `false` |
| `confirm_before_cleanup` | 清理前是否需用户确认 | `true` |
| `confirm_before_download` | 批量下载前是否需用户确认 | `true` |

### 未读判断标准

| 模块 | API 字段 | 过滤值 |
|------|----------|--------|
| 作业 | `zt` | `"未交"` |
| 公告 | `sfyd` | `"否"` |
| 课件 | `isNew` | `"1"` |
| 讨论 | `htsl` | `>0` |

### 注意事项与不可做清单

#### 不可做

- **不要硬编码课程 ID、学期、路径、姓名**
- **不要在脚本中使用 `input()` 或 `getpass()`** — AI 运行脚本，不能阻塞
- **不要直接修改 `credentials.json`** — 通过 `login_manager.py --init` 操作
- **不要创建新脚本除非绝对必要**
- **不要在 `config.json` 之外的地方存储用户信息**
- **不要告诉用户命令行操作** — 用户只回答"要/不要"，AI 代为执行

#### 注意事项

- **文件名编码**：服务器将 UTF-8 的中文文件名以 latin-1 编码发送，`download_file()` 已做修复
- **作业提交端点**：真实端点是 `/b/wlxt/kczy/zy/student/tjzy`，不是 `uploadFile/saveXszj`
- **公告标已读**：端点 GET `/f/wlxt/kcgg/wlkc_ggb/student/beforeViewXs`，不是 `saveYd`
- **公告内容**：直接从列表 API 的 `ggnr` base64 字段解码
- **学期自动检测**：每次建立 session 后调用 `get_current_semester()`
- **重置**：`login_manager.py --reset` 保留所有文件结构，只清空内容
- **已提交的作业无法撤回**：网络学堂不提供撤回已提交作业的 API
