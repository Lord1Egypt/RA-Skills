# 工作流 2：存入人才库

**触发**：用户说「把XXX存入人才库」「我对XXX感兴趣，帮我存入」

## 步骤（opencli 命令严格串行）

### Step 1：从 chatlist 找到候选人 uid

```bash
opencli boss chatlist
```
→ 按姓名匹配，记录 uid

### Step 2：获取聊天记录

```bash
opencli boss chatmsg <uid>
```
→ 提取：作品集链接（带标题）、联系方式（微信/手机）、最后沟通时间

### Step 3：获取简历

```bash
opencli boss resume <uid>
```
→ 提取：姓名、性别、年龄、学历、经验年限、工作经历、教育、期望方向

### Step 4：搜索人才库是否已有记录

```bash
lark-cli base +record-list \
  --base-token <YOUR_BASE_TOKEN> \
  --table-id <YOUR_TALENT_TABLE_ID>
```
→ 在返回的 `fields` 数组中找 `uid` 列索引，遍历 `data` 数组匹配 uid 值
→ **找到**：取对应 `record_id_list[i]`，进 Step 5a（更新）
→ **未找到**：进 Step 5b（新建）

### Step 5a：更新已有记录

对比新旧信息，AGENT 自行判断哪些字段有变化需要更新。

> 需要单独更新特定字段（不经过全流程）？参见 [workflow-4-update-candidate.md](workflow-4-update-candidate.md)。

```bash
lark-cli base +record-upsert \
  --base-token <YOUR_BASE_TOKEN> \
  --table-id <YOUR_TALENT_TABLE_ID> \
  --record-id <record_id> \
  --json '<fields_json>'
```

### Step 5b：新建记录

```bash
lark-cli base +record-upsert \
  --base-token <YOUR_BASE_TOKEN> \
  --table-id <YOUR_TALENT_TABLE_ID> \
  --json '<fields_json>'
```

---

## 字段映射

| 字段名 | field_id | 类型 | 数据来源 |
|---|---|---|---|
| 姓名 | fldl1tEw1b | text | resume.name |
| uid | flda7kISKJ | text | chatlist.uid |
| 岗位 | fldGHnocrM | select(单) | chatlist.job |
| 最后沟通时间 | fldNjou67w | datetime(Unix ms) | chatmsg 最后一条 time 转毫秒时间戳 |
| 联系方式 | fldORXX95d | text | chatmsg 中提取微信/手机号 |
| 作品集 | fldJY7XaWB | text | chatmsg 中的链接，每行一条（含标题） |
| AGENT总结 | fldhdL7B9X | text | 见下方 MD 格式模板 |
| 标签 | fldxv8TGk9 | select(多) | AGENT 自行判断，传字符串数组 |

---

## AGENT总结 MD 格式模板

```markdown
# 关键信息
- **姓名**：xxx · 性别 · 年龄
- **学历**：xxx（院校 · 专业 · 毕业年份）
- **经验**：xx年以上
- **当前状态**：自由职业 / 在职
- **期望方向**：岗位 · 城市
- **联系方式**：微信 xxxxxxxxxx

# 沟通现状
- **进展**：[一句话描述当前到了哪步，如：已获取联系方式 / 约面试中 / 初次接触]
- **最后沟通**：yyyy-mm-dd HH:mm:ss
- **对方态度**：[积极 / 观望 / 未响应]

# 作品与能力
- 🏆 [作品标题](url)（如有奖项/亮点标注）
- [作品标题](url)
- **技能**：[主要能力一句话描述]

# 工作经历
- yyyy.mm—至今：[公司] · [职位]
- yyyy.mm—yyyy.mm：[公司] · [职位]
```
