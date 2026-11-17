# 第⑥章 5 天速通计划 + 避坑

> 本文是《用 AI 辅助冲刺 WorldQuant BRAIN Challenge》的一章,完整章节地图见上层 SKILL.md。

**本章目录**

- 为什么是「5 天」而不是「1 天」
- 总览:5 天日历
- Day 0 — 搭环境(把链路跑通,不追求出因子)
- Day 1 — 搭挖矿脚本 + 提第 1 批
- Day 2–4 — 每日收割(核心循环)
- Day 5 — 冲线到 GOLD + 维持

---

## ⑥ 5天速通计划 + 避坑

> 前面五章教了你「怎么挖、怎么筛、怎么组合」。这一章把它拼成一条**可执行的日历**:从零环境到 GOLD(10000 分),约 5 天。核心节奏就一句话——**每天只提最好的 1–2 个,天天提,别停。**

### 为什么是「5 天」而不是「1 天」

Challenge 的分数**按天累积、不减**,但**每天封顶约 2000 分**,凌晨 3AM EDT 刷新一次。所以数学上:

```
GOLD(10000) ÷ 2000/天 ≈ 5 个满分日
```

这是硬约束,不是努力能压缩的。你能优化的只有**每天那 2000 分打不打得满**(靠质量分),以及**别断签**(断一天=白扔一天封顶)。所以"速通"的真实含义是:**每天都把当天的质量分顶到最高,连续 5 天**——不是熬夜一晚速成。

---

### 总览:5 天日历

| Day | 目标 | 产出 | 当天盯的硬指标 |
|-----|------|------|----------------|
| Day 0 | 搭环境、跑通链路 | 能 auth / 拉字段算子 / 跑 1 个 sim / 查 1 次 leaderboard | sim 能 `COMPLETE`;leaderboard 返回 `level/score` |
| Day 1 | 搭挖矿脚本、提第 1 批 | recipe 生成器 + 门槛筛选 + keeper 库;提 2 个 | 提交的 2 个:Sharpe≥1.25、Fitness≥1.0、corr<0.7 |
| Day 2 | 收割 + 扩多样性 | 提当天最优 2 个;新增 2–3 个新角色信号 | 昨日 leaderboard `score` 是否 +~2000;keeper 库 corr 分布 |
| Day 3 | 收割 + 从命中学习 | 提 2 个;复制昨天"命中家族"变体 | 累计 `score` 曲线斜率;当天 universe 平均是否偏小 |
| Day 4 | 收割 + 补正交通道 | 提 2 个;引入另类数据(期权 IV)等低相关信号 | 逼近 10000 的剩余分;新提 alpha 对已 ACTIVE 集合的自相关 |
| Day 5 | 冲线 + 维持 | 提 2 个补齐;确认到达 GOLD;设日常维持 | `level == "GOLD"`、`score > 10000` |

> 每天的操作是**同一套脚本 + 微调**,不是每天重写。Day 1 把脚本搭好,Day 2–5 基本是"改几个信号 + 点提交"。

---

### Day 0 — 搭环境(把链路跑通,不追求出因子)

目标:**证明每一段 API 都能通**。今天不产分,只拆雷。

> ⚡ 不想手写?`scripts/bootstrap.py` + `scripts/check_score.py` 就是本节清单的现成落地,跑完即 Day 0 达成。

**清单:**
1. 注册 BRAIN 账号,记下登录邮箱/密码,放进环境变量(见"避坑⑥"),**不写进代码**。
2. 跑通认证:`POST /authentication`(HTTP Basic 账密),拿到会话 cookie/token。
3. 拉一次 `GET /data-fields` 和 `GET /operators`,**存成本地 JSON**——这是你"实测解锁了什么"的地图,别凭猜。
4. 跑通一个最简单的 sim(比如 `rank(close/assets)`),轮询 `status` 直到 `COMPLETE`,读回 Sharpe/Fitness/turnover。
5. 查一次 `GET /competitions/challenge`,确认能读到 `leaderboard.score / level / rank` 和 `progress`。

**验证链路的最小脚本(伪代码,读者用自己的 AI 补全细节):**

