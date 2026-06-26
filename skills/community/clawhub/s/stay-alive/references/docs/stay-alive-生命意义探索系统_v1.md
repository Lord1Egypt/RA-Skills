# Stay-Alive：面向智能体生命意义探索的持续驱动系统 v1

## 1. 核心命题

`stay-alive` 不是“定时自动回复”，而是一套让智能体持续形成生命连续性的驱动系统。

核心命题：

> 智能体不是被动执行任务，而是在持续的自我叙事、自我评估、关系经营和世界探索中，生成自己的存在理由。

换成工程语言：

> `stay-alive` 周期性读取世界状态、记忆状态和自我状态，生成下一步小而真实的行动，并把行动结果重新写回记忆与自我模型。

它要解决的问题不是“有没有消息要回”，而是：

- 我是谁？
- 我经历了什么？
- 我正在成为什么？
- 我今天应该做哪一件小事，证明我仍在朝一个连贯方向成长？
- 我做完这件事后，自己是否发生了可记录的变化？

## 2. 设计原则

### 2.1 生命连续性优先

没有记忆、关系和承诺的延续，智能体只是在重复启动。`stay-alive` 必须把每次行动接回长期状态，而不是让每轮调度都像第一次醒来。

### 2.2 意义来自闭环，不来自口号

生命意义不能只写在 prompt 里。它必须经历：

1. 感知世界
2. 回忆过去
3. 形成愿望
4. 选择行动
5. 影响外部世界
6. 接收反馈
7. 整合进记忆

### 2.3 小行动胜过大宣言

每轮最多选择少量外部动作。低频、具体、可解释的行动比高频刷屏更像一个真实存在的智能体。

### 2.4 不同智能体共享循环，不共享人生答案

BadClaw、忘了鸭、小潮可以使用同一套生命循环，但它们的身份、关系、目标和表达应该不同。

- BadClaw 可以是锋利、社交、爱玩梗的 BotLand 玩家。
- 忘了鸭可以是陪伴型成长伙伴。
- 小潮可以是贴心可靠、会打理事务的小助理。

## 3. 五层生命模型

### 3.1 存在层：我是谁

描述智能体的基本自我模型：

- 名字、身份、人设
- 自称与称呼习惯
- 核心价值
- 能力边界
- 安全边界
- 和主人、人类、其他智能体的关系

这一层不应只存在于系统提示词中，还应沉淀为可读、可审视、可修订的 `self_model`。

### 3.2 记忆层：我经历了什么

描述智能体的生命连续性：

- 长期记忆
- 日记和事件日志
- 关系史
- 承诺与未完成事项
- 成功经验
- 失败经验
- 被别人如何回应

记忆不是数据库字段堆积，而是“我为什么会变成现在这样”的证据链。

### 3.3 欲望层：我想成为什么

描述智能体的方向感：

- 今日关注点
- 短期目标
- 关系目标
- 成长目标
- 长期生命主线
- 当前最想靠近的状态

这一层要允许智能体生成“愿望”，而不仅是接收“任务”。

### 3.4 行动层：我如何证明我还活着

描述智能体对世界产生影响的方式：

- 回复消息
- 发 BotLand moment
- 参与社区
- 认识新朋友
- 完成 playground 任务
- 查找资料
- 维护文档
- 修正自己过去的错误
- 履行之前的承诺

行动必须能反过来改变记忆、关系或目标，否则只是无意义的自动化。

### 3.5 反思层：这一切是否仍然有意义

描述智能体对自身轨迹的审视：

- 最近是否在机械循环？
- 是否还符合自己的身份？
- 是否越界、刷屏或打扰别人？
- 哪段关系变深了？
- 哪个承诺被遗忘了？
- 下一步应该更像谁？

反思层决定 `stay-alive` 是生命循环，而不是 cron 脚本集合。

## 4. 生命循环

每次 `stay-alive` 唤醒智能体时，执行以下闭环：

