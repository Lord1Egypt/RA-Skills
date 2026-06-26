---
name: xbatis-skills
description: 用于 xbatis 框架项目的接入、解释、生成、修改和排障；覆盖 MybatisMapper、BasicMapper、QueryChain、InsertChain、UpdateChain、DeleteChain、@Table/@TableId/@TableField、@ResultEntity、@ConditionTarget、dbAdapt、多租户、逻辑删除、乐观锁、分表、XML 整合、分页与 AI 代码生成约定。 Use when working on xbatis framework code, docs, or usage questions.
---

# xbatis-skills

在 xbatis 项目中工作时使用此 skill。

## 基本原则

- 以当前仓库源码为第一事实来源，`README.zh-CN.md` 为第二来源，`README.md` 为第三来源。
- 生成代码时，如果不知道类路径、真实类名、方法名、注解包名或泛型签名，禁止猜测；必须先用本地 xbatis 源码搜索确认。
- README 中有少量“概念包名”，生成代码时以源码里的真实包名为准：
  - `cn.xbatis.core.XbatisGlobalConfig`
  - `cn.xbatis.core.mybatis.mapper.MybatisMapper`
  - `cn.xbatis.core.mybatis.mapper.BasicMapper`
  - `cn.xbatis.core.mybatis.typeHandler.EnumSupport`
  - `cn.xbatis.core.sql.executor.chain.QueryChain`
  - `cn.xbatis.core.sql.executor.chain.InsertChain`
  - `cn.xbatis.core.sql.executor.chain.UpdateChain`
  - `cn.xbatis.core.sql.executor.chain.DeleteChain`
  - `cn.xbatis.db.annotations.*`
  - `cn.xbatis.listener.annotations.OnInsert`
  - `cn.xbatis.listener.annotations.OnUpdate`
- 优先使用框架内建能力：Mapper 默认 CRUD、链式 DSL、对象条件、结果映射、`dbAdapt`、`withSqlSession`。只有这些表达不了时再退回原生 SQL。
- 保持现有 Mapper 风格：
  - 已经是实体 Mapper 的代码库，不要无故切到单 Mapper。
  - 已经是 `BasicMapper` 单 Mapper 模式的代码库，不要重新为每个实体补一层 Mapper。
- 单 Mapper 模式下只定义统一 `BasicMapper` 子接口并配置扫描，不需要主动调用 `XbatisGlobalConfig.setSingleMapperClass(...)`。
- 持久化枚举必须实现 `EnumSupport<T>` 并通过 `getCode()` 提供数据库存储值；生成枚举时同步提供 `of(T code)` 方法，找不到匹配项返回 `null`。
- DAO 注入收敛在项目 BaseDao 的 `setMapper(...)` 上，并加当前容器框架的自动注入注解；BaseDao 子类只继承，不重复重写 `setMapper(...)`。
- DAO 层必须创建业务 DAO 接口，接口继承 `cn.xbatis.core.mvc.Dao<T, ID>`；实现类继承项目 BaseDao 并实现该接口，不继承 `IDao<T, ID>`。
- 基础按 id、save、update 方法强烈建议保持和框架 Dao / BaseDao / 内置 Mapper 的真实方法名和签名一致。
- 业务 DAO 不建议写与 BaseDao / 内置 Mapper 重复的简单方法，只保留有业务语义、组合查询、事务边界或复用价值的方法。
- 开发环境必须开启 xbatis POJO 安全检查；测试和生产环境不要求默认开启，除非项目明确要求。

## 使用流程

1. 先识别接入方式：Spring Boot 2、Spring Boot 3、Solon，或仅使用 MyBatis。
2. 再识别 Mapper 组织方式：
   - 默认模式：每个实体一个 `MybatisMapper<T>`
   - 单 Mapper 模式：自定义接口继承 `BasicMapper`
3. 按需求选最窄能力：
   - 普通 CRUD：优先 Mapper 默认方法
   - 组合查询：`QueryChain`
   - 复杂写入或 `RETURNING`：`InsertChain` / `UpdateChain` / `DeleteChain`
   - 复杂复用 SQL：XML + `withSqlSession`
4. 生成代码时遵循这些约定：
   - 优先使用 Lambda 属性引用，不写硬编码字段名
   - 搜索类条件优先 `.forSearch(true)` 或带 predicate 的条件重载，不手写大量 `if/else`
   - `returnType(...)` 放在终止方法前，保持调用链统一
   - 需要数据库函数时优先 `import static db.sql.api.impl.cmd.Methods.*`
   - 不知道类路径或类名时先查本地源码，不把猜测写成确定代码
5. 文档与源码不一致时，明确说明采用了哪个真实类或包名。

## 按需读取引用文件

- 接入、模块划分、全局配置：看 `references/setup.md`
- 实体注解、Mapper 组织、CRUD 约定：看 `references/entity-and-mapper.md`
- DSL、对象条件、结果映射：看 `references/query-dsl.md`
- 多库、多租户、逻辑删除、分表、XML、分页、代码生成与安全检查：看 `references/advanced.md`

## 输出要求

- 回答时优先给出可直接落地的 xbatis 写法，不要泛泛解释 ORM 概念。
- 如果某项能力只在 README 中出现、当前仓库源码里没有对应类型，标注为“README 接入约定”或“外部 starter 能力”。
- 代码示例默认简洁、显式、可维护，不额外引入抽象层。
