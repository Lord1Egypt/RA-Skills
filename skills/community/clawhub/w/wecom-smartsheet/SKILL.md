---
name: 企微智能表格
description: |
  企业微信智能表格全流程自动化操作技能。触发词：企微智能表格、智能表格、工作任务表格、费用申请表格、视频制作表格、企微表格、新建任务、添加任务、添加费用、费用申请、报销、视频制作流程、工作流、任务提醒、到期提醒、巡检、企微工作流。
  任何涉及在企微智能表格中新增/查询/提醒/通知的操作，均触发此技能。
version: 1.0.0
author: Jason Xie
disable: false
---

# 企微智能表格 操作技能

> 企业微信智能表格全流程自动化操作技能。
> 将用户的自然语言请求转化为企微智能表格写入 + 群机器人通知 + 本地追踪 + 定时提醒的完整闭环。

---

## 一、系统架构总览

### 1.1 三大智能表格

| 表格名称 | 标识符 | 说明 |
|---|---|---|
| 费用申请系统 | `expense` | 费用报销全流程审批 |
| 工作任务系统 | `task` | 工作任务分配与进度追踪 |
| 视频制作工作流 | `video` | 视频制作多阶段协同 |

> **配置方式**：首次使用前，需将企微智能表格的 Webhook Key 填入下方的占位符。Webhook Key 在企微文档 → 智能表格 → 更多 → Webhook 中获取。

**表格写入 URL 格式**：`https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key={Webhook_Key}`

### 1.2 三个群机器人

| 群名称 | 对应表格 | 说明 |
|---|---|---|
| 费用审批群 | `expense` | 费用申请通知与审批提醒 |
| 工作任务群 | `task` | 任务分配与到期提醒 |
| 视频制作群 | `video` | 视频制作进度通知 |

**群通知 URL 格式**：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={Bot_Key}`

### 1.3 表格与群严格一一对应

```
费用申请系统 (expense) ──→ 费用审批群 (expense bot)
工作任务系统 (task)     ──→ 工作任务群 (task bot)
视频制作工作流 (video)  ──→ 视频制作群 (video bot)
```

**⚠️ 绝对不能搞混！** 每个表格的通知必须发到它自己对应的群，不能统一发到所有群。

---

## 二、四步闭环 SOP（标准操作流程）

> **这是核心规则。每次操作企微智能表格，必须完整执行以下四步，缺一不可。**

| 步骤 | 操作 | 执行方式 | 说明 |
|---|---|---|---|
| **① 写入表格** | 构造 payload，POST 到表格 Webhook | `curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key={key}" -H "Content-Type: application/json" -d '{payload}'` | payload 中 `add_records[0].values` 的 key 是字段 ID，value 按字段类型传值 |
| **② 群通知** | 发送 Markdown 消息到对应群机器人 | `curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={bot_key}" -H "Content-Type: application/json" -d '{markdown_payload}'` | 必须发到该表格对应的群，不能发错 |
| **③ 本地追踪** | 同步写入 `wecom_deadline_tracker.json` | 调用 Python 脚本 `track_record()` 或手动追加 JSON | 记录到期信息，供每日巡检脚本读取 |
| **④ 设置提醒** | 创建一次性定时提醒，到期前发到对应群 | WorkBuddy `automation_update` 工具，`scheduleType="once"`，prompt 中用 curl 调群机器人 | 提醒消息发到对应群 |

### 2.1 步骤①详细：写入表格

**请求格式：**
```json
{
  "add_records": [
    {
      "values": {
        "字段ID": "字段值",
        "字段ID": "字段值"
      }
    }
  ]
}
```

**curl 完整示例（工作任务系统）：**
```bash
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key={TASK_WEBHOOK_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "add_records": [{
      "values": {
        "ftQMc5": "查看公司写字楼附近的商业情况",
        "fMAfWQ": [{"user_id": "USER_ID_1"}],
        "fn8TJd": [{"user_id": "USER_ID_2"}],
        "fsaQFC": [{"user_id": "USER_ID_3"}],
        "fSP1Xe": "1777353600000",
        "fIH343": "1777447060000",
        "fp6iMs": [{"text": "未开始"}],
        "f9ftBb": 0
      }
    }]
  }'
```

