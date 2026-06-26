# Mapper Modes

适用于以下场景：

- 新增实体 Mapper / DAO
- 判断项目是否使用单 Mapper 模式
- 审查现有项目的 Mapper 组织方式
- 编写 `QueryChain`、`UpdateChain`、`InsertChain`、`DeleteChain`、XML、自定义方法时决定依赖哪个入口

## 总原则

先识别当前项目的 Mapper 模式，再生成代码。

默认推荐：

- 新项目或用户未指定模式时，优先推荐单 Mapper 模式
- 默认生成 DAO 层，让 Service 依赖 DAO，而不是直接依赖 Mapper 或手动创建 Chain
- 创建业务 DAO 前，先按运行环境创建项目级 BaseDao，例如 Spring / Solon 各自的注入风格
- 通过 DAO 中框架提供的创建方法使用 Chain：`queryChain()`、`updateChain()`、`insertChain()`、`deleteChain()`

已有项目：

- 单 Mapper 项目继续单 Mapper
- 多 Mapper 项目继续多 Mapper
- 不为局部功能强行切换整体 Mapper 架构

不要：

- 凭习惯选择 `MybatisMapper<T>` 或 `BasicMapper`
- 在同一模块内混用两套风格
- 不看全局配置就新增 Mapper
- 单 Mapper 模式下主动生成或调用 `XbatisGlobalConfig.setSingleMapperClass(...)`
- 在 Service / Controller 里绕过 DAO 直接写 `QueryChain.of(...)`、`UpdateChain.of(...)`、`InsertChain.of(...)`、`DeleteChain.of(...)`

## DAO 层规则

默认生成 DAO 层。项目级 BaseDao 的基类必须跟 Mapper 模式一致：

- 单 Mapper 模式：BaseDao 继承 `BasicDaoImpl<T, ID>`
- 多 Mapper 模式：BaseDao 继承 `DaoImpl<T, ID>`
- 业务 DAO 必须拆成接口和实现类
- 业务 DAO 接口继承 `cn.xbatis.core.mvc.Dao<T, ID>`
- 业务 DAO 实现类继承项目 BaseDao，并实现对应业务 DAO 接口
- 不要让业务 DAO 接口继承 `cn.xbatis.core.mvc.IDao<T, ID>`；源码注释说明 `IDao` 是旧接口且不建议开发者使用

创建业务 DAO 前，先创建项目级 BaseDao：

- BaseDao 根据当前环境选择注入方式
- Spring 项目优先按项目现有规范注入
- Solon 项目按项目既有习惯使用 `@Inject`、`@Db` 或 setter 注入
- 项目 BaseDao 内部负责封装通用能力，并在 `setMapper(...)` 方法上添加当前容器框架的自动注入注解
- BaseDao 的 `setMapper(...)` 内部调用父类 `setMapper(mapper)` 完成 Mapper 绑定
- 业务 DAO 实现类只继承项目 BaseDao，不需要也不应重写 `setMapper(...)`
- 不要在每个业务 DAO 里重复写 Mapper 字段、构造器注入或容器注入细节
- 不要在业务 DAO 里编写与 BaseDao、DAO 基础方法或内置 Mapper 方法完全等价的简单转发方法
- 业务 DAO 只保留有业务语义、组合查询、事务边界或复用价值的方法
- 基础按 id、save、update 等方法强烈建议保持和框架 `Dao<T, ID>` / BaseDao / 内置 Mapper 的真实方法名和签名一致，不要二次包装命名
- 有 DAO 层时，事务边界强烈推荐定义在 DAO 方法上

BaseDao 示例方向：

- 单 Mapper：先定义统一 `XbatisMapper extends BasicMapper`，再让 `BaseDao<T, ID> extends BasicDaoImpl<T, ID>`；`BaseDao#setMapper(XbatisMapper mapper)` 上加容器自动注入注解，业务 DAO 实现类不重写
- 多 Mapper：`BaseDao<T, ID> extends DaoImpl<T, ID>`；`BaseDao#setMapper(...)` 上加容器自动注入注解，业务 DAO 实现类不重写。具体参数类型和泛型能否由容器正确解析，必须根据当前项目和本地 xbatis 源码确认，不得猜测

DAO 内部优先使用框架已提供的 Chain 创建方法：

- 查询：`queryChain()` / `queryChain(where)`
- 更新：`updateChain()` / `updateChain(where)`
- 插入：`insertChain()`
- 删除：`deleteChain()` / `deleteChain(where)`

这些方法会自动绑定当前 Mapper 和实体类型，比在业务代码里手写 `Chain.of(mapper, Entity.class)` 更简单，也更不容易混入错误模式。

如果项目已有 DAO 层：

