# skill-health-monitor - 技能健康监控器【自研元能力】

**版本**：v0.1.0  
**定位**：技能健康实时监控引擎 - 自动检测技能健康问题，提供预警和优化建议

**创建时间**：2026-03-30  
**维护者**：王的奴隶 · 严谨专业版

---

## 🎯 适用场景

✅ 技能健康实时监控
✅ 多维度健康评估（六维模型）
✅ 自动预警（警告/严重/紧急三级）
✅ 技能组合健康分析
✅ 优化建议生成

---

## 🔧 核心功能

**设计模式应用**（本次创造重点）：

### 1. 单例模式（Singleton）
- 确保全局只有一个监控实例
- 统一状态管理，避免数据不一致
- 节省资源，避免重复初始化

### 2. 责任链模式（Chain of Responsibility）
- 三级健康检查处理器：紧急 → 严重 → 警告
- 逐级传递，快速定位问题级别
- 易于扩展新的检查级别

### 3. 模板方法模式（Template Method）
- 定义健康检查的标准流程
- 5 步固定流程：收集→计算→检查→记录→报告
- 子类可自定义数据收集和报告格式

**核心功能**：
- ✅ 六维健康度评估（T/C/O/E/M/U）
- ✅ 三级预警系统（warning/critical/emergency）
- ✅ 实时监控记录
- ✅ 优化建议生成
- ✅ 历史检查追踪

---

## 📋 工作流程

```
1. 接收技能健康检查请求
   ↓
2. 收集六维度指标数据
   ↓
3. 计算综合健康分数
   ↓
4. 责任链逐级检查（紧急→严重→警告）
   ↓
5. 记录检查结果和告警
   ↓
6. 生成健康报告和建议
   ↓
7. 交付报告
```

---

## 🚀 使用方法

### 方式 1：检查单个技能健康

```
检查 [技能名] 的健康状态

返回：
- 六维度得分
- 综合健康分数
- 健康级别（ok/warning/critical/emergency）
- 优化建议
```

### 方式 2：批量检查技能组合

```
检查以下技能的健康状态：[技能 1, 技能 2, 技能 3]

返回：
- 每个技能的健康报告
- 整体健康趋势
- 需要优先关注的技能
```

### 方式 3：查看告警历史

```
查看技能健康告警记录

返回：
- 告警列表（按时间排序）
- 告警级别分布
- 待处理告警
```

### 方式 4：代码调用（开发者）

```javascript
const { HealthCheckTemplate } = require('./src/health-monitor');

const monitor = new HealthCheckTemplate();

// 检查技能健康
const report = await monitor.checkSkillHealth('my-skill', {
  technicalDepth: 0.80,
  cognitiveEnhancement: 0.75,
  orchestration: 0.70,
  evolution: 0.85,
  commercialization: 0.60,
  userExperience: 0.70
});

console.log(report);
// 输出：
// {
//   skillName: 'my-skill',
//   healthScore: 0.73,
//   level: 'ok',
//   message: '检查通过',
//   dimensions: { ... }
// }
```

---

## 📊 六维评估模型

| 维度 | 代码 | 说明 | 权重 |
|------|------|------|------|
| **技术深度** | T | 代码质量、架构设计、设计模式应用 | 1/6 |
| **认知增强** | C | 是否提升用户理解能力和决策质量 | 1/6 |
| **编排能力** | O | 与其他技能的协作和解耦能力 | 1/6 |
| **进化能力** | E | 自我改进和适应能力 | 1/6 |
| **商业化** | M | 商业价值、定价策略、市场潜力 | 1/6 |
| **用户体验** | U | 易用性、文档质量、交互设计 | 1/6 |

**健康分数计算**：
```
healthScore = (T + C + O + E + M + U) / 6
```

**健康级别阈值**：
- `ok`: ≥ 0.70（B 级及以上）
- `warning`: 0.50 - 0.70（C 级，需要优化）
- `critical`: 0.30 - 0.50（D 级，需要紧急修复）
- `emergency`: < 0.30（F 级，需要立即干预）

---

## 💼 服务定价

| 版本 | 价格 | 包含 |
|------|------|------|
| 个人版 | $49.9 | 永久使用 +1 年更新 + 基础监控 |
| 商业版 | $149.9 | 商业用途 + 实时监控 + 告警通知 |
| 企业版 | $499.9 | 定制部署 + 历史分析 + API 访问 |

