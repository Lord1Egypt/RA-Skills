---
name: travel-biz
displayName: TravelBiz 差旅报销助手
slug: travel-biz
description: "差旅报销一条龙——行程规划→费用记录→发票扫描→报销单生成。融合 Travel + Expense + Receipt + Invoice 四大技能，出差人员的全流程AI助手。适合商务人士、销售、自由职业者。"
version: "1.0.0"
author: "智美人团队"
tags:
  - travel
  - expense
  - receipt
  - invoice
  - business
  - reimbursement
  - finance
metadata:
  openclaw:
    emoji: "✈️"
    requires:
      skills: [travel, expense, receipt, invoice]
---

# ✈️ TravelBiz 差旅报销助手

**出差一条龙：从订行程到拿报销款，全程AI搞定。**

## 融合来源

| 源技能 | 融合点 |
|--------|--------|
| travel | 行程规划、交通住宿预订、旅行建议 |
| expense | 费用记录、分类统计、预算控制 |
| receipt | 发票识别、OCR扫描、票据管理 |
| invoice | 发票生成、税种计算、支付追踪 |

## 完整流程

```
出差前               出差中                 出差后
  │                    │                      │
  ▼                    ▼                      ▼
┌──────┐    ┌──────────────┐    ┌────────────────┐
│行程  │───▶│费用记录       │───▶│报销单一键生成    │
│规划  │    │发票扫码       │    │+ 审批流程       │
│订票  │    │预算提醒       │    │+ 财务归档       │
│订酒店│    │超标预警       │    │+ 数据分析       │
└──────┘    └──────────────┘    └────────────────┘
```

## 能力

### 1. 出差前：行程规划
- 目的地天气/时差提醒
- 交通方案比价（机票/高铁/租车）
- 酒店推荐（预算内+位置最优）
- 行程日历自动同步

### 2. 出差中：费用管理
- 扫码录发票（继承receipt能力）
- 费用自动分类（交通/住宿/餐饮/其他）
- 预算剩余提醒
- 超标预警（超预算80%时提醒）

### 3. 出差后：报销一键生成
- 自动汇总所有费用
- 生成报销单（继承invoice能力）
- 税种自动计算
- 按公司模板格式化
- 导出PDF/Excel

## 使用方式

```
# 出差前规划
travel-biz> 规划出差 北京→上海 3天 预算3000

# 出差中记录
travel-biz> 录发票（拍照/上传）
travel-biz> 记录一笔餐饮费 ¥128

# 出差后报销
travel-biz> 生成报销单
travel-biz> 导出 本月所有报销
```

## 存储结构

```
~/travel-biz/
├── trips/                    # 出差记录
│   └── {日期}_{目的地}/
│       ├── plan.md           # 行程计划
│       ├── expenses.md       # 费用明细
│       ├── receipts/         # 发票图片
│       └── reimbursement.md  # 报销单
├── templates/                # 报销模板
│   └── company_{公司名}.md
└── reports/                  # 月度报表
    └── {年月}.md
```
