# openclaw-weixin-fix

修复 `@tencent-weixin/openclaw-weixin@2.4.1` 在 OpenClaw 2026.5.4+ 上的关键 bug。

## 问题

- **Runtime 模块隔离**：`waitForWeixinRuntime()` 超时，微信通道无法启动
- **Content-Length 拒绝**：undici 8.2.0 拒绝手动设置的 Content-Length 头

## 修复

1. `channel.js`：传递 `ctx.channelRuntime` 给 monitor
2. `monitor.js`：优先使用传入的 channelRuntime
3. `api.js`：删除手动设置的 Content-Length 头

## 安装

```bash
# 方法1：使用安装脚本
bash install.sh

# 方法2：手动修复
# 参考 SKILL.md 中的修复步骤
```

## 验证

修复后微信通道应正常收发消息，`openclaw health --json` 显示 `lastError: null`。

## 相关

- GitHub Issue: https://github.com/openclaw/openclaw/issues/78376
- 原插件: https://www.npmjs.com/package/@tencent-weixin/openclaw-weixin
