# 微信公众号草稿 API 参考

## 前置条件

| 条件 | 说明 |
|------|------|
| 公众号类型 | 订阅号/服务号均可，草稿接口无类型限制 |
| AppID + AppSecret | 在公众平台后台「开发 → 基本配置」获取 |
| IP 白名单 | 若调用方 IP 不在白名单，需先添加（公众平台 → 开发 → 基本配置 → IP白名单） |
| 接口权限 | 草稿箱接口默认开放，无需额外申请 |

## 核心接口

### 1. 获取 Access Token
```
GET https://api.weixin.qq.com/cgi-bin/token
    ?grant_type=client_credential
    &appid=APPID
    &secret=APPSECRET
```
- 有效期 7200 秒（2 小时），每日调用上限 2000 次
- 返回示例：`{"access_token":"xxx","expires_in":7200}`

### 2. 上传永久图片素材（封面用）
```
POST https://api.weixin.qq.com/cgi-bin/material/add_material
    ?access_token=ACCESS_TOKEN
    &type=image
```
- Content-Type: multipart/form-data
- form 字段：`media`（图片文件）
- 支持格式：JPG/PNG/GIF
- 图片建议尺寸：900×500 px，大小 ≤ 10 MB
- 返回：`{"media_id":"xxx","url":"https://..."}`

### 3. 新建草稿
```
POST https://api.weixin.qq.com/cgi-bin/draft/add
    ?access_token=ACCESS_TOKEN
```
请求体（JSON）：
```json
{
  "articles": [{
    "title": "文章标题",
    "author": "作者（可选）",
    "digest": "摘要，最多120字（可选）",
    "content": "正文HTML（必填）",
    "thumb_media_id": "封面图 media_id（必填）",
    "need_open_comment": 0,
    "only_fans_can_comment": 0
  }]
}
```
- 返回：`{"media_id":"草稿media_id"}`
- 一次最多 8 篇文章

## 常见错误码

| errcode | 含义 | 解决方法 |
|---------|------|---------|
| 40001 | access_token 无效/过期 | 重新获取 token |
| 40164 | IP 不在白名单 | 添加当前 IP 到公众平台白名单 |
| 45009 | 接口调用超限 | 降低调用频率 |
| 40007 | media_id 无效 | 检查封面图是否上传成功 |
| 47001 | 解析 JSON/XML 错误 | 检查请求体格式 |

## HTML 内容规范（微信公众号）

- 使用**内联样式**（`style="..."`），不支持外部 CSS
- 图片需先上传到素材库，使用微信 CDN 地址
- 不支持 `<script>`、`<iframe>` 等标签
- 推荐字体：`-apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif`
- 推荐行高：`line-height: 1.8`
- 微信绿色：`#07C160`
