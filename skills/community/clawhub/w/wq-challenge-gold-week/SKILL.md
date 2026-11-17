---
name: wq-challenge-gold-week
version: "1.1.0"
description: "Use to compete in the WorldQuant BRAIN Challenge and climb to GOLD (10000) with AI assistance: sign-up, discovering accessible fields/operators via API, constructing alpha factors (fundamental x analyst-expectation x long-window, rank blends), passing Sharpe>=1.25 / Fitness>=1.0 / self-correlation<0.7 gates, and a daily submission harvest loop. Also for 中文 requests about WorldQuant BRAIN 因子挖掘、Challenge 冲金/GOLD、AI 辅助量化、alpha 提交拿分、Sharpe/Fitness/turnover 调优。"
metadata:
  author: dfkai
  version: "1.1.0"
  license: MIT
---

# 用 AI 辅助冲刺 WorldQuant BRAIN Challenge:从 0 到 GOLD

> 本 skill 是一套**方法论 + 可执行流程**:教你借助一个能调 HTTP / 写代码的 AI 助手(如 Claude Code、Kimi Code、Cursor),在 WorldQuant BRAIN 的 Challenge 竞赛里稳定、高效地**每天提交高质量 alpha、累积竞赛分**,用大约 **5 天左右的连续节奏**冲到 GOLD(10000 分)。
>
> **它教你"怎么钓鱼",不发你"一桶鱼"。** 全篇因子都是公开常识级模板,你要学的是自己发现、构造、筛选因子的动作——清单会过期、会撞车,方法不会。

**诚实的期望管理(先说清楚)**:GOLD 是排行榜等级 + track record(履历),Challenge 本身**没有现金奖**;分数每天封顶约 2000、按天累积,所以 10000 分 ≈ 连续约 5 天的稳定节奏,**没有 1 天速成**。真正发钱的是另一套选择性的 Research Consultant 项目,与此无关。

**⚡ 一键起步:** 本仓库自带配套脚本(`scripts/`,Python 3 + `requests` + `numpy`),注册好账号后四步跑通:

```bash
export BRAIN_EMAIL="你的注册邮箱"       # 凭证只进环境变量,绝不硬编码
export BRAIN_PASSWORD="你的密码"
python scripts/bootstrap.py           # ① 认证自检 + 探测你的字段/算子武器库
python scripts/mine.py --limit 20     # ② 批量挖矿:生成→回测→过门槛→入候选池
python scripts/submit_daily.py        # ③ 每日精提:推荐 top2,人工确认后提交
python scripts/check_score.py         # ④ 查分:score / level / 距下一等级
```

---

## 核心心智模型(必读,其余按需查章节)

### 计分规则(理解错了后面全是无用功)

- **按天累积、不减**;**每天封顶约 2000 分**(GOLD ≈ 5 个满分日的数学来源);**每天 3AM EDT 刷新**(北京时间 15:00 换"挑战日",之前的提交算前一天批次);**跨用户归一化**(要相对别人更好)。
- **★当天质量分 = 当天所有提交的"平均值",不是总和。** 由此整个策略浓缩成一句口诀:

> **宁缺毋滥,每天精提最优 1-2 个;质量看平均,连续看天数。掺一个弱的 = 主动拉低当天平均 = 净伤害。断更一天 = 永久少一天额度。**

### 三道提交硬门槛(不达标连提交都不行)

| 门槛 | 阈值 | 怎么救 |
|---|---|---|
| Sharpe | ≥ 1.25 | 换更干净的信号 / industry・subindustry 中性化剔行业 beta |
| Fitness | ≥ 1.0 | `Fitness = Sharpe × √(\|returns\|/max(turnover, 0.125))`,**换手在分母** → 把时间窗拉长(126/252/504)降换手,Fitness 立涨 |
| 自相关(对你已 ACTIVE 集合) | < 0.7(≥0.75 必被挡) | 提交前本地算"可过性预测器";撞车就换数据角色/换分母重构 |

### 高产骨架(80% 提交的地基)

```
group_rank( ts_rank( 分子/分母 , 长窗口 ) , 分组 )
```

分子 = 利润/现金流/分析师预期类;分母 = equity/close/assets/cap/sales/EV(每换一个分母就是一族新因子);窗口默认长窗;分组默认 industry。

### 每日循环(3AM EDT 刷新后跑一遍)

