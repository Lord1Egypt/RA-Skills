# 数据开发需求分析规范

本规范定义数据开发需求分析的标准流程、输出格式和质量标准。

---

## 1. 需求分类体系

### 1.1 按业务域分类

| 业务域 | 典型实体 | 典型指标 |
|--------|---------|---------|
| 电商 | 订单、用户、商品、店铺 | GMV、订单量、客单价、转化率 |
| 金融 | 账户、交易、产品、客户 | 余额、交易量、风险评级 |
| 内容 | 用户、内容、互动、推荐 | DAU、留存率、互动率 |
| 供应链 | 库存、采购、物流、供应商 | 库存周转、履约时效 |
| 营销 | 活动、渠道、线索、转化 | ROI、CAC、LTV |

### 1.2 按需求类型分类

```yaml
demand_types:
  new_development:  # 全新开发
    description: "从零开始建设数据系统"
    outputs: ["完整模型", "ETL Pipeline", "质量规则"]

  enhancement:  # 功能增强
    description: "在现有系统上增加功能"
    outputs: ["变更模型", "增量ETL", "新增规则"]

  optimization:  # 性能优化
    description: "优化现有系统性能"
    outputs: ["优化方案", "重构ETL", "监控规则"]

  migration:  # 系统迁移
    description: "从旧系统迁移到新系统"
    outputs: ["映射规则", "迁移ETL", "校验规则"]
```

### 1.3 按实时性分类

| 类型 | 延迟要求 | 技术方案 | 适用场景 |
|------|---------|---------|---------|
| 批量 (Batch) | T+1 ~ T+N | Airflow + SQL | 日报、月报 |
| 准实时 (Near Real-time) | 分钟级 | Kafka + Flink | 监控告警 |
| 实时 (Real-time) | 秒级/毫秒级 | Flink + Kafka | 风控、推荐 |

---

## 2. 需求解析标准

### 2.1 实体识别规范

每个业务实体应包含：

```yaml
entity:
  name: "实体名称"  # 英文，下划线命名
  display_name: "显示名称"  # 中文
  type: "业务实体"  # 业务实体/维度/事实

  attributes:
    - name: "属性名"
      type: "数据类型"
      description: "业务含义"
      is_key: false  # 是否关键属性
      is_sensitive: false  # 是否敏感

  relationships:
    - target: "关联实体"
      type: "关联类型"  # 1:1 / 1:N / N:M
      business_rule: "关联业务规则"
```

### 2.2 指标定义规范

```yaml
metric:
  name: "指标英文名"
  display_name: "指标中文名"
  alias: ["别名1", "别名2"]

  definition:
    formula: "计算公式"
    unit: "单位"
    precision: 2  # 小数位

  dimensions: ["维度1", "维度2"]  # 可分析维度
  time_grains: ["day", "week", "month"]  # 支持时间粒度

  business_rules:
    - "业务规则1"
    - "业务规则2"

  data_sources:
    - table: "来源表"
      column: "来源字段"
      transformation: "转换逻辑"

  quality_rules:
    - type: "range"
      min: 0
      severity: "error"
```

### 2.3 维度定义规范

```yaml
dimension:
  name: "维度名"
  type: "标准维度"  # 标准维度/退化维度/微型维度

  attributes:
    - name: "属性名"
      type: "类型"  # 描述属性/层次属性/计算属性
      is_mandatory: true  # 是否必填

  hierarchies:  # 层次结构
    - name: "地域层次"
      levels: ["国家", "省", "市", "区"]

  scd_policy:
    type: 2  # 0/1/2/3
    track_attributes: []  # 需要追踪历史变化的属性
```

---

## 3. 需求澄清检查清单

### 3.1 范围边界检查

```markdown
## 范围边界检查清单

### 数据范围
- [ ] 历史数据需要回溯多久？
- [ ] 是否包含测试/沙箱数据？
- [ ] 是否包含已删除/归档数据？
- [ ] 跨系统数据如何关联？

### 功能范围
- [ ] 核心功能是什么？（必须）
- [ ] 增强功能有哪些？（应该）
- [ ] 未来扩展有哪些？（可以）
- [ ] 明确不在范围内的是什么？（不会）

### 用户范围
- [ ] 主要用户群体是谁？
- [ ] 用户数量预估？
- [ ] 用户权限如何划分？
- [ ] 是否有外部用户？
```

### 3.2 数据质量检查

```markdown
## 数据质量检查清单

### 完整性
- [ ] 空值如何处理？
- [ ] 缺失数据如何补全？
- [ ] 数据延迟可接受多久？

### 准确性
- [ ] 数据精确度要求？（精确到元/分/厘）
- [ ] 允许的计算误差范围？
- [ ] 异常值如何识别和处理？

### 一致性
- [ ] 跨系统数据一致性如何保证？
- [ ] 编码规范是否统一？
- [ ] 命名规范是否统一？

### 时效性
- [ ] 数据更新频率？
- [ ] 数据可见延迟要求？
- [ ] 历史数据变更如何同步？
```

