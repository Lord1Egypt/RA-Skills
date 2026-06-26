# xfg-ddd-skills · DDD 工程解决方案

> 一套完整的 DDD 六边形架构工程搭建与开发解决方案。
> 从项目创建、分层设计、代码规范到 DevOps 部署，覆盖工程全生命周期。
>
> 📦 **ClawHub 地址**: https://clawhub.ai/fuzhengwei/xfg-ddd-skills

---

## 这是什么

**xfg-ddd-skills** 是一个面向 AI 编程助手（QClaw）的技能包，让 AI 具备 DDD 工程的完整落地能力。

日常开发中，DDD 最大的痛点不是理论，而是**落地**：

- 项目怎么搭？模块怎么划分？包名怎么定？
- Entity、Aggregate、VO 各放哪里？怎么写？
- Repository 接口定义在哪层？实现放哪里？
- 业务复杂了，Case 层怎么编排？
- 策略模式、责任链怎么在 DDD 里用？
- 部署时 Docker、docker-compose 怎么配？

这个技能包把上述问题的答案全部沉淀下来，让 AI 在你开口说"帮我创建 DDD 项目"或"帮我设计这个领域"时，直接给出符合规范的工程结构和代码。

---

## 环境准备

本技能包配套的脚手架需要以下环境：

