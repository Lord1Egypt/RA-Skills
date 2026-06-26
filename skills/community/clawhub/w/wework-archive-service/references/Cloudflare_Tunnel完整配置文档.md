# Cloudflare Tunnel 完整配置文档

## 概述

Cloudflare Tunnel（原 Argo Tunnel）是一种安全的出站连接，允许您在不暴露公共IP地址的情况下将本地服务暴露到互联网。它通过Cloudflare的全球网络提供安全、快速的连接。

## 1. 安装 Cloudflared

### 1.1 macOS 安装
```bash
# 使用 Homebrew 安装
brew install cloudflared

# 验证安装
cloudflared --version
```

### 1.2 Linux 安装
```bash
# Ubuntu/Debian
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb

# CentOS/RHEL
sudo yum install https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-x86_64.rpm

# 通用二进制安装
curl -L --output cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/
```

### 1.3 Windows 安装
```powershell
# 使用 Chocolatey
choco install cloudflared

# 或手动下载
# 从 GitHub Releases 下载 cloudflared-windows-amd64.exe
# 重命名为 cloudflared.exe 并添加到 PATH
```

## 2. 认证 Cloudflared

### 2.1 登录 Cloudflare
```bash
# 启动认证流程
cloudflared tunnel login

# 会打开浏览器，选择要托管的域名
# 授权后会在 ~/.cloudflared/cert.pem 生成证书
```

### 2.2 验证认证
```bash
# 检查证书
ls -la ~/.cloudflared/cert.pem

# 测试连接
cloudflared tunnel list
```

## 3. 创建隧道

### 3.1 创建新隧道
```bash
# 创建隧道
cloudflared tunnel create wework-tunnel

# 输出示例：
# Tunnel credentials written to /Users/username/.cloudflared/<隧道ID>.json
# Please note the tunnel ID: <隧道ID>
```

### 3.2 查看隧道列表
```bash
# 列出所有隧道
cloudflared tunnel list

# 输出示例：
# ID                                   NAME           CREATED              CONNECTIONS
# <隧道ID>                             wework-tunnel  2024-03-05T10:30:00Z 0
```

### 3.3 获取隧道信息
```bash
# 查看隧道详情
cloudflared tunnel info <隧道ID>

# 查看隧道路由
cloudflared tunnel route dns wework-tunnel
```

## 4. 配置隧道

### 4.1 创建配置文件
创建配置文件 `~/.cloudflared/config.yml`：

```yaml
tunnel: <隧道ID>
credentials-file: /Users/你的用户名/.cloudflared/<隧道ID>.json

ingress:
  # 企业微信服务
  - hostname: wework.yourdomain.com
    service: http://localhost:8400
    originRequest:
      connectTimeout: 30s
      noTLSVerify: false
      disableChunkedEncoding: false
      http2Origin: true
      keepAliveConnections: 100
      keepAliveTimeout: 90s
      noHappyEyeballs: false
      tcpKeepAlive: 30s
  
  # 健康检查
  - hostname: status.yourdomain.com
    service: http_status:200
  
  # 默认路由（404）
  - service: http_status:404

# 日志配置
logfile: /var/log/cloudflared.log
loglevel: info

# 性能配置
proxy-dns: false
proxy-dns-port: 53
proxy-dns-upstream:
  - https://1.1.1.1/dns-query
  - https://1.0.0.1/dns-query

# 高可用配置
ha-connections: 4
retries: 3
heartbeat-interval: 5s
```

### 4.2 验证配置
```bash
# 验证配置文件
cloudflared tunnel ingress validate

# 测试配置
cloudflared tunnel ingress rule
```

## 5. DNS 配置

### 5.1 自动配置（推荐）
```bash
# 自动创建DNS记录
cloudflared tunnel route dns wework-tunnel wework.yourdomain.com

# 可以创建多个子域名
cloudflared tunnel route dns wework-tunnel api.yourdomain.com
cloudflared tunnel route dns wework-tunnel status.yourdomain.com
```

### 5.2 手动配置
1. 登录 Cloudflare Dashboard
2. 进入 DNS 管理页面
3. 添加 CNAME 记录：
   - 名称: `wework`
   - 目标: `<隧道ID>.cfargotunnel.com`
   - 代理状态: ✅ 已代理（橙色云）
