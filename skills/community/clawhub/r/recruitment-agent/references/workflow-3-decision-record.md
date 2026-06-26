# 工作流 3：人才决策记录

**触发**：用户说「对XXX做决策记录」「记一下要约XXX面试」「把XXX归档」「发Offer给XXX」「跟进一下XXX」

## 步骤

### Step 1：定位候选人 record_id

```bash
lark-cli base +record-list \
  --base-token <YOUR_BASE_TOKEN> \
  --table-id <YOUR_TALENT_TABLE_ID>
```
→ 按姓名或 uid 在返回数据中匹配，取对应的 `record_id_list[i]`

### Step 2：写入决策记录

```bash
lark-cli base +record-upsert \
  --base-token <YOUR_BASE_TOKEN> \
  --table-id <YOUR_DECISION_TABLE_ID> \
  --json '{"记忆":"<决策详情>","标签":"<决策类型>","对应人才":["<record_id>"]}'
```

> 注意：`时间` 字段为自动创建时间，无需手动填写。

---

## 字段说明

| 字段名 | field_id | 类型 | 说明 |
|---|---|---|---|
| 记忆 | fldF7y6wXa | text | 言简意赅的决策详情 |
| 标签 | fldGuUf5ml | select(单) | 决策类型，见下方选项 |
| 对应人才 | fldd8Wa2i2 | link | 双向关联，填人才库V3 的 record_id 数组 |
| 时间 | fldYygiaJS | created_at | 自动填入，无需手动 |

---

## 决策类型与记忆格式

| 决策类型 | 记忆格式示例 |
|---|---|
| 加入人才库 | `加入人才库 · [候选人亮点一句话，如：自由导演10年，金雀奖作品，已获取微信]` |
| 约面试 | `约面试 · [时间/形式] · [主要考察点]` |
| 跟进 | `跟进 · [跟进内容或待确认问题]` |
| 发Offer | `发Offer · [薪资范围/岗位/期望入职时间]` |
| 归档 | `归档 · [原因：不符合需求 / 候选人无意向 / 长期备用等]` |
