# 心跳维护指南

本文档说明心跳时如何执行记忆维护任务。

## 心跳触发

心跳由 OpenClaw 定期触发，触发时会读取 `HEARTBEAT.md`。

## 维护任务轮换

不必每次心跳都执行所有任务，建议轮换执行：

| 轮次 | 任务 | 频率 |
|------|------|------|
| 1 | 中期记忆审查 | 每2天 |
| 2 | 长期记忆更新 | 每周 |
| 3 | 过期清理 | 每周 |
| 4 | IMA 同步 | 每月 |

## 任务详情

### 1. 中期记忆审查

**目标**：识别需要升级的内容

**步骤**：
1. 读取最近7天的 `memory/*.md` 文件
2. 查找带 `#重要`、`#决策`、`#错误` 标签的内容
3. 判断是否需要升级到 MEMORY.md
4. 执行升级或标记待升级

**脚本**：
```bash
python3 scripts/promote.py --days 7 --dry-run  # 预览
python3 scripts/promote.py --days 7            # 执行
```

### 2. 长期记忆更新

**目标**：更新 MEMORY.md 中的用户档案和待处理事项

**步骤**：
1. 读取 USER.md，检查是否需要更新
2. 检查 MEMORY.md 中的待处理事项
3. 标记已完成的事项
4. 添加新发现的用户偏好

**手动操作**：直接编辑 MEMORY.md

### 3. 过期清理

**目标**：清理超过30天的中期记忆

**步骤**：
1. 扫描 `memory/*.md` 文件
2. 识别超过30天的文件
3. 检查是否包含重要内容
4. 归档或删除

**脚本**：
```bash
python3 scripts/cleanup.py --retention 30 --dry-run  # 预览
python3 scripts/cleanup.py --retention 30 --action auto  # 执行
```

### 4. IMA 同步

**目标**：备份重要内容到 IMA 知识库

**前置条件**：配置 IMA 凭证

**步骤**：
1. 提取 MEMORY.md 中的决策/错误教训
2. 调用 IMA API 创建笔记
3. 记录同步状态

**脚本**：
```bash
python3 scripts/sync_ima.py --type decision --dry-run  # 预览
python3 scripts/sync_ima.py --type decision            # 执行
```

## 状态追踪

维护 `memory/heartbeat-state.json`：

```json
{
  "lastChecks": {
    "midTermReview": "2024-01-15T00:00:00Z",
    "longTermUpdate": "2024-01-14T00:00:00Z",
    "expiredCleanup": "2024-01-10T00:00:00Z",
    "imaSync": null
  },
  "stats": {
    "totalMemories": 42,
    "promotedThisMonth": 3,
    "cleanedThisMonth": 12
  }
}
```

## 心跳响应模板

**有任务时**：
```
🔄 记忆维护中...

- 检查中期记忆：发现 2 条待升级内容
- 已升级到 MEMORY.md

✅ 维护完成
```

**无任务时**：
```
HEARTBEAT_OK
```

## 注意事项

1. **静默时段**：23:00-08:00 除非紧急，否则只返回 HEARTBEAT_OK
2. **频率控制**：同一任务不要在短时间内重复执行
3. **错误处理**：脚本失败时记录错误，下次心跳重试
4. **用户优先**：如果用户正在对话，延迟执行维护任务
