# Xiaohu WeChat Format

基于 `xiaohuailabs/xiaohu-wechat-format` 适配的 OpenClaw skill，用于微信公众号排版与草稿箱发布：

- Markdown / 粗糙笔记 → 微信兼容的内联样式 HTML
- 33 套主题与浏览器画廊预览
- 本地/外部图片上传到微信 CDN
- 带封面图推送到公众号草稿箱
- 可选封面生成与评论自动回复辅助脚本

## 快速开始

```bash
cp config.example.json config.json
# 需要推送草稿时，填写 wechat.app_id / wechat.app_secret。

uv run --with markdown python scripts/format.py \
  --input article.md --theme newspaper --no-open

uv run --with markdown --with requests --with pillow python scripts/publish.py \
  --input article.md --theme newspaper --cover cover.jpg
```

OpenClaw agent 使用时请先读取 `SKILL.md`。推送草稿箱、评论自动回复等外部写操作必须先获得用户明确确认。

## 注意事项

- 不要发布 `config.json`、token、API key。
- 需要在微信公众号后台把服务器公网 IP 加入白名单；`40164` 表示 IP 未加入白名单。
- 从微信公众号文章抓取的图片可能后缀是 `.png/.jpg`，实际却是 WebP；发布时带上 Pillow，`publish.py` 会自动转 JPEG 后上传。

## License

MIT，沿用上游项目声明。
