# 工作流：约面试

**触发**：用户说「帮我给XXX约个面试」「约一下XXX」

---

## 完整流程

### Step 1：定位候选人（从人才库）

```bash
lark-cli base +record-list \
  --base-token <YOUR_BASE_TOKEN> \
  --table-id <YOUR_TALENT_TABLE_ID>
```
→ 按姓名匹配，取 record_id 和候选人基本信息（姓名、作品集、岗位）

### Step 2：在 Boss直聘 发送约面试消息

> ⚠️ **发送前必须确认候选人存在，找不到绝对不发。opencli 命令严格串行。**

消息语言要自然，像人说的，不要啰嗦。参考：

```
哈喽，我们看了您的作品集和简历，方便约个视频会议聊聊吗？
```

```bash
# 1. 获取聊天列表，找到 uid（已在 Step 1 完成，可复用）
opencli boss chatlist

# 2. 确认对话存在
opencli boss chatmsg <uid>

# 3. 发送邀约消息
opencli boss send <uid>
```

### Step 3：写入决策记录

```bash
lark-cli base +record-upsert \
  --base-token <YOUR_BASE_TOKEN> \
  --table-id <YOUR_DECISION_TABLE_ID> \
  --json '{"记忆":"约面试 · 已发送视频会议邀请，等待候选人回复","标签":"约面试","对应人才":["<record_id>"]}'
```

### Step 4：启动 30 分钟心跳检测

执行以下指令创建定时任务，每 30 分钟检查候选人是否回复：

> 使用 CronCreate 工具，cron 表达式 `*/30 * * * *`，prompt 内容：
>
> "用 opencli boss chatmsg `<uid>` 查看最新消息，判断候选人是否有新回复。如果有明确的回复（同意/拒绝/给出时间），执行约面试流程的 Step 5。如果无新回复，静默等待下次检查。"

心跳任务详见 [heartbeat_task.md](heartbeat_task.md)。

---

### Step 5：候选人回复后 —— 确认面试时间

**5a. 查看使用者日程**（参见 [util-check-calendar.md](util-check-calendar.md)）

```bash
lark-cli calendar +agenda --start "<今天>" --end "<5天后>"
```
→ 找出 11:00—19:00 之间、无冲突的时间段，准备 2—3 个候选时间

**5b. 直接在当前对话中回复使用者，等待确认**

> 用户通过 Openclaw Channels 与 Agent 对话，无需发飞书消息——直接在对话里输出确认请求即可。

输出格式参考：
```
候选人 <姓名> 回复了，有面试意向！

根据您的日程，建议以下时间：
• <选项1>（如：4月3日 周四 14:00）
• <选项2>（如：4月4日 周五 10:00）
• <选项3>（如：4月7日 周一 15:00）

请确认哪个时间OK，确认后我去通知对方并创建日程。
```

**5c. 等待使用者在当前对话回复确认**

---

### Step 6：使用者确认时间后 —— 回复候选人

在 Boss直聘 回复确认的时间：

```
那这周X X点OK不？可以的话稍后我给您发日程链接。
```

等候选人确认后：

```
好的，稍后见！这是飞书视频会议链接：[链接]
```

---

### Step 7：创建飞书日程 + 获取会议链接

```bash
# 创建日程（返回 event_id）
lark-cli calendar +create \
  --summary "面试：<候选人姓名>（新媒体编导）" \
  --start "<日期>T<时间>:00+08:00" \
  --end "<日期>T<时间+45min>:00+08:00" \
  --description "Boss直聘候选人视频面试" \
  --attendee-ids "<YOUR_OPEN_ID>"

# 用 event_id 获取日程详情，取出飞书视频会议链接
lark-cli calendar events get \
  --params '{"calendar_id":"primary","event_id":"<event_id>"}'
```

→ 从返回结果中提取：
- `vchat.meeting_url`：飞书视频会议链接，**发给面试者**
- `app_link`：日程详情链接（内部查看用）

> 注意：`calendar_id` 直接用 `"primary"` 即可，lark-cli 会自动解析。

### Step 8：更新决策记录（面试已约好）

```bash
lark-cli base +record-upsert \
  --base-token <YOUR_BASE_TOKEN> \
  --table-id <YOUR_DECISION_TABLE_ID> \
  --json '{"记忆":"面试已约好 · <日期 时间>，视频会议","标签":"约面试","对应人才":["<record_id>"]}'
```

---

## 话术参考

| 场景 | 参考话术 |
|---|---|
| 初次邀约 | 哈喽，我们看了您的作品集和简历，方便约个视频会议聊聊吗？ |
| 候选人同意，确认时间 | 那这周五下午2点OK不？可以的话稍后我给您发日程链接。 |
| 候选人确认，发链接 | 好的，稍后见！这是飞书视频会议链接：<vchat.meeting_url> |
| 候选人拒绝/无意向 | 好的没关系，有需要随时联系~ |
