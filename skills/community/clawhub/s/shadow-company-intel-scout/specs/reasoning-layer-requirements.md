# Company Intel — 推理层需求文档

> **版本：** v1.1（已实现）  
> **日期：** 2026-04-30  
> **提出人：** Jaden  
> **开发人：** Wilson  
> **状态：** ✅ 所有 P0/P1/P2 已实施

---

## 一、背景

当前 company-intel skill 完成了信息搜集和结构化输出（公司信息 + 联系人 + 邮箱验证 + 写 OKKI），但缺少**推理层**：拿到情报后，帮老板判断"为什么值得跟进"以及"怎么开口"。

参考 ClawHub 上 `afrexai-prospect-researcher` 的痛点推断框架，在现有 4 阶段工作流之后增加 Phase 5。

---

## 二、现有工作流（不变）

```
Phase 1: 网站背调 → 公司基本信息
Phase 2: 联系人挖掘 → LinkedIn + 角色识别
Phase 3: SMTP 邮箱验证 → 邮箱有效性
Phase 4: 写入 OKKI → CRM 建档 + 本地档案
```

---

## 三、新增 Phase 5：推理层

### 5.1 线索评分（Lead Score）

**输出：** Hot / Warm / Cold 三级，附理由。

**评分规则：**

| 级别 | 条件（满足任一） |
|------|-----------------|
| 🔴 Hot | 最近 6 个月内有融资/招聘扩张信号 |
| | 目标联系人是 CEO/Founder/Head of Purchasing |
| | 公司产品线与我们高度匹配（HDMI/DP/USB 线材进口商） |
| 🟡 Warm | 成立时间 > 1 年，有稳定招聘但无融资信号 |
| | 目标联系人是中层管理者 |
| | 有相关业务但不确认是否进口线材 |
| 🟢 Cold | 信息极少（官网都不可访问） |
| | 明显不匹配（如纯服务业、本地零售） |
| | 邮箱全部验证失败（550 全部 bounce） |

**输出格式示例：**

```
### 🔴 Hot — 推荐立即跟进

- 2026-02 完成 $3M A 轮融资（ Crunchbase）
- 正招聘 Procurement Manager（LinkedIn）
- CEO 为第一联系人，邮箱已验证 ✅
```

---

### 5.2 痛点分析（Pain Point Analysis）

**目的：** 根据公开信号推断客户当前可能面临什么挑战，我们的线材能解决什么问题。

**触发信号 → 痛点映射表：**

| 信号 | 推断痛点 | 我们的切入角度 |
|------|---------|---------------|
| 大量招聘 tech/engineering | 产品线扩张，需要稳定供应商 | 定制化线材方案 |
| 新开分支机构/仓库 | 供应链管理需求增加 | 批量采购 + 物流 |
| 参加展会（CES 等） | 需要新品支持 | 新品线材适配 |
| 官网有 HDMI/DP 产品但无品牌 | 可能 OEM/分销 | 提供 OEM 线材 |
| 公司网站提到 "quality"/"premium" | 对品质要求高 | Farreach 品质背书 |
| LinkedIn 提到 "supplier change"/"sourcing" | 在换供应商 | 切换成本低，快速响应 |

**输出格式示例：**

```
### 痛点推断

1. **供应链扩张** — 2026-01 新开澳洲分部（官网新闻），需要新的线材供应商配合本地配送
2. **品质升级** — 官网首页强调 "Premium Quality"，符合我们 HDMI 2.1 认证线定位
```

⚠️ **约束：** 所有推断必须基于公开证据，不得编造。每条推断后附信息来源 URL。

---

### 5.3 时机判断（Timing Signal）

**目的：** 回答"为什么现在联系"。

**检查项：**

| 时机信号 | 权重 | 说明 |
|---------|------|------|
| 最近 30 天内有新动态 | 高 | 融资、展会、新品发布 |
| 最近 90 天内有新动态 | 中 | 招聘、合作、官网改版 |
| 超过 90 天无动态 | 低 | 常规跟进，时机一般 |

**输出示例：**

```
### 时机：🟢 好 — 2026-04 刚参加完 CES，新品线正在选型
```

---

### 5.4 个性化开场白（Personalized Opener）

**目的：** 生成 2-3 句个性化邮件/LinkedIn 开头，让对方觉得你了解他。

