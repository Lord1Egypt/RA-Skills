# DevOps 部署规范

## 概述

DDD 项目需要统一的 DevOps 部署规范，包括 Docker 环境部署、应用部署、SQL 脚本管理和配置文件管理。

## 目录结构

```
project/
├── docs/
│   └── dev-ops/
│       ├── docker-compose-environment-aliyun.yml  # 基础环境部署（MySQL、Redis、RabbitMQ等）
│       ├── docker-compose-app.yml                  # 应用服务部署
│       ├── mysql/
│       │   └── {database}.sql                      # 数据库初始化脚本
│       └── README.md                               # 部署说明
├── {project}-app/
│   └── src/main/resources/
│       ├── application.yml                         # 主配置
│       ├── application-dev.yml                     # 开发环境配置
│       ├── application-test.yml                    # 测试环境配置
│       ├── application-prod.yml                    # 生产环境配置
│       ├── application-redis.yml                   # Redis 配置（可选）
│       ├── application-mq.yml                      # RabbitMQ 配置（可选）
│       └── application-mybatis.yml                 # MyBatis 配置（可选）
```

## 一、Docker Compose 环境部署

### 1. 基础环境部署脚本

**文件**: `docs/dev-ops/docker-compose-environment-aliyun.yml`

```yaml
version: '3.8'

services:
  # MySQL 8.0
  mysql:
    image: mysql:8.0
    container_name: {project}-mysql
    restart: always
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: {database}
      TZ: Asia/Shanghai
    volumes:
      - ./mysql:/docker-entrypoint-initdb.d
      - mysql_data:/var/lib/mysql
    command: 
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
      - --default-authentication-plugin=mysql_native_password
    networks:
      - {project}-network

  # Redis 6.x
  redis:
    image: redis:6.2
    container_name: {project}-redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    networks:
      - {project}-network

  # RabbitMQ
  rabbitmq:
    image: rabbitmq:3.9-management
    container_name: {project}-rabbitmq
    restart: always
    ports:
      - "5672:5672"    # AMQP
      - "15672:15672"  # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin123
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - {project}-network

networks:
  {project}-network:
    driver: bridge

volumes:
  mysql_data:
  redis_data:
  rabbitmq_data:
```

### 2. 应用部署脚本

**文件**: `docs/dev-ops/docker-compose-app.yml`

```yaml
version: '3.8'

services:
  # 应用服务
  {project}-app:
    image: openjdk:17-jdk-slim
    container_name: {project}-app
    restart: always
    ports:
      - "8080:8080"
    environment:
      SPRING_PROFILES_ACTIVE: prod
      TZ: Asia/Shanghai
      # 数据库配置
      MYSQL_HOST: mysql
      MYSQL_PORT: 3306
      MYSQL_DATABASE: {database}
      MYSQL_USER: root
      MYSQL_PASSWORD: root123
      # Redis 配置
      REDIS_HOST: redis
      REDIS_PORT: 6379
      # RabbitMQ 配置
      RABBITMQ_HOST: rabbitmq
      RABBITMQ_PORT: 5672
      RABBITMQ_USER: admin
      RABBITMQ_PASSWORD: admin123
    volumes:
      - ../{project}-app/target/{project}-app-1.0.jar:/app/app.jar
      - ./logs:/app/logs
    command: java -jar /app/app.jar
    networks:
      - {project}-network
    depends_on:
      - mysql
      - redis
      - rabbitmq

networks:
  {project}-network:
    external: true
```

### 3. 部署命令

```bash
# 进入项目 dev-ops 目录
cd docs/dev-ops

# 部署基础环境（MySQL、Redis、RabbitMQ）
docker-compose -f docker-compose-environment-aliyun.yml up -d

# 部署应用服务
docker-compose -f docker-compose-app.yml up -d

# 查看容器状态
docker-compose -f docker-compose-environment-aliyun.yml ps
docker-compose -f docker-compose-app.yml ps

# 查看日志
docker-compose -f docker-compose-app.yml logs -f {project}-app

# 停止服务
docker-compose -f docker-compose-app.yml down
docker-compose -f docker-compose-environment-aliyun.yml down
```

## 二、SQL 脚本规范

### 1. SQL 文件命名

```
docs/dev-ops/mysql/
├── easyform.sql           # 主数据库脚本
├── easyform_init.sql      # 初始化数据脚本（可选）
└── README.md              # SQL 说明文档
```

### 2. SQL 文件格式要求

**必须包含**：
1. 创建数据库语句
2. 使用数据库语句
3. 建表语句
4. 初始化数据（可选）

**示例**: `docs/dev-ops/mysql/easyform.sql`

