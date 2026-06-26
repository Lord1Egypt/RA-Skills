# SKILL.md - 公司情报侦察

> **名称：** 公司情报侦察 v2.0
> **触发：** 用户提供公司 URL、公司名、或批量 JSON，要求建档/背调/找联系人/查邮箱
> **执行：** SHADOW Agent 直接调用工具完成全流程
> **输出：** 本地档案 + OKKI 建档 + 有效邮箱列表 + 推理分析

---

## 📋 完整工作流（SHADOW 亲自执行）

```
Phase 1: 网站背调 → Phase 2: 联系人挖掘 → Phase 3: 邮箱验证 → Phase 4: 写入 OKKI → Phase 5: 推理层
```

**批量模式：** 用户提供 `companies.json` 数组 → 逐个处理 → 输出汇总报告 `summary.md`

---

## Phase 0: 红线检测（新增 · P0）

**在开始任何工作前，先运行红线检测。触发任一项 → 立即跳过。**

| 红线 | 检测方法 | 动作 |
|------|---------|------|
| 制裁国家/实体 | 检查公司所在国家是否在 OFAC/EU 制裁名单 | 🚫 直接跳过，记录原因 |
| 公司破产/注销 | 搜索 "{公司名} bankrupt" / "注销" / "liquidation" | 💀 标记为 Dead，不建档 |
| 大量差评/诉讼 | 搜索 "{公司名} scam" / "lawsuit" / "fraud" | ⚠️ 标记为 Risk，输出警告 |
| 邮箱域名不匹配 | 官网域名 vs 邮箱域名交叉验证 | ⚠️ 标记为 Suspicious |
| 色情/赌博/军火 | Phase 1 网站内容检测 | 🚫 直接跳过 |

**输出格式：**
```
### Phase 0 红线检测
- [✅ 通过] 无红线
- 或 [🚫 触发] 具体红线 + 原因
```

---

## Phase 1: 网站背调

**工具：** `web_fetch` + `web_search`

```
1. web_fetch 目标 URL（contact-us / about / 首页）
2. web_fetch 补充页面（/about/, /career/, /team/, /products/）
3. web_search 公司名（获取 LinkedIn / ZoomInfo / Moneyhouse / Glassdoor 等外部来源）
4. 交叉验证：至少 2 个独立来源确认同一信息
```

**提取字段：**
- 公司全称、简称、国家、地址
- 电话、邮箱、网站
- 成立时间、营业额、员工规模
- 业务类型、产品线、代理品牌
- 核心团队（官网 + LinkedIn 列出的）
- **Farreach 相关性信号：** 是否卖 HDMI/DP/USB/Ethernet 线材、是否有 OEM 需求

---

## Phase 2: 联系人挖掘（增强 · P1）

**工具：** `web_search`

### Step 1: 找 LinkedIn 员工
```
1. site:linkedin.com/in "{公司名}" — 找员工 LinkedIn
2. "{公司名}" "CEO" OR "Founder" OR "Director"
3. "{公司名}" "buyer" OR "purchasing" OR "category manager"
4. "{公司名}" "sales director" OR "head of sales" — 卖电子产品的人很可能也卖线
```

### Step 2: 推导邮箱格式
```
1. 从 RocketReach / Hunter.io / Apollo.io snippet 找已知邮箱
2. "{公司名}" "{人名}" email — 验证已知人名
3. 分析已确认的邮箱，推导格式：
   - first@domain.com（最常见）
   - first.last@domain.com
   - f.last@domain.com
   - first@domain.com（小公司常见）
4. 基于推导的格式，为每个目标联系人生成邮箱候选
```

### Step 3: 关键角色优先级
| 优先级 | 角色 | 原因 |
|--------|------|------|
| 1 | CEO/Founder/Owner | 最高决策人 |
| 2 | Head of Distribution/Purchasing/Procurement | 采购负责人 |
| 3 | Category Manager / Product Manager | 品类/产品采购 |
| 4 | Sales Director / Head of Sales | 卖电子产品的，需要线材配套 |
| 5 | Key Account Manager | 可反向利用获取情报 |
| 6 | Finance Head / CFO | 价格谈判时重要 |

---

## Phase 3: SMTP 邮箱验证（零风险）

**工具：** `exec` 运行 Python 脚本

```python
import socket
import time

emails = ['artur@domain.com', 'info@domain.com', ...]
mx = 'mail.domain.com'  # 从 dig MX 获取

for email in emails:
    s = socket.create_connection((mx, 25), timeout=15)
    s.settimeout(15)
    s.recv(1024)
    s.send(b"EHLO gmail.com\r\n")
    time.sleep(2)
    s.recv(4096)
    s.send(b"MAIL FROM:<test@gmail.com>\r\n")
    time.sleep(2)
    s.recv(512)
    s.send(f"RCPT TO:<{email}>\r\n".encode())
    time.sleep(2)
    resp = s.recv(512).decode()
    code = resp[:3]  # 250 = 有效，550 = 不存在
    s.send(b"QUIT\r\n")
    s.close()
    time.sleep(3)  # 每个邮箱间隔 3 秒
```

