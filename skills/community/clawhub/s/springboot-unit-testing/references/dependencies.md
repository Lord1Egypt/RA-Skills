# Spring Boot单元测试依赖配置

## Maven依赖配置

### 核心测试依赖
```xml
<!-- Spring Boot Test Starter -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

<!-- MyBatis Test -->
<dependency>
    <groupId>org.mybatis.spring.boot</groupId>
    <artifactId>mybatis-spring-boot-starter-test</artifactId>
    <version>2.3.1</version>
    <scope>test</scope>
</dependency>

<!-- JUnit 5 -->
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-api</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-engine</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter-params</artifactId>
    <scope>test</scope>
</dependency>

<!-- Mockito -->
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
```

### 增强测试依赖
```xml
<!-- AssertJ - 流式断言 -->
<dependency>
    <groupId>org.assertj</groupId>
    <artifactId>assertj-core</artifactId>
    <scope>test</scope>
</dependency>

<!-- Hamcrest - 匹配器 -->
<dependency>
    <groupId>org.hamcrest</groupId>
    <artifactId>hamcrest-library</artifactId>
    <scope>test</scope>
</dependency>

<!-- H2 Database - 内存数据库 -->
<dependency>
    <groupId>com.h2database</groupId>
    <artifactId>h2</artifactId>
    <scope>test</scope>
</dependency>

<!-- Testcontainers - 容器化测试 -->
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>mysql</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>

<!-- Faker - 测试数据生成 -->
<dependency>
    <groupId>com.github.javafaker</groupId>
    <artifactId>javafaker</artifactId>
    <version>1.0.2</version>
    <scope>test</scope>
</dependency>

<!-- Awaitility - 异步测试 -->
<dependency>
    <groupId>org.awaitility</groupId>
    <artifactId>awaitility</artifactId>
    <version>4.2.0</version>
    <scope>test</scope>
</dependency>
```

### 覆盖率工具
```xml
<!-- JaCoCo - 代码覆盖率 -->
<dependency>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.8</version>
</dependency>
```

## 完整pom.xml测试配置

