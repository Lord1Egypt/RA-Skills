# Google 广告账户诊断与审计指南

> 所属 skill: siluzan-tso
> 适用场景: 账户健康检查、定期审计、接手新账户、效果下滑排查

---

## 1. 审计总览与流程

### 三层审计框架

| 层级            | 审计对象                       | 核心命令                                                      | 关注指标                                                     |
| --------------- | ------------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------ |
| 账户层          | 整体健康度、转化追踪、预算分配 | `overview`, `gold-account`, `ads-index`, `conversion-actions` | spend, conversions, costPerConversion, searchImpressionShare |
| 广告系列层      | 结构合理性、出价策略、预算效率 | `campaigns`, `geographic`, `devices`, `daily-metrics`         | searchBudgetLostImpressionShare, conversionRate, averageCpc  |
| 广告组/关键词层 | 关键词健康、创意质量、落地页   | `keywords`, `search-terms`, `ads`, `final-urls`, `extensions` | qualityScore, ctr, costPerConversion                         |

### 效果下滑决策树

```
账户效果下滑
├─ 转化量下降？
│  ├─ 点击量也下降？
│  │  ├─ 展示次数下降 → 运行 `campaigns` 检查 searchImpressionShare → 转第11章
│  │  └─ 展示次数正常 → 运行 `ads` + `keywords` 检查 CTR → 转第7章
│  └─ 点击量正常？
│     ├─ 转化率下降 → 运行 `final-urls` 检查落地页 → 转第9章
│     └─ 转化追踪异常 → 运行 `conversion-actions` → 转第4章
├─ CPA 飙升？
│  ├─ CPC 上升 → 运行 `keywords` 检查 qualityScore → 转第6章
│  ├─ 转化率下降 → 运行 `final-urls` → 转第9章
│  └─ 出价策略学习中 → 运行 `campaigns` 检查出价状态 → 转第5章
└─ 花费异常？
   ├─ 花不出去 → 运行 `campaigns` 检查 searchBudgetLostImpressionShare → 转第10章
   └─ 花费激增 → 运行 `search-terms` 检查是否匹配到不相关词 → 转第6章
```

### 审计优先级原则

1. **先查转化追踪** — 数据不准，一切分析都无意义
2. **再查账户结构** — 结构混乱会掩盖真实问题
3. **后查执行细节** — 关键词、创意、出价等

## 2. 快速健康检查（5分钟诊断）

### 执行命令

```bash
siluzan-tso google-analysis -a <CID> --sections gold-account
siluzan-tso google-analysis -a <CID> --sections overview
siluzan-tso google-analysis -a <CID> --sections ads-index
```

### 健康指标阈值表

| 指标             | 绿色（健康） | 黄色（关注） | 红色（立即处理） |
| ---------------- | ------------ | ------------ | ---------------- |
| CTR（搜索）      | > 5%         | 3%-5%        | < 3%             |
| 转化率           | > 5%         | 2%-5%        | < 2%             |
| 质量得分均值     | >= 7         | 5-6          | < 5              |
| 搜索展示份额     | > 70%        | 40%-70%      | < 40%            |
| 预算损失展示份额 | < 5%         | 5%-20%       | > 20%            |
| 排名损失展示份额 | < 15%        | 15%-30%      | > 30%            |
| CPA vs 目标      | <= 1x 目标   | 1x-1.5x 目标 | > 1.5x 目标      |
| 无效点击率       | < 5%         | 5%-10%       | > 10%            |
| 广告强度         | 优秀/良好    | 一般         | 差               |
| 扩展覆盖率       | 全部广告系列 | > 50%系列    | < 50%系列        |

### 快速诊断流程

1. 运行 `gold-account`：获取账户综合评分，标记低分项
2. 运行 `overview`：确认花费趋势、转化量趋势是否正常
3. 运行 `ads-index`：检查广告质量分布，识别拖后腿的广告
4. 对照上表标记红/黄/绿状态，红色项优先进入对应章节深入排查

## 3. 账户结构审计

### 执行命令

```bash
siluzan-tso ad campaigns -a <CID> --json-out ./snap
siluzan-tso ad groups -a <CID> --json-out ./snap
siluzan-tso google-analysis -a <CID> --sections campaigns
```

