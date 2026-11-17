# 报销查询与展示

### 查看报销申请状态
```bash
python scripts/query_fee_requests.py
python scripts/query_fee_requests.py --state 审批中 --with-progress
```
→ 查询当前用户的报销/费用申请；`--with-progress` 会展开返回申请的流程历史与当前节点。可用 `--start-date`、`--end-date`、`--page`、`--size` 和 `--json`。日期筛选须传完整时间：`--start-date "<YYYY-MM-DD> 00:00:00" --end-date "<YYYY-MM-DD> 23:59:59"`；服务端按 `yyyy-MM-dd HH:mm:ss` 解析，纯日期会被拒绝。

### 报销耗时与完成提醒

- 查询耗时先读 `--with-progress --json`，分别计算申请 `createdTime` 至今、本轮流程 `startEvent.createTime` 至今，以及各 `userTask` 的起止时间；待办节点用当前时间代替 `endTime`。使用带明确时区的实际当前时间与代码计算，不心算。
- 申请创建与本轮流程启动不一致时，同时说明两种口径；不能把两者之间的空档归责给某位审批人，也不能假定本轮历史包含此前审批。默认注明自然时间、包含周末与节假日；未结束只能说“已耗时”，不能声称总处理耗时或预计到账。
- 完成提醒固定追踪用户指定的申请 ID，而非每次重新选“最新一笔”；审批中静默，审批通过才报通过，驳回等结果单独说明。审批通过不等于打款到账。
- 建立定时提醒须实际运行查询并读回任务配置，明确检查频率、时区和通知渠道；不要声称已经验证尚未发生的完成通知。实施步骤见 [报销完成监控](reimbursement-monitoring.md)。

### 报销查询输出约定

- 审批中用 `⏳`，已通过用 `✅`，已驳回用 `❌`，待提交用 `📝`。
- 默认不展示申请 ID、流程实例 ID、项目 ID 等内部标识。
- 不使用竖线压缩多个字段，也不在每行重复“状态”标签；移动端按两行一条记录展示。

#### 询问最新报销、状态或审批人

固定使用以下结构；“金额 + 状态”整行加粗。审批中展示节点和审批人，其他状态可省略这两行；公司不是必需字段，不默认展示。

```markdown
💰 最新报销

**¥{sumAmount}　{statusEmoji} {statusText}**

📁 项目：{projectName}
🔄 当前节点：{activityName}
👤 审批人：{assigneeName}
🕒 申请时间：{createdTime}
```

示例：

```markdown
💰 最新报销

**¥669.92　⏳ 审批中**

📁 项目：{projectName}
🔄 当前节点：商务负责人
👤 审批人：<审批人姓名>（<岗位>）
🕒 申请时间：2026-09-10 18:01
```

#### 询问历史申请记录、有哪些报销

标题后展示“项目 · 共 N 笔”，该汇总行加粗。每笔记录固定两行：第一行是序号、日期和金额，第二行是公司与状态；记录之间空一行。若项目不一致，则汇总行只写“共 N 笔”，并在每条记录第二行补充项目。驳回原因可另起第三行展示。

```markdown
💰 报销申请记录

**{projectName} · 共 {count} 笔**

1. {date}　¥{sumAmount}
{companyName} · {statusEmoji} {statusText}

2. {date}　¥{sumAmount}
{companyName} · {statusEmoji} {statusText}
```

示例：

```markdown
💰 报销申请记录

**{projectName} · 共 7 笔**

1. 2026-09-10　¥669.92
<公司名称> · ⏳ 审批中

2. 2026-06-18　¥411.20
<公司名称> · ✅ 已通过
```
