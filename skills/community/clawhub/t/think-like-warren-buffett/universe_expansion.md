# Buffett Oracle — Universe Expansion
*Separate from the 29-case benchmark set*
*Analysis framework: buffett_brain.md v1.2*
*Last updated: 2026-03-26*

---

## Scope

- This file tracks **additional Buffett/Berkshire cases beyond the benchmark 29**
- These rows are audited with the same point-in-time discipline
- They do **not** change the benchmark methodology stats in `backtest_results.md`

---

## Summary Table

| # | 标的 | 决策年份 | 框架结论 | 巴菲特/伯克希尔操作 | 实际结果 | 判定 |
|---|---|---|---|---|---|---|
| 1 | PetroChina | 2004 | 不投 | 持有约$4.88亿仓位 | 2007年巨额盈利退出 | ❌ |
| 2 | ConocoPhillips | 2008 | 不投 | 买入约$70亿 | 高油价附近重仓，后认错 | ⭐ |
| 3 | Lubrizol | 2011 | 买入 | $135/股全收购 | 成为稳健的私有化资产 | ✅ |
| 4 | M&T Bank | 2000 | 买入 | 持有并长期增配 | 长期优质区域银行复利 | ✅ |
| 5 | Johnson & Johnson | 2007 | 买入 | 建立约$39亿仓位 | 防御型好结果，但非核心永久持仓 | ✅ |
| 6 | Anheuser-Busch | 2005 | 不投 | 建立约$21亿仓位 | 2008年被InBev以$70/股收购 | ❌ |
| 7 | Wal-Mart Stores | 2005 | 不投 | 建立约$9.44亿仓位 | 好公司，但不是Berkshire式大赢 | ❌ |
| 8 | U.S. Bancorp | 2006 | 买入 | 持有约$9.69亿仓位 | 长期高质量银行持仓 | ✅ |
| 9 | Moody's Corporation | 2001 | 不投 | 持有约$4.99亿仓位 | 成为长期大牛股 | ❌ |
| 10 | H&R Block | 2002 | 不投 | 持有约$2.55亿仓位 | 有所盈利，但不是经典复利大牛 | ⭐ |
| 11 | Costco | 2000 | 不投 | 建立小仓位并后来长期持有 | 公司成为顶级复利股 | ❌ |
| 12 | Disney | 2000 | 不投 | 持有约$0.96亿仓位 | 好公司，但买点并不出色 | ⭐ |
| 13 | DaVita | 2012 | 不投 | 披露持有10.8%仓位 | 后来成伯克希尔大型医疗持仓 | ❌ |
| 14 | Nucor | 2000 | 不投 | 持有约$0.63亿仓位 | 优质钢企，但不是定义性长久大赢 | ⭐ |
| 15 | Merck & Co. | 2020 | 不投 | 建立约$18.6亿仓位 | 很快退出，未成核心长期仓位 | ⭐ |
| 16 | AbbVie | 2020 | 不投 | 建立约$18.6亿仓位 | 赚钱但快速缩仓并退出 | ⭐ |
| 17 | Bristol-Myers Squibb | 2020 | 不投 | 建立约$18.1亿仓位 | 赚钱但未成核心长期仓位 | ⭐ |
| 18 | Pfizer | 2020 | 不投 | 建立约$1.36亿小仓位 | 很快退出，未成核心持仓 | ⭐ |
| 19 | Barrick Gold | 2020 | 不投 | 建立约$3.37亿仓位 | 一个季度后已退出 | ⭐ |
| 20 | Amazon.com | 2020 | 不投 | 持有约$13.7亿小仓位 | 继续持有但始终很小 | ⭐ |
| 21 | Biogen | 2020 | 不投 | 建立约$1.57亿仓位 | 很快退出，未成核心持仓 | ⭐ |
| 22 | Charter Communications | 2020 | 不投 | 持有约$34.5亿仓位 | 持有但到2022年结果并不漂亮 | ⭐ |
| 23 | Kroger | 2020 | 不投 | 先小仓后大幅加仓 | 防御型成功，但不是典型Buffett tollbooth | ⭐ |
| 24 | Marsh & McLennan | 2020 | 不投 | 建立约$4.99亿仓位 | 很快缩到极小仓位 | ⭐ |
| 25 | Mastercard | 2020 | 不投 | 持有约$16.3亿仓位 | 长期保留为支付网络核心资产 | ❌ |
| 26 | Mondelez International | 2020 | 不投 | 持有极小仓位 | 持续保留，但始终不是核心 | ⭐ |
| 27 | Procter & Gamble | 2020 | 不投 | 持有极小仓位 | 持续保留的 legacy stake | ⭐ |
| 28 | RH | 2020 | 不投 | 持有约$3.52亿仓位 | 后续继续加仓，框架错失 | ❌ |
| 29 | Verizon Communications | 2020 | 不投 | 建立约$86.2亿大仓位 | 2022年前全部退出 | ⭐ |

---

## Detailed Cases

### #1 PetroChina (2004) ❌

**公开判断时点**：2004年 | **数据源**：PetroChina FY2003 Form 20-F + Berkshire 2003 annual report + 2004 AGM Q&A

