# 样式定制

[返回目录](../index.md)

## 功能说明

`SlDatepicker` 提供多种样式定制方式：通过内置属性（`size`、`filled`、`pill`）快速切换外观风格，通过 Slots 自定义标签、前缀、后缀等内容，通过 CSS Parts 深度自定义组件各部分样式。

## API 属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `size` | 尺寸 | `'small' \| 'medium' \| 'large'` | `'medium'` |
| `filled` | 填充样式 | `boolean` | `false` |
| `pill` | 圆角药丸样式 | `boolean` | `false` |
| `hoist` | 弹出层提升到固定定位 | `boolean` | `false` |

### Slots

| Slot | 说明 |
|------|------|
| `label` | 自定义标签内容 |
| `prefix` | 输入框前缀 |
| `suffix` | 输入框后缀（默认为日历图标） |
| `clear-icon` | 自定义清除按钮图标 |
| `help-text` | 自定义帮助提示内容 |

### CSS Parts

| Part 名称 | 说明 |
|-----------|------|
| `input` | 输入框组件 |
| `popup` | 弹出面板 |
| `calendar` | 日历组件 |
| `calendar-base` | 日历基础容器 |
| `calendar-header` | 日历头部导航 |
| `calendar-nav-button` | 日历导航按钮 |
| `calendar-title` | 日历标题（年月） |
| `calendar-day` | 日期单元格 |
| `calendar-day-header` | 星期标题 |

---

## 代码示例

### 示例1：填充样式（filled）

使用 `filled` 属性为输入框应用填充背景样式。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => (
  <div style={{ display: "flex", flexDirection: "column", gap: "16px", width: "230px" }}>
    <SlDatepicker label="默认样式" placeholder="默认外观" />
    <SlDatepicker label="填充样式" filled placeholder="filled 外观" />
  </div>
);
```

---

### 示例2：药丸样式（pill）

使用 `pill` 属性为输入框应用圆角药丸样式。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => (
  <div style={{ display: "flex", flexDirection: "column", gap: "16px", width: "230px" }}>
    <SlDatepicker label="默认圆角" placeholder="默认样式" />
    <SlDatepicker label="药丸圆角" pill placeholder="pill 样式" />
    <SlDatepicker label="填充 + 药丸" filled pill placeholder="filled + pill 样式" />
  </div>
);
```

---

### 示例3：综合样式展示

组合使用多种样式属性。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

const css = `
  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
  }
`;

export default () => (
  <>
    <div className="grid">
      <SlDatepicker size="small" placeholder="Small" />
      <SlDatepicker size="small" filled placeholder="Small Filled" />
      <SlDatepicker size="small" pill placeholder="Small Pill" />
      <SlDatepicker size="medium" placeholder="Medium" />
      <SlDatepicker size="medium" filled placeholder="Medium Filled" />
      <SlDatepicker size="medium" pill placeholder="Medium Pill" />
      <SlDatepicker size="large" placeholder="Large" />
      <SlDatepicker size="large" filled placeholder="Large Filled" />
      <SlDatepicker size="large" pill placeholder="Large Pill" />
    </div>
    <style>{css}</style>
  </>
);
```

---

### 示例4：自定义前缀 Slot

通过 `prefix` slot 在输入框前方添加自定义内容。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';

export default () => (
  <SlDatepicker label="带前缀的日期选择" placeholder="请选择日期" style={{ width: "230px" }}>
    <SlIcon slot="prefix" name="calendar-event" />
  </SlDatepicker>
);
```

---

### 示例5：自定义标签 Slot

通过 `label` slot 自定义标签内容，支持富文本。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

const css = `
  .custom-label {
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .required-badge {
    display: inline-block;
    padding: 0 6px;
    font-size: 12px;
    line-height: 20px;
    background: #d32f2f;
    color: white;
    border-radius: 4px;
  }
`;

export default () => (
  <>
    <SlDatepicker placeholder="请选择日期" style={{ width: "230px" }}>
      <div slot="label" className="custom-label">
        <span>预约日期</span>
        <span className="required-badge">必填</span>
      </div>
    </SlDatepicker>
    <style>{css}</style>
  </>
);
```

---

### 示例6：通过 CSS Parts 自定义样式

使用 `::part()` 选择器深度自定义组件内部样式。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

const css = `
  .custom-datepicker::part(input) {
    --sl-input-border-color: #722ed1;
    --sl-input-border-color-focus: #531dab;
  }
  .custom-datepicker::part(calendar-day) {
    border-radius: 50%;
  }
  .custom-datepicker::part(calendar-title) {
    color: #722ed1;
    font-weight: bold;
  }
  .custom-datepicker::part(calendar-nav-button) {
    color: #722ed1;
  }
`;

export default () => (
  <>
    <SlDatepicker
      className="custom-datepicker"
      label="自定义样式"
      placeholder="深度定制外观"
      value="2024-06-15"
      style={{ width: "230px" }}
    />
    <style>{css}</style>
  </>
);
```

---

### 示例7：弹出层提升（hoist）

在模态框或滚动容器中使用时，设置 `hoist` 属性将弹出层提升到固定定位，避免被容器裁切。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

const css = `
  .scroll-container {
    height: 120px;
    overflow: auto;
    border: 1px solid #ccc;
    border-radius: 8px;
    margin-bottom: 16px;
    padding: 16px;
  }
  .content {
    min-height: 200px;
  }
`;

export default () => (
  <>
    <div className="scroll-container">
      <div className="content">
        <SlDatepicker label="普通定位" placeholder="可能被容器裁切" />
      </div>
    </div>
    <div className="scroll-container">
      <div className="content">
        <SlDatepicker label="提升定位（hoist）" hoist placeholder="弹出层不被裁切" />
      </div>
    </div>
    <style>{css}</style>
  </>
);
```

---

## 注意事项

1. **CSS Parts 作用范围**：`::part()` 选择器只能选中组件直接暴露的 part，不支持嵌套选择器
2. **Slot 覆盖默认内容**：使用 `suffix` slot 会覆盖默认的日历图标，如需保留请手动添加
3. **filled 和 pill 可组合**：`filled` 和 `pill` 可以同时使用，产生填充 + 圆角效果
4. **hoist 的使用场景**：仅在弹出层被容器 `overflow: hidden/auto/scroll` 裁切时才需要设置 `hoist`
5. **size 影响整体**：`size` 属性会同时影响输入框高度和字体大小

[返回目录](../index.md)
