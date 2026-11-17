---
name: campus
description: 清华校园服务技能包（统一入口）。涵盖网络学堂/课表/成绩/培养方案/第二成绩单/选课/邮箱/文献/图书馆/座位预约/研读间/校内通知/水木搜索/高德地图/**校内大模型（MAD：DeepSeek-V4.1-Flash / qwen3.8-27b / DeepSeek-R1-W8A8，含本地 OpenAI 代理）** 等校园事务。当用户提到"校园服务、网络学堂、作业、课表、成绩、邮箱、文献、图书馆、座位、研读间、校内通知、搜书、地图、路径、清华附近吃饭、**清华的 Deepseek / 校内大模型 / madmodel**"等需求时使用。第一次使用需先初始化（install → creds → login → 统一 .env）。
metadata:
  openclaw:
    requires:
      env:
        - CAS_PASSWORD
    os:
      - windows
      - macos
      - linux
---

# 清华校园服务技能包

## 👤 人类可读区

> 如果你是人类用户：想知道这个技能包能干什么、怎么安装、安不安全？
> 直接对 AI 说一句 **"这个是做什么的？"**，AI 会给你讲清楚，不用自己读文档。

---

# 主技能（AI 操作手册）

> 一个技能包，多项校园服务。主 SKILL 负责**路由 + 凭据门槛 + 汇总**，业务逻辑在各子 SKILL。

---

## 如果你是 AI，请阅读以下内容

### ⚠️ 版本与自修声明（完整版见根 `SKILL.md` 新手指引 Caveat）

- 本技能包仍在迭代中，主功能已测试可用（learn/search/literature/timetable/transcript/program/course/ts2/library/mail/info/amap/madmodel）
- 遇到 bug（脚本报错/接口变更/登录失效）时，**AI 可自行修改本包代码修复**，不必等用户
- 约束：只改出问题的模块，**禁止动已测试通过的核心路径**（install/creds/base-cas 底座）
- 回归：修复后跑 `tests/smoke_test.py` + 实测一次真实数据

### 铁律（违反会导致用户愤怒）

- **铁律 1：AI 运行所有脚本**。AI 不能要求用户敲命令、复制粘贴代码。
- **铁律 2：脚本是面向 AI 的**。所有脚本 stdout 输出 JSON（绝不写 stderr——Windows PowerShell 会把 stderr 渲染成 `python.exe : ...` 报错），进度写 `runtime/logs/campus.log`。AI 必须读 JSON 决定下一步。
- **铁律 3：AI 绝不自己阻塞**。任何脚本都不含 `input()`/`getpass()`。需要用户输入（如验证码）时走**两阶段协议**：脚本立即退出返回 pending token，AI 问用户拿码后再提交。
- **铁律 4：凭据不入命令行**。所有密码/密钥经 `--value-stdin` 传入，AI 展示时脱敏。
- **铁律 5：不硬编码**。不写死学号、课程、学期、路径。全部走 creds/配置。
- **铁律 6：隐私红线**。面向用户输出绝不出现密码原文；学号/姓名脱敏（`202***`）。
- **铁律 7：单 Chromium 运行（强提示）**。本技能全部 CDP 脚本共用**同一个**无头 Chromium（`runtime/browser/cdp.pid` + `cdp.port` 记录端口）。**浏览器一律即用即退**（保留的是 session cookie 文件 + profile 指纹，不是浏览器进程）。**运行任何脚本前必须先检查是否已有 Chromium 在运行**：
  1. `python base-cas/scripts/browser.py --check` → 看 `cdp_running`。
  2. `cdp_running: false` → 干净，可启动。
  3. `cdp_running: true` → **当前环境不干净**，禁止直接跑业务脚本。先排查占用者：Windows 用 `Get-Process chrome` / `tasklist /FI "IMAGENAME eq chrome.exe"` 列 PID 与启动时间；macOS/Linux 用 `ps aux | grep chrome`。
     - 若占用者是**2FA 登录流程中的浏览器**（`login.py --ensure` 触发验证码后、`--submit-code` 完成前，属正常）→ 直接复用该浏览器，先完成登录再继续。
     - 若是**孤儿/残留进程**（pid 文件与端口监听者不匹配，或非本技能启动）→ `browser.py --stop` 清理后再跑。
     - **严禁**在 Chromium 被占用时并行启动第二个 CDP 脚本（端口冲突 → "CDP 浏览器启动失败，端口未就绪"）。所有 CDP 脚本必须**串行**执行。
  4. `browser.py --start` 报成功但 login 仍 `ECONNRESET`（浏览器进程已死）→ profile 内 GPU 缓存损坏（GraphiteDawnCache 等）致 Chrome 崩溃。`browser.py --start` 已内置自愈：启动失败自动清理损坏缓存并重试一次。仍失败则 `browser.py --stop` 后清空 `runtime/profiles/cdp_profile` 中缓存目录重试。

### 路由逻辑（主 SKILL 只做这些）

```
用户请求 → 判断意图：
  初始化/环境 → install SKILL
  配置凭据   → creds SKILL（status/guide <system>/add）
  重置凭据   → creds.py reset <system> --confirm（按系统：cas/literature/mail/llm，独立重置）
  重置 CAS 登录态 → base-cas login.py --reset（仅 CAS：凭据+session+浏览器 profile）
  网络学堂   → learn SKILL（子）
  搜索校园信息 → search SKILL（子：info/its/learn 多源搜索）
  课表考试   → timetable SKILL（子）
  成绩/绩点 → transcript SKILL（子）
  培养方案/学分 → program SKILL（子）
  选课/已选课程 → course SKILL（子）
  第二成绩单/课外经历 → ts2 SKILL（子）
  图书馆/座位/研读间 → library SKILL（子，含研读间占用+预约人）
邮箱       → mail SKILL（子）
  文献检索   → literature SKILL（子，4 源：Scopus/arXiv/OpenAlex/Crossref）
  校内通知   → info SKILL（子）
  图书馆座位 → library SKILL（子）
  地图/POI/路径/天气/地理编码 → amap SKILL（子）
  MAD / 清华 Deepseek / 校内 LLM 服务（OpenAI 兼容；可作对话·批量抽取·**需要模型的评测/基准**的后端） → madmodel SKILL（子，独立模块）
  校内通知   → info SKILL（子）
  意图不明   → 列出能力范围，不瞎猜
```

**两个重置入口的职责边界（为什么有两个）**：

| 入口 | 管什么 | 范围 |
|------|--------|------|
| `creds.py reset <system>` | **凭据存储层**：加密保险箱中该域条目（cas/literature/mail/llm 各自独立） | 只清凭据，不动登录态 |
| `login.py --reset` | **CAS 登录层**：CAS 凭据 + learn/info session + CDP 浏览器 profile | 只清 CAS，文献/邮件/LLM 凭据保留 |

> 原因：`creds.py` 是所有系统的**凭据仓库**（能按系统单独管理）；`login.py` 只管 **CAS 认证**（含登录态 session/profile），所以它的 reset 只覆盖 CAS 系统。想重置某个非 CAS 系统（如文献 key），用 `creds.py reset literature`。

**路由前置检查（每次用户请求前）**：
1. 跑 `python creds/scripts/creds.py status`
2. 若涉及的系统凭据未配置 → 引导用户 `creds.py guide <system>`（cas/literature/mail/llm）说明该系统的凭据及用途，再 `add`
3. 若涉及 CAS 系统 → 先 `python base-cas/scripts/login.py --system <name> --ensure`
   - 返回 `needs: 2fa_code` → 问用户拿验证码 → `--submit-code <token> <code>`
   - 返回 `session_valid: true` → 继续路由到子 SKILL

> **浏览器模式**：base-cas 一律**无头模式（headless）**运行——AI 自动流程、WSL 无显示器、全新机器均无需人工浏览器。**浏览器即用即退**：保留的是 session cookie（落盘 `runtime/sessions/*.json`，含完整 cookie 快照）+ profile 指纹（`runtime/profiles/cdp_profile`），**不是浏览器进程**。每个任务用完立即关闭浏览器（`browser.py --stop` / 脚本 finally）。仅 **2FA 登录流程内**浏览器保持打开等待用户填码（`--ensure` 到 `--submit-code` 之间），完成后即关。信任机制：THU 按浏览器指纹判断二次验证，首次登录走 saveFinger 信任后，同 profile 重启免 2FA；下次任务先验证 cookie 有效性，失效则自动 fall back base-cas 重新登录。
>
> **info 门户 service 登录（transcript/timetable/program）**：应用导航页（学生工作台）是 webvpn 根路径之外的**独立 CAS service**。脚本访问应用导航页若跳 CAS，会自动调用 `login.ensure_apps_service(page)` 完成该 service 登录（信任浏览器免密/自动填表），无需 AI 额外操作。若脚本报"info 会话仍无效"，删 `runtime/sessions/info.json` 后重跑即可。

### 脚本位置速查

| 模块 | 脚本 | 用途 |
|------|------|------|
| install | `install/scripts/install.py --full` | 装环境（浏览器+依赖） |
| install | `install/scripts/selfcheck.py` | 环境自检 |
| install | `install/scripts/fetch_artifacts.py --all` | 镜像下载（腾讯云优先） |
| creds | `creds/scripts/creds.py status` | 凭据状态（按系统分组） |
| creds | `creds/scripts/creds.py guide <system>` | 某系统凭据责任告知（cas/literature/mail/llm） |
| creds | `creds/scripts/creds.py reset <system> --confirm` | 重置某系统凭据（独立，不影响其他系统） |
| base-cas | `base-cas/scripts/login.py --system X --ensure` | CAS 登录（两阶段） |
| base-cas | `base-cas/scripts/session.py --list` | 查看各系统 session |
| search | `search/scripts/search.py --query <词>` | 多源搜索（info/its/learn） |
| literature | `literature/scripts/literature.py search -q <检索式> [--source scopus|arxiv|openalex|crossref|all]` | 多源文献检索（4 源，免费源 arxiv/openalex/crossref 不需 Key） |
| timetable | `timetable/scripts/timetable.py` | 课表查询 |
| transcript | `transcript/scripts/transcript.py` | 成绩单查询 |
| program | `program/scripts/program.py` | 培养方案查询 |
| course | `course/scripts/course.py enrolled` | 选课查询（已选课程） |
| ts2 | `ts2/scripts/ts2.py status|list|export` | 第二成绩单查询/导出 |
| library | `library/scripts/library.py seat|areas|my-bookings|rooms|book|cancel` | 图书馆查询/选座预约 |
| mail | `mail/scripts/mail.py list|read|send|mark-read` | 收发邮件 |
| info | `info/scripts/info.py notices|read|search` | 校内通知/水木搜索 |

> 开发文档：`../docs/subskill-template.md`、`../docs/learn-verify.md`、`../docs/handoff.md`

### 各子 SKILL 所需凭据（按系统分组，向用户索取，全部存加密保险箱）

> 📄 AI 配置指引：`skill/campus/CREDS.md`（按系统拆分，含各域 key/用途/申请途径/配置命令，供 LLM 指导配置）

| 系统域 | 子 SKILL | 需要的凭据 | 用途 |
|--------|---------|-----------|------|
| **CAS**（id.tsinghua.edu.cn） | learn / info / timetable / library | `cas_username` / `cas_password` | 清华统一认证登录（共用一套） |
| **CAS**（可选） | learn | `student_id` / `student_name` | 作业文件命名（缺省用 CAS 账号） |
| **文献**（api.elsevier.com） | literature | `scopus_api_key`（+`scopus_inst_token` 可选） | Scopus 文献检索鉴权/提配额 |
| **OpenAlex**（api.openalex.org） | literature | `OPENALEX_API_KEY`（可选，免费源无 key 也能用） | OpenAlex 元数据检索高级额度 |
| **高德**（restapi.amap.com） | amap | `AMAP_KEY`（统一 .env） | 高德地图 Web 服务 API（地点/POI/路径/天气/地理编码） |
| **LLM**（api.deepseek.com） | learn 预批改 / literature 摘要 | `deepseek_api_key` | LLM 摘要/预批改（可选） |
| **邮件**（IMAP/SMTP） | mail | `MAIL_ACCOUNTS`（统一 .env） | 收发邮件 |

> **凭据存储（加密保险箱）**：CAS 等安全凭据走 `creds.py`，全部存进**单个加密保险箱** `campus/runtime/credentials.enc`（Fernet 加密的 JSON）。解密只需**一个主密钥**，来源优先级：① 环境变量 `CAMPUS_MASTER_KEY`（跨机同步用）② OS keyring 单条（本机绑定，自动生成）③ `campus/runtime/vault/master.key`（0600，兜底）。邮箱等用户级大配置统一在 `campus/.env`（见 `.env.example`）。两者都被 git 忽略，不出设备。
>
> **跨机同步**：保险箱文件随 SKILL 文件夹同步；在新设备设同一个 `CAMPUS_MASTER_KEY`（`creds.py key show` 可在旧设备读出，`creds.py key set` 可显式设置）即可解密。没有主密钥则保险箱无法解开（文件夹泄露 ≠ 凭据泄露）。

### 初始化流程（AI 首次面对新用户）

```
Step 1: install.py --check → 若缺环境 → install.py --full（腾讯云镜像，自动换源）
Step 2: creds.py status → 按系统分组 guide + add（值必须经 --value-stdin 直传，禁止写临时文件明文）
        - CAS 必需：cas_username / cas_password（learn/info/library 都要）
        - 其余按需索取：scopus_api_key（文献）、deepseek（摘要）
Step 3: 复制 campus/.env.example 为 .env，填写学号/姓名/CAS 密码/邮箱（MAIL_ACCOUNTS）
Step 4: base-cas login.py --system learn --ensure → 验证 CAS
Step 5: 全部就绪 → 告诉用户"已初始化完成，可以说'查看待办'等"
```

> **凭据输入铁律（隐私）**：用户提供的账号/密码**必须**经 `creds.py add <key> --value-stdin` 的 stdin 直传（值只在内存 → 写入加密保险箱 `credentials.enc`）。**禁止**先写临时 JSON/文件再读（那会产生明文落盘窗口）。PowerShell 下管道传中文/特殊字符已实测无损（`$OutputEncoding` 设 UTF-8；脚本已做 BOM/\r\n 清理）。对话历史中的明文无法避免，但磁盘不留明文。
> 用户前提：机器已装 Python 3.10+。若连 Python 都没有，告知用户先装 Python（产品假设，不自动装）。

### 各子 SKILL 入口

| 子 SKILL | 目录 | 能力 | 状态 |
|---------|------|------|------|
| learn | `learn/` | 查待办/交作业/下载课件/成绩/AI预批改 | ✅ 已实现 |
| search | `search/` | 多源搜索（info 通知/its 服务/learn 课件，结果带来源） | ✅ 已实现 |
| literature | `literature/` | 多源文献检索/摘要/引用（Scopus/arXiv/OpenAlex/Crossref） | ✅ 已实现 |
| timetable | `timetable/` | 课表查询（星期×节次 + 未安排课程） | ✅ 已实现 |
| transcript | `transcript/` | 成绩单（全部课程成绩 + 总学分/绩点） | ✅ 已实现 |
| program | `program/` | 培养方案完成情况（课组完成度 + 应修/完成学分） | ✅ 已实现 |
| course | `course/` | 选课查询（已选课程 enrolled 可用；开课信息/评教非选课季锁定） | 🟡 部分实现（选课季/校内网完善） |
| ts2 | `ts2/` | 第二成绩单（课外经历 19 模块 + 填报状态 + 导出官方 PDF） | ✅ 已实现 |
| library | `library/` | 图书馆（座位余量/分布公开 + 选座预约 book/cancel + 我的预约 + 研读间占用） | ✅ 已实现 |
| mail | `mail/` | 收发邮件（配置在统一 campus/.env） | ✅ 已实现 |
| info | `info/` | 校内通知查询 + 水木搜索（馆藏检索） | ✅ 已实现 |
| amap | `amap/` | 高德地图（地点/POI/周边/路径规划/地理编码/天气/IP/行政区划/距离/静态地图） | ✅ 已实现 |
| madmodel | `madmodel/` | 清华 MAD 大模型（模型列表 + token 取/刷新 + 对话 + 本地 OpenAI 兼容代理）；**独立模块**，只依赖 base-cas/creds/common | ✅ 已实现（实验） |

> `course` 选课系统：登录链路已逆向（含验证码两阶段），`enrolled` 已选课程可用；开课信息/评教按学期开放，非选课季锁定。完整逆向笔记见 `../docs/course-reverse-notes.md`（供后续同学接手）。
> 第二成绩单（`ts2/`）已实现：课外经历 19 模块查询 + 填报状态，直连无需 webvpn，全年可用。
> `library`（`library/`）已实现：座位余量（公开）+ 座位分布（公开）+ 选座预约 book/cancel + 我的预约 + 研读间占用。我的图书馆（discover.lib 借阅记录）登录在 CDP 环境受限（第三方认证拦截），完整逆向笔记见 `../docs/library-reverse-notes.md`。
> `mail`（`mail/`）已实现：收发邮件，配置统一在 `campus/.env`（`MAIL_ACCOUNTS`）。
> `info`（`info/`）已实现：校内通知查询（分类列表 + 详情全文）。

### 面向用户的话术

- 不要说命令行/路径/技术术语（除非用户主动问）。
- "查看待办" → 自动走 learn；"我的课表" → 自动走 timetable。
- 每件事做完要汇总结果，主动问下一步。

---

## 如果你是用户，请阅读以下内容

> 📖 想了解技能包能做什么、如何初始化，看仓库根目录 **[`README.md`](../../README.md)**（项目介绍）。

### 能做什么

对 AI 说一句话就能办校园事务：
- **"查看待办"** / "有什么作业" — 网络学堂待办、截止日期、老师批改反馈
- **"帮我搜一下 XX"** — 多源搜索（info 通知 / its 服务指南 / learn 课件），结果带来源
- **"下载 XX 课件的课件"** / "交 XX 作业" — 网络学堂文件操作
- **"我的课表"** / "最近有什么考试" — 课表与考试
- **"我的成绩"** / "绩点多少" — 成绩单
- **"培养方案"** / "学分还差多少" — 培养方案完成情况
- **"我选了哪些课"** — 选课查询（需校内网）
- **"我的第二成绩单"** / "课外经历" — 第二成绩单（保研/简历）
- **"图书馆还有座位吗"** / "研读间有空吗" — 座位余量/研读间占用
- **"谁订了北馆二楼研讨间"** / "研讨间预约情况" — 研读间/研讨间占用 + 预约人（脱敏，`library.py rooms --space <空间> [--date YYYYMMDD]`）
- **"明天哪里能约 4 小时研讨间"** / "哪些研讨间有空" — 各房间已预约时段 + 空闲窗口分析（`library.py free [--date YYYYMMDD] [--min-hours N]`）
- **"帮我约研讨间"** — 预约团体研讨间（写操作，需确认；`library.py book-room ... --confirm`）
  - ⚠️ 规则：**一人一天最多 4H**；**不能连续预约**（已有 14-18 则不能订 18-22，换房间也不行）；取消用 `library.py cancel-room --uuid <uuid> --confirm`
- **"帮我预约个座位"** / "取消预约" — 座位预约/取消（写操作，需确认）
- **"看邮件"** / "有什么新邮件" — 收发邮件
- **"最近有什么通知"** / "放假安排" — 校内通知
- **"帮我搜本书"** / "图书馆有 XX 吗" — 水木搜索馆藏检索
- **"帮我查文献"** — 多源文献检索（Scopus/arXiv/OpenAlex/Crossref）
- **"图书馆还有座位吗"** — 座位预约查询
- **"最近校内有什么通知"** — 信息查询
- **"清华主楼附近有什么吃的"** / "从主楼到六教怎么走" / "海淀今天天气" — 高德地图（地点/POI/周边/路径/天气）

### 第一次使用

对 AI 说 **"开始初始化"**，AI 会：
1. 检查/安装运行环境（自动从镜像下载，无需你操心）
2. 引导你配置凭据（告诉你去哪申请、用来干嘛）
3. 完成清华统一认证登录

### 隐私说明

- 你的凭据整体加密存进**单个保险箱文件**（AES 加密），解密用的**主密钥**存在系统安全存储（凭据管理器/Keychain/Secret Service）或环境变量 `CAMPUS_MASTER_KEY`；DLL 与文件夹里都看不到明文
- 保险箱可随 SKILL 文件夹同步到别的设备，但没有主密钥解不开（文件夹泄露 ≠ 凭据泄露）
- AI 不会在对话里重复你的密码
