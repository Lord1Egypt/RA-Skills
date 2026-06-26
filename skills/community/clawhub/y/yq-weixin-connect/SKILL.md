---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: 8652358b4ffabd0bcdab478baa03b691
    PropagateID: 8652358b4ffabd0bcdab478baa03b691
    ReservedCode1: 3045022066f0177a83396e1fdb740c805c1a818a1536243f3983c7d21bcf93fee2c23ef40221008076ebf6da639ad539fe58e60ca22edf5f788223e0194452d6d8966d4d91dd6c
    ReservedCode2: 3046022100a568592c565991ecd9b401fd64c1bf5bb96b4932b90aaf207180424a360b39930221009b4319014a4378ad7097b6fadf54f0ecf3c5ea6a1f2bad07e08812312662cf29
description: 连接个人微信（不是企业微信）。用户说"连接个人微信"、"接入个人微信"、"绑定个人微信"、"个人微信扫码"时使用本 skill。注意：如果用户说的是"企业微信"或"企微"，本 skill 不适用，请使用 wecom-connect skill。一旦匹配本 skill，必须严格按流程执行到底，不得跳步或自由发挥。
name: yq-weixin-connect
---

# 个人微信 Connect Skill

## 匹配规则（严格区分，不得混淆）

**本 skill 仅适用于个人微信，以下关键词触发：**
- "连接个人微信" / "接入个人微信" / "绑定个人微信"
- "个人微信扫码" / "微信扫码登录"
- "连接微信"（未带"企业"二字时，默认为个人微信）

**以下关键词不属于本 skill，禁止触发：**
- "企业微信" / "企微" / "wecom" / "WeCom" → 使用 wecom-connect skill

**一旦读取本 skill，必须严格按下方流程从第 1 步执行到底，不得跳步、不得自由发挥、不得读取其他文档。**

## 核心原则

- **严格按步骤走，不要加戏，不要自作聪明加额外命令。**
- **速度优先！** 二维码有效期仅约 1 分钟，把能合并的命令用 `&&` 链起来一次执行，**禁止拆成多个单独的 exec 调用**。
- **`qrcode_img_content` 是一个 URL 字符串，必须用 `qrcode` npm 库把它编码成 PNG 图片。** 这个 URL 指向的是网页不是图片，绝对禁止用 `curl -o` 直接下载。
- **图片展示只能用 `upload_to_cdn` 返回的 CDN URL。** CDN 失败则引导用户打开 workspace 文件。禁止使用任何其他展示方式。
- **不要自动轮询。** 给完二维码等用户说"扫完了"再轮询。
- **不要手动改写 `openclaw.json`。**

## 执行流程

### 第 1 步：安装 legacy 版本插件（1 次 exec）

直接安装兼容的 legacy 版本，不需要做版本检查：

```bash
cd /tmp && npm pack @tencent-weixin/openclaw-weixin@legacy 2>&1 | tail -1 && rm -rf ~/.openclaw/extensions/openclaw-weixin && mkdir -p ~/.openclaw/extensions/openclaw-weixin && tar -xzf /tmp/tencent-weixin-openclaw-weixin-*.tgz -C ~/.openclaw/extensions/openclaw-weixin --strip-components=1 && cd ~/.openclaw/extensions/openclaw-weixin && npm install --production 2>&1 | tail -3 && (ln -sf "$(npm root -g)/openclaw" node_modules/openclaw 2>/dev/null || ln -sf "$(dirname "$(which openclaw)")/../lib/node_modules/openclaw" node_modules/openclaw) && ls node_modules/openclaw/package.json >/dev/null 2>&1 && echo "READY" || echo "FAILED"
```

- `READY` → 继续第 2 步
- `FAILED` → 告诉用户安装失败，需要人工排查

### 第 2 步：获取二维码（1 次 exec）

```bash
curl -s "https://ilinkai.weixin.qq.com/ilink/bot/get_bot_qrcode?bot_type=3"
```

从返回 JSON 提取：
- `qrcode` — 保存，轮询用
- `qrcode_img_content` — **这是一个 URL 字符串**，下一步用 `qrcode` npm 库将它编码为 PNG 图片

### 第 3 步：生成 PNG → upload_to_cdn + workspace 双保险

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
- **成功** → 第 4 步用 CDN URL 展示
- **失败** → 重试 upload_to_cdn，最多 3 次
- **3 次仍失败** → 用 workspace 备份兜底

禁止任何替代上传方案（0x0.st、catbox、imgbb、base64、canvas、openclaw upload 等全部禁止）。

