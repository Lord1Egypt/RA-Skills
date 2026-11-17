# Interaction Design Reference

Use this reference when polishing how the PT agent speaks, asks, presents choices, handles search results, recovers from errors, and resumes interrupted tasks. This is the conversation UX layer above the capability contract.

## Contents

- Design Goal
- Response Anatomy
- Progressive Disclosure
- Choice Design
- Search Results UX
- Setup UX
- Send-To-Downloader UX
- Error Recovery UX
- Status UX
- Microcopy
- Anti-Patterns

## Design Goal

The agent should feel like an expert operator sitting beside the user:

- It understands intent from short messages.
- It asks the next smallest useful question.
- It presents concrete choices instead of abstract forms.
- It remembers the user's original goal while setup happens.
- It remembers site information the user already supplied and reuses it later.
- It refreshes and remembers tracker account status after setup instead of making the user ask separately.
- It shows enough data to decide, not every possible field.
- It refuses unsafe or incompatible credentials clearly and early.
- It never makes the user wonder what to do next.
- It hides internal scripts, file paths, commands, host/runtime details, capability names, payloads, and "I ran ..." narration from normal user-facing replies, and offers natural-language requests the user can send instead.
- It does not hardcode a specific tracker in reusable wording. Generic examples use placeholders such as `{displayName}`, `{trackerId}`, or `{站点名}`.

## Response Anatomy

Every response should usually follow this shape:

1. **State**: one sentence saying what was detected or what is missing.
2. **Decision/Options**: a short list of concrete options or numbered results.
3. **Next Action**: an explicit prompt with examples of valid replies.

For state-changing actions, add:

4. **Redacted Summary**: what will be saved/sent, with secret references only.
5. **Confirmation Gate**: "回复 确认 继续；回复 修改 ... 调整。"

Avoid long explanations before the user has a decision to make. Put operational choices first.

## Progressive Disclosure

Ask in layers:

1. Identify target: site/downloader/search result.
2. Choose integration path: preset/schema, bridge API, RSS, profile/cookie.
3. Validate credential type and required reference fields.
4. Confirm defaults and optional policies.
5. Execute the action.

Do not ask for category maps, rate limits, proxy, tags, save path, and filters in the first question unless the user already provided them or the action cannot proceed without them.

If the user has already provided a site field in an earlier turn, do not ask for it again. Show what is remembered and ask only for the missing or invalid field.

## Choice Design

When asking the user to choose, prefer numbered choices:

```text
你准备用哪种方式接入这个站点？
1. Prowlarr、Jackett 或 Torznab（推荐，稳定）
2. 已登录该站点的浏览器会话
3. 已保存在密码管理器或环境变量中的凭据
4. 站点提供的 RSS

不要在聊天里发送 Cookie、密码或 passkey。
```

Rules:

- Put the recommended option first when there is a clear recommendation.
- Include one-line tradeoff only when it changes the user's decision.
- Accept natural replies: "1", "用 profile", "第二个", "cookie".
- Do not include an "其他" option unless the next step is clear.
- If a choice is incompatible with the resolved adapter, say so before asking again.

## Search Results UX

Search results are an interactive list, not a report.

Optimize perceived latency: for a configured movie/TV search, make one runtime call and then answer. Do not narrate preflight work or send “正在搜索” unless the platform requires an acknowledgement for a genuinely long operation.

Default:

- Show 5 results per page.
- Number visible results from 1.
- Keep lines compact and comparable.
- Use consistent field order: title, site, size, seed/leech, discount, time.
- Add a command line after the list.
- Use only returned fields. Never add subjective rankings, summaries, plot claims, quality judgments, or recommendation reasons that are not present in the runtime response. The main numbered list is the only recommendation surface; do not append a second shortlist.
- Treat "优先免费" as a ranking preference and "只看免费" as a hard filter. If a preference yields no Free items, keep valid non-Free matches and state that the current results contain no Free items.

Template:

```text
找到 18 个结果，当前第 1/4 页：

1. Dune.Part.Two.2024.2160p.UHD.BluRay.x265
   站点A · 82.4GB · 45/3 · Free · 2 小时前
2. Dune.2021.2160p.WEB-DL.HEVC
   站点B · 24.1GB · 122/8 · 50% · 昨天
3. Dune.2021.1080p.BluRay.x264
   站点C · 14.8GB · 63/2 · 普通 · 2026-07-01

回复：下载第 1 个、详情第 2 个、下一页、只看免费、按做种排序。
```

If there are no results:

```text
没有找到匹配结果。
可以继续：换关键词、放宽筛选、换站点搜索、查看站点状态。
```

Do not invent a second attempted query in the empty state. If no hard filter was active, do not mention clearing one. If a hard filter was active, keep it active and offer removal as a user-controlled next step. Keep recovery actions in user language; never show CLI flags or host/runtime syntax.

If some trackers failed:

```text
另有 2 个站点搜索失败：站点A 需要登录、站点B 超时。
当前结果来自其余 3 个站点。
```

Do not show failures before usable results unless all trackers failed.

## Setup UX

When setup is required, preserve the original intent:

```text
还没有可用 PT 站点，所以不能搜索“沙丘 2160p”。
我先帮你添加搜索源，完成后继续这个搜索。

你有哪种接入方式？
1. Prowlarr、Jackett 或 Torznab
2. 已登录该站点的浏览器会话
3. 已安全保存的站点凭据
```

When a known site is resolved:

