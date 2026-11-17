---
name: self-reflection-loop
description: |
  自我反思闭环引擎（超越性元能力）。实现 Reflexion 式「生成→评估→精炼」闭环：对产物做结构化自评 +
  工具锚定校验（代码编译/字数/关键词/正则），输出分数、缺口与整改清单，并把教训回灌下一轮生成，直到达标或达上限。
  当用户/agent 需要「自我纠错」「迭代精炼」「代码自验证」「质量门禁」时调用。
agent_created: true
visibility: "public"
---

# 自我反思闭环引擎（self-reflection-loop）

让 agent 像专家一样「退后一步审查自己的产出」。核心：把「一次性生成」变成「生成—批评—修正—再生成」的闭环，
且**教训必须回灌下一轮**（Reflexion 的关键），避免重试却重复同一错误。

## 能力依据（主流研究）
- **Reflexion (Shinn 2023, NeurIPS)**：Actor→Evaluator→Self-Reflection；失败教训以自然语言存记忆并拼回下一轮提示词，
  以 verbal reinforcement 替代梯度更新，HumanEval pass@1 从 48%→91%。
- **Self-Refine (Madaan 2023)**：生成→自批评→精炼，迭代提升。
- **PRM (Process Reward Model)**：对每一步打分，早期错误检测、引导搜索（而非只在终点判对错）。
- **工具锚定验证**：代码用 py_compile/单测、事实用检索、计算用执行——比纯自省更可靠。
- **停止准则**：基于质量阈值/分数，而非固定迭代次数。

## 标准工作流
```bash
# 1. 初始化一个 rubric（预设：generic / code / text）
python scripts/reflector.py init --out rubric.json --preset code
# 2. 对产物做结构化自评 + 工具校验，产出报告（含缺口与整改清单）
python scripts/reflector.py assess my_script.py --rubric rubric.json --out report.md
# 3. 闭环：评估→（refine 整改）→再评估，直到综合分≥阈值或达迭代上限
python scripts/reflector.py loop my_script.py --rubric rubric.json --max 3 --threshold 0.8 \
  --refine-cmd "python refine.py {artifact} --gaps '{gaps}' > {artifact}.v2 && echo {artifact}.v2"
# 4. 复盘历史，沉淀反复出现的失败模式
python scripts/reflector.py log reflect_log.json
```

## 设计要点
- **确定性测量**：rubric 可扩展、可复跑，每轮分数可比，收敛过程可观测。
- **工具锚定**：代码类产物真实 `py_compile`，避免「自认正确」的幻觉式自评。
- **回灌闭环**：`loop` 把缺口文本喂给 refine 命令产出下一版，再评估——形成真正的自动闭环。
- **阈值停止**：达标即停，节省算力；不达标给出明确整改清单供人工或自动续做。

## 质量门禁
- [ ] 是否先有 rubric（明确维度 + 权重 + 检查类型），而非空泛「找问题」
- [ ] 是否用工具锚定验证（代码编译/执行）而非只靠语言自省
- [ ] 失败教训是否真正回灌下一轮（避免重复同一错误）
- [ ] 是否设置了收敛阈值，避免无限迭代

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）
```bash
python scripts/learner.py record <本技能目录> --capability 自我反思
python scripts/learner.py record <本技能目录> --capability 自我反思 --fail --error rubric缺失 --note "未先 init rubric"
python scripts/learner.py insight <本技能目录>
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
