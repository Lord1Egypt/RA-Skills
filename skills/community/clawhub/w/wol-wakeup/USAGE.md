# WoL Wakeup 技能 - 使用说明

## 📦 技能位置
```
/root/.openclaw/workspace-zhongshu/skills/wol-wakeup/
```

## 🚀 快速开始

### 1. 安装依赖
```bash
pip3 install wakeonlan
```

### 2. 添加第一个设备
发送微信消息：
```
添加网络唤醒|00:11:22:33:44:55|我的电脑
```

### 3. 查看设备列表
```
帮我开机
```

### 4. 唤醒设备
```
开机 - 我的电脑
```

## 📝 支持命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `帮我开机` / `开机` / `列表` | 列出所有设备 | `帮我开机` |
| `开机 - 设备名` | 唤醒指定设备 | `开机 - 我的电脑` |
| `开机 - 编号` | 按编号唤醒 | `开机 -1` |
| `添加网络唤醒\|MAC\|备注` | 添加新设备 | `添加网络唤醒\|00:11:22:33:44:55\|书房电脑` |
| `删除 - 设备名` | 删除设备 | `删除 - 我的电脑` |

## 🔧 技术细节

### 核心文件
- `wol_manager.py` - WoL 设备管理核心库
- `message_handler.py` - 微信消息关键词匹配处理器
- `devices.json` - 设备配置文件（自动创建在 `~/.openclaw/wol/`）

### 关键词匹配规则
- 完全匹配，不依赖大模型
- 支持正则表达式解析参数
- 响应时间 < 100ms

### WoL 实现
- 使用 Python `wakeonlan` 库
- 发送 UDP 魔术包到端口 9
- 支持广播地址唤醒

## ✅ 测试结果
```
测试：列出设备（空）✅
测试：添加设备 ✅
测试：列表设备 ✅
测试：唤醒设备 ✅
测试：删除设备 ✅
测试：验证删除 ✅

结果：6/6 通过
```

## 📋 获取 MAC 地址

### Windows
```cmd
ipconfig /all
```

### macOS
```bash
networksetup -listallhardwareports
```

### Linux
```bash
ip link show
```

## ⚠️ 注意事项

1. 目标设备必须支持并启用 WoL
2. 设备需在同一局域网
3. 首次使用需先添加设备
4. MAC 地址格式：`XX:XX:XX:XX:XX:XX`

## 📂 文件结构
```
wol-wakeup/
├── SKILL.md           # 技能元数据和说明
├── README.md          # 详细使用文档
├── _meta.json         # ClawHub 元数据
└── scripts/
    ├── wol_manager.py      # WoL 核心库
    ├── message_handler.py  # 消息处理器
    ├── test_wol.py         # 测试脚本
    └── install.py          # 安装脚本
```

## 🔐 安全提示
- WoL 包以明文发送，仅限可信局域网使用
- 建议配合路由器 MAC 地址过滤
- 不建议跨公网使用
