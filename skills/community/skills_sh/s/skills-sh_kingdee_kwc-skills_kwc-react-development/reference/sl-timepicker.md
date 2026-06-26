# Timepicker 时间选择器

输入或选择时间的控件，支持时、分、秒的滚动选择。

## 特性概览

- **弹出面板**：点击输入框弹出时间滚动面板（时/分/秒三列），桌面端使用 Popup，移动端自动切换为 Drawer
- **手动输入**：支持在输入框中直接键入时间值（格式 `HH:mm:ss`），输入合法时实时同步面板
- **清除按钮**：默认启用清除按钮（`clearable` 默认为 `true`）
- **键盘操作**：支持 `Enter` 确认选择、`Escape` 关闭面板
- **表单集成**：实现标准表单控件接口，支持 `name`、`required`、`form` 等属性
- **响应式**：自动检测屏幕宽度，窄屏（< 500px）自动切换移动端交互模式
- **多种样式**：支持 `filled`（填充）、`pill`（胶囊）、`size`（尺寸）等外观配置

## 基础用法

最简单的时间选择器用法，点击输入框即可打开时间面板。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => <SlTimepicker style={{ width: "230px" }} />;
```

## 设置初始值

使用 `value` 属性设置初始时间值，格式为 `HH:mm:ss`。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} value="14:30:00" />
);
```

## 自定义格式（format）

通过 `format` 属性自定义时间的显示格式。格式化底层基于 [dayjs](https://day.js.org/docs/en/display/format) 实现，支持 dayjs 的时间格式化符号。`format` 仅影响输入框的显示文本，`value` 始终保持与 `format` 一致的格式。

### 支持的格式符号（dayjs）

| 符号 | 说明 | 示例 |
|------|------|------|
| `HH` | 24 小时制小时（补零） | `08`、`23` |
| `H` | 24 小时制小时（不补零） | `8`、`23` |
| `hh` | 12 小时制小时（补零） | `02`、`11` |
| `h` | 12 小时制小时（不补零） | `2`、`11` |
| `mm` | 分钟（补零） | `05`、`59` |
| `m` | 分钟（不补零） | `5`、`59` |
| `ss` | 秒（补零） | `00`、`59` |
| `s` | 秒（不补零） | `0`、`59` |
| `A` | 上午/下午（大写） | `AM`、`PM` |
| `a` | 上午/下午（小写） | `am`、`pm` |

### 常用格式示例

| 格式字符串 | 显示效果 | 说明 |
|-----------|---------|------|
| `HH:mm:ss` | `14:30:00` | 默认，24 小时制含秒 |
| `HH:mm` | `14:30` | 24 小时制不含秒 |
| `hh:mm:ss A` | `02:30:00 PM` | 12 小时制含秒 |
| `hh:mm A` | `02:30 PM` | 12 小时制不含秒 |
| `HH时mm分ss秒` | `14时30分00秒` | 中文格式 |
| `HH时mm分` | `14时30分` | 中文格式不含秒 |

### 仅显示时分（省略秒）

设置 `format="HH:mm"` 后，时间面板将只显示时和分两列，隐藏秒列。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} label="时分选择" format="HH:mm" placeholder="HH:mm" />
);
```

### 12 小时制

设置 `format="hh:mm:ss A"` 后，时间面板将以 12 小时制显示，并附带 AM/PM 选择。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} label="12 小时制" format="hh:mm:ss A" placeholder="hh:mm:ss AM/PM" />
);
```

### 12 小时制仅时分

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} label="12 小时制（时分）" format="hh:mm A" placeholder="hh:mm AM/PM" />
);
```

### 中文格式

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} label="中文时间格式" format="HH时mm分ss秒" placeholder="请选择时间" />
);
```

### 多种格式对比

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <div style={{ display: "flex", flexDirection: "column", gap: "16px", width: "230px" }}>
    <SlTimepicker label="默认 (HH:mm:ss)" value="14:30:00" />
    <SlTimepicker label="时分 (HH:mm)" format="HH:mm" value="14:30:00" />
    <SlTimepicker label="12 小时制 (hh:mm A)" format="hh:mm A" value="14:30:00" />
    <SlTimepicker label="中文 (HH时mm分)" format="HH时mm分" value="14:30:00" />
  </div>
);
```

## 标签

使用 `label` 属性为选择器提供标签。若标签内需包含 HTML，请改用 `label` 插槽。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} label="选择时间" />
);
```

