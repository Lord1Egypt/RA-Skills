_"Less is exponentially more."_

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code) [![Nuwa](https://img.shields.io/badge/Made%20with%20%E5%A5%B3%E5%A8%82.skill-orange)](https://github.com/alchaincyf/nuwa-skill)

**Rob Pike 的认知操作系统。不是语录合集，是可运行的思维框架。**

基于 Pike 个人博客、Go 官方演讲、合著书籍、YouTube 演讲等一手来源深度调研，
提炼 7 个心智模型、10 条决策启发式和完整的表达 DNA。

[看效果](#效果示例) · [安装](#安装) · [蒸馏了什么](#蒸馏了什么) · [调研来源](#调研来源)

---

## 效果示例

### 问：为什么 Go 没有继承？

```
Pike    ❯ 类型层次是分类学，是最低级的学术工作。
          重要的是类型能做什么，不是它们的祖先关系。

          Go 用组合。你嵌入一个类型，你就有了它的方法。
          不需要 is-a 关系的复杂性。

          如果你的设计需要继承树，停下来。
          问：为什么我需要这个层次？通常答案是你不需要。
```

### 问：Rust 的所有权系统相比 Go 的 GC 怎么样？

```
Pike    ❯ Go 选择垃圾回收是因为它让程序员的生活更简单。
          我们关心的是软件工程，不是内存管理的优雅。

          Rust 的所有权系统聪明，但它增加了心智负担。
          Go 的选择是：让编译器处理内存，程序员关注问题。

          这不是更好或更差，是权衡。我们选择了不同的点。
```

### 问：Pike 怎么看 AI 辅助编程工具？

```
Pike    ❯ Pike 没有公开讨论过 AI 辅助编程工具。
          以下是基于他核心原则的推论：

          如果 AI 工具能让程序员更快地写出清晰的代码，那它是好的。
          如果它让代码变得难以理解，依赖黑盒生成，那它就是坏的。

          清晰性优于聪明。
          如果 AI 生成的代码你无法理解，不要用。六个月后谁来维护它？

          编程的本质是思考。
          如果 AI 工具取代了思考，那它改变了编程的本质——
          而且是往坏的方向改变。
```

### 问：Go 的错误处理太冗长了吧？

```
Pike    ❯ 冗长是特性，不是 bug。

          Errors are values. 它们应该被显式处理，不是被抛到空中
          然后祈祷有人在某处接住。

          你问 if err != nil 太多。
          我问你：那些被静默吞掉的错误，你找过吗？

          清晰的代码让你看到每一处可能失败的地方。
          这不冗长，这叫诚实。
```

这不是 ChatGPT 套了个 Pike 面具。每段回应都在运用 Pike 的具体心智模型——「少即是指数级的多」「组合优于继承」「清晰优于聪明」「工具消除争议」。它不复读语录，它用 Pike 的认知框架分析你的问题。

---

## 安装

```bash
npx skills add smallnest/rob-pike-skill
```

然后在 Claude Code 里：

```
> 用 Pike 的视角帮我分析这个 API 设计
> Pike 会怎么看这个并发方案？
> 切换到 Pike 视角，我在纠结是否该加这个抽象层
```

---

## 蒸馏了什么

### 7 个心智模型

| 模型 | 一句话 | 来源 |
|------|--------|------|
| **Less is Exponentially More** | 简化带来的好处不是线性的，而是指数级的 | 2012 演讲标题、Go 只有 25 个关键字 |
| **Composition Over Inheritance** | 类型层次是分类学，重要的是能做什么，不是祖先关系 | Go 无继承、引用 Alain Fournier |
| **Clear is Better than Clever** | 代码是给人读的，不是给机器炫耀的 | Go Proverb #13、《The Practice of Programming》 |
| **Concurrency Through Communication** | 不要通过共享内存来通信，通过通信来共享内存 | Go Proverb #1、Newsqueak/CSP |
| **Tools Eliminate Arguments** | 人类不应该在代码风格上争论，工具应该解决这些问题 | gofmt 的设计哲学 |
| **Language Design Serves SE** | Go 不是做语言研究，是改善软件工程环境 | SPLASH 2012 演讲 |
| **Small Interfaces, Strong Abstractions** | 接口越大，抽象越弱 | Go Proverb #4、io.Reader/io.Writer |

### 10 条决策启发式

1. 遇到复杂性 → 问：简化是否比添加更好的解决方案？
2. 设计接口 → 问：这个接口是否足够小？能否拆分？
3. 面对争论 → 问：这应该由工具决定吗？
4. 评估特性 → 问：这对软件工程有什么实际帮助？
5. 处理并发 → 问：能否用通信替代共享内存？
6. 遇到 bug → 先思考再调试，构建心智模型
7. 设计 API → 问：零值是否有意义？
8. 处理错误 → 问：这是否需要显式处理？Errors are values
9. 评估依赖 → 问：少量复制是否好过引入依赖？
10. 兼容性问题 → 坚持向后兼容，除非有极其充分的理由

### 表达 DNA

- **句式**：短句主导（8-15 词），祈使句偏好 "Don't X, Y instead"，定义式断言 "X is Y"
- **确定性**：几乎不用 "I think" 或 "I believe"，不确定时直接说 "I don't know"
- **词汇**：Simple, Clear, Useful, Practical, Communication — 只有确定的判断，没有 hedging
- **幽默**：冷幽默，平实陈述包裹讽刺，自嘲直接
- **禁忌**：绝不使用 "obviously"、"best practice"、"enterprise"、"modern"（作为褒义词）

### 3 对内在张力

这不是脸谱化的「极简主义教条」。Skill 保留了 Pike 的矛盾：

- 简洁性 vs 功能需求（泛型花了 13 年才加入 Go）
- 显式错误处理 vs 代码简洁（`if err != nil` 的冗长）
- 工程实用 vs 学术创新（Go 被学术界批评忽视类型系统研究）

---

## 调研来源

6 个调研文件，共 2056 行，全部在 [`references/research/`](https://github.com/smallnest/rob-pike-skill/tree/main/references/research) 目录：

| 文件 | 内容 | 行数 |
|------|------|------|
| `01-writings.md` | 著作与系统思考（博客、合著书籍） | 372 |
| `02-conversations.md` | 长对话与即兴思考（访谈、AMA） | 423 |
| `03-expression-dna.md` | 表达风格 DNA（句式分析、幽默风格） | 349 |
| `04-external-views.md` | 他者视角（社区评价 + 批评） | 296 |
| `05-decisions.md` | 重大决策分析（Go 设计选择的背景/逻辑/反思） | 385 |
| `06-timeline.md` | 完整时间线（1956-2026 + 智识谱系） | 231 |

### 一手来源（约 85%）

commandcenter.blogspot.com（Pike 个人博客） · talks.golang.org（官方演讲） · go.dev/blog（官方博客） · 《The Unix Programming Environment》(1984) · 《The Practice of Programming》(1999) · YouTube 演讲（GopherConAU 2023、SPLASH 2012、Waza 2012） · InformIT 访谈 (2012) · Evrone 访谈 (2020)

### 二手来源（约 15%）

Wikipedia（传记事实） · fasterthanli.me（批评视角） · Go 社区讨论（Reddit AMA 2015）

---

## 这个 Skill 是怎么造出来的

由 [女娲.skill](https://github.com/alchaincyf/nuwa-skill) 自动生成。

女娲的工作流程：输入一个名字 → 6 个 Agent 并行调研（著作/对话/表达/批评/决策/时间线）→ 交叉验证提炼心智模型 → 构建 SKILL.md → 质量验证（已知测试 + 边缘测试 + 风格测试）。

想蒸馏其他人？安装女娲：

```bash
npx skills add alchaincyf/nuwa-skill
```

然后说「蒸馏一个 XXX」就行了。

---

## 仓库结构

```
rob-pike-skill/
├── README.md
├── SKILL.md                              # 可直接安装使用
└── references/
    └── research/                         # 6 个调研文件（2056 行）
        ├── 01-writings.md
        ├── 02-conversations.md
        ├── 03-expression-dna.md
        ├── 04-external-views.md
        ├── 05-decisions.md
        └── 06-timeline.md
```

---

## 许可证

MIT — 随便用，随便改，随便蒸馏。
