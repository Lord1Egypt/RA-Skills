# 历史回测、滚动调权与版本管理（v2.1）

## 范围与运行环境

Python 3.10及以上，核心程序、回测、调权、测试、打包**仅使用标准库**。不需要PyYAML、不联网、不读取券商账户、不下单。
本模块读取用户提供的历史时点快照和CSV行情，不自动假装已取得真实历史预测数据。合成数据只能检查功能，永远不能启用正式权重。

只优化Q质量、G成长、V估值权重。固定评分曲线、估值公式、风险排除规则、选股和执行策略；资金、技术、情绪权重不参与本次优化。
默认每个profile分别拟合；行业样本不足保持现有/内置权重，不硬拟合。不会自动把另一个行业的结果覆盖过来。

## 一键体验（合成数据）

在解压后的stock-portfolio-advisor目录运行：

```powershell
python scripts/make_demo_data.py --output-dir workspace/demo-history --years 12
python scripts/run_calibration.py --manifest workspace/demo-history/manifest.json --as-of 2021-12-31 --profiles default --config config/calibration.json --strategy config/backtest_strategy.json --output-dir workspace/demo-run
```

这会生成12年、12只**虚构证券**的工作日样本，然后建立历史评分面板并运行调权检查。工作日历不是实际A股交易日历，盈利、行情与历史假设均为合成，不可用来推断真实收益。
查看`workspace/demo-run/calibration.md`的人类可读摘要，JSON含完整审计。`activation.json`显示review_only；即使给合成输入加`--apply`，也会拒绝启用并返回非零退出码。
数据较大，不放入发行包；生成器随包提供。

## 真实数据入口

清单manifest.json示意（路径相对清单目录）：

```json
{
  "synthetic": false,
  "point_in_time": true,
  "includes_delisted": true,
  "historical_assumptions_verified": true,
  "source": "数据供应商、原始版本及存档标识",
  "universe_description": "当时可投资股票池的定义及历史成分来源，不是今天的存活股票清单",
  "label_months": 12,
  "bars_csv": "bars.csv",
  "benchmark_csv": "benchmark.csv",
  "snapshots": ["snapshots/2010-01-29.json", "snapshots/2010-02-26.json"]
}
```

上例仅说明格式，两个月无法训练。三个true必须经过实际外部核查后填写，不是程序对源数据真实性的认证。
快照应覆盖连续的月末交易日；每个快照使用v2评分输入结构，保存当时清单、行业、产业链分组、指标来源、财报公告日期与估值假设。不可把当前自选股/持仓倒推成历史股票池。
构建器重新计算固定v2.1规则下的Q/G/V，忽略已安装的学习权重。缺失/风险未核查/红线证券保留在面板，但不进入可投资排序；本研究策略对任何红线提示统一排除，比日常评分器的软降级更保守。
历史V必须来自当时预测存档，或当时可得资料下的固定重建规则；禁止把今天知道的盈利与合理倍数回填。任何快照标synthetic=true，整个数据集都会被标为合成。

### 行情CSV

```csv
date,code,open,close,split_factor,cash_dividend,buy_allowed,sell_allowed,delisted
2020-01-31,sh600000,10,10.1,1,0,true,true,false
```

- 每个代码/交易日唯一，使用**不复权**开盘/收盘价，元；股数按股计算。
- `split_factor`：当日股份转换倍数，默认1；拆为2股填2。`cash_dividend`为每股现金分红，按**拆股前持股数**在当日开盘前计入现金；真实数据需按现金实际入账时点处理，不能把未到账应收款当可用现金。
- 若供应商分红是拆股后每股口径，先换算；不要同时导入复权价和分红/拆股，否则重复计算收益。
- `buy_allowed`、`sell_allowed`为当日假设成交时点是否允许，使用true/false或1/0；不能只凭“未停牌”就假定涨跌停必然可成交。需供应商真实可成交性信息或保守的执行规则。
- 停牌期间也要显式提供行，买卖均false，close为合法估值标记；不静默删除暂停交易的证券。
- `delisted=true`是显式终止结算日，close为每股终止回收价值，允许0。实际尚未结算的退市证券不可假装按最后收盘价兑付；应提供可核实回收值/保守终止处理并说明。
- 终止前持仓日缺行情直接报错；不通过丢失失败股票改善收益。
- 不能用不复权价搭配缺失的企业行动。配股、复杂换股、跨币种、证券出借、融资融券暂不支持，需预处理或剔除并披露覆盖损失。