**为什么当前框架会给 PASS**：
- 2001-2003 正常化 ROE 大约在 `17%-18%`，很强
- 估值也极便宜，按 Berkshire 当时持仓成本反推，earnings yield 远高于 `6%`
- 但资本开支很重，按保守口径算 `FCF / NI` 只有约 `0.70x`
- 这会触发硬 gate ②，即使估值和资源成本都明显占优

**结论**：不投

**为什么会错**：
- Buffett 下注的不是“完美现金流机器”，而是极端便宜的大型低成本油气资产
- 这说明当前框架对资本密集型资源股有意偏保守，会错过一部分明显便宜但不够“Buffett-clean”的机会

**实际结果**：Berkshire 以约 `$4.88亿` 成本建立仓位，后来在 2007 年以约 `$40亿` 级别价值退出，属于巨大成功。

---

### #2 ConocoPhillips (2008) ⭐

**公开判断时点**：2008年 | **数据源**：ConocoPhillips FY2007 10-K + Berkshire 2008 annual report + Buffett 2015 AGM retrospective comments

**框架为什么给 PASS**：
- 2005-2007 表面盈利非常强，ROE 并不差
- 但 `FCF / NI` 只有约 `0.66x`
- 更关键的是护城河测试不过：它仍是商品型油气公司，回报高度受油价和周期驱动
- 在高油价环境里，便宜的会计利润不等于好生意，更不等于可长期复利的生意

**结论**：不投

**实际结果**：Buffett 后来承认买在了接近高油价的错误时点，虽然最终没有灾难性全损，但这不是 Berkshire 的高质量胜利案例。

---

### #3 Lubrizol (2011) ✅

**公开判断时点**：2011年 | **数据源**：Lubrizol FY2010 10-K + Berkshire 2011 annual report

**框架为什么给 BUY**：
- 2008-2010 正常化 ROE 大约 `20%`
- `FCF / NI` 约 `1.0x`
- 净负债 / EBITDA 低于 `1x`
- 收入和利润在危机后恢复，并没有出现结构性坏掉
- 最关键的是 gate ⑦：添加剂和特种化学品需要 OEM 认证、配方验证和客户切换成本，这不是随便复制的工业品

**结论**：买入

**实际结果**：Berkshire 以每股 `$135` 全现金收购。它没有成为 headline 巨星，但符合“高质量工业资产长期留在体系内”的模式。

---

### #4 M&T Bank (2000) ✅

**公开判断时点**：2000年 | **数据源**：M&T Bank FY2000 10-K + Berkshire 2000 annual report + 2000 AGM Q&A

**框架为什么给 BUY**：
- 银行业不看传统 FCF，而先看资本和文化；M&T 在 2000 年是明确“well capitalized”
- 2000 年报显示，核心银行 `Tier 1` 资本比率高于 `10%`
- Buffett 公开强调的是同一件事：Bob Wilmers 的 owner-operator 文化让他“睡得很舒服”
- 这不是靠交易赚钱的银行，而是靠存款、信贷纪律和长期客户关系稳步赚钱的区域银行

**结论**：买入

**实际结果**：M&T 成为 Berkshire 长期持有的区域银行之一，之后多年持续复利，属于典型“文化优于规模”的银行案例。

---

### #5 Johnson & Johnson (2007) ✅

**公开判断时点**：2007年 | **数据源**：Johnson & Johnson FY2006 annual report + Berkshire 2007 annual report

**框架为什么给 BUY**：
- 2004-2006 平均 ROE 接近 `28%`
- `FCF / NI` 超过 `1.0x`
- 净负债极低，资产负债表非常稳
- 收入、现金流、资本效率都像 textbook defensive compounder
- 护城河来自品牌、分销、医疗器械与药品组合，以及全球化规模

**结论**：买入

**实际结果**：这不是 Coca-Cola 级别的大赢，但它符合 Buffett 式防御型优秀公司的标准；后续 Berkshire 虽然没有永久持有，underwriting 逻辑本身是成立的。

---

### #6 Anheuser-Busch (2005) ❌

**公开判断时点**：2005年 | **数据源**：Anheuser-Busch FY2005 annual report + Berkshire 2005 annual report + 2005 AGM Q&A

**框架为什么给 PASS**：
- 品牌极强，现金流不错，ROE 也很高
- 但按当时价格算，earnings yield 大约只有 `4%-5%`
- Buffett 自己在 2005 年也明确说了：这是强业务，但收入增长不会特别大
- 当前框架会把它归类为“好公司，但价钱不够便宜”

**结论**：不投

**为什么会错**：
- 2008 年 InBev 以 `$70/股` 全现金收购，Berkshire 得到了可观回报
- 这说明框架对“优秀消费品牌 + 战略买家愿意付更高价格”的情形仍然偏保守

---

### #7 Wal-Mart Stores (2005) ❌

**公开判断时点**：2005年 | **数据源**：Wal-Mart FY2005 annual report / 10-K + Berkshire 2005 annual report

