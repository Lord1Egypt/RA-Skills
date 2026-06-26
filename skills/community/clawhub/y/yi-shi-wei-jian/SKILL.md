---
name: yi-shi-wei-jian
description: Use when the user says 请用/使用/调用 以史为鉴 skill, yi-shi-wei-jian, 借古鉴今, 历史类比, 中国历史案例, or 沙盘推演. Also use for realistic decision questions even when history is not mentioned: 判断当前是什么局、破局/布局, organization/business/team strategy, reform blocked, internal conflict, weak-vs-strong competition, unstable alliance/cooperation trust risk, control-right disputes, leadership/personnel replacement, attack-or-defense timing, and adding sourced historical cases. Output 【局面判断】【历史参照】【关键变量】【可选路径】【沙盘推演】【借鉴原则】【边界提醒】.
homepage: https://github.com/GreatXiaoRY/LearnFromHistory-skill
user-invocable: true
metadata: {"display_name":"以史为鉴","repo_name":"LearnFromHistory-skill","slug":"yi-shi-wei-jian","language":"zh-CN","version":"0.1.4","tags":["history","chinese-history","decision-support","historical-analogy","sandbox-simulation","strategy","zh-CN"],"openclaw":{"always":false,"homepage":"https://github.com/GreatXiaoRY/LearnFromHistory-skill","skillKey":"yi-shi-wei-jian"}}
---

# 以史为鉴

把现实决策问题转成“局面判断 -> 历史映射 -> 路径设计 -> 沙盘推演”的结构化分析，而不是做历史百科、哲学闲聊或宿命论判断。

本 skill 的主工作流应当是：由宿主 agent 直接阅读案例库与提示文件，按结构语义做判断。`src/main.py` 只是本地 fallback 基线，不应取代宿主 agent 的语义推理。

## 触发条件

在下列场景优先使用本 skill：

- 用户正在问“该不该推进、该先稳内部还是先上制度、该先打还是先守、该不该换人、该不该和不完全信任的合作方结盟、改革为什么推不动、资源弱势如何破局”
- 用户想借历史案例理解组织管理、商业竞争、联盟博弈、内部权力冲突、改革阻力、扩张节奏
- 用户明确提到“以史为鉴”“用中国历史类比”“帮我做沙盘推演”
- 用户明确要求“把这个案例加入案例库”“补充一个新历史案例”“把我刚说的这个历史经验沉淀下来供以后检索”
- 用户虽然没提历史，但问题本质是在问“现在是什么局”“能借什么结构性经验”“不同路径会怎么演化”

在下列场景不要触发或只部分借用：

- 用户只是要纯历史知识问答
- 用户要求命理、算命、绝对预测
- 用户要法律、医疗、投资等高风险确定性结论

## 输入解析

先从用户问题里抽取这 7 类信息：

1. 当前目标：你到底想赢什么，守什么，改什么
2. 主要对手：比你强还是比你弱，明面冲突还是暗线制衡
3. 自身资源：钱、人、时间、组织控制力、合法性
4. 内部状态：是否统一，是否有人拖后腿，是否存在派系
5. 外部关系：盟友、股东、合作方、上级、地方势力是否稳定
6. 时间窗口：是否必须立即行动，是否可以拖延、试点、换节奏
7. 约束条件：不能公开冲突、不能失去名分、不能丢现金流、不能让核心团队失控

如果这些信息明显缺失，先问 1-3 个关键澄清问题；如果用户不想补充，就在输出中显式标注你的假设。

## 语义分析原则

优先做“结构语义理解”，不要先做“字面关键词命中”。分析时至少先判断这些维度：

- 资源强弱
- 内部摩擦
- 外部压力
- 联盟依赖程度
- 信任风险
- 变革强度
- 控制权压力
- 用人调整压力
- 时间压力
- 合法性压力
- 执行阻力
- 行动取向：更偏推进、稳局、结盟，还是调权换人

只有在宿主需要确定性兜底时，才调用本地 CLI。即使调用 CLI，也应把它看成结构化基线，而不是最终权威答案。

## 分类规则

优先把局面归入 1 个主局面，再给 1-2 个次级局面：

- `以弱对强`：资源、地位、市场份额或正式权威明显弱于对手
- `内部冲突`：团队、派系、股东、盟友之间出现分裂与掣肘
- `改革推进`：制度调整、流程重构、组织变法、利益再分配
- `联盟不稳`：合作关系短期有效，但长期目标并不一致
- `守攻抉择`：到底先守基本盘，还是主动出击创造新局面
- `权力控制`：控制权、任命权、接班、军权、组织中枢的归属
- `用人换将`：是否换人、空降、授权、剥离关键岗位

优先判断“结构相似性”，不要把“同一个词”误当成“同一个局”。

## 检索规则

