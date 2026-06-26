# Excel 文档（sheet）品类操作指引

本目录提供 Excel 文档（sheet）品类的专业操作能力，包括计算、筛选、统计、Excel操作相关场景。sheetengine 是独立的 MCP 服务，专用于 Sheet 文档的精细编辑操作。

## 使用场景

> **操作优先级说明：请按以下顺序选择合适的操作方式。**

**🥇 优先使用（重点1）：** 对于以下明确支持的操作，**必须优先**使用 `api/mcp-api.md` 内的接口处理：
设置单元格值、批量设置单元格值、设置单元格样式、合并/取消合并单元格、插入/删除行列、冻结/取消冻结行列、筛选、超链接、清除内容/样式、获取子表信息、获取单元格数据、获取合并单元格信息。

**🥈 次选使用（重点2）：** 当上述接口无法满足需求时（如涉及更复杂的表格操作），再考虑使用 `api/operation-api.md` 的 `OperationSheet` 完成。

---

## 服务信息

| 项目 | 说明 |
|------|------|
| 服务名 | `tencent-sheetengine` |
| API 地址 | `https://docs.qq.com/api/v6/sheet/mcp` |
| 调用方式 | `mcporter call tencent-sheetengine <工具名>` |
| Token | 与 tencent-docs **共用同一个 Token**，完成 tencent-docs 授权后自动配置，无需单独鉴权 |
| 文档类型 | 仅支持 Sheet 文档类型 |

---

## 文档标识

所有 sheetengine 工具都支持两种文档标识方式（二选一）：
- `file_url` (string): **⭐ 推荐** 腾讯文档的文档链接（如 `https://docs.qq.com/sheet/xxxxxxxx`），直接使用用户提供的文档链接即可
- `file_id` (string): 文档唯一标识符

> 💡 **推荐优先使用 `file_url`**：用户通常会直接提供文档链接，使用 `file_url` 无需额外解析 `file_id`，更加便捷。

---

## 工具列表

| 工具名称 | 功能说明 |
|---------|---------|
| set_cell_value | 设置单个单元格的值 |
| set_range_value | 批量设置单元格的值 |
| set_cell_style | 设置单个单元格的样式 |
| merge_cell | 合并单元格 |
| insert_dimension | 插入行或列 |
| delete_dimension | 删除行或列 |
| set_freeze | 设置冻结行列 |
| set_filter | 设置筛选 |
| remove_filter | 移除筛选 |
| set_link | 设置单元格超链接 |
| clear_link | 清除单元格超链接 |
| clear_range_cells | 清除区域单元格内容 |
| clear_range_style | 清除区域单元格样式 |
| get_sheet_info | 获取子表信息 |
| clear_range_all | 清空区域内容和样式 |
| unset_freeze | 删除所有冻结 |
| unmerge_cell | 取消合并单元格 |
| get_cell_data | 获取单元格数据 |
| get_merged_cells | 获取合并单元格信息 |

---

## 注意事项

- 工具名不带前缀（如 `get_cell_data`、`set_cell_value` 等）
- 操作前需确保拥有文档的写入权限
- 详细 API 参数和调用示例请参考 `api/mcp-api.md`

---

## 按场景工作流

### 设置单元格内容和样式

```
1. 按需调用tencent-sheetengine的工具更新单元格内容或者样式
    - 更新单个单元格内容：set_cell_value
    - 更新多个单元格内容：set_range_value
    - 更新单个单元格式样: set_cell_style
```

### 清除单元格内容和样式

```
1. 按需调用tencent-sheetengine的工具清除单元格内容或者样式
    - 清除单元格内容：clear_range_cells
    - 清除单元格样式：clear_range_style
    - 同时清除内容和样式： clear_range_all
```

### 设置和取消合并单元格

```
1. 调用tencent-sheetengine的merge_cell，可以生成合并单元格
2. 调用tencent-sheetengine的unmerge_cell，可以取消合并单元格
```

### 设置和取消筛选

```
1. 调用tencent-sheetengine的set_filter，可以设置筛选
2. 调用tencent-sheetengine的remove_filter，可以取消筛选
```

### 设置和取消冻结

```
1. 调用tencent-sheetengine的set_freeze，可以设置冻结区域
2. 调用tencent-sheetengine的unset_freeze，可以取消冻结区域
```

### 添加和删除链接

```
1. 调用tencent-sheetengine的set_link，可以设置链接
2. 调用tencent-sheetengine的clear_link，可以删除链接
```

### 增删行列

```
1. 调用tencent-sheetengine的insert_dimension，可以增加行或者列
2. 调用tencent-sheetengine的delete_dimension，可以删除行或者列
```

### 查询接口

```
1. 调用tencent-sheetengine的get_sheet_info，获取在线表格的子表信息，包括子表ID、名称、类型、行列数量
2. 调用tencent-sheetengine的get_cell_data，获取在线表格指定区域的单元格数据，支持返回CSV格式或结构化单元格数据
3. 调用tencent-sheetengine的get_merged_cells,获取在线表格指定区域内与该区域相交的合并单元格信息，返回合并单元格范围列表
```
