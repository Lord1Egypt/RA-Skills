# tencent-cloud-article-publisher

OpenClaw Skill — 自动发布文章到腾讯云开发者社区

## 功能

- 直接调用腾讯云开发者社区 API，无需浏览器
- 支持 Markdown 格式自动转 HTML
- 一行命令完成发布

## 快速开始

### 1. 获取 Cookie

1. 登录 https://cloud.tencent.com/developer
2. 按 **F12** → **Application** → **Cookies** → **cloud.tencent.com**
3. 复制以下字段的值，用分号连接：
   ```
   skey; qcloud_uid; qcommunity_session; loginType; qcommunity_identify_id; tinyid; uin
   ```

### 2. 安装依赖

```bash
pip install requests
```

### 3. 发布文章

```bash
python3 publish_tencent.py "文章标题" "文章正文（支持Markdown）" "你的Cookie"
```

示例：
```bash
python3 publish_tencent.py \
  "OpenClaw + Qwen3-TTS 自动化简报系统实战" \
  "本文介绍如何用 **OpenClaw** 和 Qwen3-TTS 构建每日自动化简报系统..." \
  "skey=xxx; qcloud_uid=xxx; qcommunity_session=xxx; ..."
```

### 4. OpenClaw Skill 使用

将 `SKILL.md` 放入 `~/.openclaw/skills/tencent-cloud-publish/`，然后说"帮我发到腾讯云"即可。

## API 信息

| 项目 | 值 |
|------|-----|
| 发布 API | `POST https://cloud.tencent.com/developer/api/article/addArticle` |
| 成功响应 | `{"articleId":2650368,"status":0}` |

## Payload 格式

```json
{
  "title": "标题",
  "content": "<p>HTML正文</p>",
  "plain": "纯文本",
  "summary": "摘要",
  "userSummary": "摘要",
  "sourceType": 1,
  "isOriginal": true,
  "classifyIds": [149],
  "openComment": 1,
  "closeTextLink": 0
}
```

## 注意事项

- Cookie 会过期，发布失败时需要重新获取
- `skey` 包含特殊字符 `*`，requests 库会自动处理
- 每次发布间隔建议 > 10 秒

## License

MIT
