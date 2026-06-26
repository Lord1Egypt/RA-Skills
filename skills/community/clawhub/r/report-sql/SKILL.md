# report-sql

> 本技能由老板亲授，定义 report-service 的 SQL 模板协议与变量规范。

## Variables

report-service 变量遵循唯一、精确、零容错原则：

### ✅ 合法语法
```
#@option.where.<field>#
```

### 🔑 当前支持字段
| 字段名 | 类型 | 示例值 | 典型 SQL 用法 |
|--------|------|--------|----------------|
| `name` | string | `"张三"` | `WHERE s.name = #@option.where.name#` |
| `status_list` | array | `["draft","published"]` | `WHERE b.status IN (#@option.where.status_list#)` |
| `start_date` | date | `"2026-03-01"` | `AND u.created_at >= #@option.where.start_date#` |
| `limit` | number | `100` | `LIMIT #@option.where.limit#` |

### ⚠️ 严禁写法（运行时直接失败）
- `#@name#`, `#name#`, `@name@` → 无命名空间；
- `#@option.name#`（缺 `.where`）→ 路径错误；
- `s.name`, `b.status` → 别名+字段，非变量；
- 变量内含空格、换行、注释 → 破坏字面匹配。

### 📌 拼接原则
变量只提供值，表别名由 `FROM` 子句决定：
- 若 `FROM sale s` → 写 `s.name = #@option.where.name#`；
- 若 `FROM blog b` → 写 `b.title LIKE CONCAT('%', #@option.where.name#, '%')`；
- 变量本身**永远不带 `s.` 或 `b.` 前缀**。

### ✅ 新增：`${...}` 块级变量语法（2026-03-23 补充）

用于包裹条件片段，典型形式：
```
${
 AND `corpId` = '#@option.where.corpId#' }
```
```
${
 AND `creatorId` = '#@option.where.creatorId#' }
```

#### 规则说明
- `${...}` 是**完整 SQL 片段容器**，内部可含任意合法 SQL（含换行、缩进、注释）；
- `${...}` 内部仍使用 `#@option.where.xxx#` 注入具体值；
- `${...}` 块整体**按需渲染**：若块内所有 `#@...#` 均有值，则整个块保留；若任一 `#@...#` 为空/未传，则整块被剔除（空安全）；
- 不支持嵌套 `${...}`；
- `${...}` 外不可加额外空格或符号（如 ` ${...} ` 或 `AND ${...}` —— `AND` 必须写在块内）。

### ✅ 新增：模糊匹配常用块（2026-03-23 补充）

用于 `LIKE` 模糊查询，典型形式：
```
${
 AND `name` LIKE '%#@option.where.name#%' }
```

#### 使用说明
- `%...%` 包裹确保前后通配；
- 该块同样遵循 `${...}` 空安全规则：若 `#@option.where.name#` 未传值，整块自动剔除；
- 如需左匹配（`xxx%`）或右匹配（`%xxx`），请显式写出对应 `%` 符号。

### ✅ 新增：时间范围查询常用块（2026-03-23 补充）

用于 `createdAt` 等时间字段的开闭区间查询，典型形式：
```
${
 AND `createdAt` >= '#@option.where.createdAt[0]#'
 AND `createdAt` < '#@option.where.createdAt[1]#' }
```

#### 使用说明
- `[0]` / `[1]` 表示数组索引，要求传入长度为 2 的时间字符串数组（如 `["2026-03-01 00:00:00", "2026-03-02 00:00:00"]`）；
- 语义为 `>= start AND < end`，实现标准左闭右开区间；
- 该块同样遵循 `${...}` 空安全：任一索引值缺失 → 整块剔除。

### ✅ 新增：多值循环块语法（2026-03-23 补充）

用于生成 `IN` 或多条件 `OR` 逻辑，典型形式：
```
$@option.where.state ->
 OR {
 AND [state = '#@item#'] }
```

#### 使用说明
- `$@option.where.state ->` 声明待遍历的数组变量（如 `['draft','published']`）；
- `#@item#` 在循环中自动替换为当前数组元素；
- `OR { ... }` 是协议级语法糖：引擎会将每个 `{ ... }` 块内容作为原子条件，用 `OR` 连接，并**自动包裹外层括号 `(... OR ...)`**，最终与块外固定条件组合（如 `AND (...)`），确保 SQL 语义清晰、结构合法；
- 此机制保证生成的 SQL 永远合法（避免 `AND`/`OR` 优先级错误）；
- 该语法天然防 SQL 注入（值经模板引擎安全转义）；
- 若 `@option.where.state` 为空数组或未传，整段被剔除。

