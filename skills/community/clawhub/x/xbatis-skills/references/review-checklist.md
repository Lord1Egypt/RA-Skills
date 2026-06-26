# Review Checklist

适用于以下任务：

- 审查现有 xbatis 代码
- 发现实现是否偏离 xbatis 风格
- 排查潜在 bug、性能问题、映射错误、分页风险、租户隔离遗漏
- 在 PR Review 中判断代码是否“像 xbatis”

## 审查目标

审查时，优先关注以下问题：

1. 这段代码是否优先使用了 xbatis 原生能力
2. 是否错误回退到了 XML、原生 SQL、手工字符串拼接
3. 是否存在分页、联表、映射、租户、逻辑删除、乐观锁方面的隐患
4. 是否引入了与项目现有 xbatis 风格冲突的写法

不要把审查重点放在：

- 命名偏好
- 纯个人风格差异
- 与功能无关的轻微格式问题

## 审查顺序

按以下顺序检查：

1. 实现路径是否合理
2. 查询构造是否符合 xbatis 习惯
3. 返回对象与映射是否正确
4. 分页和 join 是否存在语义或性能风险
5. 框架特性是否被正确使用
6. 是否存在安全性和一致性问题

## 1. 实现路径检查

先判断当前实现是不是走对了路线。

### 通过信号

- 开启 xbatis 任务后，先从 `https://github.com/xbatis/xbatis` 或 `https://gitee.com/xbatis/xbatis` 下载了 xbatis 源码，并基于本地源码分析用法
- 简单 CRUD 使用 DAO / 内置 Mapper 方法
- 默认有 DAO 层，Service 不直接创建 Chain
- 单 Mapper 项目 BaseDao 继承 `BasicDaoImpl<T, ID>`
- 多 Mapper 项目 BaseDao 继承 `DaoImpl<T, ID>`
- 业务 DAO 接口继承 `cn.xbatis.core.mvc.Dao<T, ID>`
- 业务 DAO 实现类继承项目 BaseDao，并实现对应业务 DAO 接口
- 业务 DAO 没有编写与 BaseDao、DAO 基础方法或内置 Mapper 方法等价的简单转发方法
- 基础按 id、save、update 方法保持框架 `Dao<T, ID>` / BaseDao / 内置 Mapper 的真实方法名和签名
- 有 DAO 层时，事务强烈推荐定义在 DAO 方法上
- 按 id 查询实体或单表部分列使用 `getById`
- 按 id 查询单列值使用 `getValueById`
- 标准查询在 DAO 内使用 `queryChain()`
- `UpdateChain` / `InsertChain` / `DeleteChain` 在 DAO 内通过 `updateChain()` / `insertChain()` / `deleteChain()` 创建
- 适合“先查 A，顺带带出 B”的场景优先使用 `@Fetch`
- join 场景先 `.from(...)` 明确主表，并优先使用方法引用 join 写法
- 联表返回使用 VO 或映射类
- 联表 VO 优先 `select(VO.class)` / `returnType(VO.class)`，需要枚举名称时优先 `@PutEnumValue`
- 实体普通字段没有机械补 `@TableField("列名")`
- 创建时间字段优先使用 `@TableField(defaultValue = "{NOW}", update = false)`
- 修改时间字段优先使用 `@TableField(defaultValue = "{NOW}", updateDefaultValue = "{NOW}", updateDefaultValueFillAlways = true)`
- 持久化枚举实现 `cn.xbatis.core.mybatis.typeHandler.EnumSupport<T>`，并提供稳定的 `getCode()` 和找不到返回 `null` 的 `of(T code)`
- 无特殊要求时项目已集成 Lombok，实体或条件对象优先使用 `@FieldNameConstants`
- 条件对象优先使用 `@ConditionTarget` 体系，并在 `where()` 中使用 `WhereUtil.where(this)`
- 项目 BaseDao 的 `setMapper(...)` 带 Spring、Solon 等容器自动注入注解，业务 DAO 子类不重复重写 `setMapper(...)`
- VO、QO、Model 中非数据库操作字段使用 `@Ignore` 或 `@Ignores`
- 实体类保持单一性，不混入非数据库表字段
- 复杂表达先尝试 SQL 模板，再考虑 XML
- Mapper 组织方式与项目当前的单 Mapper / 多 Mapper 模式一致
- 单 Mapper 模式下没有主动调用 `XbatisGlobalConfig.setSingleMapperClass(...)`
- 不知道类路径、真实类名、方法名、注解包名或泛型签名时，先基于本地 xbatis 源码确认，没有凭空猜测

