# 视频拼接与音乐合成（Step 5）

使用 FFmpeg 将视频片段拼接并叠加背景音乐。

## 执行步骤

### 步骤1: 获取片段数量
```bash
segment_count=$(ls output/videos/segment_*.mp4 | wc -l)
```

### 步骤2: 统一视频分辨率
```bash
for i in $(seq -w 1 $segment_count); do
 ffmpeg -y -i output/videos/segment_${i}.mp4 \
 -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" \
 -c:v libx264 -preset fast -crf 23 \
 -an \
 output/merged/scaled_${i}.mp4
done
```

### 步骤3: 创建拼接列表
```bash
rm -f output/merged/filelist.txt
for i in $(seq -w 1 $segment_count); do
 echo "file 'scaled_${i}.mp4'" >> output/merged/filelist.txt
done
```

### 步骤4: 拼接视频
```bash
ffmpeg -y -f concat -safe 0 -i output/merged/filelist.txt \
 -c copy output/merged/video_only.mp4
```

### 步骤5: 叠加背景音乐
```bash
ffmpeg -y -i output/merged/video_only.mp4 \
 -i output/bgm.mp3 \
 -c:v copy -c:a aac \
 -map 0:v:0 -map 1:a:0 \
 -shortest \
 output/final_video.mp4
```

### 步骤6: 验证输出
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output/final_video.mp4
```
预期 = segment_count × 6 秒

## 参数说明
| 参数 | 说明 |
|------|------|
| -vf scale=1280:720 | 强制缩放至720p |
| -c:v libx264 | 使用H.264编码 |
| -an | 移除音频轨道 |
| -f concat | 使用concat模式拼接 |
| -map 0:v:0 | 使用第一个输入的视频 |
| -map 1:a:0 | 使用第二个输入的音频 |
| -shortest | 以较短的流为准 |

## 注意事项
1. 分辨率统一：确保所有片段为1280x720
2. 先拼后叠：先拼接视频，再叠加 BGM
3. BGM 时长：应等于视频总时长
