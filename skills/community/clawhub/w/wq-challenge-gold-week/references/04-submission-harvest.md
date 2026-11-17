# 第④章 提交规则与快速拿分

> 本文是《用 AI 辅助冲刺 WorldQuant BRAIN Challenge》的一章,完整章节地图见上层 SKILL.md。

**本章目录**

- 4.1 提交流程:从 alpha 到 ACTIVE
- 4.2 三道硬门槛 + 可过性预测器
- 4.3 ★每日收割策略:提最优 1-2 个,绝不掺弱
- 4.4 为什么快不了:~2000/天 的天花板
- 4.5 每日提交决策清单 / 伪代码

---

## ④ 提交规则与快速拿分

> 因子造出来只是半成品,**提交(submit)并变成 ACTIVE** 才真正进账。这一章讲清楚:怎么提、什么会被挡、每天该提哪几个、以及为什么"快"也快不过 5 天。

### 4.1 提交流程:从 alpha 到 ACTIVE

提交是异步的:发一个 POST,然后**轮询 status** 直到平台判完所有 checks。

```
POST /alphas/{id}/submit        # 发起提交
GET  /alphas/{id}               # 轮询,读 status 和 checks
```

status 的生命周期大致是:

| status | 含义 | 你要做的 |
|---|---|---|
| `UNSUBMITTED` | 还没提 | 发 POST /submit |
| `PENDING` / `CHECKING` | 平台正在跑门槛校验 | 每 5-10s 轮询一次 |
| `ACTIVE` | **通过,进账** | 收工,记到 ACTIVE 集合 |
| `FAILED` / `REJECTED` | 被挡 | 读 `checks[]` 看哪一项 FAIL |

失败时不要瞎猜,**直接读 checks 数组**。每一项形如 `{name, result, value, limit}`,常见的失败名:

- `LOW_SHARPE` —— Sharpe < 1.25
- `LOW_FITNESS` —— Fitness < 1.0
- `SELF_CORRELATION` / `HIGH_CORRELATION` —— 对你已 ACTIVE 集合自相关 ≥ 0.7(通常 ≥0.75 直接挡)
- 还可能有 turnover / concentration / units 等次要检查

伪代码:

```python
def submit_and_wait(alpha_id):
    api.post(f"/alphas/{alpha_id}/submit")
    while True:
        a = api.get(f"/alphas/{alpha_id}")
        if a["status"] == "ACTIVE":
            return "PASS", None
        if a["status"] in ("FAILED", "REJECTED"):
            fails = [c["name"] for c in a["checks"] if c["result"] == "FAIL"]
            return "FAIL", fails          # 例如 ["SELF_CORRELATION"]
        sleep(8)                          # 别打太快,尊重限流
```

### 4.2 三道硬门槛 + 可过性预测器

平台级(account-level)硬门槛,**任何一条不过就无法 ACTIVE**:

| 门槛 | 阈值 | 怎么救 |
|---|---|---|
| **Sharpe** | ≥ 1.25 | 换更干净的信号/加中性化(industry/subindustry)剔行业 beta |
| **Fitness** | ≥ 1.0 | Fitness=Sharpe×√(\|returns\|/max(turnover,0.125));**turnover 在分母** → 用长窗(126/252/504)降换手,Fitness 立涨 |
| **自相关** | < 0.7(对已 ACTIVE 集合) | 换角色/换分母/换分组做正交,拉低与老 alpha 的重叠 |

前两条在**回测(simulation)阶段**就能看到,提交前先自查、别浪费提交名额。第三条只有平台知道你完整的 ACTIVE 集合,但你可以自己算出**可过性预测器**。

**可过性预测器(提交前本地估算):**

- 把候选 alpha 的每日 PnL 序列,与你**每一个已 ACTIVE** alpha 的 PnL 序列算 Pearson 相关。
- 取**最大**的那个 |corr| 作为风险指标:
  - `max_corr < 0.7` → **几乎必过**(放心提)
  - `0.7 ≤ max_corr < 0.75` → 灰区(能不提就先留着改)
  - `max_corr ≥ 0.75` → **基本会被挡**(别提,回去做正交)

```python
def passability(cand_pnl, active_pnls):
    m = max(abs(pearson(cand_pnl, p)) for p in active_pnls) if active_pnls else 0
    if m < 0.70:  return "SAFE"      # 几乎必过
    if m < 0.75:  return "GREY"      # 灰区,谨慎
    return "BLOCKED"                 # 会被自相关挡
```

> 拿不到别人的 PnL,但你能拿到**自己所有 ACTIVE 的 PnL**——这就够做预测器了。ACTIVE 越多,新因子越要主动走"另类通道"(如期权 IV、分析师一致预期)来压低 max_corr。

