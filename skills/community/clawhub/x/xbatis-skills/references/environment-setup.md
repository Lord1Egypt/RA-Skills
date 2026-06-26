# Environment Setup

适用于以下场景：

- 新建 xbatis 项目骨架
- 给现有 Spring Boot / Solon 项目接入 xbatis
- 生成 starter 依赖、数据源配置、启动类、Mapper 扫描配置
- 判断单 Mapper / 多 Mapper 在不同容器环境下的落地方式

## 总原则

生成环境接入代码时，先遵循这些规则：

1. 先识别当前运行环境：Spring Boot 2 / 3 / 4，还是 Solon
2. 已有项目优先跟随现有环境、已有 parent、已有 starter、已有数据源方案
3. 不要在同一模块里同时生成 Spring Boot 和 Solon 两套接入代码
4. 版本号优先以当前本地 xbatis 源码 README 或官网对应章节为准，不要凭空硬编码旧版本
5. 先把容器、数据源、Mapper 扫描接起来，再生成实体、Mapper、DAO、Service
6. 开发环境必须开启 xbatis POJO 安全检查；测试和生产环境不要求默认开启；不知道真实注解包名或配置项时，先查当前 starter 依赖和本地源码
7. 无特殊要求时，项目必须集成 Lombok；实体、VO、QO、DTO、Model 优先使用 Lombok，字段常量按需使用 `@FieldNameConstants`

## 版本选择

生成依赖时，优先按官方章节对应关系选版本：

- Spring Boot 2：`xbatis-spring-boot-parent` 的普通版本线
- Spring Boot 3：`xbatis-spring-boot-parent` 的 `-spring-boot3` 版本线
- Spring Boot 4：`xbatis-spring-boot-parent` 的 `-spring-boot4` 版本线
- Solon：`xbatis-solon-plugin`

不要把 skill 中写死的版本号当成永远正确。生成代码前，优先从以下来源确认当前版本：

- 本地 `xbatis-source/README.md`
- 本地 `xbatis-source/README.zh-CN.md`
- 官方站对应章节：springboot2 / springboot3 / springboot4 / solon

## Spring Boot 接入

### Maven 依赖

Spring Boot 项目优先使用：

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>cn.xbatis</groupId>
            <artifactId>xbatis-spring-boot-parent</artifactId>
            <version>${xbatis.version}</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <dependency>
        <groupId>cn.xbatis</groupId>
        <artifactId>xbatis-spring-boot-starter</artifactId>
    </dependency>
</dependencies>
```

补充规则：

- `xbatis.version` 按当前 Spring Boot 主版本选择对应版本线
- JDBC 驱动必须补，例如 `mysql-connector-j`
- 连接池优先复用 Spring Boot 默认或项目现有方案；不要无故再引入另一套数据源实现
- 无特殊要求时必须补 Lombok 依赖；版本优先交给 Spring Boot parent 或项目依赖管理，不要凭空硬编码

Lombok 依赖示例：

```xml
<dependency>
    <groupId>org.projectlombok</groupId>
    <artifactId>lombok</artifactId>
    <optional>true</optional>
</dependency>
```

### 数据源配置

优先在 `application.yml` / `application.yaml` 中生成：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/demo
    username: root
    password: 123456
```

只有项目已有显式 `DataSource` Bean 习惯，或需要特殊数据源能力时，才再生成 `@Bean DataSource`。

### 启动类与 Mapper 扫描

基础写法：

```java
@SpringBootApplication
@MapperScan("com.example.mapper")
public class XbatisApplication {

    public static void main(String[] args) {
        SpringApplication.run(XbatisApplication.class, args);
    }
}
```

单 Mapper 模式补充规则：

- 如果项目统一定义 `XbatisMapper extends BasicMapper`，优先扫描统一 Mapper 所在包
- 如果项目已使用 `markerInterface = BasicMapper.class`，延续现有配置
- 单 Mapper 模式下不需要主动生成或调用 `XbatisGlobalConfig.setSingleMapperClass(...)`

多 Mapper 模式补充规则：

- `@MapperScan` 优先扫描实体 Mapper 包
- 不要为多 Mapper 项目强行切成单 Mapper 风格

### POJO 安全检查

开发环境必须开启 xbatis POJO 安全检查，用于启动时检查 VO、Model、条件对象、排序对象的映射和注解缺口。

Spring / Spring Boot 项目优先使用当前 starter 支持的 `@XbatisPojoCheckScan`：

`basePackages` 方案：

```java
@Profile("dev")
@Configuration
@XbatisPojoCheckScan(
        basePackages = "com.example"
)
public class XbatisSafeCheckConfig {
}
```

细分包路径方案：

```java
@Profile("dev")
@Configuration
@XbatisPojoCheckScan(
        modelPackages = "com.example.model",
        resultEntityPackages = "com.example.vo",
        conditionTargetPackages = "com.example.qo",
        orderByTargetPackages = "com.example.qo"
)
public class XbatisSafeCheckConfig {
}
```

注意：

