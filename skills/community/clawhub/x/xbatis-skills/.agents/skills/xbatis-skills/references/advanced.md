# 多库、租户、分页与高级能力

## 多数据库差异化

`QueryChain` / `InsertChain` / `UpdateChain` / `DeleteChain` 以及 Mapper 都支持 `dbAdapt(...)`。

适用场景：

- 同一逻辑在 MySQL、PostgreSQL、H2、SQL Server 上要生成不同 SQL
- 冲突处理、分页、函数调用需要按库区分

默认做法：

- 先用统一 DSL
- 只有数据库方言差异真的存在时，再包一层 `dbAdapt(...)`

## 动态数据源

README 记录了外部能力 `cn.xbatis:xbatis-datasource-routing`：

- 支持 `@DS("master")`
- 支持主从、分组、连接池与配置解密
- 事务切换时要注意传播行为

这部分属于外部扩展，不在当前仓库模块内实现，使用前先确认依赖是否已接入。

## 多租户

真实类型：

- 注解：`cn.xbatis.db.annotations.TenantId`
- 上下文：`cn.xbatis.core.tenant.TenantContext`

常见约定：

- 实体租户字段标 `@TenantId`
- 启动阶段注册 `TenantContext.registerTenantGetter(...)`
- 需要临时关闭时，让 getter 返回 `null`，或在上层做显式控制

## 逻辑删除

真实类型：

- 注解：`@LogicDelete`、`@LogicDeleteTime`
- 开关：`cn.xbatis.core.logicDelete.LogicDeleteSwitch`
- 工具：`cn.xbatis.core.logicDelete.LogicDeleteUtil`

要点：

- Mapper 删除方法会走逻辑删除能力
- `DeleteChain` 默认是物理删除
- 可用 `XbatisGlobalConfig.setLogicDeleteInterceptor(...)` 补充删除人等字段
- 局部关闭逻辑删除可用 `LogicDeleteSwitch.with(false)` 或 `LogicDeleteUtil.execute(false, ...)`

## 乐观锁

真实注解：`cn.xbatis.db.annotations.Version`

行为约定：

- `save` 时默认写入初始版本
- `update` / `delete` 会带上版本条件
- 成功更新后自动递增

## 分表

真实类型：

- `@SplitTable`
- `@SplitTableKey`
- `TableSplitter`

要点：

- `TableSplitter#support(Class<?>)` 声明支持的分片键类型
- `TableSplitter#split(String, Object)` 计算真实表名
- 链式查询和更新与普通实体基本一致
- 条件中必须带上分表键，否则无法定位真实表

## 自关联 Join

同一实体表参与两次查询时，用 `storey` 区分主表和第二张同实体表。

```java
List<SysUser> list = QueryChain.of(sysUserMapper)
        .innerJoin(SysUser::getId, 1, SysUser::getParentId, 2)
        .list();
```

要点：

- `1` 表示主查询中的 `SysUser`，`2` 表示第二次参与 join 的 `SysUser`
- 生成自关联代码前，必须确认关联字段真实存在，例如 `id`、`parentId`

## Join 子查询高级写法

框架会根据 `innerJoin(...)` 前两个 getter 自动生成核心等值 `ON` 条件。

不需要追加 `ON` 条件时，用 `(query, subQuery)`：

```java
List<SysUser> list = QueryChain.of(sysUserMapper)
        .from(SysUser.class)
        .innerJoin(SysUser::getRole_id, SysRole::getId, (query, subQuery) -> {
            subQuery.select(SysRole::getName);
            query.select(subQuery, SysRole::getName);
            query.orderBy(subQuery, SysRole::getId);
        })
        .list();
```

需要追加 `ON` 条件时，用 `(query, subQuery, on)`：

```java
List<SysUser> list = QueryChain.of(sysUserMapper)
        .from(SysUser.class)
        .innerJoin(SysUser::getRole_id, SysRole::getId, (query, subQuery, on) -> {
            subQuery.select(SysRole::getId, SysRole::getName);
            query.select(subQuery, SysRole::getName);
            query.orderBy(subQuery, SysRole::getId);
        })
        .list();
```

要点：

- `(query, subQuery)` 适合只调整子查询 select、外层 select、排序等内容
- `(query, subQuery, on)` 适合在自动生成的核心 `ON` 条件之外追加条件
- 生成代码时必须确认主表字段、子查询字段和 VO 映射字段真实存在

## In / Exists 子查询

优先使用 xbatis 的便捷子查询重载，不要手写 SQL 字符串。

`in` 子查询：

```java
List<SysRole> list = QueryChain.of(sysRoleMapper)
        .in(SysRole::getId, SysUser::getRole_id, (query, inQuery) -> {
            inQuery.like(SysUser::getPassword, "123456");
        })
        .list();
```

