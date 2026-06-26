# 服务端配置模板

使用时将 `<占位符>` 替换为真实值。

## 方案 A：VPS 直接出网（速度最快，不需要上游）

```json
{
  "log": {
    "level": "info",
    "timestamp": true,
    "output": "/var/log/sing-box/sing-box.log"
  },
  "inbounds": [
    {
      "type": "vless",
      "tag": "vless-in",
      "listen": "0.0.0.0",
      "listen_port": 443,
      "users": [
        {
          "uuid": "<UUID>",
          "flow": "xtls-rprx-vision"
        }
      ],
      "tls": {
        "enabled": true,
        "server_name": "<SNI_DOMAIN>",
        "reality": {
          "enabled": true,
          "handshake": {
            "server": "<SNI_DOMAIN>",
            "server_port": 443
          },
          "private_key": "<PRIVATE_KEY>",
          "short_id": ["<SHORT_ID>"]
        }
      }
    }
  ],
  "outbounds": [
    {
      "type": "direct",
      "tag": "direct"
    }
  ],
  "route": {
    "final": "direct"
  }
}
```

## 方案 B：全流量走上游 SOCKS5

```json
{
  "log": {
    "level": "info",
    "timestamp": true,
    "output": "/var/log/sing-box/sing-box.log"
  },
  "inbounds": [
    {
      "type": "vless",
      "tag": "vless-in",
      "listen": "0.0.0.0",
      "listen_port": 443,
      "users": [
        {
          "uuid": "<UUID>",
          "flow": "xtls-rprx-vision"
        }
      ],
      "tls": {
        "enabled": true,
        "server_name": "<SNI_DOMAIN>",
        "reality": {
          "enabled": true,
          "handshake": {
            "server": "<SNI_DOMAIN>",
            "server_port": 443
          },
          "private_key": "<PRIVATE_KEY>",
          "short_id": ["<SHORT_ID>"]
        }
      }
    }
  ],
  "outbounds": [
    {
      "type": "socks",
      "tag": "upstream-socks",
      "server": "<UPSTREAM_IP>",
      "server_port": <UPSTREAM_PORT>,
      "version": "5",
      "username": "<UPSTREAM_USER>",
      "password": "<UPSTREAM_PASS>"
    },
    {
      "type": "direct",
      "tag": "direct"
    }
  ],
  "route": {
    "final": "upstream-socks"
  }
}
```

## 方案 C：混合路由（推荐）
AI 服务走上游纯净 IP，其余直连享受高带宽。

```json
{
  "log": {
    "level": "info",
    "timestamp": true,
    "output": "/var/log/sing-box/sing-box.log"
  },
  "inbounds": [
    {
      "type": "vless",
      "tag": "vless-in",
      "listen": "0.0.0.0",
      "listen_port": 443,
      "users": [
        {
          "uuid": "<UUID>",
          "flow": "xtls-rprx-vision"
        }
      ],
      "tls": {
        "enabled": true,
        "server_name": "<SNI_DOMAIN>",
        "reality": {
          "enabled": true,
          "handshake": {
            "server": "<SNI_DOMAIN>",
            "server_port": 443
          },
          "private_key": "<PRIVATE_KEY>",
          "short_id": ["<SHORT_ID>"]
        }
      }
    }
  ],
  "outbounds": [
    {
      "type": "socks",
      "tag": "upstream-socks",
      "server": "<UPSTREAM_IP>",
      "server_port": <UPSTREAM_PORT>,
      "version": "5",
      "username": "<UPSTREAM_USER>",
      "password": "<UPSTREAM_PASS>"
    },
    {
      "type": "direct",
      "tag": "direct"
    }
  ],
  "route": {
    "rules": [
      {
        "domain_suffix": [
          "claude.ai",
          "anthropic.com",
          "openai.com",
          "chatgpt.com",
          "oaistatic.com",
          "oaiusercontent.com"
        ],
        "outbound": "upstream-socks"
      }
    ],
    "final": "direct"
  }
}
```

## SNI 伪装域名选择

| 推荐 | 不推荐 | 原因 |
|---|---|---|
| `www.apple.com` | `cloudflare.com` | Cloudflare 是代理基础设施，GFW 重点关注 |
| `www.microsoft.com` | 国内域名 | 境外代理服务器连国内域名，特征明显 |
| `www.amazon.com` | 个人小站 | TLS 1.3 + H2 支持不稳定 |
| `yahoo.com` | — | — |
