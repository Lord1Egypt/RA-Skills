---
name: rust-db-contracts
description: >
  Rust + SeaORM 数据库显式契约规范。当项目涉及 Rust + SeaORM 数据库开发时自动激活。
  核心：Entity 文件完全表达数据表，消灭隐式契约。
---

# Rust + SeaORM 数据库显式契约规范

> **一句话：Entity 文件就是数据表的完全表达。**
> 打开一个 entity 文件，不需要连数据库、不需要看 DDL，就能知道这张表的一切。

## 核心规则

### 1. 类型映射

| 数据表特性 | Rust 写法 | 说明 |
|---|---|---|
| NOT NULL | `pub name: String` | 不写 Option = NOT NULL，SeaORM 建表时自动加约束 |
| 可为 NULL | `pub name: Option<String>` | 编译器强制处理 None |
| 枚举字段 | `pub status: MyEnum` | 用 Rust enum + `DeriveActiveEnum`。**禁止用 String** |
| JSON 字段 | `pub config: MyStruct` | 用强类型 struct + `FromJsonQueryResult`。**禁止用 String 或 serde_json::Value**（结构不固定时除外） |
| 时间字段 | `pub created_at: DateTimeUtc` | **禁止用 NaiveDateTime**，统一 UTC |
| 默认值 | `#[sea_orm(default_value = "xxx")]` | 注解标注，SeaORM 建表时自动加 DEFAULT |
| 主键 | `#[sea_orm(primary_key)]` | |
| 唯一约束 | `#[sea_orm(unique)]` | |
| 索引 | `#[sea_orm(indexed)]` | |

### 2. 状态枚举必须带流转检查

有状态流转的枚举，必须实现 `can_transition_to()` 方法，状态变更前必须调用。

```rust
impl OrderStatus {
    pub fn can_transition_to(&self, next: &OrderStatus) -> bool {
        matches!((self, next),
            (OrderStatus::Draft, OrderStatus::Active)
            | (OrderStatus::Active, OrderStatus::Archived)
        )
    }
}
```

### 3. 业务常量不散落

- 与枚举关联的常量 → 绑定到 enum 方法（如 `member_level.max_borrows()`）
- 全局常量 → 集中定义，不在业务代码中出现裸数字/字符串

### 4. 跨表操作必须用事务

```rust
db.transaction::<_, ResultType, ErrType>(|txn| {
    Box::pin(async move {
        // 所有操作共享 txn，出错自动 rollback
        Ok(result)
    })
}).await?;
```

### 5. 软删除表查询必须过滤

使用软删除（`is_deleted: bool`）的表，查询活跃记录时必须带 `.filter(Column::IsDeleted.eq(false))`。除非明确需要查全量（注释说明原因）。

### 6. Entity 文件必须有文档

- 文件级 `//!` doc comment：业务规则、状态流转、软删除约定、关联关系等
- 每个字段 `///` 注释：业务含义，不只是字段名的复述

## 自动建表

使用 SeaORM 2.0 Entity First，entity 就是数据库 schema 的唯一事实源：

```rust
let db = Database::connect(db_url).await?;
db.get_schema_registry("my_crate::entity::*").sync(db).await?;
```

- 新增 entity → 自动建表
- 新增字段 → 自动 ALTER TABLE ADD COLUMN
- 改列名 → `#[sea_orm(renamed_from = "old_name")]` 自动 RENAME
- 不需要手写 migration

## 可选实践（按需采用）

以下不是强制要求，根据项目规模和需要决定：

- **关系定义**（`Relation` enum）：需要关联查询（JOIN/预加载）时添加
- **工厂方法**（`impl Model { fn new_xxx() }`）：有动态默认值（如"可借数量 = 总数量"）时添加，让创建逻辑集中在 entity 文件
- **查询封装**（`impl Entity { async fn find_xxx() }`）：同一段查询逻辑重复使用时提取

## 禁止清单

- ❌ 用 `String` 存枚举值
- ❌ 用 `String` 或 `serde_json::Value` 存结构化 JSON
- ❌ 用 `NaiveDateTime`
- ❌ 跨表操作不加事务
- ❌ 状态变更不检查 `can_transition_to()`
- ❌ 查询软删除表漏掉过滤（除非注释说明）
- ❌ entity 文件缺少文件级 doc comment
- ❌ 魔法数字/字符串散落在业务代码中

## 给 AI coding agent 的提示

- **先读 entity 文件**，一个文件 = 一张表的全部信息
- **直接用 Entity/ActiveModel/Column 操作数据**，不需要额外的中间类型
- **新增字段**：改 entity struct，程序启动时 schema sync 自动更新数据库
- **改状态流转**：同时改 enum 和 `can_transition_to()` 方法

参考 `references/ENTITY_EXAMPLE.md` 获取完整示例。

## 检测脚本

`references/check_db_contracts.sh` 可集成到 CI，自动检查以上规则。

```bash
# 用法
./check_db_contracts.sh [src_dir]  # 默认 ./src

# 集成到 CI
cargo build && ./check_db_contracts.sh
```

检测项：
- 是否引入了非 SeaORM 数据库库（rusqlite/sqlx/diesel 等）
- 是否有裸 SQL 操作（execute_unprepared / 硬编码 SQL 语句）
- col_expr 中是否用了字符串字面量（应用 `.set(ActiveModel)` 替代）
- Entity 文件中是否用了 `serde_json::Value` 或 `NaiveDateTime`
- 状态变更是否有 `can_transition_to()` 检查
- 软删除表查询是否过滤了 `is_deleted`
- Entity 文件是否有文件级 doc comment 和字段注释

错误（❌）会导致脚本返回非零退出码（CI 失败），警告（⚠）不阻断。
