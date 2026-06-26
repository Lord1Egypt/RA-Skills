# Seedance 2.0 Prompt 模板库

> 持续更新，适合直接复制使用

---

## 📦 产品展示

### 产品 360° 展示
```
@image1 [产品名称] as the main subject, camera movement references @video1, zoom in to close-up of [具体细节],
camera rotates and [产品] flips to show full view, [产品特性] clearly visible,
surrounding environment [氛围描述].
```

### 产品广告对比
```
This is a [产品] advertisement, @image1 as the first frame, [角色A] in [状态A],
camera quickly pans right, shooting @image2 [角色B] in [状态B],
camera pans left and zooms in shooting [产品], [产品] references @image3, [产品] in [工作状态].
```

---

## 🎬 视频延长

### 向前延长
```
[X-Y]s: [当前场景描述].
Extend @video1 forward by [N] seconds.
[0-N]s: [延长内容描述].
[Y-N]s: [结尾场景/字幕].
```

### 向后延长
```
Extend @video1 backward by [N] seconds.
[0-N]s: [开头场景描述].
[last frame state from @video1]: [承接描述].
```

---

## 🎥 One-Shot 连续镜头

### 横向移动
```
@image1@image2@image3..., [视角] one continuous shot [移动类型] camera,
[移动轨迹: 从A经过B到C], [速度/节奏变化].
No scene cuts throughout, one continuous shot.
```

### 跟拍
```
Camera follows @image1 as [动作描述], [背景事件], [音效描述].
No scene cuts throughout, one continuous shot.
```

### 环绕镜头
```
[robotic arm multi-angle circular movement] around @image1, [氛围描述],
camera completes one full rotation, smooth motion.
No scene cuts throughout, one continuous shot.
```

---

## 🎨 特效镜头

### Hitchcock Zoom（希区柯克变焦）
```
protagonist in [情绪] with Hitchcock zoom, background [透视变化描述].
```

### 粒子散射
```
[颜色] [粒子材质] particles scatter, [散射方向], [光线描述].
```

### 加速效果
```
speed accelerates like a roller coaster, [主体] [加速表现].
```

### 雨/水效果
```
rain drops on camera lens, [主体] in [场景], [光效描述].
```

---

## 📝 镜头语言

| 效果 | 推荐写法 |
|------|---------|
| 拉远 | Camera pulls back slightly, revealing [全景] |
| 推进 | Camera pushes forward toward [主体] |
| 横移 | Camera pans left/right following [主体] |
| 跟拍 | Camera tracks [主体], [动态描述] |
| 环绕 | Camera circles around [主体], [速度描述] |
| 升降 | Camera rises/drops, [视野变化] |
| 希区柯克 | protagonist in [情绪] with Hitchcock zoom |
| 旋转 | Camera rotates [角度] degrees around [主体] |

---

## ✏️ Prompt 写作规范

### 动作描述（五要素）
```
[速度]:  slow / moderate / rapid / accelerating
[方向]:  toward / away / around / through
[部位]:  hand / body / head / eyes
[变化]:  trembling / shaking / steady / accelerating
[表情]:  smiling / shocked / confused / calm
```

❌ 错误：`character is very sad`
✅ 正确：`tears slide down cheeks, mouth trembles slightly, hands shaking`

### 时间轴分段（10秒+）
```
0-3s: [场景1描述]
3-6s: [场景2描述]
6-10s: [结尾场景/字幕]
```

### 音效描述
```
[声音类型]: [强度] [音色], [节奏描述]
例如：Soft piano melody, steady rhythm, building to crescendo
```

---

## 🚀 进阶技巧

### 多素材分离控制
```
Reference character appearance from @image1,  # 人物外观
Reference camera movement from @video1,    # 镜头运动（不用@video1的人物）
Reference action from @video2,              # 动作参考
Background BGM references @audio1         # 背景音乐
```

### 长镜头写法
```
[主语] [动作1], [动作2], [动作3], [动作4].
[具体细节描写].
No scene cuts throughout, one continuous shot.
```

### 镜头+动作分离
```
Reference character action from @video1,
Reference circular camera movement from @video2.
```

---

*此模板库由 Anna 整理 · 持续更新*
