# travel-buddy：先想清楚「去哪儿」，再给你一份真能照着订的行程

<p align="center">
  <a href="README.md"><strong>English</strong></a>
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
  <img alt="Claude Code" src="https://img.shields.io/badge/Claude_Code-supported-5b5bd6">
  <img alt="Codex" src="https://img.shields.io/badge/Codex-supported-111827">
  <a href="https://clawhub.ai/dong845/skills/travel-buddy"><img alt="在 ClawHub 上" src="https://img.shields.io/badge/ClawHub-%40dong845%2Ftravel--buddy-7c3aed"></a>
  <a href="https://skillhub.cn/skills/user_f486c577/travel-buddy"><img alt="在 SkillHub 上" src="https://img.shields.io/badge/SkillHub-travel--buddy-ff6a00"></a>
</p>

<p align="center">
  <img src="docs/assets/hero.jpg" alt="五个候选目的地并排，其中四个因未通过硬性条件被划掉并置灰，一个被选中；一条箭头从它指向逐日行程页面，页面上的条目带着预订链接">
</p>

<p align="center"><sub>免费开源 · 全程在你自己的机器上跑 · 无账号、无云端</sub></p>

> **一个不肯编价格、不肯在没确认末班车之前说「可以订了」、也不肯在证明目的地根本到得了之前就给你排逐日行程的旅行助手。**

大多数 AI 行程工具，面对「我有 7 天、1500 欧」会直接给你一份信心十足的逐日行程 —— 而那座城市你从没选过。travel-buddy 把这当成两件事：先决定**去哪儿**（生成候选、做硬过滤、并说明淘汰了什么、为什么），只有目的地真正定下来之后才开始建行程，然后交付一个**自包含的 HTML 页面**：真实路线、真实预订链接、以及每一行都带来源和查询时间的人均预算。

