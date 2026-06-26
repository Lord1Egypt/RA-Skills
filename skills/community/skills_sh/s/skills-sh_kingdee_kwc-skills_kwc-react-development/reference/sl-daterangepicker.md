# Daterangepicker 日期范围选择器

选择一个日期或日期时间范围的控件，支持双日历面板联动、手动输入、范围校验。

## 特性概览

- **双日历面板**：`type="date"` 模式下左右两个日历面板联动，分别显示相邻月份
- **日期时间模式**：`type="datetime"` 模式下显示单日历 + 时间滚动面板，选择后需点击"确定"提交
- **手动输入**：支持在输入框中直接键入日期值（格式 `YYYY-MM-DD` 或 `YYYY-MM-DD HH:mm:ss`），输入合法时实时同步面板
- **范围校验**：自动校验起止日期顺序，非法输入自动回退到上次有效值
- **清除按钮**：默认启用清除按钮（`clearable` 默认为 `true`）
- **键盘操作**：支持 `Enter` 确认选择、`Escape` 关闭面板并回退值
- **表单集成**：实现标准表单控件接口，支持 `name`、`required` 等属性，表单提交时拆分为 `${name}-start` 和 `${name}-end`
- **多种样式**：支持 `filled`（填充）、`pill`（胶囊）、`size`（尺寸）等外观配置
- **min/max 限制**：通过 `min` 和 `max` 属性限制可选日期范围

## 基础用法

最简单的日期范围选择器用法，点击输入框即可打开双日历面板。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => <SlDaterangepicker style={{ width: '400px' }} />;
```

## 设置初始值

使用 `value` 属性设置初始日期范围，React 中传入 `[Date | null, Date | null]` 元组。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => <SlDaterangepicker style={{ width: '400px' }} value={[new Date(2025, 0, 1), new Date(2025, 5, 30)]} />;
```

## 标签

使用 `label` 属性为选择器提供标签。若标签内需包含 HTML，请改用 `label` 插槽。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => <SlDaterangepicker style={{ width: '400px' }} label="选择日期范围" />;
```

## 帮助文本

使用 `help-text` 属性为选择器添加描述性帮助文本。若帮助文本内需包含 HTML，请改用 `help-text` 插槽。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => <SlDaterangepicker style={{ width: '400px' }} label="入住退房" help-text="请选择入住和退房日期" />;
```

## 占位符

使用 `placeholder` 属性设置两个输入框的占位文本，React 中传入 `[string, string]` 数组。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => <SlDaterangepicker style={{ width: '400px' }} placeholder={['Check-in', 'Check-out']} />;
```

## 可清除

`clearable` 属性默认启用（`true`），当有值时会显示清除按钮。设置 `clearable` 为 `false` 可以隐藏清除按钮。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

const css = `
  .daterange-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 400px;
  }
`;

export default () => (
  <>
    <div className="daterange-group">
      <SlDaterangepicker value={[new Date(2025, 0, 1), new Date(2025, 5, 30)]} label="默认可清除" />
      <SlDaterangepicker value={[new Date(2025, 0, 1), new Date(2025, 5, 30)]} label="不可清除" clearable={false} />
    </div>
    <style>{css}</style>
  </>
);
```

## 日期时间模式

使用 `type="datetime"` 启用日期时间选择模式。此模式下显示单个日历面板并附带时间滚动选择面板（时/分/秒三列），选择日期后面板不自动关闭，需点击"确定"按钮提交。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => <SlDaterangepicker style={{ width: '500px' }} label="日期时间范围" type="datetime" />;
```

## 自定义格式（format）

通过 `format` 属性自定义日期在输入框中的显示格式。格式化底层基于 [dayjs](https://day.js.org/docs/en/display/format) 实现，支持 dayjs 的所有格式化符号。`format` 仅影响输入框的显示文本，`value`（`[Date | null, Date | null]`）不受影响。

### 支持的格式符号（dayjs）

| 符号 | 说明 | 示例 |
|------|------|------|
| `YYYY` | 四位年份 | `2024` |
| `YY` | 两位年份 | `24` |
| `MM` | 两位月份（补零） | `01`、`12` |
| `M` | 月份（不补零） | `1`、`12` |
| `DD` | 两位日期（补零） | `05`、`31` |
| `D` | 日期（不补零） | `5`、`31` |
| `HH` | 24 小时制小时（补零） | `08`、`23` |
| `hh` | 12 小时制小时（补零） | `02`、`11` |
| `mm` | 分钟（补零） | `05`、`59` |
| `ss` | 秒（补零） | `00`、`59` |
| `A` | 上午/下午（大写） | `AM`、`PM` |

### 常用格式示例

| 格式字符串 | 显示效果 | 说明 |
|-----------|---------|------|
| `YYYY-MM-DD` | `2025-01-01` | 默认格式 |
| `YYYY/MM/DD` | `2025/01/01` | 斜杠分隔 |
| `DD.MM.YYYY` | `01.01.2025` | 欧洲风格 |
| `YYYY年MM月DD日` | `2025年01月01日` | 中文格式 |
| `YYYY-MM-DD HH:mm:ss` | `2025-01-01 08:00:00` | datetime 默认 |
| `YYYY/MM/DD HH:mm` | `2025/01/01 08:00` | datetime 省略秒 |

### 斜杠分隔格式

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => <SlDaterangepicker style={{ width: '400px' }} label="斜杠格式" format="YYYY/MM/DD" />;
```