4. 保存更改

### 5.3 通配符配置
```bash
# 创建通配符记录
cloudflared tunnel route dns wework-tunnel "*.yourdomain.com"

# 或在Cloudflare Dashboard添加：
# 名称: *
# 目标: <隧道ID>.cfargotunnel.com
```

## 6. 启动隧道

### 6.1 测试运行
```bash
# 前台运行（测试用）
cloudflared tunnel run wework-tunnel

# 指定配置文件
cloudflared tunnel --config ~/.cloudflared/config.yml run wework-tunnel
```

### 6.2 作为服务运行
```bash
# 安装服务
cloudflared service install

# 启动服务
sudo systemctl start cloudflared

# 设置开机自启
sudo systemctl enable cloudflared

# 查看服务状态
sudo systemctl status cloudflared

# 查看日志
sudo journalctl -u cloudflared -f
```

### 6.3 macOS 服务
```bash
# 安装启动项
cloudflared service install

# 启动服务
sudo launchctl start com.cloudflare.cloudflared

# 查看状态
sudo launchctl list | grep cloudflare

# 查看日志
sudo log stream --process cloudflared
```

## 7. HTTPS 配置

### 7.1 自动HTTPS
Cloudflare Tunnel 自动提供：
- 自动签发和续期 Let's Encrypt 证书
- 强制HTTPS重定向
- HSTS预加载
- TLS 1.3支持

### 7.2 自定义证书
```yaml
# 在 config.yml 中添加
tls:
  cert: /path/to/cert.pem
  key: /path/to/key.pem
```

### 7.3 SSL/TLS 设置
在 Cloudflare Dashboard 配置：
1. 进入 SSL/TLS 设置
2. 加密模式: 完全（严格）
3. 最低TLS版本: TLS 1.2
4. 启用TLS 1.3
5. 启用自动HTTPS重写

## 8. 安全配置

### 8.1 防火墙规则
在 Cloudflare Dashboard 配置防火墙规则：
1. 进入防火墙 > 防火墙规则
2. 创建规则：
   - 名称: "仅允许企业微信IP"
   - 字段: IP源地址
   - 操作: 阻止
   - 表达式: `not (ip.src in {企业微信IP列表})`
3. 企业微信IP段：
   - 101.226.0.0/15
   - 101.227.0.0/16
   - 112.64.0.0/15
   - 116.128.0.0/16
   - 121.51.0.0/16
   - 183.192.0.0/15

### 8.2 WAF规则
1. 进入安全 > WAF
2. 创建自定义规则：
   - 阻止SQL注入攻击
   - 阻止XSS攻击
   - 限制请求频率

### 8.3 访问策略
```yaml
# 在 config.yml 中添加访问策略
ingress:
  - hostname: wework.yourdomain.com
    service: http://localhost:8400
    originRequest:
      access:
        teamName: your-team
        audTag: ["wework"]
```

## 9. 监控和日志

### 9.1 查看隧道状态
```bash
# 查看连接状态
cloudflared tunnel info <隧道ID>

# 查看实时日志
cloudflared tunnel run wework-tunnel --debug

# 查看连接数
cloudflared tunnel connections list <隧道ID>
```

### 9.2 Cloudflare Analytics
在 Cloudflare Dashboard 查看：
1. **Analytics** > **Traffic**
   - 请求量
   - 带宽使用
   - 国家分布
2. **Security** > **Events**
   - 安全事件
   - 攻击类型
3. **Speed** > **Performance**
   - 加载时间
   - 缓存命中率

### 9.3 日志收集
```bash
# 配置日志轮转
sudo tee /etc/logrotate.d/cloudflared << EOF
/var/log/cloudflared.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
EOF
```

## 10. 故障排除

### 10.1 常见问题

#### 问题1: 隧道连接失败
```bash
# 检查网络连接
ping 1.1.1.1

# 检查DNS解析
nslookup yourdomain.com

# 检查证书
cloudflared tunnel login --force
```

#### 问题2: 服务无法访问
```bash
# 检查本地服务
curl http://localhost:8400/health

# 检查隧道状态
cloudflared tunnel info <隧道ID>

# 检查DNS记录
dig wework.yourdomain.com
```

