# 微信公众号文章发布技能

## 安装依赖

```bash
pip install requests markdown2 Pillow
```

## 配置

1. 复制 `template.env` 为 `.env`
2. 填写微信公众号的 AppID 和 AppSecret

## 使用示例

### 发布单篇文章

```python
from publisher import WeChatPublisher

publisher = WeChatPublisher(
    app_id="your_app_id",
    app_secret="your_app_secret",
    account_name="你的公众号名称"
)

draft_id = publisher.publish_article(
    article_path="path/to/README.md",
    cover_path="path/to/cover.png"
)
print(f"草稿 ID: {draft_id}")
```

### 批量发布

```python
from publisher import WeChatPublisher, batch_publish

publisher = WeChatPublisher(app_id, app_secret, account_name)

episodes = [
    (1, "01-intro", "入门介绍"),
    (2, "02-advanced", "进阶内容"),
]

results = batch_publish("/path/to/tutorial", publisher, episodes)
```

### 生成封面图

```python
from cover_generator import generate_cover

generate_cover(
    output_path="./cover.png",
    title="教程标题",
    subtitle="副标题",
    episode="第一期",
    tagline="关键词1 | 关键词2"
)
```

### 使用 AI 生成封面图

```python
from cover_generator import generate_cover_with_ai

# 方式一：返回 base64 格式（推荐）
generate_cover_with_ai(
    output_path="./cover_ai.png",
    prompt="A modern tech blog cover with blue gradient and abstract shapes",
    base_url="https://api.openai.com/v1",
    api_key="your_api_key",
    model="dall-e-3"
)

# 方式二：返回 URL 格式
from cover_generator import generate_cover_with_ai_url
generate_cover_with_ai_url(
    output_path="./cover_ai.png",
    prompt="...",
    api_key="your_api_key"
)
```

### 环境变量配置

```bash
# AI 图片生成配置
export AI_IMAGE_BASE_URL="https://api.openai.com/v1"
export AI_IMAGE_API_KEY="your_api_key"
export AI_IMAGE_MODEL="dall-e-3"
```

## 目录结构

```
your-tutorial/
├── 01-intro/
│   ├── README.md    # 文章内容（Markdown）
│   └── cover.png    # 封面图（900x383px）
├── 02-advanced/
│   ├── README.md
│   └── cover.png
└── ...
```

## 注意事项

- 封面图尺寸建议 900x383px
- 文章使用 Markdown 格式
- 发布后需登录公众号后台确认发布
