---
name: volc-flink-skill
description: 火山引擎 Flink 版统一管理技能，智能路由到合适的子技能处理 Flink 相关问题。包括工具管理、项目配置、资源管理、连接管理、任务开发、任务运维、监控诊断等全流程功能。Use this skill as the entrypoint when the user expresses a concrete Flink intent on a concrete object, such as installing `volc_flink`, listing projects, inspecting catalog tables, configuring Kafka endpoints, creating SQL/JAR jobs, stopping/restarting jobs, checking logs/metrics, or diagnosing checkpoint/OOM failures. Always trigger when the request includes an action + target object in the Flink domain, rather than only generic words like "Flink" or "任务".
required_binaries:
  - volc_flink
may_access_config_paths:
  - ~/.volc_flink
  - $VOLC_FLINK_CONFIG_DIR
credentials:
  primary: volc_flink_local_config
  optional_env_vars:
    - VOLCENGINE_ACCESS_KEY
    - VOLCENGINE_SECRET_KEY
    - VOLCENGINE_REGION
---

# 火山引擎 Flink 版统一管理技能

这是 Flink 相关问题的统一入口，根据用户的问题智能路由到合适的子技能进行处理。

---

## 🎯 智能路由规则

根据用户的问题内容，自动选择最合适的子技能：

### 🔧 工具管理类
**触发关键词**：
- 安装、更新、升级、login、logout、登录、登出、volc_flink
- "安装 volc_flink"、"更新 volc_flink"、"登录火山引擎"、"配置 volc_flink CLI"

**路由到**：`flink-volc`

---

### 🏗️ 项目与配置管理类
**触发关键词**：
- 项目、列举项目、查看项目、项目详情、设置默认项目、配置管理、TOS 路径、切换账号、多账号、AK/SK、安全、认证
- "查看项目"、"列举项目"、"设置默认项目"、"配置 TOS 路径"、"切换账号"、"多账号管理"

**路由到**：
- 认证/账号相关 → `flink-auth`
- 项目相关 → `flink-projects`
- 配置相关 → `flink-config`

---

### 💾 资源管理类
**触发关键词**：
- catalog、database、table、元数据、资源池、resource pool、依赖、JAR、UDF
- "查看 catalog"、"列举 table"、"查看资源池"、"管理依赖"、"添加 JAR"

**路由到**：
- Catalog 元数据 → `flink-catalog`
- 资源池 → `flink-resource-pool`
- 依赖管理 → `flink-dependency`

---

### 🔌 连接管理类
**触发关键词**：
- 连接、conn、Kafka 连接、endpoint、bootstrap servers、消费消息、抽样数据、调试 Kafka
- "配置 Kafka endpoint"、"抽样 Kafka 消息"、"消费 10 条消息"

**路由到**：`flink-conn`

---

### 🚀 任务开发类
**触发关键词**：
- 创建 SQL、开发 SQL、部署 SQL、调试 SQL、SQL 任务、SQL 开发、SQL 部署、校验 SQL、语法检查、validate、JAR 任务、CDC 任务、CDC YAML、Pipeline、MySQL CDC、整库同步、分库分表同步、模板、template、最佳实践、常用场景、代码片段、快速创建
- "创建 SQL 任务"、"开发 SQL"、"部署任务"、"校验 SQL"、"语法检查"、"JAR 任务"、"创建 CDC 任务"、"生成 CDC YAML"、"MySQL 到 Paimon"、"MySQL 到 StarRocks"、"模板"、"最佳实践"

**路由到**：
- SQL 开发部署 → `flink-sql`
- SQL 语法校验 → `flink-validate`
- JAR 任务 → `flink-jar`
- CDC 任务 / CDC YAML / Pipeline 模板 → `flink-cdc`
- 模板/最佳实践（只读：输出 `flink-sql/assets/` + `flink-sql/references/`，不做创建/发布）→ `flink-sql`

---

### ⚙️ 任务运维类
**触发关键词**：
- 启动、停止、重启、扩容、缩容、修改配置、更新参数、SRE、运维、快照、savepoint、批处理、batch
- "启动任务"、"停止任务"、"重启任务"、"扩容"、"缩容"、"创建快照"、"恢复快照"、"批处理任务"

**路由到**：
- 运维操作 → `flink-sre`
- 快照管理 → `flink-savepoint`
- 批处理任务 → `flink-batch`

---

### 📊 任务监控与诊断类
**触发关键词**：
- 故障、错误、异常、诊断、troubleshoot、diagnose、OOM、checkpoint、性能优化、反压、backpressure、监控、monitor、指标、metrics、日志、logs
- "任务报错了"、"诊断一下"、"性能优化"、"查看监控"、"查看日志"、"查看指标"

**路由到**：
- 实时监控 → `flink-monitor`
- 故障诊断 → `flink-diagnostic`
- 性能优化 → `flink-performance`

---

## ⚠️ 路由冲突表