### 风险信号

- 不知道 xbatis 如何使用时，没有从本地 xbatis 源码目录分析使用方法
- 不知道类路径、真实类名、方法名、注解包名或泛型签名时，直接凭经验生成代码
- 简单 CRUD 却写了大量 XML
- 普通列表页在 Service 层拼 SQL
- 有 DAO 层却把事务主要开在 Service 层
- 只是 where 条件动态，就直接退回 XML
- 联表结果查出实体后再手工 copy 成 VO
- 在单 Mapper 项目中混入多 Mapper 写法，或反之
- 单 Mapper 项目 BaseDao 继承了 `DaoImpl`
- 多 Mapper 项目 BaseDao 继承了 `BasicDaoImpl`
- 业务 DAO 到处直接继承 `BasicDaoImpl` / `DaoImpl`，没有项目级 BaseDao
- 业务 DAO 没有接口，或接口没有继承 `Dao<T, ID>`
- 业务 DAO 接口继承了源码注释不建议开发者使用的 `IDao<T, ID>`
- 业务 DAO 堆满 `getById`、`save`、`update`、`deleteById`、`count`、`exists` 这类基础能力的简单转发方法
- 基础方法被二次命名为 `findById`、`create`、`modify`，偏离框架 Dao / BaseDao 真实 API
- 按 id 查询实体、部分列或单列值时默认写 `QueryChain`
- 有 DAO 层却在 Service / Controller 中直接写 `QueryChain.of(...)` 或其他 `Chain.of(...)`
- 本可用 `@Fetch` 的场景机械使用 join
- join 没有先 `.from(...)`，或继续使用旧式 / 字符串 join 写法
- 联表返回手工一个一个 `select` 列，本可直接 `select(VO.class)` 却堆大量字段
- 普通字段明明不需要特殊语义，却机械补满 `@TableField("列名")`
- 创建时间、修改时间没有复用 `@TableField` 的动态默认值能力
- 项目已适合对象转条件，却没用 `@ConditionTarget` 体系，或 `where()` 没有优先使用 `WhereUtil.where(this)`
- DAO 注入仍然以构造方法传 Mapper 为主，或每个业务 DAO 子类重复重写 `setMapper(...)`
- 项目 BaseDao 的 `setMapper(...)` 缺少当前容器框架的自动注入注解
- 持久化枚举没有实现 `EnumSupport<T>`，缺少 `of(T code)`，或错误依赖 `ordinal()` / `name()` 作为存储值
- xbatis 注解里继续写字符串字段名，本可使用 `SysUser.Fields.id`
- VO、QO、Model 中存在非数据库操作字段，却没有用 `@Ignore` 或 `@Ignores`
- 实体类混入非数据库表字段

## 2. Chain 与查询构造检查

### 条件拼接

检查：

- 是否优先在 DAO 内用 `queryChain()`
- 适合“先查 A，顺带带出 B”的场景是否优先考虑 `@Fetch`
- 搜索型接口是否合理使用 `forSearch(true)` 或条件对象
- 条件对象是否优先使用 `@ConditionTarget`、`@Condition`、`@Conditions`、`@ConditionGroup`
- `QO.where()` 是否优先使用 `WhereUtil.where(this)`
- 非搜索查询是否避免了机械套用 `forSearch(true)`
- 无法使用 `forSearch(true)` 时，是否优先使用 predicate 重载按值忽略条件
- 无法使用 predicate 重载时，是否使用 boolean `when` 重载
- 含 `or` 的成组条件是否使用 `.nested(...)`
- 调用 `.or()` 后是否在需要时显式 `.and()` 切回
- 使用 join 时是否先 `.from(...)` 并优先采用方法引用 join 形式
- 使用 `Methods` 风格时是否统一静态导入，并采用 `eq(gt(...))` 这类嵌套表达
- 是否把空值处理散落在业务层

