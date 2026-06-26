# TG 爬虫 — IP 代理池自建方案

> 📅 生成时间：2026-06-03
> 📄 文档类型：实施指南
> 🔒 文档级别：内部
> 📌 版本：v1.0
> ⚠️ 状态：方案已就绪，待执行

---

## 总体架构

```
                     ┌─────────────────┐
                     │   你的 MacBook   │
                     │  (tg-crawler)    │
                     └───┬───┬───┬─────┘
                         │   │   │
               SOCKS5    │   │   │   SOCKS5
               ┌─────────┘   │   └─────────┐
               ▼             ▼             ▼
         ┌─────────┐  ┌─────────┐  ┌─────────┐
         │ VPS #1  │  │ VPS #2  │  │ VPS #3  │
         │ Dante   │  │ Dante   │  │ Dante   │
         │ :1080   │  │ :1080   │  │ :1080   │
         │ IP: x.1 │  │ IP: x.2 │  │ IP: x.3 │
         └────┬────┘  └────┬────┘  └────┬────┘
              │            │            │
              ▼            ▼            ▼
         ┌─────────────────────────────────────┐
         │           Telegram API              │
         │  限速窗口: (IP, 账号) 各自独立        │
         └─────────────────────────────────────┘
```

## 代码侧已就绪

- `.env` 支持：`TG1_PROXY_HOST/PORT/USER/PASS` ~ `TG3_PROXY_HOST/PORT/USER/PASS`
- `main.py` 支持 SOCKS5 无认证 + 用户名密码认证两种模式
- 代理加载优先级：`TG{account}_PROXY_* > PROXY_* > 本地 IP`
- 代理 IP 到位后直接填入 `.env` 即生效，无需改代码

## VPS 选项对比

| 厂商 | 月费 | 按小时 | IP 更换 | 机房数 | 适合场景 |
|------|------|--------|---------|--------|----------|
| **DigitalOcean** | $6/月起 | ✅ | 删 droplet 重建 | 14 个 | IP 池质量好，控制台干净 |
| **Vultr** | $6/月起 | ✅ | 随时销毁重建 | 32 个 | 最灵活，IP 不干净秒换 |
| **Linode** | $5/月起 | ✅ | 删实例重建 | 11 个 | 老牌，API 好用 |
| **AWS Lightsail** | $3.5/月起 | ✅ | 删实例重建 | 多个 | IP 池大但 TG 识别率较高 |
| **Hetzner** | €4/月起 | ✅ | 删实例重建 | 4 个 | 欧洲为主，亚洲延迟高 |
| **RackNerd** | ~$1.5/月起 | ❌ 月付 | 工单 | 多个 | 最便宜但不灵活 |
| **BandwagonHost** | ~$50/年 | ❌ 年付 | 付费 | 有限 | ❌ IP 段大量被 TG 标记 |

### 推荐组合

| 账号 | 厂商 | 机房 | 月费 | 说明 |
|------|------|------|------|------|
| 1 | DigitalOcean | Singapore | $6 | 主力 |
| 2 | Vultr | Tokyo | $6 | 主力 |
| 3 | RackNerd | Los Angeles | ~$2 | 备胎 |

总月费 ~$14，跨厂商降低同 IP 段被关联风险。

## Dante SOCKS5 一键安装脚本

在每台 VPS 上以 root 执行（每台改不同的用户名密码）：

```bash
#!/bin/bash
set -e

apt update && apt install -y dante-server

cat > /etc/danted.conf << 'DANTE_EOF'
internal: eth0 port = 1080
external: eth0
socksmethod: username
client pass {
    from: 0.0.0.0/0 to: 0.0.0.0/0
    log: connect disconnect error
}
socks pass {
    from: 0.0.0.0/0 to: 0.0.0.0/0
    command: bind connect udpassociate
    log: connect disconnect error
}
DANTE_EOF

echo "=== 创建认证用户 ==="
useradd -r -s /bin/false dante_proxy 2>/dev/null || true
echo "dante_proxy:ChangeThisPassword123" | chpasswd

systemctl restart danted
systemctl enable danted

if systemctl is-active --quiet danted; then
    echo "✅ Dante 运行中"
else
    echo "❌ Dante 启动失败"
fi

echo ""
echo "SOCKS5 代理信息："
echo "  地址: $(curl -s ifconfig.me)"
echo "  端口: 1080"
echo "  用户: dante_proxy"
echo "  密码: ChangeThisPassword123"
```

## 安全加固

```bash
ufw allow 22/tcp
ufw allow 1080/tcp
ufw enable -y

# 强烈建议限制来源 IP
# ufw allow from 你的本地IP to any port 1080 proto tcp
```

## .env 配置格式

VPS 到位后，将 IP/端口/用户名/密码填入：

```ini
# 账号 1 → VPS #1
TG1_PROXY_HOST=45.xxx.xxx.1
TG1_PROXY_PORT=1080
TG1_PROXY_USER=dante_proxy
TG1_PROXY_PASS=xxx

# 账号 2 → VPS #2
TG2_PROXY_HOST=139.xxx.xxx.2
TG2_PROXY_PORT=1080
TG2_PROXY_USER=dante_proxy
TG2_PROXY_PASS=xxx

# 账号 3 → VPS #3
TG3_PROXY_HOST=155.xxx.xxx.3
TG3_PROXY_PORT=1080
TG3_PROXY_USER=dante_proxy
TG3_PROXY_PASS=xxx
```

## 执行步骤

1. 选厂商 → 买 VPS（建议 DigitalOcean + Vultr + RackNerd 各一台）
2. SSH 到每台 VPS → 跑一键脚本
3. 安全加固（UFW 防火墙）
4. 将 IP/端口/用户/密码告知小黑 → 填入 `.env`
5. 用 `--account 1/2/3` 各跑一次 discover，验证三账号各自走不同 IP

---

> ⏸️ 当前状态：方案就绪，等待执行
