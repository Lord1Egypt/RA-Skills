# 常见服务端口参考 / Common Service Port Reference

## 安全相关端口 / Security-Related Ports

| 端口 / Port | 服务 / Service | 说明 / Description | 安全性 / Security |
|------|------|------|--------|
| 22 | SSH | 远程登录 / Remote login | 需配置密钥认证,禁用密码登录 / Requires key authentication, disable password login |
| 23 | Telnet | 远程登录 / Remote login | 不安全,建议禁用 / Insecure, recommended to disable |
| 80 | HTTP | Web服务 / Web service | 建议重定向到HTTPS / Recommended to redirect to HTTPS |
| 443 | HTTPS | 加密Web服务 / Encrypted web service | 安全 / Secure |

## 数据库端口 / Database Ports

| 端口 / Port | 服务 / Service | 说明 / Description |
|------|------|------|
| 3306 | MySQL | 数据库,应限制访问IP / Database, should restrict access IP |
| 5432 | PostgreSQL | 数据库,应限制访问IP / Database, should restrict access IP |
| 6379 | Redis | 缓存,默认无认证,高风险 / Cache, no authentication by default, high risk |
| 27017 | MongoDB | NoSQL数据库,默认无认证 / NoSQL database, no authentication by default |

## 常见后门/恶意端口 / Common Backdoor/Malicious Ports

| 端口 / Port | 说明 / Description |
|------|------|
| 4444 | Metasploit reverse shell默认端口 / Metasploit reverse shell default port |
| 5555 | ADB调试端口,可能被滥用 / ADB debug port, may be abused |
| 6666-6669 | IRC/常见后门端口 / IRC/common backdoor ports |
| 31337 | 常见黑客后门端口(Elite拼写) / Common hacker backdoor port (Elite spelling) |
| 12345 | NetBus等木马常用端口 / NetBus and other trojan common ports |
| 5900 | VNC远程桌面,应加密 / VNC remote desktop, should be encrypted |
| 8080 | 常用代理端口,需确认是否为预期 / Common proxy port, need to confirm if expected |

## 应用服务端口 / Application Service Ports

| 端口 / Port | 说明 / Description |
|------|------|
| 3000 | Node.js开发服务器 / Node.js development server |
| 5000 | Flask/Django开发服务器 / Flask/Django development server |
| 8000 | Python HTTP服务器 / Python HTTP server |
| 9000 | Node.js/SonarQube |

## OpenClaw相关端口(需确认) / OpenClaw Related Ports (Need Confirmation)

OpenClaw可能使用的端口(需根据实际部署确认) / Ports OpenClaw may use (need to confirm based on actual deployment):
- 通常使用非标准端口 / Usually uses non-standard ports
- 可能在配置文件中指定 / May be specified in configuration files
- 检查 `/opt/openclaw/config/` 或类似目录 / Check `/opt/openclaw/config/` or similar directories
