# 校验

[返回目录](../index.md)

## 功能说明

`SlDatepicker` 支持内置校验（`required`、`min/max` 范围）和自定义校验（`setCustomValidity`）。组件实现了标准的表单校验接口，可与浏览器原生表单校验机制无缝配合。

## API

### 校验相关属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `required` | 是否必填 | `boolean` | `false` |
| `min` | 最小可选日期 | `string` | `'0001-01-01'` |
| `max` | 最大可选日期 | `string` | `'9999-12-31'` |

### 校验方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `checkValidity()` | 检查是否有效（不显示提示） | `boolean` |
| `reportValidity()` | 检查并显示校验提示 | `boolean` |
| `setCustomValidity(message)` | 设置自定义校验消息 | `void` |

### 校验事件

| 事件 | 说明 |
|------|------|
| `sl-invalid` | 校验失败时触发 |

---

## 代码示例

### 示例1：自定义校验消息

使用 `ref` 调用 `setCustomValidity()` 方法设置自定义校验消息。

```jsx
import React, { useRef, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const datepickerRef = useRef(null);

  const handleChange = useCallback(() => {
    // 值变化时清除之前的自定义校验
    datepickerRef.current?.setCustomValidity("");
  }, []);

  const handleValidate = useCallback(() => {
    const el = datepickerRef.current;
    if (!el) return;

    const val = el.value;
    if (!val) {
      el.setCustomValidity("请选择一个日期");
    } else if (val < "2024-01-01" || val > "2024-12-31") {
      el.setCustomValidity("日期必须在 2024 年范围内");
    } else {
      el.setCustomValidity("");
    }
    el.reportValidity();
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "280px" }}>
      <SlDatepicker
        ref={datepickerRef}
        label="选择日期"
        help-text="仅允许选择 2024 年内的日期"
        onSlChange={handleChange}
      />
      <SlButton variant="primary" size="small" onClick={handleValidate}>校验</SlButton>
    </div>
  );
};
```

---

### 示例2：业务规则校验（工作日校验）

自定义校验逻辑：只允许选择工作日（周一至周五）。

```jsx
import React, { useRef, useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => {
  const datepickerRef = useRef(null);
  const [statusText, setStatusText] = useState("");
  const [isValid, setIsValid] = useState(false);

  const validateWorkday = useCallback((event) => {
    const value = event.target.value;
    const el = datepickerRef.current;

    if (!value) {
      el?.setCustomValidity("");
      setStatusText("");
      return;
    }

    const date = new Date(value);
    const dayOfWeek = date.getDay();
    const dayNames = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];

    if (dayOfWeek === 0 || dayOfWeek === 6) {
      el?.setCustomValidity(`${dayNames[dayOfWeek]}不可发货，请选择工作日`);
      el?.reportValidity();
      setStatusText(`${value} 是${dayNames[dayOfWeek]}，不可发货`);
      setIsValid(false);
    } else {
      el?.setCustomValidity("");
      setStatusText(`${value} 是${dayNames[dayOfWeek]}，可以发货`);
      setIsValid(true);
    }
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "280px" }}>
      <SlDatepicker
        ref={datepickerRef}
        label="发货日期"
        placeholder="仅工作日可选"
        help-text="发货仅支持工作日（周一至周五）"
        onSlChange={validateWorkday}
      />
      {statusText && (
        <div style={{ fontSize: "14px", color: isValid ? "#2e7d32" : "#c62828" }}>
          {statusText}
        </div>
      )}
    </div>
  );
};
```

---

### 示例3：多字段联合校验

对表单中多个日期字段进行联合校验。

