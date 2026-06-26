# Gradle 多模块依赖配置

## 模块划分原则

```
domain/         # 核心领域，零框架依赖
application/    # 应用层，依赖领域层
infrastructure/ # 基础设施，实现领域接口
interfaces/     # 用户界面层，依赖应用层
```

## 根项目 build.gradle

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.2.x' apply false
    id 'io.spring.dependency-management' version '1.1.x' apply false
}

ext {
    set('springBootVersion', '3.2.x')
}

subprojects {
    repositories {
        mavenCentral()
    }

    group = 'com.company'
    version = '1.0.0'

    java {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    tasks.withType(JavaCompile) {
        options.encoding = 'UTF-8'
    }
}
```

## domain 模块

**零依赖原则**：只依赖通用工具库，不依赖 Spring、JPA 等。

```groovy
// :domain/build.gradle
plugins {
    id 'java-library'
}

dependencies {
    // 允许：纯 Java 工具库
    implementation 'org.apache.commons:commons-lang3:3.14.0'
    implementation 'org.jetbrains:annotations:24.1.0'

    // 禁止：spring-*, javax.persistence, jackson, 数据库驱动等
}
```

**domain 层禁止引入的依赖**：
- `spring-*`
- `javax.persistence` / `jakarta.persistence`
- `jackson-*`
- 数据库驱动（MySQL, PostgreSQL 等）
- 任何 HTTP 客户端
- 消息队列客户端

## application 模块

**只依赖领域层 + 必要的事务管理**。

```groovy
// :application/build.gradle
plugins {
    id 'java-library'
}

dependencies {
    implementation project(':domain')

    // 允许：仅事务相关
    implementation 'org.springframework:spring-tx'

    // 禁止：spring-boot-starter（完整启动器）、
    //       jpa、data-jpa、数据源等
}
```

## infrastructure 模块

**实现所有领域接口，引入完整技术栈**。

```groovy
// :infrastructure/build.gradle
plugins {
    id 'org.springframework.boot'
    id 'io.spring.dependency-management'
}

dependencies {
    implementation project(':domain')
    implementation project(':application')

    implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
    implementation 'org.springframework.boot:spring-boot-starter-validation'
    implementation 'org.springframework:spring-context'

    runtimeOnly 'com.mysql:mysql-connector-j'

    // 防腐层外部调用
    implementation 'com.squareup.okhttp3:okhttp:4.12.0'
}
```

## interfaces 模块

**REST API 层，引入 Web 框架**。

```groovy
// :interfaces/build.gradle
plugins {
    id 'org.springframework.boot'
    id 'io.spring.dependency-management'
}

dependencies {
    implementation project(':application')

    implementation 'org.springframework.boot:spring-boot-starter-web'
    implementation 'org.springframework.boot:spring-boot-starter-validation'

    // OpenAPI 文档（可选）
    implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.3.0'
}
```

## settings.gradle

```groovy
rootProject.name = 'dddsample'

include 'domain'
include 'application'
include 'infrastructure'
include 'interfaces'
```

## Spring Boot 启动类

启动类放在 `interfaces` 模块，依赖倒置装配基础设施。

```java
// interfaces/src/main/java/.../DddSampleApplication.java
@SpringBootApplication
@EnableTransactionManagement
@ComponentScan(
    basePackages = "com.company",
    excludeFilters = @ComponentScan.Filter(
        type = FilterType.REGEX,
        pattern = "infrastructure.*"
    )
)
public class DddSampleApplication {
    public static void main(String[] args) {
        SpringApplication.run(DddSampleApplication.class, args);
    }
}
```

## 依赖倒置配置

基础设施层通过 `@Configuration` 类显式注册实现：

```java
// infrastructure/src/main/java/.../InfrastructureConfig.java
@Configuration
public class InfrastructureConfig {

    @Bean
    public OrderRepository orderRepository(OrderJpaRepository jpaRepo,
                                            OrderDataConverter converter) {
        return new OrderRepositoryImpl(jpaRepo, converter);
    }

    @Bean
    public PaymentGateway paymentGateway() {
        return new AlipayGatewayAdapter();
    }
}
```

## 依赖方向检查

可通过 ArchUnit 在测试中强制依赖方向：

```groovy
// 在任一模块的测试中
testImplementation 'com.tngtech.archunit:archunit-junit5:1.2.1'
```

```java
@ArchTest
static final ArchRule domainShouldNotDependOnInfrastructure =
    noClasses()
        .that().resideInAPackage("..domain..")
        .should().dependOnClassesThat()
        .resideInAPackage("..infrastructure..");
```
