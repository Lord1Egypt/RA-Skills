# 拾光册：视频海报与记忆手帐 Skill

把视频链接或文件转成有来源证据、可编辑、可审稿的短视频海报，也可把关键帧和故事转成记忆手帐。当前能力版本为 `2.6.0`。

## 何时调用

适用于“视频绘卷”“短视频封面/电影感海报”“参考海报风格迁移”“海报中文标题排版”“关键帧元素提取”“记忆手帐”和“利用用户数据优化功能效果”。不适用于无来源约束的通用生图，也不复制参考海报的文字、人物或品牌内容。

## 输入与输出

- 必需输入：可解析的视频链接/文件，或用于手帐的关键帧；
- 可选输入：传播目标、参考海报与参考强度、渠道比例、必须说/不能说、手帐类型；
- 输出：来源台账、故事简报、概念竞赛、无字 key-art、安全/避让区、三套文字候选、用户选择、可编辑成品、审计与派生链；
- 失败输出：明确 blocker、已验证事实、真实降级路径和下一步，不返回“最高分的失败者”。

## 核心方法

视频海报采用“证据化故事 → 联合选帧 → 三概念竞赛 → 视觉命题双轴评选（VisualConcept）→ 逐帧元素提取与 AI 选片 → 只给 winner 生无字主视觉 → 同图三套文字骨架 → 用户选择并验签锁定 → 多渲染器审稿”。参考图只迁移可解释的版式、层级、字图关系、材料和色彩机制。本地视觉算法与源帧保底默认禁用，必须弹窗授权后才启用。详细规则见 [SKILL.md](SKILL.md)。

## 验证

在拾光册仓库根目录运行：

```bash
python skills/shiguang-memory-journal/scripts/validate_typography_plan.py --self-test
python skills/shiguang-memory-journal/scripts/validate_typography_plan.py skills/shiguang-memory-journal/references/typography-plan.example.json
pnpm font:audit
pnpm poster:render-consistency
pnpm poster:portable-html-audit
pnpm test
```

`test-prompts.json` 是独立 Agent forward-test 的声明式对抗集；它本身不是自动执行器。仓库中的单元、UI、像素和字体脚本覆盖其中的确定性硬门，传播性仍需真实用户 A/B 与人工盲评。

## 失败与复用

本地/CLI 不可用时按能力域降级：视觉与图片任务只降级到实际收到像素的视觉/图片 API，纯文本任务可降级到文本 API；所有模型调用统一走 `ModelGateway` 能力信封。字体未覆盖、语义安全区耗尽、参考内容泄漏、用户候选锁验签失败或跨渲染漂移都会关闭发布门；可修复失败先按 `EvaluationGate.repairPlan` 局部修复。数据契约可复用于视频缩略图、文旅海报、节目卡、活动 KV、产品解释图和手帐封面。

版本演进与兼容策略见 [视频海报工作流](references/video-poster-workflow.md#version-evolution)。许可证见 [LICENSE](LICENSE)。
