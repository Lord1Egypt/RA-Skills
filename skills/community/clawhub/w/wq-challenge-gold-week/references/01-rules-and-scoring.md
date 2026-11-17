# 第①章 WorldQuant Challenge 参赛与规则

> 本文是《用 AI 辅助冲刺 WorldQuant BRAIN Challenge》的一章,完整章节地图见上层 SKILL.md。

**本章目录**

- 1.1 这个 skill 是什么、给谁、能达成什么
- 1.2 WorldQuant BRAIN 是什么、如何免费注册、如何拿 API 凭证
- 1.3 Challenge 竞赛机制
- 1.4 核心计分心智模型：每天精提 1–2 个最优，绝不掺弱，天天不断
- 1.5 诚实澄清：Challenge 无现金奖 —— 那它到底给你什么？
- 1.6 开工前你需要准备什么（清单）

---

## ① WorldQuant Challenge 参赛与规则

### 1.1 这个 skill 是什么、给谁、能达成什么

| 维度 | 说明 |
|---|---|
| **是什么** | 一套"AI 辅助的每日 alpha 生产线"：发现因子 → 回测（simulate）→ 筛选 → 提交（submit）→ 累积竞赛分。 |
| **给谁** | 能看懂代码、会（或愿意让 AI 帮你）发 HTTP 请求的量化小白。不需要你懂高深数学，需要你懂"照着流程跑、看懂指标"。 |
| **能达成** | 学会独立完成"每天精提 1–2 个通过硬门槛的 alpha"，并把这个动作坚持到 GOLD。 |
| **达不成** | 不保证任何现金收益；不替你思考市场；不给你一份"抄了就赢"的因子表。 |

后续章节会带你走完：注册 → 拿凭证 → 用 API 探测可用字段/算子 → 用模板批量生成候选 → 按指标筛选 → 每日提交 → 监控竞赛进度。本章先把**规则和心智模型**打牢——**规则理解错，后面全是无用功。**

### 1.2 WorldQuant BRAIN 是什么、如何免费注册、如何拿 API 凭证

**WorldQuant BRAIN** 是 WorldQuant（一家量化对冲基金）开放的**在线量化研究平台**：你在上面用它提供的**数据字段（data-fields）**和**算子（operators）**，拼出一个"预测信号"表达式（就是一个 alpha），平台在历史数据上帮你回测，给出 Sharpe、Fitness、turnover 等指标。它对个人**免费开放**。

**注册（免费）：**
1. 访问 BRAIN 官网（platform.worldquantbrain.com），用邮箱注册一个账号。
2. 完成注册问卷 / 简单的入门确认（平台会引导）。
3. 登录网页端，先在可视化 IDE 里手动跑一两个 simulation，确认账号可用。

**拿 API 凭证：**
BRAIN 的 API **不需要单独申请 API Key**，它直接用你**注册时的邮箱 + 密码**做 **HTTP Basic 认证**，向 `POST /authentication` 换取一个会话（session / cookie），后续请求带着它即可。

- **API Base**：`https://api.worldquantbrain.com`
- **认证方式**：HTTP Basic（账号=邮箱，密码=登录密码）打到 `/authentication`，拿到会话后复用。

> ⚠️ **凭证安全铁律**：**永远不要把邮箱/密码硬编码进代码或提交进 Git**。放进环境变量或本地 `credentials.json`（加进 `.gitignore`）。下面示例演示"从外部读取、不落盘明文进代码"的正确姿势。

```python
# auth_example.py —— 通用认证示例（凭证从环境变量读取，绝不硬编码）
import os, requests

BASE = "https://api.worldquantbrain.com"

def make_session():
    s = requests.Session()
    # 账号/密码来自环境变量或本地被 gitignore 的配置，切勿写死在代码里
    user = os.environ["BRAIN_EMAIL"]
    pwd  = os.environ["BRAIN_PASSWORD"]
    s.auth = (user, pwd)                       # HTTP Basic
    r = s.post(f"{BASE}/authentication")       # 换取会话
    r.raise_for_status()
    return s                                   # 之后所有请求复用这个 session

# 用法：探测你当前 tier 能用的字段与算子（务必实测，别猜！）
sess = make_session()
fields = sess.get(f"{BASE}/data-fields", params={"limit": 50}).json()
ops    = sess.get(f"{BASE}/operators").json()
```