### 中文日期格式

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => <SlDaterangepicker style={{ width: '460px' }} label="中文格式" format="YYYY年MM月DD日" />;
```

### datetime 模式自定义格式

在 `type="datetime"` 模式下，`format` 应包含时间部分。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => (
  <SlDaterangepicker style={{ width: '500px' }} label="自定义 datetime 格式" type="datetime" format="YYYY/MM/DD HH:mm" />
);
```

### 多种格式对比

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => (
  <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
    <SlDaterangepicker style={{ width: '400px' }} label="默认 (YYYY-MM-DD)" value={[new Date(2025, 0, 1), new Date(2025, 5, 30)]} />
    <SlDaterangepicker style={{ width: '400px' }} label="斜杠 (YYYY/MM/DD)" format="YYYY/MM/DD" value={[new Date(2025, 0, 1), new Date(2025, 5, 30)]} />
    <SlDaterangepicker style={{ width: '460px' }} label="中文 (YYYY年MM月DD日)" format="YYYY年MM月DD日" value={[new Date(2025, 0, 1), new Date(2025, 5, 30)]} />
    <SlDaterangepicker style={{ width: '400px' }} label="欧洲 (DD.MM.YYYY)" format="DD.MM.YYYY" value={[new Date(2025, 0, 1), new Date(2025, 5, 30)]} />
  </div>
);
```

## 填充样式

添加 `filled` 属性可绘制填充样式的选择器。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => <SlDaterangepicker style={{ width: '400px' }} label="填充样式" filled />;
```

## 胶囊样式

使用 `pill` 属性可为选择器设置椭圆圆角样式。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => <SlDaterangepicker style={{ width: '400px' }} label="胶囊样式" pill />;
```

## 尺寸

使用 `size` 属性更改选择器的尺寸，支持 `small`、`medium`（默认）、`large`。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

const css = `
  .daterange-group {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 400px;
  }
`;

export default () => (
  <>
    <div className="daterange-group">
      <SlDaterangepicker label="Small" size="small" />
      <SlDaterangepicker label="Medium" size="medium" />
      <SlDaterangepicker label="Large" size="large" />
    </div>
    <style>{css}</style>
  </>
);
```

## 禁用

使用 `disabled` 属性禁用选择器，禁用后无法打开面板、无法输入。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => (
  <SlDaterangepicker style={{ width: '400px' }} value={[new Date(2025, 0, 1), new Date(2025, 5, 30)]} disabled />
);
```

## 只读

使用 `readonly` 属性设置只读状态，可以看到值但不能修改，面板不会弹出。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => (
  <SlDaterangepicker style={{ width: '400px' }} value={[new Date(2025, 0, 1), new Date(2025, 5, 30)]} readonly />
);
```

## 最值范围

使用 `min` 和 `max` 属性限制可选日期范围，超出范围的日期将被禁用。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => <SlDaterangepicker style={{ width: '400px' }} label="限制范围" min="2025-01-01" max="2025-12-31" />;
```

## 监听日期变化事件

`SlDaterangepicker` 的 React 包装器已映射 `sl-*` 事件，可直接在 JSX 中使用 `onSlChange`、`onSlInput` 等属性。

- `onSlChange`：用户**确认提交**值的修改时触发（选择完成关闭面板、清除值时）
- `onSlInput`：值**实时变化**时触发（用户在面板中点选日期时、在输入框中输入时）

```jsx
import React, { useState, useCallback } from "react";
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';
import type SlDaterangepickerElement from '@kdcloudjs/shoelace/dist/components/daterangepicker/daterangepicker.js';

