# Token Optimizer 安装指南

## 快速安装

### 方法1：从 ClawHub 安装（推荐）

```bash
claw install token-optimizer
```

### 方法2：手动安装

```bash
# 1. 克隆到 skills 目录
cd ~/.openclaw/workspace/skills
git clone https://github.com/thanksandyou/token-optimizer.git

# 2. 安装依赖
pip install -r token-optimizer/requirements.txt

# 3. 初始化记忆目录
python3 token-optimizer/scripts/new_session.py init
```

**重要：** 记忆文件存储在 `~/.openclaw/memory/`（OpenClaw全局记忆目录），不在技能目录内。

## 配置

**无需额外配置！** 🎉

Token Optimizer 会自动使用 OpenClaw 的 AI 配置。

### 验证安装

```bash
cd ~/.openclaw/workspace/skills/token-optimizer

# 运行测试
python3 -m pytest tests/ -v

# 查看状态
python3 scripts/status.py

# 查看记忆目录
ls -la ~/.openclaw/memory/
```

## 使用示例

### 1. 检查会话健康度

```bash
python3 scripts/session_guard.py check --message "用户消息" --context-size 50000
```

### 2. 预览压缩效果

```bash
python3 scripts/compress_session.py --dry-run
```

### 3. 实际压缩

```bash
python3 scripts/compress_session.py
```

### 4. 查看状态

```bash
python3 scripts/status.py
```

## 故障排查

### 问题1：找不到 openai 模块

```bash
pip install openai
```

### 问题2：未找到 AI 配置

确保 OpenClaw 已正确配置：

```bash
cat ~/.openclaw/config.json
```

应包含 `ai` 或 `llm` 配置段。

### 问题3：权限错误

如果看到权限警告：

```bash
chmod 600 ~/.openclaw/config.json
```

### 问题4：测试失败

```bash
# 重新安装依赖
pip install --upgrade openai

# 重新运行测试
python3 -m pytest tests/ -v
```

## 高级配置（可选）

如果需要自定义配置，可以设置环境变量：

```bash
# 自定义 API Key
export TOKEN_OPTIMIZER_API_KEY="your-key"

# 自定义模型
export TOKEN_OPTIMIZER_MODEL="gpt-4"

# 自定义 API URL
export TOKEN_OPTIMIZER_API_URL="https://api.openai.com/v1"
```

## 卸载

```bash
# 删除技能目录
rm -rf ~/.openclaw/workspace/skills/token-optimizer

# 可选：删除记忆文件
rm -rf ~/.openclaw/memory
```

## 获取帮助

- GitHub Issues: https://github.com/thanksandyou/token-optimizer/issues
- 文档: README.md
- 示例: SKILL.md
