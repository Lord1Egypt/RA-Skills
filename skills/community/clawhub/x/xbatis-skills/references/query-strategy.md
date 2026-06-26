# Query Strategy

适用于以下场景：

- 标准列表页
- 搜索页
- 分页接口
- exists / count
- 联表查询
- VO 返回

## 选择顺序

1. 按 id 查询单表或单表部分列：优先 DAO / Mapper 的 `getById`
2. 按 id 查询单列值：优先 `getValueById`
3. 常规多条件查询：优先查询对象转条件 + DAO 内部的 `queryChain(qo.where())`
4. 如果是“先查 A，顺带带出 B”的场景：优先考虑 `@Fetch`，不要默认 join
5. 联表 + 展示对象：优先 DAO 内部的 `queryChain() + returnType(VO.class)`
6. 极复杂表达：再考虑 SQL 模板 / 原生 SQL

按 id 查询不要默认写 `QueryChain`：

- 返回完整实体：`getById(id)`
- 返回单表部分列：`getById(id, Entity::getName, Entity::getStatus)`
- 返回一列：`getValueById(id, Entity::getName)`
- 只有不属于上述 id 查询的场景，才进入 `queryChain()`

## QueryChain 使用规则

默认在 DAO 内创建 `QueryChain`：

- 使用 `queryChain()` / `queryChain(where)`
- 不在 Service / Controller 中直接写 `QueryChain.of(...)`
- 单 Mapper 项目 BaseDao 继承 `BasicDaoImpl<T, ID>`，多 Mapper 项目 BaseDao 继承 `DaoImpl<T, ID>`
- 业务 DAO 继承项目 BaseDao，不直接到处继承框架 DAO 实现
- 适合“先查 A，顺带带出 B”的场景优先考虑 `@Fetch`
- join 查询优先先 `.from(...)` 明确主表
- join 优先使用 `leftJoin(SysUser::getRoleId, SysRole::getId)` 这类方法引用写法；第二个参数所属实体是被 join 的实体

如果项目有 DAO 层，Service 层不要承载数据库操作 SQL 代码：

- 不在 Service 中创建 `QueryChain` / `UpdateChain` / `InsertChain` / `DeleteChain`
- 不在 Service 中拼接 SQL、where、order by
- 不在 Service 中维护 count / limit / exists SQL
- Service 调用 DAO 方法；条件构建优先交给实现 `cn.xbatis.core.mvc.QO` 的查询对象

### 查询对象 / 对象转条件

推荐用查询对象构建 where：

- 查询条件对象实现 `cn.xbatis.core.mvc.QO`
- 类名是 `QO`，不要写成 `Qo`
- 查询条件对象优先声明 `@ConditionTarget`
- 需要字段级条件时优先使用 `@Condition`
- 单字段映射多列时优先使用 `@Conditions`
- 需要成组逻辑时优先使用 `@ConditionGroup`
- QO 中凡是不是数据库操作字段、需要忽略的字段，优先使用 `@Ignore` 或 `@Ignores`
- 在查询对象的 `where()` 中集中生成条件
- 在 `where()` 中优先使用 `WhereUtil.where(this)`
- DAO 内部优先使用 `queryChain(qo.where())`

适合：

- 标准列表页筛选
- 搜索表单
- 后台多条件过滤
- 可复用的业务查询条件

不要把一长串条件判断散落在 Service 层。条件含义属于查询对象时，优先让查询对象实现 `QO` 并输出 `Where`。

推荐示意：

```java
@Data
@ConditionTarget(SysUser.class)
public class SysUserQO implements QO {

    @Condition(Condition.Type.LIKE)
    private String userName;

    @Override
    public Where where() {
        return WhereUtil.where(this);
    }
}
```

### 搜索场景

搜索表单、后台筛选页、关键词搜索这类“搜索查询”优先使用：

- `forSearch(true)`

因为它会组合：

- 忽略 `null`
- 忽略空字符串
- 字符串 `trim`

在搜索型接口里，不要手工把这三套逻辑散落在 Service 层。

不要在非搜索查询中默认启用 `forSearch(true)`，例如：

- 详情查询
- 唯一性校验
- 内部业务规则查询
- 明确要求空字符串参与条件判断的查询

这些场景应按业务语义显式处理条件，避免搜索优化改变查询含义。

### 非搜索条件忽略

无法使用 `forSearch(true)`，但仍需要按值决定是否忽略条件时，优先使用条件方法的 predicate 重载：

```java
queryChain().eq(SysUser::getId, id, Objects::nonNull);
```

如果当前条件方法或表达方式无法使用 predicate 重载，再使用 boolean `when` 重载：

```java
queryChain().eq(Objects.nonNull(id), SysUser::getId, id);
```

注意：

- predicate 重载把“值是否有效”的判断和字段绑定在一起，优先级高于在外层散落 `if`
- boolean `when` 重载适合 predicate 不方便表达的条件
- 如果一组条件需要括号包裹，尤其组内有 `or` 条件，使用 `.nested(chain -> ...)`
- 条件拼接默认是 `and` 行为；调用 `.or()` 后后续条件会持续使用 `or`，需要切回 `and` 时显式调用 `.and()`
- 局部 `or` 条件优先放进 `.nested(...)`，避免 `.or()` 状态影响后续外层条件

