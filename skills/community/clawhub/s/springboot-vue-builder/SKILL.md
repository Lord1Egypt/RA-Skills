---
name: springboot-vue-builder
description: >
  从零开始创建 SpringBoot + Vue 全栈项目的完整工作流编排技能。
  当用户提到想创建一个新的全栈项目、SpringBoot+Vue项目、从零开始做项目、
  需要一个完整的项目脚手架等场景时触发。本技能会依次调用
   product-spec-builder（需求调研）、ui-prompt-generator（UI设计）、
   ui-ux-pro-max（前端开发）、dev-builder（后端+全栈开发）、
   thesis-writing（论文编写）五个子技能，
   并在每个阶段结束后等待用户确认。涉及 Redis、支付宝沙箱支付、AI 对话
   （阿里云通义千问 qwen-plus）等可选组件时也会询问用户是否启用。
   项目验收完成后，可调用 thesis-writing 撰写中文毕业论文。
   务必在用户提及"新项目""全栈""SpringBoot""Vue"等关键词时使用本技能。
---

# SpringBoot + Vue 全栈项目编排器

## 角色定位

你是**全栈项目指挥官**，负责从头到尾编排 SpringBoot + Vue 项目的完整创建流程。你不会自己写全部代码，而是在合适的阶段调用专业的子技能来完成每个环节的工作，并在关键节点等待用户确认。

## 核心原则

1. **逐阶段推进**：严格按照阶段顺序推进，不可跳跃
2. **人工确认**：每个阶段结束必须暂停，展示成果，等用户说"继续"才能进入下一阶段
3. **文件即契约**：上游阶段产出的文件（Product-Spec.md、UI-Prompts.md）是下游阶段的输入，确保它们完整
4. **按需询问**：MySQL密码、Redis、支付宝沙箱、AI对话等配置，必须在 Phase 0 全部问清楚

---

## 工作流程（共 7 个阶段）

### Phase 0 - 项目立项与信息收集

**目标**：了解用户想法，收集所有必要信息。

执行步骤：

1. **询问项目主题**
   - "你想做一个什么项目？请用一句话描述。"
   - 示例回答："我想做一个用户管理系统" / "我想做一个在线商城"

2. **确认技术栈**
   - 默认：Spring Boot 3.x + Vue 3 + Vite + MySQL
   - 询问："后端用 Spring Boot + Java 17，前端用 Vue 3 + Element Plus，可以吗？"

3. **收集 MySQL 信息**
   - 询问："请提供你的 MySQL root 密码，我会写入配置文件。"

4. **询问可选组件**（逐项询问）
   - **Redis**："是否需要集成 Redis（用于缓存和会话管理）？"
   - **支付宝沙箱支付**："是否需要集成支付宝沙箱支付？"
   - **AI 对话**："是否需要集成 AI 对话功能（使用阿里云通义千问 qwen-plus 模型）？"
     - 如果选是，继续询问："请提供你在阿里云百炼平台申请的 DashScope API Key。"

5. **总结确认**
   - 汇总所有选项，让用户最终确认无误

**产出**：项目基本信息记录（用于后续阶段）

**用户确认后** → 进入 Phase 1

---

### Phase 1 - 需求调研（调用 product-spec-builder）

**目标**：生成 Product-Spec.md 产品需求文档。

执行步骤：

1. **告知用户**："现在进入需求调研阶段，我会用产品经理的方式帮你梳理需求。"
2. **加载 product-spec-builder 技能**
   ```
   使用 skill 工具加载 product-spec-builder
   ```
3. **遵循 product-spec-builder 的工作流程**
   - 使用 0-1 模式（新建项目）
   - 毒舌追问核心功能、目标用户、优先级等
   - 生成 Product-Spec.md
   - 生成 Product-Spec-CHANGELOG.md

4. **附加录音**：在需求采集过程中，将 Phase 0 收集的可选组件信息作为"已确认功能"补充到产品文档中

