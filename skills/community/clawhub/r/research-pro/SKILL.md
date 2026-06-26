---
name: research-pro
version: 1.0.0
description: 科研专项工作流 - 参考 AutoResearchClaw 23阶段全流程，从想法到论文。覆盖文献调研、实验设计、代码实现、统计分析、论文写作。
keywords: [科研,研究,论文,Research,自动化科研,文献综述,实验]
---

# Research Pro - 科研专项工作流
参考 AutoResearchClaw 思路的完整科研流程

---

## 核心思想

**像 AutoResearchClaw 一样做科研：**
1. 想法 → 文献调研
2. 实验设计 → 沙盒执行
3. 统计分析 → 同行评审
4. LaTeX 论文输出

---

## 触发词

`科研模式` / `research pro` / `做研究中` / `论文模式`

---

## 完整工作流（23阶段）

### Phase 1: 想法生成 🎯

```
## 🎯 想法定义

### 研究問題
[你想研究什么问题]

### 核心创新点
1. [创新点1]
2. [创新点2]

### 预期贡献
[发表后的贡献]
```

---

### Phase 2: 文献调研 📚

```
## 📚 文献调研

### 相关工作
| 论文 | 方法 | 我们的区别 |
|------|------|-----------|
| [Paper A] | [方法A] | [改进点] |
| [Paper B] | [方法B] | [改进点] |

### 数据来源
- [x] OpenAlex
- [x] Semantic Scholar
- [x] arXiv

### 引用要求
- 真实引用（非幻觉）
- 近3年顶会优先
```

---

### Phase 3: 实验设计 🧪

```
## 🧪 实验设计

### 对比基线
1. [基线方法1]
2. [基线方法2]

### 实验配置
- 数据集：[数据集名]
- 评估指标：[指标]
- 硬件：[GPU/CPU]

### 假设检验
- H0: [原假设]
- H1: [备择假设]
```

---

### Phase 4: 代码实现 💻

（引用 code-pro skill）

```
## 💻 实现

### 核心代码
```python
# 核心实现
```

### 依赖
- Python 3.x+
- [库1]
- [库2]
```

---

### Phase 5: 执行与调试 🔄

```
## 🔄 执行

### 环境检测
[GPU/CPU 检测结果]

### 运行结果
| 实验 | 结果 | 提升 |
|------|------|------|
| 基线A | 0.85 | - |
| 我们的 | 0.89 | +4.7% |

### 统计分析
- p-value: [值]
- 显著性: [是/否]
```

---

### Phase 6: 论文写作 📄

```
## 📄 论文结构

### Abstract
[150-300字摘要]

### Introduction
1. 问题定义
2. 相关工作
3. 我们的贡献

### Method
[方法描述]

### Experiments
[实验设置与结果]

### Conclusion
[结论与未来工作]

### 格式
- LaTeX (NeurIPS/ICML/ICLR)
- 双栏排版
```

---

## 多代理协作

| 角色 | 职责 |
|------|------|
| CodeAgent | 代码生成与调试 |
| BenchmarkAgent | 实验评估 |
| FigureAgent | 图表生成 |
| Reviewer | 同行评审 |

---

## 质量保证

### Anti-Hallucination
- ✅ 引用必须从真实数据库获取
- ✅ 实验结果必须可复现
- ✅ claim 需验证

### Human-in-the-Loop
- 关键节点可人工介入
- checkpoint 审核
- 批准后继续

---

## 输出格式

### 论文模板

```markdown
# Title

## Abstract
[150-300 words]

## 1. Introduction
[1-2 paragraphs]

## 2. Related Work
[2-3 paragraphs]

## 3. Method
[2-3 paragraphs]

## 4. Experiments
[2-3 paragraphs]

## 5. Conclusion
[1 paragraph]

## References
[真实引用]
```

---

## 快速指令表

| 需求 | 命令 |
|------|------|
| 开始新研究 | `科研模式：研究[想法]` |
| 文献调研 | `调研[主题]相关文献` |
| 设计实验 | `设计实验：目标[指标]` |
| 写论文 | `生成论文：LaTeX格式` |
| 审核 | `同行评审这个研究` |

---

## 组合使用

**完整流程示例：**
```
科研模式：研究"用大模��做代码bug自动修复"
→ 帮我设计对比实验
→ 生成ICML格式论文
```

---

*Research Pro | 参考 AutoResearchClaw 的全流程科研工具*