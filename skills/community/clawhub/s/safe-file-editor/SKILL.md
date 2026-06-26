# Safe File Editor

>
> 模拟预览+4眼原则+原子备份回滚
> 参考Claude Code SedEdit安全设计

## 背景问题

文件编辑类工具的常见风险：
- **误操作覆盖**：模型匹配文本错误，导致文件损坏
- **无预览**：直接写入，无法反悔
- **无备份**：修改后原文件丢失
- **注入风险**：`_simulatedSedEdit`字段可被模型构造

**根因**：Claude Code原生的SedEdit虽有安全措施，但未完整迁移到OpenClaw

## 解决方案

### 4眼原则（Two-Person Rule）

```
第1眼（AI预览）：生成diff，不实际修改
第2眼（用户确认）：确认diff正确后执行
```

### 原子写入流程

```
1. 读取原始内容
      ↓
2. 生成diff预览（dry_run=True）
      ↓
3. 用户确认
      ↓
4. 创建备份（原子）
      ↓
5. 写入临时文件
      ↓
6. 重命名替换（原子操作）
      ↓
7. 成功/失败回滚
```

### 安全设计

参考Claude Code的`_simulatedSedEdit`字段omit策略：
```python
# 该字段在inputSchema中被omit，模型无法自行设置
_simulatedSedEdit: Optional[SedEditRequest] = Field(
    default=None,
    json_schema_extra={"omit": True}  # 关键：omit防止注入
)
```

## 使用方式

### Python API

```python
from safe_file_editor import safe_edit, rollback

# 第一步：预览（dry_run=True，默认）
result = safe_edit(
    file_path="config.json",
    old_text='"timeout": 300',
    new_text='"timeout": 600',
    dry_run=True
)
print(result.changes)  # 查看变更预览

# 第二步：确认后执行（dry_run=False）
if result.success:
    result = safe_edit(
        file_path="config.json",
        old_text='"timeout": 300',
        new_text='"timeout": 600',
        dry_run=False
    )
    print(f"备份: {result.backup_path}")

# 第三步：如需回滚
rollback("config.json", result.backup_path)
```

### EditResult结构

```python
@dataclass
class EditResult:
    success: bool          # 是否成功
    file_path: str         # 目标文件
    backup_path: str       # 备份路径（失败时用于回滚）
    changes: str           # 变更描述（diff）
    hash_before: str       # 修改前hash
    hash_after: str        # 修改后hash
    dry_run: bool          # 是否为预览模式
    message: str           # 状态消息
```

### Skill集成

在SKILL.md中声明：
```yaml
whenToUse: |
  任何需要修改文件的操作
  必须使用dry_run预览，用户确认后再执行
permissions:
  - file:read (读取原文件)
  - file:write (写入临时+重命名)
  - file:backup (创建.bak备份)
steps:
  1: dry_run预览变更
  2: 展示diff给用户确认
  3: dry_run=False执行
  4: 返回backup_path
```

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `BACKUP_DIR` | `tmp/file-backups/` | 备份文件目录 |
| `MAX_BACKUP_AGE` | 30天 | 备份保留期限 |
| 原子写入 | `temp.replace(target)` | 防止写入中断 |

## 日志审计

### 编辑日志 (`logs/safe-file-editor.log`)
```
[2026-04-03 15:30:00] DRY_RUN: config.json | a1b2c3d4->e5f6a7b8 | - "timeout": 300
+ "timeout": 600
[2026-04-03 15:30:05] COMMITTED: config.json | a1b2c3d4->e5f6a7b8 | changes | backup: tmp/...
[2026-04-03 15:30:10] FAILED: config.json | - | Permission denied
[2026-04-03 15:35:00] ROLLBACK: config.json | - | Restored from tmp/...
```

## 最佳实践

1. **always dry_run first** — 任何编辑先预览
2. **show complete diff** — 展示完整变更给用户
3. **unique old_text** — old_text必须足够唯一，避免误匹配
4. **backup before commit** — 自动备份，支持回滚
5. **log everything** — 所有操作记录审计日志

## 关联

- 并发安全：`skills/agent-concurrency-controller/`
- 结果控制：`skills/tool-result-size-controller/`
- Claude Code安全设计：`memory/learnings/claude-code-architecture-2026-04-03.md`

## 版本

- **v1.0.0** (2026-04-03): 初始实现，4眼原则+原子备份回滚
