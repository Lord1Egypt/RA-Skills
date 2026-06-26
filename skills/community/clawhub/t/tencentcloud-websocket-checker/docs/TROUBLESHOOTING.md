# 故障排查指南

## 目录

1. [依赖问题](#1-依赖问题)
2. [连接失败](#2-连接失败)
3. [结果异常](#3-结果异常)
4. [协议相关](#4-协议相关)
5. [环境兼容性](#5-环境兼容性)
6. [常见错误码](#6-常见错误码)

---

## 1. 依赖问题

### ❌ 错误：缺少依赖工具 dig

**现象**：
```
错误：缺少以下依赖工具：dig
```

**解决方案**：
```bash
# CentOS / RHEL
sudo yum install -y bind-utils

# Ubuntu / Debian
sudo apt install -y dnsutils

# macOS
brew install bind
```

### ❌ 错误：curl 不支持 HTTPS

**现象**：curl 连接 wss 地址时报错 `Protocol "https" not supported`

**解决方案**：
```bash
# 检查 curl 是否编译了 SSL 支持
curl --version | grep -i ssl

# 如果缺少 SSL 支持，重新安装 curl
# CentOS
sudo yum reinstall -y curl libcurl

# Ubuntu
sudo apt install -y curl libcurl4-openssl-dev
```

### ❌ 错误：bash 版本过低

**现象**：脚本运行报语法错误

**检查方式**：
```bash
bash --version
# 需要 bash 4.0 以上
```

**解决方案**：
```bash
# CentOS 7 升级 bash
sudo yum install -y bash

# macOS（自带 bash 3.x，建议升级）
brew install bash
```

---

## 2. 连接失败

### ❌ 所有测试轮次均失败

**可能原因及排查**：

**原因 1：DNS 解析失败**
```bash
# 检查 DNS 解析
dig your-domain.com
nslookup your-domain.com

# 尝试使用公共 DNS
dig @8.8.8.8 your-domain.com
```

**原因 2：端口不通**
```bash
# 检查端口连通性
telnet your-domain.com 443
nc -zv your-domain.com 443

# 如果不通，检查防火墙规则
sudo iptables -L -n | grep 443
```

**原因 3：代理拦截**
```bash
# 检查是否设置了代理
echo $http_proxy
echo $https_proxy
echo $no_proxy

# 临时取消代理测试
unset http_proxy https_proxy
./ws_check.sh wss://your-server.com/ws
```

**原因 4：SSL 证书问题**
```bash
# 验证 SSL 证书
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# 如果证书有问题，可临时使用 curl -k（不推荐生产使用）
curl -k -I https://your-domain.com/
```

---

## 3. 结果异常

### ⚠️ TLS 握手时间异常偏长（> 500ms）

**可能原因**：

1. **证书链过长**
   ```bash
   # 检查证书链深度
   openssl s_client -connect domain:443 2>/dev/null | grep -c "^[[:space:]]*[0-9]"
   # 正常应为 2-3 层，超过 4 层可能需要优化
   ```

2. **未启用 OCSP Stapling**
   ```bash
   openssl s_client -connect domain:443 -status 2>/dev/null | grep -A 2 "OCSP"
   ```

3. **使用了 TLS 1.2 而非 TLS 1.3**
   ```bash
   # 检查 TLS 版本
   openssl s_client -connect domain:443 2>/dev/null | grep "Protocol"
   # 如果是 TLSv1.2，建议升级到 TLS 1.3 以减少握手 RTT
   ```

### ⚠️ DNS 解析时间异常偏长（> 100ms）

**排查步骤**：
```bash
# 1. 检查本地 DNS 服务器响应时间
dig your-domain.com | grep "Query time"

# 2. 对比公共 DNS
dig @8.8.8.8 your-domain.com | grep "Query time"
dig @119.29.29.29 your-domain.com | grep "Query time"

# 3. 检查是否启用了 DNS 缓存
systemctl status nscd 2>/dev/null || echo "nscd 未安装"
systemctl status systemd-resolved 2>/dev/null || echo "systemd-resolved 未运行"
```

### ⚠️ 某些轮次耗时波动很大

**说明**：这通常是正常的网络波动，建议：

- 增加测试轮数到 5-10 轮，获取更稳定的平均值
- 关注「最小值」作为网络基线参考
- 如果波动超过 2 倍，可能存在网络拥塞或负载均衡跳转

---

## 4. 协议相关

### ❌ 错误：无法确定协议类型

**现象**：
```
错误：无法确定协议类型！
```

**解决方案**：URL 必须包含 `ws://` 或 `wss://` 前缀，或者使用 `-p` 参数指定：
```bash
# 方式 1：加上协议前缀
./ws_check.sh wss://example.com/ws

# 方式 2：用 -p 参数
./ws_check.sh -p wss example.com/ws
```

### ⚠️ 使用 ws 协议时收到 301/302 重定向

**说明**：服务端可能强制 HTTPS，将 ws 请求重定向到 wss

**解决方案**：
```bash
# 改用 wss 协议
./ws_check.sh wss://example.com/ws

# 或检查重定向目标
curl -v -I http://example.com/ws 2>&1 | grep -i "location"
```

---

## 5. 环境兼容性

### macOS 注意事项

1. **sed 行为差异**：macOS 使用 BSD sed，某些正则表达式行为不同
   - 脚本已做兼容处理，如遇问题可安装 GNU sed：`brew install gnu-sed`

2. **bash 版本**：macOS 默认 bash 3.x
   - 脚本兼容 bash 4.2 以下版本，一般无需升级

3. **dig 工具**：macOS 自带 dig，无需额外安装

### Docker 容器中使用

```bash
# Alpine Linux
apk add curl bind-tools bash gawk sed

# Debian/Ubuntu 镜像
apt update && apt install -y curl dnsutils gawk sed
```

### 无 root 权限环境

如果没有 root 权限无法安装依赖，可检查系统是否已有替代工具：
```bash
# 检查 dig 的替代品
which nslookup  # 部分系统可能有 nslookup 但没有 dig
which host       # 另一个 DNS 查询工具
```

---

## 6. 常见错误码

| HTTP 状态码 | 含义 | 建议 |
|------------|------|------|
| **101** | ✅ WebSocket Upgrade 成功 | 正常 |
| **200** | 服务端返回普通 HTTP 响应 | 检查 WebSocket 端点路径是否正确 |
| **301/302** | 发生重定向 | 检查 URL 是否正确，是否需要 HTTPS |
| **400** | 请求参数错误 | 检查 URL 参数格式 |
| **403** | 访问被拒绝 | 检查鉴权信息、IP 白名单 |
| **404** | 端点不存在 | 确认 WebSocket 路径是否正确 |
| **502/503/504** | 服务端异常 | 检查后端服务状态 |
| **000** | 未收到响应 | 网络不通或连接被重置 |

---

## 快速诊断流程

```
连接失败？
├─ DNS 解析失败 → dig domain 检查 DNS
├─ TCP 不通 → telnet domain port 检查端口
├─ TLS 失败 → openssl s_client 检查证书
└─ WS 升级失败 → 检查 HTTP 状态码和请求路径

耗时偏长？
├─ DNS 偏慢 → 配置 DNS 缓存 / 换公共 DNS
├─ TCP 偏慢 → traceroute 检查网络路径
├─ TLS 偏慢 → 升级 TLS 1.3 / 启用 Session Resumption
└─ WS 偏慢 → 检查服务端处理逻辑和中间代理
```