重点风险：

- `null` / 空字符串处理不一致
- 非搜索查询被 `forSearch(true)` 改变语义，例如空字符串本应参与唯一性校验却被忽略
- 手工 if 过多，说明本可用对象转条件
- 本可用 `.eq(SysUser::getId, id, Objects::nonNull)`，却在外层写一堆 `if`
- 已有条件对象却不用 `@ConditionTarget` 体系，反而散落手工 where
- `QO.where()` 没有统一优先使用 `WhereUtil.where(this)`
- 需要括号包裹 `or` 条件却没有使用 `.nested(...)`
- 调用 `.or()` 后没有 `.and()` 切回，导致后续条件错误变成 OR
- 使用 `Methods` 时一半静态导入、一半 `Methods.xxx(...)`，导致表达混乱
- Controller / Service 层直接决定 SQL 片段

### 写入 Chain

检查：

- `UpdateChain` 是否通过 DAO 内部 `updateChain()` 创建
- `InsertChain` 是否通过 DAO 内部 `insertChain()` 创建
- `DeleteChain` 是否通过 DAO 内部 `deleteChain()` 创建
- Chain 是否与当前单 Mapper / 多 Mapper 模式一致
- DAO 层是否有业务 DAO 接口，且接口继承 `Dao<T, ID>` 而不是 `IDao<T, ID>`
- 业务 DAO 实现类是否继承项目 BaseDao 并实现对应接口
- 修改操作是否使用 Model 类作为传参载体
- Model 是否允许直接参与 `save`、`update`
- update 字段范围是否只覆盖本次业务允许变化的字段
- 项目 BaseDao 是否通过带容器自动注入注解的 `setMapper(...)` 注入 Mapper
- 业务 DAO 实现类是否避免重复定义 Mapper 字段、构造器注入或 `setMapper(...)`
- 基础按 id、save、update 方法是否保持框架真实命名和签名
- Model 中非数据库操作字段是否使用 `@Ignore` 或 `@Ignores`
- 单条数据先查后改的场景是否优先使用 `partialUpdate(...)`
- `UpdateChain`、`InsertChain`、`DeleteChain` 是否最终调用 `execute()`

重点风险：

- 在 Service / Controller 里直接创建 `UpdateChain.of(...)`、`InsertChain.of(...)`、`DeleteChain.of(...)`
- 单 Mapper 模式下漏传实体类型或混入实体 Mapper
- 多 Mapper 模式下绕过 DAO 直接依赖具体 Mapper
- 业务 DAO 没有接口，或接口继承 `IDao<T, ID>` 而不是 `Dao<T, ID>`
- 把查询实体、响应 VO 或全量实体直接作为修改入参
- 因为前端传了字段就默认全部参与 update
- 项目已有统一 BaseDao 注入规范，却继续使用构造方法传 Mapper，或每个业务 DAO 子类重复重写 `setMapper(...)`
- 把不参与数据库操作的 Model 字段直接带进 save / update 语义
- 单条数据先查后改时，本可精准修改，却直接对查出的实体走普通 `update(entity)`
- 创建了写入 Chain，却漏掉最终的 `execute()`

### 排序

检查：

- 是否使用框架排序能力
- 排序字段是否来自受控字段或对象转排序

重点风险：

- 直接拼接排序 SQL，存在注入和维护风险

### count / exists

检查：

- 是否调用框架对应能力，而不是重复写 SQL

重点风险：

- 手工维护 count 查询，和主查询条件不一致

## 3. 返回对象与映射检查

### 返回对象选择

检查：

- Controller / API 是否优先返回 VO，而不是直接返回实体类
- 后台管理系统的列表、详情 VO 是否可按项目风格考虑继承实体类
- 非后台管理系统是否避免直接返回实体类
- 展示型、联表型、聚合型查询是否返回 VO
- DAO 内部实体返回是否没有直接穿透到接口响应

重点风险：

- 返回实体后再手工 copy 为 VO
- 为了兼容前端临时字段，把实体类污染成展示对象
- Controller / API 直接返回实体类，导致持久化结构和接口契约耦合
- 在 VO、DTO、QO、Model 等非实体类上使用实体类注解
- VO 中非数据库操作字段没有使用 `@Ignore` 或 `@Ignores`