export default () => {
  const [changeValue, setChangeValue] = useState("-");
  const [inputValue, setInputValue] = useState("-");

  const formatRange = (value: [Date | null, Date | null]) => {
    const [start, end] = value;
    if (start && end) {
      return `${start.toLocaleDateString()} ~ ${end.toLocaleDateString()}`;
    }
    return "-";
  };

  const handleChange = useCallback((event: CustomEvent) => {
    const target = event.target as SlDaterangepickerElement;
    setChangeValue(formatRange(target.value));
    console.log("sl-change:", target.value);
  }, []);

  const handleInput = useCallback((event: CustomEvent) => {
    const target = event.target as SlDaterangepickerElement;
    setInputValue(formatRange(target.value));
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "400px" }}>
      <div style={{ padding: "8px", background: "#f5f5f5", borderRadius: "4px", fontSize: "14px" }}>
        <p style={{ margin: "4px 0" }}>当前值 (sl-change): {changeValue}</p>
        <p style={{ margin: "4px 0" }}>实时值 (sl-input): {inputValue}</p>
      </div>
      <SlDaterangepicker
        label="选择日期范围"
        onSlChange={handleChange as any}
        onSlInput={handleInput as any}
      />
    </div>
  );
};
```

## 监听焦点与清除事件

```jsx
import React, { useState } from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';

export default () => {
  const [logText, setLogText] = useState('无');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', width: '400px' }}>
      <p style={{ fontSize: '14px', color: '#666' }}>最近事件: {logText}</p>
      <SlDaterangepicker
        value={[new Date(2025, 0, 1), new Date(2025, 5, 30)]}
        onSlFocus={() => setLogText('获得焦点 (sl-focus)')}
        onSlBlur={() => setLogText('失去焦点 (sl-blur)')}
        onSlClear={() => setLogText('已清除 (sl-clear)')}
      />
    </div>
  );
};
```

## 通过 JavaScript 动态设置值

通过 `ref` 动态读取和设置日期范围选择器的值。`value` 属性为 `[Date | null, Date | null]` 元组。

```jsx
import React, { useRef } from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const daterangeRef = useRef(null);

  const handleThisMonth = () => {
    if (daterangeRef.current) {
      const now = new Date();
      const start = new Date(now.getFullYear(), now.getMonth(), 1);
      const end = new Date(now.getFullYear(), now.getMonth() + 1, 0);
      daterangeRef.current.value = [start, end];
    }
  };

  const handleThisQuarter = () => {
    if (daterangeRef.current) {
      const now = new Date();
      const quarterStart = Math.floor(now.getMonth() / 3) * 3;
      const start = new Date(now.getFullYear(), quarterStart, 1);
      const end = new Date(now.getFullYear(), quarterStart + 3, 0);
      daterangeRef.current.value = [start, end];
    }
  };

  const handleClear = () => {
    if (daterangeRef.current) {
      daterangeRef.current.value = [null, null];
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', width: '400px' }}>
      <div style={{ display: 'flex', gap: '8px' }}>
        <SlButton size="small" onClick={handleThisMonth}>
          本月
        </SlButton>
        <SlButton size="small" onClick={handleThisQuarter}>
          本季度
        </SlButton>
        <SlButton size="small" onClick={handleClear}>
          清空
        </SlButton>
      </div>
      <SlDaterangepicker ref={daterangeRef} label="日期范围" />
    </div>
  );
};
```

## 自定义校验

使用 `ref` 调用 `setCustomValidity()` 方法设置自定义校验消息，实现业务逻辑校验。

```jsx
import React, { useRef, useCallback } from "react";
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';
import type SlDaterangepickerElement from '@kdcloudjs/shoelace/dist/components/daterangepicker/daterangepicker.js';

