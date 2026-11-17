# 全量提取覆盖清单（通用层 + 行业扩展层）

用户要「全量/核心数据都提出来」「深入解读这家公司」时，按本清单生成 plan 并逐组提取。
清单是**覆盖参考**而非固定 schema：meta 里不存在的组跳过并记 gaps；清单外用户点名的项照加。
提取优先走 records（`locate --records` 行检索），叙述型走正文精读。

> 深度解读的判断标准：三表勾稽能对上、盈利质量能拆开、风险事项不遗漏、股东回报说得清。

## 同义词表（records 检索不到先换词，再判 not_found）

| 概念 | 常见措辞 |
|------|----------|
| 权益合计 | 股东权益合计（H+A 公司）/ 所有者权益合计（准则措辞） |
| 资产总额 | 资产总计（工商版）/ 资产合计（银行版） |
| 期末现金 | 年末/期末 现金及现金等价物余额 |
| 现金净变动 | 现金及现金等价物净增加额 / 净减少额 |
| 归母净利润 | 归属于母公司股东的净利润 / 归属于上市公司股东的净利润（摘要表措辞） |

## 通用层 A–I（全行业底线）

## A. 主要会计数据与财务指标（sections.key_financials / tables.type=key_financials）

营业收入、归母净利润、扣非净利润、经营现金流净额、总资产、归母净资产、基本/稀释每股收益、净资产收益率（加权/摊薄）、资产负债率——**本期+上年同期+增减幅**，非经常性损益明细（non_recurring 表）。

## B. 三大报表核心科目（balance_sheet / income_stmt / cashflow_stmt）

- 资产负债表：货币资金、交易性金融资产、应收账款、存货、固定资产、在建工程、商誉、短期借款、长期借款、应付债券、归母所有者权益（期末+期初）。
- 利润表：营业总收入、营业收入、营业成本、销售/管理/研发/财务费用、投资收益、营业利润、利润总额、所得税、净利润、归母净利润。
- 现金流量表：经营/投资/筹资活动现金流净额、期末现金及等价物。
- 金融业公司：科目结构不同（存放央行/同业、客户贷款及垫款、吸收存款），按其报表科目提取，勿硬套工商科目。

## C. 主营构成与分部（segments / production_sales）

分行业/分产品/分地区的收入、成本、毛利率及变动——**每张 `type=segments` 表的每一行都要映射**，禁止只抽表头或只留一行。经营分部信息。产销量数据（`type=production_sales`：生产量/销售量/库存量）。

## D. MD&A 要点（mda_overview / mda_business / mda_industry / mda_outlook / risk_factors）

通用层，全行业。数字与归因必须成对，禁止只出金额。

- **变动原因**（`type=variance_reasons`）：费用分析表、重大资产负债变动表。每行输出 `{field, value, yoy_pct, reason}`——`reason` 取表头含「原因说明 / 情况说明 / 变动原因」的列原文；`yoy_pct` 取「变动幅度 / 变动比例」。
- **费率/比率**（`type=mda_ratios` 或财务回顾表）：毛利率、销售/管理/研发费用占营业收入比（本期+上年+变动）。银行业改用成本收入比（见 X-bank）。
- **经营模式 / 发展理念**（`mda_business`）：第四节「从事的业务情况 / 经营模式」摘要，值=当份报告原文，**禁止预置公司口号或品牌名**。
- **所处行业情况**（`mda_industry`）：行业综述中的关键量（产销规模、渗透率等），数据源名称随报告，不写死协会。
- **未来展望**（`mda_outlook`）：资本开支计划、战略方向摘要。定位必须在管理层讨论与分析章内，忽略重要提示里的前瞻性免责声明。
- **风险因素**（`risk_factors`）：优先「可能面对的风险」；不要把「前瞻性陈述的风险声明」当风险清单。

## E. 股东与股本（top_holders / holder_count）

股东总数、前十大股东（名称/持股数/比例/质押冻结标记）、控股股东与实控人、股份变动（增减持/回购 buyback）、限售解禁。

## F. 股东回报（dividend）

利润分配预案（每10股派息/转增）、现金分红总额、分红率、股息支付方式、中期分红安排。

## G. 治理与人员（executives / employees / rd_investment / equity_incentive）

