# 2026-03-10

- structured-memory 精度打磨继续推进：已补充幂等性检查。
- 继续收紧 summary 排序规则，避免补发/后续类过程句抢到摘要前排。
- 针对 summary 仍被元要求句抢占首位的问题，改为分层选句策略。
- 根因：昨天晨报发送失败，是因为 delivery channel context 丢失。
- UserA 明确纠正：信息不足时先查 memory，再决定是否回复不记得。
