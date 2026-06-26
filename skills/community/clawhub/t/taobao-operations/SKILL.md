---
name: taobao-operations
slug: taobao-operations
version: 1.0.0
description: "日常运营 + 客服售后 + 合规风控三合一 - 仅读 API、不自动修改、客服合规、人工确认"
changelog: "v1.0.0 初始版本：日常运营、客服售后、合规风控三合一"
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":["python3"],"python_deps":["requests","pandas","openpyxl"]},"os":["win32"]}}
---

# 日常运营 + 客服售后 + 合规风控三合一 Skill

## ⚠️ 重要安全声明

**本技能严格遵守以下安全铁律：**

1. **仅读 API 数据** - 仅通过淘宝官方 API 获取自身店铺、公开行业数据
2. **不自动修改** - 仅生成报告、建议、清单，所有修改人工确认执行
3. **客服合规回复** - 开头明确告知智能客服，仅 3 类低风险售后自动处理
4. **人工确认执行** - 所有操作必须人工审核后手动执行
5. **2026 新规合规** - 100% 符合淘宝最新规则，零违规风险

---

## 功能概述

### 三大核心模块

| 模块 | 功能 | 输出物 | 人工确认 |
|------|------|--------|----------|
| **日常运营辅助** | 数据汇总/合规巡检/库存同步 | 日报/巡检报告/补货提醒 | ✅ 必须 |
| **客服售后自动化** | 智能回复/订单触达/售后处理 | 客服日志/售后记录 | ✅ 部分 |
| **合规风控预警** | 风险分级/API 监控/应急预案 | 预警通知/应急预案 | ✅ 必须 |

---

## 使用命令

```bash
# 每日运营日报
python scripts/operations_main.py daily-report --日期 2026-03-26

# 全店合规巡检
python scripts/operations_main.py compliance-check --全店

# 库存同步
python scripts/operations_main.py inventory-sync --款号 KZ20260326

# 每日操作清单
python scripts/operations_main.py task-list --日期 2026-03-26

# 客服自动回复
python scripts/operations_main.py cs-auto-reply --启动

# 售后处理
python scripts/operations_main.py after-sales --订单 ID 12345 --自动处理

# 合规风控检查
python scripts/operations_main.py risk-check --实时
```

---

## 输出物

1. **《每日店铺运营日报》** - Excel 格式
2. **《全店合规巡检报告》** - Excel 格式
3. **《补货提醒通知》** - Excel 格式
4. **《每日运营关键操作清单》** - Excel 格式
5. **客服回复日志** - JSON 格式
6. **《售后处理记录》** - Excel 格式
7. **《合规风控预警通知》** - Excel 格式

---

## 安全与合规声明

**本技能不会：**
- ❌ 超范围调用 API
- ❌ 抓取非公开数据
- ❌ 自动修改商品信息
- ❌ 自动修改订单信息
- ❌ 自动修改店铺配置
- ❌ 客服回复不告知身份
- ❌ 自动处理高风险售后

**本技能仅支持：**
- ✅ 读取自身店铺数据
- ✅ 读取公开行业数据
- ✅ 生成报告/建议/清单
- ✅ 客服合规回复
- ✅ 3 类低风险售后自动处理
- ✅ 合规风控预警

---

*🛡️ 日常运营 + 客服售后 + 合规风控 — 合规第一，人工确认*
