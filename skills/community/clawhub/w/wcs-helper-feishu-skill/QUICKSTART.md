# 🚀 Python 版本快速启动指南

## 安装 Python 环境

### Windows

1. 下载 Python 3.10+： https://www.python.org/downloads/
2. 安装时勾选 "Add Python to PATH"
3. 验证安装：
   ```cmd
   python --version
   # 应输出 Python 3.10.x 或更高版本
   ```

### macOS

```bash
# 使用 Homebrew 安装
brew install python@3.12

# 验证
python3 --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip

# 验证
python3 --version
```

## 安装飞书配置助手

### 方式一：通过 ClawHub 安装（推荐）

```bash
openclaw skills install guanqi-feishu-config
```

### 方式二：本地安装（开发/测试）

```bash
# 1. 克隆项目
git clone https://github.com/guanqi/guanqi-feishu-config-skill.git
cd guanqi-feishu-config-skill

# 2. 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 安装依赖（使用国内镜像加速）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 4. 安装到 OpenClaw
openclaw skill install ./
```

## 首次配置

### 1. 验证安装

安装完成后，在任意飞书对话中输入：

```
/feishu help
```

如果看到帮助信息，说明安装成功！

### 2. 查看当前配置

```
/feishu status
```

### 3. 打开配置菜单

```
/config
```

## 常用配置场景

### 场景 1：开启流式输出（推荐）

让 AI 回复时逐字显示，体验更流畅：

1. 输入 `/config`
2. 选择 "💬 回复体验"
3. 选择 "开启流式输出"
4. 点击 "🔄 立即重启"

### 场景 2：设置仅@回复（大群推荐）

对于超过 50 人的群组，建议只让机器人在被@时回复：

1. 输入 `/config`
2. 选择 "👥 群聊模式"
3. 选择 "仅@机器人回复"
4. 重启服务

### 场景 3：开启全部消息回复（小群）

**注意：** 需要先申请飞书权限 `im:message.group_msg`

1. 访问 [飞书开放平台](https://open.feishu.cn/app) → 你的应用 → 权限管理
2. 添加权限 `im:message.group_msg`
3. 重新发布应用
4. 等待权限审批通过
5. 输入 `/config`
6. 选择 "👥 群聊模式"
7. 选择 "全部消息回复"
8. 确认警告提示
9. 重启服务

## Python 环境常见问题

### ❓ pip 安装速度慢？

**解决：** 使用国内镜像源

```bash
# 临时使用
pip install <package> -i https://pypi.tuna.tsinghua.edu.cn/simple

# 永久设置
cd ~
mkdir -p .pip
cat > .pip/pip.conf << EOF
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
EOF
```

### ❓ 提示 "No module named 'openclaw'"？

**解决：**
```bash
# 确认在虚拟环境中
which python  # 应显示 venv 路径

# 重新安装依赖
pip install openclaw>=2026.2.0
```

### ❓ Python 版本不兼容？

**解决：** 本项目需要 Python >= 3.10

```bash
# 检查版本
python --version

# 如果低于 3.10，请升级 Python
```

## 下一步

- 📖 查看完整文档：[README.md](README.md)
- 🔧 查看使用示例：[examples/usage.md](examples/usage.md)
- 🐛 遇到问题？提交 Issue

## 命令速查表

| 命令 | 功能 |
|------|------|
| `/config` | 打开配置菜单 |
| `/feishu status` | 查看当前配置状态 |
| `/feishu doctor` | 运行诊断检查 |
| `/feishu help` | 显示帮助信息 |

---

**提示：** Python 版本不需要编译，修改代码后重启 OpenClaw 即可生效！
