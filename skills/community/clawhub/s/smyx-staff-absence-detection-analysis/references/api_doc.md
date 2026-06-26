# 人员离岗实时监测 API 接口文档

## 接口概览

人员离岗实时监测功能依赖云端 API 服务进行计算机视觉分析，以下是 API 接口规范说明。

## 认证方式

- API Key 通过请求头 `Authorization: Bearer {api_key}` 传递
- 未配置 API Key 时使用默认共享配额

## 主要接口

### 1. 离岗监测分析接口

**URL**: `{base_url}/api/v1/ai-analysis/personnel-leave-post-detection`

**Method**: `POST`

**请求参数**:

- `input_type`: `file` 或 `url`
- `media_type`: `video` 或 `image`
- `confidence_threshold`: 置信度阈值，默认 0.5
- `absence_threshold`: 离岗判定阈值（秒），默认 300
- `scene_code`: `PERSONNEL_LEAVE_POST_MONITORING`（固定值）
- `open_id`: 用户标识

**响应格式**: JSON

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "request-id",
    "detection_time": "2026-04-15 10:30:00",
    "detection": {
      "post_status": "leave_post",
      "abnormal_absence_count": 2,
      "total_absence_duration": 650,
      "status_stats": [
        {
          "status": "on_duty",
          "count": 1,
          "total_duration": 1200
        },
        {
          "status": "leave_post",
          "count": 2,
          "total_duration": 650
        },
        {
          "status": "temporary_leave",
          "count": 1,
          "total_duration": 80
        }
      ]
    }
  }
}
```

### 2. 查询历史报告列表接口

**URL**: `{base_url}/api/v1/ai-analysis/list`

**Method**: `GET`

**请求参数**:

- `scene_code`: `PERSONNEL_LEAVE_POST_MONITORING`
- `open_id`: 用户标识
- `start_time`: 起始时间（可选）
- `end_time`: 结束时间（可选）

### 3. 获取报告详情接口

**URL**: `{base_url}/api/v1/ai-analysis/detail/{request_id}`

**Method**: `GET`

## 错误码说明

| 错误码  | 说明      |
|------|---------|
| 0    | 成功      |
| 1001 | 参数错误    |
| 1002 | 文件格式不支持 |
| 1003 | 文件过大    |
| 2001 | 认证失败    |
| 2002 | 配额不足    |
| 3001 | 分析失败    |
| 4001 | 记录不存在   |

## 注意事项

1. 最大支持文件大小：10MB
2. 支持视频格式：mp4、avi、mov
3. 支持图片格式：jpg、png、jpeg
4. 分析时间根据文件大小不同，通常在 3-30 秒