export default () => {
  const daterangeRef = useRef<SlDaterangepickerElement>(null);

  const handleChange = useCallback(() => {
    if (daterangeRef.current) {
      daterangeRef.current.setCustomValidity("");
    }
  }, []);

  const handleValidate = useCallback(() => {
    const picker = daterangeRef.current;
    if (!picker) return;

    const [start, end] = picker.value;
    if (!start || !end) {
      picker.setCustomValidity("请选择完整的日期范围");
    } else {
      const diffDays = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
      if (diffDays > 30) {
        picker.setCustomValidity("日期范围不能超过 30 天");
      } else {
        picker.setCustomValidity("");
      }
    }
    picker.reportValidity();
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "400px" }}>
      <SlDaterangepicker
        ref={daterangeRef}
        label="项目周期"
        help-text="范围不能超过 30 天"
        onSlChange={handleChange as any}
      />
      <SlButton variant="primary" size="small" onClick={handleValidate}>校验</SlButton>
    </div>
  );
};
```

## 使用插槽自定义后缀图标

通过 `suffix` 插槽自定义输入框的后缀内容，默认显示日历图标。

```jsx
import React from 'react';
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';

export default () => (
  <SlDaterangepicker style={{ width: '400px' }} label="自定义后缀">
    <SlIcon slot="suffix" name="calendar-event" />
  </SlDaterangepicker>
);
```

## Properties

| 属性        | 描述                                                                                                       | 类型                             | 默认值                     |
| ----------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------- | -------------------------- |
| value       | 当前值。HTML attribute 格式为 `YYYY-MM-DD ~ YYYY-MM-DD`；通过 JS 设置时为 `[Date \| null, Date \| null]`。 | `[Date \| null, Date \| null]`   | `[null, null]`             |
| type        | 选择器类型。`date` 为纯日期，`datetime` 为日期+时间。                                                      | `'date' \| 'datetime'`           | `'date'`                   |
| name        | 表单名称，实际提交为 `${name}-start` 和 `${name}-end` 两项。                                               | `string`                         | `''`                       |
| placeholder | 两个输入框的占位符。HTML attribute 格式为 `开始,结束`；通过 JS 设置时为 `[string, string]`。               | `[string, string]`               | `['开始日期', '结束日期']` |
| label       | 标签文本。                                                                                                 | `string`                         | `''`                       |
| help-text   | 辅助说明文本。                                                                                             | `string`                         | `''`                       |
| size        | 选择器的尺寸。                                                                                             | `'small' \| 'medium' \| 'large'` | `'medium'`                 |
| filled      | 是否使用填充样式。                                                                                         | `boolean`                        | `false`                    |
| pill        | 是否为圆角胶囊样式。                                                                                       | `boolean`                        | `false`                    |
| clearable   | 是否显示清除按钮（当有值时）。                                                                             | `boolean`                        | `true`                     |
| disabled    | 是否禁用输入。                                                                                             | `boolean`                        | `false`                    |
| readonly    | 是否为只读状态（只读时不弹出面板）。                                                                       | `boolean`                        | `false`                    |
| required    | 是否为必填项。                                                                                             | `boolean`                        | `false`                    |
| min         | 最小允许日期（YYYY-MM-DD 格式）。                                                                          | `string`                         | `'0001-01-01'`             |
| max         | 最大允许日期（YYYY-MM-DD 格式）。                                                                          | `string`                         | `'9999-12-31'`             |
| format      | 日期格式字符串（基于 dayjs）。                                                                             | `string`                         | `'YYYY-MM-DD'`             |
| startDate   | 开始日期（仅通过 JS 设置/读取）。                                                                          | `Date \| null`                   | `null`                     |
| endDate     | 结束日期（仅通过 JS 设置/读取）。                                                                          | `Date \| null`                   | `null`                     |

## Slots

| 名称      | 描述                                        |
| --------- | ------------------------------------------- |
| label     | 输入框的标签。也可以使用 `label` 属性。     |
| help-text | 辅助说明文字。也可以使用 `help-text` 属性。 |
| suffix    | 后缀图标区域（默认显示日历图标）。          |

## Events

`SlDaterangepicker` 的 React 包装器已映射以下事件为 JSX 属性，可以直接在 JSX 中使用。

| 事件名称   | React 属性  | 描述                                                             |
| ---------- | ----------- | ---------------------------------------------------------------- |
| sl-change  | onSlChange  | 当用户确认值的修改时触发（选择完成关闭面板、清除值时）。         |
| sl-input   | onSlInput   | 当值实时变化时触发（用户在面板中点选日期时、在输入框中输入时）。 |
| sl-focus   | onSlFocus   | 当控件获得焦点时触发。                                           |
| sl-blur    | onSlBlur    | 当控件失去焦点时触发。                                           |
| sl-clear   | onSlClear   | 当清除按钮被激活时触发。                                         |
| sl-invalid | onSlInvalid | 当表单控件校验失败时触发。                                       |

### 事件使用示例

```jsx
import SlDaterangepicker from '@kdcloudjs/shoelace/dist/react/daterangepicker/index.js';
import type SlDaterangepickerElement from '@kdcloudjs/shoelace/dist/components/daterangepicker/daterangepicker.js';

