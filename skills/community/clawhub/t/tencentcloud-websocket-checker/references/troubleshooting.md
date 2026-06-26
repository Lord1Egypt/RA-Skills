# WebSocket 延迟检测工具 - 故障排查参考

本文件是 `docs/TROUBLESHOOTING.md` 的精简版，供 Skill 快速参考。

## 依赖问题

| 工具 | CentOS 安装 | Ubuntu 安装 | macOS 安装 |
|------|-------------|-------------|------------|
| curl | `yum install -y curl` | `apt install -y curl` | `brew install curl` |
| dig  | `yum install -y bind-utils` | `apt install -y dnsutils` | `brew install bind` |
| awk  | `yum install -y gawk` | `apt install -y gawk` | `brew install gawk` |
| sed  | 系统自带 | 系统自带 | `brew install gnu-sed`（可选）|

## 常见 HTTP 状态码

| 状态码 | 含义 | 建议 |
|--------|------|------|
| 101 | WebSocket Upgrade 成功 | 正常 |
| 200 | 普通 HTTP 响应 | 检查端点路径 |
| 301/302 | 重定向 | 检查 URL，可能需要 HTTPS |
| 400 | 参数错误 | 检查 URL 参数格式 |
| 403 | 拒绝访问 | 检查鉴权/IP白名单 |
| 404 | 端点不存在 | 确认路径正确 |
| 502/503/504 | 服务端异常 | 检查后端服务 |
| 000 | 无响应 | 网络不通或超时 |

## TLS 性能优化建议

1. **升级 TLS 1.3**：减少握手 RTT（1-RTT → 0-RTT）
2. **启用 Session Resumption**：复用之前的会话参数
3. **检查证书链深度**：正常 2-3 层，超过 4 层需优化
4. **启用 OCSP Stapling**：避免客户端额外查询证书状态
5. **使用 CDN 进行 TLS 终结**：就近完成握手

## DNS 优化建议

1. 启用本地 DNS 缓存（nscd / dnsmasq / systemd-resolved）
2. 使用公共 DNS（8.8.8.8 / 119.29.29.29）
3. 应用层缓存 DNS 结果
