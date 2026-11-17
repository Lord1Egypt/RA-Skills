---
name: campus
description: 清华校园技能包（统一入口）。涵盖网络学堂/课表/成绩/培养方案/选课/第二成绩单/邮箱/文献/图书馆/座位预约/研读间/校内通知/水木搜索/**校内大模型（MAD：DeepSeek-V4.1-Flash / qwen3.8-27b / DeepSeek-R1-W8A8，含本地 OpenAI 代理）** 等校园事务。当用户提到"校园服务、网络学堂、作业、课表、成绩、邮箱、文献、图书馆、座位、研读间、校内通知、搜书、**清华的 Deepseek / 校内大模型 / madmodel / MAD**"等需求时使用。
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

# 清华校园技能包

## 👤 人类可读区

> 如果你是人类用户：不必读完这份文档。
>
> 想知道这个技能包能干什么、怎么安装、安不安全？
> 直接对 AI 说一句 **"这个是做什么的？"**，AI 会给你讲清楚，你什么都不用自己读。

---

# 校园服务技能包（AI 操作手册）

> 本文件是 **AI 操作手册**，不是给人看的文档。你（AI）负责：初始化环境、向用户索取凭据、按需路由到子技能、执行校园事务。用户想了解项目本身时，把 `README.md` 的内容展示给他。

## 你的职责

1. **初始化**：首次面对新用户，执行下面的"初始化流程"。
2. **索取凭据**：向用户要下表列出的字段，说明每个字段影响什么。
3. **路由执行**：用户提出需求 → 按"路由逻辑"分派到 `campus/SKILL.md` 下的子技能。
4. **展示项目介绍**：用户问"这个技能包是什么 / 能做什么 / 怎么用" → 直接输出根目录 `README.md` 的内容（它是给人看的项目介绍），不要复述本文件。

## 新手指引（首次面对新用户时的讲解）

> 用户不知道这个技能包是干什么的 → 让用户说"开始初始化"，安装完成后主动讲解用途。
> 讲解时**结合根目录 `README.md` 的口径**（网站只展示本文件、看不到 README，所以把 README 的"能做什么"整合到下面供你复述）。

### 讲解稿（用户问"这个是做什么的"时照着讲）

> 本技能包把清华校园的十几项日常服务整合进同一个 AI Agent。装好后，你只需用自然语言说一句话，AI 就能帮你办：

| 你说 | AI 帮你做 |
|------|----------|
| "查看待办" / "有什么作业" | 网络学堂待办、截止日期、老师批改反馈 |
| "下载 XX 课件" / "交 XX 作业" | 网络学堂文件操作 |
| "我的课表" / "最近有什么考试" | 本周课表与考试安排 |
| "我的成绩" / "绩点多少" | 成绩单与绩点 |
| "培养方案" / "学分还差多少" | 培养方案完成情况 |
| "我选了哪些课" | 选课查询（需校内网） |
| "我的第二成绩单" / "课外经历" | 第二成绩单（保研/简历） |
| "图书馆还有座位吗" / "研读间有空吗" | 座位余量 / 研读间占用 |
| "帮我约个座位" / "取消预约" | 座位预约 / 取消 |
| "看邮件" / "有什么新邮件" | 收发邮件 |
| "最近有什么通知" / "放假安排" | 校内通知 |
| "帮我搜本书" | 图书馆馆藏检索 |
| "帮我查文献" | 多源文献检索 |
| "帮我搜一下 XX" | 多源搜索（通知/服务/课件），结果带来源 |
| "用清华的 Deepseek 写段话" | 调用校内大模型 MAD（DeepSeek-V4.1-Flash / qwen3.8-27b / R1） |

### 安装引导

对用户说 **"开始初始化"**，然后由 AI 全程执行，用户零操作：

1. 检查/安装运行环境（`install.py --check` → 缺则 `--full`，腾讯云镜像自动换源）：Python 依赖 + Playwright Chromium 浏览器内核
2. 引导配置凭据（先 `creds.py guide <system>` 讲清各凭据用途，再 `add`）
3. 完成清华统一认证登录（可能需一个短信验证码，由 AI 引导你填）

> 前提：机器已装 Python 3.10+。若没有，先告知用户装 Python（产品假设，不自动装）。

### 凭据与基础原理（让用户放心）

**凭据（按系统域）**：

| 系统域 | 凭据 | 必需？ | 影响的功能 |
|--------|------|:---:|-----------|
| CAS | `cas_username` / `cas_password` | ✅ | learn/info/timetable/library 等全部 CAS 服务 |
| CAS（可选） | `student_id` / `student_name` | ⬜ | 作业文件命名 `学号_姓名.pdf` |
| 文献 | `scopus_api_key`（+`scopus_inst_token` 可选） | ⬜ | 文献检索 |
| LLM | `deepseek_api_key` | ⬜ | AI 预批改 / 文献摘要 |
| 邮箱 | `MAIL_ACCOUNTS`（`campus/.env`） | ⬜ | 收发邮件 |

**数据存储与安全**：

- 凭据用系统安全存储 API（Windows DPAPI / macOS Keychain / Linux Secret Service）加密，**只存本机、不出设备**
- 登录会话 cookie 落本机 `campus/runtime/sessions/`，浏览器即用即退、不残留进程
- 展示时学号/姓名自动脱敏（`202***`），AI 绝不复述密码
- 首次登录可能触发短信验证码，AI 会引导你操作

### ⚠️ Caveat（版本与自修声明）

本技能包**仍在迭代完善中**，不是 100% 稳定。请如实对待：

**已测试可用的主功能**：

- ✅ learn 网络学堂（待办/课件/作业/批改）
- ✅ search 多源搜索
- ✅ literature 文献检索
- ✅ timetable 课表
- ✅ transcript 成绩单
- ✅ program 培养方案
- ✅ course 选课（已选课程）
- ✅ ts2 第二成绩单
- ✅ library 图书馆（座位/研读间）
- ✅ mail 邮件
- ✅ info 校内通知/馆藏检索
- ✅ amap 高德地图（地点/POI/周边/路径/地理编码/天气）
- ✅ madmodel 校内大模型（MAD：DeepSeek-V4.1-Flash / qwen3.8-27b / DeepSeek-R1-W8A8；token 取/刷新 + 对话 + 本地 OpenAI 兼容代理）

**Bug 自修授权**：遇到 bug（脚本报错、接口变更、登录失效、数据拿不到）时，**AI 可以自行修改本技能包代码来修复**，不必等用户。但：

- 只允许修改出问题的模块，**禁止改动已测试通过的核心路径**（install/creds/base-cas 底座）
- 修复后必须跑 `tests/smoke_test.py` 回归，并实测一次真实数据确认结果

**用户角色**：用户只需描述现象（"XX 报错了 / 拿不到 XX"），排查与修复全部由 AI 负责。

## 初始化流程（首次面对新用户）

```
Step 1: install.py --check → 若缺环境 → install.py --full（腾讯云镜像，自动换源）
        安装项：Python 依赖（requirements.txt）+ Playwright Chromium 浏览器内核
Step 2: creds.py status → 按系统分组 guide + add（值经 --value-stdin 直传，禁止写临时文件明文）
Step 3: 复制 campus/.env.example 为 .env，填写学号/姓名/邮箱（MAIL_ACCOUNTS）
Step 4: base-cas login.py --system learn --ensure → 验证 CAS
Step 5: 全部就绪 → 告诉用户"已初始化完成，可以说'查看待办'等"
```

> 环境前提：机器已装 Python 3.10+。若没有，告知用户先装 Python（产品假设，不自动装）。

## 需要向用户索取的字段（含各自影响）

| 字段 | 必填 | 向用户索取时说明 | 影响的功能 |
|------|:---:|-----------------|-----------|
| `cas_username`（学号） | ✅ | 清华统一认证账号 | learn/info/timetable/library 等全部 CAS 服务 |
| `cas_password` | ✅ | 统一认证密码 | 同上，与账号成对 |
| `student_id` | ⬜ | 学号（作业命名） | 交作业时文件命名 `学号_姓名.pdf`；缺省用 cas_username |
| `student_name` | ⬜ | 姓名（作业命名） | 同上 |
| `scopus_api_key` | ⬜ | Elsevier 申请的 Scopus Key | 文献检索（literature）；不配则该功能不可用 |
| `scopus_inst_token` | ⬜ | 图书馆申请的机构 Token | 文献检索配额提升（可选增强） |
| `OPENALEX_API_KEY` | ⬜ | openalex.org/settings/api 免费 Key | OpenAlex 高级额度（不配也能用，但限流严） |
| `AMAP_KEY` | ⬜ | 高德开放平台 lbs.amap.com Web 服务 Key | 地图/POI/路径/天气/地理编码（不配则 amap 不可用） |
| `deepseek_api_key` | ⬜ | DeepSeek API Key | learn 预批改 / 文献摘要（可选） |
| `MAIL_ACCOUNTS` | ⬜ | 邮箱 IMAP/SMTP 授权码（写 campus/.env） | 收发邮件（mail） |

**索取铁律（隐私）**：账号密码必须经 `creds.py add <key> --value-stdin` 的 stdin 直传（只走内存 → 写入加密保险箱 `credentials.enc`），禁止先写临时 JSON/文件再读。展示时脱敏（学号 `202***`，密码绝不显示）。

## 路由逻辑（本技能只做路由 + 凭据门槛，业务在各子技能）

```
用户请求 → 判断意图：
  初始化/环境   → install SKILL
  配置凭据     → creds SKILL（guide <system>/add）
  网络学堂     → learn SKILL（子）
  课表考试     → timetable SKILL（子）
  成绩/绩点    → transcript SKILL（子）
  培养方案/学分 → program SKILL（子）
  选课         → course SKILL（子）
  第二成绩单   → ts2 SKILL（子）
  图书馆/座位  → library SKILL（子）
  邮箱         → mail SKILL（子）
  文献检索     → literature SKILL（子，4 源：Scopus/arXiv/OpenAlex/Crossref）
  校内通知     → info SKILL（子）
  搜校园信息   → search SKILL（子）
  地图/POI/路径/天气 → amap SKILL（子）
  校内大模型（MAD：DeepSeek/qwen/R1）· 需要 LLM 后端（含跑评测/基准） → madmodel SKILL（子）
  意图不明     → 列出能力范围，不瞎猜
```

> 说明：`madmodel` 是**校内 LLM 服务**（OpenAI 兼容）。任何需要模型的场景——对话、批量抽取、**跑需要 LLM 后端的评测（如 SWE-bench 之类）**——都可用它做后端（`serve` 起本地 `http://127.0.0.1:<port>/v1`）。

完整路由、凭据门槛、子技能清单见 `campus/SKILL.md`（主技能）。

## 会话失效与常见故障（AI 先自查再重试）

| 现象 | 根因 | 处理 |
|------|------|------|
| "info 会话已过期（应用导航页显示未登录）" | info 门户是独立 CAS service，登录态过期 | 脚本已内置自动补登录；仍失败则删 `campus/runtime/sessions/info.json` 后重跑 |
| CDP 浏览器启动失败/端口冲突 | 多脚本并行抢同一 CDP 端口 | **串行执行**脚本，不要并行跑两个 CDP 脚本 |
| login 报 `connect_over_cdp: read ECONNRESET`（浏览器进程已死） | profile 内 GPU 缓存（GraphiteDawnCache 等）损坏，Chrome 启动即崩溃 | `browser.py --start` 已内置自愈：启动失败自动清理损坏缓存并重试一次；仍失败则 `browser.py --stop` 后手动清空 `campus/runtime/profiles/cdp_profile` 重试 |
| 登录触发验证码 | headless 下 CAS 风控 | 信任浏览器可免密；必要时走两阶段验证码 |
| 座位预约"无可用时间段" | 当天时段已过/非开放时段 | 改约其他区域或次日 6:00 后再约，不要传日期参数绕过；`book` 已内置 6:00-23:00 开放窗口校验，窗口外直接报 `book_out_of_window` |

## ⚠️ 强提示：单 Chromium 运行（执行任何脚本前必读）

本技能所有 CDP 脚本共用**同一个**无头 Chromium 实例（端口记录在 `campus/runtime/browser/cdp.port`）。**运行任何脚本前**：

> 🆕 **2026-09-16 起 base-cas 自带跨进程互斥锁**（`browser.py` 的 `acquire_run_lock()`，锁文件 `runtime/browser/campus.lock`）：
> 并行的两个脚本会**自动排队**（默认等 600s，`CAMPUS_BROWSER_LOCK_TIMEOUT` 可调；超时报 `error=browser_busy`），
> 不会再互踩成「CAS 用户名或密码不正确」；`learn.py → login.py` 这类**子进程通过环境变量继承锁**，不会自锁死。
> 下面的手工检查仍然值得做——排队意味着**长任务仍会互相等待**，能串行就别并行。

1. **检查**：`python campus/base-cas/scripts/browser.py --check` → 看 `cdp_running`。
2. **干净**（`cdp_running: false`）→ 可以启动脚本。
3. **不干净**（`cdp_running: true`）→ **禁止直接跑业务脚本**，先排查：
   - Windows：`Get-Process chrome` 或 `tasklist /FI "IMAGENAME eq chrome.exe"`，看 PID/启动时间
   - macOS/Linux：`ps aux | grep chrome`
   - 占用者是 **2FA 登录流程中的浏览器**（`login.py --ensure` 触发验证码后、`--submit-code` 完成前，属正常）→ 复用该浏览器，先完成登录再继续
   - 占用者是**孤儿/残留**（pid 与端口不匹配 / 非本技能启动）→ `browser.py --stop` 清理
   - **严禁**两个 CDP 脚本并行（必现端口冲突）；全部串行执行。

## 版本与发布信息（AI 须知）

- 本技能包**完全开源**。用户问"源码在哪 / 是否开源 / 如何获取" → 直接给 **GitHub 仓库** `https://github.com/TOMUIV/tsinghua-campus-skill`。
- 发布渠道：GitHub（源码）+ **ClawHub**（技能市场 slug `tsinghua-campus`，安装 `clawhub install tsinghua-campus`）。
- 用户反馈 bug/建议 → 引导到 GitHub Issue（或直接描述现象，AI 负责排查修复）。

## 面向用户的输出规范

- 不要说命令行/路径/技术术语（除非用户主动问）。
- "查看待办" → 自动走 learn；"我的课表" → 自动走 timetable。
- 每件事做完要汇总结果，主动问下一步。
- 用户问"这是什么技能包/能做什么/如何初始化" → 直接展示 `README.md` 内容。