## 帮助文本

使用 `help-text` 属性为选择器添加描述性帮助文本。若帮助文本内需包含 HTML，请改用 `help-text` 插槽。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker
    style={{ width: "230px" }}
    label="会议时间"
    help-text="请选择会议开始时间"
  />
);
```

## 占位符

使用 `placeholder` 属性添加占位文本。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} placeholder="HH:mm:ss" />
);
```

## 可清除

`clearable` 属性默认启用（`true`），当有值时会显示清除按钮。设置 `clearable` 为 `false` 可以隐藏清除按钮。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

const css = `
  .timepicker-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 230px;
  }
`;

export default () => (
  <>
    <div className="timepicker-group">
      <SlTimepicker value="09:30:00" placeholder="默认可清除" />
      <SlTimepicker value="09:30:00" placeholder="不可清除" clearable={false} />
    </div>
    <style>{css}</style>
  </>
);
```

## 填充样式

添加 `filled` 属性可绘制填充样式的选择器。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} placeholder="Filled" filled />
);
```

## 胶囊样式

使用 `pill` 属性可为选择器设置椭圆圆角样式。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} placeholder="Pill" pill />
);
```

## 尺寸

使用 `size` 属性更改时间选择器的尺寸，支持 `small`、`medium`（默认）、`large`。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

const css = `
  .timepicker-group {
    display: flex;
    flex-direction: column;
    gap: 20px;
    width: 230px;
  }
`;

export default () => (
  <>
    <div className="timepicker-group">
      <SlTimepicker placeholder="Small" size="small" />
      <SlTimepicker placeholder="Medium" size="medium" />
      <SlTimepicker placeholder="Large" size="large" />
    </div>
    <style>{css}</style>
  </>
);
```

## 禁用

使用 `disabled` 属性禁用选择器，禁用后无法打开面板、无法输入。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} value="10:00:00" disabled />
);
```

## 只读

使用 `readonly` 属性设置只读状态，可以看到值但不能修改。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} value="10:00:00" readonly />
);
```

## Hoist（提升定位）

当时间选择器位于溢出隐藏的容器中时，弹出面板可能被裁剪。添加 `hoist` 属性可使面板使用 `fixed` 定位策略脱离容器限制。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => (
  <div style={{ overflow: "hidden", border: "1px solid #ccc", padding: "16px", height: "80px" }}>
    <SlTimepicker placeholder="Hoisted" hoist />
  </div>
);
```

## 监听时间变化事件

`SlTimepicker` 的 React 包装器已映射 `sl-*` 事件，可直接在 JSX 中使用 `onSlChange`、`onSlInput` 等属性。

- `onSlChange`：用户**确认提交**值的修改时触发（点击面板"确定"按钮、按 Enter、失焦时）
- `onSlInput`：值**实时变化**时触发（用户在面板滚动选择时、在输入框中输入时）

```jsx
import React, { useState, useCallback } from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';
import type SlTimepickerElement from '@kdcloudjs/shoelace/dist/components/timepicker/timepicker.js';

export default () => {
  const [changeValue, setChangeValue] = useState("-");
  const [inputValue, setInputValue] = useState("-");

  const handleChange = useCallback((event: CustomEvent) => {
    const target = event.target as SlTimepickerElement;
    setChangeValue(target.value || "-");
    console.log("sl-change:", target.value);
  }, []);

  const handleInput = useCallback((event: CustomEvent) => {
    const target = event.target as SlTimepickerElement;
    setInputValue(target.value || "-");
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "280px" }}>
      <div style={{ padding: "8px", background: "#f5f5f5", borderRadius: "4px", fontSize: "14px" }}>
        <p style={{ margin: "4px 0" }}>当前值 (sl-change): {changeValue}</p>
        <p style={{ margin: "4px 0" }}>实时值 (sl-input): {inputValue}</p>
      </div>
      <SlTimepicker
        placeholder="选择时间"
        onSlChange={handleChange as any}
        onSlInput={handleInput as any}
      />
    </div>
  );
};
```

## 监听焦点与清除事件

```jsx
import React, { useState, useCallback } from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';

