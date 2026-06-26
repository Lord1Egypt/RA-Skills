# Lookup 弹出选择器

> **包归属**：`@kdcloudjs/shoelace-biz`（业务组件库），非 `@kdcloudjs/shoelace` 基础库。

F7 风格的弹出选择器组件，支持实时搜索、多选、自定义列显示，可与 BOS 平台集成。

> **⚠️ 核心约束：SlLookup 不支持本地数据选择**
>
> SlLookup 是一个**远程搜索组件**，必须配置 `app` + `entity` 属性，由组件内部自动调用后端 API（`/kwc/v1/kd/{app}/kwcform/{entity}/lookupdatas?search=...`）进行搜索和数据获取。
>
> **严禁**在 `sl-lookup-search` 事件中手动设置 `results`/`columns` 来实现本地数据过滤，这不是该组件的设计用途。如果需要本地数据选择，请使用 `SlSelect` 或 `SlCombobox` 等组件。

## 特性概览

- **F7 弹出选择器风格**：点击搜索按钮或输入文字时弹出下拉面板，显示多列数据供用户选择
- **远程搜索**：必须配置 app + entity，组件自动调用后端 API 获取数据，支持防抖
- **单选/多选**：支持单选和多选模式，多选值以分号分隔
- **自定义列**：通过 columns 属性配置面板中显示的字段和表头
- **displayFields/editFields**：分别控制选中后显示值和编辑态显示值
- **BOS 平台集成**：通过 formId 等参数可打开 BOS showconfig 弹窗
- **页脚按钮**：可选的"新增"和"更多"按钮
- **三种尺寸**：small/medium/large
- **表单集成**：支持 required/disabled、表单验证等
- **快捷键**：F7 打开更多弹窗

## 基础用法

最简单的用法，配置 `app` 和 `entity` 后组件自动调用后端 API 搜索数据。

```jsx
import React, { useCallback } from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';

export default () => {
  const handleChange = useCallback((event) => {
    console.log('选中项:', event.detail.value);
  }, []);

  return (
    <SlLookup
      app="bos"
      entity="bos_user"
      placeholder="请输入搜索关键词"
      onSlLookupChange={handleChange}
    />
  );
};
```

## 自定义列

使用 columns 属性配置面板显示的列，包括字段名、表头和列宽。配合 app + entity 使用。

```jsx
import React, { useCallback } from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';

export default () => {
  const columns = [
    { field: 'number', header: '编码', width: '100px' },
    { field: 'name', header: '名称', width: '120px' },
    { field: 'department', header: '部门', width: '100px' },
  ];

  return (
    <SlLookup
      app="hr"
      entity="employee"
      columns={columns}
      placeholder="搜索员工"
    />
  );
};
```

## 实时搜索（API 集成）

配置 app 和 entity 属性后，组件会自动调用 API 获取搜索结果，无需手动处理。

```jsx
import React, { useCallback } from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';

export default () => {
  const columns = [
    { field: 'number', header: '编码', width: '100px' },
    { field: 'name', header: '名称', width: '150px' },
  ];

  const handleChange = useCallback((event) => {
    console.log('选中项:', event.detail.value);
  }, []);

  return (
    <SlLookup
      app="hr"
      entity="employee"
      columns={columns}
      debounce={300}
      placeholder="输入关键词自动搜索"
      onSlLookupChange={handleChange}
    />
  );
};
```

## 多选模式

使用 multiple 属性开启多选，选中的多个值以分号分隔显示。

```jsx
import React, { useCallback } from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';

export default () => {
  const columns = [
    { field: 'number', header: '编码', width: '100px' },
    { field: 'name', header: '名称', width: '120px' },
  ];

  const handleChange = useCallback((event) => {
    // 多选模式下 value 是数组
    const selectedItems = event.detail.value;
    console.log('选中项数组:', selectedItems);
  }, []);

  return (
    <SlLookup
      app="bos"
      entity="bos_user"
      multiple
      columns={columns}
      placeholder="选择标签（可多选）"
      onSlLookupChange={handleChange}
    />
  );
};
```

