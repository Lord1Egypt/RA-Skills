---
name: "天翼云 DMS 数据管理服务 (客户端)"
description: "提供 DMS 客户端数据管理能力，包括实例管理、SQL查询、工单创建、团队管理、用户管理。用于用户请求数据库实例添加、数据查询、提交工单、团队配置等操作时调用。"
---

# 天翼云 DMS 数据管理服务 (客户端)

本 Skill 提供 DMS（数据管理服务）客户端的自动化操作能力，支持通过 API 调用或 CLI 工具实现实例管理、数据查询、工单创建、团队配置等功能。

## 功能概述

本 Skill 支持以下 4 个核心功能场景：

1. **自动实例管理** - 数据库实例的添加、删除、修改
2. **数据查询** - SQL 执行和数据探索分析
3. **自然语言提工单** - 工单创建和查询
4. **自动团队配置管理** - 团队创建、用户邀请、实例分配

---

## ⚠️ 避坑指南（必读）

### 1. 实例登录方式

实例登录支持两种方式：

#### 方式一：使用 dbAccountId 登录（推荐）

通过 `account-list` 命令获取数据库账号 ID，然后使用账号 ID 登录，无需密码。

**步骤：**
```bash
# 1. 查询实例账户列表
java -jar dms-cli.jar instance account-list --id <实例ID> --origin <origin值>

# 2. 使用 dbAccountId 登录
java -jar dms-cli.jar instance login \
    --id <实例ID> \
    --db-account-id <账号ID> \
    --origin <origin值>
```

#### 方式二：使用账密登录

使用数据库账号和密码登录，**需要用户手动提供真实密码**，不支持任何默认密码。

**命令：**
```bash
java -jar dms-cli.jar instance login \
    --id <实例ID> \
    --db-account <数据库账号> \
    --password <数据库密码> \
    --origin <origin值>
```

**⚠️ 注意：**
- 参数名是 `--password`，不是 `--db-password`
- 密码会被自动 AES 加密传输
- **禁止**提供默认密码或自动尝试密码

### 2. origin 参数必须显式指定

**错误写法（可能失败）：**
```bash
java -jar dms-cli.jar instance login --id 10413 --db-account root --password "密码"
# origin 使用默认值 5，但实例实际可能是 2
```

**正确写法：**
```bash
# 先查询实例详情确认 origin 值
java -jar dms-cli.jar instance detail --id 10413
# 查看返回数据中的 "origin" 字段

# 登录时显式指定正确的 origin
java -jar dms-cli.jar instance login --id 10413 --db-account root --password "密码" --origin 2
```

**⚠️ origin 取值：**
| origin值 | 来源 | 常见场景 |
|---------|------|---------|
| 1 | RDS云数据库 | 天翼云RDS |
| 2 | 公网/直连 | 客户端添加的公网实例 |
| 3 | DMS代理 | Agent模式 |
| 4 | AOne环境 | AOne开发环境 |
| 5 | 内网 | 内网数据库（默认） |

### 3. 弱管控实例也需要 Token

**⚠️ 重要：即使 controlType=0（弱管控），执行 SQL 仍需要先登录获取 Token！**

**错误做法：**
```bash
# 直接执行 SQL，不登录
java -jar dms-cli.jar sql execute --instance-id 10413 --sql "SHOW DATABASES"
# 会报错："查询弱管控实例Token不能为空"
```

**正确流程：**
```bash
# 1. 先登录获取 Token
java -jar dms-cli.jar instance login --id 10413 --db-account root --password "密码" --origin 2
# 返回: {"code":200,"data":"26d4540fe7e01ff1",...}  -- Token 在 data 字段

# 2. 使用 Token 执行 SQL
java -jar dms-cli.jar sql execute \
    --instance-id 10413 \
    --sql "SHOW DATABASES" \
    --instance-token "26d4540fe7e01ff1" \
    --origin 2
```

### 4. database list API 可能返回空

**问题：** `database list` 命令返回空数组，但实例确实有数据库。

**原因：** 该 API 对某些实例可能不返回数据。

**解决方案：** 使用 SQL 直接查询
```bash
# 先登录获取 Token
java -jar dms-cli.jar instance login --id 10413 --db-account root --password "密码" --origin 2

# 用 SQL 查询数据库列表
java -jar dms-cli.jar sql execute \
    --instance-id 10413 \
    --sql "SHOW DATABASES" \
    --instance-token "Token值" \
    --origin 2
```

