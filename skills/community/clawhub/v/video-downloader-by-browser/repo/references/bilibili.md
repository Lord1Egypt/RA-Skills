# 哔哩哔哩（bilibili.com）流媒体 —— 逆向笔记

> 2026-09 实测于一个 1080P 音乐 MV（3 分钟级），登录态下成功下载

## 一、入口与链接解析

- 分享短链 `b23.tv/XXXX` 在**无 cookie 时会被 412 拦截**（缺 buvid），直接解析无效。
- 先解出真实 BV 号：`curl -sIL b23.tv/XXXX` 看 `location`，得到
  `https://www.bilibili.com/video/BVxxxxxxxxxx`（BV 号是 12 位字母数字）。
- **始终用 BV 直链**下载，不要依赖短链。

## 二、登录态 = 画质门槛（关键）

B站高画质**必须登录**：

- 1080P 高清：需有效 `SESSDATA`（登录态）
- 未登录：`yt-dlp` / 接口一律 **412 PRECONDITION FAILED**（风控升级，必须带 cookie）

→ **下载 B站前务必先确认登录态；未登录就先停下，让用户登录，再下载。**
  拿不到登录态会直接 412，下不下来。

## 三、登录方式选型（重要踩坑）

| 方式 | 结果 | 结论 |
|---|---|---|
| 账号密码 + 短信验证码 | 点"获取验证码"后弹 **Geetest 点选验证码**（提示 `Select in this order:` + 4 个扭曲文字，如"烧填鸭港"，需按序点击） | ❌ **不可用**，见下方实测 |
| 扫码登录（QR） | 不触发图形验证码；用户用 App 扫 → 确认 | ✅ **唯一可行**，已验证 |

→ **统一走扫码登录**：`scripts/bili_login_qr.py <工作目录> [超时秒]`
   生成二维码 → 用户扫 → 脚本轮询 SESSDATA → 落盘 `<工作目录>/bilibili_cookies.txt`。

### ⚠️ 短信登录为何不可用（2026-09-25 二次实测确认）

**Geetest 拦在"发短信"之前，验证码根本发不出去。** 完整链路：

```
填手机号 → 点"获取验证码" → 🔴 Geetest 点选验证码弹出 → (过不去) → 短信不发送
```

实测细节（无头 Chromium + 真实手机号）：
- 短信登录 tab 可切、手机号框可填（`input[placeholder='请输入手机号']`）
- "获取验证码"是 `div.clickable`，点后立刻出现 `.geetest_panel.geetest_wind`
- 验证码图：`.geetest_item_img`（约 307×343），提示 `Select in this order:`，需按序点 4 个**扭曲变形+彩色**文字
- 表单里另有一个 `输入图片中的内容`（图片验证码）输入框，可见 B站对短信登录设了多道验证

**结论：不要再尝试短信登录路径，不要在 skill 里把它写成"首选"。**
用户若坚持"我要给账号、你发验证码"，应如实告知：Geetest 卡在发短信前，此路不通，需改走扫码。
（真实浏览器里 Geetest 同样会弹，只是用户本人能手动点过——但沙箱无显示器，无人在场点选。）

## 四、cookie 处理细节

- `yt-dlp` 用 `--cookies bilibili_cookies.txt` 注入。
- **必须修 `expires=-1`**：部分会话级 cookie `expires=-1`，`yt-dlp` 会跳过，导致 cookie 不完整 → 仍 412。
  用 `sed -i 's/\t-1\t/\t0\t/g'` 把 `-1` 改成 `0`（保留会话 cookie）即可。
- 关键三项：`SESSDATA` / `bili_jct` / `DedeUserID`，缺一不可判断登录。
- cookie 一律落**运行时工作目录**，绝不回写进 skill、绝不随包分发。

## 五、下载（DASH 分离流）

B站是 **DASH**：音视频分开两个流，需合并。

```bash
# 列出可用清晰度（先确认有 1080P）
yt-dlp --cookies bilibili_cookies.txt -F "<BV直链>"
# 选 1080P 视频(H.264) + 音轨，合并为 mp4
yt-dlp --cookies bilibili_cookies.txt -f "30080+30280" --merge-output-format mp4 -o out.mp4 "<BV直链>"
```

常用 format-id（以实际 `-F` 输出为准，会随版本变）：

- `30080` 1080P 视频(H.264) / `30077` 等更多档位
- `30280` 音轨(约 175k) / `30232` 更高码率音轨
- 不确定就 `-f "bestvideo+bestaudio"`（但可能得到 webm/AV1，兼容性差，谨慎）

## 六、与优酷模型对比

| 维度 | 优酷 | B站 |
|---|---|---|
| 分片形态 | 大分片 MP4（~140s/片） | 单 m3u8 + 多 ts / DASH 分离流 |
| 下载方式 | 浏览器拦截 URL + 并发 Range 合并 | `yt-dlp` 直接下（带 cookie） |
| 登录影响画质 | 是（480/720/1080 三档） | 是（1080P+ 需 SESSDATA） |
| 登录方式 | 浏览器内用户手动（共享 profile） | 扫码登录脚本（QR） |

## 七、令牌时效

- `bili_ticket` 等会过期（数小时~数天），过期后 `yt-dlp` 重新 412。
- 失效了重新跑 `bili_login_qr.py` 扫一次即可，无需改任何东西。
- 登录态存**运行时工作目录**，不进 skill、不随包分发。
