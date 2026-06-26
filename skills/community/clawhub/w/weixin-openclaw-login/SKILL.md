---
name: weixin-openclaw-login
description: 处理微信个人号接入 OpenClaw 的官方登录流程与排障。用于安装 `@tencent-weixin/openclaw-weixin`、获取新的二维码授权链接、查询扫码状态、修复 `openclaw-weixin` 卡在 `SETUP / no token`、以及整理微信 8.0.70+ 接入 OpenClaw 的说明文档。
---

# Weixin OpenClaw Login

这个 skill 用来安装、排查、记录微信个人号接入 OpenClaw 的官方登录流程。

## 快速流程

1. 安装或更新插件：
   - `npx -y @tencent-weixin/openclaw-weixin-cli install`
2. 如果终端字符二维码不方便扫码，直接抓取原始二维码授权链接。
3. 让用户在电脑上打开二维码页面，用微信扫码。
4. 轮询扫码状态，直到出现 `confirmed` 或 `bot_token`。
5. 用 `openclaw status` 检查渠道状态。
6. 如果腾讯侧已经确认登录，但 OpenClaw 仍显示 `SETUP / no token`，检查本地状态文件 `~/.openclaw/openclaw-weixin/`。

## 优先使用脚本

优先使用本 skill 自带脚本：

- 获取新二维码链接：`scripts/get-login-url.js`
- 轮询扫码状态：`scripts/poll-login-status.py <qrcode>`

如果只需要快速人工操作，可继续使用下面的命令版步骤。

## 获取原始授权链接

插件源码表明，登录本质上是调用腾讯 ilink 接口并拿到一个真实的二维码页面 URL。

优先命令：

```bash
node scripts/get-login-url.js
```

脚本会打印：
- `qrcode_img_content`：真正应该在浏览器打开的二维码页面链接
- `QRCODE=...`：用于查询扫码状态的 token

如果不想用脚本，也可以直接执行：

```bash
node - <<'NODE'
const url='https://ilinkai.weixin.qq.com/ilink/bot/get_bot_qrcode?bot_type=3';
fetch(url)
  .then(r=>r.json())
  .then(j=>{
    console.log(j.qrcode_img_content || '');
    console.log('QRCODE=' + j.qrcode);
  });
NODE
```

相比转发终端字符二维码，这种方式通常更稳。

## 查询扫码状态

推荐脚本：

```bash
python3 scripts/poll-login-status.py <qrcode>
```

例如：

```bash
python3 scripts/poll-login-status.py 1cf42ee545e62408992daa64b38a37d9
```

如果只想单次查询，也可以用命令方式：

```bash
python3 - <<'PY'
import urllib.request, json
qrcode = 'REPLACE_ME'
url = f'https://ilinkai.weixin.qq.com/ilink/bot/get_qrcode_status?qrcode={qrcode}'
req = urllib.request.Request(url, headers={'iLink-App-ClientVersion':'1'})
with urllib.request.urlopen(req, timeout=40) as r:
    print(json.loads(r.read().decode()))
PY
```

常见状态：
- `wait`：还没扫码
- `scaned`：已经扫码，但还没最终确认
- `confirmed`：已确认登录
- 返回里还可能带：`bot_token`、`ilink_bot_id`、`baseurl`、`ilink_user_id`

只要出现 `bot_token`，就可以认定腾讯侧登录已经成功，即使 OpenClaw 本地状态还没立刻刷新。

## OpenClaw 本地把微信状态存在哪里

检查这些路径：

- `~/.openclaw/openclaw-weixin/accounts.json`
- `~/.openclaw/openclaw-weixin/accounts/<account-id>.json`
- 可选同步缓冲文件：`*.sync.json`

一个正常的账号文件通常长这样：

```json
{
  "token": "<bot_token>",
  "savedAt": "<timestamp>",
  "baseUrl": "https://ilinkai.weixin.qq.com"
}
```

账号 id 一般会把 `@` 和 `.` 规范化成 `-`，例如：
- 原始：`4b22f436d38f@im.bot`
- 规范化：`4b22f436d38f-im-bot`

## 验证是否真正完成

执行：

```bash
openclaw status
```

成功时通常表现为：
- channel 是 `openclaw-weixin`
- state 是 `OK`
- detail 显示账号数量，而不是 `no token`

失败时通常表现为：
- `SETUP`
- `no token`

## 如果扫码成功了，但 OpenClaw 还显示 `no token`

1. 先确认轮询结果里已经出现 `bot_token`。
2. 再检查 `~/.openclaw/openclaw-weixin/` 下对应文件是否已写入。
3. 如果文件已经存在，重启 gateway：
   - `openclaw gateway restart`
4. 再次执行 `openclaw status` 确认状态。

如果需要更底层的实现说明，读取 `references/implementation-notes.md`。