#### 🔁 进阶说明：括号语义与等价性
`$@... -> OR { ... }` 生成的 SQL **自动为每个 `{ ... }` 块添加括号**，例如：
```text
$@option.where.types ->
 OR {
 AND state = 'finished' AND [type = '#@item#'] }
```
解析为：
```sql
( state = 'finished' AND type = 'sale' )
OR ( state = 'finished' AND type = 'refund' )
```

此形式在逻辑上 **完全等价于**：
```sql
state = 'finished' AND type IN ('sale', 'refund')
```
**或**：
```sql
AND state = 'finished' AND ( (type = 'sale') OR (type = 'refund') )
```

✅ 优势：括号强制分组，杜绝 `AND`/`OR` 优先级陷阱；
✅ 优势：可轻松扩展为多字段组合（如 `AND [type = '#@item#'] AND [status = '#@item2#']`）；
⚠️ 注意：若需外层统一 `AND`（如所有 `OR` 结果再 `AND` 一个固定条件），请将该固定条件写在 `OR { ... }` 块**之外**（如 `WHERE active = 1 AND (...)`），而非塞进块内。

#### 🌐 高阶用法：对象数组遍历（2026-03-23 补充）
`$@... -> OR { ... }` 支持遍历**对象数组**，并用点语法 `#@item.xxx#` 访问嵌套字段。

**典型形式**：
```text
$@searchOrder -> OR { AND [id = '#@item.corpId#'] }
```

**解析逻辑**：
- 若 `searchOrder = [{"id":1,"corpId":"wx123"},{"id":2,"corpId":"wx456"}]`，
- 则 `#@item.corpId#` 分别取值 `"wx123"` 和 `"wx456"`，
- 最终生成：
```sql
( id = 'wx123' ) OR ( id = 'wx456' )
```

✅ 优势：直接复用上一步查询结果，实现“查完即用”的流水线；
⚠️ 注意：`#@item.xxx#` 中的 `xxx` 必须是对象存在的字段名，否则该元素被跳过（空安全）。

### ✅ 新增：复杂 EXISTS 子查询块（2026-03-23 补充）

用于封装高复用业务逻辑（如分发状态判定），典型形式：
```
${
 AND NOT (
 EXISTS(
 SELECT #@option.where.distributeYes# FROM wq.`joblist` j WHERE j.`JobId` = b.id AND j.active = 1 AND (j.`outUserID` = '' OR j.outUserID IS NULL)) OR (NOT EXISTS(SELECT 1 FROM wq.`joblist` j WHERE j.`JobId` = b.id AND j.active = 1 AND (j.`outUserID` = '' OR j.outUserID IS NULL)) and (b.outUserID is null or b.outUserID = '')))}
```
```
${ AND (EXISTS(SELECT #@option.where.distributeNo# FROM wq.`joblist` j WHERE j.`JobId` = b.id AND j.active = 1 AND (j.`outUserID` = '' OR j.outUserID IS NULL)) OR (NOT EXISTS(SELECT 1 FROM wq.`joblist` j WHERE j.`JobId` = b.id AND j.active = 1 AND (j.`outUserID` = '' OR j.outUserID IS NULL)) and (b.outUserID is null or b.outUserID = '')))}
```

#### 使用说明
- 此类块将**复杂 EXISTS 逻辑固化为可插拔条件单元**，模板中只需声明变量，无需重复书写长 SQL；
- `#@option.where.distributeYes#` / `#@option.where.distributeNo#` 仍为原子值注入（如 `1` 或 `'true'`），子查询结构由块体保证；
- 同样遵循 `${...}` 空安全：任一 `#@...#` 缺失 → 整块剔除；
- 表别名（`j.`/`b.`）由块内 SQL 自行定义，与外部 `FROM` 无关。

### ✅ 新增：变量使用场景 — 块级边界原则（2026-03-23 补充）

`${...}` 块不是“值占位符”，而是**自洽 SQL 片段容器**。其边界必须包裹完整语法单元。

#### ❌ 危险写法（绝对禁止）
```sql
-- 错！and 在块外 → 空时生成语法错误：`WHERE active = 1 and `
select id, parent, name from department where active = 1 and ${ corpId = '#@option.where.corpId#' }
```

#### ✅ 正确写法（必须）
```sql
-- 对！and 在块内 → 空时整块剔除，SQL 依然合法
select id, parent, name from department where active = 1 ${ and corpId = '#@option.where.corpId#' }
```

