---
name: wework-archive-service
description: 企业微信整合服务技能 - 包含普通回调和会话内容存档功能
version: 1.0.0
author: OpenClaw Team
license: MIT
triggers:
  - "企业微信"
  - "wework"
  - "会话存档"
  - "回调服务"
  - "企业微信服务"
  - "存档服务"
  - "wework-archive"
  - "企业微信回调"
  - "微信企业版"
  - "corp wechat"
categories:
  - enterprise
  - messaging
  - automation
  - integration
requirements:
  - python3
  - pip3
  - flask
  - pycryptodome
  - requests
ports:
  - 8400
---

# 企业微信存档服务技能

## 功能概述

本技能提供完整的企业微信整合服务，包含两大核心功能：

1. **普通回调服务** - 处理企业微信应用的事件回调（消息接收、用户变更等）
2. **会话内容存档服务** - 合规的企业微信会话内容存档与查询

---
### ⚠️ 核心配置强制注意事项（必须严格遵守）
1. **企业微信回调URL要求**：所有回调URL必须使用企业已备案的官方域名，禁止使用IP地址或临时域名，否则企业微信会拦截回调请求
2. **公网暴露方案**：若部署服务器无固定公网IP，必须使用Cloudflare Tunnel将本地8400端口映射到企业官方域名，确保HTTPS访问正常
3. **IP白名单配置**：必须在企业微信管理后台「应用管理」-「会话内容存档」页面配置服务器出口IP白名单，否则企业微信会拒绝回调请求
---

## 快速开始

### 1. 安装依赖
```bash
# 进入技能目录
cd skills/wework-archive-service

# 安装Python依赖
pip3 install flask pycryptodome requests
```

### 2. 配置企业微信
1. 复制配置文件模板：
   ```bash
   cp config/wework_config_template.json config/wework_config.json
   ```

2. 编辑配置文件 `config/wework_config.json`，填写以下信息：
   - `callback_token`: 企业微信后台 > 应用管理 > 自建应用 > 接收消息 > Token
   - `callback_encoding_aes_key`: 企业微信后台 > 应用管理 > 自建应用 > 接收消息 > EncodingAESKey
   - `corp_id`: 企业ID（我的企业 > 企业信息）
   - `agent_id`: 应用ID（应用管理 > 自建应用）
   - `corp_secret`: 应用Secret（应用管理 > 自建应用）
   - `archive_token`: 会话存档Secret（管理工具 > 会话内容存档 > 开启 > Secret）

### 3. 启动服务
```bash
# 启动服务
./scripts/start_service.sh

# 验证服务状态
./scripts/verify_service.sh

# 停止服务
./scripts/stop_service.sh
```

### 4. 配置企业微信后台
#### 普通回调配置：
1. 进入企业微信后台 > 应用管理 > 自建应用
2. 点击"接收消息" > 设置API接收
3. 填写以下信息：
   - URL: `http://你的域名/callback`
   - Token: 与配置文件中的 `callback_token` 一致
   - EncodingAESKey: 与配置文件中的 `callback_encoding_aes_key` 一致

#### 会话存档配置：
1. 进入企业微信后台 > 管理工具 > 会话内容存档
2. 点击"开启"
3. 配置回调地址：
   - URL: `http://你的域名/archive/callback`
   - Token: 与配置文件中的 `archive_token` 一致

## 服务接口

### 健康检查
- `GET /health` - 服务健康状态
- `GET /archive/health` - 存档服务健康状态

### 回调接口
- `GET /callback` - 企业微信回调验证（普通应用）
- `POST /callback` - 接收企业微信事件消息
- `POST /archive/callback` - 接收会话存档数据

### 查询接口
- `GET /messages` - 查询所有消息
- `GET /messages/<msg_id>` - 查询特定消息
- `GET /messages/user/<user_id>` - 查询用户消息
- `GET /messages/room/<room_id>` - 查询群聊消息

## Cloudflare Tunnel 配置

