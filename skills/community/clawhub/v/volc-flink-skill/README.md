# Volcano Engine Flink AI Skills（集成版）

本目录是面向 AI 场景的火山引擎 Flink “技能体系”，与同仓库的 `volc-flink-cli`（`volc_flink` 命令）整合在一起：

- 技能负责：意图理解、任务拆解、路由到合适子技能、生成可执行步骤
- CLI 负责：真实调用火山引擎 Flink API（登录/配置/资源/作业/监控等）

---

## 📁 目录结构（仓库内）

```
skills/
├── SKILL.md                          # 统一入口技能（路由）
├── README.md                         # 本说明文档
├── COMMON*.md                        # 通用约束/安全/只读/变更提示等
├── skills/                           # 子技能目录（按领域拆分）
│   ├── flink-volc/                   # 工具与 CLI 使用
│   ├── flink-auth/
│   ├── flink-config/
│   ├── flink-projects/
│   ├── flink-resource-pool/
│   ├── flink-catalog/
│   ├── flink-conn/                   # Kafka endpoint/consume 等
│   ├── flink-sql/
│   ├── flink-validate/
│   ├── flink-jar/
│   ├── flink-cdc/
│   ├── flink-sre/
│   ├── flink-savepoint/
│   ├── flink-monitor/
│   ├── flink-diagnostic/
│   └── flink-performance/
├── evals/                            # 技能评测集与结果
├── scripts/                          # 技能一致性检查与评测工具
└── docs/                             # 评测与工具链说明
```

---

## 🎯 工作原理

### 统一入口 + 智能路由

1. **统一入口**：`skills/SKILL.md` 是所有 Flink 相关问题的入口
2. **智能路由**：根据用户的问题内容，自动判断属于哪个分类
3. **子技能处理**：路由到最合适的子技能进行具体处理
4. **多技能协作**：复杂问题可以自动协调多个子技能

在本仓库的集成版形态下，工具执行通常由 `volc_flink` CLI 完成（同仓库根目录 `README.md` 有 CLI 说明）。

---

## 📚 技能分类总览

| 分类维度 | 技能名称 | 状态 | 核心功能 |
|---------|---------|------|---------|
| **🔧 volc_flink 工具管理** | flink-volc | ✅ 已完成 | 安装 volc_flink 工具，以及更新、升级、登录、配置等 |
| **🏗️ 项目与配置管理** | flink-auth | ✅ 已完成 | 登录/登出、多账号管理、AK/SK 安全管理 |
| | flink-config | ✅ 已完成 | 配置管理、默认项目设置、TOS 路径配置 |
| | flink-projects | ✅ 已完成 | 项目列举、项目详情、项目切换 |
| **💾 资源管理** | flink-resource-pool | ✅ 已完成 | 资源池列举、详情、创建 |
| | flink-catalog | ✅ 已完成 | Catalog、Database、Table 元数据管理 |
| | flink-dependency | ✅ 已完成 | JAR 包依赖管理、UDF 库管理 |
| **🔌 连接管理** | flink-conn | ✅ 已完成 | 上下游连接管理（Kafka 等），包含连接配置、接入点（Endpoint）管理、消息消费调试 |
| **🚀 任务开发** | flink-sql | ✅ 已完成 | SQL 任务创建、开发、部署、调试 |
| | flink-validate | ✅ 已完成 | SQL 语法校验、预发布验证 |
| | flink-jar | ✅ 已完成 | JAR 任务创建、部署、调试 |
| | flink-cdc | ✅ 已完成 | CDC YAML 任务创建、模板生成、发布、调试 |
| **⚙️ 任务运维** | flink-sre | ✅ 已完成 | 启动、停止、重启、扩容、缩容、配置修改 |
| | flink-savepoint | ✅ 已完成 | 快照创建、查询、恢复、删除 |
| | flink-batch | ✅ 已完成 | 批处理任务管理、调度、历史记录 |
| **📊 任务监控与诊断** | flink-monitor | ✅ 已完成 | 实时监控、指标查询、事件、日志 |
| | flink-diagnostic | ✅ 已完成 | 故障诊断、异常分析、根因定位 |
| | flink-performance | ✅ 已完成 | 性能优化、反压检测、Checkpoint 优化 |

---

## 📈 技能覆盖统计

| 分类维度 | 已完成 | 待创建 | 总计 | 覆盖率 |
|---------|-------|-------|------|--------|
| **🔧 volc_flink 工具管理** | 1 | 0 | 1 | 100% |
| **🏗️ 项目与配置管理** | 3 | 0 | 3 | 100% |
| **💾 资源管理** | 3 | 0 | 3 | 100% |
| **🔌 连接管理** | 1 | 0 | 1 | 100% |
| **🚀 任务开发** | 5 | 0 | 5 | 100% |
| **⚙️ 任务运维** | 3 | 0 | 3 | 100% |
| **📊 任务监控与诊断** | 3 | 0 | 3 | 100% |
| **总计** | **18** | **0** | **18** | **100%** | ✅

---

## 🎯 快速开始

### 首次使用流程

1. **使用统一入口技能** - 从 `skills/SKILL.md` 进入，直接提问即可
2. **智能路由** - 系统会自动判断你的问题类型并路由到合适的子技能
3. **问题解决** - 对应的子技能会处理你的具体问题

### 示例对话

**用户**：帮我安装一下 volc_flink 工具
**系统** → 路由到 `flink-volc` → 提供安装指引

**用户**：查看一下我的项目列表
**系统** → 路由到 `flink-projects` → 展示项目列表

**用户**：帮我创建一个 SQL 任务
**系统** → 路由到 `flink-sql` → 协助创建 SQL 任务

**用户**：我的任务报错了，帮我诊断一下
**系统** → 路由到 `flink-diagnostic` → 进行故障诊断

