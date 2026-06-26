---
name: wx-tabbar-icons
description: |
  微信小程序底部 TabBar 图标生成技能。用 Python PIL 生成简约几何风格的 tab 图标
  （未选中灰色 + 选中绿色），并自动写入 app.json 的 tabBar 配置。
  当用户说"生成 tabBar 图标"、"底部菜单栏图标"、"tab 图标"时使用本技能。
---

# 微信小程序 TabBar 图标生成

## 功能

为微信小程序项目生成底部 TabBar 图标，包括：
1. 用 Python PIL 绘制每个 tab 的几何图形图标（81×81 px PNG，透明背景）
2. 每个 tab 生成 2 张：未选中（灰色）+ 选中（主题色）
3. 输出到小程序项目的 `images/` 目录
4. 自动更新 `app.json` 的 tabBar 配置，补上 `iconPath` / `selectedIconPath`

## 前置条件

- Python 3 + Pillow (`pip install pillow`)
- 已知小程序项目路径和 `app.json` 中的 tabBar 配置

## 工作流程

### Step 1：读取 app.json

读取小程序项目的 `app.json`，提取 tabBar.list 中每个 tab 的：
- `pagePath`：用于推断 tab 用途
- `text`：tab 文字，用于匹配图标类型

### Step 2：匹配图标类型

根据 tab 的 `text` 或 `pagePath` 自动匹配图标类型。优先按 text 关键词匹配，
无法匹配的 tab 向用户确认。

#### 内置图标库

| 图标ID | 图形描述 | 匹配关键词 |
|--------|---------|-----------|
| star | 五角星 | 推荐、首页、精选 |
| home | 房屋 | 首页、主页、home |
| record | 记事本+横线 | 记录、日志、笔记 |
| chat | 对话气泡+三点 | 助手、聊天、问答、AI、客服 |
| history | 时钟 | 历史、记录、时间 |
| profile | 人形头像 | 我的、个人、设置、profile |
| cart | 购物车 | 购物车、购物、商城 |
| order | 文档+勾 | 订单、工单 |
| search | 放大镜 | 搜索、发现、探索 |
| category | 四宫格 | 分类、目录 |
| heart | 爱心 | 收藏、喜欢、关注 |
| bell | 铃铛 | 消息、通知、提醒 |
| map | 定位标记 | 地图、位置、附近 |
| stats | 柱状图 | 统计、数据、分析、报表 |
| camera | 相机 | 拍照、相册、图片 |
| scan | 扫码框 | 扫码、扫描 |

### Step 3：确认配色

默认配色方案：
- 未选中：`#999999`（灰色）
- 选中：`#4CAF50`（绿色）

读取 `app.json` 中 tabBar 的 `selectedColor` 字段作为选中色，保持与项目一致。
如果 app.json 没有 selectedColor，使用默认绿色，并向用户确认。

### Step 4：生成图标

运行 Python 脚本，用 PIL ImageDraw 绘制几何图形：
- 画布：81×81 px，RGBA 透明背景
- 线宽：3px
- 边距：14px
- 填充模式：实心填充（非描边），保证小尺寸下清晰可辨

每个 tab 输出 2 个文件到 `{miniprogram}/images/`：
- `tab_{id}.png`（未选中）
- `tab_{id}_active.png`（选中）

### Step 5：更新 app.json

为 tabBar.list 中每一项添加：
```json
{
  "iconPath": "images/tab_{id}.png",
  "selectedIconPath": "images/tab_{id}_active.png"
}
```

### Step 6：自检

- [ ] `images/` 目录下生成了 N×2 个 PNG 文件
- [ ] 每个 PNG 尺寸为 81×81
- [ ] `app.json` 每个 tab 都有 iconPath 和 selectedIconPath
- [ ] 图标配色与 tabBar selectedColor 一致

---

## 图标绘制参考代码

以下是各图标的 PIL 绘制逻辑参考，实际使用时封装为函数统一调用。

