> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# 项目工作台协议 v1.0

> 提供统一的项目管理界面

---

## 工作台功能

### 1. 项目概览

```json
{
  "project": {
    "name": "项目名称",
    "createdAt": "2026-09-10T10:00:00Z",
    "status": "active",
    "progress": {
      "totalTasks": 100,
      "completedTasks": 45,
      "failedTasks": 2,
      "pendingTasks": 53
    }
  }
}
```

### 2. 资产列表

```json
{
  "assets": [
    {
      "id": "asset-001",
      "type": "character",
      "name": "角色名",
      "status": "completed",
      "versions": 3,
      "lastModified": "2026-09-10T10:30:00Z"
    }
  ]
}
```

### 3. 任务列表

```json
{
  "tasks": [
    {
      "id": "task-001",
      "type": "image-generation",
      "status": "running",
      "progress": 75,
      "startedAt": "2026-09-10T10:00:00Z",
      "estimatedCompletion": "2026-09-10T10:45:00Z"
    }
  ]
}
```

---

## 工作台操作

### 1. 创建项目

```javascript
async function createProject(config) {
  const project = {
    id: generateId(),
    name: config.name,
    createdAt: new Date(),
    status: 'active',
    assets: [],
    tasks: []
  };
  
  await saveProject(project);
  return project;
}
```

### 2. 更新进度

```javascript
async function updateProgress(projectId, taskId, progress) {
  const project = await getProject(projectId);
  const task = project.tasks.find(t => t.id === taskId);
  
  if (task) {
    task.progress = progress;
    if (progress === 100) {
      task.status = 'completed';
    }
    
    await saveProject(project);
  }
}
```

### 3. 查看状态

```javascript
async function getProjectStatus(projectId) {
  const project = await getProject(projectId);
  
  return {
    project: project.name,
    progress: calculateProgress(project),
    assets: project.assets.length,
    tasks: {
      running: project.tasks.filter(t => t.status === 'running').length,
      completed: project.tasks.filter(t => t.status === 'completed').length,
      failed: project.tasks.filter(t => t.status === 'failed').length
    }
  };
}
```

---

## 实施检查清单

- [ ] 实现项目创建功能
- [ ] 实现资产管理功能
- [ ] 实现任务管理功能
- [ ] 实现进度跟踪功能
- [ ] 实现状态查询功能

---

**版本**: v1.0  
**创建时间**: 2026-09-10
