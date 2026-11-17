# 状态流转规范

## 全局状态枚举

所有记录类别共用以下 5 个状态值（严格封闭，不可自行扩展）：

| 值 | 含义 | 完成态 |
|----|------|--------|
| `open` | 新建/未开始 | ❌ |
| `pending` | 等待中（待评审/待分配/待确认） | ❌ |
| `in_progress` | 进行中/处理中 | ❌ |
| `done` | 已完成/已交付/已修复/已验证 | ✅ 唯一 |
| `deferred` | 已延期/已挂起 | ❌ |

### 原文到状态值的归一化映射

创建/更新记录时，遇到以下表述应归一化为对应状态值：

| 原文表述 | 归一化状态 |
|---------|-----------|
| `已完成`、`✅ 已完成`、`已交付`、`已上线`、`已归档` | `done` |
| `fixed`、`✅ 已修复`、`✅ 已修复（线上环境）`、`已修复` | `done` |
| `verified`、`验证通过` | `done` |
| `待评审`、`待分配`、`待确认`、`已建档` | `pending` |
| `进行中`、`处理中`、`调查中`、`已分配`、`已分配，XXX调查中`、`转交XXX排查` | `in_progress` |
| `open`、`未开始`、`待处理`、`待启动`、`新建` | `open` |
| `已延期`、`已挂起`、`搁置` | `deferred` |

---

## 12 类状态流转

### 1. badcase — 缺陷案例

```
open → in_progress → done
  ↓
deferred（挂起，可重新激活为 open/in_progress）
```

**典型流转**：新发现 → `open`，分配调查中 → `in_progress`，修复验证通过 → `done`。

### 2. task — 任务提醒/待办

```
open → in_progress → done
  ↓
deferred（延期）
```

可跳过 `in_progress` 直接 `open → done`（快速完成的小任务）。

### 3. plan — 计划/规划

```
open → pending → in_progress → done
  ↓
deferred
```

### 4. requirement — 需求文档

```
open → pending → in_progress → done
  ↓
deferred
```

### 5. meeting — 会议记录

```
open → done
```

会议记录是事件性文档，创建即归档。`open` 表示"记录中/草稿"，`done` 表示"已确认归档"。

### 6. report — 分析/复盘/总结

```
open → in_progress → done
```

可跳过 `in_progress` 直接 `open → done`。

### 7. sop — 标准流程

```
open → pending → done
```

### 8. weekly — 周报

```
open → done
```

### 9. monthly — 月报

```
open → done
```

### 10. quarterly — 季报

```
open → done
```

### 11. yearly — 年报

```
open → done
```

### 12. admin — 行政/运营事务

```
open → in_progress → done
  ↓
deferred
```

可跳过 `in_progress` 直接 `open → done`。

### 13. memo — 工作备忘录

```
open → done
```

备忘录是轻量记录文档，创建即归档。`open` 表示"编辑中/草稿"，`done` 表示"已确认归档"。

---

## 各类别可用状态汇总

| 类别 | open | pending | in_progress | done | deferred |
|------|------|---------|-------------|------|----------|
| badcase | ✅ | ❌ | ✅ | ✅ | ✅ |
| task | ✅ | ❌ | ✅ | ✅ | ✅ |
| plan | ✅ | ✅ | ✅ | ✅ | ✅ |
| requirement | ✅ | ✅ | ✅ | ✅ | ✅ |
| meeting | ✅ | ❌ | ❌ | ✅ | ❌ |
| report | ✅ | ❌ | ✅ | ✅ | ❌ |
| sop | ✅ | ✅ | ❌ | ✅ | ❌ |
| weekly | ✅ | ❌ | ❌ | ✅ | ❌ |
| monthly | ✅ | ❌ | ❌ | ✅ | ❌ |
| quarterly | ✅ | ❌ | ❌ | ✅ | ❌ |
| yearly | ✅ | ❌ | ❌ | ✅ | ❌ |
| admin | ✅ | ❌ | ✅ | ✅ | ✅ |
| memo | ✅ | ❌ | ❌ | ✅ | ❌ |

---

## 状态流转规则

1. **状态不可逆原则**：`done` 之后不允许退回其他状态。如需修改，创建新版本记录。
2. **deferred 可激活**：`deferred` 可重新变为 `open` 或 `in_progress`。
3. **初始状态**：新记录默认 `open`，除非明确说明已完成可直设 `done`。
4. **唯一完成态**：查询"未完成"只需 `status != 'done'`，不用关心中间态。
5. **合法流转校验**：状态更新时必须检查当前状态是否允许流转到目标状态。

## 合法流转矩阵

| 当前状态 → 目标状态 | open | pending | in_progress | done | deferred |
|---------------------|------|---------|-------------|------|----------|
| open | ❌ | ✅ | ✅ | ✅ | ✅ |
| pending | ❌ | ❌ | ✅ | ✅ | ✅ |
| in_progress | ❌ | ✅ | ❌ | ✅ | ✅ |
| done | ❌ | ❌ | ❌ | ❌ | ❌ |
| deferred | ✅ | ❌ | ✅ | ✅ | ❌ |
