---
name: wechat-local-reader
version: 1.0.1
description: 微信本地管家：在桌面电脑（Windows/macOS/Linux）本地读取你本人本机登录的微信加密数据库，自动脱敏（手机号/身份证/银行卡/邮箱）并生成每日工作简报，推送至邮箱/企业微信机器人/任意 HTTP 端口。全程零上传，隐私不出本机。当用户想"让 AI 自动梳理微信里的消息和工作群""每天总结微信内容并推送""把微信聊天记录接入自动化并脱敏"时使用。注意：仅限本人本机微信数据；不支持手机/平板/鸿蒙等移动端。
license: 仅供个人本机数据导出使用，禁止用于读取他人账号。
allowed-tools:
disable: false
---

# 微信本地管家（wechat-local-reader）

把"你自己电脑上登录的微信"变成可查询的数据源：自动提取微信本地数据库的密钥、解密、提供命令行查询，再喂给 AI 生成每日工作简报或接入 WorkBuddy 定时自动化。

> 📣 **一句话简介**：本地读取你自己的微信，自动脱敏生成工作简报并推送到邮箱 / 企业微信 / 任意端口——全程零上传，隐私不出本机。

**上架介绍（适合在技能市场展示）**
- **能做什么**：在本机安全地读取你本人登录的微信（消息、群聊、联系人、公众号），用 AI 提炼成每日工作简报；内置 `--mask` 一键脱敏手机号 / 身份证 / 银行卡 / 邮箱；配合定时自动化跑通「提取 → 总结 → 脱敏 → 推送」，发到指定邮箱、企业微信机器人或任意 HTTP 端口。公众号按工作 / 政策 / 科技 / 财经 / 国内外大事分类精选，娱乐八卦自动丢弃；取关某号次日即不再读取。
- **为什么安全**：全程本地运行、零网络上传；密钥与缓存存于 skill 目录之外，发布分享不会带走聊天与密钥；密钥文件权限收紧为仅本人可读写，并提供 `clean` 一键清缓存。
- **合规底线**：仅供本人本机使用，严禁读取他人账号；Windows 4.1+ 密钥扫描算法借鉴自开源 `TANGandXUE/wcdb-key-tool`（MIT），已保留署名。

## 功能总览

本 skill 面向"每日工作简报 / 日报自动化"场景，把**你自己电脑上登录的微信**变成可查询、可总结、可安全外发的数据源。五大能力：

1. **信息提取** — 命令行读取微信本地加密库，输出最近会话、聊天记录、联系人、群成员、收藏、未读、增量新消息、聊天统计，支持按时间 / 关键词 / 消息类型过滤。所有数据默认 JSON 输出，专为 AI Agent 工具调用设计。
2. **AI 智能总结** — 工具只负责"把原始消息取出来"；把结果交给 WorkBuddy 自动化里的 AI，即可自动归纳重点、生成每日工作简报 / 晚报（如本 skill 配套的日报流水线）。
3. **敏感信息脱敏** — 内置 `--mask` 开关，自动掩码手机号 / 身份证号 / 银行卡号 / 电子邮箱（如 `138****5678`、`****0123`、`z***n@qq.com`），在导出或推送前消除明文隐私，避免把同事 / 客户的个人信息泄露到外部渠道。
4. **安全保密** — 全程本地解密、零网络上传；密钥与解密缓存均存于 skill 目录之外，发布 / 分享本 skill 不会带走你的聊天与密钥（详见下方「安全与合规声明」）。
5. **定时自动推送** — 配合 WorkBuddy 定时自动化，可在固定时间（如晨报 07:00 / 晚报 20:00）自动跑"提取 → 总结 → 脱敏 → 推送"，把简报发到**指定邮箱、企业微信机器人（webhook）或任意 HTTP 端点（端口）**。下方给出完整配置教程与 prompt 模板。

## 适用边界（务必先确认）

- ✅ **桌面端微信**：Windows（Weixin.exe）开箱即用；Linux 可用；macOS 因技能市场禁止上传二进制可执行文件，当前发布包未内置 macOS helper，macOS 用户需从源码仓库获取 `find_all_keys_macos.c` 自行编译后使用（详见下方「macOS 补充说明」）。