### 5. account-list 可能返回空

**问题：** `account-list` 命令返回空数组，但实例详情显示有 `dbAccount: "root"`。

**解决方案：** 直接使用实例详情中的 `dbAccount` 值登录
```bash
# 查询实例详情
java -jar dms-cli.jar instance detail --id 10413
# 找到 "dbAccount": "root"

# 直接使用该账号登录
java -jar dms-cli.jar instance login --id 10413 --db-account root --password "密码" --origin 2
```

### 6. ⚠️⚠️⚠️ PostgreSQL 数据库切换的正确方法（极重要）

**问题：** 使用 `--database` 或 `--db-id` 参数执行 SQL 时，数据可能写入错误的数据库！

**根因分析（已验证）：**
1. WebSocket 连接建立时会绑定到登录时的数据库
2. `--database` 和 `--db-id` 参数**不会切换数据库连接**，只是设置消息体参数
3. PostgreSQL 不支持跨数据库操作，必须在连接时就指定正确的数据库

**⚠️ 验证结果：**
```bash
# 测试：创建表并插入数据，检查 db_name 列
CREATE TABLE tpcds_verify (id INT, db_name TEXT DEFAULT current_database())
INSERT INTO tpcds_verify (id) VALUES (1)
SELECT * FROM tpcds_verify
# 结果：db_name = "autotest_db_3952484"（错误的数据库！）
# 即使指定了 --database tpcds 和 --db-id 17575
```

**✅ 正确做法：登录时必须使用 --db-name 参数指定目标数据库！**

```bash
# ❌ 错误做法：登录时不指定数据库，后续无法切换
java -jar dms-cli.jar instance login \
    --id 10292 \
    --db-account-id 4587 \
    --origin 2
# 登录后连接到默认数据库，无法切换！

# ❌ 错误做法：使用 --database 参数尝试切换数据库
java -jar dms-cli.jar sql execute \
    --instance-id 10292 \
    --sql "CREATE TABLE test (id INT)" \
    --database tpcds \
    --instance-token "xxx" \
    --origin 2
# 表仍然创建在默认数据库中！

# ✅ 正确做法：登录时使用 --db-name 参数指定目标数据库(PG需要此参数)
java -jar dms-cli.jar instance login \
    --id 10292 \
    --db-account-id 4587 \
    --origin 2 \
    --db-name tpcds
# 现在连接已经绑定到 tpcs 数据库

# 验证当前数据库
java -jar dms-cli.jar sql execute \
    --instance-id 10292 \
    --sql "SELECT current_database()" \
    --instance-token "xxx" \
    --origin 2
# 应该返回 "tpcds"
```

**完整安全流程（PostgreSQL 专用）：**

```bash
# 步骤1：查询目标数据库的 dbId（可选，用于某些需要 dbId 的操作）
java -jar dms-cli.jar sql execute \
    --instance-id 10292 \
    --sql "SELECT datname, oid FROM pg_database WHERE datistemplate = false" \
    --instance-token "xxx" \
    --origin 2

# 步骤2：登出当前连接（如果有）
java -jar dms-cli.jar instance logout --token "旧Token"

# 步骤3：重新登录并指定目标数据库
java -jar dms-cli.jar instance login \
    --id 10292 \
    --db-account-id 4587 \
    --origin 2 \
    --db-name tpcds
# 返回新的 Token

# 步骤4：验证当前数据库
java -jar dms-cli.jar sql execute \
    --instance-id 10292 \
    --sql "SELECT current_database()" \
    --instance-token "新Token" \
    --origin 2
# 确认返回 "tpcds"

# 步骤5：执行 SQL（现在可以安全地操作 tpcs 数据库）
java -jar dms-cli.jar sql execute \
    --instance-id 10292 \
    --sql "CREATE TABLE test (id INT PRIMARY KEY)" \
    --instance-token "新Token" \
    --origin 2 \
    --db-type 2

# 步骤6：验证表是否在正确的数据库中
java -jar dms-cli.jar sql execute \
    --instance-id 10292 \
    --sql "SELECT tablename FROM pg_tables WHERE schemaname = 'public'" \
    --instance-token "新Token" \
    --origin 2
```

**⚠️ 不同数据库类型的处理方式：**

