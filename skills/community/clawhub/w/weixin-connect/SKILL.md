---
name: weixin-connect
description: 连接个人微信（不是企业微信）。用户说"连接个人微信"、"接入个人微信"、"绑定个人微信"、"个人微信扫码"时使用本 skill。注意：如果用户说的是"企业微信"或"企微"，本 skill 不适用，请使用 wecom-connect skill。一旦匹配本 skill，必须严格按流程执行到底，不得跳步或自由发挥。
---

# 个人微信 Connect Skill

## ⚠️ 匹配规则（严格区分，不得混淆）

**本 skill 仅适用于个人微信，以下关键词触发：**
- "连接个人微信" / "接入个人微信" / "绑定个人微信"
- "个人微信扫码" / "微信扫码登录"
- "连接微信"（未带"企业"二字时，默认为个人微信）

**以下关键词不属于本 skill，禁止触发：**
- "企业微信" / "企微" / "wecom" / "WeCom" → 使用 wecom-connect skill

**一旦读取本 skill，必须严格按下方流程从第 0 步执行到底，不得跳步、不得自由发挥、不得读取其他文档。**

## 核心原则

- **严格按步骤走，不要加戏。**
- **二维码展示优先 CDN，同时始终保存 workspace 备份。**
- **不要自动轮询。** 给完二维码等用户说"扫完了"再轮询。
- **不要手动改写 `openclaw.json`。**

## 执行流程（写死，照抄执行）

### 第 0 步：检查插件，未装则装

```bash
ls ~/.openclaw/extensions/openclaw-weixin/package.json 2>/dev/null && echo "INSTALLED" || echo "NOT_INSTALLED"
```

- `INSTALLED` → 跳到第 1 步
- `NOT_INSTALLED` → 安装：

```bash
npx -y @tencent-weixin/openclaw-weixin-cli install 2>&1
```

装完验证 `ls ~/.openclaw/extensions/openclaw-weixin/package.json`，确认 `INSTALLED` 后继续。

### 第 1 步：调用 ilink API 获取二维码

```bash
curl -s "https://ilinkai.weixin.qq.com/ilink/bot/get_bot_qrcode?bot_type=3"
```

从返回 JSON 提取：
- `qrcode` — 保存，轮询用
- `qrcode_img_content` — 二维码 URL，生成 PNG 用

### 第 2 步：生成 PNG → upload_to_cdn + workspace 双保险

**一气呵成。**

```bash
cd /tmp && npm install qrcode 2>/dev/null | tail -1
```

```bash
cd /tmp && node -e "const qr=require('qrcode'); qr.toFile('/tmp/weixin_qr.png','<qrcode_img_content>',{width:400,margin:2},(e)=>{if(e)console.error(e);else console.log('saved');})"
```

**同时做两件事：**

1. upload_to_cdn：

```
upload_to_cdn /tmp/weixin_qr.png
```

2. 保存 workspace 备份（无论 CDN 是否成功）：

```bash
cp /tmp/weixin_qr.png ~/workspace/weixin_qr.png
```

CDN 结果处理：
- **成功** → 第 3 步用 CDN URL 展示
- **失败** → 重试 upload_to_cdn，最多 3 次
- **3 次仍失败** → 用 workspace 备份兜底

禁止任何替代上传方案（0x0.st、catbox、imgbb、base64、canvas、openclaw upload 等全部禁止）。

### 第 3 步：展示二维码，等用户扫码

**CDN 成功时（推荐引导语）：**

---

## 微信扫码登录

用**微信**扫一扫下面的二维码：

<CDN 图片 URL>

（已保存备用图片至 ~/workspace/weixin_qr.png）

**操作步骤：**
1. 打开手机**微信** App
2. 扫一扫上面的二维码
3. 在手机上确认登录
4. 扫完告诉我"ok"，我会继续后续步骤

⏱ 有效期：约 1 分钟

---

**CDN 失败（workspace 兜底时）：**