- ❌ **不支持移动端**：手机 / 平板 / 鸿蒙（HarmonyOS）/ Android / iOS 上的微信无法直接用本工具读取——移动端数据在 App 沙盒内，且没有可扫描的桌面进程、文件系统也不开放，本工具的密钥扫描与本地库读取逻辑均不适用于移动端。
- 📱 **鸿蒙平板的朋友怎么办**：在**一台 Windows/Mac/Linux 电脑**上安装微信电脑版并登录同一账号，用本工具读取与生成简报，再把结果推送到邮箱 / 企业微信机器人 / 任意可同步的渠道，平板只负责**查看**产出。自动化（WorkBuddy）本身也跑在桌面或云端，不依赖平板。

> 仅用于读取**你本人本机**的微信数据，做个人整理/日报。不要用于任何读取他人账号的场景。

## 安全与合规声明（上架前必读）

**法律红线**：本工具只允许读取**你本人、本机**登录的微信账号。严禁用于读取他人、公司共用机、或任何非本人账号的微信数据——这涉及侵犯他人隐私，使用者须自行承担全部法律责任。

**我们自己的信息 / 使用者信息会不会泄露？**
- ✅ **全程本地，零网络**：工具所有代码无任何 http / socket / 上传行为，聊天数据只在你电脑本地解密与查询，不会发往任何服务器。
- ✅ **密钥与缓存都在 skill 目录之外**：`init` 提取的密钥存于 `~/.wechat-cli/all_keys.json`，解密缓存存于系统临时目录（`$TMPDIR/wechat_cli_cache`），均**不在本 skill 安装目录内**，因此打包发布时不会被带出去。
- ⚠️ **但以下文件含敏感数据，严禁分享 / 提交 git / 云同步**：
  - `~/.wechat-cli/all_keys.json` —— 含各本地库的 `enc_key`，一旦泄露等于把你的微信聊天库"钥匙"交出去。
  - `~/.wechat-cli/`（含 `decrypted/`、`last_check.json` 等）与临时目录里的明文解密库 —— 是**明文**聊天记录副本。
  - 任何 `wechat-cli export` 导出的 `.md` / `.txt` 文件 —— 同样是明文聊天内容。
  - 处理建议：发布/分享本 skill 前确认上述路径未被纳入版本库；不再需要时手动删除 `~/.wechat-cli/` 与临时缓存目录。

**使用者环境加固（已做 + 待注意）**
- 解密缓存目录与文件已设 `0700 / 0600` 权限（macOS / Linux 生效；Windows 下依赖系统用户隔离）。
- 多用户共用电脑、或临时目录被云盘同步的场景下，仍建议用完即清理（删除 `~/.wechat-cli/` 与 `wechat_cli_cache`）。
- 移动端 / 鸿蒙（HarmonyOS）**不支持**本工具。
- macOS 当前发布包未内置 helper 二进制（技能市场禁止上传可执行文件）。如需在 macOS 使用，请从源码仓库获取 `find_all_keys_macos.c` 自行编译，或改用 Windows / Linux 环境。若已自行编译 helper，遇 `task_for_pid` 权限不足时可加 `--allow-resign` 对微信重新签名（仅添加调试权限、保留原有权限），非默认静默执行。

## 工作原理（一句话）

微信 4.x 的本地数据库（db_storage 下的 *.db）是 SQLCipher 加密的，每个库有独立 enc_key + salt。
init 命令扫描**正在运行的微信进程内存**提取这些密钥 → 保存为 all_keys.json → 之后所有查询都用密钥解密本地库，无需再登录或联网。

**支持的微信版本与提取方法（重要）：**
- **微信 4.1+（当前主流）**：主路径采用**只读**运行时 `com.Tencent.WCDB.Config.Cipher` 扫描 + HMAC 校验。微信 4.1 起不再在进程内存明文缓存密钥，老式"内存明文扫描"会直接失效，本工具已改用此只读扫描法，可正常提取。
- **微信 4.0.x 及更早**：回退到传统明文 raw key 内存扫描作为兼容。
- ⚠️ 提取需要对微信进程有足够权限（Windows 建议以管理员身份运行 `init`）。

