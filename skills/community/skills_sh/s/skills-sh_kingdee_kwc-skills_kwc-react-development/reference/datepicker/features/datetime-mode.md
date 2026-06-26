# 日期时间模式

[返回目录](../index.md)

## 功能说明

通过设置 `type="datetime"`，Datepicker 组件切换为日期时间选择模式，允许用户同时选择日期和时间（时、分、秒）。在桌面端，日历面板右侧会显示时间选择面板，并需要点击"确定"按钮确认选择；在移动端，时间选择通过底部滚轮面板进行。

## API 属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `type` | 选择器类型 | `'date' \| 'datetime'` | `'date'` |

### 类型对比

| 特性 | `date` 模式 | `datetime` 模式 |
|------|-------------|-----------------|
| 值格式 | `yyyy-MM-dd` | `yyyy-MM-dd HH:mm:ss` |
| 时间面板 | 无 | 有（时/分/秒） |
| 确认按钮 | 无（选择日期即确认） | 有（需点击确定） |
| 输入验证格式 | `yyyy-MM-dd` | `yyyy-MM-dd HH:mm:ss` |
| 失焦行为 | 提交当前值 | 回退到上一有效值 |
| 示例值 | `2024-01-15` | `2024-01-15 14:30:00` |

---

## 代码示例

### 示例1：基础日期时间选择

设置 `type="datetime"` 开启日期时间选择模式。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => {
  const [selectedDatetime, setSelectedDatetime] = useState("");

  const handleChange = useCallback((event) => {
    setSelectedDatetime(event.target.value);
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "8px", width: "280px" }}>
      <SlDatepicker
        label="选择日期时间"
        type="datetime"
        placeholder="请选择日期和时间"
        onSlChange={handleChange}
      />
      {selectedDatetime && (
        <div style={{ fontSize: "14px", color: "#666", padding: "8px", background: "#f5f5f5", borderRadius: "4px" }}>
          选中的日期时间: {selectedDatetime}
        </div>
      )}
    </div>
  );
};
```

---

### 示例2：设置默认日期时间

通过 `value` 设置初始日期时间，格式必须为 `yyyy-MM-dd HH:mm:ss`。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => {
  const [currentValue, setCurrentValue] = useState("2024-06-15 09:30:00");

  const handleChange = useCallback((event) => {
    setCurrentValue(event.target.value);
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "8px", width: "280px" }}>
      <SlDatepicker
        label="会议时间"
        type="datetime"
        value="2024-06-15 09:30:00"
        onSlChange={handleChange}
      />
      <div style={{ fontSize: "14px", color: "#666" }}>当前值: {currentValue}</div>
    </div>
  );
};
```

---

### 示例3：日期与日期时间对比

并排展示两种模式的差异。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

const css = `
  .comparison {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
  }
  .picker-wrapper {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }
  .value {
    font-size: 13px;
    color: #666;
    font-family: monospace;
    word-break: break-all;
  }
`;

export default () => {
  const [dateValue, setDateValue] = useState("（未选择）");
  const [datetimeValue, setDatetimeValue] = useState("（未选择）");

  const handleDateChange = useCallback((event) => {
    setDateValue(event.target.value || "（未选择）");
  }, []);

  const handleDatetimeChange = useCallback((event) => {
    setDatetimeValue(event.target.value || "（未选择）");
  }, []);

  return (
    <>
      <div className="comparison">
        <div className="picker-wrapper">
          <SlDatepicker label="日期模式 (date)" type="date" placeholder="选择日期" onSlChange={handleDateChange} />
          <div className="value">值: {dateValue}</div>
        </div>
        <div className="picker-wrapper">
          <SlDatepicker label="日期时间模式 (datetime)" type="datetime" placeholder="选择日期和时间" onSlChange={handleDatetimeChange} />
          <div className="value">值: {datetimeValue}</div>
        </div>
      </div>
      <style>{css}</style>
    </>
  );
};
```

---

### 示例4：日期时间带范围限制

结合 `min` 和 `max` 限制日期时间的可选范围。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => {
  const [selectedValue, setSelectedValue] = useState("");

  const handleChange = useCallback((event) => {
    setSelectedValue(event.target.value);
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "8px", width: "280px" }}>
      <SlDatepicker
        label="预约时间"
        type="datetime"
        min="2024-01-01"
        max="2024-12-31"
        placeholder="请选择 2024 年内的时间"
        help-text="仅可选择 2024 年内的日期"
        onSlChange={handleChange}
      />
      {selectedValue && (
        <div style={{ fontSize: "14px", color: "#333", padding: "8px", background: "#e8f5e9", borderRadius: "4px" }}>
          预约时间: {selectedValue}
        </div>
      )}
    </div>
  );
};
```

---

### 示例5：动态切换模式

通过 React state 动态切换 `date` 和 `datetime` 模式。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const [pickerType, setPickerType] = useState("date");
  const [currentValue, setCurrentValue] = useState("");

  const handleChange = useCallback((event) => {
    setCurrentValue(event.target.value);
  }, []);

  const switchToDate = () => {
    setPickerType("date");
    setCurrentValue("");
  };

  const switchToDatetime = () => {
    setPickerType("datetime");
    setCurrentValue("");
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "280px" }}>
      <div style={{ display: "flex", gap: "8px" }}>
        <SlButton
          variant={pickerType === "date" ? "primary" : "default"}
          onClick={switchToDate}
        >日期模式</SlButton>
        <SlButton
          variant={pickerType === "datetime" ? "primary" : "default"}
          onClick={switchToDatetime}
        >日期时间模式</SlButton>
      </div>
      <SlDatepicker
        label="动态切换"
        type={pickerType}
        placeholder={pickerType === "date" ? "请选择日期" : "请选择日期和时间"}
        onSlChange={handleChange}
      />
      <div style={{ fontSize: "14px", padding: "8px", background: "#f5f5f5", borderRadius: "4px", color: "#666" }}>
        <div>当前模式: {pickerType}</div>
        <div>当前值: {currentValue || "（未选择）"}</div>
      </div>
    </div>
  );
};
```

---

## 注意事项

1. **值格式严格匹配**：`datetime` 模式下值格式必须为 `yyyy-MM-dd HH:mm:ss`，缺少时间部分会导致解析失败
2. **确认行为差异**：`date` 模式选择日期后自动关闭弹窗并提交；`datetime` 模式需要点击"确定"按钮才提交
3. **失焦行为差异**：`datetime` 模式下，如果弹窗打开时失焦，会回退到上一有效值而非提交当前值
4. **切换模式清空值**：从 `date` 切换到 `datetime` 模式（或反之）时，建议清空当前值，因为值格式不兼容
5. **时间面板**：桌面端日历面板右侧显示时/分/秒三列滚动选择；移动端通过底部滚轮选择

[返回目录](../index.md)
