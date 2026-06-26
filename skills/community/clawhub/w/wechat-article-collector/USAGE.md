# 通用网页文章采集器

支持参数化配置，可采集任意网站的文章列表。

## 快速开始

### 1. 使用预设配置

```bash
# 微信公众号（默认）
python3 scripts/collect_articles.py

# 知乎专栏
python3 scripts/collect_articles.py --profile zhihu_column --url "https://www.zhihu.com/people/username/posts"

# 掘金
python3 scripts/collect_articles.py --profile juejin --url "https://juejin.cn/user/123456/posts"
```

### 2. 自定义网站

#### 方式 1：修改配置文件

编辑 `config.json`，在 `profiles` 中添加新配置：

```json
{
  "profiles": {
    "my_blog": {
      "name": "我的博客",
      "list_url": "https://myblog.com/posts",
      "selectors": {
        "article_row": ".post-item",
        "title": ".post-title",
        "date": ".post-date",
        "link": ".post-title a",
        "next_page": ".pagination .next"
      },
      "content_selectors": [
        ".post-content",
        "article"
      ],
      "wait_after_load": 2,
      "need_login": false
    }
  }
}
```

然后运行：

```bash
python3 scripts/collect_articles.py --profile my_blog
```

#### 方式 2：使用自定义 JSON 文件

创建 `my_site.json`：

```json
{
  "selectors": {
    "article_row": ".article",
    "title": "h2.title",
    "date": ".date",
    "link": "a.link",
    "next_page": ".next-page"
  },
  "content_selectors": [
    ".article-body",
    "article"
  ]
}
```

运行：

```bash
python3 scripts/collect_articles.py --custom-selectors my_site.json --url "https://example.com/articles"
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--profile` | 使用预设配置 | `--profile zhihu_column` |
| `--url` | 文章列表页 URL | `--url "https://example.com/posts"` |
| `--save-dir` | 保存目录 | `--save-dir ~/Documents/articles` |
| `--custom-selectors` | 自定义选择器 JSON | `--custom-selectors my_site.json` |

## 选择器配置

### 必需字段

| 字段 | 说明 | CSS 选择器示例 |
|------|------|----------------|
| `article_row` | 文章列表项 | `.post-item`, `tr`, `.article` |
| `title` | 标题元素 | `.title`, `h2`, `td:nth-child(1)` |
| `link` | 链接元素 | `a`, `.title a` |

### 可选字段

| 字段 | 说明 | CSS 选择器示例 |
|------|------|----------------|
| `date` | 日期元素 | `.date`, `time`, `td:nth-child(2)` |
| `next_page` | 下一页按钮 | `.next`, `.pagination .next` |

### 内容选择器

`content_selectors` 是一个数组，按优先级尝试：

```json
{
  "content_selectors": [
    "#article-content",    // 优先尝试
    ".post-body",          // 次选
    "article",             // 再次
    ".content"             // 最后
  ]
}
```

## 使用场景

### 场景 1：采集微信公众号（需登录）

```bash
# 1. 在 Chrome 中登录微信公众号后台
# 2. 进入原创文章页面
# 3. 运行采集
python3 scripts/collect_articles.py
```

### 场景 2：采集知乎专栏（无需登录）

```bash
python3 scripts/collect_articles.py \
  --profile zhihu_column \
  --url "https://www.zhihu.com/people/username/posts"
```

### 场景 3：采集自定义博客

```bash
# 1. 在 Chrome 中打开博客文章列表页
# 2. 按 F12 打开开发者工具
# 3. 找到文章列表的 CSS 选择器
# 4. 创建配置文件或使用 --custom-selectors
python3 scripts/collect_articles.py \
  --custom-selectors my_blog.json \
  --url "https://myblog.com/posts"
```

### 场景 4：采集需要登录的网站

```bash
# 1. 在 Chrome 中登录目标网站
# 2. 打开文章列表页
# 3. 运行采集（Browser Harness 会使用已登录的 session）
python3 scripts/collect_articles.py \
  --profile custom \
  --custom-selectors my_site.json
```