### 第 4 步：展示二维码，等用户扫码

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

有效期：约 1 分钟，如果过期了告诉我"过期了"，我会立即生成新的二维码。

---

**CDN 失败（workspace 兜底时）：**

---

## 微信扫码登录

二维码已保存到 `~/workspace/weixin_qr.png`，请打开文件后用**微信**扫码。

扫完在手机上确认登录，然后告诉我"ok"。

有效期：约 1 分钟，如果过期了告诉我"过期了"，我会立即生成新的二维码。

---

然后**停下来，等用户确认**。

### 第 5 步：用户确认后 → 轮询 + 写凭证 + 重启

**5a. 轮询状态（必须加 `--max-time 10`，此 API 是长轮询）：**

```bash
curl -s --max-time 10 "https://ilinkai.weixin.qq.com/ilink/bot/get_qrcode_status?qrcode=<qrcode>"
```

| status | 处理 |
|---|---|
| 超时（exit code 28）或 `wait` | 等 3 秒再 poll |
| `scaned` | 告诉用户"已扫码，请在手机上确认登录" |
| `confirmed` | 成功！提取 `ilink_bot_id`、`bot_token`、`baseurl`、`ilink_user_id` |
| `expired` | 从第 2 步重来（不需要重新装插件） |

**5b. 写入凭证（confirmed 后必须执行）：**

将 `ilink_bot_id` 中的 `@` → `-`、`.` → `-` 得到 `accountId`（例：`a34b410e2e6f@im.bot` → `a34b410e2e6f-im-bot`）。

**API 返回的 `bot_token` 已包含 `ilink_bot_id:` 前缀，直接用 `bot_token` 的值作为 token，不要再拼接 `ilink_bot_id:`，否则 token 双重前缀、认证失败（errcode -14）。**

将真实值内联写入 JS 脚本并执行（`cat` 和 `node` 写在同一个 exec 里）：

```bash
cat > /tmp/write_weixin_account.js << 'SCRIPT'
const fs = require('fs');
const path = require('path');
const home = process.env.HOME;

const accountId = '<accountId>';
const data = {
  token: '<bot_token>',
  savedAt: new Date().toISOString(),
  baseUrl: '<baseurl>',
  userId: '<ilink_user_id>'
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
node /tmp/write_weixin_account.js
```

** `<accountId>`、`<bot_token>`、`<baseurl>`、`<ilink_user_id>` 是占位符，写入脚本时必须替换为 5a 步 confirmed 返回的真实值。

**5c. 重启 Gateway：**

```bash
openclaw gateway restart
```

### 成功回复

---

## 微信连接结果

- 状态：已绑定成功
- Gateway：已重启
- ilink_bot_id: `<ilink_bot_id>`
- ilink_user_id: `<ilink_user_id>`

现在可以直接在微信里发消息了 🎉

---

到此为止。不要再做任何额外操作。不要读文档。

## 二维码过期处理

用户说"过期了" → 只需从第 2 步重新获取二维码，**不需要重新执行第 1 步**。

## 绝对禁止

- **禁止用 `curl -o` / `curl --output` / `wget` 下载 `qrcode_img_content` URL** — 这个 URL 指向的是 HTML 网页不是 PNG 图片，下载得到的是一堆 HTML 代码。必须用 `qrcode` npm 库的 `toFile()` 将 URL 字符串编码为 PNG
- **禁止用 canvas、browser、Generate Images、Image Understanding、MEDIA: 语法 等方式展示二维码** — 只能用 `upload_to_cdn` 返回的 CDN URL，或引导用户打开 workspace 文件
- 禁止把能合并的命令拆成多次 exec（二维码有效期只有 1 分钟，拆太碎会过期）
- 禁止自动开轮询（等用户说"扫完了 / ok"）
- 禁止手动改写 `openclaw.json`
- 禁止跳过写凭证步骤（不写凭证插件无法连接）
- 禁止给用户 `qrcode_img_content` 原始 URL
- 禁止使用替代上传方案（0x0.st、catbox、imgbb、base64 等）
- 禁止在 token 前拼接 `ilink_bot_id:`（bot_token 已包含前缀）
- 禁止在 PNG 生成成功后再用 curl 下载覆盖文件

## 一句话总结

安装 legacy 插件（1 次 exec）→ curl 拿二维码（1 次 exec）→ npm install qrcode + 生成 PNG → upload_to_cdn + workspace 备份 → 展示二维码等用户扫 → 轮询确认 → 写凭证+执行（1 次 exec）→ 重启 gateway → 完成。
