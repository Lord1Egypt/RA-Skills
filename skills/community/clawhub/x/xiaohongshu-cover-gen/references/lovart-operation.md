# Lovart 平台操作手册（agent-browser 自动化）

> 基于 5 轮实战验证，14 个具体卡点的解决方案沉淀。
> 
> ⚠️ **核心原则**：每次操作遇到新卡点，必须回来更新这个文档。

---

## 前置准备

### Lovart 账号认证

Lovart 不支持 headless 浏览器的 Google/Apple OAuth，必须用 cookies 登录。

**获取 cookies 的方法**：
1. 在正常浏览器中登录 Lovart（lovart.ai）
2. 打开 DevTools → Application → Cookies → `www.lovart.ai`
3. 导出以下 3 个关键 cookies：

| Cookie 名 | 说明 | 备注 |
|-----------|------|------|
| `usertoken` | JWT 认证令牌 | 最重要，约 600 字符 |
| `useruuid` | 用户 UUID | |
| `webid` | 设备标识 | |

4. 保存为 JSON 文件（如 `.lovart_cookies.json`）

**JWT 有效期**：约 7 天，过期后需重新获取。

---

## Phase 0：页面加载

> **已知问题**：`agent-browser open "https://www.lovart.ai/zh/home"` 经常超时（25s 限制）。

**✅ 两步导航法**：

```bash
# Step 1: 先打开空白页（秒开）
agent-browser open "about:blank"

# Step 2: 用 JS 导航（不受 25s 限制）
agent-browser eval "window.location.href = 'https://www.lovart.ai/zh/home'"

# Step 3: 等待加载
agent-browser wait 8000
```

**❌ 不要直接 open**：
```bash
# 这个会超时！
agent-browser open "https://www.lovart.ai/zh/home"
```

---

## Phase 1：Cookies 注入 + 登录验证

### Step 0：JWT 过期预警

> 注入前先检查 JWT 是否过期，避免浪费时间。

```bash
node -e "
const fs = require('fs');
const cookies = JSON.parse(fs.readFileSync('.lovart_cookies.json', 'utf8'));
const token = cookies.find(c => c.name === 'usertoken');
if (!token) { console.log('❌ 未找到 usertoken'); process.exit(1); }
const payload = JSON.parse(Buffer.from(token.value.split('.')[1], 'base64').toString());
const exp = new Date(payload.exp * 1000);
const now = new Date();
const hoursLeft = (exp - now) / 3600000;
console.log('JWT 过期时间:', exp.toISOString());
console.log('剩余时间:', hoursLeft.toFixed(1), '小时');
if (hoursLeft <= 0) console.log('❌ 已过期！需重新获取 cookies');
else if (hoursLeft <= 24) console.log('⚠️ 24h 内过期，建议更新');
else console.log('✅ JWT 有效');
"
```

### Step 1：确认域名

> ⚠️ cookies 不能在 `about:blank` 设置（会报 "Blank page can not have cookie"）。
> Phase 0 完成后，当前页面已在 lovart.ai 域名下。

### Step 2：注入 cookies

**方法 A**（推荐）：`agent-browser cookies set`

```bash
agent-browser cookies set name=usertoken value=<JWT> domain=www.lovart.ai path=/ secure=true sameSite=Lax
agent-browser cookies set name=useruuid value=<UUID> domain=www.lovart.ai path=/ secure=true sameSite=None
agent-browser cookies set name=webid value=<WEBID> domain=www.lovart.ai path=/ secure=true sameSite=Lax
```

**方法 B**（备选，解决超长值报错）：`JS document.cookie`

> JWT token 约 600 字符时，方法 A 可能报 `Protocol error (Storage.setCookies): Invalid cookie fields`。

```bash
agent-browser eval "document.cookie='usertoken=<JWT>; path=/; secure; SameSite=Lax'; document.cookie='useruuid=<UUID>; path=/; secure; SameSite=Lax'; document.cookie='webid=<WEBID>; path=/; secure; SameSite=Lax'"
```

> 注意：JS `document.cookie` 无法设置 httpOnly cookies，但 Lovart 的 3 个关键 cookies 都不是 httpOnly。

### Step 3：刷新验证

```bash
agent-browser eval "window.location.reload()"
agent-browser wait 5000
agent-browser screenshot
```

**✅ 成功**：页面跳转到 `/zh/home`，右上角有用户头像，可见积分数字
**❌ 失败**：停留在登录弹窗 → 检查 JWT 是否过期

---

## Phase 2：关闭引导弹窗

> 每次新会话都会弹出引导弹窗，**关闭顺序极其重要**！

| 顺序 | 弹窗 | 按钮 | 说明 |
|------|------|------|------|
| 1️⃣ | "品牌套件"引导（首页） | **"跳过"** | |
| 2️⃣ | "The All-New Lovart Canvas"（Canvas 页） | **"Close"** | ⚠️ 最上层，全屏遮罩 |
| 3️⃣ | Fast mode 提示（Canvas） | **"Got it"** | 必须先关 2️⃣ |
| 4️⃣ | 低速生成提示（偶发） | **"知道了"** | |

```bash
agent-browser screenshot  # 先看状态
agent-browser snapshot -i  # 确认弹窗层级

# Canvas 页面：必须先关 Close，再关 Got it
# 如果 snapshot 只有 Close/Next 按钮 → 有全屏遮罩，先关掉
agent-browser click @eX   # Close 按钮
agent-browser wait 1000
agent-browser find text "Got it" click
agent-browser wait 1000
```

> ⚠️ **翻车教训**：先点 "Got it" 会被 Canvas 引导的遮罩层拦截，超时 25s。
> **识别方法**：snapshot 中只有 Close/Next 等按钮，看不到页面其他元素 → 有全屏遮罩。

