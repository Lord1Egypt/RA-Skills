---
name: zero-dep-icon-gen
slug: zero-dep-icon-gen
displayName: 零依赖图标生成器（手写 PNG / 无 Pillow）
version: 1.0.1
license: MIT
platforms: [windows, macos, linux]
category: design-media
subCategories: [design-image-gen, design-visual-asset]
description: 在完全不装任何三方库（无 Pillow / cairosvg / ImageMagick）的前提下，用标准库 zlib+struct 手写 PNG 编码器生成应用图标：圆角方形渐变底 + 白色实心剪影符号。当用户要"给工具/技能/应用生成图标""换个 icon""没有 Pillow 怎么画图""批量生成 favicon / 应用图标""icon 生成器"时使用。内置 10 个矢量符号（浏览器/云/盾牌/文件夹/对勾/下载/箭头/齿轮/放大镜/锁）+ 5x7 点阵文字，支持任意尺寸与超采样抗锯齿。
agent_created: true
---

# 零依赖图标生成器

## 这个技能解决什么

需要给一个工具、技能或应用配图标，但：
- 装不上 Pillow（`pip install` 超时 / SIGTERM / 无网络 / 代理问题）
- 目标是「打开即用」的交付物，不该引入二进制依赖
- 只想画个**几何符号图标**，不需要照片级图形

→ 用标准库手写 PNG。一个 256×256 RGBA 图标只要约 4KB，生成耗时 < 1 秒。

## 快速开始

```bash
PY="C:/Users/DELL/.workbuddy/binaries/python/versions/3.13.12/python.exe"
S="$HOME/.workbuddy/skills/zero-dep-icon-gen/scripts/gen_icons.py"

# 看有哪些符号
$PY "$S" --list-symbols

# 生成单个
$PY "$S" --spec "my-tool:#4F46E5,#818CF8,browser" -o out/

# 批量（推荐：写 specs 文件，可版本控制）
$PY "$S" --specs-file specs.txt -o out/

# 512 尺寸 + 圆角 96
$PY "$S" --spec "my-tool:#059669,#34D399,check" --size 512 --radius 96 -o out/

# 点阵文字图标
$PY "$S" --spec "wb:#1E293B,#64748B,text|text=WB" -o out/
```

**spec 格式**：`slug:#主色,#次色,符号[|key=value,key=value]`

| 选项 | 说明 |
|---|---|
| `text=` | `symbol=text` 时渲染的文字（大写字母/数字，1~4 个） |
| `rotate=` | 符号旋转角度（度），如 `rotate=15` |
| `shadow=` | `1` 时底色压暗 12%，做弱化/次要变体 |

specs 文件每行一条，`#` 开头为注释。

## 可用符号

| 符号 | 语义 | 视觉 |
|---|---|---|
| `browser` | 网页 / 浏览器 / 控制台 | 实心窗口 + 挖空屏幕 + 三圆点 + 内容线 |
| `cloud` | 上传 / 部署 / 云端 | 三圆并集云 + 向上箭头 |
| `shield` | 证书 / 安全 / 续期 | 实心盾牌 + 挖空对勾 |
| `folder` | 归档 / 整理 / 文件 | 文件夹剪影 + 三条镂空横线 |
| `check` | 完成 / 签到 / 通过 | 圆环 + 实心对勾 |
| `download` | 下载 / 导出 | 下箭头 + 底部托线 |
| `arrow-up` | 发布 / 升级 | 上箭头 |
| `gear` | 配置 / 自动化 | 8 齿齿轮 + 中心镂空 |
| `search` | 搜索 / 检索 | 放大镜 |
| `lock` | 授权 / 密钥 | 锁体 + 锁梁 |
| `text` | 缩写文字 | 5×7 点阵（配 `--text`） |

## 三条设计铁律（踩过坑，别推翻）

### 1. 符号用实心剪影，不要空心描边

第一版想做「空心描边框 + 内挖空」，结果**内挖空把符号本身吃掉了**：浏览器成了光板方块、
盾牌里对勾消失、文件夹横线被吞、云朵箭头畸形。

实心剪影两个好处：32px 缩略图下辨识度更高；实现上只需一层 `if 在形状内: return True`，
不用处理「边框+内洞」的布尔运算。