董监高薪酬合计与前三（`executives` 表）、员工人数与结构（`employees` 表）、研发投入及占营收比（`rd_investment` 表）、股权激励（`equity_incentive` 表）。有表走 `record_map`，无表走 section 锚点 + text_scan。

## H. 重要事项（related_txn / guarantees / litigation / commitments / contingencies / subsequent）

关联交易金额与定价（`related_txn` 表）、对外担保余额（`guarantees` 表）、重大诉讼仲裁、承诺履行情况、或有事项、资产负债表日后事项——每项带金额与状态。

## I. 审计与会计政策（audit_report / key_policies）

审计意见类型与事务所、关键审计事项、重要会计政策变化、会计估计/差错更正。所得税附注：法定税率、有效税率（所得税费用/利润总额，可 derived）、优惠税率影响——附注「所得税率」调节表，全行业。

## 行业扩展层（industry_hint 命中时启用）

### X-bank（银行业）

**表**（有表才建）：`capital_adequacy`（核心一级/一级/总资本充足率、杠杆率）、`asset_quality`（不良贷款率、五级分类、拨备覆盖率/拨贷比）、`nim_spread`（净息差/净利差）、`deposit_loan`（吸收存款与发放贷款和垫款结构）。

**叙述**（无表则 text_scan）：`nim_drivers`（净息差变动归因）。

**指标清单（有 table_id）**：资本充足率三档、不良与拨备、净息差/净利差、存贷款余额与结构。

**gaps 必答（无专用表）**：成本收入比（`cost_income_ratio`）；零售/对客 AUM（`retail_aum`）。

**口径陷阱**：监管资本口径 vs 会计净资产；不良贷款率与拨备覆盖率勿与利润表拨备计提混加；日均余额 vs 时点余额。

叙述型归因（如净息差变动的主要原因）亦可走 `mda_overview` 正文精读，输出仍用 D 组 `{value, yoy_pct, reason}` 形态。

### X-automobile（汽车制造业）

**表**（有表才建）：`nev_sales`（新能源销量/占比）、`capacity_util`（产能利用率）、`overseas_ops`（海外销量或收入）、`production_sales`（产销量）。

**叙述**（无表则 text_scan）：`brand_sales`（分品牌销量/收入，标题运行时抽取）、`dealer_network`（经销商数量）。

分车型产销量与产能利用率、新能源车销量及占比、**分品牌销量/收入（若披露）**、海外销量与海外收入、单车均价/单车毛利（若披露）、研发投入（费用化/资本化/占比）、经销商数量、股权激励销量考核目标。

品牌名是公司实例：从当份 MD&A 品牌小节标题抽取，**禁止把具体品牌名写入 plan/schema/清单**。SUV/轿车/皮卡等是品类，可作行标签。

### X-auto_electronics（智驾/汽车电子方案商）

**表**（有表才建）：`ad_shipments`（处理硬件出货量与平均售价 ASP）、`customer_concentration`（前五大客户/最大客户收入占比）、`overseas_ops`（境外收入或出口定点）。

**叙述**（无表则 text_scan）：`design_win_pipeline`（定点车型数/SOP 量产数/在手订单储备）、`aso_price_trend`（ASP 与单车价值量变动归因）。

**指标清单**：分线收入与毛利率（产品方案 vs 授权及服务）、处理硬件出货量与 ASP、定点车型数与 SOP 转化、前五大/最大客户占比、研发开支及占收入比、市场份额（多口径）。

**gaps 必答（无专用表）**：市场份额三口径（`market_share_multi_source`：芯片出货/方案装机/收入，须标口径不可混用）；定点 vs SOP（`design_win_vs_sop`：两个数须分行，禁止混用）。

**口径陷阱**（提取时必须显式区分，混入即错）：
- 定点数 ≠ 量产数 ≠ 装机数；生命周期定点（如「累计 1,000 万套」）≠ 当期收入；
- 客户-股东双身份（战投既是客户又是股东）须标注，关联销售单独拆出；
- 「经调整」亏损（Non-IFRS）与报表亏损差异须拆开（优先股/可转债公允价值变动等非现金项）；
- 港股无季报：全年节奏用中报 + 盈利预告拼装，不得假设 Q1/Q3 数据存在。

