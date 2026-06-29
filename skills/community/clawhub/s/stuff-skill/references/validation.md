# 校验规则文档

生成 PWA 后，Agent 必须对生成产物执行以下校验规则。每条规则对应一个具体的检查项，全部通过后方可向用户交付。

---

## 校验执行时机

1. **生成完成后**：Agent 自动执行 R1~R7 全量校验
2. **用户要求修改后**：重新执行受影响的规则
3. **部署前**：执行 R3、R5、R6 作为最终确认

---

## R1：Schema 完整性

**目标**：确保数据 schema 结构合法，具备最基本的查找和筛选能力。

### R1-A：主标识字段存在
- **检查方法**：schema 中必须存在一个 `type: "text"` 且标记为 `primary: true` 的字段（或字段名为 `name` / `title`）
- **通过条件**：存在且唯一
- **失败处理**：提示用户"未找到主标识字段，是否将 `[推断的第一个文本字段]` 设为主标识？"

### R1-B：状态字段存在
- **检查方法**：schema 中必须存在一个 `type: "select"` 且包含 2 个以上选项的字段，命名含 `status` / `状态` / `stage` / `phase`，或字段 `isStatus: true`
- **通过条件**：存在至少一个
- **失败处理**：提示用户"建议添加状态字段用于筛选，例如：在用/归档"，若用户同意则自动补充

### R1-C：字段数量合理
- **通过条件**：schema 字段数量在 2~20 之间
- **失败处理**：> 20 字段时警告"字段过多，建议拆分或合并相关字段"

---

## R2：字段类型匹配

**目标**：确保 HTML input 类型与推断的字段类型一致，避免数据录入类型错误。

| 推断类型 | 期望 HTML | 检查项 |
|----------|-----------|--------|
| text | `<input type="text">` 或 `<input>` | `type` 属性为 `text` 或缺省 |
| number | `<input type="number">` | `type="number"` 存在 |
| date | `<input type="date">` | `type="date"` 存在 |
| textarea | `<textarea>` | 使用 `textarea` 标签而非 `input` |
| select（固定）| `<select>` + 静态 `<option>` | select 内有 `<option>` 子元素 |
| smart-select | 三件套（见下方 R7）| 见 R7 |
| boolean | `<input type="checkbox">` | `type="checkbox"` 存在 |

**检查方法**（伪代码）：
```
for each field in schema:
  fieldId = field.name
  if field.type == "number":
    assert HTML contains: input[id="field-{fieldId}"][type="number"]
  if field.type == "date":
    assert HTML contains: input[id="field-{fieldId}"][type="date"]
  if field.type == "textarea":
    assert HTML contains: textarea[id="field-{fieldId}"]
  if field.type == "boolean":
    assert HTML contains: input[id="field-{fieldId}"][type="checkbox"]
```

**失败处理**：列出类型不匹配的字段，Agent 自动修正 HTML。

---

## R3：API 完整性

**目标**：确保 `functions/api/items.js` 实现了完整的 CRUD 端点，数据可持久化。

### R3-A：GET 端点
- **检查方法**：`onRequest` 函数中存在 `request.method === 'GET'` 分支
- **通过条件**：分支存在，且包含 `SELECT` SQL 语句或等效查询
- **语义验证**：返回的是列表（JSON array），而非单条记录

### R3-B：POST 端点（新增 + 更新）
- **检查方法**：`request.method === 'POST'` 分支存在
- **通过条件**：
  - 包含 `INSERT INTO` 逻辑
  - 包含 `UPDATE` 逻辑（通过 `id` 判断新增还是更新）
  - 读取 `request.json()` 或等效解析

### R3-C：DELETE 端点
- **检查方法**：`request.method === 'DELETE'` 分支存在
- **通过条件**：
  - 从 URL params 或 body 中读取 `id`
  - 包含 `DELETE FROM` SQL
  - 缺少 `id` 时返回 400 错误

### R3-D：CORS 头部
- **通过条件**：响应包含 `'Access-Control-Allow-Origin': '*'`（或具体域名）

**失败处理**：缺少端点时，Agent 自动补充对应代码块。

---

## R4：离线兜底

**目标**：确保 API 不可用时（首次加载后断网），应用仍可展示数据。

### R4-A：localStorage fallback 逻辑存在
- **检查方法**：`index.html` 中存在以下模式（任意一种）：
  ```js
  // 模式 A：try/catch 兜底
  try {
    const res = await fetch('/api/items');
    items = await res.json();
    localStorage.setItem('items-cache', JSON.stringify(items));
  } catch {
    const cached = localStorage.getItem('items-cache');
    if (cached) items = JSON.parse(cached);
  }

  // 模式 B：显式检查
  if (!navigator.onLine) {
    // 从 localStorage 读取
  }
  ```
- **通过条件**：存在上述任意模式，且 `localStorage.setItem` 和 `getItem` 均出现在数据加载逻辑附近

### R4-B：写操作离线提示（可选但推荐）
- **检查方法**：POST/DELETE 的 `catch` 块中有用户提示
- **通过条件**：catch 块不为空，包含 `alert` / `console.error` / toast 类提示