**成功响应：**
```json
{"errcode": 0, "errmsg": "ok", "add_records": [{"record_id": "recXXXXXX"}]}
```

**失败响应示例：**
```json
{"errcode": 40001, "errmsg": "invalid userid"}
```

### 2.2 步骤②详细：群通知

**Markdown 消息格式：**
```json
{
  "msgtype": "markdown",
  "markdown": {
    "content": "**📌 新任务通知**\n\n> 任务：<font color=\"info\">任务名称</font>\n> 责任人：XXX\n> 截止日期：2026-05-01\n> 状态：未开始\n\n请及时处理！"
  }
}
```

**curl 完整示例（工作任务群）：**
```bash
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={TASK_BOT_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "msgtype": "markdown",
    "markdown": {
      "content": "**📌 新任务通知**\n\n> 任务：<font color=\"info\">查看公司写字楼附近的商业情况</font>\n> 责任人：XXX\n> 协作人：XXX\n> 知会人：XXX\n> 截止日期：2026-05-01\n> 状态：未开始\n\n请及时处理！"
    }
  }'
```

**通知模板（按表格类型）：**

| 表格类型 | 标题 emoji | 标题前缀 | 关键字段 |
|---|---|---|---|
| expense | 💰 | 费用审批通知 | 报销描述、金额、申请人、付款截止 |
| task | 📌 | 工作任务通知 | 任务描述、责任人、协作人、知会人、截止日期 |
| video | 🎬 | 视频制作通知 | 视频标题、当前阶段、负责人、截止日期 |

### 2.3 步骤③详细：本地追踪

每次成功写入表格后，需将关键信息追加到本地 JSON 文件。

**文件路径**：`{WORKDIR}/wecom_deadline_tracker.json`

**记录格式：**
```json
{
  "table": "task",
  "record_id": "recXXXXXX",
  "name": "任务名称",
  "deadline": "2026-05-01",
  "responsible": "userid",
  "data": { ... },
  "tracked_at": "2026-04-27T16:30:00",
  "notified": false
}
```

**可用 Python 函数**（来自 `wecom_smartsheet.py`）：
- `track_record(table, data, record_id)` — 自动追加记录
- `load_tracker()` — 读取所有追踪记录
- `get_upcoming_deadlines(days=3)` — 获取未来 N 天内到期的记录

### 2.4 步骤④详细：设置提醒

使用 WorkBuddy 的 `automation_update` 工具创建一次性定时任务。

**参数：**
- `mode`: `"suggested create"`
- `name`: `"任务提醒-{任务名称}"`
- `scheduleType`: `"once"`
- `scheduledAt`: ISO 8601 格式，如 `"2026-04-28T09:00"`
- `status`: `"ACTIVE"`
- `prompt`: 包含 curl 命令，直接调群机器人发送提醒

**prompt 模板：**
```
发送一条提醒消息到工作任务群。执行以下命令：
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={TASK_BOT_KEY}" -H "Content-Type: application/json" -d '{"msgtype":"markdown","markdown":{"content":"**⏰ 任务提醒**\n\n> 任务：<font color=\"warning\">{任务名称}</font>\n> 责任人：{责任人}\n> 截止日期：{截止日期}\n> 状态：{状态}\n\n请尽快处理！"}}'
发送完成后简要报告结果。
```

---

## 三、字段映射表（完整）

### 3.1 费用申请系统（expense）

