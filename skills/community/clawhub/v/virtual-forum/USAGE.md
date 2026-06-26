# 使用指南 Usage Guide

> 虚拟论坛 V3.5 完整API文档

## 📖 目录

1. [快速开始](#快速开始)
2. [基础API](#基础api)
3. [进阶用法](#进阶用法)
4. [博弈论模式](#博弈论模式)
5. [配置选项](#配置选项)
6. [错误处理](#错误处理)
7. [最佳实践](#最佳实践)

---

## 快速开始

### 最简单示例

```javascript
const VirtualForum = require('./index.js');

const forum = new VirtualForum();

// 启动一场辩论
const result = await forum.launchArena({
  topic: 'AI是否会取代人类工作',
  participants: [
    { name: '马斯克', skillName: 'elon-musk' },
    { name: '巴菲特', skillName: 'warren-buffett' }
  ]
});

console.log(result.output);
```

---

## 基础API

### 1. VirtualForum 类

#### 构造函数

```javascript
const forum = new VirtualForum(skillsDir);
```

| 参数 | 类型 | 必需 | 描述 |
|------|------|------|------|
| skillsDir | string | 否 | Skill文件目录，默认 `~/.openclaw/skills` |

#### 方法概览

| 方法 | 描述 | 版本 |
|------|------|------|
| `createDiscussion(config)` | 模拟模式 | v1.0 |
| `launchArena(config)` | 子代理交锋模式 | v2.0 |
| `launchGameTheoryArena(config)` | 博弈论增强模式 | v3.5 ⭐ |

---

### 2. 标准子代理模式 (v2.0)

```javascript
const result = await forum.launchArena({
  // 必需参数
  topic: '辩论话题',
  participants: [
    { name: '参与者1', skillName: 'skill-1' },
    { name: '参与者2', skillName: 'skill-2' }
  ],
  
  // 可选参数
  mode: 'adversarial',        // 讨论模式
  rounds: 10,                 // 轮次
  moderatorName: '主持人',     // 主持人名称
  moderatorSkill: 'host-skill', // 主持人Skill
  moderatorStyle: 'provocative', // 主持风格
  outputFormat: 'dialogue'    // 输出格式
});
```

#### 返回结果

```javascript
{
  arena: Object,      // 完整的辩论数据
  output: string      // 格式化输出
}
```

---

## 进阶用法

### 上下文管理器 (Token优化)

```javascript
const result = await forum.launchArena({
  topic: '长期话题',
  participants: [...],
  
  // Token优化参数
  contextWindowSize: 6,        // 滑动窗口大小（保留最近6轮）
  summarizeEveryNRounds: 5     // 每5轮生成摘要
});

// 效果：50轮辩论的Token消耗从100K降至30K
```

### 暂停和恢复

```javascript
const arena = new SubagentArena();
await arena.initArena({...});

// 运行辩论
const debatePromise = arena.runDebate();

// 5秒后暂停
setTimeout(() => {
  arena.pause();
  console.log('辩论已暂停');
}, 5000);

// 10秒后恢复
setTimeout(() => {
  arena.resume();
  console.log('辩论已恢复');
}, 10000);

await debatePromise;
```

### 进度回调

```javascript
arena.onRoundComplete = (round, speeches) => {
  console.log(`第${round}轮完成`);
  console.log('本轮发言:', speeches.map(s => s.speaker).join(', '));
  
  // 可以在这里实现流式输出
  io.emit('roundComplete', { round, speeches });
};

await arena.runDebate();
```

---

## 博弈论模式

### 完整配置示例

```javascript
const result = await forum.launchGameTheoryArena({
  // 基础配置
  topic: '并购谈判',
  participants: [
    { name: '买方CEO', skillName: 'aggressive-ceo' },
    { name: '卖方CEO', skillName: 'defensive-ceo' }
  ],
  rounds: 20,
  
  // 博弈论参数（关键！）
  discountFactors: {
    '买方CEO': 0.95,    // 高耐心，可以慢慢谈
    '卖方CEO': 0.80     // 低耐心，急于成交
  },
  
  outsideOptions: {     // BATNA - 最佳替代方案
    '买方CEO': 40,      // 可以找其他收购目标
    '卖方CEO': 15       // 选择有限
  },
  
  totalValue: 100,      // 总价值池
  
  types: {              // 类型定义（用于信号博弈）
    '买方CEO': 'aggressive',
    '卖方CEO': 'cooperative'
  },
  
  priorBeliefs: {       // 先验信念
    '买方CEO': { hardliner: 0.7, cooperative: 0.3 },
    '卖方CEO': { hardliner: 0.3, cooperative: 0.7 }
  },
  
  reputationTypes: {    // 声誉类型
    '买方CEO': 'tough',
    '卖方CEO': 'flexible'
  }
});

// 输出结果
console.log(result.output);              // 辩论记录
console.log(result.gameTheoryReport);    // 博弈论分析报告
```

### 返回结果

```javascript
{
  arena: Object,           // 辩论数据
  output: string,          // 格式化输出
  gameTheoryReport: string // 博弈论分析报告
}
```

### 博弈论报告示例

```
🎲 博弈论状态报告
═══════════════════════
总价值池: 100
当前轮次: 15

【买方CEO】
 折扣因子: 0.95
 外部选项(BATNA): 40
 当前效用: 52.3
 声誉类型: tough
 应该让步: 否

【卖方CEO】
 折扣因子: 0.8
 外部选项(BATNA): 15
 当前效用: 28.7
 声誉类型: flexible
 应该让步: 是 ⚠️
```

---

## 配置选项

### 讨论模式 (mode)

| 值 | 描述 | 适用场景 |
|----|------|----------|
| `exploratory` | 探索性讨论 | 复杂问题，需要多角度 |
| `adversarial` | 对抗性辩论 | 明确分歧，需要胜负 |
| `decision` | 决策型讨论 | 需要拍板决策 |

### 主持人风格 (moderatorStyle)

| 值 | 描述 | 特点 |
|----|------|------|
| `balanced` | 理性主持人 | 客观中立，善于引导 |
| `provocative` | 犀利主持人 | 追问到底，挑战漏洞 |
| `synthesizing` | 整合主持人 | 归纳观点，推动共识 |

### 输出格式 (outputFormat)

| 值 | 描述 |
|----|------|
| `dialogue` | 对话流格式（默认） |
| `report` | 结构化报告 |
| `decision` | 决策建议书 |
| `json` | JSON格式 |

### 完整默认配置

```javascript
const DEFAULTS = {
  mode: 'adversarial',
  rounds: 10,
  moderatorName: '巴菲特',
  moderatorSkill: 'warren-buffett',
  moderatorStyle: 'provocative',
  verdictType: 'points',
  outputFormat: 'dialogue',
  minResponseLength: 200,
  maxResponseLength: 400,
  contextWindowSize: 6,
  summarizeEveryNRounds: 5,
  apiRetryAttempts: 3,
  apiBaseDelay: 2000,
  gameTheory: {
    totalValue: 100,
    defaultDiscountFactor: 0.9,
    defaultOutsideOption: 20,
    defaultReputationType: 'balanced'
  }
};
```

---

## 错误处理

### 常见错误

```javascript
try {
  const result = await forum.launchArena({
    topic: '',  // 空话题
    participants: []  // 空参与者
  });
} catch (err) {
  console.error(err.message);
  // 输出: 话题(topic)不能为空
  // 或: 至少需要2位参与者(participants)
}
```

### Skill加载失败

```javascript
// Skill不存在时的处理
const result = await forum.launchArena({
  topic: '测试',
  participants: [
    { name: '未知人物', skillName: 'non-existent-skill' },
    { name: '巴菲特', skillName: 'warren-buffett' }
  ]
});

// 输出警告但继续运行：
// ⚠️ 未知人物 (Skill 加载失败，将使用空背景)
// ✓ 巴菲特
```

### API调用失败

```javascript
// 自动重试机制
for (let attempt = 0; attempt < 3; attempt++) {
  try {
    return await apiCall();
  } catch (e) {
    if (attempt < 2) {
      await exponentialBackoff(attempt);  // 指数退避
    } else {
      return '（本轮未能发言）';  // 优雅降级
    }
  }
}
```

---

## 最佳实践

### 1. 选择合适的模式

```javascript
// 探索性讨论 - 适合复杂议题
forum.launchArena({
  topic: '未来10年科技趋势',
  mode: 'exploratory',
  participants: [{...}, {...}, {...}]  // 可以多人
});

// 对抗性辩论 - 适合明确分歧
forum.launchArena({
  topic: '是否应该全面禁止燃油车',
  mode: 'adversarial',
  participants: [enviromentalist, oilExecutive]  // 两方对立
});

// 决策型讨论 - 需要结论
forum.launchArena({
  topic: '选择哪个技术方案',
  mode: 'decision',
  participants: [cto, cfo, cpo]
});
```

### 2. Token优化建议

```javascript
// 长辩论（>20轮）务必启用Token优化
forum.launchArena({
  topic: '长期话题',
  rounds: 50,
  contextWindowSize: 6,        // 滑动窗口
  summarizeEveryNRounds: 5     // 定期摘要
});

// 短辩论可以不优化
forum.launchArena({
  topic: '快速讨论',
  rounds: 5
  // 不需要Token优化参数
});
```

### 3. 博弈论参数调优

```javascript
// 耐心 vs 急躁
const configs = {
  patient: {    // 巴菲特类型
    discountFactor: 0.95,
    outsideOption: 50    // 有很多选择
  },
  impatient: {  // 创业公司CEO
    discountFactor: 0.80,
    outsideOption: 10    // 时间不多了
  }
};
```

### 4. 错误处理模式

```javascript
async function safeDebate(config) {
  try {
    validateConfig(config);  // 先验证
    const result = await forum.launchArena(config);
    return { success: true, data: result };
  } catch (err) {
    console.error('辩论启动失败:', err.message);
    return { success: false, error: err.message };
  }
}
```

---

## 示例代码库

### 示例1: 投资委员会

```javascript
const result = await forum.launchGameTheoryArena({
  topic: 'NVDA估值是否合理',
  participants: [
    { name: '巴菲特', skillName: 'warren-buffett' },
    { name: '木头姐', skillName: 'cathie-wood' },
    { name: '达里奥', skillName: 'ray-dalio' }
  ],
  discountFactors: {
    '巴菲特': 0.95,    // 长期投资者，极有耐心
    '木头姐': 0.85,    // 成长股偏好，中等耐心
    '达里奥': 0.90     // 宏观视角，平衡
  },
  outsideOptions: {
    '巴菲特': 80,      // 很多其他投资机会
    '木头姐': 40,
    '达里奥': 60
  }
});
```

### 示例2: 政策辩论

```javascript
const result = await forum.launchArena({
  topic: '加密货币监管政策',
  participants: [
    { name: '支持方', skillName: 'crypto-advocate' },
    { name: '反对方', skillName: 'regulator' }
  ],
  mode: 'adversarial',
  rounds: 20,
  moderatorStyle: 'provocative',  // 犀利主持，追问到底
  contextWindowSize: 8            // 政策辩论需要较长记忆
});
```

### 示例3: 产品决策

```javascript
const result = await forum.launchArena({
  topic: '下一代产品功能优先级',
  participants: [
    { name: '产品经理', skillName: 'pm' },
    { name: '技术负责人', skillName: 'cto' },
    { name: '设计师', skillName: 'designer' }
  ],
  mode: 'decision',
  rounds: 15,
  outputFormat: 'decision'  // 输出决策建议书
});
```

---

## 更多资源

- [README](../README.md) - 项目概览
- [CHANGELOG](../CHANGELOG.md) - 版本历史
- [v3/README](../v3/README.md) - 博弈论技术细节

---

**最后更新**: 2026-04-12  
**适用版本**: v3.5.0
