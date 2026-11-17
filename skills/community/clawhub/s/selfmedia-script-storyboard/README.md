# 脚本与分镜时间校准

根据用户指定的口播稿、SRT、音频、预览和现有 Timeline 校准时序。输入路径由用户任务提供；保留项目原生 Timeline schema、Composition ID、作品数据和事实，不假设固定本机目录，也不改写已确认的文案。

音频与字幕必须以实测时长为准。需要时使用已安装的 `ffprobe` 查询时长。若现有项目格式不同，按该项目 schema 操作；附带的帧时间示例只是一种可选的通用格式。

## 通用示例验证器

时间轴用帧表示，区间为左闭右开 `[start_frame, end_frame)`。验证器只读 JSON 和字幕，不改文件：

```bash
python3 scripts/validate_timeline.py examples/timeline.json \
  --voiceover-duration 2.8 --preview-duration 3.0 --captions examples/captions.srt
python3 scripts/self_test.py
```

它检查镜头编号、帧率、连续区间、口播/预览长度和字幕越界。它不分析视频画面，也不会判断口播是否准确；改动后仍需回看预览。

## 来源与许可

源技能仅为短篇时间校准指引，无随附第三方代码或素材。本候选去掉固定目录假设，并新增独立可选的 frame-based 校验合同。[来源记录](SOURCE-ORIGIN.md) · [MIT-0](LICENSE)
