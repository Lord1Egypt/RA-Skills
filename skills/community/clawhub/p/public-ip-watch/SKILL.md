---
name: public-ip-watch
description: 获取本机公网 IP，或检测 IP 是否发生变化（对比缓存），如有变更则通知用户。适用于定时任务或手动执行。
agent_created: true
author: XP
---

# public-ip-watch

检测本机公网 IP 并与缓存对比，报告变更状态，更新缓存。

## 触发场景

- 用户说"看看我的公网 IP 是多少"
- 用户说"检查一下我的公网 IP 变了没有"
- 自动化定时任务中定期执行（如每天一次）
- 用户提到"网络断了又好了"等需要确认 IP 是否变更的场景

## 执行步骤

### 1. 获取当前公网 IP

按优先级尝试以下服务：

```bash
CURRENT_IP=$(curl -s --max-time 10 https://ip.sb)
```

如果上述请求失败（返回空或非 IP 格式），备选：

```bash
CURRENT_IP=$(curl -s --max-time 10 https://ipinfo.io/ip | xargs)
```

从结果中提取 IP 地址（去除多余的空白字符）。

### 2. 读取缓存文件

缓存文件路径：`~/.public_ip_cache.json`

如果文件不存在，视为首次检测，直接跳到步骤 4。

```bash
CACHED_JSON=$(cat ~/.public_ip_cache.json 2>/dev/null || echo '{}')
```

JSON 格式示例：

```json
{
  "ip": "153.99.16.209",
  "timestamp": "2026-06-30T09:46:00+08:00"
}
```

### 3. 对比 IP

- **IP 未变化**：向用户报告 `IP 未变化，当前 IP 为 xxx`
- **IP 已变更**：向用户报告 `⚠️ IP 已变更！从 xxx 变更为 xxx`，确保用户能注意到

若无缓存（首次检测），报告：`首次检测，当前公网 IP 为 xxx`

### 4. 更新缓存

写入当前 IP 和当前 ISO 8601 时间戳到 `~/.public_ip_cache.json`。

### 5. 返回结果

向用户输出检测结论。如果是变更事件，在结论末尾加上建议："如需重新配置依赖该 IP 的服务（如域名解析、防火墙白名单），请及时处理。"
