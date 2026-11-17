# 推荐的内部生态证据模块

服务第三项“技能/插件推荐操作”，不提供独立总管入口。

## 评分

`value_score = usage * 0.40 + alignment * 0.25 + health * 0.20 + market * 0.15`。
这是解释性启发式，不是市场验证的客观价值尺度。只在四项数据全部可用时输出综合分。
缺值使用 null/unavailable，value_score=null、layer=pending_evidence，显示“补充证据，暂不变更”；不进入高价值排行。

- usage：可归因调用次数归一化；未收集不等于零。零需要 status=observed、coverage_complete=true。
- alignment：真实用户/项目画像匹配，附规则与来源。MCP 不得用 health*0.5 替代。
- health：静态健康分与实际运行分开，启动未经验证就是 unavailable。
- market：30 天内带来源 URL、许可证、checked_at、scoring_basis 的证据。日期、格式、范围无效均不可用，Stars 不单独决定分数。

## 建议门禁

完整分数≥7为 keep，4–7为 watch；低分只表示复查价值。
hide/uninstall_candidate 还必须有明确零调用、完整采集覆盖、dependency_review_complete=true；hide 另需 ui_visible=true。任一缺口退回 watch，不操作文件。
未装或缺本地数据的市场候选可以作“考虑引入”的定性比较，不可伪造 usage 来凑综合分。
安全/解析问题不依赖完整价值分，仍独立产生有证据的 P0/P1 修复建议。

## 数据与输出

scripts/compute_value_scores.py 是计算入口；audit_skill_plugin_issues.py 通过 --signals-path 和 --market-path 接收输入。
报告包含 breakdown、missing_evidence、evidence_coverage、action_plan。健康、画像、使用、市场、上下文分开。
信号采集器支持多个客户端，但不保证嵌套工具与隐式技能的完整归因，采集日志需显示真实覆盖。

组合建议只能说“能力互补”或给出实际共现记录；没有对照实验不写 ROI、节省 token 或协同倍数。
