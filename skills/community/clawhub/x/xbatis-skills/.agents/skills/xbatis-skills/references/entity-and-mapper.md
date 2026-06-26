# 实体与 Mapper 约定

## 实体注解

这些注解的真实包名都在 `cn.xbatis.db.annotations` 下。

- `@Table`
  - 定义表名、`schema`
  - 可设置 `columnNameRule` 与 `databaseCaseRule`
- `@TableId`
  - 支持自增、生成器、SQL 生成等主键策略
  - 可按数据库类型差异化配置
- `@TableField`
  - 控制字段是否参与 `select` / `insert` / `update`
  - `neverUpdate` 可彻底禁止字段更新
  - `exists = false` 可标记非表字段
  - 支持 `jdbcType`、`typeHandler`
  - 支持 `defaultValue` / `updateDefaultValue`
- `@LogicDelete`
  - 定义删除前后值
  - `afterValue` 支持动态值
- `@LogicDeleteTime`
  - 记录逻辑删除时间
- `@TenantId`
  - 标记租户字段
- `@Version`
  - 标记乐观锁字段

生命周期注解不在 `cn.xbatis.db.annotations`，真实包名是：

- `cn.xbatis.listener.annotations.OnInsert`
- `cn.xbatis.listener.annotations.OnUpdate`

## 枚举约定

持久化枚举必须实现真实接口 `cn.xbatis.core.mybatis.typeHandler.EnumSupport<T>`：

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

规则：

- 枚举通过 `getCode()` 返回数据库存储值
- 枚举生成时必须提供 `of(T code)` 静态方法，找不到匹配项返回 `null`
- `T` 按数据库字段实际类型选择，例如 `String`、`Integer`、`Long`
- 不要默认依赖 `ordinal()`、`name()` 或手写 TypeHandler
- 需要返回枚举名称或展示值时，优先配合 `@PutEnumValue`

## 默认 Mapper 模式

默认推荐每个实体一个 Mapper：

```java
public interface SysUserMapper extends MybatisMapper<SysUser> {
}
```

特点：

- `QueryChain.of(sysUserMapper)` 可以自动推断实体类型
- 对当前实体的简单查询，通常可以省略 `select` / `from` / `returnType`
- 更适合中小项目和边界清晰的业务模块

`MybatisMapper<T>` 默认覆盖的能力包括：

- 查询：`get`、`list`、`exists`、`count`、`paging`、`cursor`、`mapWithKey`
- 新增：`save`、`saveBatch`、`saveOrUpdate`、`saveModel`
- 更新：`update`、`updateBatch`
- 删除：`deleteById`、`deleteByIds`、`delete(where)` 等
- 原生 SQL：`execute`、`select`、`selectList`
- 多库差异化：`dbAdapt(...)`

## 单 Mapper 模式

当实体很多、希望统一访问层时，再使用 `BasicMapper`：

```java
public interface MybatisBasicMapper extends BasicMapper {
}
```

使用要求：

1. `@MapperScan(..., markerInterface = BasicMapper.class)`
2. 链式 API 里显式传入实体类型
3. 不需要主动调用 `XbatisGlobalConfig.setSingleMapperClass(...)`

示例：

```java
QueryChain.of(mybatisBasicMapper, SysUser.class)
        .eq(SysUser::getId, 1)
        .list();
```

单 Mapper 模式下的要点：

- DSL 必须知道实体类，否则无法推断表和字段
- 复杂 XML 调用通过 `withSqlSession(...)`
- 如果代码库已经采用单 Mapper，就继续沿用，不要混入大量实体 Mapper
- 单 Mapper 模式下不要主动生成 `XbatisGlobalConfig.setSingleMapperClass(...)` 调用

## DAO 注入约定

如果项目使用 DAO 层，先创建项目级 BaseDao：

- 单 Mapper 模式：项目 BaseDao 继承 `BasicDaoImpl<T, ID>`
- 多 Mapper 模式：项目 BaseDao 继承 `DaoImpl<T, ID>`
- 业务 DAO 必须拆成接口和实现类
- 业务 DAO 接口继承 `cn.xbatis.core.mvc.Dao<T, ID>`
- 业务 DAO 实现类继承项目 BaseDao，并实现对应业务 DAO 接口
- 不要让业务 DAO 接口继承 `cn.xbatis.core.mvc.IDao<T, ID>`；源码注释说明 `IDao` 是旧接口且不建议开发者使用
- 项目 BaseDao 的 `setMapper(...)` 方法必须加当前容器框架的自动注入注解
- `setMapper(...)` 内部调用父类 `setMapper(mapper)` 完成绑定
- 业务 DAO 实现类只继承项目 BaseDao，不需要也不应重复重写 `setMapper(...)`
- 基础按 id、save、update 方法强烈建议保持和框架 Dao / BaseDao / 内置 Mapper 的真实方法名和签名一致
- 业务 DAO 不建议写与 BaseDao / 内置 Mapper 重复的简单方法
- 业务 DAO 只保留有业务语义、组合查询、事务边界或复用价值的方法

容器注解跟随当前项目：

- Spring 项目跟随 `@Autowired`、`@Resource` 等既有规范
- Solon 项目跟随 `@Inject`、`@Db` 等既有规范

## 写入冲突策略

README 说明 `save` / `saveBatch` / `InsertChain` 支持 `onConflict`：

- 冲突忽略：`doNothing()`
- 冲突更新：`doUpdate(...)`

这是跨数据库封装能力，适合主键或唯一键冲突场景。

## 生成代码时的默认选择

- 除非仓库已经统一使用 `BasicMapper`，否则默认生成 `MybatisMapper<T>`
- 实体字段优先用注解表达映射规则，不要把映射逻辑分散到业务层
- 默认使用 Lambda 属性引用，不写硬编码列名
- 不知道类路径、真实类名、方法名、注解包名或泛型签名时，先用本地 xbatis 源码确认，不要猜测
