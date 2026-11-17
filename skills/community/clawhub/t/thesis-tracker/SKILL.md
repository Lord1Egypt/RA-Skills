---
name: thesis-tracker
description: 投资论点追踪与验证。当用户要求"论点追踪""thesis tracker""投资逻辑""验证XX观点""跟踪XX判断"或需要持续追踪某个投资假设时触发。
---

# 投资论点追踪 Skill

## 触发条件
- "论点追踪" / "thesis tracker" / "投资逻辑" / "验证XX观点" / "跟踪XX判断"
- "我之前说XX会怎样，现在怎么样了"
- "帮我记一下这个投资逻辑"

## 数据存储
`<working_directory>/thesis-tracker/theses.json` — 所有论点的主索引

## 工作流程

### 新论点录入

#### 步骤1：提取论点结构
从用户表述中提取：
- **论点标题**：一句话描述（如"2026H2地产见底"）
- **核心假设**：支撑论点的关键假设列表（如"政策放松+销售拐点+估值极低"）
- **触发条件**：什么数据变化会确认/否定论点
- **时间窗口**：论点预期验证的时间范围
- **标的**：相关行业/ETF/个股

#### 步骤2：写入论点文件
更新 `theses.json`，格式：
```json
{
  "theses": [
    {
      "id": "T001",
      "title": "2026H2地产见底",
      "created": "2026-06-17",
      "assumptions": ["政策放松", "销售拐点", "估值极低"],
      "triggers_positive": ["30城销售面积周同比转正", "地产ETF连续5日净流入超5亿"],
      "triggers_negative": ["销售面积持续恶化", "龙头房企违约"],
      "time_window": "2026Q3-Q4",
      "targets": ["房地产ETF", "万科A"],
      "status": "pending",
      "checks": [
        {"date": "2026-06-17", "result": "pending", "summary": "销售面积仍负增长，政策预期升温"}
      ]
    }
  ]
}
```

#### 步骤3：IMA 同步
创建 IMA 笔记记录论点，标题：「投资论点{T001}: {标题}」

### 论点验证检查

#### 步骤1：读取论点列表
从 `theses.json` 获取所有 pending 状态的论点。

#### 步骤2：逐条数据验证
使用 `neodata-financial-search` 查询各论点对应的触发条件数据：
- 检查 triggers_positive 是否出现
- 检查 triggers_negative 是否出现

#### 步骤3：更新论点状态
- 如果 triggers_positive 全部出现 → status: "confirmed"
- 如果 triggers_negative 出现 → status: "negated"
- 部分出现 → status: "partial"
- 未出现 → status: "pending"

#### 步骤4：综合输出

```markdown
# 🎯 论点追踪报告 — {YYYY-MM-DD}

## 论点状态一览
| ID | 论点 | 状态 | 正向触发 | 负向触发 |
|----|------|------|----------|----------|
| T001 | 2026H2地产见底 | partial | 1/2 ✅ | 0/2 ✅ |
...

## 重点论点详情
### T001: 2026H2地产见底
- 状态：partial（部分验证）
- 正向进展：政策放松预期升温 ✅
- 未验证：销售拐点尚未出现 ❌
- 负向信号：无 ✅
- 下次检查建议：关注6月销售数据

## 新论点建议
[基于当前市场状态，建议用户考虑的新论点]
```

### 论点回顾（定时任务模式）

cron 可定期触发论点验证检查，建议频率：每周一次。

## 约束
- 单论点控制在 300 字
- 论点总数建议不超过15个（太多难以深度追踪）
- status 只有4种：pending / partial / confirmed / negated
- 已确认/已否定的论点保留30天后归档