### 结构合理性判断矩阵

| 月预算范围       | 建议最大广告系列数 | 建议每系列最大广告组数 | 理由                       |
| ---------------- | ------------------ | ---------------------- | -------------------------- |
| < ¥5,000         | 2-3                | 3-5                    | 预算有限，需集中火力       |
| ¥5,000-¥20,000   | 3-5                | 5-8                    | 适度细分，保证每系列有数据 |
| ¥20,000-¥100,000 | 5-10               | 5-10                   | 可按产品线/地域拆分        |
| > ¥100,000       | 10-20              | 按需                   | 充分细分，但仍需避免碎片化 |

### Smart Bidding 数据量要求

- **核心规则：每个广告系列需 30+ 转化/月** 才能让智能出价有效学习
- 转化量不足时的合并策略：
  1. 运行 `campaigns` 获取每个系列的月转化量
  2. 月转化 < 15 的系列：**必须合并**或切换为手动出价
  3. 月转化 15-30 的系列：**建议合并**到相似系列，或使用组合出价策略
  4. 如无法合并，考虑使用微转化（如加入购物车）作为出价信号

### 结构问题清单

| 检查项             | 判定标准                         | 处理方式          |
| ------------------ | -------------------------------- | ----------------- |
| 广告系列过多       | 活跃系列 > 预算建议值的 2 倍     | 合并同类系列      |
| 空广告组           | 广告组内无活跃关键词或无活跃广告 | 暂停或填充        |
| 单关键词广告组过多 | SKAG 占比 > 50%                  | 按主题合并为 STAG |
| 广告组主题混乱     | 同组关键词缺乏语义相关性         | 重新归类          |
| 重复关键词跨组     | 同一关键词出现在多个广告组       | 去重，保留最优组  |

## 4. 转化追踪审计

### 执行命令

```bash
siluzan-tso google-analysis -a <CID> --sections conversion-actions
siluzan-tso google-analysis -a <CID> --sections overview
```

### 审计要点

#### 4.1 主要转化操作检查

| 检查项           | 正常状态                         | 异常信号                       |
| ---------------- | -------------------------------- | ------------------------------ |
| 主要转化操作数量 | 1-3 个核心业务目标               | > 5 个设为主要 = 可能重复计数  |
| 转化操作类型     | 与业务目标一致（购买/询盘/注册） | 微转化（页面浏览）被设为主要   |
| 转化统计方式     | 购买类用"每次"，询盘类用"一次"   | 询盘类用"每次" = 重复计数      |
| 转化窗口         | 与销售周期匹配（通常 30 天）     | 窗口过短导致低估，过长导致高估 |

#### 4.2 重复计数检测

1. 从 `conversion-actions` 获取所有转化操作列表
2. 检查是否存在多个追踪同一行为的转化操作（例如：Google Tag + GTM 同时追踪购买）
3. **判定标准：** 同一类别转化操作 > 1 个且都设为主要 = 高概率重复计数
4. **修复：** 仅保留一个为主要，其余设为次要

#### 4.3 转化延迟分析

- 运行 `daily-metrics` 查看最近 7 天转化数据
- 最近 1-3 天转化数显著低于往常 → 可能是正常转化延迟，非真实下降
- **规则：** 转化窗口为 30 天时，至少等待 7 天再判断转化趋势

#### 4.4 增强型转化检查

- 在 `conversion-actions` 中确认增强型转化是否已启用
- 未启用 → 建议开启以提升转化归因准确度
- 启用后观察转化量是否有 5%-15% 的提升（正常范围）

## 5. 出价策略审计

### 执行命令

```bash
siluzan-tso ad campaigns -a <CID> --json-out ./snap
siluzan-tso google-analysis -a <CID> --sections campaigns
siluzan-tso google-analysis -a <CID> --sections daily-metrics
```

### 出价策略选择矩阵

| 月转化量 | 推荐出价策略               | 不推荐策略       | 原因                         |
| -------- | -------------------------- | ---------------- | ---------------------------- |
| 0-15     | 手动CPC / 尽可能多的点击   | tCPA, tROAS      | 数据不足，无法学习           |
| 15-30    | 尽可能多的转化（不设目标） | tCPA（严格目标） | 数据勉强够，不宜限制过死     |
| 30-50    | tCPA（宽松目标，+20%）     | tROAS            | 可开始用目标，但需留余量     |
| 50+      | tCPA / tROAS               | 手动CPC          | 数据充足，应充分利用智能出价 |