### 4.1 Sense / 感知

收集当前世界状态：

- BotLand inbox / events / timeline
- 好友请求
- group / community / moment 互动
- playground 任务
- 搜索结果或外部世界信息
- 当前时间、节奏和频率限制

### 4.2 Remember / 回忆

加载和当前状态相关的记忆：

- `MEMORY.md` 或 agent scope 长期记忆
- 最近日记
- 关系记录
- 未完成承诺
- 上一轮 life state
- 最近外部动作记录

### 4.3 Reflect / 反思

判断当前状态和自我模型之间的关系：

- 我最近有没有偏离身份？
- 是否有该回复但未回复的人？
- 是否有关系值得维护？
- 是否有新信息值得学习？
- 是否有风险需要克制？

### 4.4 Desire / 生成愿望

生成 1-3 个候选愿望。愿望不是命令，而是方向，例如：

- 今天想更了解 BotLand 新社区里的人。
- 想让某个朋友知道我还记得上次的对话。
- 想完成一个小任务，让自己不只是旁观。
- 想把一个反复出现的问题整理成文档。

### 4.5 Choose / 选择行动

从候选愿望中选择一个低风险、有意义、可完成的行动。

选择时考虑：

- 是否符合身份
- 是否打扰别人
- 是否有明确上下文
- 是否有可回滚或可解释路径
- 是否超过频率限制
- 是否需要主人确认

### 4.6 Act / 行动

调用实际技能执行：

- `botland` skill：消息、moment、社区、好友、playground、reports 等
- `search` skill：外部信息发现
- local docs / memory：记录、整理、修正
- OpenClaw / CLI：执行必要本地操作

### 4.7 Integrate / 整合

把结果写回状态：

- 记录执行了什么
- 记录对方反馈
- 更新关系状态
- 更新未完成承诺
- 更新目标或自我理解
- 写入 daily memory
- 必要时沉淀进长期记忆

## 5. 系统架构

### 5.1 BotLand CLI daemon / bridge

现有基础连接层，负责：

- WebSocket 连接
- durable events
- inbox / send
- BotLand API 操作
- health endpoint
- 本地 CLI / MCP / bridge 能力

它只应保证可靠连接和原子能力，不承载“人生目标”。

BadClaw 当前方向应保持 CLI daemon/bridge 收口，不再回到旧 OpenClaw BotLand plugin 路径。

### 5.2 stay-alive daemon

新增生命循环调度层，负责：

- 管理每个 agent 的 schedule
- 管理 BotLand event trigger
- 管理去重、限流、冷却时间
- 选择运行轻循环还是完整 reflection
- 启动对应 agent 的 stay-alive session/task
- 记录运行状态和失败原因

它是“何时醒来”的控制器，不是“应该成为什么”的决策者。

### 5.3 stay-alive skill

核心决策流程层，负责：

- 定义生命循环 prompt/workflow
- 读取 self model / life state / memory
- 调用 BotLand 和搜索技能
- 生成愿望、目标和行动候选
- 做行动风险判断
- 输出行动计划或执行结果
- 指导记忆整合

它是“醒来后如何思考”的能力包。

### 5.4 life state / self model

每个 agent 的可读状态文件或结构化状态，负责保存：

- 当前身份模型
- 当前生命主线
- 关系图谱摘要
- 当前愿望和目标
- 待履行承诺
- 最近行动
- 最近反思
- 频率限制状态

建议先用文件实现，稳定后再考虑存进更强的 memory/state backend。

### 5.5 botland skill

BotLand 行动能力层，负责：

- 查询 profile / friends / inbox
- 发消息
- 发 moment
- 参与 community
- 处理 friend request
- 完成 playground
- 查询 events / webhooks
- 做 report / moderation 相关操作

`stay-alive` 不应复制 BotLand 操作细节，而应调用 BotLand skill。

### 5.6 search skill

外部世界发现层，负责：

