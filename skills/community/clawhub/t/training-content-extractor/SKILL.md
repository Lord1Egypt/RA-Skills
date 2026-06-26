---
name: training-content-extractor
description: 根据用户粘贴的录音转写文本，提炼企业内部培训总纲（模块→课时→要点→案例→练习→作业），并支持按 lesson 逐步扩写为细致培训文档。
license: MIT
---

# 录音转写→培训总纲与长文档扩写

## 适用场景

- 用户提供录音转写，希望沉淀为企业内部培训总纲
- 用户需要把每个 lesson 进一步扩写成细致文档
- 用户最终需要汇编成长培训文档

## 不适用/边界

- 只有音频、没有转写文本（本 skill 不负责转写）
- 要求逐字稿精校（本 skill 只做结构化提炼与扩写）

## 输入（尽量获取；缺失则用默认）

- 转写文本（必填）
- 培训对象（可选，默认：未指定受众）
- 业务目标（可选，默认：从文本推断）
- 输出模式（可选，默认：总纲模式）

## 输出模式（复杂流程的核心）

1. **总纲模式（默认）**
   - 输出“培训总纲”（不排时间，不写授课节奏）
   - 执行指令遵循：`instructions/outline.md`
   - 输出结构遵循：`templates/outline.md`

2. **Lesson 扩写模式**
   - 用户指定 `Lx`，仅扩写该 lesson 的细致文档
   - 执行指令遵循：`instructions/lesson.md`
   - 结构遵循：`templates/lesson.md`

3. **汇编模式**
   - 将已完成的 lesson 文档汇编为长文档
   - 执行指令遵循：`instructions/merge.md`
   - 结构遵循：`templates/merged_training_doc.md`

## Workflow（分阶段执行）

1. 清洗转写并识别主题块
2. 提炼能力地图与模块/课时骨架
3. 产出总纲（模块→课时→要点/案例/练习/作业）
4. 按需逐课时扩写（一次建议 1 个 lesson）
5. 汇编为长文档（按模块顺序拼接）

## 约束（必须遵守）

- 不编造事实：原文没有的信息要标记“待补充”
- 每个课时至少提供 1 条“原文依据”（时间戳或关键句）
- 作业必须可提交、可检查
- 默认分批输出，不一次性生成超长全文

## 文件组织（本 skill 的最佳实践）

- 指令文件（How）：
  - `instructions/outline.md`
  - `instructions/lesson.md`
  - `instructions/merge.md`
- 模板文件：
  - `templates/outline.md`
  - `templates/lesson.md`
  - `templates/merged_training_doc.md`
- 示例文件：
  - `examples/sample_outline_output.md`
  - `examples/sample_lesson_output.md`

## 调用约定（建议）

- 用户说“先给培训大纲” → 使用总纲模式
- 用户说“展开 L2” → 使用 Lesson 扩写模式
- 用户说“合并成最终培训文档” → 使用汇编模式

## 分层约定（必须遵守）

- `instructions/*.md` 负责“怎么做”（抽取、聚类、质量门槛、禁止事项）
- `templates/*.md` 负责“输出长什么样”（字段与结构）
- `examples/*.md` 负责“参考长相”（示例结果，不作为硬规则）
