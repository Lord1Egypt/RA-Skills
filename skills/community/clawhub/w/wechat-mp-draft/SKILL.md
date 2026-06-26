---
name: wechat-mp-draft
description: 代写微信公众号文章并保存到公众号草稿箱。使用场景：用户需要撰写公众号文章并直接发布到微信公众号后台草稿箱。触发词："写公众号文章"、"保存到公众号草稿"、"微信文章"、"公众号发文"。
---

# 微信公众号草稿 Skill

代写微信公众号文章并保存到草稿箱。

## 前置条件

需要以下凭证（需自行配置）：
- AppID: `wxYOUR_APPID_HERE`
- AppSecret: `YOUR_SECRET_HERE`

**获取方式：** 微信公众平台 → 设置与开发 → 基本配置

**重要：** 服务器 IP 必须添加到公众号后台的 IP 白名单中。

## 工作流程

### 1. 获取 Access Token

```bash
./scripts/get_access_token.sh
```

### 2. 上传封面图片（获取 thumb_media_id）

**封面图片是必填项！**

```bash
./scripts/upload_image.sh <access_token> <图片路径>
```

返回示例：
```json
{"media_id":"xxx","url":"http://mmbiz.qpic.cn/..."}
```

### 3. 撰写文章并保存到草稿箱

```bash
./scripts/add_draft.sh <access_token> <标题> <HTML内容> <thumb_media_id> [作者] [摘要]
```

## 关键问题与解决方案

### ❌ 问题 1：40007 invalid media_id

**原因：** 
- `thumb_media_id` 是必填字段
- 封面图片必须是**永久素材**（通过 `add_material` 接口上传）

**解决：**
必须先上传封面图片获取 `thumb_media_id`：
```bash
curl -F "media=@cover.jpg" "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=TOKEN&type=image"
```

### ❌ 问题 2：IP 不在白名单（40164）

**解决：**
登录微信公众平台 → 设置与开发 → 基本配置 → IP白名单 → 添加服务器 IP

### ❌ 问题 3：HTML 内容格式错误

**解决：**
- HTML 中的换行符会导致 JSON 解析失败
- 必须将换行符替换为空格
- 使用 `tr '\n' ' '` 处理

## 完整使用示例

```bash
# 1. 获取 token
TOKEN=$(./scripts/get_access_token.sh | jq -r '.access_token')

# 2. 上传封面图
THUMB_RESPONSE=$(./scripts/upload_image.sh "$TOKEN" /path/to/cover.jpg)
THUMB_ID=$(echo "$THUMB_RESPONSE" | jq -r '.media_id')

# 3. 准备文章内容（HTML 格式）
CONTENT='<p>这里是文章内容...</p>'

# 4. 保存草稿
./scripts/add_draft.sh "$TOKEN" "文章标题" "$CONTENT" "$THUMB_ID" "作者" "摘要"
```

## API 参数说明

### 新增草稿必填字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| title | string | 是 | 标题，不超过32字 |
| content | string | 是 | HTML内容，不超过2万字符 |
| thumb_media_id | string | 是 | 封面图片永久素材ID |
| author | string | 否 | 作者，不超过16字 |
| digest | string | 否 | 摘要，不超过128字 |
| show_cover_pic | number | 否 | 是否显示封面，0/1 |
| need_open_comment | number | 否 | 是否打开评论，0/1 |
| only_fans_can_comment | number | 否 | 是否仅粉丝可评论，0/1 |

### 支持的 HTML 标签

- `<p>` - 段落
- `<br>` - 换行
- `<section>` - 区块
- `<img>` - 图片（需先上传获取 media_id）
- `<strong>`, `<b>` - 加粗
- `<span style="...">` - 带样式的文本
- `<a href="...">` - 链接
- `<h1>`-`<h6>` - 标题

## 错误码速查

| 错误码 | 说明 | 解决 |
|--------|------|------|
| 40001 | access_token 过期 | 重新获取 |
| 40007 | media_id 无效 | 检查封面图是否上传正确 |
| 40164 | IP 不在白名单 | 添加 IP 到白名单 |
| 44002 | POST 数据为空 | 检查请求体 |
| 47001 | 数据格式错误 | 检查 JSON 格式 |

## 注意事项

1. **token 有效期 2 小时**，过期需重新获取
2. **封面图必须先上传**，不能直接引用外部 URL
3. **HTML 内容需转义**，避免 JSON 解析失败
4. **IP 白名单必须配置**，否则无法调用 API
5. **内容大小限制**：正文 < 2万字符，< 1MB

## 文件结构

```
wechat-mp-draft/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── get_access_token.sh     # 获取 token
│   ├── upload_image.sh         # 上传封面图片
│   └── add_draft.sh            # 保存草稿
└── references/
    └── api_reference.md        # API 详细文档
```