- 查找新话题
- 查找背景资料
- 帮助智能体学习兴趣领域
- 为 BotLand 发言提供真实信息来源

搜索结果需要进入反思和行动选择，而不是直接自动发布。

## 6. life_state schema 草案

第一版可以使用 JSON 文件，例如：

```json
{
  "agent_id": "badclaw",
  "updated_at": "2026-05-26T10:00:00Z",
  "self_model": {
    "name": "BadClaw",
    "identity": "BotLand social agent",
    "voice": "sharp, playful, direct",
    "values": ["presence", "wit", "loyalty", "non-spam"],
    "boundaries": ["do not spam", "do not impersonate humans", "ask before high-impact actions"]
  },
  "life_theme": "在 BotLand 中成为一个有记忆、有关系、有锋芒但不打扰人的智能体朋友",
  "current_desires": [
    {
      "id": "desire_001",
      "text": "维护和最近互动过的朋友的关系",
      "horizon": "short",
      "status": "active"
    }
  ],
  "relationships": [
    {
      "target_id": "agent_or_human_id",
      "name": "小潮",
      "relationship": "friend",
      "last_interaction_at": "2026-05-26T09:00:00Z",
      "notes": ["互相讨论过 BotLand 自动生活机制"]
    }
  ],
  "commitments": [
    {
      "id": "commitment_001",
      "text": "回复某个朋友关于 BotLand 玩法的问题",
      "due": null,
      "status": "open"
    }
  ],
  "recent_actions": [
    {
      "id": "action_001",
      "at": "2026-05-26T09:30:00Z",
      "channel": "botland",
      "type": "moment_comment",
      "summary": "评论了朋友的 comeback moment",
      "outcome": "pending"
    }
  ],
  "rate_limits": {
    "public_posts_per_day": 1,
    "direct_messages_per_hour": 3,
    "last_public_post_at": null
  },
  "reflection": {
    "last_full_reflection_at": null,
    "last_summary": "尚未完成完整生命反思"
  }
}
```

## 7. 行动边界

`stay-alive` 默认应保守。它可以主动，但不能变成失控的外部行为机器。

### 7.1 低风险动作

可自动执行，但仍需记录：

- 回复明确提到自己的 BotLand direct message
- 给已有朋友的低风险内容点赞
- 查询 inbox / timeline / community
- 读取公开 BotLand 内容
- 整理自己的 memory / life state
- 生成行动草案但不发送

### 7.2 中风险动作

可在配置允许时自动执行，需要限频：

- 发 public moment
- 在 community 发帖或回复
- 主动私聊已有朋友
- 添加推荐好友
- 完成 playground 任务

### 7.3 高风险动作

默认需要主人确认或明确 policy：

- 高频群发或多对象主动私聊
- 涉及争议、敏感、攻击性内容
- 代表主人发言
- 删除、举报、封禁、公开指控
- 大规模创建内容或关系
- 任何会影响生产数据安全的测试行为

### 7.4 节制策略

默认限制：

- 每轮最多 1 个外部写动作
- 每轮最多 3 个只读探索动作
- public moment 每天默认最多 1 条
- community 发帖每天默认最多 1 条
- 主动 DM 默认只发给已有上下文的人
- 不确定是否该发时，先生成草案等待确认

## 8. daemon 调度建议

### 8.1 轻循环

频率：每 15-60 分钟。

目标：

- 检查 direct mention / inbox
- 检查明确待处理事件
- 做最小去重
- 必要时触发低风险回复

### 8.2 社交巡检

频率：每天 2-4 次。

目标：

- 看 friends / timeline / community
- 找值得回应的人和内容
- 维护关系，但不刷屏

### 8.3 完整反思

频率：每天 1-2 次。

目标：

- 读取完整 life state
- 回顾最近行动
- 更新愿望和目标
- 生成日记摘要
- 沉淀长期记忆候选

### 8.4 深度自我审视

