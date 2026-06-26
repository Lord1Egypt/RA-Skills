# 企业微信存档服务技能

一个完整的OpenClaw技能，用于部署和管理企业微信整合服务，包含普通回调和会话内容存档功能。

## 功能特性

- ✅ **双回调支持**: 同时处理普通应用回调和会话存档回调
- ✅ **线程安全存储**: 使用SQLite数据库安全存储消息数据
- ✅ **完整API接口**: 提供消息查询、用户管理、健康检查等接口
- ✅ **Cloudflare集成**: 支持通过Cloudflare Tunnel安全暴露到公网
- ✅ **一键部署**: 提供完整的安装和配置脚本
- ✅ **合规设计**: 遵循企业微信合规要求和数据保护法规

## 快速开始

### 1. 安装技能
```bash
# 克隆或复制技能目录到OpenClaw技能目录
cp -r wework-archive-service ~/.openclaw/workspace/skills/
```

### 2. 配置服务
```bash
cd skills/wework-archive-service

# 复制配置文件模板
cp config/wework_config_template.json config/wework_config.json

# 编辑配置文件，填写企业微信信息
vim config/wework_config.json
```

### 3. 安装依赖
```bash
# 安装Python依赖
pip3 install flask pycryptodome requests

# 或使用脚本安装
./scripts/verify_service.sh
```

### 4. 启动服务
```bash
# 启动服务
./scripts/start_service.sh

# 验证服务状态
./scripts/verify_service.sh

# 停止服务
./scripts/stop_service.sh
```

## 目录结构

```
wework-archive-service/
├── SKILL.md                    # 技能元数据和使用说明
├── README.md                   # 本文件
├── scripts/                    # 脚本目录
│   ├── wework_combined_service.py    # 主服务文件
│   ├── simple_storage.py             # 存储系统
│   ├── start_service.sh              # 启动脚本
│   ├── stop_service.sh               # 停止脚本
│   └── verify_service.sh             # 验证脚本
├── config/                     # 配置目录
│   └── wework_config_template.json   # 配置文件模板
├── references/                # 参考资料
│   ├── 企业微信API接口文档.md
│   ├── 企业微信后台配置步骤.md
│   ├── 合规要求.md
│   └── Cloudflare Tunnel完整配置文档.md
├── assets/                    # 资源文件
│   └── init_database.sql      # 数据库初始化脚本
└── wework_service.pid        # 服务PID文件（运行时生成）
```

## 配置说明

### 必需配置项
在 `config/wework_config.json` 中配置：

```json
{
  "callback_token": "企业微信后台获取的Token",
  "callback_encoding_aes_key": "43位EncodingAESKey",
  "corp_id": "企业ID",
  "agent_id": 1000002,
  "corp_secret": "应用Secret",
  "archive_token": "会话存档Secret"
}
```

### 可选配置项
```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8400,
    "debug": false
  },
  "database": {
    "path": "wework_combined.db",
    "backup_enabled": true
  },
  "cloudflare": {
    "tunnel_enabled": true,
    "domain": "wework.yourdomain.com"
  }
}
```

## 服务接口

### 健康检查
- `GET /health` - 整体服务健康状态
- `GET /archive/health` - 存档服务健康状态

### 回调接口
- `GET /callback` - 普通回调验证（企业微信调用）
- `POST /callback` - 接收普通回调消息
- `POST /archive/callback` - 接收会话存档数据

### 查询接口
- `GET /messages` - 查询所有消息
- `GET /messages/<msg_id>` - 查询特定消息
- `GET /messages/user/<user_id>` - 查询用户消息
- `GET /messages/room/<room_id>` - 查询群聊消息

### 管理接口
- `GET /stats` - 获取统计信息
- `GET /config` - 查看当前配置
- `POST /backup` - 备份数据库

## Cloudflare Tunnel 配置

### 快速配置
```bash
# 1. 安装Cloudflared
brew install cloudflared

# 2. 登录Cloudflare
cloudflared tunnel login

# 3. 创建隧道
cloudflared tunnel create wework-tunnel

# 4. 配置DNS
cloudflared tunnel route dns wework-tunnel wework.yourdomain.com

# 5. 启动隧道
cloudflared tunnel run wework-tunnel
```