### 映射准确性

检查：

- `returnType(VO.class)` 是否与 select 结果匹配
- 返回 VO 时是否优先 `select(VO.class)`，以及 `returnType` 与 `select` 一致时是否避免重复写 select
- 是否依赖自动列推导而非重复 select 全量列
- VO 类是否按项目习惯配合 `@ResultEntity` 等结果映射注解
- 需要时是否使用结果映射注解
- 需要枚举名称时是否优先使用 `@PutEnumValue`
- 实体类注解是否只出现在实体类上
- `.as(...)` 是否优先使用 getter / 字段引用形式
- 注解里的字段依赖是否优先使用 `Fields` 常量
- VO 中非数据库操作字段是否正确忽略

重点风险：

- 返回字段缺失
- 字段别名与 VO 不匹配
- 手工一个一个 `select` 列，导致字段维护成本过高
- 手工映射逻辑重复、易漏字段
- 在非实体类上误用实体类注解，导致语义混乱
- 可以用 `.as(SysUser::getId)` 或 `.as(SysUserVo::getId)` 却退回 `.as("id")`
- 注解里大量硬编码字符串字段名，导致重构脆弱
- 返回模型里需要忽略的字段没有标注 `@Ignore` / `@Ignores`

## 4. 分页与 join 风险检查

### 分页

检查：

- 是否统一使用 `paging(Pager)`
- 是否重复手写 limit / count

重点风险：

- 分页逻辑和 count 逻辑脱节
- 手工分页器与项目统一分页器冲突

### join

检查：

- join 是否真的必要
- 若只是查询 A 时顺带带出 B，是否本可改用 `@Fetch`
- 是否先 `.from(...)` 明确主表
- ON 条件是否明确
- 左联分页是否考虑 1 对多场景

重点风险：

- `leftJoin` + 分页 在 1 对多时导致结果异常或总数异常
- 1 对多分页仍然坚持 `leftJoin`，却没有改用 `rightJoin()` 或关闭 join 优化
- join 条件遗漏，造成笛卡尔积或结果放大
- 依赖旧式不推荐写法，后期难维护

## 5. 框架特性检查

### 开发环境安全检查

检查：

- 开发环境是否开启 xbatis POJO 安全检查
- 安全检查扫描范围是否覆盖 VO、Model、QO、排序对象所在包
- 安全检查扫描范围是否只选择一种方案：`basePackages` 或细分包路径，不要两套同时配置
- Spring / Spring Boot 使用 `@XbatisPojoCheckScan` 时，import 是否已按当前 starter 依赖确认真实包名
- Solon 是否在开发环境配置的 `mybatis.<数据源 bean 名称>.pojoCheck` 下声明扫描包
- 测试和生产环境是否避免默认开启安全检查，除非项目明确要求

重点风险：

- 开发环境未开启安全检查，导致 VO、Model、条件对象、排序对象的映射问题延后到运行期暴露
- 只扫描实体包，漏掉真正需要检查的 VO / Model / QO / OrderBy 包
- 同时配置 `basePackages` 和细分包路径，导致扫描范围语义不清
- 未确认 starter 真实类型就凭 README 包名直接生成 import
- 在项目未要求时为 test/prod 默认开启安全检查，增加不必要的启动开销

### 逻辑删除

检查：

- 项目如果启用了逻辑删除，当前查询是否正确复用框架能力

重点风险：

- 手工写 `deleted = 0`
- 使用 `DeleteChain` 但误以为会触发逻辑删除
- 本应走逻辑删除语义的路径直接使用 `deleteChain()`

### 多租户

检查：

- 是否依赖框架租户能力
- 是否保证租户条件不会遗漏

重点风险：

- 在关键查询、更新、删除中漏掉租户隔离
- 手工拼 `tenant_id` 导致局部遗漏

这是高优先级审查项，因为它直接影响数据隔离。

### 乐观锁

检查：

- 是否在需要并发保护的写路径中使用 `@Version`

重点风险：

- 更新覆盖
- 删除或更新未附带版本条件

### 动态值 / 默认值

检查：

