# WeChat MP Publisher - OpenClaw Skill

微信公众号文章自动发布工具。

## 功能

- 🔐 AccessToken 自动管理
- 📤 素材上传（图片、视频）
- 📝 图文消息创建
- 📢 文章发布/保存草稿
- 📊 发布状态查询

## 配置

在 `~/.openclaw/config/wechat-mp.json` 创建配置文件：

```json
{
  "app_id": "your-app-id",
  "app_secret": "your-app-secret",
  "default_author": "默认作者"
}
```

或使用环境变量：

```bash
export WECHAT_MP_APP_ID="your-app-id"
export WECHAT_MP_APP_SECRET="your-app-secret"
```

## 使用

### 通过 OpenClaw Tool

```bash
# 发布文章
openclaw tool wechat-mp-publish --title "文章标题" --content "正文内容" --cover /path/to/image.jpg

# 上传素材
openclaw tool wechat-mp-upload-media --file /path/to/image.jpg --type image

# 查询草稿列表
openclaw tool wechat-mp-query-drafts
```

### 直接调用（开发测试）

```bash
npm install
npm run build
node dist/scripts/publish.js --title "测试文章" --content "测试内容"
```

## 依赖

- Node.js >= 18
- 微信公众号认证服务号

## License

MIT