| 字段中文名 | 字段 ID | 字段类型 | 格式说明 | 可选值 |
|---|---|---|---|---|
| 报销描述 | `f95bql` | 文本 | 字符串 | — |
| 报销费用类型 | `fSIkwz` | 文本数组 | `[{"text": "选项"}]` | 房租税金、办公用品、差旅费、餐饮费、其他 |
| 费用类型 | `fV2Vy0` | 文本数组 | `[{"text": "选项"}]` | — |
| 费用内容 | `ftQMc5` | 文本 | 字符串 | — |
| 金额 | `ftk5Tx` | **文本** | ⚠️ **必须传字符串**，如 `"4800"` | — |
| 实发工资金额 | `fv0Ji4` | 文本 | 字符串 | — |
| 单据图片 | `ffC9Tb` | 附件 | Webhook 不支持，传 `[]` | — |
| 收款户名 | `fQgUks` | 文本 | 字符串 | — |
| 收款人开户银行 | `fFh8FX` | 文本 | 字符串 | — |
| 收款人银行账号 | `fpe6NV` | 文本 | 字符串 | — |
| 财务初审人 | `fMAfWQ` | 人员 | `[{"user_id": "xxx"}]` | — |
| 财务初审意见 | `f2hMiW` | 文本 | 字符串 | — |
| 终审人员 | `fn8TJd` | 人员 | `[{"user_id": "xxx"}]` | — |
| 终审人员意见 | `ff1LL6` | 文本 | 字符串 | — |
| 终审结果 | `fMRZPT` | 文本数组 | `[{"text": "选项"}]` | 同意、驳回、待审批 |
| 终审审批时间 | `fs4s7u` | 日期 | 毫秒时间戳字符串 | — |
| 支付账户 | `fBOypp` | 文本数组 | `[{"text": "选项"}]` | 示例账户 |
| 银行制单日期 | `fgbqSn` | 日期 | 毫秒时间戳字符串 | — |
| 支付人 | `fbA3YP` | 人员 | `[{"user_id": "xxx"}]` | — |
| 付款截止日期 | `fgeUSZ` | 日期 | 毫秒时间戳字符串 | — |
| 支付人意见 | `f4JIH4` | 文本数组 | `[{"text": "选项"}]` | 已支付、待支付 |
| 支付日期 | `fafRRt` | 日期 | 毫秒时间戳字符串 | — |
| 支付凭据 | `fowtyf` | 附件 | Webhook 不支持，传 `[]` | — |
| 流程结果 | `fG5K0s` | 文本数组 | `[{"text": "选项"}]` | 已完成、进行中、已取消 |
| 终审日期 | `fy8sMG` | 日期 | 毫秒时间戳字符串 | — |
| 审批进度 | `fZPqRZ` | 文本数组 | `[{"text": "选项"}]` | 待初审、初审通过、待终审、终审通过、终审驳回 |

### 3.2 工作任务系统（task）

| 字段中文名 | 字段 ID | 字段类型 | 格式说明 | 可选值 |
|---|---|---|---|---|
| 任务详细描述 | `ftQMc5` | 文本 | 字符串 | — |
| 填写任务最新进展 | `fAUNqS` | 文本 | 字符串 | — |
| 填写时间 | `fJtBHe` | 日期 | 毫秒时间戳字符串 | — |
| 完全责任人 | `fMAfWQ` | 人员 | `[{"user_id": "xxx"}]` | — |
| 任务结果交付给谁 | `fvMIN1` | 人员 | `[{"user_id": "xxx"}]` | — |
| 任务重要紧急分类 | `fLjDXp` | 文本数组 | `[{"text": "选项"}]` | 重要紧急、重要不紧急、紧急不重要、不紧急不重要 |
| 任务类型 | `ftk5Tx` | 文本数组 | `[{"text": "选项"}]` | 财务类、市场与销售类、人力资源类、技术类、行政类 |
| 任务优先级 | `f8lJy9` | 文本数组 | `[{"text": "选项"}]` | 星标任务（极其重要紧急）、高、中、低 |
| 图片 | `far6pU` | 附件 | Webhook 不支持，传 `[]` | — |
| 协同任务完成的人 | `fn8TJd` | 人员 | `[{"user_id": "xxx"}]` | — |
| 不参与任务但需要知会的人 | `fsaQFC` | 人员 | `[{"user_id": "xxx"}]` | — |
| 计划开始时间 | `fSP1Xe` | 日期 | 毫秒时间戳字符串 | — |
| 计划结束时间 | `fIH343` | 日期 | 毫秒时间戳字符串 | — |
| 实际开始时间 | `fnmp0N` | 日期 | 毫秒时间戳字符串 | — |
| 实际结束时间 | `fNxWUG` | 日期 | 毫秒时间戳字符串 | — |
| 任务工作小时数 | `f5mcXr` | 数值 | 整数 | — |
| 任务状态 | `fp6iMs` | 文本数组 | `[{"text": "选项"}]` | 未开始、进行中、已完成、已取消 |
| 进度 | `f9ftBb` | 数值 | 浮点数，如 `0`、`0.5`、`1` | — |
| 每周回顾任务 | `fOinuX` | 文本数组 | `[{"text": "选项"}]` | — |
| 每月回顾任务 | `furcM5` | 文本数组 | `[{"text": "选项"}]` | — |
| 任务完成总结 | `f2CRNT` | 文本 | 字符串 | — |
| 备注 | `fCpF71` | 文本 | 字符串 | — |

