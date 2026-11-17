---
name: weread-timeline-wall
description: 微信读书轨迹墙生成器。拉取账号"带笔记书目"（含封面），生成单文件 HTML 阅读轨迹墙：按月分组、封面网格、分类彩标、划线统计。支持全页长截图（已内置懒加载/粘性页头/分段拼接三个坑的解法）与离线 JSON 模式。
---

# 微信读书轨迹墙 (weread-timeline-wall)

一条命令生成"点开就能看"的个人阅读轨迹网页：**封面墙 + 月份时间线 + 分类标签 + 划线统计**，单文件 HTML，双击即看。

## 使用

```bash
# 0) 依赖（一次性）
pip install -r scripts/requirements.txt
playwright install chromium

# 1) 首次扫码登录
python scripts/weread_wall.py --login

# 2) 生成轨迹墙
python scripts/weread_wall.py --out weread_timeline.html

# 追加全页长截图
python scripts/weread_wall.py --out weread_timeline.html --screenshot wall.png

# 离线模式：用之前导出的 JSON 重新生成（不打开浏览器）
python scripts/weread_wall.py --from-json books.json --out wall.html

# 顺手导出书目 JSON 供离线复用
python scripts/weread_wall.py --save-json books.json
```

## 效果

- 深色单文件页面，顶部统计栏：有笔记的书 / 已读完 / 累计划线 / 今年活跃
- 2026 年内按**月**分组、更早按年分组，倒序时间线
- 每本书：真实封面 + 一级分类彩色标签 + ✓读完标记 + 划线条数 + 最近翻动时间，点击跳微信读书搜索

## 数据口径

- 来源：`/api/user/notebook`（**带笔记的书目**——纯读不划的书不在内），需登录态
- 时间用 `sort` 字段 = 最近一次活动时间（最近翻动/划线），不是"开始阅读"时间
- 封面从微信读书 CDN 加载，查看网页需联网

## 全页长截图的三个坑（已内置解法）

1. **懒加载**：封面 `loading=lazy`，直接截全页下半页全是灰框 → 强制 `eager` 并等待全部 `complete`
2. **粘性页头**：`position:sticky + backdrop-filter` 会让 Chromium 分段截图出现重复贴片 → 截图前改为 `static`
3. **fullPage 不可靠**：超高页面（>10000px）Chromium 自带 fullPage 会把顶部内容重复平铺 → 手动按视口高度分段滚动截图 + Pillow 拼接

## 账号安全

只读一个接口（`/api/user/notebook`），零写入、零注入、零第三方窗口。

## 免责

仅限本人账号数据、本地自用。自动化有理论风险，建议小号。