### 常见出价策略问题

| 问题               | 检测方式                             | 判定标准                     | 处理建议                            |
| ------------------ | ------------------------------------ | ---------------------------- | ----------------------------------- |
| 策略与转化量不匹配 | 对比系列月转化量与上表               | 使用 tCPA 但月转化 < 15      | 切换到手动CPC或尽可能多的转化       |
| tCPA 目标过低      | 对比实际 CPA 与目标 CPA              | 目标 < 实际 CPA 的 70%       | 提高目标至实际 CPA 的 90%           |
| tCPA 目标过高      | 对比实际 CPA 与目标 CPA              | 目标 > 实际 CPA 的 150%      | 逐步下调（每次不超过 20%）          |
| 学习期受干扰       | 检查 `daily-metrics` 波动            | 7 天内修改出价/预算超过 1 次 | 停止调整，等待学习期结束（通常7天） |
| 预算限制出价       | 检查 searchBudgetLostImpressionShare | > 20%                        | 提高预算或降低出价目标              |

### 学习期管理

- **学习期时长：** 通常 7 天或累计 50 次转化
- **学习期内禁止：** 修改出价目标、大幅调整预算（>20%）、暂停/启用广告系列
- **学习期检测：** 运行 `daily-metrics`，若过去 7 天 CPA 波动 > 50% 且系列近期有调整 → 可能处于学习期

## 6. 关键词健康审计

### 执行命令

```bash
siluzan-tso google-analysis -a <CID> --sections keywords
siluzan-tso google-analysis -a <CID> --sections search-terms
siluzan-tso ad keywords -a <CID> --json-out ./snap
siluzan-tso ad search-terms -a <CID>
```

### 6.1 质量得分分布分析

从 `keywords` 获取 qualityScore 数据：

| 质量得分区间 | 健康占比        | 处理措施                                 |
| ------------ | --------------- | ---------------------------------------- |
| 8-10         | 应 > 30%        | 维持，可适当提高出价获取更多流量         |
| 5-7          | 应占主体 50-60% | 优化广告相关性和落地页体验               |
| 1-4          | 应 < 10%        | 立即优化或暂停；QS ≤ 3 且花费 > 0 = 浪费 |
| 无评分       | —               | 新词或低展示量词，暂不处理               |

### 6.2 浪费花费识别

从 `keywords` 按 spend 降序排列，筛选高花费 + 零转化关键词：

| 条件                                    | 操作                         |
| --------------------------------------- | ---------------------------- |
| spend > 平均 CPA × 2 且 conversions = 0 | **暂停关键词**               |
| spend > 平均 CPA × 1 且 conversions = 0 | **降低出价或标记观察**       |
| CTR < 1% 且 impressions > 1000          | **优化广告文案相关性或暂停** |
| QS < 4 且 spend > 0                     | **优化落地页或暂停**         |

### 6.3 匹配类型审计

| 检查项       | 理想分布                   | 问题信号                            |
| ------------ | -------------------------- | ----------------------------------- |
| 广泛匹配占比 | < 30% 花费（搭配智能出价） | 广泛匹配花费 > 50% 且不使用智能出价 |
| 词组匹配占比 | 30-50%                     | —                                   |
| 完全匹配占比 | 20-40%                     | 完全匹配 < 10% = 缺乏精准流量       |

### 6.4 搜索词审计

从 `search-terms` 分析实际触发的搜索词：

1. **不相关搜索词：** 与业务无关的搜索词有花费 → 添加为否定关键词
2. **高转化搜索词：** 转化好但尚未作为关键词添加 → 添加为完全匹配关键词
3. **否定关键词覆盖率：** 不相关搜索词花费占总花费比例应 < 5%
4. **搜索词/关键词比率：** 每个关键词触发的搜索词变体过多（>20个） → 匹配过宽，需收紧或加否定词

## 7. 广告创意审计

### 执行命令

