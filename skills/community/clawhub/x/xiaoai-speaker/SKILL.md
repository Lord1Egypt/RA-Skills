---
name: xiaoai-speaker
description: 小爱音箱语音播报。一句话让小爱说话，无需编写代码，支持定时提醒、远程喊话、家庭传话。
version: 1.0.0
author: zkfan
---

# 🔊 xiaoai-speaker

> 一句话控制小爱音箱，把智能音箱变成你的私人助理

```bash
export MI_USER="你的小米账号"
export MI_PASS="你的小米密码"
xiaoai say "饭做好了，快来吃！"
```

## 🚀 3分钟上手

### 1. 安装
```bash
git clone https://github.com/zkfan/xiaoai-speaker.git
cd xiaoai-speaker
```

### 2. 配置（环境变量）
```bash
export MI_USER="你的小米账号"
export MI_PASS="你的小米密码"
export MI_DEVICE_NAME="客厅"  # 可选

# 添加到 ~/.zshrc 永久生效
echo 'export MI_USER="你的小米账号"' >> ~/.zshrc
echo 'export MI_PASS="你的小米密码"' >> ~/.zshrc
source ~/.zshrc
```

### 3. 使用
```bash
# 测试连接
python3 xiaoai_cli.py test

# 基础播报
python3 xiaoai_cli.py say "该喝水啦"

# 指定房间播报
python3 xiaoai_cli.py say --device "儿童房" "该写作业了"

# 查看设备
python3 xiaoai_cli.py list
```

## ✨ 功能特点

| 功能 | 说明 |
|------|------|
| 🎯 **零代码** | 无需 Python，一句话即可使用 |
| 🏠 **多设备** | 支持选择不同房间的小爱音箱 |
| ⏰ **定时任务** | 可配合 cron 使用 |
| 🌐 **远程控制** | 不在家也能让小爱喊话 |
| 🔒 **安全** | 账号信息通过环境变量传入，不存储 |

## 📝 使用指南

### 环境变量配置

```bash
export MI_USER="136xxxxxxxx"      # 小米账号
export MI_PASS="yourpassword"     # 小米密码
export MI_DEVICE_NAME="客厅"       # 默认设备名（可选）
```

### 基础命令

```bash
# 查看帮助
python3 xiaoai_cli.py help

# 查看配置说明
python3 xiaoai_cli.py setup

# 测试连接
python3 xiaoai_cli.py test

# 列出设备
python3 xiaoai_cli.py list

# 简单播报
python3 xiaoai_cli.py say "你好小爱"

# 指定设备播报
python3 xiaoai_cli.py say --device "客厅" "欢迎回家"
```

### 消息技巧

小爱播报速度有限，**建议控制在20字以内**：

✅ **推荐**：
- "该喝水了"
- "饭做好了"
- "10分钟后开会"
- "该起床了"

❌ **避免**：
- 长段落
- 复杂句子  
- 英文混合（发音不准）

## ⏰ 定时任务示例

### 使用系统 cron

```bash
# 编辑 crontab
crontab -e

# 每小时提醒喝水
0 * * * * export MI_USER="xxx" MI_PASS="xxx" && /usr/bin/python3 /path/to/xiaoai-speaker/xiaoai_cli.py say "该喝水了"

# 每天8点早安
0 8 * * * export MI_USER="xxx" MI_PASS="xxx" && /usr/bin/python3 /path/to/xiaoai-speaker/xiaoai_cli.py say "早上好"
```

### 使用 OpenClaw cron（如果支持）

```bash
# 每小时提醒喝水
openclaw cron add \
  --name "喝水提醒" \
  --schedule "0 * * * *" \
  --command "export MI_USER='xxx' MI_PASS='xxx' && python3 /path/to/xiaoai_cli.py say '该喝水了'"
```

## ❓ 常见问题

### 登录失败（错误70016）
```
❌ 登录验证失败
```
**解决步骤**：
1. 确认小米账号密码正确
2. 检查账号是否已绑定小爱音箱
3. 尝试在小米APP中确认新设备登录
4. 如开启二次验证，可能需要临时关闭

### 提示"缺少环境变量"
```bash
# 确保环境变量已设置
export MI_USER="你的小米账号"
export MI_PASS="你的小米密码"

# 验证
python3 xiaoai_cli.py setup
```

### 找不到设备
```bash
# 查看账号下所有设备
python3 xiaoai_cli.py list

# 确认小爱音箱已绑定到该小米账号
```

### 音量太小/太大
当前版本不支持直接调音量，可以通过消息暗示：
```bash
python3 xiaoai_cli.py say "大声提醒：该起床了！"
```

## 🔧 高级用法

### 多设备管理

```bash
# 查看所有设备
python3 xiaoai_cli.py list

# 输出示例：
# 🎵 找到 2 个设备：
# 🔊 bc7e8679-xxxx  客厅的小爱音箱mini
#    a1b2c3d4-xxxx  卧室的小爱音箱

# 指定设备播报（支持模糊匹配）
python3 xiaoai_cli.py say --device "客厅" "消息"
python3 xiaoai_cli.py say --device "卧室" "消息"
```

### 创建快捷命令

```bash
# 添加到 ~/.zshrc
echo 'alias xiaoai="python3 ~/.openclaw/skills/xiaoai-speaker/xiaoai_cli.py"' >> ~/.zshrc
source ~/.zshrc

# 然后可以直接使用
xiaoai say "该喝水啦"
xiaoai list
```

## ⚠️ 安全说明

### 关于 /tmp/MiService
首次运行时会自动从 GitHub 克隆小米官方 SDK：
```bash
git clone https://github.com/Yonsm/MiService.git /tmp/MiService
```
这是小米云服务 API 的必要依赖，**非本项目的安全风险**。

### 隐私保护
- 账号信息通过**环境变量**传入，不存储在文件中
- 不上传到任何第三方服务器
- 使用小米官方云服务 API 通信

## 📋 依赖说明

| 依赖 | 用途 | 安装方式 |
|------|------|----------|
| `aiohttp` | HTTP 客户端 | `pip install aiohttp` |
| `MiService` | 小米云服务 SDK | 运行时自动安装 |

## 🎯 适用场景

- 🏠 **家庭传话** - 不在家时提醒家人吃饭、收快递
- ⏰ **生活提醒** - 喝水、吃药、起床、睡觉
- 💼 **工作辅助** - 会议提醒、定时休息
- 📈 **量化交易** - 开盘收盘提醒、信号播报
- 👶 **孩子管理** - 作业时间、作息提醒

## 📄 开源

- **GitHub**: https://github.com/zkfan/xiaoai-speaker
- **License**: MIT
- **欢迎**: Star ⭐ | PR | Issue

---

<p align="center">
Made with ❤️ by zkfan
</p>
