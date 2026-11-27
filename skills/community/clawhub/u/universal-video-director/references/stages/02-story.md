# 子技能 02 · 剧本 story
**来源**：drama-skills 的 short-drama-write（因果节点、可拍剧本、片场格式），shuohao novel-script（台词与动作交替的 beat 流、按语速确定性估算时长、前 3 个 beat 必须是冷开场钩子、逐角色台词本），ai-short-drama-from-zero 的台词锁定。

## 目标
写出一份**可拍**的剧本：每个 beat 要么是看得见的动作，要么是一句台词，时长可以算出来。

## 方法
1. **beat 只写摄影机能拍到的内容**。内心活动要改写成动作或 OS。type 取 action / dialogue / os / vo / insert。
2. **时长确定性估算**：对白类 beat 的时长 ≥ 字数 / chars_per_sec。动作 beat 按动作本身估，一般 1.5–4 秒。总时长控制在 duration_sec ±10% 以内，**最好在 ±5% 以内**。偏差超过 5% 会报 DURATION_EDGE 警告：分镜阶段剪掉入出点后时长通常还会缩 3–8%，擦边的剧本到剪辑阶段就会越界。
3. **结构**：
   - 前 3 个 beat 里必须有一个 hook
   - 中段每 10–15 秒安排一个 rise 或 twist
   - 结尾用 cliff（连续剧）或 payoff（单集）
4. **因果**：关键 beat 用 `causal_from` 写清楚它是由哪个 beat 引起的，避免剧情是硬拼出来的。
5. **锁定台词**：用户给定或原著里的金句，标 `locked:true`。修复时只能给它加时长，不能改字。
6. **line_book**：每句台词配一条 tts_prompt（情绪、语速、音色），直接交给配音。
7. **关卡**：story_approval=true 时，把剧本整理成可读的 Markdown 给用户确认。

## 常见错误码
NO_COLD_HOOK、LINE_TOO_FAST、DURATION_OFF、REF_CHAR、ACTION_MISSING
