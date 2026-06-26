# 🔊 xiaoai-speaker

> 一句话让小爱音箱说话，远程控制、定时提醒，把智能音箱变成你的私人助理

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 😫 你是不是也遇到过这些烦恼？

- 手机静音错过重要提醒
- 想远程叫家人吃饭但电话没人接
- 老人/孩子总是忘记按时吃药
- 量化交易信号来了，手机推送被淹没

**小爱音箱明明就在家里，为什么不能直接让它喊出来？**

## ✨ 现在可以了！

```bash
# 配置环境变量（只需一次）
export MI_USER="你的小米账号"
export MI_PASS="你的小米密码"

# 一句话，小爱帮你播报
python3 xiaoai_cli.py say "饭做好了，快来吃！"

# 不在家也能远程喊话
python3 xiaoai_cli.py say --device "儿童房" "该写作业了"
```

## 🚀 3 分钟快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/zkfan/xiaoai-speaker.git
cd xiaoai-speaker

# 2. 配置环境变量
export MI_USER="你的小米账号"
export MI_PASS="你的小米密码"
export MI_DEVICE_NAME="客厅"  # 可选

# 添加到 ~/.zshrc 永久生效
echo 'export MI_USER="你的小米账号"' >> ~/.zshrc
echo 'export MI_PASS="你的小米密码"' >> ~/.zshrc
source ~/.zshrc

# 3. 开始使用
python3 xiaoai_cli.py test           # 测试连接
python3 xiaoai_cli.py say "你好小爱"  # 播报消息
```

### 创建快捷命令（推荐）

```bash
# 添加到 ~/.zshrc
echo 'alias xiaoai="python3 ~/xiaoai-speaker/xiaoai_cli.py"' >> ~/.zshrc
source ~/.zshrc

# 然后可以直接使用
xiaoai say "该喝水啦"
xiaoai list
```

## 🎯 核心功能

| 功能 | 命令 | 场景 |
|------|------|------|
| **语音播报** | `xiaoai say "消息"` | 远程喊话、提醒 |
| **多设备** | `xiaoai say -d "客厅"` | 选择特定房间 |
| **定时任务** | 配合 cron | 自动提醒 |
| **设备列表** | `xiaoai list` | 查看可用设备 |

## 💡 实用场景示例

### 🏠 生活提醒
```bash
# 每天8点早安（添加到 crontab）
0 8 * * * export MI_USER="xxx" MI_PASS="xxx" && /usr/bin/python3 /path/to/xiaoai_cli.py say '早上好！'

# 每小时喝水提醒
0 * * * * export MI_USER="xxx" MI_PASS="xxx" && /usr/bin/python3 /path/to/xiaoai_cli.py say '该喝水了'

# 睡觉提醒
0 22 * * * export MI_USER="xxx" MI_PASS="xxx" && /usr/bin/python3 /path/to/xiaoai_cli.py say '早点休息'
```

### 👨‍👩‍👧‍👦 家庭传话
```bash
# 叫全家吃饭
python3 xiaoai_cli.py say "饭做好了，快来吃"

# 提醒孩子写作业
python3 xiaoai_cli.py say --device "儿童房" "该写作业了"

# 提醒老人吃药
python3 xiaoai_cli.py say "该吃药了，记得按时服用"
```

### 💼 工作辅助
```bash
# 会议提醒
python3 xiaoai_cli.py say "10分钟后有会议，请准备"

# 任务完成通知
python3 xiaoai_cli.py say "代码部署完成"
```

## 📖 详细文档

- [SKILL.md](./SKILL.md) - 完整使用指南
- [examples/](./examples/) - 代码示例

## 🔧 配置说明

### 环境变量

| 变量名 | 必需 | 说明 |
|--------|------|------|
| `MI_USER` | ✅ | 小米账号 |
| `MI_PASS` | ✅ | 小米密码 |
| `MI_DEVICE_NAME` | ❌ | 默认设备名称 |

### 查看设备列表

```bash
python3 xiaoai_cli.py list
```

输出示例：
```
🎵 找到 2 个设备：

设备ID                 设备名称             
----------------------------------------------
🔊 bc7e8679-xxxx     客厅的小爱音箱mini    
   a1b2c3d4-xxxx     卧室的小爱音箱        
```

## 🤝 贡献指南

欢迎贡献！你可以：

- 🐛 [提交 Bug](https://github.com/zkfan/xiaoai-speaker/issues)
- 💡 [提出新功能建议](https://github.com/zkfan/xiaoai-speaker/issues)
- 🔧 [提交 Pull Request](https://github.com/zkfan/xiaoai-speaker/pulls)
- ⭐ [给个 Star](https://github.com/zkfan/xiaoai-speaker)

## 📝 相关项目

- [MiService](https://github.com/Yonsm/MiService) - 小米服务 API

## 📄 License

[MIT License](./LICENSE) © 2026 zkfan

---

> 💡 **提示**：如果这个项目帮到了你，请给个 ⭐ Star 支持一下！

> 📧 **问题反馈**：[GitHub Issues](https://github.com/zkfan/xiaoai-speaker/issues)
