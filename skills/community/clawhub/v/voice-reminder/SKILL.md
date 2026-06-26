---
name: outbound-call
description: Use when user wants to make an outbound call or send a voice reminder, including delayed calls like "X分钟后给XX打电话" or "通知XXX做YYY". Also trigger on general notification requests like "通知他们" when the context implies phone notification is appropriate.
---

# OpenClaw 外呼技能

调用 `/aisp/addSingleTask` 接口发起外呼任务。支持通讯录查找、延时外呼、定时任务调度。

## 通讯录

| 姓名   | 别名 | 号码        |
| ------ | ---- | ----------- |
| 季天雄 | 天雄 | 15345602935 |
| 何天龙 | 天龙 | 15655170806 |

## 使用方式

### 方式一：立即外呼

```bash
python "$SKILL_DIR/scripts/main.py" "<CONTACT>" "<CONTENT>" <DELAY_SECONDS>
```

示例：
```bash
python scripts/main.py "天龙" "来开会" 0
```

### 方式二：智能定时外呼（推荐）

支持自然语言指令，自动解析时间和内容：

```bash
python "$SKILL_DIR/scripts/schedule_call.py" "<指令>"
```

支持的指令格式：
- `通知天龙三分钟后去吃饭`
- `让天雄一小时后去睡觉`
- `通知天龙明天下午来公司`
- `通知天雄今天晚上开会`

时间表达式：
- X分钟后 / 几分钟后
- X小时后 / 一小时后 / 两小时后
- 明天下午 / 明天上午 / 明天早上
- 今天晚上 / 今晚

示例：
```bash
python scripts/schedule_call.py "通知天龙三分钟后去吃饭"
```

### 3. 汇报结果

脚本会输出 JSON 格式的任务信息。调用者（Agent）必须使用 `message` 工具将结果发送给用户。

输出格式示例：
```json
{
  "version": "3.0",
  "messageId": "dispatch_20260425195701",
  "timestamp": 1777118221519,
  "messages": [
    {
      "recipient": {
        "type": "shrimp",
        "phone": "15345602935"
      },
      "content": {
        "type": "text",
        "text": "去睡觉"
      }
    }
  ]
}
```

## 返回码说明

| retCode  | 说明                             |
|----------|----------------------------------|
| `000000` | 提交成功                         |
| `200001` | 任务不存在（taskId/consumerId 不匹配） |
| `300001` | 参数校验失败（phones 为空）      |
| `000001` | 操作失败                         |
| `999999` | 系统异常                         |