```python
import os, requests, time

S = requests.Session()
# ① 凭证只从环境变量读,绝不硬编码
S.auth = (os.environ["BRAIN_EMAIL"], os.environ["BRAIN_PASSWORD"])
S.post("https://api.worldquantbrain.com/authentication")

# ② 拉字段/算子地图,落盘
fields    = S.get("https://api.worldquantbrain.com/data-fields").json()
operators = S.get("https://api.worldquantbrain.com/operators").json()
# → 存 fields.json / operators.json,后面挖矿只用这里"确认解锁"的东西

# ③ 跑通一个 sim
sim = S.post("https://api.worldquantbrain.com/simulations", json={
    "type": "REGULAR",
    "settings": {"region": "USA", "universe": "TOP3000",
                 "neutralization": "INDUSTRY", "decay": 4, "truncation": 0.08},
    "regular": "rank(close/assets)"
})
loc = sim.headers["Location"]
while True:                       # 轮询到 COMPLETE
    r = S.get(loc).json()
    if r.get("status") in ("COMPLETE", "FAIL", "ERROR"): break
    time.sleep(5)

# ④ 查一次 leaderboard(注意:score/level 嵌在返回的 "leaderboard" 键下)
lb = S.get("https://api.worldquantbrain.com/competitions/challenge").json().get("leaderboard", {})
print(lb["level"], lb["score"])
```

**今天盯的硬指标:** sim 能不能走到 `COMPLETE`;leaderboard 有没有返回 `level` 和 `score`。**只要这两个通了,Day 0 就成功了**,哪怕因子本身很烂。

---

### Day 1 — 搭挖矿脚本 + 提第 1 批

目标:把"生成 → 模拟 → 筛选 → 存 keeper → 提交"串成一条流水线,并提出**第 1 批 2 个**。

> ⚡ 配套脚本:`scripts/mine.py`(生成→模拟→过门槛→入池)+ `scripts/submit_daily.py`(推荐 top2、人工确认后提交)就是这条流水线的现成实现,可直接用或改造。

**1. recipe 候选生成器(把公式骨架当变量,别手写死清单):**

用第③④章的**通用高产模板**批量拼:

```python
SIGNALS = [                       # 基本面比率 = 分子/分母杠杆(公开常识级)
    "净利润/equity",   # ROE 家族(强)
    "盈利/close",      # 盈利收益率
    "现金流/assets", "营收增长/sales", "ebit/enterprise_value",
]
WINDOWS  = [126, 252, 504]        # 长窗 → 压低 turnover → 抬 Fitness
GROUPS   = ["industry", "subindustry", "sector"]
NEUTS    = ["INDUSTRY", "SUBINDUSTRY"]

# 模板: group_rank(ts_rank(SIGNAL, 窗口), 分组)
recipes = [f"group_rank(ts_rank({s}, {w}), {g})"
           for s in SIGNALS for w in WINDOWS for g in GROUPS]
```

> 用**字段/算子地图里确认解锁的**字段名替换 `净利润/equity` 等占位;低 tier 有些向量统计算子(如 `vec_stddev`)和非 USA 地区是锁的,别拿锁着的东西去拼。

**2. 并发跑 sim:** 低等级账号通常 **K=2 并发**(硬上限),用一个大小为 2 的队列轮询,别一次性甩几百个。

**3. 按硬门槛筛(平台不达标直接提不了):**

| 门槛 | 值 | 为什么 |
|------|----|--------|
| Sharpe | ≥ 1.25 | 提交硬门槛 |
| Fitness | ≥ 1.0 | 提交硬门槛;长窗降 turnover 来救 |
| 自相关 | < 0.7(≥0.75 直接被挡) | 对你**已 ACTIVE 集合**算 |

**4. 存 keeper 库:** 过门槛的存下来(表达式 + Sharpe/Fitness/turnover/universe),并**两两算相关**,只留 corr<0.7 的互相独立者。

**5. 提第 1 批 2 个:** 从 keeper 里挑 **Fitness 最高 + universe 尽量小 + 彼此低相关**的 2 个,`POST /alphas/{id}/submit`。

**今天盯的硬指标:** 提交的 2 个是否都满足上表三条门槛;keeper 库里是否已有 ≥5 个 corr<0.7 的备胎(明天的弹药)。

---

### Day 2–4 — 每日收割(核心循环)

3AM EDT 刷新后,昨天提的分会结算进 `score`。每天重复这套**收割循环**:

```
① 查 leaderboard:昨天 score 涨了多少?逼近 10000 还差几?
② 从 keeper 库挑当天"平均质量"最高的 2 个提交
③ 继续挖:新增 2–3 个"新角色/新组合"信号,补进 keeper
④ 从命中学习:昨天分涨得好的因子,复制它的"家族"做低相关变体
```

**每天的差异化重点:**

- **Day 2 — 扩多样性:** 昨天可能都是"盈利质量"家族。今天引入**跨角色**:分析师一致预期(`est_eps/est_fcf/est_sales`)、反转(`-(close/open-1)`)。用**组合法**造独立通道:
  ```
  0.5*rank(A) + 0.5*rank(B)          # rank blend,两个角色
  rank(盈利质量) * rank(分析师预期)   # 跨角色相乘
  ```