### 4.3 ★每日收割策略:提最优 1-2 个,绝不掺弱

这是全章最重要的一条。**当天的质量分是"当天所有提交的平均值",不是总和。**所以:

- **只提最好的 1-2 个**,多提弱的会**拉低当天平均**,得不偿失。
- 挑选优先级(高 → 低):**小 universe** > **高 Fitness** > **低自相关** > in-sample D1 表现好。
  - 小 universe(如 TOP200/TOP500 而非全市场)通常归一化后单位分更高。
- **天天都要提**(连续性 > 数量):分数按天累积、不回撤,但**断一天就永久少一天的分**,后面补不回来。

一句话口诀:**宁缺毋滥,每天精提两个;质量看平均,连续看天数。**

### 4.4 为什么快不了:~2000/天 的天花板

分数机制:**按天累积、不减、每天封顶约 2000、3AM EDT 刷新、跨用户归一化。**

所以到 GOLD(10000)在数学上就是"**约 5 天、每天吃满上限**"。没有 1 天速通——"速通"指的是**每天走最高效路径**(每天稳定精提 2 个满分级因子),不是一夜到顶。

一条从 BRONZE 到 GOLD 的**示意轨迹**(理想满配,真实会有波动):

| 天 | 当天进账(封顶~2000) | 累计 score | 等级里程碑 |
|---|---|---|---|
| Day 1 | ~2000 | ~2000 | 刚过 **BRONZE**(>1000) |
| Day 2 | ~2000 | ~4000 | 逼近 SILVER |
| Day 3 | ~2000 | ~6000 | 过 **SILVER**(>5000) |
| Day 4 | ~2000 | ~8000 | 冲刺 |
| Day 5 | ~2000 | ~10000 | 到 **GOLD**(>10000) |

现实里某天质量不够、或自相关被挡,会少进账 → 顺延到第 6、7 天。**关键不是某天爆发,是别断更。**

> **诚实提醒:**
> 1. GOLD 是**排行榜/等级/信誉**,Challenge **本身没有现金**。真发钱的是另一套**选择性**的 Research Consultant 项目,GOLD ≠ 自动拿钱。
> 2. 每天封顶决定了这是**耐力赛**。断一天 = 少一天分、且 GOLD 到手日整体后延一天,没有补偿机制。

### 4.5 每日提交决策清单 / 伪代码

把下面这套当成**每天(3AM EDT 刷新后)跑一次**的例行程序:

```python
# ===== 每日提交决策 =====
def daily_harvest():
    # 1) 拉取当前 ACTIVE 集合(算自相关的基准 + 拿它们的 PnL)
    active = api.get("/users/self/alphas?status=ACTIVE")
    active_pnls = [get_pnl(a["id"]) for a in active]

    # 2) 从今天的候选池里过硬门槛 + 算可过性
    scored = []
    for c in today_candidates:                 # 已 COMPLETE 的回测结果
        if c["sharpe"] < 1.25:  continue        # 门槛1
        if c["fitness"] < 1.0:  continue        # 门槛2
        tag = passability(get_pnl(c["id"]), active_pnls)
        if tag == "BLOCKED":    continue        # 门槛3 预测:会被挡,跳过
        scored.append(c)

    # 3) 排序:小 universe 优先,再 Fitness 高,再自相关低
    scored.sort(key=lambda c: (
        universe_size(c["universe"]),           # 越小越靠前
        -c["fitness"],                          # 越高越靠前
        c["max_corr_to_active"],                # 越低越靠前
    ))

    # 4) 只提最优 2 个(绝不掺弱,保护当天平均分)
    for c in scored[:2]:
        result, fails = submit_and_wait(c["id"])
        log(c["id"], result, fails)

    # 5) 刷新后核对:score 到底涨没涨
    #    注意 3AM EDT 结算,当天提交的分次日才完全反映
    board = api.get("/competitions/challenge")
    log("score=", board["leaderboard"]["score"],
        "level=", board["leaderboard"]["level"],
        "rank=",  board["leaderboard"]["rank"])
```

**收尾核对(必做):** 次日刷新后再拉一次 `GET /competitions/challenge`,确认 `leaderboard.score` **确实上涨**。没涨 → 回查:是被自相关挡了(status 没到 ACTIVE)?还是当天平均被弱因子拖低?对症改**明天**的候选池,而不是今天硬凑数量。

> 一句话总结这一章:**每天精提 2 个小 universe、高 Fitness、对 ACTIVE 低相关的因子,提交前用可过性预测器自查,天天不断——5 天左右稳到 GOLD。**


---

