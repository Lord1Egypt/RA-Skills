# 日期格式化

[返回目录](../index.md)

## 功能说明

通过 `format` 属性自定义日期在输入框中的显示格式。格式化底层基于 [dayjs](https://day.js.org/docs/en/display/format) 实现，支持 dayjs 的所有格式化符号。`format` 仅影响输入框中的显示文本，组件内部的 `value` 始终保持标准格式（`date` 模式为 `YYYY-MM-DD`，`datetime` 模式为 `YYYY-MM-DD HH:mm:ss`）。

## API 属性

| 属性 | 说明 | 类型 | 默认值 |
|------|------|------|--------|
| `format` | 日期显示格式（dayjs 格式字符串） | `string` | `'YYYY-MM-DD'`（date 模式）/ `'YYYY-MM-DD HH:mm:ss'`（datetime 模式） |

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
| `a` | 上午/下午（小写） | `am`、`pm` |

> **注意**：dayjs 中年份使用大写 `YYYY`，日期使用大写 `DD`，与 Java/moment 的 `yyyy`、`dd` 不同。

### 常用格式示例

| 格式字符串 | 显示效果 |
|-----------|---------|
| `YYYY-MM-DD` | `2024-01-15`（默认） |
| `YYYY/MM/DD` | `2024/01/15` |
| `DD.MM.YYYY` | `15.01.2024` |
| `MM-DD-YYYY` | `01-15-2024` |
| `YYYY年MM月DD日` | `2024年01月15日` |
| `YYYY-MM-DD HH:mm:ss` | `2024-01-15 14:30:00`（datetime 默认） |
| `YYYY/MM/DD HH:mm` | `2024/01/15 14:30` |
| `YYYY-MM-DD hh:mm A` | `2024-01-15 02:30 PM` |

---

## 代码示例

### 示例1：基础格式化 - 斜杠分隔

使用 `format="YYYY/MM/DD"` 将日期显示为斜杠分隔格式。

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => {
  const [value, setValue] = useState("");

  const handleChange = useCallback((event) => {
    setValue(event.target.value);
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "8px", width: "230px" }}>
      <SlDatepicker
        label="斜杠格式"
        format="YYYY/MM/DD"
        placeholder="YYYY/MM/DD"
        onSlChange={handleChange}
      />
      {value && (
        <div style={{ fontSize: "14px", color: "#666" }}>
          实际 value: {value}
        </div>
      )}
    </div>
  );
};
```

---

### 示例2：中文日期格式

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => (
  <SlDatepicker
    style={{ width: "280px" }}
    label="中文格式"
    format="YYYY年MM月DD日"
    placeholder="请选择日期"
  />
);
```

---

### 示例3：点号分隔格式（欧洲风格）

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => (
  <SlDatepicker
    style={{ width: "230px" }}
    label="欧洲日期格式"
    format="DD.MM.YYYY"
    placeholder="DD.MM.YYYY"
  />
);
```

---

### 示例4：多种格式对比

```jsx
import React from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => (
  <div style={{ display: "flex", flexDirection: "column", gap: "16px", maxWidth: "300px" }}>
    <SlDatepicker label="默认格式 (YYYY-MM-DD)" value="2024-06-15" />
    <SlDatepicker label="斜杠格式 (YYYY/MM/DD)" format="YYYY/MM/DD" value="2024-06-15" />
    <SlDatepicker label="点号格式 (DD.MM.YYYY)" format="DD.MM.YYYY" value="2024-06-15" />
    <SlDatepicker label="中文格式 (YYYY年MM月DD日)" format="YYYY年MM月DD日" value="2024-06-15" />
    <SlDatepicker label="美式格式 (MM-DD-YYYY)" format="MM-DD-YYYY" value="2024-06-15" />
  </div>
);
```

---

### 示例5：日期时间模式下的格式化

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';

export default () => {
  const [defaultVal, setDefaultVal] = useState("2024-06-15 09:30:00");
  const [customVal, setCustomVal] = useState("2024-06-15 09:30:00");

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "16px", maxWidth: "300px" }}>
      <SlDatepicker
        label="默认 datetime 格式"
        type="datetime"
        value={defaultVal}
        onSlChange={(e) => setDefaultVal(e.target.value)}
      />
      <SlDatepicker
        label="自定义 datetime 格式"
        type="datetime"
        format="YYYY/MM/DD HH:mm"
        value={customVal}
        onSlChange={(e) => setCustomVal(e.target.value)}
      />
      <div style={{ fontSize: "14px", color: "#666" }}>
        <div>默认格式值: {defaultVal}</div>
        <div>自定义格式值: {customVal}</div>
      </div>
    </div>
  );
};
```

---

### 示例6：动态切换格式

```jsx
import React, { useState, useCallback } from "react";
import SlDatepicker from '@kdcloudjs/shoelace/dist/react/datepicker/index.js';
import SlButton from '@kdcloudjs/shoelace/dist/react/button/index.js';

const formats = [
  { label: "YYYY-MM-DD", value: "YYYY-MM-DD" },
  { label: "YYYY/MM/DD", value: "YYYY/MM/DD" },
  { label: "YYYY年MM月DD日", value: "YYYY年MM月DD日" },
];

export default () => {
  const [currentFormat, setCurrentFormat] = useState("YYYY-MM-DD");

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "12px", maxWidth: "300px" }}>
      <div style={{ display: "flex", gap: "8px" }}>
        {formats.map((f) => (
          <SlButton
            key={f.value}
            variant={currentFormat === f.value ? "primary" : "default"}
            size="small"
            onClick={() => setCurrentFormat(f.value)}
          >
            {f.label}
          </SlButton>
        ))}
      </div>
      <SlDatepicker label="动态格式" format={currentFormat} value="2024-06-15" />
      <div style={{ fontSize: "14px", color: "#666" }}>当前格式: {currentFormat}</div>
    </div>
  );
};
```

---

## 注意事项

1. **基于 dayjs 实现**：`format` 底层使用 dayjs 进行格式化，支持 dayjs 的所有格式化符号，详见 [dayjs format 文档](https://day.js.org/docs/en/display/format)
2. **format 仅影响显示**：`format` 属性只改变输入框中的显示文本，`value` 始终保持标准格式（`YYYY-MM-DD` 或 `YYYY-MM-DD HH:mm:ss`）
3. **默认格式**：`date` 模式默认为 `YYYY-MM-DD`，`datetime` 模式默认为 `YYYY-MM-DD HH:mm:ss`
4. **手动输入**：设置 `format` 后，用户手动输入时也需要按照 `format` 指定的格式输入
5. **dayjs 符号大小写**：年份用大写 `YYYY`，日期用大写 `DD`，月份用大写 `MM`，小时 `HH`（24h）/ `hh`（12h），分钟用小写 `mm`，秒用小写 `ss`
6. **与 type 配合**：`datetime` 模式的 `format` 应包含时间部分（如 `HH:mm:ss` 或 `HH:mm`），否则时间信息将不会在输入框中显示

[返回目录](../index.md)
