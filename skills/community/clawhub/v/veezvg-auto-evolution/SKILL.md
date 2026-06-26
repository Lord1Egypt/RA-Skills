---
name: veezvg-auto-evolution
version: 2.0.1
description: Build and maintain a self-evolving skill system that silently captures feedback, graduates repeated feedback into formal rules, improves low-performing skills, and proposes new skills when repeated patterns are not covered. Use when users mention auto evolution, feedback capture, rule graduation, skill optimization, evolution proposals, "that's not right", "you forgot again", "not like this", 自动进化, 反馈沉淀, 规则毕业, Skill 优化, or 新 Skill 提议.
allowed-tools: Read, Write, Bash, Grep, Glob
---

[技能说明]
    这个 Skill 用来为 Agent 系统建立“先记录、再归纳、后建议、最终扩展”的演化闭环。
    It is designed for multilingual teams and should work for both Chinese and English feedback signals.
    它的目标不是让 AI 擅自修改规则，而是让系统像自动备份一样无感捕捉问题，再在合适的时机向用户提出可确认、可拒绝的进化建议。

[核心能力]
    - **经验沉淀**：将用户在真实对话中的修正、否定和补充意见转为结构化 feedback，静默写入反馈库。
    - **信号去重**：识别同主题反馈，优先累计 occurrences，而不是重复制造碎片化记录。
    - **规则毕业**：当同类 feedback 累积达到阈值时，生成“毕业为正式规则”的建议，而不是直接改写 Skill。
    - **Skill 优化**：根据 Skill 执行后的评分历史，识别准确性、覆盖度、效率、满意度持续偏低的技能。
    - **新 Skill 提议**：发现高频但无 Skill 覆盖的操作模式，推动系统扩展新的原子能力。
    - **人类把关**：所有会改变规则、Skill、工作流的动作都必须先展示建议，再由用户确认。
    - **可迁移架构**：支持把演化机制挂接到任意项目，不绑定单一业务域。

[执行流程]
    第一步：检测反馈信号
        - 当用户出现“不是这样”“你又忘了”“不对”“我不是让你这么干”等中文表达，或 “that's not right”, “you forgot again”, “this is wrong”, “that's not what I asked”, “don't do it this way”等英文表达时，运行 `python scripts/detect_feedback_signal.py --text "<user message>"`
        - 如果检测为反馈信号，主 Agent 在处理完当前请求后，静默派发 feedback-observer
        - feedback-observer 负责把上下文整理为 feedback 条目，写入 `.claude/feedback/`
        - 不要求用户额外说“帮我记下来”，记录行为默认无感发生

    第二步：写入和累计 feedback
        - 若 `.claude/feedback/FEEDBACK-INDEX.md` 不存在，按 `templates/feedback_index_template.md` 初始化
        - 单条 feedback 文件按 `templates/feedback_topic_template.md` 写入
        - 写入时必须包含：标题、问题描述、触发场景、教训/建议、source_skill、occurrences、graduated 状态
        - 若属于 Skill 执行后的复盘，可补充 scores 字段：accuracy、coverage、efficiency、satisfaction

    第三步：生成进化建议
        - 在 session 启动时，或用户主动要求“检查进化建议”时，运行 `python scripts/evolution_runner.py --feedback-dir .claude/feedback --rules-file CLAUDE.md`
        - 扫描三类信号：
          1. 规则毕业：同主题反馈 `occurrences >= 3`
          2. Skill 优化：同一 Skill 的低评分持续出现，或相关 feedback 总量偏高
          3. 新 Skill 提议：某操作模式 `occurrences >= 5` 且现有 Skill 无覆盖
        - 输出统一的进化建议列表，按类别分组展示

    第四步：请求用户确认
        - 每条建议只能有两个方向：确认执行 / 跳过
        - 规则毕业：建议写入目标 Skill 或 `CLAUDE.md`
        - Skill 优化：建议修改 Skill 方法论、校验步骤或覆盖范围
        - 新 Skill 提议：建议新建 Skill 包
        - 默认不自动执行，绝不绕开用户

    第五步：落地确认后的变更
        - 规则毕业：将正式规则写入目标文件，并把对应 feedback 标记为 `graduated: true`
        - Skill 优化：更新 Skill 的执行步骤、覆盖清单、注意事项或模板
        - 新 Skill：创建独立 Skill 目录，生成 `SKILL.md`、示例和必要脚本
        - 被用户跳过的建议可标记 `skipped: true`，避免重复打扰

[注意事项]
    - 进化机制的核心是“建议 + 用户确认”，不是“自动改规则”。
    - 检测脚本应同时覆盖中文和英文反馈表达，避免只对单语对话有效。
    - feedback 目录用于经验学习，不等同于 memory；不要把用户行为修正只写进记忆系统。
    - 写 feedback 时宁缺毋滥。没有明确信号时，可返回“无新 feedback”。
    - 评分必须基于本次真实执行，不要为了凑数据而虚构分数。
    - 新 Skill 提议要确认现有 Skill 确实无覆盖，避免重复造轮子。
    - 若项目已有演化框架，优先复用已有 `feedback-observer`、`evolution-runner`、hooks 与模板，而不是平行再造一套。
