---
name: siyuan-notes-skill
description: "思源笔记工具——搜索、阅读、编辑、组织用户的笔记。Use when user says: 搜索笔记、查找文档、打开文档、阅读笔记、编辑笔记、创建文档、修改块、思源笔记、SiYuan、整理文档、管理标签、Daily Note、反向链接、最近修改、PMF补丁、SQL查询blocks。不要用于与思源笔记无关的通用编程或问答任务。"
allowed-tools: "Bash"
license: MIT
compatibility: "Requires Node.js 18+. Needs a running SiYuan kernel with API access. Claude Code only."
metadata:
  author: fanxing-6
  version: 1.0.5
---

## 开始前（可选）：版本检查

如需确认是否为最新版本，请运行：

```bash
node index.js version-check
```

- 若远程版本获取失败：不会阻塞任务
- 若检测到版本落后：会提示但不阻塞

## 编辑策略选择（最重要）

根据用户意图选择正确的编辑方式，**选错会导致数据丢失**：

| 用户想要 | 正确做法 | 错误做法 |
|---------|---------|---------|
| 修改单个块内容 | `update-block`（最高效） | ~~apply-patch 整个文档~~ |
| 删除单个块 | `delete-block`（最高效） | ~~apply-patch 整个文档~~ |
| 批量修改已有内容 | `apply-patch`（update/delete/reorder/insert） | |
| 批量删除/重排块 | `apply-patch`（delete/reorder） | |
| 添加新内容 | `append-block`（简单稳妥）或 `apply-patch` insert（批量场景） | |
| 在指定位置插入新块 | `insert-block --before/--after`（首选）或 `apply-patch` insert | |
| 替换章节内容 | `replace-section` | ~~apply-patch 删除+插入~~ |
| 重构文档（如拆表格） | `replace-section --clear` + `append-block` 逐步重建 | ~~apply-patch 删除旧块+插入新块~~ |
| 跨章节分散修改多个块 | 编写单个 JS 脚本，循环 `openDocument` → `updateBlock`（同一进程内版本自动刷新） | ~~并行 Bash 调用 update-block（会版本冲突）~~ |

## Intent Decision Tree

```
用户想要…
├─ 查找/搜索内容 ──────→ search / search-md / tag / attr / bookmarks
├─ 在文档内搜索 ──────→ search-in-doc {docID} {关键词}
├─ 阅读文档 ──────────→ open-doc {ID} readable（超长文档自动截断，输出大纲导航）
├─ 阅读章节 ──────────→ open-section {标题块ID} readable（精确读取一个标题的内容）
├─ 浏览最近动态 ──────→ recent / tasks / daily
├─ 了解文档结构 ──────→ docs / notebooks / headings / blocks / doc-tree / doc-tree-id / doc-children
├─ 查看引用关系 ──────→ backlinks / unreferenced
├─ 修改单个块 ────────→ open-doc readable → update-block {块ID} {内容}（最高效）
├─ 删除单个块 ────────→ open-doc readable → delete-block {块ID}（最高效）
├─ 批量修改已有内容 ──→ open-doc patchable → 编辑内容 → apply-patch（支持 update/delete/reorder/insert）
├─ 创建新文档 ────────→ create-doc（指定笔记本、标题、可选初始内容）
├─ 重命名文档 ────────→ rename-doc（只需文档 ID 和新标题）
├─ 添加新内容 ────────→ open-doc readable → append-block（逐个追加）
├─ 指定位置插入 ──────→ open-doc readable → insert-block --before/--after（按锚点插入）
├─ 替换章节 ──────────→ open-doc patchable → replace-section
├─ 重构文档结构 ──────→ open-doc readable → replace-section --clear → append-block 逐步重建
├─ 组织文档层级 ──────→ subdoc-analyze-move → move-docs-by-id
├─ 跨章节分散修改 ────→ 编写单个 JS 脚本，循环 openDocument → updateBlock（见模式8）
├─ SQL 高级查询 ──────→ node -e + executeSiyuanQuery()
└─ 检查连接 ──────────→ check / version
```

## Write Safety Protocol

**写入前通常需要完成这 2 步（`create-doc` / `rename-doc` 例外）：**

```bash
# 步骤 1：读取文档或章节（标记为"已读"，同时记录文档版本快照）
node index.js open-doc "docID" readable
# 或：node index.js open-section "headingBlockID" readable

# 步骤 2：环境变量启用写入
SIYUAN_ENABLE_WRITE=true node index.js append-block "docID" "内容"
```

