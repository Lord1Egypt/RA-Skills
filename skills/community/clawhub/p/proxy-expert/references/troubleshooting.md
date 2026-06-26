# 故障排查速查表

排查原则：**从近到远，逐层确认**。先看客户端，再看网络，再看服务端。

## 快速定位流程

```
翻墙不通
 ├── Clash 系统代理开着吗？→ 没开 → 开启
 ├── 节点选中了吗？→ 没选 → 代理页面选中
 ├── 443 端口可达？→ 不通 → 看服务端
 │    └── SSH 到 VPS → systemctl status sing-box
 │         ├── active → 看日志有无 ERROR
 │         └── failed → systemctl restart sing-box，再看日志
 └── 端口通但翻不了 → 看 Clash 日志 → DNS 问题？规则问题？
```

## 分状况排查

### 状况 1：全部不通（连国内网也慢或也断）
说明不是代理问题，是本地网络。关掉 Clash 系统代理，直接测本地网速。

### 状况 2：国内正常，翻墙不通

**步骤 1：确认端口可达**

Mac/Linux：
```bash
nc -z -w 5 {VPS_IP} 443 && echo "端口通" || echo "端口不通"
```

Windows（PowerShell）：
```powershell
Test-NetConnection -ComputerName {VPS_IP} -Port 443
# TcpTestSucceeded : True = 通
```

**步骤 2：端口不通 → SSH 看服务状态**
```bash
ssh -i ~/.ssh/proxy_expert_ed25519 -p {SSH_PORT} {SSH_USER}@{VPS_IP} "systemctl status sing-box --no-pager"
```

常见原因：
- sing-box 挂了 → `systemctl restart sing-box`
- 配置文件格式错误 → `sing-box check -c /etc/sing-box/config.json`
- 端口被防火墙屏蔽 → `iptables -L INPUT -n | grep 443`

**步骤 3：验证 Reality 伪装**

Mac/Linux（关闭系统代理后执行）：
```bash
curl -sI --resolve "www.apple.com:443:{VPS_IP}" https://www.apple.com/ -k | head -5
```

Windows：
```powershell
curl.exe -sI --resolve "www.apple.com:443:{VPS_IP}" https://www.apple.com/ -k
```

期望：`HTTP/2 200` + `server: Apple`
如果超时：Reality 没跑起来，检查 sing-box 服务和配置文件中的 private_key。

**步骤 4：看 sing-box 日志**
```bash
ssh ... "tail -50 /var/log/sing-box/sing-box.log"
```

正常日志：
- `REALITY: processed invalid connection` = GFW 在探测，被正确拦截，属正常
- `client connected from x.x.x.x` = 你的设备连上了

错误日志：
- `bind: address already in use` → 端口被占用，改端口或杀占用进程
- `invalid private key` → PrivateKey 填错了（可能填了 PublicKey）
- 日志文件为空 → sing-box 没启动成功

### 状况 3：速度慢

排查顺序：
```
1. 测 VPS 本地带宽（排除 VPS 本身限速）
   ssh ... "curl -o /dev/null -w '%{speed_download}' https://speed.cloudflare.com/__down?bytes=10000000"
   （结果单位是字节/秒，除以 1024/1024 换算 MB/s）

2. 测上游速度（如果有上游）
   ssh ... "curl -x socks5://USER:PASS@UPSTREAM_IP:PORT -o /dev/null -w '%{speed_download}' https://speed.cloudflare.com/__down?bytes=10000000"

3. 测整体：浏览器访问 https://www.fast.com（不要用 Cloudflare speedtest，UDP 会误报丢包）
```

慢的根因排序：
1. 上游 SOCKS5 限速（最常见）→ 换上游，或改用方案 A/C
2. VPS 套餐带宽不足 → 升级套餐
3. 晚高峰国际出口拥塞 → 等到非高峰时段，或换 CN2 GIA 线路
4. ISP 对境外大流量 QoS → 换运营商网络或换时段

### 状况 4：能翻墙但 AI 服务（Claude/GPT）被风控

