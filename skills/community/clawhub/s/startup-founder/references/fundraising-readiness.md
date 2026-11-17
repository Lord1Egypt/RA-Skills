# 融资准备清单 playbook

> 融资是放大器不是救命稻草。本 playbook 给融资前的就绪检查、Pitch Deck 结构与交割注意点。

## 1. 融资前就绪检查（先有 traction）

```
□ 产品已上线且有真实用户
□ 关键指标有增长曲线（MRR/活跃/留存）
□ 单位经济模型算得清（CAC/LTV/回收期）
□ 知道要融多少、花在哪、撑多久
□ 创始人全职投入（投资人看投入度）
```

**铁律**：没有 traction 就密集见投资人，只会消耗关系且拿不到 term。

## 1.1 量化门槛分档（把"有 traction"变成可算的数）

第 1 节五项是定性闸门，过了之后用下表自评——**投资人会用这几个数反推你的业务质量**，
你自己先算一遍，比在会上被问住好。分档取自 SaaS/订阅业务通行基准：

| 指标 | 优秀 | 合格 | 预警 | 怎么算 |
|------|------|------|------|--------|
| LTV : CAC | > 5x | > 3x | < 2x | `(ARPU × 毛利率) ÷ 月流失率 ÷ CAC` |
| CAC 回收期 | < 12 月 | < 18 月 | > 24 月 | `CAC ÷ (ARPU × 毛利率)` |
| 净收入留存 NDR | > 120% | > 110% | < 100% | 期末 ARR（含扩张，不含新客）÷ 期初 ARR |
| 毛留存 | > 95% | > 90% | < 85% | 期末 ARR（不含扩张）÷ 期初 ARR |
| Burn Multiple | < 1x | < 2x | > 3x | 净烧钱 ÷ 同期净新增 ARR |
| Magic Number | > 1.0x | > 0.75x | < 0.5x | 净新增 ARR ÷ 上期销售市场费用 |
| Rule of 40 | > 40 | 40 附近 | < 20 | 年增速(%) + 利润率(%) |

**独立开发者/小团队适配**（本库定位）：MRR < $10K 时样本太小，NDR / Rule of 40 / Magic Number
会剧烈失真，**只看三个**——CAC 回收期、毛留存、Burn Multiple。指标算不出来不是"暂时缺数据"，
而是**还不到融资时点**的信号。

**预警项处置**：任一指标落进预警列 → 不进第 2 节做 Deck，先回 [skills/founder-sales/](../skills/founder-sales/SKILL.md) 或
[skills/mvp-builder/](../skills/mvp-builder/SKILL.md) 把该指标拉回合格区，再重排会议。带着预警数字去见投资人 =
自己给自己制造一轮永久的"曾被拒记录"。

## 1.2 就绪速算（可直接运行）

```bash
# 客户经济：LTV / LTV:CAC / CAC 回收期（改前四个数即可）
python3 -c "
arpu=49; gm=0.85; churn=0.04; cac=180
ltv=arpu*gm/churn
print(f'LTV={ltv:.0f}  LTV/CAC={ltv/cac:.1f}x  CAC回收期={cac/(arpu*gm):.1f} 月')
"
# → LTV=1041  LTV/CAC=5.8x  CAC回收期=4.3 月

# 资金面：Runway 与 Burn Multiple（cash 现金 / net_burn 月净烧 / d_arr 当月净新增 ARR）
python3 -c "
cash=120000; net_burn=15000; d_arr=8000
print(f'Runway={cash/net_burn:.1f} 月  BurnMultiple={net_burn/d_arr:.1f}x')
"
# → Runway=8.0 月  BurnMultiple=1.9x
```

**Runway 决策线**：> 12 月 → 可以从容挑投资人；6–12 月 → 正常启动融资窗口；
< 6 月 → 议价权已经没了，优先砍成本/做收入而不是继续排会。**别在 Runway < 3 月时才开始融资**，
一轮从首次会面到打款通常 3–6 个月。

## 2. Pitch Deck 核心结构（12-15 页）

```
1. 一句话定位      2. 痛点        3. 解决方案
4. 为什么是现在    5. 市场空间    6. 产品演示
7. 商业模式        8.  traction   9. 竞争格局
10. 团队           11. 融资额与用途 12. 结尾 CTA
```