---

## 🔀 智能路由规则

### 🔧 工具管理类
**触发关键词**：
- 安装、更新、升级、login、logout、登录、登出、配置、volc_flink

**路由到**：`flink-volc`

---

### 🏗️ 项目与配置管理类
**触发关键词**：
- 项目、列举项目、查看项目、项目详情、设置默认项目、配置管理、TOS 路径

**路由到**：
- 项目相关 → `flink-projects`
- 配置相关 → `flink-config`

---

### 💾 资源管理类
**触发关键词**：
- catalog、database、table、元数据、资源池、resource pool、依赖、JAR、UDF

**路由到**：
- Catalog 元数据 → `flink-catalog`
- 资源池 → `flink-resource-pool`
- 依赖管理 → `flink-dependency`

---

### 🔌 连接管理类
**触发关键词**：
- 连接、conn、Kafka 连接、endpoint、bootstrap servers、消费消息、抽样数据、调试 Kafka

**路由到**：`flink-conn`

---

### 🚀 任务开发类
**触发关键词**：
- 创建 SQL、开发 SQL、部署 SQL、调试 SQL、SQL 任务、SQL 开发、SQL 部署、校验 SQL、语法检查、validate、CDC 任务、CDC YAML、Pipeline、MySQL CDC、整库同步、分库分表同步

**路由到**：
- SQL 开发部署 → `flink-sql`
- SQL 语法校验 → `flink-validate`
- CDC 任务 / CDC YAML / Pipeline 模板 → `flink-cdc`

---

### ⚙️ 任务运维类
**触发关键词**：
- 启动、停止、重启、扩容、缩容、修改配置、更新参数、SRE、运维、快照、savepoint

**路由到**：
- 运维操作 → `flink-sre`
- 快照管理 → `flink-savepoint`

---

### 📊 任务监控与诊断类
**触发关键词**：
- 故障、错误、异常、诊断、troubleshoot、diagnose、OOM、checkpoint、性能优化、反压、backpressure、监控、monitor、指标、metrics、日志、logs

**路由到**：
- 实时监控 → `flink-monitor`
- 故障诊断 → `flink-diagnostic`
- 性能优化 → `flink-performance`

---

## 🤝 多技能协作

### 示例 1：SQL 任务完整开发流程
1. `flink-volc` - 确认登录状态
2. `flink-projects` - 选择项目
3. `flink-catalog` - 查看库表结构
4. `flink-sql` - 创建和部署 SQL 任务
5. `flink-validate` - 发布前校验
6. `flink-monitor` - 监控任务运行

### 示例 2：故障诊断流程
1. `flink-monitor` - 查看任务状态和日志
2. `flink-diagnostic` - 深入诊断问题
3. `flink-performance` - 如需性能优化
4. `flink-sre` - 如需运维操作

---

## 📝 注意事项

### 技能依赖关系
- 所有技能都依赖 `flink-volc` 进行登录
- 很多技能在操作前需要先选择项目（使用 `flink-projects`）
- 建议先设置默认项目（使用 `flink-config`）提高效率

### 安全提示
- 不要在聊天中直接粘贴 AK/SK
- 妥善保管 AK/SK
- 定期轮换 AK/SK
- 使用最小权限原则

### 使用建议
- 直接使用 `skills/SKILL.md` 作为统一入口
- 系统会自动路由到合适的子技能
- 复杂问题可能需要多个技能协作

---

## 📚 相关资源

- [火山引擎 Flink 版文档](https://www.volcengine.com/docs/6493)
- [Flink 官方文档](https://nightlies.apache.org/flink/)
- 项目总览：仓库根目录 `README.md`
- volc_flink CLI 帮助：`volc_flink --help`
- 各子技能的 SKILL.md 文件

---

## ✅ 所有技能已完成！

### 🎉 完整技能列表（19/19，100% 覆盖率）

### 🔧 volc_flink 工具管理（1/1）
- ✅ **flink-volc** - 安装、更新、登录、配置工具

### 🏗️ 项目与配置管理（3/3）
- ✅ **flink-auth** - 登录/登出、多账号管理、AK/SK 安全管理
- ✅ **flink-config** - 配置管理、默认项目设置、TOS 路径配置
- ✅ **flink-projects** - 项目列举、项目详情、项目切换

### 💾 资源管理（3/3）
- ✅ **flink-resource-pool** - 资源池列举、详情、创建
- ✅ **flink-catalog** - Catalog、Database、Table 元数据管理
- ✅ **flink-dependency** - JAR 包依赖管理、UDF 库管理

### 🔌 连接管理（1/1）
- ✅ **flink-conn** - Kafka 等上下游连接管理，支持接入点配置与消息消费调试

### 🚀 任务开发（4/4）
- ✅ **flink-sql** - SQL 任务创建、开发、部署、调试
- ✅ **flink-validate** - SQL 语法校验、预发布验证
- ✅ **flink-jar** - JAR 任务创建、部署、调试
- ✅ **flink-cdc** - CDC YAML 任务创建、模板生成、发布、调试

### ⚙️ 任务运维（3/3）
- ✅ **flink-sre** - 启动、停止、重启、扩容、缩容、配置修改
- ✅ **flink-savepoint** - 快照创建、查询、恢复、删除
- ✅ **flink-batch** - 批处理任务管理、调度、历史记录

### 📊 任务监控与诊断（3/3）
- ✅ **flink-monitor** - 实时监控、指标查询、事件、日志
- ✅ **flink-diagnostic** - 故障诊断、异常分析、根因定位
- ✅ **flink-performance** - 性能优化、反压检测、Checkpoint 优化

---

*定位：volc-flink-cli + skills 一体化（AI Flink 技能项目）*
