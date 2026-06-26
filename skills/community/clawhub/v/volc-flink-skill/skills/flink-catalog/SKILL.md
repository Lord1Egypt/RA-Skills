---
name: flink-catalog
description: Flink Catalog 元数据管理工具，用于列举 Flink 的 catalog、database、table 和 table 的结构信息，并且可以基于这些库表信息进行 SQL 作业开发等工作。Use this skill when the user wants to inspect concrete metadata objects in Flink catalog, such as listing catalogs/databases/tables or viewing table schema/details for SQL development. Always trigger only when the request contains a metadata intent + a concrete catalog object/action.
required_binaries:
  - volc_flink
may_access_config_paths:
  - ~/.volc_flink
  - $VOLC_FLINK_CONFIG_DIR
credentials:
  primary: volc_flink_local_config
  optional_env_vars:
    - VOLCENGINE_ACCESS_KEY
    - VOLCENGINE_SECRET_KEY
    - VOLCENGINE_REGION
---

# Flink Catalog 元数据管理技能

基于 `volc_flink catalog` 命令行工具，用于管理 Flink Catalog 中注册的 catalog、database、table 和 table 的结构信息等重要内容。

---

## 通用约定（必读）

本技能的基础约定与只读约定统一收敛在：

- `../../COMMON.md`
- `../../COMMON_READONLY.md`

本技能用于 Catalog / Database / Table 的元数据查询与结构分析，不执行发布、启动、删除等变更操作。

---

## 🎯 核心功能

### 1. 登录状态检测
**在执行任何操作前，先检测登录状态！**

**检测步骤**：
1. 尝试执行一个简单的命令（如 `volc_flink config show`）
2. 如果提示"请先登录"，则提示用户需要登录
3. 提供登录指引：请使用交互式登录 `volc_flink login`（或企业内部安全方式），不要在对话/命令行参数中粘贴 AK/SK，详见 `../../COMMON.md`

**错误处理**：
- 如果检测到未登录，立即停止后续操作
- 友好提示用户需要先登录

---

### 2. 信息提取与智能选择

#### 2.1 信息提取
从用户提问中提取关键信息：
- **Flink 项目名** (project_name)
- **Catalog 名** (catalog_name)
- **Database 名** (database_name)
- **Table 名** (table_name)
- **操作类型**：列举 Catalog、列举 Database、列举 Table、查看 Table 详情、查看树形结构等

#### 2.2 智能项目选择
**如果用户没有明确提供项目名，按以下流程处理**：

1. 列出所有项目：`volc_flink projects list`
2. 让用户选择项目
3. 然后执行具体的 catalog 操作

---

### 3. Catalog 操作

#### 3.1 列举所有 Catalog
使用 `volc_flink catalog catalogs list` 列出所有 Catalog。

**命令格式**：
```bash
volc_flink catalog catalogs list
```

#### 3.2 查看某个 Catalog 详情
使用 `volc_flink catalog catalogs show` 查看某个 Catalog 的详情。

**命令格式**：
```bash
volc_flink catalog catalogs show
```

---

### 4. Database 操作

#### 4.1 列举 Catalog 下的所有 Database
使用 `volc_flink catalog databases list` 列出 Catalog 下的所有 Database。

**命令格式**：
```bash
volc_flink catalog databases list
```

#### 4.2 查看某个 Database 详情
使用 `volc_flink catalog databases show` 查看某个 Database 的详情。

**命令格式**：
```bash
volc_flink catalog databases show
```

---

### 5. Table 操作

#### 5.1 列举 Database 下的所有 Table
使用 `volc_flink catalog tables list` 列出 Database 下的所有 Table。

**命令格式**：
```bash
volc_flink catalog tables list
```

#### 5.2 查看某个 Table 详情
使用 `volc_flink catalog tables show` 查看某个 Table 的详情（包括表结构）。

**命令格式**：
```bash
volc_flink catalog tables show
```

---

### 6. 树形结构操作

#### 6.1 递归列出 Catalog/Database/Table 树
使用 `volc_flink catalog tree` 递归列出 Catalog/Database/Table 树。

**命令格式**：
```bash
# 列出所有 Catalog/Database/Table 树
volc_flink catalog tree

# 只看某个 Catalog
volc_flink catalog tree --catalog-name <Catalog名称>

# 只看某个 Database
volc_flink catalog tree --catalog-name <Catalog名称> --database <Database名称>

# 只看某个 Table
volc_flink catalog tree --catalog-name <Catalog名称> --database <Database名称> --table <Table名称>

# 获取详细信息
volc_flink catalog tree --details --table-details

# 输出完整 JSON
volc_flink catalog tree --raw
```

