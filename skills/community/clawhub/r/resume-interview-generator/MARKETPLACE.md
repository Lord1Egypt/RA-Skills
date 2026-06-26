# resume-interview-generator Marketplace Copy

## Title

resume-interview-generator

## Short Description

根据候选人简历和岗位要求，快速生成结构化面试题、追问路径、评分标准和风险验证点。

## Description Variants

### 50-char Version

根据简历生成结构化面试题、追问路径和评分标准。

### 120-char Version

根据候选人简历和岗位要求，自动生成面试题、笔试题、追问路径、评分标准和风险验证点，帮助面试官更快完成评估准备。

### 300-char Version

`resume-interview-generator` 面向技术面试官、招聘负责人和技术主管。它会先解析候选人简历中的技术栈、项目经历、亮点与风险点，再结合岗位方向、级别和面试类型，输出结构化面试题或笔试题，并附带追问路径、参考答案、评分标准和风险验证点，帮助团队更高效、更一致地完成候选人评估。

## Medium Description

`resume-interview-generator` 面向技术面试官、招聘负责人和技术主管。  
它会先解析候选人简历中的技术栈、项目经历、亮点和风险点，再结合岗位方向与级别，生成更贴合真实经历的面试题或笔试题。

输出不只是题目，还包括：

- 候选人画像摘要
- 项目深挖问题
- 基础能力问题
- 场景设计题
- 代码能力题
- 追问路径
- 参考答案
- 评分标准
- 风险验证点

适合这些场景：

- 技术面试前快速备题
- 招聘流程中做简历真实性验证
- 给候选人生成一套结构化笔试题
- 让不同面试官使用更一致的评估标准

## Long Description

`resume-interview-generator` 的目标不是生成一套泛泛的八股题，而是基于候选人简历中真实出现的技术经历、项目细节和岗位上下文，帮助面试官更快进入有效评估。

它会优先完成三件事：

1. 解析简历，提炼技术栈、项目复杂度、亮点与可疑表述  
2. 根据岗位方向、目标级别和面试类型生成结构化题目  
3. 为每道题补齐追问方向、参考答案、评分标准和风险回答信号

它特别适合以下角色：

- 技术面试官：快速准备一轮技术面
- 招聘负责人：统一团队面试题风格和评分标准
- 技术主管：围绕候选人项目真实性做深挖验证
- 用人经理：生成更贴近岗位的笔试题或综合评估材料

支持的典型输出模式：

- 面试题模式
- 笔试题模式
- 综合评估模式
- 极简模式
- 深挖模式

默认更适合技术岗位，尤其是：

- Java 后端
- 大数据开发
- 搜索 / 推荐
- AI 工程
- DevOps / 云原生

隐私处理约束：

- 默认忽略候选人姓名、电话、邮箱等敏感信息
- 输出中不重复展示联系方式
- 重点聚焦技术经历、项目内容、岗位匹配度和风险验证点

## Use Cases

- 根据一份高级 Java 后端简历，生成 50 分钟技术面试题
- 根据候选人经历，生成一套大数据开发笔试题
- 对一份“包装感较强”的简历做项目真实性深挖
- 为技术主管面准备带评分标准的候选人评估包

## Verify Prompt

```text
$resume-interview-generator 请根据这份候选人简历，为高级 Java 后端岗位生成一套 50 分钟技术面试题，包含项目深挖、基础能力、代码能力、追问路径和评分标准
```

## Suggested Tags

- interview
- hiring
- resume
- recruiting
- technical-interview
- evaluation

## Suggested Screenshots / Demos

- 一张“候选人画像摘要”输出截图
- 一张“结构化面试题 + 评分标准”输出截图
- 一张“深挖模式”输出截图

## OpenClaw Install

```bash
openclaw skills install resume-interview-generator
```

## Skills Hub Install

```bash
npx @skills-hub-ai/cli install resume-interview-generator
```
