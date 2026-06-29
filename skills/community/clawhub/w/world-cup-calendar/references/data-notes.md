# 赛程数据说明

`fwc2026-schedule.json` 包含 2026 FIFA 世界杯 104 场比赛。

数据来源：
- FIFA 官方赛程 PDF
- URL: https://digitalhub.fifa.com/m/1be9ce37eb98fcc5/original/FWC26-Match-Schedule_English.pdf
- PDF 标注：All times are Eastern Time (ET), Subject to change.
- 本地抽取日期：2026-06-19

字段说明：
- `id`: 稳定比赛 ID，例如 `FWC2026-019`。
- `match_number`: FIFA 比赛编号。
- `stage`: 中文阶段。
- `group`: 小组赛组别；淘汰赛为空。
- `home` / `away`: 球队代码或淘汰赛占位。
- `home_zh` / `away_zh`: 中文展示名。
- `start_bj` / `end_bj`: 北京时间，固定 `Asia/Shanghai`。
- `date_et` / `time_et`: FIFA PDF 中的原始 Eastern Time。
- `city_zh` / `city`: 比赛城市。

注意：
- 淘汰赛真实对阵需要小组赛结束后更新。
- 如果 FIFA 更新赛程，应以官方页面或官方 PDF 为准。
