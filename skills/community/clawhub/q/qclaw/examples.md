# Examples

## Example 1: Project group digest

### Input (anonymized)
[2026-03-10 09:23] 张三: 今天下午3点开需求评审会
[2026-03-10 10:12] 王五: 昨天说的API文档谁负责?
[2026-03-10 10:15] 张三: 赵六在写,今晚给你
[2026-03-10 11:30] 赵六: 文档写完了,但测试环境还没好
[2026-03-10 14:50] 运维: 测试环境配置有问题,明天才能好
[2026-03-10 15:00] 张三: 那会议推迟到明天下午3点

### Output
## Executive Summary
需求评审会因测试环境问题推迟。API文档已完成，但环境阻塞未解决。

## Decisions
- 评审会改到明天下午3点

## Action Items
- [ ] 修复测试环境配置
- [ ] 交付 API 文档

## Risks
- 测试环境问题可能影响后续进度

## Example 2: Keyword tracking

### Input
Tracked keywords:
- Project A
- Client B
- payment
- deadline

### Output
Return:
- keyword hit
- short context
- urgency level
- whether follow-up is needed