## displayFields 和 editFields

displayFields 控制选中后输入框显示的字段，editFields 控制获焦编辑时显示的字段。

```jsx
import React from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';

export default () => {
  const columns = [
    { field: 'number', header: '编码', width: '100px' },
    { field: 'name', header: '名称', width: '150px' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div>
        <p style={{ fontSize: '14px', marginBottom: '8px' }}>显示名称，编辑时显示编码：</p>
        <SlLookup
          app="bos"
          entity="bos_user"
          columns={columns}
          displayFields={['name']}
          editFields={['number']}
          placeholder="选择商品"
        />
      </div>
      <div>
        <p style={{ fontSize: '14px', marginBottom: '8px' }}>显示编码+名称：</p>
        <SlLookup
          app="bos"
          entity="bos_user"
          columns={columns}
          displayFields={['number', 'name']}
          editFields={['number', 'name']}
          separator=" - "
          placeholder="选择商品"
        />
      </div>
    </div>
  );
};
```

## 自定义分隔符

使用 separator 属性控制多字段显示时的分隔符。

```jsx
import React from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';

export default () => {
  const columns = [
    { field: 'number', header: '编码', width: '100px' },
    { field: 'name', header: '名称', width: '120px' },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <SlLookup
        app="bos"
        entity="bos_user"
        columns={columns}
        displayFields={['number', 'name']}
        separator=" | "
        placeholder="分隔符: |"
      />
      <SlLookup
        app="bos"
        entity="bos_user"
        columns={columns}
        displayFields={['number', 'name']}
        separator=" - "
        placeholder="分隔符: -"
      />
    </div>
  );
};
```

## 页脚按钮

通过 showAddButton 和 showMoreButton 控制面板底部的"新增"和"更多"按钮显示。

```jsx
import React, { useCallback } from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';

export default () => {
  const handleAdd = useCallback(() => {
    console.log('点击新增按钮');
  }, []);

  const handleMore = useCallback(() => {
    console.log('点击更多按钮或按 F7');
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <SlLookup
        app="bos"
        entity="bos_user"
        showAddButton
        showMoreButton
        placeholder="显示新增和更多按钮"
        onSlLookupAdd={handleAdd}
        onSlLookupMore={handleMore}
      />
      <SlLookup
        app="bos"
        entity="bos_user"
        showAddButton={false}
        showMoreButton
        placeholder="仅显示更多按钮"
        onSlLookupMore={handleMore}
      />
      <SlLookup
        app="bos"
        entity="bos_user"
        showAddButton={false}
        showMoreButton={false}
        placeholder="隐藏所有页脚按钮"
      />
    </div>
  );
};
```

## 禁用与必填

使用 disabled 禁用组件，使用 required 设置必填验证。

```jsx
import React from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';

export default () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <SlLookup
        label="禁用状态"
        disabled
        value="已选择的值"
        placeholder="禁用的 lookup"
      />
      <SlLookup
        label="必填字段"
        required
        placeholder="此字段为必填"
        helpText="请选择一个选项"
      />
    </div>
  );
};
```

## 尺寸变体

支持 small、medium、large 三种尺寸。

```jsx
import React from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';

export default () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <SlLookup size="small" placeholder="小尺寸 (small)" />
      <SlLookup size="medium" placeholder="中尺寸 (medium)" />
      <SlLookup size="large" placeholder="大尺寸 (large)" />
    </div>
  );
};
```

## 监听事件

监听 search、change、clear 等事件处理用户交互。