- 创建时间、修改时间、操作人是否复用框架动态值体系
- 创建时间是否优先使用 `@TableField(defaultValue = "{NOW}", update = false)`
- 修改时间是否优先使用 `@TableField(defaultValue = "{NOW}", updateDefaultValue = "{NOW}", updateDefaultValueFillAlways = true)`
- 普通字段是否避免机械补 `@TableField("列名")`
- 实体类是否保持只承载数据库表字段

重点风险：

- 分散在 Controller / Service 的重复填充逻辑
- 多处填充规则不一致
- 创建时间被错误允许 update
- 修改时间缺少 `updateDefaultValueFillAlways = true`，导致局部更新时不稳定
- 实体类混入非数据库表字段，导致语义污染

## 6. SQL 模板 / XML / 原生 SQL 检查

### SQL 模板

检查：

- 局部复杂表达是否优先使用 SQL 模板，而不是整段退回原生 SQL
- SQL 模板是否优先通过 `Methods.tpl`、`Methods.fTpl`、`Methods.cTpl` 创建

重点风险：

- 只是少量函数复杂，却把整条查询改成不可维护的原生 SQL
- 需要模板能力，却绕开 `Methods.tpl`、`Methods.fTpl`、`Methods.cTpl` 自己拼模板对象或字符串

### XML / 原生 SQL

检查：

- 是否真的需要 XML
- 是否有更直接的 xbatis 原生表达
- 是否符合 `xml-boundaries` 中定义的允许边界

重点风险：

- 因开发者习惯直接写 XML
- XML 与项目主流 xbatis 风格割裂
- 维护两套查询体系

## 7. 风格一致性检查

检查：

- 是否对齐项目当前使用的 Mapper 模式
- DAO 基类是否匹配当前模式
- 新项目或无既有约束时是否优先推荐单 Mapper + DAO
- 单 Mapper 模式下是否存在统一 `XbatisMapper extends BasicMapper`，以及 `@MapperScan` 是否与该模式一致
- 单 Mapper 模式下是否避免主动调用 `XbatisGlobalConfig.setSingleMapperClass(...)`
- 有 DAO 层时，事务是否强烈推荐放在 DAO 方法上
- 是否已经先下载并分析本地 xbatis 源码
- 是否对齐项目当前 VO、分页、条件对象、动态值规则
- 项目是否统一推荐 Lombok `@FieldNameConstants`
- xbatis 注解中的字段依赖是否优先使用 `Fields`
- VO、QO、Model 是否统一使用 `@Ignore` / `@Ignores` 忽略非数据库操作字段
- 业务 DAO 接口 / 实现类结构是否完整，接口是否继承 `Dao<T, ID>`
- 业务 DAO 是否只保留有业务语义、组合查询、事务边界或复用价值的方法

重点风险：

- 项目是单 Mapper 模式，却新增实体 Mapper 模式
- 项目是多 Mapper 模式，却凭空引入 `BasicMapper`
- 单 Mapper 项目使用 `DaoImpl`
- 多 Mapper 项目使用 `BasicDaoImpl`
- 有 DAO 层却把事务主要放在 Service 层，导致事务边界与数据库访问脱节
- 不知道 xbatis 如何使用时，没有从本地 xbatis 源码目录分析使用方法
- 单 Mapper 模式下没有统一 `XbatisMapper`，或 `@MapperScan` 与单 Mapper 入口不一致
- 单 Mapper 模式下主动调用 `XbatisGlobalConfig.setSingleMapperClass(...)`
- 业务 DAO 直接继承框架 DAO 实现，重复散落 Mapper 注入细节
- 业务 DAO 只有实现类没有接口，或接口继承 `IDao<T, ID>`
- 业务 DAO 编写大量与 BaseDao / 内置 Mapper 重复的简单方法，增加维护面但没有提供业务语义
- 项目已有对象转条件规范，却新写一套手工筛选逻辑
- 同仓库里混入另一套 ORM 组织习惯
- 在 VO、DTO、QO、Model 等非实体类上使用实体类注解
- 项目推荐 Lombok 字段常量，却仍大量使用字符串字段名
- 实体类不再单一，开始承载展示或临时字段

## 8. 审查结论输出建议

