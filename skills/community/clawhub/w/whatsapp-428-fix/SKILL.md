---
name: whatsapp-428-fix
description: 修复 WhatsApp Web 连接 428 错误和代理配置问题。当用户遇到 WhatsApp 连接断开 (status 428)、需要配置代理、或在新机器上部署 OpenClaw 后遇到 WhatsApp 连接问题时使用此 Skill。
---

# WhatsApp 428 问题修复

## 快速修复

运行自动修复脚本：

```bash
bash /home/admind/.openclaw/workspace/skills/whatsapp-428-fix/scripts/fix-whatsapp-428.sh
```

## 手动修复步骤

### 1. 检查当前状态

```bash
openclaw status --deep
openclaw channels status
```

### 2. 获取本地 IP

```bash
LOCAL_IP=$(hostname -I | awk '{print $1}')
echo "本地IP: $LOCAL_IP"
```

### 3. 修改 systemd service 配置

编辑 `~/.config/systemd/user/openclaw-gateway.service`，添加代理环境变量：

```ini
[Service]
Environment=HTTP_PROXY=http://LOCAL_IP:10808
Environment=HTTPS_PROXY=http://LOCAL_IP:10808
Environment=ALL_PROXY=http://LOCAL_IP:10808
```

### 4. 重新加载并重启

```bash
systemctl --user daemon-reload
openclaw gateway restart
```

### 5. 验证

```bash
openclaw logs --follow | grep -i whatsapp
```

## 注意事项

- 状态码 428 是 WhatsApp Web 本身机制，配置代理后可更快自动恢复
- 代理端口 10808 需根据实际代理服务调整

---

## 代码级修复（必选）

需要修改 OpenClaw 源码以支持 proxy，按以下步骤修改：

### 1. 添加配置 Schema

在 `auth-profiles-*.js` 的 `WhatsAppSharedSchema` 中添加：

```javascript
proxy: z.string().url().optional()
```

### 2. 修改 session.ts

添加 HttpsProxyAgent 支持：

```javascript
import { HttpsProxyAgent } from "https-proxy-agent";

// 在 makeWASocket 调用中添加 agent
const agent = new HttpsProxyAgent(opts.proxy);
```

### 3. 修改 createWaSocket 调用

在 `channel-web-*.js` 中传入 proxy 参数：

```javascript
const sock = await createWaSocket(false, options.verbose, { 
  authDir: options.authDir, 
  proxy: options.proxy 
});
```

### 4. 账户级别 proxy 配置（多账户）

```javascript
proxy: account.proxy
```