**选项说明**：
- `--catalog-id CATALOG_ID` - 只看某个 CatalogId
- `--catalog-name CATALOG_NAME` - 只看某个 CatalogName
- `--database DATABASE` - 只看某个 DatabaseName
- `--table TABLE` - 只看某个 TableName
- `--details` - 拉取 Database detail（GetCatalogDatabase）
- `--table-details` - 拉取 Table detail（GetCatalogTable）
- `--raw` - 输出完整 JSON
- `--region REGION` - Region（默认使用当前登录 region）

---

### 7. 基于库表信息进行 SQL 开发

#### 7.1 浏览库表结构
在进行 SQL 开发前，先浏览库表结构，了解可用的表和字段。

**流程**：
1. 列出所有 Catalog
2. 选择 Catalog 后，列出该 Catalog 下的所有 Database
3. 选择 Database 后，列出该 Database 下的所有 Table
4. 选择 Table 后，查看该 Table 的详情（包括表结构）

#### 7.2 生成 SQL 模板
基于浏览到的库表结构，生成常用的 SQL 模板：

**CREATE TABLE 模板**：
```sql
CREATE TABLE <table_name> (
  <field1> <type1>,
  <field2> <type2>,
  ...
) WITH (
  'connector' = '<connector_type>',
  ...
);
```

**SELECT 查询模板**：
```sql
SELECT <fields>
FROM <table_name>
WHERE <condition>;
```

**INSERT INTO 模板**：
```sql
INSERT INTO <sink_table>
SELECT <fields>
FROM <source_table>
WHERE <condition>;
```

---

## 工具调用顺序

### 列举所有 Catalog
1. **检测登录状态** - 确认已登录
2. **智能选择项目** - 如果用户没有提供，列出项目供选择
3. **列举 Catalog** - `volc_flink catalog catalogs list`

### 列举 Catalog 下的 Database
1. **检测登录状态** - 确认已登录
2. **智能选择项目** - 如果用户没有提供，列出项目供选择
3. **列举 Catalog** - `volc_flink catalog catalogs list`（如果用户没有提供 Catalog）
4. **列举 Database** - `volc_flink catalog databases list`

### 列举 Database 下的 Table
1. **检测登录状态** - 确认已登录
2. **智能选择项目** - 如果用户没有提供，列出项目供选择
3. **列举 Catalog** - `volc_flink catalog catalogs list`（如果用户没有提供 Catalog）
4. **列举 Database** - `volc_flink catalog databases list`（如果用户没有提供 Database）
5. **列举 Table** - `volc_flink catalog tables list`

### 查看 Table 详情
1. **检测登录状态** - 确认已登录
2. **智能选择项目** - 如果用户没有提供，列出项目供选择
3. **列举 Catalog** - `volc_flink catalog catalogs list`（如果用户没有提供 Catalog）
4. **列举 Database** - `volc_flink catalog databases list`（如果用户没有提供 Database）
5. **列举 Table** - `volc_flink catalog tables list`（如果用户没有提供 Table）
6. **查看 Table 详情** - `volc_flink catalog tables show`

### 查看树形结构
1. **检测登录状态** - 确认已登录
2. **智能选择项目** - 如果用户没有提供，列出项目供选择
3. **查看树形结构** - `volc_flink catalog tree`（带可选参数）

### 基于库表信息进行 SQL 开发
1. **检测登录状态** - 确认已登录
2. **智能选择项目** - 如果用户没有提供，列出项目供选择
3. **浏览库表结构** - 使用 tree 命令或逐级列举 Catalog/Database/Table
4. **选择目标表** - 让用户选择要使用的表
5. **查看表结构** - `volc_flink catalog tables show`
6. **生成 SQL 模板** - 基于表结构生成 SQL 模板
7. **用户确认** - 向用户展示 SQL 模板，等待确认
8. **（可选）调用 flink-sql 技能** - 如果用户需要，调用 flink-sql 技能进行完整的 SQL 开发

---

## 常用 volc_flink catalog 命令速查

### Catalog 操作
```bash
# 列举 Catalog
volc_flink catalog catalogs list

# 查看某个 Catalog 详情
volc_flink catalog catalogs show
```

### Database 操作
```bash
# 列举 Catalog 下的 Database
volc_flink catalog databases list

# 查看某个 Database 详情
volc_flink catalog databases show
```

