---
name: skill-quality-assurance
description: 技能质量六维评估助手。使用结构化六维评估模型（T 技术深度、C 认知增强、O 编排能力、E 进化能力、M 市场验证、U 用户体验）对技能进行自动化评估。使用当：(1) 新技能开发完成后需要质量评估，(2) 现有技能需要版本升级评估，(3) 准备 ClawHub 上架前需要质量检查，(4) 定期技能健康检查。
---

# Skill Quality Assurance - 技能质量评估助手

**版本**: v1.0.0  
**定位**: 基于六维评估模型的技能质量自动化评估工具

---

## 🎯 核心功能

1. **六维自动化评估** - 对技能进行 T/C/O/E/M/U 六维度评分
2. **评估报告生成** - 输出结构化评估报告（Markdown）
3. **改进建议生成** - 基于评估结果生成 P0/P1/P2 优先级改进项
4. **上架准备检查** - ClawHub 上架前质量检查清单

---

## 🚀 使用方法

### 1. 评估单个技能

```
评估 [技能名称] 的质量

示例：
- 评估 meta-cognition-assistant 的质量
- 评估 event-orchestrator 的六维得分
- 对 first-principle-analyzer 进行质量评估
```

### 2. 批量评估

```
批量评估 [技能列表]

示例：
- 批量评估所有元技能的质量
- 评估 Phase 1 的 7 个技能
```

### 3. 生成评估报告

```
生成 [技能名称] 的评估报告

示例：
- 生成 skill-quality-assurance 的评估报告
- 输出 event-orchestrator 的六维评估报告
```

### 4. 上架前检查

```
检查 [技能名称] 是否准备好上架

示例：
- 检查 meta-cognition-assistant 是否准备好 ClawHub 上架
- 检查 first-principle-analyzer 的上架准备情况
```

---

## 📊 六维评估模型

### T 维度（技术深度）

```
T = (T₁ + T₂ + T₃ + T₄) / 4
```

| 子维度 | 权重 | 评估要点 |
|--------|------|----------|
| T₁ 架构设计 | 25% | 分层清晰度、职责分离、模块依赖 |
| T₂ 代码质量 | 25% | 代码规范、注释充分、命名清晰 |
| T₃ 性能表现 | 25% | 响应速度、资源占用、基准测试 |
| T₄ 测试覆盖 | 25% | 单元测试、集成测试、E2E 测试覆盖率 |

**评分标准**:
- 0.9-1.0: 行业领先（创新架构、性能卓越、测试>95%）
- 0.8-0.9: 专业级（清晰分层、优于同类 70%+、测试>80%）
- 0.7-0.8: 良好（结构合理、平均水平、测试>60%）
- 0.6-0.7: 合格（基本结构、偶有卡顿、测试>40%）
- < 0.6: 不足（架构混乱、性能差、测试<40%）

### C 维度（认知增强）

```
C = (C₁ + C₂ + C₃ + C₄) / 4
```

| 子维度 | 权重 | 评估要点 |
|--------|------|----------|
| C₁ 知识沉淀 | 25% | 文档完整性、设计模式说明 |
| C₂ 决策支持 | 25% | 状态查询、进度追踪 |
| C₃ 学习辅助 | 25% | 代码注释、示例丰富度 |
| C₄ 洞察提供 | 25% | 历史追溯、数据分析 |

### O 维度（编排能力）

```
O = (O₁ + O₂ + O₃ + O₄) / 4
```

| 子维度 | 权重 | 评估要点 |
|--------|------|----------|
| O₁ 多技能协同 | 25% | 事件驱动、技能间通信 |
| O₂ 工作流编排 | 25% | 状态机、流程管理 |
| O₃ 资源调度 | 25% | 速率限制、并发控制 |
| O₄ 异常处理 | 25% | 重试机制、错误恢复 |

### E 维度（进化能力）

```
E = (E₁ + E₂ + E₃ + E₄) / 4
```

| 子维度 | 权重 | 评估要点 |
|--------|------|----------|
| E₁ 自优化 | 25% | 配置调整、性能优化 |
| E₂ 自学习 | 25% | 历史分析、模式识别 |
| E₃ 自适应 | 25% | 动态订阅、灵活扩展 |
| E₄ 版本管理 | 25% | 语义化版本、变更日志 |

### M 维度（市场验证）

```
M = (M₁ + M₂ + M₃ + M₄) / 4
```

| 子维度 | 权重 | 评估要点 |
|--------|------|----------|
| M₁ 用户验证 | 25% | 真实用户数、用户反馈 |
| M₂ 采用率 | 25% | 上架状态、下载量 |
| M₃ 反馈收集 | 25% | 反馈渠道、问题追踪 |
| M₄ 商业化 | 25% | 定价策略、商业计划 |

### U 维度（用户体验）

```
U = (U₁ + U₂ + U₃ + U₄) / 4
```