### 3.3 视频制作工作流（video）

| 字段中文名 | 字段 ID | 字段类型 | 格式说明 | 可选值 |
|---|---|---|---|---|
| 视频类别 | `fIxg8J` | 文本数组 | `[{"text": "选项"}]` | 短视频、长视频、直播、其他 |
| 逐字稿文档 | `flj0f9` | 文本 | 字符串（URL） | — |
| AI 生成的视频标题 | `fRZCUc` | 文本 | 字符串 | — |
| 逐字稿负责人 | `ftQMc5` | 人员 | `[{"user_id": "xxx"}]` | — |
| 文字稿提供日期 | `ftk5Tx` | 日期 | 毫秒时间戳字符串 | — |
| 视频营销完全责任人 | `fExzxn` | 人员 | `[{"user_id": "xxx"}]` | — |
| 视频生成完全责任人 | `f0WI70` | 人员 | `[{"user_id": "xxx"}]` | — |
| 音频负责人 | `ffFwIh` | 人员 | `[{"user_id": "xxx"}]` | — |
| 音频制作计划完成日期 | `fGP81d` | 日期 | 毫秒时间戳字符串 | — |
| 音频制作实际完成日期 | `fgbWRh` | 日期 | 毫秒时间戳字符串 | — |
| 视频生成负责人 | `fn8TJd` | 人员 | `[{"user_id": "xxx"}]` | — |
| 视频制作计划完成日期 | `faGcmb` | 日期 | 毫秒时间戳字符串 | — |
| 视频制作实际完成日期 | `f8SU87` | 日期 | 毫秒时间戳字符串 | — |
| 后期合成负责人 | `fsPk4D` | 人员 | `[{"user_id": "xxx"}]` | — |
| 后期计划完成日期 | `fRGWEC` | 日期 | 毫秒时间戳字符串 | — |
| 后期实际完成日期 | `fdRqlx` | 日期 | 毫秒时间戳字符串 | — |
| 计划上传发布日期 | `fa4rBU` | 日期 | 毫秒时间戳字符串 | — |
| 发布负责人 | `fQg3so` | 人员 | `[{"user_id": "xxx"}]` | — |
| 实际上传发布日期和时间 | `fh0mD5` | 日期 | 毫秒时间戳字符串 | — |
| 备注和总结 | `fJSKId` | 文本 | 字符串 | — |

---

## 四、字段格式规范（严格执行）

### 4.1 类型→格式映射表

| 字段类型 | 传值格式 | 示例 |
|---|---|---|
| 文本 | `"字符串"` | `"查看公司写字楼附近的商业情况"` |
| 人员 | `[{"user_id": "xxx"}]` | `[{"user_id": "USER_ID"}]` |
| 多人员 | `[{"user_id": "A"}, {"user_id": "B"}]` | `[{"user_id": "USER_ID_1"}, {"user_id": "USER_ID_2"}]` |
| 日期 | `"Unix毫秒时间戳字符串"` | `"1777447060000"` |
| 文本数组（选择型） | `[{"text": "选项文本"}]` | `[{"text": "未开始"}]` |
| 进度 | 数字（浮点） | `0`、`0.5`、`1` |
| 数值（整数） | 数字 | `8`（工作小时数） |
| 附件 | `[]` | Webhook 不支持上传附件 |

