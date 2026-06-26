# wechat-publish-pro

把文章发到微信公众号草稿箱，发布前自动 AI 去痕，让内容读起来更像真人写的。

## 装上

```bash
pip install git+https://github.com/yuesf/wechat-publish-pro.git
```

## 配一下

### 第一步：获取微信公众号凭证

1. 登录 [https://developers.weixin.qq.com/](https://developers.weixin.qq.com/) 公众号平台
2. 获取 **AppID** 和 **AppSecret**

### 第二步：配置凭证

```bash
# 初始化
wechat-publish-pro config init

# 微信公众号的凭证
wechat-publish-pro config set wechat.app_id <你的AppID>
wechat-publish-pro config set wechat.app_secret <你的AppSecret>

# AI 去痕用的 API（可选，但建议配）
wechat-publish-pro config set ai.api_key <你的API Key>
wechat-publish-pro config set ai.provider qwen  # 或者 openai、zhipu 等
```

### 第三步：设置 IP 白名单

把运行机器的 IP 添加到微信公众号后台白名单：
1. 登录 https://mp.weixin.qq.com/
2. 设置与开发 → 基本配置 → IP白名单

## 用一下

### 通过 OpenClaw 直接发送

在 OpenClaw 对话中直接说：
- "把这篇文章发到公众号"
- "用蓝色主题发布"
- "帮我发布到微信，测试一下"

### 命令行方式

```bash
# 把 HTML 文章发到公众号草稿箱，自动 AI 去痕
wechat-publish-pro publish article.html

# 不用 AI 去痕
wechat-publish-pro publish article.html --no-humanize

# 指定标题和封面
wechat-publish-pro publish article.html --title "文章标题" --cover cover.jpg

# 调过去痕强度
wechat-publish-pro publish article.html --intensity light   # 轻度
wechat-publish-pro publish article.html --intensity heavy  # 重度

# 看看配置对不对
wechat-publish-pro config show

# 测试微信连接
wechat-publish-pro test
```

### Markdown 转换

```bash
# 把 Markdown 转成 HTML（默认绿色主题）
wechat-publish-pro convert article.md

# 指定蓝色主题
wechat-publish-pro convert article.md --theme blue

# 转换后发布
wechat-publish-pro convert article.md -o /tmp/article.html
wechat-publish-pro publish /tmp/article.html
```

## 环境变量

不想用 config 命令？直接环境变量：

```bash
export WECHAT_APP_ID=xxx
export WECHAT_APP_SECRET=xxx
export AI_API_KEY=xxx
export AI_PROVIDER=qwen
```

## 支持的 AI Provider

| Provider | 说明 |
|----------|------|
| openai | OpenAI GPT 系列 |
| qwen | 通义千问（默认） |
| zhipu | 智谱 GLM |
| doubao | 豆包 |
| minimax | MiniMax |
| moonshot | Moonshot |
| hunyuan | 腾讯混元 |
| yi | 零一万物 |

## 可用主题

| 主题 | 风格 |
|------|------|
| green | 清新自然（绿色，默认） |
| blue | 清新专业（蓝色） |
| purple | 优雅神秘（紫色） |
| orange | 温暖活力（橙色） |
| default | 简洁清爽 |
| simple | 极简风格 |

## 开发

```bash
git clone https://github.com/yuesf/wechat-publish-pro.git
cd wechat-publish-pro
pip install -e .
wechat-publish-pro --help
```

## 从 multi-writing-skills 剥离

这个项目从 [multi-writing-skills](https://github.com/yuesf/multi-writing-skills) 里剥离出来的，专门用来发公众号。

## License

MIT