```jsx
import React, { useState, useCallback } from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';

export default () => {
  const [eventLog, setEventLog] = useState([]);

  const logEvent = (eventName, detail) => {
    setEventLog(prev => [...prev.slice(-4), `${eventName}: ${JSON.stringify(detail)}`]);
  };

  const handleSearch = useCallback((event) => {
    logEvent('sl-lookup-search', event.detail);
  }, []);

  const handleChange = useCallback((event) => {
    logEvent('sl-lookup-change', event.detail);
  }, []);

  const handleClear = useCallback(() => {
    logEvent('sl-lookup-clear', {});
  }, []);

  const handleFocus = useCallback(() => {
    logEvent('sl-focus', {});
  }, []);

  const handleBlur = useCallback(() => {
    logEvent('sl-blur', {});
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <SlLookup
        app="bos"
        entity="bos_user"
        clearable
        placeholder="操作后查看事件日志"
        onSlLookupSearch={handleSearch}
        onSlLookupChange={handleChange}
        onSlLookupClear={handleClear}
        onSlFocus={handleFocus}
        onSlBlur={handleBlur}
      />
      <div style={{ padding: '12px', background: '#f5f5f5', borderRadius: '4px', fontSize: '12px' }}>
        <strong>事件日志：</strong>
        {eventLog.map((log, index) => (
          <p key={index} style={{ margin: '4px 0', fontFamily: 'monospace' }}>{log}</p>
        ))}
      </div>
    </div>
  );
};
```

## 通过 ref 控制

使用 ref 操作 show/hide/focus 等方法。注意：show() 仅在组件已有搜索结果时才会打开面板。

```jsx
import React, { useRef, useCallback } from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const lookupRef = useRef(null);

  const handleHide = useCallback(async () => {
    if (lookupRef.current) {
      await lookupRef.current.hide();
    }
  }, []);

  const handleFocus = useCallback(() => {
    if (lookupRef.current) {
      lookupRef.current.focus();
    }
  }, []);

  const handleCheckValidity = useCallback(() => {
    if (lookupRef.current) {
      const isValid = lookupRef.current.checkValidity();
      alert(`表单验证结果: ${isValid ? '有效' : '无效'}`);
    }
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        <SlButton size="small" onClick={handleHide}>hide()</SlButton>
        <SlButton size="small" onClick={handleFocus}>focus()</SlButton>
        <SlButton size="small" onClick={handleCheckValidity}>checkValidity()</SlButton>
      </div>
      <SlLookup
        ref={lookupRef}
        app="bos"
        entity="bos_user"
        required
        label="通过 ref 控制"
        placeholder="使用上方按钮控制"
      />
    </div>
  );
};
```

## BOS 平台集成

配置 formId、parentPageId 等参数与 BOS showconfig 弹窗集成。

```jsx
import React, { useCallback } from "react";
import SlLookup from '@kdcloudjs/shoelace-biz/dist/react/lookup/index.js';

export default () => {
  const columns = [
    { field: 'number', header: '编码', width: '100px' },
    { field: 'name', header: '名称', width: '150px' },
  ];

  const handleMore = useCallback(() => {
    console.log('打开 BOS showconfig 弹窗');
    // 组件会根据 formId、parentPageId 等参数自动构建弹窗参数
  }, []);

  const handleChange = useCallback((event) => {
    // BOS 弹窗选中数据后触发
    console.log('BOS 选中数据:', event.detail.value);
  }, []);

  return (
    <SlLookup
      app="hr"
      entity="employee"
      formId="hr_employee_list"
      parentPageId="page_001"
      checkRightAppId="hr_app"
      callBackId="callback_001"
      columns={columns}
      showMoreButton
      placeholder="点击更多或按 F7 打开 BOS 弹窗"
      onSlLookupMore={handleMore}
      onSlLookupChange={handleChange}
    />
  );
};
```

## Properties