### 4.2 时间戳计算

**日期字段必须传 Unix 毫秒时间戳字符串。**

**计算方法**（macOS 终端）：
```bash
# 将日期转为毫秒时间戳
date -j -f "%Y-%m-%d" "2026-05-01" "+%s000"
# 输出: 1777353600000
```

**Python 方法**：
```python
from datetime import datetime
ts = str(int(datetime.strptime("2026-05-01", "%Y-%m-%d").timestamp() * 1000))
# ts = "1777353600000"
```

**⚠️ 绝不能手动计算时间戳！** 必须用 `date` 命令或 Python 计算。

### 4.3 userid 注意事项

> ⚠️ **传入无效 userid 会导致整条写入失败！**
>
> 在首次使用前，请在企微通讯录中确认每个成员的 userid。如果不确定某个人的 userid，先移除该人，写入成功后再补。

---

## 五、完整操作示例

### 5.1 新建工作任务（最常用场景）

**用户说**："在工作任务表格中新建一个任务，任务描述：查看公司写字楼附近的商业情况，完全责任人：张三，协作人：李四，知会人：王五，2026-05-01 前完成，2026-04-28 提醒"

**执行步骤：**

**① 计算时间戳：**
```bash
# 计划开始时间（今天）
date -j -f "%Y-%m-%d" "2026-04-27" "+%s000"
# 计划结束时间
date -j -f "%Y-%m-%d" "2026-05-01" "+%s000"
```

**② 写入表格：**
```bash
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key={TASK_WEBHOOK_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "add_records": [{
      "values": {
        "ftQMc5": "查看公司写字楼附近的商业情况",
        "fMAfWQ": [{"user_id": "USER_ID_1"}],
        "fn8TJd": [{"user_id": "USER_ID_2"}],
        "fsaQFC": [{"user_id": "USER_ID_3"}],
        "fSP1Xe": "1742697600000",
        "fIH343": "1777353600000",
        "fp6iMs": [{"text": "未开始"}],
        "f9ftBb": 0
      }
    }]
  }'
```

**③ 群通知（工作任务群）：**
```bash
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={TASK_BOT_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "msgtype": "markdown",
    "markdown": {
      "content": "**📌 新任务通知**\n\n> 任务：<font color=\"info\">查看公司写字楼附近的商业情况</font>\n> 责任人：张三\n> 协作人：李四\n> 知会人：王五\n> 截止日期：2026-05-01\n> 状态：未开始\n\n请及时处理！"
    }
  }'
```

**④ 本地追踪：** 调用 `track_record("task", data, record_id)`

**⑤ 设置提醒：** 用 `automation_update` 创建一次性定时任务：
- `scheduledAt`: `"2026-04-28T09:00"`
- `prompt`: 包含 curl 命令调工作任务群机器人发送提醒

### 5.2 新建费用申请

**① 写入表格（费用申请系统）：**
```bash
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key={EXPENSE_WEBHOOK_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "add_records": [{
      "values": {
        "f95bql": "4月办公室租金",
        "fSIkwz": [{"text": "房租税金"}],
        "ftk5Tx": "4800",
        "fMAfWQ": [{"user_id": "USER_ID"}],
        "fgeUSZ": "1777353600000"
      }
    }]
  }'
```

**② 群通知（费用审批群）：**
```bash
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={EXPENSE_BOT_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "msgtype": "markdown",
    "markdown": {
      "content": "**💰 费用审批通知**\n\n> 报销描述：<font color=\"info\">4月办公室租金</font>\n> 费用类型：房租税金\n> 金额：<font color=\"warning\">¥4800</font>\n> 申请人：XXX\n> 付款截止：2026-05-01\n\n请审批！"
    }
  }'
```

**③ 本地追踪** + **④ 设置提醒**：同上

