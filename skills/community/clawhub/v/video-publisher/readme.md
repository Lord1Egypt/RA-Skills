# OpenClaw Video Publisher 🚀

**一键发布短视频到多个平台** - 自动化视频发布工具

支持抖音、快手、视频号、B站、小红书、YouTube、TikTok 等主流平台的批量发布。

---

## ✨ 核心功能

- 🎯 **多平台发布** - 一次上传，同步到 7+ 个平台
- 🔐 **统一授权管理** - 安全的 API 凭证配置
- 📝 **内容管理** - 标题、描述、标签、封面统一设置
- ⏰ **定时发布** - 支持预约发布时间
- 📊 **发布记录** - 追踪发布状态，保存平台链接
- 🔄 **失败重试** - 自动重试失败的发布任务
- 🎨 **批量操作** - 支持批量上传多个视频

---

## 🌍 支持的平台

| 平台 | 状态 | 说明 |
|------|------|------|
| 抖音 (Douyin) | ✅ | 开放平台 API |
| 快手 (Kuaishou) | ✅ | 开放平台 API |
| 视频号 (WeChat Channels) | ✅ | 企业微信 API |
| 哔哩哔哩 (Bilibili) | ✅ | 创作中心 API |
| 小红书 (Xiaohongshu) | ⏳ | API 申请中 |
| YouTube | ✅ | Google API |
| TikTok | ✅ | TikTok for Developers |

---

## 🚀 快速开始

### 1. 安装

```bash
# 通过 npm 安装
npm install -g openclaw-video-publisher

# 或者克隆项目
git clone https://github.com/ZhenRobotics/openclaw-video-publisher.git
cd openclaw-video-publisher
npm install
```

### 2. 配置平台凭证

```bash
# 复制配置模板
cp config/platforms.example.json config/platforms.json
cp .env.example .env

# 编辑配置文件，填入各平台的 API 凭证
nano config/platforms.json
```

### 3. 发布视频

```bash
# 发布单个视频到所有平台
./publish.sh my-video.mp4 \
  --title "我的视频标题" \
  --description "视频描述" \
  --tags "AI,技术,教程"

# 发布到指定平台
./publish.sh my-video.mp4 \
  --platforms "douyin,kuaishou,weixin" \
  --title "我的视频"

# 批量发布
./batch-publish.sh videos/*.mp4 \
  --config publish-config.json
```

---

## 📖 使用指南

### 单个视频发布

```bash
video-publish upload \
  --video /path/to/video.mp4 \
  --title "视频标题" \
  --description "视频描述" \
  --tags "标签1,标签2,标签3" \
  --cover /path/to/cover.jpg \
  --platforms "douyin,kuaishou" \
  --schedule "2024-12-25 18:00:00"
```

### 批量发布

创建配置文件 `publish-config.json`:

```json
{
  "videos": [
    {
      "path": "video1.mp4",
      "title": "视频1标题",
      "description": "视频1描述",
      "tags": ["AI", "技术"],
      "platforms": ["douyin", "kuaishou"]
    },
    {
      "path": "video2.mp4",
      "title": "视频2标题",
      "description": "视频2描述",
      "tags": ["教程", "分享"],
      "platforms": ["bilibili", "youtube"]
    }
  ]
}
```

然后执行：

```bash
video-publish batch --config publish-config.json
```

### 查看发布记录

```bash
# 查看所有发布记录
video-publish list

# 查看某个视频的发布状态
video-publish status video1.mp4

# 重试失败的发布
video-publish retry video1.mp4
```

---

## ⚙️ 配置说明

### 平台配置 (config/platforms.json)

```json
{
  "douyin": {
    "enabled": true,
    "client_key": "your-client-key",
    "client_secret": "your-client-secret",
    "access_token": "your-access-token"
  },
  "kuaishou": {
    "enabled": true,
    "app_id": "your-app-id",
    "app_secret": "your-app-secret"
  },
  "weixin": {
    "enabled": true,
    "corp_id": "your-corp-id",
    "corp_secret": "your-corp-secret"
  },
  "bilibili": {
    "enabled": true,
    "access_key": "your-access-key",
    "secret_key": "your-secret-key",
    "session_id": "your-session-id"
  },
  "youtube": {
    "enabled": true,
    "api_key": "your-api-key",
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "refresh_token": "your-refresh-token"
  }
}
```

### 环境变量 (.env)

```bash
# 默认发布平台（逗号分隔）
DEFAULT_PLATFORMS=douyin,kuaishou,weixin

# 是否自动重试失败的发布
AUTO_RETRY=true

# 重试次数
MAX_RETRY=3

# 日志级别
LOG_LEVEL=info
```

---

## 📁 项目结构