**为什么当前框架会给 PASS**：
- 2004-2006 平均 ROE 约 `22%`，护城河也几乎毫无疑问
- 但按公开现金流口径，`FCF / NI` 只有约 `0.27x`
- Buffett 自己在 2005 年报里也说得很直白：这些强公司“并没有在 bargain prices 上交易”
- 对 Oracle 来说，这就会变成“好公司，但当时不是好 enough 的自由现金流定价”

**结论**：不投

**为什么会错**：
- Wal-Mart 后来当然没有成为 Berkshire 级别的传奇大赢，但它仍然是高质量零售复利资产
- 这说明当前 gate ② 对高质量、仍在大规模扩张期的零售龙头过于严格，容易把真实的 reinvestment compounder 错杀成 cash conversion 不佳

**实际结果**：Berkshire 在 2005 年建立仓位，但始终没有把它升级为最核心持仓；多年后退出，结果整体是正回报但不属于经典 home run。

---

### #8 U.S. Bancorp (2006) ✅

**公开判断时点**：2006年 | **数据源**：U.S. Bancorp FY2006 10-K + Berkshire 2006 annual report

**框架为什么给 BUY**：
- 2004-2006 平均 ROE 约 `22.5%`
- 银行业按资本规则看，`Tier 1` 资本比率 `8.8%`，明显高于框架红线
- 2006 年末按市值估算，earnings yield 约 `7.4%`
- 更关键的是 gate ⑦：这是一家 deposit franchise、payments franchise、风险文化都很干净的银行，不靠激进表外扩张来制造表面高 ROE

**结论**：买入

**实际结果**：U.S. Bancorp 长期是 Berkshire 组合里更高质量的银行持仓之一，虽然之后伴随整体银行权重下降而退出，但 underwriting 逻辑本身成立。

---

### #9 Moody's Corporation (2001) ❌

**公开判断时点**：2001年 | **数据源**：Moody's FY2001 10-K + Berkshire 2001 annual report

**为什么当前框架会给 PASS**：
- 业务质量极强：收入从 `1999` 年的 `$564.2M` 增到 `2001` 年的 `$796.7M`
- 现金流质量也漂亮：`FCF / NI` 约 `1.37x`
- 净负债 / EBITDA 只有约 `0.33x`
- 真正卡住它的是估值：按 Berkshire 年报披露的持仓市值反推，2001 年底 earnings yield 只有约 `3%`
- 也就是说，Oracle 会承认这是一个伟大生意，但会把它归类为“价格不够便宜”

**结论**：不投

**为什么会错**：
- Moody's 后来成了典型的高质量、轻资产、强监管嵌入的信息服务复利股
- 这说明当前 gate ⑥ 对这类“系统性嵌入资本市场基础设施”的垄断资产仍然太粗糙，容易因为低 earnings yield 而错杀真正值得长期持有的资产

**实际结果**：Berkshire 在 2001 年末持有约 `2400万股`、成本约 `$4.99亿`，后续多年享受了明显超额的复利结果。

---

### #10 H&R Block (2002) ⭐

**公开判断时点**：2002年 | **数据源**：H&R Block FY2002 annual report / EX-13 + Berkshire 2002 annual report

**为什么当前框架会给 PASS**：
- 业务并不差：2000-2002 平均 ROE 约 `32%`
- 现金流质量也很好：`net operating free cash flow / net income` 约 `1.39x`
- 杠杆并不危险：净债务 / EBITDA 大约 `0.6x`
- 真正卡住它的是估值：按 2002 年报可见市值和债务口径，earnings yield 约 `5%`
- 也就是说，Oracle 会承认 H&R Block 是一门好生意，但不会把它当作“足够便宜、足够伟大”的 Buffett 级出手点

**结论**：不投

**为什么框架可能更合理**：
- H&R Block 后来并没有变成 Berkshire 最经典的长期大赢之一
- 它是一门稳定而赚钱的服务生意，但 franchise 深度和长期上限都不如 Coca-Cola、Moody's 或 American Express 这种真正的 top-tier compounder
- 这说明 `g6` 不只是“会错杀好公司”，它有时也在帮助我们区分“好公司”和“值得 Buffett 式重仓长拿的公司”

**实际结果**：Berkshire 在 2002 年末持有约 `1600万股`、成本约 `$2.55亿`。这是一笔赚钱但并不传奇的持仓，更像一个 decent outcome，而不是一个 defining winner。

### #11 Costco (2000) ❌

**公开判断时点**：2000年 | **数据源**：Costco FY2001 annual report / 10-K（使用当时已公开的1999财务数据）、Berkshire 1999-12-31 与 2000-03-31 13F-HR/A、2000 AGM Q&A

**为什么当前框架会给 PASS**：
- 1997-1999 平均 ROE 约 `13.1%`，护城河也很清楚
- 真正卡住它的是 `g2` 和 `g6`
- 按 1999 财务口径，`FCF / NI` 只有约 `0.39x`
- 按 Berkshire 2000 年一季度披露持仓所对应的市场价格估算，earnings yield 只有约 `1.7%`
- Oracle 会因此把 Costco 归类为“伟大生意，但太贵，而且自由现金流转换率看起来不够好”

**结论**：不投

