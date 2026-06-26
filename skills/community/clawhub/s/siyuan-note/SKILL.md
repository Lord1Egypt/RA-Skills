---
name: siyuan-note
description: 思源笔记（SiYuan Note）本地 API 操作助手。用于读写笔记本、文档、块、搜索、模板、SQL 查询等本地笔记操作。触发场景：用户提到"思源笔记"、"SiYuan"、"帮我创建文档"、"搜索笔记"、"查询数据库"等。
---

# 思源笔记（SiYuan Note）API Skill

## 基础规范

- **API 基础 URL**：`http://127.0.0.1:6806`
- **认证**：请求头 `Authorization: Token <你的API Token>`（在 思源笔记 → 设置 → 关于 中查看）
- **方法**：全部 POST，Content-Type: `application/json`
- **返回格式**：`{ "code": 0, "msg": "", "data": ... }`，`code` 非 0 表示异常

> **注意**：代码执行必须包含 Token，调用示例会标注需要 Token 的端点。

## 常用操作速查

### 列出所有笔记本
```bash
curl -X POST http://127.0.0.1:6806/api/notebook/lsNotebooks \
  -H "Authorization: Token <TOKEN>"
```

### 创建文档（通过 Markdown）
```bash
curl -X POST http://127.0.0.1:6806/api/filetree/createDocWithMd \
  -H "Authorization: Token <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"notebook": "<笔记本ID>", "path": "/我的文档", "markdown": "# 标题\n\n内容"}'
```

### 执行 SQL 查询
```bash
curl -X POST http://127.0.0.1:6806/api/query/sql \
  -H "Authorization: Token <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"stmt": "SELECT * FROM blocks WHERE content LIKE '\''%关键词%'\'' LIMIT 10"}'
```

### 插入块到文档
```bash
curl -X POST http://127.0.0.1:6806/api/block/appendBlock \
  -H "Authorization: Token <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"data": "新段落内容", "dataType": "markdown", "parentID": "<父块ID>"}'
```

### 搜索文档
```bash
curl -X POST http://127.0.0.1:6806/api/query/sql \
  -H "Authorization: Token <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"stmt": "SELECT id, hpath, title FROM blocks WHERE type = '\''d'\'' AND title LIKE '\''%搜索词%'\'' LIMIT 20"}'
```

## 核心工作流程

### 工作流程 1：创建新文档
1. 调用 `lsNotebooks` 列出笔记本 → 拿到 `notebook ID`
2. 调用 `createDocWithMd` 创建文档 → 拿到 `文档ID`
3. （可选）调用 `setBlockAttrs` 设置文档属性

### 工作流程 2：搜索并读取笔记
1. 调用 `getNotebookConf` 确认笔记本存在
2. 调用 SQL `SELECT * FROM blocks WHERE content LIKE '%关键词%' LIMIT N` 全文搜索
3. 对文档 ID 调用 `getBlockKramdown` 或 `exportMdContent` 获取内容

### 工作流程 3：向文档追加内容
1. 获取目标文档的根块 ID（通常等于文档 ID 本身）
2. 调用 `appendBlock` 在文档末尾追加新块
3. 或调用 `prependBlock` 在文档开头插入

### 工作流程 4：使用模板
1. 调用 `renderSprig` 渲染 Sprig 模板表达式（如 `{{now | date "2006-01-02"}}`）
2. 结合 `createDocWithMd` 创建带有日期标题的文档

## SQL 查询要点

关键表：
- `blocks` — 所有块（段落、标题、代码块等）
  - `id` / `hpath` / `title` / `content` / `type` / `subtype` / `markdown` / `created` / `updated`
- `blocks` 表中 `type = 'd'` 为文档，标题块 `type = 'h'`，段落 `type = 'p'`

常用查询：
```sql
-- 搜索包含关键词的块
SELECT id, hpath, content FROM blocks 
WHERE content LIKE '%关键词%' LIMIT 20;

-- 列出某笔记本下所有文档
SELECT id, title, hpath FROM blocks 
WHERE notebook = '<笔记本ID>' AND type = 'd';

-- 搜索文档标题
SELECT id, hpath, title FROM blocks 
WHERE type = 'd' AND title LIKE '%标题%' LIMIT 10;
```

## 重要限制

- SQL 接口在发布模式（Publication）下需要开启文档读写权限，否则会被禁止
- 资源文件上传使用 `multipart/form-data`，不是 JSON
- API 全部为本地调用，思源笔记必须运行在本地

## 完整 API 参考

见 [references/api.md](references/api.md)（包含所有端点的完整说明）
