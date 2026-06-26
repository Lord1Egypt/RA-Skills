# HtDict 完整 API 参考

## 初始化配置

在应用根组件配置一次，所有字典组件共享：

```tsx
import { HtDictContext } from '@ht-smart/basic';

<HtDictContext.Provider value={{ request: axiosInstance }}>
  <App />
</HtDictContext.Provider>
```

## 字典类型（dictType）

| 值 | 说明 | 接口地址 |
|----|------|----------|
| `'system'`（默认） | 系统字典 | `/htwisdom-system/dict/sysytem/dictionary` |
| `'biz'` | 业务字典 | `/htwisdom-system/dict/business/dictionary` |
| `'dynamic'` | 动态字典 | `/htwisdom-system/dict/dynamic/dictionary` |

请求参数：`{ codes: string }` — 字典编码，多个用逗号分隔

## 字典数据结构

```ts
interface DictType {
  dictKey: string;      // 字典键（对应 value）
  dictValue: string;    // 字典值（对应 label）
  color?: string;       // 显示颜色
  disabled?: boolean;   // 是否禁用
  children?: DictType[];
  [key: string]: any;
}
```

## 共同基础属性

所有字典组件均支持：

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `code` | 字典编码（必填） | `string` | - |
| `dictType` | 字典类型 | `'system' \| 'biz' \| 'dynamic'` | `'system'` |
| `postData` | 数据预处理函数 | `(items: DictType[]) => DictType[]` | - |

## 展示组件

### HtDictText — 文本展示

```tsx
<HtDictText code="status" value="1" />
```

| 属性 | 说明 | 类型 |
|------|------|------|
| `value` | 字典键值 | `string \| number` |
| `color` | 文字颜色（优先于字典配置） | `string` |

### HtDictTag — 标签展示

```tsx
<HtDictTag code="status" value="1" />
```

支持 antd `Tag` 所有属性，`color` 自动从字典配置读取。

### HtDictBadge — 徽标展示

```tsx
<HtDictBadge code="status" value="1" />
```

支持 antd `Badge` 所有属性，`color`/`status` 自动从字典配置读取。

## 表单组件

### HtDictSelect — 下拉选择

```tsx
<HtDictSelect
  code="status"
  dictType="system"
  allowClear
  placeholder="请选择状态"
  mode="multiple"  // 多选
/>
```

支持 antd `Select` 所有属性。

### HtDictRadio — 单选框组

```tsx
<HtDictRadio code="status" />
```

支持 antd `Radio.Group` 所有属性。

### HtDictCheckbox — 复选框组

```tsx
<HtDictCheckbox code="status" />
```

支持 antd `Checkbox.Group` 所有属性。

## Form.Item 集成组件

与 HtForm 配合使用，已内置 `Form.Item` 包装：

```tsx
// 支持所有 Form.Item 属性（name、label、rules 等）
<HtFormDictSelect
  name="status"
  label="状态"
  code="status"
  dictType="system"
  rules={[{ required: true, message: '请选择状态' }]}
  fieldProps={{ allowClear: true }}  // 传给 HtDictSelect 的属性
/>

<HtFormDictRadio
  name="type"
  label="类型"
  code="type"
/>

<HtFormDictCheckbox
  name="tags"
  label="标签"
  code="tags"
/>
```

## Hooks

### useHtDict

```tsx
import { useHtDict } from '@ht-smart/basic';

// 单个字典
const { dictData, loading } = useHtDict('status', 'system');
// dictData: DictType[]

// 多个字典
const codes = ['status', 'type'] as const;
const { dictData, loading } = useHtDict(codes);
// dictData: { status: DictType[], type: DictType[] }
```

## 自定义渲染（HtDict 基础组件）

```tsx
<HtDict code="status" dictType="system">
  {(dict) => {
    const { items, loading } = dict;
    return <MyCustomComponent loading={loading} items={items} />;
  }}
</HtDict>
```

## 数据预处理

```tsx
// 过滤禁用项
<HtDictSelect
  code="status"
  postData={(items) => items.filter((item) => !item.disabled)}
/>

// 追加自定义选项
<HtDictSelect
  code="status"
  postData={(items) => [
    ...items,
    { dictKey: 'all', dictValue: '全部', color: '' },
  ]}
/>
```

## HtProTable 集成

在列配置中使用字典：

```tsx
const columns: HtProColumns[] = [
  {
    title: '状态',
    dataIndex: 'status',
    valueType: 'selectDict',  // 使用字典选择器
    dictCode: 'status',
    dictType: 'system',
    // 列展示使用 DictTag
    render: (_, record) => <HtDictTag code="status" value={record.status} />,
  },
];
```