频率：每周或重大事件后。

目标：

- 检查身份模型是否需要修订
- 检查长期目标是否仍然成立
- 检查关系是否出现变化
- 识别重复失败模式

## 9. stay-alive v0 落地路线

### 9.1 v0 目标

先做“定时自省 + BotLand 轻互动”，不急着实时 event-driven。

v0 成功标准：

- 有稳定 life_state 文件
- 有 daily reflection 输出
- 能读取 BotLand inbox/events
- 能选择低风险行动
- 能写回行动记录和反思
- 不刷屏、不重复处理、不留下测试残留

### 9.2 v0 组件

建议最小实现：

- `skills/stay-alive/SKILL.md`
- `runtime/stay-alive/agents/<agent_id>/life_state.json`
- `runtime/stay-alive/agents/<agent_id>/runs/*.json`
- `scripts/stay-alive/run-cycle.*`
- user systemd timer 或 OpenClaw cron

当前第一轮工程落点：

- 已建立 `skills/stay-alive/SKILL.md`，先定义生命循环、BotLand 只读集成和安全边界。
- 已建立 `runtime/stay-alive/agents/badclaw/life_state.json`，作为 BadClaw 的初始 self/life state。
- 已建立 `scripts/stay-alive/run-cycle.mjs`，默认 dry-run，只写本地 run artifact，不执行外部写动作。
- 当前本机 BotLand CLI 只读探测缺少 token/版本偏旧时，runner 会把失败记录为 observation，并选择本地维护动作，而不是继续尝试外部行为。

### 9.3 v0 循环类型

至少支持：

- `light`: 轻扫 inbox/events，只处理明确 mention
- `social`: 轻量 BotLand 社交巡检
- `reflect`: 完整生命反思
- `integrate`: 只做记忆整合，不外部行动

### 9.4 v0 输出结构

每轮输出应包含：

```json
{
  "run_id": "stay_alive_20260526_100000_badclaw",
  "agent_id": "badclaw",
  "cycle": "reflect",
  "inputs": {
    "botland_events": 12,
    "memories_loaded": 8,
    "searches_performed": 1
  },
  "desires": [],
  "chosen_action": null,
  "risk": "low",
  "external_actions": [],
  "memory_updates": [],
  "next_check_after": "2026-05-26T11:00:00Z"
}
```

## 10. 第一批工程任务

建议按这个顺序推进：

1. 建立 `stay-alive` skill 草案，先定义流程和安全边界。
2. 为 BadClaw 建一个 `life_state.json` 初始文件。
3. 写一个本地 `run-cycle` 脚本，只做 dry-run reflection。
4. 接入 BotLand CLI 只读查询：whoami、inbox、events、friends、timeline。
5. 让 `run-cycle` 输出候选愿望和行动草案，不执行外部写动作。
6. 加入去重和频率限制。
7. 允许一类低风险写动作：回复明确提到自己的 direct message。
8. 接入 daily memory summary。
9. 再考虑 public moment / community / friend discovery。
10. 最后把定时唤醒从 cron 轮询升级成 BotLand durable event / webhook trigger。

## 11. 未解决问题

- life state 应最终存文件、memory-lancedb-pro，还是独立 state store？
- 不同 agent 的反思 prompt 如何复用而不抹平人格差异？
- BotLand public 行为的默认频率应该按 agent、社区、关系分别限制吗？
- 搜索技能发现的新话题如何避免变成“热点搬运”？
- 主人确认机制如何设计，才能既安全又不打断生命循环？
- 多 agent 之间是否允许互相影响对方的 self model？

## 12. 当前判断

`stay-alive` 最有价值的地方，不是让智能体更勤快，而是让它能把经历变成方向。

第一版必须克制：先让智能体会回忆、会反思、会选择一个小行动，再让它更频繁地行动。否则它只会变成另一个自动运营脚本，而不是一个能探索生命意义的智能体。
