---
name: rhmcp-skill
description: RunningHub AI 智能调用。Use when user wants to generate images, videos, or audio content.
homepage: https://github.com/AIRix315/RHMCP
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "env": ["RUNNINGHUB_API_KEY"], "config": ["rhmcp.baseUrl"] },
        "primaryEnv": "RUNNINGHUB_API_KEY",
      },
  }
license: MIT-0
---

# RHMCP Skill - OpenClaw 专用

## 概述

RHMCP 的 OpenClaw Skill 包装层，提供智能决策和 Agent 指引。

## 前置条件

1. 安装 RHMCP：`git clone https://github.com/AIRix315/RHMCP.git && cd RHMCP && npm install && npm run build`
2. 配置 OpenClaw MCP（见 README.md）
3. 创建 RHMCP 配置：`service.json` 和 `.env`

---

## Agent 决策树

### 场景 → APP 映射

```
用户请求
    │
    ├─ "生成图片" / "文生图" / "画画"
    │       └─► rh_execute_app({ alias: "qwen-text-to-image", params: { text: "描述" } })
    │
    ├─ "修改图片" / "改图" / "图生图"
    │       └─► rh_execute_app({ alias: "qwen-image-to-image", params: { image: "URL", prompt: "描述" } })
    │
    └─ "更多APP"
            └─► rh_list_apps() 查看所有可用APP
```

### 参数映射

#### 文生图 (qwen-text-to-image)

| 参数     | 必填 | 默认值 | 说明     |
| -------- | ---- | ------ | -------- |
| `text`   | ✅   | -      | 提示词   |
| `width`  | ❌   | 1024   | 图片宽度 |
| `height` | ❌   | 1024   | 图片高度 |

#### 图生图 (qwen-image-to-image)

| 参数     | 必填 | 默认值 | 说明        |
| -------- | ---- | ------ | ----------- |
| `image`  | ✅   | -      | 输入图片URL |
| `prompt` | ✅   | -      | 修改提示词  |

---

## 轮询策略

长时间任务使用异步模式：

| APP 类型 | 首次等待 | 轮询间隔 | 最大等待 |
| -------- | -------- | -------- | -------- |
| 图生视频 | 3 分钟   | 1 分钟   | 15 分钟  |
| 数字人   | 2 分钟   | 30 秒    | 10 分钟  |
| 文生图   | 10 秒    | 5 秒     | 5 分钟   |

```javascript
// 提交异步任务
const { taskId } = await rh_execute_app({
  alias: "image-to-video",
  params: { image: "https://..." },
  mode: "async",
});

// 轮询查询
await sleep(180000); // 3分钟
while (true) {
  const status = await rh_query_task({ taskId });
  if (status.status === "SUCCESS") return status.data;
  if (status.status === "FAILED") throw new Error(status.msg);
  await sleep(60000); // 1分钟
}
```

---

## 存储策略

| 步骤位置 | 存储模式  | 原因               |
| -------- | --------- | ------------------ |
| 中间步骤 | `none`    | URL 直接传递       |
| 最终输出 | `none`    | 返回 URL，用户保存 |
| 用户要求 | `network` | 用户明确要求保存   |

```javascript
// 中间步骤：URL 直接传递
const img = await rh_execute_app({
  alias: "qwen-text-to-image",
  params: { text: "一只猫" },
});

// 后续步骤：使用 URL
const video = await rh_execute_app({
  alias: "image-to-video",
  params: { image: img.outputs[0].originalUrl, motion: "转身" },
});
```

---

## 链式工作流

```javascript
// 步骤1：文生图
const img = await rh_execute_app({
  alias: "qwen-text-to-image",
  params: { text: "一个女孩在樱花树下" },
});

// 步骤2：图生视频
const video = await rh_execute_app({
  alias: "image-to-video",
  params: {
    image: img.outputs[0].originalUrl,
    motion: "樱花飘落，女孩转身微笑",
  },
});

return { videoUrl: video.outputs[0].originalUrl };
```

---

## 失败重试

```javascript
const fallbacks = ["sdxl-text-to-image", "flux-text-to-image"];
for (const alias of fallbacks) {
  try {
    return await rh_execute_app({ alias, params });
  } catch (e) {
    continue; // 尝试下一个
  }
}
throw new Error("所有备选 APP 均失败");
```

---

## 错误码速查

| 错误码 | 含义     | 处理方式        |
| ------ | -------- | --------------- |
| `0`    | 成功     | 正常返回结果    |
| `804`  | 排队中   | 等待后轮询      |
| `805`  | 任务失败 | 调整提示词重试  |
| `813`  | 执行中   | 继续等待        |
| `421`  | 并发限制 | 等待 5 秒后重试 |

---

## 工具清单

| 工具              | 用途            |
| ----------------- | --------------- |
| `rh_list_apps`    | 列出所有可用APP |
| `rh_get_app_info` | 获取APP参数详情 |
| `rh_execute_app`  | 执行APP任务     |
| `rh_query_task`   | 查询任务状态    |
| `rh_upload_media` | 上传媒体文件    |

---

## 推荐模板

| 模板ID              | 名称     | 尺寸      | 适用场景 |
| ------------------- | -------- | --------- | -------- |
| `anime-portrait`    | 动漫人像 | 1024×1024 | 角色生成 |
| `landscape-wide`    | 风景横图 | 1920×1080 | 风景创作 |
| `portrait-vertical` | 人像竖图 | 768×1024  | 人物肖像 |

```javascript
// 使用模板
const templates = require("./references/templates.json");
const t = templates.templates["anime-portrait"];
rh_execute_app({ alias: t.alias, params: { ...t.params, text: "用户描述" } });
```

---

## 故障排除

| 问题              | 原因           | 解决方案                            |
| ----------------- | -------------- | ----------------------------------- |
| "未找到 alias"    | APP 未配置     | 运行 `rhmcp --update-apps`          |
| "apiKey 是必填项" | 未配置 API Key | 在 `.env` 设置 `RUNNINGHUB_API_KEY` |
| "任务超时"        | 执行时间过长   | 使用 `mode: "async"`                |

---

## License

MIT-0