```xml
<build>
    <plugins>
        <!-- Maven Surefire Plugin -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>2.22.2</version>
            <configuration>
                <includes>
                    <include>**/*Test.java</include>
                    <include>**/*Tests.java</include>
                </includes>
                <excludes>
                    <exclude>**/*IT.java</exclude>
                    <exclude>**/*IntegrationTest.java</exclude>
                </excludes>
                <systemPropertyVariables>
                    <java.awt.headless>true</java.awt.headless>
                </systemPropertyVariables>
            </configuration>
        </plugin>

        <!-- Maven Failsafe Plugin (集成测试) -->
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-failsafe-plugin</artifactId>
            <version>2.22.2</version>
            <executions>
                <execution>
                    <goals>
                        <goal>integration-test</goal>
                        <goal>verify</goal>
                    </goals>
                </execution>
            </executions>
            <configuration>
                <includes>
                    <include>**/*IT.java</include>
                    <include>**/*IntegrationTest.java</include>
                </includes>
            </configuration>
        </plugin>

        <!-- JaCoCo Plugin -->
        <plugin>
            <groupId>org.jacoco</groupId>
            <artifactId>jacoco-maven-plugin</artifactId>
            <version>0.8.8</version>
            <executions>
                <execution>
                    <goals>
                        <goal>prepare-agent</goal>
                    </goals>
                </execution>
                <execution>
                    <id>report</id>
                    <phase>test</phase>
                    <goals>
                        <goal>report</goal>
                    </goals>
                </execution>
                <execution>
                    <id>check</id>
                    <phase>verify</phase>
                    <goals>
                        <goal>check</goal>
                    </goals>
                    <configuration>
                        <rules>
                            <rule>
                                <element>BUNDLE</element>
                                <limits>
                                    <limit>
                                        <counter>LINE</counter>
                                        <value>COVEREDRATIO</value>
                                        <minimum>0.85</minimum>
                                    </limit>
                                    <limit>
                                        <counter>BRANCH</counter>
                                        <value>COVEREDRATIO</value>
                                        <minimum>0.80</minimum>
                                    </limit>
                                    <limit>
                                        <counter>METHOD</counter>
                                        <value>COVEREDRATIO</value>
                                        <minimum>0.90</minimum>
                                    </limit>
                                    <limit>
                                        <counter>CLASS</counter>
                                        <value>COVEREDRATIO</value>
                                        <minimum>0.95</minimum>
                                    </limit>
                                </limits>
                            </rule>
                        </rules>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

## 测试环境配置

### application-test.yml (单元测试)
```yaml
spring:
  datasource:
    url: jdbc:h2:mem:testdb;DB_CLOSE_DELAY=-1;DB_CLOSE_ON_EXIT=FALSE;MODE=MySQL
    driver-class-name: org.h2.Driver
    username: sa
    password:
  
  h2:
    console:
      enabled: true
      path: /h2-console
  
  mybatis:
    mapper-locations: classpath:mapper/*.xml
    type-aliases-package: com.example.demo.entity
    configuration:
      map-underscore-to-camel-case: true
      log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
  
  sql:
    init:
      mode: always
      schema-locations: classpath:schema.sql
      data-locations: classpath:test-data.sql

logging:
  level:
    com.example.demo: DEBUG
    org.springframework: INFO
    org.mybatis: DEBUG

test:
  database:
    name: testdb
```

### application-integration.yml (集成测试)
```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/testdb?useSSL=false&allowPublicKeyRetrieval=true&serverTimezone=UTC
    username: root
    password: password
    driver-class-name: com.mysql.cj.jdbc.Driver
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
      connection-timeout: 30000
  
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.MySQL8Dialect
        format_sql: true

testcontainers:
  mysql:
    image: mysql:8.0
    database-name: testdb
    username: test
    password: test
```

## 测试注解配置

### 测试Profile配置
```java
// 测试基类配置
@TestPropertySource(properties = {
    "spring.profiles.active=test",
    "spring.datasource.url=jdbc:h2:mem:testdb",
    "spring.jpa.hibernate.ddl-auto=create-drop"
})
@ActiveProfiles("test")
public abstract class BaseTest {
    // 公共测试配置
}
```

### 自定义测试注解
```java
// 组合注解简化配置
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Transactional
public @interface SpringBootIntegrationTest {
}

@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@MybatisTest
@AutoConfigureTestDatabase(replace = Replace.NONE)
@Sql("/test-data.sql")
public @interface MybatisIntegrationTest {
}
```

## 测试工具类配置

### TestConstants.java
```java
public final class TestConstants {
    
    // 数据库常量
    public static final String TEST_DB_URL = "jdbc:h2:mem:testdb";
    public static final String TEST_DB_USERNAME = "sa";
    public static final String TEST_DB_PASSWORD = "";
    
    // 测试数据常量
    public static final Long TEST_USER_ID = 1L;
    public static final String TEST_USERNAME = "testuser";
    public static final String TEST_EMAIL = "test@example.com";
    public static final String TEST_PHONE = "13800138000";
    
    // 时间常量
    public static final LocalDateTime TEST_CREATE_TIME = 
        LocalDateTime.of(2024, 1, 1, 12, 0, 0);
    public static final LocalDateTime TEST_UPDATE_TIME = 
        LocalDateTime.of(2024, 1, 2, 12, 0, 0);
    
    // 状态常量
    public static final Integer ACTIVE_STATUS = 1;
    public static final Integer INACTIVE_STATUS = 0;
    public static final Integer DELETED_STATUS = -1;
    
    private TestConstants() {
        // 防止实例化
    }
}
```

## 最佳实践配置

### 1. 测试隔离配置
```yaml
# 每个测试使用独立的数据库
spring.datasource.url: jdbc:h2:mem:test-${random.uuid};DB_CLOSE_DELAY=-1
```

### 2. 测试并行执行配置
```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <configuration>
        <parallel>methods</parallel>
        <threadCount>4</threadCount>
        <useUnlimitedThreads>false</useUnlimitedThreads>
        <perCoreThreadCount>true</perCoreThreadCount>
    </configuration>
</plugin>
```

### 3. 测试资源清理配置
```java
@Configuration
@Profile("test")
public class TestCleanupConfig {
    
    @Bean
    @Qualifier("testCleanupExecutor")
    public ExecutorService testCleanupExecutor() {
        return Executors.newFixedThreadPool(2);
    }
}
```

## 故障排除配置

### 测试日志配置
```yaml
logging:
  level:
    # 详细调试信息
    org.springframework.test: DEBUG
    org.springframework.transaction: DEBUG
    org.springframework.jdbc: DEBUG
    
    # SQL语句日志
    org.mybatis.spring: TRACE
    org.apache.ibatis: TRACE
    
    # 数据库连接池
    com.zaxxer.hikari: DEBUG
    
  pattern:
    console: "%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n"
```

### 测试超时配置
```java
// 测试类级别超时配置
@TestPropertySource(properties = {
    "test.timeout.unit=5000",
    "test.timeout.integration=30000",
    "test.timeout.long.running=120000"
})
public class TimeoutConfigTest {
    // 测试方法
}
```

## 版本兼容性

### Spring Boot版本兼容
- Spring Boot 2.7.x: 推荐版本，长期支持
- Spring Boot 3.x.x: 需要调整部分配置
- JDK 11+: 推荐使用JDK 11或更高版本

### 数据库版本兼容
- MySQL 8.0+: 生产环境推荐
- H2 2.x.x: 测试环境推荐
- MariaDB 10.5+: 兼容MySQL 8.0

### 工具版本建议
- JUnit 5.8+: 最新稳定版本
- Mockito 4.x+: 支持Java 11+
- AssertJ 3.24+: 功能最完整
- Testcontainers 1.18+: 支持最新Docker特性