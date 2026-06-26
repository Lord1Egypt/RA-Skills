---
name: runninghub
description: RunningHub - 云端 ComfyUI 平台，用于创建 AI 应用和工作流。支持文生图、文生视频、AI 视频合成等。国内版 runninghub.cn，国际版 runninghub.ai。
---

# RunningHub Skill

## 当使用

- 用户要求使用 ComfyUI 生成图片/视频
- 调用 RunningHub API 执行 AI 工作流
- 管理 RunningHub 工作流和应用
- 文生图、文生视频、视频合成等 AI 生成任务

## 平台版本

| 版本 | 域名 | 说明 |
|:---|:---|:---|
| 🇨🇳 国内版 | https://www.runninghub.cn | 中文界面，访问快 |
| 🌍 国际版 | https://www.runninghub.ai | 英文界面，全球服务 |

## 核心功能

| 功能 | 说明 |
|:---|:---|
| 执行工作流 | 通过 API 调用运行 ComfyUI 工作流 |
| 账户管理 | 查询账户余额、套餐信息 |
| 工作流管理 | 获取、创建、发布工作流 |
| 模型管理 | 访问预装模型库 |
| API 调用 | 批量执行 AI 生成任务 |

## 使用方式

### 1. 获取 API Key

1. 访问 https://www.runninghub.cn
2. 登录账号 → 个人中心 → API 调用
3. 创建 API Key

### 2. API 端点

根据使用版本选择对应的 API 地址：

| 功能 | 国内版端点 | 国际版端点 |
|:---|:---|:---|
| 执行工作流 | https://open.runninghub.cn/api/v1/run | https://open.runninghub.ai/api/v1/run |
| 查询任务状态 | https://open.runninghub.cn/api/v1/run/{task_id} | https://open.runninghub.ai/api/v1/run/{task_id} |
| 获取工作流列表 | https://open.runninghub.cn/api/v1/workflow/list | https://open.runninghub.ai/api/v1/workflow/list |
| 获取工作流详情 | https://open.runninghub.cn/api/v1/workflow/{id} | https://open.runninghub.ai/api/v1/workflow/{id} |
| 账户信息 | https://open.runninghub.cn/api/v1/user/info | https://open.runninghub.ai/api/v1/user/info |

### 3. 执行工作流示例

```javascript
// 执行文生图工作流
const response = await fetch('https://open.runninghub.cn/api/v1/run', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    workflow_id: 'WORKFLOW_ID',
    inputs: {
      positive_prompt: 'a beautiful landscape',
      negative_prompt: 'blurry, low quality',
      steps: 20,
      cfg_scale: 7
    }
  })
});

const result = await response.json();
console.log(result.data.task_id);
```

### 4. 查询任务状态

```javascript
const response = await fetch('https://open.runninghub.cn/api/v1/run/TASK_ID', {
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY'
  }
});
```

## 常用工作流

| 类型 | 描述 |
|:---|:---|
| 文生图 | 文本生成图片 |
| 图生图 | 图片风格转换 |
| 文生视频 | 文本生成视频 |
| 视频合成 | 视频编辑和合成 |
| AI 换脸 | 人脸替换 |

## 限制

- 需要有效的 API Key
- 部分工作流可能需要付费
- 并发请求有限制

## 参考

- 🇨🇳 国内版: https://www.runninghub.cn
- 🌍 国际版: https://www.runninghub.ai
- API 文档: https://www.runninghub.cn/call-api
- 工作流广场: https://www.runninghub.cn/works-square