**要求：**
- 基于真实情报，不编造
- 提到客户最近的具体动态（融资、展会、招聘等）
- 一句话说明 Farreach 能帮到他什么
- 不出现 "cutting-edge"（USER.md 禁令）

**模板变量：**
- `{company}` — 公司名称
- `{recent_event}` — 最近动态
- `{pain_point}` — 推断痛点
- `{product_fit}` — 产品匹配

**输出示例：**

```
### 推荐开场白

Hi [Name],

Congratulations on the $3M Series A! I noticed you're expanding into the Australian market — as you scale, reliable HDMI and USB cable supply is critical. Farreach has been manufacturing certified cables for [similar company in space] since 2010. Would love to share how we helped them reduce supplier lead time by 40%.

---

备选 2：

Hi [Name], saw your team at CES — great to see [Company] pushing into premium AV solutions. We manufacture HDMI 2.1 and DP cables with full compliance certification, and I'd love to discuss how we can support your new product line.
```

每次生成 2 个版本，一个偏商务，一个偏产品。

---

## 四、最终输出模板整合

Phase 1-4 的输出之后，追加 Phase 5 的完整内容：

```markdown
---

## 情报分析

### 线索评分：🔴 Hot / 🟡 Warm / 🟢 Cold
- [评分理由，2-3 条]

### 痛点推断
1. [痛点] — [证据] ([来源](URL))

### 时机判断
[时机评级] — [理由]

### 推荐开场白
[版本 1：偏商务]

[版本 2：偏产品]
```

---

## 五、技术实现要点

### 5.1 数据来源

推理层不需要额外 API，完全基于 Phase 1-4 已采集的数据。

### 5.2 评分逻辑

- 硬规则（融资、联系人级别、邮箱验证结果）用代码判断
- 软判断（产品匹配度、痛点推断）由 LLM 基于已有情报推理
- 两者结合：先跑硬规则，再让 LLM 做软判断

### 5.3 SKILL.md 修改

在现有 Phase 4 之后插入 Phase 5 的完整描述，包含：
- 评分规则表
- 痛点映射表
- 时机检查项
- 开场白生成指令
- 最终输出模板

### 5.4 安全约束

- 不编造任何事实
- 推断必须标注不确定性
- 所有信息附来源 URL
- 邮箱验证结果直接影响评分（全部 550 直接降级 Cold）

---

## 六、验收标准

1. **功能：** 输入一个公司名，输出必须包含线索评分 + 痛点 + 时机 + 2 个开场白
2. **准确性：** 评分至少 1 条硬规则支撑（非纯 LLM 主观判断）
3. **格式：** 严格遵循 Phase 5 输出模板
4. **安全性：** 不出现编造的事实或联系方式

---

## 七、文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `SKILL.md` | 修改 | 新增 Phase 5 工作流描述 + 输出模板 |
| `specs/reasoning-layer-requirements.md` | 新增 | 本文档 |

---

## 八、已实施的改进（v2.0）

### P0 — 红线检测（Phase 0）
- 制裁国家/实体 → 直接跳过
- 破产/注销 → 标记 Dead
- 大量差评/诉讼 → 标记 Risk
- 邮箱域名不匹配 → 标记 Suspicious
- 色情/赌博/军火 → 直接跳过

### P1 — 量化评分 + 联系人挖掘增强
- **量化评分：** 基础分 50，加减分规则明确，≥75=Hot / 50-74=Warm / <50=Cold
- **联系人角色扩展：** 新增 Sales Director（卖电子产品的很可能需要线材）
- **邮箱格式推导：** 找到 1 个邮箱后自动推导格式（first@ / first.last@ / f.last@）
- **官网团队页：** 直接抓取 /team/ /about/ 页面列出高管

### P2 — 批量模式 + 话术库
- **批量输入：** 支持 `companies.json` 数组 → 逐个处理 → 输出 `summary.md`
- **汇总报告：** 按 Hot/Warm/Cold/Dead 分组，含表格和评分
- **Farreach 话术库：** 根据 Hot/Warm/Cold 类型选择不同开场角度

### 文件变更
- ✅ `SKILL.md` → 升级为 v2.0（完整重写）
- ✅ `specs/reasoning-layer-requirements.md` → 更新状态

---

**备注：** 开发完成后同步更新 monorepo 和 ClawHub。