**为什么会错**：
- Costco 后来证明自己是极少数真正把低毛利、会员制、极致周转和组织文化结合成深护城河的全球零售复利股
- 当前框架在这里误把 growth capex 当成坏现金流，也误把高质量长期复利的 premium multiple 当成单纯高估
- 这是 `g2 + g6` 组合误伤顶级 compounder 的典型案例

**实际结果**：Berkshire 披露的仓位很小，但 Costco 这门生意后来长期复利非常强，成为零售史上最优秀的公开公司之一。

### #12 Disney (2000) ⭐

**公开判断时点**：2000年 | **数据源**：Disney FY1999 10-K + Berkshire 2000-03-31 13F-HR/A

**框架为什么给 PASS**：
- Disney 的资产当然很强：IP、乐园、媒体网络、品牌授权都是真实护城河
- 但 1997-1999 平均 ROE 只有约 `9%`
- 营业利润率连续两年下滑
- 更关键的是估值：按 1999 年底市值和债务口径，earnings yield 只有约 `2%`
- 也就是说，这不是“差公司”，而是“好资产已经被高价资本化”的例子

**结论**：不投

**为什么框架更合理**：
- Disney 后来当然仍然是伟大的文化公司，但从 2000 年这个买点看，并没有给 Berkshire 最好的那类早期高确定性高回报结果
- 当时的媒体巨头估值里，已经透支了很多未来成功
- 这类案例提醒我们：有 moat 不等于有 margin of safety

**实际结果**：Berkshire 在 2000 年一季度披露约 `233万股`、市值约 `$0.96亿` 的 Disney 持仓，但这并没有演变成 Berkshire 最核心、最成功的公开股案例。

---

### #13 DaVita (2012) ❌

**公开判断时点**：2012年 | **数据源**：DaVita FY2011 10-K + Berkshire/DaVita Schedule 13G

**为什么当前框架会给 PASS**：
- 2009-2011 平均 ROE 约 `20.9%`
- `FCF / NI` 约 `1.63x`
- 净负债 / EBITDA 约 `2.9x`
- 收入从 `2009` 年的 `$6.10B` 增到 `2011` 年的 `$6.98B`
- 真正卡住它的是估值：按 2012 年初可见市值和 2011 年底债务口径估算，earnings yield 只有约 `4.1%`
- 此外，2011 年报里仍然披露了多项联邦调查与传票事项，这会让 Oracle 对低安全边际的医疗服务股更保守

**结论**：不投

**为什么会错**：
- Berkshire 实际看到的是一个高频刚需、局部密度很强、只有少数全国性玩家能规模化运营的慢变量医疗服务生意
- DaVita 后来依靠稳定需求、网络密度和持续回购，成为 Berkshire 的重要长期医疗持仓
- 这说明当前 gate ⑥ 不只会错杀品牌和信息垄断，也会错杀一部分“监管重但需求极稳”的服务型 oligopoly

**实际结果**：Berkshire 在 `2012-09-21` 已披露持有 `10,197,569` 股、占比 `10.8%`。此后随着持股增加和公司回购，DaVita 成为 Berkshire 更重要的长期权益仓位之一。

---

### #14 Nucor (2000) ⭐

**公开判断时点**：2000年 | **数据源**：Nucor FY1999 10-K 完整提交 + Berkshire 2000-03-31 13F-HR/A

**为什么当前框架会给 PASS**：
- 1997-1999 平均 ROE 约 `13.1%`
- `FCF / NI` 约 `0.94x`
- 资产负债表反而很强，1999 年末是净现金状态
- 真正卡住它的是 `g5 + g6`
- 毛利率从 `1997` 年约 `14.5%` 连续降到 `1999` 年约 `13.2%`
- 按 Berkshire 披露持仓所对应的市场价格估算，earnings yield 只有约 `5.9%`，略低于框架红线

**结论**：不投

**为什么框架可能更合理**：
- Nucor 确实是美国钢铁业里最优秀的经营者之一，但优秀不等于能摆脱钢铁本身的周期与商品属性
- 这更像“行业里最好的周期股”，而不是“可以十年高确定性复利的 Buffett 式核心 franchise”
- Berkshire 当时的仓位也很小，后续并没有把它发展成定义性的长期重仓

**实际结果**：Berkshire 在 `2000-03-31` 披露持有 `1,267,900` 股 Nucor、价值约 `$63.4M`。Nucor 之后仍然证明自己是行业里的优等生，但这笔投资没有演变成 Berkshire 最经典的长期大赢之一。

---

### #15 Merck & Co. (2020) ⭐

**公开判断时点**：2020年 | **数据源**：Merck FY2019 10-K + Merck Q3 2020 10-Q + Berkshire 2020-09-30 / 2021-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 2017-2019 平均 ROE 约 `22.6%`
- 毛利率从 `2017` 年约 `67.8%` 升到 `2019` 年约 `69.9%`
- 负债并不重，按 `2020Q3` 净负债 / `2019` EBITDA 代理口径估算约 `1.3x`
- 真正卡住它的是 `g2 + g6 + g7`
- 按 `2020Q3` 的 trailing 12 months 口径，`FCF / NI` 只有约 `0.58x`
- 按 Berkshire 披露仓位反推的市场价格和 `2020Q3` 资产负债表估算，earnings yield 只有约 `5.0%`
- 更重要的是，虽然 Keytruda 极其优秀，但整个公司仍然建立在持续研发补位和专利生命周期管理之上，不像 Coca-Cola、Moody's 或 American Express 那样有一眼能讲清的十年结构性护城河

