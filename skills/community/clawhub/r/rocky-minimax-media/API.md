# MiniMax API 文档

## 环境配置

插件需要设置环境变量 `MINIMAX_API_KEY`：

```bash
export MINIMAX_API_KEY=你的MiniMax_API_Key
```

## API 端点

| 功能 | 端点 | 模型 |
|------|------|------|
| 图片生成 | `POST /v1/image_generation` | `image-01` |
| 视频生成 | `POST /v1/video_generation` | `MiniMax-Hailuo-2.3` / `MiniMax-Hailuo-2.3-Fast` |
| TTS语音 | `POST /v1/t2a_v2` | `speech-2.8-hd` |
| 音乐生成 | `POST /v1/music_generation` | `music-2.6` / `music-2.5` |

## API Base URL

```
https://api.minimaxi.com
```

## 模型说明

### 图片模型
- `image-01` - 通用图片生成模型

### 视频模型
- `MiniMax-Hailuo-2.3` - 文生视频，肢体动作/物理表现全面升级
- `MiniMax-Hailuo-2.3-Fast` - 图生视频，生成速度更快

### TTS模型
- `speech-2.8-hd` - 高清语音合成

### 音乐模型
- `music-2.6` - 最新版本，音质更好
- `music-2.5` - 经典版本

## TTS 可用音色

| voice_id | 说明 |
|----------|------|
| `male-qn-qingse` | 男声-青年-青涩 |
| `female-tianmei` | 女声-甜妹 |
| `female-yujie` | 女声-御姐 |

## API Key格式

MiniMax API Key 通常以 `sk-cp-` 开头，这是 Coding Plan Key。

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1004 | 登录失败 |
| 2013 | 参数错误 |
| 2056 |额度用尽 |
| 2061 | Token Plan 不支持该模型 |
