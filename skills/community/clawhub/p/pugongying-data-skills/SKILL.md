---
name: pugongying-data-skills
description: |
  蒲公英数据开发工程师Skill套件 - 专为数据开发工程师设计的完整AI Skill生态系统。
  包含7个核心模块：需求分析、架构设计、数据建模、SQL开发、ETL Pipeline、数据质量、数据测试。
  当用户需要端到端数据开发解决方案、数据仓库建设、ETL开发、SQL优化、数据质量管理时触发。
  触发词：数据开发、数据仓库、ETL、SQL优化、数据质量、数据建模、需求分析、架构设计。
---

# 🌼 蒲公英数据开发工程师Skill套件

专为数据开发工程师设计的完整AI Skill生态系统，包含7个核心模块，支持端到端数据开发工作流。

## 🎯 核心价值

- **端到端覆盖**：从需求分析到数据测试的完整数据开发生命周期
- **模块化设计**：7个独立模块，可按需组合使用
- **智能联动**：模块间自动数据流转，减少重复工作
- **企业级标准**：遵循数据工程最佳实践和行业标准

## 📦 模块概览

| 模块 | 入口命令 | 核心功能 | 适用场景 |
|------|----------|----------|----------|
| **需求分析助手** | `/requirement-analyst` | 业务需求分析、功能规格定义 | 项目启动、需求澄清 |
| **架构设计助手** | `/architecture-designer` | 数据架构设计、技术选型 | 系统设计、架构评审 |
| **数据建模助手** | `/modeling-assistant` | 维度建模、dbt开发、血缘分析 | 数仓建设、模型设计 |
| **SQL智能开发助手** | `/sql-assistant` | SQL生成、审查、执行计划分析 | 查询开发、性能优化 |
| **ETL Pipeline开发助手** | `/etl-assistant` | ETL代码生成、审查、测试 | 数据管道开发 |
| **数据质量检查助手** | `/dq-assistant` | 质量规则生成、检查、文档 | 数据质量管理 |
| **测试工程师** | `/test-engineer` | 单元测试、集成测试、性能测试 | 数据测试保障 |

## 🚀 快速开始

### 方式1：端到端工作流（推荐）

```bash
# 完整数仓建设工作流
/skill-hub 端到端建设电商数仓

# 快速Pipeline开发
/sql-assistant → /etl-assistant 生成订单数据同步Pipeline

# 质量到测试
/dq-assistant → /test-engineer 基于质量规则生成测试用例
```

### 方式2：独立模块使用

```bash
# 需求分析
/requirement-analyst 分析电商用户行为分析需求

# SQL开发
/sql-assistant 生成用户活跃度分析SQL

# ETL开发
/etl-assistant 创建用户行为数据ETL Pipeline
```

---

## 📋 示例快速索引

| 需求场景 | 推荐工作流 | 命令示例 |
|----------|-----------|----------|
| 从零建设数仓 | 端到端工作流 | `/skill-hub 端到端建设电商数仓` |
| 需求澄清 | 需求分析 | `/requirement-analyst 分析需求` |
| 架构选型 | 需求到架构 | `/requirement-analyst → /architecture-designer` |
| 数据建模 | 架构到建模 | `/architecture-designer → /modeling-assistant` |
| 生成SQL | 建模到SQL | `/modeling-assistant → /sql-assistant` |
| 开发Pipeline | SQL到ETL | `/sql-assistant → /etl-assistant` |
| 质量监控 | ETL到质量 | `/etl-assistant → /dq-assistant` |
| 生成测试 | 质量到测试 | `/dq-assistant → /test-engineer` |
| 部署上线 | 测试驱动部署 | `/test-engineer 验证并部署` |
| 快速建模开发 | 建模到开发 | `/modeling-assistant → /sql-assistant → /etl-assistant` |

---

## 🔗 上下游联动说明

### 完整数据流

```
requirement_package.yaml
    ↓（业务需求、实体定义）
architecture_package.yaml
    ↓（分层架构、技术栈）
modeling_package.yaml
    ↓（事实表、维度表）
sql_package.yaml
    ↓（DDL、转换SQL）
etl_package.yaml
    ↓（Pipeline代码）
dq_package.yaml
    ↓（质量规则）
test_package.yaml
    ↓（测试通过）
部署上线
```

### 快捷联动命令

| 联动 | 命令 | 输出 |
|------|------|------|
| 需求→架构 | `/architecture-designer --from-requirement` | architecture_package.yaml |
| 架构→建模 | `/model-design --from-architecture` | modeling_package.yaml |
| 建模→SQL | `/sql-gen --from-model` | sql_package.yaml |
| 建模→ETL | `/etl-template --from-model` | etl_package.yaml |
| SQL→ETL | `/etl-template --from-sql` | etl_package.yaml |
| ETL→质量 | `/dq-rule-gen --from-etl` | dq_package.yaml |
| 质量→测试 | `/unit-test --from-dq` | test_package.yaml |

## 🔗 智能联动系统

本Skill套件包含智能联动中枢，支持模块间自动数据流转：

