# 微信公众号草稿 API 参考

## 接口列表

| 接口 | 路径 | 说明 |
|------|------|------|
| 获取 Access Token | `/cgi-bin/token` | 获取接口调用凭证 |
| 上传永久素材 | `/cgi-bin/material/add_material` | 上传封面图片等素材 |
| 新增草稿 | `/cgi-bin/draft/add` | 保存文章到草稿箱 |
| 获取草稿列表 | `/cgi-bin/draft/batchget` | 获取草稿列表 |
| 删除草稿 | `/cgi-bin/draft/delete` | 删除指定草稿 |

---

## 获取 Access Token

**请求：**
```
GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
```

**返回：**
```json
{
  "access_token": "ACCESS_TOKEN",
  "expires_in": 7200
}
```

---

## 上传永久素材

**请求：**
```
POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=ACCESS_TOKEN&type=image
Content-Type: multipart/form-data

media: 图片文件
```

**返回：**
```json
{
  "media_id": "MEDIA_ID",
  "url": "http://mmbiz.qpic.cn/..."
}
```

---

## 新增草稿

**请求：**
```
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN
Content-Type: application/json
```

**请求体：**
```json
{
  "articles": [
    {
      "title": "标题",
      "author": "作者",
      "digest": "摘要",
      "content": "HTML内容",
      "thumb_media_id": "封面图片media_id",
      "show_cover_pic": 1,
      "need_open_comment": 1,
      "only_fans_can_comment": 0
    }
  ]
}
```

**返回：**
```json
{
  "media_id": "DRAFT_MEDIA_ID"
}
```

---

## 字段说明

### 文章字段

| 字段 | 类型 | 必填 | 限制 | 说明 |
|------|------|------|------|------|
| title | string | 是 | ≤32字 | 标题 |
| content | string | 是 | ≤2万字符, <1MB | HTML正文 |
| thumb_media_id | string | 是 | - | 封面图永久素材ID |
| author | string | 否 | ≤16字 | 作者名 |
| digest | string | 否 | ≤128字 | 摘要（单图文） |
| show_cover_pic | number | 否 | 0/1 | 是否显示封面 |
| need_open_comment | number | 否 | 0/1 | 是否打开评论 |
| only_fans_can_comment | number | 否 | 0/1 | 仅粉丝评论 |

---

## 错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 40001 | access_token 过期或无效 | 重新获取 |
| 40002 | token 错误 | 检查 token 是否正确 |
| 40007 | media_id 无效 | 检查封面图是否正确上传 |
| 40013 | appid 无效 | 检查 AppID |
| 40164 | IP 不在白名单 | 添加 IP 到白名单 |
| 44002 | POST 数据为空 | 检查请求体 |
| 47001 | 数据格式错误 | 检查 JSON 格式 |

---

## HTML 标签支持

### 支持的标签

- `<p>` - 段落
- `<br>` - 换行
- `<section>` - 区块
- `<div>` - 容器
- `<img>` - 图片（需先上传获取 media_id）
- `<strong>`, `<b>` - 加粗
- `<em>`, `<i>` - 斜体
- `<span style="...">` - 行内样式
- `<a href="...">` - 链接
- `<h1>`-`<h6>` - 标题
- `<ul>`, `<ol>`, `<li>` - 列表

### 支持的 CSS 属性

- `color` - 文字颜色
- `font-size` - 字体大小
- `text-align` - 对齐方式
- `margin`, `padding` - 间距
- `background-color` - 背景色
- `border` - 边框

---

## 注意事项

1. **thumb_media_id 必填**：封面图片必须通过 `add_material` 接口上传获取
2. **HTML 转义**：content 中的特殊字符需要转义
3. **换行处理**：JSON 中不能包含原始换行符，需替换为空格
4. **图片限制**：正文中图片需使用永久素材 media_id
5. **频率限制**：注意接口调用频率，避免被封
