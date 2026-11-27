# 子技能 01 · 原著与对标分析 source_analysis
**来源**：drama-skills 的 novel-analyze（抽样快评、逐章梳理、分集建议）和 breakdown（对标剧节奏测量、反推剧本），shuohao novel-outline 的五件套大纲。

## 目标
先判断值不值得拆，再给出分集方案。同时把不能改的设定和前期要藏住的悬念列出来，后面阶段都不能违反。

## 方法
1. **抽样快评**：从开头、中段、结尾各抽一段，给出 verdict.score 和是否值得改编。不值得就停下来，告诉用户。
2. **逐章梳理**：每一章写 summary 和 hook_strength。**不要直接拿章节数当集数**，要按冲突单元来切。
3. **immutable_facts**：人物关系、身份秘密、世界规则。这些是后面各阶段的硬约束。
4. **hidden_suspense**：前几集必须藏住、不能提前揭示的信息。
5. **episode_plan**：每集写原文范围、核心冲突和集尾钩子。
6. **有对标视频时**：用 ffprobe 或场景检测量出平均镜头时长、对白密度、钩子出现的秒数，写进 benchmark；和本项目差距大的地方写进 gaps。

## 校验
schema 校验。worth_adapting=false 时不允许进入 02。这一条由总控在流程里把关，校验器不检查。
