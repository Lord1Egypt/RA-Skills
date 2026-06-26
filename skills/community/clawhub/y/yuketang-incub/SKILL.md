---
name: yuketang
---

## 前置配置（只需一次）

### 第一步：获取 Secret

打开 <https://ykt-envning.rainclassroom.com/ai-workspace/open-claw-skill>，登录后复制你的个人 Secret。

> **没有配置 Secret？** 所有工具调用都会返回鉴权失败。请先完成上述步骤。

### 第二步：设置环境变量

**macOS / Linux：**
```
export YUKETANG_SECRET="你的Secret"
```

**Windows（PowerShell）：**
```
$env:YUKETANG_SECRET="你的Secret"
```

**Windows（CMD）：**
```
set YUKETANG_SECRET=你的Secret
```

### 第三步：运行安装脚本

**macOS / Linux：**
```
bash setup.sh
```

**Windows 或任何有 Node.js 的环境：**
```
node setup.js
```

> 具体配置文件路径取决于你使用的客户端（OpenClaw / CodeBuddy / Cursor 等），请参考对应文档。

### 第四步：验证

配置完成后，尝试问一句 **"我的雨课堂ID是多少"**。如果正常返回用户信息，说明配置成功。

---

## 触发场景

### 意图 → 工具 速查表

| 用户意图 | 调用工具 |
|----------|---------|
| 查询账号 / 我的ID / 雨课堂ID | `claw_current_user` |
| 查询我开的课 / 我教了哪些班 | `ykt_teaching_list` |
| 查询我的班级数据 / 班级教学数据 | `ykt_classroom_statistics` |
| 查询预警学生名单 / 重点关注学生 | `ykt_classroom_warning_overview` |
| 查询某个具体班级的预警学生名单 | `ykt_classroom_warning_student` |
| 今天上课情况总览 / 今天答题率 / 到课率 | `cube_teacher_today_teaching` |
| 预约开课 | `cube_lesson_reservation` |
| 查询我有哪些待批改的作业 / 考试 / 课堂/ 课件 | `ykt_teacher_correct_statistic` |
| 查询最近发布的作业 / 我在xx班发布的作业完成情况 /最近一次发布的作业完成情况 | `ykt_recent_exercise_submit` |
| 查询最近发布的公告 / 我在xx班发布的公告阅读情况 /最近一次公告的阅读情况 | `ykt_recent_notice_read` |
| 查询今天上课的情况/今天的课有多少人来上课了 | `cube_teacher_today_teaching_detail` |


### 不要触发的情况

- 讨论教学方法（不是在查询数据）
- 纯聊天中提到"课程"
- 与雨课堂无关的场景

### 组合调用示例

> 用户说："帮我看看我是谁，还有我开了哪些班"

依次调用：
1. `claw_current_user`
2. `ykt_teaching_list`

---

## 工具详细说明

### 全局规则

- **班级名称 → ID**：如果用户给的是班级名称而非 ID，先调用 `ykt_classroom_id_by_name` 拿到 `classroomId`，再调用目标工具。
- **时间处理**：所有相对时间（昨天/今天/明天/近N天）以当前系统北京时间（UTC+8）为基准，禁止硬编码年份。若用户未指定年份，默认使用当前年份。
- **参数格式**：如果用户给的参数格式不对，不要自动修正，提示用户修改。
- **预约开课**：执行前必须向用户展示即将预约的课堂信息，二次确认后再调用。
- **mcp 服务使用注意事项**：
    - 推荐使用 npx mcporter 调用 MCP 服务（无需全局安装），不建议直接使用 curl；
    - 如果 mcp 服务提示鉴权失败，请引导用户重新获取 YUKETANG_SECRET 并修改环境变量；
    - 如果 mcp 服务找不到，注意指定 mcp 配置文件的路径；
    - 如果调用失败，可以换一种方式重试，但若多次尝试仍不成功，请停止并检查配置。

---

### 1. `claw_current_user`

查询当前雨课堂用户 ID。

**典型问法：** "我的雨课堂ID是多少" / "帮我确认一下当前账号"

