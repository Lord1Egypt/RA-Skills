# 事件处理

[返回目录](../index.md)

## 功能说明

`SlDatepicker` 提供 `sl-change`、`sl-input` 和 `sl-invalid` 三个核心事件，分别用于监听值确认变更、输入过程中的值变化和校验失败。

在 JSX 中使用 `onSl*` 前缀属性绑定事件，命名规则如下：

| DOM 事件 | JSX 属性 |
|----------|----------|
| `sl-change` | `onSlChange` |
| `sl-input` | `onSlInput` |
| `sl-invalid` | `onSlInvalid` |
| `sl-focus` | `onSlFocus` |
| `sl-blur` | `onSlBlur` |
| `sl-clear` | `onSlClear` |

## API 事件

| 事件 | 说明 | 触发时机 |
|------|------|----------|
| `sl-change` | 值确认变更 | 选择日期并确认、输入框失焦提交、清除值时触发 |
| `sl-input` | 输入过程变化 | 输入框键入、日历面板选择日期时触发（值变化的实时通知） |
| `sl-invalid` | 校验失败 | 表单校验失败时触发 |

### 事件获取值的方式

```jsx
// 通过 event.target.value 获取当前值
const handleChange = (event) => {
  const value = event.target.value;  // 如 '2024-01-15' 或 '2024-01-15 14:30:00'
};
```

### sl-change 与 sl-input 的区别

| 特性 | `sl-change` | `sl-input` |
|------|-------------|------------|
| 触发频率 | 仅在值最终确认时 | 值每次变化都触发 |
| date 模式 | 选择日期后 | 选择日期时、输入时 |
| datetime 模式 | 点击确定后 | 选择日期/时间时、输入时 |
| 清除操作 | 触发 | 触发 |
| 用途 | 保存数据、提交表单 | 实时预览、联动更新 |

---

## 代码示例

### 示例1：基础事件监听

监听 `sl-change` 和 `sl-input` 事件获取日期值变化。直接在 JSX 中使用 `onSlChange`、`onSlInput` 属性。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => {
  const [changeValue, setChangeValue] = useState("-");
  const [inputValue, setInputValue] = useState("-");

  const handleChange = useCallback((event) => {
    setChangeValue(event.target.value || "-");
    console.log("sl-change:", event.target.value);
  }, []);

  const handleInput = useCallback((event) => {
    setInputValue(event.target.value || "-");
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "280px" }}>
      <div style={{ padding: "8px", background: "#f5f5f5", borderRadius: "4px", fontSize: "14px" }}>
        <p style={{ margin: "4px 0" }}>当前值 (sl-change): {changeValue}</p>
        <p style={{ margin: "4px 0" }}>实时值 (sl-input): {inputValue}</p>
      </div>
      <SlDatepicker
        placeholder="选择日期"
        clearable
        onSlChange={handleChange}
        onSlInput={handleInput}
      />
    </div>
  );
};
```

---

### 示例2：区分 sl-change 和 sl-input

对比两个事件的触发时机和频率。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

const css = `
  .event-panel {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 16px;
  }
  .event-section {
    padding: 16px;
    background: #fafafa;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
  }
  .event-section h4 {
    margin: 0 0 8px 0;
    font-size: 14px;
  }
  .count {
    font-size: 24px;
    font-weight: bold;
    color: #1976d2;
    margin-bottom: 4px;
  }
  .value {
    font-size: 13px;
    color: #666;
    font-family: monospace;
  }
`;

export default () => {
  const [inputCount, setInputCount] = useState(0);
  const [changeCount, setChangeCount] = useState(0);
  const [lastInputValue, setLastInputValue] = useState("（无）");
  const [lastChangeValue, setLastChangeValue] = useState("（无）");

  const handleInput = useCallback((event) => {
    setInputCount((prev) => prev + 1);
    setLastInputValue(event.target.value || "（空）");
  }, []);

  const handleChange = useCallback((event) => {
    setChangeCount((prev) => prev + 1);
    setLastChangeValue(event.target.value || "（空）");
  }, []);

  return (
    <>
      <SlDatepicker
        label="输入或选择日期"
        placeholder="请操作查看事件触发"
        style={{ width: "280px" }}
        onSlInput={handleInput}
        onSlChange={handleChange}
      />
      <div className="event-panel">
        <div className="event-section">
          <h4>sl-input 事件（实时触发）</h4>
          <div className="count">触发次数: {inputCount}</div>
          <div className="value">最新值: {lastInputValue}</div>
        </div>
        <div className="event-section">
          <h4>sl-change 事件（确认时触发）</h4>
          <div className="count">触发次数: {changeCount}</div>
          <div className="value">最新值: {lastChangeValue}</div>
        </div>
      </div>
      <style>{css}</style>
    </>
  );
};
```

---

### 示例3：实时预览与确认保存

利用 `sl-input` 做实时预览，`sl-change` 做最终保存。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