```jsx
import React, { useRef, useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const startRef = useRef(null);
  const endRef = useRef(null);
  const reportRef = useRef(null);
  const [errors, setErrors] = useState([]);

  const crossValidate = useCallback(() => {
    const startEl = startRef.current;
    const endEl = endRef.current;
    const reportEl = reportRef.current;

    startEl?.setCustomValidity("");
    endEl?.setCustomValidity("");
    reportEl?.setCustomValidity("");

    const startDate = startEl?.value ? new Date(startEl.value) : null;
    const endDate = endEl?.value ? new Date(endEl.value) : null;
    const reportDate = reportEl?.value ? new Date(reportEl.value) : null;

    if (startDate && endDate && endDate <= startDate) {
      endEl.setCustomValidity("结束日期必须晚于开始日期");
    }
    if (endDate && reportDate && reportDate <= endDate) {
      reportEl.setCustomValidity("报告日期必须晚于结束日期");
    }
  }, []);

  const handleSubmit = useCallback(() => {
    const pickers = [startRef.current, endRef.current, reportRef.current];
    const errorList = [];
    let allValid = true;

    pickers.forEach((picker) => {
      if (picker && !picker.reportValidity()) {
        allValid = false;
        errorList.push(`${picker.label}: ${picker.validationMessage}`);
      }
    });

    setErrors(errorList);
    if (allValid) {
      console.log("所有校验通过，提交表单");
    }
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", maxWidth: "300px" }}>
      <SlDatepicker ref={startRef} label="开始日期" required placeholder="选择开始日期" onSlChange={crossValidate} />
      <SlDatepicker ref={endRef} label="结束日期" required placeholder="选择结束日期" onSlChange={crossValidate} />
      <SlDatepicker
        ref={reportRef}
        label="报告日期"
        required
        placeholder="选择报告日期"
        help-text="报告日期必须在结束日期之后"
        onSlChange={crossValidate}
      />
      <SlButton variant="primary" onClick={handleSubmit}>提交</SlButton>
      {errors.length > 0 && (
        <div style={{ padding: "12px", background: "#ffebee", border: "1px solid #ef9a9a", borderRadius: "8px" }}>
          <h4 style={{ margin: "0 0 4px 0", color: "#c62828", fontSize: "14px" }}>校验错误:</h4>
          {errors.map((error, i) => (
            <div key={i} style={{ color: "#c62828", fontSize: "13px", marginBottom: "2px" }}>{error}</div>
          ))}
        </div>
      )}
    </div>
  );
};
```

---

### 示例4：checkValidity 静默校验

使用 `checkValidity()` 进行不显示 UI 提示的静默校验。

```jsx
import React, { useRef, useState } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const datepickerRef = useRef(null);
  const [checkResult, setCheckResult] = useState("");

  const silentCheck = () => {
    const isValid = datepickerRef.current?.checkValidity();
    setCheckResult(
      isValid
        ? "有效（checkValidity 不会显示提示框）"
        : "无效（checkValidity 不会显示提示框）"
    );
  };

  const reportCheck = () => {
    const isValid = datepickerRef.current?.reportValidity();
    setCheckResult(
      isValid
        ? "有效（reportValidity 已显示/隐藏提示）"
        : "无效（reportValidity 已显示提示）"
    );
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", maxWidth: "300px" }}>
      <SlDatepicker
        ref={datepickerRef}
        label="会议日期"
        required
        placeholder="请选择会议日期"
      />
      <div style={{ display: "flex", gap: "8px" }}>
        <SlButton variant="primary" onClick={silentCheck}>静默校验</SlButton>
        <SlButton variant="default" onClick={reportCheck}>UI 校验</SlButton>
      </div>
      {checkResult && (
        <div style={{ padding: "8px", background: "#f5f5f5", borderRadius: "4px", fontSize: "14px", fontFamily: "monospace" }}>
          校验结果: {checkResult}
        </div>
      )}
    </div>
  );
};
```

---

## 注意事项

1. **required 校验时机**：`required` 校验在调用 `reportValidity()` 或表单 `submit` 时触发，不会在输入过程中实时触发
2. **setCustomValidity 使用**：设置自定义消息后需调用 `reportValidity()` 才会显示；传入空字符串 `''` 清除错误
3. **min/max 是输入级校验**：`min/max` 范围之外的日期在日历面板中被禁用，但通过输入框键入的超范围值会在失焦时回退
4. **清除时的校验**：清除值后再次校验会触发 `required` 的必填校验
5. **validity 属性**：`validity` 是只读的 `ValidityState` 对象，包含 `valid`、`valueMissing` 等标准属性

[返回目录](../index.md)
