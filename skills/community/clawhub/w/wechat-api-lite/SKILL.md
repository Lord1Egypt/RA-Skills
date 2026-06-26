---
name: wechat-api-lite
description: 微信公众号 API 轻量化工具 — 凭证获取、素材上传、草稿创建，主打最小化依赖和零冗余
triggers:
  - "公众号 API"
  - "微信发布"
  - "创建草稿"
  - "上传素材"
  - "wechat api"
---

# WeChat API Lite

微信公众号 API 轻量化工具。只保留发布图文必需的功能：token 获取、封面图上传、正文图片上传、草稿创建。无多余命令，无依赖膨胀。

---

## 凭证配置

复制示例文件并填入真实值：

```bash
SKILL_DIR="$HOME/.hermes/skills/wechat-api-lite"
cp "$SKILL_DIR/config.env.example" "$SKILL_DIR/config.env"
# 编辑 config.env，填入 AppID 和 AppSecret
```

> AppID 和 AppSecret 获取：[微信公众平台](https://mp.weixin.qq.com) → 设置与开发 → 基本配置

---

## 核心命令

### token — 获取 access_token

有效期 7200 秒，脚本内自动缓存 + 提前刷新。

```bash
python3 $HOME/.hermes/skills/wechat-api-lite/scripts/wechat_api.py token
```

---

### upload-thumb — 上传封面图

返回 `thumb_media_id`，用于创建草稿时指定封面。

```bash
python3 $HOME/.hermes/skills/wechat-api-lite/scripts/wechat_api.py upload-thumb <文件路径>
# 示例
python3 $HOME/.hermes/skills/wechat-api-lite/scripts/wechat_api.py upload-thumb ~/hermes/research/Cover.png
```

> 封面图推荐尺寸：900 × 383 px（2.35:1 宽屏），PNG/JPG，不超过 2MB。

---

### upload-image — 上传正文图片

返回 `media_id` + `url`，在正文 HTML 中用 `url` 嵌入图片。

```bash
python3 $HOME/.hermes/skills/wechat-api-lite/scripts/wechat_api.py upload-image <文件路径>
```

---

### create-draft — 创建图文草稿

```bash
python3 $HOME/.hermes/skills/wechat-api-lite/scripts/wechat_api.py create-draft ~/hermes/research/draft.json
```

**draft.json 格式：**

```json
[
  {
    "title": "文章标题（不超过32字）",
    "author": "作者名",
    "digest": "摘要",
    "content": "<p>HTML 格式正文...</p>",
    "thumb_media_id": "upload-thumb 返回的 ID",
    "show_cover_pic": 1,
    "need_open_comment": 1,
    "only_fans_can_comment": 0
  }
]
```

成功输出：`✅ 草稿创建成功: media_id=XXXXXXXXXXXXXXXX`

---

### draft-list — 查看草稿数量

```bash
python3 $HOME/.hermes/skills/wechat-api-lite/scripts/wechat_api.py draft-list
```

---

## 完整发布流程（wechat-post + wechat-api-lite 配合）

```
1. wechat-post 生成 Markdown 正文
         ↓
2. 将 Markdown 转为 HTML，写入 draft.json
         ↓
3. wechat-api-lite upload-thumb（上传封面 → thumb_media_id）
         ↓
4. wechat-api-lite create-draft（创建草稿 → media_id）
         ↓
5. 登录 mp.weixin.qq.com 草稿箱 → 预览 → 发布
```

---

## 草稿字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `title` | ✅ | 标题，不超过 32 字符 |
| `author` | 否 | 作者名，不超过 16 字 |
| `digest` | 否 | 摘要，默认取正文前 54 字 |
| `content` | ✅ | HTML 格式正文 |
| `thumb_media_id` | ✅ | 封面图 ID（来自 upload-thumb） |
| `show_cover_pic` | 否 | 是否在正文显示封面（0/1） |
| `need_open_comment` | 否 | 是否打开评论（0/1） |
| `only_fans_can_comment` | 否 | 是否仅粉丝可评论（0/1） |

---

## 已知问题 & API 行为

### access_token 过期（40001）

token 过期后所有 API 调用均失败。清除缓存后重试：

```bash
rm ~/.hermes/skills/wechat-api-lite/scripts/.token_cache
python3 $HOME/.hermes/skills/wechat-api-lite/scripts/wechat_api.py upload-thumb ...
```

### 成功响应无 errcode

以下接口成功时不返回 `errcode`，判断成功仅看业务字段是否存在：

| 接口 | 成功判断依据 |
|------|-------------|
| `draft/add`（创建草稿） | `"media_id" in result` |
| `draft/count`（草稿数量） | `"total_count" in result` |

### url vs media_id

- **正文 HTML 图片** → 用 `upload-image` 返回的 `url`
- **草稿封面图** → 用 `upload-thumb` 返回的 `media_id`

两者不可混用。

### ⚠️ 草稿正文图注位置注意

在 JSON 中写 HTML 正文时，如果要给配图加 caption 注释，**caption 必须紧跟在对应的 `<img>` 标签后面**，不要写在正文开头或其他位置。公众号渲染会把 caption 放在图片在正文中出现的相对位置，误放在文章顶部会导致 caption 跑到文章最下方显示。

- **正文 HTML 图片** → 用 `upload-image` 返回的 `url`
- **草稿封面图** → 用 `upload-thumb` 返回的 `media_id`

两者不可混用。

---

## 注意事项

- access_token 有效期 2 小时，脚本自动维护缓存，过期后手动清缓存重刷
- 永久素材有总量限制，缩略图不超过 2MB
- 封面图推荐 900 × 383 px，正文图片宽度建议 ≤ 1080px
- 草稿创建后在 [mp.weixin.qq.com](https://mp.weixin.qq.com) 草稿箱查看和编辑
