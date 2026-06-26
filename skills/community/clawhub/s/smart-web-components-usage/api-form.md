# HtForm 完整 API 参考

## HtForm Props（继承 antd Form）

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `onFinish` | 提交成功回调，返回 `true` 自动重置表单 | `(values) => Promise<void \| boolean>` | - |
| `onReset` | 点击重置按钮回调 | `(e) => void` | - |
| `initialValues` | 表单默认值，**勿用 value/onChange 直接绑定** | `object` | - |
| `request` | 远程获取初始值，返回值覆盖 initialValues | `(params) => Promise<data>` | - |
| `params` | 配合 request 使用的参数 | `Record` | - |
| `submitter` | 提交按钮配置 | `boolean \| SubmitterProps` | `true` |
| `formRef` | 获取增强表单实例 | `MutableRefObject<HtFormInstance>` | - |
| `grid` | 开启栅格化布局 | `boolean` | - |
| `rowProps` | grid 模式下传给 Row | `RowProps` | `{ gutter: 8 }` |
| `dateFormatter` | 日期格式化 | `'string' \| 'number' \| false` | `'string'` |
| `omitNil` | 自动清空 null/undefined | `boolean` | `true` |
| `syncToUrl` | 同步参数到 url | `true \| ((values, type) => values)` | - |
| `isKeyPressSubmit` | 回车提交 | `boolean` | - |
| `autoFocusFirstInput` | 自动 focus 第一个输入框 | `boolean` | - |

## HtFormInstance 扩展方法

在原有 antd `FormInstance` 基础上新增：

```ts
// 获取格式化后的所有值（日期等自动转换）
formRef.current.getFieldsFormatValue()
formRef.current.getFieldsFormatValue(true) // 包含未托管字段

// 获取格式化后的单个值
formRef.current.getFieldFormatValue(['date'])

// 获取格式化后的单个值（含 key）
formRef.current.getFieldFormatValueObject('date') // => { date: '2024-01-01' }

// 校验并返回格式化后所有值
formRef.current.validateFieldsReturnFormatValue()
```

## SubmitterProps

| 参数 | 说明 | 类型 |
|------|------|------|
| `onSubmit` | 提交方法 | `() => void` |
| `onReset` | 重置方法 | `() => void` |
| `searchConfig` | 按钮文案配置 | `{ resetText, submitText }` |
| `submitButtonProps` | 提交按钮 props | `ButtonProps` |
| `resetButtonProps` | 重置按钮 props | `ButtonProps` |
| `render` | 完全自定义，返回 `false` 不渲染 | `false \| ((props, dom[]) => ReactNode[])` |

## HtModalForm Props

继承 HtForm，额外属性：

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `trigger` | 触发打开的元素 | `ReactNode` | - |
| `open` | 受控打开状态 | `boolean` | - |
| `onOpenChange` | open 变化回调 | `(open: boolean) => void` | - |
| `title` | 弹框标题 | `ReactNode` | - |
| `width` | 弹框宽度 | `number` | - |
| `onShow` | 弹窗打开时触发 | `() => void` | - |
| `onFinish` | 提交回调，返回 `true` 关闭弹窗 | `(values) => Promise<boolean>` | - |
| `modalProps` | 透传给 Modal 的属性 | `ModalProps` | - |
| `submitTimeout` | 禁用取消按钮的超时（ms） | `number` | - |

## HtDrawerForm Props

继承 HtForm，额外属性：

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `trigger` | 触发打开的元素 | `ReactNode` | - |
| `open` | 受控打开状态 | `boolean` | - |
| `onOpenChange` | open 变化回调 | `(open: boolean) => void` | - |
| `title` | 抽屉标题 | `ReactNode` | - |
| `width` | 抽屉宽度 | `number` | - |
| `onShow` | 抽屉打开时触发 | `() => void` | - |
| `onFinish` | 提交回调，返回 `true` 关闭抽屉 | `(values) => Promise<boolean>` | - |
| `drawerProps` | 透传给 Drawer 的属性 | `DrawerProps` | - |
| `submitTimeout` | 禁用取消按钮的超时（ms） | `number` | - |

## HtStepsForm Props

| 参数 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `current` | 当前步骤，从 0 开始 | `number` | `0` |
| `onCurrentChange` | 步骤变化回调 | `(current: number) => void` | - |
| `onFinish` | 最后一步提交回调，返回 `true` 重置 | `(values) => void \| boolean` | - |
| `stepsProps` | Steps 组件属性（去掉 current/onChange） | `StepsProps` | - |
| `formRef` | StepForm action 引用 | `MutableRefObject<FormInstance>` | - |

## 常用表单原子组件

所有原子组件均从 `@ht-smart/basic` 导入，命名规则：`HtForm` + 类型名。

| 组件 | 说明 |
|------|------|
| `HtFormText` | 文本输入 |
| `HtFormTextArea` | 多行文本 |
| `HtFormDigit` | 数字输入 |
| `HtFormSelect` | 下拉选择 |
| `HtFormDatePicker` | 日期选择 |
| `HtFormTimePicker` | 时间选择 |
| `HtFormDateRangePicker` | 日期范围 |
| `HtFormSwitch` | 开关 |
| `HtFormCheckbox` | 复选框 |
| `HtFormRadio` | 单选框 |
| `HtFormUploadDragger` | 拖拽上传 |
| `HtFormDictSelect` | 字典下拉 |
| `HtFormDictRadio` | 字典单选 |
| `HtFormDictCheckbox` | 字典复选 |
| `HtFormImageUpload` | 图片上传 |
| `HtFormRichTextEditor` | 富文本 |

每个原子组件均支持标准 `Form.Item` 