# TimeFriend 时迹 — 时间记录 Skill

通过自然语言向 TimeFriend 记录时间、写复盘日记、创建待办，并查询今日统计。

## 配置

在 OpenClaw 环境变量中设置：

```
TIMEFRIEND_TOKEN=tf_你的Token（在 timefriend.xin 设置页生成）
```

## 支持的操作

### 1. 记录时间

**触发词**：用户说"记录时间"、"刚才做了什么"、"帮我记一下"

调用：
```
POST https://timefriend.xin/api/records
Authorization: Bearer {TIMEFRIEND_TOKEN}
Content-Type: application/json

{
  "content": "活动名称",
  "startTime": "2026-03-11T08:00:00+08:00",
  "endTime":   "2026-03-11T09:30:00+08:00",
  "tags": ["标签1", "标签2"]
}
```

**自然语言解析规则**：
- "8:00-9:30 读书 #学习" → content=读书, tags=["学习"]
- "今天下午3点到5点开会 #工作/项目" → 换算为当天具体时间, tags=["工作", "项目"]
- 标签以 # 开头，多级用 / 分隔
- 时间默认为今天；若用户说"昨天"则用前一天日期
- **默认时区：北京时间（UTC+8）**，所有口语时间按北京时间解析后提交
- 成功后回复：✅ 已记录：{content} {startTime}-{endTime}

### 2. 写复盘日记（追加模式）

**触发词**：用户说"写日记"、"记录复盘"、"我今天的思考"、"追加到日记"、"记一下"（后面跟一段感想/思考类内容）

**逻辑（两步操作）**：

**第一步**：GET 今日已有内容
```
GET https://timefriend.xin/api/daily-reviews/{今日日期YYYY-MM-DD}
Authorization: Bearer {TIMEFRIEND_TOKEN}
```

- 如果返回 200：拿到 `data.content`（HTML 格式），准备追加
- 如果返回 404：今天还没有日记，从空内容开始

**第二步**：PUT 拼接后的完整内容
```
PUT https://timefriend.xin/api/daily-reviews/{今日日期YYYY-MM-DD}
Authorization: Bearer {TIMEFRIEND_TOKEN}
Content-Type: application/json

{
  "content": "{已有内容}{新段落}"
}
```

**拼接规则**：
- 新内容用 `<p>` 标签包裹：`<p>用户说的文字</p>`
- 若今天已有内容，直接在末尾拼接：`{existing_content}<p>新内容</p>`
- 若今天没有内容，直接发：`<p>新内容</p>`
- 内容原文存入，不做 AI 改写，保持用户的原始表达

成功后回复：📝 已追加到今日复盘（共 {wordCount} 字）

### 3. 创建待办任务（添加到待办清单）

**触发词**：用户说"添加待办"、"记一个任务"、"todo"、"加到待办"

调用：
```
POST https://timefriend.xin/api/todos
Authorization: Bearer {TIMEFRIEND_TOKEN}
Content-Type: application/json

{
  "title": "任务名称",
  "status": "pending"
}
```

成功后回复：✅ 待办已添加：{title}

### 4. 添加到收集箱

**触发词**：用户说"加到收集箱"、"放进收集箱"、"inbox"、"先收集一下"

收集箱和待办清单不同：收集箱用于临时存放想法/任务，不需要指定日期。

**逻辑（两步操作）**：

**第一步**：获取用户的收集箱分类列表
```
GET https://timefriend.xin/api/inbox-categories
Authorization: Bearer {TIMEFRIEND_TOKEN}
```

返回示例：
```json
{
  "success": true,
  "data": [
    { "id": 12, "name": "工作", "sortOrder": 0 },
    { "id": 13, "name": "想法", "sortOrder": 1 }
  ]
}
```

- 如果 `data` 为空数组：告知用户"你还没有创建收集箱分类，请先在 timefriend.xin 的收集箱页面创建一个分类"，终止操作
- 如果只有一个分类：直接使用该分类的 `id`
- 如果有多个分类：询问用户"你有以下收集箱分类：{分类名列表}，请问放到哪个？"，等用户选择后再继续

**第二步**：创建收集箱条目
```
POST https://timefriend.xin/api/todos
Authorization: Bearer {TIMEFRIEND_TOKEN}
Content-Type: application/json

{
  "title": "条目名称",
  "status": "pending",
  "categoryId": {第一步获取的分类id}
}
```

