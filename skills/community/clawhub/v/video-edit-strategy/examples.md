# 剪辑策略输出示例

## 示例 A：多素材混剪 — 30 秒抖音竖屏短视频

**场景**：用户提供 3 段视频素材 + 1 首 BGM，要求制作 30 秒抖音短视频。

```json
{
  "project": {
    "name": "美食探店30s",
    "platform": "douyin",
    "aspect_ratio": "9:16",
    "resolution": { "width": 1080, "height": 1920 },
    "fps": 30,
    "target_duration": 30,
    "style": "fast_pace",
    "output_path": "/tmp/ve_strategy/美食探店30s_final.mp4"
  },
  "materials": [
    {
      "id": "m1",
      "type": "video",
      "path": "/Users/me/videos/food_shop_exterior.mp4",
      "duration": 15.2,
      "width": 1920,
      "height": 1080,
      "codec": "h264",
      "fps": 30,
      "has_audio": true
    },
    {
      "id": "m2",
      "type": "video",
      "path": "/Users/me/videos/cooking_closeup.mp4",
      "duration": 45.8,
      "width": 1920,
      "height": 1080,
      "codec": "h264",
      "fps": 30,
      "has_audio": true
    },
    {
      "id": "m3",
      "type": "video",
      "path": "/Users/me/videos/dish_reveal.mp4",
      "duration": 20.1,
      "width": 1080,
      "height": 1920,
      "codec": "h264",
      "fps": 30,
      "has_audio": true
    },
    {
      "id": "m4",
      "type": "audio",
      "path": "/Users/me/music/upbeat_bgm.mp3",
      "duration": 120.0,
      "codec": "aac"
    }
  ],
  "timeline": [
    {
      "scene_id": "s1",
      "segment": "hook",
      "material_ref": "m3",
      "source_in": "00:00:02.000",
      "source_out": "00:00:05.000",
      "timeline_start": "00:00:00.000",
      "duration": 3.0,
      "speed": 1.0,
      "transition_in": { "type": "fade", "duration": 0.3 },
      "filters": [
        { "name": "saturation", "params": { "value": 1.3 } }
      ],
      "description": "成品菜特写作为开场 hook，色彩加饱和吸引眼球"
    },
    {
      "scene_id": "s2",
      "segment": "content",
      "material_ref": "m1",
      "source_in": "00:00:00.000",
      "source_out": "00:00:04.000",
      "timeline_start": "00:00:03.000",
      "duration": 3.0,
      "speed": 1.3,
      "transition_in": { "type": "fadewhite", "duration": 0.3 },
      "description": "店铺外景快速扫过，轻微加速制造节奏感"
    },
    {
      "scene_id": "s3",
      "segment": "content",
      "material_ref": "m2",
      "source_in": "00:00:05.000",
      "source_out": "00:00:08.000",
      "timeline_start": "00:00:06.000",
      "duration": 3.0,
      "speed": 1.0,
      "transition_in": { "type": "dissolve", "duration": 0.5 },
      "description": "备料切菜特写"
    },
    {
      "scene_id": "s4",
      "segment": "content",
      "material_ref": "m2",
      "source_in": "00:00:12.000",
      "source_out": "00:00:15.000",
      "timeline_start": "00:00:09.000",
      "duration": 2.0,
      "speed": 1.5,
      "transition_in": { "type": "cut", "duration": 0 },
      "description": "翻炒过程加速，快节奏卡点"
    },
    {
      "scene_id": "s5",
      "segment": "content",
      "material_ref": "m2",
      "source_in": "00:00:20.000",
      "source_out": "00:00:24.000",
      "timeline_start": "00:00:11.000",
      "duration": 4.0,
      "speed": 1.0,
      "transition_in": { "type": "cut", "duration": 0 },
      "description": "颠勺特写，正常速度展示技术"
    },
    {
      "scene_id": "s6",
      "segment": "content",
      "material_ref": "m2",
      "source_in": "00:00:30.000",
      "source_out": "00:00:35.000",
      "timeline_start": "00:00:15.000",
      "duration": 3.5,
      "speed": 1.4,
      "transition_in": { "type": "wipeleft", "duration": 0.4 },
      "description": "调味过程加速"
    },
    {
      "scene_id": "s7",
      "segment": "content",
      "material_ref": "m2",
      "source_in": "00:00:38.000",
      "source_out": "00:00:42.000",
      "timeline_start": "00:00:18.500",
      "duration": 4.0,
      "speed": 1.0,
      "transition_in": { "type": "dissolve", "duration": 0.5 },
      "description": "出锅装盘"
    },
    {
      "scene_id": "s8",
      "segment": "content",
      "material_ref": "m3",
      "source_in": "00:00:08.000",
      "source_out": "00:00:12.000",
      "timeline_start": "00:00:22.500",
      "duration": 4.0,
      "speed": 1.0,
      "transition_in": { "type": "fadewhite", "duration": 0.3 },
      "filters": [
        { "name": "contrast", "params": { "value": 1.15 } },
        { "name": "saturation", "params": { "value": 1.2 } }
      ],
      "description": "成品展示，加对比度和饱和度让菜品更诱人"
    },
    {
      "scene_id": "s9",
      "segment": "ending",
      "material_ref": "m3",
      "source_in": "00:00:14.000",
      "source_out": "00:00:18.000",
      "timeline_start": "00:00:26.500",
      "duration": 3.5,
      "speed": 0.8,
      "transition_in": { "type": "dissolve", "duration": 0.5 },
      "transition_out": { "type": "fade", "duration": 1.0 },
      "filters": [
        { "name": "vignette", "params": { "angle": 0.4 } }
      ],
      "description": "慢速收尾，暗角营造氛围感"
    }
  ],
  "audio": {
    "bgm": {
      "material_ref": "m4",
      "volume": 0.75,
      "fade_in": 0.5,
      "fade_out": 2.0,
      "start_offset": 10.0,
      "loop": false
    },
    "original_audio": {
      "keep": true,
      "volume": 0.2
    }
  },
  "text_overlays": [
    {
      "text": "这家店太绝了🔥",
      "timeline_start": "00:00:00.500",
      "timeline_end": "00:00:03.000",
      "position": "bottom_center",
      "font_size": 56,
      "font_color": "white",
      "bg_color": "black",
      "bg_opacity": 0.5
    },
    {
      "text": "📍 南京西路 xx 号",
      "timeline_start": "00:00:26.500",
      "timeline_end": "00:00:30.000",
      "position": "bottom_center",
      "font_size": 40,
      "font_color": "white"
    }
  ],
  "execution_plan": [
    {
      "step": 1,
      "action": "scale",
      "description": "将横屏素材 m1 裁切为 9:16 竖屏",
      "inputs": ["/Users/me/videos/food_shop_exterior.mp4"],
      "output": "/tmp/ve_strategy/m1_9x16.mp4",
      "params": { "width": 1080, "height": 1920, "method": "crop" },
      "skill_ref": "ffmpeg-video-editor"
    },
    {
      "step": 2,
      "action": "scale",
      "description": "将横屏素材 m2 裁切为 9:16 竖屏",
      "inputs": ["/Users/me/videos/cooking_closeup.mp4"],
      "output": "/tmp/ve_strategy/m2_9x16.mp4",
      "params": { "width": 1080, "height": 1920, "method": "crop" },
      "skill_ref": "ffmpeg-video-editor"
    },
    {
      "step": 3,
      "action": "cut",
      "description": "从 m3 中截取 hook 片段（2s-5s）",
      "inputs": ["/Users/me/videos/dish_reveal.mp4"],
      "output": "/tmp/ve_strategy/s1_hook.mp4",
      "params": { "start": "00:00:02.000", "end": "00:00:05.000" },
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 4,
      "action": "cut",
      "description": "从 m1 中截取店铺外景（0s-4s）",
      "inputs": ["/tmp/ve_strategy/m1_9x16.mp4"],
      "output": "/tmp/ve_strategy/s2_exterior.mp4",
      "params": { "start": "00:00:00.000", "end": "00:00:04.000" },
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 5,
      "action": "speed",
      "description": "将店铺外景加速 1.3x",
      "inputs": ["/tmp/ve_strategy/s2_exterior.mp4"],
      "output": "/tmp/ve_strategy/s2_fast.mp4",
      "params": { "rate": 1.3 },
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 6,
      "action": "cut",
      "description": "截取 m2 的多个精彩片段并分别变速",
      "inputs": ["/tmp/ve_strategy/m2_9x16.mp4"],
      "output": "/tmp/ve_strategy/s3_prep.mp4",
      "params": { "start": "00:00:05.000", "end": "00:00:08.000" },
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 7,
      "action": "cut",
      "description": "截取翻炒片段",
      "inputs": ["/tmp/ve_strategy/m2_9x16.mp4"],
      "output": "/tmp/ve_strategy/s4_stirfry.mp4",
      "params": { "start": "00:00:12.000", "end": "00:00:15.000" },
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 8,
      "action": "speed",
      "description": "翻炒片段加速 1.5x",
      "inputs": ["/tmp/ve_strategy/s4_stirfry.mp4"],
      "output": "/tmp/ve_strategy/s4_fast.mp4",
      "params": { "rate": 1.5 },
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 9,
      "action": "merge",
      "description": "按时间线顺序合并所有片段（无转场版本）",
      "inputs": [
        "/tmp/ve_strategy/s1_hook.mp4",
        "/tmp/ve_strategy/s2_fast.mp4",
        "/tmp/ve_strategy/s3_prep.mp4",
        "/tmp/ve_strategy/s4_fast.mp4"
      ],
      "output": "/tmp/ve_strategy/merged_no_fx.mp4",
      "params": {},
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 10,
      "action": "add_audio",
      "description": "混合 BGM（75%音量）和原声（20%音量），BGM 跳过前 10s 前奏",
      "inputs": [
        "/tmp/ve_strategy/merged_no_fx.mp4",
        "/Users/me/music/upbeat_bgm.mp3"
      ],
      "output": "/tmp/ve_strategy/merged_with_audio.mp4",
      "params": {
        "mode": "mix",
        "volume_main": 0.2,
        "volume_overlay": 0.75,
        "fade_in": 0.5,
        "fade_out": 2.0
      },
      "skill_ref": "ffmpeg-video-editor"
    },
    {
      "step": 11,
      "action": "add_text",
      "description": "添加开场文字和收尾地址",
      "inputs": ["/tmp/ve_strategy/merged_with_audio.mp4"],
      "output": "/tmp/ve_strategy/美食探店30s_final.mp4",
      "params": {
        "text": "这家店太绝了",
        "position": "bottom_center",
        "font_size": 56,
        "font_color": "white",
        "start": "00:00:00.500",
        "end": "00:00:03.000"
      },
      "skill_ref": "ffmpeg-video-editor"
    }
  ]
}
```

