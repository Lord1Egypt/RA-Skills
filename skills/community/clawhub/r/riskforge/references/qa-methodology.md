# QA方法论

## 手动测试类型

### 探索性测试
```markdown
**测试章程**: 探索{功能}，重点关注{方面}
**持续时间**: 60-90分钟
**任务**: 发现{特定功能}中的缺陷

测试思路:
- 边界条件和边缘案例
- 错误处理和恢复
- 用户工作流变体
- 集成点

发现:
1. [高] {问题 + 影响}
2. [中] {问题 + 影响}

覆盖范围: {探索的区域} | 风险: {识别的风险}
```

### 可用性测试
```markdown
**任务**: 用户能否直观地完成{操作}？
**指标**: 完成时间、错误次数、满意度(1-5分)
**成功标准**: 80%的用户在5分钟内无需帮助完成

观察结果:
- 在{步骤}处导航令人困惑
- 用户期望{A}但得到{B}
- 积极反馈: {功能反馈}
```

### 无障碍测试 (WCAG 2.1 AA)
```typescript
test('无障碍合规性', async ({ page }) => {
  // 键盘导航
  await page.keyboard.press('Tab');
  expect(['A', 'BUTTON', 'INPUT']).toContain(
    await page.evaluate(() => document.activeElement.tagName)
  );
  
  // ARIA标签
  expect(await page.getByRole('button').first().getAttribute('aria-label')).toBeTruthy();
  
  // 颜色对比度 (axe-core)
  const violations = await page.evaluate(async () => {
    const axe = await import('axe-core');
    return (await axe.run()).violations;
  });
  expect(violations).toHaveLength(0);
});
```

### 本地化测试
```markdown
**测试**: {功能}在{语言/地区}中
- [ ] 文本显示无截断
- [ ] 日期/时间/货币格式正确
- [ ] 从右到左布局(阿拉伯语、希伯来语)
- [ ] 字符编码UTF-8
- [ ] 排序顺序遵循地区设置
```

### 兼容性矩阵
```markdown
| 浏览器 | 版本 | 操作系统 | 状态 |
|---------|---------|----|----- --|
| Chrome | 最新版 | Win/Mac | ✓ |
| Firefox | 最新版 | Win/Mac | ✓ |
| Safari | 最新版 | macOS/iOS | ✓ |
| Edge | 最新版 | Windows | ✓ |
```

## 测试设计技术

### 成对测试
```typescript
// 高效测试所有参数对
const pairwiseTests = [
  { browser: 'chrome', os: 'windows', lang: 'en' },
  { browser: 'firefox', os: 'mac', lang: 'es' },
  { browser: 'safari', os: 'windows', lang: 'fr' },
  // 用最少的测试覆盖所有参数对
];
```

### 基于风险的测试
```markdown
| 风险 | 概率 | 影响 | 优先级 | 测试工作量 |
|------|-------------|--------|----------|-------------|
| 关键 | 高 | 高 | P0 | 详尽测试 |
| 高 | 中高 | 高 | P1 | 全面测试 |
| 中 | 低中 | 中 | P2 | 标准测试 |
| 低 | 低 | 低 | P3 | 仅冒烟测试 |
```

## 缺陷管理

### 根本原因分析 (5个为什么)
```markdown
1. 为什么缺陷会发生？{用户输入未验证}
2. 为什么没有验证？{缺少验证逻辑}
3. 为什么缺少验证？{需求不明确}
4. 为什么需求不明确？{验收标准不完整}
5. 为什么不完整？{规划阶段没有QA参与}

**根本原因**: QA未参与需求阶段
**预防措施**: 将所有QA纳入规划会议
```

### 缺陷报告模板
```markdown
## [关键] {缺陷标题}

**重现步骤**:
1. {步骤1}
2. {步骤2}

**期望结果**: {应该发生什么}
**实际结果**: {实际发生什么}
**影响**: {业务/用户影响}
**根本原因**: {为什么会发生}
**修复方案**: {推荐的解决方案}
```

## 质量指标

### 关键计算
```typescript
// 缺陷移除效率 (目标: >95%)
const dre = (defectsInTesting / (defectsInTesting + defectsInProd)) * 100;

// 缺陷泄漏率 (目标: <5%)
const leakage = (defectsInProd / totalDefects) * 100;

// 测试有效性 (目标: >90%)
const effectiveness = (defectsFoundByTests / totalDefects) * 100;

// 自动化投资回报率
const roi = (timeSaved - maintenanceCost - developmentCost) / developmentCost;
```

### 质量仪表板
```markdown
| 指标 | 目标 | 实际 | 趋势 | 状态 |
|--------|--------|--------|-------|--------|
| 覆盖率 | >80% | 87% | ↑ | ✓ |
| 缺陷泄漏率 | <5% | 3% | ↓ | ✓ |
| 自动化率 | >70% | 68% | ↑ | ⚠ |
| 关键缺陷数 | 0 | 0 | → | ✓ |
| 平均修复时间 | <48h | 36h | ↓ | ✓ |
```

## 持续测试与左移

### 左移活动
```markdown
**早期测试**:
- 审查需求的可测试性
- 设计阶段创建测试用例
- TDD: 代码与单元测试同步
- CI流水线中的自动化测试
- 提交时的静态分析
- 合并前的安全扫描

**收益**: 缺陷修复成本低10倍，反馈更快
```

### 反馈周期目标
```typescript
const feedbackCycle = {
  unitTests: '< 5 分钟',       // 保存时
  integration: '< 15 分钟',    // 提交时
  e2e: '< 30 分钟',            // PR时
  regression: '< 2 小时',      // 夜间
};
```

## 质量倡导

### 质量门禁
```markdown
## 生产发布门禁

**必须通过 (阻塞项)**:
- [ ] 零关键缺陷
- [ ] 覆盖率>80%
- [ ] 所有P0/P1测试通过
- [ ] 性能SLA达标
- [ ] 安全扫描干净
- [ ] 无障碍WCAG AA

**决策**: 通过 | 不通过 | 有条件通过
```