# 🎉 免费 LLM API 指南

本指南为您提供免费的 LLM API 配置方法，让记忆系统能够处理图片、音频、视频等多模态内容。

## 🔧 支持的免费 API

| 服务 | 网址 | 免费额度 | 特点 |
|------|------|----------|------|
| **DeepSeek** | https://platform.deepseek.com | 每月 300 万 token | 支持多模态，响应速度快 |
| **智谱AI** | https://open.bigmodel.cn | 每月 100 万 token | 中文支持好，免费额度高 |
| **百川智能** | https://www.baichuan-ai.com | 每月 200 万 token | 支持多模态，API 稳定 |
| **Qwen** | https://dashscope.aliyuncs.com | 每月 100 万 token | 阿里云支持，可靠稳定 |

## 🚀 配置步骤

### 方法 1：DeepSeek（推荐）

1. **注册账号**
   - 访问 https://platform.deepseek.com
   - 点击「注册」按钮，使用邮箱或手机号注册

2. **获取 API Key**
   - 登录后，进入「控制台」→「API 密钥」
   - 点击「创建密钥」，复制生成的 API Key

3. **配置环境变量**
   ```bash
   # Linux/macOS
   export FREE_LLM_API_URL="https://api.deepseek.com/v1"
   export FREE_LLM_API_KEY="your-api-key"

   # Windows (PowerShell)
   $env:FREE_LLM_API_URL = "https://api.deepseek.com/v1"
   $env:FREE_LLM_API_KEY = "your-api-key"
   ```

### 方法 2：智谱AI

1. **注册账号**
   - 访问 https://open.bigmodel.cn
   - 点击「注册」按钮，使用手机号注册

2. **获取 API Key**
   - 登录后，进入「控制台」→「API 密钥」
   - 点击「创建密钥」，复制生成的 API Key

3. **配置环境变量**
   ```bash
   # Linux/macOS
   export FREE_LLM_API_URL="https://open.bigmodel.cn/api/mcp"
   export FREE_LLM_API_KEY="your-api-key"

   # Windows (PowerShell)
   $env:FREE_LLM_API_URL = "https://open.bigmodel.cn/api/mcp"
   $env:FREE_LLM_API_KEY = "your-api-key"
   ```

### 方法 3：百川智能

1. **注册账号**
   - 访问 https://www.baichuan-ai.com
   - 点击「注册」按钮，使用手机号注册

2. **获取 API Key**
   - 登录后，进入「控制台」→「API 密钥」
   - 点击「创建密钥」，复制生成的 API Key

3. **配置环境变量**
   ```bash
   # Linux/macOS
   export FREE_LLM_API_URL="https://api.baichuan-ai.com/v1"
   export FREE_LLM_API_KEY="your-api-key"

   # Windows (PowerShell)
   $env:FREE_LLM_API_URL = "https://api.baichuan-ai.com/v1"
   $env:FREE_LLM_API_KEY = "your-api-key"
   ```

### 方法 4：Qwen（通义千问）

1. **注册账号**
   - 访问 https://dashscope.aliyuncs.com
   - 使用阿里云账号登录

2. **获取 API Key**
   - 登录后，进入「API-KEY 管理」
   - 点击「创建 API Key」，复制生成的 Key

3. **配置环境变量**
   ```bash
   # Linux/macOS
   export FREE_LLM_API_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
   export FREE_LLM_API_KEY="your-api-key"

   # Windows (PowerShell)
   $env:FREE_LLM_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
   $env:FREE_LLM_API_KEY = "your-api-key"
   ```

## 🎯 自动检测机制

记忆系统会按照以下顺序自动检测 LLM：

1. **OpenClaw 的 LLM**（如果运行在 OpenClaw 中）
2. **OpenAI GPT-4o**（如果设置了 OPENAI_API_KEY）
3. **Anthropic Claude 3.5**（如果设置了 ANTHROPIC_API_KEY）
4. **Google Gemini 1.5**（如果设置了 GOOGLE_API_KEY）
5. **小米 MiMo Omni**（如果设置了 MIMO_API_URL）
6. **Ollama 本地模型**（如果设置了 OLLAMA_HOST）
7. **免费 LLM API**（如果设置了 FREE_LLM_API_URL）
8. **基础处理**（无多模态能力）

## 🔍 测试配置

```bash
# 测试 LLM 配置
python3 -c "
from media_processor import MediaProcessor
p = MediaProcessor.auto()
print('处理器创建成功')
print('视觉能力:', p.vision_fn is not None)
print('音频能力:', p.audio_fn is not None)
"
```

## 💡 常见问题

### Q: 免费 API 有什么限制？
**A:** 免费 API 通常有每月 token 限制，超出后需要付费或等待下月重置。

### Q: 免费 API 支持哪些功能？
**A:** 大多数免费 API 支持图片处理，但可能不支持音频和视频。

### Q: 如何查看 API 使用情况？
**A:** 登录对应平台的控制台，查看 API 使用统计。

### Q: 配置后不生效怎么办？
**A:** 检查环境变量是否正确设置，重启终端后再试。

## 📊 性能对比

| 服务 | 响应速度 | 多模态支持 | 中文能力 | 稳定性 |
|------|----------|------------|----------|--------|
| DeepSeek | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 智谱AI | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 百川智能 | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Qwen | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## 🎉 推荐方案

**初学者推荐：DeepSeek**
- 注册简单，免费额度高
- 支持多模态，响应速度快
- 接口与 OpenAI 兼容

**中文需求推荐：智谱AI**
- 中文支持最好
- 免费额度高
- 国内访问速度快

**稳定需求推荐：百川智能**
- API 稳定可靠
- 支持多模态
- 企业级服务

现在您已经了解了如何配置免费的 LLM API，记忆系统可以使用这些 API 来处理多模态内容了！
