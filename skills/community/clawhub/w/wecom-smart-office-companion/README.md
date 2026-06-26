# 企业微信智能办公助手 (wecom-smart-office-companion)

> 每日自动汇总日程、会议、待办和团队数据，生成可视化早报卡片

## 业务场景

企业中高层管理者每天面临信息碎片化问题：
- **日程**在企业微信日程应用
- **会议**分散在会议室系统
- **待办**在各个项目管理工具中
- **团队数据**在智能表格里

每次查看完整信息需要切换4-5个应用，效率极低。本 Combo 一次查询全部数据，生成统一的智能早报。

## 痛点分析

| 痛点 | 现状 | 理想状态 |
|------|------|---------|
| 信息分散 | 5个应用来回切换 | 一个卡片看清全天 |
| 日程冲突 | 人工检查重叠时间 | 自动检测并提示 |
| 待办遗漏 | 靠记忆或手动追 | 按优先级强制排序 |
| 数据滞后 | 团队进度靠群消息 | 实时拉取智能表格 |

## Skill 编排图谱

```
[wecom-schedule] ──┐
                   ├──→ [数据聚合引擎] ──→ [card-renderer] ──→ 📱 早报卡片
[wecom-meeting-query] ─┤
[wecom-get-todo-list] ──┤
[wecom-get-todo-detail] ┘
[wecom-smartsheet-data] ──→ [团队数据快照]
```

### 技能详解

| Skill | 职责 | 输入 | 输出 |
|-------|------|------|------|
| wecom-schedule | 查询今日日程 | 日期范围 | 日程列表（时间/地点/参与人） |
| wecom-meeting-query | 拉取会议列表 | 日期过滤 | 会议详情+确认状态 |
| wecom-get-todo-list | 获取全部待办 | 排序规则 | 按优先级排序的待办列表 |
| wecom-get-todo-detail | 读取重点待办详情 | 待办ID | 详细内容+截止时间 |
| wecom-smartsheet-data | 读取团队智能表格 | docid/URL | 关键指标数据 |
| card-renderer | 渲染可视化卡片 | 聚合数据 | PNG卡片图片 |

## 工作流程

### Step 1：日程查询（wecom-schedule）
```python
# 查询今日全部日程
wecom_mcp.schedule.list(start_time, end_time)
# → 返回时间、地点、参与人列表
```

### Step 2：会议拉取（wecom-meeting-query）
```python
# 过滤今日会议
wecom_mcp.meeting.list(date=today)
# → 标注已确认/待定状态
```

### Step 3：待办汇总（wecom-get-todo-list）
```python
# 按截止时间排序
wecom_mcp.todo.list(sort_by="due", order="asc")
# → 紧急→重要→常规排序
```

### Step 4：团队数据（wecom-smartsheet-data）
```python
# 读取关键智能表格
wecom_mcp.smartsheet.get_records(docid, table_id)
# → 项目进度/OKR/风险指标
```

### Step 5：卡片渲染（card-renderer）
```python
# 生成 Mac Pro 风格早报
card-renderer --style mac-pro --input data.json --output morning-brief.png
```

## 使用示例

### 场景一：手动触发早报
```
用户：帮我生成今天的早报
AI：正在汇总日程、会议、待办和团队数据...
     → 查询 wecom-schedule ✓
     → 查询 wecom-meeting-query ✓
     → 查询 wecom-get-todo-list ✓
     → 读取 wecom-smartsheet-data ✓
     → 渲染早报卡片...
[发送卡片图片]
```

### 场景二：定时自动执行（推荐）
```json
{
  "schedule": "0 7 * * *",
  "tz": "Asia/Shanghai",
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行 wecom-smart-office-companion，生成今日早报并发送至飞书"
  }
}
```

## 变现路径（企业版）

- **SaaS订阅**：企业按席位付费，30-99元/人/月
- **定制开发**：为大型企业定制企业微信RPA早报系统
- **数据洞察包**：在早报中加入行业数据订阅（额外收费）

## 适用人群

- 企业中高层管理者（CEO/VP/总监）
- 项目经理/PMO
- 需要每日全面掌握团队状态的运营负责人
- 习惯用视觉化方式获取信息的知识工作者
