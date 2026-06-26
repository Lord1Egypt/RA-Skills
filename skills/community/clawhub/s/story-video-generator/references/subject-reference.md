# 主体参考图生成（Step 1.5）

在首帧生成之前，先生成一张高质量的"主体参考图"，作为整个视频中视觉一致性的锚点。

## 输入要求
- `output/story_script.json` 中的 `analysis.subject`
- 可选：用户提供的主体参考图片

## 执行步骤

### 1. 读取角色特征
从 `output/story_script.json` 读取 `analysis.subject`

### 2. 判断主体类型

| 类型 | 判断依据 | 参考图特点 |
|------|---------|-----------|
| 人物/动物 | 描述中有生物特征 | 正面照，中性姿态 |
| 物体/产品 | 描述中有物品特征 | 3/4视角，展示细节 |
| 场景/地点 | 描述中以环境为主 | 全景或标准视角 |

### 3. 构建参考图 Prompt

```
Character reference sheet, [角色详细特征描述],
front-facing view, neutral pose, centered composition,
clean background, studio lighting, high detail,
consistent character design, reference image for animation,
same character as will appear throughout the video,
stable face, preserve features, detailed facial features,
high quality, 8k resolution
```

### 4. 生成参考图

**有用户参考图：**
```json
{
 "prompt": "[参考图 prompt]",
 "output_file": "output/subject_reference.png",
 "reference_files": ["用户提供的参考图片"],
 "aspect_ratio": "1:1",
 "resolution": "2K"
}
```

**纯文字模式：**
```json
{
 "prompt": "[参考图 prompt，含风格关键词]",
 "output_file": "output/subject_reference.png",
 "aspect_ratio": "1:1",
 "resolution": "2K"
}
```

### 5. 保存路径
`output/subject_reference.png`

## 一致性关键词

**人物/动物：**
```
stable appearance, preserve features, consistent character design,
same character throughout, detailed features
```

**物体/产品：**
```
stable appearance, preserve details, consistent product design,
same object throughout, detailed features
```

**场景/地点：**
```
stable atmosphere, preserve environment style, consistent location design,
same environment throughout, detailed features
```

## 注意事项
1. 简洁背景：避免干扰主体特征提取
2. 合适视角：根据主体类型选择最佳展示视角
3. 高细节：主体细节要清晰，便于后续复现
4. 单主体：一张参考图只包含一个主要主体
