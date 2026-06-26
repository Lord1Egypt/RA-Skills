# WoL Wakeup 技能配置说明

## 安装

### 方法 1：手动安装
```bash
# 复制技能到 OpenClaw 技能目录
cp -r /path/to/wol-wakeup /root/.openclaw/workspace-zhongshu/skills/

# 安装依赖
pip3 install wakeonlan
```

### 方法 2：通过 ClawHub（推荐）
```bash
clawhub install wol-wakeup
```

## 依赖

- Python 3.6+
- `wakeonlan` Python 库

安装依赖：
```bash
pip3 install wakeonlan
```

## 配置

### 设备存储位置
设备信息保存在：`~/.openclaw/wol/devices.json`

### 文件格式
```json
[
  {
    "name": "书房电脑",
    "mac": "00:11:22:33:44:55",
    "note": "书房台式机",
    "id": 1
  }
]
```

## 使用方法

### 1. 列出可唤醒设备
发送消息：
```
帮我开机
```
或
```
列表
```

### 2. 添加设备
发送消息：
```
添加网络唤醒|00:11:22:33:44:55|书房电脑
```
格式：`添加网络唤醒|MAC 地址 | 备注`

### 3. 唤醒设备
发送消息：
```
开机 - 书房电脑
```
或按编号：
```
开机 -1
```

### 4. 删除设备
发送消息：
```
删除 - 书房电脑
```

## 获取 MAC 地址

### Windows
```cmd
ipconfig /all
```
查找"物理地址"

### macOS
```bash
networksetup -listallhardwareports
```
或
```bash
ifconfig | grep ether
```

### Linux
```bash
ip link show
```
或
```bash
ifconfig -a
```

## 启用 WoL 功能

### Windows
1. 设备管理器 → 网络适配器 → 右键属性
2. 电源管理 → 勾选"允许此设备唤醒计算机"
3. 高级 → "Wake on Magic Packet" → 启用

### macOS
1. 系统偏好设置 → 节能
2. 勾选"唤醒以供网络访问"

### Linux
```bash
# 检查 WoL 状态
ethtool eth0 | grep "Wake-on"

# 启用 WoL
ethtool -s eth0 wol g

# 永久启用（systemd）
# 创建 /etc/systemd/system/wol.service
```

## 测试

```bash
# 测试添加
python3 scripts/message_handler.py "添加网络唤醒|00:11:22:33:44:55|测试电脑"

# 测试列表
python3 scripts/message_handler.py "列表"

# 测试唤醒
python3 scripts/message_handler.py "开机 - 测试电脑"

# 测试删除
python3 scripts/message_handler.py "删除 - 测试电脑"
```

## 故障排除

### 问题：唤醒失败
- 确认设备支持 WoL 并已启用
- 确认设备在同一局域网
- 检查防火墙是否阻止 UDP 端口 9

### 问题：命令不识别
- 确认消息格式正确
- 检查关键词是否完全匹配

### 问题：设备列表为空
- 首次使用需先添加设备
- 检查配置文件 `~/.openclaw/wol/devices.json` 是否存在

## 安全注意事项

- WoL 包以明文发送，不建议跨公网使用
- 建议仅在受信任的局域网内使用
- 可配合路由器 MAC 地址过滤增强安全性
