---
name: smart-web-components-usage
description: 提供 @ht-smart/basic 组件库中所有组件的使用指导和 API 参考。当用户询问如何使用、如何配置或如何集成 HtProTable、HtProTree、HtForm、HtModal、HtDrawer、HtDict、HtCard、HtCascader、HtSelect、HtSearchForm、HtList、HtNiceModal、HtProRegionTree、HtTree、HtColorPicker、HtDescription、HtFileUpload、HtFilePreview、HtFloatButton、HtGrid、HtLayout、HtDrawer、HtException、HtRichTextEditor、HtCopyright、HtDevicePlayer、HtButton、HtTab、HtTableSelect、ScrollLoadSelect、HtFormatTime、ActionSpace 等组件时使用此 skill。
---

# smart-web-components 组件库使用指南

本 skill 覆盖 `packages/basic/src/components` 目录下所有组件的关键用法、API 和最佳实践。

## 组件速查索引

| 组件名 | 导入名 | 分类 | 说明 |
|--------|--------|------|------|
| HtActionSpace | `HtActionSpace` | 基础 | 列表操作栏，间隔布局 |
| HtButton | `IconButton` | 基础 | 增强按钮，内置常用 icon 配置 |
| HtInput | `BaseInput` | 基础 | 输入框封装 |
| HtTab | `BaseTab` | 基础 | 标签页，支持 url 同步和定制样式 |
| HtModal | `HtModal` | 基础 | 弹窗封装，简化状态管理 |
| HtDrawer | `HtDrawer` | 基础 | 抽屉封装，支持拖拽宽度/最大化 |
| HtException | `HtException` | 基础 | 异常页（401/403/404/500/502） |
| HtCopyright | `HtCopyright` | 基础 | 版权信息组件 |
| HtGrid | `HtGrid` | 基础 | 网格布局 |
| HtSearchForm | `HtSearchForm` | 基础 | 搜索表单 |
| HtRichTextEditor | `HtRichTextEditor` | 基础 | 富文本编辑器（基于 WangEditor） |
| HtFormatTime | `HtFormatTime` | 基础 | 时间格式转换展示组件 |
| HtForm | `HtForm` | 高级 | 高级表单，含 Modal/Drawer/Steps 表单 |
| HtProTable | `HtProTable` | 高级 | 企业级表格，内置搜索/分页/列设置 |
| HtTableSelect | `HtTableSelect` | 高级 | 弹窗表格选择器 |
| HtCard | `HtCard` | 高级 | 高级卡片，支持栅格/折叠/统计 |
| HtList | `HtList` | 高级 | 卡片风格列表，基于 HtProTable |
| HtCascader | `HtCascader` / `HtRegionCascader` | 高级 | 级联选择，支持区划懒加载 |
| HtSelect | `HtSelect` | 高级 | 下拉选择，支持 options 或远程请求 |
| ScrollLoadSelect | `ScrollLoadSelect` | 高级 | 远程搜索+滚动加载选择器 |
| HtDict | 多组件 | 高级 | 字典组件集合（Text/Tag/Badge/Select等） |
| HtDescription | `HtDescriptions` | 高级 | 高级描述列表，支持远程请求 |
| HtTree | `HtTree` / `HtRegionTree` | 高级 | 树形组件，支持懒加载/搜索 |
| HtProTree | `HtProTree` | 高级 | 高级树，支持节点增删改/搜索 |
| HtProRegionTree | `HtProRegionTree` | 高级 | 行政区划树，内置接口 |
| HtColorPicker | `HtColorPicker` | 高级 | 颜色选择器，支持 hex/rgb/hsb |
| HtDevicePlayer | `HtDevicePlayer` | 高级 | 设备（摄像头）实时播放组件 |
| HtFileUpload | `HtProFileUpload` | 高级 | 大文件切片上传，支持断点续传 |
| HtFilePreview | `HtFilePreview` | 高级 | 文件预览，通过 fileId 获取地址 |
| HtFloatButton | `HtFloatButton` | 基础 | 悬浮按钮，支持受控选中/分组 |
| HtNiceModal | `HtNiceModal` | 高级 | API 方式调用弹窗，解决多次渲染问题 |
| HtLayout | `HtProLayout` | 高级 | 中后台标准布局 |

