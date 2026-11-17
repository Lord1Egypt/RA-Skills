# 账户审计 · 快速检查与 CLI

> 由 [`google-ads-account-audit.md`](google-ads-account-audit.md) 索引。**何时 Read**：5 分钟健康检查、常见问题速查、CLI 审计命令序列

## Contents

- 1. 审计总览与流程
- 2. 快速健康检查（5分钟诊断）
- 13. 常见问题诊断速查表
- 14. CLI 审计命令序列

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
