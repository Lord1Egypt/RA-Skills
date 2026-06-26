# Step 5: 发送邮件

## 核心接口

**发邮件接口：**
```
POST /email/writeMultipleEmailClaw            # 需校验权益
```

---

## 请求公共字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `currentUserId` | integer | 否 | 接口文档字段；当前 skill 脚本层不依赖也不暴露该字段 |
| `emails` | array | ✅ | 邮件数据数组 |
| `bloggerInfos` | array | ✅ | 博主信息数组 |
| `type` | integer | ✅ | 1=普通邮件; 2=定时邮件; 3=Gmail代发; 99=草稿 |
| `timing` | string | 定时必填 | 格式 `yyyy-MM-dd HH:mm:ss` |
| `replyId` | integer | 回复必填 | 回复邮件ID |
| `isReplyAll` | boolean | 否 | 是否回复所有抄送人，默认 false |
| `cc` | string | 否 | 抄送人，逗号拼接 |
| `taskId` | integer | 否 | 邮件类型，0=普通；正整数=自动邀约 |
| `nickName` | string | 否 | 昵称 |

---

## emails 数组元素

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `frontId` | string | 否 | 前端预先生成的邮件id |
| `templateId` | integer | 否 | 模版id |
| `id` | integer | 否 | 写信ID（有值为更新，否则为插入） |
| `subject` | string | ✅ | 主题 |
| `content` | string | ✅ | 正文（HTML或纯文本） |
| `attachments` | array | 否 | 附件列表 |
| `bloggerIds` | array | 否 | 该邮件对应的博主ID列表 |

### attachments 元素

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `link` | string | ✅ | 附件地址 |
| `size` | integer | ✅ | 附件大小 |
| `name` | string | 否 | 文件名 |
| `uuid` | string | 否 | uuid |

---

## bloggerInfos 数组元素

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `bloggerId` | string | ✅ | 博主id |
| `chooseSource` | integer | 否 | 添加来源，默认0 |
| `popularizePlanId` | integer | 否 | 推广计划id，无推广计划默认-1 |
| `popularizePlanName` | string | 否 | 推广计划名称 |
| `isFiltered` | boolean | 否 | 是否过滤，默认false |

---

## 使用脚本发送

### 单封邮件发送

```bash
python3 scripts/inbox.py send \
  --blogger-ids "besId123" \
  --subject "Partnership Opportunity" \
  --content "Dear xxx, we would like to collaborate..."
```

### 批量发送（多个博主，同主题同正文）

```bash
python3 scripts/inbox.py send \
  --blogger-ids "besId123,besId456,besId789" \
  --subject "Partnership Opportunity with Brand" \
  --content "Hi, we love your content and would like to collaborate..."
```

### 批量发送（多个邮件实体，从文件读取）

```bash
python3 scripts/inbox.py send --emails-file batch_send.json
```

`batch_send.json` 示例：

```json
{
  "emails": [
    {
      "subject": "Collab idea: Product A x Alice",
      "content": "Hi Alice, ...",
      "bloggerIds": ["besId123"]
    },
    {
      "subject": "Collab idea: Product A x Bob",
      "content": "Hi Bob, ...",
      "bloggerIds": ["besId456"]
    }
  ],
  "bloggerInfos": [
    { "bloggerId": "besId123", "chooseSource": 0, "popularizePlanId": -1 },
    { "bloggerId": "besId456", "chooseSource": 0, "popularizePlanId": -1 }
  ]
}
```

### 定时发送

```bash
python3 scripts/inbox.py send \
  --blogger-ids "besId123" \
  --subject "Partnership Opportunity" \
  --content "Dear xxx..." \
  --timing "2026-03-26 10:00:00"
```

## 响应格式

```json
{
  "code": "200",
  "message": "success",
  "data": {
    "groupId": 12345,
    "emails": [
      { "frontId": "xxx", "writeId": 111 },
      { "frontId": "yyy", "writeId": 112 }
    ]
  }
}
```

| 字段 | 说明 |
|------|------|
| `groupId` | 写信组ID |
| `emails[].frontId` | 前端邮件ID |
| `emails[].writeId` | 写信ID（可用于后续操作） |

---

## 与生成文案的衔接

