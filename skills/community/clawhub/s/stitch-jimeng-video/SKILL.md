---
name: jimeng-video-gen
description: |
  即梦AI视频生成3.0 1080P。通过火山引擎即梦AI API生成视频（图生视频-首尾帧模式）。
  触发词：即梦、极梦、视频生成、图生视频、首尾帧、火山引擎视频
---

# 即梦AI 视频生成3.0 1080P

通过火山引擎即梦AI API生成视频（图生视频-首尾帧模式）。

## 前置要求

在环境变量或 `.env` 中配置：
```bash
export VOLC_ACCESS_KEY="你的 Access Key ID"
export VOLC_SECRET_KEY="你的 Secret Access Key"
```

## 使用方式

```bash
python3 {baseDir}/scripts/jimeng_video.py \
  --prompt "镜头缓缓推进，画面从冬天的枯树过渡到春天的花开" \
  --first "/path/to/start.jpg" \
  --last "/path/to/end.jpg"
```

## 参数

| 参数 | 说明 | 必填 |
|------|------|------|
| --prompt | 视频描述（建议400字以内） | 是 |
| --first | 首帧图片路径或URL | 是 |
| --last | 尾帧图片路径或URL | 是 |
| --seed | 随机种子（默认-1随机） | 否 |
| --output | 输出文件路径 | 否 |
| --no-poll | 只提交不轮询 | 否 |

## API 信息

- 端点：`https://visual.volcengineapi.com`
- 提交任务 Action：`CVSync2AsyncSubmitTask`
- 查询任务 Action：`CVSync2AsyncGetResult`
- req_key：`jimeng_i2v_first_tail_v30_1080`
- 认证：火山引擎 HMAC-SHA256 签名（SDK 自动处理）
