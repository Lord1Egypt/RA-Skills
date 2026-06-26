# 依赖替换矩阵

## 核心版本（参考）

- `spring-boot-starter-parent`: `3.5.8`
- `spring-cloud.version`: `2025.0.0`
- `spring-cloud-alibaba.version`: `2025.0.0.0`

## 坐标替换

1. MyBatis Plus

- 旧：`com.baomidou:mybatis-plus-spring-boot-starter`
- 新：`com.baomidou:mybatis-plus-spring-boot3-starter`

2. Druid

- 旧：`com.alibaba:druid-spring-boot-starter`
- 新：`com.alibaba:druid-spring-boot-3-starter`

3. Sleuth

- 旧：`org.springframework.cloud:spring-cloud-starter-sleuth`
- 新：`io.micrometer:micrometer-tracing-bridge-brave`

4. Servlet/Annotation

- 旧：`javax.servlet:javax.servlet-api`
- 新：`jakarta.servlet:jakarta.servlet-api`

- 增加：`jakarta.annotation:jakarta.annotation-api`

5. Mail

- 旧：`javax.mail`
- 新：`org.eclipse.angus:jakarta.mail`

6. OpenAPI

- 删除：`knife4j-openapi2-spring-boot-starter`（如存在）
- 增加：`org.springdoc:springdoc-openapi-starter-webmvc-ui`

7. OkHttp

- 升级到 5.x 时增加：`com.squareup.okhttp3:okhttp-jvm`

8. 微服务标准依赖

- 增加：`com.baiwang.basictools:bw-spring-boot-starter-microservice-blocking`

## 辅助工具升级（可选）

- 引入 `org.openrewrite.maven:rewrite-maven-plugin`
- recipe：`com.baiwang.rewrite.java.spring.UpgradeBoot27To35`
- 执行：`mvn rewrite:run`