| 冲突场景 | 优先路由到 | 判断规则 |
|---------|-----------|---------|
| 登录/安装/升级 CLI vs 默认项目/TOS 路径配置 | `flink-volc` / `flink-config` | 如果动作是安装、升级、登录、退出、查看 CLI 版本，走 `flink-volc`；如果动作是设置默认项目、查看配置、设置 TOS 路径，走 `flink-config` |
| 查看日志/指标/事件 vs 深入排障 | `flink-monitor` / `flink-diagnostic` | 如果动作是查看、监控、查询日志/事件/指标，走 `flink-monitor`；如果动作是分析错误原因、定位根因、排查失败/OOM/checkpoint timeout，走 `flink-diagnostic` |
| 性能优化 vs 故障诊断 | `flink-performance` / `flink-diagnostic` | 如果动作是调优并行度、内存、checkpoint、反压，走 `flink-performance`；如果动作是解释失败原因或故障归因，走 `flink-diagnostic` |
| 生成模板/示例 SQL vs 创建/更新真实任务 | `flink-sql` | 两类都走 `flink-sql`：如果只是要模板/示例/最佳实践，则只读输出 `flink-sql/assets/` + `flink-sql/references/`；如果是创建/修改/发布/调试真实任务，则按 `COMMON_MUTATION.md` 执行变更流程 |
| SQL 校验 vs SQL 开发部署 | `flink-validate` / `flink-sql` | 如果动作是校验语法、预发布检查，走 `flink-validate`；如果动作是创建、更新、发布、启动任务，走 `flink-sql` |
| CDC YAML / CDC 草稿任务 vs SQL/JAR 任务 | `flink-cdc` / `flink-sql` / `flink-jar` | 如果用户目标是 CDC pipeline YAML、`--type cdc`、MySQL->Paimon/StarRocks/Doris/Kafka/ByteHouse CDW 同步，走 `flink-cdc`；SQL/JAR 仍分别走 `flink-sql` / `flink-jar` |
| Kafka 连接配置/消费调试 vs Kafka SQL 模板 | `flink-conn` / `flink-sql` | 如果动作是配置 Instance/Endpoint、消费消息、抽样数据，走 `flink-conn`；如果动作是生成 Kafka Source/Sink SQL 模板，走 `flink-sql`（只读模板输出） |
| 任务启停/扩缩容/改参数 vs 快照恢复/删除 | `flink-sre` / `flink-savepoint` | 如果动作是 stop/restart/rescale/update params，走 `flink-sre`；如果动作是创建、查询、恢复、删除快照，走 `flink-savepoint` |

---

## 🔀 路由决策流程

### 步骤 1：问题分类
根据用户的问题，先判断属于哪个大类：
1. 🔧 工具管理
2. 🏗️ 项目与配置管理
3. 💾 资源管理
4. 🔌 连接管理
5. 🚀 任务开发
6. ⚙️ 任务运维
7. 📊 任务监控与诊断

### 步骤 2：子技能选择
在确定的大类中，根据具体关键词选择最合适的子技能。

### 步骤 3：执行路由
调用对应的子技能处理用户的问题。

---

## 🤝 多技能协作

有些问题可能需要多个技能协作：

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

## 📋 技能清单

### 🔧 volc_flink 工具管理（1/1）✅
- ✅ **flink-volc** - 安装、更新、登录、配置工具

### 🏗️ 项目与配置管理（3/3）✅
- ✅ **flink-auth** - 登录/登出、多账号管理、AK/SK 安全管理
- ✅ **flink-config** - 配置管理、默认项目设置、TOS 路径配置
- ✅ **flink-projects** - 项目列举、项目详情、项目切换

### 💾 资源管理（3/3）✅
- ✅ **flink-resource-pool** - 资源池列举、详情、创建
- ✅ **flink-catalog** - Catalog、Database、Table 元数据管理
- ✅ **flink-dependency** - JAR 包依赖管理、UDF 库管理

### 🔌 连接管理（1/1）✅
- ✅ **flink-conn** - Kafka 等上下游连接管理，支持接入点配置与消息消费调试

### 🚀 任务开发（4/4）✅
- ✅ **flink-sql** - SQL 任务创建、开发、部署、调试
- ✅ **flink-validate** - SQL 语法校验、预发布验证
- ✅ **flink-jar** - JAR 任务创建、部署、调试
- ✅ **flink-cdc** - CDC YAML 任务创建、模板生成、发布、调试

### ⚙️ 任务运维（3/3）✅
- ✅ **flink-sre** - 启动、停止、重启、扩容、缩容、配置修改
- ✅ **flink-savepoint** - 快照创建、查询、恢复、删除
- ✅ **flink-batch** - 批处理任务管理、调度、历史记录

### 📊 任务监控与诊断（3/3）✅
- ✅ **flink-monitor** - 实时监控、指标查询、事件、日志
- ✅ **flink-diagnostic** - 故障诊断、异常分析、根因定位
- ✅ **flink-performance** - 性能优化、反压检测、Checkpoint 优化

---

## 💡 使用建议

### 首次使用
如果用户是第一次使用 Flink 相关功能：
1. 先检查是否需要安装和登录（`flink-volc`）
2. 查看可用项目（`flink-projects`）
3. 根据具体需求路由到对应技能

### 问题不明确
如果用户的问题比较模糊，无法明确分类：
1. 询问用户更具体的需求
2. 或者提供一个技能列表供用户选择

### 复杂问题
如果用户的问题涉及多个方面：
1. 分析问题的主要方面
2. 先路由到主要技能
3. 根据需要引导使用其他协作技能

---

## 📚 相关文档

详细的技能说明请参考各子技能的 SKILL.md 文件，以及插件总览文档：
`skills/flink-volc/README.md`

---

*这是 Flink 技能的统一入口，智能路由到合适的子技能处理用户的问题！*