**⚠️ 关键：**
- 必须 `time.sleep(2~3)`，否则超时
- 只到 RCPT TO，绝不发 DATA
- 每个邮箱之间间隔 3 秒

---

## Phase 4: 写入 OKKI

**工具：** `exec` 调 OKKI CLI

**4a. 本地存档：**
```
intelligence/clients/{Company_Name}.md
```

**4b. OKKI 新建客户：**
```python
data = {
    'name': '公司全称',
    'short_name': '简称',
    'country': 'ISO两位码',
    'address': '详细地址',
    'homepage': 'https://...',
    'user_id': 56785529,  # Jordan
    'group_id': 0,
    'pool_id': 0,
    'is_public': 0,
    'remark': '关键信息摘要',
    'customers': [
        {'first_name': '名', 'last_name': '姓', 'position': '职位', 'email': '已验证邮箱'}
    ]
}
```

注意：`group_id` 和 `pool_id` 必填，不能省略。

---

## Phase 5: 推理层（增强 · P0+P1+P2）

**目的：** 基于 Phase 0-4 已采集的情报，帮老板判断"为什么值得跟进"以及"怎么开口"。

**不需要额外 API，完全基于已有数据推理。**

### 5.1 量化线索评分（Lead Score）

**基础分 50 分，按以下规则加减：**

| 信号 | 分值 | 说明 |
|------|------|------|
| 有 CEO/Founder/Owner 已验证邮箱 | +15 | 最高决策人可直达 |
| 产品线匹配 HDMI/DP/USB/Ethernet | +15 | 直接采购需求 |
| 公司成立 > 3 年 | +10 | 稳定性 |
| 有招聘/融资/扩张信号 | +10 | 业务在增长 |
| 官网提到 quality/certification/premium | +5 | 品质意识 |
| 有 OEM/白牌产品 | +5 | 可能需要代工 |
| Sales Director 邮箱已验证 | +5 | 销售端入口 |
| 所有邮箱全部 bounce（550） | -20 | 无法触达 |
| 明显不相关（纯服务/零售/个人博客） | -15 | 非目标客户 |
| 官网不可访问/信息极少 | -10 | 数据不足 |
| Phase 0 触发红线（非制裁类） | -10 | 风险提示 |

**评级阈值：**
| 分数 | 评级 | 动作 |
|------|------|------|
| ≥ 75 | 🔴 Hot | 立即跟进，优先处理 |
| 50-74 | 🟡 Warm | 正常跟进，排入计划 |
| < 50 | 🟢 Cold | 暂存，定期回顾 |

**输出格式：**
```
### 🔴 Hot — 评分 85/100

| 信号 | 分值 |
|------|------|
| 有 CEO 已验证邮箱 | +15 |
| 产品线匹配 HDMI/USB | +15 |
| 公司成立 8 年 | +10 |
| 正招聘产品经理 | +10 |
| 官网提到 "premium quality" | +5 |
| **总计** | **85** |
```

### 5.2 痛点分析（Pain Point Analysis）

根据公开信号推断客户当前面临的挑战，Farreach 线材能解决什么。

**触发信号 → 痛点映射：**

| 信号 | 推断痛点 | 切入角度 |
|------|---------|----------|
| 大量招聘 tech/engineering | 产品线扩张，需稳定供应商 | 定制化线材方案 |
| 新开分支机构/仓库 | 供应链需求增加 | 批量采购 + 物流 |
| 参加展会（CES/IFA 等） | 需要新品支持 | 新品线材适配 |
| 官网有 HDMI/DP 产品但无品牌 | 可能 OEM/分销 | 提供 OEM 线材 |
| 官网提到 "quality"/"premium"/"certified" | 对品质要求高 | Farreach 认证背书 |
| LinkedIn 提到 "supplier change"/"sourcing" | 在换供应商 | 切换成本低，快速响应 |
| 有自有品牌但产品线不全 | 缺品类，需要补齐 | 补充产品线 |

⚠️ **约束：** 所有推断必须基于公开证据，不得编造。每条推断附信息来源 URL。

### 5.3 时机判断（Timing Signal）

| 时机信号 | 权重 | 说明 |
|---------|------|------|
| 最近 30 天内有新动态 | 🔴 高 | 融资/展会/新品发布 |
| 最近 90 天内有新动态 | 🟡 中 | 招聘/合作/官网改版 |
| 超过 90 天无动态 | 🟢 低 | 常规跟进，时机一般 |

**输出格式：**
```
### 时机：🟢 好 — 2026-04 刚参加完 CES，新品线正在选型
```