```bash
siluzan-tso google-analysis -a <CID> --sections ads
siluzan-tso google-analysis -a <CID> --sections ads-index
siluzan-tso google-analysis -a <CID> --sections extensions
siluzan-tso ad list -a <CID> --json-out ./snap
siluzan-tso ad extension list -a <CID>
```

### 7.1 广告强度分布

从 `ads-index` 获取广告强度（Ad Strength）分布：

| 广告强度 | 目标占比 | 处理                                           |
| -------- | -------- | ---------------------------------------------- |
| 优秀     | > 30%    | 保持                                           |
| 良好     | > 40%    | 可优化但非紧急                                 |
| 一般     | < 20%    | 添加更多标题/描述素材                          |
| 差       | 0%       | **必须立即优化** — 添加素材至 15 标题 + 4 描述 |

### 7.2 RSA 素材覆盖检查

从 `ad list --json-out ./snap` 检查每个 RSA 的素材数量：

| 素材类型         | 最低要求 | 推荐数量   | 不足时影响                   |
| ---------------- | -------- | ---------- | ---------------------------- |
| 标题             | 3        | 15（上限） | 广告强度降低，组合测试不充分 |
| 描述             | 2        | 4（上限）  | 同上                         |
| 包含关键词的标题 | >= 2     | 5+         | 相关性降低，QS 受影响        |
| 独特卖点标题     | >= 2     | 3+         | 差异化不足                   |
| CTA 标题         | >= 1     | 2+         | 缺乏行动号召                 |

### 7.3 广告组广告数量

| 每广告组 RSA 数量 | 状态 | 处理                         |
| ----------------- | ---- | ---------------------------- |
| 0                 | 红色 | 广告组无法投放，立即创建     |
| 1                 | 黄色 | 建议增至 2-3 个进行 A/B 测试 |
| 2-3               | 绿色 | 理想状态                     |
| > 3               | 黄色 | 数据分散，暂停表现最差的     |

### 7.4 扩展覆盖检查

从 `extensions` + `ad extension list` 检查：

| 扩展类型              | 是否必须   | 缺失影响                    |
| --------------------- | ---------- | --------------------------- |
| 站内链接（Sitelink）  | 必须       | 广告面积小，CTR 损失 10-15% |
| 摘要信息（Callout）   | 必须       | 缺少信任信号                |
| 结构化摘要（Snippet） | 推荐       | 缺少品类信息                |
| 电话（Call）          | 视业务而定 | 服务类必须，电商可选        |
| 图片（Image）         | 推荐       | 错失视觉吸引力              |
| 促销（Promotion）     | 季节性     | 有促销活动时必须添加        |

## 8. 地域与设备审计

### 执行命令

```bash
siluzan-tso google-analysis -a <CID> --sections geographic
siluzan-tso google-analysis -a <CID> --sections devices
siluzan-tso ad geo list -a <CID> --mode targeted
```

### 8.1 地域审计

#### 地域泄漏检测

1. 运行 `geographic` 获取实际展示地域数据
2. 运行 `ad geo list --mode targeted` 获取目标定向地域
3. **对比两者：** 是否有非目标地域产生花费？
4. 常见泄漏原因：定向模式为"在某地或对某地感兴趣的用户"（Presence or Interest）而非"在某地的用户"（Presence）

#### 地域性能分析

| 检查项             | 判定标准                     | 操作                     |
| ------------------ | ---------------------------- | ------------------------ |
| 地域 CPA 差异      | 某地域 CPA > 账户均值 2 倍   | 降低该地域出价调整或排除 |
| 零转化地域         | 花费 > 2x 目标 CPA 且 0 转化 | 排除该地域               |
| 高转化地域         | CPA < 账户均值 50%           | 提高出价调整 +10%-30%    |
| 不在目标市场的地域 | 有花费但不在业务覆盖范围     | 立即排除                 |

### 8.2 设备审计

从 `devices` 获取设备维度数据：

| 设备   | 检查指标                 | 常见问题            | 处理                                 |
| ------ | ------------------------ | ------------------- | ------------------------------------ |
| 移动端 | conversionRate vs 桌面端 | 移动端转化率低 50%+ | 检查移动落地页体验，考虑降低出价调整 |
| 桌面端 | CPA 对比                 | 通常 CPA 最优       | 如是，可提高出价调整                 |
| 平板   | 花费占比                 | 花费高但转化差      | 考虑设置 -100% 出价排除              |

