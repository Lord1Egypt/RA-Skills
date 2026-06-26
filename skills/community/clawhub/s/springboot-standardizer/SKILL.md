---
name: springboot-standardizer
description: |
  Java SpringBoot + MyBatis 项目标准化重构工具。用于分析非标准项目结构，
  生成标准化目录结构，提供重构迁移方案。支持标准三层架构（Controller → Service → DAO），
  自动识别 Entity/DTO/VO 分层，生成 MyBatis/Redis/Kafka 等标准配置模板。
  
  使用场景：
  - "把项目整理成标准 SpringBoot 结构"
  - "重构这个 Java 项目"
  - "标准化项目目录"
  - "生成 SpringBoot 标准配置"
  - "检查项目结构是否规范"
  
  触发关键词：springboot 标准化、项目重构、整理项目结构、mybatis 配置、
  生成标准目录、Java 项目规范、三层架构整理
---

# SpringBoot 项目标准化工具

## 功能概述

将非标准的 SpringBoot + MyBatis 项目重构为业界标准结构。

## 标准项目结构

```
src/main/java/com/{company}/{project}/
├── controller/          # REST API 控制器
│   └── UserController.java
├── service/             # 业务层接口
│   ├── UserService.java
│   └── impl/            # 业务层实现
│       └── UserServiceImpl.java
├── dao/                 # 数据访问层（Mapper 接口）
│   └── UserMapper.java
├── entity/              # 数据库实体类
│   └── User.java
├── dto/                 # 数据传输对象（API 入参）
│   ├── UserCreateDTO.java
│   └── UserUpdateDTO.java
├── vo/                  # 视图对象（API 出参）
│   └── UserVO.java
├── config/              # 配置类
│   ├── MybatisConfig.java
│   ├── RedisConfig.java
│   └── KafkaConfig.java
└── util/                # 工具类
    └── JsonUtil.java

src/main/resources/
├── mapper/              # MyBatis XML 映射文件
│   └── UserMapper.xml
├── application.yml      # 主配置文件
├── application-dev.yml  # 开发环境配置
└── application-prod.yml # 生产环境配置
```

## 工作流程

### 1. 项目扫描分析

首先扫描现有项目，识别当前结构问题：

```bash
python scripts/analyze_project.py <项目路径>
```

输出报告包括：
- 当前目录结构
- 识别出的问题（如类放错位置、命名不规范）
- 建议的迁移方案

### 2. 生成标准结构

生成标准目录结构和配置文件：

```bash
python scripts/generate_structure.py <输出路径> --package com.company.project
```

### 3. 配置文件模板

参考 `references/` 目录下的标准配置模板：
- `mybatis-config.md` — MyBatis 配置指南
- `redis-config.md` — Redis 配置模板
- `kafka-config.md` — Kafka 配置模板
- `naming-conventions.md` — 命名规范

### 4. 项目骨架模板

`assets/project-template/` 包含可直接使用的标准项目骨架。

## 使用方式

### 场景一：分析现有项目

1. 运行分析脚本扫描项目
2. 查看分析报告
3. 根据建议手动或自动重构

### 场景二：创建新项目

1. 复制 `assets/project-template/` 作为起点
2. 修改包名和配置
3. 开始开发

### 场景三：生成配置模板

根据需要读取 `references/` 中的配置模板，应用到项目中。

## 命名规范

### 包命名
- 根包：`com.{公司}.{项目}`
- 子包按层划分：controller, service, dao, entity, dto, vo, config, util

### 类命名
- Controller：`XxxController`
- Service 接口：`XxxService`
- Service 实现：`XxxServiceImpl`
- Mapper：`XxxMapper`
- Entity：`Xxx`（对应表名，驼峰命名）
- DTO：`XxxDTO` / `XxxCreateDTO` / `XxxUpdateDTO`
- VO：`XxxVO`
- Config：`XxxConfig`

### 方法命名
- Controller：HTTP 方法对应（getXxx, createXxx, updateXxx, deleteXxx）
- Service：业务语义（findXxx, saveXxx, updateXxx, deleteXxx）
- Mapper：数据库操作（selectXxx, insertXxx, updateXxx, deleteXxx）