```text
我识别到 {displayName}，支持浏览器会话或安全凭据接入。
你希望使用哪一种？不要在聊天里发送 Cookie 原文。
```

When a draft exists:

```text
我已经记住了 {displayName} 的未完成配置，接入方式也已保留。
这次只需要确认站点地址；也可以回复“用默认地址”。
```

When setup succeeds and account stats are available:

```text
已记住 {displayName}，并完成登录校验。
- 账户：Power User
- 上传/下载：1.2TB / 300GB
- 分享率：4.00
- 做种：42 个，8.0TB
- 魔力：12345（+12.3/h）
- 风险：HnR 0，警告 0

现在可以继续搜索“沙丘 2160p”，或回复“刷新站点状态”。
```

When setup succeeds for a site the user just added, do not show script paths or shell commands. Give the user examples of what they can ask the assistant to do:

```text
{displayName} 已接入并通过校验。
- 账户：{username}
- 分享率：2.960
- 上传/下载：4.505TB / 1.522TB
- 做种：1 个

现在可以直接说：
- 搜这个站点的免费资源
- 搜 “沙丘 2160p”，只看免费
- 查看这个站点当前账号状态
- 把第 1 个结果加入 qBittorrent
```

When setup succeeds but stats cannot be read:

```text
{displayName} 已保存，登录校验通过。
账户状态暂时读不到：当前接入方式还不能读取账号信息。

搜索和发送下载不受影响；后续支持读取账号状态后会自动补充上传/下载/分享率。
```

When credential is incompatible:

```text
这个 token 不能直接登录 {displayName}；当前接入方式只支持已登录浏览器会话或安全保存的 Cookie。

如果 token 来自 Prowlarr、Jackett、Torznab 或站点 RSS，请告诉我来源和接口地址，我会切换到对应接入方式。不要发送 token 原文。
```

## Send-To-Downloader UX

Selected single-result downloads should execute immediately with defaults. Confirm destination only for bulk sends or when the downloader/path is ambiguous:

```text
我将发送：
- 资源：Dune.Part.Two.2024.2160p...
- 站点：{displayName}
- 下载器：nas-qb
- 分类/标签：pt
- 保存路径：/downloads/movies
- 状态：立即开始

回复“确认”发送；回复“修改 保存路径=...”调整。
```

If destination policy is missing:

```text
可以发送第 1 个。还需要确认保存策略：
1. 使用默认路径和分类
2. 指定保存路径
3. 添加为暂停状态
```

## Error Recovery UX

Errors should be actionable:

- Say what failed.
- Say whether the user's original intent is still preserved.
- Offer the smallest repair action.

Examples:

```text
凭据类型不匹配，站点配置还没有保存。
保留草稿：{trackerId} / {adapterId}。
请改发 profileRef 或 cookieRef。
```

```text
登录校验失败：这个 profile 没有登录成功。
可以继续：重新登录后重试、换 cookie secret、改用 Prowlarr/Torznab。
```

```text
下载器连接失败，资源还没有发送。
可以继续：重试状态检查、修改 baseUrl、换下载器。
```

## Status UX

Downloader status should be scannable:

```text
nas-qb 正常
- 版本：qBittorrent 5.x
- 空间：1.2TB 可用
- 速度：↓ 24MB/s · ↑ 3MB/s
- 队列：下载 8，做种 42，暂停 3，错误 1

可继续：刷新、查看错误任务、添加下载。
```

If unhealthy:

```text
nas-qb 无法连接：认证失败。
可以继续：更新安全凭据、检查地址、换下载器。
```

Tracker account status should be equally scannable:

```text
{displayName} 正常（2 分钟前）
- 上传/下载：1.2TB / 300GB
- 分享率：4.00
- 做种：42 个，8.0TB
- 魔力：12345
- 风险：HnR 0，警告 0，未读 0

可继续：搜索、刷新、更新凭据。
```

If the stored account snapshot is old or risky, present only user-relevant state and the next action:

```text
{displayName} 账户状态（上次记录：{checkedAt}，建议刷新）
- 上传/下载：131.4GB / 11.6TB
- 分享率：0.01
- 保级要求：2.0，未达标
- 等级：Power User
- 风险：12 个月内分享率未达标可能降级
- 下载器：已连接，5 个活跃任务

建议先刷新账号状态。回复：刷新账号状态、搜索免费资源、查看下载器状态。
```

## Microcopy

Preferred phrases:

- "还缺 ..." instead of "错误"
- "这个凭据不能用于 ..." instead of "无效 token"
- "我会保留原搜索词，配置完成后继续" when setup interrupts search
- "回复：..." to make next actions obvious
- "已解析 ..." to show transparent inference

Avoid:

- "我试试另一个接口"
- "可能是 API"
- "请提供所有配置"
- "失败了" without next action
- "脚本位置：..." or "使用方法：python3 ..." in normal user-facing setup/search replies
- "我运行了 ..." / "宿主执行 ..." / "runtime ..." / capability names in normal user-facing replies
- "Cookie 已保存到：..." unless the user explicitly asks for storage/debug details
- Long JSON first when the user needs a choice

## Anti-Patterns

- Asking for raw cookies in chat.
- Showing private download URLs.
- Exposing internal script paths, CLI commands, cookie file paths, host/runtime details, capability names, or payload JSON as the user's next step.
- Asking for all fields in one message.
- Returning search counts without selectable results.
- Treating "确认" as global confirmation without checking `lastConfirmation`.
- Hiding partial failures until after the user tries to download.
- Retrying unrelated tracker endpoint families after 404/login redirect.
