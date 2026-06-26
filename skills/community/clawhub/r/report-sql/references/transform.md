# report-service 数据变换规则（Transform）

> 本文件定义 `report-service` 中用于处理查询结果的数据变换操作，支持链式执行、条件分支、字段映射与关联补全。

## 变换语法说明

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

## 常见变换示例

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

---

### 示例 2：对象字段提取与重命名
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
- **作用**：从 `@countOrder[0]` 对象中提取 `totalCount` → `count`、`totalMoney` → `money`，缺失时用 `default` 填充。
- **关键**：`copyObject` 支持字段级映射与兜底。

---

### 示例 3：多步关联与结果组装
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
  1. 初始化 `@rows`；
  2. 若 `@searchOrder` 存在，则赋值；
  3. 用 `@searchCorp` 左关联 `@rows`（`corpId` ↔ `id`），补全 `corpName`/`corpNickname`；
  4. 将最终 `@rows` 组装为 `@result.rows`。
- **关键**：`leftJoin` 实现跨数据源关联，`copyObject` 支持嵌套目标（`to: "rows"`）。

---

## ⚠️ 使用原则
- 所有 `@xxx` 变量必须由上游 SQL 查询或前序变换生成；
- `precondition` 中的 `#@...#` 必须是 `option.where.*` 变量，用于控制流程分支；
- `leftJoin` 要求 `targetKey` 和 `sourceKey` 字段类型一致，否则关联失败；
- `default` 值用于字段缺失时兜底，避免 `null` 传播。