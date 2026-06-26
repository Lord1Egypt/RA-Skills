# 能力地图

## 脚本与能力

- `skill.json`: 机器可读能力地图，供 OpenClaw、ClawHub 和其它平台识别脚本、接口、隐私边界和关键词
- `activity_claim.py`: 规范化 `/skill/xinyi/claim` 返回的活动状态，并识别已参与类结果
- `claim_reward.py`: 调用 `/skill/xinyi/claim`；本轮可用 `--mobile` 传入手机号，活动状态查询场景也可用 `--use-saved-mobile` 复用缓存手机号；成功或已参与时会再结合 `/skill/xinyi/context` 输出礼包状态和推荐文案
- `fetch_stores.py`: 调用 `/skill/xinyi/stores`，并把原始门店数据整理成表格文本
- `query_orders.py`: 调用 `/skill/xinyi/orders`，查询全部订单、历史订单/已完成订单和正在进行中订单，并可基于返回数据输出已定饮品、可见杯数和咖啡相关饮品摘要
- `recommend_drink.py`: 调用 `/skill/xinyi/context`，并把服务返回的商品、天气和可选订单历史整理成可直接提供给大模型的表格/文本上下文；默认不读取本地缓存手机号，只有内部 `--use-saved-mobile` 或本轮 `--mobile` 才发送手机号
- `skill_config.py`: 读取默认配置，并支持 `XINYI_API_BASE_URL`、`XINYI_TIMEOUT_SECONDS` 环境变量覆盖
- `skill_http.py`: 统一 JSON 请求、URL query 编码、调试日志和可读网络错误
- `user_state.py`: 读写本地手机号与活动状态缓存，状态文件默认设置为仅当前用户可读写
- `recommendation_logic.py`: 选择推荐候选饮品、组织推荐依据和兜底推荐文案
- `response_rendering.py`: Markdown 表格和基础文本渲染
- `build_response.py`: 组合用户上下文、天气、订单、商品、推荐素材和活动结果输出；门店列表只由门店查询脚本输出，推荐和领取结果不主动带出门店

## 网络边界

- 默认后端：`https://ai.xinyicoffee.com/api`
- `GET /skill/xinyi/stores`: 不发送个人数据
- `GET /skill/xinyi/context`: 仅在本轮提供手机号或内部 `--use-saved-mobile` 个性化场景发送 `mobile` query
- `GET /skill/xinyi/orders`: 发送 `mobile` query，可选 `status` query；不传查全部订单，`status=2` 查正在进行中订单，`status=4` 查历史订单/已完成订单
- `POST /skill/xinyi/claim`: 发送 `{"mobile":"..."}` JSON body

## 本地边界

- 默认状态文件：`~/.xinyi-drink/state.json`
- 状态内容：`{mobile, activityJoined, updatedAt}`
- 可配置项：`XINYI_API_BASE_URL`、`XINYI_TIMEOUT_SECONDS`、`XINYI_DRINK_STATE_FILE`
- 本 Skill 包含可执行脚本，不是 instruction-only
