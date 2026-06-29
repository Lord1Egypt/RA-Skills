---
name: system_stats
description: 读取当前系统内存、CPU 占用率、网络吞吐率等实时性能指标
---

# System Stats Skill

读取当前系统的内存、CPU 占用率、网络吞吐率等实时性能指标。

## 用法

```
[EXEC:system_stats][/EXEC]
[EXEC:system_stats]{"interval":2}[/EXEC]
```

## 参数

| 字段 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| interval | int | 1 | CPU 占用率采样间隔（秒），间隔越大越准确 |

## 输出内容

- CPU 占用率（%）
- 内存使用情况（总量/已用/可用/使用率）
- 交换分区使用情况
- 网络吞吐率（每秒收发字节数）
- 磁盘 I/O 速率（如可获取）
- 系统负载（Linux）
- 进程数

## 平台支持

- Windows: 通过 psutil 获取
- Linux: 通过 psutil 获取
- macOS: 通过 psutil 获取

## 依赖

需要安装 psutil：`pip install psutil`
