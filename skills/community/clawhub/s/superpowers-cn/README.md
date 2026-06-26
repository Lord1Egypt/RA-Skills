# 超能力 CN (Superpowers CN)

🧠 **让AI做事更有逻辑、更有章法**

> 中文AI工作流框架 - 借鉴 [Superpowers](https://github.com/obra/superpowers)，专为中文AI助手设计

**⭐ 120k GitHub Stars 的中文复刻版**

---

## 理念

**不是直接写代码，而是：理解需求 → 设计方案 → 确认执行 → 逐步完成**

传统AI工作流：
```
用户 → AI立刻写代码 → 结果往往不符合预期 → 反复修改
```

超能力CN工作流：
```
用户 → AI先问清楚 → AI设计并确认 → AI逐步执行 → 交付符合预期
```

## 工作流

```
┌─────────────────────────────────────────────────────────┐
│  1️⃣  澄清 (Clarify)                                     │
│       - 理解真正的问题是什么                            │
│       - 问清楚你要什么                                  │
│       - 明确范围和限制                                   │
├─────────────────────────────────────────────────────────┤
│  2️⃣  设计 (Plan)                                       │
│       - 制定具体方案                                    │
│       - 展示文件结构和模块                              │
│       - 展示给你确认                                    │
├─────────────────────────────────────────────────────────┤
│  3️⃣  执行 (Execute)                                    │
│       - 分解成小任务                                    │
│       - 逐步完成并验证                                  │
│       - 及时汇报进度                                    │
├─────────────────────────────────────────────────────────┤
│  4️⃣  审核 (Review)                                     │
│       - 检查是否符合需求                                │
│       - 代码质量review                                  │
│       - 最终交付确认                                    │
└─────────────────────────────────────────────────────────┘
```

## 核心模块

| 模块 | 文件 | 功能 |
|------|------|------|
| 澄清 | `workflows/clarify.js` | 生成需求澄清问题 |
| 设计 | `workflows/plan.js` | 制定设计方案 |
| 执行 | `workflows/execute.js` | 分解并执行任务 |
| 审核 | `workflows/review.js` | 验证结果质量 |

## 安装

### 方法一：放入AI助手的skills目录

```bash
# 克隆到本地
git clone https://github.com/yourusername/superpowers-cn.git

# 放入AI助手skills目录
cp -r superpowers-cn /path/to/your/ai/skills/
```

### 方法二：作为独立模块使用

```javascript
import { generateClarifyQuestions } from './workflows/clarify.js';
import { generatePlan } from './workflows/plan.js';
```

## 使用示例

```javascript
import { generateClarifyQuestions } from './workflows/clarify.js';

// 收到用户请求时
const questions = generateClarifyQuestions('做一个待办事项CLI工具');
console.log(questions);

// 输出：
// ## 🎯 需求澄清
// 
// 在开始之前，我想确认几个问题：
// 
// 1. 你想解决什么问题？
// 2. 最终效果是什么样的？
// 3. 有什么限制或要求？
// ...
```

## 与原版Superpowers的区别

| 特性 | Superpowers (原版) | 超能力 CN |
|------|-------------------|----------|
| 语言 | 英文 | **中文** |
| 平台 | Claude Code/Cursor | **通用** |
| 复杂度 | 高（完整TDD） | **简化版** |
| 学习成本 | 高 | **低** |
| 适用场景 | 复杂企业项目 | **日常小工具** |

## 适用人群

- 😤 **受够了AI乱来** - 想要AI先想清楚再做
- 🤔 **需求经常被误解** - 想要AI先确认再动手  
- 📝 **快速原型开发** - 想要有章法的快速迭代
- 🎓 **学习编程** - 想要看AI的设计思路

## 开源协议

**MIT License** - 随便用，商用也可以，不需要署名

## 参与贡献

欢迎提交 Issue 和 PR！

- 🐛 报告Bug
- 💡 提出新功能
- 📖 完善文档
- 🔧 提交代码

---

**超能力 CN** - 让AI成为真正的助手，而不是乱来的代码生成器。

Made with ❤️ by [张满仓](https://github.com/yourusername)
