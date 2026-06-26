# video-gen

AI 视频生成 Skill，基于火山引擎 Doubao Seedance 模型，支持文生视频、图生视频、有声视频。

## 安装

### OpenClaw

```bash
# ClawHub 安装（推荐）
clawhub install video-gen

# Git 直接安装
cd /path/to/your/workspace/skills
git clone git@github.com:qiujiahong/video-gen.git video-gen
```

### Claude Code

```bash
cd ~/.claude/skills
git clone git@github.com:qiujiahong/video-gen.git video-gen
```

### OpenCode

```bash
cd ~/.opencode/skills
git clone git@github.com:qiujiahong/video-gen.git video-gen
```

## 环境变量配置

使用前需配置以下环境变量：

```bash
VIDEO_GEN_API_KEY=your-volcengine-api-key
VIDEO_GEN_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
```

## 获取 API Key

火山引擎方舟平台：https://console.volcengine.com/ark

1. 注册/登录火山引擎
2. 开通方舟大模型服务
3. 创建 API Key

## 支持的模式

- 文生视频
- 图+文生视频
- 图生视频（Base64）
- 有声视频-首帧
- 有声视频-首尾帧
- Seedance-Lite 参考图

## License

MIT