不是网络问题，是 IP 信誉问题：
1. 查出口 IP：`https://ipinfo.io/ip`
2. 查 IP 信誉：`https://ipinfo.io`（看 ASN，数据中心 IP 容易被风控）
3. 解决方案：
   - 启用上游 SOCKS5，切换到方案 C（AI 站走纯净 IP）
   - 更换住宅 IP 上游服务商

### 状况 4b：ChatGPT 打不开但 Claude/Gemini 正常（ERR_CONNECTION_CLOSED）

**症状**：切换 IP（如切到备用 IP 再切回主 IP）后，只有 `chatgpt.com` 打不开，提示：

```
chatgpt.com 意外终止了连接。
ERR_CONNECTION_CLOSED
```

但 Claude、Gemini 及其他网站都正常。这不是节点被封，而是 Chrome 缓存了旧连接的 TLS/HSTS/socket 状态，与新 IP 发生冲突。

**最快恢复：彻底清理 Chrome 网络状态**

1. **关闭 Chrome QUIC**

   在出问题的 Chrome 地址栏打开：
   ```
   chrome://flags/#enable-quic
   ```
   把 `Experimental QUIC protocol` 改成 `Disabled`。

2. **清除 Chrome DNS 缓存**

   打开：
   ```
   chrome://net-internals/#dns
   ```
   点击 `Clear host cache`。

3. **清除 Chrome socket 连接池**

   打开：
   ```
   chrome://net-internals/#sockets
   ```
   依次点击：
   - `Close idle sockets`
   - `Flush socket pools`

4. **删除 chatgpt.com 的 HSTS 状态**

   打开：
   ```
   chrome://net-internals/#hsts
   ```
   在 `Delete domain security policies` 下输入以下域名，逐个点击 `Delete`：
   ```
   chatgpt.com
   openai.com
   auth.openai.com
   chat.openai.com
   oaistatic.com
   oaiusercontent.com
   ```

5. **完全退出 Chrome**

   不要只关窗口，要彻底退出（`Cmd + Q`），或在终端执行：
   ```bash
   pkill -x "Google Chrome"
   ```
   然后重新打开 Chrome 访问 `https://chatgpt.com`。

**第二层：清系统 DNS 缓存**

如果上述步骤无效，在终端执行：

Mac：
```bash
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
```

Windows（管理员 PowerShell）：
```powershell
ipconfig /flushdns
```

然后重启 Clash Verge（完全退出再重新打开），确认 TUN 已开启、当前节点仍是主 IP 的 Reality 节点。

**额外场景**：刚装好梯子登录 GPT/Claude 时提示"当前区域不在可访问范围"，也可以尝试以上步骤并清空 Cookie。

---

### 状况 5：Reality 真的被封（极少见，但有应对）

症状：`nc` 测端口不通，但 `ping` VPS 通（ICMP 没封，TCP 443 被封）。

应对：
1. 临时：改 sing-box 监听端口到 8443
   ```bash
   ssh ... "sed -i 's/\"listen_port\": 443/\"listen_port\": 8443/' /etc/sing-box/config.json && systemctl restart sing-box"
   ```
   同步修改 Clash Verge YAML 的 `port: 8443`。

2. 中期：更换 SNI 伪装域名（把 `server_name` 改为 `www.microsoft.com`）

3. 长期：联系 VPS 服务商更换 IP

## 常见误解和坑

| 现象 | 误解 | 真相 |
|---|---|---|
| Cloudflare speedtest 显示 60% 丢包 | 网络真的丢包 | UDP 测丢包，Clash 关了 UDP，用 fast.com 测 |
| Reality 日志里有大量 invalid connection | 服务异常 | GFW 主动探测被拦截，越多越说明伪装有效 |
| 切换 IP 后只有 ChatGPT 打不开 | 节点被封了 | Chrome 缓存了旧连接的 TLS/HSTS/socket 状态，按状况 4b 清理即可 |
| tar 提示 "Removing leading /" | 备份出错 | 正常行为，tar 把绝对路径转相对路径 |
| PowerShell 里 curl 报错 | curl 不可用 | 要用 curl.exe（加.exe）才是真正的 curl |
| fail2ban status 报 socket 错误 | 服务异常 | 服务刚启动还没就绪，等 2-3 秒再查 |