它是给 [Claude Code](https://claude.ai/code) 和 [Codex](https://openai.com/codex) 用的 skill。你在终端里跟它说话，它用本机浏览器表单收集需求，实时查证易变事实，最后把结果存进你自己机器上的一个文件夹。除了查资料的请求本身没有任何数据离开你的电脑，生成的页面里也没有第三方脚本。

<p align="center">
  <a href="#从这里开始"><strong>从这里开始</strong></a> ·
  <a href="#你会拿到什么"><strong>你会拿到什么</strong></a> ·
  <a href="#它和别的不一样在哪"><strong>有什么不同</strong></a> ·
  <a href="#它会问你什么"><strong>它会问你什么</strong></a> ·
  <a href="#快速开始"><strong>快速开始</strong></a> ·
  <a href="#遇到问题"><strong>遇到问题</strong></a>
</p>

---

<a id="从这里开始"></a>

## 从这里开始

你不用挑模式。把你手上已经有的东西说出来，模式自己就定了：

| 你手上有 | 模式 | 你会拿到 |
| --- | --- | --- |
| 还没有目的地，或者只有一个大洲 | **Discovery（发现）** | 3–5 个排过序的候选，附取舍理由和淘汰记录 |
| 有国家/地区，但还没定城市 | **Constrained discovery（受限发现）** | 先比较子区域和城市，再谈行程 |
| 目的地已经定了 | **Construction（建行程）** | 完整逐日方案 + 两份产物 |
| 已有方案，但条件变了 | **Incremental replanning（增量重排）** | 只重算受影响的部分，并给出变更记录 |

[装好之后](#安装)，说话大概是这样：

```text
用 travel-buddy —— 五月有 7 天、预算 1500 欧左右，从阿姆斯特丹出发，我该去哪儿？
用 travel-buddy —— 秋天想去日本玩 8 天，先帮我把城市定下来。
用 travel-buddy —— 帮我们两个人排瑞士六日，湖区和老城，不要长距离步行。
用 travel-buddy —— 这是我存好的方案，日期往后挪了一周，哪些要改？
```

它只开一次本地表单，问那些真正决定行程的事，然后开始干活。Discovery 不会悄悄滑进 Construction：范围写死却没点名任何具体地点，会被**拦下**，不会靠猜。

---

<a id="你会拿到什么"></a>

## 你会拿到什么

都是普通文件，存在你自己的文件夹里 —— 前两份是 Construction 任务不交齐就不算完成的产物，第三份顺带生成：

| 产物 | 内容 |
| --- | --- |
| `plans/<日期>-<标题>.json` | 结构化的完整方案 —— 每个选项、价格口径、来源 URL 与假设 |
| `html/<日期>-<标题>.html` | 单文件自包含页面：分时行程、逐段地图、预订卡片、预算表、来源登记 |
| `plans/<日期>-<标题>.ics` | 同一趟行程的日历文件：已选或已订的交通、住宿、用餐和有时刻的安排，在任何日历 App 里都是正确的当地时间，带提醒进你手机 |

**页面上有什么。** 每天一条带真实时刻和步行分钟数的时间线；每一段都有能用的导航链接，且按当地真正可用的服务商路由；预订卡片打开的是**你自己去完成**的搜索页；人均预算的每一行都写明口径和查询日期；步行负荷、预算构成、每天行程分散度的内嵌图表；真实地点的自由许可照片，字节内嵌所以断网也能看；一块「落地第一小时」面板（能不能刷卡、怎么上网、出事找谁、保险怎么算）；以及一份来源登记：查了什么、什么时候查的、下单前还需要复核什么。

**页面上没有什么。** 任何没人核过、却不标注的东西。没有经过核验就保存的方案，会在页面最上方用你自己的语言印一条 **「未经事实核验」** 横幅。

**订好之后告诉它。** 页面会标出已订的选项、把备选折叠起来，并合计你已付的金额；核验过的计划依然算核验过。

---

## 它和别的不一样在哪

能给你写行程的工具很多。区别在于：行程里那些**说法**后来怎么样了。

- 🧭 **先定「去哪儿」，再谈「玩什么」** —— 候选、硬过滤，以及一份写下来的淘汰记录。过不了硬性条件的目的地，不会因为「有魅力」而胜出。
- 🔎 **它检查真正会毁掉行程的那件事** —— 末班接驳、那天正好闭馆的博物馆、以及压根就不通航的机场。
- 🧾 **没有来源和日期，就不写价格、营业时间和入境规则** —— 没查成的，页面会如实说明，而不是装得很有把握。
- 🔗 **只浏览，不替你交易** —— 每个链接打开的都是**你自己去完成**的搜索页。它不登录、不碰支付，也不会因为网页显示了什么就说「已订」。
- 🚦 **规则是闸门，不是良好愿望** —— 保存之前有四个程序先跑一遍；跳过事实核验的方案，会在自己首页上印一条横幅说明。
- 💻 **本地的，也是你的** —— 文件就在你自己的文件夹里，无账号、不同步云端、仅用标准库，页面里没有第三方脚本。

其中三条，来自真实运行：

**那趟根本不成立的行程。** 齐齐哈尔→深圳：当地机场通航表只有八个航点，深圳不在其中 —— 「只接受直飞」在任何行程存在之前就已经不成立。返程是从当天**末班接驳动车（21:35）倒推**选的；而漫步那天的博物馆，正好周一闭馆。

**那条差了 ¥2,761 的渠道。** 同样四个航班，国内站 ¥4,259，国际站 ¥7,020 —— 这个差价直接决定预算够不够。所以每个预订渠道都带着可达状态（`available` / `limited` / `unknown`），而不是假设「搜索结果看得见」就等于「你能买成」。

**那份通过了全部结构校验、却依然是错的方案。** 一次运行交付了：只写到签证、漏掉 EVUS 登记的入境结论（中国护照持有人会因此在值机柜台被拒登机）、把同一架飞机当成两个选项比价、把免费导览排在它根本不开的那一天、把晚餐排进 17:00 就打烊的店，以及在旅客明确要求「避免长距离步行」的前提下，把实际最重的一天标成「最轻」。**格式规整**和**内容属实**是两条不同的轴，所以后者由一轮独立的事实核验负责 —— 而跳过了它的方案，会在自己首页上说明这一点。

---

## 它会问你什么

有七件事真正决定这趟行程。在收齐它们、或者显式写出假设之前，它不会说任何目的地「很合适」：

1. **出发地** —— 城市、国家、可接受机场（绝不从城市推断机场：同一个都市圈里，有人优先廉价二级机场，有人只要直飞）
2. **时间窗** —— 有确切日期就用确切日期，否则月份 + 时长，外加灵活度与必须迁就的固定事项
3. **同行人** —— 人数、相关年龄、行动/健康需求，以及饮食或宗教限制
4. **预算** —— **人均**，含货币、目标价与硬上限、以及涵盖哪些类别
5. **目的地范围** —— `fixed` / `anchored` / `continent` / `open`
6. **出行目的** —— 它对「怎样才算好的一天」的影响，比大多数偏好字段都大
7. **体验方向** —— 自然 / 人文 / 平衡，再选 2–4 个具体子类并排出前两名

所有只有在定了目的地之后才有意义的细节（房间数、早餐、退改、舱位、行李、地图 App）都折叠在可选区块里，好让真正决定成败的问题保持可读。

**它凭现有信息肯走到哪一步。**

| 它知道 | 它会给 |
| --- | --- |
| 出发地、大致时间窗、粗预算、范围、大方向 | **探索性灵感清单**，并明确标注为探索性 |
| ……再加同行人与高影响过滤项（入境、旅行时长、天气、行动能力） | **排序推荐** |
| ……再加确切日期、入境状态、预算口径、住宿与行动能力全部确认 | **可预订方案** —— 且易变事实会在你下单前重新核实 |

只有过了硬门的候选才进入打分。推荐的起始权重：体验契合 25、全包性价比 20、季节契合 15、出发可达性与本地物流 15、舒适/人群/美食/语言/安全 15、灵活性与证据置信度 10 —— 并且只在你真正表达过的偏好之间分配。分数只是摘要，永远不是解释本身。

只有已经过了硬性过滤的候选才会进入打分，而分数只是摘要，永远不是解释本身。任何东西都不会因为网页上显示了就被称作**「已订」**—— 那个词只留给你亲口告诉它「我订好了」的交易。

---

## 快速开始

### 安装

需要 **Python 3.10+**（开发环境为 3.13）。**不需要 pip 装任何东西** —— 所有脚本只用标准库。四条路任选其一。

**方式一 —— 用 [`npx skills`](https://github.com/vercel-labs/skills) 一行装完**（最省事）：

```bash
npx skills add dong845/travel-buddy
```

它会询问 agent 与安装范围。加 `-g` 全局安装（对所有项目生效），加 `-a claude-code`（或 `-a codex`）跳过 agent 选择，加 `-y` 全程非交互，加 `-l` 只列出发现的 skill 而不安装。仓库根目录本身**就是**这个 skill，所以整个目录会被复制进你的 skills 文件夹。

**方式二 —— 作为 Claude Code 插件安装**（可管理更新，也是唯一能覆盖云端会话的方式）：

```text
/plugin marketplace add dong845/travel-buddy
/plugin install travel-buddy@travel-buddy
/reload-plugins
```

插件里的 skill 带命名空间，所以调用形式是 `/travel-buddy:travel-buddy`。两点要注意：如果你**同时**在 `~/.claude/skills/` 里还留着手动装的副本，这个 skill 会出现两次 —— 系统不做去重，请把手动那份删掉。另外第三方 marketplace **默认不自动更新**，要拿新版本得跑 `/plugin marketplace update travel-buddy`。

**方式三 —— 克隆 + 软链**（打算改代码就选这个：改完立即生效，插件缓存做不到这一点）：

```bash
git clone --depth 1 https://github.com/dong845/travel-buddy.git ~/code_project/travel-buddy
ln -s ~/code_project/travel-buddy ~/.claude/skills/travel-buddy
```

不需要放在别处的话，也可以直接克隆进 skills 目录：

```bash
git clone --depth 1 https://github.com/dong845/travel-buddy.git ~/.claude/skills/travel-buddy
```

**方式四 —— 从 [ClawHub](https://clawhub.ai/dong845/skills/travel-buddy) 安装**（[OpenClaw](https://clawhub.ai) 智能体的 skill 市场）：

```bash
openclaw skills install @dong845/travel-buddy
```

travel-buddy 同时上架了 **[SkillHub](https://skillhub.cn/skills/user_f486c577/travel-buddy)**（面向中文用户的 skills 社区），适合在那里浏览和横向比较；安装仍然走上面四条路之一。

然后初始化一次工作区：

```bash
cd ~/.claude/skills/travel-buddy
python scripts/travel_workspace.py init          # 创建 ~/Travel Buddy/{profiles,plans,html}
```

### 开始用

在 Claude Code 里敲 `/travel-buddy`，或者直接描述需求 —— 说一句「帮我找个三月份暖和的地方待一周」就够触发了。

第一次用，让它走引导表单：

```bash
python scripts/start_intake_workflow.py --assistant auto
```

它会打印一个 `http://127.0.0.1:<随机端口>/?token=…` 链接。打开、填写、保存 —— 同一个标签页会自动跳到本次行程表单。提交之后，它把存好的路径交回给**你正在对话的那个助手**，绝不会在你背后另起一个 agent（[为什么](docs/internals_CN.md#为什么-assistant-auto-永不自启第二个规划器)）。

无论哪种情况都**不需要下载、搬运、上传或粘贴 JSON，也不用打「继续」。**

```bash
# 先复核/修改已保存的稳定偏好，再进入本次行程表单
python scripts/start_intake_workflow.py --edit-profile

# 有多个档案时，传 ID（不是路径）
python scripts/start_intake_workflow.py --profile alice --assistant claude

# 完全关掉自动接续
python scripts/start_intake_workflow.py --assistant none

# 你的 CLI 没法把命令放到后台？让脚本自己去后台
python scripts/start_intake_workflow.py --detach
```

---

## 工作区与隐私

```
~/Travel Buddy/
├── profiles/   # 自愿保存的可复用旅行者档案
├── plans/      # intake、工作流事件、方案 JSON、发现任务日志
└── html/       # 最终的只读浏览型行程页
```

**会存的：** 国籍、居留国家与居留**身份类别**、语言、常住城市与可接受机场、常用货币、节奏、住宿档次、无障碍与饮食需求、去过的地方、心愿单、明确排除项。

**永远不存的：** 护照或证件号码与图像、签证有效期、支付或银行信息、账号密码、精确住址、本地身份证号、私人账号上下文。表单服务端还会**直接拒绝**包含这类字段的提交，而不是默默存下来。

只有你在表单里勾选同意，档案才会被创建。你最新一次的指令永远压过已保存的值。

**删除档案是刻意手动的** —— 没有 `forget` 子命令。先确认解析出的确切路径，再删那一个文件：

```bash
rm "~/Travel Buddy/profiles/<你点名的那个>.json"
```

绝不能为了删一个档案而清掉整个工作区。

---

## 遇到问题

**提交时报「不支持的本次旅行需求格式」。** 表单的工作模式必须和目的地状态一致（`fixed` → `construction`，`anchored` → `constrained_discovery`，其余 → `discovery`）。服务端是**故意**拒绝矛盾组合的，免得存下来的文件一边说目的地已定、一边说还需要帮你找目的地。

**自动接续没反应。** 在 `--assistant auto` 下这通常是**正确行为**而不是故障：只要本 skill 跑在**任何助手内部**，runner 都会主动让位，把保存好的意向文件路径打印出来，交给你正在对话的那个助手继续。它以前会在这种情况下另起一个无人看管的 agent，结果是同一个工作区里出现两份互相矛盾的方案。现在**从裸终端运行时它也不再启动** —— pty 证明不了「有人打开了这个终端」，而会分配 pty 的那些 harness 正因此拿到了子进程 —— 所以 `auto` 下它一律让位，并打印一行说明原因和覆盖方式。想强制后台运行用 `--assistant codex` 或 `--assistant claude`（或 `TRAVEL_BUDDY_ASSISTANT=codex`）；启动之后日志在 `plans/destination-discovery-*.log`，PID 和停止命令在 `plans/destination-discovery-*.pid.json`。如果 CLI 不在 `PATH` 里，runner 会明说。

**`--edit-profile` 好像没生效。** 它只在已经存在档案时起作用；`profiles/` 为空时，流程会直接去创建新档案。

**刚建的档案校验通过，但里面是空的。** `create-profile` 写的是一个已同意的**空壳**，`validate-profile` 在所有实质字段仍为 null 时也会判 VALID。用 `--edit-profile` 填完再依赖它。

**它拒绝保存，报「没有核验报告」。** 这是闸门在正常工作。按 [`references/verification.md`](references/verification.md) 跑完那一轮核验 —— 五个真实性域加两个不联网的审计员，走完整档位是七个块；如果这份计划够得上轻量档位，则是四个块（`sights_and_hours`、`transport` 与两个审计员）—— 保存报告，再用 `--verification <report.json>` 传进去。档位由 `check_plan_consistency.py` 读计划本身算出，不是谁声明的；交足七个块永远不会被拒，所以档位只会把下限往下调。如果你是有意保存草稿，用 `--unverified`：它会照常落盘，并在页面顶部盖一条「未经事实核验」横幅，免得有人把它当成可预订版本。

---

## 安全

表单由临时 HTTP 服务提供，**只绑定 `127.0.0.1`**、使用随机端口、只接受一次有效提交然后自行关闭。页面里没有第三方脚本、没有远程请求、没有登录、没有支付、没有上传。

回环绑定**不是**唯一的屏障。服务启动时会生成一次性 token 并写进终端打印的链接里，任何不带 token 的页面访问和提交都会被拒；跨站 POST 还会再被 `Origin` 校验拦一次，并且要求 `Content-Type: application/json`——这会触发预检，而本服务从不应答预检。此外有一把锁保证只接受一次提交，所以连点两下不会存两份、也不会拉起两个 agent。随机端口和对落盘内容的敏感字段扫描仍然在。

如实说明残余边界：**以你的身份**在**你的机器上**运行的任何进程，都能从终端或进程列表里读到那个 token。所以它防的是恶意网页，不是已经以你账号身份运行的本机恶意程序。

这个 skill 不会为了让被拦截的服务能用而建议 VPN、代理、账号变通或共享凭据，也不会代你完成预订、支付或账户变更。

**机票价格来自 Kiwi.com。** `scripts/kiwi_flights.py` 向 Kiwi.com 的公开航班搜索接口查询往返票价——不需要账号和密钥，任何机器都能用。它只发送航线、日期、人数和币种，从不发送你的姓名或证件信息。目前没有找到这个接口公开的使用条款；它是公开的、专为 AI 助手开放的，脚本会如实标明自己的身份，每次查机票只搜索一到两次。

---

## 内部是怎么工作的

流水线、每一道闸门、每一个脚本，以及催生每条规则的那个缺陷：**[docs/internals_CN.md](docs/internals_CN.md)**。用 travel-buddy 不需要读它。

---

## 开源协议

MIT，见 [LICENSE](LICENSE)。
