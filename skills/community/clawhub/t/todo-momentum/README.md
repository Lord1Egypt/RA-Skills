# Todo Momentum - 3 分钟启动器

把拖延待办、卡住任务、模糊目标、家务、项目和习惯拆成下一步物理动作、3 分钟启动、5 分钟扩展、今日算赢标准和断了以后的回归脚本。

## Best Triggers

- 我有一堆待办，不知道先做哪个。
- 这个任务拖了很久，帮我启动。
- 把这个项目拆成今天能做的一小步。
- 我最近断了，怎么重新回来？
- I am overwhelmed by my todo list.
- Give me a 3-minute start for this task.

## What It Produces

- A single main line for today.
- Tiny physical next actions instead of vague intentions.
- 3-minute and 5-minute starts.
- A low-friction trigger: after what existing event to start.
- A done-for-today standard so progress is visible.
- A shame-free recovery script when the plan breaks.

## Fast Modes

| Mode | Best For |
|---|---|
| `todo_list_rescue` | 一堆杂乱待办，先找今天主线 |
| `three_minute_start` | 一个卡住任务，需要马上启动 |
| `daily_momentum_plan` | 做今天的轻量执行方案 |
| `fallen_off_recovery` | 断了、失败了、没坚持后的回归 |
| `procrastination_debug` | 反复拖延，找阻塞并降摩擦 |

## Example

```text
我拖了两周没写项目说明，越拖越抗拒。帮我用 3 分钟启动。
```

Expected shape:

```text
今天先不追求完整，只追求启动。

今日主线：让项目说明有一个丑稿入口
下一步物理动作：打开文档，写下 5 个小标题
3 分钟启动：只写标题，不写正文
今天做到什么算赢：文档里出现 5 个标题和 1 句最粗糙的项目目标
如果卡住：把标题改成问题句，比如“这个项目解决什么？”
```

## Version

`0.2.0` sharpens the skill around 3-minute starts, anti-procrastination search terms, fast modes, README examples, and UI metadata.
