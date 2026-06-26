# 首帧图片生成（Step 2）

基于故事脚本中的 visual_desc **串联生成**首帧图片。

## 角色一致性策略

```
主体参考图 ──────────────────────────────────────────────────┐
 │ │
 ▼ ▼
 frame_01 ──→ frame_02 ──→ frame_03 ──→ ... ──→ frame_N
 (上一帧) (上一帧) (上一帧)
```

## 执行步骤

### 1. 读取输入
- 从 `output/story_script.json` 读取 analysis 和 story_script
- 确认 `output/subject_reference.png` 存在

### 2. 串联生成（逐帧）

**必须按顺序逐帧生成，禁止并行！**

#### Frame 1（第一帧）
```json
{
 "prompt": "[visual_desc_1] + [一致性关键词]",
 "output_file": "output/frames/frame_01.png",
 "reference_files": ["output/subject_reference.png"],
 "aspect_ratio": "16:9",
 "resolution": "2K"
}
```

#### Frame 2-N（后续帧）
```json
{
 "prompt": "[visual_desc_N] + [一致性关键词]",
 "output_file": "output/frames/frame_0N.png",
 "reference_files": [
 "output/subject_reference.png",
 "output/frames/frame_0{N-1}.png"
 ],
 "aspect_ratio": "16:9",
 "resolution": "2K"
}
```

## Prompt 构建规则

每个 prompt 必须包含：
```
[风格描述: analysis.style].
[场景描述: analysis.scene].
[主体描述: analysis.subject].
[该段 visual_desc].
same subject as reference image, stable appearance, preserve features,
consistent design, consistent lighting style,
high quality, cinematic shot, detailed texture, 8k resolution.
```

## 一致性关键词

**人物/动物：**
```
same character as reference image,
stable appearance, preserve features,
consistent character design, same outfit as reference,
consistent lighting style
```

**物体/产品：**
```
same object as reference image,
stable appearance, preserve details,
consistent product design, consistent lighting style
```

**场景/地点：**
```
same environment as reference image,
stable atmosphere, preserve style,
consistent location design, consistent lighting style
```

## 参数要求
| 参数 | 值 |
|------|-----|
| reference_files[0] | subject_reference.png（必须） |
| reference_files[1] | 上一帧（frame 2+ 时） |
| aspect_ratio | "16:9" |
| resolution | "2K" |

## 风格强化关键词

| 风格 | 关键词 |
|------|--------|
| 吉卜力 | Ghibli style, soft lighting, hand-drawn animation |
| 赛博朋克 | Cyberpunk, neon lights, futuristic city |
| 写实 | Photorealistic, natural lighting |
| 水彩 | Watercolor painting, soft edges, pastel colors |
| 像素 | Pixel art, 8-bit style, retro gaming |
| 动漫 | Anime style, vibrant colors |
| 油画 | Oil painting style, rich textures |
| 极简 | Minimalist, clean lines |

## 注意事项
1. **串联生成**：必须逐帧生成，等上一帧完成后再生成下一帧
2. **双重参考**：每帧都用主体参考图 + 上一帧
3. **比例锁定**：必须使用 16:9 比例
