# 工作流 4：更新人才库信息

**触发**：用户说「更新XXX的备注」「给XXX加个面试摘要」「把XXX的标签改成...」「XXX已经归档了」

> 首次存入候选人（含完整简历和聊天记录）参见 [workflow-2-save-candidate.md](workflow-2-save-candidate.md)。

## 步骤

### Step 1：定位候选人 record_id 及当前字段值

```bash
lark-cli base +record-list \
  --base-token <YOUR_BASE_TOKEN> \
  --table-id <YOUR_TALENT_TABLE_ID>
```
→ 按姓名匹配，取 record_id；同时读取当前字段值（用于参考，避免覆盖已有内容）

### Step 2：按用户要求更新对应字段

```bash
lark-cli base +record-upsert \
  --base-token <YOUR_BASE_TOKEN> \
  --table-id <YOUR_TALENT_TABLE_ID> \
  --record-id <record_id> \
  --json '{"<字段名>": "<新值>"}'
```

> 只传需要更新的字段，其他字段保持不变。

---

## 常用字段速查

| 字段名 | field_id | 类型 | 说明 |
|---|---|---|---|
| 姓名 | fldl1tEw1b | text | |
| 岗位 | fldGHnocrM | select(单) | 字符串 |
| 标签 | fldxv8TGk9 | select(多) | 字符串数组 `["tag1","tag2"]` |
| 联系方式 | fldORXX95d | text | |
| 作品集 | fldJY7XaWB | text | 每行一条带标题的链接 |
| AGENT总结 | fldhdL7B9X | text | MD 格式，参见 workflow-2 模板 |
| 备注 | fldMErJmKY | text | 人类手动备注 |
| 面试摘要 | fldindcQ0O | text | |
| 归档 | fldjA6sj0f | checkbox | `true` / `false` |
| 标记 | fldHUNPTFm | select(单) | 字符串 |
| 最后沟通时间 | fldNjou67w | datetime | Unix 毫秒时间戳（整数） |
| uid | flda7kISKJ | text | 一般不需要改 |
