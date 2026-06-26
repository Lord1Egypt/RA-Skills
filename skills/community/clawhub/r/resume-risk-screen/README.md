# Resume Risk Screen

这是一个用于 OpenClaw 的简历风险初筛 Skill。

## 适用场景
适用于 HR 或技术面试团在初发阶段对候选人简历进行自动化筛查。主要用于：
- 批量初筛候选人简历
- 深度判断候选人真实性风险、包装风险及岗位匹配度
- 输出下一轮面试的追问建议

## 本地如何使用
将此 Skill 提供给 OpenClaw Agent。将候选人的简历文本（或 OCR 提取文本）、甚至相关公开信息链接作为上下文传入，Agent 将会自动按规程出具客观、直接的风险初筛报告。

## 如何发布到 ClawHub
当前可以通过 ClawHub CLI 将此 Skill 推送到注册表。
```bash
clawhub skill publish ./resume-risk-screen --slug resume-risk-screen --name "Resume Risk Screen" --version 0.1.0 --changelog "Initial release" --tags latest,recruiting,screening,hr,ai
```
