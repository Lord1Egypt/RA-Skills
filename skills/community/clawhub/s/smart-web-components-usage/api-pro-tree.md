# HtProTree 完整 API 参考

## 公共 Props

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `request` | `(params) => Promise<any>` | - | 数据请求函数 |
| `lazy` | `boolean` | `true` | `true` 懒加载；`false` 全量加载 |
| `expandLevel` | `number` | `1` | 初始展开层级，`999` 展开全部 |
| `toggleExpandLevel` | `number` | `1` | 头部展开按钮点击后的展开层级 |
| `autoExpandParent` | `boolean` | `true` | 搜索命中时自动展开父节点 |
| `height` | `string \| number` | - | 组件整体高度，设置后启用虚拟滚动 |
| `nodeExtensions` | `NodeExtensions` | - | 节点增删改查扩展配置 |
| `headerLeft` | `ReactNode \| ((treeData) => ReactNode)` | - | 树顶部左侧标题插槽 |
| `extraActions` | `ExtraActionItem[] \| ((treeData) => ExtraActionItem[])` | - | 树顶部右侧自定义操作 |
| `headerMenuItems` | `MenuProps['items'] \| ((ctx: HeaderMenuContext) => items)` | - | 顶部更多操作下拉菜单 |
| `onHeaderMenuClick` | `({ key, context }) => void` | - | 头部菜单点击事件 |
| `className` / `style` | - | - | 根容器样式 |
| `headerClassName` / `headerStyle` | - | - | 头部工具栏样式 |
| `treeWrapperClassName` / `treeWrapperStyle` | - | - | 树内容区样式 |

## NodeExtensions 配置

| 属性 | 类型 | 说明 |
|------|------|------|
| `refresh` | `boolean` | 显示刷新按钮 |
| `add` | `AddNodeConfig` | 新增子节点配置 |
| `edit` | `EditNodeConfig` | 编辑节点配置 |
| `delete` | `DeleteNodeConfig` | 删除节点配置 |
| `extra` | `MenuProps['items'] \| ((node) => items)` | 自定义节点右键菜单 |

## AddNodeConfig

| 属性 | 类型 | 说明 |
|------|------|------|
| `onBeforeAdd` | `(newData, parentNode) => boolean \| Promise<boolean>` | 新增前验证，返回 `false` 终止 |
| `onRemoteAdd` | `(newData, parentNode) => Promise<{ success: boolean, data?: any, error?: string }>` | 远程新增，返回完整节点数据 |
| `onSuccess` | `(newNode, parentNode) => void` | 新增成功回调 |
| `render` | `(props: RenderProps) => ReactNode` | 自定义新增界面 |

## EditNodeConfig

| 属性 | 类型 | 说明 |
|------|------|------|
| `onBeforeEdit` | `(editedData, currentNode) => boolean \| Promise<boolean>` | 编辑前验证，返回 `false` 终止 |
| `onRemoteEdit` | `(editedData, currentNode) => Promise<{ success: boolean, data?: any, error?: string }>` | 远程编辑，返回更新后完整节点数据 |
| `onSuccess` | `(editedNode, originalNode) => void` | 编辑成功回调 |
| `render` | `(props: RenderProps) => ReactNode` | 自定义编辑界面 |

## DeleteNodeConfig

| 属性 | 类型 | 说明 |
|------|------|------|
| `onRemoteDelete` | `(nodeKey, nodeData) => Promise<any>` | 远程删除方法 |
| `onSuccess` | `() => void` | 删除成功回调 |

## ExtraActionItem

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `key` | `string` | - | 唯一标识（必填） |
| `icon` | `ReactNode` | - | 操作图标（必填） |
| `tooltip` | `ReactNode` | - | Tooltip 提示文字 |
| `onClick` | `() => void` | - | 点击回调 |
| `disabled` | `boolean` | `false` | 是否禁用 |

## HeaderMenuContext

| 属性/方法 | 类型 | 说明 |
|-----------|------|------|
| `treeData` | `any[]` | 当前树数据（搜索后） |
| `refreshRoot()` | `() => Promise<void>` | 刷新根节点 |
| `expandAll()` | `() => void` | 展开所有节点 |
| `collapseAll()` | `() => void` | 收起所有节点 |
| `getLocalTreeData()` | `() => any[]` | 获取本地完整树数据 |

## HtProTreeRef 方法

```ts
const treeRef = useRef<HtProTreeRef>();
<HtProTree ref={treeRef} />

treeRef.current.expandAll()           // 展开所有节点
treeRef.current.collapseAll()         // 收起所有节点
treeRef.current.refreshNode(nodeKey?) // 刷新指定节点，不传则刷新根节点
treeRef.current.refreshRoot()         // 刷新根节点
treeRef.current.getLocalTreeData()    // 获取本地树数据
```

## 节点操作完整示例

```tsx
<HtProTree
  request={fetchDeptTree}
  lazy
  expandLevel={1}
  nodeExtensions={{
    refresh: true,
    add: {
      onBeforeAdd: async (data, parent) => {
        if (!data.name) { message.error('名称不能为空'); return false; }
        return true;
      },
      onRemoteAdd: async (data, parent) => {
        try {
          const res = await api.addDept({ ...data, parentId: parent.id });
          return { success: true, data: res.data };
        } catch (e) {
          return { success: false, error: e.message };
        }
      },
      onSuccess: (newNode) => message.success(`"${newNode.name}" 创建成功`),
    },
    edit: {
      onRemoteEdit: async (data, node) => {
        const res = await api.updateDept({ id: node.id, ...data });
        return { success: true, data: res.data };
      },
      onSuccess: (node) => message.success('修改成功'),
    },
    delete: {
      onRemoteDelete: async (key) => api.deleteDept(key),
      onSuccess: () => message.success('删除成功'),
    },
  }}
/>
```

## 注意事项

- `lazy=true` 时，`expandLevel` 只展开**已加载**的节点，不触发新请求
- `expandLevel` 控制初始展开，`toggleExpandLevel` 控制按钮点击后的展开
- `onRemoteAdd/Edit` 必须返回 `{ success: boolean, data? }` 格式
- `isLeafNode` 返回 `true` 的节点不再加载子级