| 工具 | 版本要求 | 安装方式 |
|------|----------|----------|
| **JDK** | 17+ | [Eclipse Temurin](https://adoptium.net/) / `brew install openjdk@17` |
| **Maven** | 3.8.x | [官方下载](https://maven.apache.org/download.cgi) / `brew install maven` |

### 验证安装

```bash
java -version        # 应显示 17.x.x
mvn -version         # 应显示 3.8.x
```

### 配置国内镜像（推荐）

编辑 `~/.m2/settings.xml` 配置阿里云镜像，加速依赖下载：

```xml
<mirrors>
  <mirror>
    <id>aliyunmaven</id>
    <name>阿里云公共仓库</name>
    <url>https://maven.aliyun.com/repository/public</url>
    <mirrorOf>central</mirrorOf>
  </mirror>
</mirrors>
```

---

## 使用技巧

### 一、创建项目

#### 方式一：AI 对话创建（推荐）

在 QClaw 中直接说：

```
帮我在 /path/to/workspace 创建一个 DDD 项目，名称为 xfg-xxx
```

AI 会引导确认参数并自动生成完整工程。

**对话示例**：

```
用户：帮我创建一个 DDD 项目
AI：好的，我来帮您创建 DDD 项目。请问您希望将项目创建在哪个目录？
     例如：
     1) /Users/xxx/projects
     2) /Users/xxx/Documents
     3) 其他路径（请直接输入）

用户：创建在 /Users/xxx/projects 下
AI：确认在 /Users/xxx/projects 下创建项目，开始执行...
```

#### 方式二：Maven 命令行创建

```bash
mvn archetype:generate \
  -DarchetypeGroupId=io.github.fuzhengwei \
  -DarchetypeArtifactId=ddd-scaffold-std-jdk17 \
  -DarchetypeVersion=1.8 \
  -DarchetypeRepository=https://maven.xiaofuge.cn/ \
  -DgroupId=cn.bugstack \
  -DartifactId=your-project-name \
  -Dversion=1.0.0-SNAPSHOT \
  -Dpackage=cn.bugstack.your.project \
  -B
```

#### 方式三：IDEA 图形界面创建

<details>
<summary>展开查看配置步骤</summary>

1. 编辑 `~/.m2/settings.xml` 添加脚手架仓库：

```xml
<profiles>
  <profile>
    <id>xfg-archetype</id>
    <repositories>
      <repository>
        <id>xfg-archetype-repo</id>
        <url>https://maven.xiaofuge.cn/</url>
        <releases><enabled>true</enabled></releases>
        <snapshots><enabled>false</enabled></snapshots>
      </repository>
    </repositories>
    <pluginRepositories>
      <pluginRepository>
        <id>xfg-archetype-plugin-repo</id>
        <url>https://maven.xiaofuge.cn/</url>
        <releases><enabled>true</enabled></releases>
        <snapshots><enabled>false</enabled></snapshots>
      </pluginRepository>
    </pluginRepositories>
  </profile>
</profiles>

<activeProfiles>
  <activeProfile>xfg-archetype</activeProfile>
</activeProfiles>
```

2. 执行 `mvn archetype:update-local-catalog` 更新本地目录

3. IDEA → `File → New → Project → Maven Archetype` → 搜索 `ddd-scaffold-std-jdk17`

4. 若列表未出现，点击 **Add Archetype** 手动填写：
   - GroupId：`io.github.fuzhengwei`
   - ArtifactId：`ddd-scaffold-std-jdk17`
   - Version：`1.8`

</details>

---

### 二、开发功能

项目创建后，按以下流程与 AI 协作开发：

#### 1. 创建领域模型

告诉 AI 你要创建什么：

```
帮我在 xfg-form 项目中创建一个表单提交领域，包含：
- 表单实体（FormEntity）：表单ID、表单名称、创建人、状态
- 表单状态枚举（FormStatusEnumVO）：草稿、已发布、已归档
- 表单提交值对象（FormSubmitVO）：字段ID、字段值
```

AI 会自动生成：
- `domain/form/model/entity/FormEntity.java`
- `domain/form/model/valobj/FormStatusEnumVO.java`
- `domain/form/model/valobj/FormSubmitVO.java`

#### 2. 创建仓储接口

```
为 FormEntity 创建仓储接口，支持：
- 根据ID查询表单
- 保存表单
- 更新表单状态
```

AI 生成：
- `domain/form/adapter/repository/IFormRepository.java`
- `infrastructure/adapter/repository/FormRepositoryImpl.java`
- `infrastructure/dao/IFormDao.java`
- `infrastructure/dao/po/FormPO.java`

#### 3. 创建领域服务

```
创建表单服务，实现以下能力：
- 创建表单（校验名称唯一性，初始状态为草稿）
- 发布表单（状态从草稿变为已发布）
- 提交表单数据（校验表单已发布，保存提交记录）
```

AI 生成：
- `domain/form/service/IFormService.java`
- `domain/form/service/impl/FormServiceImpl.java`

#### 4. 复杂业务编排（Case 层）

当业务涉及多个领域协作时：

```
创建一个表单审批 Case，流程如下：
1. 查询表单配置
2. 校验用户权限
3. 执行审批逻辑
4. 发送审批通知
5. 记录审批日志
```

AI 生成：
- `cases/form/approval/IFormApprovalCase.java`
- `cases/form/approval/impl/FormApprovalCaseImpl.java`

#### 5. 添加 HTTP 接口

```
为表单模块添加 HTTP 接口：
- POST /api/form/create - 创建表单
- GET /api/form/{formId} - 查询表单详情
- POST /api/form/submit - 提交表单数据
```

AI 生成：
- `trigger/http/FormController.java`

---

### 三、设计模式落地

在 DDD 中使用设计模式，直接告诉 AI：

#### 策略模式

```
表单审批有多种策略：
- 自动审批：无需人工，直接通过
- 人工审批：需要管理员审核
- 条件审批：根据金额阈值决定

使用策略模式实现，在 EnumVO 中定义策略路由。
```

#### 责任链模式

```
表单提交需要经过以下校验：
1. 表单存在性校验
2. 表单状态校验（已发布）
3. 必填字段校验
4. 字段格式校验

使用责任链模式实现，支持动态组装校验链。
```

---

### 四、项目部署

#### 1. 本地启动

```bash
# 进入项目目录
cd your-project

# 编译打包
mvn clean install -DskipTests

# 启动应用
cd your-project-app
mvn spring-boot:run
```

#### 2. Docker 部署

项目已包含标准部署配置，直接执行：

```bash
# 1. 进入部署目录
cd docs/dev-ops

# 2. 启动基础环境（MySQL、Redis）
docker-compose -f docker-compose-environment-aliyun.yml up -d

# 3. 等待 MySQL 就绪（约30秒）
sleep 30

# 4. 初始化数据库
docker exec -i mysql mysql -uroot -p123456 < mysql/sql/your_project.sql

# 5. 构建应用镜像
cd ../../your-project-app
docker build -t system/your-project:1.0.0 .

# 6. 启动应用
cd ../docs/dev-ops
docker-compose -f docker-compose-app.yml up -d

# 7. 验证部署
curl http://localhost:8080/actuator/health
```

#### 3. 生产环境部署

生产环境建议：
- 使用 `application-prod.yml` 配置
- 配置外部 MySQL、Redis 连接
- 使用阿里云镜像加速：`registry.cn-hangzhou.aliyuncs.com/xfg-studio/`

详细配置见 [references/devops-deployment.md](references/devops-deployment.md)

---

## 架构全景

```
┌─────────────────────────────────────────────────────────────┐
│                      触发层 Trigger                          │
│              (HTTP Controller / MQ Listener / Job)           │
│              职责：接收请求，路由转发，不含业务逻辑            │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                       API 层                                 │
│                  (DTO / Request / Response)                  │
│              职责：定义对外契约，纯数据结构                   │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      编排层 Case                             │
│              (业务编排 / 跨域协作 / 流程串联)                 │
│              职责：组合多个领域服务，完成复杂业务场景          │
└─────────────────────────┬───────────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      领域层 Domain                           │
│          (Entity / Aggregate / VO / Domain Service)         │
│              职责：核心业务逻辑，不依赖任何基础设施            │
└─────────────────────────┬───────────────────────────────────┘
                          ▲
┌─────────────────────────────────────────────────────────────┐
│                  基础设施层 Infrastructure                   │
│        (Repository Impl / Port Adapter / DAO / PO)          │
│              职责：实现领域层接口，处理数据持久化与外部调用    │
└─────────────────────────────────────────────────────────────┘
```

**核心依赖规则**：`Trigger → API → Case → Domain ← Infrastructure`

Domain 层不依赖任何框架，Infrastructure 层实现 Domain 层定义的接口。

---

## 工程结构

脚手架生成的标准多模块工程：

```
your-project/
├── your-project-types/          # 公共类型：枚举、常量、异常
├── your-project-domain/         # 领域层：Entity、Aggregate、VO、Service、接口定义
├── your-project-infrastructure/ # 基础设施层：Repository 实现、DAO、PO、Gateway
├── your-project-api/            # API 层：DTO、对外接口定义
├── your-project-case/           # 编排层：跨域业务流程编排
├── your-project-trigger/        # 触发层：HTTP Controller、MQ Listener、Job
├── your-project-app/            # 启动入口：Spring Boot Application
└── docs/dev-ops/                # 部署配置：docker-compose 模板
```

### Domain 层内部结构

```
domain/{bounded-context}/
├── adapter/
│   ├── port/                    # 外部系统端口接口（防腐层）
│   │   └── IXxxPort.java        # 远程调用抽象（HTTP/RPC）
│   └── repository/              # 仓储接口
│       └── IXxxRepository.java  # 数据持久化抽象
├── model/
│   ├── aggregate/               # 聚合对象（跨实体的事务边界）
│   ├── entity/                  # 实体（含命令实体 XxxCommandEntity）
│   └── valobj/                  # 值对象（含枚举 XxxEnumVO）
└── service/                     # 领域服务
    ├── IXxxService.java
    └── {capability}/
        └── XxxServiceImpl.java
```

### Infrastructure 层内部结构

```
infrastructure/
├── adapter/
│   ├── repository/              # 实现 Domain 层 IXxxRepository
│   └── port/                    # 实现 Domain 层 IXxxPort
├── dao/                         # MyBatis DAO 接口
│   └── po/                      # 数据库映射 PO 对象
├── gateway/                     # HTTP/RPC 客户端
│   └── dto/                     # 远程调用 DTO
└── redis/                       # Redis 配置
```

---

## 参考文档

| 主题 | 文档 |
|------|------|
| 架构概览 | [references/architecture.md](references/architecture.md) |
| 项目结构 | [references/project-structure.md](references/project-structure.md) |
| 命名规范 | [references/naming.md](references/naming.md) |
| 实体设计 | [references/entity.md](references/entity.md) |
| 聚合根设计 | [references/aggregate.md](references/aggregate.md) |
| 值对象设计 | [references/value-object.md](references/value-object.md) |
| 仓储模式 | [references/repository.md](references/repository.md) |
| 端口与适配器 | [references/port-adapter.md](references/port-adapter.md) |
| 领域服务 | [references/domain-service.md](references/domain-service.md) |
| 领域设计指南 | [references/domain-design-guide.md](references/domain-design-guide.md) |
| 领域核心模式 | [references/domain-patterns.md](references/domain-patterns.md) |
| 编排层设计 | [references/case-layer.md](references/case-layer.md) |
| 触发层设计 | [references/trigger-layer.md](references/trigger-layer.md) |
| 基础设施层 | [references/infrastructure-layer.md](references/infrastructure-layer.md) |
| 基础设施模式 | [references/infrastructure-patterns.md](references/infrastructure-patterns.md) |
| DevOps 部署 | [references/devops-deployment.md](references/devops-deployment.md) |
| Docker 镜像 | [references/docker-images.md](references/docker-images.md) |

---

## 参考项目

| 项目 | 说明 |
|------|------|
| [group-buy-market](https://bugstack.cn/md/project/group-buy-market/group-buy-market.html) | 拼团营销领域完整实现，含策略模式、责任链、领域事件 |
| [ai-mcp-gateway](https://bugstack.cn/md/project/ai-mcp-gateway/ai-mcp-gateway.html) | AI MCP 网关领域完整实现，含端口适配器、多模型路由 |

---

## License

MIT © [小傅哥 bugstack.cn](https://bugstack.cn)