相关子查询 `in`：

```java
List<SysRole> list = QueryChain.of(sysRoleMapper)
        .in(SysRole::getId, SysUser::getRole_id, SysRole::getId, SysUser::getRole_id)
        .list();
```

`exists` 子查询：

```java
int count = QueryChain.of(sysUserMapper)
        .exists(SysUser::getRole_id, SysRole::getId, existsQuery -> {
            existsQuery.isNotNull(SysRole::getId);
        })
        .count();
```

`notExists` 子查询：

```java
int count = QueryChain.of(sysUserMapper)
        .notExists(SysUser::getRole_id, SysRole::getId)
        .count();
```

复杂相关子查询可用 `SubQuery.create()`：

```java
import cn.xbatis.core.sql.executor.SubQuery;

List<SysUser> list = QueryChain.of(sysUserMapper)
        .connect(query -> query.exists(SubQuery.create()
                .select1()
                .from(SysUser.class)
                .eq(SysUser::getId, query.$(SysUser::getId))
                .isNotNull(SysUser::getPassword)
                .limit(1)))
        .list();
```

要点：

- `in(sourceGetter, selectGetter, consumer)` 会构建 `sourceGetter in (select selectGetter ...)`
- 四 getter 的 `in(sourceGetter, selectGetter, sourceEqGetter, targetEqGetter)` 用于相关子查询等值关联
- `exists(sourceGetter, targetGetter, consumer)` / `notExists(...)` 会按两个 getter 自动构建关联子查询
- `notIn(...)` 与 `in(...)` 同形态；复杂场景再退到 `SubQuery.create()`

## SQL 函数与模板

优先静态导入：

```java
import static db.sql.api.impl.cmd.Methods.*;
```

常用能力：

- 聚合和数学函数：`count`、`sum`、`avg`、`round`、`pow`
- 字符串函数：`concat`、`upper`、`lower`、`substring`
- 日期函数：`currentDate`、`dateDiff`、`dateAdd`、`year`、`month`、`day`、`hour`、`minute`、`second`
- 模板：
  - `tpl(...)`：普通 SQL 片段模板，返回 `CmdTemplate`
  - `fTpl(...)`：函数表达式模板，返回 `FunTemplate`，可继续 `.as(...)`、`.gt(...)` 等
  - `cTpl(...)`：条件模板，返回 `ConditionTemplate`，用于 `where` / `having`

默认策略：

- 能用标准函数就不用模板
- 模板只在表达复杂片段时使用，避免 SQL 字符串到处散落
- 模板占位符用 `{0}`、`{1}` 传入字段和值，不要把用户输入拼进模板 SQL 字符串
- 单列模板直接用普通 `Getter` 方法；多列模板才用 `db.sql.api.cmd.GetterFields.of(...)`
- 生成代码前必须确认实体、VO、Mapper、字段 getter 和返回字段真实存在；示例类名不能直接照抄

SQL 模板示例按“单列 / 多列”拆开写，再分别给 `select`、`where`、`groupBy`、`orderBy`、`having` 小例子。下面类名和字段只是形态示例，生成时必须替换为项目真实类型。

通用 import：

```java
import cn.xbatis.core.sql.executor.chain.QueryChain;
import db.sql.api.cmd.GetterFields;
import db.sql.api.impl.cmd.basic.OrderByDirection;

import static db.sql.api.impl.cmd.Methods.*;
```

### 单列模板

字段表达式只引用一个字段时，直接用普通 `Getter`。

`select` 示例：

```java
QueryChain.of(sysUserMapper)
        .select(SysUser::getId,
                c -> fTpl("count({0})", c).as(UserStatVo::getUserCount))
        .returnType(UserStatVo.class)
        .list();
```

`where` 示例：

```java
QueryChain.of(sysUserMapper)
        .where(SysUser::getUserName,
                c -> cTpl("{0} like {1}", c, "%" + keyword + "%"));
```

`groupBy` 示例：

```java
QueryChain.of(sysUserMapper)
        .select(SysUser::getRoleId)
        .select(SysUser::getCreatedAt,
                c -> fTpl("date({0})", c).as(UserStatVo::getStatDay))
        .groupBy(SysUser::getRoleId)
        .groupBy(SysUser::getCreatedAt,
                c -> fTpl("date({0})", c))
        .returnType(UserStatVo.class)
        .list();
```

`orderBy` 示例：

```java
QueryChain.of(sysUserMapper)
        .orderBy(OrderByDirection.DESC,
                SysUser::getScore,
                c -> fTpl("coalesce({0}, 0)", c));
```

`having` 示例：

```java
QueryChain.of(sysUserMapper)
        .having(SysUser::getScore,
                c -> fTpl("sum({0})", c).gt(minScore));
```