```
openclaw-video-publisher/
├── src/
│   ├── core/
│   │   ├── publisher.ts        # 核心发布逻辑
│   │   ├── uploader.ts         # 视频上传管理
│   │   └── scheduler.ts        # 定时任务管理
│   ├── platforms/
│   │   ├── douyin.ts           # 抖音适配器
│   │   ├── kuaishou.ts         # 快手适配器
│   │   ├── weixin.ts           # 视频号适配器
│   │   ├── bilibili.ts         # B站适配器
│   │   ├── youtube.ts          # YouTube适配器
│   │   └── tiktok.ts           # TikTok适配器
│   ├── utils/
│   │   ├── logger.ts           # 日志工具
│   │   ├── validator.ts        # 参数验证
│   │   └── database.ts         # 发布记录存储
│   └── cli/
│       └── index.ts            # CLI 入口
├── config/
│   ├── platforms.json          # 平台配置（需创建）
│   └── platforms.example.json  # 配置模板
├── examples/
│   ├── single-publish.sh       # 单个发布示例
│   └── batch-publish.json      # 批量发布示例
├── tests/
│   ├── test-douyin.ts
│   ├── test-kuaishou.ts
│   └── test-all.sh
├── publish.sh                  # 主入口脚本
├── batch-publish.sh            # 批量发布脚本
├── .env.example                # 环境变量模板
├── package.json
└── README.md
```

---

## 🔐 获取平台凭证

### 抖音开放平台
1. 访问 https://open.douyin.com/
2. 创建应用 → 获取 `client_key` 和 `client_secret`
3. 授权后获取 `access_token`

### 快手开放平台
1. 访问 https://open.kuaishou.com/
2. 创建应用 → 获取 `app_id` 和 `app_secret`

### 微信视频号
1. 访问 https://channels.weixin.qq.com/
2. 企业认证 → 获取 `corp_id` 和 `corp_secret`

### 哔哩哔哩
1. 访问 https://member.bilibili.com/
2. 创作中心 → API 设置 → 获取凭证

### YouTube
1. 访问 https://console.cloud.google.com/
2. 创建项目 → 启用 YouTube Data API v3
3. 创建 OAuth 2.0 凭证

---

## 🎯 使用场景

### 自媒体创作者
- 一次性发布视频到所有平台，节省时间
- 统一管理内容，避免重复操作

### 企业营销
- 批量发布产品宣传视频
- 定时发布营销内容

### 视频剪辑工作室
- 为客户自动分发视频到指定平台
- 保存发布记录，方便对账

---

## 📊 发布记录示例

发布记录保存在 `data/publish-history.json`:

```json
{
  "video1.mp4": {
    "title": "我的视频",
    "uploaded_at": "2024-03-10T10:00:00Z",
    "platforms": {
      "douyin": {
        "status": "success",
        "url": "https://www.douyin.com/video/1234567890",
        "video_id": "1234567890"
      },
      "kuaishou": {
        "status": "success",
        "url": "https://www.kuaishou.com/short-video/1234567890"
      },
      "bilibili": {
        "status": "failed",
        "error": "Token expired",
        "retry_count": 2
      }
    }
  }
}
```

---

## 🛠️ 开发指南

### 添加新平台

1. 创建平台适配器 `src/platforms/new-platform.ts`:

```typescript
import { BasePlatform } from './base';

export class NewPlatform extends BasePlatform {
  async upload(video: VideoFile, metadata: VideoMetadata) {
    // 实现上传逻辑
  }

  async getStatus(videoId: string) {
    // 查询视频状态
  }
}
```

2. 在 `src/core/publisher.ts` 中注册平台
3. 添加配置示例到 `config/platforms.example.json`
4. 编写测试用例

---

## ⚠️ 注意事项

1. **API 限流**: 各平台都有 API 调用限制，建议控制发布频率
2. **内容审核**: 部分平台需要内容审核，发布后不会立即上线
3. **凭证安全**: 不要将 `config/platforms.json` 和 `.env` 提交到 Git
4. **视频格式**: 建议使用 MP4 格式，分辨率 1080x1920 (竖屏)
5. **文件大小**: 注意各平台的文件大小限制

---

## 🐛 故障排查

### 上传失败
```bash
# 检查网络连接
curl -I https://open.douyin.com

# 验证凭证有效性
video-publish test --platform douyin

# 查看详细日志
LOG_LEVEL=debug video-publish upload video.mp4
```

### Token 过期
```bash
# 刷新 token
video-publish refresh-token --platform douyin
```

---

## 📝 更新日志

### v1.0.0 (2024-03-10)
- ✨ 初始版本
- ✅ 支持抖音、快手、视频号、B站、YouTube、TikTok
- ✅ 单个和批量发布
- ✅ 发布记录管理
- ✅ 失败重试机制

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- **GitHub**: https://github.com/ZhenRobotics/openclaw-video-publisher
- **文档**: https://github.com/ZhenRobotics/openclaw-video-publisher/wiki
- **问题反馈**: https://github.com/ZhenRobotics/openclaw-video-publisher/issues

---

**用 AI 发布视频，让内容触达更多人！** ✨🚀
