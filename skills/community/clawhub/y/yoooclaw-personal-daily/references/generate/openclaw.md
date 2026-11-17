# OpenClaw 日报生成

仅在 `runtime=openclaw` 且当前任务是生成日报时读取本文件。

## 关注配置

读取：

```text
~/.openclaw/个性化日报/interests.md
```

配置不存在、不可读或解析后为空时，将“未取得有效话题”返回主流程处理。

## 选择联网能力

1. 读取当前已安装 Skill 列表。列表包含 `byted-web-search` 时，检查该 Skill 的搜索能力是否可调用且状态为可用；状态无法直接确认时，用它提交一次查询 `OpenAI`、最多返回 1 条结果的探测。返回可解析响应时，设置 `acquisition=search`、`search_tool=byted-web-search` 和 `search_failure_message=当前 OpenClaw 缺少可用的 byted-web-search，个性化日报未运行`，然后停止选择。状态不可用、能力不可调用或探测失败时继续下一步，不修复或重新安装该 Skill。列表不包含它时直接继续，不尝试安装。
2. 检查当前 Agent 的 `web_search` 是否可调用且状态为可用；状态无法直接确认时，同样提交一次查询 `OpenAI`、最多返回 1 条结果的探测。返回可解析响应时，设置 `acquisition=search`、`search_tool=web_search` 和 `search_failure_message=当前 OpenClaw 缺少可用的 web_search，个性化日报未运行`，然后停止选择。
3. 前两种能力均不可用时，设置 `acquisition=rss`，不设置 `search_tool` 或 `search_failure_message`。

探测失败包括鉴权、配置、网络和响应解析错误。丢弃探测结果，不把它作为日报候选；探测查询计入 15 次查询提交总预算。不要读取、打印或转述任何凭据原值。不要安装、升级、启用或配置联网 Skill 或工具；业务查询开始后不切换获取方式。

搜索方式支持日期、时效或结果数量参数时，将范围限制到宿主时区当天，并将单次结果限制为 5 条。

**完成条件：** `acquisition` 已且仅已取 `search` 或 `rss` 中的一个值；搜索方式设置唯一的 `search_tool` 和 `search_failure_message`，RSS 方式不设置这两个值。候选获取由任务路由选择的 acquisition reference 负责。
