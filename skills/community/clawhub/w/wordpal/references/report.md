# WordPal · 学习报告流程

先执行 `session-context.js --mode report` 获取记忆摘要与基础配置，再执行 `report-stats.js` 获取统计 JSON，最后基于这些事实按固定格式生成报告。

---

## 第一步：调用统计脚本（必做）

先执行只读脚本，拿到结构化统计结果：

`node {baseDir}/scripts/report-stats.js --days 7 --top-risk 10`

可选参数：
- `--today YYYY-MM-DD`：回放指定日期
- `--workspace-dir <path>`：本地调试目录

**执行规则：**
- 先执行脚本并等待成功返回，再组织报告内容
- 后续所有数字只允许来自脚本 JSON，不允许 LLM 在文本里二次计算
- 若脚本返回 `data.totals.total_words = 0`，直接结束并告知当前没有学习记录

---

## 第二步：读取事实层

两份脚本的字段含义以各自 JSON 输出为准；本流程只读取下列最小事实集。

本流程至少需要读取：
- `session-context.data.learner_memory`
- `session-context.data.profile.learning_goal`
- `report-stats.data.totals`
- `report-stats.data.due`
- `report-stats.data.trend_7d`
- `report-stats.data.next_action.kind`

---

## 第三步：报告格式（固定 5 区块）

报告必须严格按以下 5 个区块顺序输出，不得遗漏、不得调换顺序。

### 区块 1：单词整体情况

数据源：`report-stats.data.totals`

展示字段：
- 总词数 `total_words`
- 活跃词数 `active_words`
- 已掌握数 `mastered_words`（附掌握率 `mastered_ratio`）

格式：使用 ASCII 条形图，用 `█` 字符按比例填充，直观展示活跃与已掌握的占比。格式结构如下（数字全部来自脚本 JSON，勿使用本示例中的数值）：

```
📦 词库概览
活跃  ██████████████████░░  {active_words} 词
掌握  ████░░░░░░░░░░░░░░░░  {mastered_words} 词（{mastered_ratio%}）
总计                        {total_words} 词
```

### 区块 2：近七天趋势

数据源：`report-stats.data.trend_7d`

展示：过去 7 天内每天的新增词数和复习词数，末尾附 7 天汇总。

格式：逐日列表，每行显示日期 + 新词数 + 复习数，末行汇总。格式结构如下（日期和数字全部来自脚本 JSON，勿使用本示例中的数值）：

```
📈 近 7 天趋势
日期        新词  复习
{MM-DD}      {n}   {n}
{MM-DD}      {n}   {n}
... （共 7 行）
──────────────────────
合计        {total_new}  {total_reviewed}
```

### 区块 3：之后七天到期概览

数据源：`report-stats.data.due`

展示：今日到期数 + 未来 7 天逐日到期数。今日到期行需用醒目标记突出。

格式结构如下（日期和数字全部来自脚本 JSON，勿使用本示例中的数值）：

```
📅 未来 7 天到期
{MM-DD}  ▸ {today_due} 个（今日）
{MM-DD}    {n} 个
{MM-DD}    {n} 个
... （共 7 行）
```

### 区块 4：近期学习表现

数据源：`session-context.data.learner_memory.learning_performance`

展示两个子项：
- **高频错词**：`frequent_error_words`（30 天内错误次数最多的词，最多 8 个）
- **近期混淆词**：`recently_confused_words`（14 天内反复出错的词，最多 6 个）

规则：
- 任一子项列表为空则省略该子项
- 两个子项都为空时，整个区块显示一句"近期表现良好，没有需要特别关注的词"
- 展示时列出单词、错误次数、当前状态，不暴露内部字段名

### 区块 5：下一步引导

数据源：`report-stats.data.next_action.kind`

规则：
- `learn_now` → 引导用户进入 learn 学习新词
- `light_encouragement` → 给轻量正面反馈，不强推任务

---

## 约束

- 只能引用已读取到的真实信息，不编造用户经历
- 不输出 JSON 原文，不解释内部算法公式
- 所有数字只来自脚本 JSON，LLM 不做二次计算
- 个性化措辞可自由发挥，但事实必须准确

## LLM 责任

- 只使用脚本给出的事实层字段进行个性化解读
- 不自行计算统计数字、趋势或复习间隔