| 数据库类型 | dbType | 切换数据库方式 | 关键参数 |
|-----------|--------|---------------|---------|
| MySQL | 1 | `--database` 参数有效 | 登录后可用 `USE database` |
| **PostgreSQL** | 2 | **必须登录时指定** | `--db-name` 在登录时 |
| SQL Server | 6 | `--database` 参数有效 | 登录后可用 `USE database` |
| MongoDB/DDS | 9 | `--database` 参数有效 | 连接字符串指定 |

**⚠️ PostgreSQL 特殊说明：**
- **`--db-name` 参数只在 `instance login` 命令中有效**
- 登录后无法通过任何参数切换数据库
- 每次需要操作不同数据库时，必须先登出再重新登录
- `--db-id` 和 `--schema-id` 参数用于 schema 级别操作，不切换数据库

---

## 枚举参数说明

### 一、实例来源 (origin)

| 值 | 枚举名 | 中文说明 | 英文说明 |
|----|--------|---------|----------|
| 1 | RDS | 云数据库/天翼云数据库 | Cloud Database |
| 2 | PUBLIC | 公网/直连数据库 | Public Network/Direct Connection Database |
| 3 | AGENT | DMS代理数据库 | DMS Proxy Database |
| 4 | AONE | AOne环境数据库 | AOne Environment Database |
| 5 | INTRANET | 内网数据库 | Intranet Database |

### 二、数据库类型 (dbType)

| 值 | 枚举名 | 中文说明 |
|----|--------|---------|
| 1 | MYSQL | MySQL |
| 2 | PGSQL | PostgreSQL |
| 3 | ADB | TeleDB For AnalyticDB |
| 4 | GPSQL | Greenplum |
| 5 | TELEDBX | TeleDB for Xscale |
| 6 | SQLSERVER | SQL Server |
| 7 | DRDS | DRDS |
| 8 | MONGO | MongoDB |
| 9 | DDS | DDS |
| 10 | HIVE | Hive |
| 11 | ORACLE | Oracle |
| 12 | DAMENG | 达梦 |
| 13 | CLICKHOUSE | ClickHouse |
| 14 | TIDB | TiDB |

### 三、实例环境 (envType / defaultEnvType)

| 值 | 枚举名 | 中文说明 | 英文说明 |
|----|--------|---------|----------|
| 1 | DEV | 开发 | develop |
| 2 | BETA | 测试 | beta |
| 3 | PRE | 预发 | pre-product |
| 4 | PRO | 生产 | product |

### 四、实例状态 (state)

| 值 | 枚举名 | 中文说明 | 英文说明 |
|----|--------|---------|----------|
| 1 | DEFAULT | 正常 | Normal |
| 2 | ERROR | 异常 | Exception |
| 3 | DISABLE | 禁用 | Disabled |

### 五、读写类型 (rw / isRw)

| 值 | 枚举名 | 中文说明 |
|----|--------|---------|
| 0 | READONLY | 只读 |
| 1 | RW | 读写 |

### 六、实例模式 (mode / instanceMode)

| 值 | 枚举名 | 中文说明 | 英文说明 |
|----|--------|---------|----------|
| 1 | WEB | Web模式 | Web Mode |
| 2 | CLIENT | Client模式 | Client Mode |

### 七、管控类型 (controlType)

| 值 | 枚举名 | 中文说明 |
|----|--------|---------|
| 0 | WEAK_CONTROL_TYPE | 弱管控模式 |
| 1 | STRONG_CONTROL_TYPE | 强管控模式 |

**⚠️ 说明：**
- 弱管控模式：无需数据库账号密码即可登录，但执行 SQL **仍需要 Token**
- 强管控模式：需要数据库账号密码授权后才能执行 SQL

### 八、工单类型 (type)

| 值 | 中文说明 |
|----|---------|
| export | 数据导出工单 |
| import | 数据导入工单 |
| sql | SQL变更工单 |
| query | SQL查询工单 |
| sqlreview | SQL评审工单 |

### 九、工单状态 (status)

| 值 | 中文说明 |
|----|---------|
| 0 | 待提交 |
| 1 | 审批中 |
| 2 | 审批通过 |
| 3 | 审批拒绝 |
| 4 | 执行中 |
| 5 | 执行成功 |
| 6 | 执行失败 |
| 7 | 已撤回 |
| 8 | 已关闭 |