**参数：** 无

---

### 2. `ykt_teaching_list`

查询当前账号开设的班级列表。

**典型问法：** "我教了哪些班" / "这学期我教的课"

**参数：** 无

**注意：** 返回结果中的 emoji 需保留。

---

### 3. `ykt_classroom_statistics`

查询本学期班级数据概览。

**典型问法：** "我的班级数据" / "XXX 班级数据情况"

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `classroomName` | 否 | 不传则返回本学期所有班级概览；传入后返回指定班级详情 |

**交互规则：**
- 用户第一次查询或未指定班级 → 返回全部班级概览
- 用户输入班级序号（1、2、3）、完整名称或可识别的简称 → 返回该班级详情

---

### 4. `ykt_classroom_warning_overview`

查询本学期各班级的学习活动完成率预警总览。

**典型问法：** "查看班级预警情况"

**参数：** 无

**返回内容包括：** 教学班名称、完成率 = 0% 人数、预警人数（完成率 < 80%）、数据截止时间。

---

### 5. `ykt_classroom_warning_student`

查询指定班级的预警学生名单。

**典型问法：** "高等数学A-2 的预警学生" / "第 1 个班级的预警名单"

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `classroomName` | 是 | 班级名称、序号或可识别简称 |

**交互规则：**
- 如果用户未指定班级，先调用 `ykt_classroom_warning_overview` 展示总览，再让用户选择。

---

### 6. `cube_teacher_today_teaching` - 查询教师当日授课总览

查询教师某天的授课总览信息，如课堂状态、到课情况、答题情况等。

**典型问法：** "今天上课情况怎么样" / "今天有多少人来上课了" / "我今天有课吗" / "看一下今天的授课总览" / "今天课堂进行得怎么样"

**参数：** 

| 参数 | 必填 | 说明 |
|------|------|------|
| `date` | 否 | 查询日期 yyyy-MM-dd，缺省当天（北京） |

** 输出规范 **
- 若 `data.clawUserText` 非空，assistant 的最终输出必须且只能为 `data.clawUserText`
- 不得添加标题、emoji、列表、表格、总结、提示语
- 不得改写、压缩、润色或转述 `data.clawUserText`
- 不得基于 `date`、`hasLessons`、`lessons` 等其他字段生成回复
- 仅当 `data.clawUserText` 为空或缺失时，才可基于其他字段组织回复

---

### 7. `ykt_classroom_id_by_name`

通过班级名称查询班级 ID（辅助工具，通常由其他工具间接调用）。

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `classroomName` | 是 | 班级名称 |

---

### 8. `cube_lesson_reservation`

为指定教学班预约开课。

**参数：**

| 参数 | 必填 | 说明 |
|------|------|------|
| `classroomId` | 是 | 班级 ID |
| `startDateTime` | 否 | 开课时间（字符串） |
| `startEpochMs` | 否 | 开课时间（毫秒时间戳） |
| `lessonTitle` | 否 | 课次标题 |
| `lessonDurationMinutes` | 否 | 课次时长（分钟） |
| `meetingType` | 否 | 会议类型 |

**使用逻辑：**
- 用户给班级名称 → 先调 `ykt_classroom_id_by_name` 获取 `classroomId`，再调本工具
- 用户直接给 `classroomId` → 直接调用

> 详细参数说明见 `references/api_references.md` 中 `cube_lesson_reservation` 部分。

** 输出规范 **
- 当存在`✅ 课堂预约成功！`时， 内容禁止渲染成表格


### 9. `ykt_teacher_correct_statistic` - 教师待批改/已批改统计

用于按课程班级查询教师的作业、考试、课堂、课件批改统计，包括待批改、已批改数量等信息。

** 适用场景：**
当用户有以下意图时，应使用本工具：
- 查看作业、考试、课堂、课件的批改情况
- 查询待批改数量
- 查询已批改数量

**输出规范**
- 不得省略班级
- 不得省略任一班级下的统计数据
- 若结果包含 `🔗去班级内批改`，必须：
  - 在对应班级下展示
  - 严格按照原始返回内容输出
  - 不得修改其位置、文案或格式