#### 📌 核心原则
- 所有逻辑词（`AND`/`OR`/`IN`/`BETWEEN` 等）必须写在 `${...}` 块内；
- 块内 SQL 必须是独立、可执行的语法片段（能单独 `EXPLAIN`）；
- 块外只允许固定 SQL（如 `SELECT ... FROM ... WHERE`），绝不拼接动态逻辑。

> 这是 `report-service` 空安全的最后防线 —— 宁可多写一个 `and`，不可少包一行 SQL。

## Transform

`report-service` 支持链式数据变换操作，用于处理 SQL 查询结果，支持初始化、条件赋值、字段映射、关联补全与结果组装。

### 变换语法说明

所有变换以 JSON 数组形式声明，每个对象为一个操作步骤，按顺序执行。

| 字段 | 类型 | 说明 |
|------|------|------|
| `method` | string | 操作类型（`setData` / `copyObject` / `leftJoin`） |
| `target` | string | 目标变量名（如 `@result`, `@rows`），以 `@` 开头 |
| `source` | any | 源数据（可为字面值、数组、对象、或另一变量如 `@deptList`） |
| `precondition` | string | 执行前置条件（如 `#@deptList#`，当该变量有值时才执行此步） |
| `attributes` / `fields` | array | 字段映射规则（`from` → `to`，可设 `default`） |
| `targetKey` / `sourceKey` | string | 关联键名（用于 `leftJoin`） |

---

### 示例 1：结果初始化与条件赋值
```json
[
 {
  "method": "setData",
  "target": "@result",
  "source": []
 },
 {
  "method": "setData",
  "target": "@result",
  "source": "@deptList",
  "precondition": "#@deptList#"
 }
]
```
- **作用**：先初始化 `@result` 为空数组；若 `@deptList` 存在，则用其覆盖 `@result`。
- **关键**：`precondition` 实现空安全分支。

> 💡 **权威说明（老板亲授）**：
> `precondition: "#@deptList#"` 的语义是——**判断上一步产生的中间变量 `@deptList` 是否存在且非空**（非 `null` / `undefined` / `[]` / `{}`）；
> 仅当该条件为真时，第二步 `setData` 才执行；
> 第一步 `source: []` 确保 `@result` 始终有默认值，避免未定义状态。

---

### 示例 2：对象字段提取与结构重组
```json
[
 {
  "method": "setData",
  "target": "@result",
  "source": {}
 },
 {
  "method": "copyObject",
  "target": "@result",
  "source": "@countOrder[0]",
  "attributes": [
    {
     "from": "totalCount",
     "to": "count",
     "default": 0
    },
    {
     "from": "totalMoney",
     "to": "money",
     "default": 0
    }
  ]
 }
]
```
- **作用**：先初始化 `@result` 为空对象 `{}`；再从 `@countOrder[0]`（数组首项，必须是对象）中提取 `totalCount` → `count`、`totalMoney` → `money`，缺失时用 `default` 填充。
- **关键**：`copyObject` 支持字段级映射、类型安全兜底，且目标必须是对象（非数组）。

---

### 示例 3：多源关联与标准响应组装
```json
[
 {
  "method": "setData",
  "target": "@rows",
  "source": []
 },
 {
  "method": "setData",
  "target": "@rows",
  "source": "@searchOrder",
  "precondition": "#@searchOrder#"
 },
 {
  "method": "leftJoin",
  "target": "@rows",
  "source": "@searchCorp",
  "targetKey": "corpId",
  "sourceKey": "id",
  "fields": [
    {
     "from": "name",
     "to": "corpName",
     "default": ""
    },
    {
     "from": "nickname",
     "to": "corpNickname",
     "default": ""
    }
  ]
 },
 {
  "method": "copyObject",
  "target": "@result",
  "source": "@rows",
  "to": "rows",
  "default": []
 }
]
```
- **作用**：
  1. 初始化 `@rows` 为空数组；
  2. 若 `@searchOrder` 存在，则赋值；
  3. 用 `@searchCorp` 左关联 `@rows`（`corpId` ↔ `id`），补全 `corpName`/`corpNickname`；
  4. 将最终 `@rows` 数组整体写入 `@result.rows`（非覆盖 `@result`）。
- **关键**：`leftJoin` 保障跨源数据一致性，`copyObject` 的 `to: "rows"` 实现标准响应结构（`{ "rows": [...] }`）。