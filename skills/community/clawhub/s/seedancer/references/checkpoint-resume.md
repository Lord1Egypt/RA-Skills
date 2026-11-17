> **Language**: This document is in Chinese only. For English overview, see [README.md](../README.md).
>
> **语言说明**: 本文档仅提供中文版本。英文概述请查看 [README.md](../README.md)。

---
# 断点续跑协议 v1.0

> 借鉴 ShotFunClaw `workflow-runtime.js` 设计

---

## 核心概念

当 Seedancer 执行长流程（P0-P2 预生产、多集分镜生成、批量视频生成）时，可能因以下原因中断：
- 用户主动暂停
- API 限流/失败
- 上下文超限
- 网络错误

断点续跑协议确保：中断后可恢复，不丢失进度，不重复已完成工作。

---

## 1. 一致性校验

### 1.1 Hash 校验项

| Hash 类型 | 内容 | 用途 |
|-----------|------|------|
| `runSpecHash` | 整个流程输入的 SHA-256 | 检测用户是否修改了需求 |
| `seedancerVersion` | Seedancer 版本号 | 检测技能是否升级 |
| `step.inputHash` | 每步输入的 SHA-256 | 检测该步骤是否需要重跑 |
| `registryVersion` | 模型注册表版本 | 检测模型是否更新 |

### 1.2 续跑决策树

```
恢复请求进入
  ├─ runSpecHash 一致？
  │   ├─ YES → 检查 seedancerVersion
  │   │   ├─ YES → 跳过已成功步骤，从中断处继续
  │   │   └─ NO → 提示用户：Seedancer 已升级，建议重新评估
  │   └─ NO → 提示用户：需求已变化，需要重新开始
  │           ├─ 用户确认重新开始 → 清除旧状态，从头开始
  │           └─ 用户要求强制续跑 → 使用 --force-resume（需明确确认风险）
```

---

## 2. 状态文件结构

### 2.1 项目目录

```
<项目目录>/
├── .seedancer/
│   ├── manifest.json          # 运行总清单
│   ├── steps/                 # 每步状态
│   │   ├── p0.json           # P0 项目接收
│   │   ├── p0a.json          # P0A 十项解析
│   │   ├── p1.json           # P1 创作基准
│   │   ├── p2a.json          # P2a 角色资产
│   │   ├── p2b.json          # P2b 道具母板
│   │   └── shot-NNN.json     # 每个镜头的生成状态
│   └── logs/
│       └── run.jsonl         # 事件日志
```

### 2.2 manifest.json 结构

```json
{
  "schemaVersion": 1,
  "runId": "2026-09-10-project-x",
  "seedancerVersion": "8.0.0",
  "runSpecHash": "sha256:abc123...",
  "registryVersion": "2026.09.10.1",
  "currentStage": "p2a",
  "stages": [
    {
      "id": "p0",
      "status": "completed",
      "summary": "项目基准卡已生成",
      "completedAt": "2026-09-10T10:30:00Z"
    },
    {
      "id": "p0a",
      "status": "completed",
      "summary": "十项解析完成，情绪曲线已生成",
      "completedAt": "2026-09-10T10:45:00Z"
    },
    {
      "id": "p2a",
      "status": "running",
      "summary": "角色资产生成中，已完成 3/8",
      "startedAt": "2026-09-10T11:00:00Z"
    }
  ],
  "modelSelection": {
    "videoModel": "seedance-2.5",
    "imageModel": "gpt-image2",
    "decision": "用户选择高质量视频 + 照片级真实感图片"
  },
  "userArtifacts": [
    {
      "kind": "image",
      "name": "character-01-main",
      "localPath": "assets/characters/character-01-main.png",
      "url": "https://..."
    }
  ]
}
```

### 2.3 step sidecar 结构

```json
{
  "stepId": "p2a-character-01",
  "status": "completed",
  "inputHash": "sha256:def456...",
  "startedAt": "2026-09-10T11:00:00Z",
  "completedAt": "2026-09-10T11:05:00Z",
  "model": "gpt-image2",
  "cost": {
    "estimated": 55,
    "actual": 55,
    "currency": "CNY"
  },
  "resultUrls": ["https://..."],
  "localFiles": [
    {
      "kind": "image",
      "path": "assets/characters/character-01-main.png"
    }
  ],
  "error": null
}
```

---

## 3. 续跑命令

### 3.1 检查恢复安全性

```
用户输入：检查恢复安全性
Agent 行为：
1. 读取 .seedancer/manifest.json
2. 计算当前输入的 runSpecHash
3. 对比 manifest 中的 runSpecHash
4. 输出：
   ├─ "安全恢复" → 所有 hash 一致，可以续跑
   ├─ "需求已变化" → runSpecHash 不一致，需要确认
   └─ "Seedancer 已升级" → seedancerVersion 不一致，建议重新评估
```

### 3.2 从断点续跑

```
用户输入：从断点续跑
Agent 行为：
1. 检查恢复安全性（同上）
2. 如果安全：
   - 读取所有 step sidecar
   - 跳过 status="completed" 的步骤
   - 从 status="running" 或 status="pending" 的步骤继续
3. 如果不安全：
   - 提示用户风险
   - 等待用户确认后执行 --force-resume
```

### 3.3 强制续跑（--force-resume）

```
用户输入：强制从断点续跑
Agent 行为：
1. 明确告知风险：
   - "需求已变化，续跑可能导致不一致"
   - "或 Seedancer 已升级，旧步骤可能不适用"
2. 等待用户明确确认
3. 如果确认：忽略 hash 不一致，从中断处继续
```

---

## 4. 阶段状态机

### 4.1 预生产阶段（P0-P2）

