---
name: java-string-utils
description: 【仅当项目已依赖 commons-lang3（能 import org.apache.commons.lang3.StringUtils）时才触发】字符串判空一律用 StringUtils.isBlank/isNotBlank/isEmpty/isNotEmpty（null 安全）替换裸 `s == null || s.isBlank()` 双目，并保持原 isBlank/isEmpty 语义不混用。项目没装这个依赖就不触发，也不要为此新增依赖。
---

# Java 字符串判空（commons-lang3）

> 本 skill 仅在项目已经把 `commons-lang3` 作为依赖时适用。先确认能 `import org.apache.commons.lang3.StringUtils`；不能就别套用、也别为这个加依赖——退回 `s == null || s.isBlank()` 即可。

`StringUtils.isBlank/isNotBlank/isEmpty/isNotEmpty` 都是 null 安全的，省掉 `s == null || s.isBlank()` 这种裸双目 boilerplate。

## 替换

以下均针对 String（`String.isEmpty` 与 `Collection.isEmpty` 同名，故标 String 与下文「不改集合」区分）：

- `s == null || s.isBlank()` → `StringUtils.isBlank(s)`
- `s != null && !s.isBlank()` → `StringUtils.isNotBlank(s)`
- `s == null || s.isEmpty()` → `StringUtils.isEmpty(s)`
- `s != null && !s.isEmpty()` → `StringUtils.isNotEmpty(s)`

## 保持原语义（关键）

原来用 `isBlank`（空白算空）的对应 `isBlank/isNotBlank`，原来用 `isEmpty` 的对应 `isEmpty/isNotEmpty`——**不要混用**：`isNotEmpty` 不查空白，和 `isBlank` 混用会悄悄改变校验松紧（空格串突然算「非空」）。

## 不改

- 集合（List/Set/Map）的 `.isEmpty()`（那是集合判空，不是字符串）
- 确定非 null 的单目 `.isEmpty()`（如 `substring` 的结果）
