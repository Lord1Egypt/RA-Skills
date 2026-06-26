# 短视频混剪自动化技能

> 基于 MoviePy 的批量视频生成工作流

---

## 📌 技能概述

**技能名称**: `short-video-auto-editing`

**版本**: 1.0.0

**适用场景**:
- 抖音/视频号/小红书短视频批量生成
- 门店宣传视频自动化
- 团购推广视频制作
- 多版本 A/B 测试视频

**核心能力**:
- ✅ 素材自动筛选与裁剪
- ✅ AI 配音生成（Edge TTS）
- ✅ 字幕自动同步
- ✅ 批量混剪输出
- ✅ 重复率控制（≤40%）

---

## 🎯 标准工作流

### Phase 1: 素材准备（10 分钟）

**素材库规范**:
```
~/视频素材/
├── 原始素材/          # 原始拍摄视频
│   ├── LCD_采耳/
│   ├── MUX_健身/
│   └── ...
├── 输出/              # 生成结果（自动排除）
└── 音频库/            # 预生成配音
```

**素材要求**:
- 格式：MP4/MOV
- 分辨率：≥1080p
- 时长：≥30 秒（便于裁剪）
- 数量：≥20 个（保证多样性）

**素材索引**:
```python
MATERIALS = [
    "/path/to/video1.mp4",
    "/path/to/video2.mp4",
    # ... 至少 20 个
]
```

---

### Phase 2: 文案创作（15 分钟）

**文案规范**:
- 口语化、自然流畅
- 包含门店信息 + 团购引导
- 避免绝对化用词
- 符合平台合规要求

**文案模板**（以采耳为例）:
```python
COPYWRITING = [
    """
    在常熟想找个地方好好放松一下
    老成都采耳馆开了有些年头了
    环境干净师傅手法也到位
    累了困了过来躺一会儿挺舒服的
    位置就在万达团购嘛左下角自己看哈
    """,
    # ... 至少 10 条独立文案
]
```

**文案库要求**:
- 数量：≥10 条
- 每条字数：60-100 字
- 时长：15-20 秒朗读
- 重复率：≤30%

---

### Phase 3: 配音生成（5 分钟）

**Edge TTS 配置**:
```python
import edge_tts

VOICES = {
    "晓晓": "zh-CN-XiaoxiaoNeural",      # 女声，温暖
    "云扬": "zh-CN-YunyangNeural",        # 男声，专业
    "云健": "zh-CN-YunjianNeural",        # 男声，活力
    "晓艺": "zh-CN-XiaoyiNeural",         # 女声，活泼
}

async def generate_audio(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
```

**配音轮换策略**:
- 4 种音色循环使用
- 避免同一文案重复音色
- 每条配音单独保存

---

### Phase 4: 视频生成（自动）

**核心脚本**:
```python
from moviepy import (
    VideoFileClip, AudioFileClip, TextClip,
    CompositeVideoClip, concatenate_videoclips, vfx
)

def generate_video(c文案，音色，素材索引，output_path):
    # 1. 生成配音
    audio_file = f"audio_{文案 id}_{音色}.mp3"
    generate_audio(文案，音色，audio_file)
    
    # 2. 加载音频获取时长
    audio = AudioFileClip(audio_file)
    duration = audio.duration
    
    # 3. 裁剪并拼接素材（3-4 秒/片段）
    clips = []
    current_time = 0
    for idx in 素材索引:
        if current_time >= duration:
            break
        clip = VideoFileClip(MATERIALS[idx])
        clip = clip.with_duration(min(3.5, clip.duration))
        clip = clip.with_effects([vfx.Resize(height=1920)])
        clip = clip.with_effects([vfx.Crop(
            x1=clip.w//2 - 540, y1=0, width=1080, height=1920
        )])
        clips.append(clip)
        current_time += clip.duration
    
    # 4. 拼接视频
    video = concatenate_videoclips(clips, method="compose")
    video = video.with_duration(duration)
    
    # 5. 生成字幕
    subtitles = generate_subtitles(文案，duration)
    subtitle_clips = []
    for start, end, text in subtitles:
        txt = TextClip(
            text=text,
            font='/System/Library/Fonts/STHeiti Light.ttc',
            font_size=50,
            color='white',
            stroke_color='black',
            stroke_width=2,
            duration=end - start
        )
        txt = txt.with_position(('center', video.h - 150)).with_start(start)
        subtitle_clips.append(txt)
    
    # 6. 合成
    final = CompositeVideoClip([video] + subtitle_clips)
    final = final.with_audio(audio)
    
    # 7. 导出
    final.write_videofile(
        output_path,
        codec='libx264',
        audio_codec='aac',
        fps=30,
        preset='medium',
        bitrate='5000k'
    )
```

---

### Phase 5: 质量控制（自动）

**自检清单**:
```python
def quality_check(video_path):
    clip = VideoFileClip(video_path)
    
    checks = {
        "时长": 15 <= clip.duration <= 20,
        "分辨率": clip.size == (1080, 1920),
        "帧率": clip.fps == 30,
        "有音频": clip.audio is not None,
        "文件大小": 5 <= os.path.getsize(video_path)/1024/1024 <= 15,
    }
    
    if not all(checks.values()):
        print(f"❌ 质量检查失败：{checks}")
        return False
    
    print(f"✅ 质量检查通过")
    return True
```

