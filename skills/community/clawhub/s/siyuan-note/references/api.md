# 思源笔记 API 参考

> 来源：[官方 API 文档](https://github.com/siyuan-note/siyuan/blob/master/API_zh_CN.md)

## 规范

- **Base URL**：`http://127.0.0.1:6806`
- **全部 POST**，Content-Type: `application/json`
- **认证**：`Authorization: Token <token>`（设置 → 关于 查看）
- **响应**：`{ "code": 0, "msg": "", "data": ... }`，code 非 0 = 异常

---

## 笔记本 `/api/notebook/`

### 列出笔记本
```
POST /api/notebook/lsNotebooks
无参数
```

### 打开笔记本
```json
{ "notebook": "<笔记本ID>" }
```

### 关闭笔记本
```json
{ "notebook": "<笔记本ID>" }
```

### 创建笔记本
```json
{ "name": "笔记本名称" }
```

### 重命名笔记本
```json
{ "notebook": "<笔记本ID>", "name": "新名称" }
```

### 删除笔记本
```json
{ "notebook": "<笔记本ID>" }
```

### 获取笔记本配置
```json
{ "notebook": "<笔记本ID>" }
```

### 保存笔记本配置
```json
{
  "notebook": "<笔记本ID>",
  "conf": { "name": "...", "closed": false, "refCreateSavePath": "", "createDocNameTemplate": "", "dailyNoteSavePath": "/daily note/{{now | date \"2006/01\"}}/{{now | date \"2006-01-02\"}}", "dailyNoteTemplatePath": "" }
}
```

---

## 文档 `/api/filetree/`

### 通过 Markdown 创建文档
```json
{
  "notebook": "<笔记本ID>",
  "path": "/foo/bar",
  "markdown": "# 标题\n\n内容"
}
```
- `path` 需要以 `/` 开头
- 重复调用不会覆盖已有文档

### 重命名文档（按路径）
```json
{ "notebook": "<笔记本ID>", "path": "/xxx.sy", "title": "新标题" }
```

### 重命名文档（按 ID）
```json
{ "id": "<文档ID>", "title": "新标题" }
```

### 删除文档（按路径）
```json
{ "notebook": "<笔记本ID>", "path": "/xxx.sy" }
```

### 删除文档（按 ID）
```json
{ "id": "<文档ID>" }
```

### 移动文档（按路径）
```json
{ "fromPaths": ["/xxx.sy"], "toNotebook": "<目标笔记本ID>", "toPath": "/" }
```

### 移动文档（按 ID）
```json
{ "fromIDs": ["<文档ID>"], "toID": "<目标父文档或笔记本ID>" }
```

### 根据路径获取人类可读路径
```json
{ "notebook": "<笔记本ID>", "path": "/xxx/xxx.sy" }
```

### 根据 ID 获取人类可读路径
```json
{ "id": "<块ID>" }
```

### 根据 ID 获取存储路径
```json
{ "id": "<块ID>" }
```

### 根据人类可读路径获取 IDs
```json
{ "path": "/foo/bar", "notebook": "<笔记本ID>" }
```

---

## 资源文件 `/api/asset/`

### 上传资源文件
```
POST /api/asset/upload
Content-Type: multipart/form-data
```
- `assetsDirPath`：资源目录，如 `"/assets/"` 或 `"/assets/sub/"`
- `file[]`：文件列表

---

## 块 `/api/block/`

### 插入块
```json
{
  "dataType": "markdown",
  "data": "内容",
  "nextID": "<后一个块ID>",
  "previousID": "<前一个块ID>",
  "parentID": "<父块ID>"
}
```
- `nextID` / `previousID` / `parentID` 至少有一个必须有值，优先级：nextID > previousID > parentID

### 插入前置子块
```json
{ "data": "内容", "dataType": "markdown", "parentID": "<父块ID>" }
```

### 插入后置子块
```json
{ "data": "内容", "dataType": "markdown", "parentID": "<父块ID>" }
```

### 更新块
```json
{ "dataType": "markdown", "data": "新内容", "id": "<块ID>" }
```

### 删除块
```json
{ "id": "<块ID>" }
```

### 移动块
```json
{ "id": "<块ID>", "previousID": "<前一个块ID>", "parentID": "<父块ID>" }
```

### 折叠块
```json
{ "id": "<块ID>" }
```

### 展开块
```json
{ "id": "<块ID>" }
```

### 获取块 kramdown 源码
```json
{ "id": "<块ID>" }
```

### 获取子块
```json
{ "id": "<父块ID>" }
```

### 转移块引用
```json
{ "fromID": "<源块ID>", "toID": "<目标块ID>", "refIDs": ["<引用块ID>"] }
```

---

## 属性 `/api/attr/`

### 设置块属性
```json
{ "id": "<块ID>", "attrs": { "custom-attr1": "值" } }
```
- 自定义属性必须以 `custom-` 为前缀

### 获取块属性
```json
{ "id": "<块ID>" }
```

---

## SQL `/api/query/`

### 执行 SQL 查询
```json
{ "stmt": "SELECT * FROM blocks WHERE content LIKE '%关键词%' LIMIT 10" }
```

### 提交事务
```
POST /api/sqlite/flushTransaction
无参数
```

### 常用 SQL 示例

```sql
-- 全文搜索
SELECT id, hpath, content FROM blocks WHERE content LIKE '%关键词%' LIMIT 20;

-- 列出所有文档
SELECT id, title, hpath FROM blocks WHERE type = 'd';

-- 按笔记本筛选
SELECT id, hpath, content FROM blocks WHERE notebook = '<笔记本ID>' LIMIT 20;

-- 搜索文档标题
SELECT id, hpath, title FROM blocks WHERE type = 'd' AND title LIKE '%标题%';

-- 获取块更新时间
SELECT id, updated FROM blocks ORDER BY updated DESC LIMIT 10;

-- 统计某笔记本块数
SELECT COUNT(*) FROM blocks WHERE notebook = '<笔记本ID>';
```

---

## 模板 `/api/template/`

### 渲染模板
```json
{ "id": "<文档ID>", "path": "模板文件绝对路径" }
```

### 渲染 Sprig 表达式
```json
{ "template": "/daily note/{{now | date \"2006/01\"}}/{{now | date \"2006-01-02\"}}" }
```

---

## 文件 `/api/file/`

### 获取文件
```json
{ "path": "/data/笔记本ID/文档ID.sy" }
```
- 返回 200 = 文件内容，202 = 错误信息

### 写入文件（multipart）
```
POST /api/file/putFile
Content-Type: multipart/form-data
```
- `path`：工作空间路径
- `isDir`：是否为文件夹
- `modTime`：Unix 时间戳
- `file`：文件内容

### 删除文件
```json
{ "path": "/data/xxx.sy" }
```

### 重命名文件
```json
{ "path": "/data/旧路径", "newPath": "/data/新路径" }
```

### 列出文件
```json
{ "path": "/data/笔记本ID" }
```

---

## 导出 `/api/export/`

### 导出 Markdown 文本
```json
{ "id": "<文档ID>" }
```

### 导出文件与目录
```json
{ "paths": ["/conf/appearance/boot", "/conf/appearance/langs"], "name": "导出文件名" }
```

---

## 转换 `/api/convert/`

### Pandoc 转换
```json
{ "dir": "test", "args": ["--to", "markdown_strict-raw_html", "foo.epub", "-o", "foo.md"] }
```

---

## 通知 `/api/notification/`

### 推送消息
```json
{ "msg": "消息内容", "timeout": 7000 }
```

### 推送报错消息
```json
{ "msg": "错误信息", "timeout": 7000 }
```

---

## 网络 `/api/network/`

### 正向代理
```json
{ "url": "https://example.com", "method": "GET", "timeout": 7000, "contentType": "text/html", "headers": [], "payload": {}, "payloadEncoding": "text", "responseEncoding": "text" }
```

---

## 系统 `/api/system/`

### 获取启动进度
```
POST /api/system/bootProgress
无参数
```

### 获取系统版本
```
POST /api/system/version
无参数
```

### 获取系统当前时间
```
POST /api/system/currentTime
无参数
```