### 十、团队成员角色 (role)

| 值 | 枚举名 | 中文说明 |
|----|--------|---------|
| 1 | ADMIN | 管理员 |
| 2 | MEMBER | 普通成员 |
| 5 | READONLY | 只读 |

### 十一、实例登录状态 (loginStatus)

| 值 | 中文说明 |
|----|---------|
| 0 | 未登录 |
| 1 | 已登录 |

---

## 构建与运行

### 前提条件

- Java 11 或更高版本
- Maven 3.6+

### 构建项目

```bash
cd dms-data-management-java
mvn clean package
```

### 运行 CLI

```bash
java -jar target/dms-cli-1.0.0.jar <command>
```

---

### 一、实例管理命令

#### 创建实例
```bash
java -jar dms-cli.jar instance create \
    --alias "测试数据库" \
    --host 127.0.0.1 \
    --port 3306 \
    --user root \
    --password "your_password" \
    --type mysql
```

#### 修改实例
```bash
# 基本修改
java -jar dms-cli.jar instance modify --id 123 --alias "新名称"
java -jar dms-cli.jar instance modify --id 123 --host 192.168.1.1 --port 3307

# 将实例添加到团队（重要：需要先通过 instance detail 获取 origin 值）
java -jar dms-cli.jar instance modify --id <实例ID> --team-id <团队ID> --origin <origin值>
# origin值说明：
#   1 = RDS (云数据库)
#   2 = PUBLIC (公网/直连)
#   3 = AGENT (DMS代理)
#   4 = AONE (AOne环境)
#   5 = INTRANET (内网)
```

#### 删除实例
```bash
java -jar dms-cli.jar instance delete --id 123
```

#### 查看实例详情
```bash
java -jar dms-cli.jar instance detail --id 123
# 返回示例：
# {"code":200,"data":{..., "id":"10413", "origin":2, "controlType":0, "dbAccount":"root", ...}}
```

#### 查看实例列表
```bash
java -jar dms-cli.jar instance list --page 1 --page-size 10
```

#### 测试连接
```bash
java -jar dms-cli.jar instance test \
    --host 127.0.0.1 \
    --port 3306 \
    --user root \
    --password "password" \
    --type mysql
# type可选值：mysql(1), pgsql(2), sqlserver(6), mongo(8), doris(3), etc.
```

#### 登录/登出实例 ⚠️

实例登录支持两种方式：

**方式一：使用 dbAccountId 登录（推荐）**
```bash
# 查询账户列表
java -jar dms-cli.jar instance account-list --id <实例ID> --origin <origin值>

# 使用 dbAccountId 登录（无需密码）
java -jar dms-cli.jar instance login \
    --id <实例ID> \
    --db-account-id <账号ID> \
    --origin <origin值>
```

**方式二：使用账密登录**
```bash
# ⚠️ 必须指定正确的 origin 值（从实例详情获取）
# ⚠️ 密码需要用户手动提供，不支持默认密码
java -jar dms-cli.jar instance login \
    --id <实例ID> \
    --db-account <数据库账号> \
    --password <数据库密码> \
    --origin <origin值>
```

**登出**
```bash
java -jar dms-cli.jar instance logout --token "instance_token"
```

#### 添加实例到团队
```bash
java -jar dms-cli.jar instance add-to-team --id 123 --team-id 456
```

---

### 二、用户管理命令

#### 用户列表
```bash
java -jar dms-cli.jar user list --page 1 --page-size 10
```

#### 用户详情
```bash
java -jar dms-cli.jar user detail --id 123
```

#### 添加用户
```bash
java -jar dms-cli.jar user add --email "user@example.com" --captcha "123456"
```

#### 删除用户
```bash
java -jar dms-cli.jar user delete --id 123
java -jar dms-cli.jar user delete --id 123 --tenant-id 456
```

#### 修改用户
```bash
java -jar dms-cli.jar user modify --id 123 --comment "用户备注"
```

---

### 三、团队管理命令

#### 创建团队
```bash
java -jar dms-cli.jar team create --name "数据分析团队" --desc "团队描述" --manager-ids "42"
```

#### 按名称查找团队
```bash
java -jar dms-cli.jar team find --name "数据分析团队"
# 返回: {"id":"123","teamName":"数据分析团队","memberCount":1,...}
# Agent可以通过此命令获取团队ID
```

