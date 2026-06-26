# CLI Agent Routing Examples (Published V1)

Use this reference for the **published V1 default examples**.
These examples assume Workhorse Duo is using real local agents:
- `xiaoma`
- `xiaoniu`

Default routing model:
- dispatch with `openclaw agent --agent xiaoma ...`
- dispatch with `openclaw agent --agent xiaoniu ...`
- keep the main session responsive
- do not require `sessions_send` as the default path

## 1. Example goals

These examples optimize for:
- fastest first use after bootstrap
- real agent dispatch instead of role-only prompts
- simple boss -> execute -> review flow
- non-blocking chat during worker execution

## 2. Example command defaults

Recommended V1 pattern:

```powershell
openclaw agent --agent xiaoma --message "<task packet>"
openclaw agent --agent xiaoniu --message "<qa packet>"
```

If you need to reuse existing worker context, add `--session-id <existing-session-id>`.
Do not make that the default teaching path unless context reuse is actually required.

## 3. Example 小马 packet

```powershell
openclaw agent --agent xiaoma --message "你是小马（执行位）。请按以下要求执行。

目标：检查当前 skill 目录结构，并指出发布版是否还残留本地专属路径或旧默认口径。
范围：只读检查，不修改文件。
约束：不要泛泛而谈，要列出具体文件和判断。
验收标准：给出清晰结论，并说明哪些文件还要继续收口。
补充要求：输出格式固定为：已完成 / 未完成 / 风险阻塞 / 建议下一步。" --json
```

## 4. Example 小牛 packet

```powershell
openclaw agent --agent xiaoniu --message "你是小牛（验收位）。请只做验收，不重做主体工作。

任务目标：确认小马是否正确判断该 skill 是否已达到发布版口径。
验收标准：判断结论是否具体、是否抓住关键文件、是否把建议和结论混淆。
小马产出摘要：<贴上小马摘要>
重点检查：SKILL.md、bootstrap、references 文档是否覆盖到。

输出规则：
- 通过：只回复‘验收没问题’
- 不通过：只列具体问题或未完成项" --json
```

## 5. Example smoke test

### Step 1 — xiaoma ping

```powershell
openclaw agent --agent xiaoma --message "你是小马（执行位）。请只回复：PONG" --timeout 120 --json
```

### Step 2 — xiaoniu ping

```powershell
openclaw agent --agent xiaoniu --message "你是小牛（验收位）。请只回复：PONG" --timeout 120 --json
```

### Step 3 — real loop

- send one tiny real task to `xiaoma`
- summarize it compactly for `xiaoniu`
- require `验收没问题` or a short issue list

If all three steps pass, the V1 published route is operational enough for real use.

## 6. Example reporting

### Accepted case

```text
小马已完成：已检查发布版关键文件，并确认默认路径已切到真实 agent + CLI agent routing。
小牛验收：没问题
```

### Rejected case

```text
小马已完成：已检查主文件与 references。
小牛验收未通过：
- examples 文档仍残留旧默认路径
- 风险/回滚说明不完整
```

## 7. Advanced note

Persistent worker architecture is still a V2 / advanced topic.
Do not let historical persistent-session assumptions leak back into the published V1 examples.
