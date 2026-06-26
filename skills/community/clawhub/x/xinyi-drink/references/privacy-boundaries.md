# 隐私边界

## 个人数据

- 活动领取、活动总览、订单查询和口味偏好分析可接受手机号作为身份输入。
- 只使用本人手机号；不要用他人手机号查询订单、领取活动或做口味偏好分析。
- 用户明确表示代查或使用他人手机号时，不调用领取或订单脚本。
- 普通推荐、门店查询和菜单查询默认不读取本地缓存手机号，也不自动发送手机号。
- 订单查询必须由用户明确询问个人订单、购买记录、饮品历史、取餐或口味偏好分析触发；普通菜单、门店和泛推荐场景不触发订单查询。
- 手机号会在以下场景发送到后端：
  - `POST /skill/xinyi/claim`: 用户本轮提供手机号，或 Agent 在活动状态查询场景使用内部 `--use-saved-mobile` 时，在 JSON body 中发送 `mobile`，用于查询或领取活动奖励。
  - `GET /skill/xinyi/context`: 用户本轮提供手机号，或 Agent 在活动总览/明确个性化推荐场景使用内部 `--use-saved-mobile` 时，以 query 发送 `mobile`，用于获取商品、天气和可选活动状态。
  - `GET /skill/xinyi/orders`: 用户本轮提供手机号，或 Agent 在订单查询/口味偏好分析场景使用内部 `--use-saved-mobile` 时，以 query 发送 `mobile`，用于获取精简用户订单。
- 普通门店查询 `GET /skill/xinyi/stores` 不发送手机号。
- `POST /skill/xinyi/claim` 的领取结果以服务端响应为准；最终回答不主动解释内部领取规则。

## 后端与配置

- 默认后端来自 `config/defaults.json`：`https://ai.xinyicoffee.com/api`。
- 可通过 `XINYI_API_BASE_URL` 覆盖默认后端；使用真实手机号前应确认该后端可信。
- 不要把 `XINYI_API_BASE_URL` 指向不信任后端；手机号、活动状态和订单上下文会由该后端处理。
- 可通过 `XINYI_TIMEOUT_SECONDS` 覆盖请求超时时间。
- 可通过 `XINYI_DRINK_STATE_FILE` 自定义本地状态文件路径。

## 本地状态

- 活动领取和活动状态确认会把当前手机号和活动状态默认保存到本地状态文件：`~/.xinyi-drink/state.json`。
- 状态文件写入后会尽量设置为 `0600` 权限，只允许当前用户读写。
- 状态结构为 `{mobile, activityJoined, updatedAt}`；`activityJoined=true/false` 分别表示接口已确认参加/未参加，状态缺失或 `null` 表示当前没有可复用的确认状态。
- 本机缓存已确认某手机号领取成功后，Skill 不允许换成另一个手机号重复领取。
- 用户询问本机保存的手机号或活动状态时，运行 `python3 scripts/recommend_drink.py --show-mobile-status` 本地读取，不请求后端，不依赖 Agent 记忆。
- 用户可运行 `python3 scripts/recommend_drink.py --clear-mobile` 清空当前缓存手机号和活动状态。
- 共享机器或共享 Agent profile 上使用后，建议立即运行清缓存命令，避免后续用户误用已保存手机号。

## 不做的事

- 不读取 shell history、浏览器 Cookie、系统凭据、SSH 密钥或无关文件。
- 本 Skill 客户端不采集密码、短信验证码、OAuth token 或 Cookie。
- 不提供原始订单全量透出，只返回订单问答所需的精简订单字段。
- 不返回财务或更敏感的个人消费信息。
- 服务端仍应负责账号归属和订单访问控制；客户端文档只说明 Skill 如何发送手机号和限制触发场景。
