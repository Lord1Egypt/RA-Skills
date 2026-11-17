> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# 进度状态查询协议 v1.0

> 提供项目进度的实时查询能力

---

## 查询接口

### 1. 项目总览查询

```json
{
  "project": {
    "id": "project-001",
    "name": "项目名称",
    "status": "in-progress",
    "startTime": "2026-09-10T10:00:00Z",
    "estimatedCompletion": "2026-09-10T18:00:00Z"
  },
  "progress": {
    "total": 100,
    "completed": 45,
    "failed": 2,
    "pending": 53
  },
  "currentTask": {
    "id": "task-045",
    "type": "video-generation",
    "startTime": "2026-09-10T14:30:00Z"
  }
}
```

### 2. 分镜进度查询

```json
{
  "storyboard": {
    "total": 10,
    "completed": 7,
    "failed": 0,
    "pending": 3
  },
  "details": [
    {
      "id": "storyboard-001",
      "status": "completed",
      "videoStatus": "completed",
      "videoUrl": "https://..."
    }
  ]
}
```

### 3. 资产生成进度查询

```json
{
  "assets": {
    "total": 20,
    "completed": 15,
    "failed": 1,
    "pending": 4
  },
  "details": [
    {
      "id": "asset-001",
      "type": "image",
      "status": "completed",
      "url": "https://..."
    }
  ]
}
```

---

## 状态定义

| 状态 | 含义 |
|-----|------|
| pending | 待处理 |
| running | 运行中 |
| completed | 已完成 |
| failed | 失败 |
| cancelled | 已取消 |

---

## 实时更新机制

### 1. WebSocket 推送

```javascript
// 服务端
const ws = new WebSocketServer({ port: 8080 });

ws.on('connection', (socket) => {
  // 推送进度更新
  socket.send(JSON.stringify({
    type: 'progress-update',
    data: getProjectProgress()
  }));
});
```

### 2. 轮询查询

```javascript
// 客户端
setInterval(async () => {
  const progress = await fetch('/api/progress').then(r => r.json());
  updateUI(progress);
}, 5000); // 每5秒查询一次
```

---

## 实施检查清单

- [ ] 实现项目总览查询
- [ ] 实现分镜进度查询
- [ ] 实现资产生成进度查询
- [ ] 实现WebSocket推送（可选）
- [ ] 实现轮询查询（可选）

---

**版本**: v1.0  
**创建时间**: 2026-09-10
