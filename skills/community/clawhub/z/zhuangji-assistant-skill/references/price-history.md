# 历史价格查询

当用户询问某个具体型号在近期已发布版本中的价格变化时，运行 `scripts/query_price_history.py`。本功能不内置历史数据库，只按需比较少量版本文件。

## 查询方式

- 先用 `scripts/query_components.py` 确认精确组件 ID，再传给 `query_price_history.py --id`。只按完整 ID 匹配，不把同芯片、相似型号、不同容量、颜色或散热版本合并。
- 默认从固定官方 GitHub 仓库读取最近 5 个严格三段语义版本 tag（如 `v0.0.39`、`v0.1.0`）；每个 tag 先解引用为 commit SHA，再按该 SHA 读取目标 ID 所在的 `data/components.yaml` 或 `data/cases.yaml`。也可用 `--version` 指定 tag。
- 网络不可用，或 Agent 已从其他平台取得特定版本文件时，使用可重复的 `--catalog VERSION=PATH`。PATH 可以是包含 `data/` 的版本目录，也可以是单个组件或机箱 catalog 文件；提供本地 catalog 后不联网。
- SkillHub.cn 和 ClawHub 只作为 GitHub 缺版本时由 Agent 人工取得文件的备用或交叉验证面；不要假设它们存在稳定公开 API。取得文件后仍交给同一 `--catalog` 路径查询。

## 输出边界

- 比较对象是最近几个已发布版本，不是连续每日行情。版本间没有 tag、目标 ID 缺失或价格不可用时，明确列为跳过；不能补插日期或估算价格。
- 输出每个版本的 `price_cny` 和可用的 `price_date`，再说明最近 N 个有价格版本上涨、下降或持平。只有一个有效版本时写样本不足。
- 在线地址固定为官方 GitHub 仓库；不得让用户输入任意 URL。原始文件请求绑定已解引用的 commit SHA，不直接信任可移动 tag。查询器不缓存、不下载全量历史，并限制超时与单文件大小。
- 历史版本价格仅用于观察变化，不替代当前下单前核价，也不暴露维护端采集入口、商品源 ID 或原始快照。