---

## 详细 API 参考文档

以下组件有完整的 API 参考文档，当需要精确的属性类型、默认值、方法签名时请阅读：

- 完整表格 API、valueType 列表、actionRef/tableRef 方法：[api-pro-table.md](api-pro-table.md)
- 完整树节点操作 API、NodeExtensions、Ref 方法：[api-pro-tree.md](api-pro-tree.md)
- 完整表单 API、formRef 方法、所有变体组件、原子组件列表：[api-form.md](api-form.md)
- 完整字典 API、所有展示/表单组件、Hooks 用法：[api-dict.md](api-dict.md)

---

## 核心组件使用要点

### HtProTable — 企业级表格

```tsx
import { HtProTable } from '@ht-smart/basic';
import type { HtProColumns, HtHocActionType } from '@ht-smart/basic';

const columns: HtProColumns<DataItem>[] = [
  { title: '名称', dataIndex: 'name', search: true },
  { title: '状态', dataIndex: 'status', valueType: 'select', search: true },
];

<HtProTable
  rowKey="id"
  columns={columns}
  actionRef={actionRef}
  request={async (params) => {
    const res = await fetchList(params);
    return { records: res.data, total: res.total };
  }}
/>
```

**关键属性：**
- `containerHeight` — 容器高度，自动固定表头（推荐替代 `scroll.y`）
- `actionRef` — 调用 `reload()` / `reset()` / `getLastParams()`
- `tableRef` — 调用 `getSelectedRows()` / `setSelectedRowKeys()` / `cleanSelected()`
- `renderToolbarLeft/Right` — 自定义工具栏
- `searchConfig={false}` — 隐藏搜索栏
- `options={{ setting: { cacheKey: 'xxx' }, size: true }}` — 列设置缓存 + 尺寸切换
- `memoizedSelected` — 分页记忆选中

**列配置 `HtProColumns` 扩展属性：**
- `valueType` — 19 种搜索表单类型（input/select/date/dateRange/cascader 等）
- `search: true` — 声明为搜索项
- `fieldProps` — 透传给表单控件的属性
- `ellipsis: 2` — 超出 2 行省略
- `hidden: true` — 隐藏列

---

### HtForm — 高级表单

```tsx
import { HtForm, HtFormText, HtFormDatePicker } from '@ht-smart/basic';

<HtForm
  onFinish={async (values) => {
    await submitApi(values);
    return true; // 返回 true 重置表单
  }}
  initialValues={{ name: '默认值' }}
>
  <HtFormText name="name" label="名称" rules={[{ required: true }]} />
  <HtFormDatePicker name="date" label="日期" format="YYYY-MM-DD" />
</HtForm>
```

**变体组件：**
- `HtModalForm` — Modal 内表单，通过 `trigger` 触发，`onFinish` 返回 `true` 自动关闭
- `HtDrawerForm` — Drawer 内表单，用法同上
- `HtStepsForm` — 分步表单

**formRef 扩展方法：**
- `getFieldsFormatValue()` — 获取格式化后所有值
- `validateFieldsReturnFormatValue()` — 校验并返回格式化值

---

### HtModal / HtDrawer — 弹窗/抽屉

```tsx
// 触发器方式
<HtModal trigger={<Button>打开</Button>} title="标题" onOk={async () => true}>
  内容
</HtModal>

// 受控方式
<HtModal open={open} onOpenChange={setOpen} />

// HtDrawer 额外支持
<HtDrawer resizable draggable maximizable defaultMaximize />
```

**注意：** 弹窗中有表单时，使用 `HtModalForm` / `HtDrawerForm`，不要用 `HtModal` 嵌套 `HtForm`。

---

### HtProTree — 高级树组件

```tsx
import { HtProTree } from '@ht-smart/basic';

<HtProTree
  request={fetchTreeData}
  lazy          // 默认 true，懒加载
  expandLevel={1}
  nodeExtensions={{
    add: { onRemoteAdd: async (data, parent) => ({ success: true, data: newNode }) },
    edit: { onRemoteEdit: async (data, node) => ({ success: true, data: updatedNode }) },
    delete: { onRemoteDelete: async (key, node) => api.delete(key) },
    refresh: true,
  }}
/>
```