### 5.4 个性化开场白（Personalized Opener）

生成 2 个版本：一个偏商务，一个偏产品。

**Farreach 特色话术库（根据线索类型选角度）：**

| 线索类型 | 商务版角度 | 产品版角度 |
|----------|-----------|-----------|
| 🔴 Hot（有明确采购需求） | "我们刚帮 [类似公司] 解决了 [具体问题]" | "HDMI 2.1 认证线缆 + 你的产品线 = 完美匹配" |
| 🟡 Warm（可能相关） | "注意到你们在做 [具体业务]，我们有相关经验" | "我们的 HDMI/USB 产品线能帮你补齐 [具体品类]" |
| 🟢 Cold（常规接触） | "简单介绍 Farreach，看是否有合作可能" | "18 年制造经验 + HDMI 认证会员，越南工厂" |

**要求：**
- 基于真实情报，不编造
- 提到客户最近的具体动态
- 一句话说明 Farreach 能帮到什么
- ⛔ 禁止出现 "cutting-edge"、"innovative"、"leading"

**输出格式：**
```
### 推荐开场白

**版本 1（偏商务）：**
Hi [Name], [个性化开场，基于真实情报]. Farreach 可以 [具体帮助]. 

**版本 2（偏产品）：**
Hi [Name], [产品角度切入]. We manufacture [具体产品线] with [认证/优势].
```

---

## 📝 交付模板

### 单家公司档案
```markdown
# {Company Name}

> 建档日期：YYYY-MM-DD | 跟进人：XXX | 线索评分：🔴 Hot / 🟡 Warm / 🟢 Cold

## 基本信息
| 项目 | 内容 |
|------|------|
| 公司全称 | |
| 简称 | |
| 国家 | |
| 地址 | |
| 电话 | |
| 邮箱 | |
| 网站 | |
| 成立时间 | |
| 员工规模 | |
| 业务类型 | |
| 产品线 | |
| Farreach 相关性 | |

## 核心联系人（已验证邮箱）
| 姓名 | 职位 | 邮箱 | 状态 |
|------|------|------|------|

## 关键点
- ...

## Phase 0 红线检测
- [✅ 通过] 无红线

---

## 情报分析

### 线索评分：🔴 Hot — 85/100
| 信号 | 分值 |
|------|------|
| ... | +X |

### 痛点推断
1. [痛点] — [证据] ([来源](URL))

### 时机判断
[时机评级] — [理由]

### 推荐开场白

**版本 1（偏商务）：**
[内容]

**版本 2（偏产品）：**
[内容]
```

### 批量汇总报告（summary.md）
```markdown
# Farreach 线索背调汇总

> 生成日期：YYYY-MM-DD | 总计：X 家

## 概览
| 评级 | 数量 | 占比 |
|------|------|------|
| 🔴 Hot | X | X% |
| 🟡 Warm | X | X% |
| 🟢 Cold | X | X% |
| 🚫 Dead/Skip | X | X% |

## 🔴 Hot（立即跟进）
| 公司 | 国家 | 评分 | CEO/联系人 | 邮箱 | 关键信号 |
|------|------|------|-----------|------|---------|

## 🟡 Warm（正常跟进）
| 公司 | 国家 | 评分 | 联系人 | 邮箱 | 关键信号 |
|------|------|------|--------|------|---------|

## 🟢 Cold（暂存）
| 公司 | 国家 | 评分 | 原因 |
|------|------|------|------|

## 🚫 跳过/排除
| 公司 | 原因 |
|------|------|
```

---

## 🔧 批量模式使用说明

**输入：** `companies.json` 数组
```json
[
  {"name": "Company A", "url": "https://...", "country": "US"},
  {"name": "Company B", "url": "https://...", "country": "DE"}
]
```

**执行：**
1. 逐个处理，每家公司生成独立档案
2. 每处理完 5 家，更新一次进度报告
3. 全部完成后，生成 `summary.md` 汇总

**输出位置：**
- 单家档案：`intelligence/clients/{Company_Name}.md`
- 汇总报告：`intelligence/batch-{YYYY-MM-DD}-summary.md`

---

## ⚠️ 安全红线

1. **邮箱验证绝不发 DATA** — 只到 RCPT TO 阶段
2. **Phase 0 红线检测优先** — 触发制裁类直接跳过
3. **公司背调三步法则** — 域名可访问 → 内容匹配 → 交叉验证
4. **不捏造信息** — 不确定时说"不确定"，推断标注不确定性
5. **OKKI 建档必填 group_id/pool_id**
6. **所有推断附来源 URL** — 不得无依据猜测

---

## 📊 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0 | 2026-04-30 | 新增 Phase 0 红线检测、量化评分（P1）、批量模式（P2）、话术库 |
| v1.0 | 2026-04-30 | 初始版本：4 阶段工作流 + Phase 5 推理层 |
