# 微信公众号一键写作发布 - OpenClaw Skill

一句话生成文章，自动排版美化，一键发布到微信公众号草稿箱。可选 AI 配图。

## 功能

- AI 写作：根据一句话主题自动撰写完整文章
- AI 配图（可选）：使用文生图 API 自动生成文章配图和封面
- 精美排版：自动将 Markdown 转换为微信公众号适配的精美 HTML
- 一键发布：自动上传素材并创建草稿到微信公众号草稿箱

## 安装（Linux 服务器）

### 1. 安装 Skill

```bash
cp -r wechat-article-publisher ~/.openclaw/skills/

# 给脚本加执行权限
chmod +x ~/.openclaw/skills/wechat-article-publisher/scripts/publish.py
```

### 2. 安装 Python 依赖

```bash
pip3 install -r ~/.openclaw/skills/wechat-article-publisher/requirements.txt
```

### 3. 配置

复制示例配置并填写：

```bash
cd ~/.openclaw/skills/wechat-article-publisher
cp config_example.json config.json
```

编辑 `config.json`：

```json
{
  "wechat": {
    "appid": "你的微信公众号 AppID",
    "appsecret": "你的微信公众号 AppSecret"
  },
  "image_api": {
    "api_key": "你的文生图 API Key",
    "api_base_url": "https://api.siliconflow.cn/v1/images/generations",
    "model": "black-forest-labs/FLUX.1-schnell"
  }
}
```

也可以通过环境变量配置（config.json 优先）：

```bash
# ===== 必填：微信公众号 =====
export WECHAT_APPID="你的AppID"
export WECHAT_APPSECRET="你的AppSecret"

# ===== 可选：AI 配图 =====
# 不填则不启用 AI 自动配图，使用默认封面图
export IMAGE_API_KEY="你的API Key"
export IMAGE_API_BASE_URL="https://api.siliconflow.cn/v1/images/generations"
export IMAGE_MODEL="black-forest-labs/FLUX.1-schnell"
```

**获取方式：**

| 配置项 | 是否必填 | 获取地址 |
|--------|----------|----------|
| WECHAT_APPID / APPSECRET | 必填 | [微信公众平台](https://mp.weixin.qq.com/) → 开发 → 基本配置 |
| IMAGE_API_KEY | 可选 | 你使用的文生图 API 服务商（如 [SiliconFlow](https://siliconflow.cn/)） |

> 支持任何兼容 OpenAI 格式的文生图 API，如 SiliconFlow、智谱、通义万相等。

### 4. 微信公众号 IP 白名单

在微信公众平台 → 开发 → 基本配置 → IP白名单 中，添加你 Linux 服务器的公网 IP：

```bash
# 查看服务器公网 IP
curl -s ifconfig.me
```

## 使用

在 OpenClaw 中直接输入：

```
帮我写一篇关于 AI Agent 发展趋势的文章
```

```
写一篇 Python 异步编程入门教程，不需要配图
```

```
写一篇 3000 字长文，主题是"大模型微调实战"
```

OpenClaw 会自动：
1. 确认配图偏好
2. 撰写完整文章
3. （如果开启 AI 配图）生成配图和封面
4. 排版为精美的微信公众号格式
5. 上传到微信公众号草稿箱

## 目录结构

```
wechat-article-publisher/
├── SKILL.md                        # OpenClaw Skill 定义
├── README.md                       # 本文件
├── requirements.txt                # Python 依赖
├── config_example.json             # 配置示例
├── assets/
│   └── default_cover.jpg           # 默认封面图（纯文字模式使用）
└── scripts/
    ├── publish.py                  # 主流程脚本
    ├── wechat_api.py               # 微信公众号 API
    ├── image_api.py                # 通用文生图 API
    └── formatter.py                # HTML 排版格式化
```

## 脚本独立使用

如果你想直接调用发布脚本（不通过 OpenClaw）：

```bash
# AI 配图模式（需要配置 image_api）
python3 scripts/publish.py \
  --article my_article.md \
  --cover-prompt "A futuristic AI illustration" \
  --author "你的名字"

# 纯文字模式（使用默认封面图）
python3 scripts/publish.py \
  --article my_article.md \
  --no-images \
  --author "你的名字"

# 纯文字模式 + 自定义封面
python3 scripts/publish.py \
  --article my_article.md \
  --no-images \
  --cover-image /path/to/cover.png \
  --author "你的名字"
```

参数说明：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--article` | 是 | Markdown 文章文件路径 |
| `--cover-prompt` | 否 | 封面图英文提示词（不填则自动生成） |
| `--cover-image` | 否 | 本地封面图路径（纯文字模式下可提供） |
| `--author` | 否 | 文章作者 |
| `--no-images` | 否 | 跳过 AI 图片生成（纯文字模式） |
| `--publish` | 否 | 草稿创建后立即提交发布 |

## 注意事项

- 微信公众号 access_token 有效期 2 小时，脚本会自动刷新
- 2025 年起，未认证公众号只能存草稿，不能正式发布
- 封面图推荐比例 2.35:1（AI 模式默认生成 1024x576）
- 部署在 Linux 服务器时，确保服务器公网 IP 已加入微信 IP 白名单
