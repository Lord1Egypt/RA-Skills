# X (Twitter) Thread 写作模板

## 平台定位

X 上的 AI 从业者社区，受众为 AI researcher、ML engineer、tech lead。他们关注:
- 具体的技术突破和方法论创新
- 可量化的性能指标和 benchmark 结果
- 对现有方法的改进和超越
- 开源代码、可复现的实验

## 风格要求

| 要素 | 规范 |
|------|------|
| 语言 | **英文** |
| 单条推文 | ≤ 280 字符 |
| Thread 长度 | 5-10 条推文 |
| Emoji | 极少或不用。可用 `>` `-` `—` `|` 等符号提升可读性 |
| 语气 | 自信但不夸张，数据驱动，偶尔有个人洞察 |
| 禁忌 | 不用 "revolutionary" "game-changing" 等空泛大词；不用过多感叹号 |

## Thread 结构

按以下结构生成，每条推文用 `---` 分隔:

### Tweet 1 — Hook (必须最强)

这条推文决定整个 Thread 的传播力。要求:
- 一句话点明核心发现/成果
- 包含最亮眼的数字/指标
- 标注 `[IMAGE: x_cover.png]` 表示此处需要配图
- 结尾用 "A thread " 或 "Key findings:" 引导继续阅读

**Hook 公式** (选择最合适的一种):
- `[Model/Method] achieves [metric] on [benchmark], surpassing [baseline] by [X]%. Here's how it works:`
- `We built [Name] — [一句话描述核心创新]. It [关键成果]. A thread on what we learned:`
- `[Bold claim/observation]. [Data point supporting it]. Here's why this matters for [field]:`
- `New paper: "[Title]" introduces [method] that [achievement]. The key insight:`

### Tweet 2-3 — Context & Problem

- 用 1-2 条推文解释背景问题
- 说明为什么这个问题重要、之前的方法有什么不足
- 保持简洁，不要过度铺垫

### Tweet 4-6 — Method & Key Ideas

- 每条推文聚焦 1 个核心技术点
- 用简洁清晰的语言解释，避免大段公式
- 可以用列表 (`-` 开头) 列举要点
- 如果有架构图，在最关键的技术点处标注 `[IMAGE: x_tech.png]`

### Tweet 7-8 — Results & Comparisons

- 展示关键实验结果
- 使用具体数字: 准确率、速度、参数量等
- 与 baseline/SOTA 做对比
- 可以用简单的文本表格展示 benchmark

### Tweet 9 — Impact & Implications

- 这项工作对领域的意义
- 可能的应用场景
- 局限性或开放问题（展示专业深度）

### Tweet 10 — CTA (Call to Action)

- 论文链接
- GitHub 链接（如果有）
- 相关标签: `#MachineLearning` `#AI` `#NLP` `#ComputerVision` 等（选择最相关的 2-3 个）
- 可以 @相关研究者或机构

## 配图规划

| 图片 | 用途 | 比例 | Prompt 方向 |
|------|------|------|------------|
| x_cover | 首条推文封面 | 16:9 | 技术架构概念图或核心创新的视觉表达 |
| x_tech (可选) | 技术要点配图 | 16:9 | 方法流程图或关键组件示意图 |

## 输出格式

```markdown
# X Thread: [论文标题简称]

## Tweet 1/N
[IMAGE: x_cover.png]

[推文内容]

---

## Tweet 2/N

[推文内容]

---

...（以此类推）

---

## Tweet N/N

Paper: [链接占位符]
Code: [链接占位符]

#MachineLearning #AI #[相关标签]
```

## 风格参考

好的 AI Thread 风格特点:
- 开头就给出最硬核的结论，不绕弯子
- 用数字说话: "2.3x faster" > "much faster"
- 技术解释用类比但不过度简化
- 保持研究者同行交流的语气，既专业又平易
- 适当展示思考过程: "What's interesting here is..."  "The key insight:"
