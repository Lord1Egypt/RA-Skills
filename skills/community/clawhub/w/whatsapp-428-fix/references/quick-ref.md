# WhatsApp 428 问题详细参考

## 问题说明

- **status 428**: WhatsApp Web 连接中断，Gateway 自动重连成功
- 配置 proxy 后，WhatsApp Web 通过指定代理服务器连接，断连后更快恢复

## 核心修复逻辑

1. **systemd service 添加代理环境变量**
   - HTTP_PROXY, HTTPS_PROXY, ALL_PROXY
   - 需要获取本地 IP (hostname -I)

2. **代码级修复** (如需永久解决)
   - 在 auth-profiles-*.js 添加 proxy 字段到 WhatsAppSharedSchema
   - 在 session.ts 添加 HttpsProxyAgent 支持
   - 在 channel-web-*.js 传入 proxy 参数

## 验证命令

```bash
openclaw status --deep
openclaw channels status
openclaw logs --follow | grep -i whatsapp
```

## 代理端口

默认 10808，需根据实际代理服务调整