### 3.3 安全合规检查

```markdown
## 安全合规检查清单

### 敏感数据
- [ ] 是否涉及PII（个人身份信息）？
- [ ] 是否涉及财务敏感数据？
- [ ] 是否涉及商业机密？

### 数据脱敏
- [ ] 哪些字段需要脱敏？
- [ ] 脱敏规则是什么？（掩码/加密/哈希）
- [ ] 谁可以查看原始数据？

### 访问控制
- [ ] 用户角色如何划分？
- [ ] 行级权限如何控制？
- [ ] 列级权限如何控制？

### 审计要求
- [ ] 是否需要访问日志？
- [ ] 日志保留多久？
- [ ] 是否需要定期审计报告？
```

---

## 4. 输出规范

### 4.1 标准化需求包格式

```yaml
# requirement_package.yaml
requirement_package:
  version: "1.0.0"
  schema: "https://claude-code.skill/requirement/v1"

  metadata:
    package_id: "REQ-2024-001"
    project_name: "项目名称"
    analyst: "requirement-analyst"
    generated_at: "2024-01-15T10:00:00Z"
    confirmed: true
    confidence_score: 0.85  # 置信度评分

  business:
    domain: "业务域"
    subdomain: "子域"
    owner: "业务负责人"
    goal: "业务目标"
    success_criteria: []
    kpis: []

  functional:
    entities: []
    processes: []
    metrics: []
    dimensions: []
    reports: []

  non_functional:
    performance:
      query_response_time: ""
      data_freshness: ""
      concurrent_users: 0
    reliability:
      availability: "99.9%"
      rto: "1小时"
      rpo: "24小时"
    security:
      compliance: []
      encryption: []
      access_control: {}
    maintainability:
      documentation: "完整"
      test_coverage: "80%"

  technical:
    preferred_stack: []
    existing_systems: []
    constraints: []
    assumptions: []

  specifications:
    model_spec:
      file: "specs/model_spec.yaml"
      version: "1.0"
    etl_spec:
      file: "specs/etl_spec.yaml"
      version: "1.0"
    dq_spec:
      file: "specs/dq_spec.yaml"
      version: "1.0"

  downstream_tasks:
    - skill: "model-design"
      input: "specifications.model_spec"
      priority: "high"
    - skill: "sql-gen"
      input: "specifications.etl_spec"
      priority: "high"
    - skill: "etl-template"
      input: "specifications.etl_spec"
      priority: "high"
    - skill: "dq-rule-gen"
      input: "specifications.dq_spec"
      priority: "medium"
```

### 4.2 文档质量标准

| 检查项 | 标准 | 检查方式 |
|--------|------|---------|
| 完整性 | 所有必填字段都有值 | 自动校验 |
| 一致性 | 术语使用一致 | 自动校验 |
| 可追溯 | 需求有唯一ID | 自动校验 |
| 可测试 | 需求可验证 | 人工审查 |
| 无歧义 | 表述清晰明确 | 人工审查 |

---

## 5. 术语表

| 术语 | 英文 | 定义 |
|------|------|------|
| 业务域 | Business Domain | 业务的垂直领域划分 |
| 业务实体 | Business Entity | 业务中有意义的对象 |
| 业务过程 | Business Process | 产生数据的业务活动 |
| 指标 | Metric | 可量化的业务度量 |
| 维度 | Dimension | 分析视角 |
| 粒度 | Grain | 事实表的最小细节级别 |
| SCD | Slowly Changing Dimension | 缓慢变化维 |
| ETL | Extract-Transform-Load | 数据抽取转换加载 |
| CDC | Change Data Capture | 变更数据捕获 |
| PII | Personally Identifiable Information | 个人身份信息 |

---

## 6. 最佳实践

### 6.1 需求分析流程

```
1. 收集原始需求
   ├── 业务方访谈
   ├── 文档收集
   └── 系统调研

2. 结构化解析
   ├── 实体识别
   ├── 指标提取
   └── 数据源映射

3. 缺口识别
   ├── 歧义检测
   ├── 缺失识别
   └── 风险评估

4. 需求澄清
   ├── 问题准备
   ├── 业务确认
   └── 决策记录

5. 规格转化
   ├── 模型设计
   ├── ETL设计
   └── 质量设计

6. 评审确认
   ├── 技术评审
   ├── 业务确认
   └── 基线建立
```

### 6.2 常见问题及应对

| 问题类型 | 典型表现 | 应对策略 |
|---------|---------|---------|
| 需求蔓延 | 范围不断扩大 | 严格变更控制，影响分析 |
| 表述模糊 | "大概"、"可能" | 要求具体化，举例说明 |
| 目标冲突 | 多方需求矛盾 | 优先级排序，协商平衡 |
| 技术约束 | 现有系统限制 | 提前识别，方案评估 |
| 数据缺失 | 关键数据没有 | 替代方案，补全策略 |

---

**版本**: v1.0
**更新日期**: 2024-01-15
**维护者**: requirement-analyst Skill
