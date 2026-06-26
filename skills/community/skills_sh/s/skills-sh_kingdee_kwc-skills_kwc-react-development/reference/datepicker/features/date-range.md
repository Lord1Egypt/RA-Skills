# 日期范围限制

[返回目录](../index.md)

## 功能说明

通过 `min` 和 `max` 属性限制用户可选择的日期范围。超出范围的日期在日历面板中会被禁用（灰色不可点击），通过输入框输入的超范围日期也会被视为无效值。

## API 属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `min` | 最小可选日期 | `string` | `'0001-01-01'` |
| `max` | 最大可选日期 | `string` | `'9999-12-31'` |

### 格式要求

- `min` 和 `max` 的值格式为 `yyyy-MM-dd`（如 `2024-01-01`）
- 支持 `-`、`/`、`.` 分隔符
- 超出范围的日期在日历中显示为禁用状态

---

## 代码示例

### 示例1：设置可选范围

同时使用 `min` 和 `max` 限定一个日期范围。

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => (
  <SlDatepicker
    style={{ width: "230px" }}
    min="2026-01-01"
    max="2026-12-31"
    help-text="仅可选择 2026 年内的日期"
  />
);
```

---

### 示例2：动态设置最小日期（今天及之后）

根据当天日期动态设置 `min` 属性。

```jsx
import React, { useMemo } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => {
  const today = useMemo(() => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  }, []);

  return (
    <SlDatepicker
      style={{ width: "230px" }}
      label="预约日期"
      min={today}
      placeholder="只能选择今天及之后"
      help-text={`最早可选日期: ${today}`}
    />
  );
};
```

---

### 示例3：关联日期选择器（开始/结束日期）

两个日期选择器联动，开始日期限制结束日期的最小值，结束日期限制开始日期的最大值。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

const css = `
  .date-range-group {
    display: flex;
    align-items: flex-end;
    gap: 12px;
  }
  .separator {
    padding-bottom: 8px;
    color: #999;
    font-size: 14px;
  }
`;

export default () => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  const handleStartChange = useCallback((event) => {
    setStartDate(event.target.value);
  }, []);

  const handleEndChange = useCallback((event) => {
    setEndDate(event.target.value);
  }, []);

  return (
    <>
      <div className="date-range-group">
        <SlDatepicker
          label="开始日期"
          max={endDate || undefined}
          placeholder="选择开始日期"
          onSlChange={handleStartChange}
        />
        <span className="separator">至</span>
        <SlDatepicker
          label="结束日期"
          min={startDate || undefined}
          placeholder="选择结束日期"
          onSlChange={handleEndChange}
        />
      </div>
      {startDate && endDate && (
        <div style={{ marginTop: "12px", fontSize: "14px", padding: "8px", background: "#e3f2fd", borderRadius: "4px" }}>
          选择的日期范围: {startDate} 至 {endDate}
        </div>
      )}
      <style>{css}</style>
    </>
  );
};
```

---

### 示例4：动态调整日期范围

根据业务逻辑动态设置可选日期范围。

```jsx
import React, { useState, useMemo } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

export default () => {
  const [rangeType, setRangeType] = useState("week");

  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  };

  const { minDate, maxDate } = useMemo(() => {
    const now = new Date();
    if (rangeType === "week") {
      const dayOfWeek = now.getDay();
      const monday = new Date(now);
      monday.setDate(now.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1));
      const sunday = new Date(monday);
      sunday.setDate(monday.getDate() + 6);
      return { minDate: formatDate(monday), maxDate: formatDate(sunday) };
    } else if (rangeType === "month") {
      const firstDay = new Date(now.getFullYear(), now.getMonth(), 1);
      const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);
      return { minDate: formatDate(firstDay), maxDate: formatDate(lastDay) };
    } else {
      return { minDate: `${now.getFullYear()}-01-01`, maxDate: `${now.getFullYear()}-12-31` };
    }
  }, [rangeType]);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "280px" }}>
      <div style={{ display: "flex", gap: "8px" }}>
        <SlButton variant={rangeType === "week" ? "primary" : "default"} onClick={() => setRangeType("week")}>本周</SlButton>
        <SlButton variant={rangeType === "month" ? "primary" : "default"} onClick={() => setRangeType("month")}>本月</SlButton>
        <SlButton variant={rangeType === "year" ? "primary" : "default"} onClick={() => setRangeType("year")}>本年</SlButton>
      </div>
      <SlDatepicker
        label="选择日期"
        min={minDate}
        max={maxDate}
        placeholder="请在范围内选择"
        help-text={`可选范围: ${minDate} 至 ${maxDate}`}
      />
    </div>
  );
};
```

---

## 注意事项

1. **min/max 格式**：`min` 和 `max` 的值格式为 `yyyy-MM-dd`，不包含时间部分（即使在 `datetime` 模式下也是按日期维度限制）
2. **禁用效果**：超出范围的日期在日历面板中显示为灰色禁用状态，无法点击
3. **输入验证**：通过输入框键入的超出范围日期会被视为无效值，失焦时回退到上一有效值
4. **"今天"按钮**：日历面板底部的"今天"快捷按钮在今天日期不在 min/max 范围内时也会被禁用
5. **动态更新**：修改 `min` 或 `max` 后，日历面板会自动更新禁用状态

[返回目录](../index.md)
