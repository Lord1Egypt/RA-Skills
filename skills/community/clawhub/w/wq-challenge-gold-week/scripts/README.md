# 一键参赛脚本(scripts/)

配套 [SKILL.md](../SKILL.md) 的可运行实现:注册账号后,四条命令走完
「链路自检 → 挖矿 → 每日精提 → 查分」的完整闭环。

> **红线先说**:`submit_daily.py` 的每一次提交都需要你在终端里**逐个敲 y 确认**,
> 没有也永远不会有"跳过确认"的开关——"今天到底提交哪几个"必须人拍板
> (SKILL.md §5.7 自动化红线)。

## 0. 前置准备

1. **注册 BRAIN 账号**(免费):访问 platform.worldquantbrain.com,邮箱注册,
   在网页端手动跑通一个 simulation,并在竞赛页加入 Challenge(详见 SKILL.md §1.2)。
2. **Python 环境**:Python ≥ 3.8,只依赖两个第三方库:

   ```bash
   pip install requests numpy
   ```

3. **导出凭证环境变量**(绝不硬编码、绝不进 Git):

   ```bash
   export BRAIN_EMAIL="你的注册邮箱"
   export BRAIN_PASSWORD="你的登录密码"
   ```

   (也兼容 `BRAIN_USER` / `BRAIN_PASS` 这对变量名,二选一即可。)

## 1. 完整命令序列

在仓库根目录(或任意目录,工作文件会建在当前目录的 `wq_workspace/` 下)依次执行:

```bash
# ① 链路自检 + 武器库探测:认证 → 拉字段/算子 → 写 arsenal_usa.json + 打印摘要
python scripts/bootstrap.py

# ② 挖矿:骨架 group_rank(ts_rank(分子/分母, 窗口), 分组) 批量回测,
#    过三道门(Sharpe≥1.25 / Fitness≥1.0 / checks 无 FAIL)的 keeper 入池
python scripts/mine.py --limit 20

# ③ 每日精提(每天跑,按 3AM EDT 规划):可过性预测(对 ACTIVE 集合 corr<0.70)
#    → 推荐最优 1-2 个 → 你逐个 y/N 确认 → 提交并轮询结果
python scripts/submit_daily.py

# ④ 查分:score / level / rank + 距下一等级差距(BRONZE 1000 / SILVER 5000 / GOLD 10000)
python scripts/check_score.py
```

每日循环 = ②③④(②可加大 `--limit` 多挖);到 GOLD ≈ 连续约 5 天、每天精提 1-2 个,
断一天就永久少一天的分(SKILL.md §4.4)。

## 2. 各脚本一句话

| 脚本 | 作用 |
|---|---|
| `bootstrap.py` | 认证自检;分页拉 `/data-fields`(USA/TOP3000/delay1/EQUITY)与 `/operators`,按 category 汇总写 `wq_workspace/arsenal_usa.json`,打印武器库摘要与关键算子解锁情况。tier 升级后重跑。 |
| `mine.py` | 读武器库,按 SKILL.md §③ 公开骨架做「分子 × 分母(close/assets/equity/cap/sales)× 窗口(63/126/252)× 分组(industry/subindustry)」笛卡尔积;K=2 并发回测、8s 轮询;过三道门且与池内相关 <0.9 的入 `pool.jsonl`。`--limit N` 控制本次条数(默认 20)。Ctrl-C 安全,再跑即续。 |
| `submit_daily.py` | 拉你已 ACTIVE 的 alpha 做基准,对池内未提交候选算最大相关;只推荐 corr<0.70 的,按 universe 小优先 + Fitness 降序取前 2;**逐个人工确认**后提交,轮询到 ACTIVE 或打印失败 checks(如 SELF_CORRELATION),记录 `submit_log.jsonl`。 |
| `check_score.py` | 查 `GET /competitions/challenge`(嵌套 `leaderboard` 结构),打印 score/level/rank 与距下一等级差距。 |
| `wq_common.py` | 四个脚本共享的模块:凭证读取、认证会话(401 自动重认证一次、429 按 Retry-After 退避)、分页、PnL→日收益(带缓存)、Pearson 相关等。 |

## 3. 运行时产物(`wq_workspace/`,自动创建)

| 文件 | 内容 |
|---|---|
| `arsenal_usa.json` | 你账号实测可用的字段/算子清单(bootstrap 生成,mine 消费) |
| `tried.txt` | 已回测过的表达式,跨次运行去重 |
| `pool.jsonl` | 过三道门的 keeper 候选池(表达式 + 指标 + universe) |
| `pnl_cache/` | 各 alpha 的 PnL 缓存(删掉即强制重新拉取) |
| `submit_log.jsonl` | 提交记录(成功/失败/被你跳过) |

建议把 `wq_workspace/` 加进 `.gitignore`——里面有你的 alpha id 与回测数据,别提交进公开仓库。

## 4. 平台礼仪(脚本已内置,请勿修改去"绕过")

- 并发回测严格 ≤ **K=2**(低 tier 账号级硬上限)
- 轮询间隔 **8 秒**,不打快
- **429** 按 `Retry-After` 头退避;**401** 自动重认证一次
- 提交**永远人工确认**,每天只提最优 **1-2 个**(当天分是平均值,掺弱即降分)

## 5. 常见问题

- **认证失败(非 201)**:核对 `BRAIN_EMAIL` / `BRAIN_PASSWORD`;401 = 账密错误。
- **mine.py 说找不到 arsenal**:先跑 `bootstrap.py`。
- **候选全被三道门刷掉**:正常,继续加 `--limit` 挖,或按 SKILL.md §3.3 拉长窗口救 Fitness。
- **提交被 SELF_CORRELATION 挡**:换数据角色/换分母重构(§3.4 第五式),别只换中性化(§避坑⑤)。
- **分数没涨**:次日 3AM EDT 刷新后再查;确认提交真的到了 ACTIVE(看 `submit_log.jsonl`)。

> 免责声明:本目录不含任何账号、凭证或专有因子,只教方法;Challenge 无现金奖,
> GOLD 是排行榜/信誉等级(SKILL.md §1.5)。