- 数据库操作代码不要放到 Service 层
- SQL / Chain 构造不要放到 Service 层
- where 条件构建不要散落在 Service 层
- 事务强烈推荐开在 DAO 方法上，不要默认放到 Service 层
- Service 负责业务编排，数据库访问交给 DAO，查询条件交给 `QO` 查询对象或 DAO 内部方法

## 多 Mapper 模式

多 Mapper 模式通常表现为：

- 一个实体对应一个 `MybatisMapper<T>`
- 每个实体有自己的 Mapper 接口
- 旧代码或无 DAO 代码里可能出现 `QueryChain.of(userMapper)`

适合：

- 已经按实体 Mapper 组织的现有项目
- Mapper 粒度明确的系统
- 需要按实体边界划分查询职责的系统

### 多 Mapper 模式下的默认写法

实体 Mapper：

- `public interface UserMapper extends MybatisMapper<User> {}`

QueryChain：

- DAO 内部优先 `queryChain()...`

自定义 SQL：

- 自定义方法一般写在具体实体 Mapper 下
- XML namespace 通常对应具体实体 Mapper

DAO：

- `public interface UserDao extends Dao<User, Long> {}`
- `public class UserDaoImpl extends BaseDao<User, Long> implements UserDao {}`

UpdateChain / InsertChain / DeleteChain：

- DAO 内部使用 `updateChain()...execute()`
- DAO 内部使用 `insertChain()...execute()`
- DAO 内部使用 `deleteChain()...execute()`

### 多 Mapper 模式下 Agent 的规则

1. 新增实体时，默认新增对应 Mapper
2. 默认同时生成对应 DAO
3. 不要无故引入 `BasicMapper`
4. 不要为了少一个接口，把项目改成单 Mapper 风格
5. Service 层优先调用 DAO 方法，不直接持有具体实体 Mapper
6. Mapper 注入收敛到项目 BaseDao 的 `setMapper(...)`，并补 Spring、Solon 等容器自动注入注解；业务 DAO 实现类不重写 `setMapper(...)`
7. 业务 DAO 接口继承 `Dao<T, ID>`，实现类继承项目 BaseDao 并实现业务 DAO 接口

## 单 Mapper 模式

项目如果启用了单 Mapper 模式，则：

- 会定义一个继承 `BasicMapper` 的接口
- 通常会命名为统一的 `XbatisMapper`
- 不需要主动调用 `XbatisGlobalConfig.setSingleMapperClass(...)`
- 旧代码或无 DAO 代码里可能出现 `QueryChain.of(basicMapper, Entity.class)`
- CRUD 时可能通过 `basicMapper.save(Entity)` 或 `basicMapper.getById(Entity.class, id)` 调用

Agent 在修改代码前必须先确认：

1. 项目是否已经启用单 Mapper 模式
2. 代码生成是否已经围绕 `BasicMapper`
3. DAO / Repository 是否建立在 `BasicDaoImpl` 风格之上

### 单 Mapper 模式下的默认写法

Mapper：

- 定义一个统一 `XbatisMapper extends BasicMapper`
- Spring 项目配置 `@MapperScan` 扫描这个统一 Mapper 所在包；如果项目已使用 `markerInterface = BasicMapper.class`，延续现有配置
- 不生成 `XbatisGlobalConfig.setSingleMapperClass(...)` 调用

QueryChain：

- DAO 内部优先 `queryChain()...`

按主键查询或删除：

- `basicMapper.getById(Entity.class, id)`
- `basicMapper.getById(Entity.class, id, Entity::getName, Entity::getStatus)` 用于按 id 返回单表部分列
- `basicMapper.getValueById(Entity.class, id, Entity::getName)` 用于按 id 返回单列值
- `basicMapper.deleteById(Entity.class, id)`
- 按 id 查询实体、部分列或单列值时，不要默认写 `QueryChain`

DAO：

- `public interface UserDao extends Dao<User, Long> {}`
- `public class UserDaoImpl extends BaseDao<User, Long> implements UserDao {}`

UpdateChain / InsertChain / DeleteChain：

- DAO 内部使用 `updateChain()...execute()`
- DAO 内部使用 `insertChain()...execute()`
- DAO 内部使用 `deleteChain()...execute()`

XML：

- XML namespace 对应统一的 `XbatisMapper` 或当前项目约定的统一 `BasicMapper` 子接口
- 自定义 SQL id 可能带实体名前缀，例如 `User:selectXxx`

### 单 Mapper 模式下 Agent 的规则

1. 不要再新增每实体一个 `MybatisMapper<T>`
2. 不要把 `QueryChain.of(entityMapper)` 风格混进来
3. DAO 层使用项目 BaseDao，BaseDao 基于 `BasicDaoImpl<T, ID>`
4. 自定义 SQL、withSqlSession、代码生成都要围绕统一 Mapper 设计
5. Service 层优先调用 DAO 方法，不直接持有 `BasicMapper`
6. 统一 Mapper 注入收敛到项目 BaseDao 的 `setMapper(...)`，并配合 Spring、Solon 等容器自动注入注解完成；业务 DAO 实现类不重写
7. 业务 DAO 接口继承 `Dao<T, ID>`，实现类继承项目 BaseDao 并实现业务 DAO 接口
8. 不主动调用 `XbatisGlobalConfig.setSingleMapperClass(...)`