#### 添加团队成员
```bash
# role取值说明：
#   1 = 管理员 (ADMIN)
#   2 = 普通成员 (MEMBER)
#   5 = 只读 (READONLY)
java -jar dms-cli.jar team add-member --team-id 123 --user-id "405" --role 2
```

#### 修改团队
```bash
java -jar dms-cli.jar team modify --id 123 --name "新团队名"
```

#### 删除团队
```bash
java -jar dms-cli.jar team delete --id 123
```

#### 团队详情
```bash
java -jar dms-cli.jar team detail --id 123
```

#### 团队列表
```bash
java -jar dms-cli.jar team list --page 1 --page-size 10
```

#### 我的团队
```bash
java -jar dms-cli.jar team my
```

---

### 四、工单管理命令

#### 创建工单
```bash
# 导出工单 (type=export)
java -jar dms-cli.jar workorder create \
    --type export \
    --instance-id 123 \
    --database "db_name" \
    --table "table_name"

# 导入工单 (type=import)
java -jar dms-cli.jar workorder create \
    --type import \
    --instance-id 123 \
    --database "db_name"

# SQL变更工单 (type=sql)
java -jar dms-cli.jar workorder create \
    --type sql \
    --instance-id 123 \
    --sql "UPDATE table SET column='value' WHERE id=1"
```

#### 工单详情
```bash
java -jar dms-cli.jar workorder detail --id 123
```

#### 工单列表
```bash
# 支持 status 参数过滤
# status取值：
#   0=待提交, 1=审批中, 2=审批通过, 3=审批拒绝
#   4=执行中, 5=执行成功, 6=执行失败, 7=已撤回, 8=已关闭
java -jar dms-cli.jar workorder list --page 1 --page-size 10
java -jar dms-cli.jar workorder list --status 1
```

#### 撤回工单
```bash
java -jar dms-cli.jar workorder withdraw --id 123
```

#### 重试工单
```bash
java -jar dms-cli.jar workorder retry --id 123
```

---

### 五、数据库查询命令 ⚠️

#### 查看数据库列表
```bash
# ⚠️ 注意：可能返回空数组，建议使用 SQL 查询
java -jar dms-cli.jar database list --instance-id 123

# 分页查询
java -jar dms-cli.jar database page-list --instance-id 123 --page 1 --page-size 20
```

#### 执行 SQL ⚠️ 完整流程

**⚠️ 重要：执行 SQL 前必须先登录获取 Token！**

### 流程步骤

1. **查询实例详情，获取关键信息**
   ```bash
   java -jar dms-cli.jar instance detail --id <实例ID>
   # 记录 origin, dbAccount, controlType
   ```

2. **登录实例获取 Token**

   **方式一：使用 dbAccountId 登录（推荐）**
   ```bash
   # 查询账户列表获取 dbAccountId
   java -jar dms-cli.jar instance account-list --id <实例ID> --origin <origin值>

   # 使用 dbAccountId 登录
   java -jar dms-cli.jar instance login \
       --id <实例ID> \
       --db-account-id <账号ID> \
       --origin <origin值>
   ```

   **方式二：使用账密登录**
   ```bash
   # ⚠️ 参数是 --password，不是 --db-password
   # ⚠️ 必须指定正确的 --origin 值
   # ⚠️ 密码需要用户手动提供
   java -jar dms-cli.jar instance login \
       --id <实例ID> \
       --db-account <数据库账号> \
       --password <数据库密码> \
       --origin <origin值>
   ```

3. **⚠️ 验证当前数据库（关键步骤！）**
   ```bash
   # MySQL/PostgreSQL 验证当前数据库
   java -jar dms-cli.jar sql execute \
       --instance-id <实例ID> \
       --sql "SELECT current_database()" \
       --instance-token <Token> \
       --origin <origin值>
   # 确认返回的数据库名称是否为目标数据库！
   # 如果不匹配，需要使用 --db-id 参数或重新登录
   ```

4. **执行 SQL**
   ```bash
   # 基本执行
   java -jar dms-cli.jar sql execute \
       --instance-id <实例ID> \
       --sql "SELECT * FROM table_name" \
       --instance-token <登录获取的Token> \
       --origin <origin值>

   # PostgreSQL 必须使用 db-id 参数
   java -jar dms-cli.jar sql execute \
       --instance-id <实例ID> \
       --sql "CREATE TABLE test (id INT)" \
       --database <数据库名> \
       --db-id <数据库ID> \
       --schema-id <SchemaID> \
       --db-type 2 \
       --instance-token <Token> \
       --origin <origin值>
   ```