> **第三方算法归属与许可证（发布合规必读）**：Windows 端微信 4.1+ 的只读 Config.Cipher 扫描算法**借鉴自开源项目 [TANGandXUE/wcdb-key-tool](https://github.com/TANGandXUE/wcdb-key-tool)（MIT License）**。本 skill 仅将其适配进自身公共扫描框架，未改动核心逻辑；发布/上架时**必须保留原作者署名与该 MIT 许可证说明**（见 `tool/wechat_cli/keys/scanner_windows.py` 文件头）。

## 安装

依赖：Python >= 3.10，以及 click / pycryptodome / zstandard（已写入 tool/requirements.txt）。

```bash
# macOS / Linux（WorkBuddy Bash 或系统终端）
bash tool/setup.sh

# Windows（WorkBuddy PowerShell 或系统 PowerShell）
.\tool\setup.ps1
```

安装后会在 tool/ 下生成 .venv/，其中包含启动器 `.venv/Scripts/wechat-cli`（Windows）或 `.venv/bin/wechat-cli`（macOS/Linux）。
把 `tool/.venv/Scripts`（或 `tool/.venv/bin`）加入 PATH，或在自动化里用绝对路径调用。

## 使用步骤

**1. 初始化 / 提取密钥**（微信电脑版必须处于登录且运行状态）

```bash
wechat-cli init
# 自动检测数据目录；如需指定：
wechat-cli init --db-dir "C:\Users\你\Documents\xwechat_files\<账号>\db_storage" --force
```

目录自动探测规则（通用，非硬编码；兼容 OneDrive 重定向的本地化"文档"目录）：
- Windows：先读微信本地 `config/*.ini`；若该文件为"我的文档"占位符（`MyDocument:`），或 ini 指向的路径不存在，则回退到系统"文档"目录（含 `OneDrive/<本地化文档>/xwechat_files/*/db_storage`）搜索。也可直接用 `--db-dir` 指定。
- macOS：~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/*/db_storage
- Linux：~/Documents/xwechat_files/*/db_storage

**2. 验证能读到数据**

```bash
wechat-cli sessions                 # 最近会话列表
wechat-cli history "群名或联系人" --limit 20
wechat-cli search "关键词" --limit 50
# 任意查询加 --mask 可自动脱敏手机号/身份证/银行卡/邮箱（推送前推荐加上）
wechat-cli history "群名" --limit 20 --mask
```

**3. 取增量（日报主步骤）**

```bash
wechat-cli new-messages                 # 自上次调用以来的新消息
wechat-cli new-messages --mask --clean  # 脱敏 + 输出后清空明文缓存（自动化推荐，避免隐私残留）
```

**4. 清理明文缓存（隐私保护）**

解密后的明文数据库缓存在系统临时目录（`$TMPDIR/wechat_cli_cache`），共享/公用电脑上用完建议清理，或直接在自动化里加 `--clean`：

```bash
wechat-cli clean                         # 删除解密缓存（明文数据库），不影响微信原始加密库
```

> 说明：缓存目录与文件已做 `0700 / 0600` 权限收紧（Linux/macOS 生效；Windows 依赖系统用户隔离）；`clean` 仅删除本工具生成的明文副本，绝不触碰微信原始数据。

其他命令：contacts --query "李"、members "群名"、export、stats、unread、favorites。详见 tool/README_CN.md。

## 接入 WorkBuddy 定时自动化（提取 → 总结 → 脱敏 → 推送）

完整流水线：**① wechat-cli 提取微信消息 → ② AI 总结归纳 → ③ 脱敏（--mask / prompt 级）→ ④ 定时推送到邮箱 / 企业微信机器人 / 自定义端口**。

### 步骤 1：新建定时自动化
在 WorkBuddy 新建"定时自动化"，设置触发时间（如 `07:00` 晨报、`20:00` 晚报；可用 RRULE 配置"每天"）。

### 步骤 2：prompt 模板（直接复制，按业务改关键词）
```
你是我的微信日报助理。请按以下流程生成今日工作简报（**为节省 AI 额度，禁止全量读取微信，只精准拉取相关内容**）：

1) 调用微信本地读取工具（需先 wechat-cli init 过）：
   export PATH="$PATH:<本 skill 的 tool 目录绝对路径>"

   # —— 精准拉取：按"政策/工作类"关键词搜 + 指定关键群/公众号 history ——
   # 不要用 new-messages 全量（订阅号/娱乐号会灌满额度，浪费积分）
   wechat-cli search --keyword "国网"   --limit 50 --mask
   wechat-cli search --keyword "电力"   --limit 50 --mask
   wechat-cli search --keyword "政策"   --limit 50 --mask
   wechat-cli history "关键群名"        --limit 50 --mask   # 你的工作群（按需改）
   wechat-cli history "国网江苏电力"    --limit 20 --mask   # 政策类公众号白名单（按需增删）

2) 内容取舍规则（重要，违反即浪费额度）：
   - 保留：国网/电力/能源/发改/营商/政务/政策/政府/工信/供电/通州/南通/江苏
           等工作、国家政府、政策类消息与公众号推送；以及政策新闻、科技前沿、财经宏观、
           国内外大事类公众号推送（如新华社/人民日报/央视新闻/部委发布号、科技媒体、财经媒体、
           国际时事号等），作为"资讯参考"单列，不与工作部署混同。
   - 丢弃：娱乐、吃瓜、八卦、养生、健康、购物、团购、影视、搞笑等无关公众号与消息，
           一律不纳入日报，也不要喂给总结步骤（省积分）。

3) 结构化输出日报：分"工作动态 / 待办 / 风险预警 / 明日安排"四块。
   涉及个人信息（手机号、身份证、银行卡、邮箱）一律用 *** 代替，不得出现明文。
   - 【说话人方向不可反置】总结对话/发言/工作指示/部署时，严格保留原始"谁对谁说"的方向：说话主体必须是微信消息的发送人，听话/被指向方是接收方。A 对 B 说的话只能写成"A 对 B 说/要求/布置…"，不得反置为"B 对 A 说"。方向无法从原文判断的标注"（方向待确认）"，不臆测。

4) 推送：把日报通过下方"推送配置"里选定的渠道发出。

---

#### 省积分：公众号只取政策/工作类（重要）

微信订阅号/公众号极多（本机实测订阅号聚合入口 `unread` 高达数千条），**全量读取会严重浪费 AI 积分**。
因此日报默认采用"**精准拉取**"模式，而非 `new-messages` 全量：

- **怎么做**：用 `wechat-cli search --keyword "<政策类关键词>"` 按关键词拉取命中消息；
  对明确有价值的政策/政府类公众号，用 `wechat-cli history "<公众号名>"` 逐个拉取（白名单制）。
- **保留（白名单关键词）**：工作类——国网、电力、能源、发改、营商、政务、政策、政府、工信、
  供电、通州、南通、江苏、应急、安全、环保、税务、人社；资讯类——政策、时政、新华社、人民
  日报、央视新闻、国务院、部委、新规、改革、科技、人工智能、AI、半导体、芯片、新能源技术、
  航天、量子、机器人、财经、经济、宏观、央行、美联储、A股、股市、基金、汇率、GDP、国际、
  全球、外交、中美、俄乌、中东、联合国、地缘、贸易战……（按你的业务持续增删）。
- **排除（黑名单关键词）**：娱乐、吃瓜、八卦、养生、健康、购物、团购、影视、搞笑、情感……
  这些公众号推送**不拉取、不总结**。
- **维护白名单**：把你关注的"政策/政府/工作类"公众号名（如 `国网江苏电力`、`工信微报`、`江苏发改`）
  直接写进自动化 prompt 的 `history` 列表即可，新增一个号就加一行，零代码。
  资讯类（政策新闻/科技/财经/国内外大事）一般无需逐个列名——靠关键词命中即可自动捕获；
  若某号长期无价值，直接取关，本地库不再有该号新推送，次日即不再出现（见下方"取消关注"说明）。
- **为什么不用 new-messages 全量**：`new-messages` 会返回所有会话的新消息（含数千条订阅号），
  若全喂给 AI 总结，积分消耗巨大且产出大量无关内容。关键词搜 + 白名单 history 把读取量压到最小。
- **取消关注某公众号，会自动停止读取吗？** 会。本工具按"内容关键词 + 白名单"筛选，并**不**维护
  一份写死的公众号名单；你取关后，微信不再向本机推送该号新文章，本地库 `biz_message_*` 里便不再
  新增该号消息，日报的"政策资讯与宏观要闻"板块次日自然不再出现它的新内容（已下载但未过 24h 窗口的
  极少数存量可能当天再出现一次，随后即消失）。无需手动改任何配置。
```

### 步骤 3：脱敏（两层保障）
- **工具层**：命令加 `--mask`，自动掩码手机号 / 身份证 / 银行卡 / 邮箱（示例：`138****5678`、`****0123`、`z***n@qq.com`）。适用于 `history` / `search` / `new_messages` / `export`。
- **AI 层**：在 prompt 里要求"涉及个人信息一律用 *** 代替"，兜底金额、姓名、住址等工具未自动覆盖的敏感项。

### 步骤 4：推送配置（邮箱 / 企业微信机器人 / 自定义端口）

#### A. 推送到邮箱
- **方式一（推荐，零代码）**：自动化配置里直接使用 WorkBuddy 的"邮件"渠道（已连接邮箱即可），让 AI 把日报作为邮件正文 / 附件发出。
- **方式二（脚本）**：让 AI 执行如下 Python（需自备 SMTP 账号与授权码）：

  ```python
  import smtplib
  from email.mime.text import MIMEText
  msg = MIMEText(content, "markdown", "utf-8")
  msg["Subject"], msg["From"], msg["To"] = "微信日报", "你@qq.com", "接收人@xx.com"
  with smtplib.SMTP_SSL("smtp.qq.com", 465) as s:
      s.login("你@qq.com", "授权码"); s.send_message(msg)
  ```

#### B. 推送到企业微信机器人（群 webhook）
1. 在企业微信里"添加群机器人"，复制 Webhook 地址：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY`
2. 让 AI 执行（把日报以 markdown 推送到该地址）：

   ```bash
   curl -sS "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY" \
     -H 'Content-Type: application/json' \
     -d "{\"msgtype\":\"markdown\",\"markdown\":{\"content\":$(python -c "import json,sys;print(json.dumps(open('日报.md').read()))")}}"
   ```
   > 企业微信机器人单条 markdown 限 4096 字节，超长请分段或改发文件。

#### C. 推送到自定义端口 / 通用 HTTP 端点
任意支持 `POST JSON` 的服务（自建服务、飞书 / 钉钉机器人、IoT 端口等）都可用同样方式推送：

```bash
curl -sS "http://你的服务器:端口/api/wechat-daily" \
  -H 'Content-Type: application/json' \
  -d "{\"date\":\"$(date +%F)\",\"brief\":\"$(echo "$CONTENT" | head -c 2000)\"}"
```

> 提示：微信大版本升级（尤其 4.x 架构变动）后密钥可能失效，重新跑一次 `wechat-cli init --force` 即可。

## 文件结构

```
wechat-local-reader/
├── SKILL.md
└── tool/
    ├── setup.sh / setup.ps1     # 一键安装（建 venv + 装依赖 + 注册命令）
    ├── pyproject.toml           # 包定义，含 wechat-cli 入口
    ├── requirements.txt
    ├── entry.py                 # PyInstaller 入口（可选）
    ├── README_CN.md             # 工具完整文档
    └── wechat_cli/              # 已脱敏的源码（无个人账号/路径/密钥）
        ├── main.py              # CLI 入口（click 命令组）
        ├── commands/            # init/sessions/history/search/new_messages/...
        ├── core/                # config/crypto/messages/contacts/db_cache/mask(脱敏)
        └── keys/                # 跨平台密钥扫描：scanner_windows/macos/linux
        ├── main.py              # CLI 入口（click 命令组）
        ├── commands/            # init/sessions/history/search/new_messages/...
        ├── core/                # config/crypto/messages/contacts/db_cache/mask(脱敏)
        └── keys/                # 跨平台密钥扫描：scanner_windows/macos/linux
```

## 排错

- Weixin.exe 未运行 / 找不到进程：确认微信电脑版已登录且前台运行，再 init。
- 自动检测不到目录：用 init --db-dir 手动指定 db_storage 路径。
- macOS 提示"找不到 macOS 密钥提取二进制"：当前发布包未内置 macOS helper，请从源码仓库获取 `find_all_keys_macos.c` 自行编译，或改用 Windows / Linux 环境运行。
- macOS 报 `task_for_pid`：密钥扫描可能需要 sudo；若已自行编译 helper，可按提示加 `--allow-resign`。
- 解密失败 / 读不到消息：多半是微信升级导致密钥变化，执行 wechat-cli init --force 重新提取。
