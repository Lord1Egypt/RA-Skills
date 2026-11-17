# 持久评论通知与 Agent 唤醒

当用户要求持续监听评论、通知 scode 或其他 Agent 时使用本工作流。先完成 `environment-and-credentials.md`，使用页面 owner 的凭据。接收器不创建新账号。

## 接到现有 Agent

通用接收器运行在 Agent 所在机器，无需公网 webhook。服务端持久保存事件和每个消费者的确认位置；即使接收器离线，回来后仍会收到未确认的批次。

```bash
node scripts/agent_watch.js --consumer review-agent --share '<分享链接>' \
  --cwd '<项目目录>' --command-json '["node","receive-shareone.js"]'
```

`--command-json` 是可执行文件和参数的 JSON 数组，不经过 shell。接收命令从 stdin 读取一行 JSON：

```json
{"source":"shareone","consumer":"review-agent","events":[{"id":"事件UUID","sequence":1,"event_type":"comment.created","share_id":"稳定分享ID","comment_id":"评论UUID","parent_id":null,"actor_role":"visitor","status":"open","created_at":"UTC时间"}]}
```

接收命令必须在**处理完成或可靠写入自己的持久收件箱后**才返回退出码 0。失败返回非零；不能先启动一个易丢失的后台任务就报告成功。事件只带引用，不含评论正文、截图、API Key 或确认令牌。处理前调用评论 API 读最新线程，按 `comments-process.md` 的认领、修改、同链接更新和明确回复流程执行。分享或评论已删除时跳过失效引用。

## 恢复 scode 会话

```bash
node scripts/agent_watch.js --consumer scode-review --share '<分享链接>' \
  --cwd '<项目目录>' --scode-session '<已有会话路径>'
```

接收器启动 `scode acp`，通过 ACP 的 `session/load` 加载指定会话，再用 `session/prompt` 交付事件。只有会话返回 `end_turn` 才确认；交互权限请求会被取消并保留未确认批次。需要机器已安装并配置 scode，且该会话的权限适合任务。请使用专供监听的会话；不要同时在另一个进程操作同一会话。接收器不会增加 scode 权限。不要猜会话路径或自动选择最近一次会话。

默认使用 scode 配置；需要指定模型或认证模式时，可加 `--scode-args-json '["--auth","api-key","--model","sonnet"]'`。这里只放 scode 参数，API Key 仍保存在 scode 的凭据配置里。

## 可靠性与运行方式

- 默认消费上线后记录的全部历史事件；`--start now` 仅在首次注册时从当前位置开始。重复启动同名消费者不会清空进度。上线前已有评论仍需先用 `comment_list.js` 做一次基线检查。
- `--share` 可省略（接收该 owner 全部分享）；使用者确定范围后再开启。消费者名称和范围固定；更换范围使用新名称。
- 默认只把访客变化交给命令，避免 Agent 的回复唤醒自己；其他事件也会正常推进确认位置。`--all-actors` 明确开启全部作者事件。
- 持续长轮询，断网或命令失败后退避重试，最长间隔 60 秒。一个消费者同一时刻只有一个有效批次租约；处理时自动续租。进程崩溃后，5 分钟租约到期即可重领。
- 语义为**至少一次**。处理完成但确认前崩溃可能重复送达；以事件 `id` 去重，并检查当前评论状态，不能假定恰好一次。
- `--timeout-seconds` 默认 1800，超时终止本接收器启动的命令进程树，保留未确认事件。`--once` 只检查并处理一个批次，适合排障和验收。
- 常驻运行由机器的服务管理器监督：Linux 可用 systemd，Windows 可用任务计划程序（登录启动、失败重启、禁止重叠实例）。工作目录指向项目；命令指向安装目录内本脚本。把 API Key 放凭据文件或安全环境配置，不放命令行或任务参数。机器休眠或接收器停止时不会立即唤醒；恢复后补发。
- 启动常驻监听前确定接收项目、消费者范围和具体会话/命令。只完成脚本安装不表示已开始后台监听。

## HTTP 接口

均需 owner 鉴权，路径前缀 `/api/v1/agent-consumers`：

| 请求 | 含义 |
|---|---|
| `PUT /<name>`，`{"share_id":null,"start":"beginning"}` | 幂等注册；可传稳定 ID 或 slug |
| `GET /`（实际不带尾斜杠） | 列出自己的消费者和游标 |
| `GET /<name>` | 查看游标和租约到期时间 |
| `POST /<name>/poll`，`{"limit":50,"wait_seconds":20}` | 最多 100 条、最多等 25 秒；空批次无令牌 |
| `POST /<name>/renew`，`{"lease_token":"..."}` | 将当前租约续到 5 分钟后 |
| `POST /<name>/ack`，`{"lease_token":"..."}` | 确认整个已交付批次；重试同一确认幂等 |
| `POST /<name>/release`，`{"lease_token":"..."}` | 处理失败后释放，不推进游标 |
| `DELETE /<name>` | 删除消费者；需要重置进度时明确执行再注册 |

读取不会确认。`ack` 不接受任意目标游标，过期/被替换的令牌返回 409。每个 owner 的事件有独立递增序号；不同 Agent 使用不同消费者名。当前事件不自动过期，删除消费者不会删事件；不承诺无限保存评论正文，事件中的引用可能已失效。

## 防止重投产生重复写入

事件按至少一次投递：处理成功后才 ACK。发布新页面、上传文件或回复评论时，使用稳定的 `--idempotency-key`，例如 `<event.id>.reply`；重试必须保留同一键和同一请求内容。回复脚本返回实际 `parent_status` / `parent_agent_stance`。幂等冲突时先检查原操作与资源状态，不要换键绕过冲突后重复创建；操作返回 409 busy 时按 `Retry-After` 等待。直接上传确认重试应保留原 `share_id`。
