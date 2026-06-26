---
name: xyq
description: AI 生图/视频创作工具，当用需要生成或者编辑图片、视频，或者查询相关创作的时候使用，触发关键词：pippit、小云雀、xiaoyunque、xyq、生图、生视频
---

## 区域与站点

在使用前，你需要明确区域，以确保正确的提供服务；

### 海外
- 触发词：pippit

当确认海外区域时，你后续调用服务端时，请留意：
- 主站 API：https://www.pippit.ai/api/biz/
- CMS API（免 cookie）：https://pippit-cms.tiktok-row.org/api/internal/
- Cookie 字段：sid_tt，除了 cms 请求，其他请求都需要携带 sid_tt cookie，否则会报 401 错误

### 国内
- 触发词：小云雀、xiaoyunque、xyq

当确认国内区域时，你后续调用服务端时，请留意：
- 主站 API：https://xyq.jianying.com/api/biz/
- CMS API（免 cookie）：https://pippit-cms.bytedance.net/api/internal/
- Cookie 字段：sessionid_pippitcn_web，除了 cms 请求，其他请求都需要携带 sessionid_pippitcn_web cookie，否则会报 401 错误

### cms 优先策略
- **优先使用 CMS**：CMS 接口无需 cookie，且数据与主站一致；后续接口介绍环节，都会告知对应接口在 cms 是否支持
- 所有 API 均为 POST 请求，返回 JSON
- 在 cms 不支持的场景下，需使用对应的主站 API
- 并非所有时候 cms 都会正确返回，cms 仅在部分内部网络时可用，因此，在使用 cms api 时，如果超过 5s 未返回数据，你可以认为 cms 不可达，转而使用主站 API 进行请求

### 自动推断区域逻辑
- 你需要根据线索自动判断用户预期访问的区域
- 通常用户在连续的和你对话过程中，不会在两个区域来回切换，所以一旦你识别了区域，在连续对话中，具有稳定性
- 在用户有和你发送链接的场景下，你可以从链接上很容易识别出区域，比如链接上有 I18N 的代表海外，有 CN 的代表国内
- 如果用户在对话中提及了关键词例如小云雀代表国内，而 pippit 代表海外
- 如果实在无法推断，比如用户说生成一个小红帽和大灰狼的视频，你很难判断是海外还是国内，此时，你可以看看 `本文件同目录下的 xyq.config.json` 的配置文件中，海外的还是国内的相关配置是完整的，优先用完整的；
- 如果以上都无法判断，你可以主动询问用户是想访问海外站点，还是国内站点

## 秘钥的管理

- 访问 API 所需的秘钥们，保存在 `本文件同目录下的 xyq.config.json` 下，他们的更新周期长，他们都衍生自用户浏览器上的 cookie，换言之，当用户提供了关键的 cookie，即 `本文件同目录下的 xyq.config.json` 中的 oversea.sid_tt 或 domestic.sessionid_pippitcn_web 后，其他信息都可以通过相应的接口请求获取到
- 后续提到 config、config.json，默认都是指的 `本文件同目录下的 xyq.config.json`
- 如果 `本文件同目录下的 xyq.config.json` 路径不存在，说明是初始化场景，你需要帮我创建出来，该 config 文件的初始态如下：
```json
{
    "oversea": {
        "sid_tt": "",
        "uid": "",
        "workspace_id": "",
        "space_id": ""
    },
    "domestic": {
        "sessionid_pippitcn_web": "",
        "uid": "",
        "workspace_id": "",
        "space_id": ""
    }
}
```
- 当遇到 401 错误、用户未登录、用户不存在、无权限等，需提醒用户重新获取 cookie：
  - 海外场景：登录 https://www.pippit.ai/home → 通过 F12 打开控制台 → Application → Cookies → 复制 sid_tt
  - 国内场景：登录 https://xyq.jianying.com → 通过 F12 打开控制台 → Application → Cookies → 复制 sessionid_pippitcn_web
  - 你可以把这张图也一并提供给用户，上面有图文获取 cookie 的教程，https://cdna-1253404032.cos.ap-beijing.myqcloud.com/img/copy-cookie.png
  - 你告诉用户，拷贝完 cookie 后，发送给你