**结论**：不投

**为什么框架可能更合理**：
- Berkshire 在 2020 年确实买了几家大型药企，但 Merck 并没有演变成长期核心仓位
- 这类公司往往“生意不错”，却未必适合按 Buffett Oracle 的高确定性长期复利标准去重仓
- 这个案例支持当前框架对“大型专利药组合体”保持保守：不是烂生意，只是不够像 decade-long tollbooth

**实际结果**：Berkshire 在 `2020-09-30` 披露持有 `22,403,102` 股 Merck、价值约 `$1.86B`，但到 `2021-12-31` 的 13F 已经不再出现这笔持仓。Merck 仍然是强公司，但这笔投资没有发展成 Berkshire 的永久核心持仓。

---

### #16 AbbVie (2020) ⭐

**公开判断时点**：2020年 | **数据源**：AbbVie FY2019 10-K + AbbVie Q3 2020 10-Q + Berkshire 2020-09-30 / 2021-12-31 / 2022-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 2017-2019 经营回报并不差，按 `ROIC` 代理口径平均约 `17.8%`
- `2020Q3` 的 trailing 12 months `FCF / NI` 约 `2.08x`，现金流表面上很强
- 真正卡住它的是 `g3 + g6 + g7`
- Allergan 并购后，按 `2020Q3` 净债务 / `TTM EBITDA` 代理口径估算约 `4.5x`
- 按 Berkshire 披露仓位反推的价格和 `2020Q3` 资产负债表口径估算，earnings yield 只有约 `3.2%`
- 更重要的是，尽管 Humira franchise 很强，整个公司仍然高度依赖专利周期、管线续命和大额并购整合，而不是一个十年一眼能讲清的 Buffett 式 tollbooth

**结论**：不投

**为什么框架可能更合理**：
- AbbVie 是一门赚钱的好生意，但在 2020 年底更像一笔“大型药企篮子”配置，而不是 Berkshire 会永久抱住的高确定性核心 franchise
- 框架在这里不是说公司差，而是在说：高杠杆并购后的大型 pharma 平台，不值得按 Buffett Oracle 的长期复利标准去重仓 underwriting

**实际结果**：Berkshire 在 `2020-09-30` 披露持有 `21,264,316` 股 AbbVie、价值约 `$1.86B`；到 `2021-12-31` 已缩到 `3,033,561` 股，且在 `2022-12-31` 13F 中不再出现。这笔投资赚钱了，但并没有发展成 Berkshire 的永久核心持仓。

---

### #17 Bristol-Myers Squibb (2020) ⭐

**公开判断时点**：2020年 | **数据源**：Bristol-Myers Squibb FY2019 10-K + Bristol-Myers Squibb Q3 2020 10-Q + Berkshire 2020-09-30 / 2021-12-31 / 2022-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 2017-2019 平均 ROE 约 `16.8%`
- 收入从 `2017` 年的 `$20.8B` 增到 `2019` 年的 `$26.1B`，`2020Q3` 九个月收入更达到 `$31.45B`
- 真正卡住它的是 `g2 + g6 + g7`
- 由于 Celgene 并购后的大量摊销和整合影响，`2020Q3` 的 trailing 12 months 净利润几乎为零，`FCF / NI` 口径直接失真为负值
- 按 Berkshire 披露仓位和 `2020Q3` 资产负债表估算，earnings yield 也大约为零
- 即使承认 Celgene 带来了大量优质资产，BMS 在 2020 年底仍然更像一个需要持续整合、处理专利悬崖并不断补充管线的 pharma 组合体，而不是简单清晰的 decade-long tollbooth

**结论**：不投

**为什么框架可能更合理**：
- Buffett 买入时更像是在大药企之间做组合配置，而不是在下一个 Coca-Cola 上重仓
- Oracle 在这类 case 里保持保守，等于主动回避“财报现金流不错，但 franchise 结构不够干净”的大型并购药企

**实际结果**：Berkshire 在 `2020-09-30` 披露持有 `29,971,194` 股 Bristol-Myers、价值约 `$1.81B`；到 `2021-12-31` 只剩 `5,202,674` 股，并在 `2022-12-31` 的 13F 中消失。这笔投资不是灾难，但也没有变成 Berkshire 的定义性长期大赢。

---

### #18 Pfizer (2020) ⭐

