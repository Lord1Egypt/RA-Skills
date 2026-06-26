# Design Token 模板

> 每次配图任务前，基于调研结果填写本模板。
> 代码生成图卡时必须使用这些 Token，不要自由发挥。

---

## 基础模板

```python
# ============================================================
# Design Tokens — [你的品牌/本帖主题]
# ============================================================

# 调色板
BG_COLOR     = (245, 240, 232)  # 背景色
TEXT_PRIMARY  = (30, 30, 30)     # 标题文字
TEXT_SECONDARY = (60, 55, 50)    # 正文文字
TEXT_TERTIARY = (120, 115, 108)  # 辅助文字
ACCENT_MAIN  = (212, 168, 83)   # 主强调色
ACCENT_HIGH  = (199, 91, 58)    # 高亮色
ACCENT_SOFT  = (225, 215, 200)  # 柔和色（分隔线等）

# 间距
MARGIN_X     = 96       # 左右边距
MARGIN_TOP   = 140      # 顶部留白
LINE_H_TITLE = 80       # 标题行高
LINE_H_BODY  = 52       # 正文行高

# 字体
FONT_CN_TITLE = "/path/to/chinese-bold-font"
FONT_CN_BODY  = "/path/to/chinese-regular-font"
FONT_EN_TITLE = "/path/to/english-bold-font"
FONT_EN_BODY  = "/path/to/english-regular-font"
```

---

## 示例：暖色极简风

```python
BG_COLOR      = (245, 240, 232)  # #F5F0E8 奶油米色
TEXT_PRIMARY   = (30, 30, 30)
TEXT_SECONDARY = (60, 55, 50)
TEXT_TERTIARY  = (120, 115, 108)
ACCENT_MAIN   = (212, 168, 83)   # #D4A853 暖黄金
ACCENT_HIGH   = (199, 91, 58)    # #C75B3A 暖红
ACCENT_SOFT   = (225, 215, 200)
```

## 示例：蓝紫科技风

```python
BG_COLOR      = (240, 237, 248)  # #F0EDF8 浅薰衣草
TEXT_PRIMARY   = (30, 30, 40)
TEXT_SECONDARY = (55, 50, 65)
TEXT_TERTIARY  = (110, 105, 120)
ACCENT_MAIN   = (108, 92, 231)   # #6C5CE7 主紫
ACCENT_HIGH   = (66, 133, 244)   # #4285F4 蓝
ACCENT_SOFT   = (210, 205, 225)
```

## 示例：深色科技风

```python
BG_COLOR      = (22, 25, 30)     # 深灰黑
TEXT_PRIMARY   = (245, 249, 255)  # 近白
TEXT_SECONDARY = (180, 185, 195)
TEXT_TERTIARY  = (120, 125, 135)
ACCENT_MAIN   = (0, 200, 150)    # 科技绿
ACCENT_HIGH   = (255, 165, 0)    # 橙色
ACCENT_SOFT   = (45, 48, 55)
```

---

## 推荐字体方案

### macOS

| 用途 | 字体 | 路径 |
|------|------|------|
| 中文粗体 | Hiragino Sans GB W6 | `/System/Library/Fonts/Hiragino Sans GB.ttc` (index=1) |
| 中文常规 | Hiragino Sans GB W3 | `/System/Library/Fonts/Hiragino Sans GB.ttc` (index=0) |
| 英文标题 | Inter Bold | 开源下载 [Google Fonts](https://fonts.google.com/specimen/Inter) |
| 英文正文 | Inter Regular | 同上 |

### 开源替代

| 用途 | 字体 | 说明 |
|------|------|------|
| 中文 | 思源黑体 (Noto Sans CJK) | 开源，全平台 |
| 英文标题 | Nunito Bold | 圆角无衬线，可爱科技感 |
| 英文正文 | Inter | 21世纪标准无衬线 |
| 圆角字体 | SF Pro Rounded / Varela Round | 友好感 |

---

## 图片尺寸规范

| 用途 | 尺寸 | 比例 | 说明 |
|------|------|------|------|
| 小红书封面 | 1080×1440 px | 3:4 | 竖图（推荐） |
| 小红书方图 | 1080×1080 px | 1:1 | 方图 |
| 内页图卡 | 1080×1440 px | 3:4 | 和封面保持一致 |
| Lovart 生成 | 1792×2400 px | 3:4 | Lovart 默认输出 |
