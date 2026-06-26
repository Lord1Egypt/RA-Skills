---
name: runninghub_api
description: RunningHub AI Platform 直接调用 - 文生图、图生图、视频生成等，支持智能存储判断和链式工作流
homepage: https://github.com/AIRix315/RHSkill
metadata: { "openclaw": { "emoji": "🎨", "requires": { "env": ["RUNNINGHUB_API_KEY"], "config": ["runninghub.baseUrl"] }, "primaryEnv": "RUNNINGHUB_API_KEY" } }
---

# RunningHub API Skill

## 概述

直接调用 RunningHub API，支持生图、生视频、音频处理等 AI 任务。

**与 RHMCP 的关系**：
- RHMCP 是 MCP Server，提供 STDIO/HTTP 接口
- 本 Skill 直接复用 RHMCP 的 API Client，跳过 MCP 层，速度更快
- 支持 RHMCP 配置文件中定义的 APP

## 前置条件

1. **RunningHub 账号**
   - 注册：https://www.runninghub.cn（国内）或 https://www.runninghub.ai（国际）
   - 获取 API Key：个人中心 → API 控制台

2. **百度网盘**（可选，用于 cloud 存储）
   - 安装 bdpan-storage Skill
   - 执行登录：`bash ~/.agents/skills/bdpan-storage/scripts/login.sh`

3. **Google Drive**（可选，用于 cloud 存储）
   - 安装 gog Skill
   - 执行授权：`gog auth credentials /path/to/client_secret.json`

## 配置

### 环境变量

```bash
export RUNNINGHUB_API_KEY="your-api-key"
export RUNNINGHUB_BASE_URL="www.runninghub.cn"  # 或 www.runninghub.ai
```

### OpenClaw 配置

编辑 `~/.openclaw/openclaw.json`：

```json5
{
  skills: {
    entries: {
      "runninghub-api": {
        enabled: true,
        env: {
          RUNNINGHUB_API_KEY: "your-api-key",
          RUNNINGHUB_BASE_URL: "www.runninghub.cn",
        },
        config: {
          defaultStorage: "auto",      // auto/none/cloud
          defaultCloudProvider: "auto", // auto/bdpan/gog
        }
      }
    }
  }
}
```

## 存储模式

| 模式 | 说明 | 触发条件 |
|------|------|---------|
| `none` | 返回 RH 服务器 URL | 默认、直接交付、链式流程 |
| `cloud` | 上传到网盘 | 明确要求保存、需要确认 |
| ~~`local`~~ | ~~下载到本地~~ | ~~服务器不适用，禁用~~ |

### AUTO 决策逻辑

```javascript
if (storage === "auto") {
  if (链式流程 || 直接交付) → "none"
  else if (要求保存 || 需要确认) → "cloud"
  else → "none"
}

if (cloudProvider === "auto") {
  if (提到 Google/Sheet) → "gog"
  else → "bdpan"
}
```

### 路径规则

- **bdpan**: `runninghub/{projectName}/{timestamp}_{filename}`
- **gog**: `RunningHub/{projectName}/{timestamp}_{filename}`
- **项目名**: 用户指定 > 自动生成（`rh-{timestamp}`）

## 工具

### rh_list_apps

列出可用的 RunningHub APP。

```javascript
rh_list_apps({ refresh: false })
// 返回: { apps: [{ alias, appId, category, description }] }
```

### rh_execute

执行 APP 任务。

```javascript
rh_execute({
  alias: string,              // APP 别名
  params: Record<string, any>, // APP 参数
  storage?: "none" | "cloud" | "auto",
  cloudProvider?: "bdpan" | "gog" | "auto",
  projectName?: string,       // 项目名称
  mode?: "sync" | "async",    // 同步/异步
  timeout?: number            // 超时时间（秒）
})

// 返回: {
//   taskId: string,
//   status: "SUCCESS" | "PENDING",
//   outputs: [{
//     originalUrl: string,   // RH 服务器 URL
//     cloudUrl?: string      // 网盘 URL（cloud 模式）
//   }]
// }
```

### rh_query_task

查询任务状态（用于异步模式）。

```javascript
rh_query_task({ taskId: string })
// 返回: { taskId, status, outputs?, progress? }
```

## 使用示例

### 简单生图（none 模式）

```
用户: 生成一只可爱的猫咪

Agent 调用:
rh_execute({
  alias: "qwen-text-to-image",
  params: { text: "一只可爱的猫咪，卡通风格" },
  storage: "none"
})
// 返回 RH 服务器 URL
```

### 上传到百度网盘

```
用户: 生成一张风景图保存到网盘

Agent 调用:
rh_execute({
  alias: "qwen-text-to-image",
  params: { text: "美丽的风景" },
  storage: "cloud",
  cloudProvider: "bdpan",
  projectName: "landscape"
})
// 返回 bdpan://runninghub/landscape/...
```

### 链式流程（图生视频）

```
用户: 生成主角图片，然后用它生成视频

步骤1: 生成图片（storage: "none"）
const imageResult = await rh_execute({
  alias: "qwen-text-to-image",
  params: { text: "主角形象" },
  storage: "none"
});
const imageUrl = imageResult.outputs[0].originalUrl;

步骤2: 图生视频（使用上一步 URL）
rh_execute({
  alias: "image-to-video",
  params: { image: imageUrl, prompt: "奔跑动画" },
  storage: "cloud"
});
```

## 共享 APP 清单

内置共享测试 APP（来自 RHMCP 官方）：

| 别名 | APP ID | 类型 | 说明 |
|------|--------|------|------|
| qwen-text-to-image | 2037760725296357377 | image | Qwen 文生图 |
| qwen-image-to-image | 2037822548796252162 | image | Qwen 图生图 |

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| 提交任务失败 | APP 参数不匹配 | 检查 shared-apps.json 中的 inputs 配置 |
| bdpan 上传失败 | 未登录 | 执行 `bash scripts/login.sh` 重新登录 |
| 任务超时 | 执行时间过长 | 使用 `mode: "async"` 异步模式 |
| Token 过期 | 授权失效 | 重新登录或授权 |

## 扩展开发

### 添加新 APP

编辑 `references/shared-apps.json`：

```json
{
  "apps": {
    "my-new-app": {
      "appId": "your-app-id",
      "alias": "my-new-app",
      "category": "video",
      "description": "描述",
      "inputs": {
        "param1": { "nodeId": "1", "fieldName": "field1" }
      }
    }
  }
}
```

## 参考链接

- RHMCP GitHub: https://github.com/AIRix315/RHMCP
- RunningHub: https://www.runninghub.cn
- OpenClaw Docs: https://docs.openclaw.ai

## License

MIT
