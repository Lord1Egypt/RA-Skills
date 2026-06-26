# Smart Email 自动安装指南

本指南供 OpenClaw 读取并执行自动安装。

## 安装步骤

### 1. 克隆仓库

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/bu-bu-xxx/smart-email.git
cd smart-email
```

### 2. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
# 仅当 ~/.openclaw/.env 不存在时复制配置模板
[ -f ~/.openclaw/.env ] || cp .env.example ~/.openclaw/.env
# 编辑 ~/.openclaw/.env 填写邮箱和 AI API Key
```

### 4. 初始化

```bash
python3 -m smart_email init
```

## 验证安装

```bash
# 测试邮件检查
python3 -m smart_email test-check

# 查看生成的消息
ls /tmp/smart-email-data/outbox/pending/
```

## 完成

安装完成。使用 `python3 -m smart_email --help` 查看所有命令。
