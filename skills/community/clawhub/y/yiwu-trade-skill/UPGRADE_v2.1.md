# 义乌.Skill v2.1 升级说明

## 升级时间
2026年4月26日

## 版本对比

| 项目 | v2.0.0 | v2.1.0 |
|------|--------|--------|
| 模块数量 | 7个 | **10个** |
| 核心模块 | 政策合规、供应链、物流、获客、起盘、品控、风险 | **新增支付结算、财务税务、数据决策** |
| 参考文档 | 6个 | **9个** |
| 模板工具 | 4个 | **7个** |
| 唤醒指令 | 7条 | **15条** |

---

## 新增内容详情

### 新增模块8：支付结算技能
**文件：** `references/payment_guide.md`

涵盖内容：
- 7种支付方式对比（T/T、PayPal、PingPong、Escrow等）
- T/T分阶段付款模式详解（30%+70%结构）
- 收汇结汇SOP流程（1039政策）
- 支付风控10大信号识别
- 欺诈防范SOP（账户变更验证）
- 汇率管理工具箱（远期锁汇、外汇期权等）
- Escrow托管交易流程
- 信用证L/C入门
- 账期管理与逾期催收

### 新增模块9：财务税务技能
**文件：** `references/finance_guide.md`

涵盖内容：
- 外贸成本全景图（FOB/CIF/DDP）
- 成本计算示例（圣诞饰品案例）
- 物流成本参考表（7种运输方式）
- 利润分析模型
- 订单利润分析表模板
- 客户利润贡献度分析
- 出口退税全流程（1039 vs 0110对比）
- 退税计算示例
- 税务合规检查清单
- 财务报表解读（利润表、现金流量表）

### 新增模块10：数据决策技能
**文件：** `references/analytics_guide.md`

涵盖内容：
- 核心指标字典（规模/盈利/效率/客户/风险5大类）
- 月度经营分析模板
- RFM客户分层模型（8类客户策略）
- 客户生命周期价值（CLV）计算
- 爆款识别标准（5维评估）
- 滞销预警机制（4大规则）
- 商品分析报表模板
- 渠道ROI分析模型
- 归因模型选择
- 决策看板设计模板
- 指标预警规则库

---

## 新增模板工具

### 1. payment_comparison.xlsx（支付通道对比表）
- Sheet1：7种支付方式对比矩阵
- Sheet2：T/T付款方案选择器
- Sheet3：水单核实检查清单

### 2. exchange_rate_tracker.xlsx（汇率追踪表）
- Sheet1：30天汇率追踪记录
- Sheet2：远期锁汇记录表
- Sheet3：汇率敏感性分析

### 3. cost_calculator.xlsx（成本核算表）
- Sheet1：订单成本计算器
- Sheet2：订单利润分析表
- Sheet3：多产品成本对比

---

## 新增唤醒指令

| 指令 | 功能 |
|------|------|
| `义乌.Skill 支付方案选择` | 跨境支付通道推荐 |
| `义乌.Skill 汇率管理建议` | 结汇时机+锁汇策略 |
| `义乌.Skill 成本利润核算` | 订单成本+利润计算 |
| `义乌.Skill 出口退税指导` | 退税流程+1039对比 |
| `义乌.Skill 税务合规自查` | 税务合规清单 |
| `义乌.Skill 客户价值分析` | RFM分层+CLV计算 |
| `义乌.Skill 经营数据看板` | 核心指标+预警看板 |
| `义乌.Skill 商品销售分析` | 爆款识别+滞销预警 |

---

## 文件结构

```
skills/yiwu-trade-skill/
├── SKILL.md                    # 主技能文件（v2.1.0）
├── SKILL-payment-module.md     # 支付模块源文件
├── SKILL-finance-module.md     # 财务模块源文件
├── SKILL-analytics-module.md   # 数据模块源文件
├── references/
│   ├── compliance_guide.md     # 政策合规指南
│   ├── sourcing_guide.md       # 供应链指南
│   ├── logistics_guide.md      # 物流指南
│   ├── startup_guide.md        # 起盘指南
│   ├── quality_control.md      # 品控指南
│   ├── risk_control.md         # 风险防控指南
│   ├── payment_guide.md        # ⭐ 支付结算指南（新增）
│   ├── finance_guide.md        # ⭐ 财务税务指南（新增）
│   └── analytics_guide.md      # ⭐ 数据决策指南（新增）
├── templates/
│   ├── sales_scripts.md        # 话术库
│   ├── pi_template.docx        # PI模板
│   ├── contract_template.docx  # 合同模板
│   ├── packing_list.xlsx       # 装箱单模板
│   ├── payment_comparison.xlsx # ⭐ 支付对比表（新增）
│   ├── exchange_rate_tracker.xlsx # ⭐ 汇率追踪表（新增）
│   └── cost_calculator.xlsx    # ⭐ 成本核算表（新增）
├── scripts/
│   ├── logistics_optimizer.py
│   └── price_calculator.py
└── agents/                     # 子Agent配置
```

---

## 升级方式

### 方式1：直接使用
直接使用 `skills/yiwu-trade-skill/` 目录

### 方式2：打包部署
使用 `skills/yiwu-trade-skill-v2.1.tar.gz` 进行部署

---

## 维护建议

1. **支付模块**：每季度更新支付通道政策和费率
2. **财务模块**：每年更新税率和成本参考数据
3. **数据模块**：根据业务发展持续迭代指标体系

---

**升级完成时间：** 2026年4月26日  
**升级执行者：** Agent自动化升级