### Table 操作
```bash
# 列举 Database 下的 Table
volc_flink catalog tables list

# 查看某个 Table 详情
volc_flink catalog tables show
```

### 树形结构操作
```bash
# 递归列出 Catalog/Database/Table 树
volc_flink catalog tree

# 只看某个 Catalog
volc_flink catalog tree --catalog-name <Catalog名称>

# 只看某个 Database
volc_flink catalog tree --catalog-name <Catalog名称> --database <Database名称>

# 只看某个 Table
volc_flink catalog tree --catalog-name <Catalog名称> --database <Database名称> --table <Table名称>

# 获取详细信息
volc_flink catalog tree --details --table-details

# 输出完整 JSON
volc_flink catalog tree --raw
```

### 通用选项
```bash
# 指定项目
volc_flink catalog -p <项目名> <子命令>

# 指定项目 ID
volc_flink catalog --project-id <项目ID> <子命令>
```

---

## 输出格式

### 列举 Catalog 输出
```
# 📚 Flink Catalog 列表

## 📋 项目信息
- **项目名**: [项目名]

## 📊 Catalog 列表
[Catalog 列表内容]
```

### 列举 Database 输出
```
# 📚 Flink Database 列表

## 📋 项目信息
- **项目名**: [项目名]
- **Catalog**: [Catalog 名]

## 📊 Database 列表
[Database 列表内容]
```

### 列举 Table 输出
```
# 📚 Flink Table 列表

## 📋 项目信息
- **项目名**: [项目名]
- **Catalog**: [Catalog 名]
- **Database**: [Database 名]

## 📊 Table 列表
[Table 列表内容]
```

### 查看 Table 详情输出
```
# 📊 Flink Table 详情

## 📋 基本信息
- **项目名**: [项目名]
- **Catalog**: [Catalog 名]
- **Database**: [Database 名]
- **Table**: [Table 名]

## 📝 表结构
[表结构内容]

## 💡 SQL 模板
```sql
-- CREATE TABLE 模板
CREATE TABLE [table_name] (
  [field1] [type1],
  [field2] [type2],
  ...
) WITH (
  'connector' = '[connector_type]',
  ...
);

-- SELECT 查询模板
SELECT [fields]
FROM [table_name]
WHERE [condition];
```
```

### 树形结构输出
```
# 🌳 Flink Catalog 树形结构

## 📋 项目信息
- **项目名**: [项目名]

## 🌲 树形结构
[树形结构内容]
```

---

## 错误处理

### 常见错误及处理

#### 错误 1：未登录
**错误信息**：`❌ 请先登录`

**处理方式**：
- 友好提示："检测到未登录火山引擎账号，请先登录"
- 提供登录指引：请使用交互式登录 `volc_flink login`（或企业内部安全方式），详见 `../../COMMON.md`
- 停止后续操作，等待用户登录后重试

#### 错误 2：Catalog/Database/Table 不存在
**错误信息**：指定的 Catalog/Database/Table 不存在

**处理方式**：
- 提示："未找到指定的 Catalog/Database/Table，请检查名称是否正确"
- 提供帮助：列出可用的 Catalog/Database/Table 供用户选择

#### 错误 3：网络超时
**错误信息**：命令执行超时

**处理方式**：
- 提示："命令执行超时，请检查网络连接"
- 建议稍后重试
- 如果多次失败，建议检查火山引擎服务状态

---

## 注意事项

1. **先检测登录状态**：在执行任何操作前，先检测是否已登录
2. **智能选择**：如果用户没有提供足够的信息，逐级列出选项供用户选择
3. **提供清晰反馈**：向用户提供清晰的操作结果和后续建议
4. **友好的错误处理**：如果操作失败，向用户说明失败原因，并提供解决方案
5. **SQL 模板生成**：查看表详情时，自动生成常用的 SQL 模板
6. **与其他技能协作**：可以与 flink-sql 技能协作，进行完整的 SQL 开发

---

## 🎯 技能总结

### 核心功能
1. ✅ **Catalog 管理** - 列举和查看 Catalog
2. ✅ **Database 管理** - 列举和查看 Database
3. ✅ **Table 管理** - 列举和查看 Table（包括表结构）
4. ✅ **树形结构浏览** - 递归查看 Catalog/Database/Table 树
5. ✅ **SQL 模板生成** - 基于表结构生成常用 SQL 模板
6. ✅ **与 flink-sql 协作** - 可以调用 flink-sql 技能进行完整的 SQL 开发

这个技能可以完整地覆盖 Flink Catalog 元数据的浏览和管理，并且可以基于库表信息进行 SQL 作业开发！
