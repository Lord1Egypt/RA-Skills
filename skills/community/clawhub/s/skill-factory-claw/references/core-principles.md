# Core Principles — 智能体工程核心原则速查

> 来源：OpenAI Harness Engineering (2026-02-11)  
> 适用场景：在回答智能体工程问题时的快速参考

---

## Principle 1：人类掌舵，智能体执行

**"Humans steer, agents row."**

人类工程师的工作不是写代码，而是：
- **设计环境**（Environment Design）
- **明确意图**（Intent Specification）  
- **构建反馈回路**（Feedback Loop Engineering）

---

## Principle 2：情境是稀缺资源

**"Context is scarce. Be a map, not a manual."**

- `AGENTS.md` ≤ 100 行，作为目录指向深层文档
- 绝不把所有规则塞进一个文件
- 渐进式披露（Progressive Disclosure）

---

## Principle 3：通过不变量约束，而非微观管理

**"Enforce invariants, not instructions."**

- 严格分层架构：`Types → Config → Repo → Service → Runtime → UI`
- 约束通过 linter 自动强制，不依赖约定
- 在错误信息中嵌入修复指令，让智能体自我修正

---

## Principle 4：让应用对智能体可读

**"Make your app observable to agents."**

- UI：接入 Chrome DevTools 协议（DOM + 截图 + 导航）
- 日志：LogQL 查询
- 指标：PromQL 查询
- 目标：让性能要求变成可验证的提示

---

## Principle 5：持续垃圾回收技术债务

**"GC your codebase like memory."**

- 黄金原则（Golden Rules）定义代码应有的形态
- 循环后台任务扫描偏差 → 发起重构 PR → 快速合并
- 小额持续偿还 > 周期性大规模清理

---

## Principle 6：纠错成本低于等待成本

**"The cost of correction is lower than the cost of delay."**

- 减少阻塞合并门
- PR 生命周期保持短暂
- 偶发测试失败通过重跑解决，不无限期阻塞

---

## Principle 7：仓库是唯一真相来源

**"If it's not in the repo, it doesn't exist for agents."**

- Docs、聊天记录、人脑中的知识对智能体不可见
- 每次决策后立即更新仓库文档
- 计划作为一等公民提交进仓库

---

## Principle 8：偏好智能体可读的技术

**"Choose tech that's legible to agents."**

偏好：可组合 + API 稳定 + 训练数据中充分表示  
必要时：重新实现功能子集 > 绕过不透明的上游库

---

## Principle 9：架构约束是早期先决条件（反直觉）

**"Strict architecture is a Day-1 prerequisite for agent-first, not a Day-100 luxury."**

- 传统工程：严格分层架构通常等到百人团队规模时才考虑
- 智能体工程：必须在项目初期就到位，否则 AI 残渣以指数级扩散
- 智能体会无差别放大代码库中的所有模式——好的坏的均会复制

---

## Principle 10：自我审查闭环（Ralph Wiggum 循环）

**"Agents review their own changes—humans only intervene where judgment is needed."**

```
Codex 本地审核自身变更
    → 请求额外审查（智能体或人类）
    → 响应反馈 → 修改
    → 循环直到满意
    → 合并
```

- 这是"无需人工直接编码"成为可能的关键机制
- 人类只在需要真正判断力的节点介入

---

## 快速判断框架

遇到问题时，按以下顺序思考：

```
1. 这个问题是否可以通过「架构约束」自动解决？
   → 是：写成 linter 规则或结构测试
   → 否：继续

2. 这个知识是否在代码仓库中可查？
   → 否：立即更新文档
   → 是：继续

3. 智能体是否能「看到」相关的 UI/日志/指标？
   → 否：建立可观测性接口
   → 是：继续

4. 情境文件是否过载？
   → 是：拆分为目录 + 深层文档
   → 否：继续执行任务
```