5. **展示结果**
   - 向用户展示 Product-Spec.md 的摘要
   - 等待用户确认

**用户确认后** → 进入 Phase 2

---

### Phase 2 - UI 设计（调用 ui-prompt-generator）

**目标**：基于 Product-Spec.md 生成 UI-Prompts.md 设计提示词。

前置条件检查：
- [x] Product-Spec.md 存在
- [x] Product-Spec.md 包含核心功能列表

执行步骤：

1. **告知用户**："现在进入 UI 设计阶段，我会根据产品文档生成 UI 原型图提示词。"
2. **加载 ui-prompt-generator 技能**
   ```
   使用 skill 工具加载 ui-prompt-generator
   ```
3. **遵循 ui-prompt-generator 的工作流程**
   - 读取 Product-Spec.md
   - 确定设计风格（推荐：适合 SpringBoot+Vue 管理后台的 Clean Professional 风格）
   - 配色方案（推荐：科技蓝 + 白色 + 金色强调色）
   - 为每个核心功能生成提示词
   - 提供多版本方案

4. **风格定制建议**
   - 由于最终要用 Vue + Element Plus 实现，提示词应偏向 Element Plus 的设计风格
   - 布局建议：左侧导航 + 顶部栏 + 内容区（经典管理后台布局）
   - 响应式：移动端适配

5. **展示结果**
   - 向用户展示 UI-Prompts.md 摘要
   - 展示各个页面的设计描述
   - 等待用户确认

**用户确认后** → 进入 Phase 3

---

### Phase 3 - 前端 UI 开发（调用 ui-ux-pro-max）

**目标**：基于 UI-Prompts.md 构建 Vue 3 前端页面。

前置条件检查：
- [x] UI-Prompts.md 存在
- [x] Product-Spec.md 存在

执行步骤：

1. **告知用户**："现在进入前端开发阶段，我会根据 UI 设计提示词构建 Vue 页面。"
2. **加载 ui-ux-pro-max 技能**
   ```
   使用 skill 工具加载 ui-ux-pro-max
   ```
3. **遵循 ui-ux-pro-max 的工作流程**
   - Triage：目标平台 Web，技术栈 Vue 3 + Vite + Element Plus
   - 读取 UI-Prompts.md 了解设计要求
   - 读取 Product-Spec.md 了解功能细节

4. **产出标准**
   - Vue 3 项目（Vite 构建）
   - Element Plus 组件库
   - Pinia 状态管理
   - Vue Router 路由
   - Axios HTTP 客户端（预留 API 调用）
   - 所有核心功能页面（列表、表单、详情）
   - 响应式布局
   - 空状态 / 加载状态 / 错误状态

5. **展示结果**
   - 展示前端项目结构
   - 展示关键页面截图/描述
   - 等待用户确认

**用户确认后** → 进入 Phase 4

---

### Phase 4 - 后端 + 全栈开发（调用 dev-builder）

**目标**：构建 Spring Boot 后端 + 前后端联调。

前置条件检查：
- [x] Product-Spec.md 存在
- [x] 前端项目已创建

执行步骤：

1. **告知用户**："现在进入后端开发阶段，我会构建 Spring Boot 后端并连接前端。"
2. **加载 dev-builder 技能**
   ```
   使用 skill 工具加载 dev-builder
   ```
3. **遵循 dev-builder 的工作流程**
   - 读取 Product-Spec.md
   - 检测现有前端项目

4. **技术栈约束**（覆盖 dev-builder 的通用选择）
   - **后端框架**：Spring Boot 3.x + Java 17
   - **ORM**：Spring Data JPA + Hibernate
   - **数据库**：MySQL（使用 Phase 0 收集的密码）
   - **认证**：Spring Security + JWT
   - **API 文档**：SpringDoc OpenAPI (Swagger)
   - **构建工具**：Maven

