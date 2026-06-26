# Windows TTS Reminder Configuration

## 家庭提醒时间表

### 每日固定提醒

| 时间 | 提醒内容 | 音色 | 音量 |
|------|----------|------|------|
| 07:00 | 早安！新的一天开始了，记得吃早餐哦 | zh-CN-YunxiNeural | 0.7 |
| 08:30 | 提醒：该吃药了，请记得服用今天的维生素 | zh-CN-XiaoxiaoNeural | 0.6 |
| 19:00 | 程老板，该提醒孩子写作业了！ | zh-CN-XiaoxiaoNeural | 0.8 |
| 20:30 | 温馨提示：作业时间快结束了，请检查完成情况 | zh-CN-XiaoxiaoNeural | 0.7 |
| 21:30 | 该准备休息了，明天还要早起呢 | zh-CN-YunxiNeural | 0.6 |
| 22:00 | 晚安！祝你好梦 | zh-CN-XiaoxiaoNeural | 0.5 |

### 特殊场景

| 场景 | 触发条件 | 提醒内容 |
|------|----------|----------|
| 作业提醒 | 工作日 19:00 | "亲爱的程老板，现在是晚上 7 点，该提醒孩子写作业了！" |
| 吃药提醒 | 每天 08:30, 20:30 | "温馨提示：该吃药了，请记得服用今天的维生素。" |
| 吃饭提醒 | 检测到人未活动超过 30 分钟 | "饭准备好了，快来吃饭吧！" |
| 紧急通知 | 手动触发 | 自定义内容 |

## 配置文件位置

1. **OpenClaw 配置**: `/home/cmos/.openclaw/openclaw.json`
2. **Life Agent 心跳**: `/home/cmos/.openclaw/workspace-life/HEARTBEAT.md`
3. **Cron 作业**: `/home/cmos/.openclaw/cron/jobs.json`

## 快速测试

```bash
# 测试 TTS 连接
curl -X POST http://192.168.1.60:5000/play_tts \
  -H "Content-Type: application/json" \
  -d '{"text": "测试一下，这里是跨设备自动播报系统。"}'

# 使用 OpenClaw 工具测试
# 在 OpenClaw 中执行：tts_notify({"text": "你好，这是测试消息"})
```

## 使用示例

### 在 Heartbeat 中使用

编辑 `/home/cmos/.openclaw/workspace-life/HEARTBEAT.md`:

```markdown
# Life Agent Heartbeat - Family Reminders

每 30 分钟检查一次：

1. 检查当前时间是否在提醒时间段
2. 检查是否有待发送的家庭提醒
3. 使用 tts_notify 工具发送到 Windows TTS

## 提醒逻辑

- 07:00-07:30: 早安提醒
- 08:25-08:35: 吃药提醒
- 19:00-19:10: 作业提醒
- 20:25-20:35: 作业检查提醒
- 21:25-21:35: 休息提醒
- 22:00-22:10: 晚安提醒
```

### 在 Cron 中使用

编辑 `/home/cmos/.openclaw/cron/jobs.json`:

```json
{
  "version": 1,
  "jobs": [
    {
      "id": "life-homework-reminder",
      "agent": "life",
      "schedule": "0 19 * * *",
      "task": "发送作业提醒到 Windows TTS",
      "delivery": {
        "method": "tts_notify",
        "config": {
          "text": "程老板，该提醒孩子写作业了！"
        }
      },
      "enabled": true
    }
  ]
}
```

## 音色推荐

### 中文女声
- `zh-CN-XiaoxiaoNeural` - 温暖亲切，适合家庭提醒
- `zh-CN-YunxiNeural` - 清晰专业，适合正式通知
- `zh-CN-YunjianNeural` - 激情活力，适合运动场景

### 中文男声
- `zh-CN-YunyangNeural` - 沉稳专业
- `zh-CN-YunhaoNeural` - 广告男声，适合播报

### 英文
- `en-US-JennyNeural` - 友好女声
- `en-US-GuyNeural` - 专业男声
- `en-GB-SoniaNeural` - 英式女声
