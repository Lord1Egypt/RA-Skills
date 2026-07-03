# ZCodeProject — sess_011aad62 归档
> 最后更新: 2026-06-22

## 压缩上下文
本轮围绕 AGENTS.md 行为准则的自进化回测与强化。
1. 首轮回测：从 AI 自身执行视角发现 4 类结构性弱点（缺反思触发器、错误未闭环、盲区无治理、冲突无仲裁），落地 5 项强化（reflection 节、回写闭环、harness状态、前提清单、冲突仲裁），89 行。
2. token 暴涨归因：6/21 jsonl 10.97MB（6/20 的 3 倍）。首次归因误判为重试风暴（P0-换路失效），被用户质疑后重算——重试仅占增量 5.6%，真凶是长会话 context 平方级累积（813/839/786 请求的超长会话）。
3. 规则迭代：初版 P0-长会话压缩 阈值 200/2h，回测模拟只省 34%；改为周期性压缩（每 100 次/1h），省 81%，增幅从 499% 降至 16%。
4. 最终精炼：AGENTS.md 91 行 2868 字符，12 条规则 ID 全保留，只压缩解释性文字。

## 完整文件清单
- AGENTS.md — 新增 reflection 节、4 条规则（P0-回写闭环/P1-harness状态/P0-会话节流/P0-长会话压缩）、research 前提清单、decision 冲突仲裁；全文精炼
- .agents/skills/summarize/harvests/ZCodeProject/sess_011aad62.md — 本归档（新建）
- .agents/skills/summarize/harvests/error-ledger.md — 更新 token 暴涨根因统计
- .agents/skills/summarize/harvests/index.md — 新增 sess_011aad62 索引
- .agents/skills/summarize/harvests/_self-stats.md — 更新运行统计

## 完整错误列表
- 归因误判：首次将 token 暴涨归因为 P0-换路 失效+重试风暴，被用户质疑后重算发现重试仅占 5.6%。分类=ASSU（基于"27次重试"表面现象假设根因，未算占比）。避免规则=P0-验证后引用（数据先算占比再下结论）
- 规则设计偏差：初版 P0-长会话压缩 阈值 200/2h 单次压缩，回测只省 34%，改为周期性压缩省 81%。分类=KNOW（未理解 context 平方增长机制）。避免规则=P0-换路（方案效果不达标即换设计）

## 技能调用详情
- summarize ×1 (本轮): 压缩长会话，净省 token（本轮会话约 30 轮）
