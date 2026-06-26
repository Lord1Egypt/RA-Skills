# 🌼 蒲公英数据开发工程师Skill套件

专为数据开发工程师设计的完整AI Skill生态系统，包含7个核心模块，支持端到端数据开发工作流。

## 🎯 项目概述

**蒲公英数据开发工程师Skill套件**是一个全面的数据开发解决方案，覆盖从需求分析到数据测试的完整数据开发生命周期。通过7个智能模块的协同工作，帮助数据工程师高效完成数据仓库建设、ETL开发、SQL优化等任务。

## 📦 核心模块

### 1. 需求分析助手 (`/requirement-analyst`)
- **功能**：业务需求分析、功能规格定义、非功能性需求识别
- **输出**：需求规格文档、数据字典、验收标准
- **适用场景**：项目启动、需求澄清、范围定义

### 2. 架构设计助手 (`/architecture-designer`)
- **功能**：数据架构设计、技术选型、系统拓扑规划
- **输出**：架构设计文档、技术栈建议、部署方案
- **适用场景**：系统设计、架构评审、技术选型

### 3. 数据建模助手 (`/modeling-assistant`)
- **功能**：维度建模、dbt模型开发、数据血缘分析
- **输出**：数据模型设计、dbt代码、血缘文档
- **适用场景**：数仓建设、模型设计、Schema管理

### 4. SQL智能开发助手 (`/sql-assistant`)
- **功能**：SQL生成、代码审查、执行计划分析
- **输出**：优化后的SQL代码、审查报告、性能建议
- **适用场景**：查询开发、性能优化、代码Review

### 5. ETL Pipeline开发助手 (`/etl-assistant`)
- **功能**：ETL代码生成、代码审查、数据测试生成
- **输出**：ETL Pipeline代码、测试用例、部署配置
- **适用场景**：数据管道开发、数据集成、批处理作业

### 6. 数据质量检查助手 (`/dq-assistant`)
- **功能**：质量规则生成、数据质量检查、质量文档输出
- **输出**：质量规则集、检查报告、数据字典
- **适用场景**：数据质量管理、数据监控、数据治理

### 7. 测试工程师 (`/test-engineer`)
- **功能**：单元测试、集成测试、性能测试、回归测试
- **输出**：测试用例、测试报告、性能基准
- **适用场景**：数据测试、质量保障、发布验证

## 🚀 快速开始

### 安装方式

```bash
# 方式1：从ClawHub安装
clawhub install pugongying-data-skills

# 方式2：手动安装
# 将本目录复制到 ~/.openclaw/skills/ 或项目 .claude/skills/ 目录
```

### 基本使用

```bash
# 查看所有可用命令
ls -la ~/.openclaw/skills/pugongying-data-skills/

# 使用单个模块
/sql-assistant 生成用户活跃度分析SQL

# 使用联动功能
/skill-hub 端到端建设电商数仓
```

## 🔗 智能联动系统

本Skill套件的核心特色是模块间的智能联动：

### 联动架构

```
需求分析 → 架构设计 → 数据建模 → SQL开发 → ETL开发 → 质量检查 → 数据测试
```

### 标准数据包格式

每个模块输出标准化的YAML数据包，便于模块间数据交换：

```yaml
# requirement_package.yaml 示例
version: "1.0"
metadata:
  project_name: "电商用户行为分析"
  generated_by: "requirement-analyst"
  generated_at: "2026-03-18T10:00:00Z"
content:
  functional:
    entities: ["用户", "订单", "商品"]
    metrics: ["日活用户", "转化率", "客单价"]
  non_functional:
    freshness: "T+1"
    retention: "3年"
```

### 预定义工作流

1. **端到端数仓建设** (`/skill-hub 端到端建设{业务}数仓`)
2. **SQL到ETL快速通道** (`/sql-assistant → /etl-assistant`)
3. **质量到测试** (`/dq-assistant → /test-engineer`)

## 📁 项目结构

