# 可编辑单元格

[返回目录](../index.md)

## 功能说明

通过 `slot` 渲染输入框实现单元格编辑，点击进入编辑态，失焦后保存。

## 示例代码（React）

示例代码参考路径：`../example/editableCell` 
**在用户没有特殊要求的情况下，你需要严格按照示例代码生成**

---

## 注意事项

1. **Slot 名称格式**：必须严格遵循 `custom-cell-{dataIndex}-{rowKeyValue}` 格式
2. **rowKey 值**：slot 名称中的 rowKeyValue 是数据中 rowKey 字段的实际值
3. **性能考虑**：大量自定义单元格会增加 DOM 复杂度，大数据量时建议配合虚拟滚动
4. **组件使用**：当需要渲染通用组件如（`input、select、datepicker`）时，优先使用`@kdcloudjs/shoelace`提供的组件
