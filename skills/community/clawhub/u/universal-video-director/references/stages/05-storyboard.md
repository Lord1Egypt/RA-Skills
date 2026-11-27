# 子技能 05 · 分镜与首帧 storyboard
**来源**：shuohao novel-storyboard（segment 一次生成 ≤15 秒 → cut 2–5 秒硬门禁 → 关键帧时间点，18 道门禁），drama-skills short-drama-storyboard（镜头职责、起止画面、首尾帧提示词、逐镜挂图计划），ai-short-drama-from-zero 的 13/14/15（统一导演机位方案、CUT 几何审计、镜头任务覆盖），claude-video-studio 的 animatic。

## 目标
把剧本拆成可以直接拿去生成的镜头。每个镜头要写清楚：拍什么、从哪里拍、从什么画面开始、到什么画面结束。

## 方法
1. **三级结构**：
   - segment：一次生成，时长 ≤ segment_max_sec，不跨场景
   - cut：一个连续机位区间，时长在 cut_min 到 cut_max 之间
   - keyframe_t：关键帧所在的时间点
2. **先做全场 coverage 设计，再写单镜**：先规划这场戏的机位站点（station）序列和景别曲线，再逐镜填写 camera.station、angle、movement 和 motivation（为什么这样运镜）。
3. **镜头内部机位连续，镜头之间才是 CUT**：
   - 机位不变，就是固定镜头
   - 机位连续变化，就是运镜
   - 同场相邻的两个 cut，景别、机位、角度不能完全相同（JUMP_CUT）
   - 不能连续 4 镜都在同一个机位（MONO_COVERAGE）
4. **start_frame 和 end_frame**：写起止画面的状态，包括手部姿态、手里拿的东西、视线方向。起止画面相同就说明这个镜头没有推进。
5. **first_frame_prompt**：只描述开场那一格画面。用到的每个资产的锁定词都要原样带上；画幅写在最前面，最后加 `no text, no logo`。需要首尾帧控制时，再写 last_frame_prompt。
6. **opening_blocking**：每场第一个 segment 要原样带入 04 的站位句。
7. **覆盖检查**：每个 beat 都至少要有一个 cut 覆盖。

## 常见错误码
SEG_SUM、SEG_TOO_LONG、CUT_LEN、BEAT_UNCOVERED、LOCK_MISSING、JUMP_CUT、REF_ASSET
