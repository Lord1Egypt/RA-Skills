# 📦 Cross-Agent Skill 安装说明

## 🚀 快速安装

### 方法一: 直接运行安装脚本
```bash
cd ~/Desktop/skill-cross-agent
./install.sh
```

### 方法二: 手动复制到 OpenClaw skills 目录
```bash
# 创建 skills 目录（如果不存在）
mkdir -p ~/.openclaw/skills

# 复制 skill
cp -r ~/Desktop/skill-cross-agent ~/.openclaw/skills/

# 创建命令链接
ln -sf ~/.openclaw/skills/skill-cross-agent/cross-agent.sh ~/.local/bin/cross-agent
```

### 方法三: 打包分享
```bash
# 打包 skill
cd ~/Desktop
tar czvf skill-cross-agent-v1.0.0.tar.gz skill-cross-agent/

# 其他人解压后安装
tar xzvf skill-cross-agent-v1.0.0.tar.gz
cd skill-cross-agent
./install.sh
```

---

## ⚙️ 安装依赖

```bash
sudo apt update
sudo apt install -y sshpass openssh-client netcat-openbsd iputils-ping
```

---

## 🎯 使用方法

### 安装后直接使用
```bash
# 如果 install.sh 添加了 PATH
~/.openclaw/skills/cross-agent/cross-agent.sh --help

# 或者创建了快捷命令
cross-agent --help
```

### 常用命令
```bash
# 1. 扫描网络
cross-agent scan 192.168.3.0/24

# 2. 交互式向导
cross-agent wizard

# 3. 测试连接
cross-agent test 192.168.3.54 admin 123456

# 4. 发送任务
cross-agent send "请搜索教程"

# 5. 获取文件
cross-agent get ~/Desktop/result.md ~/Desktop/
```

---

## 📁 文件结构

```
skill-cross-agent/
├── SKILL.md              # 技能定义和使用说明
├── cross-agent.sh        # 主入口脚本
├── install.sh            # 安装脚本
├── README.md             # 本文件
└── scripts/
    ├── scan.sh           # 扫描网络
    ├── test.sh           # 测试SSH
    ├── sessions.sh       # 查看会话
    ├── send.sh           # 发送任务
    ├── get.sh            # 获取文件
    ├── put.sh            # 发送文件
    ├── exec.sh           # 执行命令
    ├── config.sh         # 配置管理
    └── wizard.sh         # 交互式向导
```

---

## 🐛 故障排除

### 命令找不到
```bash
# 检查文件是否存在
ls -la ~/.openclaw/skills/cross-agent/

# 检查执行权限
chmod +x ~/.openclaw/skills/cross-agent/*.sh
chmod +x ~/.openclaw/skills/cross-agent/scripts/*.sh
```

### 依赖缺失
```bash
sudo apt install -y sshpass openssh-client netcat-openbsd
```

---

## 📞 支持

- OpenClaw 文档: https://docs.openclaw.ai
- 技能问题: 查看 SKILL.md 中的故障排除部分