export default () => {
  const [logText, setLogText] = useState("无");

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "8px", width: "230px" }}>
      <p style={{ fontSize: "14px", color: "#666" }}>最近事件: {logText}</p>
      <SlTimepicker
        value="08:00:00"
        onSlFocus={() => setLogText("获得焦点 (sl-focus)")}
        onSlBlur={() => setLogText("失去焦点 (sl-blur)")}
        onSlClear={() => setLogText("已清除 (sl-clear)")}
      />
    </div>
  );
};
```

## 通过 JavaScript 动态设置值

通过 `ref` 动态读取和设置时间选择器的值。

```jsx
import React, { useRef } from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const timepickerRef = useRef(null);

  const handleMorning = () => {
    if (timepickerRef.current) {
      timepickerRef.current.value = "09:00:00";
    }
  };

  const handleNoon = () => {
    if (timepickerRef.current) {
      timepickerRef.current.value = "12:00:00";
    }
  };

  const handleClear = () => {
    if (timepickerRef.current) {
      timepickerRef.current.value = "";
    }
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "280px" }}>
      <div style={{ display: "flex", gap: "8px" }}>
        <SlButton size="small" onClick={handleMorning}>设为上午9点</SlButton>
        <SlButton size="small" onClick={handleNoon}>设为中午12点</SlButton>
        <SlButton size="small" onClick={handleClear}>清空</SlButton>
      </div>
      <SlTimepicker ref={timepickerRef} placeholder="选择时间" />
    </div>
  );
};
```

## 自定义校验

使用 `ref` 调用 `setCustomValidity()` 方法设置自定义校验消息，实现业务逻辑校验。

```jsx
import React, { useRef, useCallback } from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';
import type SlTimepickerElement from '@kdcloudjs/shoelace/dist/components/timepicker/timepicker.js';

export default () => {
  const timepickerRef = useRef<SlTimepickerElement>(null);

  const handleChange = useCallback(() => {
    // 值变化时清除之前的自定义校验
    if (timepickerRef.current) {
      timepickerRef.current.setCustomValidity("");
    }
  }, []);

  const handleValidate = useCallback(() => {
    const picker = timepickerRef.current;
    if (!picker) return;

    const val = picker.value;
    if (!val) {
      picker.setCustomValidity("请选择一个时间");
    } else if (val < "09:00:00" || val > "18:00:00") {
      picker.setCustomValidity("时间必须在 09:00 到 18:00 之间");
    } else {
      picker.setCustomValidity("");
    }
    picker.reportValidity();
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "280px" }}>
      <SlTimepicker
        ref={timepickerRef}
        label="工作时间"
        help-text="仅允许选择 09:00 - 18:00 之间的时间"
        onSlChange={handleChange as any}
      />
      <SlButton variant="primary" size="small" onClick={handleValidate}>校验</SlButton>
    </div>
  );
};
```

## 多个时间选择器组合（时间范围）

组合两个时间选择器实现起止时间选择。

```jsx
import React, { useRef, useCallback } from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';
import type SlTimepickerElement from '@kdcloudjs/shoelace/dist/components/timepicker/timepicker.js';

