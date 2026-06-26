---
name: z-card-image
version: 1.1.0
description: 生成配图、封面图、卡片图、文字海报、公众号文章封面图、微信公众号头图、X 风格帖子分享图、帖子长图、社媒帖子长图。适用于帖子类型数据、post data、social posts、tweet/thread、转发推文、转发帖子、小绿书配图、图片封面、card image。
metadata:
  openclaw:
    requires:
      bins:
        - python3
        - google-chrome
---

# z-card-image

将用户提供的文案渲染成 PNG 卡片图。
支持短文案封面图、长文分页图、X 风格帖子分享长图，以及公众号文章封面图。只要输入是“帖子类型数据”并希望导出成 X 风格长图，都应走 `x-like-posts`。

## 环境要求

- Python 3
- Google Chrome（macOS：`/Applications/Google Chrome.app`；Linux：`chromium` 需修改脚本路径）

## 执行流程

0. **环境提示**（用户触发时检测一次，有问题给提示，不中止流程）：
   - `python3 --version` → 失败则告知：「⚠️ 未检测到 Python 3，渲染可能失败」
   - 检查 Chrome 路径 → 失败则提示安装

1. **识别场景**：
   - 短文案封面图 → `poster-3-4`
   - 长文分页图 → `article-3-4`
   - X 风格帖子分享图 / 帖子长图 / 帖子类型数据 → `x-like-posts`
   - 公众号文章封面图 → `wechat-cover-split`
2. **查模板规则**：根据模板在「模板索引」中找到对应规范文档，读取后按其规则处理文案和参数。**如用户要求高亮：整行用 `--hl1/hl2/hl3`，按词用 `--highlight-words`（逗号分隔），两者可同时使用，不能忽略**
3. **识别平台**：按「平台预设」自动设置配色；推特长图默认使用 Twitter 风格蓝白灰配色
4. **渲染输出**：
   - `poster-3-4` → 执行 `render_card.py`
   - `article-3-4` → 执行 `render_article.py`
   - `x-like-posts` → 执行 `render_x_like_posts.py`
   - `wechat-cover-split` → 执行 `render_card.py`
   - 默认 `--out` 填 `tmp/...png`；如用户指定导出位置，可直接传绝对路径或相对路径
5. **输出产物**：生成 PNG 到指定路径，供后续发送、裁切或复用；如需给外部工具上传，仍应避免写入系统 `/tmp/`

## x-like-posts 导航

`x-like-posts` 用于“帖子类型数据 → X 风格分享长图”。

当命中这条路线时，继续读取：

- [references/x-like-posts.md](references/x-like-posts.md)：输入 JSON 格式、可显示字段、时间规则、导出规则
- [references/tweet-thread.md](references/tweet-thread.md)：旧命名兼容说明

## 输入校验

- **比例不存在**：驳回请求，告知当前支持的比例列表，询问是否新增模板
- **文案超出模板字数上限**：先自动拆分/缩写后再渲染，不要直接塞入
- **帖子过多**：按规范拆成多张 `Part 1 / Part 2`，不要把超长内容强行塞进一张
- **公众号封面标题过长**：先压缩成 2~3 行短标题，再渲染，不能把完整长标题硬塞进模板

## 平台预设

| 平台 | `--footer` | `--bg` | `--highlight` |
|------|-----------|--------|--------------|
| 公众号（默认） | `公众号 · 早早集市` | `#e6f5ef` | `#22a854` |
| 小红书 | `小红书 · 阿康` | `#fdecea` | `#e53935` |

> 用户提到"小红书配图"时使用小红书预设；"小绿书"= 公众号配图，使用公众号预设；否则默认公众号。

## 模板索引

| 模板名 | 比例 | 尺寸 | 用途 | 规范文档 |
|--------|------|------|------|---------|
| `poster-3-4` | 3:4 | 900×1200 | 文字海报（金句/大字报/封面） | [references/poster-3-4.md](references/poster-3-4.md) |
| `article-3-4` | 3:4 | 900×1200 | 长文分页卡片 | [references/article-3-4.md](references/article-3-4.md) |
| `x-like-posts` | 自适应长图 | 900px 宽 | X 风格帖子分享长图 | [references/x-like-posts.md](references/x-like-posts.md) |
| `wechat-cover-split` | 335:100 | 1340×400 | 公众号文章封面长条图（左标题右 icon） | [references/wechat-cover-split.md](references/wechat-cover-split.md) |

## 新增模板

1. 新建 `assets/templates/<name>.html`
2. 在 `render_card.py` 的 `size_map` 里注册尺寸
3. 在上方模板索引中添加一行
4. 创建对应 `references/<name>.md`，记录该模板的参数、字数上限、配图选取规则