---

## 示例 B：图文混剪 — 5 张图片 + 配音

**场景**：用户有 5 张产品图片和 1 段配音旁白，要求做一个 20 秒的小红书种草视频。

```json
{
  "project": {
    "name": "好物推荐20s",
    "platform": "xiaohongshu",
    "aspect_ratio": "9:16",
    "resolution": { "width": 1080, "height": 1920 },
    "fps": 30,
    "target_duration": 20,
    "style": "narrative",
    "output_path": "/tmp/ve_strategy/好物推荐20s_final.mp4"
  },
  "materials": [
    { "id": "m1", "type": "image", "path": "/Users/me/photos/product_01.jpg", "width": 3000, "height": 4000 },
    { "id": "m2", "type": "image", "path": "/Users/me/photos/product_02.jpg", "width": 3000, "height": 4000 },
    { "id": "m3", "type": "image", "path": "/Users/me/photos/product_03.jpg", "width": 3000, "height": 4000 },
    { "id": "m4", "type": "image", "path": "/Users/me/photos/product_detail.jpg", "width": 4000, "height": 3000 },
    { "id": "m5", "type": "image", "path": "/Users/me/photos/product_lifestyle.jpg", "width": 3000, "height": 4000 },
    { "id": "m6", "type": "audio", "path": "/Users/me/audio/voiceover.mp3", "duration": 18.5, "codec": "aac" }
  ],
  "timeline": [
    {
      "scene_id": "s1",
      "segment": "hook",
      "material_ref": "m1",
      "source_in": "00:00:00.000",
      "source_out": "00:00:00.000",
      "timeline_start": "00:00:00.000",
      "duration": 3.0,
      "transition_in": { "type": "fade", "duration": 0.5 },
      "filters": [
        { "name": "crop_to_ratio", "params": { "ratio": "9:16" } }
      ],
      "description": "产品正面图作为封面 hook"
    },
    {
      "scene_id": "s2",
      "segment": "content",
      "material_ref": "m2",
      "source_in": "00:00:00.000",
      "source_out": "00:00:00.000",
      "timeline_start": "00:00:03.000",
      "duration": 4.0,
      "transition_in": { "type": "slideleft", "duration": 0.6 },
      "filters": [
        { "name": "crop_to_ratio", "params": { "ratio": "9:16" } }
      ],
      "description": "产品侧面图，滑动转场"
    },
    {
      "scene_id": "s3",
      "segment": "content",
      "material_ref": "m3",
      "source_in": "00:00:00.000",
      "source_out": "00:00:00.000",
      "timeline_start": "00:00:07.000",
      "duration": 4.0,
      "transition_in": { "type": "dissolve", "duration": 0.5 },
      "filters": [
        { "name": "crop_to_ratio", "params": { "ratio": "9:16" } }
      ],
      "description": "产品使用场景"
    },
    {
      "scene_id": "s4",
      "segment": "content",
      "material_ref": "m4",
      "source_in": "00:00:00.000",
      "source_out": "00:00:00.000",
      "timeline_start": "00:00:11.000",
      "duration": 4.0,
      "transition_in": { "type": "wipeup", "duration": 0.4 },
      "filters": [
        { "name": "crop_to_ratio", "params": { "ratio": "9:16" } },
        { "name": "saturation", "params": { "value": 1.15 } }
      ],
      "description": "细节特写，微增饱和度突出质感"
    },
    {
      "scene_id": "s5",
      "segment": "ending",
      "material_ref": "m5",
      "source_in": "00:00:00.000",
      "source_out": "00:00:00.000",
      "timeline_start": "00:00:15.000",
      "duration": 5.0,
      "transition_in": { "type": "dissolve", "duration": 0.8 },
      "transition_out": { "type": "fade", "duration": 1.0 },
      "filters": [
        { "name": "crop_to_ratio", "params": { "ratio": "9:16" } },
        { "name": "vignette", "params": { "angle": 0.3 } }
      ],
      "description": "生活方式图收尾，暗角增加氛围"
    }
  ],
  "audio": {
    "voiceover": {
      "material_ref": "m6",
      "volume": 1.0,
      "timeline_start": "00:00:00.500"
    },
    "original_audio": {
      "keep": false
    }
  },
  "text_overlays": [
    {
      "text": "这个真的绝了!!",
      "timeline_start": "00:00:00.000",
      "timeline_end": "00:00:03.000",
      "position": "top_center",
      "font_size": 52,
      "font_color": "white",
      "bg_color": "#FF4757",
      "bg_opacity": 0.85
    },
    {
      "text": "点击主页看更多好物",
      "timeline_start": "00:00:16.000",
      "timeline_end": "00:00:20.000",
      "position": "bottom_center",
      "font_size": 40,
      "font_color": "white"
    }
  ],
  "execution_plan": [
    {
      "step": 1,
      "action": "scale",
      "description": "将 5 张图片统一缩放裁切为 1080x1920",
      "inputs": [
        "/Users/me/photos/product_01.jpg",
        "/Users/me/photos/product_02.jpg",
        "/Users/me/photos/product_03.jpg",
        "/Users/me/photos/product_detail.jpg",
        "/Users/me/photos/product_lifestyle.jpg"
      ],
      "output": "/tmp/ve_strategy/images_scaled/",
      "params": { "width": 1080, "height": 1920, "method": "crop" },
      "skill_ref": "ffmpeg-video-editor"
    },
    {
      "step": 2,
      "action": "convert",
      "description": "将每张图片转为 3-5 秒静态视频片段",
      "inputs": ["/tmp/ve_strategy/images_scaled/"],
      "output": "/tmp/ve_strategy/clips/",
      "params": { "durations": [3.0, 4.0, 4.0, 4.0, 5.0] },
      "skill_ref": "ffmpeg-video-editor"
    },
    {
      "step": 3,
      "action": "xfade",
      "description": "按 timeline 定义的转场效果拼接所有片段",
      "inputs": [
        "/tmp/ve_strategy/clips/s1.mp4",
        "/tmp/ve_strategy/clips/s2.mp4",
        "/tmp/ve_strategy/clips/s3.mp4",
        "/tmp/ve_strategy/clips/s4.mp4",
        "/tmp/ve_strategy/clips/s5.mp4"
      ],
      "output": "/tmp/ve_strategy/merged_with_transitions.mp4",
      "params": {
        "transitions": [
          { "transition": "slideleft", "duration": 0.6, "offset": 2.4 },
          { "transition": "dissolve", "duration": 0.5, "offset": 6.5 },
          { "transition": "wipeup", "duration": 0.4, "offset": 10.6 },
          { "transition": "dissolve", "duration": 0.8, "offset": 14.2 }
        ]
      },
      "skill_ref": "ffmpeg-video-editor"
    },
    {
      "step": 4,
      "action": "add_audio",
      "description": "叠加配音旁白",
      "inputs": [
        "/tmp/ve_strategy/merged_with_transitions.mp4",
        "/Users/me/audio/voiceover.mp3"
      ],
      "output": "/tmp/ve_strategy/with_voiceover.mp4",
      "params": { "mode": "replace", "volume_overlay": 1.0 },
      "skill_ref": "ffmpeg-video-editor"
    },
    {
      "step": 5,
      "action": "add_text",
      "description": "添加标题和 CTA 文字",
      "inputs": ["/tmp/ve_strategy/with_voiceover.mp4"],
      "output": "/tmp/ve_strategy/好物推荐20s_final.mp4",
      "params": {
        "text": "这个真的绝了!!",
        "position": "top_center",
        "font_size": 52,
        "font_color": "white",
        "start": "00:00:00.000",
        "end": "00:00:03.000"
      },
      "skill_ref": "ffmpeg-video-editor"
    }
  ]
}
```