export default () => {
  const startRef = useRef<SlTimepickerElement>(null);
  const endRef = useRef<SlTimepickerElement>(null);

  const validateRange = useCallback(() => {
    const startPicker = startRef.current;
    const endPicker = endRef.current;
    if (!startPicker || !endPicker) return;

    const startVal = startPicker.value;
    const endVal = endPicker.value;

    if (startVal && endVal && endVal <= startVal) {
      endPicker.setCustomValidity("结束时间必须晚于开始时间");
      endPicker.reportValidity();
    } else {
      endPicker.setCustomValidity("");
    }
  }, []);

  return (
    <div style={{ display: "flex", alignItems: "flex-end", gap: "8px" }}>
      <SlTimepicker
        ref={startRef}
        label="开始时间"
        placeholder="开始"
        onSlChange={validateRange as any}
      />
      <span style={{ lineHeight: "40px", color: "#999" }}>~</span>
      <SlTimepicker
        ref={endRef}
        label="结束时间"
        placeholder="结束"
        onSlChange={validateRange as any}
      />
    </div>
  );
};
```

## 使用插槽自定义前缀

通过 `prefix` 和 `suffix` 插槽自定义输入框的前缀和后缀内容。

```jsx
import React from "react";
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';
import SlIcon from '@kdcloudjs/shoelace/dist/react/icon/index.js';

export default () => (
  <SlTimepicker style={{ width: "230px" }} placeholder="选择时间">
    <SlIcon slot="prefix" name="alarm" />
  </SlTimepicker>
);
```

## Properties

| 属性          | 描述                                                         | 类型                              | 默认值       |
| ------------- | ------------------------------------------------------------ | --------------------------------- | ------------ |
| value         | 时间选择器的当前值，格式由 `format` 决定，默认 `HH:mm:ss`。 | `string`                          | `''`         |
| format        | 时间格式字符串（基于 dayjs）。                               | `string`                          | `'HH:mm:ss'` |
| name          | 表单名称，随表单数据以"名称/值"对的形式提交。                | `string`                          | `''`         |
| placeholder   | 为空时的占位提示文本。                                       | `string`                          | `''`         |
| label         | 标签文本。                                                   | `string`                          | `''`         |
| help-text     | 辅助说明文本。                                               | `string`                          | `''`         |
| size          | 时间选择器的尺寸。                                           | `'small' \| 'medium' \| 'large'`  | `'medium'`   |
| filled        | 是否使用填充样式。                                           | `boolean`                         | `false`      |
| pill          | 是否为圆角胶囊样式。                                         | `boolean`                         | `false`      |
| clearable     | 是否显示清除按钮（当有值时）。                               | `boolean`                         | `true`       |
| disabled      | 是否禁用输入。                                               | `boolean`                         | `false`      |
| readonly      | 是否为只读状态。                                             | `boolean`                         | `false`      |
| required      | 是否为必填项。                                               | `boolean`                         | `false`      |
| hoist         | 是否使用 `fixed` 定位策略提升弹出面板，避免被溢出容器裁剪。  | `boolean`                         | `false`      |
| form          | 关联的表单 ID。                                              | `string`                          | `''`         |
| autofocus     | 是否自动获取焦点。                                           | `boolean`                         | `false`      |

## Slots

| 名称       | 描述                                            |
| ---------- | ----------------------------------------------- |
| label      | 时间选择器的标签。也可以使用 `label` 属性。     |
| prefix     | 在输入框前部添加图标或元素。                    |
| suffix     | 在输入框后部添加图标或元素（默认显示时钟图标）。|
| clear-icon | 自定义清除按钮的图标。                          |
| help-text  | 辅助说明文字。也可以使用 `help-text` 属性。     |

## Events

`SlTimepicker` 的 React 包装器已映射以下事件为 JSX 属性，可以直接在 JSX 中使用。

| 事件名称   | React 属性  | 描述                                                                               |
| ---------- | ----------- | ---------------------------------------------------------------------------------- |
| sl-change  | onSlChange  | 当用户确认值的修改时触发（点击"确定"按钮、按 Enter 键、输入框失焦时）。            |
| sl-input   | onSlInput   | 当值实时变化时触发（用户在面板中滚动选择时、在输入框中输入合法时间时）。            |
| sl-focus   | onSlFocus   | 当控件获得焦点时触发。                                                             |
| sl-blur    | onSlBlur    | 当控件失去焦点时触发。                                                             |
| sl-clear   | onSlClear   | 当清除按钮被激活时触发。                                                           |

### 事件使用示例

```jsx
import SlTimepicker from '@kdcloudjs/shoelace/dist/react/timepicker/index.js';
import type SlTimepickerElement from '@kdcloudjs/shoelace/dist/components/timepicker/timepicker.js';