- `open-doc` 和 `open-section` 计为"已读"；`headings`/`blocks`/`doc-tree` 等不算
- **核心保护：版本检查（乐观锁）**——写入前对比文档 `updated` 时间戳，若文档在读取后被其他端修改过则拒绝写入
- 连续写入安全：每次写入成功后自动刷新版本号，`open-doc → write → write → write` 不会误报冲突
- **⚠️ 版本刷新仅在同一 node 进程内生效**。若用多个独立 Bash 命令（如 Claude Code 并行调用），每次写入会改变文档版本，后续的独立命令会版本冲突。**解决方案**：对同一文档的多次写入必须串行执行，不能并行
- 读标记持久化存储在磁盘缓存中，跨 CLI 调用有效（同一台机器上的不同终端共享读标记）
- 读标记超过 3600 秒自动过期（仅作为缓存清理，版本检查才是真正的安全机制）
- 例外：`create-doc` 与 `rename-doc` 不要求先 `open-doc`


## Core Commands Quick Reference

所有命令：`node index.js {command} [args]`

### 读取

| Command | Signature | Description |
|---------|-----------|-------------|
| `search` | `{keyword} [limit] [type]` | 搜索笔记（type: p/h/l/c/d…） |
| `search-md` | `{keyword} [limit] [type]` | 搜索并输出 Markdown 结果页 |
| `open-doc` | `{docID} [readable\|patchable] [--full] [--cursor {块ID}] [--limit-chars {N}] [--limit-blocks {N}]` | 打开文档（默认 readable）。超长文档自动截断/分页，`--full` 跳过截断输出全量。**副作用：标记已读** |
| `open-section` | `{标题块ID} [readable\|patchable]` | 读取标题下的章节内容。**副作用：标记文档已读** |
| `search-in-doc` | `{docID} {关键词} [数量]` | 在指定文档内搜索匹配的块 |
| `notebooks` | | 列出笔记本 |
| `docs` | `[notebookID] [limit]` | 列出文档（含文档 ID，默认 200） |
| `headings` | `{docID} [level]` | 文档标题（level 格式：`h1`/`h2`/…/`h6`，不是数字） |
| `blocks` | `{docID} [type]` | 文档子块（含块 ID，可用于写入） |
| `doc-children` | `{notebookID} [path]` | 子文档列表 |
| `doc-tree` | `{notebookID} [path] [depth]` | 子文档树（默认深度 4） |
| `doc-tree-id` | `{docID} [depth]` | 以文档 ID 展示子文档树 |
| `tag` | `{tagName}` | 按标签搜索 |
| `backlinks` | `{blockID}` | 反向链接 |
| `tasks` | `[status] [days]` | 任务（`[ ]`/`[x]`/`[-]`，默认 7 天） |
| `daily` | `{start} {end}` | Daily Note（YYYYMMDD） |
| `attr` | `{name} [value]` | 按属性查询（自定义属性加 `custom-` 前缀） |
| `bookmarks` | `[name]` | 书签 |
| `random` | `{docID}` | 随机标题 |
| `recent` | `[days] [type]` | 最近修改（默认 7 天） |
| `unreferenced` | `{notebookID}` | 未被引用的文档 |
| `check` | | 连接检查 |
| `version` | | 内核版本 |

### 写入

| Command | Signature | 适用场景 |
|---------|-----------|---------|
| `create-doc` | `{notebookID} {标题}` | 创建新文档（标题即文档名，初始内容仅支持 stdin） |
| `rename-doc` | `{docID} {新标题}` | 重命名文档 |
| `update-block` | `{块ID}` | 更新块内容（Markdown 仅支持 stdin；多块输入自动拆块安全写入） |
| `delete-block` | `{块ID}` | 删除单个块 |
| `append-block` | `{parentID}` | 添加新内容（parentID 可以是文档 ID 或标题块 ID；Markdown 仅支持 stdin） |
| `insert-block` | `{--before 块ID\|--after 块ID\|--parent 块ID}` | 在指定锚点插入内容（前/后/父块下；Markdown 仅支持 stdin） |
| `replace-section` | `{headingID}` 或 `{headingID} --clear` | 替换/清空章节（保留标题块本身；Markdown 仅支持 stdin） |
| `apply-patch` | `{docID}` （PMF 通过 stdin 传入） | **仅限**批量修改/删除/重排已有块（拒绝 partial PMF） |
| `move-docs-by-id` | `{targetID} {sourceIDs}` | 移动文档（需先 open-doc 目标文档**和**所有来源文档） |
| `subdoc-analyze-move` | `{targetID} {sourceIDs} [depth]` | 分析移动计划（只读） |

## Common Patterns