```
pugongying-data-skills/
├── SKILL.md                    # 主Skill定义
├── README.md                   # 本文档
├── skill-connections.yaml      # Skill联动配置
├── skill-hub.md               # 联动中枢文档
├── Skill驱动数据系统开发探讨.md  # 设计理念和技术探讨
├── requirement-analyst/        # 需求分析模块
│   ├── SKILL.md
│   ├── references/
│   └── examples/
├── architecture-designer/      # 架构设计模块
│   ├── SKILL.md
│   ├── references/
│   └── examples/
├── modeling-assistant/         # 数据建模模块
│   ├── SKILL.md
│   ├── references/
│   └── examples/
├── sql-assistant/             # SQL开发模块
│   ├── SKILL.md
│   ├── references/
│   └── examples/
├── etl-assistant/             # ETL开发模块
│   ├── SKILL.md
│   ├── references/
│   └── examples/
├── dq-assistant/              # 数据质量模块
│   ├── SKILL.md
│   ├── references/
│   └── examples/
└── test-engineer/             # 数据测试模块
    ├── SKILL.md
    ├── references/
    └── examples/
```

## 🛠️ 技术特色

### 1. 多Agent智能协作
- **general-purpose Agent**：用于生成、编辑、执行任务
- **Explore Agent**：用于分析、审查、只读操作
- 智能Agent切换，确保安全性和效率

### 2. 企业级最佳实践
- 数据建模：星型/雪花模型、SCD策略
- SQL开发：性能优化、安全审查、方言适配
- ETL开发：幂等性、容错处理、监控集成
- 数据质量：完整性、准确性、一致性、及时性检查

### 3. 标准化输出
- 统一的YAML数据包格式
- 完整的文档生成
- 可复用的代码模板

## 📚 学习资源

### 文档目录
- **SKILL.md** - 主Skill定义和使用说明
- **skill-connections.yaml** - 详细联动配置
- **skill-hub.md** - 联动中枢使用指南
- **各模块内的references/** - 规范文档和最佳实践
- **各模块内的examples/** - 典型场景示例

### 配套资源
- 《AI编程与数据开发工程师融合实战手册》配套使用
- ClawHub社区支持和讨论
- 持续更新的最佳实践库

## 🆘 故障排除

### 常见问题

1. **Skill未触发**
   ```bash
   # 检查skill目录位置
   ls ~/.openclaw/skills/ | grep pugongying
   
   # 检查Frontmatter格式
   head -20 ~/.openclaw/skills/pugongying-data-skills/SKILL.md
   ```

2. **模块联动失败**
   ```bash
   # 检查配置文件
   cat ~/.openclaw/skills/pugongying-data-skills/skill-connections.yaml
   
   # 检查输出文件格式
   cat outputs/requirement_package.yaml
   ```

3. **性能问题**
   - 复杂任务分步骤执行
   - 使用多Agent并行处理
   - 提供明确的上下文信息

### 获取帮助
- 查看各模块的故障排除章节
- 参考示例项目学习正确用法
- 在ClawHub社区提问：https://clawhub.com

## 🔄 版本管理

### 当前版本：v1.0.0
- ✅ 7个核心模块完整功能
- ✅ 智能联动系统
- ✅ 标准化数据包格式
- ✅ 企业级最佳实践

### 更新计划
- **v1.1.0**：增加更多数据库方言支持
- **v1.2.0**：优化联动性能和用户体验
- **v2.0.0**：集成更多数据工具和平台

## 🤝 贡献指南

欢迎贡献代码、文档、示例或建议：

1. Fork本仓库
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

### 贡献方向
- 新的数据开发模块
- 更多的数据库方言支持
- 优化现有功能
- 增加示例和文档

## 📄 许可证

本项目采用 MIT 许可证 - 查看 LICENSE 文件了解详情。

## 🌟 致谢

感谢所有贡献者和用户的支持，让蒲公英数据开发工程师Skill套件不断成长和完善。

---

**蒲公英数据开发工程师Skill套件** - 让数据开发更智能、更高效、更可靠。

🌼 *像蒲公英种子一样，将数据开发的最佳实践传播到每一个项目*