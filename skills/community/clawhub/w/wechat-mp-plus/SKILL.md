# Skill: wechat-mp-publisher

微信公众号自动化管理。支持草稿发布、菜单管理、自动回复查询、Markdown排版。

## Triggers

- "发布公众号文章", "微信公众号", "公众号草稿", "公众号菜单"
- "wechat mp", "publish article", "mp draft"

## Prerequisites

- 环境变量 `WECHAT_MP_APP_ID` 和 `WECHAT_MP_APP_SECRET`，或 `.secrets/wechat_mp.env` 文件
- Python 3.7+

## Usage

所有脚本位于 `scripts/` 目录。工作目录应为 skill 根目录。

### 一键发布（最常用）

输入一个 Markdown 文件 + 封面图 → 自动完成图片上传、HTML转换、创建草稿。

```bash
cd skills/wechat-mp-publisher
python3 scripts/publish.py <markdown文件> <封面图> <标题> [作者] [摘要] [主题]
```

主题可选：`default`（清爽简约）、`elegant`（文艺范）、`dark`（暗色科技）

### 草稿管理

```bash
# 获取Token（测试连通性）
python3 scripts/wechat_mp.py token

# 上传图片素材（永久）
python3 scripts/wechat_mp.py upload <图片路径>

# 上传文内图片
python3 scripts/wechat_mp.py upload-article-image <图片路径>

# 创建草稿
python3 scripts/wechat_mp.py draft-create '{"title":"标题","author":"作者","content":"<p>内容HTML</p>","thumb_media_id":"xxx","digest":"摘要"}'

# 列出草稿
python3 scripts/wechat_mp.py draft-list [offset] [count]

# 删除草稿
python3 scripts/wechat_mp.py draft-delete <media_id>
```

### 菜单管理

```bash
# 查询菜单
python3 scripts/menu.py get

# 创建菜单
python3 scripts/menu.py create '{"button":[{"type":"view","name":"官网","url":"https://example.com"}]}'

# 删除菜单
python3 scripts/menu.py delete
```

### 自动回复查询

```bash
python3 scripts/wechat_mp.py autoreply
```

### Markdown转HTML

```bash
python3 scripts/md2html.py <markdown文件> [主题名]
```

## Notes

- Token自动缓存2小时，无需手动管理
- 所有API错误有中文提示
- 图片支持永久素材上传和文内图片上传两种模式