**公开判断时点**：2020年 | **数据源**：Pfizer FY2019 10-K + Pfizer Q3 2020 10-Q + Berkshire 2020-09-30 / 2021-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 2017-2019 平均 ROE 约 `24.4%`
- `2020Q3` 的 trailing 12 months `FCF / NI` 约 `1.20x`，现金流表面上并不差
- 负债也没有失控，按 `2020Q3` 净债务 / `2019 EBITDA` 代理口径估算约 `2.1x`
- 真正卡住它的是 `g6 + g7`
- 按 Berkshire 披露的小仓位反推的价格和 `2020Q3` 资产负债表估算，earnings yield 只有约 `3.4%`
- 更重要的是，Pfizer 在当时依然是一个需要不断靠研发、BD 和产品组合更新去维持盈利的平台型药企，而不是一个十年后一眼还能讲清“别人为什么复制不了”的 Buffett 式 tollbooth

**结论**：不投

**为什么框架可能更合理**：
- 这笔仓位从一开始就很小，明显不像 Berkshire 在下一个 American Express 或 Coca-Cola 上重仓
- 即使承认 Pfizer 是全球顶级医药公司之一，它在 2020 年更像一笔 tactical pharma basket 配置，而不是一个高确定性长期核心 franchise
- Oracle 在这里保持保守，等于拒绝把“有钱赚的大药企”直接等同于“值得长期 underwriting 的 Buffett 式资产”

**实际结果**：Berkshire 在 `2020-09-30` 披露持有 `3,711,780` 股 Pfizer、价值约 `$136.2M`，但到 `2021-12-31` 的 13F 已经不再出现这笔持仓。Pfizer 后续当然受益于疫情期间的特殊环境，但从 Berkshire 的持仓行为看，这更像短期组合动作，而不是长期核心押注。

---

### #19 Barrick Gold (2020) ⭐

**公开判断时点**：2020年 | **数据源**：Barrick Gold FY2019 Form 40-F + Barrick Gold Q3 2020 6-K / Exhibit 99.2 + Berkshire 2020-09-30 / 2020-12-31 / 2021-03-31 13F-HR

**为什么当前框架会给 PASS**：
- `2017-2019` 平均 ROE 只有约 `6.3%`，因为 2018 年的巨额亏损把三年均值明显拉低
- 按 `2020Q3` 的 trailing 12 months 口径，`FCF / NI` 约 `0.74x`，没有过 `0.8x` 的硬门槛
- 资产负债表其实很强，按 `2020Q3` 净债务 / `9M 2020 adjusted EBITDA` 代理口径估算只有约 `0.08x`
- 估值也不算离谱，earnings yield 大约 `7.2%`
- 真正让它仍然过不了的是 `g1 + g2 + g7`：这门生意的回报和现金流仍然高度依赖金价与矿山资产周期，而不是一个可以十年清晰复述的结构性护城河

**结论**：不投

**为什么框架可能更合理**：
- Barrick 在 2020 年确实是“修复后更漂亮”的矿业公司，但更漂亮不等于变成 Buffett Oracle 想长期 underwriting 的 franchise
- 这个框架在 commodity names 上本来就故意严格，因为它要回避的是“看起来便宜而且正在好转”的周期资产被误判成长期复利机
- Berkshire 后续的交易轨迹也支持这一点：这不是重仓长期押注，而更像一次很快就撤掉的战术仓位

**实际结果**：Berkshire 在 `2020-09-30` 披露持有 `12,000,000` 股 Barrick Gold、价值约 `$337.3M`，但这笔持仓在 `2020-12-31` 的 13F 已经消失。它并没有演变成 Berkshire 的长期矿业平台。

---

### #20 Amazon.com (2020) ⭐

**公开判断时点**：2020年末可见 Berkshire 持仓 | **数据源**：Amazon FY2019 10-K + Berkshire 2020-12-31 / 2021-12-31 / 2022-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 2017-2019 平均 ROE 约 `17.6%`
- 生意质量毋庸置疑，moat 也明确能过
- 真正卡住它的是 `g2 + g6`
- 2019 年 `FCF / NI` 约 `0.73x`，看起来还没达到框架要求的现金转化
- 按 2020 年底 Berkshire 披露仓位反推价格，earnings yield 只有约 `0.7%`
- 也就是说，Oracle 会承认 Amazon 是世界级平台，但仍会说“太贵了”

**结论**：不投

**为什么框架可能更合理**：
- Berkshire 的仓位并不小，但也始终没有被升级成真正的 top-tier Buffett 核心
- 这是好生意明显好过好价格的案例
- Oracle 在这里更像是在坚持 margin-of-safety，而不是否定 business quality

**实际结果**：Berkshire 在 `2020-12-31` 披露持有 `419,500` 股 Amazon、价值约 `$1.37B`；到 `2022-12-31` 仍持有经拆股调整后的 `8,390,000` 股，但这始终不是组合里的 defining core position。

---

### #21 Biogen (2020) ⭐

**公开判断时点**：2020年末可见 Berkshire 持仓 | **数据源**：Biogen FY2019 10-K + Berkshire 2020-12-31 / 2021-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 2017-2019 平均 ROE 约 `33.2%`
- `FCF / NI` 约 `1.12x`
- 负债也不重，净债务 / EBITDA 约 `0.85x`
- 但 gate ⑦ 过不了：Biogen 仍然是典型需要靠管线和专利续命的 biotech 平台
- 这类公司可以非常赚钱，却不够像 Buffett Oracle 想长期 underwriting 的 tollbooth

