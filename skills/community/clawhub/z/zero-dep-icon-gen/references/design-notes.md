# 图标设计参考

## 配色：怎么给一个工具选图标主色

### 方法一：挑语义色（最快，推荐）

按技能/工具的**领域**选一个大家都认的色系，然后取「深 + 浅」两个同色调：

| 领域 | 深色（main） | 浅色（accent） | 语义 |
|---|---|---|---|
| 网页 / 开发者工具 / 控制台 | `#4F46E5` | `#818CF8` | 靛蓝 |
| 云 / 部署 / 存储 | `#0284C7` | `#38BDF8` | 天蓝 |
| 安全 / 证书 / 授权 | `#D97706` | `#FBBF24` | 琥珀 |
| 文件 / 归档 / 整理 | `#059669` | `#34D399` | 翠绿 |
| 完成 / 签到 / 任务 | `#DC2626` | `#F87171` | 正红 |
| 下载 / 导出 | `#7C3AED` | `#A78BFA` | 紫罗兰 |
| 配置 / 自动化 | `#0891B2` | `#22D3EE` | 青 |
| 搜索 / 检索 | `#DB2777` | `#F472B6` | 桃红 |
| 通用 / 中性 | `#475569` | `#94A3B8` | 石板灰 |
| 深色主题文字底 | `#1E293B` | `#64748B` | 深蓝灰 |

这套取自 Tailwind CSS 的 600/400 档位 —— 保证有足够对比度（白符号叠上去清晰），
且深浅之间有自然的明度差，渐变好看。

### 方法二：从真实界面截图反推主色

要给一个**已有品牌色**的产品做图标时：

```python
# 1. 读截图，统计高频非灰度色
from collections import Counter
import struct, zlib

def dominant_colors(png_path, top=10):
    """手写 PNG 解码（仅 filter 0/1/2 + 8bit RGBA 或 RGB）。"""
    data = open(png_path, "rb").read()
    pos, w, h, raw = 8, 0, 0, bytearray()
    while pos < len(data):
        ln = struct.unpack(">I", data[pos:pos+4])[0]
        tag = data[pos+4:pos+8]
        body = data[pos+8:pos+8+ln]
        if tag == b"IHDR":
            w, h, depth, ctype = struct.unpack(">IIBB", body[:10])
            bpp = {0:1, 2:3, 4:2, 6:4}[ctype]
        elif tag == b"IDAT":
            raw += body
        pos += 12 + ln
    rows = zlib.decompress(bytes(raw))
    stride = w * bpp
    cnt = Counter()
    prev = bytearray(stride)
    p = 0
    for _ in range(h):
        ft = rows[p]; p += 1
        line = bytearray(rows[p:p+stride]); p += stride
        # 只处理 filter 0/1/2，够用于截图
        if ft == 1:
            for i in range(bpp, stride): line[i] = (line[i] + line[i-bpp]) & 255
        elif ft == 2:
            for i in range(stride): line[i] = (line[i] + prev[i]) & 255
        for x in range(0, stride, bpp):
            r, g, b = line[x], line[x+1], line[x+2]
            if max(r,g,b) - min(r,g,b) < 24:      # 跳过灰/白/黑
                continue
            cnt[(r//16*16, g//16*16, b//16*16)] += 1
        prev = line
    return cnt.most_common(top)

for rgb, n in dominant_colors("shot.png"):
    print("#%02X%02X%02X" % rgb, n)
```

拿到高频色后，**加深作为 main、提亮作为 accent**（保持色相不变，改明度）：

```python
import colorsys
def shade(hexcolor, delta_l):
    h = hexcolor.lstrip("#")
    r, g, b = (int(h[i:i+2], 16)/255 for i in (0, 2, 4))
    hh, ll, ss = colorsys.rgb_to_hls(r, g, b)
    ll = min(0.95, max(0.06, ll + delta_l))
    r, g, b = colorsys.hls_to_rgb(hh, ll, ss)
    return "#%02X%02X%02X" % (round(r*255), round(g*255), round(b*255))

main   = shade("#4F46E5", -0.18)   # 加深 -> 渐变起点
accent = shade("#4F46E5", +0.14)   # 提亮 -> 渐变终点
```

## 规范建议

| 项 | 建议值 | 理由 |
|---|---|---|
| 画布 | 256×256（另出 512 备高清） | 主流平台要求，体积仍很小 |
| 圆角半径 | 边长 × 21.9%（256 → 56） | 接近 iOS / Material 的 squircle 观感 |
| 底色 | 对角线双色渐变 | 比平涂更有质感，且和平台通用占位图明显区分 |
| 符号色 | 纯白 `#FFFFFF` | 最高对比，任何底色都清晰 |
| 符号占幅 | 45%~60%，坐标留在 0.22~0.78 | 四周留白，缩到 32px 不糊边 |
| 符号数量 | 1 个 | 图标不是插图，多符号在缩略图下必糊 |

## 一排图标放在一起时的可辨识度检查

批量生成后**务必逐张 Read 图片目视检查**（本技能踩过的所有渲染 bug 都是肉眼看出来的，
脚本不会报错）。检查点：

1. 6 张缩到 32px 后**颜色**能否区分？（色相别撞）
2. 6 张缩到 32px 后**符号轮廓**能否区分？（别都是圆/方块）
3. 有没有哪个符号被挖空吃掉、缺胳膊少腿？
4. 圆角边缘有没有一圈深色描边（`shape_a` 二次衰减）？

## 安全区（避免被平台裁切）

多数技能市场/应用商店会对图标做圆形或圆角裁切，所以：

- 关键视觉控制在**内切圆**内（半径 ≤ 边长的 40%，即 256 → 102px）
- 或至少留出 8% 边距（256 → 20px）

本生成器的圆角方形底 + 居中符号默认是安全的：符号最大延伸到 0.245~0.775，
距边缘 62px（24%），远大于 8% 边距要求。