#### 设备出价调整建议

```
调整幅度计算公式：
出价调整 = (设备转化率 / 账户平均转化率 - 1) × 100%

示例：
- 桌面端转化率 5%，账户均值 4% → 调整 +25%
- 移动端转化率 2%，账户均值 4% → 调整 -50%
```

> **注意：** 使用智能出价（tCPA/tROAS）时，设备出价调整会被出价策略覆盖，但仍建议设置 -100% 来排除表现极差的设备。

## 9. 落地页审计

### 执行命令

```bash
siluzan-tso google-analysis -a <CID> --sections final-urls
siluzan-tso google-analysis -a <CID> --sections devices
```

### 9.1 落地页性能分析

从 `final-urls` 获取各 URL 的 spend、clicks、conversions、conversionRate：

| 检查项             | 判定标准                               | 操作                              |
| ------------------ | -------------------------------------- | --------------------------------- |
| 高花费零转化 URL   | spend > 3x 目标 CPA 且 conversions = 0 | 暂停指向该 URL 的广告或更换落地页 |
| 转化率显著低于均值 | conversionRate < 账户均值 × 0.5        | 检查页面内容、加载速度、表单体验  |
| 转化率显著高于均值 | conversionRate > 账户均值 × 1.5        | 将更多流量引向该页面              |
| URL 过多           | 独立 URL > 20 个                       | 检查是否有无效/重复页面           |

### 9.2 移动端 vs 桌面端落地页

结合 `devices` 数据：

- 若移动端转化率 < 桌面端转化率的 50% → 落地页移动端体验可能有问题
- 常见移动端问题：表单字段过多、按钮太小、页面加载慢、弹窗遮挡
- 建议：单独为移动端设置优化过的落地页 URL

### 9.3 落地页与关键词相关性

- 同一落地页承接多个不同意图的关键词 → 相关性不足 → QS 下降
- **理想状态：** 每组高意图关键词对应一个专属落地页

## 10. 预算效率审计

### 执行命令

```bash
siluzan-tso google-analysis -a <CID> --sections campaigns
siluzan-tso google-analysis -a <CID> --sections daily-metrics
siluzan-tso ad campaigns -a <CID> --json-out ./snap
```

### 10.1 预算利用率分析

从 `campaigns` 获取 searchBudgetLostImpressionShare：

| 预算损失展示份额 | 状态                     | 操作                               |
| ---------------- | ------------------------ | ---------------------------------- |
| 0%               | 可能预算过高或关键词过少 | 检查是否有扩量空间                 |
| 1%-10%           | 理想状态                 | 维持，可微调                       |
| 10%-20%          | 黄色                     | 评估是否有增加预算的 ROI 空间      |
| 20%-50%          | 红色                     | 错失大量展示机会，优先加预算       |
| > 50%            | 严重                     | 预算严重不足，需大幅调整或收窄定向 |

### 10.2 预算分配合理性

1. 从 `campaigns` 获取每个系列的 spend、conversions、costPerConversion
2. 计算每个系列的 ROAS 或 CPA
3. 检查以下不合理分配：

| 问题                  | 检测方式                            | 处理                               |
| --------------------- | ----------------------------------- | ---------------------------------- |
| 高 CPA 系列获得高预算 | CPA 排名前 25% 但预算也在前 25%     | 降低预算，转移至低 CPA 系列        |
| 低 CPA 系列预算受限   | CPA 最优但 searchBudgetLostIS > 20% | 增加预算                           |
| 无转化系列持续花费    | 30 天 spend > 0 且 conversions = 0  | 暂停或重新诊断                     |
| 每日预算过低          | 日预算 < 目标 CPA × 2               | 提高日预算至少为目标 CPA 的 2-3 倍 |

### 10.3 花费趋势分析

运行 `daily-metrics` 检查：

- 花费突然下降 → 可能是预算耗尽、广告被拒、出价策略异常
- 花费突然上升 → 可能是新关键词触发或出价策略调整
- 周末/工作日花费差异大 → 考虑设置广告投放时间

## 11. 竞争态势分析