示例：

```java
queryChain().nested(chain -> chain.eq(SysUser::getId, id, Objects::nonNull));
```

### Methods 风格

如果当前项目或表达方式使用 `Methods`：

- 优先静态导入所需 `Methods` 方法
- 方法嵌套优先写成 `eq(gt(...))` 这类形式
- 不要混用一半静态导入、一半 `Methods.xxx(...)` 的风格

### 分页场景

分页统一优先：

- `paging(Pager)`

不要自己手工写：

- `count(*)`
- `limit`
- 页码和总页数计算

### 联表场景

优先原则：

1. 先明确是否真的需要 join
2. 如果只是查询 A 时顺带带出 B，优先考虑 `@Fetch`
3. 真正需要 join 时，优先先 `.from(...)` 明确主表
4. join 时优先明确 ON 条件，并优先使用 `leftJoin(SysUser::getRoleId, SysRole::getId)` 这类方法引用写法
5. 返回展示对象优先用 VO
6. 优先让框架自动 select 需要的列

### 返回对象

Controller / API 对外返回优先使用 VO，不建议直接返回实体类：

- 后台管理系统的列表、详情 VO 可按项目风格考虑继承实体类
- 非后台管理系统也建议返回 VO，避免把持久化实体直接暴露给外部接口
- 展示型、联表型、聚合型结果优先用 VO
- DAO 内部和纯持久化读写方法可以返回实体，但不要把实体直接穿透到接口响应

Controller / API 入参优先保持可演进：

- 入参超过 2 个时，使用 QO、DTO、Model 等对象接收
- 即使当前不超过 2 个，但大概率后续会增加过滤项、分页项、排序项或业务参数，也应提前使用对象
- Controller 接收对象后传给 Service 层，不要把多个散参继续透传到 Service / DAO
- 查询入参优先使用 QO，修改入参优先使用 Model 或项目统一的 DTO / Model 约定

不要为了前端展示字段污染实体类，也不要先查实体再手工 copy 成 VO；优先使用 `select(VO.class)`、`returnType(VO.class)` 和结果映射注解。

补充规则：

- 返回 VO 时，优先 `select(VO.class)`
- 如果 `returnType` 和 `select` 的类型一致，且没有额外 select 字段，可省略 `.select(...)`
- 不要手工一个一个 `select` 列，本可直接 `select(VO.class)` 却堆大量字段
- VO 类尽量配合 xbatis 的 `@ResultEntity`、`@NestedResultEntity`、`@NestedResultEntityField`、`@ResultCalcField` 等结果映射注解
- 需要枚举名称时优先使用 `@PutEnumValue`
- VO 中凡是不是数据库操作字段、需要忽略的字段，优先使用 `@Ignore` 或 `@Ignores`
- select 别名优先使用 getter / 字段引用形式，例如 `.select(SysUser::getId, c -> c.as(SysUser::getId))`
- 只有字段无法自然映射或别名需要脱离现有字段体系时，才使用 `.select(SysUser::getId, c -> c.as("id"))`

### leftJoin 注意事项

如果是 1 对多分页场景，要特别检查分页优化是否适合当前 SQL。

文档里明确提示：

- 左联分页更适合 1 对 1
- 非 1 对 1 时要优先评估是否改用 `rightJoin()`，或至少关闭 join 优化，例如关注 `Pager.of(1).setOptimize(false)`

这属于 Agent 应该主动注意的风险点。

## 不推荐行为

1. 在 Service 层手工拼 where 片段
2. 在 Controller 层拼排序 SQL
3. 按 id 查询实体、部分列或单列值时直接写 `QueryChain`
4. 查询对象可表达的条件直接写 XML
5. 查实体再手工 copy 到 VO
6. 明明能用 `QueryChain` 却退回字符串 SQL
7. 在非搜索查询中机械套用 `forSearch(true)`
8. 本可用 `.eq(field, value, Objects::nonNull)`，却在外层写一堆 `if`
9. 需要括号包裹 `or` 条件却没有使用 `.nested(...)`
10. 调用 `.or()` 后没有显式 `.and()` 切回，导致后续条件错误变成 OR
11. 有 DAO 层却绕过 `queryChain()` 直接创建 `QueryChain.of(...)`
12. 有查询对象却不实现 `QO`，改在 Service 中手工拼条件
13. 有 DAO 层却把数据库操作 SQL 代码放在 Service 层
14. Controller / API 直接返回实体类，或为响应字段污染实体
15. 本可用 `@Fetch` 的场景机械使用 join
16. join 没有先 `.from(...)`，或继续使用旧式 / 字符串 join 写法
17. 手工一个一个 `select` 列，本可直接 `select(VO.class)` 却堆大量字段
18. 1 对多分页场景继续使用 `leftJoin` 却不处理 `rightJoin()` 或关闭 join 优化
19. QO 已适合对象转条件，却不使用 `@ConditionTarget` 体系和 `WhereUtil.where(this)`
20. `.as(...)` 明明可以使用 getter / 字段引用，却默认退回字符串别名
21. VO、QO 中存在非数据库操作字段，却没有使用 `@Ignore` 或 `@Ignores`
