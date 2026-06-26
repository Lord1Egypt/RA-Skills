# 项目脚手架指南

## 多模块 Gradle 项目结构

```
project-root/
├── build.gradle
├── settings.gradle
├── gradle.properties
├── gradlew
├── gradlew.bat
└── modules/
    ├── domain/
    │   ├── build.gradle
    │   └── src/
    │       ├── main/java/
    │       └── test/java/
    ├── application/
    │   ├── build.gradle
    │   └── src/
    │       ├── main/java/
    │       └── test/java/
    ├── infrastructure/
    │   ├── build.gradle
    │   └── src/
    │       ├── main/java/
    │       ├── main/resources/
    │       └── test/java/
    └── interfaces/
        ├── build.gradle
        └── src/
            ├── main/java/
            ├── main/resources/
            └── test/java/
```

## 各层 Stub 类示例

### 领域层基类

```java
// domain/src/main/java/.../AggregateRoot.java
public abstract class AggregateRoot<T extends DomainObjectId> {
    private final T id;
    private final List<DomainEvent> domainEvents = new ArrayList<>();

    protected AggregateRoot(T id) {
        this.id = Objects.requireNonNull(id);
    }

    protected void registerEvent(DomainEvent event) {
        this.domainEvents.add(event);
    }

    public List<DomainEvent> getDomainEvents() {
        return Collections.unmodifiableList(domainEvents);
    }

    public void clearEvents() {
        this.domainEvents.clear();
    }

    public T getId() {
        return id;
    }
}
```

```java
// domain/src/main/java/.../DomainException.java
public class DomainException extends RuntimeException {
    public DomainException(String message) {
        super(message);
    }
}
```

### 领域层值对象基类

```java
// domain/src/main/java/.../ValueObject.java
public abstract class ValueObject<T> {
    protected abstract Object[] getAttributes();

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        ValueObject<?> that = (ValueObject<?>) o;
        return Arrays.equals(getAttributes(), that.getAttributes());
    }

    @Override
    public int hashCode() {
        return Arrays.hashCode(getAttributes());
    }
}
```

### 应用层命令/查询基类

```java
// application/src/main/java/.../ApplicationService.java
public interface ApplicationService {
    // 标记接口，区分应用服务与其他服务
}
```

```java
// application/src/main/java/.../Command.java
public interface Command {
    // 命令标记接口
}
```

```java
// application/src/main/java/.../Query.java
public interface Query<T> {
    // 查询标记接口，T 为返回结果类型
}
```

### 基础设施层配置

```java
// infrastructure/src/main/java/.../InfrastructureConfig.java
@Configuration
public class InfrastructureConfig {
    // 仓储实现、数据源、消息发布等 Bean 配置
}
```

### 接口层启动类

```java
// interfaces/src/main/java/.../Application.java
@SpringBootApplication
@EnableTransactionManagement
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
```

### Spring Boot 配置

```properties
# interfaces/src/main/resources/application.yml
spring:
  application:
    name: ddd-sample

  datasource:
    url: jdbc:mysql://localhost:3306/ddd_sample
    driver-class-name: com.mysql.cj.jdbc.Driver

  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        format_sql: true

server:
  port: 8080
```

## 快速启动检查清单

- [ ] Gradle 多模块结构已创建
- [ ] 各模块 build.gradle 配置正确
- [ ] domain 层无框架依赖
- [ ] 基类（AggregateRoot, DomainException）已创建
- [ ] 依赖方向通过 ArchUnit 测试验证
- [ ] application.yml 配置完成
- [ ] 启动类可正常启动