### 2. 判定顺序：先外框 → 再挖空 → 最后挖细节

以 `sym_browser` 为例，顺序错了细节会被覆盖：

```
1. 不在窗口外框内      -> False
2. 在屏幕区（挖空）    -> 屏幕内容线 True，其余 False   ← 提前 return
3. 在标题栏且碰到圆点  -> False                        ← 最后挖
4. 其余                -> True
```

第 2 步必须提前 `return`，否则第 3、4 步的 `True` 会把屏幕重新填实。

### 3. 边缘抗锯齿用「超采样 + shape_a 归一」

```python
sym_a = (cov_sym / total) / max(shape_a, 1e-6)
```

**必须除以 `shape_a`**。否则在圆角边缘，像素的符号覆盖本身就是被形状裁剪过的，
再乘一次形状 alpha 会二次衰减，符号边缘出现一圈深色描边。

## 技术实现要点

### PNG 编码（`write_png`）

只需 3 个 chunk，全部标准库：

```python
png  = b"\x89PNG\r\n\x1a\n"
png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))  # 6 = RGBA
png += chunk(b"IDAT", zlib.compress(raw, 9))   # raw = 每行前加一个 \x00 (filter None)
png += chunk(b"IEND", b"")

def chunk(tag, data):
    return (struct.pack(">I", len(data)) + tag + data
            + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))
```

坑：`zlib.crc32` 在旧版本返回有符号 int，`& 0xFFFFFFFF` 保证一致；
`IHDR` 的 CRC 必须覆盖 `b"IHDR" + data`，漏掉 tag 会导致图片打不开。

### 几何工具函数

- `seg_dist(px,py,ax,ay,bx,by)` — 点到线段距离，用于对勾 / 箭头杆 / 任意角度笔画
- `bar_dist(px,py,x0,x1,y0,y1)` — 轴对齐矩形距离，`<=0` 在内部，用于窗口 / 文件夹 / 横线
- `rounded_square_alpha(...)` — 圆角方形覆盖度

### 尺寸与体积参考

| 尺寸 | 典型体积 |
|---|---|
| 128 | 1.5~2 KB |
| 256 | 3.5~6 KB |
| 512 | 10~18 KB |

超采样倍数 `SS = 2`（2×2）。改 4×4 渲染时间 ×4，肉眼几乎无差别，**不建议**。

## 常见错误排查

| 现象 | 原因 | 处置 |
|---|---|---|
| `spec 格式应为 slug:main,accent,symbol` | spec 只给了一段 | 必须 `slug:#a,#b,sym` 三段，冒号分隔 |
| `WARN: 未知符号` | 符号名拼错 | `--list-symbols` 核对 |
| 图标中心一片空白 | 挖空区域过大，把符号吃掉了 | 见「铁律 1」，改实心剪影 |
| 圆角边缘有深色描边 | 忘了除以 `shape_a` | 见「铁律 3」 |
| 符号被截断贴边 | 坐标超出 0.2~0.8 | 符号坐标应留在 0.22~0.78，四周留白 |
| 文件生成但打不开 | CRC 或 IHDR 写错 | 确认 CRC 覆盖 `tag + data`，color type = 6 |

## 与图标上传链路的衔接

生成完图标只是第一半。若目标是**发布到技能市场**，图标还需上传：

- SkillHub：图标**没有独立更新端点**，`iconUrl` 只能随 publish 的 payload 提交。
  **换图标 = 发一个新版本**。先 `POST /api/v1/community/skill-icons/upload`
  （multipart 字段名 `file`）拿到 `iconUrl`，再放进 `payload.iconUrl`。
  判据：响应里 `iconAuditStatus: "pending"` 表示收到；`null` 表示没生效。
  完整流程见 `skillhub-publish-skill` 技能的 `references/icon-upload.md`。

- 若平台方是「上传 zip 包」，把生成的 `<slug>.png` 放在技能目录根部
  （文件名 = slug），发布脚本的 `find_icon()` 会自动兜底找到。

## 资源

- `scripts/gen_icons.py` — 生成器主体，含 10 个符号 + 点阵字体 + PNG 编码器。
  加新符号只需写一个 `sym_xxx(x, y)` 函数并注册进 `SYMBOLS` 字典。
- `references/design-notes.md` — 配色方案与从真实截图反推主色的方法。