---

## Phase 3：输入 Prompt + 生图

### 输入 prompt

```bash
# 1. 找到输入框
agent-browser snapshot -i

# 2. 点击获取焦点 + 分段输入
agent-browser click @e8
agent-browser type @e8 "第一段：场景描述..."
agent-browser type @e8 " 第二段：品牌元素..."
agent-browser type @e8 " 第三段：文字需求..."
agent-browser type @e8 " 第四段：风格配色..."

# 3. 找发送按钮（输入后从 disabled 变为 enabled 的按钮）
agent-browser snapshot -i
agent-browser click @eXX
```

> ⚠️ **长 prompt 处理**：agent-browser 命令 ≤ 1024 字节。
> - `type` = 追加输入（不清空），`fill` = 清空后填入
> - 分段时用 `type`，每段开头加空格分隔

> ⚠️ **发送按钮识别**：输入前是 `[disabled]`，输入后变 enabled。
> 最可靠：输入前后各做一次 snapshot，对比哪个 button 状态变了。

### 等待生成

```bash
agent-browser wait 10000
agent-browser screenshot    # 检查是否进入 Canvas

# 分段等待（每段 ≤ 20s）+ 截图轮询
agent-browser wait 15000
agent-browser screenshot
agent-browser wait 20000
agent-browser screenshot
# 重复 3-5 轮直到看到结果
```

> ⚠️ **不要** `wait 30000` 以上！会触发 idle timeout 被系统中断。

### Prompt 编写规则

| 规则 | 说明 |
|------|------|
| 语言 | 英文优先（效果更精准），中文也可 |
| 格式 | 自然语言描述，不是 SD/MJ 式 tag |
| Logo | 必须精确描述视觉元素，不能只写品牌名 |
| 文字 | 逐字指定标题内容（Lovart 有设计字体能力） |
| 比例 | 明确写 "portrait 3:4 ratio" 或 "1080x1440px" |
| 风格 | 明确写风格关键词 |

---

## Phase 4：获取图片 + 下载

### 获取图片 URL

```bash
agent-browser eval "JSON.stringify(Array.from(document.querySelectorAll('img[src*=\"artifact\"]')).map(i => ({src: i.src, w: i.naturalWidth, h: i.naturalHeight})))"
```

> **URL 技巧**：去掉 `?x-oss-process=...` 参数可获取原始高质量 PNG。

### 下载图片

> ⚠️ `a.lovart.ai` 的 SSL 与 curl/Python requests 不兼容。

**✅ 用 Node.js 下载**：

```bash
NODE_TLS_REJECT_UNAUTHORIZED=0 node -e "
const https = require('https');
const fs = require('fs');
const url = '<IMAGE_URL>';
https.get(url, {rejectUnauthorized: false}, res => {
  const chunks = [];
  res.on('data', c => chunks.push(c));
  res.on('end', () => {
    fs.writeFileSync('<OUTPUT_PATH>', Buffer.concat(chunks));
    console.log('Downloaded:', Buffer.concat(chunks).length, 'bytes');
  });
}).on('error', e => console.error(e));
"
```

### 方法 C：浏览器内 fetch + base64 分块提取（🔴 当 Node.js 也 SSL 失败时）

> ⚠️ 某些情况下本地所有 SSL 客户端（Node.js / curl / Python）都会失败
> （如 macOS LibreSSL 3.3.6 与 CDN 的 TLS 配置不兼容）。
> 浏览器（Chromium）有独立的 SSL 栈（BoringSSL），不受本地限制。

```bash
# Step 1: 确保 agent-browser 在 lovart.ai 域名下

# Step 2: 浏览器内 JS fetch → base64
agent-browser eval "fetch('<IMAGE_URL>').then(r=>r.blob()).then(b=>{const reader=new FileReader();reader.onloadend=()=>{window._imgData=reader.result;document.title='IMG_READY_'+reader.result.length};reader.readAsDataURL(b)})"

# Step 3: 等待完成
agent-browser wait 10000
agent-browser eval "document.title"
# 输出: "IMG_READY_<总长度>"

# Step 4: 分块提取（每块 ~500KB）
agent-browser eval "window._imgData.split(',')[1].length"
# 假设 7000000，分 14 块

rm -f /tmp/lovart_b64.txt
for i in $(seq 0 13); do
  START=$((i * 500000))
  END=$(((i + 1) * 500000))
  agent-browser eval "window._imgData.split(',')[1].substring($START, $END)" \
    | sed 's/^"//;s/"$//' >> /tmp/lovart_b64.txt
done

# Step 5: base64 解码
node -e "
const fs = require('fs');
const b64 = fs.readFileSync('/tmp/lovart_b64.txt', 'utf8').replace(/\n/g, '');
const buf = Buffer.from(b64, 'base64');
fs.writeFileSync('<OUTPUT_PATH>', buf);
console.log('Downloaded:', buf.length, 'bytes');
console.log('PNG header:', buf.slice(0,4).toString('hex'));
"
```

> **注意**：不要尝试 `agent-browser open "<图片URL>"`，会触发浏览器下载行为而非渲染。

---

## Phase 5：关闭浏览器

> 必须做！不关闭 → 下次操作可能触发 hCaptcha。

```bash
agent-browser close
```

---

## hCaptcha 防触发规则

- 每次会话只生图 **1-2 张**
- 生成完毕**立即关闭浏览器**
- 下次：重新打开 → 注入 cookies → 生图
- 触发 hCaptcha → 关浏览器，等 5 分钟，重新开始

## 积分控制

- 低速模式（Relax）不消耗积分，但可能繁忙失败
- 单次配图任务 **≤ 100 积分**
- 每次生图前后记录积分变化
- 超标前停下来和用户确认