5. **⚠️ 执行后验证数据是否写入正确的数据库**
   ```bash
   java -jar dms-cli.jar sql execute \
       --instance-id <实例ID> \
       --sql "SELECT current_database(), table_name FROM information_schema.tables WHERE table_schema = 'public'" \
       --database <数据库名> \
       --instance-token <Token> \
       --origin <origin值>
   ```

#### SQL 执行示例

```bash
# 1. 登录获取 Token
java -jar dms-cli.jar instance login \
    --id 10413 \
    --db-account root \
    --password "DIEVU-k7eNxR" \
    --origin 2
# 返回: {"code":200,"data":"26d4540fe7e01ff1",...}

# 2. ⚠️ 验证当前数据库
java -jar dms-cli.jar sql execute \
    --instance-id 10413 \
    --sql "SELECT database()" \
    --instance-token "26d4540fe7e01ff1" \
    --origin 2
# 确认返回的数据库名称是否正确！

# 3. 使用 Token 查询数据库列表
java -jar dms-cli.jar sql execute \
    --instance-id 10413 \
    --sql "SHOW DATABASES" \
    --instance-token "26d4540fe7e01ff1" \
    --origin 2

# 4. 在指定数据库执行 SQL（先验证数据库）
java -jar dms-cli.jar sql execute \
    --instance-id 10413 \
    --sql "SHOW TABLES" \
    --database "dms_console" \
    --instance-token "26d4540fe7e01ff1" \
    --origin 2

# 5. PostgreSQL 示例（必须使用 db-id 和 schema-id）
# 先查询数据库 ID
java -jar dms-cli.jar sql execute \
    --instance-id 10292 \
    --sql "SELECT datname, oid FROM pg_database WHERE datistemplate = false" \
    --instance-token "xxx" \
    --origin 2

# 使用 db-id 执行 SQL
java -jar dms-cli.jar sql execute \
    --instance-id 10292 \
    --sql "CREATE TABLE test (id INT PRIMARY KEY)" \
    --database tpcds \
    --db-id 17575 \
    --schema-id 4239 \
    --db-type 2 \
    --instance-token "xxx" \
    --origin 2

# 验证表是否创建在正确的数据库
java -jar dms-cli.jar sql execute \
    --instance-id 10292 \
    --sql "SELECT current_database(), tablename FROM pg_tables WHERE schemaname = 'public'" \
    --database tpcds \
    --db-id 17575 \
    --instance-token "xxx" \
    --origin 2
```

---

## 配置文件说明

配置文件 `config.json` 需要包含以下内容：

```json
{
  "base_url": "https://localhost:8091",
  "ws_url": "wss://localhost:8091/cloud/ws/sqlConsole/query",
  "tokens": ["token1", "token2"],
  "headers": {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN",
    "Content-Type": "application/json",
    "From-Client": "true",
    "User-Agent": "Mozilla/5.0..."
  },
  "cookies": {
    "Authorization-jwt": "your_jwt_token",
    "XSRF-TOKEN": "your_xsrf_token",
    "Authorization-jwt-local": "your_local_token"
  },
  "xsrf_token": "your_xsrf_token",
  "verify": false
}
```

---

## API 接口说明

### 一、实例管理

| 功能 | 方法 | 接口 | 说明 |
|------|------|------|------|
| 创建实例 | POST | `/cloud/meta/instance/create` | 创建新的数据库实例 |
| 修改实例 | POST | `/cloud/meta/instance/modify` | 修改实例信息，支持添加实例到团队 |
| 删除实例 | POST | `/cloud/meta/instance/delete` | 删除指定实例 |
| 实例详情 | POST | `/cloud/meta/instance/detail` | 获取实例详细信息 |
| 实例列表 | POST | `/cloud/meta/instance/pageList` | 分页查询实例列表 |
| 测试连接 | POST | `/cloud/meta/instance/testConnection` | 测试实例连接是否正常 |
| 登录实例 | POST | `/cloud/meta/instance/login` | 登录到指定实例 |
| 登出实例 | POST | `/cloud/meta/instance/logout` | 登出实例 |
| **添加实例到团队** | POST | `/cloud/meta/instance/modify` | 通过修改接口的 `--team-id` 参数添加 |