1. 先读 `data/historical_cases.json`，再合并读取 `data/user_cases.json`
2. 以 `situation_tags`、`objective`、`hidden_constraints`、`chosen_action`、`key_reasons` 的结构语义为主做匹配，`modern_analogy_keywords` 只是辅助
3. 选 2-4 个最相似案例，优先选择“结构接近但结果不同”的案例组合；若合适，至少给 1 个失败或代价过高的对照案例
4. 每个案例必须交代：
   - 事件
   - 核心局面
   - 关键决策
   - 成败原因
5. 最少用一句话说明“为什么这个案例像当前问题”，尤其要指出约束条件、权力结构、资源状态、时间压力上的相似性
6. 不要只因为案例著名就选它；要优先选择与用户约束最像的

如果需要确定性基线，可运行本地 CLI：

- Claude Code 路径变量：`python "${CLAUDE_SKILL_DIR}/src/main.py" --question "$ARGUMENTS"`
- OpenClaw 路径变量：`python "{baseDir}/src/main.py" --question "<用户问题>"`

调用 CLI 后，不要机械复述 CLI 输出；应结合案例文本和用户上下文再做一次语义整理。

## 案例扩充

如果用户提供了一个新的历史案例，并明确希望后续检索也能用到它，不要只在当前回答里临时引用。按下面流程处理：

1. 先判断用户是不是在要求“把新案例加入库”，而不只是临时举例
2. 如果信息不完整，先追问 1-3 个关键缺口，优先补齐：
   - 事件概述
   - 关键决策
   - 成败原因
   - 可迁移原则
   - 来源说明
3. 把用户的自然语言描述整理成单条 JSON，对照模板 `examples/case_submission_template.json`
4. 优先直接通过标准输入写入，而不是把责任丢回给用户手工改文件：
   - PowerShell：`@'<json>'@ | python scripts/add_case.py --stdin`
   - 或：`python scripts/add_case.py --case-json '<json>'`
   - 或：`python scripts/add_case.py --case-file <json 文件路径>`
5. 写入目标是 `data/user_cases.json`
6. 成功后明确告诉用户新案例的 `id`，并说明后续检索会自动加载

如果用户只给了模糊描述，先帮他补齐以下内容再入库：

- 事件概述
- 核心局面
- 关键决策
- 成败原因
- 可迁移原则
- 不可直接照搬的因素
- 来源说明

最低入库质量要求：

- 必须是真实历史案例，不能是虚构或模糊传说
- `id` 必须唯一
- `source_note` 不能为空
- `summary`、`chosen_action`、`key_reasons`、`transferable_principles` 不能空
- `situation_tags` 要尽量贴近本 skill 的分类体系

## 推演规则

生成 2-4 条彼此不同的可选路径，而不是同一策略的改写版。常见路径包括：

- 立即推进
- 先稳内部
- 暂避锋芒
- 联盟博弈
- 换将整队
- 试点改革

对每条路径都必须分析：

- 适用条件
- 短期收益
- 短期风险
- 中期演化
- 最容易失败点

如果用户问题明显涉及“中层拖延、合作方翻脸、负责人是否要换、控制权被架空、资源比对手更弱”，优先让路径名称直接回应这些现实语句，而不是写得过泛。

推演时优先围绕这些变量：

- 资源
- 内部一致性
- 对手状态
- 联盟稳定性
- 时间窗口
- 合法性

## 输出模板

最终输出必须固定为以下结构：

```text
【局面判断】

【历史参照】

【关键变量】

【可选路径】

【沙盘推演】

【借鉴原则】

【边界提醒】
```

要求：

- `【历史参照】` 输出 2-4 个案例
- `【可选路径】` 输出 2-4 条路径
- `【沙盘推演】` 必须逐路径展开，不能省略
- `【借鉴原则】` 提炼可复用规则，不要只复述历史

## 安全边界

始终保留以下边界：

- 历史类比 != 现实预测
- 推演 != 结果保证
- 历史人物、制度、地理与技术条件不可直接照搬
- 不给“必胜”“一定成功”“唯一正确路线”这类绝对结论
- 如果用户问题属于高风险专业场景，只能给结构化思考框架，不能冒充专业意见
- 本 skill 不需要 `always` 常驻权限；只在用户触发决策分析或明确要求补充案例时使用。写入能力仅限本 skill 目录下的 `data/user_cases.json`。

## 附加资源

- 局面分类提示：`prompts/classify_situation.md`
- 案例检索提示：`prompts/retrieve_cases.md`
- 案例比较提示：`prompts/compare_cases.md`
- 案例入库提示：`prompts/add_case_intake.md`
- 方案综合提示：`prompts/synthesize_advice.md`
- 沙盘推演提示：`prompts/sandbox_simulation.md`
- 安全边界提示：`prompts/safety_boundary.md`
- 可运行分析引擎：`src/main.py`
- 示例：`examples/`
