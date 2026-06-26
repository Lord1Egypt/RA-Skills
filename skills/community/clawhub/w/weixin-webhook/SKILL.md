# weixin-webhook

企业微信 Webhook 消息发送工具，一行命令即可完成通知推送。

## 前置准备：获取 Webhook URL

**在使用前，你需要先获取企业微信的 Webhook 地址。**

### 操作步骤

1. 打开企业微信，进入需要接收消息的群聊  
2. 点击右上角「三个点」→ 选择「消息推送」→ 添加消息推送  
3. 复制生成的 Webhook URL，格式如下：  
   `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxx-xxxxx`

### 注意事项

- 请勿将 Webhook URL 分享给他人  
- 如不慎泄露，可删除该推送后重新创建

---

## 快速使用

```bash
# 发送文本消息
~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh "webhook_key" "text" "消息内容"

# 发送 Markdown 消息
~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh "webhook_key" "markdown" "**重要** <font color=\"warning\">提醒</font>"

# @ 指定人员
~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh "key" "text" "会议提醒" "zhangsan,lisi" "13800001111"
```

### 参数说明

| 位置 | 说明 |
|------|------|
| 1 | webhook_key（URL 中 key 参数的值） |
| 2 | msgtype（text / markdown） |
| 3 | 消息内容 |
| 4 | @ 用户的 userid 列表（逗号分隔，可选） |
| 5 | @ 用户的手机号列表（逗号分隔，可选） |

---

## 设置定时任务

```bash
# 每天 14:00 发送提醒
openclaw cron add \
  --cron "0 14 * * *" \
  --agent main \
  --message "执行：~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh 'your_key' 'text' '【健康提醒】请做提肛运动！' 'liujie'" \
  --name "daily_kegel" \
  --description "每日提肛提醒" \
  --no-deliver

# 每天 9:00 团队通知
openclaw cron add \
  --cron "0 9 * * *" \
  --agent main \
  --message "执行：~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh 'your_key' 'text' '晨会即将开始，请准时参加' '@all'" \
  --name "morning_meeting" \
  --description "晨会通知" \
  --no-deliver

# 每日汇报提醒（Markdown 格式）
openclaw cron add \
  --cron "0 17 * * *" \
  --agent main \
  --message "执行：~/.openclaw/workspace/skills/weixin-webhook/send_weixin.sh 'your_key' 'markdown' '【日报提醒】请在18:00前提交日报。<font color=\"info\">1. 今日完成</font><font color=\"info\">2. 遇到问题</font><font color=\"info\">3. 明日计划</font>'" \
  --name "daily_report" \
  --description "日报提醒" \
  --no-deliver
```

## 管理定时任务

```bash
openclaw cron list                    # 查看所有任务
openclaw cron run daily_kegel         # 手动执行测试
openclaw cron disable daily_kegel     # 禁用任务
openclaw cron enable daily_kegel      # 启用任务
openclaw cron rm daily_kegel          # 删除任务
```

---

## 消息格式示例

### 文本消息

```json
{
  "msgtype": "text",
  "text": {
    "content": "会议提醒",
    "mentioned_list": ["zhangsan", "@all"],
    "mentioned_mobile_list": ["13800001111", "@all"]
  }
}
```

### Markdown 消息

```json
{
  "msgtype": "markdown",
  "markdown": {
    "content": "实时新增<font color=\"warning\">132例</font>\n>普通用户:<font color=\"comment\">117例</font>\n>VIP用户:<font color=\"comment\">15例</font>"
  }
}
```

---

## 文件结构

```
weixin-webhook/
├── SKILL.md       # 使用说明
└── send_weixin.sh # 发送脚本
```

## 依赖

- `curl`（系统通常自带）