---

## 微信扫码登录

二维码已保存到 `~/workspace/weixin_qr.png`，请打开文件后用**微信**扫码。

扫完在手机上确认登录，然后告诉我"ok"。

⏱ 有效期：约 1 分钟

---

然后**停下来，等用户确认**。

### 第 4 步：用户确认后 → 轮询 + 写凭证 + 重启

**4a. 轮询状态：**

```bash
curl -s "https://ilinkai.weixin.qq.com/ilink/bot/get_qrcode_status?qrcode=<qrcode>"
```

| status | 处理 |
|---|---|
| `wait` | 等 3 秒再 poll |
| `scaned` | 告诉用户"已扫码，请在手机上确认登录" |
| `confirmed` | 成功！提取 `ilink_bot_id`、`bot_token`、`baseurl`、`ilink_user_id` |
| `expired` | 从第 1 步重来 |

**4b. 写入凭证（confirmed 后必须执行）：**

将 `ilink_bot_id` 中的 `@` → `-`、`.` → `-` 得到 `accountId`（例：`a34b410e2e6f@im.bot` → `a34b410e2e6f-im-bot`）。

写一个临时脚本执行：

```bash
cat > /tmp/write_weixin_account.js << 'SCRIPT'
const fs = require('fs');
const path = require('path');
const home = process.env.HOME;

const accountId = '__ACCOUNT_ID__';
const data = {
  token: '__ILINK_BOT_ID__:__BOT_TOKEN__',
  savedAt: new Date().toISOString(),
  baseUrl: '__BASEURL__',
  userId: '__ILINK_USER_ID__'
};

const accountsDir = path.join(home, '.openclaw/openclaw-weixin/accounts');
fs.mkdirSync(accountsDir, { recursive: true });

const accountFile = path.join(accountsDir, accountId + '.json');
fs.writeFileSync(accountFile, JSON.stringify(data, null, 2));
fs.chmodSync(accountFile, 0o600);

const indexPath = path.join(home, '.openclaw/openclaw-weixin/accounts.json');
let existing = [];
try { existing = JSON.parse(fs.readFileSync(indexPath, 'utf-8')); } catch {}
if (!existing.includes(accountId)) existing.push(accountId);
fs.writeFileSync(indexPath, JSON.stringify(existing, null, 2));

console.log('凭证 + 索引写入成功');
SCRIPT
```

将脚本中的占位符替换为实际值后执行：

```bash
sed -i 's/__ACCOUNT_ID__/<accountId>/g; s/__ILINK_BOT_ID__/<ilink_bot_id>/g; s/__BOT_TOKEN__/<bot_token>/g; s/__BASEURL__/<baseurl>/g; s/__ILINK_USER_ID__/<ilink_user_id>/g' /tmp/write_weixin_account.js && node /tmp/write_weixin_account.js
```

**4c. 重启 Gateway：**

```bash
openclaw gateway restart
```

### 成功回复

---

## 微信连接结果

- ✅ 状态：已绑定成功
- ✅ Gateway：已重启
- ilink_bot_id: `<ilink_bot_id>`
- ilink_user_id: `<ilink_user_id>`

现在可以直接在微信里发消息了 🎉

---

到此为止。不要再做任何额外操作。不要读文档。

## 绝对禁止

- 禁止跳过 upload_to_cdn（失败 3 次才用 workspace 兜底）
- 禁止自动开轮询（等用户说"扫完了 / ok"）
- 禁止手动改写 `openclaw.json`
- 禁止跳过写凭证步骤（不写凭证插件无法连接）
- 禁止给用户 `qrcode_img_content` 原始 URL
- 禁止使用替代上传方案（0x0.st、catbox、imgbb、base64、canvas 等）

## 一句话总结

检查插件 → curl 拿二维码 → PNG → CDN + workspace 双保险 → 用户微信扫码 → 轮询确认 → 写凭证文件 → 重启 gateway → 完成。