**你会用到的核心 API 端点（后续章节展开）：**

| 端点 | 作用 |
|---|---|
| `POST /authentication` | HTTP Basic 登录，换会话 |
| `GET /data-fields` | 列出**你当前 tier 能用的**数据字段 |
| `GET /operators` | 列出**你当前 tier 能用的**算子 |
| `POST /simulations` | 提交回测；轮询 `status` 直到 `COMPLETE` |
| `GET /alphas/{id}` | 取某个 alpha 的指标（Sharpe/Fitness/turnover…） |
| `POST /alphas/{id}/submit` | **正式提交**该 alpha 进竞赛 |
| `GET /competitions/challenge` | 看 leaderboard：`score` / `level` / `rank` + 你的 `progress` |

> 🔑 **重要提醒**：算子和地区是**按 tier（等级）逐步解锁**的。低等级账号通常有些向量统计算子（如 `vec_stddev`）和非 USA 地区被锁。**永远用 `/operators` 和 `/data-fields` 实测你现在有什么，不要凭记忆或别处的清单去猜。** 同时低等级账号的**并发回测**一般硬性限制在 **K=2**（账号级上限），批量跑 simulation 时要排队。

### 1.3 Challenge 竞赛机制

> 📌 **出处说明**：本节机制细节（日封顶 ~2000、3AM EDT 刷新、当日质量取平均、跨用户归一化、自相关 ≥0.75 被挡等）综合自平台官方 FAQ 与作者参赛期间的实测观察，属经验总结；平台规则可能随时调整，**一切以 BRAIN 官方最新说明为准**。

Challenge 是一个**按天累积的信誉竞赛**，核心规则如下：

**① 等级门槛（累积分达到即解锁）**

| 等级 | 累积分门槛 |
|---|---|
| BRONZE | > 1,000 |
| SILVER | > 5,000 |
| **GOLD** | **> 10,000** |

**② 计分规则（四个必须记牢的机制）**

- **按天累积、不减**：每天你提交的 alpha 会产生"当天分"，加进总分；总分只涨不掉。
- **每天封顶约 2000 分**：当天再怎么猛，也就贡献 ~2000 上限。这是 GOLD ≈ 5 天的数学来源（10000 ÷ ~2000）。
- **每天 3AM EDT 刷新**：新的一天从**美东时间凌晨 3 点**开始。规划你的"每日提交"要按这个时区，别用本地零点。
- **跨用户归一化（cross-user normalized）**：你当天的得分不是绝对值，而是**和当天所有参赛者相比的相对位置**。所以"绝对指标不错"不够，要**相对别人更好**。

**③ 当天质量分 = 你当天所有提交 alpha 指标的"平均值"**（不是总和！）

平台综合当天这批 alpha 的质量算出一个"平均品质"。经验上，单个 alpha 品质更高的方向是：
- **universe 更小** → 更高（如小盘/子集比全市场更值钱）
- **对你已 ACTIVE 集合的自相关越低越好**（越正交越加分）
- **Fitness 越高越好**
- **in-sample 的 D1（第一天样本内表现）好**

> 这条"取平均"的规则，直接决定了下一节的心智模型——**它是整个 skill 里最重要的一句话。**

**④ 平台提交硬门槛（不达标直接被挡，连提交都不行）**

| 门槛 | 要求 |
|---|---|
| Sharpe | **≥ 1.25** |
| Fitness | **≥ 1.0** |
| 自相关（对你已 ACTIVE 的 alpha 集合） | **< 0.7**（达到 **≥ 0.75 会被挡下**） |

其中 Fitness 的定义值得刻进脑子：

```
Fitness = Sharpe × sqrt( |returns| / max(turnover, 0.125) )
```

`turnover`（换手率）在**分母**上——所以**降低换手能直接抬 Fitness**。实操里用**长时间窗口**（如 `ts_` 类算子取 126 / 252 / 504 天）来平滑信号、压低 turnover，是过 Fitness 门槛的常规手段。

