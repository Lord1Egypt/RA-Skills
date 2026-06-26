# Patchable Markdown Format (PMF v1)

PMF 是保留思源块 ID 的 Markdown 格式，用于精确文档编辑。

## 格式结构

### 文档标记（第一行，必需）

```
%% @siyuan:doc id=20260119203720-12nweia hpath="/数据构建/数据分析" view=patchable pmf=v1 %%
```

### 块标记（每个块一个）

```
%% @siyuan:block id=20260121165142-nzdyfe0 type=t parent=20260119203720-12nweia %%
| 列1 | 列2 |
|------|------|
| 数据 | 数据 |
```

| 属性 | 必需 | 说明 |
|------|------|------|
| `id` | 是 | 块 ID，格式 `YYYYMMDDHHmmss-xxxxxxx` |
| `type` | 是 | 块类型：`h`标题 `p`段落 `l`列表 `c`代码 `t`表格 `m`公式 `b`引述 `s`超级块 |
| `subType` | 否 | `h1`-`h6`（标题）、`u`/`t`/`o`（列表） |
| `parent` | 否 | 父块 ID（省略则父块为文档根） |

---

## 安全操作 vs 危险操作

### 安全：仅修改已有块内容（推荐）

**只改 markdown 内容，不增删块。** 这是最可靠的用法。

```
%% @siyuan:doc id=20260119203720-12nweia hpath="/文档" view=patchable pmf=v1 %%

%% @siyuan:block id=20260121165142-nzdyfe0 type=p parent=20260119203720-12nweia %%
这是修改后的段落内容

%% @siyuan:block id=20260121165142-abc1234 type=h subType=h2 parent=20260119203720-12nweia %%
## 修改后的标题
```

### 安全：删除块

从 PMF 中移除块标记及其内容即可。

### 安全：重排已有块

改变块标记的顺序即可。

### 插入新块（可用）

apply-patch 支持插入新块。建议使用唯一临时 ID（如 `tmp-001`）并确保同一 PMF 内不重复。

注意：
- PMF 必须完整（缺失块会被视为删除）
- `partial=true` 的分页/章节 PMF 会被拒绝

---

## 正确的编辑策略

### 策略 1：仅修改内容（apply-patch 安全场景）

适用于：改文字、改表格数据、改标题、重排块顺序

```bash
# 1. 导出
node index.js open-doc "docID" patchable --full | tee /tmp/doc.pmf

# 2. 编辑 /tmp/doc.pmf —— 只改 markdown 内容，保留所有块 ID 注释不变

# 3. 执行
cat /tmp/doc.pmf | SIYUAN_ENABLE_WRITE=true node index.js apply-patch "docID"
```

### 策略 2：需要增加新内容（文末/父块末尾追加，用 append-block）

适用于：添加段落、标题、表格等新块

```bash
# 1. 先读取文档（满足读围栏）
node index.js open-doc "docID" readable

# 2. 追加内容到文档末尾（parentID = 文档ID）
printf '%s\n' '## 新标题' | SIYUAN_ENABLE_WRITE=true node index.js append-block "docID"
printf '%s\n' '新段落内容' | SIYUAN_ENABLE_WRITE=true node index.js append-block "docID"

# 3. 或追加到特定块下
printf '%s\n' '子内容' | SIYUAN_ENABLE_WRITE=true node index.js append-block "某个块ID"
```

### 策略 2.5：需要在指定块前/后插入（用 insert-block）

适用于：在文档开头插入导读、在两个现有块之间插入新段落

```bash
# 1. 先读取文档（满足读围栏）
node index.js open-doc "docID" readable

# 2. 在目标块前插入
printf '%s\n' '## 导读' | SIYUAN_ENABLE_WRITE=true node index.js insert-block --before "目标块ID"

# 3. 或在目标块后插入
printf '%s\n' '补充说明' | SIYUAN_ENABLE_WRITE=true node index.js insert-block --after "目标块ID"
```

### 策略 3：需要替换某个章节（用 replace-section）

适用于：用全新内容替换某个标题下的所有子块

```bash
# 1. 先读取文档，找到要替换的标题块 ID
node index.js open-doc "docID" patchable

# 2. 替换标题下的所有内容
printf '%s\n' '新的段落内容' | SIYUAN_ENABLE_WRITE=true node index.js replace-section "标题块ID"
```

### 策略 4：需要重构整个文档（先清空再逐步追加）

适用于：把 1 个表格拆成多个、整体重排文档结构

```bash
# 1. 读取并记录原始内容
node index.js open-doc "docID" readable

# 2. 清空标题下内容（如果有标题）或逐个删除旧块
SIYUAN_ENABLE_WRITE=true node index.js replace-section "标题块ID" --clear
# 3. 逐步追加新内容
printf '%s\n' '## 概览' | SIYUAN_ENABLE_WRITE=true node index.js append-block "docID"
printf '%s\n' '|列1|列2|' '|---|---|' '|数据|数据|' | SIYUAN_ENABLE_WRITE=true node index.js append-block "docID"
printf '%s\n' '## 详情' | SIYUAN_ENABLE_WRITE=true node index.js append-block "docID"
```

**注意：** 每次 append-block / insert-block 都是独立的 API 调用，不需要重新 open-doc（每次写入后版本自动刷新，支持连续写入）。写入内容统一必须通过 stdin（printf pipe）传入，避免 shell 展开破坏公式。

---

## 常见错误及处理

| 错误 | 原因 | 处理方式 |
|------|------|---------|
| `invalid ID argument` | 块 ID 不存在或格式错误（含手工编辑 PMF 写错） | 重新导出完整 PMF，修正 block ID 后再提交 |
| `PMF 文档ID不匹配` | PMF 中的 doc id 与目标文档不一致 | 检查文档 ID |
| `重复 block id` | PMF 中有重复的块 ID | 确保每个块 ID 唯一 |
| 文档被清空 | 提交了不完整 PMF，缺失块被当作删除 | 仅基于 `open-doc ... patchable --full` 导出的完整 PMF 编辑 |
| 写入围栏报错 | 没有先 open-doc / open-section | 先执行 `open-doc "docID" readable`（或针对章节用 `open-section`） |

---

## 总结：什么时候用什么

| 场景 | 方法 | 安全性 |
|------|------|--------|
| 修改已有块内容 | apply-patch（update） | 安全 |
| 重排已有块 | apply-patch（仅 reorder） | 安全 |
| 删除块 | apply-patch（delete） | 安全 |
| 追加新内容 | append-block | 安全 |
| 替换章节 | replace-section | 安全 |
| 删除 + 插入新块 | apply-patch（delete + insert）或 replace-section/append-block | 需要完整 PMF，避免 partial |