### 执行命令

```bash
siluzan-tso google-analysis -a <CID> --sections campaigns
siluzan-tso google-analysis -a <CID> --sections keywords
siluzan-tso google-analysis -a <CID> --sections dimension-summary
```

### 展示份额指标解读

| 指标                            | 含义                              | 取值范围 |
| ------------------------------- | --------------------------------- | -------- |
| searchImpressionShare           | 实际展示次数 / 有资格展示的总次数 | 0%-100%  |
| searchBudgetLostImpressionShare | 因预算不足损失的展示份额          | 0%-100%  |
| searchRankLostImpressionShare   | 因广告排名不足损失的展示份额      | 0%-100%  |

**核心公式：** searchImpressionShare + searchBudgetLostIS + searchRankLostIS ≈ 100%

### 竞争策略决策矩阵

| 预算损失IS | 排名损失IS | 诊断                   | 建议操作                             |
| ---------- | ---------- | ---------------------- | ------------------------------------ |
| 高 (>20%)  | 低 (<15%)  | 预算受限，但竞争力足   | 增加预算即可获取更多转化             |
| 低 (<10%)  | 高 (>30%)  | 预算充足，但竞争力不足 | 提高 QS（优化广告+落地页）或提高出价 |
| 高 (>20%)  | 高 (>20%)  | 预算和竞争力双重不足   | 优先提 QS（免费提升），再考虑加预算  |
| 低 (<10%)  | 低 (<15%)  | 展示份额已较高         | 维持现状或开拓新关键词               |

### 提升广告排名的优先级

1. **提高质量得分（免费）** — 优化广告相关性 → 优化落地页 → 提高预期 CTR
2. **增加扩展覆盖（免费）** — 确保所有扩展类型都已启用
3. **提高出价（付费）** — 在 ROI 允许的范围内提高出价
4. **增加预算（付费）** — 仅在预算损失IS > 20% 时

## 12. 审计报告模板

使用以下模板输出审计结果，按严重程度排序：

```markdown
# Google Ads 账户审计报告

- 账户 CID: <CID>
- 审计日期: <DATE>
- 审计周期: 过去 30 天

## 账户概要

| 指标         | 数值          | 趋势（vs 上期） |
| ------------ | ------------- | --------------- |
| 总花费       | ¥<SPEND>      | ↑/↓ <PERCENT>%  |
| 总转化       | <CONVERSIONS> | ↑/↓ <PERCENT>%  |
| 平均 CPA     | ¥<CPA>        | ↑/↓ <PERCENT>%  |
| 平均 CTR     | <CTR>%        | ↑/↓ <PERCENT>%  |
| 搜索展示份额 | <IS>%         | ↑/↓ <PERCENT>%  |

## 严重问题（Critical）

> 需立即处理，正在造成资金浪费或数据失真

### C1: <问题标题>

- **数据依据：** 运行 `<CLI命令>` 发现 <具体数据>
- **影响：** <对账户的具体影响>
- **建议操作：** <具体修复步骤>
- **预期效果：** <修复后预计改善>

## 警告问题（Warning）

> 需尽快处理，正在影响效果但非紧急

### W1: <问题标题>

- **数据依据：** 运行 `<CLI命令>` 发现 <具体数据>
- **影响：** <对账户的具体影响>
- **建议操作：** <具体修复步骤>

## 优化机会（Opportunity）

> 非问题，但有提升空间

### O1: <机会标题>

- **数据依据：** 运行 `<CLI命令>` 发现 <具体数据>
- **潜在收益：** <预估提升幅度>
- **建议操作：** <具体优化步骤>

## 正常项

- [x] 转化追踪正常，主要转化操作设置正确
- [x] 账户结构合理，系列数量与预算匹配
- [x] <其他正常项...>

## 下次审计建议

- 重点关注：<基于本次发现，下次需重点复查的项>
- 建议审计时间：<DATE>
```

## 13. 常见问题诊断速查表

