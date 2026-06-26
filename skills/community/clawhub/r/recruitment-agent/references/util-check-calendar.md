# 工作流 5：查看使用者日程

**触发**：需要确认可用时间段时（约面试流程中调用）

## 命令

```bash
# 查看今天日程
lark-cli calendar +agenda

# 查看指定日期范围
lark-cli calendar +agenda --start "2026-04-01" --end "2026-04-05"
```

## 返回字段

| 字段 | 说明 |
|---|---|
| summary | 日程标题 |
| start / end | 开始/结束时间（ISO 8601） |
| attendees | 参会人 |

## 选时间原则

- 优先 **11:00—19:00** 之间
- 避开已有日程时间段
- 面试时长预留 **45分钟**
- 优先选距今 **2—5个工作日** 内
- 最终提供 2—3 个候选时间段供用户确认

## 创建日程（约好后执行）

```bash
lark-cli calendar +create \
  --summary "面试：<候选人姓名>（新媒体编导）" \
  --start "2026-04-04T14:00:00+08:00" \
  --end "2026-04-04T14:45:00+08:00" \
  --description "Boss直聘候选人面试，视频会议" \
  --attendee-ids "<YOUR_OPEN_ID>"
```
