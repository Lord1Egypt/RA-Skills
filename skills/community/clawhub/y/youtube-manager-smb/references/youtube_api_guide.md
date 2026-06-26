# YouTube Data API v3 使用指南

## API 准备步骤

### 1. 创建 Google Cloud 项目
1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用 **YouTube Data API v3**

### 2. 获取 API 凭据
#### API 密钥（用于公开数据）
- 适用于：频道统计、视频基本信息、公开播放列表
- 限制：无法访问私有数据、分析数据

#### OAuth 2.0 客户端 ID（用于完整功能）
- 适用于：视频上传、私有数据、完整分析数据
- 需要：用户授权

### 3. 环境变量配置
```bash
# 基础配置
YOUTUBE_API_KEY=your_api_key_here
YOUTUBE_CHANNEL_ID=UCxxxxxxxxxxxxxxxxxxxxxx

# 完整功能配置（OAuth）
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret
YOUTUBE_REFRESH_TOKEN=your_refresh_token
```

## API 端点说明

### 频道数据
- **channels.list**: 获取频道基本信息和统计
- 参数: `part=snippet,statistics,contentDetails`

### 视频数据  
- **videos.list**: 获取视频详细信息
- 参数: `part=snippet,statistics,contentDetails`

### 播放列表
- **playlists.list**: 获取播放列表
- **playlistItems.list**: 获取播放列表中的视频

### 分析数据（需要 OAuth）
- **analytics.reports**: 获取详细分析报告
- 支持维度: `views`, `likes`, `comments`, `shares`
- 支持指标: `views`, `watchTime`, `subscribersGained`

## 配额限制

- **channels.list**: 1 unit
- **videos.list**: 1 unit  
- **analytics.reports**: 5 units
- **videos.insert** (上传): 1600 units

每日配额: 10,000 units

## 最佳实践

1. **缓存数据**: 避免重复请求相同数据
2. **批量处理**: 使用批量 API 减少请求数量
3. **错误处理**: 实现重试机制处理配额限制
4. **数据验证**: 验证返回数据的完整性