### 基准CSV

```csv
date,open_tr,close_tr
2020-01-31,1000,1005
```

用与股票数据一致的交易日历、含分红总回报指数开盘/收盘值；必须有全部模拟交易日，值为正。需要真实同口径基准，不能混用普通价格指数。
持股分红留现金而非自动再投；基准总回报指数可能隐含分红再投，二者差异需要在评估中承认。

## 完整真实数据运行

```powershell
python scripts/run_calibration.py --manifest data/manifest.json --as-of 2026-09-05 --config config/calibration.json --strategy config/backtest_strategy.json --output-dir workspace/calibration/2026-09-05 --apply
```

`--apply`只在真实数据声明、校验通过、候选通过全部门槛时更新本地config/weights.json；不涉及买卖或外部发布。不带该参数只出报告。
最新月度快照距截止日不能超过35天，最近行情不能超过7天；不可把多年前数据包装成今天的新校准。
分析截止日之后的数据与尚未结束的收益标签不进入训练/验证。正式权重最早**截止日次日生效**，不会回写改变过去快照。

也可分步执行：

```powershell
python scripts/build_backtest_dataset.py --manifest data/manifest.json --output workspace/dataset.json
python scripts/backtest.py --dataset workspace/dataset.json --start 2018-12-28 --end 2020-12-31 --weights 40,30,30 --profile default --strategy config/backtest_strategy.json --output workspace/backtest.json
python scripts/calibrate_weights.py --dataset workspace/dataset.json --as-of 2026-09-05 --config config/calibration.json --strategy config/backtest_strategy.json --output workspace/calibration.json --apply
```

示例日期必须换成数据集真实交易日，截止日也必须有相应新数据。backtest.py输出逐日净值、交易、未成交记录、费用、回撤、换手及基准对照。

## 回测的固定策略

这是用于比较权重的研究组合，**不是重演用户个人账户配置器**。
- 每月末排序，次一交易日开盘执行。不得同日收盘出信号又按该收盘价成交。
- 选择高于50分的前top_k，按预定权益预算/top_k分配，再受评级单票上限15%、行业30%、产业链30%约束；不足额度留现金，不自动放大其余股票。
- 当前卖单先执行再买入；被阻止卖出的持仓继续逐日计价、占用行业/权益额度，不用虚假成交腾出额度。
- 空股票池或某行业该月无成分时仍进行月度目标复核。未成交单不在下一日自动追单，等下次月度复核。
- 支持股数最小交易单位、分红、拆股和终止结算；现金不计利息，无杠杆。
- 持仓按每日收盘计净值，回撤为收盘净值回撤；测试区间末按市值结算展示，不假装全部清仓，不额外收退出手续费。
- 12个月收益标签用于检查排名能力；组合收益来自**月度调仓的逐日模拟**，不能把重叠的12个月收益直接连乘。

config/backtest_strategy.json的费用（买3bps、卖8bps、滑点5bps）只是演示假设，**不是当前法定费率或你的券商实际收费**。真实回测按时期提供费用，卖出费需包含适用税费。双倍费用/滑点是压力测试。
可添加`fee_schedule`数组，元素包含`from`日期与完整buy_fee_bps/sell_fee_bps/slippage_bps，按日期升序。首个生效日前用顶层假设。当前不支持最低佣金阶梯等复杂结构，需要预先确定近似影响或扩展执行器。