- traction 页要放真实曲线，不是"即将爆发"。
- 为什么是现在：技术/监管/习惯的时机窗口。

## 3. 见投资人节奏

- 先 warm intro，再 cold；投资人时间稀缺，开场 30 秒讲清价值。
- 每次会议后要明确 next step（跟进数据/引荐）。
- 维护投资人关系表（阶段/兴趣度/反馈），别只见不跟。

## 4. 交割注意点

- term sheet 看估值更看条款（清算优先、反稀释、董事会）。
- 法律尽调提前整理（股权、IP、合同）。
- 多家并行推进，制造轻微竞争，但别造假。

## 5. 常见坑

- **过早融资**：没 traction 硬推，关系耗尽且估值低。
- **只讲功能**：投资人不买功能，买增长与护城河。
- **忽视条款**：拿了高估值但苛刻条款，后续被动。
- **数据注水**：traction 经不起尽调，信誉破产。
- **用 NDR 盖住毛流失**：扩张收入把 NDR 顶到 100% 以上，毛留存其实只有 80%。
  两个数必须同时给，只报 NDR 一定会在尽调被拆穿。
- **只给聚合数字**：客户级明细一被要求就拿不出来。聚合指标能藏问题（少数大客户撑起全部增长），
  提前按客户/按 cohort 整理好，比被追问三轮更省信誉。
- **把服务收入算进 ARR**：一次性实施/咨询收入不是 recurring，毛利率也低，
  混进 ARR 会在尽调被剔除，估值直接缩水。

## 5.1 轮次门槛速查（经验区间，随市场松紧波动）

| 轮次 | traction 基准 | 指标重点 | 典型错配 |
|------|--------------|----------|----------|
| Pre-seed | 有可用产品 + 少量真实付费/深度访谈证据 | 问题真实性、创始人投入度 | 拿 Seed 的指标要求自我否定，迟迟不启动 |
| Seed | MRR 有连续 3–6 个月增长曲线 | 增长斜率、CAC 回收期 | 只有注册数没有留存，靠"用户量"讲故事 |
| A 轮 | 可重复的获客渠道 + 单位经济成立 | LTV:CAC、NDR、Magic Number | 渠道靠创始人单点人力，不可复制 |

**用法**：先定位自己在哪一轮，再回第 1.1 节只看该轮"指标重点"那两项，
其余指标不足不构成阻塞。跨轮硬套指标是本节最常见的误用。

## 6. 相关子技能与层次边界

本 playbook 只给**融资时机判断与就绪门槛**（L2 方法论）；Deck 逐页怎么写、投资人怎么跟、条款怎么谈，交给下列子技能（L3 落地）：

| 落地需求 | 调用子技能 |
|----------|-----------|
| Bootstrapping vs VC 决策、Deck 打磨、交割全流程 | [`skills/fundraising-guide/SKILL.md`](../skills/fundraising-guide/SKILL.md) |
| 用创始人身份换取早期成交，把 traction 做实 | [`skills/founder-sales/SKILL.md`](../skills/founder-sales/SKILL.md) |
| traction 不足时回到产品侧补最小可信增长 | [`skills/mvp-builder/SKILL.md`](../skills/mvp-builder/SKILL.md) |

**层次边界**：本文回答「现在该不该融、够不够格融」；子技能回答「Deck 每页写什么、会议后怎么推进」。第 1 节就绪检查未过 → 不进 [skills/fundraising-guide/](../skills/fundraising-guide/SKILL.md)，先回 [skills/founder-sales/](../skills/founder-sales/SKILL.md) 或 [skills/mvp-builder/](../skills/mvp-builder/SKILL.md) 补 traction；第 4 节交割条款细节在 [skills/fundraising-guide/](../skills/fundraising-guide/SKILL.md) 展开。第 1.1/1.2 节的量化门槛与速算**只在本层**维护——子技能不重复基准数字，需要判档时回读本文，避免两处基准漂移。

**兄弟 playbook**：融资前若方向本身未被验证 → 回 [references/validation-methodology.md](validation-methodology.md) 重走三问。
