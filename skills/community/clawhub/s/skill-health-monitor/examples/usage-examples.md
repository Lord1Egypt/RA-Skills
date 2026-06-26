# skill-health-monitor 使用示例

## 示例 1：检查单个技能健康

**场景**：检查 meta-skill-weaver 的健康状态

**调用**：
```
检查 meta-skill-weaver 的健康状态
```

**预期输出**：
```markdown
## 技能健康报告：meta-skill-weaver

**综合健康分数**：0.78/1.00 ✅
**健康级别**：ok（良好）

### 六维度评估

| 维度 | 得分 | 状态 |
|------|------|------|
| 技术深度 (T) | 0.85 | ✅ |
| 认知增强 (C) | 0.75 | ✅ |
| 编排能力 (O) | 0.90 | ✅ |
| 进化能力 (E) | 0.70 | ✅ |
| 商业化 (M) | 0.75 | ✅ |
| 用户体验 (U) | 0.75 | ✅ |

### 建议
继续保持当前状态，建议定期复查。
```

---

## 示例 2：检查技能组合

**场景**：检查所有自研技能的健康状态

**调用**：
```
检查以下技能的健康状态：meta-skill-weaver, skill-evolver, first-principle-analyzer
```

**预期输出**：
```markdown
## 技能组合健康报告

### 整体概况
- 检查技能数：3
- 平均健康分数：0.75
- 健康技能：2
- 需要关注：1

### 详细报告

#### meta-skill-weaver：0.78 ✅
状态：良好

#### skill-evolver：0.74 ✅
状态：良好

#### first-principle-analyzer：0.68 ⚠️
状态：需要优化
短板维度：商业化 (M: 0.50)、用户体验 (U: 0.60)
建议：完善文档和示例，考虑商业化包装
```

---

## 示例 3：代码调用（开发者）

**场景**：在技能中集成健康监控

**代码**：
```javascript
const { HealthCheckTemplate } = require('skill-health-monitor');

class MySkill {
  constructor() {
    this.monitor = new HealthCheckTemplate();
  }

  async execute(task) {
    // 执行前健康检查
    const preCheck = await this.monitor.checkSkillHealth('my-skill', {
      technicalDepth: 0.80,
      cognitiveEnhancement: 0.75,
      orchestration: 0.70,
      evolution: 0.85,
      commercialization: 0.60,
      userExperience: 0.70
    });

    if (preCheck.level === 'emergency') {
      throw new Error('技能健康度紧急，暂停服务');
    }

    // 执行任务
    const result = await this.doTask(task);

    // 执行后健康检查
    const postCheck = await this.monitor.checkSkillHealth('my-skill', {
      // 更新指标
    });

    return { result, healthReport: postCheck };
  }
}
```

---

## 示例 4：告警处理

**场景**：收到技能健康告警

**调用**：
```
查看技能健康告警记录
```

**预期输出**：
```markdown
## 技能健康告警记录

### 待处理告警（2）

#### 🚨 紧急告警
- 技能：deprecated-skill
- 级别：emergency
- 健康分数：0.25
- 时间：2026-03-30 14:30
- 建议：立即停止服务，回滚到上一版本

#### ⚠️ 警告告警
- 技能：old-analyzer
- 级别：warning
- 健康分数：0.65
- 时间：2026-03-30 10:00
- 建议：分析短板维度，制定优化计划

### 历史告警（5）
[展开查看...]
```

---

## 示例 5：与 skill-evolver 结合使用

**场景**：完整技能生命周期管理

**工作流**：
```
1. skill-health-monitor 发现健康问题
   ↓
2. skill-evolver 分析原因并生成优化方案
   ↓
3. 实施优化
   ↓
4. skill-health-monitor 验证优化效果
```

**调用序列**：
```
# 步骤 1：发现健康问题
检查 first-principle-analyzer 的健康状态
→ 发现健康分数 0.65，级别 warning

# 步骤 2：分析原因
如何优化 first-principle-analyzer？
→ skill-evolver 分析短板，生成优化方案

# 步骤 3：实施优化
[根据优化方案进行改进]

# 步骤 4：验证效果
再次检查 first-principle-analyzer 的健康状态
→ 健康分数提升至 0.78，级别 ok ✅
```

---

## 最佳实践

### 1. 定期检查频率

| 技能类型 | 检查频率 |
|----------|----------|
| 核心技能 | 每天 1 次 |
| 重要技能 | 每周 2-3 次 |
| 一般技能 | 每周 1 次 |
| 实验技能 | 每月 1 次 |

### 2. 告警响应 SLA

| 告警级别 | 响应时间 | 处理时间 |
|----------|----------|----------|
| emergency | 立即 | < 1 小时 |
| critical | < 4 小时 | < 24 小时 |
| warning | < 24 小时 | < 1 周 |

### 3. 健康目标

| 技能等级 | 目标健康分数 |
|----------|--------------|
| 核心技能 | ≥ 0.85 |
| 重要技能 | ≥ 0.75 |
| 一般技能 | ≥ 0.70 |
| 实验技能 | ≥ 0.60 |

---

## 故障排除

### 问题 1：健康分数计算不准确

**原因**：六维度指标输入有误
**解决**：确保每个维度得分在 0-1 之间，使用客观评估标准

### 问题 2：告警过多

**原因**：阈值设置过严
**解决**：根据技能重要性调整阈值，核心技能用严格阈值，实验技能用宽松阈值

### 问题 3：监控数据丢失

**原因**：内存存储，重启后丢失
**解决**：v0.2.0 将支持数据持久化，当前版本建议定期导出报告

---

**文档版本**：v0.1.0  
**最后更新**：2026-03-30