**Ref 方法：** `expandAll()` / `collapseAll()` / `refreshNode(key?)` / `refreshRoot()` / `getLocalTreeData()`

**节点操作流程：** `onBeforeAdd/Edit`（验证）→ `onRemoteAdd/Edit`（API 调用，返回 `{ success, data }`）→ `onSuccess`（回调）

---

### HtDict — 字典组件

```tsx
// 根组件配置请求实例
<HtDictContext.Provider value={{ request: axiosInstance }}>
  <App />
</HtDictContext.Provider>

// 展示组件
<HtDictText code="status" value="1" />      // 文本
<HtDictTag code="status" value="1" />       // 标签
<HtDictBadge code="status" value="1" />     // 徽标

// 表单组件
<HtDictSelect code="status" dictType="system" />
<HtDictRadio code="status" />
<HtDictCheckbox code="status" />

// 表单集成（配合 HtForm）
<HtFormDictSelect name="status" label="状态" code="status" />

// Hooks
const { dictData, loading } = useHtDict('status', 'system');
```

`dictType` 可选值：`'system'`（默认）| `'biz'` | `'dynamic'`

---

### ScrollLoadSelect / HtSelect — 选择器

```tsx
// 远程搜索+滚动加载
<ScrollLoadSelect
  request={({ page, size, keyword }) => fetchData({ page, size, keyword })}
  pageSize={30}
  mode="multiple"
  fieldNames={{ label: 'name', value: 'id' }}
  disabledValues={[1, 2]}
  params={{ departmentId: 1 }}
/>

// 静态 options（自动降级为 antd Select）
<HtSelect options={[{ label: '启用', value: 1 }]} />
```

---

### HtNiceModal — API 弹窗

```tsx
// 1. 根组件包裹
<HtNiceModal.Provider><App /></HtNiceModal.Provider>

// 2. 创建弹窗组件
const MyModal = HtNiceModal.create<{ name: string }>(({ name }) => {
  const modal = HtNiceModal.useModal();
  return (
    <HtModal
      open={modal.open}
      onOk={async () => { modal.hide(); modal.resolve(); return true; }}
      onCancel={modal.hide}
      afterClose={() => { modal.resolveHide(); modal.remove(); }}
      destroyOnClose={!modal.keepMounted}
    >
      Hello, {name}!
    </HtModal>
  );
});

// 3. 调用
const result = await HtNiceModal.show(MyModal, { name: 'World' });
```

**注意：** 禁止嵌套使用 `HtNiceModal.Provider`，全应用只用一个。

---

### HtTableSelect — 弹窗表格选择器

```tsx
<HtTableSelect
  title="选择用户"
  value={selected}
  onChange={setSelected}
  columns={columns}
  request={fetchUsers}
  multiple // 多选，默认 true
>
  {(value, actions) => (
    <Button>已选 {value?.length ?? 0} 项</Button>
  )}
</HtTableSelect>

// 带左侧树的布局
<HtTableSelect
  sideContent={({ onChange }) => (
    <HtTree request={fetchDepts} onSelect={(_, { node }) => onChange({ deptId: node.id })} />
  )}
  sideWidth={220}
>
  {(value) => <Button>选择</Button>}
</HtTableSelect>
```

---

### HtCascader / HtRegionCascader

```tsx
// 基础级联，单选时 value 为 string|number，多选时为 (string|number)[]
<HtCascader
  request={(params) => fetchCascaderData(params)}
  fieldNames={{ label: 'name', value: 'id' }} // 默认值
/>

// 区划级联，开箱即用（需 GlobalProvider 上下文）
<HtRegionCascader
  regionLevel={RegionLevel.District} // 限制到区县层级
  versionConfig={{ enabled: true, getVersions: fetchVersions }}
/>
```

---

### HtTree / HtRegionTree

```tsx
<HtTree
  request={fetchTreeData}
  lazy={true}           // 懒加载
  fieldNames={{ title: 'name', key: 'id', children: 'children' }}
  isLeafNode={(node) => node.code?.length >= 6}
/>

// 区划树（需 GlobalProvider）
<HtRegionTree regionLevel={RegionLevel.City} />
```