```python
import math
from PIL import Image, ImageDraw

SIZE = 81
PAD = 14

def new_canvas():
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)

# ===== star（五角星）=====
def draw_star(color):
    img, d = new_canvas()
    cx, cy = SIZE // 2, SIZE // 2
    r_out = SIZE // 2 - PAD + 4
    r_in = r_out * 0.38
    pts = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    d.polygon(pts, fill=color)
    return img

# ===== home（房屋）=====
def draw_home(color):
    img, d = new_canvas()
    m = PAD
    # 屋顶三角
    d.polygon([(SIZE//2, m), (m, SIZE//2), (SIZE-m, SIZE//2)], fill=color)
    # 屋体矩形
    d.rectangle([m+8, SIZE//2, SIZE-m-8, SIZE-m], fill=color)
    # 门（透明挖洞效果用背景色）
    d.rectangle([SIZE//2-8, SIZE//2+10, SIZE//2+8, SIZE-m], fill=(0,0,0,0))
    return img

# ===== record（记事本）=====
def draw_record(color):
    img, d = new_canvas()
    m = PAD
    d.rounded_rectangle([m, m, SIZE-m, SIZE-m], radius=6, outline=color, width=3)
    lm, rm = m+10, SIZE-m-10
    for pct in [0.30, 0.48, 0.66]:
        y = int(SIZE * pct)
        d.line([(lm, y), (rm, y)], fill=color, width=2)
    return img

# ===== chat（对话气泡）=====
def draw_chat(color):
    img, d = new_canvas()
    m = PAD - 2
    d.rounded_rectangle([m, m, SIZE-m, SIZE-m-10], radius=14, fill=color)
    cx, by = SIZE//2, SIZE-m-10
    d.polygon([(cx-8, by), (cx+8, by), (cx, by+12)], fill=color)
    dot_y = (m + SIZE-m-10) // 2
    for dx in [-12, 0, 12]:
        d.ellipse([cx+dx-3, dot_y-3, cx+dx+3, dot_y+3], fill=(255,255,255,255))
    return img

# ===== history（时钟）=====
def draw_history(color):
    img, d = new_canvas()
    cx, cy = SIZE//2, SIZE//2
    r = SIZE//2 - PAD
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=3)
    d.line([(cx, cy), (cx, cy-r+8)], fill=color, width=3)
    d.line([(cx, cy), (cx+r-12, cy)], fill=color, width=3)
    d.ellipse([cx-3, cy-3, cx+3, cy+3], fill=color)
    return img

# ===== profile（人形）=====
def draw_profile(color):
    img, d = new_canvas()
    cx = SIZE//2
    hr = 12
    hy = PAD + hr
    d.ellipse([cx-hr, hy-hr, cx+hr, hy+hr], fill=color)
    br, body_top = 24, hy+hr+4
    d.ellipse([cx-br, body_top, cx+br, SIZE-PAD+br], fill=color)
    return img

# ===== cart（购物车）=====
def draw_cart(color):
    img, d = new_canvas()
    m = PAD
    # 车身
    d.line([(m, m+5), (m+10, m+5), (SIZE-m-5, SIZE-m-18)], fill=color, width=3)
    d.line([(m+10, m+5), (SIZE-m, m+5)], fill=color, width=3)
    d.line([(SIZE-m, m+5), (SIZE-m-5, SIZE-m-18)], fill=color, width=3)
    d.line([(m+10, SIZE-m-18), (SIZE-m-5, SIZE-m-18)], fill=color, width=3)
    # 轮子
    d.ellipse([m+12, SIZE-m-12, m+22, SIZE-m-2], fill=color)
    d.ellipse([SIZE-m-22, SIZE-m-12, SIZE-m-12, SIZE-m-2], fill=color)
    return img

# ===== order（文档+勾）=====
def draw_order(color):
    img, d = new_canvas()
    m = PAD
    d.rounded_rectangle([m, m, SIZE-m, SIZE-m], radius=6, outline=color, width=3)
    # 勾
    cx, cy = SIZE//2, SIZE//2
    d.line([(cx-12, cy), (cx-2, cy+10), (cx+14, cy-10)], fill=color, width=3)
    return img

# ===== search（放大镜）=====
def draw_search(color):
    img, d = new_canvas()
    cx, cy = SIZE//2 - 4, SIZE//2 - 4
    r = 16
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=3)
    d.line([(cx+r-4, cy+r-4), (SIZE-PAD, SIZE-PAD)], fill=color, width=4)
    return img

# ===== category（四宫格）=====
def draw_category(color):
    img, d = new_canvas()
    m = PAD
    gap = 6
    bw = (SIZE - 2*m - gap) // 2
    for r in range(2):
        for c in range(2):
            x0, y0 = m + c*(bw+gap), m + r*(bw+gap)
            d.rounded_rectangle([x0, y0, x0+bw, y0+bw], radius=6, fill=color)
    return img

# ===== heart（爱心）=====
def draw_heart(color):
    img, d = new_canvas()
    cx, cy = SIZE//2, SIZE//2 + 2
    r = 13
    d.ellipse([cx-r*2, cy-r-4, cx, cy+2], fill=color)
    d.ellipse([cx, cy-r-4, cx+r*2, cy+2], fill=color)
    d.polygon([(cx-r*2+1, cy), (cx, cy+r+8), (cx+r*2-1, cy)], fill=color)
    return img

# ===== bell（铃铛）=====
def draw_bell(color):
    img, d = new_canvas()
    cx = SIZE//2
    m = PAD
    # 铃身
    d.arc([m+6, m, SIZE-m-6, SIZE-m-10], 180, 0, fill=color, width=3)
    d.line([(m+6, SIZE//2), (m+6, SIZE-m-10)], fill=color, width=3)
    d.line([(SIZE-m-6, SIZE//2), (SIZE-m-6, SIZE-m-10)], fill=color, width=3)
    d.line([(m, SIZE-m-10), (SIZE-m, SIZE-m-10)], fill=color, width=3)
    # 铃舌
    d.ellipse([cx-5, SIZE-m-8, cx+5, SIZE-m+2], fill=color)
    return img

# ===== map（定位标记）=====
def draw_map(color):
    img, d = new_canvas()
    cx = SIZE//2
    r = 18
    d.ellipse([cx-r, PAD, cx+r, PAD+r*2], fill=color)
    d.polygon([(cx-r+4, PAD+r+4), (cx, SIZE-PAD), (cx+r-4, PAD+r+4)], fill=color)
    d.ellipse([cx-6, PAD+r-6, cx+6, PAD+r+6], fill=(0,0,0,0))
    return img

# ===== stats（柱状图）=====
def draw_stats(color):
    img, d = new_canvas()
    m = PAD
    bw = 10
    heights = [0.4, 0.7, 0.55, 0.85]
    total_w = len(heights) * bw + (len(heights)-1) * 5
    sx = (SIZE - total_w) // 2
    for i, h in enumerate(heights):
        x = sx + i * (bw + 5)
        bh = int((SIZE - 2*m) * h)
        d.rectangle([x, SIZE-m-bh, x+bw, SIZE-m], fill=color)
    return img

# ===== camera（相机）=====
def draw_camera(color):
    img, d = new_canvas()
    m = PAD
    d.rounded_rectangle([m, m+10, SIZE-m, SIZE-m], radius=8, outline=color, width=3)
    # 镜头
    cx, cy = SIZE//2, SIZE//2 + 5
    d.ellipse([cx-12, cy-12, cx+12, cy+12], outline=color, width=3)
    # 闪光灯
    d.rectangle([SIZE//2-6, m+4, SIZE//2+6, m+12], fill=color)
    return img

# ===== scan（扫码框）=====
def draw_scan(color):
    img, d = new_canvas()
    m = PAD
    l = 14  # 角标线长
    # 四个角标
    for x0, y0, dx, dy in [(m,m,1,1), (SIZE-m,m,-1,1), (m,SIZE-m,1,-1), (SIZE-m,SIZE-m,-1,-1)]:
        d.line([(x0, y0), (x0+l*dx, y0)], fill=color, width=3)
        d.line([(x0, y0), (x0, y0+l*dy)], fill=color, width=3)
    # 中间扫描线
    d.line([(m+4, SIZE//2), (SIZE-m-4, SIZE//2)], fill=color, width=2)
    return img
```

---

## 绝对不能做的事

1. **不能生成超过 81×81 px 的图标** — 微信 tabBar 要求 81×81
2. **不能使用外部图标字体或 iconfont** — 用纯几何绘制，零依赖
3. **不能忘记更新 app.json** — 生成图标后必须写入 iconPath/selectedIconPath
4. **不能让选中色与 app.json 的 selectedColor 不一致**