// 在 JSX 中直接使用 onSl* 属性
<SlDaterangepicker
  onSlChange={(event: CustomEvent) => {
    const target = event.target as SlDaterangepickerElement;
    const [start, end] = target.value;
    console.log('确认选择的范围:', start, '~', end);
  }}
  onSlInput={(event: CustomEvent) => {
    const target = event.target as SlDaterangepickerElement;
    const [start, end] = target.value;
    console.log('实时变化的范围:', start, '~', end);
  }}
/>
```

## Methods

| 方法                | 描述                                     | 参数            |
| ------------------- | ---------------------------------------- | --------------- |
| checkValidity()     | 检查有效性但不显示消息。                 | -               |
| getForm()           | 获取关联的表单元素。                     | -               |
| reportValidity()    | 检查有效性并在无效时显示浏览器原生消息。 | -               |
| setCustomValidity() | 设置自定义校验消息。传空字符串清除校验。 | message: string |

## Parts

| 名称                   | 描述                                       |
| ---------------------- | ------------------------------------------ |
| form-control           | 包裹标签、输入框和帮助文本的表单控件容器。 |
| form-control-label     | 标签的包装器。                             |
| form-control-input     | 输入框的包装器。                           |
| form-control-help-text | 帮助文本的包装器。                         |
| base                   | 组件的基础包装器。                         |
| start-input            | 内部的开始日期 `<input>`。                 |
| end-input              | 内部的结束日期 `<input>`。                 |
| separator              | 两个输入框之间的分隔符 `~`。               |
| suffix                 | 包裹后缀图标的容器。                       |
| clear-button           | 清除按钮。                                 |
| popup                  | 包裹日历面板的弹层。                       |
| calendars              | 包裹日历面板的容器。                       |
| calendar-base          | 日历组件的基础包装器。                     |
| calendar-header        | 日历的头部区域。                           |
| calendar-nav-button    | 日历的导航按钮。                           |
| calendar-title         | 日历的标题。                               |
| calendar-title-year    | 日历标题中的年份部分。                     |
| calendar-title-month   | 日历标题中的月份部分。                     |
| calendar-body          | 日历的主体区域。                           |
| calendar-date-panel    | 日历的日期面板。                           |
| calendar-day-header    | 日历的星期标题。                           |
| calendar-day           | 日历中的日期单元格。                       |
| calendar-day-footer    | 日历日期面板的底部区域。                   |
| calendar-month-grid    | 月份选择网格。                             |
| calendar-month-item    | 月份选择项。                               |
| calendar-year-grid     | 年份选择网格。                             |
| calendar-year-item     | 年份选择项。                               |
| calendar-time-footer   | 日历时间选择的底部区域。                   |
| calendar-time-base     | 时间面板基础容器。                         |
| calendar-time-header   | 时间面板头部（显示当前时间）。             |
| calendar-time-columns  | 时间面板滚动列容器。                       |
| calendar-time-column   | 时间面板单列（时/分/秒）。                 |
| calendar-time-item     | 时间面板中的单个时间项。                   |

## 交互行为说明

### 桌面端

- **打开面板**：点击输入框或后缀日历图标打开日历面板（Popup 定位于输入框下方）
- **双日历联动**：`type="date"` 模式下显示左右两个日历面板，分别显示相邻月份，翻页时自动保持左 < 右的约束
- **选择流程**：点击开始日期 → 自动跳到结束日期输入框 → 点击结束日期 → 面板关闭并提交值
- **两步编辑**：当已有完整区间时重新打开面板，进入两步编辑模式，允许用户重新定义起点或终点
- **范围预览**：鼠标悬停日期时，实时预览选中范围的高亮效果
- **手动输入**：在输入框中直接键入 `YYYY-MM-DD` 格式日期，输入合法时实时同步面板
- **确认/取消**：按 `Enter` 确认当前输入，按 `Escape` 关闭面板并回退到上次有效值
- **面板外点击**：点击面板和输入框以外的区域自动关闭面板

### datetime 模式

- 显示单个日历面板 + 时间滚动面板（时/分/秒三列）
- 选择日期后面板不自动关闭，需点击"确定"按钮提交
- 输入框格式为 `YYYY-MM-DD HH:mm:ss`
- 焦点在开始/结束输入框之间切换时，日历面板同步切换显示对应日期

### 值格式说明

React 中 `value` 使用 `[Date | null, Date | null]` 元组，HTML attribute 使用 `~` 分隔的字符串格式：

```jsx
// React JSX 设置（推荐）
<SlDaterangepicker value={[new Date(2025, 0, 1), new Date(2025, 5, 30)]} />
<SlDaterangepicker value={[null, null]} />  // 清空

