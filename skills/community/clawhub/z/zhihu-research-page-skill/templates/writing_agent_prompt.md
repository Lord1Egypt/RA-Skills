{topic}
{chapter_title}
{chapter_points}
{chapter_urls}

./other/_draft_ch_{chapter_id}.html

文件有效中文字数必须 ≥11,000。写完后运行独立验收脚本：
python scripts/wordcount_check.py ./other/_draft_ch_{chapter_id}.html
结果 ≥11,000 且与自述差 ≤5% 才算完成，否则扩写。

只写一个 <article class="zh-card zh-answer"> 片段，不要写 <html>/<head>/<body>。
严禁内嵌 <style> 块——骨架已通过 css-template.css 提供全部样式。
结构：作者块 + <div class="zh-answer__body"> + 操作条。

作者块（统一模板，头像 URL 由阶段 4.5 配置，直接填入，不自行编造）：
见 templates/author_block.html

章节内所有图片引用本地 ./images/ 路径：<img src="./images/xxx.png" alt="说明">。禁止外链。

正文用 <h3> 大节、<h4> 小节、<p> 段落、<table> 对比表。
<blockquote> 引用重点。文末附操作条（赞/评论/喜欢/收藏/分享）。

<code> 标签规范：代码块用 <pre><code>，不单独 <code> 包裹多行。
不与 <strong> 混用。不在 <code> 内嵌套块级标签（<p>/<table>/<h3>）。

写作风格：知乎回答体，口语化、大量生活类比、少堆术语。
目标读者：零专业基础初学者。每节先给生活类比再展开技术细节。

链接规则：只用已核验来源池中的 URL 或知名官网根域名。
严禁编造任何 URL。宁可不加链接也不要编。
存疑信息标注"以官方最新资料为准"。
