# REFERENCE_ARCHITECTURE.md - 自动进化 Skill 架构参考

## 架构目标
这套 Skill 的目标不是“让 AI 自己学会一切”，而是建立一条安全、可解释、可审计的演化链路：

1. 先把真实使用中的负反馈和修正沉淀下来
2. 再从积累的数据里识别模式
3. 最后把模式转化为建议，由用户决定是否升级为正式规则

这样做的好处是，系统既能长期变强，又不会因为误判而偷偷污染规则系统。

## 四层进化模型

### 第一层：经验沉淀
目标：无感记录 feedback。

核心特征：
- 用户不需要额外下命令
- 主 Agent 正常完成当前任务后，再静默派发记录动作
- 优先记录“被纠正了什么”，而不是泛泛记录情绪

典型信号：
- “不是这样”
- “你又忘了”
- “不对”
- “我不是让你这么干”
- “你漏了”
- “为什么没做”

推荐实现：
- Hook 或脚本先做关键词级检测
- 命中后，派发 `feedback-observer`
- observer 结合上下文生成结构化 feedback
- feedback 存放在 `.claude/feedback/`

最小字段建议：

| 字段 | 说明 |
|---|---|
| `type` | 固定为 `feedback` |
| `description` | 一句话摘要 |
| `created` / `updated` | 创建和更新时间 |
| `occurrences` | 同类反馈累计次数 |
| `graduated` | 是否已毕业为正式规则 |
| `source_skill` | 来自哪个 Skill，没有则 `N/A` |
| `proposal_hint` | 可选分类提示：`auto`、`rule`、`optimize_skill`、`new_skill` |
| `scores` | 仅 Skill 执行后评估时填写 |

### 第二层：规则毕业
目标：把高频、稳定、足够清晰的 feedback 升级为正式规则。

建议阈值：
- 同主题反馈 `occurrences >= 3`
- `graduated == false`
- 未标记 `skipped == true`

毕业目标判断：
- 如果问题只影响某一个 Skill，则写入对应 Skill
- 如果问题跨多个 Skill 或属于全局工作方式，则写入 `CLAUDE.md`

关键约束：
- 只能“提议毕业”，不能直接毕业
- 必须让用户看到建议内容、目标文件和拟写入位置
- 用户确认后才允许修改规则文件

典型例子：
- “UI 变更后必须同步更新设计稿”
- “改需求时不能只改代码，必须同步改 Spec”
- “进入开发前先对照设计稿做页面清单”

### 第三层：Skill 优化
目标：发现一个 Skill 虽然存在，但持续表现不好，需要改方法论。

评分维度建议：

| 维度 | 含义 | 低分含义 |
|---|---|---|
| accuracy | 指引是否准确 | 经常做错方向 |
| coverage | 是否覆盖完整场景 | 经常漏步骤、漏状态、漏边界 |
| efficiency | 执行是否顺畅 | 反复来回、多轮补充 |
| satisfaction | 用户是否认可 | 经常要求重做 |

推荐触发条件，满足任一即可提议：
- 同一 Skill 连续 3 次同一维度 `<= 2`
- 最近 5 次平均分 `<= 3`
- 同一 Skill 相关 feedback 的 `occurrences` 合计 `>= 5`

建议输出内容：
- 低分维度
- 证据摘要
- 建议改动
- 可能要补的流程步骤

典型例子：
- design-maker 总漏掉弹窗、空状态、确认框
- dev-planner 只拆主流程，不拆异常流程
- code-review 总关注格式，不关注行为回归

### 第四层：新 Skill 提议
目标：发现系统能力边界外的新需求模式。

建议阈值：
- 某类操作模式 `occurrences >= 5`
- 现有 Skill 列表中找不到对应覆盖
- 该模式具有稳定输入、稳定输出或稳定工作流程

判断问题：
- 这是单次偶发需求，还是可复用模式？
- 现有 Skill 是不会做，还是做得不够好？
- 这个模式是否值得独立成 Skill，而不是补一条规则？

适合新建 Skill 的情况：
- 输入输出边界清晰
- 触发词稳定
- 复用概率高
- 有独立方法论或脚本需求

不适合新建 Skill 的情况：
- 只是某个现有 Skill 的一个边缘规则
- 需求过于一次性
- 其实只是执行质量差，不是覆盖缺失

## 角色分工建议

### 主 Agent
- 负责处理用户当前请求
- 在检测到 feedback 信号后，收尾时派发 `feedback-observer`
- 在 session 启动时或用户手动触发时，派发 `evolution-runner`
- 展示建议并收集用户确认
- 根据确认结果执行真正变更

### feedback-observer
- 专职做 feedback 分析与记录
- 不负责改规则
- 没有信号时返回“无新 feedback”

### evolution-runner
- 专职扫描 feedback 目录
- 识别毕业候选、低评分 Skill、新 Skill 候选
- 只输出建议，不执行修改

## 文件与流程映射
这份 Skill 参考了“产品经理技能包”中的以下机制，并做了抽象：

| 来源 | 作用 | 在本 Skill 中的落点 |
|---|---|---|
| `hooks/detect-feedback-signal.sh` | 识别用户修正信号 | `scripts/detect_feedback_signal.py` |
| `agents/feedback-observer.md` | 静默记录反馈 | `SKILL.md` 的第一、二步 |
| `skills/feedback-writer/SKILL.md` | 结构化写 feedback | 模板和字段规范 |
| `agents/evolution-runner.md` | 启动扫描器 | `SKILL.md` 的第三步 |
| `skills/evolution-engine/SKILL.md` | 生成进化建议 | `scripts/evolution_runner.py` |
| `EVOLUTION.md` | 四层概念框架 | 本参考文档整体 |

## 建议输出格式

```markdown
**进化建议**（共 3 条）

**规则毕业**（1 条）
1. UI 变更后必须同步更新设计稿：出现 3 次
   建议写入：design-maker/SKILL.md 的 [注意事项]
   内容摘要：所有 UI 变更都要同步更新设计稿与 Spec
   操作：确认 / 跳过

**Skill 优化**（1 条）
1. design-maker：coverage 最近 5 次平均 2.4
   建议：加入“沿用户流程枚举默认态、空状态、错误态、弹窗态”的步骤
   操作：确认 / 跳过

**新 Skill 提议**（1 条）
1. 发布说明整合与发版校对：出现 6 次
   建议：创建 release-note-builder Skill
   操作：确认创建 / 跳过
```

## 风险与边界
- 反馈信号检测只能作为入口提示，不能替代语义判断
- 毕业阈值不是绝对真理，项目可按噪音水平调整
- 低评分不一定意味着要新建 Skill，也可能只是现有 Skill 缺步骤
- 如果没有用户确认，任何规则文件都不应改动
- 若 feedback 来源不清晰，应先标为 `source_skill: N/A`，避免误毕业到错误位置
