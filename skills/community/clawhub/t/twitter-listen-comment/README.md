# Twitter Listen Comment

一个可打包分发的 OpenClaw skill：
- 用 6551 API 监控一个 Twitter/X 用户名单
- 检测到新推文后生成幽默回复
- 调用 OpenClaw agent 驱动浏览器去评论
- 在 Telegram 等渠道发送“检测到推文”与“评论成功”通知

## 目录结构
- `SKILL.md`：给 agent 看的技能说明
- `scripts/twitter_listen_comment.py`：主脚本
- `scripts/run.sh`：启动脚本
- `references/config.example.json`：配置模板
- `references/config.json`：可直接修改的配置文件
- `references/config.md`：配置字段说明

## 使用前提
使用者本机需要具备：

1. 已安装并可运行 `openclaw`
2. 已在 shell 环境中设置 `TWITTER_TOKEN`
3. Chrome 已登录 X/Twitter
4. 需要浏览器自动化时，Chrome Relay 已可用
5. 已配置好消息通知目标（例如 Telegram chat id）

## 第一步：配置
直接编辑：

- `references/config.json`

重点字段：

- `fromUsers`：要监控的用户名列表（不要带 `@`）
- `agentTarget`：让 `openclaw agent` 路由到哪个会话/目标
- `notifyChannel`：通知渠道，例如 `telegram`
- `notifyTarget`：通知发给谁，例如 `telegram:7164765322`
- `maxTweetAgeSeconds`：只处理多少秒内发布的新推文，默认 300 秒

### 配置示例
```json
{
  "pollIntervalSeconds": 10,
  "maxResultsPerUser": 5,
  "fromUsers": ["elonmusk"],
  "agentTarget": "telegram:7164765349",
  "notifyChannel": "telegram",
  "notifyTarget": "telegram:7164765349",
  "maxTweetAgeSeconds": 300,
  "replyStyle": {
    "language": "zh",
    "tone": "humorous",
    "maxSentences": 2,
    "constraints": [
      "像真人",
      "简短",
      "不客服腔",
      "不要投资建议",
      "不要夸张承诺"
    ]
  }
}
```

## 第二步：运行
### 单次执行
```bash
python3 scripts/twitter_listen_comment.py --config references/config.json --once
```

### 持续运行
```bash
sh scripts/run.sh references/config.json
```

## 当前逻辑
1. 每隔 `pollIntervalSeconds` 秒轮询一次名单
2. 只处理 `maxTweetAgeSeconds` 时间窗口内的新推文
3. 检测到新推后，先发送一条通知：
   - `检测到@xxx的推文，链接...`
4. 生成幽默回复
5. 调用 OpenClaw agent 用浏览器提交评论
6. 提交成功后，再发送：
   - `评论成功`
7. 然后把该 tweet 标记为已处理

## 成功语义
当前版本的“成功”含义是：

- **评论提交成功**
- 不是更深一层的最终平台落库校验

也就是说，这个版本偏实用、偏轻量，不做第三步异步验证。

## 可选环境变量
- `TWITTER_TOKEN`：必需
- `OPENCLAW_BIN`：可选，默认使用 PATH 里的 `openclaw`
- `TWITTER_LISTEN_COMMENT_DATA_DIR`：可选，自定义状态/日志目录

## 打包
如果要重新打包：

```bash
python3 ~/.nvm/versions/node/v22.22.0/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py \
  /Users/pakyo/.openclaw/workspace/skills/twitter-listen-comment \
  /Users/pakyo/.openclaw/workspace/dist
```

打包产物会输出到：
- `dist/twitter-listen-comment.skill`