#### 问题3: HTTPS证书问题
```bash
# 检查证书
openssl s_client -connect wework.yourdomain.com:443 -servername wework.yourdomain.com

# 强制更新证书
cloudflared tunnel route dns --overwrite-dns wework-tunnel wework.yourdomain.com
```

### 10.2 调试命令
```bash
# 详细调试
cloudflared tunnel run wework-tunnel --loglevel debug

# 检查配置
cloudflared tunnel ingress validate --config ~/.cloudflared/config.yml

# 测试连接
cloudflared tunnel test wework.yourdomain.com
```

### 10.3 日志分析
常见日志信息：
- `Connected to edge`: 成功连接到Cloudflare边缘节点
- `Registered tunnel connection`: 隧道注册成功
- `connection error`: 连接错误，检查网络
- `certificate expired`: 证书过期，重新登录

## 11. 性能优化

### 11.1 连接优化
```yaml
# 在 config.yml 中优化
originRequest:
  connectTimeout: 30s
  keepAliveConnections: 100
  keepAliveTimeout: 90s
  tcpKeepAlive: 30s
  http2Origin: true
```

### 11.2 缓存配置
在 Cloudflare Dashboard 配置：
1. 进入缓存 > 配置
2. 设置缓存级别: 标准
3. 浏览器缓存TTL: 4小时
4. 边缘缓存TTL: 2小时

### 11.3 压缩配置
```yaml
# 启用压缩
compression-quality: 5
```

## 12. 高可用配置

### 12.1 多隧道配置
```bash
# 创建多个隧道
cloudflared tunnel create wework-tunnel-1
cloudflared tunnel create wework-tunnel-2

# 配置负载均衡
cloudflared tunnel route lb wework.yourdomain.com wework-tunnel-1 wework-tunnel-2
```

### 12.2 健康检查
```yaml
# 配置健康检查
ingress:
  - hostname: wework.yourdomain.com
    service: http://localhost:8400
    originRequest:
      noTLSVerify: false
      httpHostHeader: wework.yourdomain.com
```

### 12.3 故障转移
```bash
# 配置故障转移
cloudflared tunnel route lb --failure-threshold 3 wework.yourdomain.com wework-tunnel-1 wework-tunnel-2
```

## 13. 备份和恢复

### 13.1 备份配置
```bash
# 备份配置文件
cp ~/.cloudflared/config.yml ~/.cloudflared/config.yml.backup

# 备份证书
cp ~/.cloudflared/cert.pem ~/.cloudflared/cert.pem.backup

# 备份隧道凭证
cp ~/.cloudflared/<隧道ID>.json ~/.cloudflared/<隧道ID>.json.backup
```

### 13.2 恢复配置
```bash
# 恢复配置文件
cp ~/.cloudflared/config.yml.backup ~/.cloudflared/config.yml

# 重新登录（如果需要）
cloudflared tunnel login

# 重启服务
sudo systemctl restart cloudflared
```

## 14. 更新和维护

### 14.1 更新 Cloudflared
```bash
# macOS
brew upgrade cloudflared

# Linux
sudo cloudflared update

# 手动更新
curl -L --output cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/
```

### 14.2 定期维护
- 每月检查证书状态
- 每季度更新Cloudflared
- 每年审查安全配置

## 15. 成本估算

### 15.1 免费套餐
- 隧道数量: 无限
- 连接数: 无限
- 流量: 免费（合理使用）
- 功能: 基础功能

### 15.2 付费套餐
- Zero Trust 套餐: $7/用户/月
- 企业套餐: 定制价格
- 额外功能: 高级安全、分析、支持

## 16. 支持资源

### 16.1 官方文档
- Cloudflare Tunnel 文档: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/
- 社区论坛: https://community.cloudflare.com/
- GitHub: https://github.com/cloudflare/cloudflared

### 16.2 故障排除
- 状态页面: https://www.cloudflarestatus.com/
- 支持渠道: Cloudflare Dashboard 支持
- 企业支持: 付费客户专属支持

---

**最后更新**: 2024-03-05  
**版本**: 1.0.0  
**适用场景**: 企业微信服务公网暴露  
**安全等级**: 生产环境可用