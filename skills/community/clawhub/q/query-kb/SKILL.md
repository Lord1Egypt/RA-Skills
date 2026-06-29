---
name: query_kb
description: Answer questions from personal and team knowledge bases with strict source grounding, no-answer behavior when the knowledge base lacks evidence, answer validation, and query logging.
---

# Skill: query_kb - 来源约束知识库查询

## 用途

基于个人知识库、团队知识库、项目空间或跨库范围回答问题。所有回答必须依赖知识库来源；知识库没有答案时直接说明没有答案，不补通用知识。

## 触发条件

Activate when:

- 用户问“我之前/我们团队/某项目/某人/知识库里有没有……”
- 用户要求查询会议、实验、论文、项目进展、人物贡献
- 用户追问依赖已存知识库内容

Do NOT activate when:

- 用户要存资料，交给 `ingest_document`
- 用户要批量编译资料源，交给 `batch_compile`
- 用户要写综述/研究缺口/实验建议，交给 `kb_review`

## 执行流程

### 1. 解析查询范围

OpenClaw 字段映射：

- `SenderId`：发消息的人 open_id
- `ChatType`：`direct` 或 `group`
- `GroupSubject`：群聊 chat_id；私聊为空

```bash
python3 scripts/resolve_scope.py \
  --sender_id <SenderId> \
  --chat_type <ChatType> \
  --chat_id <GroupSubject> \
  --question "<用户问题>"
```

范围规则：

- 私聊：`SenderId -> users.json -> 个人库 / 用户所属团队`
- 群聊：`GroupSubject -> chat_bindings.json -> team_id -> 团队库`
- 群聊未绑定团队：不回答知识问题，提示管理员绑定本群
- 群聊默认只查团队知识库，不查个人知识库
- 群聊中问“我/我的/个人资料”：拒绝并提示私聊查询
- 私聊中“我/我的/我之前” -> 个人库
- 私聊中“我们/团队/组会/成员/项目” -> 团队库
- 私聊范围不明确 -> 同时查个人库和团队库目录
- 项目问题优先读项目聚合页
- 人物问题优先读 `people/<姓名>.md`

### 2. 读取目录

```bash
python3 scripts/kb_list.py --owner <owner> --repo <repo> --kind all
```

### 3. OpenClaw 判断相关页

优先级：

- 项目问题：`projects/<project>/index/timeline/decisions/open_questions/people`
- 人物问题：`people/<姓名>.md`
- 概念问题：`concepts/`
- 资源问题：`resources/`
- 资料问题：`summaries/`

### 4. 精读页面

```bash
python3 scripts/kb_read.py --owner <owner> --repo <repo> --path "<page path>"
```

### 5. 生成回答

回答只能基于精读内容。

必须包含：

```text
来源：
1. 《页面名》（个人知识库/团队知识库/项目）链接
```

没有命中：

```text
我在知识库中没有找到与「xxx」相关的资料，因此无法基于知识库回答。

来源：无
```

资料不足：

```text
我找到了相关资料，但其中没有足够信息回答该问题，因此目前不能得出结论。

来源：
1. 《页面名》链接
```

### 6. 回答前校验

发送给用户前必须调用：

```bash
python3 scripts/validate_answer.py --answer_file /tmp/paperkb/answer.md \
  --allowed_sources_file /tmp/paperkb/read_pages.json
```

校验规则：

- 缺少 `来源：` 直接失败。
- 非“没有答案”场景下，来源不能为空。
- “没有答案”场景也必须显式写 `来源：无`。
- “没有答案”场景不能列出知识库页面作为来源；如果读到相关页面但信息不足，应使用“资料不足”话术并列出实际来源。
- 如果传入 `allowed_sources` 或 `allowed_sources_file`，回答中的来源必须来自本次实际读取的页面。

### 7. 写查询日志

查了哪个库就写哪个库；跨库两个都写：

```bash
python3 scripts/log_query.py --owner <owner> --repo <repo> \
  --open_id <SenderId> --question "<用户问题>" --scope "<scope>" --hits "<命中页面>"
```

## 脚本清单

- `resolve_scope.py`：判断个人库/团队库/跨库范围
- `chat_context.py`：解析 OpenClaw 群聊上下文和群绑定
- `kb_list.py`：读取目录
- `kb_read.py`：读取具体页面
- `validate_answer.py`：机械校验回答是否满足来源约束
- `log_query.py`：记录查询日志