芯片型号/客户代号（「供应商A」「客户A」）是公司实例：保留原文代号并标注「推断需依据」，**禁止把推断身份写成事实**。

### 季报 vs 年报

- `filing_kind=quarter` 时，D 组 MD&A 叙述（`mda_business` / `mda_industry` / `mda_outlook` / `risk_factors`）在 `gaps.json` 标 `not_applicable`，不强制 pending。
- 行业扩展叙述（`brand_sales` / `dealer_network` / `design_win_pipeline` / `aso_price_trend` / `project_progress` / `unit_cost` / `underwriting_profit` / `spread_income` / `trading_volume_drivers` / `sell_through` / `project_financing` / `power_price` / `fuel_cost` / `nim_drivers` / `pipeline_progress` / `vbp_policy_impact` / `pricing_volume` / `channel_reform` / `traffic_volume_drivers` / `tariff_policy` / `commodity_price`）仅年报启用。

### X-manufacturing（通用制造）
产销量、产能与在建产能、产能利用率、前五大客户/供应商集中度、存货结构与周转。

### X-nonferrous（有色金属）

**表**（有表才建）：`production_sales`（分金属产销量）、`reserves`（资源储量：矿石量/品位/金属量/分级）、`construction_projects`（重要在建工程：预算/本期增加/转固/工程进度）、`hedging`（衍生品与套保：合约金额/报告期损益/占净资产比）。分产品/分地区收入毛利率走通用 `segments`——**矿山端 vs 冶炼端毛利率对比是盈利结构核心**。

**叙述**（无表则 text_scan）：`project_progress`（重大项目投产时间、投资额、达产新增产能——增量逻辑核心）、`unit_cost`（单位成本/C1 现金成本/AISC/采选冶成本拆分）。

**指标清单**：分金属产量（矿产金/铜/锌、电解铝、氧化铝、阴极铜、锂盐、钴钼钨等）及**下一年度产量指引**（经营计划章节）；销量、库存量；保有资源量/储量及分级（探明/控制/推断 或 JORC/NI 43-101 口径）、储量年度变动、矿山服务年限；单位销售成本与成本构成（原材料/人工/折旧/能源）；在建项目进度与转固节奏、资本开支投向；套保规模与衍生品损益、TC/RC 加工费与原料自给率（冶炼企业利润核心变量）；安全生产费专项储备、环保投入；海外资产/收入/利润占比与权益比例；主要控股参股公司净利润（少数股东损益拆分）。

**口径陷阱**（提取时必须显式区分，混入即错）：
- 总产量 vs **权益产量**（联营/合营矿山权益份额，产量公告附注口径）；
- 锂盐实物吨 vs 折 LCE；金 千克 vs 吨；
- 资源量 vs 储量（仅证实+可信储量可用于服务年限测算）；JORC/NI 43-101 vs 国内分类；
- `hedging` 损益是套保噪音，还原主营盈利时需与公允价值变动损益对照。

矿山/项目名是公司实例：从当份报告原文抽取，**禁止把具体公司名/矿山名写入 plan/schema/清单**。

### X-insurance（保险业）

**表**（有表才建）：`premium_income`（原保险保费/已赚保费，宜分寿险/财险/健康险）、`claims_payout`（赔付支出/退保金）、`solvency`（综合/核心偿付能力充足率）、`investment_assets`（投资资产结构）、`nbv_ev`（新业务价值 NBV / NBV margin / 内含价值 EV）、`channel_mix`（个险/银保/经代渠道）。

**叙述**（无表则 text_scan）：`underwriting_profit`（承保利润与综合成本率归因）、`spread_income`（利差/投资收益率归因）。

**指标清单（有 table_id）**：保费收入与增速、已赚保费、赔付/退保、新业务价值与内含价值、渠道结构、综合/核心偿付能力充足率、投资资产余额与资产配置。

**gaps 必答（无专用表，不得静默跳过）**：IFRS17 CSM / 保险服务业绩（`ifrs17_csm`）；继续率/退保率时间序列（`persistency_surrender_rate`）；综合成本率若仅在正文则走叙述 `underwriting_profit`。

