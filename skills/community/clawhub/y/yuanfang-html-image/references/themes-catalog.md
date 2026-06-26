# 12 主题完整目录

agent 在 Step 2 推荐主题时备查。详细视觉特征：

| # | 主题 | 底色 | 主色 | 视觉特征 | 适合 |
|--:|------|------|------|---------|------|
| 01 | minimal-white | `#FFFFFF` | `#5856E9` | 左侧内容+右侧 Indigo 装饰块, 品牌色驱动 | 品牌通用、教程、干货 |
| 02 | dark-gold | #1A1A2E | #E2B714 | 对角分割+装饰圆, 渐变金字, 磨砂纹理 | 重磅消息、产品发布 |
| 03 | editorial | #F5F0EB | #C0392B | 大引号+顶部分隔线, 红色点缀 | 深度分析、访谈 |
| 04 | warm-handdrawn | #FDF6EC | #D97706 | 纸纹底+手绘下划线, 胶带装饰, 星星标记 | 个人故事、生活 |
| 05 | tech-modern | #0F172A | #4FACFE | 终端点数+网格底, 代码注释前缀, 发光点缀 | AI/科技、数码 |
| 06 | bold-poster | #000000 | #FF3355 | 对角大幅红色色块, 超大字体 | 金句引爆、活动 |
| 07 | data-infographic | #F8FAFC | #10B981 | 数据卡片+进度条, 线图装饰 | 排行、报告、数据 |
| 08 | eastern | #F7F3EE | #8D6E63 | 水墨晕染+竖排标题, 印章/竹线装饰 | 文化、哲思、诗词 |
| 09 | magazine-cover | #F5F0EB | #4F46E5 | 全出血版式, 超大标题居中, 右下角品牌标签 | 精品文章、封面故事 |
| 10 | split-screen | #FFFFFF | #4F46E5 | 左右双色背景, 一侧品牌色一侧留白 | 对比/双语/产品展示 |
| 11 | minimal-white-editorial | #FAFAFA | #4F46E5 | 超多留白, 精致小字, 瑞士风排版 | 高端品牌、艺术、设计 |
| 12 | list-ranking | #FFFFFF | #4F46E5 | 编号列表, 大号数字标记, 底部品牌条 | 排行榜、Top 10、步骤流程 |

## 内容类型 → 主题推荐

```
干货/教程 → minimal-white / data-infographic / list-ranking
重磅消息 → dark-gold / bold-poster / magazine-cover
深度分析 → editorial / eastern / magazine-cover
个人故事 → warm-handdrawn / minimal-white-editorial
科技资讯 → tech-modern / split-screen / minimal-white-editorial
```

## 主题文件位置

```
yuanfang-design/themes/<theme-name>.css
```

每个主题是一个独立的 CSS 文件，override `base.css` 的 token。添加新主题：复制 `themes/_template.css`，覆盖 token，测试，更新 showcase。
