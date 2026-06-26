# 任务记忆管理（精简指南）

## 核心理念
- **任务即容器**：每个任务管理自己的记忆上下文
- **结构即记忆**：文件夹结构反映工作流程
- **智能加载**：只加载相关记忆，避免过载

## 核心文件
```
workspace/
├── input/YYYY-MM-DD_任务描述/     # 输入文件
├── output/YYYY-MM-DD_任务描述/    # 输出文件+元数据
├── memory/YYYY-MM-DD.md          # 每日记忆
└── MEMORY.md                     # 长期记忆
```

## 任务元数据 (.task-meta.json)
```json
{
  "task_id": "2026-03-13_文档分析",
  "status": "进行中",
  "current_step": "02_分析",
  "progress": 50,
  "memory_points": [
    {
      "step": "01_准备",
      "summary": "收集了3个文档",
      "timestamp": "2026-03-13T11:30:00+08:00"
    }
  ]
}
```

## 关键操作

### 1. 开始新任务
```bash
# 创建目录结构
mkdir -p output/2026-03-19_新任务/01_准备

# 保存初始记忆
python scripts/safe-writer.py "开始任务：新任务" --task-id "2026-03-19_新任务" --step "01_准备"
```

### 2. 保存进度
```bash
python scripts/safe-writer.py "完成了数据分析" --task-id "2026-03-19_新任务" --step "02_分析"
```

### 3. 恢复任务
```bash
# 扫描未完成任务
python scripts/task-memory-manager.py recovery

# 加载特定任务记忆
python scripts/task-memory-manager.py load --task-ids "2026-03-19_新任务"
```

### 4. 任务状态管理
```bash
# 更新状态
python scripts/task-memory-manager.py update --task-id "2026-03-19_新任务" --status "完成"

# 添加记忆点
python scripts/task-memory-manager.py add-memory --task-id "2026-03-19_新任务" --step "02_分析" --type "进展" --summary "发现关键模式"
```

## 最佳实践
1. **关键决策立即记录**：重要发现或决定及时保存
2. **步骤完成时记录**：每个步骤结束保存摘要
3. **关联相关文件**：记忆点提及使用的文件
4. **定期检查点**：长时间任务每10-15分钟自动保存

## 故障恢复
- **记忆丢失**：启用原子写入（safe-writer工具）
- **文件损坏**：从.task-meta.json恢复上下文
- **加载过慢**：减少加载的任务数量

## 核心命令速查
- `safe-writer.py <内容> --task-id <ID> --step <步骤>` - 保存记忆
- `task-memory-manager.py recovery` - 恢复界面
- `task-memory-manager.py scan` - 扫描任务
- `task-recovery-check.py notify` - 心跳检查（Python版本）
- 如需PowerShell版本：将 `task-recovery-check-ps1.txt` 重命名为 `.ps1` 使用