# 子技能 08 · 剪辑与合成 edl
**来源**：drama-skills short-drama-edit（逐段写入出点理由、字幕逐字取自剧本、统一响度），video-use（转写加按需取帧，避免把所有帧都塞进上下文；剪辑点 30ms 音频淡化；EDL → 渲染 → 自评，最多 3 次），ffmpeg-skill（类型化工具、先 probe 再编辑再验证、不覆盖源文件），remotion-best-practices 和 hyperframes（程序化字幕、动效叠层、确定性渲染），claude-video-studio（-14 LUFS 母带、9:16 和 16:9 两种画幅各自排版、不直接裁切）。

## 目标
用一份 EDL 描述整条成片，按它确定性地渲染，再用实测数据验证。

## 方法
1. **clips**：每个 cut 挑出可用的区间，写 in_sec、out_sec，并在 reason 里写明为什么在这里进出（比如动作完成、视线落点、去掉生成首尾的瑕疵）。
2. **subtitles**：字幕文本**逐字**取自 story 里的 line，不改写。时间对齐台词音频。
3. **overlays**：系统面板、花字、图表这类叠层，复杂的用 remotion 或 hyperframes 做，简单字卡直接用 ffmpeg 的 drawtext。
4. **audio**：
   - 每个剪辑点做 fade_ms ≥ 30
   - 目标 -14 LUFS，真峰值 -1 dBTP
   - 渲染后实测，把结果写进 measured_lufs
5. **静帧段渲染**：ffmpeg 用 `zoompan` 实现推拉，用 `crop` 加表达式实现摇移；视差需要把前后景分层，用 remotion 或 hyperframes 分层位移。先把原图放大到输出分辨率的 1.5 倍再做 zoompan，避免抖动。
6. **渲染**：
   - engine=ffmpeg：concat、xfade，再 loudnorm 两遍
   - remotion / hyperframes：EDL 转成时间轴组件后再渲染
   - 渲染完用 ffprobe 测实际时长，写进 measured_duration_sec
6. **自评（进入 09 之前先做）**：在每个剪辑点前后各取帧，拼成帧条，检查画面跳变、爆音、字幕被遮挡。发现问题先在本阶段修，最多 3 次。
7. **多画幅**：每种画幅单独排版字幕和安全区，不要把横版直接裁成竖版。

## 常见错误码
SUB_NOT_VERBATIM、SRC_NOT_PRODUCED、TIMELINE_OFF、LOUDNESS、RENDER_DURATION、IN_OUT