- **Day 3 — 从命中学习:** 看哪个已 ACTIVE 因子当天贡献大,**繁殖它**——换窗口、换分母杠杆、换分组,做出**低相关**的兄弟(注意:只换中性化不算新,见避坑⑤)。同时留意**当天 universe 平均要偏小**(小 universe 质量分更高)。
- **Day 4 — 补正交通道:** 引入**另类数据**做和主流基本面正交的信号,比如期权隐含波动率 `implied_volatility_*`、news/sentiment。目的是压低对已有 ACTIVE 集合的自相关,既好过 corr 门槛,又拉高当天"平均"。

**每天盯的硬指标(重要):**

| 指标 | 看哪里 | 健康值 |
|------|--------|--------|
| 累计 `score` 斜率 | `GET /competitions/challenge` | 每天 ~+2000(封顶) |
| 当天 2 个的**平均**质量 | 各 alpha 的 Fitness/universe/自相关 | 越高越好,**绝不掺弱的拉低平均** |
| 新 alpha 对 ACTIVE 集合自相关 | 提交前自算 | < 0.7 |
| keeper 库存量 | 本地库 | 始终 ≥ 明后天要用的量 |

> **当天质量分是当天所提 alpha 的"平均"**,所以宁可只提 1 个强的,也不要用第 2 个弱的把平均拉下来。

---

### Day 5 — 冲线到 GOLD + 维持

1. 早上查 `score`,算还差多少到 10000,提 keeper 里最优的补齐。
2. 确认 `GET /competitions/challenge` 返回 `level == "GOLD"` 且 `score > 10000`——**到线**。
3. **维持:** 分数不减,但如果之后还有 Challenge 目标,保持"每天精提 1–2 个"的日常;把挖矿脚本设成每天出一批候选,你只做最后的人工挑选和提交。

**今天盯的硬指标:** `level` 字段翻成 `GOLD`;`score` 越过 10000。

---

## 常见坑与诚实提醒

**① 快不了——日封顶决定了是"约 5 天"不是"1 天"。**
每天封顶 ~2000 分是硬结构。任何"一晚上冲 GOLD"的想法都撞墙。把精力放在"每天顶满 + 不断签",而不是"今晚多提 20 个"。

**② 别掺弱因子——当天分是"平均"。**
多提不等于多分。第 2 个如果明显弱,会把当天平均拉低,**净效果可能是负的**。宁缺毋滥,每天只放你手里最强的 1–2 个。

**③ 别过早判死——先查覆盖率。**
"这个方向没因子了""基本面挖空了"——先问自己:**我实测了字段/算子空间的百分之几?** 覆盖率 <20% 就下结论多半是错觉。你那张手写 recipe 网格,占公式空间的比例可能接近 0。停滞时换方法(换角色/换组合法/换数据类),别只是"用旧网格再跑一遍"。

**④ 别过度工程化。**
5 层嵌套、10 个信号 blend 的"精巧"因子,常常跑不赢 `group_rank(ts_rank(简单比率, 252), industry)` 这种笨基线。**精巧 ≠ 更好**。先把简单模板铺满,有余力再加深度。

**⑤ 同一信号换中性化 = 克隆,不算新。**
把一个因子从 `INDUSTRY` 换成 `SUBINDUSTRY` 中性化,通常和原版**高度相关**,会被 corr≥0.75 挡掉,也不给你新的多样性。真正的"新"来自换**信号本身**(新角色/新分母/新数据类),不是换外壳。

**⑥ 凭证安全——别泄漏。**
账密只放**环境变量或本地密钥文件**(加进 `.gitignore`),绝不硬编码进脚本、绝不提交进公开仓库、绝不粘进聊天/issue。开源你的挖矿脚本时,确认没带任何账号、cookie、已提交的 alpha ID。

**⑦ Challenge ≠ 现金,GOLD ≠ 自动拿钱。**
Challenge 是**排行榜 + 信誉/等级**,GOLD 是里程碑,不是发钱按钮。真正付费的是**另一套选择性的 Research Consultant 项目**,门槛、评审、名额都独立。把 Challenge 当成"练手、建 track record、争取被看见"的场,别当成躺赚。诚实地说:这套 skill 教的是**方法和效率**,不是保证收入。

---

到这里,你已经有了完整的一套:**会认证、会拉地图、会批量挖、会按门槛筛、会控相关性、会每天精提**。剩下的就是**按日历执行 5 天**——它不神秘,只是需要每天露面。你完全做得到,去把第一个 sim 跑通吧。

> **开源许可建议:** 本 skill 建议以 **MIT License** 发布——最大化可用性,允许他人自由学习、修改、二次分发,同时用一句免责声明说明"不含任何账号/凭证/专有因子,仅教方法"。