### 5.3 新建视频制作任务

**① 写入表格（视频制作工作流）：**
```bash
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/webhook?key={VIDEO_WEBHOOK_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "add_records": [{
      "values": {
        "fIxg8J": [{"text": "短视频"}],
        "fRZCUc": "AI创业入门5步法",
        "ftQMc5": [{"user_id": "USER_ID"}],
        "f0WI70": [{"user_id": "USER_ID"}],
        "faGcmb": "1777353600000"
      }
    }]
  }'
```

**② 群通知（视频制作群）：**
```bash
curl -s -X POST "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={VIDEO_BOT_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "msgtype": "markdown",
    "markdown": {
      "content": "**🎬 视频制作通知**\n\n> 视频标题：<font color=\"info\">AI创业入门5步法</font>\n> 类别：短视频\n> 逐字稿负责人：XXX\n> 计划完成日期：2026-05-01\n\n请及时推进！"
    }
  }'
```

---

## 六、每日巡检自动化

### 6.1 配置方式

- **运行时间**：每日 09:00
- **执行内容**：运行 `wecom_daily_check.py`
- **工作目录**：本技能所在目录

### 6.2 巡检逻辑

1. 从 `wecom_deadline_tracker.json` 读取所有追踪记录
2. 筛选未来 3 天内到期的记录
3. **按表格类型分组**（task/video/expense）
4. 逐组发送到对应群：
   - 有到期记录 → 发送到期提醒（🔴/🟡/🟢 标识紧急程度）
   - 无到期记录 → 发送日常摘要

### 6.3 巡检消息模板

**有到期记录时：**
```
**📌 工作任务提醒**
> 日期：2026-04-28

🔴 **任务名称**
   截止：2026-05-01（剩余3天）
   责任人：XXX

_定时巡检_
```

**无到期记录时：**
```
**📌 工作任务提醒**
> 日期：2026-04-28

> 任务追踪记录：X 条
> 即将到期：0 条（3天内）

> 今日暂无紧急到期任务 ✅

_定时巡检_
```

**紧急程度标识：**
- 🔴 剩余 ≤1 天
- 🟡 剩余 ≤2 天
- 🟢 剩余 ≤3 天

---

## 七、踩坑记录与注意事项

### 7.1 已踩过的坑

| # | 问题 | 原因 | 解决方案 | 日期 |
|---|---|---|---|---|
| 1 | 金额字段写入失败 | 费用表格的 `ftk5Tx`（金额）是文本类型，传了数字 | **金额必须传字符串**，如 `"4800"` 而非 `4800` | — |
| 2 | 三个群收到相同通知 | 巡检脚本只发一条通用摘要到一个群 | **必须按表格类型分别发到对应群**，每个群有专属内容 | — |
| 3 | wecom-cli 写入失败 | CLI 的 `smartsheet_add_records` 需要 `sheet_id` 且参数复杂 | **放弃 CLI，直接 POST Webhook** 更简单可靠 | — |
| 4 | Bot 读取返回 851003 | Bot 未被授权文档访问权限 | **用本地 tracker 文件替代读取**，需在企微管理后台添加授权才能启用 | — |
| 5 | `xxx` userid 无效 | 该用户 ID 在企微中不存在或格式错误 | **移除无效 userid**，只传已验证有效的 ID | — |

### 7.2 操作注意事项

1. **绝对不要用 wecom-cli 写入智能表格**。直接 POST Webhook 是唯一推荐方式。
2. **绝对不要手动计算时间戳**。用 `date -j` 命令或 Python `datetime` 计算。
3. **金额字段永远传字符串**。即使看起来像数字，也必须用引号包裹。
4. **人员字段必须是数组格式**。即使只有一个人，也要用 `[{"user_id": "xxx"}]`。
5. **文本数组字段必须是数组格式**。即使只有一个选项，也要用 `[{"text": "选项"}]`。
6. **无效 userid 会导致整条记录写入失败**。不确定的 userid 先跳过。
7. **每个表格的通知只发到它对应的群**。task→工作任务群，expense→费用审批群，video→视频制作群。
8. **附件字段无法通过 Webhook 上传**。传 `[]` 即可。
9. **四步闭环必须完整执行**。写入→通知→追踪→提醒，缺一不可。
10. **日期字段传毫秒时间戳字符串**。注意是字符串格式，不是数字。

