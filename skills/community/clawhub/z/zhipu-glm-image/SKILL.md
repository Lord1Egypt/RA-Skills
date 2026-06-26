---
name: zhipu-glm-image
description: 智谱 GLM-Image 网页端图片生成与下载。用于：检查 image.z.ai 登录态、必要时自动打开浏览器登录、抓取浏览器 Cookie、通过网页接口生成图片并下载到本地。适用于“用智谱生图”“生成一张图并保存/发送”“检查智谱登录状态”“自动打开智谱登录页”等场景。
---

# zhipu-glm-image

这个 skill 走的是**网页登录态**路线，不是独立 API Key 路线。

## 主入口

- `scripts/zhipu_api.js`：检查 session、必要时自动打开登录页、生成图片并下载
- `scripts/network_monitor.js`：历史抓包辅助脚本，仅在逆向接口变化时参考

## 一条命令先准备好

```bash
npm run ready
```

或：

```bash
node zhipu_api.js ready
```

它会自动完成：

1. 检查本地 `~/.zhipu_image_session.json`
2. 必要时尝试抓当前浏览器登录态
3. 如果还没登录，则自动打开 `https://image.z.ai/`
4. 等待登录完成
5. 最后输出 `available` / `unavailable`

## 生成图片

```bash
node zhipu_api.js generate "一只可爱老虎吉祥物，圆润，萌系插画风"
```

也可以省略 `generate`，直接把提示词传进去：

```bash
node zhipu_api.js "一只可爱老虎吉祥物，圆润，萌系插画风"
```

默认会：

- 自动检查/修复登录态
- 调用 `image.z.ai` 网页接口生成图片
- 下载到当前目录下的 `captures/`

## 常用命令

```bash
npm run ready
npm run check-session
npm run login-if-needed
npm run generate
```

## 注意

- 依赖浏览器远程调试端口 `18800`
- 需要浏览器里登录 `https://image.z.ai/`
- session 保存在 Windows 用户目录：`%USERPROFILE%\\.zhipu_image_session.json`
- 首次使用前请先在 `scripts/` 目录执行 `npm install`
- 这是网页接口方案；如果网页字段更新，优先用 `network_monitor.js` 重新观察请求
