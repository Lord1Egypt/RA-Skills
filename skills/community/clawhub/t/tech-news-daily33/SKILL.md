# tech-news-daily

科技资讯日报生成 Skill：从 IT之家 + 快科技 抓取内容，生成带 iOS 液态玻璃风格的 HTML 日报。

## 工作流程

1. **抓取数据**（RSS + 文章页）
   - IT之家 RSS：`https://www.ithome.com/rss/`
   - 快科技列表页：`https://news.mydrivers.com/`（需按日期过滤 1113 开头链接）
   - 每条资讯获取：标题、正文、来源、图片 URL

2. **整理数据**（JSON 格式）
   ```json
   [
     ["key", "cat_id", "title", "src", "url", "text"],
     ...
   ]
   ```
   - cat_id: 1=手机/硬件, 2=AI/大模型, 3=汽车, 4=科技大厂, 5=系统App
   - text 需做 CJK+ASCII 空格处理：`re.sub(r'([\u4e00-\u9fff])([A-Za-z0-9])', r'\1 \2', s)`

3. **下载图片**
   - 目录：`news_imgs_today/`
   - 文件名：`{key}.jpg` 或 `{key}.png`
   - base64 内嵌到 HTML

4. **生成 HTML**
   ```bash
   python scripts/gen_html.py
   ```
   - 输出：`tech_news_YYYYMMDD.html`
   - iOS 液态玻璃风格：毛玻璃卡片 + 四色渐变背景
   - **正文完整展开，无截断**
   - **图片按原始比例完整显示**

## 数据格式

每条资讯为 6 字段数组：
- `[0]` key：唯一标识（英文，用于本地图片文件名）
- `[1]` cat_id：板块 ID（1-5）
- `[2]` title：标题
- `[3]` src：来源名称（如 "IT之家"、"快科技"）
- `[4]` url：文章链接
- `[5]` text：正文摘要（完整不截断，中英/数字之间有空格）

参考：`references/data_format.md`

## 设计规范

- iOS 26 液态玻璃风格
  - `backdrop-filter: blur(24px) saturate(180%)`
  - 背景 `rgba(255,255,255,0.62)` + 白色边框
  - 悬停上浮 spring 动画
  - 四色渐变背景（蓝→紫→绿→粉）
- 标题：完整显示，不截断
- 正文：完整展开，无 `-webkit-line-clamp` 限制
- 图片：`width:100%; height:auto`，原始比例完整展示
- 三栏自适应网格布局