## 如何找到正确的选择器

### 方法 1：Chrome 开发者工具

1. 打开目标网页
2. 按 `F12` 打开开发者工具
3. 点击左上角的"选择元素"图标
4. 点击页面上的文章标题
5. 在 Elements 面板中右键 → Copy → Copy selector

### 方法 2：使用 Browser Harness 测试

```bash
printf 'print(js("document.querySelectorAll(\\".post-item\\").length"))\n' | browser-harness
```

### 方法 3：逐步调试

```bash
# 测试文章列表项
printf 'items = js("Array.from(document.querySelectorAll(\\".post\\")).map(el => el.textContent.slice(0, 50))")\nprint(items)\n' | browser-harness

# 测试标题提取
printf 'titles = js("Array.from(document.querySelectorAll(\\".post .title\\")).map(el => el.textContent)")\nprint(titles)\n' | browser-harness
```

## 预设配置

### 微信公众号 (`wechat_mp`)

```json
{
  "list_url": "https://mp.weixin.qq.com/cgi-bin/appmsgcopyright?action=orignal&type=1",
  "selectors": {
    "article_row": "tr",
    "title": "td:nth-child(1)",
    "date": "td:nth-child(2)",
    "link": "a",
    "next_page": "a.page_next:not(.page_disabled)"
  },
  "content_selectors": ["#js_content", ".rich_media_content"],
  "need_login": true
}
```

### 知乎专栏 (`zhihu_column`)

```json
{
  "list_url": "https://www.zhihu.com/people/{username}/posts",
  "selectors": {
    "article_row": ".ArticleItem",
    "title": ".ContentItem-title a",
    "date": ".ContentItem-time",
    "link": ".ContentItem-title a",
    "next_page": ".Pagination-next"
  },
  "content_selectors": [".Post-RichTextContainer", ".RichText"],
  "need_login": false
}
```

### 掘金 (`juejin`)

```json
{
  "list_url": "https://juejin.cn/user/{user_id}/posts",
  "selectors": {
    "article_row": ".entry",
    "title": ".title",
    "date": ".date",
    "link": ".title a",
    "next_page": ".next-page"
  },
  "content_selectors": [".markdown-body", "article"],
  "need_login": false
}
```

## 故障排查

### 问题 1：提取不到文章

**症状**：`✅ 提取到 0 篇文章`

**原因**：选择器不正确

**解决**：

1. 用 Chrome 开发者工具检查实际的 HTML 结构
2. 更新 `selectors` 配置
3. 用 Browser Harness 测试选择器

### 问题 2：内容提取失败

**症状**：`❌ 下载失败`

**原因**：`content_selectors` 不匹配

**解决**：

1. 打开单篇文章页面
2. 找到正文容器的 CSS 选择器
3. 更新 `content_selectors` 数组

### 问题 3：翻页失败

**症状**：只提取到第一页

**原因**：`next_page` 选择器不正确

**解决**：

1. 检查"下一页"按钮的 CSS 选择器
2. 确保选择器能匹配到可点击的元素
3. 注意禁用状态的按钮（如 `.next:not(.disabled)`）

## 高级用法

### 批量采集多个网站

```bash
#!/bin/bash
sites=(
  "wechat_mp"
  "zhihu_column"
  "juejin"
)

for site in "${sites[@]}"; do
  echo "采集 $site..."
  python3 scripts/collect_articles.py --profile "$site"
  sleep 5
done
```

### 定时采集

```bash
# 添加 cron 任务
0 2 * * * cd ~/.openclaw/workspace/skills/wechat-article-collector && python3 scripts/collect_articles.py --profile wechat_mp
0 3 * * * cd ~/.openclaw/workspace/skills/wechat-article-collector && python3 scripts/collect_articles.py --profile zhihu_column --url "https://www.zhihu.com/people/myusername/posts"
```

## 许可

MIT License