---

## 八、工具链与脚本

### 8.1 脚本文件

| 文件 | 功能 |
|---|---|
| `references/wecom_smartsheet.py` | 包含所有字段映射、格式转换、Webhook 推送、群通知、本地追踪函数 |
| `references/wecom_daily_check.py` | 读取 tracker，按表格类型分组发送到期提醒到对应群 |
| `wecom_deadline_tracker.json` | JSON 格式的到期追踪记录 |
| Token 存储 | 所有 Webhook URL 和群机器人 URL 的集中存储（本地，不对外发布） |

### 8.2 CLI 工具

- **wecom-cli**（如已安装）：**不推荐用于智能表格写入**（参数复杂且需 sheet_id）
- **推荐方式**：直接 `curl` POST Webhook

### 8.3 Python 可用函数（from wecom_smartsheet.py）

```python
# 推送到表格
push_to_table(table, data, track=True)

# 构造 Webhook payload
build_webhook_payload(table, data)

# 发送群通知
send_notification(notify_type, title, fields, mention_list=None)

# 场景化通知
notify_expense_pending(description, amount, deadline, applicant, reviewer)
notify_task_deadline(task_name, responsible, deadline, priority, progress)
notify_video_milestone(video_title, stage, deadline, responsible)

# 本地追踪
track_record(table, data, record_id)
load_tracker()
save_tracker(records)
get_upcoming_deadlines(days=3)

# 日期转换
date_to_timestamp(date_str)  # "2026-05-01" → "1777353600000"

# 字段值自动转换
convert_field_value(table, field_title, value)
```

---

## 九、Markdown 通知格式规范

### 9.1 企微群 Markdown 支持范围

企微群机器人 Markdown 仅支持以下语法：
- **粗体**：`**文本**`
- 引用：`> 文本`
- 字体颜色：`<font color="warning">文本</font>`（支持 `info`/`warning`/`comment`）
- 链接：`[文本](URL)`

**不支持**：标题（#）、代码块（```）、表格、图片、列表等。

### 9.2 颜色值

| 颜色关键字 | 显示效果 | 适用场景 |
|---|---|---|
| `info` | 绿色 | 正常信息、任务名称 |
| `warning` | 橙红色 | 截止日期、金额、紧急提醒 |
| `comment` | 灰色 | 进度、状态等辅助信息 |

---

## 十、首次配置指南

> 克隆此技能后，按以下步骤配置凭证：

1. 在企微智能表格中获取三个表格的 Webhook Key：
   - 企微文档 → 智能表格 → 更多 → Webhook
   - 将 Key 填入脚本的对应位置

2. 在企微群中添加群机器人，获取群机器人 Webhook Key：
   - 群设置 → 群机器人 → 添加机器人
   - 记录每个群对应的 Key

3. 配置 userid 映射：
   - 在企微通讯录中确认每个成员的 userid
   - 建立中文名→userid 的映射表

---

## 十一、执行检查清单

每次操作前，用此清单自查：

- [ ] 确定目标表格类型（expense / task / video）
- [ ] 字段 ID 是否正确（查本文第三章映射表）
- [ ] 人员字段是否用 `[{"user_id": "xxx"}]` 格式
- [ ] 日期字段是否用毫秒时间戳字符串（用命令计算，不手算）
- [ ] 金额字段是否传了字符串（不是数字）
- [ ] 文本数组字段是否用 `[{"text": "选项"}]` 格式
- [ ] userid 是否在已验证列表中（不在则先跳过）
- [ ] 通知是否发到了正确的群（对照对应关系）
- [ ] 本地 tracker 是否已更新
- [ ] 提醒自动化是否已创建
- [ ] 四步闭环是否全部完成
