---
name: wechat-publisher
description: 微信公众号文章发布工具。覆盖微信官方全部发布相关 API：草稿管理、发布管理、素材管理、数据统计、评论管理。纯 Python 标准库实现，零外部依赖。
version: 1.0.7
license: MIT-0
metadata: {"openclaw": {"emoji": "📱", "requires": {"bins": ["python3"], "env": ["WECHAT_APP_ID", "WECHAT_APP_SECRET"]}, "primaryEnv": "WECHAT_APP_ID"}}
--

# 微信公众号文章发布工具

纯 Python stdlib，零外部依赖。覆盖微信官方文档全部发布相关 API。

## 配置

```bash
export WECHAT_APP_ID='your_app_id'
export WECHAT_APP_SECRET='your_app_secret'
export WECHAT_AUTHOR='作者名（可选）'
```

> ⚠️ 2025 年 7 月起，个人主体账号、企业主体未认证账号将被回收发布接口权限。

## 全部命令

```
公众号发布工具 v1.0.7
======================== 草稿管理 ========================
draft create <json>         创建草稿（JSON 支持多图文）
draft get <media_id>        获取草稿详情
draft update <media_id> <json> [--index N]
draft count                 草稿数量
draft list [--offset 0] [--count 20]
draft delete <media_id>

======================== 发布管理 ========================
publish <media_id>          提交发布（返回 publish_id + msg_data_id）
publish status <publish_id> 查询发布状态

======================== 已发布管理 ======================
published list [--offset 0] [--count 20] [--no-content 1]
published delete <article_id>
published getarticle <article_id>  获取已发布图文详情

======================== 素材管理 ========================
material add <file> [--type image|thumb|video] [--title T] [--intro I]
material get <media_id> [--out <file>]
material delete <media_id>
material list [--type image|video|voice|news] [--offset 0] [--count 20]
material update_news <media_id> <json> [--index 0]

======================== 图片上传 ========================
upload <image_path>         上传图片用于正文（返回永久 URL）

======================== 数据统计 ========================
stats summary <begin> <end>
stats total <begin> <end>
stats read <begin> <end>
stats readhour <begin> <end>
stats share <begin> <end>
stats sharehour <begin> <end>
stats userread <begin> <end>
stats userreadhour <begin> <end>

======================== 评论管理 ========================
comment list <msg_data_id> [--index 0] [--begin 0] [--count 50] [--type 0]
comment mark <msg_data_id> --comment_id <id>
comment unmark <msg_data_id> --comment_id <id>
comment delete <msg_data_id> --comment_id <id>
comment reply <msg_data_id> --comment_id <id> --content <text>
comment delreply <msg_data_id> --comment_id <id>

======================== 其他 ============================
render <file> [--style standard|business|minimal|tech|academic|warm]
test                                   测试连接
```

## 多图文草稿示例

```bash
# 创建包含 2 篇图文消息的草稿
cat > articles.json << 'EOF'
[
  {
    "title": "第一篇",
    "author": "作者",
    "content": "<p>正文 HTML</p>",
    "digest": "摘要",
    "thumb_media_id": "MEDIA_ID",
    "need_open_comment": 1
  },
  {
    "title": "第二篇",
    "author": "作者",
    "content": "<p>第二篇正文</p>",
    "thumb_media_id": "MEDIA_ID"
  }
]
EOF

python3 scripts/publish_wechat.py draft create articles.json
```

## 完整工作流

```
内容准备
  ↓
render 命令 → 公众号排版 HTML
  ↓
upload 命令 → 上传正文图片（media/uploadimg）→ 图片 URL
  ↓
material add --type image → 上传封面图（永久素材）→ media_id
  ↓
draft create <json> → 创建草稿 → media_id
  ↓
publish <media_id> → 提交发布 → publish_id + msg_data_id
  ↓
publish status <publish_id> → 确认发布成功
  ↓
published getarticle <article_id> → 查看已发布详情
  ↓
comment list <msg_data_id> → 管理评论
```

## 安全

- Token 仅存内存，不在磁盘持久化
- 所有请求 HTTPS
- 每日 2000 次调用限流内置自动等待
- Token 过期自动刷新并以退避重试
- 错误信息不泄露完整凭据
