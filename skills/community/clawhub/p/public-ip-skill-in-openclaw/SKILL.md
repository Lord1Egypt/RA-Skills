---
name: public_ip
description: 查询当前机器的公网 IP 地址。用于需要确定服务器或客户端在互联网上的公开标识时。
---

# OpenClaw Public IP Query

此 Skill 提供了一种可靠的方法来查询当前机器的公网 IP 地址。它通过调用多个第三方服务（如 ipify, ifconfig.me 等）来确保结果的准确性和可用性。

## 使用场景

- 确认服务器的网络出口 IP。
- 在配置白名单或防火墙规则时获取本机公网 IP。
- 诊断网络连接问题。

## 工作流程

1. **执行查询脚本**：运行 `scripts/get_public_ip.py`。
2. **解析输出**：脚本将返回一个包含 `public_ip` 的 JSON 对象。
3. **展示结果**：向用户报告查询到的公网 IP。



## 核心组件

### `scripts/get_public_ip.py`

这是一个 Python 脚本，它尝试从以下服务获取 IP 地址：
- `api.ipify.org`
- `ifconfig.me`
- `ipapi.co`
- `api.myip.com`

它会自动处理超时和错误，并返回最一致的结果。

### 运行方式

```bash
python3 /home/ubuntu/skills/public_ip/scripts/get_public_ip.py
```

### 预期输出

```json
{
  "public_ip": "1.2.3.4",
  "details": {
    "https://api.ipify.org?format=json": "1.2.3.4",
    ...
  }
}
```

## Resources

### scripts/

- `get_public_ip.py`: 用于查询公网 IP 地址的 Python 脚本。

---
