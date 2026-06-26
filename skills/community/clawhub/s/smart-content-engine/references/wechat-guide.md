# 微信公众号 API 配置与使用指南

本指南帮助你完成微信公众号的 API 接入配置，实现通过 content-engine 自动发布文章到公众号。

---

## 前置条件

1. 已注册微信公众号（服务号或订阅号，推荐服务号）
2. 已完成微信认证（未认证账号 API 权限受限）
3. 具有管理员权限

---

## 第一步：获取 AppID 和 AppSecret

1. 登录 [微信公众平台](https://mp.weixin.qq.com/)
2. 进入「设置与开发」→「基本配置」
3. 在「公众号开发信息」区域找到：
   - **AppID（应用ID）**：固定不变，直接复制
   - **AppSecret（应用密钥）**：点击「重置」生成新密钥，**务必立即保存**，页面关闭后无法再次查看

4. 配置环境变量：
   ```bash
   export CE_WECHAT_APPID="你的AppID"
   export CE_WECHAT_SECRET="你的AppSecret"
   ```

> **安全提醒**：AppSecret 等同于账号密码，绝不能泄露。不要将其写入代码或提交到版本控制系统。

---

## 第二步：配置 IP 白名单

1. 在「基本配置」页面找到「IP白名单」
2. 点击「修改」，添加你的服务器公网 IP 地址
3. 若在本地开发，添加本机公网 IP（可通过 `curl ifconfig.me` 查询）

> 未配置白名单的 IP 地址调用 API 将返回 `40164` 错误。

---

## 第三步：access_token 机制说明

### 获取 access_token

content-engine 会自动调用以下接口获取 access_token：

```
GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
```

返回示例：
```json
{
  "access_token": "ACCESS_TOKEN",
  "expires_in": 7200
}
```

### 有效期与刷新

- access_token 有效期为 **7200 秒（2 小时）**
- 每日调用上限为 **2000 次**
- content-engine 会在每次发布操作时自动获取新的 access_token
- 建议不要频繁调用，避免触发速率限制

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 40001 | AppSecret 错误 | 检查 CE_WECHAT_SECRET 是否正确 |
| 40002 | grant_type 无效 | 检查请求参数 |
| 40164 | IP 未在白名单 | 在公众号后台添加 IP 白名单 |
| 42001 | access_token 过期 | 重新获取（自动处理） |
| 45009 | API 调用频次超限 | 降低调用频率，等待后重试 |

---

## 第四步：文章发布流程

content-engine 的微信发布采用以下流程：

### 1. 创建草稿

```
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN
```

请求体：
```json
{
  "articles": [
    {
      "title": "文章标题",
      "author": "作者",
      "digest": "摘要",
      "content": "<p>HTML格式正文</p>",
      "content_source_url": "",
      "thumb_media_id": "封面图素材ID",
      "need_open_comment": 0,
      "only_fans_can_comment": 0
    }
  ]
}
```

### 2. 发布文章

```
POST https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=ACCESS_TOKEN
```

请求体：
```json
{
  "media_id": "草稿的media_id"
}
```

### 3. 查询发布状态

```
POST https://api.weixin.qq.com/cgi-bin/freepublish/get?access_token=ACCESS_TOKEN
```

请求体：
```json
{
  "publish_id": "发布任务ID"
}
```

---

## 第五步：素材管理

### 上传永久素材（封面图）

如需设置文章封面图，需先上传图片为永久素材：

```
POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=ACCESS_TOKEN&type=image
```

返回的 `media_id` 可用于文章的 `thumb_media_id` 字段。

### 上传正文图片

正文中的图片需通过以下接口上传：

```
POST https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=ACCESS_TOKEN
```

返回的 URL 可直接在 HTML 正文的 `<img>` 标签中使用。

---

## 常见问题

### Q1：订阅号和服务号有什么区别？

服务号拥有更多 API 权限，包括模板消息、自定义菜单、网页授权等。建议使用服务号进行内容分发。

### Q2：发布后可以修改文章吗？

微信公众号已发布的文章不支持直接修改内容。如需更正，可以删除后重新发布，或发布勘误声明。

### Q3：每天可以发布几篇文章？

- 订阅号：每天 1 次推送，每次最多 8 篇
- 服务号：每月 4 次推送，每次最多 8 篇

### Q4：如何处理图片？

目前 content-engine 的微信适配器会将 Markdown 图片转换为 HTML `<img>` 标签。若图片为外部 URL，需确保微信服务器可访问该地址。建议使用微信素材接口上传图片获取永久链接。

---

## 调试建议

1. 使用 [微信公众平台接口调试工具](https://mp.weixin.qq.com/debug/) 测试 API 调用
2. 检查返回的 JSON 中是否包含 `errcode` 字段
3. 确认 IP 白名单配置正确
4. 确认 AppSecret 未被重置（重置后旧密钥立即失效）