## 滚动调权与防止泄漏

默认配置：训练36个月、验证24个月、独立留出24个月；最多3个、至少2个非重叠留出窗口。每个日期的全部股票在同一分区。
训练标签必须在验证开始前完成，验证标签必须在留出开始前完成；跨边界标签**整条剔除**。12个月标签会损失约12个月有效观测，所以24个月验证/留出并不等于24个月独立标签。
默认至少8只股票/截面，训练至少18个、验证/留出至少6个可计算Rank IC的月份。原始历史通常需要约9年以上，实际取决于样本完整度。

每个窗口：
1. 以当前权重为中心，在±10个百分点范围按5个百分点网格产生候选，限制每项10–70%。
2. **先**使用alpha=0.2平滑，并限制单维调整≤3个百分点，然后才训练/验证，确保最终测试的就是将要启用的权重。
3. 训练按月度平均Rank IC加小幅偏移惩罚筛选前5个；验证用固定的IC/收益/回撤/换手目标选择，始终包括旧权重。
4. 将已选权重冻结后，在独立留出区间与旧权重对照，并做双倍成本测试。留出数据不用于从候选中择优。

各窗口可能选出不同向量；多窗口检验的是**滚动选择流程**，正式提案是最后一个窗口中冻结且实际检验过的向量。不会把测试通过后重新拟合的另一套权重直接上线。
门槛包含平均IC改善、平均扣费超额收益改善、至少60%窗口改善、最近窗口改善、非负成本压力改善、回撤和换手约束。所有门槛都为公开可配置的工程默认值，不是统计显著性证明。
搜索次数、候选筛选、有效月份、标签最后日期和分区边界保存在报告中。IC月份的12个月收益可能重叠，**不能把股票条数或月数当完全独立样本做显著性承诺**。

程序不会反复把上次校准已使用过的留出区间当新独立证据：某profile已有正式校准时，新留出开始日必须晚于上次training_cutoff。默认2×24个月留出要求意味着再次正式升级可能需要多年新增数据；季度可以检查，但绝不保证季度都有新权重。可事先调整观察期和门槛，但不能看过结果后反复放宽直到通过。

## 权重注册、到期与审计

发行包的config/weights.json初始无学习版本，使用内置权重，不附带私人校准结果。
启用时核对校准报告指纹、权重注册表指纹与日期，使用互斥锁、原子替换写入。完整报告保存在config/weight_history，重复运行同一校准不重复添加版本。
每份release保留权重、有效起始日期、校准截止日、最大标签结束日、规则版本、数据指纹和验证状态。有效期默认370天，到期后选择仍有效的较早版本，否则回退内置权重；到期回退也会体现在weights_version中。
错误文件、负权重、总和不为100%、规则版本错误、合成版本或未来标签都不会用于评分。
结果和HTML显示weights_version；分数变化拆分为数据变化、调权影响与红线/舍入差异，避免把调权造成的升分误写成基本面改善。

## 验证与打包

```powershell
python -B -m unittest discover -s scripts -p "test_*.py"   # 54 tests
python scripts/package_skill.py --output dist/stock-portfolio-advisor-2.2.0.zip
```

ZIP采用白名单，只含程序、规则说明、报告样式、图标提示词、默认配置和测试。排除workspace、用户持仓/历史行情、调权档案、缓存、临时文件以及旧ZIP。每个发行文件的SHA-256在包内MANIFEST.json中。
`assets/icon.png`不进包——SkillHub服务端会以「不允许的文件类型」拒绝，技能图标走平台托管的`iconUrl`字段；仓库里仍保留该图供GitHub展示。SKILL.md、程序、规则说明、config为必需项，缺失直接打包失败；assets下其余文件缺失只跳过不报错。
不把“程序测试通过”称为“真实市场回测通过”，不把模拟收益视作未来承诺。
