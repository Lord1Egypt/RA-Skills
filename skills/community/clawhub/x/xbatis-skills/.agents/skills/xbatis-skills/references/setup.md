# 接入与模块总览

## 仓库结构

- 根 `pom.xml` 是聚合工程，当前版本是 `1.9.9`。
- `xbatis-annotation`：注解、分页字段、监听注解。
- `xbatis-sql-api`：SQL 抽象接口与调用解析。
- `xbatis-sql-api-impl`：数据库函数实现，核心入口是 `db.sql.api.impl.cmd.Methods`。
- `xbatis-core`：Mapper、链式 DSL、分页、租户、逻辑删除、MVC 支撑。
- `xbatis-bom` / `xbatis-parent`：依赖管理与父 POM。

## 常见接入方式

### Spring Boot 3

README 给出的依赖坐标：

```xml
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>cn.xbatis</groupId>
            <artifactId>xbatis-spring-boot-parent</artifactId>
            <version>1.9.9</version>
            <type>pom</type>
            <scope>import</scope>
        </dependency>
    </dependencies>
</dependencyManagement>

<dependencies>
    <dependency>
        <groupId>cn.xbatis</groupId>
        <artifactId>xbatis-spring-boot3-starter</artifactId>
    </dependency>
</dependencies>
```

最小启动骨架：

```java
@SpringBootApplication
@MapperScan("com.example.mapper")
public class XbatisApplication {
    public static void main(String[] args) {
        SpringApplication.run(XbatisApplication.class, args);
    }
}
```

### Spring Boot 2

- 仍使用 `xbatis-spring-boot-parent:1.9.9`
- starter 改为 `xbatis-spring-boot-starter`

### Solon

README 约定的依赖顺序：

1. `cn.xbatis:xbatis-solon-plugin`
2. `org.noear:mybatis-solon-plugin`

常见配置点：

- `ds.*` 定义数据源
- `mybatis.<beanName>.mappers` 配置包扫描或 XML 扫描
- 单数据源可用 `@Db`，多数据源显式写 `@Db("master")`

## 全局配置

真实类名是 `cn.xbatis.core.XbatisGlobalConfig`，不是 README 里的概念路径。

高频配置点：

- `setTableUnderline(...)` / `setColumnUnderline(...)`：下划线策略
- `setDatabaseCaseRule(...)`：数据库大小写规则
- `setDynamicValue(...)`：注册动态默认值
- `setLogicDeleteInterceptor(...)` / `setLogicDeleteSwitch(...)`：逻辑删除行为
- `setGlobalOnInsertListener(...)` / `setGlobalOnUpdateListener(...)`：全局写入监听
- `setPagingProcessor(...)`：按数据库定制分页
- `addMapperMethodInterceptor(...)`：扩展 Mapper 方法拦截

源码里 `onInit()` 会注册这些内置动态值：

- `{BLANK}`
- `{EMPTY}`
- `{NOW}`
- `{TODAY}`

## 实用接入约定

- 搜索接口优先显式声明 `mybatis.configuration.databaseId`，减少数据库自动识别开销。
- 业务代码先选 xbatis DSL，再考虑手写 SQL。
- 如果要做 AI 自动生成，优先同时生成 Mapper、实体、VO、条件 DTO 和开发环境安全检查配置，避免只生成半套结构。
- 开发环境必须开启 POJO 安全检查；测试和生产环境不要求默认开启，除非项目明确要求。

## 需要额外验证的能力

- `@XbatisPojoCheckScan` 在 README 中写明为 `org.mybatis.spring.boot.autoconfigure.XbatisPojoCheckScan`，当前仓库源码里没有这个类型；把它视为 README 记录的 starter 接入能力。
- `GeneratorConfig` 在 README 中有说明，但当前仓库模块里没有对应源码；使用前先确认实际依赖来源。
