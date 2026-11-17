---
name: quickref-taskflow-ingest
description: "TaskFlow + ClawHub 数字资源入库速查表：两工具串联完成从业务流程处理到资源中心入库的完整操作参考，含命令模板与检查清单。"
metadata:
  clawdbot:
    emoji: "📋"
    requires:
      - taskflow
    tags:
      - workflow
      - taskflow
      - clawhub
      - quick-reference
      - digital-resource
  author: openclaw-demo
  created: "2026-10-07"
  version: "1.0.1"
  license: MIT
  tags:
    - workflow
    - taskflow
    - clawhub
    - quick-reference
    - digital-resource
---

# TaskFlow + ClawHub 数字资源入库速查表

## 工具定位

| 工具 | 用途 |
|------|------|
| **TaskFlow** | 业务流程编排：多步骤处理、状态持久化、等待/恢复、子任务链接 |
| **ClawHub CLI** | 数字资源入库：发布到资源中心、元数据管理、检索验证 |

## 串联流程

```
内容准备 → TaskFlow 预处理(分类/质检/元数据) → clawhub publish → clawhub search/inspect 验证
```

## 关键命令

### TaskFlow 编排（代码层）

```ts
const tf = api.runtime.tasks.flow.fromToolContext(ctx);
const flow = tf.createManaged({
  controllerId: "demo/ingest",
  goal: "ingest digital resource",
  currentStep: "prepare",
  stateJson: { resource: "", checks: [] },
});
// ... runTask, setWaiting, resume, finish
```

### ClawHub 入库

```bash
# 发布
clawhub publish ./resource-dir \
  --slug my-resource \
  --name "资源名称" \
  --version 1.0.0 \
  --changelog "初始版本"

# 验证
clawhub inspect my-resource
clawhub search "关键词"
```

## 元数据必填字段

- `name` — 唯一标识（slug）
- `description` — 10-200字描述
- `author` — 创建者
- `created` — YYYY-MM-DD
- `version` — SemVer
- `tags` — 3-8个标签

## 发布前检查

- [ ] 内容完整无错误
- [ ] 描述覆盖核心内容
- [ ] 标签准确（3-8个）
- [ ] 无敏感信息
- [ ] 链接可访问
- [ ] 元数据字段齐全
