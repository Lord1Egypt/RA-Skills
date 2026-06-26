# 视频片段生成（Step 3）

从首帧图片生成视频片段。

## 执行步骤

### 1. 读取故事脚本
从 `output/story_script.json` 读取 segment_count

### 2. 调用 gen_videos

**注意：每次最多 5 个请求，需分批生成**

分批策略：
- 4 段 → 1 批
- 8 段 → 2 批（5 + 3）
- 12 段 → 3 批（5 + 5 + 2）

### 3. 请求格式

```json
{
 "video_requests": [
 {
 "prompt": "[该段的 visual_desc，添加动态描述]",
 "output_file": "output/videos/segment_01.mp4",
 "image_file": "output/frames/frame_01.png",
 "reference_type": "first_frame",
 "duration": 6,
 "resolution": "768P"
 }
 ]
}
```

## 参数要求
| 参数 | 值 |
|------|-----|
| duration | 6 |
| resolution | "768P" |
| reference_type | "first_frame" |

## 注意事项
1. 时长统一：所有视频必须是 6 秒
2. 分辨率统一：所有视频必须是 768P
3. 分批生成：gen_videos 每次最多 5 个
4. 动态描述：prompt 中添加动作相关描述增强动态效果