### 1. 搜索并阅读

```bash
node index.js search "项目总结" 5
node index.js open-doc "找到的文档ID" readable
```

### 2. 修改已有块内容（apply-patch 安全用法）

```bash
# 导出完整 PMF（必须 --full；默认 patchable 在长文档会分页并标记 partial=true）
node index.js open-doc "docID" patchable --full | tee /tmp/doc.pmf

# 编辑 /tmp/doc.pmf：只改 markdown 内容，保留所有块 ID 注释不变
# ⚠️ 关键：PMF 必须包含文档的 **所有** 块！缺失的块会被视为删除！
#    正确做法：导出完整 PMF → 只修改目标块的文本 → 提交完整文件
#    错误做法：只写目标块 → 其他块全部丢失

# 执行
cat /tmp/doc.pmf | SIYUAN_ENABLE_WRITE=true node index.js apply-patch "docID"
```

### 3. 添加新内容到文档

```bash
node index.js open-doc "docID" readable                    # 先读
printf '## 新标题' | SIYUAN_ENABLE_WRITE=true node index.js append-block "docID"
printf '段落内容' | SIYUAN_ENABLE_WRITE=true node index.js append-block "docID"
printf '- [ ] 任务' | SIYUAN_ENABLE_WRITE=true node index.js append-block "docID"
```

### 3.5 在指定位置插入内容

```bash
node index.js open-doc "docID" readable
printf '插入在该块之前' | SIYUAN_ENABLE_WRITE=true node index.js insert-block --before "目标块ID"
printf '插入在该块之后' | SIYUAN_ENABLE_WRITE=true node index.js insert-block --after "目标块ID"
```

### 4. 重构文档（如拆分表格为多个）

```bash
# 读取原始内容
node index.js open-doc "docID" readable

# 用 patchable 视图找到要操作的块 ID
node index.js open-doc "docID" patchable

# 方案A：有标题块 → 清空章节再重建
# replace-section 保留标题块本身，只删除标题下的子内容
# 所以新内容不要重复标题（例如标题是 "## 表格" 则直接追加表格数据即可）
SIYUAN_ENABLE_WRITE=true node index.js replace-section "标题块ID" --clear
# 追加到标题块 ID 下 → 新内容会出现在该标题的章节内
printf '### 概览' | SIYUAN_ENABLE_WRITE=true node index.js append-block "标题块ID"
printf '|列1|列2|\n|---|---|\n|数据|数据|' | SIYUAN_ENABLE_WRITE=true node index.js append-block "标题块ID"

# 方案B：没有标题块 → 用 node -e 删除旧块再追加
SIYUAN_ENABLE_WRITE=true node -e "
const s = require('./index.js');
s.deleteBlock('旧块ID').then(function(r) { console.log(JSON.stringify(r)); });
"
printf '新内容' | SIYUAN_ENABLE_WRITE=true node index.js append-block "docID"
```

### 5. 创建新文档

```bash
# 先查笔记本ID
node index.js notebooks

# 创建空文档
SIYUAN_ENABLE_WRITE=true node index.js create-doc "笔记本ID" "文档标题"

# 创建带初始内容的文档（Markdown 仅支持 stdin）
printf '## 第一章\n内容' | SIYUAN_ENABLE_WRITE=true node index.js create-doc "笔记本ID" "文档标题"

# 重命名已有文档
SIYUAN_ENABLE_WRITE=true node index.js rename-doc "文档ID" "新标题"
```

### 6. 修改/删除单个块

```bash
# 修改单个块
node index.js open-doc "文档ID" readable
printf '新内容' | SIYUAN_ENABLE_WRITE=true node index.js update-block "块ID"

# 多行内容同样通过 stdin
printf '## 新标题\n\n段落内容' | SIYUAN_ENABLE_WRITE=true node index.js update-block "块ID"

# 删除单个块
node index.js open-doc "文档ID" readable
SIYUAN_ENABLE_WRITE=true node index.js delete-block "块ID"
```

**注意**: 若传入内容可解析为多个块（例如"段落 + $$公式$$"），`update-block` 会自动执行"首块 update + 后续 insert"，并做写后校验，避免刷新后内容丢失。

### 7. 超长文档处理