- README 记录的注解包名是 `org.mybatis.spring.boot.autoconfigure.XbatisPojoCheckScan`
- 当前 xbatis core 源码里没有该类型；生成 import 前必须从当前项目依赖或本地 starter 源码确认真实包名
- 新项目默认只生成 dev profile 下的安全检查配置；测试和生产环境不要求默认开启
- `basePackages` 和 `modelPackages` / `resultEntityPackages` / `conditionTargetPackages` / `orderByTargetPackages` 是二选一的扫描方案，不要同时生成
- 扫描范围必须覆盖 VO、Model、QO、排序对象所在包，不要只扫描实体包

## Solon 接入

### Maven 依赖

Solon 项目优先使用：

```xml
<!-- 注意顺序 -->
<dependency>
    <groupId>cn.xbatis</groupId>
    <artifactId>xbatis-solon-plugin</artifactId>
    <version>${xbatis.solon.version}</version>
</dependency>

<dependency>
    <groupId>org.noear</groupId>
    <artifactId>mybatis-solon-plugin</artifactId>
    <version>${mybatis.solon.version}</version>
</dependency>
```

规则：

- `xbatis-solon-plugin` 放在 `mybatis-solon-plugin` 前面
- 版本号优先按本地源码或官方 solon 章节确认
- 无特殊要求时必须补 Lombok 依赖；版本优先沿用项目依赖管理

### solon.yml 配置

优先生成：

```yaml
ds:
  schema: demo
  jdbcUrl: jdbc:mysql://localhost:3306/demo?useUnicode=true&characterEncoding=utf8
  driverClassName: com.mysql.cj.jdbc.Driver
  username: root
  password: 123456

mybatis.master:
  pojoCheck:
    basePackages: com.example
  mappers:
    - "com.example.mapper"
    - "classpath:mapper/**/*.xml"
```

或使用细分包路径方案：

```yaml
mybatis.master:
  pojoCheck:
    modelPackages: com.example.model
    resultEntityPackages: com.example.vo
    conditionTargetPackages: com.example.qo
    orderByTargetPackages: com.example.qo
  mappers:
    - "com.example.mapper"
    - "classpath:mapper/**/*.xml"
```

注意：

- `mybatis.<数据源 bean 名称>` 要和数据源 Bean 名称对应
- `mappers` 可放包路径，也可放 XML 路径
- 开发环境必须配置 `pojoCheck`；多数据源项目要在 dev 配置中对应 `mybatis.<beanName>` 下配置
- 测试和生产环境不要求默认配置 `pojoCheck`；除非项目明确要求，不要在 test/prod 配置里生成
- `basePackages` 和其他细分包路径是二选一方案，不要在同一个 `pojoCheck` 中同时生成
- `pojoCheck` 路径可按项目约定使用逗号分隔的多个包路径

### DataSource Bean

Solon 项目优先保持和官方示例一致：

```java
@Configuration
public class MybatisConfig {

    @Bean(name = "master", typed = true)
    public DataSource dataSource(@Inject("${ds}") HikariDataSource ds) {
        return ds;
    }
}
```

### 使用方式

Solon 中如果项目已把 Mapper 托管到容器：

- 优先沿用项目现有注入方式
- `@Db`、`@Inject`、直接注入 Mapper 哪种是现有规范，就跟随哪种

不要在 Solon 项目里生成 Spring 的 `@Autowired`、`@SpringBootApplication`、`application.yml` 风格代码。

## 代码生成时的默认落地顺序

生成接入代码时，优先按这个顺序：

1. 识别环境：Spring Boot 2 / 3 / 4 或 Solon
2. 生成或对齐 xbatis 依赖
3. 生成或对齐 JDBC 驱动 / 数据源配置
4. 生成启动类、容器配置类、`@MapperScan` 或 Solon Bean
5. 生成 dev 环境的 xbatis POJO 安全检查配置
6. 再生成 Mapper、BaseDao、业务 DAO、实体、QO、VO、Model

## 环境接入后的生成检查

提交前检查：

1. 依赖是否和当前环境主版本匹配
2. Spring Boot 2 / 3 / 4 是否选对了对应版本线
3. Solon 插件顺序是否正确
4. 数据源配置是否和容器风格一致
5. `@MapperScan` 是否和单 Mapper / 多 Mapper 模式一致
6. 是否没有同时混入另一套容器代码
7. 项目 BaseDao 的 `setMapper(...)` 是否已经按当前容器使用自动注入注解，业务 DAO 子类是否不重复重写
8. dev 环境是否已经开启 xbatis POJO 安全检查，并覆盖 VO、Model、QO、排序对象所在包；test/prod 是否避免默认开启

## 不推荐行为

1. 不识别当前环境就直接生成依赖
2. 在 Spring Boot 项目里生成 Solon 配置
3. 在 Solon 项目里生成 Spring Boot 启动类
4. 不核对版本线就硬编码旧版 `xbatis.version`
5. 单 Mapper / 多 Mapper 还没判断，就先生成 `@MapperScan`
6. 生成 xbatis 项目骨架却漏掉 dev 的 POJO 安全检查配置
7. 在项目未要求时，为 test/prod 默认开启 POJO 安全检查
