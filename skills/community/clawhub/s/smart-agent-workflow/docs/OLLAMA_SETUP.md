# 本地大模型接入指南（Ollama）

## 🎯 目标

使用 Ollama 在本地运行大模型，完全免费，无需 API Key。

## 📋 准备工作

### 1. 安装 Ollama

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
下载安装包：https://ollama.com/download

### 2. 启动 Ollama 服务

```bash
ollama serve
```

服务会在 `http://localhost:11434` 运行。

### 3. 下载模型

```bash
# 推荐模型（按大小和性能排序）

# 小模型（适合笔记本，4GB 内存）
ollama pull llama2:7b

# 中等模型（推荐，8GB 内存）
ollama pull llama2:13b
ollama pull mistral

# 大模型（性能最好，16GB+ 内存）
ollama pull llama2:70b
ollama pull codellama:34b  # 代码专用

# 中文模型
ollama pull qwen:7b
ollama pull qwen:14b
```

### 4. 测试模型

```bash
# 交互式测试
ollama run llama2

# 输入问题测试
> 你好，介绍一下你自己
```

## 🚀 接入 Telegram Bot

### 方式 1：使用环境变量（推荐）

```bash
cd ~/Desktop/smart-agent-template/integrations/telegram

# 配置环境变量
export TELEGRAM_BOT_TOKEN="你的Bot Token"
export TELEGRAM_ADMIN_CHAT_ID="你的Chat ID"
export AI_ENGINE=ollama
export OLLAMA_BASE_URL=http://localhost:11434
export OLLAMA_MODEL=llama2

# 启动 Bot
python bot.py
```

### 方式 2：使用 .env 文件

```bash
cd ~/Desktop/smart-agent-template/integrations/telegram

# 创建 .env 文件
cat > .env << 'EOF'
TELEGRAM_BOT_TOKEN=你的Bot Token
TELEGRAM_ADMIN_CHAT_ID=你的Chat ID
AI_ENGINE=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
EOF

# 安装 python-dotenv
pip install python-dotenv

# 启动 Bot
python bot.py
```

### 方式 3：直接修改代码

编辑 `config.py`，在 `Config.__init__` 中添加默认值：

```python
self.ai = AIConfig(
    engine='ollama',
    api_key=None,
    model='llama2',
    base_url='http://localhost:11434'
)
```

## 📝 完整启动步骤

### 第 1 步：启动 Ollama 服务

```bash
# 新开一个终端
ollama serve
```

保持这个终端运行。

### 第 2 步：下载模型（首次使用）

```bash
# 新开另一个终端
ollama pull llama2
```

等待下载完成（约 3.8GB）。

### 第 3 步：测试模型

```bash
ollama run llama2
> 你好
> exit
```

确认模型可以正常回复。

### 第 4 步：配置 Bot

```bash
cd ~/Desktop/smart-agent-template/integrations/telegram

# 方式 1：环境变量
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_ADMIN_CHAT_ID="your_chat_id"
export AI_ENGINE=ollama
export OLLAMA_MODEL=llama2

# 方式 2：或者创建 .env 文件
echo 'TELEGRAM_BOT_TOKEN=your_bot_token' > .env
echo 'TELEGRAM_ADMIN_CHAT_ID=your_chat_id' >> .env
echo 'AI_ENGINE=ollama' >> .env
echo 'OLLAMA_MODEL=llama2' >> .env
```

### 第 5 步：启动 Bot（需要翻墙）

```bash
# 设置代理（Surge）
export http_proxy=http://127.0.0.1:6152
export https_proxy=http://127.0.0.1:6152

# 启动 Bot
python bot.py
```

### 第 6 步：测试 Bot

1. 打开 Telegram
2. 搜索你的 Bot
3. 发送消息测试

## 🎨 推荐模型对比

| 模型 | 大小 | 内存需求 | 速度 | 质量 | 适用场景 |
|------|------|---------|------|------|---------|
| llama2:7b | 3.8GB | 4GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 日常对话 |
| llama2:13b | 7.3GB | 8GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 推荐 |
| mistral | 4.1GB | 4GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 平衡选择 |
| qwen:7b | 4.4GB | 4GB | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中文优化 |
| codellama:7b | 3.8GB | 4GB | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 代码生成 |

## ⚡ 性能优化

### 1. 使用 GPU 加速（如果有 NVIDIA 显卡）

Ollama 会自动检测并使用 GPU。

### 2. 调整并发数

```bash
# 设置最大并发请求数
export OLLAMA_MAX_LOADED_MODELS=1
```

### 3. 预加载模型

```bash
# 启动时预加载模型到内存
ollama run llama2 --keepalive 24h
```

## 🐛 常见问题

### 1. Ollama 服务无法启动

```bash
# 检查端口是否被占用
lsof -i :11434

# 或者换个端口
ollama serve --port 11435
```

### 2. 模型下载失败

```bash
# 清理缓存重试
rm -rf ~/.ollama/models
ollama pull llama2
```

### 3. Bot 连接 Ollama 失败

```bash
# 检查 Ollama 是否运行
curl http://localhost:11434/api/tags

# 应该返回模型列表
```

### 4. 回复很慢

- 使用更小的模型（llama2:7b）
- 确保 Ollama 使用了 GPU
- 减少 max_tokens

## 💡 进阶使用

### 自定义模型参数

编辑 `ai_adapter.py`，在 `OllamaAdapter.get_response` 中添加：

```python
response = await self.client.chat.completions.create(
    model=self.model,
    messages=[...],
    temperature=0.7,      # 创造性（0-1）
    max_tokens=512,       # 最大长度
    top_p=0.9            # 采样策略
)
```

### 切换模型

```bash
# 运行时切换
export OLLAMA_MODEL=mistral
python bot.py

# 或者在代码中动态切换
```

## 📊 对比：本地 vs 云端

| 项目 | 本地（Ollama） | 云端（OpenAI/Claude） |
|------|---------------|---------------------|
| 费用 | ✅ 完全免费 | ❌ 按量付费 |
| 速度 | ⚠️ 取决于硬件 | ✅ 快速 |
| 质量 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 隐私 | ✅ 完全本地 | ⚠️ 数据上传 |
| 网络 | ✅ 无需翻墙 | ❌ 需要翻墙 |
| 门槛 | ⚠️ 需要配置 | ✅ 开箱即用 |

## 🎯 推荐方案

**开发测试：** Ollama（免费，快速迭代）  
**生产环境：** Claude/OpenAI（质量更好）  
**混合方案：** 简单问题用 Ollama，复杂问题用云端

---

**更新日期**: 2026-03-28  
**适用场景**: 本地开发、隐私保护、成本控制
