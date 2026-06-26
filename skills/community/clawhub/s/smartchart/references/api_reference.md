# SmartChart 工具参数参考

## CLI 参数说明

### run_tool 子命令参数

| 参数 | 说明 | 必填 |
|------|------|------|
| `-n` | 工具名称（数据集名） | 是 |
| `--format` | 输出格式：`raw`/`json`/`array` | 否（默认 raw） |
| `<变量>=<值>` | 传入数据集的 SQL 变量 | 视工具而定 |

### help_tool 用法

```bash
smartchart run_tool -n help_tool -t <工具名>
```

查看指定工具的详细信息。**仅在 remark 中未说明参数用法时使用。**

## 常用命令速查

```bash
# 查看所有可用工具
smartchart run_tool -n list_tool

# 查看具体工具的用法和参数（仅在 remark 未说明时使用）
smartchart run_tool -n help_tool -t <工具名>

# 执行工具（JSON 格式）
smartchart run_tool -n <工具名> --format json
```

## 安装与升级

```bash
# 安装
pip install smartchart

# 升级到最新版
pip install --upgrade smartchart

# 查看已安装版本
pip show smartchart
```

## 常见问题

**Q: 执行命令报 "command not found: smartchart"**  
A: 确认已安装：`pip install smartchart`，并检查 Python bin 目录是否在 PATH 中。

**Q: 工具返回空数据**  
A: 检查数据集的 SQL 查询是否正确，或传入的变量值是否有误。

**Q: 如何知道某个工具需要哪些参数？**  
A: 优先查看 `list_tool` 输出中 remark 字段的说明；若未说明，使用 `smartchart run_tool -n help_tool -t <工具名>` 查看。
