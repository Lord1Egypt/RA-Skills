# 悟空邀请码监控 (Wukong Invite Monitor)

自动监控钉钉悟空邀请码更新，**零 token 消耗**，支持本地 OCR 识别和心跳推送通知。

## 🚀 60 秒快速开始

```bash
# 1. 进入目录
cd ~/.openclaw/workspace/skills/wukong-invite-monitor/scripts

# 2. 安装依赖（自动检测并安装）
./install-dependencies.sh

# 3. 初始化
python3 monitor_lite.py init

# 4. 测试
python3 monitor_lite.py check

# 5. 设置定时监控（可选）
./setup-cron.sh 5
```

## 📦 依赖说明

运行 `./install-dependencies.sh` 会自动安装：
- ✅ Python 3.6+（通常已预装）
- ✅ Tesseract OCR 4.1+
- ✅ 中文语言包

**手动安装（如果自动安装失败）：**

```bash
# Alibaba Cloud Linux / CentOS
sudo yum install -y tesseract tesseract-langpack-chi_sim

# Ubuntu / Debian
sudo apt install -y tesseract-ocr tesseract-ocr-chi-sim

# macOS
brew install tesseract tesseract-lang
```

## 🎯 使用方法

### 基本命令

```bash
# 初始化（首次使用）
python3 monitor_lite.py init

# 检查一次
python3 monitor_lite.py check

# 查看状态
python3 monitor_lite.py status

# 扫描版本
python3 monitor_lite.py scan
```

### 设置定时监控

```bash
# 每 5 分钟检查
./setup-cron.sh 5

# 查看日志
tail -f /tmp/wukong-monitor.log
```

### 心跳推送通知

配置心跳检查，当发现新邀请码时自动推送通知：

```bash
# 添加心跳检查任务
cat >> /tmp/wukong-cron.txt << 'EOF'
# 心跳检查 - 每 5 分钟检查一次通知（只在官方时间段推送）
*/5 * * * * python3 heartbeat-check.py >> /tmp/wukong-heartbeat.log 2>&1
EOF

crontab /tmp/wukong-cron.txt
```

## 📊 输出示例

```
🎉 发现新邀请码！
━━━━━━━━━━━━━━━━━━━━━━━
📅 时间：2026-03-21 16:20:05
🔢 版本：v18 → v19
📝 内容：大圣闹瑶池
🔍 OCR: Tesseract (tesseract 4.1.1)
📦 大小：77.0 KB
💡 本地 OCR 识别，零 token 消耗！
```

## 💡 资源消耗

- **Token**: 0（完全本地）
- **CPU**: < 1%
- **内存**: < 10MB
- **网络**: ~1KB/次

## ❓ 常见问题

**Q: 必须安装 Tesseract 吗？**

A: 不是必须。不安装时：
- ✅ 版本检测正常
- ✅ 图片下载正常
- ⚠️ OCR 降级为简单分析

**Q: 如何停止监控？**

```bash
crontab -e  # 删除包含 wukong 的行
```

**Q: 心跳推送如何工作？**

A: 心跳检查脚本会：
1. 每 5 分钟检查通知文件
2. 只在官方更新时间段工作（9-12 点、14-18 点）
3. 发现新内容时推送通知
4. 避免重复通知

## 📖 更多文档

- [QUICKSTART.md](QUICKSTART.md) - 60 秒上手
- [LOCAL-OCR.md](LOCAL-OCR.md) - OCR 配置
- [HEARTBEAT.md](HEARTBEAT.md) - 心跳推送配置

---

**许可证**: MIT