**结论**：不投

**为什么框架可能更合理**：
- Buffett/伯克希尔这笔仓位本来就不大
- 如果公司真是高确定性 decade-long franchise，通常不会这么快从披露列表里消失
- Oracle 在这里更像是在回避“财务不错但 moat 不够干净”的 biotech 组合体

**实际结果**：Berkshire 在 `2020-12-31` 披露持有 `643,022` 股 Biogen、价值约 `$157.5M`；到 `2021-12-31` 13F 已经不再出现这笔持仓。

---

### #22 Charter Communications (2020) ⭐

**公开判断时点**：2020年末可见 Berkshire 持仓 | **数据源**：Charter FY2019 10-K + Berkshire 2020-12-31 / 2021-12-31 / 2022-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 宽带业务确实有 local monopoly / duopoly 特征，moat 可以讲得清楚
- 但 `g1` 没过，2017-2019 平均 ROE 只有约 `9.9%`
- `g3` 也没过，净负债 / EBITDA 约 `6.3x`
- 再加上 `g6` 只有约 `0.8%` 的 earnings yield，价格和资本结构都太绷

**结论**：不投

**为什么框架可能更合理**：
- Charter 是好资产，但不是便宜资产
- 2020 年底这个价位更像市场把未来多年 broadband economics 都提前贴现了
- Oracle 在这里不是看不懂 moat，而是在说：太贵、太 levered

**实际结果**：Berkshire 在 `2020-12-31` 披露持有 `5,213,461` 股 Charter、价值约 `$3.45B`；到 `2022-12-31` 仍持有 `3,828,941` 股，但市值明显低于 2020 年底水平，这不是一笔干净的 Buffett-style compounding win。

---

### #23 Kroger (2020) ⭐

**公开判断时点**：2020年末可见 Berkshire 持仓 | **数据源**：Kroger FY2020 10-K + Berkshire 2020-12-31 / 2021-12-31 / 2022-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 财务上它其实很干净：ROE、现金流和杠杆都过关
- 真正卡住它的是 `g6 + g7`
- 按 2020 年末价格算，earnings yield 约 `4.4%`
- 更关键的是，Kroger 虽然是好 operator，但 grocery 并不是一个十年一眼能讲清的 irreplicable moat

**结论**：不投

**为什么框架可能更合理**：
- Berkshire 后来确实加了很多 Kroger，但这更像 defensive retail / inflation basket 里的成功仓位
- 它不是 Coca-Cola、American Express 或 Moody's 那种 franchise purity
- Oracle 在这里保持保守，是在区分“好执行的零售商”和“Buffett 式 tollbooth”

**实际结果**：Berkshire 在 `2020-12-31` 披露持有 `3,900,000` 股 Kroger、价值约 `$123.9M`；到 `2021-12-31` 增到 `28,020,000` 股，`2022-12-31` 仍持有 `16,607,090` 股。这是一笔有效的防御型仓位，但不是定义性的 moat 胜利。

---

### #24 Marsh & McLennan (2020) ⭐

**公开判断时点**：2020年末可见 Berkshire 持仓 | **数据源**：Marsh & McLennan FY2019 10-K + Berkshire 2020-12-31 / 2021-03-31 / 2021-12-31 / 2022-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 2017-2019 平均 ROE 约 `21.6%`
- `FCF / NI` 约 `1.09x`
- 客户黏性和全球风险管理关系也是真实 moat
- 但按 2020 年底价格算，earnings yield 只有约 `2.5%`
- 所以 Oracle 会给出一个典型的“伟大服务 franchise，但价格太贵”的 PASS

**结论**：不投

**为什么框架可能更合理**：
- 这笔仓位虽然 2021Q1 还加过，但很快就被砍到 token size
- 如果 Berkshire 自己都没有把它变成长期核心，那 Oracle 保持 valuation discipline 是说得通的
- 这条主要是提醒我们：好公司和好价格不是一回事

**实际结果**：Berkshire 在 `2020-12-31` 披露持有 `4,267,825` 股 Marsh、价值约 `$499.3M`；`2021-03-31` 增到 `5,287,526` 股，但到 `2021-12-31` 已缩到 `404,911` 股，并在 `2022-12-31` 仍保持这个极小仓位。

---

### #25 Mastercard (2020) ❌

**公开判断时点**：2020年末可见 Berkshire 持仓 | **数据源**：Mastercard FY2019 10-K + Berkshire 2020-12-31 / 2021-12-31 / 2022-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 经营质量极高，支付网络 moat 当然成立
- `FCF / NI` 约 `0.96x`，杠杆几乎没有
- 真正卡住它的只有 `g6`：按 2020 年末价格估算，earnings yield 只有约 `2.2%`
- Oracle 会因此把它归类为“顶级 business，但价格不合格”

**结论**：不投

**为什么会错**：
- 这类全球支付网络本身就是 Buffett/Berkshire 非常愿意长期拿的资产类型
- Berkshire 到 `2022-12-31` 仍然持有接近 `399万` 股 Mastercard
- 这说明当前 `g6` 对超级网络型 franchise 仍然太钝，容易把真正 exceptional business 全部一刀切掉