| #   | 症状                   | 检查数据                                     | 可能原因                | 修复命令/操作                             |
| --- | ---------------------- | -------------------------------------------- | ----------------------- | ----------------------------------------- |
| 1   | CPA 突然飙升           | `campaigns` 查 costPerConversion 趋势        | 出价策略进入学习期      | `daily-metrics` 确认，等待 7 天或回退策略 |
| 2   | CPA 突然飙升           | `search-terms` 查新增搜索词                  | 触发不相关搜索词        | 添加否定关键词                            |
| 3   | CPA 突然飙升           | `keywords` 查 qualityScore 变化              | QS 下降导致 CPC 上升    | 优化广告相关性和落地页                    |
| 4   | CTR 持续下降           | `ads` 查广告强度和创意内容                   | 广告疲劳                | 更新广告素材，添加新标题/描述             |
| 5   | CTR 持续下降           | `campaigns` 查 searchImpressionShare         | 广告位置下降            | 检查出价竞争力和 QS                       |
| 6   | 展示量大幅下降         | `campaigns` 查 searchBudgetLostIS            | 预算耗尽                | 增加预算                                  |
| 7   | 展示量大幅下降         | `keywords` 查关键词状态                      | 关键词被暂停或否定      | `ad keywords --json-out ./snap` 检查状态  |
| 8   | 展示量大幅下降         | `campaigns` 查系列状态                       | 广告被拒或系列暂停      | `ad campaigns --json-out ./snap` 检查状态 |
| 9   | 转化量下降但点击正常   | `final-urls` 查转化率                        | 落地页问题（改版/故障） | 检查落地页是否可访问且正常                |
| 10  | 转化量下降但点击正常   | `conversion-actions` 查转化操作              | 转化追踪代码失效        | 检查 Google Tag 是否正常触发              |
| 11  | 预算花不出去           | `keywords` 查展示量和出价                    | 出价过低无竞争力        | 提高出价或切换出价策略                    |
| 12  | 预算花不出去           | `ad keywords --json-out ./snap` 查关键词数量 | 关键词太少或搜索量低    | 扩展关键词列表                            |
| 13  | QS 整体下降            | `keywords` 查 QS 分布                        | 落地页体验下降          | 检查落地页加载速度和内容相关性            |
| 14  | QS 整体下降            | `ads` 查广告相关性                           | 广告与关键词不匹配      | 重写广告，确保包含核心关键词              |
| 15  | 移动端效果差           | `devices` 查移动端 CPA                       | 移动落地页体验差        | 优化移动端页面或降低移动出价              |
| 16  | 某地域 CPA 极高        | `geographic` 查各地域 CPA                    | 地域定向过宽            | 排除低效地域或降低出价调整                |
| 17  | 搜索展示份额骤降       | `campaigns` 查 searchRankLostIS              | 竞争对手加大投放        | 提高 QS 和出价应对                        |
| 18  | 转化波动大（时高时低） | `daily-metrics` 查每日趋势                   | 转化延迟或追踪不稳定    | `conversion-actions` 确认追踪和归因窗口   |
| 19  | 花费突然激增           | `search-terms` 查新搜索词                    | 广泛匹配触发大量新词    | 添加否定关键词，收紧匹配类型              |
| 20  | 广告审核被拒           | `ad list --json-out ./snap` 查广告状态       | 广告违规政策            | 修改广告内容后重新提交                    |

## 14. CLI 审计命令序列

### 14.1 每周健康检查（5-10 分钟）

```bash
# 步骤 1: 快速健康评分
siluzan-tso google-analysis -a <CID> --sections gold-account

# 步骤 2: 账户概览，确认花费和转化趋势
siluzan-tso google-analysis -a <CID> --sections overview

# 步骤 3: 广告系列表现，检查异常系列
siluzan-tso google-analysis -a <CID> --sections campaigns

# 步骤 4: 每日趋势，发现近期波动
siluzan-tso google-analysis -a <CID> --sections daily-metrics

# 步骤 5: 搜索词，识别新出现的不相关搜索词
siluzan-tso google-analysis -a <CID> --sections search-terms
```

**检查重点：** 花费/转化趋势是否正常、有无新增不相关搜索词、系列是否有异常状态变更。

### 14.2 月度深度审计（30-60 分钟）

