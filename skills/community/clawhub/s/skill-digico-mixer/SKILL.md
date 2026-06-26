---
name: skill_digico_mixer
description: DiGiCo调音台OSC协议远程控制系统
priority: P1
version: "1.0"
invocation_mode: both
preferred_provider: minimax
---

# DiGiCo调音台控制技能

## 功能概述

DiGiCo调音台是专业级数字调音台，广泛应用于大型演出、音乐会、剧院、电视直播等场景。本技能通过OSC（Open Sound Control）协议实现远程控制和监控，让技术人员在无法物理接触设备时也能实时调整调音台参数。

### 核心功能
- **场景切换**: 快速加载预设场景配置
- **通道控制**: 调整输入/输出通道的增益、EQ、压缩等参数
- **输出路由**: 管理音频信号的路由和分配
- **状态监控**: 实时监控调音台运行状态
- **快照管理**: 保存和调用场景快照

### 应用场景
1. **演出实时调整**: 演出过程中远程调整调音参数
2. **彩排预设置**: 提前配置场景参数，演出时快速切换
3. **设备巡检**: 定时检查调音台状态和连接性
4. **故障诊断**: 远程诊断调音台异常问题

---

## 使用方法

### 基础调用

```python
from skill_digico_mixer import execute

# 连接调音台
result = execute(
    action="connect",
    ip="192.168.1.100",
    port=12345
)

# 切换场景
result = execute(
    action="load_scene",
    scene_id=5
)

# 调整通道增益
result = execute(
    action="set_channel_gain",
    channel=12,
    gain=-6.0
)
```

### 状态监控

```python
# 获取调音台状态
status = execute(
    action="get_status"
)

# 获取通道列表
channels = execute(
    action="get_channels"
)
```

---

## 参数说明

### 连接参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| ip | str | 192.168.1.100 | DiGiCo调音台IP地址 |
| port | int | 12345 | OSC协议端口（DiGiCo默认端口） |

### 控制参数

| 参数 | 类型 | 范围 | 说明 |
|------|------|------|------|
| scene_id | int | 1-999 | 场景编号 |
| channel | int | 1-128 | 通道编号 |
| gain | float | -∞ to +12dB | 增益值（dB） |
| eq_band | str | low/mid/high | EQ频段 |
| eq_gain | float | -20 to +20 | EQ增益（dB） |

### OSC协议路径

DiGiCo OSC协议标准路径：
- `/digico/scene/load` - 加载场景
- `/digico/channel/{id}/gain` - 通道增益
- `/digico/channel/{id}/eq` - 通道EQ
- `/digico/output/{id}/route` - 输出路由
- `/digico/status` - 状态查询

---

## 示例

### 示例1：演出前预设置

```python
# 连接调音台
execute(action="connect", ip="192.168.1.100")

# 加载演出场景
execute(action="load_scene", scene_id=10)

# 调整主唱通道
execute(
    action="set_channel_gain",
    channel=1,
    gain=-3.0
)

# 添加压缩
execute(
    action="set_channel_compressor",
    channel=1,
    threshold=-20,
    ratio=4.0
)

# 保存快照
execute(action="save_snapshot", name="演出开场")
```

### 示例2：定时设备巡检

```python
# 自动化巡检脚本（适合cron任务）
import schedule

def check_digico_status():
    status = execute(action="get_status")
    if status["cpu_usage"] > 80:
        send_alert("DiGiCo CPU使用率过高")
    if status["network_latency"] > 50:
        send_alert("DiGiCo网络延迟异常")

# 每5分钟执行一次
schedule.every(5).minutes.do(check_digico_status)
```

### 示例3：故障诊断

```python
# 检查调音台连接性
ping_result = execute(action="ping")

if ping_result["status"] == "success":
    # 检查OSC端口
    port_result = execute(action="check_port", port=12345)
    
    # 获取错误日志
    logs = execute(action="get_error_logs", lines=50)
    
    print("诊断结果:", {
        "ping": ping_result,
        "port": port_result,
        "errors": logs
    })
```

---

## 注意事项

1. **网络连接**: 确保调音台和控制端在同一网络，或已配置正确的路由
2. **OSC端口**: DiGiCo默认OSC端口为12345，确保未被防火墙拦截
3. **权限要求**: 需要调音台管理员权限才能执行某些控制操作
4. **调用合规**: 本技能支持人工触发和自动化触发两种方式

---

## 依赖要求

- Python OSC库：`python-osc`
- 网络连接：TCP/IP协议支持
- DiGiCo调音台：OSC协议开放端口

```bash
# 安装依赖
pip install python-osc
```

---

## 技能信息

- **技能名称**: skill_digico_mixer
- **优先级**: P1（核心设备控制）
- **调用模式**: both（人工+自动化）
- **推荐套餐**: MiniMax（适合自动化场景）
- **版本**: 1.0.0