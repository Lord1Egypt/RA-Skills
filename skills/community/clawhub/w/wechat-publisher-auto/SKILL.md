# wechat-publish-pro Skill

微信公众号文章发布工具，完全独立实现，不依赖任何外部 CLI 工具。

## 功能特性

- **纯 Python 实现**: 不依赖 wenyan-cli 或其他外部工具
- **Markdown 转换**: 内置 Markdown → HTML 转换，参考 wenyan-cli 排版风格
- **多主题支持**: 多种精美主题（green、blue、purple、orange、default、simple）
- **代码高亮**: Mac 风格代码块，语法高亮
- **AI 去痕**: 发布前自动 AI 去痕处理，让内容读起来更像真人写的
- **封面生成**: 自动处理封面图，支持本地/网络图片
- **直接发布**: 一键发布到微信公众号草稿箱

## 触发条件

当用户需要以下操作时自动触发：
- 将 Markdown 或 HTML 文章发布到微信公众号草稿箱
- 转换 Markdown 为公众号格式 HTML
- 使用特定主题发布公众号文章
- 测试微信连接

## 安装

```bash
# 从 GitHub 安装
pip install git+https://github.com/yuesf/wechat-publish-pro.git
```

## 配置

### 第一步：获取微信公众号凭证

1. 登录 [https://developers.weixin.qq.com/](https://developers.weixin.qq.com/) 公众号平台
2. 获取 **AppID** 和 **AppSecret**

### 第二步：配置凭证

#### 配置文件（多账号支持）

配置文件路径：`~/.wechat-publish-pro/config.yaml`

```yaml
accounts:
  # 账号1（设为默认）
  default:
    name: 技术公众号
    app_id: wx89c409208d11dc5b
    app_secret: your_app_secret_here
  # 账号2
  health:
    name: 养生公众号
    app_id: cli_a95b243c6278dccf
    app_secret: your_app_secret_here
  # 可添加更多账号...
default_account: default

ai:
  provider: qwen
  api_key: your_api_key
  base_url: ""
  model: ""
```

#### 环境变量（单账号兼容）

```bash
export WECHAT_APP_ID=your_wechat_app_id
export WECHAT_APP_SECRET=your_wechat_app_secret

# AI 去痕（可选）
export AI_API_KEY=your_api_key
export AI_PROVIDER=qwen  # openai, qwen, zhipu, doubao, minimax, moonshot, hunyuan, yi
```

### 第三步：设置 IP 白名单

把运行机器的 IP 添加到微信公众号后台白名单：
1. 登录 https://mp.weixin.qq.com/
2. 设置与开发 → 基本配置 → IP白名单

## 使用方式

### 通过 OpenClaw 直接发送

在 OpenClaw 对话中直接说：
- "把这篇文章发到公众号"
- "用蓝色主题发布"
- "帮我发布到微信，测试一下"
- "使用 AI 去痕发布"

### 命令行方式

#### Markdown 转换

```bash
# 基本转换（默认绿色主题）
wechat-publish-pro convert article.md

# 指定蓝色主题
wechat-publish-pro convert article.md --theme blue

# 指定输出文件
wechat-publish-pro convert article.md -o output.html
```

#### 发布到微信

```bash
# 发布 HTML 文件到草稿箱（使用默认账号）
wechat-publish-pro publish article.html

# 指定账号发布
wechat-publish-pro publish article.html --account health

# 指定标题和封面
wechat-publish-pro publish article.html --title "文章标题" --cover cover.jpg

# 不使用 AI 去痕
wechat-publish-pro publish article.html --no-humanize

# 调整 AI 去痕强度
wechat-publish-pro publish article.html --intensity heavy
```

#### 一站式：Markdown → 转换 → 发布

```bash
# 转换后直接发布
wechat-publish-pro convert article.md --theme blue -o /tmp/article.html
wechat-publish-pro publish /tmp/article.html --title "文章标题"
```

#### 测试连接

```bash
wechat-publish-pro test
```

#### 上传图片

```bash
wechat-publish-pro upload-image image.jpg
```

## Markdown 格式

文件顶部可以包含 frontmatter：

```markdown
---
title: 文章标题
cover: ./assets/cover.jpg
---

# 正文开始（frontmatter 有 title 时会自动移除）

你的内容...
```

## 可用主题

| 主题 | 风格 |
|------|------|
| green | 清新自然（绿色，默认） |
| blue | 清新专业（蓝色） |
| purple | 优雅神秘（紫色） |
| orange | 温暖活力（橙色） |
| default | 简洁清爽 |
| simple | 极简风格 |

## AI 去痕

AI 去痕是可选功能，让文章读起来更自然。支持的 Provider：

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

去痕强度：
- `light` - 轻度：保持原文大部分内容，只做轻微调整
- `medium` - 中度：适度调整，保留核心内容
- `heavy` - 重度：大幅调整，使文章焕然一新

## 故障排查

### 错误：45166 (IP地址不在白名单中)
- 原因：运行机器的 IP 未添加到微信白名单
- 解决：登录公众号后台添加 IP 到白名单

### 发布成功但看不到文章？
- 原因：文章在草稿箱，需要审核发布
- 解决：草稿箱 → 选中文章 → 发布

## 架构说明

```
wechat-publish-pro/
├── src/wechat_publisher/
│   ├── cli.py         # CLI 入口
│   ├── config.py      # 配置管理
│   ├── converter/     # Markdown 转换模块
│   │   ├── wechat_style.py   # 微信公众号样式转换器
│   │   ├── themes.py          # 主题配置
│   │   └── theme_types.py     # 主题数据类型
│   ├── humanizer/     # AI 去痕模块
│   └── platforms/     # 平台适配器
│       └── wechat.py # 微信公众号 API
└── pyproject.toml
```

## 设计参考

本项目参考了以下优秀项目的设计思路：
- **wenyan-cli**: Markdown 转微信 HTML 的排版思路
- **multi-writing-skills**: 转换器和主题系统的实现

但本项目是完全独立实现的，不依赖任何外部代码。

## 作者

yuesf

## 许可证

MIT