// 在 JSX 中直接使用 onSl* 属性
<SlTimepicker
  onSlChange={(event: CustomEvent) => {
    const target = event.target as SlTimepickerElement;
    console.log('确认选择的时间:', target.value);
  }}
  onSlInput={(event: CustomEvent) => {
    const target = event.target as SlTimepickerElement;
    console.log('实时变化的时间:', target.value);
  }}
/>
```

## Methods

| 方法                | 描述                                     | 参数                  |
| ------------------- | ---------------------------------------- | --------------------- |
| focus()             | 使时间选择器获得焦点并打开面板。         | options: FocusOptions |
| blur()              | 使时间选择器失去焦点并关闭面板。         | -                     |
| checkValidity()     | 检查有效性但不显示消息。                 | -                     |
| getForm()           | 获取关联的表单元素。                     | -                     |
| reportValidity()    | 检查有效性并在无效时显示浏览器原生消息。 | -                     |
| setCustomValidity() | 设置自定义校验消息。传空字符串清除校验。 | message: string       |

## Parts

| 名称                        | 描述                         |
| --------------------------- | ---------------------------- |
| input                       | 内部输入框元素。             |
| popup                       | 弹出面板容器（桌面端）。     |
| panel                       | 时间面板。                   |
| time-panel-base             | 时间面板基础容器。           |
| time-panel-header           | 时间面板头部（显示当前时间）。|
| time-panel-columns          | 时间面板滚动列容器。         |
| time-panel-column           | 时间面板单列（时/分/秒）。   |
| time-panel-hour             | 小时列。                     |
| time-panel-minute           | 分钟列。                     |
| time-panel-second           | 秒列。                       |
| time-panel-item             | 时间面板中的单个时间项。     |
| time-panel-footer           | 时间面板底部（确定按钮）。   |

## 交互行为说明

### 桌面端
- **打开面板**：点击输入框或尾部时钟图标打开时间面板
- **滚动选择**：面板包含时/分/秒三列，鼠标悬停列可滚动，点击项即选中
- **确认选择**：点击面板底部"确定"按钮或按 `Enter` 键确认选择并关闭面板
- **取消选择**：按 `Escape` 键或点击面板外部区域关闭面板，值回退到上次有效值
- **手动输入**：在输入框中直接键入 `HH:mm:ss` 格式时间，输入合法时实时同步面板

### 移动端（屏幕宽度 < 500px）
- 自动切换为 Drawer 抽屉模式
- 输入框变为只读，点击后弹出抽屉面板
- 抽屉面板包含"确定"、"取消"、"清除"操作按钮

### 值格式说明

时间值必须为 `HH:mm:ss` 格式字符串（24 小时制，两位补零）：

```jsx
// 正确
picker.value = '09:05:00';
picker.value = '23:59:59';
picker.value = '';  // 清空

// 错误
picker.value = '9:5:0';     // 不补零
picker.value = '09:05';     // 缺少秒
picker.value = '2:30 PM';   // 12 小时制
```

## 常见问题

### Q: 为什么设置 value 后面板没有滚动到对应时间？

A: 确保 `value` 格式为 `HH:mm:ss`（如 `"09:30:00"`）。非法格式的值会被组件忽略并清空。面板打开时会自动滚动到当前选中时间。

### Q: sl-change 和 sl-input 有什么区别？

A: `sl-input` 在用户每次滚动面板选择或输入合法时间时即触发（实时变化），适合做预览、联动等；`sl-change` 仅在用户确认提交值时触发（点击确定、按 Enter、失焦），适合做最终的数据保存和业务逻辑处理。

### Q: 弹出面板被父容器遮挡怎么办？

A: 添加 `hoist` 属性，使面板使用 `fixed` 定位策略：`<SlTimepicker hoist />`。

### Q: 如何通过 JavaScript 读取当前选中时间？

A: 使用 `ref` 直接访问 `value` 属性即可：
```jsx
const timepickerRef = useRef(null);
const currentTime = timepickerRef.current?.value; // 例如 "14:30:00" 或 ""
```
