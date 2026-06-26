---
name: z1-matrix-memory-palace
description: "Build and operate a file-driven Memory Palace for multi-agent systems, combining a spatial memory shell with a continuously maintained LLM Wiki reflection layer. Use when designing or deploying long-term memory architecture for agent teams, especially for (1) project rooms + task corridors + reflection wings, (2) low-token file-based coordination buses, (3) converting work artifacts into principles, prompt kernels, failure patterns, and thinking paths, (4) building a silent librarian/archivist agent, or (5) migrating scattered protocol/history files into a structured memory operating system. Includes source attribution and fusion guidance from Karpathy's llm-wiki idea and Jeff Pierce's memory-palace approach."
---

# Z1矩阵宫殿记忆法

以“空间骨架 + 编译灵魂 + 低 token 调度宪法”为核心，构建长期运行的多 Agent 记忆操作系统。

## 核心定义
将长期记忆拆成三层：
1. **Raw Layer**：工作区原始产物、协议、日志、任务卡
2. **Palace Layer**：房间、走廊、项目室、总厅、索引、路由
3. **Wiki / Reflection Layer**：原则页、提示词内核、失败模式、思考路径、候选宪法

一句话总纲：
**用 Memory Palace 组织空间，用 LLM Wiki 编译知识，用文件驱动宪法压低噪声。**

## 参考来源与融合思路
必须明确标注两条来源：

### 来源A：Karpathy 的 llm-wiki 思路
核心启发：
- 不是每次查询都从原始材料重新拼装知识
- 而是由 LLM 持续维护一个持久、结构化、可交叉引用的 wiki 中层
- 新材料进入后，不只是索引，而是编译进既有知识结构
- 问答结果也可回写为新页面

一句话：
**知识不是临时召回，而是持续编译。**

### 来源B：Jeff Pierce 的 memory-palace 思路
核心启发：
- 记忆应独立于模型上下文存在
- 记忆应具备跨实例、跨 Agent 的共享与检索能力
- 记忆层适合承接关系、消息、分区、长期存储
- 记忆系统应成为模型旁边的长期层，而不是模型内部的幻觉延长线

一句话：
**记忆不属于模型，记忆属于系统。**

### 融合方法
本技能不照抄任何单一方案，而是融合为：
- **Memory Palace** 负责：空间分层、项目房间、任务走廊、总控路由
- **LLM Wiki** 负责：持续编译原则、方法、失败模式、思考路径
- **文件驱动宪法** 负责：把通信从聊天迁移到路径、卡片、物理产物

## 适用对象
适用于：
- 多 Agent 团队
- 长期项目知识沉淀
- 跨任务经验复用
- 希望减少上下文漂移与 token 浪费的系统
- 需要把“项目事实”与“长期原则”分层的知识架构

不适用于：
- 一次性临时笔记
- 只有单轮聊天、无长期维护需求的场景
- 没有物理文件产出的纯对话式工作流

## 默认空间拓扑
### 1. Grand Hall
全局总控台，负责：
- active 任务总览
- completed 链路总览
- reflection 覆盖总览
- 核心协议入口

### 2. Chambers
按 Agent 分房：
- 01_core
- 02_intel
- 03_pub
- 04_code
- 05_media
- 可扩展 archivist 等后台角色

### 3. Project Rooms
按项目分房，例如：
- raw_stone
- karpathy_daily
- lobster_legion

### 4. Dispatch Corridor
任务运行态总线：
- active/
- blocked/
- completed/

### 5. Reflection Wing
长期编译区：
- principles/
- prompt_kernels/
- failure_patterns/
- thinking_paths/
- constitution_candidates/

### 6. Archive Basement
低频历史归档层。

## 运行原则
### 原则1：路径即状态
任务状态优先由 task card 和目录位置承载，而不是由聊天上下文承载。

### 原则2：文件优先于对话
能通过输入/输出路径锚定，就不要重复灌输背景。

### 原则3：项目沉淀与原则提炼分离
- project room 存项目事实
- reflection wing 存长期逻辑
- constitution candidate 只接收反复验证的硬规则

### 原则4：一题一主链
同一任务默认一条主执行链，不开多子对话分叉。

### 原则5：静默 Librarian
专设 Archivist / Librarian，只在后台读取 completed cards 与 project rooms，编译长期记忆，不参与前线对话。

## 标准工作流
### A. 建骨架
1. 创建 grand_hall / chambers / project_rooms / dispatch_corridor / reflection_wing
2. 创建总控台、命名规范、索引与日志
3. 明确每个房间的职责边界

### B. 让任务上走廊
1. 每条主链任务建立唯一 task card
2. active / blocked / completed 三态迁移
3. 卡片中必须写明输入/输出路径、验收、下一步

### C. 让项目进房间
1. 为长期项目建立 project room
2. 写 index、chain_map、reflection_backfill
3. 把 corridor 卡与 reflection 页面回链到项目房间

### D. 让经验进反思侧翼
当 completed card 出现后，判断是否编译：
- principle card
- prompt kernel
- failure pattern
- thinking path
- constitution candidate

### E. 做旧记忆回填
对已有高价值协议：
1. 保留原始文件作为历史源
2. 在 palace 对应 chamber 或 project room 中建立镜像文件
3. 建立 legacy_index
4. 让 grand hall 和 reflection 可以导航到这些镜像

## 记忆代谢规则
### 只留在 Project Room 的内容
- 单一项目事实
- 样本与阶段痕迹
- 不具跨任务复用价值的内容

### 进入 Reflection Wing 的内容
- 多任务复现有效
- 能压缩为原则 / kernel / failure / path
- 能降低未来 token 成本或错误率

### 升级为 Constitution Candidate 的内容
必须同时满足：
1. 多任务验证
2. 偏离代价显著
3. 属于长期默认行为
4. 不是局部技巧

## Librarian / Archivist 规则
若你需要后台记忆编译员：
- 只读取已落盘文件
- 只在 completed 后触发编译
- 不直接对外交互
- 不把聊天当主证据
- 不把局部经验滥升为宪法

## 命名与路由规范
优先采用：
- Corridor 卡片：`YYYY-MM-DD_<slug>.md`
- task_id：`<scope>-<slug>-<date>`
- Project Room：`<project_slug>/`
- Reflection 页面：`<semantic_slug>_<YYYY-MM-DD>.md`
- Core Protocol：`z1_<protocol_name>_v<major>_<YYYY-MM-DD>.md`
- Agent Runbook：`RUNBOOK_V<major>_<YYYY-MM-DD>.md`

## 何时读取 references/
- 若需要完整房间拓扑、任务卡模板、代谢协议样例：读取 `references/architecture.md`
- 若需要发布文案、来源说明、融合声明：读取 `references/publishing-note.md`
- 若需要快速命名与路由速查：读取 `references/naming-quickref.md`
- 若需要中文发布介绍页：读取 `references/release-copy-zh.md`
- 若需要英文发布介绍页：读取 `references/release-copy-en.md`

## 交付要求
当使用本技能帮助他人落地时，最终交付应至少包含：
1. 参考来源说明
2. 融合逻辑说明
3. 空间拓扑
4. 运行层（corridor）
5. 反思层（reflection wing）
6. 后台 archivist 方案
7. 命名与路由规范
8. 阶段性总控入口

## 一句话结尾
**Z1矩阵宫殿记忆法，不是做一个会搜的库，而是做一个能持续沉淀、持续编译、持续收束噪声的多 Agent 记忆中枢。**
