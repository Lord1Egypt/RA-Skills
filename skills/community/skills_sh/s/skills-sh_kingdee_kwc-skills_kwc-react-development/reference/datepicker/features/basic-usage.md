# 基础用法

[返回目录](../index.md)

## 功能说明

Datepicker 组件的基础用法包括：日期选择、设置占位符、默认值、标签、帮助文本、不同尺寸、可清除、禁用、只读等基础功能。

## API 属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `value` | 当前日期值（格式：`yyyy-MM-dd`） | `string` | `''` |
| `placeholder` | 占位提示文本 | `string` | `''` |
| `label` | 标签文本 | `string` | `''` |
| `help-text` | 帮助提示文本 | `string` | `''` |
| `size` | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| `clearable` | 是否可清除 | `boolean` | `false` |
| `disabled` | 是否禁用 | `boolean` | `false` |
| `readonly` | 是否只读 | `boolean` | `false` |

---

## 代码示例

### 示例1：最简日期选择器

最基础的用法，点击输入框弹出日历面板选择日期。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => <SlDatepicker style={{ width: "230px" }} />;
```

---

### 示例2：设置默认值

通过 `value` 属性设置初始日期值，格式为 `yyyy-MM-dd`。通过 `onSlChange` 属性监听值变化。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => {
  const [selectedDate, setSelectedDate] = useState("2024-06-15");

  const handleChange = useCallback((event) => {
    setSelectedDate(event.target.value);
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "8px", width: "230px" }}>
      <SlDatepicker label="入职日期" value="2024-06-15" onSlChange={handleChange} />
      <div style={{ fontSize: "14px", color: "#666" }}>当前值: {selectedDate}</div>
    </div>
  );
};
```

---

### 示例3：标签与帮助文本

通过 `label` 属性为选择器提供标签，`help-text` 属性添加描述性帮助文本。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => (
  <div style={{ display: "flex", flexDirection: "column", gap: "16px", width: "230px" }}>
    <SlDatepicker label="Select a date" />
    <SlDatepicker
      label="Datepicker"
      help-text="Select a date for your appointment"
    />
  </div>
);
```

---

### 示例4：占位符

使用 `placeholder` 属性添加占位文本。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => (
  <SlDatepicker style={{ width: "230px" }} placeholder="YYYY-MM-DD" />
);
```

---

### 示例5：不同尺寸

通过 `size` 属性设置三种尺寸：`small`、`medium`（默认）、`large`。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

const css = `
  .datepicker-group {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 230px;
  }
`;

export default () => (
  <>
    <div className="datepicker-group">
      <SlDatepicker placeholder="Small" size="small" />
      <SlDatepicker placeholder="Medium" size="medium" />
      <SlDatepicker placeholder="Large" size="large" />
    </div>
    <style>{css}</style>
  </>
);
```

---

### 示例6：可清除

添加 `clearable` 属性可在选择器有内容时显示清除按钮。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => (
  <SlDatepicker
    style={{ width: "230px" }}
    placeholder="Select a date With clearable"
    clearable
  />
);
```

---

### 示例7：禁用与只读

`disabled` 禁止所有交互，`readonly` 允许查看值但不允许修改。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => (
  <div style={{ display: "flex", flexDirection: "column", gap: "16px", width: "230px" }}>
    <SlDatepicker label="禁用状态" value="2024-01-15" disabled />
    <SlDatepicker label="只读状态" value="2024-01-15" readonly />
    <SlDatepicker label="正常状态" value="2024-01-15" />
  </div>
);
```

---

### 示例8：动态控制值

通过 `ref` 动态读取和设置日期选择器的值。

```jsx
import React, { useRef } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const datepickerRef = useRef(null);

  const handleSetToday = () => {
    const today = new Date();
    const formatted = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
    if (datepickerRef.current) {
      datepickerRef.current.value = formatted;
    }
  };

  const handleClear = () => {
    if (datepickerRef.current) {
      datepickerRef.current.value = "";
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "280px" }}>
      <div style={{ display: "flex", gap: "8px" }}>
        <SlButton size="small" onClick={handleSetToday}>设为今天</SlButton>
        <SlButton size="small" onClick={handleClear}>清空</SlButton>
      </div>
      <SlDatepicker ref={datepickerRef} placeholder="选择日期" />
    </div>
  );
};
```

---

## 注意事项

1. **值格式**：`value` 属性的格式必须为 `yyyy-MM-dd`（如 `2024-01-15`），不符合格式的值会被自动清空
2. **事件绑定**：在 JSX 中使用 `onSlChange`、`onSlInput` 等 `onSl*` 前缀属性绑定事件
3. **clearable 默认关闭**：React 版本 `clearable` 默认为 `false`，如需要请显式设置
4. **响应式更新**：通过 `ref.current.value = xxx` 直接赋值方式设置值；通过 React state 传递 `value` 属性也可以
5. **输入分隔符**：支持 `-`、`/`、`.` 三种分隔符输入，输出统一为 `-` 分隔的标准格式

[返回目录](../index.md)
