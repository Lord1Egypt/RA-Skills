# 客户端配置模板（Clash Verge Rev）

此配置同时适用于 Mac 和 Windows 的 Clash Verge Rev。

## 完整 YAML 模板

将 `<占位符>` 替换为 `.proxy-keys.txt` 中的实际值。

```yaml
# ============================================================
# Clash Verge Rev 导入步骤：
# 1. 打开 Clash Verge → 订阅 → 右上角"新建" → 选 Local
# 2. 填写名称（如：我的节点），点编辑图标
# 3. 粘贴本文件全部内容，Ctrl+S / Cmd+S 保存
# 4. 订阅页面右键刚创建的配置 → 启用
# 5. 代理页面：在 PROXY 组里选中节点名
# 6. 主界面：打开"系统代理"开关
# 注意：修改配置后需完全退出 Clash Verge 再重新打开
# ============================================================

mixed-port: 7890
allow-lan: false
mode: rule
log-level: info
ipv6: false

dns:
  enable: true
  ipv6: false
  enhanced-mode: fake-ip
  fake-ip-range: 198.18.0.1/16
  nameserver:
    - 223.5.5.5
    - 119.29.29.29
  fallback:
    - https://1.1.1.1/dns-query
    - https://dns.google/dns-query
  fallback-filter:
    geoip: true
    geoip-code: CN

proxies:
  - name: "我的Reality节点"
    type: vless
    server: <VPS_IP>
    port: 443
    uuid: <UUID>
    network: tcp
    udp: false
    tls: true
    flow: xtls-rprx-vision
    servername: <SNI_DOMAIN>
    reality-opts:
      public-key: <PUBLIC_KEY>
      short-id: <SHORT_ID>
    client-fingerprint: chrome

proxy-groups:
  - name: "PROXY"
    type: select
    proxies:
      - "我的Reality节点"
      - DIRECT

rules:
  # 关键：VPS 自身 IP 直连，防止死循环
  - IP-CIDR,<VPS_IP>/32,DIRECT,no-resolve
  # 本地地址直连
  - IP-CIDR,127.0.0.0/8,DIRECT,no-resolve
  - IP-CIDR,192.168.0.0/16,DIRECT,no-resolve
  - IP-CIDR,10.0.0.0/8,DIRECT,no-resolve
  # 国内直连
  - GEOIP,CN,DIRECT
  - DOMAIN-SUFFIX,cn,DIRECT
  # 其余走代理
  - MATCH,PROXY
```

## 关键字段说明

| 字段 | 来源 | 说明 |
|---|---|---|
| `server` | `proxy-setup-info.txt` 的 VPS_IP | VPS 公网 IP |
| `uuid` | VPS 生成，保存在 `.proxy-keys.txt` | 服务端客户端共用 |
| `public-key` | VPS 生成的 PublicKey | **不是** PrivateKey！|
| `short-id` | VPS 生成，保存在 `.proxy-keys.txt` | 服务端客户端共用 |
| `servername` | `proxy-setup-info.txt` 的 SNI_DOMAIN | 和服务端 server_name 一致 |
| `udp: false` | 固定值 | 关闭 UDP，避免 QUIC 兼容问题 |
| `client-fingerprint` | 固定 chrome | 浏览器 TLS 指纹模拟 |

## 常见错误

- ❌ 把 PrivateKey 填到 `public-key` 字段 → 连接必然失败
- ❌ 没加 `IP-CIDR,{VPS_IP}/32,DIRECT` → 系统代理开启后 SSH 也无法连接 VPS，形成死循环
- ❌ 修改配置后只切换配置不重启 Clash → 旧配置缓存生效
- ❌ Windows 用 PowerShell 的 `curl`（实为 `Invoke-WebRequest`）测试 → 应用 `curl.exe`