### 详细配置
参考 `references/Cloudflare Tunnel完整配置文档.md` 获取完整配置指南。

## 企业微信后台配置

### 普通回调配置
1. 企业微信后台 > 应用管理 > 自建应用
2. 点击"接收消息" > 设置API接收
3. 配置：
   - URL: `https://wework.yourdomain.com/callback`
   - Token: 与配置文件一致
   - EncodingAESKey: 与配置文件一致

### 会话存档配置
1. 企业微信后台 > 管理工具 > 会话内容存档
2. 点击"开启"
3. 配置回调地址：
   - URL: `https://wework.yourdomain.com/archive/callback`
   - Token: 与配置文件中的archive_token一致

## 数据库管理

### 初始化数据库
服务首次启动时会自动创建数据库。如需手动初始化：

```bash
sqlite3 wework_combined.db < assets/init_database.sql
```

### 备份数据库
```bash
# 手动备份
cp wework_combined.db wework_combined_backup_$(date +%Y%m%d).db

# 使用SQLite工具
sqlite3 wework_combined.db ".backup backup.db"
```

### 数据库维护
```bash
# 优化数据库
sqlite3 wework_combined.db "VACUUM;"

# 检查完整性
sqlite3 wework_combined.db "PRAGMA integrity_check;"
```

## 监控和日志

### 查看日志
```bash
# 实时查看服务日志
tail -f wework_service.log

# 查看详细日志
tail -f wework_combined.log

# 查看错误日志
grep -i error wework_service.log
```

### 监控指标
- 服务运行状态: `curl http://localhost:8400/health`
- 消息处理统计: `curl http://localhost:8400/stats`
- 数据库大小: `du -h wework_combined.db`

## 故障排除

### 常见问题

#### 1. 服务启动失败
```bash
# 检查端口占用
lsof -ti:8400

# 检查Python依赖
python3 -c "import flask, Crypto, requests"
```

#### 2. 企业微信回调失败
- 检查Token和EncodingAESKey配置
- 检查IP白名单配置
- 检查服务器时间同步

#### 3. Cloudflare Tunnel连接失败
```bash
# 检查隧道状态
cloudflared tunnel info <隧道ID>

# 查看日志
sudo journalctl -u cloudflared -f
```

### 调试模式
```bash
# 启用调试日志
修改 config/wework_config.json 中的 "debug": true

# 重启服务
./scripts/stop_service.sh
./scripts/start_service.sh

# 查看详细日志
tail -f wework_combined.log
```

## 安全建议

### 1. 定期更新
- 每3个月更换Token和EncodingAESKey
- 定期更新Python依赖包
- 保持Cloudflared最新版本

### 2. 访问控制
- 配置企业微信IP白名单
- 使用Cloudflare防火墙规则
- 限制管理接口访问

### 3. 数据保护
- 定期备份数据库
- 加密存储敏感数据
- 设置数据保留策略

### 4. 监控告警
- 监控服务运行状态
- 设置磁盘空间告警
- 监控API调用异常

## 更新日志

### v1.0.0 (2024-03-05)
- 初始版本发布
- 支持企业微信普通回调和会话存档
- 集成线程安全存储系统
- 提供完整Cloudflare Tunnel配置
- 包含一键部署脚本

## 技术支持

### 文档资源
- `references/` 目录下的详细文档
- 企业微信官方文档: https://open.work.weixin.qq.com/api/doc
- Cloudflare Tunnel文档: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/

### 问题反馈
1. 检查日志文件获取错误信息
2. 参考故障排除章节
3. 确保配置正确

### 社区支持
- OpenClaw社区
- 企业微信开发者社区
- Cloudflare社区论坛

## 许可证

MIT License - 详见 LICENSE 文件

## 贡献指南

欢迎提交Issue和Pull Request来改进这个技能。

### 开发规范
1. 遵循Python PEP8编码规范
2. 添加适当的注释和文档
3. 编写单元测试
4. 更新相关文档

### 测试要求
- 测试企业微信回调验证
- 测试消息加解密
- 测试数据库操作
- 测试API接口

---

**注意**: 本技能仅供技术学习和合法用途。使用企业微信服务需遵守相关法律法规和企业微信开发者规范。