代码审查型 Agent 输出结论时，优先按以下顺序组织：

1. 严重问题
2. 中风险实现偏差
3. 风格偏离但暂不致命的问题
4. 建议的 xbatis 原生替代方案

### 应优先指出的严重问题

- 多租户条件遗漏
- 乐观锁缺失导致并发覆盖
- 逻辑删除误用
- join / 分页导致结果错误
- 手工拼 SQL 带来的安全风险

### 不应作为主问题的内容

- 纯命名喜好
- 与功能无关的细小格式差异
- 不影响行为的个人偏好式建议

## 9. 最终判断标准

一段 xbatis 代码如果满足下面这些条件，通常可认为是“像 xbatis”的：

1. 简单 CRUD 走内置 Mapper
2. 默认有 DAO 层，且业务 DAO 接口继承 `Dao<T, ID>`，实现类继承项目 BaseDao
3. 按 id 查询实体或部分列走 `getById`，按 id 查单列值走 `getValueById`
4. 常规查询在 DAO 内走 `queryChain()`
5. 搜索查询才使用 `forSearch(true)`
6. 适合“先查 A，顺带带出 B”的场景优先 `@Fetch`
7. 非搜索条件忽略优先 predicate 重载，其次 boolean `when` 重载；使用 `Methods` 风格时优先静态导入
8. 成组 `or` 条件走 `.nested(...)`，`.or()` 后需要时用 `.and()` 切回
9. 写入 Chain 在 DAO 内通过框架方法创建
10. 修改操作优先用 Model 类收敛入参并缩小更新字段范围，Model 可直接参与 `save`、`update`
11. 接口返回优先 VO，联表结果优先 `select(VO.class)` / `returnType(VO.class)`，VO 优先配合 `@ResultEntity` 等结果映射注解，需要枚举名称时优先 `@PutEnumValue`
12. 实体普通字段默认不机械写 `@TableField`；创建时间、修改时间优先复用 `@TableField` 动态默认值能力
13. 条件对象优先实现 `QO` 并配合 `@ConditionTarget` 体系；`where()` 优先使用 `WhereUtil.where(this)`
14. VO、QO、Model 中非数据库操作字段优先使用 `@Ignore` / `@Ignores`
15. 无特殊要求时项目集成 Lombok；xbatis 注解里涉及字段引用时优先使用 `@FieldNameConstants` 生成的 `Fields` 常量；select 别名优先使用 getter / 字段引用形式
16. 单条数据先查后改部分字段时，优先使用 `partialUpdate(...)` 精准修改
17. `UpdateChain`、`InsertChain`、`DeleteChain` 最终统一通过 `execute()` 执行
18. 分页走统一 `Pager`；1 对多分页 join 需要处理 join 优化
19. 多租户、逻辑删除、乐观锁、动态值走框架能力
20. 单 Mapper 模式优先统一 `XbatisMapper extends BasicMapper` 并配置 `@MapperScan`，不主动调用 `XbatisGlobalConfig.setSingleMapperClass(...)`
21. 有 DAO 层时，事务强烈推荐在 DAO 方法上开启
22. DAO 注入收敛在项目 BaseDao 的 `setMapper(...)`，并配合 Spring、Solon 等容器自动注入注解完成装配；业务 DAO 实现类不重复重写
23. 实体类只承载数据库表字段，保持单一性
24. 实体类注解只能写在实体类上
25. 持久化枚举实现 `EnumSupport<T>` 并通过 `getCode()` 提供数据库存储值，同时提供找不到返回 `null` 的 `of(T code)`
26. 不知道类路径或类名时，先查本地 xbatis 源码，不凭空猜测
27. 开发环境开启 xbatis POJO 安全检查，并覆盖 VO、Model、QO、排序对象所在包；`basePackages` 和细分包路径二选一；测试和生产环境不默认开启
28. 业务 DAO 不写和 BaseDao / 内置 Mapper 重复的简单方法
29. 基础按 id、save、update 方法保持框架真实命名和签名
30. XML / 原生 SQL 只在必要时出现
31. 与项目已有 xbatis 风格一致

如果一段代码反复违背这些条件，优先判定它偏离了 xbatis 习惯，而不是继续在现有写法上做局部修补。
