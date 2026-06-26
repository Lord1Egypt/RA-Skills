# 升级检查清单

## 0. 环境基线

- JDK: 21
- Maven: 3.9+
- 推荐：统一 CI 与本地 JDK，避免编译行为不一致

## 1. 版本对齐（优先）

```bash
rg -n "<parent>|spring-boot|spring-cloud|java.version|maven.compiler" -g "**/pom.xml"
```

建议版本线（来自升级资料）：

- Spring Boot: 3.5.8+
- Spring Cloud: 2025.0.0
- Spring Cloud Alibaba: 2025.0.0.0
- MyBatis Spring Boot Starter: 3.0.5
- MyBatis: 3.5.19

## 2. 父 POM 升级

如果命中企业父 POM：

- `com.baiwang.basictools:bw-spring-boot-starter-parent-security`

优先升级父版本，再处理子模块冲突。

## 3. 依赖替换

按 `dependency-replacement-matrix.md` 执行，关键替换包括：

- Sleuth -> Micrometer Tracing
- mybatis-plus boot2 starter -> boot3 starter
- druid boot2 starter -> boot3 starter
- javax.* 相关依赖 -> jakarta.* 相关依赖
- knife4j-openapi2 -> springdoc-openapi-starter-webmvc-ui

## 4. 代码迁移

```bash
rg -n "^import javax\." --glob "**/*.java"
rg -n "WebSecurityConfigurerAdapter|EnableEurekaClient|CommonsMultipartResolver|ServletFileUpload" --glob "**/*.java"
```

使用 `pitfall-cookbook.md` 中对应改造模板落地。

## 5. 配置迁移

- `spring.redis.*` -> `spring.data.redis.*`
- 网关 trace 传递配置补齐
- `springdoc` 路径配置补齐
- 检查 `spring.factories` / `AutoConfiguration.imports` 扩展点

## 6. 验证门禁

```bash
mvn -DskipTests compile
mvn -DskipTests package
mvn -DskipTests -pl <startup-module> -am compile
```

至少通过：

1. 编译通过
2. 启动通过
4. 无关键初始化异常