**口径陷阱**：原保险保费 vs 已赚保费；寿险首年保费 vs 续期；偿付能力为监管口径非会计利润；投资收益含公允价值变动时勿与承保利润混加。

### X-broker（证券业）

**表**：`brokerage_income`（经纪手续费及佣金）、`ib_underwriting`（投行承销保荐）、`am_aum`（资管规模/管理费）、`risk_indicators`（净资本、风险覆盖率等）、`margin_trading`（两融余额/利息）、`prop_trading`（自营与权益衍生品损益）。

**叙述**：`trading_volume_drivers`（市场成交量/佣金率变动对经纪收入的归因）。

**指标清单（有 table_id）**：经纪/投行/资管分部收入、两融余额、自营/衍生品损益、净资本与风险覆盖率、代理买卖证券交易额。

**gaps 必答（无专用表）**：客户资金/托管规模（`client_funds_custody`）。

**口径陷阱**：银行与券商均有「手续费及佣金」——须结合经纪/投行/资管分部或标题「证券」判断；客户保证金非自有资金。

### X-real_estate（房地产业）

**表**：`contracted_sales`（签约金额/签约面积）、`land_bank`（土地储备权益面积）、`delivery_completion`（竣工/交付/结转面积）、`contract_liabilities`（合同负债/预收与结转对照）、`three_red_lines`（净负债率/现金短债比/剔除预收后资产负债率）。

**叙述**：`sell_through`（去化率与项目销售节奏）、`project_financing`（融资渠道、债务与拿地节奏）。

**指标清单（有 table_id）**：签约金额与面积、土储总建面与权益建面、竣工与交付面积、合同负债/预收、三道红线指标。

**gaps 必答（无专用表）**：拿地金额/面积（`land_acquisition`）；权益口径 vs 全口径须在字段 `scope` 显式标注（`equity_vs_full_scope`）。

**口径陷阱**：签约销售（经营口径）≠ 收入确认（会计口径）；全口径 vs 权益口径土储/销售；预收账款与合同负债科目切换年份。

### X-energy（电力能源）

**表**：`installed_capacity`（分电源装机）、`power_generation`（发电量/上网电量/售电量）、`utilization_hours`（平均利用小时）、`hydrology`（来水/水库/蓄能，水电）、`power_price_mix`（中长期 vs 现货/市场化电量与电价）。

**叙述**：`power_price`（上网电价/市场化电价文字归因）、`fuel_cost`（燃料成本与电价联动，火电相关）。

**指标清单（有 table_id）**：装机容量、发电量、上网电量、利用小时、来水与水库、电价/交易结构。

**gaps 必答（无专用表）**：在建装机/外延并购容量（`capacity_under_construction`）；控股 vs 权益装机须在字段 `scope` 显式标注（`controlling_vs_equity_capacity`）。

**口径陷阱**：控股装机 vs 权益装机；发电量 vs 上网电量；利用小时口径（设备 vs 等效）。

### X-pharma（制药）

首批范围：创新药/仿制药/中药/生物制品等**制药企业**。明确不纳入：医疗器械、医药流通、医疗服务、独立 CDMO 路由。

**表**：`rd_pipeline`（在研项目/适应症/临床阶段）、`sales_channel_mix`（医院/OTC/配送等渠道）、`regulatory_milestones`（注册/一致性评价/医保/集采）、`capacity_gmp`（GMP 产能）、复用通用 `production_sales`。

**叙述**：`pipeline_progress`、`vbp_policy_impact`。

**gaps 必答**：`key_product_pricing`、`market_share_estimate`、`sales_force_scale`、`innovative_vs_generic_mix`、`cdmo_order_visibility`。

**口径陷阱**：原料药 vs 制剂；创新 vs 仿制；研发费用化 vs 资本化；中标价 vs 出厂价；药品单位不可混加。公司/产品名从原文抽取，**禁止写入 schema**。

### X-consumer（消费零售）

首批范围：白酒/饮料/乳业等快消 + 连锁零售，**同一 industry key**，用窄表区分业态。明确不纳入：珠宝黄金、银行零售、快递物流。

**表**：`retail_channel_mix`（分渠道收入；id 避开保险 `channel_mix`）、`dealer_network`、`store_operations`、`same_store_sales`、复用 `production_sales`。

