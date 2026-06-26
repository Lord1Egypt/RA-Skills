# OpenClaw Video Publisher Skill

**多平台视频发布工具 - AI Agent 使用指南**

---

## 🎯 Skill 简介

这是一个多平台视频发布工具，支持一键将视频上传到抖音、快手、视频号、B站、YouTube、TikTok 等平台。

### 核心功能
- 📤 多平台批量发布
- 🔐 统一的凭证管理
- 🔄 失败自动重试
- 📊 发布记录追踪
- ⚡ 命令行和编程接口

---

## 📋 依赖和要求

### 系统要求
- **Node.js**: >= 18.0.0
- **操作系统**: Linux, macOS, Windows
- **磁盘空间**: >= 100MB

### 外部 API 依赖
- 抖音开放平台 API (可选)
- 快手开放平台 API (可选)
- 微信视频号 API (可选)
- 哔哩哔哩创作中心 API (可选)
- YouTube Data API v3 (可选)
- TikTok for Developers API (可选)

### npm 依赖包
```json
{
  "dependencies": {
    "axios": "^1.6.0",
    "dotenv": "^16.3.1",
    "form-data": "^4.0.0",
    "commander": "^11.1.0"
  }
}
```

---

## 🚀 快速开始

### 安装

```bash
# 方式 1: npm 安装
npm install -g openclaw-video-publisher

# 方式 2: 克隆仓库
git clone https://github.com/ZhenRobotics/openclaw-video-publisher.git
cd openclaw-video-publisher
npm install
```

### 配置

```bash
# 1. 复制配置模板
cp config/platforms.example.json config/platforms.json
cp .env.example .env

# 2. 编辑 .env 填入 API 凭证
nano .env
```

### 使用

```bash
# 发布视频到抖音和快手
./publish.sh upload \
  --video my-video.mp4 \
  --title "我的视频" \
  --platforms "douyin,kuaishou"
```

---

## 🤖 AI Agent 使用指南

### 推荐使用场景

1. **批量发布内容**
   ```
   User: "帮我把 videos 目录下的所有视频发布到抖音和快手"
   Agent: 使用批量发布功能处理所有视频
   ```

2. **定时发布**
   ```
   User: "每天下午 6 点发布视频到所有平台"
   Agent: 创建定时任务，自动调用发布工具
   ```

3. **多平台管理**
   ```
   User: "查看今天发布了哪些视频"
   Agent: 读取发布历史记录并汇总
   ```

### Agent 调用示例

```typescript
// TypeScript Agent 示例
import { VideoPublisher } from 'openclaw-video-publisher';

async function publishVideo(videoPath: string, title: string) {
  const publisher = new VideoPublisher(
    platformsConfig,
    credentials
  );

  const result = await publisher.publish({
    video: {
      path: videoPath,
      filename: path.basename(videoPath),
      size: fs.statSync(videoPath).size,
    },
    metadata: {
      title: title,
      tags: ['AI', '技术'],
    },
    platforms: ['douyin', 'kuaishou'],
    retry: true,
    maxRetries: 3,
  });

  return result;
}
```

### Shell Script Agent 示例

```bash
#!/bin/bash
# Agent 批量发布脚本

VIDEO_DIR="./videos"
PLATFORMS="douyin,kuaishou,bilibili"

for video in "$VIDEO_DIR"/*.mp4; do
  echo "发布: $video"

  ./publish.sh upload \
    --video "$video" \
    --title "$(basename "$video" .mp4)" \
    --platforms "$PLATFORMS" \
    --retry

  sleep 5  # 避免 API 限流
done
```

---

## 🔐 安全性说明

### API 凭证管理
- ✅ 所有凭证存储在 `.env` 文件中
- ✅ `.env` 已加入 `.gitignore`，不会提交到版本控制
- ✅ 支持环境变量覆盖
- ⚠️ 请勿在日志中输出完整凭证

### 数据隐私
- ✅ 视频文件仅上传到用户配置的平台
- ✅ 发布记录存储在本地 `data/` 目录
- ✅ 不收集用户数据
- ✅ 不连接第三方服务器（除配置的平台 API）

### 网络安全
- ✅ 使用 HTTPS 连接平台 API
- ✅ 支持代理配置
- ✅ 遵循平台 API 频率限制

---

## 📊 API 频率限制

| 平台 | 每小时 | 每天 |
|------|--------|------|
| 抖音 | 100 | 1000 |
| 快手 | 100 | 1000 |
| 视频号 | 50 | 500 |
| B站 | 50 | 500 |
| YouTube | 1000 | 10000 |

建议：
- 使用 `--retry` 参数处理临时失败
- 批量发布时添加延迟（5-10秒）
- 监控 API 配额使用情况

---

## 📁 项目结构

```
openclaw-video-publisher/
├── src/
│   ├── core/           # 核心逻辑
│   ├── platforms/      # 平台适配器
│   ├── cli/            # CLI 入口
│   └── utils/          # 工具函数
├── config/
│   └── platforms.json  # 平台配置
├── examples/           # 使用示例
├── publish.sh          # 主入口脚本
├── .env               # 环境变量（需创建）
└── README.md          # 完整文档
```

---

## 🐛 常见问题

### Q1: 上传失败怎么办？
**A**: 检查以下几点：
1. API 凭证是否正确
2. 视频文件是否符合平台要求
3. 网络连接是否正常
4. 是否超过 API 限流

使用 `--retry` 参数自动重试。

### Q2: 如何添加新平台？
**A**:
1. 在 `src/platforms/` 创建新的适配器类
2. 在 `config/platforms.example.json` 添加配置
3. 在 `.env.example` 添加凭证模板
4. 提交 Pull Request

### Q3: 支持视频编辑吗？
**A**: 当前版本仅支持发布，不支持编辑。可以结合其他工具（如 ffmpeg）预处理视频。

---

## 🔗 相关资源

- **GitHub 仓库**: https://github.com/ZhenRobotics/openclaw-video-publisher
- **npm 包**: https://www.npmjs.com/package/openclaw-video-publisher
- **问题反馈**: https://github.com/ZhenRobotics/openclaw-video-publisher/issues
- **文档**: [README.md](README.md) | [QUICKSTART.md](QUICKSTART.md)

---

## 📝 验证信息

- **Skill 版本**: 1.0.0
- **最后更新**: 2024-03-10
- **作者**: justin
- **许可证**: MIT
- **验证仓库**: https://github.com/ZhenRobotics/openclaw-video-publisher
- **验证提交**: [待发布]

---

## 🙏 贡献

欢迎贡献代码！
1. Fork 仓库
2. 创建特性分支
3. 提交 Pull Request

---

**让 AI Agent 帮你自动发布视频！** ✨🚀
