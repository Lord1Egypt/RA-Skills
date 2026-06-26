# 火山引擎 Flink 版 (volc_flink) 技能插件

完整的火山引擎 Flink 版管理技能插件，涵盖工具安装、项目管理、资源管理、任务开发、任务运维、任务监控等全流程。

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

1. **使用 `flink-volc` 安装和登录**
   - 安装 volc_flink 工具
   - 登录火山引擎账号
   - 验证登录状态

2. **使用 `flink-projects` 查看项目**
   - 列出所有可用项目
   - 查看项目详情和配额

3. **使用 `flink-config` 配置默认项目**
   - 设置默认项目
   - 配置 TOS Jar 路径（可选）

4. **开始使用其他技能**
   - 资源管理：`flink-catalog`、`flink-resource-pool`、`flink-dependency`
   - 连接管理：`flink-conn`
   - 任务开发：`flink-sql`、`flink-validate`、`flink-jar`、`flink-cdc`
   - 任务运维：`flink-sre`、`flink-savepoint`
   - 监控诊断：`flink-monitor`、`flink-diagnostic`、`flink-performance`

---

## 📋 技能详情

### 🔧 volc_flink 工具管理

#### flink-volc
**状态**：✅ 已完成
**核心功能**：
- 安装和更新 volc_flink 工具
- 登录和退出火山引擎
- 配置管理（查看配置）
- 快速入门指引
- 多账号管理（高级）

---

### 🏗️ 项目与配置管理

#### flink-config
**状态**：✅ 已完成
**核心功能**：
- 查看当前配置
- 设置默认项目
- 设置 TOS Jar 存储路径
- 配置验证

#### flink-projects
**状态**：✅ 已完成
**核心功能**：
- 列举所有项目
- 查看项目详情
- 查看配额和使用情况
- 智能项目选择

#### flink-auth
**状态**：✅ 已完成
**核心功能**：
- 登录/登出管理
- 多账号切换
- 登录状态检测
- AK/SK 安全管理

---

### 💾 资源管理

#### flink-resource-pool
**状态**：✅ 已完成
**核心功能**：
- 列举资源池
- 查看资源池详情
- 创建资源池

#### flink-catalog
**状态**：✅ 已完成
**核心功能**：
- Catalog 管理
- Database 管理
- Table 管理
- 树形结构浏览

#### flink-dependency
**状态**：✅ 已完成

---

### 🔌 连接管理

#### flink-conn
**状态**：✅ 已完成
**核心功能**：
- Kafka 等上下游连接配置
- Endpoint（接入点）管理
- 消息消费/抽样调试（便于 SQL/JAR 开发前做数据确认）
**核心功能**：
- JAR 包依赖管理
- UDF 库管理
- 依赖列表查看

---

### 🚀 任务开发

#### flink-sql
**状态**：✅ 已完成
**核心功能**：
- SQL 任务创建
- SQL 代码生成
- 草稿管理
- 任务发布和调试

#### flink-validate
**状态**：✅ 已完成
**核心功能**：
- SQL 语法校验
- 预发布验证
- 错误定位和提示
- 修复建议

#### flink-jar
**状态**：✅ 已完成
**核心功能**：
- JAR 任务创建
- JAR 包上传
- JAR 任务配置
- JAR 任务调试

#### flink-cdc
**状态**：✅ 已完成
**核心功能**：
- CDC YAML 模板生成
- CDC 草稿创建
- CDC 任务发布与调试
- MySQL 到 Paimon/StarRocks/Doris/Kafka/ByteHouse CDW 同步模板

### ⚙️ 任务运维

#### flink-sre
**状态**：✅ 已完成
**核心功能**：
- 启动/停止/重启任务
- 扩容/缩容任务
- 配置修改
- 参数验证
- 状态监控

#### flink-savepoint
**状态**：✅ 已完成
**核心功能**：
- 快照创建
- 快照查询
- 快照恢复
- 快照删除

#### flink-batch
**状态**：✅ 已完成
**核心功能**：
- 批处理任务管理
- 批处理任务调度
- 批处理历史记录
- 批量任务依赖管理

---

### 📊 任务监控与诊断

#### flink-diagnostic
**状态**：✅ 已完成
**核心功能**：
- 故障诊断
- 异常分析
- 根因定位
- 修复建议

#### flink-performance
**状态**：✅ 已完成
**核心功能**：
- 性能优化
- 反压检测
- Checkpoint 优化
- 状态优化
- 并行度调优

#### flink-monitor
**状态**：✅ 已完成
**核心功能**：
- 实时任务监控
- 指标查询
- 事件查询
- 日志查询
- Flink UI 访问
- 综合监控面板

---

## ✅ 状态说明

本插件当前为完整版，所有技能均已完成（18/18，100% 覆盖率）。

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
- 首次使用：按照"快速开始"流程操作
- 开发 SQL：`flink-catalog` → `flink-sql` → `flink-validate` → 发布
- 任务运维：`flink-monitor` → `flink-sre`（如需）
- 故障处理：`flink-monitor` → `flink-diagnostic` → `flink-performance`（如需）

---

## 📚 相关资源

- [火山引擎 Flink 版文档](https://www.volcengine.com/docs/6493)
- [Flink 官方文档](https://nightlies.apache.org/flink/)
- volc_flink CLI 帮助：`volc_flink --help`

---

*插件版本：3.0（完整版）*
*最后更新：2026-03-30*