注意：收集箱条目**不需要** `taskDate` 字段（留 null 即可）。

成功后回复：📥 已加入收集箱「{分类名}」：{title}

### 5. 查询待办清单

**触发词**：用户说"今天有什么待办"、"我的任务"、"待办有哪些"、"查一下我的待办"

调用：
```
GET https://timefriend.xin/api/todos?taskDate=今天日期(YYYY-MM-DD)
Authorization: Bearer {TIMEFRIEND_TOKEN}
```

将返回的待办列表整理后告知用户，例如：
"今天有 3 个待办：✅ 整理会议纪要（已完成）、⏳ 写周报（未完成）、⏳ 回复邮件（未完成）"

- status 为 `pending` → 未完成
- status 为 `in-progress` → 进行中
- status 为 `completed` → 已完成

### 6. 查询收集箱

**触发词**：用户说"收集箱里有什么"、"查收集箱"、"我收集了什么"

**逻辑（两步操作）**：

**第一步**：获取收集箱分类名称（用于显示）
```
GET https://timefriend.xin/api/inbox-categories
Authorization: Bearer {TIMEFRIEND_TOKEN}
```

**第二步**：获取所有收集箱条目
```
GET https://timefriend.xin/api/todos?taskDate=null
Authorization: Bearer {TIMEFRIEND_TOKEN}
```

⚠️ **极其重要**：URL 中必须包含 `taskDate=null`（字面字符串 "null"），这是区分收集箱与普通待办的唯一依据。
- ✅ 正确：`/api/todos?taskDate=null`
- ❌ 错误：`/api/todos`（不带参数，会返回所有日期的待办，数量会远超实际收集箱条目数）
- ❌ 错误：`/api/todos?status=pending`（只过滤状态，不限制 taskDate，同样会混入普通待办）

返回的每条数据包含 `categoryId`，对照第一步的分类列表显示分类名。

**展示规则**：
- **只显示** `status` 为 `pending` 或 `in-progress` 的活跃任务
- **过滤掉** `status` 为 `cancelled` 或 `completed` 的条目
- 如果有 `completed` 的任务，在最后补一句："另有 X 条已完成，如需查看请告知"

整理后告知用户，例如：
"你的收集箱共有 5 条：
📁 工作：写一篇关于时间管理的文章、整理 Q1 复盘
📁 想法：买一本《心流》、学习 Swift 语言
📁 未分类：看牙医"

注意：`categoryId` 为 null 的条目显示为"未分类"。

### 7. 查询今日统计

**触发词**：用户说"今天记录了什么"、"查统计"、"今天怎么样"

调用：
```
GET https://timefriend.xin/api/records?date=今天日期(YYYY-MM-DD)
Authorization: Bearer {TIMEFRIEND_TOKEN}
```

将返回的记录列表整理后用自然语言告知用户，例如：
"今天共记录了 5 段时间，合计 6.5 小时。最长一段：工作/项目（3小时）。"

## 错误处理

- 401：Token 无效或已撤销，提示用户去 timefriend.xin 重新生成
- 400：参数错误，检查格式是否正确（若提示 `source not allowed`，请去掉 source 字段）
- 其他：提示"服务暂时不可用，请稍后再试"

## 示例对话

**用户**：帮我记一下今天早上 8 点到 9 点半读书，标签学习
**OpenClaw**：✅ 已记录：读书 08:00-09:30 #学习

**用户**：添加一个待办，整理会议纪要
**OpenClaw**：✅ 待办已添加：整理会议纪要

**用户**：把"买一本关于时间管理的书"加到收集箱
**OpenClaw**：（你有两个分类：工作、想法，请问放到哪个？）
**用户**：想法
**OpenClaw**：📥 已加入收集箱「想法」：买一本关于时间管理的书

**用户**：写日记，今天状态很好，上午专注工作了三小时，感觉效率很高，下午和团队开了个很有成效的会
**OpenClaw**：📝 已追加到今日复盘（共 42 字）

**用户**：再补充一下，晚上读了半小时书，感觉很放松
**OpenClaw**：📝 已追加到今日复盘（共 63 字）
