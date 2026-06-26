# 表单集成

[返回目录](../index.md)

## 功能说明

`SlDatepicker` 实现了表单控件接口（`ShoelaceFormControl`），可以无缝集成到 HTML 表单中。支持 `name`、`required`、`form` 等标准表单属性，以及 `checkValidity()`、`reportValidity()` 等表单校验方法。

## API 属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `name` | 表单字段名 | `string` | `''` |
| `value` | 表单提交值 | `string` | `''` |
| `required` | 是否必填 | `boolean` | `false` |
| `form` | 关联表单的 ID | `string` | `''` |
| `disabled` | 禁用（不参与表单提交） | `boolean` | `false` |

### 表单方法

| 方法 | 说明 | 返回值 |
|------|------|--------|
| `checkValidity()` | 校验是否有效 | `boolean` |
| `reportValidity()` | 校验并显示提示 | `boolean` |
| `setCustomValidity(message)` | 设置自定义校验消息 | `void` |
| `getForm()` | 获取关联的表单元素 | `HTMLFormElement \| null` |

---

## 代码示例

### 示例1：基础表单提交

Datepicker 配合表单使用，通过 `name` 属性设置表单字段名。

```jsx
import React, { useState } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const [submitResult, setSubmitResult] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });
    setSubmitResult(JSON.stringify(data, null, 2));
  };

  return (
    <div style={{ maxWidth: "300px" }}>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "16px" }}>
          <SlDatepicker name="birthday" label="出生日期" required placeholder="请选择出生日期" />
        </div>
        <div style={{ marginBottom: "16px" }}>
          <SlDatepicker name="joinDate" label="入职日期" placeholder="请选择入职日期" />
        </div>
        <div style={{ display: "flex", gap: "8px", marginTop: "24px" }}>
          <SlButton type="submit" variant="primary">提交</SlButton>
          <SlButton type="reset" variant="default">重置</SlButton>
        </div>
      </form>
      {submitResult && (
        <div style={{ marginTop: "16px", padding: "8px", background: "#f5f5f5", borderRadius: "4px", fontFamily: "monospace", fontSize: "14px", whiteSpace: "pre" }}>
          提交数据: {submitResult}
        </div>
      )}
    </div>
  );
};
```

---

### 示例2：必填校验

设置 `required` 属性后，表单提交时会自动校验。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("表单校验通过，提交数据");
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: "300px" }}>
      <div style={{ marginBottom: "16px" }}>
        <SlDatepicker
          name="startDate"
          label="项目开始日期"
          required
          placeholder="必填项"
          help-text="此字段为必填"
        />
      </div>
      <div style={{ marginBottom: "16px" }}>
        <SlDatepicker
          name="endDate"
          label="项目结束日期"
          placeholder="选填项"
          help-text="此字段为选填"
        />
      </div>
      <SlButton type="submit" variant="primary">提交</SlButton>
    </form>
  );
};
```

---

### 示例3：程序化校验

通过 JavaScript 调用 `ref` 上的校验方法进行程序化校验。

```jsx
import React, { useRef, useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const datepickerRef = useRef(null);
  const [validationMessage, setValidationMessage] = useState("");
  const [isValid, setIsValid] = useState(false);

  const handleChange = useCallback((event) => {
    if (event.target.value) {
      datepickerRef.current?.setCustomValidity("");
      setValidationMessage("");
    }
  }, []);

  const validate = () => {
    const picker = datepickerRef.current;
    if (!picker) return;

    if (!picker.value) {
      picker.setCustomValidity("请选择一个有效的交付日期");
      picker.reportValidity();
      setValidationMessage("校验失败：请选择交付日期");
      setIsValid(false);
      return;
    }

    const date = new Date(picker.value);
    const dayOfWeek = date.getDay();
    if (dayOfWeek === 0 || dayOfWeek === 6) {
      picker.setCustomValidity("交付日期不能是周末");
      picker.reportValidity();
      setValidationMessage("校验失败：不能选择周末");
      setIsValid(false);
      return;
    }

    picker.setCustomValidity("");
    setValidationMessage("校验通过");
    setIsValid(true);
  };

  const resetValidation = () => {
    datepickerRef.current?.setCustomValidity("");
    setValidationMessage("");
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", maxWidth: "300px" }}>
      <SlDatepicker
        ref={datepickerRef}
        label="交付日期"
        required
        placeholder="请选择交付日期"
        onSlChange={handleChange}
      />
      <div style={{ display: "flex", gap: "8px" }}>
        <SlButton variant="primary" onClick={validate}>校验</SlButton>
        <SlButton variant="default" onClick={resetValidation}>重置校验</SlButton>
      </div>
      {validationMessage && (
        <div style={{
          padding: "8px",
          borderRadius: "4px",
          fontSize: "14px",
          background: isValid ? "#e8f5e9" : "#ffebee",
          border: isValid ? "1px solid #a5d6a7" : "1px solid #ef9a9a",
          color: isValid ? "#2e7d32" : "#c62828",
        }}>
          {validationMessage}
        </div>
      )}
    </div>
  );
};
```

---

## 注意事项

1. **name 属性**：设置 `name` 后，Datepicker 的值才会包含在 FormData 中
2. **disabled 不提交**：禁用状态的 Datepicker 不参与表单提交
3. **required 校验**：`required` 校验在 `reportValidity()` 或表单提交时触发，空值会提示必填
4. **自定义校验**：使用 `setCustomValidity(message)` 设置自定义错误信息，传入空字符串 `''` 清除校验错误
5. **表单重置**：原生表单的 `reset` 事件会将 Datepicker 恢复到 `defaultValue`

[返回目录](../index.md)
