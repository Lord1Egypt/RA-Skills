# Google 广告系列结构与投放优化指南

> 所属 skill：`siluzan-tso`。
>
> 适用场景：设计广告系列架构（`ad campaign-create`）、调整出价策略（`ad campaign-edit`）、优化地域/设备投放、转化追踪配置、账户健康诊断。
> 关键词维度见 `references/google-ads-keyword-strategy.md` + `google-ads-keyword-optimization.md`；
> 创意维度见 `references/google-ads-creative-optimization.md`。

---

## 目录

- [一、广告系列类型选择](#一广告系列类型选择)
- [二、账户架构设计](#二账户架构设计)
- [三、出价策略优化](#三出价策略优化)
- [四、地域优化](#四地域优化)
- [五、设备优化](#五设备优化)
- [六、转化追踪配置](#六转化追踪配置)
- [七、预算优化](#七预算优化)
- [八、网络设置](#八网络设置)
- [九、广告系列实验](#九广告系列实验)
- [十、账户健康与优化得分](#十账户健康与优化得分)
- [十一、新账户启动清单](#十一新账户启动清单)
- [十二、CLI 实操流程](#十二cli-实操流程)

---

## 一、广告系列类型选择

### 1.1 类型矩阵

| 类型           | 最佳用途                         | 漏斗位置  | 控制度 | 自动化程度 |
| -------------- | -------------------------------- | --------- | ------ | ---------- |
| **Search**     | 高意图关键词捕获、线索、品牌防御 | 底部      | 高     | 中         |
| **PMax**       | 全漏斗覆盖、有产品 Feed 的电商   | 全部      | 低     | 极高       |
| **Demand Gen** | YouTube/Discover/Gmail 视觉获客  | 中上部    | 中高   | 中         |
| **Display**    | 再营销、品牌曝光                 | 顶部/中部 | 高     | 低中       |
| **YouTube**    | 视频驱动转化、品牌叙事           | 顶部/中部 | 中     | 中         |
| **App**        | 应用安装、应用内行为             | 全部      | 低     | 极高       |

### 1.2 选择决策树

**第一步：主要目标是什么？**

- 直接转化 + 有明确关键词 → **Search 优先，再叠加 PMax**
- 有产品 Feed 的电商 → **PMax（Feed 驱动）+ Search（品牌/高价值词）+ Demand Gen**
- 线索生成 → **Search + PMax（必须配置离线转化导入）**
- 品牌知名度 → **YouTube + Display + Demand Gen**

**第二步：有多少创意素材？**

- 仅文字 → Search
- 图片 + 文字 → Search + Display + Demand Gen
- 视频 + 图片 + 文字 → 全类型

**第三步：每月转化量多少？**

- < 15 次/月/系列 → 仅 Search（Manual CPC 或 Max Clicks）
- 15-30 次/月 → Search + 谨慎启动 PMax
- 30+ 次/月 → Smart Bidding + PMax 可放心使用

### 1.3 2025-2026 关键变化

- **Demand Gen 已完全替代 Discovery** — 新增 YouTube Shorts、In-stream 版位
- **PMax + Demand Gen 是电商推荐组合** — PMax 捕获需求，Demand Gen 创造需求
- **PMax 已支持**：品牌排除、搜索主题、否定关键词（最多 10,000 条）
- **品牌词始终用 Search** — PMax 竞价品牌词 CPC 更高且控制度低

---

## 二、账户架构设计

### 2.1 命名规范

```
[系列类型]_[目标]_[定向]_[地域]_[匹配/受众]
```

示例：

- `Search_LeadGen_BrandedTerms_US_Exact`
- `PMax_Ecom_AllProducts_US`
- `DemandGen_Prospecting_LookalikeBuyers_US`

### 2.2 电商架构

```
Account
├── Search_Brand_[Geo]_Exact          ← 品牌词，最低 CPA，防止被 PMax 抢走
├── Search_NonBrand_[品类]_[Geo]      ← 高价值非品牌词
├── PMax_AllProducts_[Geo]            ← 全品类，含 asset group
│   ├── Asset Group: 品类 A
│   ├── Asset Group: 品类 B
│   └── Asset Group: 高利润品
├── PMax_FeedOnly_[Geo]               ← 仅 Feed 无素材 → 强制 Shopping 版位
├── DemandGen_Prospecting_[Geo]       ← 相似受众 + 自定义受众
├── DemandGen_Remarketing_[Geo]       ← 网站访客 + 弃购用户
└── YouTube_BrandAwareness_[Geo]      ← 可选
```

### 2.3 线索生成架构

```
Account
├── Search_Brand_[Geo]_Exact
├── Search_NonBrand_HighIntent_[Geo]_Exact   ← "hire plumber near me"
├── Search_NonBrand_MidIntent_[Geo]_Broad    ← "best CRM for small business"
├── PMax_LeadGen_[Geo]                        ← ⚠️ 必须配置离线转化导入
├── DemandGen_Prospecting_[Geo]
└── Display_Remarketing_[Geo]
```

> **线索生成的 PMax 陷阱**：无离线转化数据时，PMax 会优化最容易的转化（通常是垃圾表单）。**必须**先导入 CRM 合格线索数据再启用。

### 2.4 本地服务架构

```
Account
├── Search_Brand_[城市/区域]
├── Search_Services_[服务类型]_[城市]_Exact
├── Search_Services_[服务类型]_[城市]_Broad
├── PMax_LocalStore_[城市]               ← 关联 Google Business Profile
└── Display_Remarketing_[半径]
```

- 半径定向：典型 10-25 英里
- 预算充足时按主要城市分系列

### 2.5 SaaS 架构

```
Account
├── Search_Brand_Global_Exact
├── Search_Competitors_Global_Exact
├── Search_HighIntent_[Geo]_Exact        ← "CRM software pricing"
├── Search_MidFunnel_[Geo]_Broad         ← "how to manage remote teams"
├── PMax_SaaS_[Geo]                       ← 配多阶段转化：试用 > MQL > SQL > 付费
├── DemandGen_Prospecting_[Geo]
├── YouTube_Demo_[Geo]
└── Display_Remarketing_TrialUsers_[Geo]  ← 试用未付费用户
```

---

## 三、出价策略优化

### 3.1 策略选择指南

| 场景                       | 推荐策略                            | 原因                     |
| -------------------------- | ----------------------------------- | ------------------------ |
| 新系列，< 15 转化/月       | Max Clicks（设 CPC 上限）           | 积累数据                 |
| 15-30 转化/月              | Max Conversions（无目标）           | 让算法无约束学习         |
| 30+ 转化/月，明确 CPA 目标 | **Target CPA**                      | 数据充足，可精准控制     |
| 30+ 转化/月，价值差异大    | **Target ROAS**                     | 按价值优化               |
| 品牌系列                   | Target Impression Share（90%+）     | 品牌防御                 |
| 竞品系列                   | Manual CPC 或 Max Clicks + CPC 上限 | 成本不可预测，需精细控制 |

### 3.2 校准 tCPA / tROAS

**设定初始 tCPA：**

1. 先用 Max Conversions（不设目标）运行 2-4 周
2. 计算该期间的平均 CPA
3. 设 tCPA = 平均 CPA 或高 10-20%（避免过度约束）
4. 每 2 周收紧不超过 10-15%

**设定初始 tROAS：**

1. 先用 Max Conversion Value（不设目标）运行 2-4 周
2. 计算平均 ROAS
3. 设 tROAS = 平均 ROAS 或低 10-20%（给算法空间）
4. 每 2 周提高不超过 15-20%

### 3.3 新系列启动协议

| 阶段 | 时间      | 策略                                 | 目标          |
| ---- | --------- | ------------------------------------ | ------------- |
| 1    | 第 1-2 周 | Max Clicks（CPC 上限 = 2× 预期均值） | 积累点击数据  |
| 2    | 第 2-4 周 | Max Conversions（无目标）            | 积累 15+ 转化 |
| 3    | 第 4-8 周 | tCPA / tROAS（按平均值设）           | 稳定优化      |
| 4    | 持续      | 每 2 周调整 10-15%                   | 逐步趋近目标  |

### 3.4 学习期规则

- 学习期约 7 天或直到积累足够数据
- **学习期内避免**：预算变动 >20%、出价策略变更、转化目标变更、大幅关键词/受众变更
- "Learning (limited)" = 数据不足 → 考虑合并系列、扩大定向、增加预算

### 3.5 组合出价策略（Portfolio Bid Strategies）

**适用场景**：

- 多个系列共享同一转化目标和 CPA/ROAS 目标
- 单系列 < 30 转化/月但合计 > 50
- **禁忌**：不把品牌和非品牌系列放同一组合

---

## 四、地域优化

### 4.1 位置定向模式

| 模式                             | 含义                          | 推荐场景                                 |
| -------------------------------- | ----------------------------- | ---------------------------------------- |
| **Presence or interest**（默认） | 在该地区 + 对该地区有兴趣的人 | 旅游、房产、留学                         |
| **Presence only**                | 仅物理上在该地区的人          | **线索生成、本地服务、有配送限制的电商** |

> 多数业务应改为 **Presence only**，避免预算浪费在「仅感兴趣」的用户上。

### 4.2 数据驱动的地域出价调整

```
1. 收集 2-4 周地域数据
   → google-analysis -a <CID> --sections geographic

2. 识别高效地域：CPA 低于均值 20%+ 或 ROAS 高于均值 20%+
   → 出价 +10% ~ +30%

3. 识别低效地域：CPA 高于均值 30%+ 或 ROAS 低于均值 30%+
   → 出价 -10% ~ -30%

4. 严重低效地域：CPA > 2× 均值
   → 出价 -50% 或排除

5. 每季度复审（季节性会显著影响地域表现）
```

> **Smart Bidding 下的注意**：tCPA/tROAS 已自动考虑地域信号。更有效的做法是**按地域分系列 + 不同预算/目标**，而非手动调地域出价。

### 4.3 地域排除

始终排除：

- 不提供服务/不配送的国家
- 有法律限制的地区
- 60+ 天有显著花费但 0 转化的地区

### 4.4 CLI 地域操作

```bash
# 搜索地域 ID
siluzan-tso ad geo search -a <CID> -q "California"

# 添加定向
siluzan-tso ad geo add -a <CID> --campaign-id <ID> --location-id 21137

# 添加排除
siluzan-tso ad geo add -a <CID> --campaign-id <ID> --location-id <ID> --exclude

# 添加出价调整（+20%）
siluzan-tso ad geo add -a <CID> --campaign-id <ID> --location-id <ID> --bid-modifier 1.2
siluzan-tso ad geo set-bid -a <CID> --campaign-id <ID> --location-id <ID> --bid-modifier 1.2

# 查看地域效果报告
siluzan-tso google-analysis -a <CID> --sections geographic

# 查看已定向/已排除地域
siluzan-tso ad geo list -a <CID> --mode targeted
siluzan-tso ad geo list -a <CID> --mode excluded
```

---

## 五、设备优化

### 5.1 设备出价调整规则

| 出价策略                             | 设备调整生效？                                |
| ------------------------------------ | --------------------------------------------- |
| Manual CPC / ECPC                    | ✅ 生效（-100% ~ +900%）                      |
| Smart Bidding（tCPA/tROAS/Max Conv） | ❌ **被忽略**（唯一例外：-100% 移动端仍生效） |

### 5.2 设备分析框架

```bash
# 拉取设备数据
siluzan-tso google-analysis -a <CID> --sections devices
```

对比 CTR、转化率、CPA、ROAS 按设备：

| 情况                      | 诊断                 | 操作                              |
| ------------------------- | -------------------- | --------------------------------- |
| 移动端 CPA > 桌面端 50%+  | 移动落地页体验差     | 优先修复移动端 UX                 |
| 移动端转化率 < 桌面端 40% | 严重移动端问题       | 短期可用 -100% 移动端；中期修页面 |
| 移动端 CTR 高但转化低     | 点击真实但页面不转化 | 检查页面速度、表单、支付流程      |

### 5.3 是否按设备拆分系列？

**拆分条件**（同时满足）：

- 使用 Manual CPC
- 移动端 vs 桌面端 CPA/ROAS 差异 >40%，持续 30+ 天
- 有不同的移动端/桌面端落地页或优惠

**不拆分**（2025 最佳实践）：

- 使用 Smart Bidding 时（自动处理设备优化）
- 转化量低（拆分进一步碎片化数据）

---

## 六、转化追踪配置

### 6.1 主转化 vs 次转化

| 类型       | 含义                                    | 示例                       |
| ---------- | --------------------------------------- | -------------------------- |
| **主转化** | 纳入「转化」列 + Smart Bidding 优化依据 | 购买、合格线索、60s+ 通话  |
| **次转化** | 仅观察，不影响出价                      | 页面浏览、视频播放、微转化 |

**规则**：每个系列目标只设**一种**主转化。多种主转化表示同一行为（如表单 + 感谢页）会导致重复计数。

### 6.2 Enhanced Conversions

| 类型                               | 用途                         | 效果                  |
| ---------------------------------- | ---------------------------- | --------------------- |
| **Enhanced Conversions for Web**   | 在线转化 → hash 用户数据匹配 | 恢复 5-15% 未归因转化 |
| **Enhanced Conversions for Leads** | 离线转化 → CRM 数据回传      | 替代旧版 GCLID 导入   |

**2025 优先级**：所有账户启用 Web 版；所有线索生成账户启用 Leads 版。

### 6.3 离线转化导入要点

| 要素       | 建议                                       |
| ---------- | ------------------------------------------ |
| 上传频率   | 每 24 小时（越新鲜越好）                   |
| 最大回溯期 | 90 天（Enhanced for Leads 为 63 天）       |
| 主转化设为 | 最深漏斗阶段（如「成交」而非「表单提交」） |
| 转化价值   | 反映实际收入或预估 LTV                     |
| 匹配率目标 | > 50%（70%+ 为佳）                         |

### 6.4 转化价值规则

在不修改网站/CRM 的情况下，按条件调整报告中的转化价值：

| 维度 | 示例                | 影响            |
| ---- | ------------------- | --------------- |
| 地域 | 加州线索价值 +100%  | 影响 tROAS 出价 |
| 受众 | 回头客 +50%         | 影响 tROAS 出价 |
| 设备 | 移动端线索价值 -30% | 影响 tROAS 出价 |

### 6.5 归因模型

| 模型                    | 说明                    | 推荐                 |
| ----------------------- | ----------------------- | -------------------- |
| **DDA（数据驱动归因）** | ML 分配跨触点功劳       | **默认推荐**         |
| Last-click              | 100% 归功于最后一次点击 | 低转化量或简单结构时 |

DDA 最低要求：~300 转化 + ~3,000 广告互动/30 天。

---

## 七、预算优化

### 7.1 日预算设置原则

- **最低日预算 = 2-3× 目标 CPA** — 给 Smart Bidding 足够空间
- Google 单日可花费最高 2× 日预算（月度不超过 30.4× 日预算）
- 系列持续触达日预算上限 = 「受预算限制」→ Smart Bidding 会跳过高质量竞价

### 7.2 共享预算 vs 独立预算

| 共享预算                       | 独立预算              |
| ------------------------------ | --------------------- |
| 系列目标和 CPA/ROAS 相近       | 系列目标/盈利能力不同 |
| 希望 Google 按日动态分配       | 需要按系列保底花费    |
| **不适用**：品牌 vs 非品牌混合 | 品牌系列必须独立预算  |

### 7.3 扩量协议

- 以 **15-20% 周增量**逐步扩展预算
- 扩 20% 后若 CPA 上升 >20% → 触达边际递减 → 回退
- 使用 **Performance Planner** 预估不同预算的增量转化
- 单系列饱和 → 扩展到新系列类型/地域，而非继续加注

---

## 八、网络设置

### 8.1 Google Search Partners

| 状态         | 建议                                                  |
| ------------ | ----------------------------------------------------- |
| **默认关闭** | 2025 最佳实践：先关闭，测试后再开                     |
| 开启条件     | Search Partners CPA 在 Google Search CPA 的 120% 以内 |
| 关闭条件     | Search Partners CPA > Google Search 130%              |

### 8.2 Display Network 扩展（Search 系列）

**始终关闭** — 混合两种不同意图层级的渠道，干扰效果评估。如需 Display 覆盖，建立独立 Display 系列。

---

## 九、广告系列实验

### 9.1 可用实验类型（2025）

| 类型               | 适用                                 |
| ------------------ | ------------------------------------ |
| Custom Experiments | Search/Display/Demand Gen 系列级变更 |
| PMax Experiments   | PMax 增量测试                        |
| Video Experiments  | 视频创意对比                         |
| Ad Variations      | 跨多系列文案变更                     |

### 9.2 实验设置建议

| 参数       | 推荐                                        |
| ---------- | ------------------------------------------- |
| 流量分配   | 50/50（最快达到统计显著；风险低时用 70/30） |
| 运行时长   | 最少 2 周，推荐 4-8 周                      |
| 置信度阈值 | ≥ 95% 再做决策                              |
| 评估指标   | 转化量、CPA、ROAS — 不仅看点击或 CTR        |

### 9.3 高价值测试清单

1. **出价策略切换**（Manual → Max Conv → tCPA → tROAS）— 影响最大
2. **Exact → Broad + Smart Bidding** — Google 数据称 +25% 转化
3. **落地页对比** — 同关键词同广告，不同 URL
4. **受众叠加测试** — 观察模式 vs 定向模式
5. **AI Max for Search** — 开启 vs 关闭

---

## 十、账户健康与优化得分

### 10.1 优化得分（0-100%）

高分 ≠ 高效果。它只意味着 Google 认为还有更多机会。

### 10.2 推荐处理原则

**接受**：

- 修复被拒广告/附加信息
- 添加 RSA 变体（如 <3 个/广告组）
- 添加 sitelink/callout/snippet
- 修复转化追踪问题
- 移除重复/冲突关键词

**谨慎/拒绝**：

- 「提高预算」→ 仅在受限且 CPA 达标时接受
- 「切换到 Max Conversions」→ 仅在数据充足时
- 「开启 Display Network 扩展」→ 几乎总是拒绝
- 「移除阻止流量的否定词」→ 逐条检查，那些否定词可能有存在的理由
- 「自动应用」→ **永远不开**出价/预算/关键词自动应用

### 10.3 账户级关键设置

| 设置             | 要求                                          |
| ---------------- | --------------------------------------------- |
| Auto-tagging     | **必须开启**（转化追踪和 Analytics 集成前提） |
| 转化目标         | 确认仅预期的转化设为账户默认主转化            |
| 自动应用推荐     | 检查并**关闭**高风险项                        |
| IP 排除          | 排除已知机器人/竞品 IP（每系列最多 500）      |
| 品牌限制（PMax） | 使用品牌列表防止 PMax 竞价无关品牌            |
| 内容适宜性       | 设置账户级内容排除（暴力/色情/争议内容）      |

---

## 十一、新账户启动清单

```
□ 配置 Enhanced Conversions（在投放前）
□ 设定账户默认转化目标（仅一种主转化）
□ 从 Search 系列开始（高意图关键词）
□ 前 2-4 周用 Manual CPC 或 Max Clicks 积累数据
□ 有 30+ 转化/月后再启动 PMax
□ 线索生成：导入离线转化后再用 PMax
□ 关闭 Search Partners 和 Display Network 扩展
□ 地域定向设为 Presence only（多数业务）
□ 检查自动应用推荐，关闭高风险项
□ 完成广告主身份验证（见 google-ads-compliance.md 10.3 节）
```

---

## 十二、CLI 实操流程

### 12.1 创建完整广告系列

```bash
# 1. 搜索地域 ID
siluzan-tso ad geo search -a <CID> -q "United States"

# 2. 一体化创建（系列 + 广告组 + 关键词 + 广告）
siluzan-tso ad campaign-create

# 3. 查看创建进度
siluzan-tso ad batch get --id <taskId>
```

### 12.2 调整出价策略

```bash
# 查看当前系列设置
siluzan-tso ad campaigns -a <CID> --json-out ./snap

# 切换到 Target CPA（数据充足后）
# --target-cpa 是「主币种金额」，CLI 内部自动 ×100 写入；50 = 50 USD（不是微单位 5000）
siluzan-tso ad campaign-edit -a <CID> --id <系列ID> \
  --bidding TARGET_CPA --target-cpa 50

# 切换到 Target ROAS（ROAS 是比例，不是金额，无需 ×100）
siluzan-tso ad campaign-edit -a <CID> --id <系列ID> \
  --bidding TARGET_ROAS --target-roas 3.0
```

### 12.3 地域优化操作

```bash
# 查看地域效果
siluzan-tso google-analysis -a <CID> --sections geographic

# 排除低效地域
siluzan-tso ad geo add -a <CID> --campaign-id <ID> --location-id <低效地域ID> --exclude

# 高效地域加价 20%
siluzan-tso ad geo add -a <CID> --campaign-id <ID> --location-id <高效地域ID> --bid-modifier 1.2
```

### 12.4 账户诊断

```bash
# 总览
siluzan-tso google-analysis -a <CID> --sections overview

# 黄金账户诊断（检查各项配置是否达标）
siluzan-tso google-analysis -a <CID> --sections gold-account

# 质量指标
siluzan-tso google-analysis -a <CID> --sections ads-index

# 转化动作配置
siluzan-tso google-analysis -a <CID> --sections conversion-actions

# 设备分析
siluzan-tso google-analysis -a <CID> --sections devices
```