```
需求分析 → 架构设计 → 数据建模 → SQL开发 → ETL开发 → 质量检查 → 数据测试
```

### 联动配置

查看详细联动关系：
```bash
# 查看Skill依赖关系
cat skill-connections.yaml

# 查看完整工作流定义
cat skill-hub.md
```

## 📁 项目结构

```
pugongying-data-skills/
├── SKILL.md                    # 本文件（主Skill定义）
├── README.md                   # 详细文档
├── skill-connections.yaml      # Skill联动配置
├── skill-hub.md               # 联动中枢文档
├── requirement-analyst/        # 需求分析模块
├── architecture-designer/      # 架构设计模块
├── modeling-assistant/         # 数据建模模块
├── sql-assistant/             # SQL开发模块
├── etl-assistant/             # ETL开发模块
├── dq-assistant/              # 数据质量模块
└── test-engineer/             # 数据测试模块
```

## 🛠️ 技术特色

### 1. 标准化输出格式

每个模块输出标准化的YAML包文件，便于模块间数据交换：

| 包文件 | 生成者 | 主要用途 |
|--------|--------|----------|
| `requirement_package.yaml` | requirement-analyst | 业务需求、数据实体、指标定义 |
| `architecture_package.yaml` | architecture-designer | 架构决策、分层设计、技术栈 |
| `modeling_package.yaml` | modeling-assistant | 事实表、维度表、SCD策略 |
| `sql_package.yaml` | sql-assistant | SQL代码、表结构、优化建议 |
| `etl_package.yaml` | etl-assistant | Pipeline代码、DAG配置、调度策略 |
| `dq_package.yaml` | dq-assistant | 质量规则、检查结果、数据字典 |
| `test_package.yaml` | test-engineer | 测试用例、测试报告、部署决策 |

**标准包格式**：
```yaml
{package_name}:
  version: "1.0"
  metadata:
    generated_by: "skill-name"
    generated_at: "2024-01-15T10:00:00Z"
    upstream_package: "上游包文件名"
  content: { ... }
  downstream_specs:
    - target: "下游skill"
      input_file: "{package_name}.yaml"
```

### 2. 多Agent协作
- **general-purpose Agent**：用于生成、编辑、执行任务
- **Explore Agent**：用于分析、审查、只读操作
- 智能Agent切换，确保安全性和效率

### 3. 企业级最佳实践
- 数据建模：星型/雪花模型、SCD策略
- SQL开发：性能优化、安全审查
- ETL开发：幂等性、容错处理
- 数据质量：完整性、准确性、一致性检查

## 📚 学习资源

### 套件文档

| 文档 | 内容 | 场景 |
|------|------|------|
| `README.md` | 详细功能说明和使用指南 | 了解套件全貌 |
| `skill-connections.yaml` | Skill联动配置 | 查看模块间关系 |
| `skill-hub.md` | 联动中枢文档 | 了解工作流定义 |
| `skill-template.md` | Skill开发模板 | 开发新Skill |
| `Skill驱动数据系统开发探讨.md` | 设计理念和技术探讨 | 深入理解设计思想 |

### 各模块文档

| 模块 | 参考文档 | 示例 |
|------|----------|------|
| requirement-analyst | `references/requirement-standards.md` | `examples/` |
| architecture-designer | `references/architecture-standards.md` | `examples/` |
| modeling-assistant | `references/data-modeling-standards.md` | `examples/` |
| sql-assistant | `references/sql-standards.md` | `examples/` |
| etl-assistant | `references/etl-standards.md` | `examples/` |
| dq-assistant | `references/data-quality-standards.md` | `examples/` |
| test-engineer | `references/test-standards.md` | `examples/` |

## 🔄 版本管理

### 版本号规则
- **v1.0.0**：基础功能发布
- **v1.1.0**：功能增强和优化
- **v2.0.0**：重大架构升级

### 更新日志
查看各模块内的`CHANGELOG.md`文件获取详细更新记录。

## 🆘 故障排除

### 常见问题

1. **Skill未触发**
   - 确认skill文件在正确的skills目录
   - 检查Frontmatter格式是否正确
   - 重启Claude Code

2. **模块联动失败**
   - 检查`skill-connections.yaml`配置
   - 确认输出包文件格式正确
   - 查看模块日志输出

3. **性能问题**
   - 复杂任务建议分步骤执行
   - 使用多Agent并行处理
   - 优化输入描述，提供更明确的上下文

### 技术支持
- 查看各模块的故障排除章节
- 参考示例项目学习正确用法
- 在ClawHub社区寻求帮助

## 🌟 未来规划

### 近期计划
- 增加更多数据库方言支持
- 优化联动性能
- 增加可视化输出

### 长期愿景
- 集成更多数据工具（dbt、Airflow、Great Expectations等）
- 支持更多数据架构模式（Data Vault、Lakehouse等）
- 建立数据开发社区和最佳实践库

---

**蒲公英数据开发工程师Skill套件** - 让数据开发更智能、更高效、更可靠。

🌼 *像蒲公英种子一样，将数据开发的最佳实践传播到每一个项目*