```bash
# open-doc 超长文档自动截断/分页，输出大纲和导航提示
node index.js open-doc "超长文档ID" readable
# → 自动截断到 ~15K 字符，附带标题大纲

# 读取特定章节（精确获取标题下内容）
node index.js open-section "标题块ID" readable

# 在文档内搜索关键词（无需读完全文）
node index.js search-in-doc "文档ID" "关键词"

# patchable 视图分页（默认每页 50 块）
node index.js open-doc "文档ID" patchable
# → 分页时 PMF header 含 partial=true next_cursor=xxx

# 翻页
node index.js open-doc "文档ID" patchable --cursor "下一块ID"

# 需要完整 PMF（如整文 apply-patch）→ 用 --full 跳过分页
node index.js open-doc "文档ID" patchable --full | tee /tmp/doc.pmf
# ⚠️ 输出可能很大，注意上下文限制
```

### 8. 跨章节分散修改多个块（单进程批量脚本）

当需要修改同一文档中分散在不同章节的多个块时，**不能**用多个并行 Bash 命令（会版本冲突）。正确做法是编写单个 JS 脚本：

```javascript
// /tmp/batch_edit.js
const s = require('/root/.claude/skills/siyuan-notes-skill/index.js');
async function main() {
  const docId = '文档ID';

  // 辅助函数：刷新版本 + 更新块（同一进程内版本自动刷新）
  async function edit(blockId, markdown) {
    await s.openDocument(docId, 'readable');
    await s.updateBlock(blockId, markdown);
    console.log(`Updated ${blockId}: OK`);
  }

  // 辅助函数：刷新版本 + 在锚点后插入
  async function insertAfter(previousID, markdown) {
    await s.openDocument(docId, 'readable');
    await s.insertBlock(markdown, { previousID });
    console.log(`Inserted after ${previousID}: OK`);
  }

  // 依次执行所有修改（必须串行，不能 Promise.all）
  await edit('块ID1', '新内容1');
  await edit('块ID2', '新内容2');
  await insertAfter('锚点块ID', '插入的新内容');
}
main().catch(e => { console.error(e.message); process.exit(1); });
```

```bash
# 执行
cd /root/.claude/skills/siyuan-notes-skill
SIYUAN_ENABLE_WRITE=true node /tmp/batch_edit.js
```

**关键点**：
- 所有操作在**同一个 node 进程**内串行执行
- 每次写入前 `openDocument` 刷新版本号（进程内版本缓存自动更新）
- JS API 签名：`updateBlock(id, markdown)`、`insertBlock(markdown, { previousID?, nextID?, parentID? })`、`deleteBlock(id)`、`appendMarkdownToBlock(parentID, markdown)`

## 错误恢复

| 错误 | 原因 | 恢复方法 |
|------|------|---------|
| `invalid ID argument` | 块 ID 不存在或格式错误 | 重新导出 `open-doc ... patchable --full`，校验 block ID 后再提交 |
| 文档被清空 | 提交了不完整 PMF，缺失块被当作删除 | 用 `open-doc ... patchable --full` 重新导出完整 PMF 后恢复 |
| 写入围栏报错 | 未先 open-doc/open-section 或读标记过期 | `open-doc "docID" readable`（或 `open-section`）然后重试 |
| 版本冲突报错 | 文档在读取后被其他端修改 | `open-doc "docID" readable` 重新读取最新版本然后重试 |
| PMF 版本冲突 | PMF 导出后文档被修改 | `open-doc "docID" patchable --full` 重新导出后再编辑，输出用 `tee` 保存 |
| partial PMF 被拒绝 | 分页/章节导出的 PMF 不完整 | 改用 `update-block` 编辑单块，或 `open-section` + `replace-section` 编辑章节 |
| 只读模式报错 | 未设置 `SIYUAN_ENABLE_WRITE=true` | 在命令前加 `SIYUAN_ENABLE_WRITE=true` |
| 文档标题为"未命名文档" | `createDocWithMd` 的 path 参数决定标题 | 用 `create-doc` CLI 命令（自动设置标题）或 `rename-doc` 修正 |
| 连接失败 | 思源未运行/端口/Token 错误 | `node index.js check` 验证 |
| search 返回空 | 关键词过短/确实无匹配 | 改用 `search-in-doc` 限定文档范围，或扩大关键词上下文 |
| 并行写入版本冲突 | 多个独立 Bash 命令并行修改同一文档 | 改用单个 JS 脚本串行执行（见模式8），或每次写入前重新 `open-doc` |

## Output Guidance

- 读取命令返回格式化文本 → 直接展示给用户
- `open-doc readable` 返回干净 Markdown → 适合阅读和总结（超长文档自动截断到 ~15K 字符，附带标题大纲）
- `open-doc patchable` 返回 PMF 格式 → 仅用于编辑后 apply-patch（超长文档自动分页，分页 PMF 含 `partial=true`，**不可用于 apply-patch**）
- `open-section` 返回单章节内容 → 适合精确阅读/编辑特定章节
- 写入命令返回 JSON（通常很冗长） → 只提取关键信息（如新文档 ID、成功/失败）展示给用户，不要原样输出全部 JSON
- 公式渲染：行内公式用 `$...$`，独立公式块用 `$$...$$`（思源会渲染为数学块）