```
pending → running → completed
                  → failed
                  → needs-user-confirmation
                  → skipped
```

### 4.2 分镜生成阶段

```
pending → analyzing → writing → reviewing → generating → completed
                                                    → failed
```

### 4.3 视频生成阶段

```
pending → prompting → generating → qa-checking → completed
                                          → needs-retake
                                          → failed
```

---

## 5. 失败处理

### 5.1 单项失败

```
当某个步骤失败时：
1. 写入 step sidecar，status="failed"，记录 error 信息
2. 不阻塞其他步骤继续执行
3. 最终报告中：
   - 先列出所有成功的产出物（localPath + URL）
   - 再列出失败项 + 错误原因 + 恢复建议
```

### 5.2 部分失败恢复

```
当批量任务部分失败时：
1. 读取现有 manifest.json 和 step sidecars
2. 识别失败项
3. 只重跑失败项，不重跑成功项
4. 更新 manifest.json 和 step sidecars
```

### 5.3 常见错误码

| 错误码 | 含义 | 恢复建议 |
|--------|------|----------|
| `F-RESUME-UNSAFE` | runSpecHash 不一致 | 需要 --force-resume 或重新开始 |
| `F-RESUME-VERSION` | seedancerVersion 不一致 | 建议重新评估，或 --force-resume |
| `F-RESUME-NO-MANIFEST` | 找不到 manifest.json | 无法续跑，需要重新开始 |
| `F-RESUME-CORRUPT` | manifest.json 损坏 | 尝试从 step sidecars 重建，或重新开始 |

---

## 6. 实现检查清单

### 6.1 每个步骤必须

- [ ] 开始时写入 step sidecar（status="running"）
- [ ] 计算 inputHash
- [ ] 成功时更新 status="completed"，记录 localPath + URL
- [ ] 失败时更新 status="failed"，记录 error
- [ ] 更新 manifest.json 的 currentStage

### 6.2 续跑时检查

- [ ] manifest.json 存在且可读
- [ ] runSpecHash 一致（或用户已确认 --force-resume）
- [ ] seedancerVersion 一致（或用户已确认）
- [ ] 所有 step sidecars 可读
- [ ] 成功步骤的 localPath 存在

### 6.3 用户可见信息

- [ ] 当前阶段 + 进度
- [ ] 已完成的产出物（localPath + URL）
- [ ] 失败项 + 错误原因 + 恢复建议
- [ ] 下一步操作

---

## 7. 与现有系统的整合

### 7.1 与运营循环整合

在 Seedancer SKILL.md 的运营循环中增加：

```
门控 9: 断点检测 (Resume Gate)
- 检查是否存在 .seedancer/manifest.json
- 如果存在，提示用户："检测到上次未完成的流程，是否从断点续跑？"
- 用户选择：
  ├─ 是 → 进入续跑流程
  ├─ 否，重新开始 → 清除 .seedancer/，从头开始
  └─ 查看上次进度 → 输出 manifest.json 摘要
```

### 7.2 与序列项目管理整合

断点续跑协议与现有的序列项目管理（`sequence-project-state.md`）互补：
- 断点续跑：恢复单个流程
- 序列项目管理：管理多个镜头/集的状态

---

## 8. 示例场景

### 场景 1：P2a 角色资产生成中断

```
用户：开始 P0-P2 预生产流程
Agent：执行 P0 → P0A → P1 → P2a（已完成 3/8 个角色）
      ↓ API 限流，中断

用户：（30分钟后）从断点续跑
Agent：
1. 检查恢复安全性 → 安全
2. 读取 manifest.json → currentStage="p2a"
3. 读取 step sidecars → 3个 completed，5个 pending
4. 从第 4 个角色开始继续生成
5. 输出：继续生成角色资产（4/8 开始）
```

### 场景 2：用户修改需求

```
用户：开始 P0-P2 预生产流程
Agent：执行 P0 → P0A → P1
      ↓ 用户修改剧本

用户：我修改了剧本，从断点续跑
Agent：
1. 检查恢复安全性 → runSpecHash 不一致
2. 输出："检测到需求已变化，续跑可能导致不一致。是否强制续跑？"
3. 用户：强制续跑
4. 使用 --force-resume，从 P1 继续
5. 但提示用户：P0A 可能需要重新评估
```

### 场景 3：Seedancer 升级

```
用户：（一周后）从断点续跑
Agent：
1. 检查恢复安全性 → seedancerVersion 不一致（8.0.0 → 8.1.0）
2. 输出："Seedancer 已升级到 8.1.0，建议重新评估。是否强制续跑？"
3. 用户：重新评估
4. 清除 .seedancer/，从头开始
```

---

## 9. 注意事项

### 9.1 不要

- ❌ 静默降级：hash 不一致时不要自动续跑
- ❌ 丢失成功项：失败时不要丢弃已成功的产出物
- ❌ 伪造 taskNo：失败时不要伪造任务号
- ❌ 只显示最后一个错误：必须列出所有成功项 + 失败项

### 9.2 要

- ✅ 明确告知风险：hash 不一致时必须告知用户
- ✅ 保留成功项：部分失败时保留成功项
- ✅ 结构化输出：使用 userArtifacts 归一化产出物
- ✅ 原子写入：使用 tmp + rename 写入 manifest/step，避免中断导致损坏

---

## 10. 参考

- ShotFunClaw `scripts/core/workflow-runtime.js`
- ShotFunClaw 项目的 stage-protocol.md（**外部来源**，非本技能文件）
- Seedancer `references/sequence-project-state.md`

---

**版本**: v1.0  
**创建时间**: 2026-09-10  
**来源**: ShotFunClaw 断点续跑机制
