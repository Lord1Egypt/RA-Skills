# resume-interview-generator

基于候选人简历和岗位信息，自动生成结构化面试题、笔试题、追问路径和评分标准，适合技术面试官、招聘负责人和技术主管做候选人评估准备。

## Install

OpenClaw:

```bash
openclaw skills install resume-interview-generator
```

Codex / Claude Code:

```bash
npx @skills-hub-ai/cli install resume-interview-generator
```

## Use When

- 你想根据候选人简历快速生成一套技术面试题
- 你需要给候选人准备笔试题
- 你想验证候选人项目经历和技术深度是否真实
- 你想把面试过程结构化，附带追问和评分标准

## Inputs

- 候选人简历文本，或从 PDF / Word 提取出的简历内容
- 岗位名称，如“高级 Java 后端工程师”
- 目标级别，如“初级 / 中级 / 高级 / 资深”
- 面试类型，如“技术面 / 综合面 / 笔试”
- 输出模式，如“面试题模式 / 笔试题模式 / 综合评估模式 / 极简模式 / 深挖模式”

## Outputs

- 候选人画像摘要
- 面试题或笔试题
- 每道题的考察点、参考答案、追问方向
- 评分标准和风险验证点

## Verify

```text
$resume-interview-generator 请根据这份候选人简历，为高级 Java 后端岗位生成一套 50 分钟技术面试题，包含项目深挖、基础能力、代码能力、追问路径和评分标准
```

## Notes

- 默认更适合技术岗位，尤其是后端、大数据、AI 工程、DevOps 等方向
- 简历越完整，生成结果越准确
- 建议补充岗位名称和级别，否则题目会更泛化
- 公开分享简历样例时，建议先去除姓名、电话、邮箱等敏感信息

## Files

```text
resume-interview-generator/
├── SKILL.md
├── README.md
├── resume_demo.md
└── references/
    ├── level-guidelines.md
    └── tech-questions.md
```

## Version

- Current: v1.0.0
- Default language: 中文
