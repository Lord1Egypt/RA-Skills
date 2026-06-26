---
name: features-media-video-audio
description: uni-app 视频与音频 chooseVideo、createVideoContext、getRecorderManager、createInnerAudioContext、getBackgroundAudioManager
---

# 视频与音频

## 视频

- **uni.chooseVideo(OBJECT)**：从相册选视频或拍摄。success 返回 tempFilePath、duration、size 等。部分平台支持 sourceType、maxDuration、camera 等。
- **uni.createVideoContext(videoId, componentInstance)**：创建 video 组件上下文，可控制播放、暂停、 seek、播放速率等。videoId 为 video 组件的 id；自定义组件内传 this。
- **uni.saveVideoToPhotosAlbum**、**uni.getVideoInfo**、**uni.compressVideo**、**uni.openVideoEditor** 等见官方「video」文档。

## 录音

- **uni.getRecorderManager()**：获取录音管理器。可 start、stop、onStart、onStop、onFrameRecorded 等。需用户授权录音；小程序需配置权限与隐私。

## 音频播放

- **uni.createInnerAudioContext()**：创建内部音频上下文，用于播放音频（src、play、pause、stop、seek 等）。不依赖 audio 组件。
- **uni.getBackgroundAudioManager()**：获取全局唯一背景音频管理器，支持后台播放、封面、进度等。同一时间仅一个背景音频。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/media/video
- https://uniapp.dcloud.net.cn/api/media/video-context
- https://uniapp.dcloud.net.cn/api/media/record-manager
- https://uniapp.dcloud.net.cn/api/media/audio-context
- https://uniapp.dcloud.net.cn/api/media/background-audio-manager
-->
