---
name: java-null
description: 写、改、审 Java（.java）的判空、取默认值、属性/Map 安全访问时套用。默认用 java.util.Objects / java.util.Optional，避免裸 == null / != null 三元 null 判断（例外见正文）。任何 .java 里的 null 处理都触发，即使用户没提规范。
---

# Java null 处理

裸三元判空（`x == null ? null : x.foo()`）噪声大、易漏 null。JDK 自带的 `Objects` / `Optional` 是标准做法，语义清晰且 null 安全。

## 对照表

| 场景 | 反模式 | 推荐 |
|---|---|---|
| 判空 | `x == null` / `x != null` | `Objects.isNull(x)` / `Objects.nonNull(x)` |
| 取默认值 | `x != null ? x : def` | `Objects.requireNonNullElse(x, def)` |
| 取默认值（延迟计算） | `x != null ? x : expensive()` | `Objects.requireNonNullElseGet(x, () -> expensive())` |
| 安全取属性 | `x == null ? null : x.foo()` | `Optional.ofNullable(x).map(X::foo).orElse(null)` |
| 安全取属性带默认 | `x == null ? def : x.foo()` | `Optional.ofNullable(x).map(X::foo).orElse(def)` |
| 安全 Map 查询 | `k == null ? null : map.get(k)` | `Optional.ofNullable(k).map(map::get).orElse(null)` |
| 相等比较 | `a != null && a.equals(b)` | `Objects.equals(a, b)` |

> Map 查询那行尤其注意 `ConcurrentHashMap`：`CHM.get(null)` 会直接抛 NPE，所以「key 可能为 null」时 `Optional.ofNullable(k).map(map::get)` 这层保护不能丢。

> 「安全取属性」那两行注意 `map` 对 null 返回值的处理：`x.foo()` 返回 null 时，`Optional.ofNullable(x).map(X::foo)` 会把它当成 empty（`map` 对 null 返回值返回 `Optional.empty()`），链路到此截断——结果仍是 null，但「foo 不存在」和「foo 返回 null」被合并了。多数场景无碍；若后续链路依赖这个区分，改用局部变量显式判空。

## 例外（保留三元 / if，不为工具而工具，可读性永远第一）

- 业务分支选择（如「有 groupPath → 组授权，无 → 用户授权」），三元表达的是逻辑分叉而非判空取值，保留
- `Optional` 链应只塞入表达式Lambda（Expression Lambda）。如果塞入代码块Lambda（Block Lambda）则会牺牲可读性。如果必须使用代码块Lambda，则应放弃硬套 Optional ，回退 if-else + `Objects.isNull(x)` / `Objects.nonNull(x)` 判空
- 嵌套三级回退（`a!=null?a:(b!=null?b:c)`）：`requireNonNullElseGet` + lambda 嵌套 `requireNonNullElse` 两层下来可读性未必更好，优先 `if` + 局部变量逐层赋值
- 框架适配 / 反射工具层（如 `ClassPathResourceUtils`）可豁免，避免对底层工具做风格改造引入风险
- Stream / Optional 链路内部的局部判断、record 构造里连续同源字段访问，按可读性取舍
