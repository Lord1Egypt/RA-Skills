# Prompt 模板库

经过验证的高质量 AI 绘画提示词模板。使用时将 `[占位符]` 替换为实际内容。

## 目录
1. [海报模板](#海报模板)
2. [配图模板](#配图模板)
3. [封面模板](#封面模板)
4. [数字人背景模板](#数字人背景模板)
5. [通用负面提示词](#通用负面提示词)

---

## 海报模板

### 科技感活动海报
```
[主题]主题活动海报, 科技感设计, 深蓝色渐变背景, 光线特效粒子, 未来感, 
现代排版, 中文[标题文字]醒目标题, 高端商务风格,
high quality, 8K, sharp details, professional design
```

### 课程/培训海报
```
[课程名称]在线课程海报, 简洁专业设计, 白色/浅色背景, 
几何图形装饰, 权威感, 醒目的[讲师名/机构]字样, 
modern layout, clean design, professional, high quality
```

### 产品宣传海报
```
[产品名称]产品海报, 高端产品摄影风格, [主色调]背景,
产品特写展示, 精致质感, 简洁文案空间,
commercial photography style, studio lighting, high quality, 8K
```

---

## 配图模板

### 科技类配图
```
[主题]科技概念图, 数字科技风格, 蓝紫色调, 
电路板/数据流/AI大脑视觉元素, 未来感, 抽象且专业,
digital art, futuristic, high quality, detailed
```

### 生活/小清新配图
```
[场景]生活场景, 小清新风格, 自然光线, 
莫兰迪色系, 温暖氛围, 真实感, 
soft colors, warm lighting, lifestyle photography, high quality
```

### 商务配图
```
[主题]商务场景, 专业办公环境, 
现代简约风格, 暖白色调, 成功感, 专业感,
business professional, modern office, clean, high quality
```

---

## 封面模板

### 视频封面（竖版 9:16）
```
[主题]视频封面, 竖版构图, 鲜艳吸睛, 
大标题文字空间预留在上方, 画面下方主体突出,
强烈视觉冲击, 高对比度色彩,
vertical format, eye-catching, high quality
```

### 文章封面（横版 16:9）
```
[主题]文章配图, 横版构图, 专业媒体风格,
左侧/右侧留白给文字, 主视觉元素突出,
editorial style, professional, high quality
```

---

## 数字人背景模板

### 办公室背景
```
现代高端办公室背景, 虚化处理, 专业商务感,
落地窗城市景观, 简约北欧风家具, 温暖室内灯光,
bokeh background, professional office, high quality, 16:9
```

### 演播室背景
```
专业电视演播室背景, 科技感布景, LED屏幕环境,
蓝紫色灯光氛围, 新闻播报风格,
studio background, broadcast, professional lighting, high quality
```

### 户外场景背景
```
[城市/自然]户外场景背景, 明亮自然光线, 
城市街景/公园绿地, 适度虚化,
outdoor scene, natural lighting, bokeh, high quality
```

### 抽象科技背景
```
抽象科技感背景, 深色调, 粒子光效, 
数据流动感, 适合数字人叠加, 
无明显主体, 氛围感强,
abstract tech background, particle effects, dark theme, high quality
```

---

## 通用负面提示词

适用于所有模板，加在 prompt 末尾：

```
negative prompt: blurry, low quality, pixelated, distorted text, 
watermark, logo, signature, oversaturated, unrealistic colors,
deformed, ugly, bad anatomy, extra limbs, low resolution
```

## 使用技巧

1. **风格叠加**：可以组合多个风格词，如 `科技感 + 国潮` → 加入 `中国传统纹样, 科技蓝, 龙凤元素`
2. **色彩控制**：明确指定主色调比描述氛围更有效
3. **构图控制**：用 `左侧/右侧/上方/下方留白` 控制文字排版空间
4. **批量备选**：重要任务建议生成 4-8 张备选，从中挑选最佳