```
① 查 leaderboard:昨天涨了多少,距目标还差多少
② 批量生成候选 → 回测(严格 K=2 并发排队)→ 按三道门槛筛
③ 对幸存者算"对已 ACTIVE 集合的自相关",<0.7 才有提交资格
④ 只提最好的 1-2 个(小 universe > 高 Fitness > 低自相关)
⑤ 把这轮学到的写进你的研究 log / 活页手册
⑥ 明天再来(连续性 > 一切)
```

### 红线(任何模式下都生效)

- **提交永远人在环**:自动化可以跑回测、出排序,"今天提交哪几个"必须人拍板(不可逆动作)。
- **凭证只进环境变量**,绝不硬编码、绝不进 Git、绝不粘进聊天。
- **BRAIN 并发回测上限 K=2(账号级硬顶)**,尊重限流,绝不硬刚。
- **多 agent / swarm 用户**:并行"想"(探测/生成/复盘),串行"打"(回测收敛到单队列)——详见第⑤章 §5.9。

---

## 章节地图(按需读,全文在 `references/`)

| 何时读 | 章节 |
|---|---|
| 注册账号、拿 API 凭证、理解计分规则细节与等级门槛 | [第①章 参赛与规则](references/01-rules-and-scoring.md) |
| 探测你账号实际可用的字段/算子(tier 锁)、落盘武器库清单 | [第②章 数据与算子](references/02-arsenal-probing.md) |
| 构造能过闸的因子:分母杠杆表、换手-Fitness 数字表、组合五式、中性化选择 | [第③章 因子构造](references/03-factor-construction.md) |
| 提交生命周期、读 checks 定位失败原因、可过性预测器实现、每日收割策略 | [第④章 提交规则与收割](references/04-submission-harvest.md) |
| 可迁移的研究方法:OBSERVE→DECIDE→ACT→VERIFY→RECORD 循环、FRAME-CHECK、exploit/explore、提示词模板 A-D、**5.8 活页手册法(让迭代自己进化)**、**5.9 swarm/goal 多 agent 适配** | [第⑤章 AI 循环研究法](references/05-research-loop.md) |
| Day 0-5 的逐日执行日历 + 七大避坑 | [第⑥章 5 天计划与避坑](references/06-five-day-plan.md) |

**推荐阅读顺序**:第一次用 → ①→②→⑥(Day 0)跑通链路;开始挖矿 → ③④;跑到第 3 天觉得"挖空了"或想长期化 → ⑤(尤其 5.2 覆盖率纪律和 5.8 活页手册法)。

---

## 本 skill 的产出哲学:起步相同,演化不同

这个 skill **不发因子**(清单会过期、会撞车),它发的是一个**会分叉的方法**:所有人从同一套默认起步——但你的每一次复盘都应该改写两个属于你自己的文件:

1. **`wq_workspace/recipes.json`**(首跑 `mine.py` 自动生成)——你的搜索空间:换关键词、加分母、开新窗口、写自定义模板(占位符 `{num} {den} {num2} {den2} {w} {g}`,双腿相乘、rank blend 任意结构)。**改这里 = 你的网和别人的网开始不同。**每次挖矿跑完,脚本会当面提示你能改什么;**还不会调参?一键最全网:`python scripts/mine.py --preset full`**(窗口全档+三级分组+组合模板全开,空间 ~2000 条,靠 tried.txt 分天推进)——它依然只是"更大的公共起步",分叉靠你此后的修剪。
2. **你的活页手册**(从 `PLAYBOOK.template.md` 复制)——你的信念、教训、待验假设。**改这里 = 你的判断和别人的判断开始不同。**

两个人用同一个 skill 跑一个月,应该挖出完全不同的因子——如果没有,说明你只在"跑",没在"迭代"。第⑤章教的循环,就是驱动这两个文件演化的引擎。

还有一条进阶玩法:**把你读到的论文/文章直接投喂给系统**(第⑤章模板 E)——AI 会把不可部署的模型拆成可移植的"透镜"(一把本地尺子 / 一个新模板 / 一条待验假设),用你已有的回测数据零成本先验。你读的东西和别人不同,你的系统就长得和别人不同。

---

> **开源许可**:MIT(见 `LICENSE`)。本 skill 不含任何账号/凭证/专有因子,仅教方法;机制数字来自官方 FAQ 与作者实测,平台可能调整,以官方为准。不构成投资建议。
