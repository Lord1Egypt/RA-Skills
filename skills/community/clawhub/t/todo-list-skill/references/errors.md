# todo-list Skill — 错误处理 + 降级路径

> 版本：v1.0 | 更新：2026-06-11

## 异常类型（4 个）

| 异常 | 触发 | 退出码 |
|------|------|:---:|
| `TodoNotFoundError` | 未找到匹配的 TODO | 1 |
| `TodoAmbiguousError` | 多个匹配（candidates 列表）| 1 |
| `TodoValidationError` | 参数校验失败 | 2 |
| `TodoDatabaseError` | 数据库异常（锁死/损坏）| 70 |

## 4 个降级路径

### 1. NL 解析失败

**触发**：用户输入无关键词
**降级**：
- 回复"无法识别，请用'加个待办：xxx'格式"
- 不写数据库
- 不推送

### 2. 歧义处理

**触发**：done/delete 模糊匹配多个
**降级**：
- 列出候选（最多 5 个）
- 问"完成哪一个？"
- 不执行

### 3. 数据库 lock（重试 3 次）

**触发**：`sqlite3.OperationalError: database is locked`
**降级**：
- 指数退避：0.1s → 0.2s → 0.4s
- 仍失败 → 写 `/tmp/todos_fallback.json`
- 推送："数据库暂时异常，已记录到 fallback"

### 4. 数据库损坏

**触发**：`sqlite3.DatabaseError`
**降级**：
- 立即返回错误
- 写日志 CRITICAL
- 提示用户检查 `todos.db`
- 不自动恢复（避免数据丢失）

## 边界处理

| 输入 | 处理 |
|------|------|
| 空字符串 | unknown |
| 纯空格 | unknown |
| 超长（>2000）| 截断 + WARNING |
| 含 HTML 标签 | 原样存储（agent 渲染时转义） |
| 含 SQL 注入 | 参数化查询自动防护 |
| 表情符号 | 保留（UTF-8） |
| 中文+英文混合 | 正常处理 |
| 纯英文 | 正常处理 |

## 推送降级

| 场景 | 处理 |
|------|------|
| qwenpaw 命令不存在（开发环境）| 仅打印消息 |
| 推送超时（10s）| 失败返回 |
| subprocess 异常 | 失败返回 + 写日志 |