### 1.4 核心计分心智模型：每天精提 1–2 个最优，绝不掺弱，天天不断

因为**当天质量分是"平均"**，所以整个策略可以浓缩成四句话：

> **① 每天只提你手上最好的 1–2 个 alpha。**
> **② 绝不为了"多提"而掺进弱的**——一个平庸 alpha 会把当天平均拉下来，**净伤害**。宁可只提 1 个精品。
> **③ 每天都提（连续性 > 数量）**——分数按天累积，**断更一天 = 白白丢一天 ~2000 的额度**。GOLD 的本质是"连续 5 天不掉链子"，不是"某天爆产 20 个"。
> **④ 提交前先过硬门槛 + 查自相关**：Sharpe≥1.25、Fitness≥1.0、对已 ACTIVE 集合自相关<0.7。撞车的（自相关高）要么中性化/换分母重构，要么直接放弃。

**反直觉但正确的推论：**"数量思维"在这里是陷阱。传统直觉是"多提多得"，但取平均 + 封顶 + 归一化的规则下，**多提弱 alpha 会主动降分**。正确姿势是**质量优先、少而精、天天到岗**。把每天当成一次"只交最优答卷"的考试。

**一个健康的每日循环（后续章节详细展开）：**

```
每天（按 3AM EDT）：
  1. 用模板批量生成候选表达式（如 group_rank(ts_rank(SIGNAL, 长窗口), 分组)）
  2. POST /simulations 批量回测（注意 K=2 并发，排队跑）
  3. 按 Sharpe / Fitness / turnover / universe 筛出 top 候选
  4. 对候选查自相关，剔除撞车的（≥0.75 必挡，<0.7 才安全）
  5. 只 submit 最优的 1–2 个
  6. GET /competitions/challenge 看 score / level 涨了多少
  7. 明天再来（不断更）
```

### 1.5 诚实澄清：Challenge 无现金奖 —— 那它到底给你什么？

**必须说清，别被误导：**

- **Challenge 的产出是"信誉 + track record"**，不是钱。爬到 GOLD 意味着：你在平台上有**可验证的、持续产出合规 alpha 的记录**。这条记录本身是资产——它是你申请更高权限、参与更深度合作、或被平台关注的**敲门砖**。
- **GOLD ≠ 自动拿钱**。它是等级/排行榜/履历，不触发任何现金支付。
- **真正发钱的是另一套项目：Research Consultant（研究顾问）**。那是**选择性（selective）**的：由平台按表现邀请/筛选，有独立的机制和合约，**和 Challenge 的计分不是一回事**。Challenge 里的好成绩可能**有助于**被看见，但不是"到 GOLD 就自动转正拿薪"。

一句话：**把 Challenge 当"练本事 + 攒履历"，把现金预期放到 Research Consultant 那条独立赛道上——两者别混为一谈。**

### 1.6 开工前你需要准备什么（清单）

| # | 准备项 | 说明 |
|---|---|---|
| 1 | **一个 BRAIN 账号** | 邮箱免费注册，能登录网页端并手动跑通一个 simulation。 |
| 2 | **凭证的安全存放** | 邮箱 + 密码放环境变量 / 被 gitignore 的本地配置，**绝不硬编码、绝不进 Git**。 |
| 3 | **一个能调 HTTP / 写代码的 AI 助手** | 如 Claude Code。它替你写认证、批量 simulate、筛选、submit 的脚本。 |
| 4 | **基础的"看懂代码 + 看懂指标"能力** | 不需要精通数学，但要能看懂 Python `requests`、能读 Sharpe / Fitness / turnover / 自相关 是高是低。 |
| 5 | **时区意识** | 按 **3AM EDT** 规划每日提交窗口，别用本地零点。 |
| 6 | **心理预期校准** | 接受"约 5 天连续节奏 + 每天精提 1–2 个"，不追求 1 天速成，不期待现金奖。 |
| 7 | **（建议）一个每日提醒 / 轻量调度** | 保证"天天不断更"——断一天就丢一天额度。 |

准备齐这 7 项，就可以进入下一章：**用 API 探测你当前 tier 能用的字段与算子，并开始批量生成候选 alpha。**


---

