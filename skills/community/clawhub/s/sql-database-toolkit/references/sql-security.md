# SQL 安全规范

## 核心原则：永远不要拼接 SQL

任何将用户输入直接拼接进 SQL 字符串的做法都是危险的，无论输入看起来多么"安全"。

---

## 1. 参数化查询（Parameterized Queries）

### Python (psycopg2 / mysql-connector)
```python
# ❌ 危险：字符串拼接
query = f"SELECT * FROM users WHERE name = '{user_input}'"

# ✅ 安全：参数化
cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))

# ✅ 多参数
cursor.execute(
    "INSERT INTO orders (user_id, amount) VALUES (%s, %s)",
    (user_id, amount)
)
```

### Python (SQLite)
```python
# ✅ SQLite 用 ? 占位符
conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```

### Java (JDBC PreparedStatement)
```java
// ✅ 安全
PreparedStatement stmt = conn.prepareStatement(
    "SELECT * FROM users WHERE email = ?"
);
stmt.setString(1, email);
ResultSet rs = stmt.executeQuery();
```

### Node.js (mysql2)
```javascript
// ✅ 安全
const [rows] = await conn.execute(
  'SELECT * FROM users WHERE id = ?',
  [userId]
);
```

### Go (database/sql)
```go
// ✅ 安全
row := db.QueryRow("SELECT name FROM users WHERE id = $1", userID)
```

---

## 2. ORM 安全使用

ORM 本身是安全的，但原生查询（raw query）仍需参数化：

```python
# Django ORM ✅
User.objects.filter(name=user_input)

# Django raw ✅（仍需参数化）
User.objects.raw("SELECT * FROM users WHERE name = %s", [user_input])

# SQLAlchemy ✅
session.query(User).filter(User.name == user_input)

# SQLAlchemy text() ✅
from sqlalchemy import text
session.execute(text("SELECT * FROM users WHERE name = :name"), {"name": user_input})
```

---

## 3. 动态表名 / 列名处理

参数化查询**不能**用于表名和列名，需要白名单校验：

```python
# ❌ 危险
query = f"SELECT * FROM {table_name}"

# ✅ 白名单校验
ALLOWED_TABLES = {"users", "orders", "products"}
if table_name not in ALLOWED_TABLES:
    raise ValueError(f"Invalid table: {table_name}")
query = f"SELECT * FROM {table_name}"  # 此时安全

# ✅ 列名同理
ALLOWED_SORT_COLUMNS = {"created_at", "name", "price"}
if sort_col not in ALLOWED_SORT_COLUMNS:
    sort_col = "created_at"  # 默认值
```

---

## 4. 常见 SQL 注入模式（识别与防御）

| 攻击模式 | 示例 | 防御 |
|---------|------|------|
| 经典注入 | `' OR '1'='1` | 参数化查询 |
| UNION 注入 | `' UNION SELECT password FROM users--` | 参数化 + 最小权限 |
| 盲注 | `' AND SLEEP(5)--` | 参数化 + 超时限制 |
| 二阶注入 | 存储后再读取执行 | 读取时也参数化 |
| 批量注入 | `'; DROP TABLE users;--` | 参数化 + 禁止多语句 |

---

## 5. 最小权限原则

```sql
-- 为应用创建专用账号，只授予必要权限
-- MySQL
CREATE USER 'app_user'@'%' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE ON mydb.orders TO 'app_user'@'%';
-- 不授予 DROP、CREATE、DELETE（除非必要）

-- PostgreSQL
CREATE ROLE app_user LOGIN PASSWORD 'strong_password';
GRANT SELECT, INSERT, UPDATE ON orders TO app_user;
REVOKE DELETE ON orders FROM app_user;
```

---

## 6. 输入验证清单

生成 SQL 前，对用户输入做以下检查：

- [ ] 类型校验（数字就是数字，不接受字符串）
- [ ] 长度限制（防止超长输入导致缓冲区问题）
- [ ] 格式校验（邮箱、日期、UUID 等用正则验证）
- [ ] 范围校验（分页 limit 不超过 1000，offset 不超过合理值）
- [ ] 枚举校验（状态字段只接受已知值）

---

## 7. 风险等级标注

生成涉及用户输入的 SQL 时，必须在注释中标注：

```sql
-- ⚠️ 安全级别：HIGH（含用户输入，已参数化）
-- 参数：user_id (int, validated), status (enum, whitelisted)
SELECT id, name FROM orders WHERE user_id = %s AND status = %s
```
