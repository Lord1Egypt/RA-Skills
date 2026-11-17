<!-- 头图见 GitHub 版:github.com/dfkai/wq-challenge-gold-skill -->

# 一周拿下 WorldQuant 因子挑战金牌 —— AI 辅助的开源 Skill

> **实测战绩:6 天,score 2000 → 11306,GOLD 🏅,提交连发零被拒。**
> 你只需要:一个 AI 编程工具(Claude Code / Kimi Code / Cursor 均可)+ 一个免费 BRAIN 账号。

*An open-source Agent Skill: from zero to WorldQuant BRAIN Challenge **GOLD (10,000)** in about a week, with your AI assistant doing the heavy lifting — and a self-evolving research loop doing the thinking.*

---

## 为什么它不一样

特别感谢 [QuantML 的 wq-alpha-research](https://github.com/QuantML-Research/wq-alpha-research) 带来的灵感与起点。在它的基础上,这个版本做了三点关键优化:

**1. 把"冲金牌的真规则"炼进了经验里——不是提交越多越好。**
当天得分取的是你所有提交的**平均质量**,每天封顶、按天累积。所以最优策略只有一种:每天只提最优 1-2 个、绝不掺弱、天天不断。这套反直觉的打法(以及提交前的"可过性预测器":本地算自相关,<0.7 才放行)贯穿全篇——实测多日连发零被拒。

**2. 多 Agent 迭代学习 + 自我进化机制。**
分工明确:**Agent 负责挖,WorldQuant 的回测系统负责检验**。每一次策略改动都必须带一个可证伪的预测,到期由数据判决——兑现就采纳,判错自动回滚。这套"活页手册法"(§5.8)让系统跑得越久越聪明,而不是越久越乱;支持 swarm 多智能体并行研究(§5.9:并行"想",串行"打")。

**3. 同一起跑线,千人千面。**
所有人从同样的默认搜索空间起步;但你的每次复盘都在改写两个只属于你的文件——`recipes.json`(你的网)和活页手册(你的判断)。你还可以**把读到的论文/文章直接投喂给它**(模板 E),AI 会把不可部署的模型炼成你系统里的一把新尺子。**两个人跑一个月,应该挖出完全不同的因子。**

---

## 上手

**第 0 步:注册一个免费 BRAIN 账号** → **https://platform.worldquantbrain.com/**
(邮箱注册,完成平台引导,先在网页端手动跑通一个 simulation)

**第 1 步:安装 skill(按你的 AI 工具选一条)**

```bash
# Claude Code / Cursor / Codex / Kimi Code 及 20+ agents,通用安装:
npx skills add dfkai/wq-challenge-gold-skill

# Claude Code 插件市场:
/plugin marketplace add dfkai/wq-challenge-gold-skill
/plugin install wq-challenge-gold-week@wq-challenge-gold

# 腾讯 WorkBuddy:在 ClawHub(clawhub.ai)搜索导入,或手动拷贝到 ~/.workbuddy/skills/

# 手动:把本目录拷进你的 agent 的 skills 目录,如
#   .claude/skills/wq-challenge-gold-week/   (Claude Code, Cursor)
#   .agents/skills/wq-challenge-gold-week/   (Codex, Copilot, Gemini CLI, Kimi Code)
```

**第 2 步:四条命令跑通全流程**

```bash
pip install requests numpy
export BRAIN_EMAIL="你的注册邮箱"       # 凭证只进环境变量,绝不硬编码
export BRAIN_PASSWORD="你的密码"

python scripts/bootstrap.py           # ① 认证自检 + 探测你的字段/算子武器库
python scripts/mine.py --limit 20     # ② 批量挖矿:生成→回测→过门槛→入候选池
python scripts/submit_daily.py        # ③ 每日精提:推荐 top2,人工确认后提交
python scripts/check_score.py         # ④ 查分:score / level / 距下一等级
```

不会调参?一键最全搜索空间:`python scripts/mine.py --preset full`。
多 Agent / swarm 用户:见 SKILL.md §5.9——**并行"想",串行"打"**(BRAIN 账号级并发上限 K=2)。
**提交永远需要人工交互确认**——这是刻意设计的红线,不是缺失的功能。

---

## 仓库里有什么

- **`SKILL.md`** —— 核心心智模型 + 每日循环 + 章节地图(~90 行,渐进披露:agent 低成本加载核心,按需拉取章节)
- **`references/`** —— 六章全文:①规则与计分 ②武器库探测 ③因子构造 ④提交收割 ⑤AI 循环研究法(含活页手册法、论文投喂模板、swarm/goal 适配)⑥五天日历与避坑
- **`scripts/`** —— 可直接运行的四件套 + 共享模块(429 退避 / 401 重认证 / PnL 缓存 / 可过性预测器)
- **`PLAYBOOK.template.md`** —— 你的活页手册起点(复制后长成只属于你的版本)

## 诚实声明

Challenge 的 GOLD 是**排行榜等级 + 履历(track record)**,本身没有现金奖;真正付费的 Research Consultant 项目是独立、选择性的赛道。本项目仅教方法与效率,不构成投资建议;量化研究有风险。

## License

MIT — see `LICENSE`.
