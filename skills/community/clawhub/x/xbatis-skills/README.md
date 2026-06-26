[//]: # ([![skills.sh]&#40;https://skills.sh/b/anthropics/skills&#41;]&#40;https://gitee.com/xbatis/xbatis-skills&#41;)

# Xbatis Skills

使用这份 Skills 时，优先遵循 xbatis 的原生表达方式，不要把它当成其他 ORM 或传统 XML MyBatis 使用。

## 执行范围

处理以下任务时，使用这份 Skill：

- 新增或修改 xbatis 实体、Mapper、Service、DAO
- 初始化或接入 Spring Boot / Solon 等 xbatis 运行环境
- 使用 DAO、`BasicMapper`、`MybatisMapper<T>`、`QueryChain`、`UpdateChain`、`InsertChain`、`DeleteChain`
- 实现分页、联表、VO 映射、对象转条件、对象转排序
- 接入逻辑删除、多租户、乐观锁、动态值、动态默认值
- 使用 SQL 模板、动态 where、动态 query、原生 SQL 包装
- 审查现有 xbatis 代码是否偏离框架习惯

不要将这份 Skill 用于：

- 纯 JPA / Hibernate 项目
- 不使用 xbatis 的普通 MyBatis 项目
- 仅做宣传介绍、安装教程、用户导览的任务

## 核心原则

始终按以下顺序决策：

1. 先判断能否直接使用框架原生能力。
2. 再判断是否需要映射或模板能力。
3. 最后才回退 XML 或原生 SQL。

始终保持以下优先级：

1. DAO 层和内置 Mapper 方法
2. DAO 内部的 `queryChain()` / `updateChain()` / `insertChain()` / `deleteChain()`
3. 注解映射、VO 自动映射、`returnType`
4. SQL 模板、动态 where、动态 query、数据库函数
5. 少量 XML / 原生 SQL

避免以下默认倾向：

- 不要跳过 DAO 层直接在 Service / Controller 创建 Chain
- 不要为简单 CRUD 先写 XML
- 不要为标准列表页先拼 SQL 字符串
- 不要为联表返回先手工 copy VO
- 不要把“复杂”直接等同于“只能 XML”

## 项目约束

默认按以下项目级约束生成和审查代码：

- 开发环境必须开启 xbatis POJO 安全检查，用于启动时检查 VO、Model、条件对象、排序对象的映射和注解缺口
- Spring / Spring Boot 项目优先按当前 starter 支持的 `@XbatisPojoCheckScan` 接入；README 记录的包名是 `org.mybatis.spring.boot.autoconfigure.XbatisPojoCheckScan`，但生成前必须从当前项目依赖或本地 starter 源码确认真实包名
- Solon 项目优先在 `solon.yml` 的 `mybatis.<数据源 bean 名称>.pojoCheck` 下配置 `basePackages`、`modelPackages`、`resultEntityPackages`、`conditionTargetPackages`、`orderByTargetPackages`
- POJO 安全检查扫描范围二选一：要么使用 `basePackages` 覆盖项目相关包，要么使用 `modelPackages` / `resultEntityPackages` / `conditionTargetPackages` / `orderByTargetPackages` 等细分包路径；不要同时生成两种方案
- 测试环境和生产环境不要求默认开启安全检查；除非项目明确要求，不要为 test/prod 生成安全检查配置
- 生成新项目骨架、接入 xbatis、生成 VO / Model / QO / OrderBy 对象时，必须同步补安全检查扫描范围
- Controller 入参超过 2 个，或大概率后续会继续增加参数时，必须使用 QO、DTO、Model 等对象接收，并把对象传递到 Service 层，不要继续堆散参
- 无特殊要求时，项目必须集成 Lombok；实体、VO、QO、DTO、Model 优先使用 Lombok 减少样板代码，并按需启用 `@FieldNameConstants` 支持字段常量引用

## 读取 references

按任务读取对应参考文件，不要一次性加载全部 references：

- 处理 Spring Boot / Solon 接入、starter 依赖、数据源、启动类、`@MapperScan` 时，读取 `references/environment-setup.md`
- 处理标准查询、分页、联表、VO 返回时，读取 `references/query-strategy.md`
- 判断项目是否使用单 Mapper 或 `BasicMapper` 时，读取 `references/mapper-modes.md`
- 处理逻辑删除、多租户、乐观锁、动态值、对象转条件时，读取 `references/framework-features.md`
- 判断是否应回退 SQL 模板、原生 SQL、XML 时，读取 `references/advanced-sql.md`
- 需要明确 XML / 原生 SQL 使用边界时，读取 `references/xml-boundaries.md`
- 执行代码审查、PR Review、实现偏差排查时，读取 `references/review-checklist.md`

## 启用前准备

启用 xbatis 任务时，先做这件事：

- 第一件事就是从 GitHub / Gitee 下载 xbatis/starter 源码到本地目录
- GitHub: `https://github.com/xbatis/xbatis`
- Gitee: `https://gitee.com/xbatis/xbatis`
- springboot starter GitHub: `https://github.com/xbatis/xbatis-spring-boot-parent`
- springboot starter Gitee: `https://gitee.com/xbatis/xbatis-spring-boot-parent`
- solon starter GitHub: `https://github.com/xbatis/xbatis-solon-plugin`
- solon starter Gitee: `https://gitee.com/xbatis/xbatis-solon-plugin`
- 后续实现、改写、审查、答疑时，优先从本地源码目录分析真实 API、注解、Chain、DAO、Mapper 的用法
- references 用于收敛规则，本地源码用于确认真实能力和调用方式
- 不知道 xbatis 如何使用时，从本地 xbatis 源码目录进行分析使用方法
- 生成代码时，如果不知道类路径、真实类名、方法名、注解包名或泛型签名，禁止猜测；必须先用本地 xbatis 源码搜索确认
- 没有在本地 xbatis 源码或当前项目里确认到的类型和 API，不要写成确定代码；应先继续分析源码，或明确标注为待项目确认

## 执行流程

### 1. 先识别任务类型

先将任务归类为以下一种：

- 简单 CRUD
- 标准列表查询
- 联表 / VO 查询
- 搜索表单 / 动态条件
- 高复杂度报表 SQL
- 框架特性接入

### 2. 再选实现方式

#### 简单 CRUD

优先使用：

- DAO 基础方法
- 按 id 返回实体或单表部分列时使用 `getById`
- 按 id 返回单列值时使用 `getValueById`
- 单 Mapper 模式下由项目 BaseDao 封装的 `BasicDaoImpl<T, ID>`
- 多 Mapper 模式下由项目 BaseDao 封装的 `DaoImpl<T, ID>`

避免：

- 按 id 查询实体、部分列或单列值时默认写 `QueryChain`
- 为主键查询、批量 ID 查询、基础新增修改删除编写自定义 XML

#### 标准列表 / 分页 / 条件查询

优先使用：

- DAO 内部的 `queryChain()`
- `paging(Pager)`
- 条件对象转 where

避免：

- 在业务层手工拼接 where
- 手工维护 count + limit 两套 SQL
- 在非搜索查询里机械套用 `forSearch(true)`

只有搜索查询、搜索表单、后台筛选页、关键词查询才优先使用 `forSearch(true)`。

#### 联表 / VO 查询

优先使用：

- DAO 内部的 `queryChain()`
- 如果是“先查 A，顺带带出 B”的场景，优先考虑 `@Fetch`，不要默认写 join
- join 查询优先先 `.from(...)` 明确主表
- `returnType(VO.class)`
- `select(VO.class)` 或实体/VO 自动列推导
- 需要枚举名称时优先使用 `@PutEnumValue`
- 结果映射注解

避免：

- 先查实体再 copy 到 VO
- 为常规 join 结果堆大量别名和转换代码
- 本可用 `@Fetch` 的场景机械改成 join
- 手工一个一个 `select` 字段，本可直接 `select(VO.class)` 却堆大量列

#### 更新 / 插入 / 删除链

优先使用：

- DAO 内部的 `updateChain()`
- DAO 内部的 `insertChain()`
- DAO 内部的 `deleteChain()`

避免：

- 在 Service / Controller 中直接创建 `UpdateChain.of(...)`
- 在 Service / Controller 中直接创建 `InsertChain.of(...)`
- 在 Service / Controller 中直接创建 `DeleteChain.of(...)`
- 把 `DeleteChain` 当成逻辑删除入口

#### 复杂 SQL

优先使用：

- SQL 模板
- 动态 query
- 原生 SQL + 动态 where

最后再考虑：

- XML

避免：

- 在还未验证框架原生表达能力前直接绕开 xbatis

### 3. 再对齐项目现有模式

落代码前，先确认：

- 是否启用了单 Mapper 模式
- DAO 层是否已存在
- DAO 基类是否与 Mapper 模式一致
- 是否已有统一分页器
- 是否已有动态值规则
- 是否已统一逻辑删除和多租户策略
- 是否已有 VO / DTO 命名与映射习惯
- 当前项目采用的是单 Mapper 还是多 Mapper

已有明确风格时，跟随项目，不要引入另一套 ORM 写法。

新项目或用户未指定模式时，优先推荐单 Mapper + DAO。

## 实体规则

默认执行以下规则：

- 使用 `@Table`
- 使用 `@TableId`
- 仅在必要时使用 `@TableField`
- 无特殊要求时项目必须集成 Lombok，并在实体类上优先补 `@FieldNameConstants`
- 实体类只承载数据库表字段，保持实体类单一性
- 实体类注解只能写在实体类上，禁止写在 VO、DTO、QO、Model 等其他类上

仅在以下场景补更多注解：

- 逻辑删除
- 多租户
- 乐观锁
- 动态填充
- 结果映射
- 条件映射

推荐的字段规则：

- 创建时间字段优先使用 `@TableField(defaultValue = "{NOW}", update = false)`
- 修改时间字段优先使用 `@TableField(defaultValue = "{NOW}", updateDefaultValue = "{NOW}", updateDefaultValueFillAlways = true)`
- 无特殊行为的普通字段，不要为了声明列名而机械补 `@TableField("xxx")`
- 只有在需要控制默认值、更新行为、类型处理、查询参与、非表字段等特殊语义时才补 `@TableField`
- 非数据库表字段不要放进实体类；这类字段应放到 VO、QO、Model，并按需使用 `@Ignore` 或 `@Ignores`

避免：

- 对每个字段机械地重复写 `@TableField`
- 明明可由命名规则推导，还重复硬编码列名
- 在实体类里混入非数据库表字段
- 在 VO、DTO、QO、Model 等非实体类上使用实体类注解

## Mapper 规则

默认执行以下规则：

- 新项目优先推荐单 Mapper 模式
- 默认生成 DAO 层
- 创建业务 DAO 前，先按 Spring / Solon 等运行环境创建项目级 BaseDao
- BaseDao 负责注入并封装通用 DAO 能力
- 有 DAO 层时，事务强烈推荐在 DAO 方法上开启
- 单 Mapper 模式下优先定义统一 `XbatisMapper extends BasicMapper`
- 单 Mapper 模式下不需要主动生成或调用 `XbatisGlobalConfig.setSingleMapperClass(...)`
- 单 Mapper 模式下项目 BaseDao 继承 `BasicDaoImpl<T, ID>`
- 多 Mapper 模式下项目 BaseDao 继承 `DaoImpl<T, ID>`
- DAO 层必须创建业务 DAO 接口，接口继承 `cn.xbatis.core.mvc.Dao<T, ID>`
- 业务 DAO 实现类继承项目 BaseDao，并实现对应业务 DAO 接口
- 项目 BaseDao 的 `setMapper(...)` 方法必须加上当前容器框架的自动注入注解；Spring 跟随 `@Autowired` / `@Resource` 等项目既有规范，Solon 跟随 `@Inject` / `@Db` 等项目既有规范
- 业务 DAO 实现类只继承项目 BaseDao，不需要也不应重复重写 `setMapper(...)`
- 业务 DAO 接口不要继承 `cn.xbatis.core.mvc.IDao<T, ID>`；源码注释说明 `IDao` 是旧接口且不建议开发者使用
- 已有项目按既有单 Mapper / 多 Mapper 模式实现

避免：

- 只为基础 CRUD 定义大量重复 Mapper 方法
- 不判断现有模式就切换为另一种 Mapper 组织方式
- 有 DAO 层却在业务层直接持有 Mapper 或手动创建 Chain
- 有 DAO 层却把事务主要开在 Service 层
- 每个业务 DAO 都重复写一遍 Mapper 注入细节
- 在业务 DAO 里编写与 BaseDao、DAO 基础方法或内置 Mapper 方法完全等价的简单转发方法
- 业务 DAO 接口直接继承 `IDao<T, ID>`，或不建接口只建实现类

重点执行：

- 遇到 Mapper 相关任务时，优先读取 `references/mapper-modes.md`
- 先确认当前项目是单 Mapper 还是多 Mapper，再决定新增代码的组织方式
- 先创建并复用项目 BaseDao，再生成具体业务 DAO
- 项目 BaseDao 统一定义带容器自动注入注解的 `setMapper(...)`，内部调用父类 `setMapper(mapper)` 完成绑定
- 业务 DAO 接口统一继承 `Dao<T, ID>`；业务 DAO 实现类继承项目 BaseDao 并实现该接口
- 业务 DAO 实现类只声明实体泛型并继承项目 BaseDao，不重复写 Mapper 字段、构造器注入或 `setMapper(...)`
- 基础按 id、save、update 等方法强烈建议保持和框架 Dao / BaseDao / 内置 Mapper 的真实方法名和签名一致；不要改造成 `findById`、`create`、`modify` 这类二次命名
- 业务 DAO 只保留有业务语义、组合查询、事务边界或复用价值的方法；简单 CRUD、按 id 查询、count、exists、save、update、delete 等基础能力直接使用 BaseDao / 内置 Mapper，或在接口契约中按框架真实签名继承
- 有 DAO 层时，强烈推荐把数据库访问与事务边界一起收敛到 DAO 方法
- Spring 项目在单 Mapper 模式下配置 `@MapperScan` 扫描统一 `XbatisMapper` 所在包；如果项目已使用 `markerInterface = BasicMapper.class`，延续现有配置
- 单 Mapper 模式下不要主动调用 `XbatisGlobalConfig.setSingleMapperClass(...)`
- 不要在同一模块里混入两套 Mapper 风格

## 枚举规则

默认执行以下规则：

- 生成或改写持久化枚举时，枚举必须实现 `cn.xbatis.core.mybatis.typeHandler.EnumSupport<T>`
- 枚举必须提供稳定的 `code` 值并实现 `getCode()`；字段类型 `T` 按数据库实际存储类型选择，例如 `String`、`Integer`、`Long`
- 枚举必须提供 `public static Xxx of(T code)` 方法；遍历枚举按 `code` 匹配，找不到时返回 `null`
- 示例形态：`public enum Status implements EnumSupport<Integer> { ... }`
- 不要默认依赖 `Enum.name()`、`ordinal()` 或手写 TypeHandler 作为 xbatis 枚举持久化方案
- 需要在 VO 中返回枚举名称或展示值时，优先配合 xbatis 的 `@PutEnumValue`

示例：

```java
public enum Status implements EnumSupport<Integer> {

    ENABLED(1),
    DISABLED(0);

    private final Integer code;

    Status(Integer code) {
        this.code = code;
    }

    @Override
    public Integer getCode() {
        return code;
    }

    public static Status of(Integer code) {
        for (Status item : values()) {
            if (java.util.Objects.equals(item.getCode(), code)) {
                return item;
            }
        }
        return null;
    }
}
```

生成前必须从本地 xbatis 源码确认真实包名；当前源码中 `EnumSupport` 位于 `cn.xbatis.core.mybatis.typeHandler.EnumSupport`。

## QueryChain 规则

默认执行以下规则：

- 查询优先在 DAO 内使用 `queryChain()`
- 可选条件优先用对象转条件
- 查询条件对象优先实现 `cn.xbatis.core.mvc.QO` 并提供 `where()`
- 查询条件对象优先使用 `@ConditionTarget`、`@Condition`、`@Conditions`、`@ConditionGroup` 等对象转条件注解
- QO、VO、Model 中凡是不是数据库操作字段、需要忽略的字段，优先使用 `@Ignore` 或 `@Ignores`
- 搜索查询才优先 `forSearch(true)`
- 分页优先 `paging(Pager)`
- 适合“先查 A，顺带带出 B”的场景时，优先考虑 `@Fetch`
- join 查询优先先 `.from(...)` 明确主表
- join 优先使用 `leftJoin(SysUser::getRoleId, SysRole::getId)` 这类带方法引用的写法，第二个参数所属实体是被 join 的实体
- 返回 VO 时优先 `select(VO.class)`；如果 `returnType` 与 `select` 类型一致且没有额外 select，可省略 `.select(...)`

按 id 查询：

- 返回实体或单表部分列：优先 `getById`
- 返回单列值：优先 `getValueById`
- 其他条件查询才使用 `queryChain()`

额外检查：

- 在 1 对多分页场景检查 `leftJoin` 分页优化是否合适，必要时改用 `rightJoin()` 或关闭 join 优化
- 在 join 场景优先显式定义 ON 条件

避免：

- 依赖旧式不推荐 join 写法
- 在适合 `@Fetch` 的场景机械使用 join
- 把搜索场景的空值忽略逻辑散落在 Service 层
- 在详情查询、唯一性校验、内部业务规则查询中默认套用 `forSearch(true)`
- 在无法使用 `forSearch(true)` 时，仍把值忽略判断散落成外层 `if`
- 本可用 `.eq(SysUser::getId, id, Objects::nonNull)`，却使用更绕的写法
- 需要括号包裹 `or` 条件时，没有使用 `.nested(chain -> ...)`
- 手工一个一个 `select` 字段，本可直接 `select(VO.class)` 却堆大量列
- 把可复用查询条件拆散成 Service 层的一长串 if

注意：源码接口名是 `QO`，不要写成 `Qo`。
注意：`QO.where()` 中优先使用 `WhereUtil.where(this)` 写法。

无法使用 `forSearch(true)`，但需要根据值忽略条件时：

1. 优先使用 predicate 重载，例如 `.eq(SysUser::getId, id, Objects::nonNull)`
2. 无法使用 predicate 重载时，再使用 boolean `when` 重载，例如 `.eq(Objects.nonNull(id), SysUser::getId, id)`
3. 一组条件需要括号包裹，尤其组内存在 `or` 条件时，使用 `.nested(chain -> ...)`
4. 条件拼接默认是 `and`；调用 `.or()` 后会持续使用 `or`，需要切回时显式调用 `.and()`
5. 局部 `or` 条件优先放进 `.nested(...)`，避免 `.or()` 状态影响后续外层条件

## 写入 Chain 规则

默认执行以下规则：

- 更新链在 DAO 内使用 `updateChain()`
- 插入链在 DAO 内使用 `insertChain()`
- 删除链在 DAO 内使用 `deleteChain()`
- `UpdateChain`、`InsertChain`、`DeleteChain` 最终执行方法统一是 `execute()`
- 修改操作优先使用 Model 类作为传参载体
- Model 可以像实体类一样直接参与 `save(Model)`、`update(Model)`, xbatis 自带这些方法
- Model 中凡是不是数据库操作字段、需要忽略的字段，优先使用 `@Ignore` 或 `@Ignores`
- 单条数据如果是“先查询出来，再改部分字段”的场景，强烈建议使用 xbatis 的 `partialUpdate(...)` 精准修改
- 更新时缩小字段范围，只更新本次业务允许变化的字段

避免：

- 在 Service / Controller 中直接创建 `UpdateChain.of(...)`、`InsertChain.of(...)`、`DeleteChain.of(...)`
- 在单 Mapper 模式下混入多 Mapper 的 Chain 创建方式
- 在多 Mapper 模式下混入 `BasicMapper` 的 Chain 创建方式
- 把查询实体、响应 VO 或全量实体直接作为修改入参
- 因为前端传了字段就默认全部参与 update
- 单条数据先查后改时，本可用 `partialUpdate(...)` 精准修改，却直接对查出的实体做普通 `update(entity)`
- 创建了 `UpdateChain`、`InsertChain`、`DeleteChain` 却没有以 `execute()` 收尾

## 返回对象规则

默认执行以下规则：

- Controller / API 对外返回优先使用 VO，不建议直接返回实体类
- 后台管理系统的列表、详情 VO 可按项目风格考虑继承实体类，以减少重复字段
- 非后台管理系统也建议返回 VO，避免把持久化实体直接暴露给外部接口
- 展示型、联表型、聚合型结果必须优先返回 VO
- DAO 内部和纯持久化读写方法可以返回实体，但不要把实体直接穿透到接口响应
- 优先让 xbatis 自动 select 所需列
- VO 自动映射场景下，VO 类尽量配合 xbatis 的 `@ResultEntity`、`@NestedResultEntity`、`@NestedResultEntityField`、`@ResultCalcField` 等结果映射注解
- 需要返回枚举名称时优先使用 `@PutEnumValue`
- VO 中凡是不是数据库操作字段、需要忽略的字段，优先使用 `@Ignore` 或 `@Ignores`
- 非实体类不要使用实体类注解

避免：

- 查询实体后手工映射成 VO
- 只有在项目已有稳定转换层并明确要求时才例外
- 为了兼容前端字段，把实体类污染成响应对象
- 在 VO、DTO、QO、Model 等非实体类上使用 `@Table`、`@TableId`、`@TableField` 等实体类注解
- 把不存在于 xbatis 的泛化“VO 注解”当成抽象概念写法；应落到真实的结果映射注解

## XML / 原生 SQL 规则

将 XML / 原生 SQL 视为后置选项。

仅在以下场景使用：

- 极重报表 SQL
- xbatis 原生表达明显不清晰
- 特定数据库语义很强
- 现有系统已有成熟 XML 且明确要求延续

使用 SQL 模板时：

- 命令模板优先使用 `Methods.tpl(...)`
- 函数模板优先使用 `Methods.fTpl(...)`
- 条件模板优先使用 `Methods.cTpl(...)`

避免在以下场景使用：

- 简单 CRUD
- 常规分页列表
- 普通联表
- 仅因为开发者熟悉 XML 而回退

## 框架特性规则

### 逻辑删除

优先复用框架逻辑删除能力。

避免：

- 在普通查询里反复手工拼 `deleted = 0`
- 忘记 `DeleteChain` 删除不触发逻辑删除规则
- 需要逻辑删除语义时误用 `deleteChain()`

### 多租户

优先使用 `@TenantId` 和框架多租户能力。

避免：

- 在业务代码里遍地补 `tenant_id`
- 破坏项目已有的租户上下文传递方式

### 乐观锁

优先使用 `@Version`。

避免：

- 手工给每个 update 写版本判断逻辑

### 动态值 / 默认值

优先使用全局动态值、`@OnInsert`、`@OnUpdate`。

避免：

- 在 Controller / Service 层重复填充创建时间、修改时间、操作人

实体审计字段建议：

- 创建时间字段优先使用 `@TableField(defaultValue = "{NOW}", update = false)`
- 修改时间字段优先使用 `@TableField(defaultValue = "{NOW}", updateDefaultValue = "{NOW}", updateDefaultValueFillAlways = true)`

### 对象转条件 / 对象转排序

优先将搜索对象、筛选对象、排序对象交给框架对象转换能力处理。

查询对象规则：

- 查询对象优先实现 `cn.xbatis.core.mvc.QO`
- `QO.where()` 负责集中构建 `Where`
- 条件对象优先声明 `@ConditionTarget`，并按需使用 `@Condition`、`@Conditions`、`@ConditionGroup`
- `QO.where()` 中优先使用 `WhereUtil.where(this)`
- DAO 方法优先接收查询对象并使用 `queryChain(qo.where())`
- 多字段排序优先使用对象转排序
- 使用 `Methods` 风格时，优先静态导入所需方法，并保持 `eq(gt(...))` 这类嵌套表达

避免：

- 为动态筛选写一长串 `if`
- 在 Service 层手工拼接查询条件
- 在 Service / Controller 手工拼接多字段 `order by`

## 禁止事项

将以下行为视为明显偏离 xbatis 风格：

1. 套用其他 ORM 的默认查询组织习惯
2. 一看到动态查询就写 XML
3. 在 Service 层拼 SQL 片段
4. 自己实现分页而不用框架分页
5. 在搜索查询中忽略 `forSearch(true)` 与空值忽略能力
6. 明明适合 VO 自动映射却手工转换
7. 不看项目现有风格，直接生成另一套 ORM 写法
8. 在逻辑删除、多租户、乐观锁场景下手工编码条件
9. 用大量自定义 Mapper 方法替代可复用的原生能力
10. 不区分“复杂 SQL”和“可被 QueryChain 表达的中等复杂查询”
11. 有 DAO 层却绕过 DAO 直接创建 Chain
12. 在非搜索查询中滥用 `forSearch(true)`
13. 不创建项目 BaseDao，导致每个 DAO 重复写 Mapper 注入
14. 可用 `QO` 表达的查询条件却散落在 Service 层
15. Controller / API 直接返回实体类，或为响应字段污染实体
16. 按 id 查询实体、部分列或单列值时绕过 `getById` / `getValueById`
17. 需要按值忽略条件时，不使用 predicate / boolean `when` 重载
18. 需要括号包裹 `or` 条件时，不使用 `.nested(...)`
19. 调用 `.or()` 后没有显式 `.and()` 切回，导致后续条件错误变成 OR
20. 修改操作不使用 Model 类收敛入参，或更新字段范围过大
21. 在无特殊语义的普通字段上机械补 `@TableField("列名")`
22. 创建时间、修改时间没有优先复用 `@TableField` 的动态默认值能力
23. QO 已适合对象转条件，却不使用 `@ConditionTarget` 体系和 `WhereUtil.where(this)`
24. DAO 注入仍以构造方法传 Mapper 为主，或把 `setMapper(...)` 重复写在每个业务 DAO 子类里，而不是在项目 BaseDao 上统一加容器自动注入注解
25. xbatis 注解里有字段依赖时仍写字符串字面量，不优先使用 `SysUser.Fields.id`
26. `.as(...)` 明明可以使用字段 / getter 引用，却默认回退字符串别名
27. VO、QO、Model 中存在非数据库操作字段，却没有使用 `@Ignore` 或 `@Ignores`
28. 实体类混入非数据库表字段，破坏实体类单一性
29. 单条数据先查后改时，不使用 `partialUpdate(...)` 精准修改
30. 创建了 `UpdateChain`、`InsertChain`、`DeleteChain` 却没有调用 `execute()`
31. 需要 SQL 模板时，不通过 `Methods.tpl`、`Methods.fTpl`、`Methods.cTpl` 创建
32. 业务 DAO 编写大量与 BaseDao / 内置 Mapper 等价的简单转发方法

## 质量检查

提交前，逐项检查：

1. 这个需求是否真的需要 XML
2. 是否已经优先考虑 DAO / 内置 Mapper / DAO 内部 Chain
3. Controller / API 返回对象是否优先使用 VO，而不是直接暴露实体
4. 是否复用了项目现有分页、逻辑删除、多租户、乐观锁方案
5. 是否存在字符串拼 SQL 的低质量实现
6. 是否有本可自动映射却手工 copy 的代码
7. 是否引入了与项目现有风格冲突的 ORM 习惯
8. 是否已经利用 xbatis 原生能力而不是重复造轮子
9. DAO 基类是否匹配 Mapper 模式
10. `forSearch(true)` 是否只用于搜索查询
11. 是否已经按 Spring / Solon 等环境抽取项目 BaseDao
12. 查询条件对象是否优先实现 `cn.xbatis.core.mvc.QO`
13. 按 id 查询是否优先使用 `getById` / `getValueById`
14. 非搜索条件忽略是否优先使用 predicate 重载，其次 boolean `when` 重载
15. 含 `or` 的成组条件是否使用 `.nested(...)`
16. 使用 `.or()` 后是否已在需要时通过 `.and()` 切回
17. 修改入参是否使用 Model 类并限制更新字段范围
18. join 场景是否优先使用 `.from(...)`、方法引用 join 和 `select(VO.class)`
19. 适合“先查 A，顺带带出 B”的场景是否优先考虑 `@Fetch`
20. 单 Mapper 模式下是否定义统一 `XbatisMapper` 并配置 `@MapperScan`
21. 需要枚举名称时是否优先使用 `@PutEnumValue`
22. 实体普通字段是否避免了机械 `@TableField("列名")`
23. 创建时间、修改时间是否优先使用 `@TableField(defaultValue = "{NOW}", update = false)` 和 `@TableField(defaultValue = "{NOW}", updateDefaultValue = "{NOW}", updateDefaultValueFillAlways = true)`
24. QO 是否优先配合 `@ConditionTarget` 体系，并在 `where()` 中使用 `WhereUtil.where(this)`
25. 项目 BaseDao 的 `setMapper(...)` 是否带 Spring、Solon 等容器自动注入注解，业务 DAO 子类是否避免重复重写 `setMapper(...)`
26. 实体、QO、VO 等涉及字段引用的 xbatis 注解是否优先使用 Lombok `@FieldNameConstants` 生成的 `Fields`
27. `.as(...)` 是否优先使用 getter / 字段引用形式，例如 `.select(SysUser::getId, c -> c.as(SysUser::getId))`
28. VO、QO、Model 中需要忽略的非数据库操作字段是否使用了 `@Ignore` 或 `@Ignores`
29. 实体类是否保持单一性，不包含非数据库表字段
30. 单条数据先查后改的场景是否优先使用 `partialUpdate(...)` 精准修改
31. `UpdateChain`、`InsertChain`、`DeleteChain` 是否最终使用 `execute()` 执行
32. SQL 模板是否优先通过 `Methods.tpl`、`Methods.fTpl`、`Methods.cTpl` 创建
33. 开发环境是否已经开启 xbatis POJO 安全检查，并覆盖 VO、Model、QO、排序对象所在包；test/prod 是否避免默认开启
34. 业务 DAO 是否避免编写与 BaseDao / 内置 Mapper 重复的简单方法

## 任务映射

### 新增后台列表页

执行：

1. 定义查询条件对象
2. 查询条件对象实现 `cn.xbatis.core.mvc.QO`
3. 查询条件对象优先配 `@ConditionTarget`、`@Condition`、`@Conditions`、`@ConditionGroup`
4. 需要忽略的非数据库操作字段使用 `@Ignore` 或 `@Ignores`
5. 在 `where()` 中优先使用 `WhereUtil.where(this)`
6. 在 DAO 内使用 `queryChain(qo.where())`
7. 仅搜索查询启用 `forSearch(true)`，其他场景使用对象转条件、predicate / boolean `when` 或显式条件
8. 使用 `paging(Pager)`
9. 返回后台列表 VO；字段基本等同实体时可考虑让 VO 继承实体

### 新增联表详情页

执行：

1. 在 DAO 内使用 `queryChain()`
2. 先用 `.from(...)` 明确主表，再定义 join
3. join 优先使用方法引用写法，例如 `leftJoin(SysUser::getRoleId, SysRole::getId)`
4. 使用 `returnType(VO.class)`；需要时优先 `select(VO.class)`
5. VO 优先配合 `@ResultEntity` 等结果映射注解；必要时补 `@PutEnumValue`
6. VO 中需要忽略的非数据库操作字段使用 `@Ignore` 或 `@Ignores`
7. 字段别名优先使用 getter / 字段引用形式；只有特殊场景才使用字符串别名

### 实现审计字段填充

执行：

1. 配置动态值
2. 创建时间字段优先使用 `@TableField(defaultValue = "{NOW}", update = false)`
3. 修改时间字段优先使用 `@TableField(defaultValue = "{NOW}", updateDefaultValue = "{NOW}", updateDefaultValueFillAlways = true)`
4. 使用 `@OnInsert`
5. 使用 `@OnUpdate`

## 结论

始终记住这些规则：

1. 开启 xbatis 时，第一件事就是从 GitHub / Gitee 下载 xbatis 源码到本地目录
2. 后续生成、改写、审查时，优先从本地源码目录分析真实用法
3. 新项目优先单 Mapper，并默认生成 DAO
4. 先按 Spring / Solon 等环境创建项目 BaseDao
5. 简单 CRUD 用 DAO / 内置 Mapper
6. 大多数业务查询使用 `QO` 对象转条件并在 DAO 内执行
7. 按 id 查询实体或部分列用 `getById`，按 id 查单列值用 `getValueById`
8. 更新、插入、删除链在 DAO 内使用框架方法创建
9. 修改操作用 Model 类收敛入参并缩小更新字段范围
10. 搜索查询才使用 `forSearch(true)`
11. 适合“先查 A，顺带带出 B”的场景优先考虑 `@Fetch`，真正需要 join 时先 `.from(...)`，再用方法引用 join
12. 条件对象优先实现 `QO` 并使用 `@ConditionTarget` 体系；`QO.where()` 优先用 `WhereUtil.where(this)`
13. 非搜索条件忽略优先 predicate 重载，其次 boolean `when` 重载；成组 `or` 条件用 `.nested(...)`，`.or()` 后需要时用 `.and()` 切回；使用 `Methods` 风格时优先静态导入
14. 接口返回优先 VO；后台管理 VO 可考虑继承实体，联表和展示结果优先 `select(VO.class)` / `returnType(VO.class)` 自动映射，VO 优先配合 `@ResultEntity` 等结果映射注解
15. 需要枚举名称时优先使用 `@PutEnumValue`
16. 实体普通字段默认不写 `@TableField`；创建时间优先 `@TableField(defaultValue = "{NOW}", update = false)`，修改时间优先 `@TableField(defaultValue = "{NOW}", updateDefaultValue = "{NOW}", updateDefaultValueFillAlways = true)`
17. 实体类只承载数据库表字段，禁止混入非数据库表字段；VO、QO、Model 中需要忽略的非数据库操作字段优先使用 `@Ignore` 或 `@Ignores`
18. 无特殊要求时项目必须集成 Lombok，并优先使用 `@FieldNameConstants` 和 `SysUser.Fields.id` 这类字段引用
19. `.as(...)` 优先使用 getter / 字段引用形式，例如 `.select(SysUser::getId, c -> c.as(SysUser::getId))`；只有特殊情况才使用 `.as("id")`
20. DAO 注入收敛在项目 BaseDao 的 `setMapper(...)` 上，并补 Spring、Solon 等容器自动注入注解；BaseDao 子类不重复重写 `setMapper(...)`，不默认走构造方法传 Mapper
21. 单条数据如果是先查后改部分字段，强烈建议使用 `partialUpdate(...)` 精准修改
22. `UpdateChain`、`InsertChain`、`DeleteChain` 最终统一通过 `execute()` 执行
23. SQL 模板优先通过 `Methods.tpl`、`Methods.fTpl`、`Methods.cTpl` 创建
24. 逻辑删除、多租户、乐观锁、动态值优先框架能力
25. XML 是补充手段，不是默认起点
26. 单 Mapper 模式优先统一 `XbatisMapper extends BasicMapper` 并配置 `@MapperScan`，不主动调用 `XbatisGlobalConfig.setSingleMapperClass(...)`
27. 有 DAO 层时，事务强烈推荐在 DAO 方法上开启
28. 实体类注解只能写在实体类上
29. 先识别项目现有 xbatis 风格，再落具体代码
30. 开发环境必须开启 xbatis POJO 安全检查，扫描范围在 `basePackages` 和细分包路径中二选一；测试和生产环境不要求默认开启；不知道真实注解包名或配置项时，先查当前 starter 依赖和本地源码
31. 业务 DAO 不建议写与 BaseDao / 内置 Mapper 重复的简单方法；只新增有明确业务语义或复用价值的方法

如果生成结果不满足这些规则，继续收敛实现方案。