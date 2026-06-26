# 提示词输出格式模板

## 基础模板（单帧 → 单句提示词）

```
[景别] [主体描述] in [场景], [服装], [色调], [光线], [构图], shot on [设备], [运镜]
```

### 分镜段模板（多帧 → 10秒片段）

每 1.33 秒（约40帧）为一个镜头的起始点：

```
[序号] | [时间点] | [景别] | [主体+动作] | [场景] | [色调] | [光线] | [运镜]

示例：
01 | 0:00 | MCU | Young man, upper body, looking forward | Rural dirt road | Dusty blue-gray | Side golden light | Static, slight breathing
02 | 0:01.3 | WS | Full body, walking forward | Same dirt road | Dusty blue-gray | Golden hour | Slow zoom-in
03 | 0:02.6 | CU | Face, focused expression | Same location | Warmer tones | Backlit rim light | Slow push-in
```

## AI 绘图提示词模板

### 通用场景
```
[景别] shot of [主体], [场景描述], wearing [服装细节], [色调], [光线描述], [构图], [相机+焦段], [风格标签]
```

### 人物肖像
```
[景别] portrait of [年龄/性别描述], [面部特征], [发型发色], wearing [上衣], [裤子], [鞋子], in [背景场景], [色调], [主光线方向], [氛围], shot on [设备/焦段], [景深], cinematic, 8k, highly detailed
```

### 场景/环境
```
[景别] establishing shot of [场景总览], [前景细节], [中景主体], [背景元素], [色调], [时间段光线], [天气], shot on [设备/焦段], [运镜], hyperrealistic, cinematic color grading
```

## 批量处理模板（多帧 → 多句）

当上传 4-6 张帧图时，按时间顺序输出：

```
【镜头 1 · 0:00 - 0:03s】
Medium Close-up portrait of a young man in rural setting, wearing a gray cotton jacket, muted dusty blue tones, soft afternoon side light, centered composition, shot on Sony A7III 85mm f/1.4, slight static, intimate mood

【镜头 2 · 0:03 - 0:07s】
Wide shot of the same man walking down a dirt path, warm golden light growing stronger, dusty atmosphere, 2.39:1 cinematic aspect ratio, slow tracking shot following movement, documentary realism

【镜头 3 · 0:07 - 0:10s】
Close-up of jacket collar and neck, warm orange tones, rim lighting from behind, shallow depth of field, shot on Canon 50mm f/1.2, push-in movement, contemplative atmosphere
```

## 风格标签参考

| 类别 | 标签 |
|------|------|
| 摄影风格 | cinematic, documentary, editorial, fine art, street photography |
| 画质 | 8K, ultra-detailed, hyperrealistic, sharp focus, soft focus |
| 构图 | centered, rule-of-thirds, golden ratio, leading lines, symmetrical |
| 情绪 | melancholic, hopeful, nostalgic, tense, serene, raw |
| 胶片 | Kodak Portra 400, Fujifilm Pro 400H, Cinestill 800T, Ilford HP5 |
