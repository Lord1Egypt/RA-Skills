# 故障排查清单（6 种模式）

## 故障 1：假成功（最常见、最坑）

**症状**：脚本输出 `SUCCESS: push sent`，但用户手机微信**没收到**。

**根因**：只判断 HTTP 200，不解析业务层 `ret`/`errcode`。

**v1 触发场景**（已修）：
```python
# v1 假成功代码
if result.returncode == 0:
    return True   # ⚠️ 只看 curl 退出码
```

**v2 修法**（本 skill 默认）：
```python
# v2 真成功判定
if "Sent via" in result.stdout and result.returncode == 0:
    return True
```

**如何验证**：
```bash
wechat-push "test"  # 推完问你"收到了吗？"
```

## 故障 2：errcode -14, "session timeout"

**症状**：
```json
{"errcode":-14, "errmsg":"session timeout"}
```

**根因**：bot session 被微信服务端踢出。

**触发条件**：
- 静默超过几小时（具体阈值未测出）
- 触发 errcode=-14 后，session-guard 暂停 1 小时

**修法**：
1. **短期**：换另一个活跃账号（`~/.openclaw/openclaw-weixin/accounts/` 扫一下 mtime 最近的）
2. **长期**：用户手机微信**重新扫码**激活

**怎么知道哪些账号是死的**：
```bash
for f in ~/.openclaw/openclaw-weixin/accounts/*@im.bot.json; do
    if [[ "$(basename $f)" != *-* ]]; then
        mtime=$(stat -f "%Sm" "$f")
        echo "$(basename $f): $mtime"
    fi
done
```

**token > 30 天没改的 = 大概率死了**。

## 故障 3：ret=-2 / HTTP 000（裸 curl）

**症状**：curl 直接返非 0 退出码，或 HTTP 000（连不上）。

**根因**：
- macOS 系统代理干扰
- ilink 服务端拒绝非插件内部连接
- CGN / 防火墙

**修法**：**永远不要裸 curl ilink。** 必须走 `openclaw message send` CLI。

**反例**（不要这样写）：
```bash
curl -X POST https://ilinkai.weixin.qq.com/ilink/bot/sendmessage \
  -H "Authorization: Bearer $TOKEN" ...  # ❌ 不会通
```

**正例**（正确写法）：
```bash
openclaw message send --channel openclaw-weixin \
  --account <YOUR_BOT_ID>-im-bot \
  --target "$OPENID" -m "$MSG"  # ✅
```

## 故障 4：半活（getupdates 通，sendmessage 不通）

**症状**：
- 接收用户消息正常（getupdates 工作）
- 推消息给用户失败（sendmessage 返错）

**根因**：OpenClaw 插件内部状态机错位。getupdates 长连接活着，但 sendmessage 走的另一条投递通道断了。

**修法**：
```bash
# 重启 OpenClaw 微信插件
launchctl unload ~/Library/LaunchAgents/com.openclaw.wechat-tunnel.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.wechat-tunnel.plist
```

**等价的 graceful 重启**：
```bash
# 看 PID
launchctl list | grep openclaw-weixin
# 找主进程，kill -HUP
```

## 故障 5：静默被踢（推 8 次突然全失败）

**症状**：连续推几次都成功，之后突然全失败。

**根因**：bot session 静默过久（无 getupdates 轮询）→ 微信服务端踢出。

**缓解**：
- **接 ilink-probe 探活**（每 15 分钟 silent 推一次）—— 保持活跃
- **不依赖 push 的"持续 24h 不掉"**——把 push 当 transient 操作

## 故障 6：openid 不对（推了但用户没收到且无报错）

**症状**：所有检查都过，但消息推错人 / 推空。

**根因**：`--to` 传错 openid，或者配置文件里的 openid 失效。

**修法**：
```bash
# 1. 确认配置
cat ~/.config/wechat-push/config

# 2. 推给自己（如果 openid 是自己的）
wechat-push --to "$MY_OPENID" "test"

# 3. 如果推给别人，确认他们的 openid
#    openid 怎么拿：见 references/protocol-notes.md 7
```

## 终极排查路径

```bash
# 1. 跑 verify 看链路
wechat-push-verify

# 2. 跑 doctor 看健康
wechat-push-doctor

# 3. 手动推一次 silent 看 OpenClaw CLI 反馈
wechat-push --silent "manual test"

# 4. 推一次非 silent + 问用户
wechat-push "你看到了吗？"
```

如果前 3 步都过、用户还是没收到 → 检查 openid（故障 6）。
如果前 3 步就有 fail → 按 fail 那一跳对应的故障模式查。
