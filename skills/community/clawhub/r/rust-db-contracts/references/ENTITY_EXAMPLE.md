# Entity 文件完整示例

一个 entity 文件应该包含的所有部分。

```rust
//! # tasks 表 —— 任务实体
//!
//! ## 业务规则
//! - 状态流转：Pending → Running → Done（单向）；Running → Failed（可重试：Failed → Pending）
//! - 此表使用软删除（is_deleted 字段）
//! - config 字段存 JSON，结构为 TaskConfig
//! - 所有时间字段统一 UTC
//! - project_id 关联 projects 表（逻辑外键）

use sea_orm::entity::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Clone, Debug, PartialEq, Eq, DeriveEntityModel, Serialize, Deserialize)]
#[sea_orm(table_name = "tasks")]
pub struct Model {
    /// 主键，自增
    #[sea_orm(primary_key)]
    pub id: i64,

    /// 任务名称
    pub name: String,

    /// 所属项目 ID（逻辑外键 → projects.id）
    #[sea_orm(indexed)]
    pub project_id: i64,

    /// 任务状态（见 TaskStatus 枚举）
    #[sea_orm(default_value = "pending")]
    pub status: TaskStatus,

    /// 优先级，1=最高
    #[sea_orm(default_value = 5)]
    pub priority: i32,

    /// 任务配置（JSON），可为空
    #[sea_orm(column_type = "Json")]
    pub config: Option<TaskConfig>,

    /// 描述，可为空
    pub description: Option<String>,

    /// 软删除标记
    #[sea_orm(default_value = false)]
    pub is_deleted: bool,

    /// 创建时间，UTC
    pub created_at: DateTimeUtc,

    /// 更新时间，UTC
    pub updated_at: DateTimeUtc,
}

/// 任务状态
///
/// 流转规则：
/// - Pending → Running → Done
/// - Running → Failed
/// - Failed → Pending（重试）
#[derive(Clone, Debug, PartialEq, Eq, EnumIter, DeriveActiveEnum, Serialize, Deserialize)]
#[sea_orm(rs_type = "String", db_type = "String(StringLen::N(20))")]
pub enum TaskStatus {
    #[sea_orm(string_value = "pending")]
    Pending,
    #[sea_orm(string_value = "running")]
    Running,
    #[sea_orm(string_value = "done")]
    Done,
    #[sea_orm(string_value = "failed")]
    Failed,
}

impl TaskStatus {
    pub fn can_transition_to(&self, next: &TaskStatus) -> bool {
        matches!((self, next),
            (TaskStatus::Pending, TaskStatus::Running)
            | (TaskStatus::Running, TaskStatus::Done)
            | (TaskStatus::Running, TaskStatus::Failed)
            | (TaskStatus::Failed, TaskStatus::Pending) // 重试
        )
    }
}

/// tasks.config 字段的 JSON 结构
#[derive(Clone, Debug, PartialEq, Eq, Serialize, Deserialize, FromJsonQueryResult)]
pub struct TaskConfig {
    /// 超时时间（秒）
    pub timeout_secs: Option<u64>,
    /// 最大重试次数
    pub max_retries: Option<u32>,
    /// 环境变量
    #[serde(default)]
    pub env: std::collections::HashMap<String, String>,
}

// 关系（可选，需要关联查询时添加）
#[derive(Copy, Clone, Debug, EnumIter, DeriveRelation)]
pub enum Relation {}

impl ActiveModelBehavior for ActiveModel {}
```

## 数据库操作示例

```rust
use sea_orm::*;

// 插入 —— 直接用 ActiveModel
let task = task::ActiveModel {
    name: Set("构建镜像".to_string()),
    project_id: Set(1),
    // status 和 priority 有 default_value，可以不设
    // is_deleted 有 default_value = false，可以不设
    created_at: Set(chrono::Utc::now()),
    updated_at: Set(chrono::Utc::now()),
    ..Default::default()
};
let task = task.insert(db).await?;

// 查询
let task = task::Entity::find_by_id(1).one(db).await?;

// 条件查询（注意软删除过滤）
let active_tasks = task::Entity::find()
    .filter(task::Column::ProjectId.eq(project_id))
    .filter(task::Column::IsDeleted.eq(false))  // 软删除过滤
    .filter(task::Column::Status.eq(TaskStatus::Pending))
    .all(db).await?;

// 更新 —— 先查再改
let mut active: task::ActiveModel = task.unwrap().into();
active.status = Set(TaskStatus::Running);
active.updated_at = Set(chrono::Utc::now());
active.update(db).await?;

// 跨表操作 —— 用事务
db.transaction::<_, (), DbErr>(|txn| {
    Box::pin(async move {
        // 操作1
        task_active_model.insert(txn).await?;
        // 操作2（同一事务）
        project_active_model.update(txn).await?;
        Ok(())
    })
}).await?;
```

## Checklist

新建 entity 时确认：

- [ ] 文件级 `//!` doc comment（业务规则）
- [ ] 每个字段有 `///` 注释
- [ ] 可空字段用 `Option<T>`，非空字段用 `T`
- [ ] 枚举字段用 enum + `DeriveActiveEnum`，有流转的带 `can_transition_to()`
- [ ] JSON 字段用强类型 struct + `FromJsonQueryResult`
- [ ] 时间字段用 `DateTimeUtc`
- [ ] 静态默认值用 `#[sea_orm(default_value = "...")]`
- [ ] 相关常量不散落在业务代码中
