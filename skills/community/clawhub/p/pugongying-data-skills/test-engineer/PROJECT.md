# test-engineer Skill 项目

> Skill名称: 数据仓库测试工程师
> 创建时间: 2024-03-17
> 版本: v1.0.0
> 维护者: 数据平台团队

---

## 项目概述

- **Skill名称**: test-engineer (数据仓库测试工程师)
- **项目目标**: 提供端到端数据仓库测试工作流，包含单元测试、集成测试、性能测试
- **技术栈**: pytest, pandas, Snowflake
- **项目状态**: ✅ 已发布 v1.0.0

---

## 功能清单

| 功能ID | 功能名称 | 命令 | 状态 | 关联文档 |
|--------|----------|------|------|----------|
| TST-001 | 单元测试生成 | /unit-test | ✅ 已实现 | examples/example-unit-test.md |
| TST-002 | 集成测试生成 | /integration-test | ✅ 已实现 | examples/example-integration-test.md |
| TST-003 | 性能测试生成 | /performance-test | ✅ 已实现 | examples/example-performance-test.md |
| TST-004 | 端到端测试工作流 | /test-engineer | ✅ 已实现 | SKILL.md |

---

## 项目结构

```
test-engineer/
├── SKILL.md                          # Skill主文档（入口）
├── PROJECT.md                        # 项目中枢（本文件）
├── references/
│   └── test-standards.md             # 测试规范
├── examples/
│   ├── example-unit-test.md          # 单元测试示例
│   ├── example-integration-test.md   # 集成测试示例
│   └── example-performance-test.md   # 性能测试示例
└── scripts/
    └── init-project.sh               # 项目初始化脚本
```

---

## 进度追踪

- [x] v0.1.0: 项目初始化
  - [x] 创建目录结构
  - [x] 编写SKILL.md主文档
- [x] v0.2.0: 测试规范
  - [x] 编写test-standards.md
  - [x] 定义命名规范和断言规范
- [x] v0.3.0: 示例文档
  - [x] 单元测试示例
  - [x] 集成测试示例
  - [x] 性能测试示例
- [x] v0.4.0: 初始化脚本
  - [x] init-project.sh
- [x] v1.0.0: 发布
  - [x] 添加Skill联动配置
  - [x] 与dq-assistant、etl-assistant、sql-assistant联动

---

## 文档索引

### 参考资料
- [测试规范](references/test-standards.md) - 测试金字塔、命名规范、断言库、覆盖率标准

### 使用示例
- [单元测试示例](examples/example-unit-test.md) - fct_order_items表单元测试
- [集成测试示例](examples/example-integration-test.md) - DWD到DWS对账测试
- [性能测试示例](examples/example-performance-test.md) - 销售日报查询性能测试

### 脚本
- [项目初始化](scripts/init-project.sh) - 创建标准化测试项目结构

---

## 快速开始

### 初始化测试项目

```bash
bash .claude/skills/test-engineer/scripts/init-project.sh ./test-project "电商数仓测试"
```

### 生成单元测试

```bash
/unit-test 表: fct_order_items
测试内容:
- 代理键唯一性
- 维度外键有效性
- 金额计算正确性
```

### 生成集成测试

```bash
/integration-test 场景: DWD到DWS汇总对账
验证:
- 日期: 2024-01-15
- 维度: 省份+用户等级
- 容忍度: 金额0.1%
```

### 生成性能测试

```bash
/performance-test 目标: 销售日报查询
基准:
- P50 < 2秒, P95 < 5秒
- 并发10用户
```

---

## 下游Skill调用指令

```bash
# 基于质量规则生成测试
/dq-assistant 生成质量规则 → /unit-test 基于规则生成单元测试

# 基于Pipeline生成集成测试
/etl-assistant 生成Pipeline → /integration-test 验证数据流一致性

# 基于SQL生成性能测试
/sql-assistant 生成查询 → /performance-test 验证查询性能
```

---

## 变更记录

| 日期 | 版本 | 变更内容 | 作者 |
|------|------|----------|------|
| 2024-03-17 | v0.1.0 | 项目初始化 | test-engineer |
| 2024-03-17 | v0.2.0 | 测试规范 | test-engineer |
| 2024-03-17 | v0.3.0 | 示例文档 | test-engineer |
| 2024-03-17 | v0.4.0 | 初始化脚本 | test-engineer |
| 2024-03-17 | v1.0.0 | 添加Skill联动 | test-engineer |

---

## 相关Skill

- [requirement-analyst](../requirement-analyst/) - 需求分析
- [architecture-designer](../architecture-designer/) - 架构设计
- [modeling-assistant](../modeling-assistant/) - 数据建模
- [sql-assistant](../sql-assistant/) - SQL开发
- [etl-assistant](../etl-assistant/) - ETL开发
- [dq-assistant](../dq-assistant/) - 数据质量

---

## 路线图

### v1.1.0 (计划)
- [ ] 自动化测试发现
- [ ] 测试覆盖率报告
- [ ] CI/CD集成

### v2.0.0 (计划)
- [ ] 智能测试用例推荐
- [ ] 历史测试趋势分析
- [ ] 自动回归测试选择

---

## 参考资料

- 《AI编程与数据开发工程师融合实战手册》§07 AI辅助测试验证实战