**重复率控制**:
```python
# 记录已用素材索引
used_materials = set()

def select_materials(文案 id, count=6):
    available = set(range(len(MATERIALS))) - used_materials
    selected = random.sample(available, count)
    used_materials.update(selected)
    
    # 如果素材用完，重置
    if len(used_materials) > len(MATERIALS) * 0.6:
        used_materials.clear()
    
    return selected
```

---

## 📊 出片规格

| 项目 | 标准值 |
|------|--------|
| **总时长** | 15-20 秒 |
| **分辨率** | 1080x1920 竖屏 (9:16) |
| **帧率** | 30 fps |
| **片段时长** | 3-4 秒/个 |
| **片段数量** | 5-6 个 |
| **重复率** | ≤40% |
| **配音** | Edge TTS（4 音色轮换） |
| **字幕** | 逐字对应，STHeiti 字体 |
| **编码** | H.264 + AAC |
| **文件大小** | 5-15 MB |

---

## 📁 文件结构

```
short-video-auto-editing/
├── SKILL.md                 # 技能文档
├── config.py                # 配置管理
├── materials.py             # 素材管理
├── copywriting.py           # 文案库
├── audio_gen.py             # 配音生成
├── video_edit.py            # 视频编辑
├── subtitle.py              # 字幕生成
├── quality_check.py         # 质量控制
├── batch_generate.py        # 批量生成
└── outputs/                 # 输出目录
```

---

## 🔧 批量生成脚本

```python
#!/usr/bin/env python3
# batch_generate.py

import asyncio
from datetime import datetime

async def batch_generate(count=10):
    """批量生成视频"""
    tasks = []
    
    for i in range(count):
        # 选择文案（轮换）
        文案 id = i % len(COPYWRITING)
        文案 = COPYWRITING[文案 id]
        
        # 选择音色（轮换）
        音色 key = list(VOICES.keys())[i % len(VOICES)]
        音色 = VOICES[音色 key]
        
        # 选择素材（避免重复）
        素材索引 = select_materials(文案 id)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%H%M%S")
        output = f"outputs/video_{文案 id}_{音色 key}_{timestamp}.mp4"
        
        # 创建任务
        task = asyncio.create_task(
            generate_video(文案，音色，素材索引，output)
        )
        tasks.append(task)
    
    # 等待所有任务完成
    await asyncio.gather(*tasks)
    print(f"✅ 批量生成完成：{count} 条视频")

if __name__ == '__main__':
    asyncio.run(batch_generate(10))
```

---

## ⚠️ 故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 最后几秒无画面 | 字幕时间轴超出视频 | 调整字幕匹配视频时长 |
| 最后几秒无声音 | 音频时长不足 | 使用 AudioFileClip 确保完整 |
| 画面静止 | 帧率不统一 | 统一 30 fps，用 `method="compose"` |
| 字幕有逗号 | 文案格式问题 | 移除逗号，逐行显示 |
| 字幕多行同时 | 时间轴错误 | 每条独立 `with_start()` |
| 文件过大 | 码率过高 | 调整 `bitrate='3000k'` |
| 重复率超标 | 素材轮换不足 | 增加素材库，优化轮换逻辑 |

---

## 📈 性能指标

| 指标 | 目标值 |
|------|--------|
| 单条生成时间 | <90 秒 |
| 批量生成（10 条） | <15 分钟 |
| 一次通过率 | ≥95% |
| 重复率 | ≤40% |
| 自动化程度 | ≥80% |

---

## 🔄 自我迭代机制

### 每次生成后

1. **记录素材使用**: 更新 `used_materials`
2. **检查重复率**: 确保 ≤40%
3. **收集反馈**: 记录用户满意/不满意的点
4. **优化文案**: 根据效果调整文案库

### 每周回顾

1. **爆款分析**: 哪些视频数据好？为什么？
2. **素材更新**: 补充新素材，淘汰旧素材
3. **文案优化**: 迭代文案库，提升转化率
4. **技术升级**: 关注 MoviePy 新版本特性

### 月度升级

- 新增音色（Edge TTS 更新）
- 优化剪辑逻辑
- 集成新平台规格（如小红书 3:4）
- 技能文档版本升级

---

## 📝 品牌模板

### LCD 老成都采耳馆

**文案特点**:
- 强调"万达店专享"
- 突出"50 分钟深度采耳 99.9 元"
- 引导"团购在左下角"

**色调**: 暖色系，放松氛围

---

### MUX 米欧克斯健身房

**文案特点**:
- 强调"5 家门店就近选择"
- 突出"专业教练 + 新器械"
- 引导"看左下角团购"

**色调**: 紫色/橙色品牌色，激励氛围

---

## 📝 变更记录

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-03-25 | v1.0 | 初始版本，基于 LCD 项目沉淀 |

---

*技能文档版本：1.0.0 | 最后更新：2026-03-25*
