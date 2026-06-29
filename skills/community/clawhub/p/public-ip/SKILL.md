---
name: public_ip
description: 读取当前设备的外网 IP 地址和地理位置信息
---

# Public IP Skill

读取当前设备的外网 IP 地址。

## 用法

```
[EXEC:public_ip][/EXEC]
[EXEC:public_ip]{"service":"ipify"}[/EXEC]
```

## 参数

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| service | string | auto | IP 查询服务：ipify/ifconfig.me/myip/auto(自动尝试) |

## 输出内容

- 外网 IPv4 地址
- 外网 IPv6 地址（如可获取）
- 地理位置（国家/地区/城市）
- ISP 信息
- 查询服务

## 备注

- 需要联网
- 多个服务作为备用，自动切换