### 多列模板

表达式同时引用两个或更多字段时，再用 `GetterFields.of(...)`。

`select` 示例：

```java
QueryChain.of(sysUserMapper)
        .select(GetterFields.of(SysUser::getScore, SysUser::getExtraScore),
                cs -> fTpl(
                        "coalesce({0}, 0) + coalesce({1}, 0)",
                        cs[0],
                        cs[1]
                ).as(UserStatVo::getTotalScore))
        .returnType(UserStatVo.class)
        .list();
```

`where` 示例：

```java
QueryChain.of(sysUserMapper)
        .where(GetterFields.of(SysUser::getUserName, SysUser::getNickName),
                cs -> cTpl(
                        "({0} like {2} or {1} like {2})",
                        cs[0],
                        cs[1],
                        "%" + keyword + "%"
                ));
```

`groupBy` 示例：

```java
QueryChain.of(sysUserMapper)
        .select(GetterFields.of(SysUser::getProvinceCode, SysUser::getCityCode),
                cs -> fTpl(
                        "coalesce({0}, {1})",
                        cs[0],
                        cs[1]
                ).as(UserStatVo::getAreaCode))
        .groupBy(GetterFields.of(SysUser::getProvinceCode, SysUser::getCityCode),
                cs -> fTpl("coalesce({0}, {1})", cs[0], cs[1]))
        .returnType(UserStatVo.class)
        .list();
```

`orderBy` 示例：

```java
QueryChain.of(sysUserMapper)
        .orderBy(OrderByDirection.DESC,
                GetterFields.of(SysUser::getScore, SysUser::getExtraScore),
                cs -> fTpl(
                        "coalesce({0}, 0) + coalesce({1}, 0)",
                        cs[0],
                        cs[1]
                ));
```

`having` 示例：

```java
QueryChain.of(sysUserMapper)
        .having(GetterFields.of(SysUser::getScore, SysUser::getExtraScore),
                cs -> fTpl(
                        "sum(coalesce({0}, 0) + coalesce({1}, 0))",
                        cs[0],
                        cs[1]
                ).gt(minScore));
```

使用要点：

- 动态普通条件优先用 `.eq(when, getter, value)`、`.like(when, getter, value)` 等内置方法；只有跨字段表达式或框架函数未覆盖时才用 `cTpl(...)`。
- 示例默认不写 `boolean when`；只有需要动态开关时，才使用 `select(boolean, ...)`、`where(boolean, ...)`、`groupBy(boolean, ...)` 等重载。
- 单列表达式用 `select(getter, fn)`、`where(getter, fn)`、`groupBy(getter, fn)`；多列表达式才用 `GetterFields.of(...)`。
- `having` 默认推荐用 `.having(...)`；只有需要显式切换连接关系时，才使用 `.havingAnd(...)` 或 `.havingOr(...)`。
- 部分函数有数据库差异时，结合 `dbAdapt(...)` 处理。

## XML 整合

单 Mapper 模式下，可通过 `withSqlSession(...)` 调用 XML：

- 命名空间通常是 `MybatisBasicMapper`
- statement 命名可按 `EntityName:method`

适合场景：

- 已有复杂 XML 资产
- 特殊 SQL 很难用 DSL 表达
- 需要和现有 MyBatis 语句直接复用

## 分页与性能

真实分页类型是 `cn.xbatis.core.mybatis.mapper.context.Pager`。

建议：

- 用 `Pager.of(pageNo, pageSize)` 驱动分页
- 默认信任框架的分页优化能力
- 遇到特殊数据库分页语法，再通过 `XbatisGlobalConfig.setPagingProcessor(...)` 定制

README 说明框架会自动优化：

- `COUNT(*)`
- 冗余 `LEFT JOIN`
- 冗余 `ORDER BY`

## 代码生成与安全检查

README 中记录了两类能力，但当前仓库源码未直接提供实现：

- `GeneratorConfig`
- `org.mybatis.spring.boot.autoconfigure.XbatisPojoCheckScan`

因此使用时要区分：

- 可以把它们当成 xbatis 生态里的“接入约定”
- 不能把它们当成当前仓库源码已存在的类型

AI 生成代码时的默认建议：

- 开发环境必须启用 POJO 安全检查；测试和生产环境不要求默认开启
- Spring / Spring Boot 优先使用当前 starter 支持的 `@XbatisPojoCheckScan`，生成 import 前先确认真实包名
- Solon 优先在开发环境配置的 `mybatis.<beanName>.pojoCheck` 下声明扫描包
- 显式配置 `databaseId`
- 查询接口优先 `.forSearch(true)`
- VO 优先 `@ResultEntity` 驱动
- 日志排查时开启 `cn.xbatis` 的 `trace`