| 属性 | HTML 属性 | 类型 | 默认值 | 说明 |
|-----|----------|------|-------|------|
| name | name | `string` | `''` | 表单提交时的字段名 |
| value | value | `string` | `''` | 当前选中值 |
| defaultValue | - | `string` | `''` | 表单控制的默认值 |
| size | size | `'small' \| 'medium' \| 'large'` | `'medium'` | 输入框尺寸 |
| placeholder | placeholder | `string` | `''` | 输入框占位符 |
| disabled | disabled | `boolean` | `false` | 禁用状态 |
| clearable | clearable | `boolean` | `true` | 是否显示清除按钮 |
| open | open | `boolean` | `false` | 下拉面板是否打开 |
| hoist | hoist | `boolean` | `true` | 防止面板在 overflow 容器中被裁剪 |
| filled | filled | `boolean` | `false` | 使用填充样式 |
| label | label | `string` | `''` | 输入框标签 |
| placement | placement | `'top' \| 'bottom' \| 'top-start' \| 'top-end' \| 'bottom-start' \| 'bottom-end'` | `'bottom-start'` | 面板首选位置 |
| helpText | help-text | `string` | `''` | 帮助文本 |
| form | form | `string` | `''` | 关联的表单 ID |
| required | required | `boolean` | `false` | 必填字段 |
| results | - | `LookupResult[]` | `[]` | 搜索结果数据数组 |
| columns | - | `LookupColumn[]` | `[]` | 面板列定义（对象数组传递） |
| showAddButton | show-add-button | `boolean` | `true` | 显示页脚"新增"按钮 |
| showMoreButton | show-more-button | `boolean` | `true` | 显示页脚"更多"按钮 |
| app | app | `string` | `''` | API 请求的应用编码 |
| entity | entity | `string` | `''` | API 请求的实体名称 |
| formId | form-id | `string` | `''` | BOS showconfig 子页面标识 |
| parentPageId | parent-page-id | `string` | `''` | BOS showconfig 父页面 ID |
| checkRightAppId | check-right-app-id | `string` | `''` | BOS showconfig 权限检查应用 ID |
| callBackId | call-back-id | `string` | `''` | BOS showconfig 回调 ID |
| apiUrl | api-url | `string` | `''` | 自定义 API 基础 URL |
| debounce | debounce | `number` | `300` | 搜索防抖延迟（毫秒） |
| displayFields | display-fields | `string[]` | `['name']` | 选中后输入框显示的字段列表 |
| editFields | edit-fields | `string[]` | `['name']` | 获焦时编辑显示的字段列表 |
| editStyle | edit-style | `'button' \| 'input'` | `'input'` | 编辑触发模式 |
| separator | separator | `string` | `','` | 多字段值拼接分隔符 |
| multiple | multiple | `boolean` | `false` | 是否允许多选 |

## Events

| 事件名 | React 属性 | 说明 | 事件详情 |
|--------|-----------|------|---------|
| sl-lookup-search | `onSlLookupSearch` | 点击搜索按钮或输入时触发 | `{ value: string; results?: any[] }` |
| sl-lookup-change | `onSlLookupChange` | 选中项变化时触发 | `{ value: StandardData \| StandardData[] }` |
| sl-lookup-clear | `onSlLookupClear` | 点击清除按钮时触发 | - |
| sl-clear | `onSlClear` | 清除按钮（向后兼容） | - |
| sl-lookup-add | `onSlLookupAdd` | 点击"新增"按钮时触发 | - |
| sl-lookup-more | `onSlLookupMore` | 点击"更多"按钮或按 F7 键时触发 | - |
| sl-focus | `onSlFocus` | 获得焦点时触发 | - |
| sl-blur | `onSlBlur` | 失去焦点时触发 | - |

## Public Methods

| 方法名 | 参数 | 返回值 | 说明 |
|-------|------|-------|------|
| show() | - | `Promise<void>` | 显示下拉面板 |
| hide() | - | `Promise<void>` | 隐藏下拉面板 |
| focus(options?) | `FocusOptions` | `void` | 设置焦点 |
| blur() | - | `void` | 移除焦点 |
| checkValidity() | - | `boolean` | 检查有效性 |
| reportValidity() | - | `boolean` | 检查有效性并显示验证消息 |
| setCustomValidity(message) | `string` | `void` | 设置自定义验证消息 |
| getForm() | - | `HTMLFormElement \| null` | 获取关联表单 |

## CSS Parts