```sql
-- =============================================
-- Easy Form 数据库初始化脚本
-- Author: xiaofuge bugstack.cn @小傅哥
-- Create: 2026-03-25
-- =============================================

-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS easyform
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

-- 2. 使用数据库
USE easyform;

-- 3. 用户表
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '用户ID',
    `username` VARCHAR(50) NOT NULL COMMENT '用户名',
    `password` VARCHAR(100) NOT NULL COMMENT '密码',
    `mobile` VARCHAR(20) DEFAULT NULL COMMENT '手机号',
    `email` VARCHAR(100) DEFAULT NULL COMMENT '邮箱',
    `real_name` VARCHAR(50) DEFAULT NULL COMMENT '真实姓名',
    `status` VARCHAR(20) DEFAULT 'ENABLED' COMMENT '状态：ENABLED/DISABLED',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_username` (`username`),
    UNIQUE KEY `uk_mobile` (`mobile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 4. 鉴权规则表
DROP TABLE IF EXISTS `auth_rule`;
CREATE TABLE `auth_rule` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '规则ID',
    `name` VARCHAR(100) NOT NULL COMMENT '规则名称',
    `type` VARCHAR(20) NOT NULL COMMENT '规则类型：token/mobile/idcard/custom',
    `rule` VARCHAR(500) DEFAULT NULL COMMENT '规则表达式',
    `config` TEXT DEFAULT NULL COMMENT '规则配置JSON',
    `status` VARCHAR(20) DEFAULT 'ENABLED' COMMENT '状态：ENABLED/DISABLED',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='鉴权规则表';

-- 5. 表单定义表
DROP TABLE IF EXISTS `form_definition`;
CREATE TABLE `form_definition` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '表单ID',
    `code` VARCHAR(50) NOT NULL COMMENT '表单编码',
    `name` VARCHAR(100) NOT NULL COMMENT '表单名称',
    `description` VARCHAR(500) DEFAULT NULL COMMENT '表单描述',
    `status` VARCHAR(20) DEFAULT 'DRAFT' COMMENT '状态：DRAFT/PUBLISHED/OFFLINE',
    `require_auth` TINYINT(1) DEFAULT 0 COMMENT '是否需要鉴权',
    `auth_type` VARCHAR(20) DEFAULT NULL COMMENT '鉴权类型',
    `auth_rule_id` BIGINT DEFAULT NULL COMMENT '鉴权规则ID',
    `visit_count` BIGINT DEFAULT 0 COMMENT '访问次数',
    `submit_count` BIGINT DEFAULT 0 COMMENT '提交次数',
    `create_by` BIGINT DEFAULT NULL COMMENT '创建人',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_by` BIGINT DEFAULT NULL COMMENT '更新人',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='表单定义表';

-- 6. 表单字段表
DROP TABLE IF EXISTS `form_field`;
CREATE TABLE `form_field` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '字段ID',
    `form_id` BIGINT NOT NULL COMMENT '表单ID',
    `name` VARCHAR(50) NOT NULL COMMENT '字段名称',
    `label` VARCHAR(100) NOT NULL COMMENT '字段标签',
    `type` VARCHAR(20) NOT NULL COMMENT '字段类型：text/number/email/select/checkbox/radio/date/textarea',
    `required` TINYINT(1) DEFAULT 0 COMMENT '是否必填',
    `placeholder` VARCHAR(200) DEFAULT NULL COMMENT '字段提示',
    `default_value` VARCHAR(500) DEFAULT NULL COMMENT '默认值',
    `options` TEXT DEFAULT NULL COMMENT '字段选项JSON',
    `sort` INT DEFAULT 0 COMMENT '排序号',
    `create_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY `idx_form_id` (`form_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='表单字段表';

-- 7. 表单提交表
DROP TABLE IF EXISTS `form_submission`;
CREATE TABLE `form_submission` (
    `id` BIGINT NOT NULL AUTO_INCREMENT COMMENT '提交ID',
    `form_id` BIGINT NOT NULL COMMENT '表单ID',
    `form_name` VARCHAR(100) DEFAULT NULL COMMENT '表单名称',
    `user_id` BIGINT DEFAULT NULL COMMENT '提交人用户ID',
    `user_name` VARCHAR(50) DEFAULT NULL COMMENT '提交人名称',
    `data` TEXT NOT NULL COMMENT '提交数据JSON',
    `status` VARCHAR(20) DEFAULT 'PENDING' COMMENT '状态：PENDING/APPROVED/REJECTED',
    `submit_ip` VARCHAR(50) DEFAULT NULL COMMENT '提交IP',
    `submit_time` DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '提交时间',
    `approve_time` DATETIME DEFAULT NULL COMMENT '审核时间',
    `remark` VARCHAR(500) DEFAULT NULL COMMENT '审核备注',
    PRIMARY KEY (`id`),
    KEY `idx_form_id` (`form_id`),
    KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='表单提交表';

-- =============================================
-- 初始化数据
-- =============================================

-- 初始化管理员用户
INSERT INTO `user` (`username`, `password`, `mobile`, `email`, `real_name`, `status`)
VALUES ('admin', 'e10adc3949ba59abbe56e057f20f883e', '13800000000', 'admin@easyform.com', '管理员', 'ENABLED');

-- 初始化默认鉴权规则
INSERT INTO `auth_rule` (`name`, `type`, `rule`, `status`)
VALUES ('默认Token认证', 'token', '{"header":"Authorization","prefix":"Bearer "}', 'ENABLED');
```

## 三、配置文件规范

### 1. 主配置文件

**文件**: `{project}-app/src/main/resources/application.yml`

```yaml
spring:
  application:
    name: {project}
  profiles:
    active: dev
  config:
    import:
      - application-redis.yml
      - application-mq.yml
      - application-mybatis.yml
```

### 2. 环境配置文件

**开发环境**: `application-dev.yml`

```yaml
server:
  port: 8080

spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/{database}?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai&useSSL=false
    username: root
    password: root123
    hikari:
      pool-name: {project}-hikari
      minimum-idle: 5
      maximum-pool-size: 20
      idle-timeout: 300000
      connection-timeout: 30000
      max-lifetime: 1800000

logging:
  level:
    root: INFO
    cn.bugstack: DEBUG
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n"
```

**测试环境**: `application-test.yml`

```yaml
server:
  port: 8080

spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://${MYSQL_HOST:localhost}:${MYSQL_PORT:3306}/${MYSQL_DATABASE:{database}}?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai&useSSL=false
    username: ${MYSQL_USER:root}
    password: ${MYSQL_PASSWORD:root123}

logging:
  level:
    root: INFO
    cn.bugstack: INFO
```

**生产环境**: `application-prod.yml`

```yaml
server:
  port: 8080

spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DATABASE}?useUnicode=true&characterEncoding=utf8&serverTimezone=Asia/Shanghai&useSSL=true
    username: ${MYSQL_USER}
    password: ${MYSQL_PASSWORD}
    hikari:
      pool-name: {project}-hikari-prod
      minimum-idle: 10
      maximum-pool-size: 50
      idle-timeout: 300000
      connection-timeout: 30000
      max-lifetime: 1800000

logging:
  level:
    root: WARN
    cn.bugstack: INFO
  file:
    name: /app/logs/{project}.log
```

### 3. 组件配置文件（复杂配置拆分）

**Redis 配置**: `application-redis.yml`

```yaml
spring:
  redis:
    host: ${REDIS_HOST:localhost}
    port: ${REDIS_PORT:6379}
    password: ${REDIS_PASSWORD:}
    database: 0
    lettuce:
      pool:
        max-active: 20
        max-idle: 10
        min-idle: 5
        max-wait: 3000ms
    timeout: 5000ms
```

**RabbitMQ 配置**: `application-mq.yml`

```yaml
spring:
  rabbitmq:
    host: ${RABBITMQ_HOST:localhost}
    port: ${RABBITMQ_PORT:5672}
    username: ${RABBITMQ_USER:admin}
    password: ${RABBITMQ_PASSWORD:admin123}
    virtual-host: /
    listener:
      simple:
        acknowledge-mode: manual
        prefetch: 10
        concurrency: 5
        max-concurrency: 20
```

**MyBatis 配置**: `application-mybatis.yml`

```yaml
mybatis:
  mapper-locations: classpath:/mapper/*.xml
  type-aliases-package: cn.bugstack.{project}.infrastructure.dao.po
  configuration:
    map-underscore-to-camel-case: true
    cache-enabled: false
    log-impl: org.apache.ibatis.logging.stdout.StdOutImpl
```

## 四、部署流程

### 1. 本地开发环境部署

```bash
# 1. 进入项目目录
cd {project}/docs/dev-ops

# 2. 启动基础环境
docker-compose -f docker-compose-environment-aliyun.yml up -d

# 3. 等待 MySQL 初始化完成（约 30 秒）
docker-compose -f docker-compose-environment-aliyun.yml logs -f mysql

# 4. 验证数据库
docker exec -it {project}-mysql mysql -uroot -proot123 -e "SHOW DATABASES;"

# 5. 本地启动应用（IDEA 或命令行）
mvn spring-boot:run -pl {project}-app
```

### 2. 服务器部署

```bash
# 1. 打包应用
mvn clean package -Dmaven.test.skip=true

# 2. 上传到服务器
scp -r docs/dev-ops user@server:/home/{project}/
scp {project}-app/target/{project}-app-1.0.jar user@server:/home/{project}/

# 3. 服务器上启动
cd /home/{project}/dev-ops
docker-compose -f docker-compose-environment-aliyun.yml up -d
docker-compose -f docker-compose-app.yml up -d

# 4. 查看日志
docker-compose -f docker-compose-app.yml logs -f
```

## 五、常见问题

### 1. MySQL 连接失败

**问题**: Sequel Ace 连接 MySQL 8.0 失败

**原因**: MySQL 8.0 默认使用 `caching_sha2_password` 认证插件

**解决**:
```bash
docker exec {project}-mysql mysql -uroot -proot123 -e "ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'root123'; FLUSH PRIVILEGES;"
```

### 2. 容器网络问题

**问题**: 应用容器无法连接 MySQL/Redis

**解决**: 确保使用同一个 Docker 网络
```yaml
networks:
  {project}-network:
    driver: bridge
```

### 3. 端口冲突

**问题**: 3306/6379/5672 端口被占用

**解决**: 修改 docker-compose.yml 中的端口映射
```yaml
ports:
  - "13306:3306"  # 改为非标准端口
```