**实际结果**：Berkshire 在 `2020-12-31` 披露持有 `4,564,756` 股 Mastercard、价值约 `$1.63B`；到 `2021-12-31` 和 `2022-12-31` 仍各持有 `3,986,648` 股。它明显不是短线仓位。

---

### #26 Mondelez International (2020) ⭐

**公开判断时点**：2020年末可见 Berkshire 持仓 | **数据源**：Mondelez FY2019 10-K + Berkshire 2020-12-31 / 2021-12-31 / 2022-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 2017-2019 平均 ROE 约 `12.8%`
- snack brand moat 也可以成立
- 但 `FCF / NI` 只有约 `0.78x`
- 按 2020 年末价格算，earnings yield 也只有约 `3.8%`
- 于是它会变成一条标准的“成熟好公司，但回报起点不够高”的 PASS

**结论**：不投

**为什么框架可能更合理**：
- Berkshire 自己也只持有极小仓位
- 这更像 legacy/observer position，而不是 high-conviction underwriting
- Oracle 在这里不是说 Mondelez 差，而是说“没便宜到值得按 Buffett 核心仓标准出手”

**实际结果**：Berkshire 在 `2020-12-31` 披露持有 `578,000` 股 Mondelez、价值约 `$33.8M`，并在 `2021-12-31` 和 `2022-12-31` 继续持有同样数量。

---

### #27 Procter & Gamble (2020) ⭐

**公开判断时点**：2020年末可见 Berkshire 持仓 | **数据源**：P&G FY2020 10-K + Berkshire 2020-12-31 / 2021-12-31 / 2022-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 财务指标漂亮：ROE、FCF / NI、杠杆、收入趋势、毛利率都过
- 真正的问题还是 `g6`
- 按 2020 年末价格估算，earnings yield 只有约 `3.6%`
- 也就是说，Oracle 会承认这是世界级 consumer franchise，但仍然不会说“这价钱够便宜”

**结论**：不投

**为什么框架可能更合理**：
- Berkshire 留下的是一个极小的 legacy stake，不像在做新的高确信重仓
- 这更像对 franchise quality 的认可，而不是对 future return 的强背书
- Oracle 在这里强调的仍是同一句话：quality 不等于 margin of safety

**实际结果**：Berkshire 在 `2020-12-31` 披露持有 `315,400` 股 P&G、价值约 `$43.9M`，并在 `2021-12-31` 和 `2022-12-31` 都保持这个极小仓位。

---

### #28 RH (2020) ❌

**公开判断时点**：2020年末可见 Berkshire 持仓 | **数据源**：RH FY2020 10-K + Berkshire 2020-12-31 / 2021-12-31 / 2022-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 经营数据其实不差：ROIC proxy 很高，现金流和负债也都过关
- 收入和毛利率到 2020 年都在走强
- 真正卡住它的是 `g6 + g7`
- 按 2020 年末价格算，earnings yield 只有约 `2.3%`
- 更关键的是，Oracle 不愿意把 luxury furnishings retailer 直接认定成十年后仍不可复制的 Buffett moat

**结论**：不投

**为什么会错**：
- Berkshire 后来不仅没退出，反而继续加仓
- 这说明当前 moat test 对某些 founder-led specialty retail 模式仍然偏严
- RH 不是传统快消品牌，也不是普通家具零售商，这种“设计系统 + 客户群 + price architecture”的 moat 现在还没被框架吃透

**实际结果**：Berkshire 在 `2020-12-31` 披露持有 `787,469` 股 RH、价值约 `$352.4M`；到 `2021-12-31` 增到 `871,468` 股，`2022-12-31` 又增到 `1,163,000` 股。

---

### #29 Verizon Communications (2020) ⭐

**公开判断时点**：2020年末可见 Berkshire 持仓 | **数据源**：Verizon FY2019 10-K + Berkshire 2020-12-31 / 2021-03-31 / 2021-12-31 / 2022-12-31 13F-HR

**为什么当前框架会给 PASS**：
- 2017-2019 平均 ROE 约 `43.1%`
- `FCF / NI` 约 `0.99x`
- 杠杆也没有失控，净负债 / EBITDA 约 `2.4x`
- 真正卡住它的是 `g6 + g7`
- 按 2020 年末价格估算，earnings yield 只有约 `5.5%`，略低于框架红线
- 更重要的是，telecom 虽然有 spectrum 和规模，但很难算成 Buffett 最爱的 pristine tollbooth

**结论**：不投

**为什么框架可能更合理**：
- 这笔仓位很大，但最终并没有长期留下来
- Oracle 在这里坚持的是：成熟 telecom 的可见性不错，但 franchise purity 不够
- 后来的退出轨迹说明，这更像大额但非永久的 defensive allocation

**实际结果**：Berkshire 在 `2020-12-31` 披露持有 `146,716,496` 股 Verizon、价值约 `$8.62B`；到 `2021-03-31` 增到 `158,824,575` 股，`2021-12-31` 仍保持该数量，但到 `2022-12-31` 已不再出现。