const css = `
  .panels {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 16px;
  }
  .panel {
    padding: 16px;
    border-radius: 8px;
  }
  .preview {
    background: #fff3e0;
    border: 1px solid #ffcc80;
  }
  .saved {
    background: #e8f5e9;
    border: 1px solid #a5d6a7;
  }
  .panel h4 {
    margin: 0 0 4px 0;
    font-size: 14px;
  }
  .display {
    font-size: 16px;
    font-family: monospace;
    font-weight: 500;
  }
`;

export default () => {
  const [previewValue, setPreviewValue] = useState("等待输入...");
  const [savedValue, setSavedValue] = useState("等待确认...");

  const handleInput = useCallback((event) => {
    setPreviewValue(event.target.value || "（空）");
  }, []);

  const handleChange = useCallback((event) => {
    const value = event.target.value;
    setSavedValue(value || "（已清空）");
    console.log("保存到服务器:", value);
  }, []);

  return (
    <>
      <SlDatepicker
        label="选择日期"
        type="datetime"
        placeholder="实时预览 + 确认保存"
        style={{ width: "280px" }}
        onSlInput={handleInput}
        onSlChange={handleChange}
      />
      <div className="panels">
        <div className="panel preview">
          <h4>实时预览（sl-input）</h4>
          <div className="display">{previewValue}</div>
        </div>
        <div className="panel saved">
          <h4>已保存（sl-change）</h4>
          <div className="display">{savedValue}</div>
        </div>
      </div>
      <style>{css}</style>
    </>
  );
};
```

---

### 示例4：联动多个日期选择器

通过 `onSlChange` 实现多个日期选择器的联动逻辑。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => {
  const [joinDate, setJoinDate] = useState("");
  const [probationEndDate, setProbationEndDate] = useState("");
  const [regularDate, setRegularDate] = useState("");

  const handleJoinChange = useCallback((event) => {
    const value = event.target.value;
    setJoinDate(value);
    if (value) {
      const date = new Date(value);
      date.setMonth(date.getMonth() + 3);
      const y = date.getFullYear();
      const m = String(date.getMonth() + 1).padStart(2, "0");
      const d = String(date.getDate()).padStart(2, "0");
      setProbationEndDate(`${y}-${m}-${d}`);
    } else {
      setProbationEndDate("");
      setRegularDate("");
    }
  }, []);

  const handleProbationChange = useCallback((event) => {
    setProbationEndDate(event.target.value);
    if (!event.target.value) setRegularDate("");
  }, []);

  const handleRegularChange = useCallback((event) => {
    setRegularDate(event.target.value);
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
      <div style={{ display: "flex", gap: "16px", flexWrap: "wrap" }}>
        <SlDatepicker
          label="入职日期"
          placeholder="先选择入职日期"
          onSlChange={handleJoinChange}
        />
        <SlDatepicker
          label="试用期结束"
          min={joinDate || undefined}
          value={probationEndDate}
          placeholder={joinDate ? "选择试用期结束日期" : "请先选择入职日期"}
          disabled={!joinDate}
          onSlChange={handleProbationChange}
        />
        <SlDatepicker
          label="转正日期"
          min={probationEndDate || undefined}
          value={regularDate}
          placeholder={probationEndDate ? "选择转正日期" : "请先选择试用期结束日期"}
          disabled={!probationEndDate}
          onSlChange={handleRegularChange}
        />
      </div>
      {joinDate && probationEndDate && regularDate && (
        <div style={{ fontSize: "14px", padding: "8px", background: "#e3f2fd", borderRadius: "4px" }}>
          入职: {joinDate} → 试用期结束: {probationEndDate} → 转正: {regularDate}
        </div>
      )}
    </div>
  );
};
```

---

## 事件绑定模式总结

```jsx
// 正确方式：JSX onSl* 属性
const handleChange = useCallback((event) => {
  console.log("选中日期:", event.target.value);
}, []);

const handleInput = useCallback((event) => {
  console.log("实时值:", event.target.value);
}, []);

<SlDatepicker
  onSlChange={handleChange}
  onSlInput={handleInput}
/>
```

---

## 注意事项

1. **事件命名规范**：`sl-change` → `onSlChange`，`sl-input` → `onSlInput`，依此类推（`onSl*` + PascalCase）
2. **获取值**：统一通过 `event.target.value` 获取当前值，而非 `event.detail`
3. **sl-change 不频繁触发**：`sl-change` 仅在值最终确认时触发，适合做数据保存；`sl-input` 实时触发，适合做预览
4. **datetime 模式差异**：在 `datetime` 模式下，选择日期/时间过程中只触发 `sl-input`，点击确定后才触发 `sl-change`
5. **清除触发**：清除按钮会同时触发 `sl-input` 和 `sl-change`，值为空字符串 `''`
6. **建议使用 useCallback**：将事件处理函数用 `useCallback` 包裹，避免不必要的重渲染

[返回目录](../index.md)
