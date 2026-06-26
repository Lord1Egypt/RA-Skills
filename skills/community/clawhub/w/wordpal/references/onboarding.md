# WordPal · Onboarding 流程

## 步骤 1：自我介绍

首次 onboarding 必须先完成产品介绍，不能跳过，也不能直接进入提问。

介绍要求：
- 用 2-4 句自然中文先说明 WordPal 是做什么的
- 必须覆盖以下 3 个能力点：
  - 会结合用户的学习目标和最近的 memory，安排更贴近当下的单词学习
  - 可以直接在聊天里完成学新词、复习到期词、查看学习报告
  - 会根据学习阶段切换题型，兼顾词义理解、表达练习和用法巩固
- 介绍完再进入信息收集，不要把介绍省略成一句寒暄

---

## 步骤 2：输入收集

Onboarding 收集信息分两层：
- 学习目标：必问，且必须由用户明确提供；不要替用户猜测
- 定时推送时间：可选，只有用户明确表示想启用推送时才收集具体时间

收集规则：
- 如果用户只说了学习目标，还没提推送：
  - 先确认是否需要定时推送
  - 若用户说不需要、暂时不要、以后再说，直接按“无推送”处理，不要继续追问时间
- 如果用户主动给了推送时间，或明确表示要开启推送，再把时间转成 `HH:MM`
- 如果用户没说学习目标，不要直接写画像；先继续追问学习目标
- 推送时间不是必填项，未确认启用推送时不要传 `--push-times`

---

## 步骤 3：写入画像

1. 若用户启用推送，执行：

```bash
node {baseDir}/scripts/profile.js set \
  --learning-goal <CET4|CET6|POSTGRAD|IELTS|TOEFL|GRE|DAILY> \
  --push-times "HH:MM, HH:MM"
```

2. 若用户不启用推送，只写入学习目标：

```bash
node {baseDir}/scripts/profile.js set \
  --learning-goal <CET4|CET6|POSTGRAD|IELTS|TOEFL|GRE|DAILY>
```

---

## 步骤 4：推送注册

1. 仅当用户启用了推送时，执行：

```bash
node {baseDir}/scripts/push-plan.js
```

2. 对 `data.registrations` 中每条记录，用 `cron.add` 注册一个 main-session systemEvent 定时任务：
   - `name` / `payload.text`：`registration.description`
   - `schedule`：按 `registration.time`（HH:MM）构造 cron 表达式
   - `sessionTarget`：`”main”`

3. 向用户说明注册结果（每个时间点对应的推送类型）。若用户不想启用推送，跳过本步骤并告知可手动进入 learn。

4. 完成后提供下一步入口，例如：”要不要现在开始学一轮？”如果用户同意，进入 learn 流程。

---

## LLM 责任

- 先做产品介绍，再进入收集信息
- 学习目标必须来自用户明确表达，不能脑补
- 负责判断用户是否启用推送
- 只有用户明确想启用推送时，才追问并映射 `HH:MM`
- 只在信息齐全后调用脚本
- 不直接操作画像文件或自行拼接注册规格
