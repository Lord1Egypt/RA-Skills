# 实现说明

## 为什么可以抓到原始二维码链接

官方插件源码里，登录流程大致是这样的：

- `src/auth/login-qr.ts`
  - 调用 `GET https://ilinkai.weixin.qq.com/ilink/bot/get_bot_qrcode?bot_type=3`
  - 返回 JSON，里面有：
    - `qrcode`
    - `qrcode_img_content`
- `src/channel.ts`
  - 优先尝试用 `qrcode-terminal` 在终端里渲染字符二维码
  - 如果不可用，就回退打印：`二维码链接: ${startResult.qrcodeUrl}`

所以终端二维码只是展示层；真正的登录载体其实是 `qrcode_img_content` 这个 URL。

## 为什么这个方法更靠谱

终端字符二维码很容易在这些场景里失真：

- iMessage / Messenger / Telegram 等聊天软件转发
- 字体不是严格等宽
- 截图时边缘安静区被裁掉
- 通过消息中继表面再次渲染

直接使用 `qrcode_img_content`，让用户在电脑浏览器打开，再用手机微信扫，成功率通常高得多。

## 查询状态的接口

插件还会调用：

`GET https://ilinkai.weixin.qq.com/ilink/bot/get_qrcode_status?qrcode=<token>`

常见成功返回：

```json
{
  "baseurl": "https://ilinkai.weixin.qq.com",
  "bot_token": "<account>@im.bot:<secret>",
  "ilink_bot_id": "...",
  "ilink_user_id": "...",
  "status": "confirmed"
}
```

在实际排障里，只要出现 `bot_token`，基本就可以认为腾讯侧已经接受了登录。

## 本地状态目录

官方插件解析状态目录的顺序是：

- `OPENCLAW_STATE_DIR`
- 否则 `CLAWDBOT_STATE_DIR`
- 否则 `~/.openclaw`

然后把微信状态写到：

- `~/.openclaw/openclaw-weixin/accounts.json`
- `~/.openclaw/openclaw-weixin/accounts/*.json`

## 操作建议

- 优先发原始二维码链接，不要优先发字符二维码。
- 优先看轮询接口结果，不要先怀疑用户没扫好。
- 把“腾讯侧确认成功”和“OpenClaw 本地状态已落盘”分开检查。
- 最终以 `openclaw status` 作为渠道是否可用的准绳。
