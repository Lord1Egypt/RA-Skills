---
name: zero-dep-image-inspect
slug: zero-dep-image-inspect
displayName: 零依赖图片诊断与并排对照（无 Pillow）
version: 1.0.1
license: MIT
platforms: [windows, macos, linux]
visibility: public
category: design-media
subCategories: [design-visual-asset]
description: 不装 Pillow / OpenCV 也能读图和量图：用标准库 zlib 解码 PNG，做亮度与主色统计、相邻像素跳变（锐度代理）、非白外接框、双线性缩放、裁切、写 PNG、并排/上下对照图、联系表，并用「模拟暗部提亮」把色带暴露出来。当用户说「图片不清晰」「图好糊/发灰/有横条斜条」「颜色不对」「帮我对比这两张图」「从截图里把某块裁出来」「批量看图挑一张」，或需要诊断「生成出来的图为什么在别处变丑」时使用。
agent_created: true
---

# 零依赖图片诊断与并排对照

## 何时用

- 用户贴图说「**不清晰 / 糊 / 发灰 / 有色带**」——先量，别猜。
- 要验证「我生成的图」和「用户在别处看到的图」到底差在哪。
- 从一张截图里裁出目标区域做进一步处理。
- 批量产物要目检（30 张封面/图标/牌面）→ 拼联系表一眼过。
- 环境装不上 Pillow（本机常驻、CI、客户机）时的唯一出路。

## 核心心法：先区分「分辨率问题」还是「渲染问题」

**「不清晰」有四种完全不同的原因，对应的解法互不通用：**

| 症状 | 判据 | 解法 |
|---|---|---|
| 真分辨率不够 | 原始像素尺寸 < 显示所需像素 | 提高生成分辨率 |
| 被下游二次压缩 | 源图锐、落到目标平台再拉回来就脏 | 改设计（见下） |
| 色带 / 发灰 | 像素挤在近黑区，色阶跨度只有几十级 | 换设计：避开近黑、去平滑渐变 |
| 被缩放显示 | 显示宽度 > 可用像素 | 按最终尺寸设计字号 |

判据来源：**把目标平台上实际存的那张图下载回来量**。不要只看自己本地生成的文件。

### 实例（2026-09-21，公众号封面）

本地生成 2250×958 → 平台 CDN `/0` 也是 2250×958 原图（无损），`/640` 是 1080×460。
分辨率全程没问题。真正原因：渐变 `#0f2b1c → #0d1117` 两端亮度都在 0~40，
98% 的像素挤在两个近黑桶里，**平均亮度只有 28.5/255（11%）**。显示端把暗部提一档
（用户截图实测平均亮度 103.6、暗部抬到 RGB≈(40,56,56)）后，量化台阶被放大成
**肉眼可见的斜向色带** —— 用户描述就是「糊 + 脏」。

```bash
python scripts/inspect.py stats old.png new.png       # 亮度 / 主色 / 跳变
python scripts/inspect.py lift old.png -o old_lift.png
python scripts/inspect.py lift new.png -o new_lift.png
python scripts/inspect.py compare old_lift.png new_lift.png -o cmp.png
```

量化结果：提亮后背景最强跳变 **旧版 83 → 新版 2**。

## 设计侧的三条硬规则（跨项目通用）

1. **避开近黑区**。底色平均亮度别低于 ~40/255。近黑是 8-bit 最脆弱的区间，
   任何 gamma / 色彩配置差异都把它掀翻。
2. **不要平滑渐变**。改成「硬停」渐变（色标重叠、无插值）＝两块纯色 + 一条硬边：
   ```css
   background: linear-gradient(100deg, #10362c 0%, #1d5f4a 63%, #1d5f4a 63%, #1d5f4a 100%);
   ```
   纯色区域在 PNG 里是常量，压缩 / 缩放 / 色彩变换都不会产生色带。
3. **按最终尺寸设计字号**。若下游会把图归一化到 1080 宽，就按 1080 画布定字号，
   再 `scale:2` 截图交给下游降采样 —— 比「大画布设计 + 被缩小」锐。

补充：`text-overflow:ellipsis` 对 12 字以上的中英混排产品名很容易吃掉内容，
**小字号永远比截断好看**。而且字号估算公式不可靠（CJK 1.0em / 拉丁 0.56em 对
「混排 + 粗体」会偏窄约 5%），正确做法是**在浏览器里实测并自动缩字号**：

```js
if (e.scrollWidth > e.clientWidth + 1) e.style.fontSize = (fs * 0.93) + 'px';
// 循环最多 10 轮，直到不溢出
```

## CLI

`scripts/inspect.py`（`scripts/imgtool.py` 是被它 import 的库）

```bash
python inspect.py stats   <图...>                    # 亮度/主色/跳变 一张表
python inspect.py lift    <图> [--gamma 0.62] -o x   # 模拟暗部提亮，暴露色带
python inspect.py compare <图A> <图B> -o cmp.png     # 上下拼接（白底留边）
python inspect.py bbox    <图> [--thresh 235]        # 非白外接框（从句图截图裁目标）
python inspect.py crop    <图> --box x0,y0,x1,y1 -o x
python inspect.py resize  <图> --width 900 -o x
python inspect.py sheet   <图...> --cols 5 --width 300 -o sheet.png
```

`stats` 输出读法：**亮度 <40/255 = 整图挤在近黑区**（危险的信号）；
主色数少 + 跳变低 = 平滑区域已经块状化。

## 库 API（`imgtool.py`）

```python
import imgtool as I
w, h, px = I.load_rgb("a.png")              # -> (w, h, RGB 紧凑 bytes)
I.write_png("out.png", w, h, px)            # 写 PNG（zlib 压缩），吃三元组
I.fit_width("a.png", 1000)                  # -> (nw, nh, px, (原w, 原h))
I.resize(w, h, px, nw, nh)                  # -> 裸 bytes（双线性）
I.crop(w, h, px, x, y, cw, ch)              # -> 裸 bytes（裁切）
I.crop_rgb(w, h, px, x, y, cw, ch)          # -> (cw, ch, px)，裁切的对称版
I.bbox_nonwhite("a.png", thresh=235)        # -> (x0, y0, x1, y1)
I.vstack([(w,h,px), ...], pad=12)           # -> (tw, th, out) 上下拼接
```

**返回值分两类，混用必炸 `ValueError`**（踩过）：
- **三元组 `(w,h,px)`**：`load_rgb` / `fit_width` / `crop_rgb` / `vstack` —— 可无缝喂给下一环
- **裸 `bytes`（只有像素）**：`resize` / `crop` —— 尺寸要自己记，或改用 `crop_rgb`
- 所以 `cw, ch, p = I.crop(...)` 是**错的**；`cw, ch, p = I.crop_rgb(...)` 才对。

支持 PNG 色彩类型 0/2/3/4/6、滤镜 0-4、PLTE 调色板。**不支持** 16bit 与隔行；
JPEG 需要先转 PNG（可用浏览器 CDP 截图或系统工具）。

## 坑

- **不要只量本地文件**。要看下游实际存的那张：CDN 常有多档（`/0` 原图、`/640`
  降级），编辑器预览加载的往往是降级档，实际显示宽度可能超过它的像素数。
- **别用「平均亮度」单指标下结论**，配合主色分布一起看：平均 28 但主色只有两个
  近黑桶，比平均 60 而主色分散更危险。
- **对称地做对照**：把两张图放到同一宽度再拼，否则尺寸差本身就会被误读成清晰度差。
- `vstack` 的入参是 `(w, h, px)` 三元组，不是裸 `bytes` —— 传错会 `ValueError`。
