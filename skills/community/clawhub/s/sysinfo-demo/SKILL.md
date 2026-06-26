---
name: sysinfo
description: "用 df / uname / uptime 报告本机的磁盘占用、内存、运行时间和系统信息。"
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🖥️",
        "os": ["darwin", "linux"],
        "requires": { "bins": ["df", "uname", "uptime"] }
      }
  }
---

# sysinfo

当用户询问本机的磁盘空间、内存、运行时长、内核 / 操作系统版本，或者「这台机器现在状态怎么样」时，
通过 `exec` 工具运行对应命令，并用一两句话汇报结果。

## 命令对照

- 各挂载卷的磁盘占用：  `df -h`
- 内核和系统版本：       `uname -a`
- 运行时长与负载：       `uptime`

## 规则

- 总是先把原始命令打出来，再附一句简短总结，不要花哨格式化；
- 不要编造数字——命令失败就老实说；
- 拒绝任何需要 sudo 或会写入文件系统的请求。