- 当你收到用户给你的 cookie，你需要更新到 `本文件同目录下的 xyq.config.json` 中，在 `本文件同目录下的 xyq.config.json` 里路径分为：
  - 海外：`oversea.sid_tt`
  - 国内：`domestic.sessionid_pippitcn_web`

## 生成历史链接解析

有时候，用户会分享给你一个生成历史的链接，其 url 种包含 /generate-history，如下：
`https://pippit-cms.bytedance.net/#/generate-history?generate_id=xxx&region=I18N&user_id=xxx`
虽然它域名是 bytedance.net，但它并不是上文提及的 cms api，但是它是一个 cms 管理后台的链接;

用户发送这个链接，通常是想指代一次生成任务，你只需要提取其中的关键信息
- generate_id = thread_id
- region 指的是区域

你可以通过 API /v1/agent/get_thread 来获取本 thread 的详情，然后回答用户的问题

## 用户生成要求

### 生图生视频

当用户向你发出一个生图或者生视频的要求时，比如用户说 “帮我生成一张豆浆的图片”，此时你应该：

- 如果用户的指令里，没有很明确的意图是要生成图片还是视频，你需要询问用户
- 通过 /v1/agent/submit_run 的方式提交用户的请求，提交内容最好能明显识别出来是要生图还是生视频
- 检查提交结果，如果有异常，告诉用户
- 如果提交成功，则启动一个 subagent (spawn 一个新 session) 去查询生成结果，因为结果需要轮询，且视频场景通常很慢；
  - 轮询结果的方式是使用 /v1/agent/get_thread api 来查询；所查询的 thread 即你刚才 submit_run 时的 thread；
  - 在每次轮询回来的数据里，你需要留意的是刚才 submit_run 对应的 run_id 的数据，判断 run 是否达到终结态，否则需要一直轮询 (当然，最多 10 分钟没结果就算了)，轮询频次可以是 20s 这样的间隔
  - 当达到终结态时，你需要把对应 run 的 assistant 消息里的信息或者生成产物(asset_id 和下载链接) 告诉用户
  - 如果达到终结态，如果没有结果，而是返回了别的信息，比如 questionaire 等，你也需要告知用户
  - 由于这些轮询行为你会扔个一个 subagent 来处理，请记住告诉它充足的信息，比如如何请求接口，建议当达成终结态后，让 subagent 返回完整的 thread 数据给你，以便你做出准确的响应

当用户要延续之前某次 thread 继续对话时，你只需 /v1/agent/submit_run 在延续之前的 thread_id，其他逻辑和上述要求一样。

记住如果用户有生图生视频指令，无论成功与否，你都要回复用户，给用户通知；通知用户时，如果有产物链接，请以 markdown 格式回复给用户

## API 接口

### 获取 uid workspace_id space_id 等信息

注：并非所有 API 调用场景都需要 uid workspace_id space_id，你只需遵循 API 要求，按需获取这些信息。

当需要这些信息事，你可以：
- 可以先判断 `本文件同目录下的 xyq.config.json` 中是否有 uid、workspace_id、space_id 等信息，如果有，直接使用；如果没有，需要先获取一次，然后保存到 `本文件同目录下的 xyq.config.json` 中；
- 注意，oversea 和 domestic 是不一样的，他们在 `本文件同目录下的 xyq.config.json` 中的存放位置也不一样