---

### HtFileUpload / HtImageUpload

```tsx
// 文件上传
<HtProFileUpload
  maxCount={5}
  concurrentNumber={3}
  onBeforeUpload={(file) => file.size < 50 * 1024 * 1024}
  beforeRemove={async () => confirm('确认删除？')}
/>

// 图片上传
<HtImageUpload
  directoryType="private"
  maxCount={1}
  previewable
  onChange={(fileId) => console.log(fileId)}
/>

// 表单集成
<HtFormImageUpload name="avatar" label="头像" fieldProps={{ maxCount: 1 }} />
```

---

### HtCard

```tsx
// 基础
<HtCard title="卡片" extra={<Button>操作</Button>}>
  内容
</HtCard>

// 栅格布局（子卡片）
<HtCard>
  <HtCard colSpan={12}>左侧</HtCard>
  <HtCard colSpan={12}>右侧</HtCard>
</HtCard>

// 折叠
<HtCard collapsible defaultCollapsed title="可折叠卡片" />
```

---

### HtList

```tsx
<HtList
  rowKey="id"
  columns={columns}
  request={fetchList}
  renderItem={(item, index) => <div>{item.name}</div>}
  onItemClick={(item) => console.log(item)}
/>
```

---

### HtDescriptions

```tsx
<HtDescriptions
  title="详情"
  request={() => fetchDetail(id)}
  columns={[
    { title: '名称', dataIndex: 'name' },
    { title: '状态', dataIndex: 'status', valueType: 'select', valueEnum: statusEnum },
  ]}
  bordered
  column={3}
/>
```

---

### HtProRegionTree

```tsx
// 行政区划树，无需配置 request
const treeRef = useRef();
<HtProRegionTree
  ref={treeRef}
  onSelect={(keys, { node }) => setSelected(node)}
/>

// ref 方法
treeRef.current.refreshRoot();
treeRef.current.expandAll();
treeRef.current.collapseAll();
```

---

### HtColorPicker

```tsx
<HtColorPicker
  value={color}
  onChange={(htColor, hex) => setColor(hex)}
  format="hex"
  showText
  allowClear
  presets={[{ label: '推荐色', colors: ['#1677ff', '#52c41a'] }]}
/>
```

---

### HtFloatButton

```tsx
<HtFloatButton.Group activeType="single" active={activeKey} onChange={setActiveKey}>
  <HtFloatButton name="edit" tooltip="编辑" icon={<EditOutlined />} />
  <HtFloatButton name="delete" tooltip="删除" icon={<DeleteOutlined />} />
</HtFloatButton.Group>
```

---

### HtRichTextEditor

```tsx
// 表单集成（推荐）
<HtFormRichTextEditor
  name="content"
  label="内容"
  fieldProps={{
    request: uploadFile, // 图片上传接口
    style: { height: 300 },
  }}
/>

// 基础用法
<HtRichTextEditor
  request={uploadFile}
  onChange={(html) => setContent(html)}
/>
```

---

## 公共注意事项

1. **所有组件均从 `@ht-smart/basic` 导入**
2. **基于 antd@4**，不兼容 antd@5
3. **HtRegionCascader / HtRegionTree / HtProRegionTree** 必须在 `GlobalProvider`（来自 `@ht-smart/workbench`）上下文中使用
4. **HtDict** 组件需要在根组件配置 `HtDictContext.Provider`，提供 axios 请求实例
5. **HtNiceModal** 需要在应用根组件包裹 `HtNiceModal.Provider`，且只能有一个
6. **HtModal / HtDrawer 中有表单** → 用 `HtModalForm` / `HtDrawerForm`，勿嵌套 `HtForm`
7. **表单默认值** → 使用 `initialValues`，勿直接绑定 `value/onChange`
8. **HtProTable `request` 返回格式**：`{ records: TData[], total: number }`
9. **HtProTree `onRemoteAdd/Edit` 返回格式**：`{ success: boolean, data?: any, error?: string }`
10. **`HtFileUpload` 大文件上传** → 自动切片，支持断点续传，可通过 `quicklyUpload` 方法简单调用
 