`generate_outreach_emails.py` 输出 JSON 后，用桥接脚本一键发送。

**批量发送规则：** 如果有多个博主，优先使用单次 API 调用的批量发送方式；请求体中的 `emails` 与 `bloggerInfos` 可以同时装多个邮件实体，不要再按“一封邮件一次请求”串行发送。

```bash
# 先生成文案（先确认目标达人和署名，再生成）
python3 scripts/generate_outreach_emails.py --input search_result.json --cooperation sample --sender-name "Your Real Name" --limit 20 --output emails.json

# 一键批量发送（默认单次请求装多个邮件实体）
python3 scripts/send_generated_emails.py emails.json

# 试运行（只打印批量 payload，不发送）
python3 scripts/send_generated_emails.py emails.json --dry-run

# 限制发送数量（默认 200 封）
python3 scripts/send_generated_emails.py emails.json --limit 10

# 定时批量发送
python3 scripts/send_generated_emails.py emails.json --timing "2026-03-26 10:00:00"
```

**发送记录**：每次运行后会追加到 `~/.config/wotohub/logs/sent_log.json`（可通过 `WOTOHUB_STATE_DIR` 覆盖），记录批次摘要、发送状态、跳过项与响应结果，方便后续追踪。回复接口同理，也建议写入用户本地日志目录。

---

## Send Protocol（推荐）

统一 send protocol：
- `prepare_only`：仅准备发送候选与摘要，不执行发送
- `manual_send`：人工确认后再发送
- `scheduled_send`：仅用于定时场景；在 `scheduled_cycle` 下如未显式要求 review，且发送校验通过，会直接执行发送

新增质量护栏：
- 默认只允许发送 **host-model drafts**
- `fallback-script` 草稿默认只可预览，不可直接外发
- 如确需发送 fallback 草稿，必须显式开启 `allowFallbackSend=true` / `--allow-fallback-send`
- 不允许为了省步骤而把 fallback 草稿当成默认发送主链路

推荐发送摘要至少包含：
- 待发送数量
- blocked / skipped 数量
- 主题预览
- 是否定时发送
- 是否需要人工 review

发送前 guardrails：
- 标题不能为空
- 正文不能为空
- 英文场景下标题不应混入明显 CJK
- 标题尾部达人名与目标达人昵称不应错位
- opening greeting 与目标达人昵称不应错位

默认策略说明：
- 单次任务默认先 `prepare_only`
- 定时任务默认 `scheduled_send`
- 若只想演练定时链路不发信，显式设置 `sendPolicy=prepare_only`
- `scheduled_send` 在定时任务里就是默认真实发信；若不想真实发信，必须显式改成 `prepare_only`
- 单次 / 手动场景如需真实发送，仍应显式指定 send policy，不要把手动真实发信做成隐式默认
- 即使进入真实发送链路，默认也要求邮件来源是 `host-model drafts`；fallback 草稿需要额外显式授权

## 发信后必做动作

发信完成后，不要直接结束流程。必须继续询问用户：
- 希望多久扫描一次回信
- 是固定间隔（如每30分钟 / 每2小时）还是固定时间点（如每天9:00）
- 是否只扫描未读 / 未回复邮件

推荐提问示例：
- “邮件已经发出。你希望我按什么频率帮你扫描回信？比如每30分钟一次，或者每天上午9点和下午6点。”

在用户给出频率后，再进入收件扫描/提醒配置。

## 发送建议

1. **默认批量上限**：`send_generated_emails.py` 默认一次最多发送 200 封；可通过 `--limit` 调低，传 `--limit 0` 表示不额外限制
2. **默认搜索页大小**：搜索 API 默认 `pageSize=50`，脚本层最大不超过 200，避免请求过大
3. **发送间隔**：如需分批运营节奏控制，可由外层调度分轮执行；脚本默认优先单次批量请求
4. **每日上限**：建议结合账号风控和业务节奏自行配置，不再在脚本文档中硬编码较小默认值
5. **定时发送**：用 `--timing` 参数设置发送时间
6. **userId**：当前 `scripts/inbox.py` 不提供 `--user-id` 参数；如接口后续恢复该依赖，再单独补到脚本层，不在当前主链路中引入
