---
name: springboot27-to-35-upgrade
description: 将 Spring Boot 2.7 项目升级到 Spring Boot 3.5 的实战流程，覆盖版本基线、依赖坐标替换、Jakarta 迁移、配置兼容、异步上下文传递改造与验证门禁。用于企业多模块 Maven 项目升级与排障。
---

# Spring Boot 2.7 -> 3.5 升级

按固定阶段执行，优先保证可编译、可启动、可回归。

## 快速入口

1. 先读 `references/upgrade-checklist.md`，确定环境与迁移顺序。
2. 再读 `references/dependency-replacement-matrix.md`，按坐标替换依赖。
3. 执行 `references/pitfall-cookbook.md` 的代码级坑点改造。
4. 若父 POM 是 `bw-spring-boot-starter-parent-security`，执行 `references/enterprise-parent-security.md`。

## 执行阶段

### 1) 基线准备

- 统一 JDK 21、Maven 3.9+。
- 建立升级分支并记录当前编译状态。
- 识别启动入口模块（通常 `*-startup`）。

### 2) 依赖升级

- 先升级 parent/BOM，再替换不兼容坐标。
- `spring-cloud-starter-sleuth` 迁移至 Micrometer Tracing。
- `mybatis-plus-spring-boot3-starter`、`druid-spring-boot-3-starter` 等 Boot3 坐标替换到位。

### 3) 代码改造

- 执行 `javax.*` 到 `jakarta.*` 的精确迁移。
- 替换 `@EnableEurekaClient` 为 `@EnableDiscoveryClient`。
- 修复文件上传判断、线程池上下文传递、trace 工具调用等高频坑点。

### 4) 配置收敛

- `spring.redis.*` 迁移为 `spring.data.redis.*`。
- 网关链路追踪补充 `spring.reactor.contextPropagation: AUTO` 与 tracing 传播配置。
- 修正 Logback 与 OpenAPI 文档配置。

### 5) 验证门禁

- 根工程编译通过。
- 启动模块编译/启动通过。
- 核心接口冒烟通过。
- 关键日志告警（初始化失败、依赖冲突）清零或可解释。

## 输出要求

每次执行升级后输出：

1. 变更文件与变更原因。
2. 依赖替换结果与残留冲突。
3. 验证命令及结果。
4. 未完成项与后续建议。
