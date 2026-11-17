# 向量索引使用指南

**用途**：记录文件的语义搜索和快速检索

---

## 文件位置

| 用途 | 路径 | 说明 |
|------|------|------|
| 向量数据库 | `{WORKSPACE}/vectors/embeddings.db` | **主存储** (SQLite) |
| 嵌入脚本 | `{SKILL_DIR}/scripts/embed.py` | 向量生成/搜索工具 |

> `{WORKSPACE}` 指 agent 当前工作目录（即 exec 的 `workdir` 参数）。
> `{SKILL_DIR}` 指本 skill 的安装目录（agent 加载 skill 时自动解析）。

---

## 向量生成配置

| 项目 | 配置 |
|------|------|
| API Provider | 硅基流动 (SiliconFlow) |
| 嵌入模型 | `BAAI/bge-m3` |
| 向量维度 | 1024 |
| API KEY 环境变量 | `SILICONFLOW_API_KEY` |

---

## 使用方式

### 生成/更新索引

**每次创建或修改记录文件后**，需要更新向量索引：

```
exec: command="/usr/bin/python3 {SKILL_DIR}/scripts/embed.py init", workdir="{WORKSPACE}"
```

脚本会自动从 `{WORKSPACE}/records/` 扫描记录文件，将向量存入 `{WORKSPACE}/vectors/embeddings.db`。

### 搜索记录

当需要查找相关记录时：

```
exec: command="/usr/bin/python3 {SKILL_DIR}/scripts/embed.py search \"关键词\" 5", workdir="{WORKSPACE}"
```

### 输出示例

```
🔍 搜索：分词接口争议

  [0.892] 20260310-report-分词接口争议.md - 20260310
    算法部门提供的分词接口无法区分 Landmark 的具体类型...

  [0.756] 20260320-meeting-分词迭代讨论.md - 20260320
    识别分词的下一个迭代方向，引入新华词典等中文词库...
```

---

## 索引文件结构

```sql
-- 数据库：{WORKSPACE}/vectors/embeddings.db
CREATE TABLE records (
    id         TEXT PRIMARY KEY,
    file       TEXT NOT NULL,
    filename   TEXT NOT NULL,
    date       TEXT NOT NULL,
    category   TEXT,
    file_hash  TEXT,
    mtime      REAL,
    preview    TEXT,
    embedding  BLOB NOT NULL,  -- 1024 维向量 (binary)
    created_at TEXT,
    updated_at TEXT,
    status     TEXT DEFAULT 'open'
);
```

**特性**：
- 增量更新：自动检测变更文件（基于文件哈希），无需全量重建
- SQLite 索引优化，查询速度快

---

## 检索优先级

当用户要求查阅记录时，按以下顺序检索：

1. **向量搜索** — 使用 embed.py 进行语义检索（首选）
2. **文件名匹配** — 根据文件名中的 category/topic 关键词
3. **全文 grep** — 在 records/ 目录下 grep 关键词

---

## 注意事项

1. **API KEY 安全** — `SILICONFLOW_API_KEY` 通过环境变量传递，不要硬编码到文件中
2. **增量更新** — 脚本已支持增量更新，自动检测变更文件
3. **模型一致性** — 更换嵌入模型后需重新生成全部索引
4. **回退机制** — 如 SQLite 数据库损坏，可删除后重新 `embed.py init` 生成
5. **文本截断** — 单条记录超过 15000 字符时会自动截断（bge-m3 模型限制）
