# Output Template

Use this template when the user asks for one or more industry scans.

## Header

- 观察窗口: `YYYY-MM-DD to YYYY-MM-DD`
- 检索日期: `YYYY-MM-DD`
- 输出目标: `方案更新 / 行业简报 / 销售话术 / 高层汇报`

## Per-Industry Template

```markdown
## 行业：<行业名>

### 结论
用 2-4 句话说明这个行业在最近 30-60 天最值得关注的变化，以及旧方案哪里可能已经过时。

### 新趋势 / 新变化
| 日期 | 变化 | 影响判断 | 证据 |
| --- | --- | --- | --- |
| 2026-04-10 | <发生了什么> | <为什么重要> | [来源标题](https://example.com) |

### 新需求
- <客户开始更看重什么>
- <采购/落地要求发生了什么变化>

### 新模式
- <交付模式、定价模式、渠道模式、部署模式、生态合作模式等变化>

### 重点融资
- <公司名> - <日期 / 轮次 / 金额>
- 为什么重要: <这笔融资为什么会改变行业关注点、商业化速度、竞争格局或客户预期>

### 重点团队
- <团队或公司名>
- 窗口内动作: <发布 / 扩张 / 获客 / 合作 / 融资 / 招聘 / 生态动作>
- 为什么值得跟踪: <对方案、竞品、渠道、客户需求有什么影响>

### 对方案的影响
- <建议新增的能力点>
- <建议删除或弱化的旧说法>
- <建议补充的案例、指标、对比项>

### 方案更新建议
- <PPT/话术/报价/产品包应该怎么改>

### 来源
- [来源 1](https://example.com) - `YYYY-MM-DD`
- [来源 2](https://example.com) - `YYYY-MM-DD`
```

## Compression Rule

If the user asks for many industries at once:
- keep each industry to the highest-signal 3-5 changes
- prefer market and commercial implications over technical trivia
- keep only the single most valuable financing and 1-2 most important teams per industry unless the user asks for depth
- keep the `对方案的影响` and `方案更新建议` sections even when the rest is compressed

## Confidence Rule

When the signal is mixed or sparse, add:

```markdown
### 置信度
- 高 / 中 / 低
- 原因: <信号强弱、来源质量、是否存在相互矛盾的信息>
```