**叙述**：`pricing_volume`、`channel_reform`。

**gaps 必答**：`dealer_inventory`、`same_store_sales_text`、`shipment_vs_revenue`、`member_metrics`。

**口径陷阱**：公司库存 vs 渠道库存；发货 vs 收入确认；出厂/批发/终端价；同店闭店调整；会员类型。

### X-transport_infrastructure（交运基建 · 高速/港口）

首批仅覆盖**高速公路、港口运营**。明确不纳入：航司、航运、机场、铁路、快递、工程承包（后续独立加厚）。

`industry_hint.transport_segment` ∈ `highway|port|mixed`：按 segment 将不适用 gaps 标 `not_applicable`。

**表**：highway — `highway_toll_traffic`、`concession_network_assets`；port — `port_throughput`、`port_berth_assets`。

**叙述**：`traffic_volume_drivers`、`tariff_policy`。

**共性 gaps**：`equity_vs_consolidated_throughput`、`operating_revenue_vs_accounting`、`concession_remaining_years`、`capacity_under_construction`。

**segment gaps**：highway — `etc_traffic_mix`、`toll_per_vehicle_text`；port — `berth_utilization`、`hinterland_economy`。

**口径陷阱**：车流量 vs 折算标准车；自然吨 vs TEU；吞吐量 vs 装卸量；控股 vs 权益资产；收费年限 vs 剩余特许期。

**注意**：吞吐量 KPI 并非必有表格——上港 2025 年报为纯叙述披露（MD&A「一是/二是」段），全档候选表无一含吞吐量；此时 `port_throughput` 不走表路径，吞吐量数据以 `traffic_volume_drivers` 叙述落盘（found 须 quote+page）。

### X-fossil_energy（化石能源 · 煤/油气）

首批覆盖煤炭与油气**商品侧**；table 层拆煤/油气。发电侧仍属 `energy`，金属矿山仍属 `nonferrous`。

**表**：煤 — `coal_production`、`coal_reserves`、`coal_cost_price`；油气 — `hydrocarbon_production`、`hydrocarbon_reserves`、`lifting_cost`。

**叙述**：`commodity_price`、`unit_cost`。

**gaps 必答**：`equity_vs_attributable_output`、`railway_port_shipment`、`coal_washing_yield`、`refining_chemical_margin`、`proved_vs_probable_reserves`。

**口径陷阱**：原煤/商品煤/外购煤；长协/市场价；吨煤完全/现金成本；油气当量换算；煤资源量 vs 油气证实储量。

## 未建模行业（暂缓）

以下行业**暂不**增加探测词 / 空 `table_id` 骨架，待 ≥2 家全链路 `quality=pass` 与叙述 KPI 硬门稳定后再按业务实例选型：

医疗器械、医药流通、医疗服务、独立 CDMO、珠宝黄金、快递物流、航司、航运、机场、铁路、工程承包、互联网/软件、钢铁、化工、农牧、传媒、水务燃气、REITs/物管、信托/租赁等。

`manufacturing` 维持探测 + 通用 `production_sales`，本轮不加专属表。

## 输出组织

- 统一输出到 `result-{ts}/`：`manifest.json` + `tables/*.json` + `narratives/*.json` + `gaps.json`。
- 未定型表进 `generic_table_*` + `promote_candidates.json`，由 Agent 按分析意图晋升（禁止写死品牌/公司名）；混源不晋升。
- 表格型条目按 `table_id` 分表；须经 `qa-tables`，无 `quality.json` 不得给下游。只消费 `verdict=pass` 的 typed 表。
- 每个表和叙述块必须自解释：`title`、`description`、`schema`（或 `bullets`）齐全。
- 对未进入清单分类但有稳定结构的表，允许保底输出 `generic_table_*`，确保“有表即落盘”。
- `variance_reasons` 若表内无 `reason` 列，只允许对缺失行逐条回补；失败则必须进 `gaps.json`，不能静默丢失。
- gaps 汇总列出不适用/未披露项——**全量提取的完整性由清单+gaps 共同保证**。
- derived 比率（净利率/净现比/分红率等）按 provenance.md 规则统一放 `derived/*.json`。