## 判断规则

如果你看到下面任一特征，就要优先按单 Mapper 模式思考：

- 自定义 `MybatisBasicMapper extends BasicMapper`
- 自定义 `XbatisMapper extends BasicMapper`
- `@MapperScan(... markerInterface = BasicMapper.class)`
- DAO BaseDao类继承 `BasicDaoImpl`

如果你看到下面这些特征，就优先按多 Mapper 模式思考：

- 大量实体各自拥有 `XxxMapper extends MybatisMapper<Xxx>`
- `@MapperScan("...mapper")` 扫描的是实体 Mapper 包
- 旧代码或无 DAO 代码里常见 `QueryChain.of(userMapper)`
- XML namespace 直接对应各个实体 Mapper

## 选型规则

新项目默认优先推荐单 Mapper 模式。

已有项目默认不要主动切换项目模式。

只有在用户明确要求重构整体 Mapper 架构时，才讨论单 Mapper 和多 Mapper 的切换。

在普通任务里：

- 单 Mapper 项目就继续单 Mapper
- 多 Mapper 项目就继续多 Mapper

## 审查重点

代码审查时，优先检查这些问题：

1. 当前改动是否与项目现有 Mapper 模式一致
2. 项目 BaseDao 基类是否与当前模式一致：单 Mapper 用 `BasicDaoImpl`，多 Mapper 用 `DaoImpl`
3. 单 Mapper 模式下是否存在统一 `XbatisMapper extends BasicMapper`，以及 `@MapperScan` 是否对齐该模式
4. 有 DAO 层时，事务是否强烈推荐定义在 DAO 方法上
5. 自定义 SQL 的 namespace 和调用方式是否与当前模式一致
6. DAO / Repository 是否错误混入了另一种模式
7. `QueryChain` / `UpdateChain` / `InsertChain` / `DeleteChain` 是否优先在 DAO 内通过框架方法创建
8. 项目 BaseDao 的 `setMapper(...)` 是否带 Spring、Solon 等容器自动注入注解，业务 DAO 实现类是否避免重复重写
9. 业务 DAO 是否有接口，且接口继承 `Dao<T, ID>` 而不是 `IDao<T, ID>`
10. 基础按 id、save、update 方法是否保持框架真实命名和签名

高风险问题：

1. 项目已启用单 Mapper，却新增一套实体 Mapper 模式
2. 项目是多 Mapper 模式，却凭空引入 `BasicMapper`
3. 单 Mapper 模式下 BaseDao 继承了 `DaoImpl`
4. 多 Mapper 模式下 BaseDao 继承了 `BasicDaoImpl`
5. 单 Mapper 模式下仍然以多 Mapper 习惯写 Chain
6. 有 DAO 层却把事务主要开在 Service 层，导致事务边界和数据库访问分离
7. 单 Mapper 模式下没有统一 `XbatisMapper` 或 `@MapperScan` 配置与单 Mapper 入口不一致
8. 多 Mapper 模式下把公共查询硬塞进统一 Mapper，导致职责混乱
9. 业务 DAO 通过构造方法一路传 Mapper，或每个子类重复重写 `setMapper(...)`
10. 项目 BaseDao 的 `setMapper(...)` 缺少 Spring、Solon 等容器自动注入注解，导致 DAO 无法按统一方式装配
11. 业务 DAO 里堆满 `getById`、`save`、`update`、`deleteById`、`count`、`exists` 这类基础能力的简单转发方法
12. 业务 DAO 没有接口，或接口继承了不建议开发者使用的 `IDao<T, ID>`
13. 基础方法被二次命名为 `findById`、`create`、`modify`，偏离框架 Dao / BaseDao 真实 API
14. 单 Mapper 模式下主动调用 `XbatisGlobalConfig.setSingleMapperClass(...)`

## 不推荐行为

1. 在同一业务模块中混用单 Mapper 和多 Mapper 风格
2. 不确认全局配置就生成 Mapper
3. 因个人偏好随意切换当前项目的 Mapper 模式
4. 有 DAO 层却绕过 DAO 直接在业务层创建 Chain
5. 有 DAO 层却把事务主要放到 Service 层
6. 业务 DAO 明明已有统一 BaseDao 注入规范，却继续使用构造方法传 Mapper 或重复重写 `setMapper(...)`
7. 业务 DAO 编写大量和 BaseDao / 内置 Mapper 重复的简单方法
8. 不创建业务 DAO 接口，或业务 DAO 接口继承 `IDao<T, ID>`
9. 对基础按 id、save、update 方法做二次命名包装