## KaTeX Formula Rules (No Silent Rewrite)

**核心原则：写入内容必须与模型输出一致。禁止在写入前/写入中对公式做隐式重写。**

### 必须遵守

- 数学定界符只用两种：行内 `$...$`，独立 `$$...$$`
- 数学模式内禁止再次出现 `$`（例如 `$$ ... $x$ ... $$` 是错误）
- 需要乘幂星号时写 `e^*` 或 `e^{\ast}`，不要写 `e^\*`
- 计数项不要写 `#web_search`、`#tokens`，改写为 `N_{web\_search}`、`N_{tokens}`
- 不要把"给普通文本用的转义"直接搬进数学模式（如 `\_`、`\=`、`\*`）

### 常见错误与正确写法

- 错误：`$$ ... $s_0,a_0^j,o_1^j$ ... $$`（数学模式内嵌 `$`）
  正确：`$$ ... s_0, a_0^j, o_1^j ... $$`
- 错误：`$-\lambda \cdot #web_search$`
  正确：`$-\lambda \cdot N_{web\_search}$`
- 错误：`$\hat e = e^\*$`
  正确：`$\hat e = e^*$`

### 写后验证（必须）

- 写入后立刻 `open-doc {docID} readable` 回读，确保模型看到的是"最终落地文本"
- 至少搜索以下高风险串：`KaTeX parse error`、`Undefined control sequence`、`e^\\*`、`#web_search`、`#tokens`
- 若命中，优先修正文档内容本身，不要在工具层做自动改写

## Supporting Files

- [docs/command-reference.md](docs/command-reference.md) — 每个命令的详细参数、默认值、返回格式、示例
- [docs/pmf-spec.md](docs/pmf-spec.md) — PMF 格式规范、安全操作 vs 危险操作、编辑策略详解
- [docs/sql-reference.md](docs/sql-reference.md) — SQL 表结构、字段说明、查询示例

## SQL Quick Reference

- SQLite 语法；默认最多返回 64 行
- 时间格式 `YYYYMMDDHHmmss`
- 主要表：`blocks`（块）、`refs`（引用）、`attributes`（属性）
- 块类型：`d`文档 `h`标题 `p`段落 `l`列表 `c`代码 `t`表格 `m`公式 `b`引述 `s`超级块
- **⚠️ `tb` 是分割线（thematic break / `---`），不是"表格体"！** 表格的块类型是 `t`
- 层级：`root_id` → 文档，`parent_id` → 父容器
- JS API 查询：`s.executeSiyuanQuery('SQL')` 执行查询，`s.formatResults(r)` 格式化输出

## Block Type Reference（思源内核源码 `treenode/node.go`）

| 类型代码 | 节点类型 | 说明 | 是否容器块 |
|---------|---------|------|-----------|
| `d` | NodeDocument | 文档 | 是 |
| `h` | NodeHeading | 标题 | 否 |
| `p` | NodeParagraph | 段落 | 否 |
| `l` | NodeList | 列表 | 是 |
| `i` | NodeListItem | 列表项 | 是 |
| `c` | NodeCodeBlock | 代码块 | 否 |
| `m` | NodeMathBlock | 公式块 | 否 |
| `t` | NodeTable | **表格**（整体为一个块，内部 head/body/row/cell 不是独立块） | 否 |
| `b` | NodeBlockquote | 引述 | 是 |
| `s` | NodeSuperBlock | 超级块 | 是 |
| `tb` | NodeThematicBreak | **分割线**（`---`），⚠️ 不是表格体 | 否 |
| `html` | NodeHTMLBlock | HTML 块 | 否 |
| `av` | NodeAttributeView | 属性视图（数据库） | 否 |

**表格结构说明**：思源中表格（`t`）是原子块，内部的 TableHead/TableBody/TableRow/TableCell 是 AST 节点，**没有独立 block ID**。编辑表格只能整体替换，不能操作单个单元格。

## Notes

- cwd 必须是 skill 目录（`index.js` 所在目录）
- `.env` 自动从 `index.js` 目录加载
- 路径含空格需加引号
- Markdown 内容含换行时必须用 `$'...\n...'` 语法（Bash ANSI-C quoting），普通双引号 `"...\n..."` 中的 `\n` 是字面文本不是换行
- 连接检查：`node index.js check`
