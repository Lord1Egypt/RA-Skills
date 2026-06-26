# Framework Features

适用于以下场景：

- 逻辑删除
- 多租户
- 乐观锁
- 动态值和默认值
- 结果映射和枚举展示
- 对象转条件 / 对象转排序

## 逻辑删除

要点：

- 使用逻辑删除注解，而不是手工写删除标记条件
- 注意 `DeleteChain` 删除时逻辑删除不会生效
- DAO 内部创建 `DeleteChain` 时使用 `deleteChain()` / `deleteChain(where)`
- 可以通过全局拦截器补额外字段，例如删除人、删除时间
- 存在全局开关和局部开关

Agent 规则：

1. 如果项目使用逻辑删除，优先复用框架能力
2. 如果需求是“查已删除数据”，先检查是否应局部关闭逻辑删除
3. 不要在普通查询里反复手工拼 `deleted = 0`
4. 不要把 `deleteChain()` 当成逻辑删除入口；需要逻辑删除语义时优先使用框架删除方法

## 多租户

要点：

- 围绕实体类自动注入租户条件
- 常见于 `from`、`join`、`delete`、`update`
- DAO 内部创建 `QueryChain` / `UpdateChain` / `DeleteChain` 时使用框架方法，减少漏传 Mapper 或实体类型的风险
- 租户值通常通过 `TenantContext.registerTenantGetter(...)` 获取

Agent 规则：

1. 租户字段优先用 `@TenantId`
2. 查询、更新、删除优先走框架租户能力
3. 不要在业务代码里遍地补 `tenant_id`
4. 如果项目通过 `ThreadLocal` 提供租户值，保持现有上下文传递方式

## 乐观锁

要点：

- `save` 时版本字段自动初始化
- `update(实体类)`、`delete(实体类)` 自动追加版本条件

Agent 规则：

1. 需要并发写保护时优先使用 `@Version`
2. 不要手工给每个 update 写版本判断逻辑

## 动态值 / 默认值

适合场景：

- 创建时间
- 修改时间
- 创建人
- 修改人
- 时间区间动态默认值

Agent 规则：

1. 优先用框架动态值和插入/更新事件
2. 不要在 Controller / Service 层重复填这些审计字段
3. 创建时间字段优先使用 `@TableField(defaultValue = "{NOW}", update = false)`
4. 修改时间字段优先使用 `@TableField(defaultValue = "{NOW}", updateDefaultValue = "{NOW}", updateDefaultValueFillAlways = true)`
5. 普通字段无特殊语义时，不要为了声明列名机械补 `@TableField`
6. 无特殊要求时项目必须集成 Lombok，并在实体类上优先使用 `@FieldNameConstants`
7. 实体类只保留数据库表字段，禁止混入非数据库表字段

## 结果映射 / 枚举展示

Agent 规则：

1. 返回 VO 时，优先让框架自动映射，而不是手工 copy
2. 需要返回枚举名称时，优先使用 `@PutEnumValue`
3. 持久化枚举必须实现 `cn.xbatis.core.mybatis.typeHandler.EnumSupport<T>`，通过 `getCode()` 提供数据库存储值
4. 生成持久化枚举时必须提供 `of(T code)` 静态方法，按 `code` 匹配，找不到时返回 `null`
5. 枚举字段类型 `T` 按数据库实际存储类型选择，不要默认使用 `ordinal()` 或 `name()`
6. 不要为了展示字段把实体类硬改成接口响应模型
7. 实体类注解只能写在实体类上，禁止写在 VO、DTO、QO、Model 等其他类上
7. VO 优先使用真实存在的结果映射注解，例如 `@ResultEntity`、`@NestedResultEntity`、`@NestedResultEntityField`、`@ResultCalcField`
8. 注解里只要有字段依赖，优先使用 Lombok `@FieldNameConstants` 生成的 `Fields` 常量，例如 `SysUser.Fields.id`
9. VO 中凡是不是数据库操作字段、需要忽略的字段，优先使用 `@Ignore` 或 `@Ignores`

## 修改入参 / 更新字段范围

Agent 规则：

1. 修改操作优先使用 Model 类作为传参载体
2. Model 可以像实体类一样直接参与 `save`、`update`
3. 根据接口语义缩小允许修改的字段范围
4. 更新时只更新本次业务真正允许变化的字段
5. 不要把查询实体、响应 VO 或全量实体直接作为修改入参使用
6. 不要因为前端传了字段就默认全部参与 update
7. Model 中凡是不是数据库操作字段、需要忽略的字段，优先使用 `@Ignore` 或 `@Ignores`
8. 单条数据如果是“先查询出来，再改部分字段”的场景，优先使用 `partialUpdate(...)` 精准修改

## 对象转条件 / 对象转排序

适合场景：

- 搜索表单
- 后台筛选
- 动态排序
- 复杂条件对象

Agent 规则：

1. 查询对象优先实现 `cn.xbatis.core.mvc.QO`
2. `QO.where()` 负责集中构建 `Where`
3. 条件对象优先声明 `@ConditionTarget`
4. 字段条件优先使用 `@Condition`、`@Conditions`、`@ConditionGroup`
5. `QO.where()` 中优先使用 `WhereUtil.where(this)`
6. DAO 方法优先接收查询对象并使用 `queryChain(qo.where())`
7. 搜索对象优先映射成条件对象
8. 多列关键字搜索优先使用条件注解体系
9. 多字段排序优先使用对象转排序
10. 非搜索查询需要按值忽略条件时，优先使用 predicate 重载，例如 `.eq(SysUser::getId, id, Objects::nonNull)`
11. 无法使用 predicate 重载时，再使用 boolean `when` 重载，例如 `.eq(Objects.nonNull(id), SysUser::getId, id)`
12. 需要括号包裹一组条件，尤其组内存在 `or` 条件时，使用 `.nested(chain -> ...)`
13. 条件拼接默认是 `and`；调用 `.or()` 后会持续使用 `or`，需要切回时调用 `.and()`
14. 局部 `or` 条件优先放进 `.nested(...)`，避免 `.or()` 状态影响后续外层条件
15. 不要为动态筛选写一长串 `if`
16. 有 DAO 层时，不要把 where 构建散落到 Service 层
17. 有 DAO 层时，不要在 Service / Controller 手工拼 `order by`
18. 使用 `Methods` 风格时，优先静态导入所需方法
19. 方法嵌套优先写成 `eq(gt(...))` 这类形式，避免混用多种调用风格
20. QO 中凡是不是数据库操作字段、需要忽略的字段，优先使用 `@Ignore` 或 `@Ignores`