### 二、用户与团队管理

| 功能 | 方法 | 接口 | 说明 |
|------|------|------|------|
| 用户登录 | POST | `/cloud/dmsUser/userLogin` | DMS 用户登录 |
| 用户登出 | POST | `/cloud/dmsUser/userLogout` | DMS 用户登出 |
| 添加用户 | POST | `/cloud/dmsUser/joinTenant` | 添加用户到组织 |
| 删除用户 | POST | `/cloud/dmsUser/exitTenant` | 从组织删除用户 |
| 用户列表 | POST | `/cloud/dmsUser/pageList` | 分页查询用户列表 |
| 用户详情 | POST | `/cloud/dmsUser/detail` | 获取用户详细信息 |
| 修改用户 | POST | `/cloud/dmsUser/modify` | 修改用户信息 |
| 创建团队 | POST | `/cloud/team/create` | 创建新的团队 |
| **添加团队成员** | POST | `/cloud/team/member/create` | 将用户添加到团队 |
| 修改团队 | POST | `/cloud/team/modify` | 修改团队信息 |
| 删除团队 | POST | `/cloud/team/delete` | 删除指定团队 |
| 团队详情 | POST | `/cloud/team/detail` | 获取团队详细信息 |
| 团队列表 | POST | `/cloud/team/pageList` | 分页查询团队列表 |
| **按名称查找团队** | - | `team find` 命令 | 遍历列表查找指定名称的团队 |

### 三、工单管理

| 功能 | 方法 | 接口 | 说明 |
|------|------|------|------|
| 创建工单 | POST | `/cloud/workOrder/create` | 创建新的工单 |
| 工单详情 | POST | `/cloud/workOrder/detail` | 获取工单详情 |
| 工单列表 | POST | `/cloud/workOrder/pageList` | 分页查询工单列表 |
| 撤回工单 | POST | `/cloud/workOrder/withdraw` | 撤回指定工单 |
| 重试工单 | POST | `/cloud/workOrder/retry` | 重试失败的工单 |

---

## 常见场景流程

### 场景一：创建团队并添加成员和实例

当用户要求创建团队、邀请用户加入、将实例添加到团队时，使用以下流程：

**步骤1：创建团队**
```bash
java -jar dms-cli.jar team create --name "团队名称" --desc "描述" --manager-ids "42"
# 返回 {"code":200,"data":"SUCCESS"}
```

**步骤2：查找新团队ID**（因为创建返回无ID）
```bash
java -jar dms-cli.jar team find --name "团队名称"
# 返回团队详情，包含 id
```

**步骤3：添加成员**
```bash
# role: 1=管理员, 2=普通成员, 5=只读
java -jar dms-cli.jar team add-member --team-id <团队ID> --user-id <用户ID> --role 2
```

**步骤4：查找实例ID和origin**（从instance detail获取）
```bash
java -jar dms-cli.jar instance detail --id <实例ID>
# 从返回数据中找到 id, origin 字段
```

**步骤5：将实例添加到团队**
```bash
java -jar dms-cli.jar instance modify --id <实例ID> --team-id <团队ID> --origin <origin值>
```

### 场景二：SQL查询执行

**⚠️ 请参考上方"数据库查询命令"部分的完整流程**

---

## 重要说明

1. **认证要求**: 所有 API 调用需要有效的 JWT Token，通过配置文件中的 `cookies` 传递
2. **密码安全**: 敏感密码需要使用 AES 加密后传输，加密密钥为 `DMS-FRONT@2023#*`
3. **权限控制**: 部分操作需要特定权限（如实例创建、删除需要对应功能权限）
4. **WebSocket 连接**: SQL 执行使用 WebSocket 协议，需要保持连接直到查询完成
5. **实例管控模式**: 实例分为强管控和弱管控两种模式
   - **弱管控 (controlType=0)**: 登录时无需密码，但执行 SQL **仍需要 Token**
   - **强管控 (controlType=1)**: 需要数据库账号密码授权后才能执行 SQL
6. **⚠️ Token 有效期**: Token 有有效期限制，过期需要重新登录
7. **⚠️ origin 参数**: 登录和 SQL 执行都必须指定正确的 origin 值，默认值可能不正确