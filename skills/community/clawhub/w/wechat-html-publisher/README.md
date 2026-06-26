# 微信公众号HTML发布工具

快速上传HTML富文本到微信公众号草稿箱

## 快速使用

```bash
# 设置环境变量
export WECHAT_APP_ID=YOU_WECHAT_APP_ID
export WECHAT_APP_SECRET=YOU_WECHAT_APP_SECRET

# 发布文章
python scripts/publish_html.py \
  --file article.html \
  --title "文章标题" \
  --cover cover.jpg
```

## 安装依赖

```bash
pip install requests
```

## 完整示例

```bash
python scripts/publish_html.py \
  --file my-article.html \
  --title "2026年税务新政解读" \
  --cover ./images/cover.jpg \
  --author "慧评税" \
  --digest "详细解读2026年最新税务政策" \
  --source-url "https://example.com/article"
```

## 注意事项

1. HTML必须使用内联样式
2. 确保IP在微信公众号白名单中
3. 图片会自动上传到微信图床
4. 封面图必须提供

详细文档请查看 SKILL.md
