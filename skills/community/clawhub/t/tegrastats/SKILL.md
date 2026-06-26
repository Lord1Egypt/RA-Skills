# tegrastats

NVIDIA Jetson GPU/内存/温度实时监控工具。

## 功能

- 实时 GPU 状态监控
- 内存使用情况
- CPU 温度监控
- 频率信息

## 命令

```bash
# 一次性输出
tegrastats

# 持续监控 (1秒间隔)
tegrastats --interval 1000

# 停止监控
tegrastats --stop
```

## 依赖

- tegrastats (系统自带)