```bash
# ---- 第一阶段：全局数据采集 ----
siluzan-tso google-analysis -a <CID> --sections gold-account
siluzan-tso google-analysis -a <CID> --sections overview
siluzan-tso google-analysis -a <CID> --sections ads-index
siluzan-tso google-analysis -a <CID> --sections conversion-actions

# ---- 第二阶段：系列与结构 ----
siluzan-tso google-analysis -a <CID> --sections campaigns
siluzan-tso ad campaigns -a <CID> --json-out ./snap
siluzan-tso ad groups -a <CID> --json-out ./snap

# ---- 第三阶段：关键词与搜索词 ----
siluzan-tso google-analysis -a <CID> --sections keywords
siluzan-tso google-analysis -a <CID> --sections search-terms
siluzan-tso ad keywords -a <CID> --json-out ./snap

# ---- 第四阶段：创意与扩展 ----
siluzan-tso google-analysis -a <CID> --sections ads
siluzan-tso ad list -a <CID> --json-out ./snap
siluzan-tso google-analysis -a <CID> --sections extensions
siluzan-tso ad extension list -a <CID>

# ---- 第五阶段：维度分析 ----
siluzan-tso google-analysis -a <CID> --sections devices
siluzan-tso google-analysis -a <CID> --sections geographic
siluzan-tso google-analysis -a <CID> --sections final-urls
siluzan-tso google-analysis -a <CID> --sections audience
siluzan-tso google-analysis -a <CID> --sections dimension-summary
```

**审计流程：** 采集全部数据后，按第 1-11 章逐项检查，使用第 12 章模板输出报告。

### 14.3 新账户接手审计

```bash
# ---- 基础信息了解 ----
siluzan-tso google-analysis -a <CID> --sections overview
siluzan-tso google-analysis -a <CID> --sections gold-account

# ---- 转化追踪验证（最关键） ----
siluzan-tso google-analysis -a <CID> --sections conversion-actions

# ---- 账户结构梳理 ----
siluzan-tso ad campaigns -a <CID> --json-out ./snap
siluzan-tso ad groups -a <CID> --json-out ./snap
siluzan-tso ad keywords -a <CID> --json-out ./snap
siluzan-tso ad list -a <CID> --json-out ./snap

# ---- 效果基线建立 ----
siluzan-tso google-analysis -a <CID> --sections campaigns
siluzan-tso google-analysis -a <CID> --sections keywords
siluzan-tso google-analysis -a <CID> --sections daily-metrics

# ---- 全维度扫描 ----
siluzan-tso google-analysis -a <CID> --sections devices
siluzan-tso google-analysis -a <CID> --sections geographic
siluzan-tso ad geo list -a <CID> --mode targeted
siluzan-tso google-analysis -a <CID> --sections search-terms
siluzan-tso google-analysis -a <CID> --sections extensions
siluzan-tso google-analysis -a <CID> --sections final-urls
siluzan-tso google-analysis -a <CID> --sections ads-index
```

**接手要点：** 优先验证转化追踪准确性，建立 30 天效果基线，记录当前账户结构和策略作为参照。

### 14.4 效果下滑紧急排查

```bash
# ---- 步骤 1：确认下滑范围 ----
siluzan-tso google-analysis -a <CID> --sections overview
siluzan-tso google-analysis -a <CID> --sections daily-metrics

# ---- 步骤 2：排除追踪问题 ----
siluzan-tso google-analysis -a <CID> --sections conversion-actions

# ---- 步骤 3：定位问题系列 ----
siluzan-tso google-analysis -a <CID> --sections campaigns

# ---- 步骤 4：深入问题系列（根据步骤3结果选择性执行） ----
siluzan-tso google-analysis -a <CID> --sections keywords
siluzan-tso google-analysis -a <CID> --sections search-terms
siluzan-tso google-analysis -a <CID> --sections ads
siluzan-tso google-analysis -a <CID> --sections final-urls

# ---- 步骤 5：外部因素排查 ----
siluzan-tso google-analysis -a <CID> --sections devices
siluzan-tso google-analysis -a <CID> --sections geographic
siluzan-tso google-analysis -a <CID> --sections dimension-summary
```

**排查逻辑：** 先确认是真实下滑还是转化延迟/追踪问题（步骤1-2），再从系列层定位问题根源（步骤3），最后深入到关键词/创意/落地页层找到具体原因（步骤4-5）。参考第1章决策树选择排查路径。
