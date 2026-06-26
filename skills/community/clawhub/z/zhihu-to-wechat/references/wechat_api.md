# 微信公众号 API 参考文档

## 目录
1. [权限要求](#权限要求)
2. [Access Token](#access-token)
3. [草稿箱接口](#草稿箱接口)
4. [素材上传](#素材上传)
5. [常见错误码](#常见错误码)

---

## 权限要求

| 接口 | 要求 |
|------|------|
| 草稿创建/发布 | **已认证服务号**，需在公众平台开通 |
| 图片上传 | 同上 |
| Access Token | 所有公众号均可获取 |

> ⚠️ **订阅号**无法通过 API 发布文章，只有**服务号**且完成微信认证（企业主体）才支持。
> 个人订阅号只能在公众平台后台手动发布。

---

## Access Token

**接口地址：**
```
GET https://api.weixin.qq.com/cgi-bin/token
    ?grant_type=client_credential
    &appid=APPID
    &secret=APPSECRET
```

**返回示例：**
```json
{
  "access_token": "ACCESS_TOKEN",
  "expires_in": 7200
}
```

**注意事项：**
- 有效期 **7200 秒（2小时）**
- 每日调用次数上限 **2000次**（同一 AppID）
- 建议缓存 Token，到期前 5 分钟刷新
- 多台服务器需使用**集中缓存**，避免各自刷新导致旧 Token 失效

---

## 草稿箱接口

### 新建草稿

```
POST https://api.weixin.qq.com/cgi-bin/draft/add
     ?access_token=ACCESS_TOKEN
```

**请求体：**
```json
{
  "articles": [
    {
      "title": "文章标题",
      "author": "作者",
      "digest": "文章摘要（120字以内）",
      "content": "HTML格式的正文内容",
      "content_source_url": "原文链接（可为空）",
      "thumb_media_id": "封面图的media_id（永久素材）",
      "need_open_comment": 1,
      "only_fans_can_comment": 0
    }
  ]
}
```

**注意：**
- `thumb_media_id` 必须是**永久素材**的 media_id，用 `add_material` 接口上传
- `content` 中的图片必须是微信CDN图片，不能用外链
- 一次最多提交 **8 篇**文章（图文消息）

**返回示例：**
```json
{
  "errcode": 0,
  "errmsg": "ok",
  "media_id": "草稿media_id"
}
```

### 发布草稿（触发发布）

```
POST https://api.weixin.qq.com/cgi-bin/freepublish/submit
     ?access_token=ACCESS_TOKEN
```

```json
{
  "media_id": "草稿media_id"
}
```

> **注意：** 发布接口存在**每日次数限制**，建议通过公众平台后台预览后手动发布。

---

## 素材上传

### 上传正文图片（返回 URL，推荐）

```
POST https://api.weixin.qq.com/cgi-bin/media/uploadimg
     ?access_token=ACCESS_TOKEN
```
- Content-Type: `multipart/form-data`
- 字段名：`media`
- 支持格式：jpg/png/gif，大小 ≤ 1MB
- **返回永久 URL**，可直接嵌入文章正文 `<img src="...">`

```json
{
  "url": "https://mmbiz.qpic.cn/..."
}
```

### 上传永久封面图（返回 media_id）

```
POST https://api.weixin.qq.com/cgi-bin/material/add_material
     ?access_token=ACCESS_TOKEN&type=image
```
- 用于草稿的 `thumb_media_id` 字段

```json
{
  "media_id": "xxx",
  "url": "https://mmbiz.qpic.cn/..."
}
```

### 上传临时素材（返回临时 media_id，3天有效）

```
POST https://api.weixin.qq.com/cgi-bin/media/upload
     ?access_token=ACCESS_TOKEN&type=thumb
```

---

## 常见错误码

| 错误码 | 含义 | 解决方案 |
|--------|------|----------|
| 0 | 成功 | — |
| 40001 | Access Token 无效或过期 | 重新获取 Token |
| 40013 | AppID 无效 | 检查 AppID 是否正确 |
| 40125 | AppSecret 无效 | 重置 AppSecret |
| 41001 | 缺少 access_token | 请求 URL 添加 token 参数 |
| 42001 | Access Token 过期 | 重新获取 |
| 45009 | 超过每日调用限额 | 明日重试 |
| 48001 | 接口未授权 | 在公众平台申请相应权限 |
| 50001 | 用户未授权该接口 | 服务号需完成微信认证 |
| 40007 | media_id 无效 | 检查图片是否上传成功，临时素材是否过期 |
| -1 | 系统繁忙 | 稍后重试 |

---

## 开发配置步骤

1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 左侧菜单：**设置与开发 → 基本配置**
3. 获取 **AppID** 和 **AppSecret**（需手机扫码确认）
4. 左侧菜单：**设置与开发 → 接口权限**，确认以下接口已开通：
   - 素材管理 → 新增临时素材
   - 素材管理 → 新增永久素材
   - 草稿箱 → 新建草稿
   - 发布能力 → 发布接口
5. IP 白名单（可选）：如有固定服务器 IP，建议添加白名单

---

## Unsplash API 配置

1. 注册：https://unsplash.com/join
2. 创建 App：https://unsplash.com/oauth/applications
3. 获取 **Access Key**（免费套餐每小时50次请求）
4. Demo 模式下可直接使用，正式上线需申请 Production 权限

**搜索接口：**
```
GET https://api.unsplash.com/search/photos
    ?query=artificial+intelligence
    &per_page=3
    &orientation=landscape
Authorization: Client-ID YOUR_ACCESS_KEY
```