| 子维度 | 权重 | 评估要点 |
|--------|------|----------|
| U₁ 易用性 | 25% | API 简洁度、学习曲线 |
| U₂ 文档质量 | 25% | README 完整度、示例质量 |
| U₃ 错误提示 | 25% | 错误消息清晰度、解决建议 |
| U₄ 可访问性 | 25% | 接口友好度、平台支持 |

---

## 📋 评估流程

### Phase 1: 信息收集

1. 读取技能 SKILL.md 文件
2. 分析代码结构（目录、文件数、代码行数）
3. 检查测试文件（存在性、覆盖率）
4. 检查文档完整性（README、示例）
5. 检查上架状态（ClawHub 链接、版本）

### Phase 2: 维度评分

对每个维度执行：
1. 读取评估标准（references/six-dimensions-criteria.md）
2. 逐项检查子维度
3. 计算子维度得分
4. 汇总维度得分

### Phase 3: 报告生成

1. 生成六维得分表
2. 生成各维度详细评估
3. 生成待改进项（P0/P1/P2 优先级）
4. 输出评估报告（assets/evaluation-template.md）

### Phase 4: 改进建议

根据得分差距生成：
- P0（紧急）：差距>0.15 或阻塞上架
- P1（重要）：差距>0.05
- P2（次要）：差距≤0.05

---

## 🎯 应用的设计模式

### 1. 评估工厂模式（Evaluation Factory）

**来源**: first-principle-analyzer/src/evaluation-factory.js

**核心思想**: 将评估逻辑封装为可复用的工厂类，支持不同评估策略。

**本技能应用**:
```javascript
// 评估工厂类
class EvaluationFactory {
  createEvaluator(dimension) {
    switch(dimension) {
      case 'T': return new TechnologyEvaluator();
      case 'C': return new CognitionEvaluator();
      case 'O': return new OrchestrationEvaluator();
      case 'E': return new EvolutionEvaluator();
      case 'M': return new MarketEvaluator();
      case 'U': return new UserExperienceEvaluator();
    }
  }
}
```

### 2. 渐进式披露设计（Progressive Disclosure）

**来源**: skill-creator SKILL.md

**核心思想**: 三层加载系统（元数据→SKILL.md→资源文件），按需加载详细信息。

**本技能应用**:
- SKILL.md 保持核心流程（<500 行）
- 详细评估标准移至 references/six-dimensions-criteria.md
- 评估报告模板移至 assets/evaluation-template.md
- 评估引擎脚本移至 scripts/evaluation-engine.js

### 3. 六维评估模型（Six-Dimensions Model）

**来源**: 2026-04-15 学习日志（T 维度详细学习）

**核心思想**: 多维度综合评估，避免单一指标偏差。

**本技能应用**:
- 每个维度 4 个子维度，权重各 25%
- 维度得分 = 子维度平均
- 综合得分 = 六维平均
- 目标得分：≥0.70（B 级）

---

## 📁 文件结构

```
skill-quality-assurance/
├── SKILL.md                          # 本文件
├── scripts/
│   └── evaluation-engine.js          # 评估引擎核心
├── references/
│   └── six-dimensions-criteria.md    # 六维评估详细标准
└── assets/
    └── evaluation-template.md        # 评估报告模板
```

---

## 🔧 脚本使用说明

### evaluation-engine.js

**用途**: 执行自动化评估

**使用方法**:
```bash
node scripts/evaluation-engine.js <skill-path> [output-path]

示例：
node scripts/evaluation-engine.js ~/.openclaw/skills/meta-cognition-assistant
node scripts/evaluation-engine.js ~/.openclaw/skills/event-orchestrator ./reports
```

**输出**:
- 控制台输出六维得分摘要
- 生成 Markdown 评估报告

---

## ✅ 质量检查清单

### 上架前必查项（P0）

- [ ] 六维平均分 ≥ 0.70
- [ ] M 维度 ≥ 0.50（或已提交上架）
- [ ] T 维度 ≥ 0.70（技术质量达标）
- [ ] 文档完整（SKILL.md + README）
- [ ] 测试覆盖 ≥ 60%

### 推荐检查项（P1）

- [ ] 性能基准测试
- [ ] 用户反馈渠道
- [ ] 版本变更日志
- [ ] 示例代码丰富

### 可选检查项（P2）

- [ ] CLI 命令支持
- [ ] 多语言文档
- [ ] 视频教程

---

## 📈 评估报告示例

参考：`~/.openclaw/skills/event-orchestrator/docs/evaluation-report.md`

---

## 🎓 学习资源

- 六维评估标准：`references/six-dimensions-criteria.md`
- 评估工厂模式：`first-principle-analyzer/src/evaluation-factory.js`
- 渐进式披露设计：`skill-creator SKILL.md`

---

**创建时间**: 2026-04-15  
**创建者**: 王的奴隶 · 严谨专业版  
**应用知识**: 评估工厂模式、渐进式披露设计、六维评估模型
