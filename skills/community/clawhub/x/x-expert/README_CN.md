# X Expert - 智能 X 发布助手

ClawHub Skill for OpenClaw/NanoClaw

## 功能

这是一个智能的 X (Twitter) 发布助手，通过**对话式流程**帮助你创建、策划和发布推文。

### 核心功能

- ✅ 对话式发布流程（9 步）
- ✅ 信息收集（Exa / MiniMax / Brave Search）
- ✅ 智能推文生成（多种风格）
- ✅ 配图生成（DALL-E / MiniMax / Nano Banana / Leonardo.ai）
- ✅ 定时发布
- ✅ 发布前审核

## 安装

### 方式 1: ClawHub CLI

```bash
npx clawhub@latest install x-expert
```

### 方式 2: 手动安装

```bash
git clone https://github.com/shiyusimon/x-publisher-skill.git ~/.openclaw/skills/x-publisher
cd ~/.openclaw/skills/x-publisher
npm install
```

## 配置

### 必需的环境变量

```bash
# X API (必需)
X_API_KEY=your_api_key
X_API_SECRET=your_api_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
```

### 可选的环境变量

```bash
# 搜索服务 (可选，选择一个或多个)
EXA_API_KEY=your_exa_key
MINIMAX_API_KEY=your_minimax_key
BRAVE_API_KEY=your_brave_key

# 图像生成服务 (可选，选择一个或多个)
OPENAI_API_KEY=your_openai_key       # DALL-E
MINIMAX_API_KEY=your_minimax_key    # MiniMax Image
NANO_BANANA_API_KEY=your_nano_key   # Nano Banana
LEONARDO_API_KEY=your_leonardo_key # Leonardo.ai
```

## 使用

输入 `/x-expert` 启动对话式发布流程。

### 对话流程

1. **确认需求** - 是否需要先收集信息？
2. **收集信息** - 搜索相关主题
3. **确认内容** - 是否需要帮你写推文？
4. **确定风格** - 选择推文风格和参考案例
5. **发布设置** - 定时/审核设置
6. **确认配图** - 是否需要图片？
7. **图片风格** - 选择图片风格和服务
8. **生成配图** - 调用 AI 生成图片
9. **最终确认** - 预览并发布

## 脚本

| 脚本 | 功能 |
|------|------|
| `post-tweet.js` | 发布单条推文 |
| `post-thread.js` | 发布推文串 |
| `post-media.js` | 发布带媒体推文 |
| `collect-info.js` | 搜索信息 |
| `generate-tweet.js` | 生成推文内容 |
| `generate-image.js` | 生成配图 |
| `delete-tweet.js` | 删除推文 |

## License

MIT
