---
name: weixin-runtime-fix
version: 2.4.2
description: |
  修复 @tencent-weixin/openclaw-weixin@2.4.1 在 OpenClaw 2026.5.4+ 上的两个关键 bug：
  1. Runtime 模块隔离导致 waitForWeixinRuntime 超时
  2. undici 8.2.0 拒绝手动设置的 Content-Length 头
  
  修复后微信通道可正常收发消息。
setup: |
  本修复直接 patch 插件文件，无需额外配置。
  
  安装后会自动备份原文件到 .bak 后缀。
permissions:
  paths:
    - "~/.openclaw/npm/node_modules/@tencent-weixin/openclaw-weixin/**"
  write: true
---

# openclaw-weixin-fix

修复 `@tencent-weixin/openclaw-weixin@2.4.1` 在 OpenClaw 2026.5.4+ 上的关键 bug。

## 问题

1. **Runtime 模块隔离**：`runtime.ts` 被加载两次，`waitForWeixinRuntime()` 读取的实例与 `setWeixinRuntime()` 写入的实例不同，导致超时
2. **Content-Length 拒绝**：undici 8.2.0 不允许手动设置 `Content-Length` 头

## 修复内容

### 改动1：channel.js — 传递 channelRuntime

```diff
  return monitorWeixinProvider({
      ...
      setStatus: ctx.setStatus,
+     channelRuntime: ctx.channelRuntime,
  });
```

### 改动2：monitor.js — 优先使用传入的 channelRuntime

```diff
  let channelRuntime;
- try {
-     const pluginRuntime = await waitForWeixinRuntime();
-     channelRuntime = pluginRuntime.channel;
- }
+ if (opts.channelRuntime) {
+     channelRuntime = opts.channelRuntime;
+ } else {
+     try {
+         const pluginRuntime = await waitForWeixinRuntime();
+         channelRuntime = pluginRuntime.channel;
+     }
+     catch (err) { ... }
+ }
```

### 改动3：api.js — 删除 Content-Length 头

删除 `buildHeaders()` 中手动设置 `Content-Length` 的代码。

## 验证结果

- ✅ 微信消息接收正常
- ✅ 微信回复发送成功
- ✅ 文件上传正常
- ✅ `openclaw health --json` 显示 `lastError: null`

## 注意事项

- 每次 `openclaw plugins install` 重装插件后，需要重新运行此修复
- 备份文件：`channel.js.bak` 和 `monitor.js.bak`

## 相关链接

- GitHub Issue: https://github.com/openclaw/openclaw/issues/78376
- 修复报告: https://github.com/user-attachments/files/27447892/openclaw-weixin-fix-report.md
