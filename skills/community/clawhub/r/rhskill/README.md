# RHSkill - RunningHub API Skill for OpenClaw

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-blue)](https://openclaw.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

直接调用 RunningHub API 的 OpenClaw Skill，支持文生图、图生图、视频生成等 AI 任务。

## 特性

- 🎨 **文生图/图生图** - 基于 Qwen 等模型的图像生成
- 🎬 **视频生成** - 支持图生视频等高级功能
- ☁️ **智能存储** - 支持百度网盘、Google Drive 自动上传
- 🔗 **链式流程** - 支持多步骤工作流，URL 自动传递
- 🤖 **AUTO 决策** - 根据上下文自动选择存储方式

## 快速开始

### 安装

```bash
# 克隆到 OpenClaw skills 目录
git clone https://github.com/AIRix315/RHSkill.git ~/.openclaw/workspace/skills/runninghub-api

# 重启 OpenClaw 或刷新 skills
```

### 配置

1. **获取 RunningHub API Key**
   - 访问 https://www.runninghub.cn
   - 注册账号 → 个人中心 → API 控制台

2. **设置环境变量**
   ```bash
   export RUNNINGHUB_API_KEY="your-api-key"
   export RUNNINGHUB_BASE_URL="www.runninghub.cn"
   ```

3. **配置 OpenClaw**
   
   编辑 `~/.openclaw/openclaw.json`：
   ```json
   {
     "skills": {
       "entries": {
         "runninghub-api": {
           "enabled": true,
           "env": {
             "RUNNINGHUB_API_KEY": "your-api-key",
             "RUNNINGHUB_BASE_URL": "www.runninghub.cn"
           }
         }
       }
     }
   }
   ```

### 使用示例

```javascript
// 生成图片
rh_execute({
  alias: "qwen-text-to-image",
  params: { text: "一只可爱的猫咪" },
  storage: "none"
})

// 上传到百度网盘
rh_execute({
  alias: "qwen-text-to-image",
  params: { text: "美丽的风景" },
  storage: "cloud",
  cloudProvider: "bdpan",
  projectName: "my-project"
})
```

## 目录结构

```
{baseDir}/
├── SKILL.md                 # Skill 定义文件
├── README.md                # 本文件
├── LICENSE                  # MIT 许可证
├── scripts/
│   ├── rh-client.mjs       # API 客户端
│   ├── storage-handler.mjs # 存储处理
│   └── task-executor.mjs   # 任务执行器
├── references/
│   ├── shared-apps.json    # 共享 APP 清单
│   └── config-template.json # 配置模板
└── config/
    └── default.json        # 默认配置
```

## 存储模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `none` | 返回 RH 服务器 URL | 直接交付、链式流程 |
| `cloud` | 上传到网盘 | 需要保存、确认 |

### AUTO 决策

Skill 会根据上下文自动选择存储方式：
- 链式流程中间步骤 → `none`
- 明确要求保存 → `cloud`
- 默认 → `none`

## 支持的 APP

| 别名 | 类型 | 说明 |
|------|------|------|
| `qwen-text-to-image` | image | Qwen 文生图 |
| `qwen-image-to-image` | image | Qwen 图生图 |

更多 APP 可在 `references/shared-apps.json` 中添加。

## 依赖

- **必需**: Node.js 18+, RunningHub API Key
- **可选**: bdpan-storage Skill（百度网盘）
- **可选**: gog Skill（Google Drive）

## 相关项目

- [RHMCP](https://github.com/AIRix315/RHMCP) - RunningHub MCP Server
- [OpenClaw](https://openclaw.ai) - AI Agent 平台
- [ClawHub](https://clawhub.com) - Skill 市场

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 PR！
