# 微信公众号文章发布技能

自动化发布 Markdown 文章到微信公众号草稿箱的完整流程。

## 功能

- Markdown 转 HTML（适配微信公众号格式）
- 自动生成封面图（Pillow 规则绘制 / AI 大模型生成）
- 批量发布文章到草稿箱
- 支持多个专题管理

## 使用方法

1. 配置 `.env` 文件填写微信公众号 AppID 和 Secret
2. （可选）配置 AI 图片生成 API
3. 准备文章目录结构（每个期数一个文件夹）
4. 运行发布脚本

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| WECHAT_APP_ID | 公众号 AppID | - |
| WECHAT_APP_SECRET | 公众号 AppSecret | - |
| WECHAT_ACCOUNT_NAME | 作者署名 | - |
| AI_IMAGE_BASE_URL | AI 图片 API 地址 | https://api.openai.com/v1 |
| AI_IMAGE_API_KEY | AI 图片 API 密钥 | - |
| AI_IMAGE_MODEL | AI 图片模型 | dall-e-3 |

## 目录结构示例

```
tutorials/
├── your-tutorial/
│   ├── 01-getting-started/
│   │   ├── README.md      # 文章内容
│   │   └── cover.png      # 封面图（可选）
│   ├── 02-advanced/
│   │   ├── README.md
│   │   └── cover.png
│   └── ...
```

## 文件说明

- `publisher.py` - 核心发布脚本
- `cover_generator.py` - 封面图生成工具
- `template.env` - 环境变量模板

## 注意事项

- 文章使用 Markdown 格式编写
- 封面图尺寸建议 900x383px
- 发布前请确保文章内容已审核
