# Zeelin Auto Evolution - 使用示例

## 示例 1：无感记录用户纠错

### 背景
用户在开发流程中反复指出 AI 忘记同步更新设计稿，希望系统自动把这类错误沉淀下来。

### 输入
```text
你又忘了同步更新设计稿，不是让你只改代码和 Spec。
```

### 执行过程
1. `detect_feedback_signal.py` 命中“你又忘了”“不是让你”。
2. 主 Agent 正常完成当下任务。
3. 主 Agent 在收尾时派发 `feedback-observer`。
4. observer 将该问题归档为“UI 变更未同步设计稿”。
5. feedback 写入 `.claude/feedback/ui-design-sync.md`，并更新索引。

### 输出
```text
记录了 1 条 feedback：UI 变更未同步设计稿（ui-design-sync.md）
```

## 示例 2：规则毕业提议

### 背景
同一类 feedback 已经累计 3 次，系统在 session 启动时扫描到毕业信号。

### 输入
```text
检查一下有没有该升级的规则
```

### 执行过程
1. `evolution_runner.py` 扫描 `.claude/feedback/`。
2. 发现 `ui-design-sync.md` 的 `occurrences = 3` 且 `graduated = false`。
3. 判断该规则应归属于设计相关 Skill 或全局流程。
4. 生成“建议写入正式规则”的提议。

### 输出
```markdown
**规则毕业**（1 条）
1. UI 变更后必须同步更新设计稿：出现 3 次
   建议写入：CLAUDE.md 的 [总体规则]
   内容摘要：任何 UI 变更都要同步更新设计稿、Spec 与代码
   操作：确认 / 跳过
```

## 示例 3：Skill 优化提议

### 背景
`design-maker` 连续几次只完成主页面，没有覆盖弹窗、空状态和错误态，覆盖度长期偏低。

### 输入
```text
检查哪些 skill 该优化
```

### 执行过程
1. 扫描脚本汇总 `source_skill = design-maker` 的评分。
2. 发现 `coverage` 最近 5 次平均分小于等于 3。
3. 汇总证据：经常漏中间态、确认框、错误提示。
4. 生成优化建议，要求补齐流程枚举步骤。

### 输出
```markdown
**Skill 优化**（1 条）
1. design-maker：coverage 最近 5 次平均 2.4
   优化建议：在设计规划阶段加入“沿用户流程枚举所有中间页面和状态”的步骤
   操作：确认 / 跳过
```

## 示例 4：新 Skill 提议

### 背景
用户反复要求 AI 整理发版说明、提取改动摘要、输出渠道文案，但现有 Skill 没有稳定覆盖。

### 输入
```text
这种需求是不是该单独做成新 skill
```

### 执行过程
1. 系统扫描到某类“发版说明整合” feedback 已累计 5 次以上。
2. 检查现有 Skill 列表，没有直接覆盖该模式。
3. 判断该模式有稳定输入、稳定输出、独立方法论。
4. 输出“创建新 Skill”的提议。

### 输出
```markdown
**新 Skill 提议**（1 条）
1. 发版说明整合与校对：出现 5 次
   建议：创建 release-note-builder Skill
   操作：确认创建 / 跳过
```