// 通过 ref 设置
const daterangeRef = useRef(null);
daterangeRef.current.value = [new Date(2025, 0, 1), new Date(2025, 5, 30)];
daterangeRef.current.value = [null, null]; // 清空

// 读取值
const [start, end] = daterangeRef.current.value;
// start: Date | null, end: Date | null

// 也可以通过便捷属性读取
const startDate = daterangeRef.current.startDate; // Date | null
const endDate = daterangeRef.current.endDate;     // Date | null
```

### datetime 模式值格式

```jsx
// React JSX 设置
<SlDaterangepicker type="datetime" value={[new Date(2025, 0, 1, 8, 0, 0), new Date(2025, 5, 30, 18, 0, 0)]} />;

// 通过 ref 设置
const start = new Date(2025, 0, 1, 8, 0, 0);
const end = new Date(2025, 5, 30, 18, 0, 0);
daterangeRef.current.value = [start, end];
```

### 值校验

- `type="date"` 要求值匹配 `YYYY-MM-DD` 格式（支持 `-`、`.`、`/` 分隔符）
- `type="datetime"` 要求值匹配 `YYYY-MM-DD HH:mm:ss` 格式
- 非法输入不会更新 `value`，失焦或关闭面板时自动回退到上次有效值
- 起始日期不能晚于结束日期，否则自动清空另一端并引导重新选择
- `[null, null]` 视为合法值（清空状态）

### 日期禁用规则

1. 超出 `min`/`max` 范围的日期始终禁用
2. 已有完整区间且刚打开面板（未切换焦点）时，不禁用任何日期，允许自由重选
3. 选择开始日期时，晚于已选结束日期的日期被禁用
4. 选择结束日期时，早于已选开始日期的日期被禁用

## 常见问题

### Q: 为什么设置 value 后面板没有显示对应月份？

A: 确保 `value` 格式正确。HTML attribute 格式为 `YYYY-MM-DD ~ YYYY-MM-DD`（注意 `~` 两侧有空格）。通过 JavaScript 设置时传入 `[Date, Date]` 数组。非法格式的值会被组件忽略并清空。

### Q: sl-change 和 sl-input 有什么区别？

A: `sl-input` 在用户每次点选日期或输入合法日期时即触发（实时变化），适合做预览、联动等；`sl-change` 仅在用户确认提交值时触发（选择完成关闭面板、清除值），适合做最终的数据保存和业务逻辑处理。

### Q: 如何限制可选日期范围？

A: 使用 `min` 和 `max` 属性：`<SlDaterangepicker min="2025-01-01" max="2025-12-31" />`。超出范围的日期会被自动禁用。

### Q: 如何通过 JavaScript 读取当前选中的日期范围？

A: 使用 `ref` 直接访问 `value` 属性即可：

```jsx
const daterangeRef = useRef(null);
const [start, end] = daterangeRef.current?.value ?? [null, null];
// start: Date | null, end: Date | null

// 或使用便捷属性
const startDate = daterangeRef.current?.startDate;
const endDate = daterangeRef.current?.endDate;
```

### Q: datetime 模式下为什么选择日期后面板没有关闭？

A: 这是预期行为。`datetime` 模式下选择日期后需要继续选择时间，点击面板中的"确定"按钮才会提交选择并关闭面板（或跳转到下一个输入框）。

### Q: 弹出面板被父容器遮挡怎么办？

A: 组件默认使用 `fixed` 定位策略，面板会脱离容器限制。如果仍有问题，请检查父容器的 `z-index` 设置。
