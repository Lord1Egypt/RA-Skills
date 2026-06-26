# Tool Result Size Controller

>
> 大结果自动落盘，保护上下文窗口
> 参考Claude Code的maxResultSizeChars机制

## 背景问题

原生OpenClaw工具返回大结果时：
- 直接回显到对话上下文
- 大JSON数据导致**token爆炸**
- 影响后续对话质量

**根因**：缺乏Claude Code的`maxResultSizeChars`保护机制

## 解决方案

### 自动落盘机制

```python
from tool_result_size_controller import maybe_spill, ToolResultWrapper

# 方式1：便捷函数
result = maybe_spill(large_data, tool_name="search_results", threshold=10000)
# 如果结果>10000字符，自动写入磁盘，返回文件路径

# 方式2：装饰器
@ToolResultWrapper("my_tool", threshold=5000)
def my_tool_func(*args, **kwargs):
    return large_result
```

### 返回格式

**小结果**（≤阈值）：直接返回原数据
```python
{"key": "value"}  # 直接返回
```

**大结果**（>阈值）：返回元数据
```json
{
  "spilled": true,
  "file_path": "/path/to/result-20260403-a1b2c3d4.json.gz",
  "size_chars": 15000,
  "size_bytes": 4500,
  "content_hash": "a1b2c3d4",
  "preview": "前500字符预览..."
}
```

### 智能压缩

- 大结果自动gzip压缩（>10KB）
- 节省磁盘空间
- 透明解压读取

## 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `DEFAULT_THRESHOLD` | 10000 | 字符阈值，超过则落盘 |
| `MAX_AGE_DAYS` | 7 | 结果文件保留天数 |
| `RESULTS_DIR` | `tmp/tool-results/` | 落盘目录 |

## 使用方式

### Python API

```python
from tool_result_size_controller import (
    maybe_spill,
    load_spilled_result,
    cleanup_old_results
)

# 1. 包装结果（自动判断是否落盘）
result = maybe_spill(large_data, "my_tool", threshold=8000)

# 2. 读取落盘结果
if result.get("spilled"):
    data = load_spilled_result(result["file_path"])
    
# 3. 清理过期文件（cron定期执行）
deleted = cleanup_old_results(max_age_days=7)
```

### Skill集成

在SKILL.md中声明：
```yaml
whenToUse: |
  工具返回大结果可能超过10000字符时
  使用本技能自动落盘，保护上下文窗口
permissions:
  - file:write (tmp/tool-results目录)
  - file:read (读取落盘结果)
```

## 日志审计

### 落盘日志 (`logs/tool-size.log`)
```
[2026-04-03 15:20:00] search_results: spilled=15000_chars >> tmp/tool-results/...
[2026-04-03 15:20:01] small_query: direct_return (500_chars)
[2026-04-03 15:20:02] cleanup: deleted 3 old files
```

## 最佳实践

1. **默认使用**：大多数返回不确定大小数据的工具
2. **阈值调整**：
   - 快速查询：5000字符
   - 标准工具：10000字符
   - 大文件处理：50000字符
3. **定期清理**：cron任务每日清理过期结果
4. **预览友好**：始终返回前500字符预览，便于快速判断

## 关联

- 架构设计：`memory/learnings/claude-code-architecture-2026-04-03.md`
- 并发安全：`skills/agent-concurrency-controller/`
- 安全编辑：`skills/safe-file-editor/`

## 版本

- **v1.0.0** (2026-04-03): 初始实现，参考Claude Code maxResultSizeChars
