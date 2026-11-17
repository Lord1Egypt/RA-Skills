# 脚本完整索引（scripts/lib/）

> 从 `SKILL.md` 拆出（渐进式披露）。SKILL.md 只保留最常用的核心入口，
> 需要了解某个模块职责时再读本文件。
>
> **目录结构**：普通用户只接触 `scripts/run_ssq.py`（唯一入口）；所有内部模块与离线
> 数据都收在 `scripts/lib/` 下（你无需碰它们）。下表模块名均位于 `scripts/lib/`。

## 全部脚本职责一览

| 脚本 | 职责 |
|------|------|
| `run_ssq.py` | 跨平台统一启动器（本 skill 入口） |
| `lib/ssq_smart.py` | 真正执行器：下载→自检→预测→报告 |
| `ssq_auto.py` | 预测生成（含胆拖优化接入、频率板块、反遗漏自检） |
| `ssq_healthcheck_all.py` | 22 项自检护栏（含三体协同第 18 项、根↔SKILL 产物同步第 19 项、离线数据同步第 20 项、静态未定义名闸门第 21 项） |
| `check_undefined_names.py` | 零依赖 AST 静态检查：捕获 `py_compile` 看不见的 `NameError` 风险（护栏第 21 项调用） |
| `ssq_method_explorer.py` | 方法发现 + 证伪引擎（9 法） |
| `ssq_randomness_test.py` | 开奖随机性检验电池 |
| `ssq_common.py` | 核心纯函数（9 项过滤器、AC/奇偶/质合/012路等）+ 属性/差分/变质自测 |
| `ssq_power_engine.py` | 奖金派发可信源（9→7 奖级、奖池分档） |
| `ssq_dantuo_optimizer.py` | 胆拖优化（形态自适应、多目标：最可靠/最低成本/最高中一等奖概率） |
| `verify_report_sections.py` | 报告反遗漏必需板块清单断言 |
| `ssq_cross_validate_v84_final.py` | 三方交叉验证（第 4 节调权威重算） |
| `ssq_huiniao_api.py` / `ssq_data_recovery.py` / `ssq_period.py` / `ssq_result_verify.py` | 数据源/恢复/期号/闭环校验 |
| `ssq_enhance.py` / `ssq_ml_models.py` / `ssq_expert_scraper.py` / `ssq_expert_roster.py` / `ssq_expert_tracker.py` / `ssq_winner_stats.py` | 增强层（ML/冷热图/专家抓取+常驻名录+战绩自算/中奖人数） |
| `ssq_expert_roster.py` | **常驻专家名录（V1.0.8）**：内置 46 位专家元数据（42 权威名家 + 4 野路子高手）+ 6 个官方权威数据源，系统无论实时抓取成败始终"拥有"这批专家 |
| `ssq_expert_tracker.py` | **战绩自算 + 随机基线对照（V1.0.8）**：每期开奖后用系统自身抓到的专家推荐 vs 实际开奖独立打分，同时生成机选基线；专家排名仅相对基线有意义，不采信平台注水战绩 |
| `ssq_hypothesis_test.py` / `ssq_symmetry_test.py` / `ssq_visual_pattern_test.py` / `ssq_overlap_test.py` | 反诈骗闸门（常驻 no_edge） |
| `ssq_eci_backtest.py` / `ssq_enhanced_backtest.py` / `ssq_exhaustive.py` | 回测与穷举 |
| `ssq_draw_check.py` | **开奖核对 + 随机基线实证**：展开全部投注注→逐注算奖→蒙特卡洛随机基线对照→生成桌面《开奖核对报告.html》。把每次"没中"变成诚实性实证。**已接入统一入口 `run_ssq.py` 分析模式自动调用**（`--auto --sim 20000`，非致命）。也可手动：`python lib/ssq_draw_check.py --auto`（自动取最近已开奖期），或 `python lib/ssq_draw_check.py --period 26087 --front 5,10,16,24,27 --back 4,10` |
| `ssq_cost_effectiveness.py` | **胆拖性价比最优分析器（V4）**：精确超几何概率枚举预算内全部"真正胆拖"（前蓝球均展开≥2注），已剔除 3胆2拖/1胆4拖/2胆3拖/4胆1拖 等退化单注形态（W=5-K 致红球仅1注，本质=普通单注6+1，非胆拖）。按"最大候选号码池（相对复式最省）"与"最高任意中奖概率"双目标推荐；新增"复式等效注数/节省倍数"量化胆拖唯一真实优势。诚实声明所有结构期望收益恒 −50%，优化只能改结构不能改期望。`python lib/ssq_cost_effectiveness.py --budget 120`（预算120注=240元） |
| `ssq_history.json` / `ssq_valid_combos.json` | 历史开奖（3487 期）/ 9 项过滤合法组合 |
| `run_ssq.py` | **统一入口（推荐）**：自动探测 Python、支持 `--skip-download` 离线兜底。注：发布包不含 Windows `.bat`（平台禁用可执行脚本），定时任务请用本文件替代 |

