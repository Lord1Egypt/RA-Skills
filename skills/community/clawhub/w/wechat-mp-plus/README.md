# wechat-mp-publisher

微信公众号自动化管理 OpenClaw Skill - 草稿发布、菜单管理、自动回复、Markdown排版

## 功能

- **草稿箱管理**：上传素材、创建/列出/删除草稿
- **自定义菜单**：查询/创建/删除菜单
- **自动回复查询**：查看关注回复和关键词回复规则
- **Markdown排版**：Markdown转微信HTML，内置3套主题（default/elegant/dark）
- **一键发布**：Markdown文件 → 图片上传 → HTML转换 → 创建草稿

## 配置

设置环境变量：

```bash
export WECHAT_MP_APP_ID="你的AppID"
export WECHAT_MP_APP_SECRET="你的AppSecret"
```

或在 `.secrets/wechat_mp.env` 中配置：

```
WECHAT_MP_APP_ID=你的AppID
WECHAT_MP_APP_SECRET=你的AppSecret
```

## 快速开始

```bash
# 获取Token
python3 scripts/wechat_mp.py token

# 一键发布
python3 scripts/publish.py article.md cover.jpg "文章标题" "作者" "摘要" elegant

# 菜单管理
python3 scripts/menu.py get
python3 scripts/menu.py delete

# 查看自动回复
python3 scripts/wechat_mp.py autoreply

# Markdown转HTML
python3 scripts/md2html.py article.md dark
```

## 主题

| 主题 | 说明 |
|------|------|
| default | 清爽简约，微信绿色调 |
| elegant | 文艺范，衬线字体+红色点缀 |
| dark | 暗色科技感，适合技术文章 |

## 依赖

- Python 3.7+
- `markdown` 库（脚本自动安装）

## 作者

huuuwnnn-droid