### 1. 安装 Cloudflare Tunnel
```bash
# macOS
brew install cloudflared

# Linux
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared.deb

# 验证安装
cloudflared --version
```

### 2. 登录 Cloudflare
```bash
cloudflared tunnel login
```
在浏览器中完成认证。

### 3. 创建隧道
```bash
# 创建隧道
cloudflared tunnel create wework-tunnel

# 查看隧道ID
cloudflared tunnel list
```

### 4. 配置路由
```bash
# 创建配置文件
cloudflared tunnel route dns wework-tunnel wework.yourdomain.com

# 或者手动配置DNS
# 在Cloudflare DNS设置中添加CNAME记录：
# wework.yourdomain.com -> <隧道ID>.cfargotunnel.com
```

### 5. 配置隧道
创建配置文件 `~/.cloudflared/config.yml`：
```yaml
tunnel: <隧道ID>
credentials-file: /Users/你的用户名/.cloudflared/<隧道ID>.json

ingress:
  - hostname: wework.yourdomain.com
    service: http://localhost:8400
  - service: http_status:404
```

### 6. 启动隧道
```bash
# 测试配置
cloudflared tunnel ingress validate

# 启动隧道
cloudflared tunnel run wework-tunnel

# 或作为服务运行
cloudflared service install
sudo systemctl start cloudflared
```

### 7. HTTPS设置
Cloudflare Tunnel自动提供：
- 自动HTTPS证书（Let's Encrypt）
- DDoS防护
- Web应用防火墙
- 全球CDN加速

## 数据库管理

### 初始化数据库
服务首次启动时会自动创建SQLite数据库 `wework_combined.db`。

### 数据库结构
- `messages` - 存储所有消息记录
- `attachments` - 存储附件信息
- `users` - 存储用户信息
- `rooms` - 存储群聊信息

### 备份数据库
```bash
# 备份数据库
cp wework_combined.db wework_combined_backup_$(date +%Y%m%d).db

# 使用SQLite工具查看
sqlite3 wework_combined.db
```

## 故障排除

### 常见问题

#### 1. 服务启动失败
```bash
# 检查端口占用
lsof -ti:8400

# 检查Python依赖
python3 -c "import flask, Crypto, requests"
```

#### 2. 企业微信回调验证失败
- 检查Token、EncodingAESKey是否与后台一致
- 检查服务器时间是否同步
- 检查网络连通性

#### 3. Cloudflare Tunnel连接失败
```bash
# 检查隧道状态
cloudflared tunnel info <隧道ID>

# 查看日志
cloudflared tunnel run wework-tunnel --debug
```

#### 4. 数据库问题
```bash
# 修复数据库
sqlite3 wework_combined.db "VACUUM;"

# 检查数据库完整性
sqlite3 wework_combined.db "PRAGMA integrity_check;"
```

### 日志查看
```bash
# 查看服务日志
tail -f wework_service.log

# 查看详细日志
tail -f wework_combined.log
```

## 安全建议

1. **定期更新配置**：
   - 定期更换Token和EncodingAESKey
   - 使用强密码

2. **网络防护**：
   - 使用Cloudflare Tunnel的防火墙规则
   - 限制访问IP（企业微信IP白名单）

3. **数据安全**：
   - 定期备份数据库
   - 加密敏感数据
   - 设置访问权限

4. **监控告警**：
   - 监控服务运行状态
   - 设置磁盘空间告警
   - 监控API调用频率

## 更新日志

### v1.0.0 (2024-03-05)
- 初始版本发布
- 支持企业微信普通回调
- 支持会话内容存档
- 集成线程安全存储
- 提供完整Cloudflare Tunnel配置

## 技术支持

如有问题，请参考：
1. `references/` 目录下的详细文档
2. 企业微信官方文档
3. Cloudflare Tunnel文档
4. 查看日志文件排查问题

## 许可证

MIT License - 详见 LICENSE 文件