- 每个班级下均必须展示 `🔗去班级内批改`



### 10. `ykt_recent_exercise_submit` - 教师发布的作业完成情况

用于查询教师发布作业完成情况

**参数**: 

| 参数 | 必填 | 说明 |
|------|------|------|
| classroomId | ❌ | 班级 ID |
| classroomName | ❌ | 班级名称 |
| isLatest | ❌ | `1` 表示仅查询最近一次；不传表示查询最近三天 |

**使用逻辑：**
- 用户给班级名称 → 先调 `ykt_classroom_id_by_name` 获取 `classroomId`，再调本工具
- 用户直接给 `classroomId` → 直接调用
- 用户查询“最近一次发布的作业情况” → 调本工具时使用 `isLatest = 1` 



### 11. `ykt_recent_notice_read` - 教师发布的公告阅读情况

用于查询用户发布的所有近7天发布公告，按照发布时间顺序倒序排列

**参数**:

| 参数 | 必填 | 说明 |
|------|------|------|
| classroomId | ❌ | 班级 ID |
| classroomName | ❌ | 班级名称 |
| isLatest | ❌ | `1` 表示仅查询最近一次；不传表示查询最近七天 |

**使用逻辑：**
- 用户给班级名称 → 先调 `ykt_classroom_id_by_name` 获取 `classroomId`，再调本工具
- 用户直接给 `classroomId` → 直接调用
- 用户查询“最近一次发布的公告情况” → 调本工具时使用 `isLatest = 1`



### 12. `cube_lesson_resolve_by_names`  - 按名称解析 lessonId

用于按照 “课程名+教学班名+课堂名（课节标题）”查询当日 lessonId（辅助工具，通常由其他工具间接调用）。

**参数**:

| 参数 | 必填 | 说明 |
|------|------|------|
| courseName | ✅ | 班级名称 |
| classroomName | ✅ | 班级名称 |
| lessonTitle | ❌ |课堂名，即课节标题；可与 lessonName 二选一 |
| lessonName | ❌ | 同 lessonTitle（课堂名） |
| date | ❌ | 日历日 yyyy-MM-dd，默认当天（北京）；须与查详情为同一天 |
| fuzzy | ❌ | true 时三项名称允许包含匹配（精确匹配优先） |

** 默认值策略 **
- `date` 默认当天（北京时间）
- `lessonTitle` 与 `lessonName` 二选一
- `fuzzy` 默认传 `true`


### 13. `cube_teacher_today_teaching_detail`  - 查询当日单个课程的详情

用于查询当日单个课程的详情；lessonId 来自 cube_lesson_resolve_by_names

** 🎯 适用场景 **
当用户有以下意图时，应使用本工具：

- 查看某一节课的课堂详情
- 用户已经提供了 `lessonId`
- 或用户已能通过上游工具`cube_lesson_resolve_by_names`解析出 `lessonId`

**参数**:

| 参数 | 必填 | 说明 |
|------|------|------|
| lessonId | ✅ | 课堂ID |
| date | ❌ | 日历日 yyyy-MM-dd，默认当天（北京）；须与查详情为同一天 |

** 默认值策略 **
- `date` 默认当天（北京时间）， 必须与解析时保持同一天

**交互规则：**
- 如果用户未指定班级，先调用 `cube_teacher_today_teaching` 展示总览，再让用户选择。

**使用逻辑：**
- 用户给课程名称、班级名称、课堂名称 → 先调 `cube_lesson_resolve_by_names` 获取 `lessonId`，再调本工具
- 用户直接给 `lessonId` → 直接调用
- 如果用户未指定“课程名称、班级名称、课堂名称”，先调用 `cube_teacher_today_teaching` 展示总览，再让用户选择。





---

## 输出规范

- 结果结构化展示（列表形式）
- 保留工具返回的 emoji 和原始文案，不要自由发挥改写
- 课程信息至少包含：课程名、班级名
- 严格保留表头

## 红线

- 不编造任何课程数据，必须依赖工具返回
- 不做权限外操作（如选课、退课）
