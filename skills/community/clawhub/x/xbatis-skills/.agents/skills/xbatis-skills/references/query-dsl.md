# DSL、对象条件与结果映射

## 链式 DSL 的真实类

源码中的真实包名：

- `cn.xbatis.core.sql.executor.chain.QueryChain`
- `cn.xbatis.core.sql.executor.chain.InsertChain`
- `cn.xbatis.core.sql.executor.chain.UpdateChain`
- `cn.xbatis.core.sql.executor.chain.DeleteChain`

README 里有时写成 `cn.xbatis.core.chain.*`，生成代码时不要照抄那个包名。

## QueryChain

适合绝大多数查询拼装场景：

- `select`
- `from`
- `join`
- `where`
- `groupBy`
- `having`
- `orderBy`
- 子查询、嵌套条件、分页、游标、`mapWithKey`

生成代码时优先使用这些约定：

- 搜索接口默认 `.forSearch(true)`，自动忽略 `null`、空字符串并做 `trim`
- 或直接使用条件重载：`eq(field, value, Objects::nonNull)`
- `returnType(...)` 放在 `get` / `list` / `paging` 前
- 对当前实体的简单查询尽量用省略写法

典型省略写法：

```java
SysUser user = QueryChain.of(sysUserMapper)
        .eq(SysUser::getId, 1)
        .get();
```

复杂查询再显式写 `select` / `join` / `returnType`。

## InsertChain / UpdateChain / DeleteChain

适合默认 CRUD 不够用时：

- `InsertChain`
  - 支持 `insert ... values`
  - 支持 `insert ... select`
  - 支持 `onConflict`
- `UpdateChain`
  - 支持动态 `set`
  - 支持函数更新，例如版本号自增
  - 支持 `RETURNING`
- `DeleteChain`
  - 支持条件删除
  - 支持 `RETURNING`
  - 默认是物理删除，不走逻辑删除拦截

## 对象驱动条件

对象条件相关注解都在 `cn.xbatis.db.annotations`：

- `@ConditionTarget`
- `@Condition`
- `@Conditions`
- `@ConditionGroup`
- `@OrderByTarget`
- `@OrderBy`

常见用法：

- DTO 类上用 `@ConditionTarget(Entity.class)`
- 字段上用 `@Condition(...)` 声明 EQ、LIKE、BETWEEN 等映射
- 一个字段要映射多列时，用 `@Conditions`
- 需要分组逻辑时，用 `@ConditionGroup`

当前仓库里可核实的扩展点：

- `cn.xbatis.core.sql.ObjectConditionLifeCycle`
  - 可在构建条件前处理 DTO 入参

## 结果映射

结果映射注解也在 `cn.xbatis.db.annotations`：

- `@ResultEntity`
- `@ResultField`
- `@NestedResultEntity`
- `@NestedResultEntityField`
- `@ResultCalcField`
- `@Fetch`
- `@PutEnumValue`
- `@PutValue`

生成 VO 查询时优先遵循这些规则：

- 如果 VO 和实体字段同名，优先 `@ResultEntity` 自动映射
- 多层嵌套时再补 `@NestedResultEntity`
- 自动级联或补充字段时使用 `@Fetch`
- 不要先手写大段 `select a.xxx as ...`，优先让注解驱动自动选列

`@Fetch` 的能力较强，支持：

- 源字段或列指定
- 中间表
- 目标实体和目标属性
- 排序、限制条数、内存分页
- 缓存名称

只有在注解表达不清楚或性能要求特殊时，才退回显式 SQL。

## AI 生成建议

- 优先生成短链、直接可读的 DSL，不要把条件拆成很多无意义中间变量
- 搜索类接口默认启用忽略空值能力
- 需要数据库函数时优先静态导入 `Methods.*`
- 生成 VO 时优先注解映射，少写手工别名 SQL