---

## 示例 C：长视频精华提取 — 单素材重新编排

**场景**：用户有一段 5 分钟的 vlog 原始素材，要求提取精华做 30 秒快剪。

```json
{
  "project": {
    "name": "vlog精华30s",
    "platform": "douyin",
    "aspect_ratio": "9:16",
    "resolution": { "width": 1080, "height": 1920 },
    "fps": 30,
    "target_duration": 30,
    "style": "fast_pace",
    "output_path": "/tmp/ve_strategy/vlog精华30s_final.mp4"
  },
  "materials": [
    {
      "id": "m1",
      "type": "video",
      "path": "/Users/me/videos/vlog_raw.mp4",
      "duration": 302.5,
      "width": 1920,
      "height": 1080,
      "codec": "h264",
      "fps": 30,
      "has_audio": true
    }
  ],
  "timeline": [
    {
      "scene_id": "s1",
      "segment": "hook",
      "material_ref": "m1",
      "source_in": "00:03:45.000",
      "source_out": "00:03:48.000",
      "timeline_start": "00:00:00.000",
      "duration": 3.0,
      "speed": 1.0,
      "transition_in": { "type": "fade", "duration": 0.3 },
      "description": "高潮片段前置作为 hook —— 日落海边跳跃瞬间"
    },
    {
      "scene_id": "s2",
      "segment": "content",
      "material_ref": "m1",
      "source_in": "00:00:10.000",
      "source_out": "00:00:16.000",
      "timeline_start": "00:00:03.000",
      "duration": 4.0,
      "speed": 1.5,
      "transition_in": { "type": "fadewhite", "duration": 0.3 },
      "description": "出门准备，加速推进节奏"
    },
    {
      "scene_id": "s3",
      "segment": "content",
      "material_ref": "m1",
      "source_in": "00:00:45.000",
      "source_out": "00:00:49.000",
      "timeline_start": "00:00:07.000",
      "duration": 2.5,
      "speed": 1.6,
      "transition_in": { "type": "cut", "duration": 0 },
      "description": "驾车出发，加速"
    },
    {
      "scene_id": "s4",
      "segment": "content",
      "material_ref": "m1",
      "source_in": "00:01:20.000",
      "source_out": "00:01:25.000",
      "timeline_start": "00:00:09.500",
      "duration": 3.0,
      "speed": 1.6,
      "transition_in": { "type": "wipeleft", "duration": 0.4 },
      "description": "到达海边，第一眼海景"
    },
    {
      "scene_id": "s5",
      "segment": "climax",
      "material_ref": "m1",
      "source_in": "00:02:00.000",
      "source_out": "00:02:06.000",
      "timeline_start": "00:00:12.500",
      "duration": 6.0,
      "speed": 1.0,
      "transition_in": { "type": "dissolve", "duration": 0.5 },
      "description": "海边漫步，正常速度享受画面"
    },
    {
      "scene_id": "s6",
      "segment": "climax",
      "material_ref": "m1",
      "source_in": "00:02:30.000",
      "source_out": "00:02:33.000",
      "timeline_start": "00:00:18.500",
      "duration": 3.0,
      "speed": 0.7,
      "transition_in": { "type": "cut", "duration": 0 },
      "filters": [
        { "name": "saturation", "params": { "value": 1.3 } }
      ],
      "description": "浪花拍岸慢放，增加饱和度"
    },
    {
      "scene_id": "s7",
      "segment": "climax",
      "material_ref": "m1",
      "source_in": "00:03:45.000",
      "source_out": "00:03:50.000",
      "timeline_start": "00:00:21.500",
      "duration": 5.0,
      "speed": 0.8,
      "transition_in": { "type": "dissolve", "duration": 0.5 },
      "description": "日落跳跃（完整版），慢速呈现"
    },
    {
      "scene_id": "s8",
      "segment": "ending",
      "material_ref": "m1",
      "source_in": "00:04:30.000",
      "source_out": "00:04:36.000",
      "timeline_start": "00:00:26.500",
      "duration": 3.5,
      "speed": 0.8,
      "transition_in": { "type": "dissolve", "duration": 0.8 },
      "transition_out": { "type": "fadeblack", "duration": 1.5 },
      "filters": [
        { "name": "vignette", "params": { "angle": 0.5 } },
        { "name": "colorbalance", "params": { "rs": 0.1, "gs": -0.05, "bs": -0.1 } }
      ],
      "description": "暮色归途，暗角 + 暖色调收尾"
    }
  ],
  "audio": {
    "original_audio": {
      "keep": true,
      "volume": 0.15
    }
  },
  "text_overlays": [
    {
      "text": "一个人的海边日落",
      "timeline_start": "00:00:00.000",
      "timeline_end": "00:00:03.000",
      "position": "center",
      "font_size": 60,
      "font_color": "white",
      "bg_color": "black",
      "bg_opacity": 0.4
    }
  ],
  "execution_plan": [
    {
      "step": 1,
      "action": "extract_frame",
      "description": "提取 hook 帧用于预览确认",
      "inputs": ["/Users/me/videos/vlog_raw.mp4"],
      "output": "/tmp/ve_strategy/hook_preview.jpg",
      "params": { "time": "00:03:46.000" },
      "skill_ref": "video-frames"
    },
    {
      "step": 2,
      "action": "scale",
      "description": "将 16:9 原始素材裁切为 9:16 竖屏",
      "inputs": ["/Users/me/videos/vlog_raw.mp4"],
      "output": "/tmp/ve_strategy/vlog_9x16.mp4",
      "params": { "width": 1080, "height": 1920, "method": "crop" },
      "skill_ref": "ffmpeg-video-editor"
    },
    {
      "step": 3,
      "action": "cut",
      "description": "裁剪 8 个精华片段",
      "inputs": ["/tmp/ve_strategy/vlog_9x16.mp4"],
      "output": "/tmp/ve_strategy/clips/s1.mp4",
      "params": { "start": "00:03:45.000", "end": "00:03:48.000" },
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 4,
      "action": "cut",
      "description": "裁剪出门准备片段",
      "inputs": ["/tmp/ve_strategy/vlog_9x16.mp4"],
      "output": "/tmp/ve_strategy/clips/s2.mp4",
      "params": { "start": "00:00:10.000", "end": "00:00:16.000" },
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 5,
      "action": "speed",
      "description": "出门准备片段加速 1.5x",
      "inputs": ["/tmp/ve_strategy/clips/s2.mp4"],
      "output": "/tmp/ve_strategy/clips/s2_fast.mp4",
      "params": { "rate": 1.5 },
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 6,
      "action": "speed",
      "description": "浪花片段减速 0.7x",
      "inputs": ["/tmp/ve_strategy/clips/s6.mp4"],
      "output": "/tmp/ve_strategy/clips/s6_slow.mp4",
      "params": { "rate": 0.7 },
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 7,
      "action": "merge",
      "description": "合并所有处理后的片段",
      "inputs": [
        "/tmp/ve_strategy/clips/s1.mp4",
        "/tmp/ve_strategy/clips/s2_fast.mp4",
        "/tmp/ve_strategy/clips/s3.mp4",
        "/tmp/ve_strategy/clips/s4.mp4",
        "/tmp/ve_strategy/clips/s5.mp4",
        "/tmp/ve_strategy/clips/s6_slow.mp4",
        "/tmp/ve_strategy/clips/s7.mp4",
        "/tmp/ve_strategy/clips/s8.mp4"
      ],
      "output": "/tmp/ve_strategy/merged_raw.mp4",
      "params": {},
      "skill_ref": "ffmpeg-cli"
    },
    {
      "step": 8,
      "action": "filter",
      "description": "对收尾段应用暖色调色",
      "inputs": ["/tmp/ve_strategy/merged_raw.mp4"],
      "output": "/tmp/ve_strategy/color_graded.mp4",
      "params": {
        "filters": [
          { "name": "colorbalance", "params": { "rs": 0.1, "gs": -0.05, "bs": -0.1 } }
        ],
        "apply_range": { "start": "00:00:26.500", "end": "00:00:30.000" }
      },
      "skill_ref": "ffmpeg-video-editor"
    },
    {
      "step": 9,
      "action": "add_text",
      "description": "添加标题文字",
      "inputs": ["/tmp/ve_strategy/color_graded.mp4"],
      "output": "/tmp/ve_strategy/with_text.mp4",
      "params": {
        "text": "一个人的海边日落",
        "position": "center",
        "font_size": 60,
        "font_color": "white",
        "start": "00:00:00.000",
        "end": "00:00:03.000"
      },
      "skill_ref": "ffmpeg-video-editor"
    },
    {
      "step": 10,
      "action": "add_audio",
      "description": "调整原声音量为 15%",
      "inputs": ["/tmp/ve_strategy/with_text.mp4"],
      "output": "/tmp/ve_strategy/vlog精华30s_final.mp4",
      "params": { "mode": "adjust", "volume_main": 0.15 },
      "skill_ref": "ffmpeg-video-editor"
    }
  ]
}
```
