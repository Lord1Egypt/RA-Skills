# 用户工作分析报告模板

> 生成的报告应遵循以下结构，根据实际数据填充内容。

## 报告结构

```markdown
# 用户 {realname}（{account}）{年份}年工作分析报告

**生成时间**：{当前日期}  
**分析范围**：{start_date} 至 {end_date}  
**数据来源**：禅道项目管理系统（主表 + zt_action 操作日志）

---

## 一、用户基本信息

| 项目 | 内容 |
|------|------|
| 账号 | {account} |
| 姓名 | {realname} |
| 部门 | {dept} |
| 角色 | {role} |

---

## 二、工作概览统计

### 2.1 总体统计

| 类型 | 参与数 | 完成/解决数 | 完成率/解决率 | 总工时 |
|------|--------|------------|--------------|--------|
| 需求 | {story_total} | {story_done} | {story_rate}% | - |
| 任务 | {task_total} | {task_done} | {task_rate}% | {task_hours}h |
| Bug | {bug_total} | {bug_resolved} | {bug_rate}% | {bug_hours}h |

**总工时合计**：{total_hours}h

### 2.2 操作类型分布

| 对象类型 | 操作类型 | 次数 |
|---------|---------|------|
| story | opened | {cnt} |
| story | assigned | {cnt} |
| story | edited | {cnt} |
| task | opened | {cnt} |
| task | finished | {cnt} |
| task | closed | {cnt} |
| bug | opened | {cnt} |
| bug | resolved | {cnt} |
| bug | closed | {cnt} |

---

## 三、需求列表

### 3.1 参与的需求（按优先级排序）

| ID | 标题 | 优先级 | 状态 | 阶段 | 用户操作 | 创建人 | 指派人 |
|----|------|--------|------|------|---------|--------|--------|
| {id} | {title} | P{pri} | {status} | {stage} | {actions} | {openedBy} | {assignedTo} |

**说明**：
- 用户操作列展示该用户对此需求的所有操作（如 opened、assigned、edited、commented）
- 状态字段翻译为中文（active=激活、closed=已关闭、changed=已变更）

---

## 四、任务列表

### 4.1 参与的任务（按优先级排序）

| ID | 任务名称 | 优先级 | 状态 | 类型 | 预估(h) | 已消耗(h) | 剩余(h) | 完成人 | 用户操作 |
|----|---------|--------|------|------|---------|----------|---------|--------|---------|
| {id} | {name} | P{pri} | {status} | {type} | {estimate} | {consumed} | {left} | {finishedBy} | {actions} |

### 4.2 任务状态分布

| 状态 | 数量 | 占比 |
|------|------|------|
| done（已完成） | {cnt} | {rate}% |
| wait（未开始） | {cnt} | {rate}% |
| doing（进行中） | {cnt} | {rate}% |
| pause（已暂停） | {cnt} | {rate}% |
| cancel（已取消） | {cnt} | {rate}% |

### 4.3 任务类型分布

| 类型 | 数量 |
|------|------|
| design（设计） | {cnt} |
| devel（开发） | {cnt} |
| request（需求） | {cnt} |
| test（测试） | {cnt} |
| discuss（讨论） | {cnt} |

---

## 五、Bug 列表

### 5.1 参与的 Bug（按严重度排序）

| ID | Bug 标题 | 严重度 | 优先级 | 状态 | 解决方案 | 提交人 | 解决人 |
|----|---------|--------|--------|------|---------|--------|--------|
| {id} | {title} | {severity} | P{pri} | {status} | {resolution} | {openedBy} | {resolvedBy} |

### 5.2 Bug 严重度分布

| 严重度 | 数量 | 说明 |
|--------|------|------|
| 1 | {cnt} | 致命 |
| 2 | {cnt} | 严重 |
| 3 | {cnt} | 一般 |
| 4 | {cnt} | 轻微 |

### 5.3 Bug 解决方案分布

| 解决方案 | 数量 |
|---------|------|
| fixed（已解决） | {cnt} |
| postponed（延期处理） | {cnt} |
| duplicate（重复） | {cnt} |
| external（外部原因） | {cnt} |
| fixed | {cnt} |

---

## 六、工时统计

### 6.1 按对象类型统计

| 对象类型 | 对象 ID | 日期 | 消耗(h) | 剩余(h) | 工作内容 |
|---------|---------|------|---------|---------|---------|
| {objectType} | {objectID} | {date} | {consumed} | {left} | {work} |

**工时合计**：{total_consumed}h

### 6.2 按产品统计

| 产品 | 任务数 | 总工时(h) |
|------|--------|----------|
| {product_name} | {task_cnt} | {hours} |

---

## 七、月度工作趋势

### 7.1 月度操作统计

| 月份 | 对象类型 | 操作 | 次数 |
|------|---------|------|------|
| {month} | {objectType} | {action} | {cnt} |

### 7.2 月度工时趋势

| 月份 | 总工时(h) | 说明 |
|------|----------|------|
| {month} | {hours} | 柱状图数据 |

---

## 八、关键发现

### 8.1 工作亮点

- {highlight_1}
- {highlight_2}
- {highlight_3}

### 8.2 待改进项

- {improvement_1}
- {improvement_2}

### 8.3 建议

- {suggestion_1}
- {suggestion_2}

---

## 附录：数据说明

### A. 数据来源

本报告数据来自禅道数据库，包括：

1. **主表数据**：zt_story、zt_task、zt_bug、zt_effort
2. **操作日志**：zt_action（记录所有操作行为）
3. **字段变更**：zt_history（记录关键字段变更）

### B. 追踪方法

- 通过 `zt_action` 表的 `actor` 字段追踪用户所有操作
- 通过 `DISTINCT objectID` 去重，获取用户参与的所有对象
- 结合主表数据获取对象的完整信息

### C. 状态字段翻译

| 英文值 | 中文翻译 |
|--------|---------|
| active | 激活 |
| closed | 已关闭 |
| changed | 已变更 |
| resolved | 已解决 |
| fixed | 已解决 |
| postpone | 延期处理 |

---

**报告结束**
```

## 状态字段翻译对照表

### 需求状态（zt_story.status）

| 英文 | 中文 |
|------|------|
| active | 激活 |
| closed | 已关闭 |
| changed | 已变更 |

### 任务状态（zt_task.status）

| 英文 | 中文 |
|------|------|
| wait | 未开始 |
| doing | 进行中 |
| done | 已完成 |
| pause | 已暂停 |
| cancel | 已取消 |
| closed | 已关闭 |

### Bug 状态（zt_bug.status）

| 英文 | 中文 |
|------|------|
| active | 激活 |
| resolved | 已解决 |
| closed | 已关闭 |

### 任务类型（zt_task.type）

| 英文 | 中文 |
|------|------|
| design | 设计 |
| devel | 开发 |
| request | 需求 |
| test | 测试 |
| discuss | 讨论 |
| story | 需求 |
| bug | Bug |
| misc | 其他 |

### Bug 解决方案（zt_bug.resolution）

| 英文 | 中文 |
|------|------|
| fixed | 已解决 |
| postponed | 延期处理 |
| duplicate | 重复 |
| external | 外部原因 |
| fixed | 已修复 |
| bydesign | 设计如此 |

## 操作类型说明

| action | 含义 |
|--------|------|
| opened | 创建 |
| assigned | 指派 |
| started | 开始 |
| finished | 完成 |
| resolved | 解决 |
| closed | 关闭 |
| commented | 评论 |
| edited | 编辑 |
| linked2project | 关联项目 |
| linked2execution | 关联执行 |