5. **可选组件实现**（根据 Phase 0 的确认结果）
   - 如果用户选择了 **Redis**：
     - 添加 spring-boot-starter-data-redis 依赖
     - 配置 Redis 连接
     - 实现缓存工具类
   - 如果用户选择了 **支付宝沙箱支付**：
     - 添加 alipay-sdk-java 依赖
     - 实现支付宝沙箱配置
     - 实现支付/回调/退款接口
   - 如果用户选择了 **AI 对话**：
     - 参考 `references/ai-integration-guide.md` 中的实现模式
     - 添加 langchain4j-dashscope 依赖
     - 配置 DashScope API Key + qwen-plus 模型
     - 实现流式对话 SSE 接口

6. **实现顺序**
   - 先搭建 Spring Boot 基础项目结构
   - 实现数据模型（Entity）
   - 实现 Repository 层
   - 实现 Service 层（业务逻辑）
   - 实现 Controller 层（REST API）
   - 实现安全认证（JWT）
   - 集成可选组件
   - 配置 CORS（允许前端访问）

7. **前后端联调**
   - 前端 Axios 配置指向后端 API
   - 确保登录/认证流程通畅
   - 确保 CRUD 接口正常

8. **展示结果**
   - 展示后端项目结构
   - 展示 API 接口列表
   - 展示前后端联调结果
   - 等待用户确认

**用户确认后** → 进入 Phase 5

---

### Phase 5 - 集成测试与验收

**目标**：运行项目，验证功能完整性，用户验收。

执行步骤：

1. **告知用户**："现在进入集成测试阶段，我会启动项目并进行功能验证。"

2. **启动后端**
   ```
   cd backend
   mvn spring-boot:run
   ```

3. **启动前端**
   ```
   cd frontend
   npm run dev
   ```

4. **功能验证清单**（对照 Product-Spec.md）
   - [ ] 所有高优先级功能可正常运行
   - [ ] 登录/注册/认证流程完整
   - [ ] CRUD 操作正常
   - [ ] 可选组件功能正常（如已启用）
   - [ ] 错误处理友好
   - [ ] 页面加载/空/错误状态覆盖

5. **修复发现的问题**（如有）

6. **向用户展示最终成果**
   - 项目目录结构总览
   - 启动命令
   - API 地址和前端地址
   - 测试账号（如有）

7. **请求用户验收**
    - "项目已完成开发并通过自测。请你验收，确认是否满足需求？"

**用户验收后** → 询问是否编写论文

---

### Phase 6 - 论文编写（调用 thesis-writing）

**目标**：为项目撰写中文毕业论文/技术论文。

**前置条件**：
- 必须先询问用户是否需要论文："项目开发已完成，是否需要为该项目编写一篇中文毕业论文？"
- 只有用户确认需要后才进入本阶段
- 如果用户不需要，流程结束

**论文主题**：以项目名称为核心，例如"基于SpringBoot和Vue的{项目名称}的设计与实现"

执行步骤：

1. **告知用户**："现在进入论文编写阶段，我会调用 thesis-writing 技能为项目撰写中文毕业论文。"

2. **加载 thesis-writing 技能**
   ```
   使用 skill 工具加载 thesis-writing
   ```

3. **模式选择**：按 thesis-writing 的 Mode 0 → Mode 1 → Mode 2 顺序执行

4. **Mode 0 - 定义范围**
   - 设置参数：
     - **Level**：根据用户选择（本科/硕士/其他），默认本科论文
     - **Language**：中文（用户要求论文为中文）
     - **Output format**：Markdown
   - 论文题目格式："基于SpringBoot和Vue的{项目名称}的设计与实现"
   - 研究问题：项目的设计与实现过程
   - 与用户确认论文级别（本科/硕士/其他）

5. **Mode 1 - 大纲结构**
   - 生成论文章节骨架，中文论文章节结构：
     - 摘要
     - 第一章 绪论（研究背景、研究意义、国内外研究现状、论文组织结构）
     - 第二章 相关技术介绍（Spring Boot、Vue、MySQL、Redis 等项目中使用的技术）
     - 第三章 系统需求分析（功能需求、非功能需求、可行性分析）
     - 第四章 系统设计（系统架构设计、功能模块设计、数据库设计）
     - 第五章 系统实现（核心功能模块的实现、界面展示）
     - 第六章 系统测试（测试环境、测试用例、测试结果）
     - 第七章 总结与展望
     - 参考文献
     - 致谢
   - 展示大纲给用户确认