**失败处理**：R4-A 未通过时，Agent 自动将 fetch 调用包裹在 try/catch + localStorage 模式中。

---

## R5：移动端适配

**目标**：确保应用在移动设备上可用，包括 PWA standalone 模式。

### R5-A：viewport meta 正确
- **检查方法**：`index.html` `<head>` 中存在：
  ```html
  <meta name="viewport" content="width=device-width, initial-scale=1">
  ```
  或包含 `viewport-fit=cover`（推荐，用于 safe area 支持）
- **通过条件**：存在 viewport meta 且包含 `width=device-width`

### R5-B：standalone 模式 padding 存在
- **检查方法**：CSS 中存在以下模式：
  ```css
  @media (display-mode: standalone) {
    /* 包含 safe-area-inset-top 或 safe-area-inset-bottom */
  }
  ```
  或全局使用了 `env(safe-area-inset-*)` 变量
- **通过条件**：至少一处使用了 `safe-area-inset` 相关属性

### R5-C：FAB 按钮 bottom 适配
- **检查方法**：`.fab` 的 `bottom` 属性包含 `env(safe-area-inset-bottom)`
- **通过条件**：`.fab` 样式中包含此属性

**失败处理**：自动补充缺失的 meta 或 CSS 规则。

---

## R6：PWA 要素

**目标**：确保应用可被安装为 PWA，具备离线能力和原生体验。

### R6-A：manifest.json 必要字段
- **检查方法**：`public/manifest.json` 存在且包含以下字段：
  ```json
  {
    "name": "...",           // 必须
    "short_name": "...",     // 必须
    "start_url": "/",        // 必须
    "display": "standalone", // 必须，必须是 "standalone"
    "background_color": "...", // 必须
    "theme_color": "...",    // 必须
    "icons": [               // 必须，至少包含 192 和 512
      { "src": "...", "sizes": "192x192", "type": "image/png" },
      { "src": "...", "sizes": "512x512", "type": "image/png" }
    ]
  }
  ```
- **通过条件**：以上所有字段均存在且不为空

### R6-B：manifest link 标签存在
- **检查方法**：`index.html` `<head>` 中包含：
  ```html
  <link rel="manifest" href="/manifest.json">
  ```
- **通过条件**：存在且 href 指向正确路径

### R6-C：Service Worker 注册存在
- **检查方法**：`index.html` 中存在：
  ```js
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
  }
  ```
- **通过条件**：注册代码存在，`sw.js` 文件在 `public/` 目录下

### R6-D：sw.js 包含 install + fetch 事件监听
- **检查方法**：`public/sw.js` 中同时包含：
  - `self.addEventListener('install', ...)`
  - `self.addEventListener('fetch', ...)`
- **通过条件**：两个事件均有监听

**失败处理**：
- R6-A 缺字段：自动补充默认值
- R6-C 缺注册：在 `</body>` 前插入注册代码
- R6-D 缺事件：补充对应事件监听骨架

---

## R7：Smart Select 一致性

**目标**：确保标记为 `smart-select` 的字段，HTML 中有完整的三件套实现，避免数据无法正确录入。

**三件套定义**（每个 smart-select 字段必须同时存在）：

1. **`<select>` 下拉**（id 格式：`field-{fieldName}-select`）
2. **`<input type="hidden">`**（id 格式：`field-{fieldName}`，实际存值）
3. **`<input type="text">`**（id 格式：`field-{fieldName}-custom`，手动输入新值）

**检查方法**（伪代码）：
```
for each field in schema where field.type == "smart-select":
  fieldName = field.name
  assert HTML contains: select#field-{fieldName}-select
  assert HTML contains: input[type="hidden"]#field-{fieldName}
  assert HTML contains: input[type="text"]#field-{fieldName}-custom
```

**JS 联动函数存在性检查**：
- `syncSmartSelect(fieldName)` 函数必须存在（select 变化时调用）
- `syncSmartSelectCustom(fieldName)` 函数必须存在（custom input 变化时调用）
- 两个函数都应写入 hidden input 的值

**通过条件**：schema 中每个 `smart-select` 字段的三件套均完整存在，JS 联动函数均已定义。

**失败处理**：列出缺失件，Agent 自动补充对应 HTML 和 JS。

---

## 校验结果报告格式

Agent 执行完全量校验后，向用户输出如下摘要：

```
校验结果：
✅ R1 Schema 完整性 — 通过（主标识: name, 状态字段: status）
✅ R2 字段类型匹配 — 通过（11 个字段全部匹配）
✅ R3 API 完整性 — 通过（GET / POST / DELETE 均已实现）
✅ R4 离线兜底 — 通过（localStorage fallback 已配置）
✅ R5 移动端适配 — 通过（viewport + standalone padding 均存在）
✅ R6 PWA 要素 — 通过（manifest + SW 注册 + install/fetch 事件）
✅ R7 Smart Select — 通过（2 个 smart-select 字段三件套完整）

全部通过，可以部署。
```

若有失败项：
```
⚠️ R4 离线兜底 — 未通过
  问题：fetch 调用未包裹 try/catch，无 localStorage fallback
  已自动修复：在 loadItems() 函数中添加 fallback 逻辑
  请确认修复后重新校验
```