**企业联系**：business@cloud-shrimp.com

---

## 🏆 头部技能对标

**对标**：skill-evolver（技能进化器）

**差异化优势**：
- ✅ 实时监控 vs 定期分析
- ✅ 自动预警 vs 手动查询
- ✅ 三级告警系统 vs 单一评估
- ✅ 轻量级部署 vs 完整分析引擎

**互补关系**：
- skill-health-monitor 负责实时监控和预警
- skill-evolver 负责深度分析和优化方案
- 两者可结合使用，形成完整的技能生命周期管理

---

## 📐 设计模式详解

### 单例模式（Singleton）

**实现**：
```javascript
class HealthMonitorInstance {
  constructor() {
    if (HealthMonitorInstance._instance) {
      return HealthMonitorInstance._instance;
    }
    HealthMonitorInstance._instance = this;
  }
}
```

**优势**：
- 全局唯一实例，避免状态不一致
- 节省内存和初始化开销
- 便于集中管理监控数据

**适用场景**：
- 配置管理
- 日志记录
- 监控中心
- 缓存管理

---

### 责任链模式（Chain of Responsibility）

**实现**：
```javascript
// 构建责任链
this.chain = new EmergencyCheckHandler()
  .setNext(new CriticalCheckHandler())
  .setNext(new WarningCheckHandler());

// 执行检查
const result = this.chain.handle(skillData);
```

**优势**：
- 解耦请求发送者和接收者
- 动态组合检查逻辑
- 易于添加新的检查级别

**适用场景**：
- 多级审批流程
- 异常处理
- 数据过滤
- 权限验证

---

### 模板方法模式（Template Method）

**实现**：
```javascript
async checkSkillHealth(skillName, metrics) {
  const skillData = this.collectSkillData(skillName, metrics);  // 可自定义
  const healthScore = this.calculateHealthScore(skillData);     // 固定
  const checkResult = this.chain.handle(skillData);             // 固定
  this.recordCheckResult(skillName, healthScore, checkResult);  // 固定
  const report = this.generateReport(skillName, skillData, checkResult); // 可自定义
  return report;
}
```

**优势**：
- 定义算法骨架，子类实现细节
- 代码复用，避免重复
- 易于扩展新的检查类型

**适用场景**：
- 数据处理流程
- 报告生成
- 任务执行框架

---

## 📞 支持

- 📧 support@cloud-shrimp.com
- 💬 微信：CloudShrimpSupport

**响应**：24 小时内

---

## 📁 项目结构

```
skill-health-monitor/
├── SKILL.md                 # 技能文档
├── src/
│   └── health-monitor.js    # 核心实现（3 个设计模式）
├── examples/
│   └── usage-examples.md    # 使用示例
├── assets/
│   └── ...                  # 资源文件
└── package.json             # 依赖配置
```

---

## 🐛 已知局限

1. **数据持久化**：当前监控数据存储在内存中，重启后丢失
2. **被动检查**：需要主动调用检查，非完全自动监控
3. **阈值固定**：健康阈值需要手动配置，不支持自适应调整

---

## 📈 版本规划

### v0.2.0（规划中）

- [ ] 数据持久化（SQLite/JSON 文件）
- [ ] 定时自动检查（cron 集成）
- [ ] 告警通知（邮件/消息推送）
- [ ] 健康趋势图表
- [ ] 自适应阈值调整

### v0.3.0（愿景）

- [ ] 机器学习预测（基于历史数据预测健康趋势）
- [ ] 自动优化建议生成
- [ ] 技能依赖关系分析
- [ ] 团队协作监控

---

## 💡 使用技巧

### 技巧 1：定期检查

每天调用一次：
```
检查所有技能的健康状态
```

### 技巧 2：版本发布前检查

每次发布新版本前：
```
检查 [技能名] 的健康状态，确保≥0.70
```

### 技巧 3：告警响应

收到告警时：
```
查看 [技能名] 的详细健康报告，分析短板维度
```

### 技巧 4：组合使用

与 skill-evolver 结合：
```
1. 用 skill-health-monitor 发现健康问题
2. 用 skill-evolver 生成详细优化方案
3. 实施优化后再次检查确认
```

---

**版本**：v0.1.0 | **创建**：2026-03-30 | **维护者**：王的奴隶 · 严谨专业版