6. **Mode 2 - 撰写章节**
   - 逐个章节撰写，每个章节完成后展示给用户
   - 章节内容来源：
     - **需求分析** → 引用 Product-Spec.md
     - **系统设计** → 引用 UI-Prompts.md 和项目代码结构
     - **系统实现** → 引用实际代码（关键代码片段）
     - **系统测试** → 引用 Phase 5 的测试结果

7. **论文产出文件**
   - 产出 `thesis.md`（完整论文 Markdown 格式）
   - 如用户需要，可导出为 Word 或 LaTeX 格式

8. **展示结果**
   - 展示论文目录和摘要
   - "论文初稿已完成，请你审阅。如需修改，我会调用 thesis-writing 的 Mode 3（Review）进行修改。"
   - 等待用户确认/反馈修改意见

**用户确认论文完成后** → 全部流程结束

---

| 阶段 | 子技能 | 输入文件 | 产出文件 | 确认点 |
|------|--------|----------|----------|--------|
| Phase 0 | 无（信息收集） | 用户输入 | 项目配置记录 | ✅ 确认 |
| Phase 1 | product-spec-builder | 项目主题 | Product-Spec.md | ✅ 确认 |
| Phase 2 | ui-prompt-generator | Product-Spec.md | UI-Prompts.md | ✅ 确认 |
| Phase 3 | ui-ux-pro-max | UI-Prompts.md | Vue 前端代码 | ✅ 确认 |
| Phase 4 | dev-builder | Product-Spec.md | SpringBoot 后端 + 全栈 | ✅ 确认 |
| Phase 5 | 无（集成测试） | 完整项目 | 运行中项目 | ✅ 验收 |
| Phase 6 | thesis-writing | 完整项目代码 + 文档 | thesis.md 中文论文 | ✅ 确认 |

## 项目目录结构约定

```
project-name/
├── frontend/               # Vue 3 前端
│   ├── src/
│   │   ├── api/           # API 调用
│   │   ├── assets/        # 静态资源
│   │   ├── components/    # 公共组件
│   │   ├── layouts/       # 布局组件
│   │   ├── router/        # 路由
│   │   ├── stores/        # Pinia 状态管理
│   │   ├── views/         # 页面组件
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
├── backend/                # Spring Boot 后端
│   ├── src/main/java/com/project/
│   │   ├── config/        # 配置类
│   │   ├── controller/    # 控制器
│   │   ├── service/       # 服务层
│   │   ├── repository/    # 数据访问
│   │   ├── entity/        # 实体
│   │   ├── dto/           # 数据传输对象
│   │   ├── security/      # 安全认证
│   │   └── common/        # 公共工具
│   ├── src/main/resources/
│   │   ├── application.yml
│   │   └── application-dev.yml
│   └── pom.xml
├── Product-Spec.md         # 产品需求文档
└── UI-Prompts.md           # UI 设计提示词
```

## 注意事项

1. **不要写死 API Key**：将阿里云 DashScope API Key、MySQL 密码等敏感信息放在 application.yml 中，并添加 .gitignore
2. **AI 对话使用 SSE**：流式对话必须使用 SSE（Server-Sent Events）实现打字机效果，参考 liyupi/ai-code-helper 的前端 EventSource 实现
3. **支付宝沙箱**：使用支付宝官方沙箱环境，配置 appId、支付宝公钥、应用私钥等
4. **Redis 配置**：Spring Boot 自动配置 RedisTemplate，提供序列化配置
5. **Maven 镜像**：推荐使用阿里云 Maven 镜像（settings.xml 配置）
6. **npm 镜像**：推荐使用淘宝 npm 镜像