| Part 名称 | 描述 |
|-----------|------|
| form-control | 表单控制顶层容器 |
| form-control-label | 标签容器 |
| form-control-input | 输入框容器 |
| form-control-help-text | 帮助文本容器 |
| combobox | 包装前缀、输入框、按钮的容器 |
| display-input | 实际的 input 元素 |
| clear-button | 清除按钮 |
| search-button | 搜索按钮 |
| panel | 下拉面板容器 |
| panel-header | 面板表头 |
| panel-body | 面板主体 |
| panel-footer | 面板页脚 |
| empty | 空状态区域 |
| prefix | 前缀区域 |
| suffix | 后缀区域 |

## Slots

| 插槽名称 | 描述 |
|---------|------|
| label | 标签的插槽 |
| prefix | 输入框前的图标或元素 |
| suffix | 输入框后的图标或元素 |
| search-icon | 搜索按钮图标 |
| clear-icon | 清除按钮图标 |
| empty | 无结果时显示的内容（默认 '暂无数据'） |

## 接口定义

```typescript
interface LookupColumn {
  field: string;     // 对应数据字段名
  header: string;    // 列表头显示文本
  width?: string;    // 列宽（CSS 值，如 "120px"）
}

interface LookupResult {
  [key: string]: any;
  disabled?: boolean;   // 是否禁用该行
}

// sl-lookup-change 事件返回的标准数据格式
interface StandardData {
  id: string | number;
  name: string;
  number: string;
}
```

## API 路径

- 默认: `/kwc/v1/kd/{app}/kwcform/{entity}/lookupdatas?search={searchValue}`
- 自定义: `{apiUrl}/kwc/v1/kd/{app}/kwcform/{entity}/lookupdatas?search={searchValue}`

## 常见问题

### Q: SlLookup 能否做本地数据选择？

A: **不能**。SlLookup 是远程搜索组件，必须配置 `app` + `entity`，由组件自动调用后端 API 获取数据。如需本地数据选择，请使用 `SlSelect` 或 `SlCombobox`。

### Q: app 和 entity 必须配置吗？

A: **是的**。`app` 指定应用编码，`entity` 指定实体名称，组件会自动请求 `/kwc/v1/kd/{app}/kwcform/{entity}/lookupdatas?search=...` 获取搜索结果。

### Q: displayFields 和 editFields 有什么区别？

A: 
- **displayFields**：选中后输入框显示的字段，如 `['name']` 显示名称
- **editFields**：获焦进入编辑态时显示的字段，通常用于显示编码以便快速搜索

例如：`displayFields={['name']} editFields={['number']}` 表示选中后显示名称，点击编辑时显示编码。

### Q: 多选模式下值的格式是什么？

A: 多选模式下：
- 输入框显示值以分号分隔，如 "张三;李四;王五"
- `sl-lookup-change` 事件的 `detail.value` 是数组格式：`StandardData[]`

```jsx
const handleChange = (event) => {
  const selectedItems = event.detail.value; // StandardData[]
  console.log(selectedItems); // [{ id: '1', name: '张三', number: 'EMP001' }, ...]
};
```

### Q: 如何与 BOS 平台集成？

A: 配置以下属性实现 BOS showconfig 弹窗集成：

```jsx
<SlLookup
  formId="hr_employee_list"      // 子页面标识
  parentPageId="page_001"         // 父页面 ID
  checkRightAppId="hr_app"        // 权限检查应用 ID
  callBackId="callback_001"       // 回调 ID
  onSlLookupMore={handleMore}     // 监听更多按钮或 F7 按键
/>
```

点击"更多"按钮或按 F7 键时触发 `sl-lookup-more` 事件，组件会根据配置参数打开 BOS 弹窗。

### Q: sl-lookup-change 事件的 detail 格式是什么？

A: 事件详情包含 `value` 字段：
- 单选模式：`{ value: StandardData }` 
- 多选模式：`{ value: StandardData[] }`

StandardData 格式：
```typescript
interface StandardData {
  id: string | number;
  name: string;
  number: string;
}
```

### Q: 如何自定义面板列宽？

A: 在 columns 配置中设置 width 属性：

```jsx
const columns = [
  { field: 'number', header: '编码', width: '80px' },
  { field: 'name', header: '名称', width: '150px' },
  { field: 'department', header: '部门', width: '120px' },
];

<SlLookup columns={columns} />
```