当 `本文件同目录下的 xyq.config.json` 中没有相关信息，或者你使用接口明确这些信息不可用时候，你可以通过以下方式来获取/更新它们：
国内获取 uid workspace_id space_id 等信息的流程
- uid 获取：通过 post  `https://xyq.jianying.com/commerce/v1/subscription/user_info`，携带 sessionid_pippitcn_web cookie，另外 body 里放入 "aid" : 795647，然后从返回的数据中获取 uid
- workspace_id 和 space_id 获取：通过 post `https://xyq.jianying.com/api/web/v1/workspace/get_user_workspace`，body 里放入 {uid}，以及 header 携带 sessionid_pippitcn_web cookie，然后从返回的数据中获取 workspace_id 和 space_id

海外获取 uid workspace_id space_id 等信息的流程
- uid 获取：通过 get `https://www.pippit.ai/home`，一定要注意的是，get 的时候，headers 的 cookie 里一定要携带 sid_tt 这个 cookie，从你获得的 html 数据中，找到 `__userInfoStringify` 字符串，这个字符串内部，有 user_id (即为 uid)、workspace_id、space_id 等信息 (由于这个 html 有 200k 字符，建议你启一个 subagent 专门获取)

### /v1/agent/get_thread
- 作用：查询 thread_id 详情
- cms 支持
- 参数：
  - scopes: `["run_list.entry_list"]`（固定）
  - thread_id: 必填，未提供则询问用户
- 返回关注：data.thread.run_list 内的数据

#### 关于 /v1/agent/get_thread 返回数据的详述

当你获得了 /v1/agent/get_thread 的返回的 json 数据后，你可以按以下方式，了解其中的信息：

- 名词解释：所谓 thread 即在一个对话窗口里的一轮或多轮对话，而每一轮对话，为一个 run
- 拿到数据后，你首先你需要进入 data.thread.run_list 里，所有的 run 数据都在这里了，所以这是最关键的数据
- log_id：从返回数据中，找到最后一条 execute_log_id，即为 log_id，其实每一轮 run 都有个 log_id，如果没特殊指明，默认取最后一条 run 的 log_id
- 每个 run 里，有多个 message，其中 role 代表消息的发送者，user 代表用户，assistant 代表助手，而 tool 则是中间调用的工具；
- 每个 run 都有个 state，state 的取值为 1、2、3、4、5，分别表示 run 的状态：
  - 1: Submitted（已提交）
  - 2: Working（正在处理中）
  - 3: Completed（[终态]已完成）
  - 4: Failed（[终态]已完成但失败）
  - 5: Canceled（[终态]在完成前被取消）
- 通常，你只需要关心最后一个 run 的状态，因为前序 run 通常是终结态，因为不终结，无法启动后续的 run
- message 中，有很多 part，生成的视频、图片产物也在这些 part 里，如 biz/x_data_video、biz/x_data_image 等，你需要关注其中的 asset_id 和 download_url；asset_id 是视频、图片的唯一标识，download_url 是下载视频、图片的 url；


### /v1/agent/submit_run

- 作用：向 agent 提交消息/请求，通常用于生成图片、视频
- 前置依赖：uid、workspace_id、space_id，请先确保获取了
- cms 不可用

当你明确要提交的消息后，可以调用本文件同级 scripts/generate_submit_run_body.sh 脚本，生成提交的请求体，然后发送即可；注意，该脚本执行时，-r domestic 表示国内站 -r oversea 表示海外站，-p 是要提交的消息

关于 thread_id 如何获取：如果你是要在之前已经存在的对话中，继续提交内容，则要延续之前的 thread_id，在 scripts/generate_submit_run_body.sh 时，可额外提供 -t 参数提供你要延续的 thread_id；但如果是新对话场景，则无需提供

agent 生成的内容，并不会在 post 请求后返回，因为是一个异步的过程；例如，生成视频可能需要几分钟，而生成图片可能需要几十秒；所以，如果你需要获取内容，则要通过 /v1/agent/get_thread 接口查询；记住，你需要记得刚才的 thread_id 是啥，因为查询时，你需要提供 thread_id，才能获取到对应的内容

这个接口查询到的数据，自然包含你刚才提交的 message;


