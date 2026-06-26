# 平台 ID 完整表

| 平台 ID | 尺寸 | 用途 |
|---------|------|------|
| `xiaohongshu-v` | 1080×1440 | 小红书竖版 |
| `xiaohongshu-s` | 1080×1080 | 小红书方版 |
| `wechat-cover` | 900×383 | 公众号头图 |
| `wechat-thumb` | 300×300 | 公众号小图 |
| `moments` | 1080×1080 | 朋友圈 |
| `weibo` | 1080×608 | 微博 |
| `toutiao` | 1080×500 | 头条号 |
| `douyin-cover` | 1080×1920 | 抖音封面 |
| `bilibili-cover` | 1920×1080 | B站封面 |
| `twitter` | 1200×675 | Twitter/X |
| `a4` | 2480×3508 (300dpi) | A4 海报 |
| `a3` | 3508×4960 (300dpi) | A3 海报 |

## 用法

```bash
# 指定平台（逗号分隔）
--platforms xiaohongshu-v,wechat-cover

# 全部平台
--platforms all

# 自定义尺寸（不在上表）
--platforms custom:800x600
```

## 默认输出（不传 --platforms）

当 `--platforms` 没传时，生成 5 种通用比例：
- 3:4 竖版 (1080×1440)
- 1:1 方版 (1080×1080)
- 16:9 横版 (1920×1080)
- 2.35:1 封面 (1800×766)
- 1.9:1 OG 卡片 (1200×630)
