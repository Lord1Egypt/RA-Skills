# Step 6: 收件箱与回信

## 当前定位

这一部分当前分成两层：

- **稳定能力**：收件箱列表、邮件详情、对话详情、手动回信
- **保守型辅助能力**：reply assist / auto-reply 相关链路

对外使用时，建议把 **收件箱查看 + 人工确认后回信** 作为主路径。  
`reply assist` 当前按保守型辅助能力描述，不建议把它作为激进自动回复能力对外承诺。

---

## 核心接口

| 功能 | API | 方法 |
|------|-----|------|
| 收件箱列表 | `/email/selInboxClaw` | POST |
| 邮件详情 | `/email/inboxDetailClaw/{id}` | GET |
| 对话详情 | `/email/inboxDialogueClaw` | POST |
| 回复邮件 | `/email/writeMultipleEmailClaw` | POST |

---

## 稳定主链路

### 1. 收件箱列表

```bash
python3 scripts/inbox.py list --page 1 --page-size 20
python3 scripts/inbox.py list --is-read 1 --page-size 50
python3 scripts/inbox.py list --is-reply 0 --page-size 20
python3 scripts/inbox.py list --blogger-name "xxx" --page-size 20
```

关键字段：
- `id`：邮件 ID
- `chatId`：会话 ID
- `bloggerId`：达人 ID
- `subject`
- `cleanContent`
- `isRead`
- `isReply`

### 2. 邮件详情

```bash
python3 scripts/inbox.py detail 12345
```

适合在需要查看单封邮件完整内容、附件、抄送信息时使用。

### 3. 对话详情

```bash
python3 scripts/inbox.py dialogue "chatId_xxx"
```

适合在正式回复前先查看同一会话下的完整历史邮件。

### 4. 手动回信

```bash
python3 scripts/inbox.py reply \
  --blogger-ids "besId_xxx" \
  --reply-id 12345 \
  --subject "Re: Collaboration" \
  --content "<p>Hi ...</p>"
```

关键规则：
- `replyId` 必填
- `bloggerId` 必填
- **单个 `replyId` 只能对应单个 `bloggerId`**
- `content` 可以是 HTML，也可以是纯文本；脚本层会按接口要求发送

---

## 推荐操作顺序

1. 先用 `inbox.py list` 找到需要处理的邮件
2. 用 `inbox.py detail` 看单封详情
3. 用 `inbox.py dialogue` 看完整上下文
4. 生成人工确认过的回复主题和正文
5. 用 `inbox.py reply` 发出回复

这个顺序更符合当前 skill 的稳定边界，也能避免把未完成收口的 reply assist 子链路暴露给外部用户。

---

## 回复辅助能力说明

仓库里仍保留了 `monitor_inbox.py`、`reply_handler.py`、`reply_pipeline.py` 等回复辅助相关实现，但当前文档不把它们当成激进自动回复主入口。

如果你要在内部继续打磨 reply assist，建议遵守下面三条：

1. 必须基于完整 `chatId` 历史上下文，不要只看最后一封邮件
2. 语义理解、风险判断、回复意图分类应优先借用宿主模型；skill 内的规则分类只能作为 fallback
3. 新接入默认优先使用 canonical 字段 `replyModelAnalysis`；历史兼容字段如 `conversationAnalysis` 仅保留迁移吸收，不应继续扩散
4. 涉及价格、合同、物流、付款、排期承诺时，默认人工审核
5. 自动回复只能作为白名单增强能力，不能作为默认公开路径
